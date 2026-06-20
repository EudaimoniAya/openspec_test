## Context

项目测试栈：

| 层 | 工具 | 当前输出 |
|----|------|----------|
| 后端 | pytest + pytest-asyncio | 终端 `-v` |
| 前端 | vitest run | 终端默认 reporter |
| CI | GitHub Actions 分 job | 无持久化报告 |
| 本地 | `task test:all` | 无 HTML 报告 |

用户希望 **CI 与本地** 均生成 **Allure 测试报告**；CI 通过 **GitHub Actions Artifacts** 传出，便于 PR 审查与 AI 辅助分析失败用例。

## Goals / Non-Goals

**Goals:**

- 本地 `task test:report` 生成可浏览器打开的 Allure HTML（`reports/allure-report/`）
- CI 在 backend-test / frontend-test 后聚合 Allure 结果并 **upload-artifact**
- 测试失败时仍上传报告（`if: always()`），便于排查
- 报告目录 gitignore，不提交生成物
- 与现有 mock 策略一致，CI 仍不调用真实 DeepSeek

**Non-Goals:**

- 部署 Allure Server / ReportPortal / TestOps
- 将 Allure 接入 lint/typecheck job
- CI 改用 Taskfile 执行测试（保持 workflow 内联命令，与现有 dev-tooling 一致）
- 覆盖率报告（coverage）——可后续独立变更

## Decisions

### 1. 选用 Allure 作为统一报告格式

**理由**：
- pytest 有成熟插件 `allure-pytest`
- vitest 可通过 JUnit XML 或 `@vitest/allure` 适配器导出 Allure 兼容结果
- `allure generate` 可合并多目录 results 为单一 HTML 站点
- 用户诉求「测试报告 + Artifacts」与 Allure 生态匹配（用户表述 alembic 实为 Allure）

**备选**：
- 仅 JUnit XML + GitHub Actions 原生测试摘要——无 rich HTML，放弃
- pytest-html 仅覆盖后端——前后端不统一，放弃

### 2. 目录约定

```
reports/
├── allure-results/          # 原始结果（backend + frontend 子目录或合并）
│   ├── backend/
│   └── frontend/
└── allure-report/           # 生成的静态 HTML（本地打开 index.html）

.gitignore:
  reports/allure-results/
  reports/allure-report/
```

### 3. 后端：pytest + allure-pytest

`backend/pyproject.toml` dev 依赖增加 `allure-pytest`。

测试命令（CI 与 Task 对齐）：

```bash
cd backend
uv run pytest -v --alluredir=../reports/allure-results/backend
```

可选：在 `conftest.py` 注册 Allure 环境信息（Python 版本、项目名称），非必须。

### 4. 前端：vitest + JUnit → Allure

Vitest 4 原生支持 JUnit reporter。策略：

```ts
// vite.config.ts test.reporters
reporters: ['default', ['junit', { outputFile: '../reports/allure-results/frontend/junit.xml' }]]
```

CI/聚合阶段使用 `allure generate` 时，需将 JUnit 转为 Allure 或在 vitest 侧使用 **allure-vitest**（若可用）直接写 allure-results。

**首选**：调研并采用 **直接写 allure-results 的 vitest reporter**（如 `allure-vitest` 或官方兼容包）；若仅 JUnit，则在聚合脚本中说明 Allure 2 对 JUnit 的导入限制，优先 vitest-native allure adapter。

**实施默认**（tasks 中细化）：
- 尝试 `allure-vitest` 输出到 `reports/allure-results/frontend`
- fallback：`@vitest/reporter-junit` + 文档说明前端在 Allure 中显示为 JUnit suite

### 5. Allure CLI

生成 HTML 需要 `allure` 命令：

| 环境 | 来源 |
|------|------|
| Devbox | `devbox add allure` 或 nix 包 `allure` |
| CI | `sudo apt` / `choco` 不适用；使用 **npx allure-commandline** 或 **actions 安装 Java + allure release** |

**CI 推荐**：

```yaml
- uses: actions/setup-java@v4
  with:
    distribution: temurin
    java-version: '17'
- run: npm install -g allure-commandline --save-dev  # 或下载 release zip
```

更轻量：**在 repo 根添加 devDependency `allure-commandline`** 或 CI 使用 `quay.io/allure/allure` docker one-shot：

