# Adapter design — facebook-page (runbook 5, step 1)

Status: implemented (script, skill, web registration, tests); not yet run against a live Meta app.
Additions vs. the original design: `pages [--set-default ID]` subcommand, `publish --offline`, default Graph version `v23.0`. Platform code `facebook-page`, script
`skills/shared/scripts/facebook_publish.py`, skill `skill-facebook-page-upload`.

Evidence labels: **Observed** = read in this repo (commit `73de7e5`).
**External** = Meta documentation / general knowledge; re-check the official
docs before coding (versions, permissions and limits change).

## 1. Contracts this adapter plugs into (Observed)

| Contract | File | What the adapter must do |
|---|---|---|
| Login state file | `login_state.py` `write_status(path, state, message, qr)` | Atomic JSON `{state,message,qr,ts}`; states `starting, qr_ready, scanned, sms_required, verifying, success, expired, error` |
| QR image | `web/app.py` `_login_status` | Any file at `outputs/_login/<platform>.png` is returned as `qr` + `qrTs` (mtime cache key) |
| Runner lifecycle | `api_login_start` (pre-4.3 version in `git show 73de7e5`) | Deletes old `.png`/`.json`, `Popen`s runner with log `outputs/_login/<platform>.log`, polls 0.5 s × 50 until `qr`/`qr_ready`/terminal state; `LOGIN_TIMEOUT = 240` |
| Crash detection | `_login_status` | Runner exiting while state is `unknown`/`starting` → UI shows `error` with exit code |
| whoami | `api_account_whoami` | Last stdout line JSON `{loggedIn,name,avatar[,error]}`; `error` = not confident, not cached |
| Logout | `api_logout` | `rmtree(BROWSER_PROFILES / cfg['profile'])` + removes `outputs/_login/<platform>{.json,.png,-me.png,.code}` |
| Publish (sync) | pre-4.3 `api_publish` | `subprocess.run(... --exec, env=_publish_env(), timeout=600)`; rc 0 = ok; last 8 lines of stderr→detail; appends `_publish.log`; web writes `_schedule.json` itself |
| Content guard | `content_guard.guard_or_die(parts, exec_mode=, allow_unsafe=, label=)` | BLOCK categories exit 7 only when `exec_mode and not allow_unsafe`; dry-run only warns |
| Calendar | `calendar_ops.record_publish(platform, title, url, ptype, tags, note, source)` | No-op when `EASEL_CALENDAR_AUTORECORD=0` (web sets it); never raises |
| Manifest | `manifest.py record --topic --layer publish --skill --outputs --summary` | CLI only (no importable API besides `cmd_*`); `LAYERS` includes `publish` |
| Output paths | `output_paths.validate_output_path(p, allow_system=True)` | `_login`, `_publish` are in `SYSTEM_DIRS` |
| Validator | `scripts/validate_skills.py` `PUBLISH_SCRIPT_CONTRACTS` (empty dict) | Needs markers `content_guard.guard_or_die` and `add_argument("--exec"` |

Frontend `AccountsPage.tsx` (Observed, read for this doc): renders
`<img>` when `state == 'qr_ready' && qr`, shows `STATE_LABEL[state] — message`,
stops polling on `success|expired|error`, calls whoami after `success`. No
frontend change is needed for the flow below.

## 2. OAuth → QR state machine

### Choice: Facebook Login for Devices (External)

A web-redirect OAuth flow needs a callback URL reachable from the phone that
scans the QR; `easel web` binds a LAN/localhost address with no auth and no
callback route, and Meta requires registered HTTPS redirect URIs. The device
flow needs no callback, so the runner stays a self-contained polling process —
the same shape as the retired Playwright runners.

Device flow (External, developers.facebook.com/docs/facebook-login/for-devices):

1. `POST https://graph.facebook.com/<ver>/device/login`
   `access_token=<APP_ID>|<CLIENT_TOKEN>&scope=<csv>` →
   `{code, user_code, verification_uri, expires_in (~420), interval (~5)}`.
2. Poll `POST .../device/login_status` `access_token=...&code=<code>` every
   `interval` s. Error subcodes: `1349174` pending, `1349172` polling too fast
   (back off), `1349152` code expired. Success → `{access_token, expires_in}`
   (docs: device tokens "may be valid for up to 60 days").
3. `GET /me?fields=id,name,picture` and `GET /me/accounts?fields=id,name,access_token,picture`
   → Page tokens.

**Open risk (must verify first):** the scope must contain permissions approved
for the app. Whether `pages_show_list`, `pages_manage_posts`,
`pages_read_engagement` are grantable through device login was not confirmed
from the docs page. Test with an app in Development mode and a Page the app
admin manages before writing the runner. Fallback if refused: `login --token`
(paste a user token from Graph API Explorer; the runner skips steps 1–2 and
does step 3) — same state file, no QR.

