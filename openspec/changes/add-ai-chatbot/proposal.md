## Why

项目需要一个小型但工程化的 AI 聊天应用，用于学习 FastAPI + React 全栈开发与 TDD 实践。在具备多轮对话、流式输出等核心功能的同时，通过测试先行、类型检查、代码风格检查、容器构建与 GitHub Actions CI，建立可重复、可验证的交付流程。

## What Changes

- 新增 **FastAPI 后端**：通过 LangChain 集成 DeepSeek，支持多轮对话与 SSE 流式响应
- 新增 **React + TypeScript 前端**：简约聊天界面，展示用户消息与 AI 流式回复
- 采用 **LangChain ConversationBufferMemory** 实现进程内短期会话记忆（按 `session_id` 隔离）
- 采用 **TDD**：先编写测试用例，再实现功能；CI 中不调用真实 DeepSeek API（使用 mock）
- 新增 **Docker** 配置：`backend` 与 `frontend` 镜像及 `docker-compose.yml` 本地编排
- 新增 **GitHub Actions CI**：自动化测试、类型检查（mypy / tsc）、风格检查（ruff / ESLint）、Docker 镜像构建（不部署）
- 新增 **`.env.example`** 与 **`.gitignore`**：API Key 通过本地 `.env` 管理，不提交密钥
- 代码托管至 **GitHub** 仓库

## Capabilities

### New Capabilities

- `chat-api`：聊天 REST/SSE API——会话管理、多轮上下文、流式输出、输入校验
- `chat-ui`：简约 Web 聊天界面——消息展示、流式打字效果、发送与清空会话
- `dev-tooling`：工程化工具链——TDD 工作流、Docker 构建、GitHub Actions CI 质量门禁

### Modified Capabilities

（无——项目尚无既有 spec）

## Impact

- **新增目录**：`backend/`、`frontend/`、`.github/workflows/`、`docker-compose.yml`
- **新增依赖**：LangChain、langchain-openai（DeepSeek 兼容接口）、FastAPI、React、Vitest、pytest、ruff、mypy、ESLint 等
- **运行时**：本地需配置 `DEEPSEEK_API_KEY`；CI 无需真实 API Key
- **Python 版本**：开发与 CI 统一使用 **3.12**
- **Non-goals**：CD/自动部署、数据库持久化、长期记忆、用户认证、E2E 调用真实 DeepSeek API
