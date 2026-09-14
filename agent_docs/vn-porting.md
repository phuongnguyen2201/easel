# Porting map — Vietnam fork

Scope: keep the engine, replace the China-platform layers. Every path below
was read in the analysis session; effort labels are estimates.

## Keep as-is

- `easel/` (CLI, persona, timeouts, OpenClaw argv), `openclaw/sync.sh`,
  `scripts/gateway.*`, `scripts/session_heal.py`.
- Contracts: `manifest.py`, `output_paths.py`, `content_guard.py`, `login_state.py`.
- Produce-layer media scripts in `skills/shared/scripts/` (ffmpeg/Pillow/opencv based).
- Web app structure, SSE streaming, profile pages.

## Language-locked code (must change before anything else)

| Item | File | Change |
|---|---|---|
| Trigger-phrase regex | `scripts/validate_skills.py` `TRIGGER_RE` | Add Vietnamese phrases or make the list locale-configurable |
| Profile prefix and turn reminder | `easel/persona.py` `persona_prefix`, `TURN_REMINDER` | Vietnamese text; keep the `profiles/<name>/memory.md` scoping sentence |
| System prompt | `openclaw/workspace/SOUL.md`, `AGENTS.md` | Translate; keep rule numbering and the appended runtime-root block from `sync.sh` |
| Chinese NLP | `skills/openclaw/skill-comment-insights/scripts/comment_insights.py` (jieba, snownlp) | Vietnamese tokenizer/sentiment; drop the two deps from `pyproject.toml` |
| Internal-network leftovers | `_proxy_env()` in `easel/cli.py` and `web/app.py`; `internal-host` patterns in `content_guard.py` | Remove Xiaohongshu domains; read `no_proxy` from env |
| SKILL descriptions | all 112 `SKILL.md` | Translate `description` (routing depends on it) and bodies; 80–300 chars stays |
| Card fonts | `card-design`, `render_card.py` | Fonts with full Vietnamese diacritics |

## Replace by layer

- Discover (9): `skill-trending-topics`, `skill-news-intelligence`,
  `skill-algorithm-updates`, `skill-event-calendar` read Chinese hot lists
  and holidays (`skills/shared/hotlist-apis.md`). Rebuild sources; keep
  `skill-rss-aggregator`, `skill-competitor-analysis`, `skill-content-gap-analysis` prompts.
- Plan (16): prompts portable; rewrite `references/` that encode 618/Double-11
  and XHS formats (`skill-campaign-planner`, `skill-content-calendar`).
- Produce (50): portable. Video providers in `.env.example` are
  `dashscope | ark | kling | openai-compatible | xhs-maas | agnes`; only
  `openai-compatible` is non-Chinese. Voice: `gemini` and `openai-compatible`
  cover Vietnamese; `edge-tts` fallback has vi-VN voices (not verified in code).
  `chart-visualization` calls an AntV API over the network — check reachability.
- Publish (20): all runners in `LOGIN_RUNNERS` (`web/app.py`) target
  xiaohongshu, kuaishou, weixin-channels, zhihu, bilibili, douyin. Douyin is
  not TikTok; `douyin_publish.py` does not transfer. Build new runners per
  `agent_docs/skills.md` → "Adding a publisher", preferring official APIs
  (Meta Graph, TikTok Content Posting, YouTube Data, Zalo OA) over Playwright.
  Portable: `skill-publish-scheduler`, `skill-publish-notify`,
  `skill-short-link`, `skill-persona-check`, `skill-publish-checklist`.
  `skill-quality-gate` needs a Vietnamese sensitive-word and ad-law list.
- Attribute (11): `skill-xhs-analyzer`, `skill-my-account`,
  `account_stats.py`, `social_stats.py` read Chinese platforms — replace
  with platform analytics APIs. Keep `skill-content-postmortem`,
  `roi-calculator`, `skill-data-tracker`, `skill-publish-analytics`.

## Dependency cleanup

Remove `biliup`, `jieba`, `snownlp` from `pyproject.toml`; move
`playwright`, `rembg`, `faster-whisper`, `librosa`, `opencv-python` into a
`media` extra so the README's `pip install -e ".[media]"` becomes true.
Pin `openclaw` in `setup.sh` (currently `@latest`; web needs ≥ 2026.9.x).

## Before exposing the web app

Add an auth token middleware and default `host=127.0.0.1` in `web/app.py`;
block `SYSTEM_DIRS` in `_safe_output_path` so `outputs/_login/*` is not
served by `/api/media`. Legal review items (not legal advice): Nghị định
147/2024 (social-network management) and Nghị định 13/2023 (personal data)
for profile and comment data stored in `profiles/` and `outputs/`.

## Suggested order

1. Language-locked code table above; run `python scripts/validate_skills.py`.
2. Dependency cleanup; `bash setup.sh` on a clean machine.
3. One publisher end-to-end (Facebook Page via Graph API) through
   `login_state.py` + `content_guard.py`; wire into `LOGIN_RUNNERS`.
4. Discover sources; then translate Plan/Produce references in usage order.
5. Attribute analytics last — they depend on the publishers' data access.
