"""easel doctor — 检查开发环境是否就绪。"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

from easel.gateway_port import gateway_port, gateway_url

# 项目根目录（Easel/）
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# OpenClaw 已验证的稳定下限。低于此版本会命中一系列破坏性变更：anthropic provider 必须原子写入、
# timeoutSeconds 被判 Unrecognized key、记忆检索 schema 尚未迁移到 memory.search.* 等（见 issue #9/#11）。
MIN_OPENCLAW = (2026, 6, 11)

GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
NC = "\033[0m"


def _check(label: str, ok: bool, detail: str = "") -> bool:
    status = f"{GREEN}OK{NC}" if ok else f"{RED}FAIL{NC}"
    print(f"  {label:<40s} {status}")
    if not ok and detail:
        print(f"    └─ {detail}")
    return ok


def _warn(label: str, ok: bool, detail: str = "") -> bool:
    """Như _check nhưng lỗi chỉ là cảnh báo — không tính vào kết quả chung."""
    status = f"{GREEN}OK{NC}" if ok else f"{YELLOW}WARN{NC}"
    print(f"  {label:<40s} {status}")
    if not ok and detail:
        print(f"    └─ {detail}")
    return ok


def _node_version_ok(strict: bool) -> bool:
    """Kiểm tra phiên bản Node.js.

    strict=True khớp engine của openclaw@latest (2026.9.x): >=24.16.0 <25 || >=26.1.0 (loại 25.x/26.0).
    strict=False dùng cho OpenClaw cũ đã cài (<=2026.6.x, engine ^20.10 || ^22.11 || >=24), ngưỡng nới >=20.10.
    """
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return False
        # e.g. "v24.21.0"
        m = re.match(r"v(\d+)\.(\d+)", result.stdout.strip())
        if not m:
            return False
        major, minor = int(m.group(1)), int(m.group(2))
        if strict:
            return (major == 24 and minor >= 16) or (major == 26 and minor >= 1) or major >= 27
        return (major, minor) >= (20, 10)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _openclaw_version() -> tuple[int, int, int] | None:
    """解析 `openclaw --version`，返回 (year, month, patch)；无法确定时返回 None。"""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return None
        # e.g. "OpenClaw 2026.9.4 (3a9d69d)"
        m = re.search(r"(\d+)\.(\d+)\.(\d+)", result.stdout)
        if not m:
            return None
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def _python_version_ok() -> bool:
    import sys
    return sys.version_info >= (3, 10)


def _module_available(name: str) -> bool:
    try:
        __import__(name)
        return True
    except ImportError:
        return False


def _venv_available() -> bool:
    return _module_available("venv")


def _chromium_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as playwright:
            return Path(playwright.chromium.executable_path).is_file()
    except (ImportError, OSError, RuntimeError):
        return False


def _gateway_healthy() -> bool:
    """Check OpenClaw gateway is running via healthz endpoint."""
    try:
        with urllib.request.urlopen(gateway_url(), timeout=5) as response:
            return response.status == 200
    except (OSError, urllib.error.URLError):
        return False


def _skills_synced() -> bool:
    """Check ~/.openclaw/workspace-easel/skills/ has content."""
    skills_dir = Path.home() / ".openclaw" / "workspace-easel" / "skills"
    if not skills_dir.is_dir():
        return False
    return any(skills_dir.iterdir())


def _env_key_valid() -> bool:
    """Kiểm tra .env có cấu hình xác thực dùng được.

    Chỉ cần thoả một trong các kênh:
    - API key chuẩn: ANTHROPIC_API_KEY
    - Dịch vụ Anthropic-compatible: EASEL_LLM_API_KEY + EASEL_LLM_BASE_URL

    ping mới là kiểm tra kết nối chính thức; ở đây chỉ kiểm tra cấu hình có tồn tại.
    """
    env_file = PROJECT_ROOT / ".env"
    if not env_file.is_file():
        return False

    # 认证变量 → 是否已填入非占位值
    auth_vars: dict[str, str] = {}
    try:
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key in (
                "ANTHROPIC_API_KEY", "EASEL_LLM_API_KEY", "EASEL_LLM_BASE_URL",
                "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL",
                "OPENAI_API_KEY", "OPENAI_BASE_URL",
                "OPENAI_MAAS_API_KEY", "OPENAI_MAAS_ENDPOINT",
            ):
                auth_vars[key] = value
    except OSError:
        return False

    def _set(name: str) -> bool:
        v = auth_vars.get(name, "")
        return bool(v) and "REPLACE_ME" not in v

    # 标准 key 通道
    if _set("ANTHROPIC_API_KEY"):
        return True
    # Anthropic-compatible 服务：key + base_url 同时配好
    if _set("EASEL_LLM_API_KEY") and _set("EASEL_LLM_BASE_URL"):
        return True
    if _set("ANTHROPIC_AUTH_TOKEN") and _set("ANTHROPIC_BASE_URL"):
        return True
    if _set("OPENAI_API_KEY"):
        return True
    if _set("OPENAI_MAAS_API_KEY") and _set("OPENAI_MAAS_ENDPOINT"):
        return True
    return False


def cmd_doctor(_args) -> int:
    print("Easel — Kiểm tra môi trường\n")
    all_ok = True

    # 1. Runtime prerequisites
    all_ok &= _check("Python >= 3.10", _python_version_ok(),
                      "Hãy cài Python 3.10 trở lên")
    all_ok &= _check("Python venv module", _venv_available(),
                      "Debian/Ubuntu: hãy cài python3-venv")
    # openclaw 版本决定 Node 引擎要求：2026.9.x 需要 Node 24.16+，较旧版本沿用 >=20.10 的宽松下限。
    # 未装 openclaw 时按 setup 的默认安装目标（openclaw@latest）从严要求 24.16+。
    oc_ver = _openclaw_version()
    node_strict = oc_ver is None or oc_ver >= (2026, 9, 0)
    node_floor = "24.16" if node_strict else "20.10"
    has_node = shutil.which("node") is not None
    node_ok = _node_version_ok(node_strict)
    node_detail = (f"Hãy cài Node.js >= {node_floor}: https://nodejs.org/" if not has_node
                   else f"Phiên bản Node.js không đạt yêu cầu của OpenClaw hiện tại, hãy nâng lên >= {node_floor}: https://nodejs.org/")
    all_ok &= _check(f"Node.js >= {node_floor}", node_ok, node_detail)
    all_ok &= _check("FFmpeg", shutil.which("ffmpeg") is not None,
                      "Xử lý media cần FFmpeg; hãy cài rồi thử lại")

    # 2. openclaw command + 版本
    has_openclaw = shutil.which("openclaw") is not None
    all_ok &= _check("openclaw command", has_openclaw,
                      "Hãy cài openclaw: npm i -g openclaw")
    if has_openclaw:
        min_str = ".".join(map(str, MIN_OPENCLAW))
        ver_str = ".".join(map(str, oc_ver)) if oc_ver else "không rõ"
        oc_ver_ok = oc_ver is not None and oc_ver >= MIN_OPENCLAW
        all_ok &= _check(
            f"OpenClaw >= {min_str}", oc_ver_ok,
            f"Hiện tại {ver_str}, bản quá cũ sẽ lỗi tương thích provider/schema; hãy nâng cấp: npm i -g openclaw@latest",
        )

    for module in ("fastapi", "uvicorn", "sse_starlette", "multipart"):
        all_ok &= _check(f"Python package: {module}", _module_available(module),
                          "Chạy pip install -e . để cài phụ thuộc của Easel")

    frontend_ready = (PROJECT_ROOT / "web" / "frontend" / "dist" / "index.html").is_file()
    all_ok &= _check("Web frontend build", frontend_ready,
                      "Chạy cd web/frontend && npm ci && npm run build")
    all_ok &= _check("Playwright Chromium", _chromium_available(),
                      "Chạy python3 -m playwright install chromium")

    # 3. .env file with valid key
    # Không tính vào all_ok: các kênh đăng nhập như claude-cli / OAuth giữ
    # credential trong profile OpenClaw (~/.openclaw-easel/), không đặt trong .env,
    # nên check tĩnh này sẽ FAIL vĩnh viễn dù máy đang chạy tốt.
    env_ok = _env_key_valid()
    _warn(".env (API Key)", env_ok,
          "Không thấy key trong .env. Dùng claude-cli/OAuth thì đây là bình thường; "
          "nếu không, điền ANTHROPIC_API_KEY hoặc EASEL_LLM_API_KEY + EASEL_LLM_BASE_URL. "
          "Kết luận cuối cùng lấy từ: python -m easel ping")

    # 4. OpenClaw gateway running
    gw_ok = _gateway_healthy()
    all_ok &= _check(f"OpenClaw gateway (localhost:{gateway_port()})", gw_ok,
                      "Chạy python -m easel gateway start")

    # 5. Skills synced
    synced = _skills_synced()
    all_ok &= _check("Skills synced", synced,
                      "Chạy lại setup.ps1 (Windows) hoặc bash openclaw/sync.sh (Linux/macOS)")

    # 6. Key project files
    gateway_label = "scripts/gateway.ps1" if os.name == "nt" else "scripts/gateway.sh"
    gateway_path = PROJECT_ROOT / "scripts" / ("gateway.ps1" if os.name == "nt" else "gateway.sh")
    key_files = [
        ("openclaw/openclaw.json5", PROJECT_ROOT / "openclaw" / "openclaw.json5"),
        ("skills/openclaw/", PROJECT_ROOT / "skills" / "openclaw"),
        (gateway_label, gateway_path),
    ]
    for label, path in key_files:
        all_ok &= _check(label, path.exists())

    print()
    if all_ok:
        print(f"{GREEN}✓ Môi trường sẵn sàng{NC} — chạy python -m easel ping để kiểm tra kết nối")
    else:
        print(f"{YELLOW}⚠ Còn mục chưa đạt{NC} — sửa theo gợi ý trên rồi thử lại")

    return 0 if all_ok else 1