### State mapping

| login_state | When | `message` (Vietnamese, user-facing) | Files |
|---|---|---|---|
| `starting` | runner started, before `/device/login` returns | `Đang tạo mã đăng nhập Facebook…` | `.json` |
| `qr_ready` | code received; QR written | `Quét mã hoặc mở facebook.com/device, nhập mã: <user_code>` | `.png`, `.json` |
| `scanned` | not used — Meta gives no "opened" signal, only pending | — | — |
| `sms_required` / `verifying` | not used — 2FA happens on facebook.com | — | — |
| `verifying` (optional) | token received, fetching `/me/accounts` | `Đang lấy danh sách Trang…` | — |
| `success` | token file written, ≥1 Page | `Đã kết nối: <page name>` (or `<n> Trang, mặc định: <name>`) | token file |
| `expired` | subcode `1349152`, or `--timeout` reached | `Mã đã hết hạn, vui lòng thử lại` | — |
| `error` | HTTP/Graph error, no Page, missing env | Graph `error.message` shortened, or `Thiếu FB_APP_ID/FB_CLIENT_TOKEN trong .env` | — |

Note `verifying` is shown by the frontend as a spinner; using it is optional.

Timeout: effective deadline = `min(--timeout, expires_in)`. Web passes
`LOGIN_TIMEOUT` (240 s), shorter than `expires_in` (~420 s), so web users hit
`expired` at 240 s — acceptable; CLI default can be `expires_in`.

### QR rendering with segno

`segno` is not installed (checked: `import segno` fails on this machine) and
was removed from dependencies in runbook 4.1. Re-add `"segno>=1.6,<2"` in
`pyproject.toml` when implementing (that file is outside this doc task).

```python
target = f"{verification_uri}?user_code={user_code}"   # prefill param: External, unverified
qr_path = validate_output_path(args.qr_out, allow_system=True, create_parent=True)
segno.make(target, error="m").save(str(qr_path), kind="png", scale=8, border=2)
write_status(args.status_file, "qr_ready", f"... {user_code}", qr=f"_login/{qr_path.name}")
```

Always print `user_code` in `message` even if the prefill parameter works,
so the flow survives if Meta ignores it. Write the PNG before the status so the
backend never sees `qr_ready` without a file.

### Token storage

Tokens must not live under `outputs/`: `_safe_output_path` (web/app.py) does
not block `SYSTEM_DIRS`, so `/api/media` would serve `outputs/_login/*`
(vn-porting.md, "Before exposing the web app"). Store in
`~/.easel-browser-profiles/FacebookPageProfile/token.json`, mode `0600`:

```json
{"user": {"id": "...", "name": "...", "token": "...", "obtained": 1726..., "expires_in": 5183944},
 "pages": [{"id": "...", "name": "...", "token": "...", "picture": "..."}],
 "default_page_id": "..."}
```

Reasons: `LOGIN_RUNNERS['facebook-page']['profile'] = 'FacebookPageProfile'`
makes the existing `api_logout` delete it with no new code, and
`content_guard` already flags the `.easel-browser-profiles` path as
`internal-path` (BLOCK). Override with `--token-file` for tests.

## 3. CLI — `skills/shared/scripts/facebook_publish.py`

Stdlib `urllib` for HTTP (no `requests` dependency assumed), `segno` imported
lazily inside `login` only. Every subcommand prints one JSON object as the
last stdout line; human messages go to stderr.

### Common options (all subcommands)

| Flag | Default | Notes |
|---|---|---|
| `--token-file PATH` | `~/.easel-browser-profiles/FacebookPageProfile/token.json` | |
| `--graph-version vXX.0` | env `FB_GRAPH_VERSION`, else a constant in the script | Pin; do not float |
| `--no-proxy` | off | Otherwise honours env proxy like other runners |

### `login`

| Flag | Default | Notes |
|---|---|---|
| `--qr-out PATH` | `outputs/_login/facebook-page.png` | via `validate_output_path(allow_system=True)` |
| `--status-file PATH` | none (skip) | `login_state.write_status` skips on empty path |
| `--timeout SEC` | `expires_in` from Meta | web passes 240 |
| `--scope CSV` | `pages_show_list,pages_manage_posts,pages_read_engagement` | see open risk |
| `--page-id ID` | first Page returned | sets `default_page_id` |
| `--token USER_TOKEN` | — | fallback path, skips device flow |

Exit: 0 success, 3 expired, 1 error, 2 argparse. Stdout:
`{"ok": true, "pages": [{"id","name"}], "default_page_id": "..."}`.

### `whoami`

`--page-id ID` optional. Calls `GET /<page-id>?fields=name,picture{url}` with
the Page token. Stdout `{"loggedIn": bool, "name": "...", "avatar": "<url>"}`;
on network failure add `"error": "..."` so the backend does not cache a false
negative. Token file missing → `{"loggedIn": false}` without `error`.

