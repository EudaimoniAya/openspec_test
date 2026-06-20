## Context

当前后端依赖通过 `pip install -r requirements-dev.txt` 安装到用户 Conda 环境（`socket_env`），而非项目隔离环境。项目已有 `pyproject.toml`（工具配置）和 `requirements.txt`（运行时依赖），但缺少锁文件与 venv 约定。

用户已具备 Docker Desktop，且代码已推送 GitHub；本 change 聚焦 Python 环境隔离，并验证 Docker Compose。

## Goals / Non-Goals

**Goals:**

- 所有后端开发与测试命令在 `backend/.venv` 内执行
- 使用 `uv sync` 一键安装/同步依赖，生成 `uv.lock`
- CI 使用 `uv` 替代裸 `pip install`
- 文档明确：禁止在项目外全局安装本项目依赖
- 验证 `docker compose up --build` 可启动前后端

**Non-Goals:**

- 修改聊天业务逻辑或 API 契约
- 强制卸载用户 Conda 中其他无关包（仅文档指引清理本项目误装包）
- 前端包管理变更（继续 npm）

## Decisions

### 1. 工具链：uv + 项目内 .venv

```
backend/
├── pyproject.toml      # 依赖声明 + 工具配置（单一来源）
├── uv.lock             # 锁定版本（提交 Git）
├── .venv/              # 本地虚拟环境（gitignore）
└── requirements.txt    # Docker 用导出（uv export 或 hand-sync）
```

**理由**：uv 速度快、锁文件可复现、与 pyproject 原生集成。

**本地工作流**：

```bash
cd backend
uv venv --python 3.12
uv sync --all-extras --dev
uv run pytest
uv run uvicorn app.main:app --reload
```

### 2. pyproject.toml 依赖分组

```toml
[project]
dependencies = [ ... ]  # 运行时

[dependency-groups]
dev = [ "pytest", "pytest-asyncio", "httpx", "ruff", "mypy" ]
```

使用 PEP 735 `dependency-groups`（uv 原生支持），替代单独的 `requirements-dev.txt`。

**`requirements.txt`**：保留供 Docker `pip install` 使用，通过 `uv export --no-dev -o requirements.txt` 生成，避免 Dockerfile 强依赖 uv（或 Dockerfile 改用 uv，二选一）。

**决策**：Dockerfile 使用 **uv** 安装（更一致），同时提交 `uv.lock`；`requirements.txt` 可作为导出备份或删除（design 选保留 export 以兼容简单 pip 场景）。

### 3. 全局环境污染清理

实施时**不会**自动修改用户 Conda 环境。文档提供：

```bash
# 在误装的全局/conda 环境中执行（示例）
pip uninstall -y fastapi uvicorn pydantic python-dotenv langchain langchain-openai langchain-core \
  pytest pytest-asyncio httpx ruff mypy langsmith anyio ...
```

 packages 列表来自 `pip freeze` 对比项目依赖。用户自行确认后卸载。

### 4. CI 迁移

```yaml
- uses: astral-sh/setup-uv@v5
- run: uv sync --dev
- run: uv run ruff check .
- run: uv run pytest
```

所有 backend job 统一 `working-directory: backend`。

### 5. Docker

**backend/Dockerfile** 改用官方 uv 镜像或 pip 安装 uv：

```dockerfile
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 6. .gitignore 更新

```
backend/.venv/
```

### 7. 补完 add-ai-chatbot 遗留项

| 原任务 | 本 change 处理 |
|--------|----------------|
| 7.4 docker compose 验证 | tasks 中执行并勾选 |
| 8.9 GitHub CI | 用户已推送；CI 更新后再次验证 |
| 9.2 dev 联调 | uv 环境就绪后文档步骤验证 |

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 用户未安装 uv | README 提供 `pip install uv` 或官方安装脚本 |
| Windows 路径/激活问题 | 统一使用 `uv run`，避免手动 activate |
| CI 与本地 lock 不一致 | 提交 `uv.lock`，CI `--frozen` |
| 清理全局包误删其他项目依赖 | 文档强调只卸载本项目相关包，先 `pip freeze` 核对 |

## Migration Plan

1. 扩展 `pyproject.toml` 添加 `[project.dependencies]` 与 dev group
2. 运行 `uv lock` + `uv sync` 创建 `.venv`
3. 用 `uv run` 验证 pytest / ruff / mypy
4. 更新 CI、Dockerfile、README
5. `docker compose up --build` 验证
6. 文档添加全局环境清理步骤

## Open Questions

- （已决）Python 3.12，uv 管理 dev + runtime 依赖
- （已决）Dockerfile 改用 uv sync
