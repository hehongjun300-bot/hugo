#!/usr/bin/env bash
# install-skills.sh — 批量下载资源目录里登记的 Agent Skill
#
# 用法：bash tools/install-skills.sh
#
# 行为：
#   - 克隆到仓库根目录的 skills/<名字>/
#   - 已有目录跳过，不覆盖（带 --force 才重新拉取）
#   - 每个仓库只拉最新一次提交（--depth 1），省时间省空间
#   - 结束后打印实际占用，并提醒哪些还没装依赖
#
# 注意：skills/ 已在 .gitignore 中排除，不会进仓库。

set -uo pipefail

cd "$(dirname "$0")/.." || exit 1
DEST="skills"
FORCE="${1:-}"

# 名字|仓库地址|约大小(供参考)
SKILLS=(
  "xilo-opus-video|https://github.com/Kianzzz/xilo-opus-video.git|1.9 MB"
  "dashi-animationstyle|https://github.com/chuspeeism/dashi-animationstyle.git|29 MB"
  "huashu-art-motion|https://github.com/alchaincyf/huashu-art-motion.git|77 MB"
  "lemo-opuscar|https://github.com/lemomo-ai/lemo-opuscar.git|142 MB"
  "mg-styles-15|https://github.com/Vincentwei1021/mg-styles-15.git|555 MB"
)

mkdir -p "$DEST"

ok=0; skip=0; fail=0

for entry in "${SKILLS[@]}"; do
  IFS='|' read -r name url size <<< "$entry"
  target="$DEST/$name"

  if [ -d "$target/.git" ]; then
    if [ "$FORCE" != "--force" ]; then
      echo "跳过 $name（已存在；要重新拉取用 --force）"
      skip=$((skip+1))
      continue
    fi
    echo "重新拉取 $name ..."
    rm -rf "$target"
  fi

  echo "下载 $name（约 $size）..."
  if git clone --depth 1 --quiet "$url" "$target" 2>/dev/null; then
    echo "  ✓ $name"
    ok=$((ok+1))
  else
    echo "  ✗ $name 下载失败（检查网络或仓库是否仍存在）"
    fail=$((fail+1))
  fi
done

echo
echo "================ 结果 ================"
echo "成功 $ok 个 / 跳过 $skip 个 / 失败 $fail 个"
echo
echo "各 skill 实际占用："
du -sh "$DEST"/* 2>/dev/null | sort -h
echo
echo "skills 目录合计："
du -sh "$DEST" 2>/dev/null

echo
echo "提示："
echo "  - 这些是「菜谱」，要真正渲染出片，多数还需要装依赖（npm install / pip install）"
echo "  - 各仓库的用法不同，用前先读它自己的 SKILL.md 或 README.md"
echo "  - skills/ 已在 .gitignore 排除，不会传到 GitHub"

exit 0
