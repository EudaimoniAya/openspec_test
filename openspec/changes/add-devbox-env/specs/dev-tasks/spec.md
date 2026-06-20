## MODIFIED Requirements

### Requirement: 统一 Task 入口

项目 SHALL 在仓库根目录提供 `Taskfile.yml`，使开发者可通过 `task <task-name>` 执行常见开发与质量命令，而无需手动 `cd` 子目录。

在已配置 Devbox 的环境中，推荐流程 SHALL 为：先 `devbox shell`，再执行 `task` 或 `devbox run <script>`。

#### Scenario: 查看可用任务

- **WHEN** 开发者在 devbox shell 内于仓库根目录执行 `task --list`
- **THEN** SHALL 列出所有已定义任务及简短描述

#### Scenario: 后端开发启动

- **WHEN** 开发者在 devbox shell 内执行 `task dev:backend`
- **THEN** SHALL 在 `backend/` 使用 `uv run uvicorn app.main:app --reload --port 8000` 启动服务

#### Scenario: 前端开发启动

- **WHEN** 开发者在 devbox shell 内执行 `task dev:frontend`
- **THEN** SHALL 在 `frontend/` 执行 `npm run dev`

## ADDED Requirements

### Requirement: Devbox 优先文档

README 的「快速开始」SHALL 将 `devbox shell` 列为推荐第一步（在 WSL2/Devcontainer 可用时），Task 命令作为 shell 内操作说明。

#### Scenario: 新开发者 onboarding

- **WHEN** 新开发者按 README 操作
- **THEN** 首要步骤 SHALL 包含安装 Devbox 并执行 `devbox shell`，然后 `task setup:all`
