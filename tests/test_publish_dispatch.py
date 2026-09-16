"""Unit test cho skill-cross-platform-publish/scripts/publish_dispatch.py.

Chạy: pytest tests/test_publish_dispatch.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "skills" / "openclaw" / "skill-cross-platform-publish" / "scripts"))

import publish_dispatch as pd  # noqa: E402


def test_available_platforms_have_existing_publisher():
    for key, c in pd.PLATFORMS.items():
        if c["status"] == "available":
            assert (PROJECT_ROOT / c["script"]).is_file(), key
            assert (PROJECT_ROOT / "skills" / "openclaw" / c["publisher"] / "SKILL.md").is_file(), key
        else:
            assert c["status"] == "planned" and c["publisher"] is None and c["script"] is None, key


def test_plan_splits_publishable_and_manual():
    plan = pd.build_plan({"content": {"title": "T", "body": "B", "tags": ["a"], "media_type": "video"},
                          "platforms": ["facebook-page", "youtube", "nope"]})
    assert plan["publishable"] == ["facebook-page"]
    assert plan["manual_only"] == ["youtube"]
    assert plan["dispatch"][2]["ok"] is False


def test_dry_run_command_never_exec():
    item = pd.check_platform("facebook-page", {"title": "T", "tags": ["a", "b"], "media_type": "video", "topic": "x"})
    cmd = item["dry_run_command"]
    assert "--exec" not in cmd and "--allow-unsafe" not in cmd
    assert "--video" in cmd and "--topic x" in cmd and "--tags a,b" in cmd


def test_warnings_for_limits():
    item = pd.check_platform("tiktok", {"body": "x" * 3000, "tags": list("abcdef"), "media_type": "article"})
    assert len(item["warnings"]) == 3


@pytest.mark.parametrize("manifest", [
    {"content": {}, "platforms": []},
    {"content": {"media_type": "carousel"}, "platforms": ["facebook-page"]},
])
def test_build_plan_rejects_bad_manifest(manifest):
    with pytest.raises(ValueError):
        pd.build_plan(manifest)


def test_registry_matches_login_runners():
    pytest.importorskip("fastapi")
    sys.path.insert(0, str(PROJECT_ROOT))
    sys.path.insert(0, str(PROJECT_ROOT / "web"))
    import app as web

    available = {k for k, c in pd.PLATFORMS.items() if c["status"] == "available"}
    assert available == set(web.LOGIN_RUNNERS)
    for key in available:
        assert pd.PLATFORMS[key]["name"] == web.LOGIN_RUNNERS[key]["name"]
        assert pd.PLATFORMS[key]["body"] == web.LOGIN_RUNNERS[key]["bodyLimit"]
