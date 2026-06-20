#!/usr/bin/env bash
# 在 devbox 环境中验证 Task 与快捷脚本
set -euo pipefail

export PATH="/nix/var/nix/profiles/default/bin:/usr/local/bin:${PATH}"
if [ -f /etc/profile.d/nix.sh ]; then
  # shellcheck disable=SC1091
  source /etc/profile.d/nix.sh
fi

WIN_HOST="${DEVBOX_PROXY_HOST:-127.0.0.1}"
export HTTP_PROXY="http://${WIN_HOST}:7897"
export HTTPS_PROXY="http://${WIN_HOST}:7897"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== task --list ==="
devbox run -- bash -lc 'task --list'

echo "=== task setup:all ==="
devbox run setup

echo "=== devbox run test ==="
devbox run test