### `publish`

| Flag | Required | Maps to |
|---|---|---|
| `--title TEXT` | no | video: `title`; text/photo: prepended as first line of `message` unless `--content` already starts with it |
| `--content TEXT` | one of title/content | `message` (text, photo) / `description` (video) |
| `--tags CSV` | no | appended as `#tag` line; strip spaces and `#`, keep Vietnamese letters |
| `--images a.png,b.jpg` | no | 1 image → `POST /<page>/photos` (`source` multipart, `message`); ≥2 → each `photos` with `published=false`, then `POST /<page>/feed` with `attached_media=[{"media_fbid":...}]` |
| `--video v.mp4` | no, exclusive with `--images` | `POST /<page>/videos` (`source`, `title`, `description`); resumable upload for large files is a later step |
| `--link URL` | no | `link` on `/feed` (text-only posts) |
| `--page-id ID` | no | default `default_page_id` from token file |
| `--topic NAME` | no | after success: `manifest.py record --topic NAME --layer publish --skill skill-facebook-page-upload --summary <post url>` (subprocess, best-effort) |
| `--exec` | — | without it: dry-run |
| `--allow-unsafe` | — | passed to `guard_or_die` |

No media and no `--link` → `POST /<page>/feed` with `message`.

Validation before any network call (exit 5): both `--images` and `--video`;
missing file; extension not in the image/video sets used by `web/app.py`;
empty title+content.

Order in `--exec` (fixed):
1. arg + media validation
2. `guard_or_die([title, content, tags, link], exec_mode=args.exec, allow_unsafe=args.allow_unsafe, label="Nội dung đăng Facebook")` → exit 7 on BLOCK
3. load token, resolve page (exit 3 if missing)
4. upload / post
5. `calendar_ops.record_publish("facebook-page", title, url, ptype, tags, note=content[:200])` — no-op under web
6. optional manifest record
7. stdout `{"ok": true, "post_id": "...", "url": "https://www.facebook.com/<post_id>", "dry_run": false}`

Exit codes: 0 ok · 1 unexpected · 2 argparse · 3 not logged in / Graph
`code 190` (token invalid/expired) · 4 permission (`code 10`, `200`–`299`) ·
5 input/media invalid · 6 Graph rate limit (`code 4`, `17`, `32`, `613`) ·
7 content guard. Error text on stderr in Vietnamese, with Graph `fbtrace_id`
for support; never print tokens (mask like `content_guard._mask`).

Validator lines to add when implementing:

```python
PUBLISH_SCRIPT_CONTRACTS = {
    "skills/shared/scripts/facebook_publish.py": ("content_guard.guard_or_die", 'add_argument("--exec"'),
}
```

## 4. Env and `SKILL_API_REQUIREMENTS`

`.env` keys (append to `.env.example` too):

| Key | Required | Secret | Purpose |
|---|---|---|---|
| `FB_APP_ID` | yes | no | device login `access_token` prefix |
| `FB_CLIENT_TOKEN` | yes | yes | App Dashboard → Settings → Advanced → Client token (External) |
| `FB_PAGE_ID` | no | no | default Page when the account manages several |
| `FB_GRAPH_VERSION` | no | no | pin Graph version |

No app secret is needed for the device flow; do not add `FB_APP_SECRET`
unless a later token-exchange step is designed.

Entry (key = skill folder name, as `d.name in SKILL_API_REQUIREMENTS` at
web/app.py L307/L719 expects):

```python
"skill-facebook-page-upload": {
    "label": "Đăng Trang Facebook (Meta Graph API)",
    "providers": [{
        "id": "facebook-page",
        "name": "Ứng dụng Meta — Đăng nhập thiết bị",
        "keys": [
            _k("FB_APP_ID", "App ID của ứng dụng Meta", secret=False),
            _k("FB_CLIENT_TOKEN", "Client token (Cài đặt → Nâng cao)"),
            _k("FB_PAGE_ID", "ID Trang mặc định (tuỳ chọn)", required=False, secret=False),
            _k("FB_GRAPH_VERSION", "Phiên bản Graph API (tuỳ chọn, vd v23.0)", required=False, secret=False),
        ],
    }],
},
```

Effects (Observed): the loop after the dict adds all four to `_ENV_ALLOWLIST`,
so `/api/env` can write them. `content_guard.load_env_literals` already treats
names matching `_TOKEN` as sensitive, so the literal `FB_CLIENT_TOKEN` value is
scanned; `FB_APP_ID` is not (not secret). Adding `FB_CLIENT_TOKEN` to the
`env-name` regex in `content_guard.py` is optional and a separate task.

## 5. Web registration (for the implementation task)

