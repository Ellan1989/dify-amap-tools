#!/usr/bin/env bash
# Publish the Amap Tools plugin to the Dify Marketplace.
#
# Prerequisites (already satisfied on this machine):
#   - gh CLI logged in as Ellan1989
#   - Plugin packaged at amap_tools-0.0.1.difypkg, validator-clean
#   - Source repo committed at ./
#
# After the PR is merged by the Dify team, the marketplace page URL will be:
#   https://marketplace.dify.ai/plugin/ellan1989/amap_tools
set -euo pipefail

GH_USER="Ellan1989"
PLUGIN_DIR_NAME="ellan1989/amap_tools"
PKG="amap_tools-0.0.1.difypkg"
BRANCH="add-amap_tools-0.0.1"
REPO_NAME="dify-amap-tools"
ROOT="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT"

echo "==> [1/4] Creating public source repo ${GH_USER}/${REPO_NAME} (if missing)..."
if gh repo view "${GH_USER}/${REPO_NAME}" >/dev/null 2>&1; then
  echo "    repo already exists, pushing latest commit"
  git push -u "https://github.com/${GH_USER}/${REPO_NAME}.git" HEAD:main 2>/dev/null || \
    git remote add origin "https://github.com/${GH_USER}/${REPO_NAME}.git" && \
    git push -u origin main
else
  gh repo create "${GH_USER}/${REPO_NAME}" --public --source . --push
fi

echo "==> [2/4] Forking langgenius/dify-plugins (if missing)..."
if ! gh repo view "${GH_USER}/dify-plugins" >/dev/null 2>&1; then
  gh repo fork langgenius/dify-plugins --clone=false
  sleep 5
fi

echo "==> [3/4] Preparing submission branch..."
WORK="$(mktemp -d)/dify-plugins"
gh repo clone "${GH_USER}/dify-plugins" "$WORK" -- --depth 5
cd "$WORK"
git checkout -b "$BRANCH"
git remote add upstream https://github.com/langgenius/dify-plugins.git 2>/dev/null || true
git fetch upstream main --depth 5 && git merge --ff-only upstream/main 2>/dev/null || true
mkdir -p "$PLUGIN_DIR_NAME"
cp "$ROOT/$PKG" "$PLUGIN_DIR_NAME/"
git add "$PLUGIN_DIR_NAME"
git -c user.name="$GH_USER" -c user.email="${GH_USER}@users.noreply.github.com" \
  commit -m "feat: add Amap Tools 0.0.1 tool plugin"
git push -u origin "$BRANCH"

echo "==> [4/4] Opening PR..."
gh pr create \
  --repo langgenius/dify-plugins \
  --base main \
  --head "${GH_USER}:${BRANCH}" \
  --title "feat: add Amap Tools 0.0.1 tool plugin" \
  --body-file "$ROOT/PR_DESCRIPTION.md"

echo
echo "Done. PR opened. After merge, your marketplace URL will be:"
echo "  https://marketplace.dify.ai/plugin/ellan1989/amap_tools"
