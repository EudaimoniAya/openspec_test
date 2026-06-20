## MODIFIED Requirements

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

### Requirement: 本地 Docker 编排

项目 SHALL 提供 `docker-compose.yml`，使开发者可通过一条命令启动 backend 与 frontend；backend 镜像构建 SHALL 与 uv 锁文件策略一致（使用 `uv.lock` 或等价的锁定安装方式）。

#### Scenario: Compose 启动

- **WHEN** 开发者执行 `docker compose up --build` 且已配置 `.env`
- **THEN** backend 与 frontend 容器 SHALL 启动并可访问

## ADDED Requirements

### Requirement: 全局环境清理指引

README SHALL 提供从误装的全局/Conda 环境卸载本项目依赖的指引，并明确推荐仅使用 `backend/.venv`。

#### Scenario: 文档包含清理步骤

- **WHEN** 开发者阅读 README 的 Python 环境章节
- **THEN** SHALL 找到全局误装包的卸载说明与 `uv sync` 正确流程
