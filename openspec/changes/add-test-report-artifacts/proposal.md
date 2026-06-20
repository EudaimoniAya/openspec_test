## Why

当前 CI 与本地测试仅输出终端日志，失败用例需人工翻阅 pytest/vitest 输出，不便于 AI 辅助 TDD 复盘与 PR 审查。需要统一的 **Allure 测试报告**：本地一条命令生成 HTML，CI 在 GitHub Actions 中上传 **Artifacts** 供下载查看。

## What Changes

- 后端 pytest 集成 **allure-pytest**，输出 `allure-results`
- 前端 vitest 集成 Allure/JUnit 结果导出，输出可合并的 results
- 新增报告聚合脚本与 **`task test:report`**（本地生成 HTML 到 `reports/allure-report/`）
- 更新 **`.github/workflows/ci.yml`**：测试 job 生成 Allure 结果，新增 **`upload-artifact`** 上传合并报告
- 更新 **README**：如何本地查看报告、如何从 CI Artifacts 下载
- **Non-goals**：不引入 Allure Server / TestOps 托管；不改变测试断言逻辑；lint job 不上传报告

## Capabilities

### New Capabilities

- `test-reports`：Allure 结果收集、本地 HTML 生成、CI Artifacts 上传

### Modified Capabilities

- `dev-tooling`：CI 测试 job 产出 Allure 报告并上传 Artifacts
- `dev-tasks`：Taskfile 增加 `test:report` 等报告相关任务

## Impact

- **修改**：`backend/pyproject.toml`、`frontend/package.json`、`frontend/vite.config.ts`、`.github/workflows/ci.yml`、`Taskfile.yml`、`README.md`、`.gitignore`
- **新增**：报告聚合脚本（如 `scripts/allure-report.sh`）、可选 `reports/.gitkeep`
- **依赖**：`allure-pytest`、vitest Allure/JUnit reporter、`allure-commandline`（Devbox 包或 npm/nix）
- **CI**：Artifacts 保留策略（默认 90 天）；仅 test job 上传，失败 run 仍保留报告
