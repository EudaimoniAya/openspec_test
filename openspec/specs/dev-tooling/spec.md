## Purpose

CI/CD、Docker、TDD 与项目质量门禁。

## Requirements

### Requirement: TDD 工作流

项目 SHALL 采用测试驱动开发：在实现功能前先编写失败测试，实现后测试通过，必要时重构。

#### Scenario: 后端 TDD

- **WHEN** 新增后端聊天功能
- **THEN**  SHALL 先存在对应 pytest 测试（API 或 service 层）
- **THEN** 实现代码 SHALL 使测试由红变绿

#### Scenario: 前端 TDD

- **WHEN** 新增前端聊天组件行为
- **THEN** SHALL 先存在 Vitest 组件测试
- **THEN** 实现代码 SHALL 使测试由红变绿

### Requirement: CI 不依赖真实 DeepSeek

GitHub Actions CI SHALL 在不配置 `DEEPSEEK_API_KEY` 的情况下完整运行，通过 mock 或 dependency override 完成测试。

#### Scenario: CI 无密钥运行

- **WHEN** CI workflow 执行 backend-test job
- **THEN** 所有 pytest SHALL 通过且 SHALL NOT 发起真实 DeepSeek HTTP 请求

### Requirement: 后端质量门禁

CI SHALL 对 backend 执行以下检查，任一失败则 workflow 失败：

- ruff lint 与 format 检查
- mypy 类型检查（针对 `app/`）
- pytest 全量测试

所有 backend CI 步骤 SHALL 通过 **uv** 在 `backend/` 目录安装依赖（`uv sync --frozen --dev`），SHALL NOT 使用裸 `pip install -r requirements-dev.txt`。

#### Scenario: CI 使用 uv 安装

- **WHEN** GitHub Actions 运行 backend-test job
- **THEN** SHALL 使用 `uv sync --frozen --dev` 安装依赖
- **THEN** SHALL 使用 `uv run pytest` 执行测试

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

#### Scenario: TypeScript 错误阻断

- **WHEN** 存在 TypeScript 编译错误
- **THEN** `frontend-typecheck` job SHALL 失败

### Requirement: Docker 镜像构建

CI SHALL 成功构建 `backend` 与 `frontend` 的 Docker 镜像，且不 push 到 registry。

#### Scenario: Docker build 成功

- **WHEN** CI 执行 docker-build job 且上游质量 job 均已通过
- **THEN** `docker build` backend 与 frontend SHALL 均 exit 0

#### Scenario: Docker build 依赖质量门禁

- **WHEN** 任一 lint、typecheck 或 test job 失败
- **THEN** docker-build job SHALL NOT 运行或 SHALL 被跳过/失败

### Requirement: 密钥与 Git hygiene

仓库 SHALL 包含 `.env.example` 列出所需环境变量；`.gitignore` SHALL 排除 `.env` 及常见密钥文件；真实 API Key SHALL NOT 提交到 Git。

#### Scenario: env 模板存在

- **WHEN** 开发者 clone 仓库
- **THEN** SHALL 可参照 `.env.example` 创建本地 `.env`

#### Scenario: env 不被跟踪

- **WHEN** 开发者创建 `.env` 文件
- **THEN** Git SHALL NOT 跟踪该文件

### Requirement: 本地 Docker 编排

项目 SHALL 提供 `docker-compose.yml`，使开发者可通过一条命令启动 backend 与 frontend；backend 镜像构建 SHALL 与 uv 锁文件策略一致（使用 `uv.lock` 或等价的锁定安装方式）。

开发者 SHALL 可通过 **`task docker:up`**（或等价 Task 名）启动 compose，作为除直接 `docker compose` 外的推荐方式。

#### Scenario: Compose 启动

- **WHEN** 开发者执行 `docker compose up --build` 或 `task docker:up`
- **THEN** backend 与 frontend 容器 SHALL 启动并可访问

#### Scenario: 文档包含 Task 入口

- **WHEN** 开发者阅读 README Docker 章节
- **THEN** SHALL 同时看到 `task docker:*` 与原始 docker compose 命令

### Requirement: 无 CD

项目 SHALL NOT 配置自动部署（CD）workflow；CI 仅验证质量与构建。

#### Scenario: 无 deploy job

- **WHEN** 查看 `.github/workflows/` 中的 CI workflow
- **THEN** SHALL NOT 存在 push 镜像到 registry 或 deploy 到生产环境的 job

### Requirement: 全局环境清理指引

README SHALL 提供从误装的全局/Conda 环境卸载本项目依赖的指引，并明确推荐仅使用 `backend/.venv`。

#### Scenario: 文档包含清理步骤

- **WHEN** 开发者阅读 README 的 Python 环境章节
- **THEN** SHALL 找到全局误装包的卸载说明与 `uv sync` 正确流程

### Requirement: Task 优先的本地开发文档

README 与本地开发指引 SHALL 将 **Task 命令**列为首选入口，完整 shell 命令作为补充说明。

#### Scenario: 快速开始使用 task

- **WHEN** 新开发者按 README「本地开发」章节操作
- **THEN** 首要步骤 SHALL 为 `task setup:all` 与 `task dev:backend` / `task dev:frontend`
