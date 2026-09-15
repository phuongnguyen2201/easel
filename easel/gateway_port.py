"""Gateway port — single source of truth for the loopback gateway endpoint.

Resolution order (first hit wins):
  1. ``EASEL_GATEWAY_PORT`` in the environment — explicit per-shell override.
  2. ``OPENCLAW_PORT`` in the project ``.env`` (last occurrence, as the shell
     reader in ``scripts/gateway.sh`` does).
  3. ``DEFAULT_PORT`` — OpenClaw's own default.

This value must match ``gateway.port`` in the OpenClaw profile config
(``~/.openclaw-easel/openclaw.json``). That config decides both what the
gateway binds and where ``openclaw --profile easel agent`` connects, so moving
the port here alone only moves the health checks::

    openclaw --profile easel config set gateway.port <port>

Read once per process; editing ``.env`` needs a restart of the reader. There is
no python-dotenv dependency in this project, hence the hand-rolled parse (same
shape as the ``.env`` reader in ``easel/commands/doctor.py``).
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

# easel/gateway_port.py -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_PORT = 18789
ENV_OVERRIDE = "EASEL_GATEWAY_PORT"
DOTENV_KEY = "OPENCLAW_PORT"


def _coerce(value: str | None) -> int | None:
    """A plausible TCP port, or None. Never raises on junk input."""
    if not value:
        return None
    cleaned = value.strip().strip('"').strip("'").strip()
    try:
        port = int(cleaned)
    except ValueError:
        return None
    return port if 1 <= port <= 65535 else None


def _from_dotenv() -> int | None:
    """Read OPENCLAW_PORT out of the project .env; last assignment wins."""
    try:
        lines = (PROJECT_ROOT / ".env").read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    found: int | None = None
    for line in lines:
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == DOTENV_KEY:
            found = _coerce(value) or found
    return found


@lru_cache(maxsize=1)
def gateway_port() -> int:
    return _coerce(os.environ.get(ENV_OVERRIDE)) or _from_dotenv() or DEFAULT_PORT


def gateway_url(path: str = "/healthz") -> str:
    """Loopback gateway URL, e.g. http://127.0.0.1:18789/healthz."""
    return f"http://127.0.0.1:{gateway_port()}{path}"
