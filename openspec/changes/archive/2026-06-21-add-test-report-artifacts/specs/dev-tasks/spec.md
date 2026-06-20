## MODIFIED Requirements

### Requirement: 测试与 Lint 任务

Taskfile SHALL 提供 test 与 lint 分组任务，命令 SHALL 与 CI 使用的底层工具一致（pytest、vitest、ruff、mypy、eslint、tsc）。

`test:backend` 与 `test:frontend` SHALL 在运行测试时写入 Allure 结果到 `reports/allure-results/`（与 CI 路径一致）。

Taskfile SHALL 提供 **`test:report`** 任务，在测试完成后生成 Allure HTML 到 `reports/allure-report/`。

#### Scenario: 运行全部测试

- **WHEN** 开发者执行 `task test:all`
- **THEN** SHALL 运行 backend pytest 与 frontend vitest，任一失败则任务失败
- **THEN** SHALL 写入 Allure 结果到约定目录

#### Scenario: 生成本地 HTML 报告

- **WHEN** 开发者执行 `task test:report`
- **THEN** SHALL 生成 `reports/allure-report/index.html`

#### Scenario: 运行全部 lint

- **WHEN** 开发者执行 `task lint:all`
- **THEN** SHALL 运行 backend ruff/mypy 与 frontend eslint/typecheck
