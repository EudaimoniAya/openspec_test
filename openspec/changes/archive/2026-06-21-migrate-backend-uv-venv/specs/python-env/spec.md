## ADDED Requirements

### Requirement: 项目内虚拟环境

后端开发 SHALL 使用 `backend/.venv` 作为唯一 Python 运行环境，SHALL NOT 要求向全局或 Conda 环境安装项目依赖。

#### Scenario: 首次环境初始化

- **WHEN** 开发者在 `backend/` 执行 `uv sync`
- **THEN** SHALL 创建或更新 `backend/.venv`
- **THEN** SHALL 根据 `pyproject.toml` 与 `uv.lock` 安装全部运行时与开发依赖

#### Scenario: venv 不进入版本控制

- **WHEN** 开发者查看 Git 状态
- **THEN** `backend/.venv/` SHALL 被 `.gitignore` 忽略

### Requirement: 锁文件可复现

项目 SHALL 在 `backend/uv.lock` 中锁定依赖版本，并提交至 Git。

#### Scenario: 冻结安装

- **WHEN** CI 或新开发者执行 `uv sync --frozen`
- **THEN** 安装的包版本 SHALL 与 `uv.lock` 一致

### Requirement: 统一运行命令

开发与测试命令 SHALL 通过 `uv run` 在项目 venv 中执行，无需手动激活。

#### Scenario: 运行测试

- **WHEN** 开发者执行 `uv run pytest`
- **THEN** SHALL 使用 `backend/.venv` 中的 pytest 运行全部测试

#### Scenario: 启动开发服务器

- **WHEN** 开发者执行 `uv run uvicorn app.main:app --reload`
- **THEN** SHALL 使用项目 venv 中的 uvicorn 启动服务

### Requirement: 依赖声明单一来源

运行时与开发依赖 SHALL 声明在 `backend/pyproject.toml`，SHALL NOT 仅存在于未锁定的 `requirements-dev.txt`。

#### Scenario: pyproject 包含运行时依赖

- **WHEN** 查看 `backend/pyproject.toml`
- **THEN** `[project].dependencies` SHALL 列出 fastapi、langchain 等运行时包

#### Scenario: pyproject 包含开发依赖

- **WHEN** 查看 `backend/pyproject.toml`
- **THEN** `[dependency-groups].dev` SHALL 列出 pytest、ruff、mypy 等开发工具
