"""Subprocess environment shared by the CLI, ``easel skill``, ``easel ping``
and the web app.

Single source of truth for the proxy variables handed to OpenClaw and to
publish/analytics scripts.  ``EASEL_PROXY`` feeds ``http_proxy``/``https_proxy``;
``EASEL_NO_PROXY`` (comma-separated hosts/patterns) feeds ``no_proxy`` and
defaults to loopback only — no platform domains are hardcoded here.
"""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_NO_PROXY = "localhost,127.0.0.1"


def proxy_env(base: dict[str, str] | None = None) -> dict[str, str]:
    """Return a copy of the environment with proxy settings applied.

    ``http_proxy``/``https_proxy``/``EASEL_ROOT`` use ``setdefault`` semantics,
    so values already in the environment win.  ``no_proxy`` is set explicitly
    when ``EASEL_NO_PROXY`` is given (an inherited shell ``no_proxy`` must not
    silently override the project's own setting); otherwise it defaults to
    loopback unless the shell already provides one.
    """
    env = dict(os.environ if base is None else base)
    env.setdefault("EASEL_ROOT", str(PROJECT_ROOT))
    proxy = os.environ.get("EASEL_PROXY", "")
    env.setdefault("http_proxy", proxy)
    env.setdefault("https_proxy", proxy)
    no_proxy = os.environ.get("EASEL_NO_PROXY", "").strip()
    if no_proxy:
        env["no_proxy"] = no_proxy
    else:
        env.setdefault("no_proxy", DEFAULT_NO_PROXY)
    return env
