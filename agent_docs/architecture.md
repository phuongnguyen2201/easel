# Architecture

## Request flow (all three entry points)

1. Build the message. `easel/persona.py` prepends
   `我当前使用的画像是「<profile>」…` when a profile exists; `chat_turn_message`
   also appends `TURN_REMINDER` (hidden from the user, tells the agent to route
   to a SKILL first and never leak secrets into public copy).
2. Shell out: `openclaw_base_cmd() + ["--profile", "easel", "agent", "--agent", "main",
   "--message", ...]` with `cwd=PROJECT_ROOT` and `_proxy_env()`.
   - `easel chat` is the exception: it runs `openclaw --profile easel tui --session <key>`
     and passes the profile prefix as `--message`; `chat`/`terminal` subcommands
     force local mode and collide with the running gateway (`easel/cli.py`).
3. OpenClaw loads the prompt stack (`docs/prompt-stack.md`): `SOUL.md`,
   `AGENTS.md` (+ runtime root appended by `sync.sh`), `CONTEXT.md`, then the
   triggered `SKILL.md` and its `references/`.
4. The agent `cd`s to the project root and runs `skills/shared/scripts/*.py`
   or `skills/openclaw/<skill>/scripts/*`, writing to `outputs/<topic>/`.

## Streaming and sessions (web)

- `POST /api/chat/stream` sets `OPENCLAW_RAW_STREAM=1` and a per-turn
  `OPENCLAW_RAW_STREAM_PATH`; a supervisor task tails that jsonl and forwards
  `token` / `thinking` / `question` SSE events. Client disconnects do not kill
  the agent; `GET /api/chat/last/{session_id}` recovers the answer.
- Session keys: web uses `web-<ms>`; transcripts live in
  `~/.openclaw-easel/agents/main/sessions/<id>.jsonl`.
- Before every turn `_heal_openclaw_session()` runs `scripts/session_heal.py`
  to strip unsigned thinking blocks. `--thinking` defaults to `low`
  (`EASEL_THINKING_LEVEL`).
- `ask_user` questions are bridged by polling the gateway WebSocket RPC in
  `easel/gateway_questions.py` (Ed25519 device signing, `websocket-client`);
  the bridge trips a process-level breaker on connect failure or an old
  OpenClaw version.

## Gateway

`scripts/gateway.sh start` runs
`openclaw --profile easel gateway run --force --allow-unconfigured --bind loopback`
(port from `OPENCLAW_PORT`, default 18789), logging to `/tmp/easel-gateway.log`.
`scripts/gateway.ps1` is the Windows twin. Profile isolation:
workspace `~/.openclaw/workspace-easel/`, config `~/.openclaw-easel/openclaw.json`.

## State on disk

| Path | Content | Writer |
|---|---|---|
| `profiles/<name>/{identity,style,audience,platforms,preferences,memory}.md` | Six-dimension profile; concatenated in `_FILE_ORDER` | web `PUT /api/persona/{name}/file`, agent |
| `outputs/<topic>/` + `.easel.json` | Deliverables, `assets/`, manifest with `steps[]` | skills via `manifest.py` |
| `outputs/_schedule.json`, `outputs/_ideas.json` | Calendar and ideas | `web/app.py` |
| `outputs/_login/<platform>.{json,png,log,code}` | Login state machine, QR, SMS code | login runners |
| `outputs/_publish/`, `outputs/_publish.log` | Async publish status, publish log | `web/app.py` |
| `cookies.json` (project root) | Bilibili cookies for `biliup` | `bili_login.py` |
| `~/.openclaw/workspace-easel/` | Synced skills, `shared/`, symlinks `outputs/`, `easel-profiles/` | `openclaw/sync.sh` |

`sync.sh` symlinks `workspace/outputs` → `outputs/` so agent writes land in the
project, and `workspace/easel-profiles` → `profiles/`.

## Module boundaries

- `easel/` — CLI, persona, timeouts, OpenClaw argv resolution. No business logic.
- `web/app.py` — one module: routes, subprocess orchestration, SSE, login and
  publish dispatch, JSON storage, env registry (`SKILL_API_REQUIREMENTS`).
- `skills/openclaw/<skill>/` — 112 skills, 30 with their own `scripts/`.
- `skills/shared/scripts/` — 46 deterministic scripts (media ops, publishers,
  guard, manifest, model registry). See `agent_docs/skills.md`.
- `scripts/` — validators, gateway control, session heal, MaaS adapters.
