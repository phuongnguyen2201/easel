#!/usr/bin/env bash
set -euo pipefail

# Easel — 同步 SKILL + workspace 到 OpenClaw 的 easel 隔离 profile
#
# --profile easel 的实际路径：
#   workspace → ~/.openclaw/workspace-easel/
#   config    → ~/.openclaw-easel/openclaw.json
#
# 用法：bash openclaw/sync.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PROFILE="easel"
# --profile easel 的 workspace 在 ~/.openclaw/workspace-easel/
OPENCLAW_WORKSPACE_DST="$HOME/.openclaw/workspace-${PROFILE}"
OPENCLAW_SKILL_DST="$OPENCLAW_WORKSPACE_DST/skills"
OPENCLAW_WORKSPACE_SRC="$SCRIPT_DIR/workspace"
OPENCLAW_SKILL_SRC="$PROJECT_ROOT/skills/openclaw"

echo "[easel] Syncing to OpenClaw profile: $PROFILE"
echo "  workspace → $OPENCLAW_WORKSPACE_DST"
echo ""

# ---- 确保目录存在 ----
mkdir -p "$OPENCLAW_SKILL_DST"
mkdir -p "$OPENCLAW_WORKSPACE_DST"

# ---- 清理已删除的 SKILL ----
# 收集源目录中存在的 SKILL 名单，删除 workspace 中多余的
for dst_dir in "$OPENCLAW_SKILL_DST"/*/; do
    [ -d "$dst_dir" ] || continue
    name=$(basename "$dst_dir")
    if [ ! -d "$OPENCLAW_SKILL_SRC/$name" ]; then
        rm -rf "$dst_dir"
        echo "  ✗ $name (removed — no longer in source)"
    fi
done

# ---- 同步 skills ----
# 单一技能库：五层（发现/策划/制作/发布/归因）全部由 OpenClaw 直接执行，
# SKILL 完整同步进 workspace，OpenClaw 读进来照其流程自己产出。
echo "Skills:"
synced=0
for skill_dir in "$OPENCLAW_SKILL_SRC"/*/; do
    [ -d "$skill_dir" ] || continue
    name=$(basename "$skill_dir")
    rm -rf "$OPENCLAW_SKILL_DST/$name"
    cp -r "$skill_dir" "$OPENCLAW_SKILL_DST/$name"
    echo "  ✓ $name"
    synced=$((synced + 1))
done
echo "  ($synced skills synced)"
echo ""

# ---- 同步 shared/ 跨 SKILL 共享层 ----
# 多个 SKILL 用 ../../shared/xxx.md 引用（workspace 扁平化后解析为 workspace/shared/）
SHARED_SRC="$PROJECT_ROOT/skills/shared"
SHARED_DST="$OPENCLAW_WORKSPACE_DST/shared"
if [ -d "$SHARED_SRC" ]; then
    rm -rf "$SHARED_DST"
    cp -r "$SHARED_SRC" "$SHARED_DST"
    echo "Shared: ✓ synced → workspace/shared/ ($(find "$SHARED_DST" -type f | wc -l) files)"
    echo ""
fi

