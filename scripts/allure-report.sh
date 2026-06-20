#!/usr/bin/env bash
# 合并 backend/frontend Allure 结果并生成 HTML 报告
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS="${ROOT}/reports/allure-results"
OUT="${ROOT}/reports/allure-report"

if [ ! -d "${RESULTS}" ] || [ -z "$(find "${RESULTS}" -type f 2>/dev/null | head -1)" ]; then
  echo "错误: 未找到 Allure 结果，请先运行 task test:all" >&2
  exit 1
fi

mkdir -p "${OUT}"

if [ -x "${ROOT}/node_modules/.bin/allure" ]; then
  "${ROOT}/node_modules/.bin/allure" generate "${RESULTS}" -o "${OUT}" --clean
else
  npx --yes allure-commandline generate "${RESULTS}" -o "${OUT}" --clean
fi

echo "报告已生成: file://${OUT}/index.html"
