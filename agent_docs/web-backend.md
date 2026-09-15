# Web backend (`web/app.py`)

Single FastAPI module, 2,658 lines, started by `easel web` as
`python web/app.py` with `EASEL_PORT`. `uvicorn.run(host="0.0.0.0")`,
`docs_url=None`, CORS `allow_origins=["*"]`. There is no authentication on
any route.

## Route groups

| Prefix | Purpose | Notes |
|---|---|---|
| `/`, `/assets/*`, `/static/*` | React `frontend/dist` if built, else legacy `web/static/index.html` | Path-traversal guarded. `/onepage` (trang giới thiệu TQ) đã retire vào `retired/web-static/` cùng `main.html`, `showcase/` |
| `/api/status`, `/api/personas`, `/api/persona/{name}[/files|/file]` | Gateway check, profile CRUD | `PUT …/file` atomic write; `DELETE` removes the directory |
| `/api/skills`, `/api/skill/{name}`, `/api/env` | Skill list/detail with masked key status; write keys to `.env` | Writes limited to `_ENV_ALLOWLIST` |
| `/api/chat/stream`, `/api/chat/last/{id}`, `/api/chat/jobs/{turn}/stream`, `/api/chat/stop`, `/api/chat/question/*` | SSE chat, recovery, stop, ask_user bridge | See `agent_docs/architecture.md` |
| `/api/chat`, `/api/skill` | Non-streaming turn / direct skill run | `subprocess.run` with `TIMEOUT_*` |
| `/api/outputs`, `/api/output/{path}`, `/api/media/{path}`, `DELETE /api/output/{path}`, `/api/upload` | Content library | Delete refuses `PROTECTED_OUTPUTS`; `/api/media` does not |
| `/api/accounts`, `/api/login/{platform}[/status|/sms]`, `/api/accounts/{platform}/whoami`, `/api/logout/{platform}` | Platform login runners | Table `LOGIN_RUNNERS` |
| `/api/analytics/*` | Per-platform stats via `account_stats.py` / `social_stats.py` | |
| `/api/publish/{platform}[/status|/sms]` | Real publish (`--exec`) | Confirmation only in the frontend |
| `/api/profile/build[/status/{name}]` | Profile builder job | Writes `outputs/_profile_build/` |
| `/api/trends`, `/api/schedule*`, `/api/ideas*` | Hot lists, calendar, ideas | JSON files under `outputs/` |
| `DELETE /api/session/{key}` | Remove an OpenClaw transcript | |

## Login runner protocol

`POST /api/login/{platform}` spawns a background Python process
(`xhs_publish.py login`, `bili_login.py login`, `douyin_publish.py login`, or
`web_publisher.py login-qr --platform <wp>`), writing
`outputs/_login/<platform>.json` with states
`starting → qr_ready → [scanned] → [sms_required → verifying] → success | expired | error`
(`login_state.py`). The frontend polls `/status`; `/sms` writes
`outputs/_login/<platform>.code`, which the runner consumes once.
`LOGIN_TIMEOUT` is 240 s. Processes are tracked in `LOGIN_PROCESSES`.

## Publish dispatch

`api_publish` validates media (image xor video, `MEDIA_REQUIRED`,
`VIDEO_ONLY_PUBLISH`), then:

- `xiaohongshu` → `xhs_publish.py publish|publish-video --no-proxy … --exec`
- `bilibili` → `biliup -u cookies.json upload <video> --tid 36 --copyright 1 --tag …`
- `douyin` → async (`_start_async_publish`) because of SMS walls; status in `outputs/_publish/douyin.json`
- others → `web_publisher.py publish --platform <wp> … --exec`

Runs with `_publish_env()` (`EASEL_CALENDAR_AUTORECORD=0`, because the web
layer appends to `_schedule.json` itself). Output tails go to
`outputs/_publish.log`. Timeout 600 s.

## Storage helpers

`_read_schedule/_write_schedule`, `_read_env/_write_env` (atomic, allowlisted),
`_safe_output_path` (files only, traversal check), `_safe_output_target`
(dirs allowed, root refused), `_is_protected`. File locks use `fcntl`
(`msvcrt` on Windows).

## Env registry

`SKILL_API_REQUIREMENTS` maps skills to required env keys built with `_k()`
and `model_group()` from `skills/shared/scripts/model_registry.py`; the Skill
Library page renders masked status from `_api_spec_status`.
