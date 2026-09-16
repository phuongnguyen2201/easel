#!/usr/bin/env python3
"""publish_dispatch.py — lập kế hoạch đăng đa nền tảng (bảng ràng buộc + định tuyến + kế hoạch).

Một nội dung → nhiều nền tảng. Script cung cấp: ràng buộc định dạng từng nền tảng (số ký tự,
tỉ lệ khung hình, số hashtag, loại nội dung), định tuyến nền tảng → SKILL/script đăng, và
"kế hoạch phân phối" (kiểm tra vượt giới hạn, nền tảng nào đã có adapter, lệnh chạy thử).

Việc viết lại nội dung theo từng nền tảng do LLM làm; việc đăng thật do script đăng của từng
nền tảng thực hiện (chạy thử trước, --exec sau khi người dùng xác nhận). Script này thuần xác
định, không gọi mạng, test offline được.

Bảng PLATFORMS phải khớp LOGIN_RUNNERS trong web/app.py cho các nền tảng status="available"
(tests/test_publish_dispatch.py kiểm tra điều này).

Subcommand:
    platforms  liệt kê nền tảng và ràng buộc
    plan       đọc manifest nội dung → kế hoạch từng nền tảng
    selftest   tự kiểm

Ví dụ:
    publish_dispatch.py platforms
    publish_dispatch.py plan --manifest content.json
    echo '{...}' | publish_dispatch.py plan --manifest -
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys

# status: available = đã có adapter đăng; planned = runbook 5.2, chưa có adapter.
# title/body: số ký tự tối đa (0 = không áp dụng). tags: số hashtag khuyến nghị tối đa (0 = không giới hạn cứng).
# Giới hạn của nền tảng planned là kiến thức ngoài repo — kiểm lại tài liệu chính thức khi xây adapter.
PLATFORMS: dict[str, dict] = {
    "facebook-page": {
        "name": "Facebook Page", "status": "available",
        "publisher": "skill-facebook-page-upload",
        "script": "skills/shared/scripts/facebook_publish.py",
        "types": ["text", "image", "video"],
        "title": 255, "body": 63206, "tags": 0, "aspect": "ảnh 1:1 hoặc 4:5; video 16:9 hoặc 9:16",
        "note": "Tiêu đề chỉ là tiêu đề video, bài chữ/ảnh thì thành dòng đầu; 3–5 hashtag là đủ; "
                "album nhiều ảnh = một bài; ảnh và video không đăng cùng lúc",
    },
    "youtube": {
        "name": "YouTube", "status": "planned", "publisher": None, "script": None,
        "types": ["video"], "title": 100, "body": 5000, "tags": 15, "aspect": "16:9; Shorts 9:16",
        "note": "Chưa có adapter (runbook 5.2 bước 2, Data API v3 có hạn mức ngày)",
    },
    "tiktok": {
        "name": "TikTok", "status": "planned", "publisher": None, "script": None,
        "types": ["video", "image"], "title": 0, "body": 2200, "tags": 5, "aspect": "9:16",
        "note": "Chưa có adapter (runbook 5.2 bước 3, Content Posting API cần app audit)",
    },
    "zalo-oa": {
        "name": "Zalo OA", "status": "planned", "publisher": None, "script": None,
        "types": ["article"], "title": 0, "body": 0, "tags": 0, "aspect": "-",
        "note": "Chưa có adapter (runbook 5.2 bước 4)",
    },
    "instagram": {
        "name": "Instagram", "status": "planned", "publisher": None, "script": None,
        "types": ["image", "video"], "title": 0, "body": 2200, "tags": 30, "aspect": "4:5 hoặc 1:1; Reels 9:16",
        "note": "Chưa có adapter (runbook 5.2 bước 5, dùng chung app Meta)",
    },
    "threads": {
        "name": "Threads", "status": "planned", "publisher": None, "script": None,
        "types": ["text", "image", "video"], "title": 0, "body": 500, "tags": 1, "aspect": "-",
        "note": "Chưa có adapter (runbook 5.2 bước 5)",
    },
}

MEDIA_TYPES = {"text", "image", "video", "article"}


def _die(msg: str, code: int = 1) -> None:
    print(f"LỖI: {msg}", file=sys.stderr)
    sys.exit(code)


def cmd_platforms(_a) -> int:
    print(f"{len(PLATFORMS)} nền tảng:\n")
    for key, c in PLATFORMS.items():
        state = f"→ {c['publisher']}" if c["status"] == "available" else "→ (chưa có adapter)"
        title = f"tiêu đề ≤{c['title']}" if c["title"] else "tiêu đề: không áp dụng"
        body = f"nội dung ≤{c['body']}" if c["body"] else "nội dung: không giới hạn cứng"
        print(f"  {key:14s} {c['name']:14s} {state}")
        print(f"    loại {'/'.join(c['types'])} · {title} · {body} · hashtag ≤{c['tags'] or '∞'} · tỉ lệ {c['aspect']}")
        print(f"    {c['note']}")
    return 0


def _dry_run_command(c: dict, content: dict) -> str:
    """Lệnh chạy thử (không --exec) cho nền tảng đã có adapter."""
    parts = ["python", c["script"], "publish"]
    if content.get("title"):
        parts += ["--title", str(content["title"])]
    parts += ["--content", "<nội dung đã thích ứng>"]
    tags = content.get("tags") or []
    if tags:
        parts += ["--tags", ",".join(str(t) for t in tags)]
    mtype = content.get("media_type", "")
    if mtype == "video":
        parts += ["--video", "<đường dẫn video>"]
    elif mtype == "image":
        parts += ["--images", "<ảnh 1>,<ảnh 2>"]
    if content.get("topic"):
        parts += ["--topic", str(content["topic"])]
    return " ".join(shlex.quote(p) if not p.startswith("<") else p for p in parts)


def check_platform(key: str, content: dict) -> dict:
    """Kiểm tra ràng buộc cho một nền tảng, trả mục kế hoạch (kèm warnings)."""
    if key not in PLATFORMS:
        return {"platform": key, "ok": False,
                "error": f"Nền tảng không xác định (hỗ trợ: {', '.join(PLATFORMS)})"}
    c = PLATFORMS[key]
    warns: list[str] = []
    title = content.get("title", "") or ""
    body = content.get("body", "") or ""
    tags = content.get("tags", []) or []
    mtype = content.get("media_type", "")

    if c["title"] and len(title) > c["title"]:
        warns.append(f"Tiêu đề {len(title)}>{c['title']} ký tự, cần rút gọn")
    if c["body"] and len(body) > c["body"]:
        warns.append(f"Nội dung {len(body)}>{c['body']} ký tự, cần rút gọn")
    if c["tags"] and len(tags) > c["tags"]:
        warns.append(f"Hashtag {len(tags)}>{c['tags']}, cần bớt")
    if mtype and mtype not in c["types"]:
        warns.append(f"Loại nội dung {mtype} không hợp với nền tảng (hỗ trợ {'/'.join(c['types'])}), cần đổi hình thức")

    item = {"platform": key, "name": c["name"], "ok": True, "available": c["status"] == "available",
            "recommend_aspect": c["aspect"], "constraints_note": c["note"], "warnings": warns}
    if item["available"]:
        item.update({
            "publisher": c["publisher"],
            "dry_run_command": _dry_run_command(c, content),
            "action": f"Thích ứng nội dung theo ràng buộc → chạy thử → người dùng xác nhận → thêm --exec",
        })
    else:
        item.update({"publisher": None,
                     "action": f"{c['name']} chưa có adapter đăng: báo người dùng, chỉ soạn bản thích ứng để đăng tay"})
    return item


def build_plan(manifest: dict) -> dict:
    content = manifest.get("content", {}) or {}
    platforms = manifest.get("platforms", []) or []
    if not platforms:
        raise ValueError("manifest.platforms rỗng (cần danh sách nền tảng đích)")
    mtype = content.get("media_type", "")
    if mtype and mtype not in MEDIA_TYPES:
        raise ValueError(f"media_type không hợp lệ: {mtype} (chọn {', '.join(sorted(MEDIA_TYPES))})")
    dispatch = [check_platform(p, content) for p in platforms]
    return {
        "content_title": content.get("title", ""),
        "target_count": len(platforms),
        "publishable": [d["platform"] for d in dispatch if d.get("available")],
        "manual_only": [d["platform"] for d in dispatch if d.get("ok") and not d.get("available")],
        "dispatch": dispatch,
        "hint": "Với từng nền tảng available: thích ứng tiêu đề/nội dung/hashtag theo constraints_note, "
                "chạy dry_run_command, xác nhận với người dùng rồi thêm --exec. Nền tảng manual_only: "
                "chỉ đưa bản thích ứng để người dùng đăng tay.",
    }


def cmd_plan(a) -> int:
    raw = sys.stdin.read() if a.manifest == "-" else _read(a.manifest)
    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as e:
        _die(f"manifest không phải JSON hợp lệ: {e}")
    try:
        plan = build_plan(manifest)
    except ValueError as e:
        _die(str(e))
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


def _read(path: str) -> str:
    from pathlib import Path
    p = Path(path).expanduser()
    if not p.is_file():
        _die(f"Không tìm thấy manifest: {p}")
    return p.read_text(encoding="utf-8")


def cmd_selftest(_a) -> int:
    print("publish_dispatch tự kiểm ...", file=sys.stderr)
    fb = PLATFORMS["facebook-page"]
    assert fb["status"] == "available" and fb["publisher"] == "skill-facebook-page-upload"
    r = check_platform("threads", {"body": "x" * 600, "tags": ["a", "b"], "media_type": "article"})
    assert r["ok"] and not r["available"] and r["warnings"], "vượt giới hạn phải có warnings"
    assert any("Nội dung" in w for w in r["warnings"])
    assert any("Hashtag" in w for w in r["warnings"])
    assert any("Loại nội dung" in w for w in r["warnings"])
    ok = check_platform("facebook-page", {"title": "Ngắn", "body": "Nội dung", "tags": ["a"], "media_type": "image"})
    assert ok["ok"] and ok["available"] and not ok["warnings"], ok
    assert "--exec" not in ok["dry_run_command"] and "facebook_publish.py publish" in ok["dry_run_command"]
    assert "--images" in ok["dry_run_command"]
    assert not check_platform("nope", {})["ok"]
    plan = build_plan({"content": {"title": "T", "body": "B", "media_type": "video"},
                       "platforms": ["facebook-page", "youtube"]})
    assert plan["publishable"] == ["facebook-page"] and plan["manual_only"] == ["youtube"]
    try:
        build_plan({"content": {}, "platforms": []})
        raise AssertionError("platforms rỗng phải lỗi")
    except ValueError:
        pass
    print("✅ selftest đạt (ràng buộc/cảnh báo/định tuyến/plan)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Lập kế hoạch đăng đa nền tảng (bảng ràng buộc + định tuyến + kế hoạch)",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("platforms", help="Liệt kê nền tảng và ràng buộc").set_defaults(func=cmd_platforms)

    p = sub.add_parser("plan", help="Manifest nội dung → kế hoạch phân phối")
    p.add_argument("--manifest", required=True, help="Đường dẫn manifest JSON (- là stdin)")
    p.set_defaults(func=cmd_plan)

    sub.add_parser("selftest", help="Tự kiểm").set_defaults(func=cmd_selftest)

    a = ap.parse_args()
    if not getattr(a, "func", None):
        ap.print_help()
        return 1
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
