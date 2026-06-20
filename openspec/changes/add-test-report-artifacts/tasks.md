## 1. 依赖与配置

- [x] 1.1 `backend/pyproject.toml` 添加 `allure-pytest` 到 dev 依赖并 `uv lock`
- [x] 1.2 配置 pytest 默认可选 `--alluredir`（Task/CI 显式传参即可，无需改默认）
- [x] 1.3 前端添加 vitest Allure/JUnit reporter 依赖并更新 `vite.config.ts`
- [x] 1.4 更新 `.gitignore` 忽略 `reports/allure-results/`、`reports/allure-report/`

## 2. 报告聚合脚本

- [x] 2.1 创建 `scripts/allure-report.sh`（`allure generate`，输出 `reports/allure-report/`）
- [x] 2.2 根目录添加 `allure-commandline`（npm devDependency 或文档化 npx 用法）
- [x] 2.3 本地验证：先跑测试再 `bash scripts/allure-report.sh`，确认 `index.html` 可打开

## 3. Taskfile

- [x] 3.1 更新 `test:backend`：`pytest --alluredir=../reports/allure-results/backend`
- [x] 3.2 更新 `test:frontend`：确保 vitest 写入 `reports/allure-results/frontend`
- [x] 3.3 新增 `test:report`：依赖 `test:all` 后执行聚合脚本
- [x] 3.4 运行 `task test:report` 验证端到端

## 4. GitHub Actions

- [x] 4.1 更新 `backend-test`：pytest 带 `--alluredir`，`upload-artifact`（`if: always()`）
- [x] 4.2 更新 `frontend-test`：导出结果并 `upload-artifact`（`if: always()`）
- [x] 4.3 新增 `test-report` job：`download-artifact` → `allure generate` → 上传 `allure-report` Artifact
- [x] 4.4 配置 Java（Allure CLI 需要）与 Node（npx allure-commandline）
- [ ] 4.5 推送分支验证 Actions Artifacts 可下载（需 push 后在 Actions 页面确认）

## 5. 文档

- [x] 5.1 README 新增「测试报告（Allure）」：本地 `task test:report`、CI Artifacts 下载步骤
- [x] 5.2 说明测试失败时如何查看报告

## 6. 收尾

- [x] 6.1 运行 `openspec validate add-test-report-artifacts --strict`
- [x] 6.2 确认 CI lint/typecheck job 行为未改变
