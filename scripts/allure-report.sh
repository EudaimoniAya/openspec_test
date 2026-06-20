#!/usr/bin/env bash
# 合并 backend/frontend Allure 结果并生成 HTML 报告
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS="${ROOT}/reports/allure-results"
OUT="${ROOT}/reports/allure-report"
BACKEND="${RESULTS}/backend"
FRONTEND="${RESULTS}/frontend"

RESULT_DIRS=()
if [ -d "${BACKEND}" ] && [ -n "$(find "${BACKEND}" -maxdepth 1 -name '*-result.json' -print -quit 2>/dev/null)" ]; then
  RESULT_DIRS+=("${BACKEND}")
fi
if [ -d "${FRONTEND}" ] && [ -n "$(find "${FRONTEND}" -maxdepth 1 -name '*-result.json' -print -quit 2>/dev/null)" ]; then
  RESULT_DIRS+=("${FRONTEND}")
fi

if [ ${#RESULT_DIRS[@]} -eq 0 ]; then
  echo "错误: 未找到 Allure 结果，请先运行 task test:all" >&2
  exit 1
fi

mkdir -p "${OUT}"

ALLURE_BIN="${ROOT}/node_modules/.bin/allure"
if [ ! -x "${ALLURE_BIN}" ]; then
  echo "错误: 未找到 allure CLI，请先运行 task setup:reports" >&2
  exit 1
fi

# allure generate 不会递归子目录，需分别传入 backend/frontend 结果目录
"${ALLURE_BIN}" generate "${RESULT_DIRS[@]}" -o "${OUT}" --clean

echo "报告已生成: ${OUT}/index.html"
echo "注意: 不要用 file:// 直接打开（会 Failed to fetch），请执行:"
echo "  task test:report:open"
echo "或:"
echo "  ${ALLURE_BIN} open ${OUT}"
