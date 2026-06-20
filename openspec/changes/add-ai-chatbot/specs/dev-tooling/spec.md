## ADDED Requirements

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

- `ruff check` 与 `ruff format --check`
- `mypy` 类型检查（针对 `app/`）
- `pytest` 全量测试

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

### Requirement: 密钥与 Git  hygiene

仓库 SHALL 包含 `.env.example` 列出所需环境变量；`.gitignore` SHALL 排除 `.env` 及常见密钥文件；真实 API Key SHALL NOT 提交到 Git。

#### Scenario: env 模板存在

- **WHEN** 开发者 clone 仓库
- **THEN** SHALL 可参照 `.env.example` 创建本地 `.env`

#### Scenario: env 不被跟踪

- **WHEN** 开发者创建 `.env` 文件
- **THEN** Git SHALL NOT 跟踪该文件

### Requirement: 本地 Docker 编排

项目 SHALL 提供 `docker-compose.yml`，使开发者可通过一条命令启动 backend 与 frontend。

#### Scenario: Compose 启动

- **WHEN** 开发者执行 `docker compose up --build` 且已配置 `.env`
- **THEN** backend 与 frontend 容器 SHALL 启动并可访问

### Requirement: 无 CD

项目 SHALL NOT 配置自动部署（CD）workflow；CI 仅验证质量与构建。

#### Scenario: 无 deploy job

- **WHEN** 查看 `.github/workflows/` 中的 CI workflow
- **THEN** SHALL NOT 存在 push 镜像到 registry 或 deploy 到生产环境的 job
