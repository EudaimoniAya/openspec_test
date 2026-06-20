## Context

当前仓库仅有 OpenSpec 脚手架，无业务代码。目标是在学习场景下构建一个工程化的小型 AI 聊天应用：用户通过 Web 界面输入问题，后端经 LangChain 调用 DeepSeek 返回答复，支持多轮对话与流式输出。项目采用 TDD，代码提交 GitHub，并通过 CI 验证质量；不要求 CD。

约束：
- 技术栈：FastAPI（Python 3.12）+ React（TypeScript）+ LangChain + DeepSeek
- 短期记忆：LangChain `ConversationBufferMemory`，进程内按 `session_id` 隔离
- API Key：`.env` 本地配置，不进 Git
- CI 不调用真实 DeepSeek API

## Goals / Non-Goals

**Goals:**

- 提供可用的多轮 AI 聊天功能（流式 SSE）
- 前后端分层清晰，核心业务可单元测试
- TDD 工作流：先写失败测试，再实现，再重构
- GitHub Actions CI 覆盖：测试、类型检查、风格检查、Docker 构建
- 本地可通过 `docker-compose up` 一键启动

**Non-Goals:**

- CD / 自动部署到云环境
- 数据库或文件持久化（重启后会话记忆丢失可接受）
- 用户认证、多租户、速率限制
- CI 或 E2E 中调用真实 DeepSeek API
- 复杂 UI（侧边栏、模型切换、附件等）

## Decisions

### 1. 整体架构：前后端分离 + SSE 流式

```
React (Vite, TS)  ──POST /api/chat/stream──▶  FastAPI
       ▲                                              │
       │         SSE (text/event-stream)              │
       └──────────────────────────────────────────────┘
                              │
                              ▼
                    ChatService (LangChain)
                    ├─ ChatOpenAI (DeepSeek base_url)
                    └─ ConversationBufferMemory (per session)
```

**理由**：前后端分离符合 FastAPI + React 技术栈；SSE 语义清晰，便于前端逐 token 渲染。

**备选**：WebSocket——对流式聊天无显著优势，SSE 更简单。

### 2. 后端分层

| 层 | 职责 |
|----|------|
| `routers/chat.py` | HTTP 路由、请求校验、StreamingResponse |
| `services/chat_service.py` | LangChain 链、流式生成、写入 memory |
| `memory/session_store.py` | `dict[session_id, ConversationBufferMemory]` |

**理由**：路由与 LangChain 解耦，测试时可 mock `ChatService`，符合 TDD。

### 3. LangChain 集成 DeepSeek

使用 `langchain-openai` 的 `ChatOpenAI`，配置：

- `base_url`: `https://api.deepseek.com`
- `model`: `deepseek-chat`
- `api_key`: 从环境变量 `DEEPSEEK_API_KEY` 读取

**理由**：DeepSeek 兼容 OpenAI API，LangChain 生态成熟，文档丰富。

**备选**：`langchain-deepseek` 专用包——可用，但 OpenAI 兼容层更通用。

### 4. 会话记忆

- 前端首次加载生成 `session_id`（UUID），存 `sessionStorage`
- 后端 `SessionStore` 维护 `session_id → ConversationBufferMemory`
- 流式响应**结束后**将完整 AI 回复写入 memory（避免半截写入）

**理由**：`ConversationBufferMemory` 是 LangChain 最简单的短期记忆，满足 demo 需求。

### 5. 流式协议（SSE）

事件格式：

```
data: {"token": "你"}\n\n
data: {"token": "好"}\n\n
data: [DONE]\n\n
```

错误时：

```
data: {"error": "message"}\n\n
```

**理由**：JSON payload 便于扩展；`[DONE]` 明确结束边界。

### 6. 前端技术选型

- **Vite + React 18 + TypeScript**
- **Vitest + Testing Library** 组件测试
- **ESLint + Prettier** 风格
- 开发时代理：`vite.config.ts` 将 `/api` 代理到 `http://localhost:8000`

UI：白底、消息气泡（用户右/AI 左）、底部输入框，无多余装饰。

### 7. 测试策略（TDD）

| 层级 | 工具 | Mock 策略 |
|------|------|-----------|
| 后端单元 | pytest | mock `ChatService.stream()` |
| 后端 API | httpx AsyncClient + TestClient | `app.dependency_overrides` 注入 fake service |
| 前端单元 | Vitest | mock `fetch` / stream reader |
| CI | 同上 | 无 `DEEPSEEK_API_KEY` |

**TDD 顺序**：先写 API 契约测试 → 实现 service → 写组件测试 → 实现 UI。

### 8. 质量工具

**后端（pyproject.toml）：**

- `ruff`：lint + format
- `mypy`：类型检查（`strict` 可选，至少检查 `app/`）
- `pytest` + `pytest-asyncio` + `httpx`

**前端：**

- `tsc --noEmit`
- `eslint` + `prettier`
- `vitest run`

### 9. Docker

- `backend/Dockerfile`：`python:3.12-slim`，uvicorn 启动
- `frontend/Dockerfile`：multi-stage，`node:20` build → `nginx:alpine` 托管静态文件
- `docker-compose.yml`：backend 端口 8000，frontend 端口 80，backend 读 `.env`

CI 仅 `docker build`，不 push registry。

### 10. GitHub Actions CI

单 workflow `ci.yml`，`push` / `pull_request` 触发：

| Job | 命令 |
|-----|------|
| `backend-lint` | `ruff check .` + `ruff format --check .` |
| `backend-typecheck` | `mypy app/` |
| `backend-test` | `pytest` |
| `frontend-lint` | `npm run lint` |
| `frontend-typecheck` | `npm run typecheck` |
| `frontend-test` | `npm run test` |
| `docker-build` | `needs` 上述 job，`docker build` backend + frontend |

`docker-build` 作为 merge 门禁（全部通过才绿）。

### 11. 目录结构

```
├── .github/workflows/ci.yml
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/chat.py
│   │   ├── services/chat_service.py
│   │   ├── memory/session_store.py
│   │   └── schemas/chat.py
│   ├── tests/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| LangChain API 版本变动 | 锁定 `requirements.txt` 版本；CI 锁定依赖 |
| 流式 + Memory 时序错误 | 仅在 stream 完整结束后写入 memory；单测覆盖 |
| 进程内 memory 无上限 | demo 可接受；可加 session 数量上限（可选） |
| Docker 构建慢 | CI 使用 layer cache；frontend multi-stage 减小镜像 |
| DeepSeek API 本地不可用 | 开发用 mock；真实 Key 仅本地手动 smoke |
| Python 3.14 与 CI 3.12 不一致 | 文档与 CI 统一 3.12 |

## Migration Plan

不适用（绿field 项目）。实施步骤见 `tasks.md`：

1. 初始化仓库结构与工具链
2. TDD 实现后端
3. TDD 实现前端
4. Docker + compose
5. GitHub Actions
6. README 与 `.env.example`

## Open Questions

- （已决）Python 3.12、TypeScript、docker-build 作为 CI 必过项——按上述设计执行
- 是否在 README 中记录本地 smoke 测试步骤（调用真实 DeepSeek）——建议有，但不进 CI
