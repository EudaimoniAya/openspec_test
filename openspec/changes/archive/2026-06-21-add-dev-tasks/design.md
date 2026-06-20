## Context

当前常用命令分散在 README 各节，典型流程需多次 `cd` 与记忆参数。项目技术栈：

| 服务 | 目录 | 工具 |
|------|------|------|
| 后端 | `backend/` | uv, pytest, ruff, mypy |
| 前端 | `frontend/` | npm, vitest, eslint |
| 全栈容器 | 根目录 | docker compose |

用户希望在 Cursor 与终端中**简单执行**，避免重复输入长命令。

## Goals / Non-Goals

**Goals:**

- 根目录 `task <task-name>` 覆盖 90% 日常开发场景
- Cursor「终端 → 运行任务」可启动 backend / frontend / docker
- 任务命名清晰、分组（setup / dev / test / lint / docker）
- Windows 兼容（用户环境为 win32 + PowerShell）

**Non-Goals:**

- CI 改用 Taskfile（GitHub Actions 保持现有步骤）
- 用 Task 管理 Python/Node 依赖安装工具本身（仍用 uv / npm）
- 复杂编排（watch、进程守护、多终端自动分屏由 IDE 负责）

## Decisions

### 1. 选用 go-task（Taskfile.yml）

**理由**：
- CLI 命令 literally 叫 `task`，符合用户「task 工具」诉求
- 跨平台 YAML，比 Makefile 对 Windows 友好
- 支持 `dir:`、`env:`、`deps:`，可组合任务

**备选**：
- 仅 `.vscode/tasks.json`——终端用户无法受益；**两者都做**
- Makefile——Windows 支持差
- 根 package.json scripts——无法优雅调用 uv/docker

### 2. Taskfile 任务清单

```yaml
# 分组概览
setup:backend      → cd backend && uv sync --dev
setup:frontend     → cd frontend && npm install
setup:all          → deps: setup:backend, setup:frontend

dev:backend        → uv run uvicorn app.main:app --reload --port 8000
dev:frontend       → npm run dev
dev:all            → 提示：需两个终端分别运行 backend/frontend（或 IDE 复合任务）

test:backend       → uv run pytest -v
test:frontend      → npm run test
test:all           → deps 顺序执行

lint:backend       → ruff check + format --check + mypy
lint:frontend      → npm run lint && npm run typecheck
lint:all

docker:build       → docker compose build（可选 HTTP_PROXY env）
docker:up          → docker compose up -d
docker:down        → docker compose down
docker:logs        → docker compose logs -f
```

### 3. 代理环境变量（Docker）

Taskfile 中为 docker 任务预设可选 env（用户本机代理 7897）：

```yaml
env:
  HTTP_PROXY: '{{.HTTP_PROXY | default "http://127.0.0.1:7897"}}'
  HTTPS_PROXY: '{{.HTTPS_PROXY | default "http://127.0.0.1:7897"}}'
```

用户可通过 `task docker:build HTTP_PROXY=` 覆盖为空以禁用。

### 4. VS Code / Cursor 集成

`.vscode/tasks.json`：
- **Backend Dev** → `task dev:backend`（`isBackground: true` + problemMatcher）
- **Frontend Dev** → `task dev:frontend`（background）
- **Run All Tests** → `task test:all`
- **Docker Up** → `task docker:up`
- **Setup All** → `task setup:all`

`options.cwd` 设为 `${workspaceFolder}`。

### 5. 文件结构

```
openspec_test/
├── Taskfile.yml
├── .vscode/
│   └── tasks.json
└── README.md          # 增加「常用 Task」表格
```

### 6. 安装说明

README 增加：

```bash
# Windows (scoop)
scoop install task

# 或 go install
go install github.com/go-task/task/v3/cmd/task@latest
```

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 用户未安装 go-task | README 前置要求 + setup 任务失败时提示安装 |
| `dev:all` 无法单进程跑两个服务 | 文档说明用两个终端或 IDE 分别 Run Task |
| Task 与 CI 命令漂移 | Taskfile 注释注明「与 CI 等价」；test/lint 任务调用相同底层命令 |

## Migration Plan

1. 编写 `Taskfile.yml` 并本地验证各 task
2. 添加 `.vscode/tasks.json`
3. 更新 README「快速开始」以 task 为主
4. 不修改 CI / Dockerfile

## Open Questions

- （已决）使用 go-task + vscode tasks 双轨
- （已决）docker 任务默认带 7897 代理 env，可覆盖
