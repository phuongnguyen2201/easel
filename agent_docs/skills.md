# Skills

Source of truth: `docs/SKILL-SPEC.md` (v0.3). This file records what the
validators actually enforce and the shared scripts a skill can call.

## Layout

```
skills/openclaw/<skill>/SKILL.md      required, < 200 lines
skills/openclaw/<skill>/references/   optional, loaded on demand
skills/openclaw/<skill>/scripts/      optional, never enters the prompt
skills/openclaw/<skill>/tests/        optional, test1.prompt + test1.expected
skills/shared/scripts/                cross-skill scripts (46 files)
skills/shared/references/             copy frameworks, hook formulas, voice casting
```

Layers (`layer:` field): `discover`, `plan`, `produce`, `publish`,
`attribute`, `general`. Counts: 9 / 16 / 50 / 20 / 11 / 6
(`docs/skill-function-mapping.md`).

## Validator rules (`scripts/validate_skills.py`)

- Allowed frontmatter keys: `name`, `description`, `layer`, `metadata`.
- `description` length 80–300; must match `TRIGGER_RE`
  (`当用户|触发|使用时机|适用场景|用户说|用户问|用户需要|用于`).
- `name` == folder name, except `skill-xhs-analyzer` → `redbook`.
- `LEGACY_OUTPUT_DIRS` lists old flat output folders the validator rejects.
- `scripts/validate_skill_commands.py` parses Python commands quoted in
  SKILL.md and checks paths/flags against each script's argparse.

## Shared scripts by concern

- Contracts: `manifest.py` (`meta`, `record`, `latest`, `read`),
  `output_paths.py` (`validate_output_path`, `SYSTEM_DIRS`), `content_guard.py`
  (`scan`, `redact`, `selftest`; exit 7 on BLOCK), `persona_gate.py`,
  `model_registry.py configured`, `login_state.py`, `calendar_ops.py`.
- Publishers: `xhs_publish.py`, `douyin_publish.py`, `web_publisher.py`
  (kuaishou, weixin-channels, zhihu), `bili_login.py` (+ `biliup` CLI),
  `zhihu_answer.py`, `xhs_comment.py`, `zhihu_comments_fetch.py`.
- Analytics: `account_stats.py`, `social_stats.py`.
- Media: `image_ops.py`, `img_enhance.py`, `remove_bg.py`, `render_card.py`,
  `meme_ops.py`, `mindmap.py`, `doc_convert.py`, `video_ops.py`, `reframe.py`,
  `highlight_cut.py`, `intro_outro.py`, `slideshow.py`, `beatsync.py`,
  `chromakey.py`, `audio_ops.py`, `audio_mix.py`, `audio_viz.py`, `asr.py`,
  `subtitle_ops.py`, `fix_timing.py`, `tts.py`, `multivoice.py`,
  `voice_clone.py`, `ai_image.py`, `ai_video.py`, `ai_music.py`,
  `batch_process.py`, `wordcount.py`.

## Manifest contract

```
python skills/shared/scripts/manifest.py meta   --topic <t> --title "..." --platform <p> --kind cards --status draft --deliverables a.png,b.png
python skills/shared/scripts/manifest.py record --topic <t> --layer plan --skill video-script --outputs script.md --summary "..."
python skills/shared/scripts/manifest.py latest --topic <t> [--layer plan]
```

`kind`: `article|xhs-note|video|cards|poster|audio|other`;
`status`: `draft|ready|published`; step `status`: `done|failed`.
Decisions that are not in the deliverable go to `outputs/<topic>/brief.md`.

## Content guard

BLOCK categories (fail-closed, exit 7): API keys, Bearer tokens, internal
hosts, proxy IPs, internal paths, env names with `.env` values. WARN
categories (printed only): AI-disclosure phrasing and model names. Dry runs
only warn. Every publish/comment script calls `guard_or_die()` before
`--exec`.

## Adding a skill

1. Create `skills/openclaw/<name>/SKILL.md` with the three-field frontmatter
   and sections 输入 / 输出 / 执行步骤 / Profile 感知.
2. Put domain knowledge in `references/`, executable steps in `scripts/`
   (call `validate_output_path()` before writing).
3. Add the row to `docs/skill-function-mapping.md`.
4. `python scripts/validate_skills.py && python scripts/validate_skill_commands.py`.
5. `bash openclaw/sync.sh`.
6. If the skill needs API keys, register them in `SKILL_API_REQUIREMENTS`
   in `web/app.py` so the Skill Library page can prompt for them.

## Adding a publisher (files in order)

`skills/shared/scripts/<platform>_publish.py` (subcommands `login`,
`publish --exec`; write `outputs/_login/<platform>.json` through
`login_state.py`; call `guard_or_die`) → `skills/openclaw/skill-<platform>-upload/SKILL.md`
→ `LOGIN_RUNNERS` and the `api_login_start` / `api_publish` branches in
`web/app.py` → mapping doc → validators → `sync.sh`.
Whether `web/frontend/src/components/AccountsPage.tsx` needs a change was not
verified.