# ---- 同步 workspace 文件（AGENTS.md / SOUL.md） ----
echo "Workspace:"
for f in "$OPENCLAW_WORKSPACE_SRC"/*.md; do
    [ -f "$f" ] || continue
    name=$(basename "$f")
    cp "$f" "$OPENCLAW_WORKSPACE_DST/$name"
    echo "  ✓ $name"
done

# AGENTS.md is injected every turn. Embed the resolved project root there so
# configuration checks never fall back to the workspace's shared/ copy.
cat >> "$OPENCLAW_WORKSPACE_DST/AGENTS.md" << AGENTROOTEOF

## Thư mục gốc dự án lúc chạy (do openclaw/sync.sh sinh ra)

Đường dẫn tuyệt đối của thư mục gốc Easel: \`$PROJECT_ROOT\`

Trước khi chạy bất kỳ script dự án nào trong \`skills/...\`, bắt buộc thực hiện:

\`\`\`bash
cd "$PROJECT_ROOT"
test -f .env && test -d skills/shared/scripts
\`\`\`

Không kiểm tra Key, URL hay cấu hình model trong bản sao \`shared/\` tại \`$OPENCLAW_WORKSPACE_DST\`.
AGENTROOTEOF
echo "  ✓ AGENTS.md runtime project root"
echo ""

# ---- Dọn USER.md toàn cục đã bỏ ----
# Profile nay được tiêm inline vào message (xem docs/prompt-stack.md), không ghi USER.md toàn cục nữa.
# Xoá tàn dư cũ để profile cũ không làm bẩn system prompt.
rm -f "$OPENCLAW_WORKSPACE_DST/USER.md" 2>/dev/null && echo "Cleanup: ✓ đã xoá USER.md còn sót" || true
# Bộ nhớ dài hạn của Easel tách theo profile; MEMORY.md toàn cục phải luôn rỗng để tránh lẫn giữa các profile.
: > "$OPENCLAW_WORKSPACE_DST/MEMORY.md"
echo "Cleanup: ✓ đã làm rỗng MEMORY.md toàn cục (bộ nhớ profile đọc theo từng phiên)"
echo ""

# ---- Profile 目录 symlink ----
# 注意：必须先删除旧 symlink 再创建，否则 ln -sf 会跟着旧 symlink 进入目标目录创建循环
PROFILE_LINK="$OPENCLAW_WORKSPACE_DST/easel-profiles"
rm -f "$PROFILE_LINK" 2>/dev/null
ln -s "$PROJECT_ROOT/profiles" "$PROFILE_LINK"
echo "Profiles: ✓ symlinked → $PROJECT_ROOT/profiles"

# ---- outputs 目录 symlink ----
# Agent CWD 是 workspace，SKILL 写 outputs/ 会落到 workspace 内
# 通过 symlink 让 workspace/outputs/ → 项目 outputs/，产物自动归位
OUTPUTS_LINK="$OPENCLAW_WORKSPACE_DST/outputs"
if [ -d "$OUTPUTS_LINK" ] && [ ! -L "$OUTPUTS_LINK" ]; then
    # 真目录残留，搬走内容后删除
    cp -rn "$OUTPUTS_LINK"/* "$PROJECT_ROOT/outputs/" 2>/dev/null || true
    rm -rf "$OUTPUTS_LINK"
fi
rm -f "$OUTPUTS_LINK" 2>/dev/null
ln -s "$PROJECT_ROOT/outputs" "$OUTPUTS_LINK"
echo "Outputs: ✓ symlinked → $PROJECT_ROOT/outputs"
echo ""

# ---- 记录项目根路径（供 workspace 内人工/工具读取；AGENTS.md 另有每轮注入副本） ----
cat > "$OPENCLAW_WORKSPACE_DST/CONTEXT.md" << CTXEOF
# Đường dẫn dự án Easel

Thư mục gốc dự án: $PROJECT_ROOT

Cả năm tầng Khám phá / Lập kế hoạch / Sản xuất / Xuất bản / Đo lường đều do bạn trực tiếp thực hiện.
Trước khi chạy script dự án hoặc tạo sản phẩm, phải \`cd\` về thư mục gốc dự án
(**phiên bản claude này không hỗ trợ --cwd**):
\`\`\`
cd $PROJECT_ROOT && python skills/shared/scripts/<script>.py ...   # script sản xuất / xuất bản / phân tích
\`\`\`
Bộ kỹ năng đã được đồng bộ đầy đủ (\`skills/\`); đọc vào rồi làm theo quy trình của kỹ năng, ghi sản phẩm ra \`outputs/\`.

Sản phẩm ghi ra: $PROJECT_ROOT/outputs/
Tư liệu người dùng ở: $PROJECT_ROOT/assets/
Hồ sơ người dùng (profile) ở: $PROJECT_ROOT/profiles/
CTXEOF
echo "Project context: ✓ CONTEXT.md"
echo ""

echo "[easel] Sync done."
