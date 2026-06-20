## MODIFIED Requirements

### Requirement: 后端质量门禁

CI SHALL 对 backend 执行以下检查，任一失败则 workflow 失败：

- ruff lint 与 format 检查
- mypy 类型检查（针对 `app/`）
- pytest 全量测试

所有 backend CI 步骤 SHALL 通过 **uv** 在 `backend/` 目录安装依赖（`uv sync --frozen --dev`），SHALL NOT 使用裸 `pip install -r requirements-dev.txt`。

backend-test job SHALL 使用 pytest 的 Allure 输出（`--alluredir`）将结果写入 `reports/allure-results/backend/`，并 SHALL 通过 GitHub Actions **upload-artifact** 上传该目录（测试失败时仍上传）。

#### Scenario: CI 使用 uv 安装

- **WHEN** GitHub Actions 运行 backend-test job
- **THEN** SHALL 使用 `uv sync --frozen --dev` 安装依赖
- **THEN** SHALL 使用 `uv run pytest` 执行测试

#### Scenario: CI 上传后端 Allure 结果

- **WHEN** backend-test job 完成（无论 pass 或 fail）
- **THEN** SHALL 上传包含 `reports/allure-results/backend` 的 Artifact

#### Scenario: Lint 失败阻断

- **WHEN** 代码存在 ruff 违规
- **THEN** `backend-lint` job SHALL 失败

#### Scenario: 类型错误阻断

- **WHEN** mypy 报告类型错误
- **THEN** `backend-typecheck` job SHALL 失败

### Requirement: 前端质量门禁

CI SHALL 对 frontend 执行以下检查，任一失败则 workflow 失败：

- ESLint
- `tsc --noEmit`
- `vitest run`

frontend-test job SHALL 将测试结果导出到 `reports/allure-results/frontend/`，并 SHALL 通过 **upload-artifact** 上传（测试失败时仍上传）。

CI SHALL 包含聚合 job（或等价步骤），下载各 test job 的 Allure 结果片段，生成 HTML 并上传 **`allure-report`** Artifact。

#### Scenario: TypeScript 错误阻断

- **WHEN** 存在 TypeScript 编译错误
- **THEN** `frontend-typecheck` job SHALL 失败

#### Scenario: CI 上传前端测试结果

- **WHEN** frontend-test job 完成（无论 pass 或 fail）
- **THEN** SHALL 上传包含 frontend 测试结果的 Artifact

#### Scenario: CI 上传合并 HTML 报告

- **WHEN** CI workflow 中 test 相关 job 已执行
- **THEN** SHALL 存在可下载的 `allure-report` Artifact（静态 HTML）
