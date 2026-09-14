# Easel — Claude Code guide

Easel is a social-media content workbench: three entry points (`easel chat`,
`easel skill`, the FastAPI web app) each build a message and shell out to
`openclaw --profile easel agent --agent main`. OpenClaw reads the 112 skills
synced into `~/.openclaw/workspace-easel/` and runs their scripts itself.
There is no database; all state is files under `outputs/`, `profiles/`, and
`~/.openclaw-easel/`.

Detail lives in `@agent_docs/architecture.md`, `@agent_docs/skills.md`,
`@agent_docs/web-backend.md`, and `@agent_docs/vn-porting.md`.

## Commands

| Command | What it does | Defined in |
|---|---|---|
| `bash setup.sh` | Installs Node/OpenClaw/ffmpeg, pip installs, builds frontend, runs sync | `setup.sh` |
| `easel web [--port 7860]` | Runs `web/app.py` via uvicorn | `easel/cli.py` |
| `easel chat` | Interactive OpenClaw TUI session with a chosen profile | `easel/cli.py` |
| `easel skill <name> -i "..." [-p <profile>]` | One skill run through the agent | `easel/commands/skill.py` |
| `easel doctor` / `easel ping` | Environment check / gateway connectivity | `easel/commands/` |
| `easel gateway start\|stop\|restart\|status\|logs` | Wraps `scripts/gateway.sh` | `easel/commands/gateway.py` |
| `bash openclaw/sync.sh` | Copies skills + workspace into the OpenClaw profile | `openclaw/sync.sh` |
| `python scripts/validate_skills.py` | Frontmatter, links, output/publish contract check | `scripts/validate_skills.py` |
| `python scripts/validate_skill_commands.py` | Script argparse vs SKILL.md command drift | `scripts/validate_skill_commands.py` |
| `pytest tests/ -q` | 49 unit tests (pure functions) | `pytest.ini`, `tests/` |
| `npm run dev` / `build` / `lint` (in `web/frontend/`) | Vite dev server / `tsc -b && vite build` / oxlint | `web/frontend/package.json` |

Run `bash openclaw/sync.sh` after any change under `skills/` or
`openclaw/workspace/`; the agent only sees the synced copy.

## Hard rules

- Project scripts run from the project root, never from the workspace copy.
  `sync.sh` appends the absolute root to `AGENTS.md`; `CONTEXT.md` repeats it.
- A SKILL.md frontmatter has only `name`, `description`, `layer`, and
  optionally `metadata`. `description` is 80–300 characters and must contain a
  trigger phrase matched by `TRIGGER_RE` in `scripts/validate_skills.py`.
  `name` equals the folder name (`INTENTIONAL_NAME_MISMATCHES` lists the one exception).
- Deliverables go to `outputs/<topic>/` root, intermediates to
  `outputs/<topic>/assets/`, metadata to `.easel.json` via
  `skills/shared/scripts/manifest.py`. New scripts call
  `validate_output_path()` from `skills/shared/scripts/output_paths.py`.
  System state uses `_`-prefixed dirs listed in `SYSTEM_DIRS` there.
- Any script that posts text to a public platform calls
  `guard_or_die()` from `skills/shared/scripts/content_guard.py` before
  `--exec`. Exit code 7 means blocked; `--allow-unsafe` overrides.
- Profiles are injected as a message prefix by `easel/persona.py`
  (`persona_prefix`, `chat_turn_message`). Do not write a workspace `USER.md`;
  `sync.sh` empties the global `MEMORY.md`. Account memory is only
  `profiles/<name>/memory.md`.
- Timeouts for all three entry points come from `easel/timeouts.py`.
- Invoke OpenClaw through `easel.openclaw_cmd.openclaw_base_cmd()` (Windows
  `.cmd` shim handling), never a bare `"openclaw"` string in new code.

## Environment

`.env` at the project root is the only config source the agent may trust
(`AGENTS.md`). Keys from `.env.example`: `ANTHROPIC_API_KEY`, `CLAUDE_MODEL`,
optional `EASEL_LLM_*` (Anthropic-compatible), `OPENAI_*`,
`EASEL_EMBEDDING_*`, `OPENCLAW_PORT`, and media providers
`VIDEO_PROVIDER`, `MUSIC_PROVIDER`, `VOICE_PROVIDER` with their
`*_API_KEY/_BASE_URL/_MODEL`. `web/app.py` writes keys via `/api/env`,
restricted to `_ENV_ALLOWLIST`. Runtime knobs: `EASEL_PROXY`,
`EASEL_THINKING_LEVEL` (default `low`), `EASEL_CALENDAR_AUTORECORD`.

## Gotchas

- `openclaw/openclaw.json5` is a stale template that `setup.sh` never applies;
  real config is written with `openclaw config set` into `~/.openclaw-easel/openclaw.json`.
- `setup.sh` installs `openclaw@latest` (unpinned) and requires Node >= 24.16
  (<25) or >= 26.1; `web/app.py` disables the ask_user question bridge on
  OpenClaw older than 2026.9.x.
- `openclaw agent` buffers stdout; the web app streams by tailing a per-turn
  jsonl written under `OPENCLAW_RAW_STREAM_PATH`.
- Session history is sanitized every turn by `scripts/session_heal.py`
  (unsigned thinking blocks break replay).
- `_proxy_env()` exists twice (`easel/cli.py`, `web/app.py`) and hardcodes
  Xiaohongshu domains in `no_proxy`.
- `pyproject.toml` has no optional extras; the README's `[media]` extra does not exist.
- `.gitignore` ignores `.claude/`, `profiles/*/` (except `_template`),
  `outputs/**`, `cookies.json`, `*.jsonl`. Un-ignore `.claude/commands/` to commit commands.
- The web server binds `0.0.0.0` with no authentication; keep it on a trusted network.
