# AI Chatbot

基于 **FastAPI + React + LangChain + DeepSeek** 的工程化学习项目：多轮对话、SSE 流式输出、TDD 与 GitHub Actions CI。

## 架构

```
React (Vite/TS)  ──POST /api/chat/stream──▶  FastAPI
       ▲                                         │
       │              SSE 流式                   ▼
       └──────────────────────────────  LangChain + DeepSeek
                                        InMemoryChatMessageHistory
```

## 前置要求

**推荐**：通过 [Devbox](https://www.jetify.com/devbox) 进入统一开发 shell（`task`、`uv`、`node` 一次就绪）。

- [Devbox](https://www.jetify.com/devbox)（**推荐**统一工具链；Windows 需 WSL2 或 Devcontainer）
- [go-task](https://taskfile.dev/)（`task` CLI；Devbox 已包含，也可本机安装）
- [uv](https://docs.astral.sh/uv/getting-started/installation/)（Python 包与环境管理；Devbox 已包含）
- Node.js 20+（Devbox 已包含 `nodejs_22`；`nodejs_20` 在最新 nixpkgs 无预编译包，会触发本地编译）
- Docker Desktop（可选，用于 compose 部署）

### Devbox 与 Task / uv .venv 分工

```
宿主 OS (Windows / macOS / Linux)
        │
        ▼
  devbox shell          ← OS 级工具：task, uv, node, python
        │
        ▼
  task setup:all        ← 项目级：uv sync, npm install
  task dev:backend      ← 项目命令（使用 backend/.venv）
```

| 层级 | 职责 | 示例 |
| --- | --- | --- |
| **Devbox** | Shell 内工具二进制 | `task`、`uv`、`node` |
| **Taskfile** | 项目命令编排 | `task dev:backend` |
| **backend/.venv** | Python 依赖隔离 | `uv sync --dev` |

## 快速开始（Devbox 推荐）

### Windows：WSL2 安装 Devbox

原生 PowerShell **不能直接**运行 Devbox CLI。请使用 WSL2：

```bash
# 在 WSL2 终端内
curl -fsSL https://get.jetify.com/devbox | bash

# 进入项目（Windows 盘符挂载路径示例）
cd /mnt/e/projects/openspec_test

devbox shell
```

> **性能提示**：项目在 WSL 文件系统内（如 `~/projects/openspec_test`）比 `/mnt/e/...` 更快；首次 `devbox install` 会从 `cache.nixos.org` 拉取预编译包。

> **Node.js 版本**：`nodejs_20` 在最新 nixpkgs 中已 EOL 且无官方预编译包，会触发本地编译（耗时数十分种）。本项目 Devbox 使用 `nodejs_22`（满足 Node 20+ 要求，可从 cache 直接下载）。WSL 内可运行 `bash scripts/devbox-install.sh`（代理默认 `127.0.0.1:7897`）。

### 进入 shell 后

```bash
cp .env.example .env          # 填入 DEEPSEEK_API_KEY
task setup:all                # 或 devbox run setup
task dev:backend              # 终端 1：后端 :8000
task dev:frontend             # 终端 2：前端 :5173
```

浏览器打开 [http://localhost:5173](http://localhost:5173)

### Devbox 快捷脚本

| 命令 | 等价 Task |
| --- | --- |
| `devbox run setup` | `task setup:all` |
| `devbox run test` | `task test:all` |
| `devbox run lint` | `task lint:all` |
| `devbox run dev:backend` | `task dev:backend` |
| `devbox run dev:frontend` | `task dev:frontend` |

### 可选：direnv 自动激活

安装 [direnv](https://direnv.net/) 后，项目根目录已提供 `.envrc`（`use devbox`），`cd` 进目录可自动进入 Devbox 环境。

### 可选：Cursor / VS Code Devcontainer

需安装 Docker Desktop，在项目根目录执行：

```bash
devbox generate devcontainer
```

然后在 Cursor 中选择 **Dev Containers: Reopen in Container**，容器内已包含 Devbox 工具链，可直接 `task setup:all`。

### Windows 原生 PowerShell：`task` 找不到？

若未使用 Devbox，本机安装 go-task 后 PATH 可能未刷新：

```powershell
# 方案 A（推荐）：改用 WSL2 + devbox shell（见上文）
# 方案 B：winget/scoop 安装后重开终端
winget install GoTask.GoTask
# 关闭并重新打开 PowerShell，再执行 task --list
```

## 快速开始（本机 Task，无 Devbox）

在**仓库根目录**执行（需本机已安装 task、uv、node）：

```bash
cp .env.example .env          # 填入 DEEPSEEK_API_KEY
task setup:all                # 初始化 backend + frontend 依赖
task dev:backend              # 终端 1：后端 :8000
task dev:frontend             # 终端 2：前端 :5173
```

浏览器打开 [http://localhost:5173](http://localhost:5173)

### 安装 go-task（本机 fallback）

```powershell
# Windows (scoop)
scoop install task

# 或 winget
winget install GoTask.GoTask

# 或 Go 安装
go install github.com/go-task/task/v3/cmd/task@latest
```

## Task 命令一览


| 命令                  | 说明                              |
| ------------------- | ------------------------------- |
| `task --list`       | 列出全部任务                          |
| `task setup:all`    | 安装 backend（uv）+ frontend（npm）依赖 |
| `task dev:backend`  | 启动 FastAPI 热重载                  |
| `task dev:frontend` | 启动 Vite 开发服务器                   |
| `task test:all`     | pytest + vitest                 |
| `task test:report`  | 运行测试并生成 Allure HTML 报告        |
| `task lint:all`     | ruff/mypy + eslint/tsc          |
| `task docker:up`    | compose 构建并后台启动（默认代理 7897）      |
| `task docker:down`  | 停止 compose                      |
| `task docker:logs`  | 查看 compose 日志                   |


Docker 任务默认使用 `http://127.0.0.1:7897` 代理；禁用代理示例：

```bash
task docker:up HTTP_PROXY= HTTPS_PROXY=
```

### Cursor / VS Code 运行任务

`Ctrl+Shift+P` → **Tasks: Run Task**，可选：

- **Setup All** / **Backend Dev** / **Frontend Dev**
- **Test All** / **Lint All**
- **Docker Up** / **Docker Down**

## 本地开发（原生命令参考）

### 1. 环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
```

### 2. 后端（uv + 项目内 .venv）

**所有 Python 命令请在 `backend/` 下通过 `uv run` 执行，不要向全局/Conda 环境安装本项目依赖。**

```bash
cd backend
uv sync --dev          # 等价 task setup:backend
uv run pytest -v       # 等价 task test:backend
uv run uvicorn app.main:app --reload --port 8000  # 等价 task dev:backend
```

### 3. 前端

```bash
cd frontend
npm install            # 等价 task setup:frontend
npm run dev            # 等价 task dev:frontend
```

### 4. Smoke 测试（真实 DeepSeek）

配置 `.env` 后，在前端发送消息，应看到流式 AI 回复。多轮对话会保留同一标签页内的上下文。

## Python 环境说明


| 路径                         | 用途                          |
| -------------------------- | --------------------------- |
| `backend/.venv/`           | 项目专用虚拟环境（**gitignore，勿删库**） |
| `backend/pyproject.toml`   | 依赖声明单一来源                    |
| `backend/uv.lock`          | 锁定版本（提交 Git）                |
| `backend/requirements.txt` | `uv export` 导出，供参考/兼容       |


## 清理误装到全局/Conda 的包

若曾用 `pip install -r requirements-dev.txt` 装到 Conda 等全局环境，请在**该环境**中核对后手动卸载（**不会自动执行**）：

```bash
# 1. 查看当前环境已安装包
pip freeze

# 2. 仅卸载本项目相关包（确认后再执行）
pip uninstall -y fastapi uvicorn pydantic python-dotenv langchain langchain-openai langchain-core \
  pytest pytest-asyncio httpx ruff mypy langsmith langgraph langgraph-checkpoint \
  langgraph-prebuilt langgraph-sdk langchain-protocol openai tiktoken
```

之后仅使用 `task setup:backend` 或 `cd backend && uv sync --dev` 管理依赖。

## 测试与质量

等价 Task：`task test:all`、`task lint:all`

### 后端

```bash
cd backend
uv run pytest -v
uv run ruff check .
uv run ruff format --check .
uv run mypy app/
```

### 前端

```bash
cd frontend
npm run test
npm run lint
npm run typecheck
```

CI 中**不调用**真实 DeepSeek API，全部使用 mock。

## 测试报告（Allure）

本地与 CI 均会收集 Allure 结果；本地可生成 HTML，CI 通过 **GitHub Actions Artifacts** 下载。

### 本地生成报告

**前置**：Devbox 环境已包含 JDK 17（Allure CLI 需要 Java）。首次请执行 `task setup:all`（含根目录 `allure-commandline`）。

```bash
task test:report
# 浏览器打开 reports/allure-report/index.html
```

- `task test:backend` / `task test:frontend` 会将结果写入 `reports/allure-results/`
- 即使部分测试失败，`task test:report` 仍会尝试生成报告（便于排查）

仅重新生成 HTML（已有 results 时）：

```bash
bash scripts/allure-report.sh
```

### 从 CI 下载报告

1. 打开 GitHub → **Actions** → 选择对应的 workflow run
2. 在页面底部 **Artifacts** 区域下载 **`allure-report`**
3. 解压后在浏览器打开 `index.html`

测试 job 失败时仍会上传报告（`if: always()`），便于查看失败用例详情。

原始结果 Artifact（可选）：`allure-results-backend`、`allure-results-frontend`。

## Docker

推荐使用 Task（已内置代理 7897）：

```bash
task docker:up
task docker:logs
task docker:down
```

或手动设置代理：

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7897"
$env:HTTPS_PROXY="http://127.0.0.1:7897"
docker compose up --build
```

- 前端: [http://localhost:8080](http://localhost:8080)
- 后端 API（经 nginx 反代）: [http://localhost:8080/api/health](http://localhost:8080/api/health)
- 后端直连（若 8000 端口未被占用）: [http://localhost:8000](http://localhost:8000)

## CI

GitHub Actions（`.github/workflows/ci.yml`）在 push/PR 时运行：

- backend: `uv sync --frozen --dev` → ruff、mypy、pytest（含 Allure 结果）
- frontend: eslint、tsc、vitest（含 Allure 结果）
- **test-report**：合并 Allure 结果并上传 **`allure-report`** Artifact（见上文「测试报告」）
- docker-build: 构建 backend 与 frontend 镜像（不 push）

## TDD 说明

1. 先编写失败测试（红）
2. 实现最小代码使测试通过（绿）
3. 必要时重构

后端 API 测试通过 `dependency_overrides` 注入 mock LLM；前端通过 mock `fetch` 模拟 SSE 流。

## 技术栈


| 层   | 技术                                                      |
| --- | ------------------------------------------------------- |
| 后端  | FastAPI, LangChain, langchain-openai (DeepSeek), **uv** |
| 前端  | React 19, TypeScript, Vite                              |
| 测试  | pytest, Vitest, Testing Library                         |
| 质量  | ruff, mypy, ESLint, Prettier                            |
| 容器  | Docker, docker-compose, nginx                           |
| 任务  | go-task (Taskfile.yml)                                  |
| 开发环境 | Devbox（`devbox.json` + `devbox.lock`）                  |


