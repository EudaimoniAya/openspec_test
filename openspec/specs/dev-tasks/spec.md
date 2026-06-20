## Purpose

Taskfile 统一开发命令入口与 IDE 集成。

## Requirements

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

### Requirement: 环境与依赖初始化

Taskfile SHALL 提供 setup 类任务，用于首次或依赖变更后初始化。

#### Scenario: 初始化后端环境

- **WHEN** 开发者执行 `task setup:backend`
- **THEN** SHALL 在 `backend/` 执行 `uv sync --dev`

#### Scenario: 初始化前端依赖

- **WHEN** 开发者执行 `task setup:frontend`
- **THEN** SHALL 在 `frontend/` 执行 `npm install`

#### Scenario: 初始化全部

- **WHEN** 开发者执行 `task setup:all`
- **THEN** SHALL 依次完成 backend 与 frontend 初始化

### Requirement: 测试与 Lint 任务

Taskfile SHALL 提供 test 与 lint 分组任务，命令 SHALL 与 CI 使用的底层工具一致（pytest、vitest、ruff、mypy、eslint、tsc）。

#### Scenario: 运行全部测试

- **WHEN** 开发者执行 `task test:all`
- **THEN** SHALL 运行 backend pytest 与 frontend vitest，任一失败则任务失败

#### Scenario: 运行全部 lint

- **WHEN** 开发者执行 `task lint:all`
- **THEN** SHALL 运行 backend ruff/mypy 与 frontend eslint/typecheck

### Requirement: Docker 任务

Taskfile SHALL 提供 docker 分组任务，封装 compose 构建与启停。

#### Scenario: 构建并启动容器

- **WHEN** 开发者执行 `task docker:up`
- **THEN** SHALL 执行 `docker compose up -d`（或等价 up 任务）

#### Scenario: 停止容器

- **WHEN** 开发者执行 `task docker:down`
- **THEN** SHALL 执行 `docker compose down`

### Requirement: IDE 任务集成

项目 SHALL 提供 `.vscode/tasks.json`，将常用 Task 暴露为 Cursor/VS Code 可运行的任务。

#### Scenario: 从 IDE 启动后端

- **WHEN** 用户在 Cursor 中选择「Run Task → Backend Dev」
- **THEN** SHALL 执行等价于 `task dev:backend` 的命令

#### Scenario: 从 IDE 运行全部测试

- **WHEN** 用户选择「Run Task → Test All」
- **THEN** SHALL 执行等价于 `task test:all` 的命令

### Requirement: 文档

README SHALL 包含「常用 Task」章节，列出推荐任务名与用途；SHALL 说明 go-task 安装方式。

#### Scenario: 文档包含 task 列表

- **WHEN** 开发者阅读 README
- **THEN** SHALL 找到 `task --list` 说明及 setup/dev/test/lint/docker 示例

### Requirement: Devbox 优先文档

README 的「快速开始」SHALL 将 `devbox shell` 列为推荐第一步（在 WSL2/Devcontainer 可用时），Task 命令作为 shell 内操作说明。

#### Scenario: 新开发者 onboarding

- **WHEN** 新开发者按 README 操作
- **THEN** 首要步骤 SHALL 包含安装 Devbox 并执行 `devbox shell`，然后 `task setup:all`
