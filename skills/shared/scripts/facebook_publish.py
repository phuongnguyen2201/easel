#!/usr/bin/env python3
"""facebook_publish.py — adapter đăng Trang Facebook qua Meta Graph API.

Thiết kế: agent_docs/adapter-facebook-page.md.

Đăng nhập dùng Facebook Login for Devices (không cần callback URL): runner xin
mã thiết bị, vẽ QR bằng segno vào outputs/_login/facebook-page.png, ghi trạng
thái theo login_state.py (starting → qr_ready → verifying → success | expired
| error), rồi đổi token người dùng lấy Page token.

Subcommand:
  login    --qr-out --status-file --timeout --scope --page-id --token
  whoami   [--page-id]                         # dòng JSON cuối: {loggedIn,name,avatar[,error]}
  pages    [--set-default ID]                  # liệt kê Trang trong token file (không in token)
  publish  --title --content --tags --images a,b | --video v --link --page-id --topic
           [--exec] [--allow-unsafe] [--offline]

Không có --exec = dry-run: content_guard chỉ cảnh báo, không gửi request ghi.
Mã thoát: 0 ok · 1 lỗi khác · 2 argparse · 3 chưa đăng nhập / token hỏng / mã hết hạn
· 4 thiếu quyền · 5 đầu vào sai · 6 bị giới hạn tần suất · 7 content_guard chặn.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import calendar_ops  # noqa: E402
import content_guard  # noqa: E402
from login_state import write_status  # noqa: E402

PLATFORM = "facebook-page"
SKILL_NAME = "skill-facebook-page-upload"
DEFAULT_GRAPH_VERSION = "v23.0"   # ghim phiên bản; đổi bằng FB_GRAPH_VERSION
GRAPH_HOST = "https://graph.facebook.com"
GRAPH_VIDEO_HOST = "https://graph-video.facebook.com"
DEFAULT_TOKEN_FILE = Path.home() / ".easel-browser-profiles" / "FacebookPageProfile" / "token.json"
DEFAULT_QR_OUT = f"outputs/_login/{PLATFORM}.png"
DEFAULT_SCOPE = "pages_show_list,pages_manage_posts,pages_read_engagement"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".webm"}

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_AUTH = 3
EXIT_PERMISSION = 4
EXIT_INPUT = 5
EXIT_RATE_LIMIT = 6
EXIT_GUARD = content_guard.EXIT_LEAK   # 7

# Subcode của device/login_status (tài liệu Meta "Facebook Login for Devices").
DEVICE_PENDING = 1349174
DEVICE_SLOW_DOWN = 1349172
DEVICE_EXPIRED = 1349152

REQUEST_TIMEOUT = 60
VIDEO_TIMEOUT = 540

_PLACEHOLDER_RE = re.compile(r"replace_me|your[-_]?api[-_]?key|xxx|^\.{3}$|^<.*>$", re.I)


class InputError(ValueError):
    """Đầu vào CLI không hợp lệ (exit 5)."""


class GraphError(Exception):
    """Lỗi trả về từ Graph API hoặc mạng."""

    def __init__(self, message: str, code: int | None = None, subcode: int | None = None,
                 fbtrace_id: str = "", http_status: int | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.subcode = subcode
        self.fbtrace_id = fbtrace_id
        self.http_status = http_status


# ── Hàm thuần (có unit test) ────────────────────────────────────────────────
def mask(value: str) -> str:
    v = (value or "").strip()
    if len(v) <= 8:
        return "***"
    return f"{v[:4]}***{v[-2:]}"


def format_tags(tags: str | None) -> str:
    """'AI, giáo dục,#AI' → '#AI #giáodục' (bỏ trùng, giữ thứ tự, giữ chữ có dấu)."""
    if not tags:
        return ""
    seen: set[str] = set()
    out: list[str] = []
    for raw in re.split(r"[,，;\n]", tags):
        tag = re.sub(r"[^\w]", "", raw.strip().lstrip("#"))
        if tag and tag.casefold() not in seen:
            seen.add(tag.casefold())
            out.append(f"#{tag}")
    return " ".join(out)


def build_message(title: str | None, content: str | None, tags: str | None = None) -> str:
    """Ghép message cho bài chữ/ảnh: tiêu đề làm dòng đầu (trừ khi nội dung đã mở đầu bằng nó)."""
    title = (title or "").strip()
    content = (content or "").strip()
    parts: list[str] = []
    if title and not content.startswith(title):
        parts.append(title)
    if content:
        parts.append(content)
    tag_line = format_tags(tags)
    if tag_line:
        parts.append(tag_line)
    return "\n\n".join(parts)


def build_video_description(content: str | None, tags: str | None = None) -> str:
    return "\n\n".join(p for p in ((content or "").strip(), format_tags(tags)) if p)


def classify_media(images: str | None, video: str | None, link: str | None = None) -> tuple[str, list[Path]]:
    """Trả (kind, files) với kind ∈ text | photo | album | video."""
    image_list = [s.strip() for s in (images or "").split(",") if s.strip()]
    if image_list and video:
        raise InputError("Không thể đăng đồng thời ảnh và video, vui lòng chọn một")
    if link and (image_list or video):
        raise InputError("--link chỉ dùng cho bài chữ (không kèm ảnh/video)")
    if video:
        path = Path(video).expanduser()
        if path.suffix.lower() not in VIDEO_EXTS:
            raise InputError(f"Định dạng video không hỗ trợ: {path.name}")
        if not path.is_file():
            raise InputError(f"Không tìm thấy tệp video: {video}")
        return "video", [path]
    files: list[Path] = []
    for item in image_list:
        path = Path(item).expanduser()
        if path.suffix.lower() not in IMAGE_EXTS:
            raise InputError(f"Định dạng ảnh không hỗ trợ: {path.name}")
        if not path.is_file():
            raise InputError(f"Không tìm thấy tệp ảnh: {item}")
        files.append(path)
    if not files:
        return "text", []
    return ("photo" if len(files) == 1 else "album"), files


def plan_requests(kind: str, page_id: str, files: list[Path], link: str | None = None) -> list[dict]:
    """Mô tả các request sẽ gửi (dùng cho dry-run và làm khung cho --exec)."""
    if kind == "text":
        fields = ["message"] + (["link"] if link else [])
        return [{"method": "POST", "path": f"{page_id}/feed", "fields": fields}]
    if kind == "photo":
        return [{"method": "POST", "path": f"{page_id}/photos", "fields": ["source", "message"],
                 "file": files[0].name}]
    if kind == "album":
        steps = [{"method": "POST", "path": f"{page_id}/photos", "fields": ["source", "published=false"],
                  "file": f.name} for f in files]
        steps.append({"method": "POST", "path": f"{page_id}/feed", "fields": ["message", "attached_media"]})
        return steps
    if kind == "video":
        return [{"method": "POST", "path": f"{page_id}/videos", "host": "graph-video",
                 "fields": ["source", "title", "description"], "file": files[0].name}]
    raise InputError(f"Loại bài không xác định: {kind}")


def post_url(kind: str, page_id: str, result: dict) -> str:
    if kind == "video":
        vid = result.get("id", "")
        return f"https://www.facebook.com/{page_id}/videos/{vid}" if vid else ""
    post_id = result.get("post_id") or result.get("id") or ""
    return f"https://www.facebook.com/{post_id}" if post_id else ""


def exit_code_for(err: GraphError) -> int:
    code = err.code
    if code == 190 or code == 102:
        return EXIT_AUTH
    if code == 10 or (code is not None and 200 <= code < 300):
        return EXIT_PERMISSION
    if code in (4, 17, 32, 341, 613):
        return EXIT_RATE_LIMIT
    return EXIT_ERROR


def classify_device_poll(err: GraphError | None) -> str:
    """Kết quả một lần poll device/login_status: ok | pending | slow_down | expired | error."""
    if err is None:
        return "ok"
    if err.subcode == DEVICE_PENDING:
        return "pending"
    if err.subcode == DEVICE_SLOW_DOWN:
        return "slow_down"
    if err.subcode == DEVICE_EXPIRED:
        return "expired"
    return "error"


def select_page(pages: list[dict], wanted: str | None, default: str | None = None) -> dict | None:
    if not pages:
        return None
    for pid in (wanted, default):
        if pid:
            for page in pages:
                if str(page.get("id")) == str(pid):
                    return page
            if pid == wanted:
                return None   # người dùng chỉ định rõ nhưng không có trong token
    return pages[0]


def verification_target(verification_uri: str, user_code: str) -> str:
    sep = "&" if "?" in verification_uri else "?"
    return f"{verification_uri}{sep}{urllib.parse.urlencode({'user_code': user_code})}"


# ── Cấu hình / token file ───────────────────────────────────────────────────
def load_env() -> dict[str, str]:
    try:
        from model_registry import read_env_file
        env = read_env_file()
    except Exception:   # noqa: BLE001 — thiếu model_registry vẫn đọc được process env
        env = dict(os.environ)
    return {k: v for k, v in env.items() if v and not _PLACEHOLDER_RE.search(v)}


def graph_version(arg: str | None, env: dict[str, str]) -> str:
    return (arg or env.get("FB_GRAPH_VERSION") or DEFAULT_GRAPH_VERSION).strip()


def load_token_file(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or not data.get("pages"):
        return None
    return data


def save_token_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path.parent, 0o700)
    except OSError:
        pass
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ── HTTP ────────────────────────────────────────────────────────────────────
def build_opener(no_proxy: bool) -> urllib.request.OpenerDirector:
    if no_proxy:
        return urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return urllib.request.build_opener()


def _multipart(fields: dict[str, str], files: dict[str, Path]) -> tuple[bytes, str]:
    boundary = f"----easel{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n".encode())
        chunks.append(str(value).encode("utf-8") + b"\r\n")
    for name, path in files.items():
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.append((f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; "
                       f"filename=\"{path.name}\"\r\nContent-Type: {ctype}\r\n\r\n").encode())
        chunks.append(path.read_bytes() + b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


class Graph:
    def __init__(self, version: str, opener: urllib.request.OpenerDirector):
        self.version = version
        self.opener = opener

    def call(self, method: str, path: str, params: dict | None = None,
             files: dict[str, Path] | None = None, host: str = GRAPH_HOST,
             timeout: int = REQUEST_TIMEOUT) -> dict:
        params = {k: v for k, v in (params or {}).items() if v is not None}
        url = f"{host}/{self.version}/{path.lstrip('/')}"
        data = None
        headers = {"User-Agent": "easel-facebook-publish"}
        if method == "GET":
            if params:
                url = f"{url}?{urllib.parse.urlencode(params)}"
        elif files:
            data, headers["Content-Type"] = _multipart(params, files)
        else:
            data = urllib.parse.urlencode(params).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with self.opener.open(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            raise _graph_error(body, exc.code) from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise GraphError(f"Lỗi mạng khi gọi Graph API: {exc}") from None
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            raise GraphError("Graph API trả về dữ liệu không phải JSON") from None
        if isinstance(payload, dict) and "error" in payload:
            raise _graph_error(body, None)
        return payload


def _graph_error(body: str, http_status: int | None) -> GraphError:
    try:
        err = json.loads(body).get("error", {})
    except (json.JSONDecodeError, AttributeError):
        err = {}
    return GraphError(
        err.get("error_user_msg") or err.get("message") or f"HTTP {http_status}",
        code=err.get("code"), subcode=err.get("error_subcode"),
        fbtrace_id=err.get("fbtrace_id", ""), http_status=http_status,
    )


def _emit(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False))


def _report_graph_error(err: GraphError) -> None:
    trace = f" (fbtrace_id={err.fbtrace_id})" if err.fbtrace_id else ""
    print(f"❌ Graph API: {err.message} [code={err.code}, subcode={err.subcode}]{trace}", file=sys.stderr)


def fetch_pages(graph: Graph, user_token: str) -> list[dict]:
    pages: list[dict] = []
    params = {"access_token": user_token, "fields": "id,name,access_token,picture{url}", "limit": 100}
    resp = graph.call("GET", "me/accounts", params)
    for item in resp.get("data", []):
        if not item.get("access_token"):
            continue
        pages.append({
            "id": str(item.get("id")),
            "name": item.get("name", ""),
            "token": item["access_token"],
            "picture": ((item.get("picture") or {}).get("data") or {}).get("url", ""),
        })
    return pages


def _public_pages(pages: list[dict]) -> list[dict]:
    return [{"id": p["id"], "name": p.get("name", "")} for p in pages]


# ── login ───────────────────────────────────────────────────────────────────
def render_qr(target: str, qr_path: Path) -> None:
    try:
        import segno
    except ImportError as exc:
        raise InputError("Thiếu thư viện segno: pip install 'segno>=1.6,<2'") from exc
    qr_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = qr_path.with_name(qr_path.stem + ".tmp.png")
    segno.make(target, error="m").save(str(tmp), kind="png", scale=8, border=2)
    os.replace(tmp, qr_path)


def _device_flow(a, graph: Graph, env: dict[str, str], status: str | None) -> tuple[str, int | None] | int:
    app_id = env.get("FB_APP_ID", "").strip()
    client_token = env.get("FB_CLIENT_TOKEN", "").strip()
    if not app_id or not client_token:
        msg = "Thiếu FB_APP_ID/FB_CLIENT_TOKEN trong .env"
        write_status(status, "error", msg)
        print(f"❌ {msg}", file=sys.stderr)
        _emit({"ok": False, "error": msg})
        return EXIT_INPUT
    app_token = f"{app_id}|{client_token}"
    start = graph.call("POST", "device/login", {"access_token": app_token, "scope": a.scope})
    code = start["code"]
    user_code = start["user_code"]
    uri = start.get("verification_uri") or "https://www.facebook.com/device"
    expires_in = int(start.get("expires_in") or 420)
    interval = max(int(start.get("interval") or 5), 5)
    deadline = time.time() + min(a.timeout or expires_in, expires_in)

    from output_paths import validate_output_path
    qr_path = validate_output_path(a.qr_out, allow_system=True, create_parent=True)
    render_qr(verification_target(uri, user_code), qr_path)
    # Ưu tiên nhập mã trên máy tính: quét QR bằng iPhone mở màn hình "Log in with Facebook"
    # của app Facebook và báo "Given URL is not allowed by the Application configuration".
    host = uri.replace("https://", "").rstrip("/")
    message = (f"Trên máy tính, mở {host} và nhập mã: {user_code} "
               f"(quét QR bằng điện thoại có thể lỗi trên iPhone)")
    print(message, file=sys.stderr)
    write_status(status, "qr_ready", message, qr=f"_login/{qr_path.name}")

    while True:
        time.sleep(interval)
        if time.time() > deadline:
            write_status(status, "expired", "Mã đã hết hạn, vui lòng thử lại")
            _emit({"ok": False, "error": "expired"})
            return EXIT_AUTH
        try:
            resp = graph.call("POST", "device/login_status", {"access_token": app_token, "code": code})
            err = None
        except GraphError as exc:
            resp, err = {}, exc
        outcome = classify_device_poll(err)
        if outcome == "pending":
            continue
        if outcome == "slow_down":
            interval += 5
            continue
        if outcome == "expired":
            write_status(status, "expired", "Mã đã hết hạn, vui lòng thử lại")
            _emit({"ok": False, "error": "expired"})
            return EXIT_AUTH
        if outcome == "error":
            raise err  # type: ignore[misc]
        token = resp.get("access_token")
        if not token:
            raise GraphError("Graph API không trả access_token")
        return token, resp.get("expires_in")


def cmd_login(a) -> int:
    env = load_env()
    graph = Graph(graph_version(a.graph_version, env), build_opener(a.no_proxy))
    status = a.status_file
    if status:
        from output_paths import validate_output_path
        status = str(validate_output_path(status, allow_system=True, create_parent=True))
    write_status(status, "starting", "Đang tạo mã đăng nhập Facebook…")
    try:
        if a.token:
            user_token, expires_in = a.token.strip(), None
        else:
            result = _device_flow(a, graph, env, status)
            if isinstance(result, int):
                return result
            user_token, expires_in = result
        write_status(status, "verifying", "Đang lấy danh sách Trang…")
        me = graph.call("GET", "me", {"access_token": user_token, "fields": "id,name"})
        pages = fetch_pages(graph, user_token)
        if not pages:
            msg = "Tài khoản chưa quản trị Trang nào hoặc chưa cấp quyền pages_show_list"
            write_status(status, "error", msg)
            print(f"❌ {msg}", file=sys.stderr)
            _emit({"ok": False, "error": msg})
            return EXIT_PERMISSION
        default = select_page(pages, a.page_id or env.get("FB_PAGE_ID"))
        if default is None:
            default = pages[0]
            print(f"⚠️ Không thấy Trang {a.page_id or env.get('FB_PAGE_ID')}, dùng {default['name']}",
                  file=sys.stderr)
        save_token_file(Path(a.token_file).expanduser(), {
            "user": {"id": str(me.get("id", "")), "name": me.get("name", ""), "token": user_token,
                     "obtained": int(time.time()), "expires_in": expires_in},
            "pages": pages,
            "default_page_id": default["id"],
        })
        msg = (f"Đã kết nối: {default['name']}" if len(pages) == 1
               else f"Đã kết nối {len(pages)} Trang, mặc định: {default['name']}")
        write_status(status, "success", msg)
        print(f"✅ {msg}", file=sys.stderr)
        _emit({"ok": True, "pages": _public_pages(pages), "default_page_id": default["id"]})
        return EXIT_OK
    except InputError as exc:
        write_status(status, "error", str(exc))
        print(f"❌ {exc}", file=sys.stderr)
        _emit({"ok": False, "error": str(exc)})
        return EXIT_INPUT
    except GraphError as exc:
        _report_graph_error(exc)
        write_status(status, "error", exc.message[:200])
        _emit({"ok": False, "error": exc.message})
        return exit_code_for(exc)


# ── whoami / pages ──────────────────────────────────────────────────────────
def cmd_whoami(a) -> int:
    env = load_env()
    data = load_token_file(Path(a.token_file).expanduser())
    if data is None:
        _emit({"loggedIn": False, "name": "", "avatar": ""})
        return EXIT_OK
    page = select_page(data["pages"], a.page_id or env.get("FB_PAGE_ID"), data.get("default_page_id"))
    if page is None:
        _emit({"loggedIn": False, "name": "", "avatar": ""})
        return EXIT_OK
    graph = Graph(graph_version(a.graph_version, env), build_opener(a.no_proxy))
    try:
        resp = graph.call("GET", page["id"], {"access_token": page["token"], "fields": "name,picture{url}"})
    except GraphError as exc:
        if exc.code in (190, 102):
            _emit({"loggedIn": False, "name": "", "avatar": ""})
        else:
            _emit({"loggedIn": False, "name": "", "avatar": "", "error": exc.message})
        return EXIT_OK
    avatar = ((resp.get("picture") or {}).get("data") or {}).get("url", "")
    _emit({"loggedIn": True, "name": resp.get("name") or page.get("name", ""), "avatar": avatar})
    return EXIT_OK


def cmd_pages(a) -> int:
    path = Path(a.token_file).expanduser()
    data = load_token_file(path)
    if data is None:
        print("❌ Chưa đăng nhập Facebook, hãy chạy: facebook_publish.py login", file=sys.stderr)
        _emit({"ok": False, "pages": []})
        return EXIT_AUTH
    if a.set_default:
        if select_page(data["pages"], a.set_default) is None:
            print(f"❌ Không có Trang {a.set_default} trong danh sách đã cấp quyền", file=sys.stderr)
            return EXIT_INPUT
        data["default_page_id"] = str(a.set_default)
        save_token_file(path, data)
    _emit({"ok": True, "pages": _public_pages(data["pages"]), "default_page_id": data.get("default_page_id")})
    return EXIT_OK


# ── publish ─────────────────────────────────────────────────────────────────
def _execute(graph: Graph, kind: str, page: dict, files: list[Path], message: str,
             title: str, description: str, link: str | None) -> dict:
    token = page["token"]
    pid = page["id"]
    if kind == "text":
        return graph.call("POST", f"{pid}/feed", {"access_token": token, "message": message, "link": link})
    if kind == "photo":
        return graph.call("POST", f"{pid}/photos", {"access_token": token, "message": message},
                          files={"source": files[0]}, timeout=VIDEO_TIMEOUT)
    if kind == "album":
        params: dict[str, str] = {"access_token": token, "message": message}
        for index, path in enumerate(files):
            print(f"… tải ảnh {index + 1}/{len(files)}: {path.name}", file=sys.stderr)
            photo = graph.call("POST", f"{pid}/photos", {"access_token": token, "published": "false"},
                               files={"source": path}, timeout=VIDEO_TIMEOUT)
            params[f"attached_media[{index}]"] = json.dumps({"media_fbid": photo["id"]})
        return graph.call("POST", f"{pid}/feed", params)
    if kind == "video":
        return graph.call("POST", f"{pid}/videos",
                          {"access_token": token, "title": title or None, "description": description},
                          files={"source": files[0]}, host=GRAPH_VIDEO_HOST, timeout=VIDEO_TIMEOUT)
    raise InputError(f"Loại bài không xác định: {kind}")


def _record_manifest(topic: str, files: list[Path], url: str) -> None:
    script = HERE / "manifest.py"
    base = [sys.executable, str(script)]
    cmds = [
        base + ["record", "--topic", topic, "--layer", "publish", "--skill", SKILL_NAME,
                "--outputs", ",".join(f.name for f in files), "--summary", f"Facebook Page: {url}"],
        base + ["meta", "--topic", topic, "--status", "published", "--platform", "Facebook Page"],
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        except Exception as exc:  # noqa: BLE001 — ghi manifest không được làm hỏng lần đăng
            print(f"⚠️ Không ghi được manifest: {exc}", file=sys.stderr)


def cmd_publish(a) -> int:
    env = load_env()
    title = (a.title or "").strip()
    content = (a.content or "").strip()
    try:
        if not title and not content:
            raise InputError("Tiêu đề/nội dung không được để trống")
        kind, files = classify_media(a.images, a.video, a.link)
    except InputError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        _emit({"ok": False, "error": str(exc)})
        return EXIT_INPUT

    content_guard.guard_or_die([a.title, a.content, a.tags, a.link], exec_mode=a.exec,
                               allow_unsafe=a.allow_unsafe, label="Nội dung đăng Facebook ")

    data = load_token_file(Path(a.token_file).expanduser())
    if data is None:
        msg = "Chưa đăng nhập Facebook, hãy chạy: facebook_publish.py login"
        print(f"❌ {msg}", file=sys.stderr)
        _emit({"ok": False, "error": msg})
        return EXIT_AUTH
    page = select_page(data["pages"], a.page_id or env.get("FB_PAGE_ID"), data.get("default_page_id"))
    if page is None:
        msg = f"Không có Trang {a.page_id or env.get('FB_PAGE_ID')} trong danh sách đã cấp quyền"
        print(f"❌ {msg}", file=sys.stderr)
        _emit({"ok": False, "error": msg})
        return EXIT_AUTH

    message = build_message(title, content, a.tags)
    description = build_video_description(content, a.tags)
    graph = Graph(graph_version(a.graph_version, env), build_opener(a.no_proxy))
    plan = plan_requests(kind, page["id"], files, a.link)

    try:
        if not a.exec:
            page_name = page.get("name", "")
            if not a.offline:
                resp = graph.call("GET", page["id"], {"access_token": page["token"], "fields": "name"})
                page_name = resp.get("name") or page_name
            print("ℹ️ Dry-run: chưa đăng gì. Thêm --exec để đăng thật.", file=sys.stderr)
            _emit({"ok": True, "dry_run": True, "kind": kind,
                   "page": {"id": page["id"], "name": page_name}, "requests": plan,
                   "message": description if kind == "video" else message,
                   "title": title if kind == "video" else ""})
            return EXIT_OK

        result = _execute(graph, kind, page, files, message, title, description, a.link)
    except InputError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        _emit({"ok": False, "error": str(exc)})
        return EXIT_INPUT
    except GraphError as exc:
        _report_graph_error(exc)
        _emit({"ok": False, "error": exc.message, "code": exc.code})
        return exit_code_for(exc)

    url = post_url(kind, page["id"], result)
    post_id = result.get("post_id") or result.get("id", "")
    ptype = "Video" if kind == "video" else ("Ảnh" if kind in ("photo", "album") else "Chữ")
    calendar_ops.record_publish(PLATFORM, title or content.splitlines()[0][:60], url=url, ptype=ptype,
                                tags=a.tags or "", note=content[:200])
    if a.topic:
        _record_manifest(a.topic, files, url)
    print(f"✅ Đã đăng lên Trang {page.get('name', page['id'])}: {url}", file=sys.stderr)
    _emit({"ok": True, "dry_run": False, "kind": kind, "post_id": post_id, "url": url,
           "page": {"id": page["id"], "name": page.get("name", "")}})
    return EXIT_OK


# ── CLI ─────────────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Đăng Trang Facebook qua Meta Graph API")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--token-file", default=str(DEFAULT_TOKEN_FILE),
                       help="Tệp token (mặc định ~/.easel-browser-profiles/FacebookPageProfile/token.json)")
        p.add_argument("--graph-version", help=f"Phiên bản Graph API (mặc định FB_GRAPH_VERSION hoặc {DEFAULT_GRAPH_VERSION})")
        p.add_argument("--no-proxy", action="store_true", help="Không dùng proxy từ env")

    lg = sub.add_parser("login", help="Đăng nhập thiết bị, lưu Page token")
    common(lg)
    lg.add_argument("--qr-out", default=DEFAULT_QR_OUT, help="Đường dẫn PNG mã QR")
    lg.add_argument("--status-file", help="Tệp JSON trạng thái đăng nhập (web backend poll)")
    lg.add_argument("--timeout", type=int, help="Số giây chờ tối đa (mặc định theo expires_in của Meta)")
    lg.add_argument("--scope", default=DEFAULT_SCOPE, help="Quyền xin cấp, phân tách bằng dấu phẩy")
    lg.add_argument("--page-id", help="Trang mặc định")
    lg.add_argument("--token", help="Dán user access token có sẵn (bỏ qua đăng nhập thiết bị)")
    lg.set_defaults(func=cmd_login)

    wh = sub.add_parser("whoami", help="Kiểm tra token, in tên/ảnh Trang")
    common(wh)
    wh.add_argument("--page-id", help="Trang cần kiểm tra")
    wh.set_defaults(func=cmd_whoami)

    pg = sub.add_parser("pages", help="Liệt kê Trang đã cấp quyền")
    common(pg)
    pg.add_argument("--set-default", help="Đặt Trang mặc định theo ID")
    pg.set_defaults(func=cmd_pages)

    pb = sub.add_parser("publish", help="Đăng bài (mặc định dry-run)")
    common(pb)
    pb.add_argument("--title", help="Tiêu đề (video: title; bài chữ/ảnh: dòng đầu)")
    pb.add_argument("--content", help="Nội dung bài / mô tả video")
    pb.add_argument("--tags", help="Hashtag, phân tách bằng dấu phẩy")
    pb.add_argument("--images", help="Đường dẫn ảnh, phân tách bằng dấu phẩy")
    pb.add_argument("--video", help="Đường dẫn video")
    pb.add_argument("--link", help="Link đính kèm (chỉ bài chữ)")
    pb.add_argument("--page-id", help="Trang đăng (mặc định Trang mặc định trong token)")
    pb.add_argument("--topic", help="Chủ đề outputs/<topic>/ để ghi manifest sau khi đăng")
    pb.add_argument("--offline", action="store_true", help="Dry-run không gọi mạng")
    pb.add_argument("--exec", action="store_true", help="Đăng thật (mặc định dry-run)")
    pb.add_argument("--allow-unsafe", action="store_true", help="Bỏ qua chặn của content_guard (thận trọng)")
    pb.set_defaults(func=cmd_publish)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
