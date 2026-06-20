## Why

`add-ai-chatbot` 实施阶段通过全局/Conda 环境的 `pip install` 安装了后端依赖，污染了用户本机 Python 环境，且与项目隔离、可复现的工程化目标不符。需要将 Python 依赖管理迁移到项目内的 **uv + `.venv`**，并补完 Docker 本地验证等遗留项。

## What Changes

- 在 `backend/` 使用 **uv** 创建并管理项目本地 **`.venv`**（Python 3.12）
- 将 `pyproject.toml` 作为依赖声明单一来源，生成 **`uv.lock`** 锁定版本
- 移除对全局 `pip install -r requirements*.txt` 的文档与 CI 依赖方式
- **保留** `requirements.txt` 作为 Docker 构建兼容导出（由 uv 同步生成或维护）
- 更新 **README** 与 **CI workflow**：本地与 CI 均通过 `uv sync` 安装依赖
- 更新 **backend/Dockerfile**：可选使用 uv 安装（或继续 pip + 锁定的 requirements）
- 提供**全局环境污染清理指引**（列出曾安装包，用户自行从 Conda 环境卸载）
- 补完 `add-ai-chatbot` 遗留验证：`docker compose up --build` 本地冒烟

## Capabilities

### New Capabilities

- `python-env`：项目内 uv + venv 依赖管理、锁文件、本地开发命令约定

### Modified Capabilities

- `dev-tooling`：CI 与本地开发流程从 pip 迁移到 uv；Docker 构建与文档同步更新

## Impact

- **变更文件**：`backend/pyproject.toml`、`backend/uv.lock`、`.gitignore`、`README.md`、`.github/workflows/ci.yml`、`backend/Dockerfile`
- **新增目录**：`backend/.venv/`（本地，不进 Git）
- **不影响**：聊天 API 行为、前端代码、DeepSeek 集成逻辑
- **用户操作**：需在 Conda/全局环境中手动卸载误装包（文档提供命令）；本地首次运行 `uv sync`
