#!/usr/bin/env bash
# 通过 Nix 官方二进制缓存安装 Devbox 包（nodejs_22 有预编译包，避免 nodejs_20 本地编译）
set -euo pipefail

export PATH="/nix/var/nix/profiles/default/bin:/usr/local/bin:${PATH}"
if [ -f /etc/profile.d/nix.sh ]; then
  # shellcheck disable=SC1091
  source /etc/profile.d/nix.sh
fi

WIN_HOST="${DEVBOX_PROXY_HOST:-127.0.0.1}"
export HTTP_PROXY="http://${WIN_HOST}:7897"
export HTTPS_PROXY="http://${WIN_HOST}:7897"
export ALL_PROXY="http://${WIN_HOST}:7897"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Proxy: $HTTP_PROXY"
echo "nix: $(nix --version)"
echo "devbox install（nodejs_22，默认使用 cache.nixos.org 预编译包）..."
devbox install

echo "验证工具链..."
devbox run -- bash -lc 'task --version && uv --version && node --version && python3 --version'
