"""Unit test cho adapter facebook-page (facebook_publish.py + đăng ký trong web/app.py).

Không gọi mạng: Graph được thay bằng đối tượng giả.
Chạy: pytest tests/test_facebook_publish.py -q
"""
from __future__ import annotations

import json
import stat
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "skills" / "shared" / "scripts"))

import facebook_publish as fb  # noqa: E402


# ── hàm thuần ───────────────────────────────────────────────────────────────
def test_format_tags_dedupes_and_keeps_vietnamese():
    assert fb.format_tags("AI, giáo dục,#ai，Mẹo hay") == "#AI #giáodục #Mẹohay"
    assert fb.format_tags("") == ""
    assert fb.format_tags(None) == ""


def test_build_message_prepends_title_once():
    assert fb.build_message("Tiêu đề", "Nội dung", "a,b") == "Tiêu đề\n\nNội dung\n\n#a #b"
    assert fb.build_message("Tiêu đề", "Tiêu đề và thân bài") == "Tiêu đề và thân bài"
    assert fb.build_message("", "Chỉ nội dung") == "Chỉ nội dung"
    assert fb.build_message("Chỉ tiêu đề", "") == "Chỉ tiêu đề"


def test_classify_media(tmp_path):
    a = tmp_path / "a.png"; a.write_bytes(b"x")
    b = tmp_path / "b.jpg"; b.write_bytes(b"x")
    v = tmp_path / "v.mp4"; v.write_bytes(b"x")
    assert fb.classify_media(None, None) == ("text", [])
    assert fb.classify_media(str(a), None) == ("photo", [a])
    assert fb.classify_media(f"{a},{b}", None) == ("album", [a, b])
    assert fb.classify_media(None, str(v)) == ("video", [v])
    with pytest.raises(fb.InputError):
        fb.classify_media(str(a), str(v))
    with pytest.raises(fb.InputError):
        fb.classify_media(str(tmp_path / "missing.png"), None)
    with pytest.raises(fb.InputError):
        fb.classify_media(str(v), None)          # video truyền vào --images
    with pytest.raises(fb.InputError):
        fb.classify_media(str(a), None, link="https://example.com")


def test_plan_requests_album_ends_with_feed(tmp_path):
    files = [tmp_path / "a.png", tmp_path / "b.png"]
    plan = fb.plan_requests("album", "111", files)
    assert [step["path"] for step in plan] == ["111/photos", "111/photos", "111/feed"]
    assert fb.plan_requests("video", "111", [tmp_path / "v.mp4"])[0]["host"] == "graph-video"


def test_post_url():
    assert fb.post_url("text", "111", {"id": "111_222"}) == "https://www.facebook.com/111_222"
    assert fb.post_url("photo", "111", {"id": "9", "post_id": "111_333"}) == "https://www.facebook.com/111_333"
    assert fb.post_url("video", "111", {"id": "444"}) == "https://www.facebook.com/111/videos/444"


@pytest.mark.parametrize("code,expected", [
    (190, fb.EXIT_AUTH), (10, fb.EXIT_PERMISSION), (200, fb.EXIT_PERMISSION),
    (4, fb.EXIT_RATE_LIMIT), (613, fb.EXIT_RATE_LIMIT), (1, fb.EXIT_ERROR), (None, fb.EXIT_ERROR),
])
def test_exit_code_for(code, expected):
    assert fb.exit_code_for(fb.GraphError("x", code=code)) == expected


def test_classify_device_poll():
    assert fb.classify_device_poll(None) == "ok"
    assert fb.classify_device_poll(fb.GraphError("x", subcode=fb.DEVICE_PENDING)) == "pending"
    assert fb.classify_device_poll(fb.GraphError("x", subcode=fb.DEVICE_SLOW_DOWN)) == "slow_down"
    assert fb.classify_device_poll(fb.GraphError("x", subcode=fb.DEVICE_EXPIRED)) == "expired"
    assert fb.classify_device_poll(fb.GraphError("x", code=190)) == "error"


def test_select_page():
    pages = [{"id": "1", "name": "A"}, {"id": "2", "name": "B"}]
    assert fb.select_page(pages, None)["id"] == "1"
    assert fb.select_page(pages, None, "2")["id"] == "2"
    assert fb.select_page(pages, "2", "1")["id"] == "2"
    assert fb.select_page(pages, "9") is None
    assert fb.select_page([], None) is None


