"""easel ping — 连通性测试（直接运行，不依赖 Docker）。"""

from __future__ import annotations

import subprocess
import urllib.error
import urllib.request

from easel.env import proxy_env
from easel.gateway_port import gateway_port, gateway_url
from easel.openclaw_cmd import openclaw_base_cmd

GREEN = "\033[0;32m"
RED = "\033[0;31m"
NC = "\033[0m"


def _step(label: str, cmd: list[str], timeout: int = 30,
          env: dict[str, str] | None = None) -> bool:
    """Run a command and print OK/FAIL."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=timeout,
            env=env,
        )
        ok = result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        ok = False
        result = None

    status = f"{GREEN}OK{NC}" if ok else f"{RED}FAIL{NC}"
    print(f"  {label:<50s} {status}")

    if not ok and result and result.stderr:
        for line in result.stderr.strip().splitlines()[:5]:
            print(f"    {line}")

    return ok


def cmd_ping(_args) -> int:
    print("[easel] 连通性测试\n")
    all_ok = True

    # Step 1: Gateway healthz
    try:
        with urllib.request.urlopen(gateway_url(), timeout=10) as response:
            gateway_ok = response.status == 200
    except (OSError, urllib.error.URLError):
        gateway_ok = False
    step1 = f"Step 1: Gateway healthz (localhost:{gateway_port()})"
    print(f"  {step1:<50s} "
          f"{GREEN if gateway_ok else RED}{'OK' if gateway_ok else 'FAIL'}{NC}")
    all_ok &= gateway_ok

    # Step 2: OpenClaw agent
    oc_cmd = openclaw_base_cmd() + [
        "--profile", "easel",
        "agent", "--agent", "main",
        "--timeout", "30", "--message", "say PONG",
    ]
    all_ok &= _step(
        "Step 2: OpenClaw agent via Gateway (say PONG)",
        oc_cmd,
        timeout=60,
        env=proxy_env(),
    )

    print()
    if all_ok:
        print(f"{GREEN}✓ 全部通过{NC}")
    else:
        print(f"{RED}✗ 有步骤失败{NC} — 请运行 python -m easel doctor 检查环境")

    return 0 if all_ok else 1
