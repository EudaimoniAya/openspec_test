## Purpose

Allure 测试报告的收集、本地生成与 CI Artifacts 分发。

## ADDED Requirements

### Requirement: Allure 结果目录

项目 SHALL 在仓库根目录使用 `reports/allure-results/` 存放测试原始结果，`reports/allure-report/` 存放生成的 HTML 报告；两者 SHALL 被 `.gitignore` 忽略。

#### Scenario: 生成物不被 Git 跟踪

- **WHEN** 开发者运行测试并生成 Allure 结果
- **THEN** `reports/allure-results/` 与 `reports/allure-report/` SHALL NOT 被 Git 跟踪

### Requirement: 后端 Allure 集成

后端 pytest SHALL 支持通过 `--alluredir` 将结果写入 `reports/allure-results/backend/`。

#### Scenario: 后端测试写 Allure 结果

- **WHEN** 开发者在 `backend/` 执行带 Allure 的 pytest 命令（或等价 `task test:backend`）
- **THEN** SHALL 在 `reports/allure-results/backend/` 产生 Allure 兼容结果文件

### Requirement: 前端测试结果导出

前端 vitest SHALL 将测试结果导出到 `reports/allure-results/frontend/`，格式 SHALL 可与 Allure generate 合并（Allure 原生或 JUnit 经文档化流程合并）。

#### Scenario: 前端测试写结果

- **WHEN** 开发者执行前端测试（或等价 `task test:frontend`）
- **THEN** SHALL 在 `reports/allure-results/frontend/` 产生可聚合的结果文件

### Requirement: 本地 HTML 报告生成

项目 SHALL 提供脚本或 Task，将 backend 与 frontend 结果合并生成静态 HTML 到 `reports/allure-report/`。

#### Scenario: 本地生成报告

- **WHEN** 开发者执行 `task test:report`（或文档等价命令）
- **THEN** SHALL 生成 `reports/allure-report/index.html` 可供浏览器打开

#### Scenario: 测试失败仍生成报告

- **WHEN** 测试命令 exit code 非 0 但已产生 allure-results
- **THEN** 报告生成步骤 SHALL 仍尝试执行（或文档说明先 `--alluredir` 再单独 generate）

### Requirement: CI Artifacts 上传

GitHub Actions SHALL 在测试 workflow 中上传 Allure 报告为 Artifact，供用户从 Actions run 页面下载。

#### Scenario: CI 上传合并 HTML 报告

- **WHEN** CI workflow 完成 backend-test 与 frontend-test
- **THEN** SHALL 存在名为 `allure-report`（或文档约定名）的 Artifact，内含可离线打开的 HTML

#### Scenario: CI 失败仍保留报告

- **WHEN** backend-test 或 frontend-test job 失败
- **THEN** Allure 相关 Artifact SHALL 仍被上传（`if: always()` 或等价策略）

#### Scenario: 下载路径文档化

- **WHEN** 开发者阅读 README 测试报告章节
- **THEN** SHALL 找到从 GitHub Actions → Artifacts 下载报告的步骤说明