def test_verification_target_and_mask():
    assert fb.verification_target("https://www.facebook.com/device", "AB12") == \
        "https://www.facebook.com/device?user_code=AB12"
    assert "EAAB1234" not in fb.mask("EAAB1234567890")
    assert fb.mask("short") == "***"


def test_save_token_file_is_private(tmp_path):
    path = tmp_path / "prof" / "token.json"
    fb.save_token_file(path, {"pages": [{"id": "1", "token": "t"}]})
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert fb.load_token_file(path)["pages"][0]["id"] == "1"
    assert fb.load_token_file(tmp_path / "none.json") is None


# ── luồng CLI (không mạng) ──────────────────────────────────────────────────
@pytest.fixture
def token_file(tmp_path):
    path = tmp_path / "token.json"
    path.write_text(json.dumps({"user": {}, "pages": [{"id": "111", "name": "Trang", "token": "EAAtoken"}],
                                "default_page_id": "111"}), encoding="utf-8")
    return path


def _last_json(capsys) -> dict:
    return json.loads(capsys.readouterr().out.strip().splitlines()[-1])


def test_publish_dry_run_offline(token_file, capsys, monkeypatch):
    monkeypatch.delenv("FB_PAGE_ID", raising=False)
    rc = fb.main(["publish", "--token-file", str(token_file), "--title", "T", "--content", "C",
                  "--tags", "x", "--offline"])
    out = _last_json(capsys)
    assert rc == 0 and out["dry_run"] is True and out["message"] == "T\n\nC\n\n#x"


def test_publish_exec_blocked_by_guard_before_token(tmp_path):
    with pytest.raises(SystemExit) as exc:
        fb.main(["publish", "--token-file", str(tmp_path / "none.json"),
                 "--content", "key sk-abcdefghijklmnopqrst", "--exec"])
    assert exc.value.code == fb.EXIT_GUARD


def test_publish_without_login(tmp_path, capsys):
    rc = fb.main(["publish", "--token-file", str(tmp_path / "none.json"), "--content", "x", "--offline"])
    assert rc == fb.EXIT_AUTH


def test_publish_input_error(token_file):
    assert fb.main(["publish", "--token-file", str(token_file)]) == fb.EXIT_INPUT


def test_whoami_without_token(tmp_path, capsys):
    assert fb.main(["whoami", "--token-file", str(tmp_path / "none.json")]) == 0
    assert _last_json(capsys) == {"loggedIn": False, "name": "", "avatar": ""}


class FakeGraph:
    def __init__(self):
        self.calls = []

    def call(self, method, path, params=None, files=None, host=fb.GRAPH_HOST, timeout=0):
        self.calls.append((method, path, dict(params or {}), files, host))
        if path.endswith("/photos"):
            return {"id": f"ph{len(self.calls)}"}
        return {"id": "111_999"}


def test_execute_album_attaches_unpublished_photos(tmp_path):
    files = [tmp_path / "a.png", tmp_path / "b.png"]
    graph = FakeGraph()
    result = fb._execute(graph, "album", {"id": "111", "token": "t"}, files, "msg", "", "", None)
    assert result == {"id": "111_999"}
    assert [c[2].get("published") for c in graph.calls[:2]] == ["false", "false"]
    feed = graph.calls[-1][2]
    assert json.loads(feed["attached_media[0]"]) == {"media_fbid": "ph1"}
    assert json.loads(feed["attached_media[1]"]) == {"media_fbid": "ph2"}


def test_execute_video_uses_video_host(tmp_path):
    graph = FakeGraph()
    fb._execute(graph, "video", {"id": "111", "token": "t"}, [tmp_path / "v.mp4"], "", "Tiêu đề", "Mô tả", None)
    method, path, params, files, host = graph.calls[0]
    assert path == "111/videos" and host == fb.GRAPH_VIDEO_HOST
    assert params["title"] == "Tiêu đề" and params["description"] == "Mô tả"


# ── đăng ký trong web/app.py ────────────────────────────────────────────────
def test_web_registration():
    pytest.importorskip("fastapi")
    sys.path.insert(0, str(PROJECT_ROOT))
    sys.path.insert(0, str(PROJECT_ROOT / "web"))
    import app as web

    cfg = web.LOGIN_RUNNERS["facebook-page"]
    assert cfg["backend"] == "graph" and (web.SHARED_SCRIPTS / cfg["script"]).is_file()
    assert {"FB_APP_ID", "FB_CLIENT_TOKEN", "FB_PAGE_ID", "FB_GRAPH_VERSION"} <= web._ENV_ALLOWLIST
    assert "skill-facebook-page-upload" in web.SKILL_API_REQUIREMENTS