```python
LOGIN_RUNNERS["facebook-page"] = {
    "name": "Facebook Page", "backend": "graph", "profile": "FacebookPageProfile",
    "mediaRequired": False, "videoOnly": False,
    "titleLimit": 255,        # video title; External, verify
    "bodyLimit": 63206,       # post message; External, verify
    "hint": "Đăng qua Meta Graph API, cần quyền quản trị Trang",
}
```

- `api_login_start`: restore the pre-4.3 body (clear files, `Popen`, poll) with
  a `backend == 'graph'` branch:
  `[py, SHARED_SCRIPTS/'facebook_publish.py', 'login', '--qr-out', qr, '--status-file', status, '--timeout', str(LOGIN_TIMEOUT)]`.
- `api_account_whoami`: add `elif backend == 'graph'` →
  `facebook_publish.py whoami`; the current `else` falls through to the retired
  `web_publisher.py`.
- `api_publish`: sync path (no SMS wall):
  `[py, facebook_publish.py, 'publish', '--content', req.body, '--tags', tags, '--exec']`
  + `--title` only when `req.title.strip()` (the old code fabricates a title from
  `body[:20]`, which would duplicate text on Facebook) + `--images ','.join(imgs)`
  or `--video vids[0]`. Keep the old `_publish.log` and `_schedule.json` writes.
- `calendar_ops.PLATFORM_NAMES`: add `"facebook-page": "Facebook Page"` so
  agent-side records match the web's `cfg['name']`.
- `/api/accounts` returns the new fields (runbook 4.3 table) — not done yet.

Files the implementation will touch (ask before each is edited):
`skills/shared/scripts/facebook_publish.py` (new),
`skills/openclaw/skill-facebook-page-upload/SKILL.md` (new), `web/app.py`,
`scripts/validate_skills.py`, `skills/shared/scripts/calendar_ops.py`,
`pyproject.toml`, `.env.example`, `docs/skill-function-mapping.md`,
`tests/` (pure functions: message assembly, tag formatting, Graph error → exit code).

## 6. Dry-run → `--exec` scenario

Preconditions: Meta app in Development mode, the tester is app admin and Page
admin, `FB_APP_ID`/`FB_CLIENT_TOKEN` in `.env`, test Page (not production).

```bash
# 0. contract checks
python scripts/validate_skills.py
python scripts/validate_skill_commands.py
pytest tests/ -q

# 1. login from CLI (QR + code on stderr/status file)
python skills/shared/scripts/facebook_publish.py login \
  --status-file outputs/_login/facebook-page.json
cat outputs/_login/facebook-page.json          # expect state=success
python skills/shared/scripts/facebook_publish.py whoami   # loggedIn=true

# 2. dry-run: guard warns only, no POST; token + page read-only GET allowed
python skills/shared/scripts/facebook_publish.py publish \
  --title "Thử nghiệm" --content "Bài test ầ ữ ỡ" --tags "easel,test"
#   expect rc 0, stdout {"ok":true,"dry_run":true,"endpoint":"/<page>/feed",...}

# 3. guard check: BLOCK content must fail only with --exec
python skills/shared/scripts/facebook_publish.py publish --content "key sk-abcdefghijklmnopqrst" ; echo rc=$?   # 0, warning
python skills/shared/scripts/facebook_publish.py publish --content "key sk-abcdefghijklmnopqrst" --exec ; echo rc=$?   # 7, nothing posted

# 4. real posts on the test Page, one per media type
python skills/shared/scripts/facebook_publish.py publish --content "Text only" --exec
python skills/shared/scripts/facebook_publish.py publish --content "1 ảnh" --images outputs/<topic>/a.png --exec
python skills/shared/scripts/facebook_publish.py publish --content "2 ảnh" --images outputs/<topic>/a.png,outputs/<topic>/b.png --exec
python skills/shared/scripts/facebook_publish.py publish --title "Video" --content "mô tả" --video outputs/<topic>/v.mp4 --exec

# 5. side effects (agent path: autorecord on)
python - <<'PY'
import json; print(json.load(open("outputs/_schedule.json"))[-1])
PY

# 6. autorecord off (web path) must not add a calendar row
EASEL_CALENDAR_AUTORECORD=0 python skills/shared/scripts/facebook_publish.py publish --content "no calendar" --exec

# 7. web: bash openclaw/sync.sh; easel web → Accounts → Facebook Page → login
#    → Publish → confirm → tail -n 30 outputs/_publish.log → Logout removes token dir
```

Pass criteria: each `--exec` returns a `post_id` visible on the Page; step 3
exit 7 posts nothing; step 6 leaves `_schedule.json` length unchanged by the
script (web adds its own row); after Logout `whoami` returns `loggedIn:false`.

Delete test posts manually on the Page afterwards (no delete subcommand in scope).