```bash
docker run --rm -v $PWD/reports:/reports allure/allure generate /reports/allure-results -o /reports/allure-report
```

**决策**：CI 使用 **allure-commandline npm 包**（`npx allure generate`），与 Node 前端 job 复用 setup-node，避免额外 Docker in test job。

### 6. 聚合脚本 `scripts/allure-report.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS="${ROOT}/reports/allure-results"
OUT="${ROOT}/reports/allure-report"

mkdir -p "${RESULTS}/backend" "${RESULTS}/frontend"
# 假定 test 已跑完并写入 results

npx --yes allure-commandline generate "${RESULTS}" -o "${OUT}" --clean
echo "报告: file://${OUT}/index.html"
```

WSL/Devbox 友好；Windows PowerShell 可文档说明在 WSL 内执行 `task test:report`。

### 7. Taskfile 任务

```yaml
test:backend:
  cmds:
    - uv run pytest -v --alluredir=../../reports/allure-results/backend
  dir: backend

test:frontend:
  # vitest 配置写 allure/junit 到 reports

test:report:
  desc: 运行全部测试并生成 Allure HTML 报告
  deps: [test:all]
  cmds:
    - bash scripts/allure-report.sh

test:report:open:
  desc: 生成报告并用默认浏览器打开（WSL 可选）
  deps: [test:report]
  cmds:
    - 'echo 请打开 reports/allure-report/index.html'
```

保留 `test:all` 行为：可改为始终写 allure-results，或 `test:all` 不变、`test:report` 显式聚合——**决策**：`test:backend` / `test:frontend` 始终 `--alluredir`，`test:report` 只负责 `allure generate`（需先 test:all）。

### 8. GitHub Actions Artifacts

新增 job **`test-report`**（或合并到现有 test jobs 末尾）：

```yaml
test-report:
  runs-on: ubuntu-latest
  needs: [backend-test, frontend-test]
  if: always() && (needs.backend-test.result != 'skipped' || needs.frontend-test.result != 'skipped')
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: temurin
    - name: Download allure results from jobs
      # 方案 A：各 test job 用 upload-artifact 传 results，此 job download 后 merge
      # 方案 B：单 job 跑全部测试（简化 artifact，但失去并行）
```

**决策：方案 A——各 test job 上传 results 片段，report job 合并生成**

`backend-test` 末尾：

```yaml
- run: uv run pytest -v --alluredir=../../reports/allure-results/backend
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: allure-results-backend
    path: reports/allure-results/backend
    retention-days: 30
```

`frontend-test` 同理上传 `allure-results-frontend`。

`test-report` job：

```yaml
- uses: actions/download-artifact@v4
  with:
    pattern: allure-results-*
    merge-multiple: true
    path: reports/allure-results
- run: npx allure-commandline generate reports/allure-results -o reports/allure-report --clean
- uses: actions/upload-artifact@v4
  with:
    name: allure-report
    path: reports/allure-report/
    retention-days: 30
```

PR 页面 → Actions → 对应 workflow run → **Artifacts** → 下载 `allure-report.zip` → 解压打开 `index.html`。

### 9. Devbox

可选 `devbox add allure` 或文档说明 `npx allure-commandline`；不强制 CI 使用 Devbox。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| Allure CLI 依赖 Java | CI setup-java；本地 npx 或 Devbox 包 |
| vitest Allure 集成不成熟 | JUnit fallback + 文档 |
| Artifact 体积 | 仅 HTML 报告 + raw results 分 artifact；retention 30 天 |
| test job 与 report job 复杂度 | README 图解 Artifacts 下载路径 |
| WSL/Windows 路径 | 报告路径统一在 repo `reports/` |

## Migration Plan

1. 添加依赖与 pytest/vitest 配置
2. 实现 `scripts/allure-report.sh` 与 Taskfile 任务
3. 更新 CI workflow（test 命令 + artifacts + report job）
4. 更新 README 与 `.gitignore`
5. 本地 `task test:report` 与 CI 各验证一次

## Open Questions

- vitest 侧最终选用 **allure-vitest** 还是 **junit reporter**（implement 阶段以可用性为准）
- 是否在 Devbox 中固定添加 `allure` nix 包（可选，npx 亦可）
