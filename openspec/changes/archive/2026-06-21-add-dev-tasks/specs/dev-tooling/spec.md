## MODIFIED Requirements

### Requirement: 本地 Docker 编排

项目 SHALL 提供 `docker-compose.yml`，使开发者可通过一条命令启动 backend 与 frontend；backend 镜像构建 SHALL 与 uv 锁文件策略一致（使用 `uv.lock` 或等价的锁定安装方式）。

开发者 SHALL 可通过 **`task docker:up`**（或等价 Task 名）启动 compose，作为除直接 `docker compose` 外的推荐方式。

#### Scenario: Compose 启动

- **WHEN** 开发者执行 `docker compose up --build` 或 `task docker:up`
- **THEN** backend 与 frontend 容器 SHALL 启动并可访问

#### Scenario: 文档包含 Task 入口

- **WHEN** 开发者阅读 README Docker 章节
- **THEN** SHALL 同时看到 `task docker:*` 与原始 docker compose 命令

## ADDED Requirements

### Requirement: Task 优先的本地开发文档

README 与本地开发指引 SHALL 将 **Task 命令**列为首选入口，完整 shell 命令作为补充说明。

#### Scenario: 快速开始使用 task

- **WHEN** 新开发者按 README「本地开发」章节操作
- **THEN** 首要步骤 SHALL 为 `task setup:all` 与 `task dev:backend` / `task dev:frontend`
