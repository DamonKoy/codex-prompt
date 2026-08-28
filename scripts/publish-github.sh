#!/bin/zsh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OWNER="DamonKoy"
REPO="codex-prompt"
HTTPS_URL="https://github.com/${OWNER}/${REPO}.git"
SSH_URL="git@github.com:${OWNER}/${REPO}.git"

cd "$REPO_ROOT"

echo "[1/5] validate plugin structure"
python3 scripts/validate.py
python3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/prompt-refiner

echo "[2/5] ensure gh auth"
if ! gh api user --jq .login >/dev/null 2>&1; then
  echo "gh 未登录。将启动浏览器登录（协议=https，不上传新 SSH key）"
  gh auth login -h github.com -p https -w --skip-ssh-key
fi
gh auth status

echo "[3/5] probe GitHub SSH (optional)"
if ssh -o BatchMode=yes -o ConnectTimeout=5 -T git@github.com 2>/dev/null; then
  PUSH_URL="$SSH_URL"
  echo "SSH usable; prefer SSH remote"
else
  PUSH_URL="$HTTPS_URL"
  echo "SSH unavailable; fall back to HTTPS remote"
fi

echo "[4/5] create public repo if missing"
if gh repo view "${OWNER}/${REPO}" >/dev/null 2>&1; then
  echo "repo already exists: ${OWNER}/${REPO}"
else
  gh repo create "${OWNER}/${REPO}" --public --description "Codex Prompt Refiner plugin: refine prompts without executing the original task" --source=. --remote=origin --disable-wiki
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "$PUSH_URL"
else
  git remote set-url origin "$PUSH_URL"
fi

echo "[5/5] push main"
git push -u origin main

echo "done: https://github.com/${OWNER}/${REPO}"
echo "install:"
echo "  codex plugin marketplace add ${OWNER}/${REPO}"
echo "  codex plugin add prompt-refiner@prompt-refiner"
