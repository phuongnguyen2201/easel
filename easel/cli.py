"""Easel CLI — lớp tích hợp quy trình nội dung mạng xã hội.

Cách dùng:
    easel chat                              # phiên mới (chọn hồ sơ rồi vào)
    easel doctor                            # kiểm tra môi trường
    easel gateway {start|stop|status}       # quản lý gateway
    easel ping                              # kiểm tra kết nối
    easel skill <name> -i "..." -p <hồ sơ>  # chạy SKILL
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from easel.commands.doctor import cmd_doctor
from easel.commands.gateway import cmd_gateway
from easel.commands.ping import cmd_ping
from easel.commands.skill import cmd_skill
from easel.env import proxy_env
from easel.persona import list_personas as _list_personas
from easel.persona import persona_prefix
from easel.timeouts import TIMEOUT_CHAT

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = PROJECT_ROOT / "profiles"
PROFILE = "easel"


CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
DIM = "\033[0;90m"
NC = "\033[0m"


def cmd_chat(_args) -> int:
    """启动 Easel 交互对话（每次新会话）。"""

    print()
    print(f"  {CYAN}Easel{NC} — Quy trình nội dung mạng xã hội")
    print()

    # ---- 选择画像 ----
    personas = _list_personas()
    selected_persona = None

    if personas:
        print("  Chọn hồ sơ (profile):")
        for i, name in enumerate(personas, 1):
            identity = PROFILES_DIR / name / "identity.md"
            desc = ""
            if identity.is_file():
                for line in identity.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("<!--"):
                        desc = f"  — {line[:50]}"
                        break
            print(f"    {i}) {name}{desc}")
        print(f"    0) Không dùng hồ sơ (chế độ chung)")
        print()

        try:
            choice = input("  Chọn [0]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if choice and choice != "0":
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(personas):
                    selected_persona = personas[idx]
            except ValueError:
                if choice in personas:
                    selected_persona = choice

    # ---- 每次新会话 ----
    if selected_persona:
        print(f"\n  {GREEN}✓{NC} Hồ sơ: {selected_persona}")
    else:
        print(f"\n  {YELLOW}→{NC} Chế độ chung")

    session_key = f"easel-{time.strftime('%m%d-%H%M%S')}"

    print(f"  {DIM}Phiên: {session_key}{NC}")
    print(f"  {DIM}Đổi sang phiên cũ: gõ /session trong cuộc trò chuyện{NC}")
    print(f"  {CYAN}Ctrl+C{NC} để thoát")
    print()

    cmd = [
        "openclaw", "--profile", PROFILE,
        # 必须用 tui，不能用 chat：`chat`/`terminal` 是 `tui` 的别名，会强制本地模式
        # （openclaw dist/tui-cli-*.js: invokedSubcommand === "chat" → isLocal = true）。
        # 而 --local 要求独占 state 目录，与 Easel 自己启动的 gateway 冲突，
        # 结果只会打印 "A Gateway is running for this state directory" 后直接退出。
        "tui",
        "--session", session_key,
        # chat 里可能直接发起制作层/跨层编排，给足制作层预算，避免长任务被 turn 超时掐断（O2）。
        # 超时统一走 easel/timeouts.py（三入口单一真相源），毫秒 = TIMEOUT_CHAT * 1000。
        "--timeout-ms", str(TIMEOUT_CHAT * 1000),
    ]

    # 画像作为初始消息内联注入（无全局 USER.md，避免并发竞态；与 web/skill 同源）。
    # 说明：注入随 session 历史留存，超长会话被压缩后可能丢画像——换取「每个请求自包含」，
    # 与 docs/prompt-stack.md 声明的架构一致。
    prefix = persona_prefix(selected_persona)
    if prefix:
        cmd += ["--message", prefix]

    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), env=proxy_env())

    return result.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="easel",
        description="Easel — CLI quy trình nội dung mạng xã hội",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # chat
    p_chat = sub.add_parser("chat", help="Trò chuyện tương tác (phiên mới)")
    p_chat.set_defaults(func=cmd_chat)

    # doctor
    p_doctor = sub.add_parser("doctor", help="Kiểm tra môi trường")
    p_doctor.set_defaults(func=cmd_doctor)

    # gateway
    p_gw = sub.add_parser("gateway", help="Quản lý OpenClaw gateway")
    p_gw.add_argument("action", choices=["start", "stop", "restart", "status", "logs"],
                       default="status", nargs="?")
    p_gw.set_defaults(func=cmd_gateway)

    # ping
    p_ping = sub.add_parser("ping", help="Kiểm tra kết nối")
    p_ping.set_defaults(func=cmd_ping)

    # skill
    p_skill = sub.add_parser("skill", help="Chạy SKILL (tự định tuyến)")
    p_skill.add_argument("name", help="Tên SKILL")
    p_skill.add_argument("--input", "-i", required=True, help="Nội dung đầu vào")
    p_skill.add_argument("--profile", "-p", default=None, help="Tên hồ sơ")
    p_skill.set_defaults(func=cmd_skill)

    # web
    def cmd_web(args):
        port = getattr(args, "port", 7860)
        env = proxy_env()
        env["EASEL_PORT"] = str(port)
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "web" / "app.py")],
            cwd=str(PROJECT_ROOT),
            env=env,
        )
        return 0

    p_web = sub.add_parser("web", help="Chạy giao diện web")
    p_web.add_argument("--port", type=int, default=7860, help="Cổng (mặc định 7860)")
    p_web.set_defaults(func=cmd_web)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
