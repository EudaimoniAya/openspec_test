## 1. 项目脚手架与 Git

- [x] 1.1 初始化 Git 仓库，创建 `.gitignore`（排除 `.env`、`__pycache__`、`node_modules`、`dist` 等）
- [x] 1.2 创建 `.env.example`（`DEEPSEEK_API_KEY`、`DEEPSEEK_MODEL=deepseek-chat`）
- [x] 1.3 创建根目录 `README.md`：项目简介、本地开发步骤、CI 说明、smoke 测试指引

## 2. 后端脚手架与工具链

- [x] 2.1 创建 `backend/` 目录结构（`app/`、`tests/`、`pyproject.toml`、`requirements.txt`、`requirements-dev.txt`）
- [x] 2.2 配置 ruff（lint + format）与 mypy（`app/` 类型检查）
- [x] 2.3 配置 pytest + pytest-asyncio + httpx 测试环境
- [x] 2.4 实现 `GET /api/health` 及对应测试（首个绿测试，验证脚手架）

## 3. 后端 TDD — Chat API（mock LLM）

- [x] 3.1 编写 `test_chat_api.py`：缺少 `session_id` / `message` 返回 422（红）
- [x] 3.2 编写 `test_chat_api.py`：有效请求返回 200 + SSE 流（mock ChatService）（红）
- [x] 3.3 实现 `schemas/chat.py` 请求体 Pydantic 模型
- [x] 3.4 实现 `memory/session_store.py`：`session_id → ConversationBufferMemory`
- [x] 3.5 实现 `services/chat_service.py`：LangChain 链 + `stream()` 接口（可注入 mock LLM）
- [x] 3.6 实现 `routers/chat.py`：`POST /api/chat/stream` + StreamingResponse（绿）
- [x] 3.7 编写 `test_chat_service.py`：同一 session 第二轮请求 memory 含历史（红 → 绿）
- [x] 3.8 编写 `test_chat_service.py`：不同 session 记忆隔离（红 → 绿）
- [x] 3.9 实现流式结束后写入 memory 的逻辑
- [x] 3.10 配置 CORS 并添加 API 测试
- [x] 3.11 实现缺少 `DEEPSEEK_API_KEY` 时的错误处理及测试

## 4. 后端 — 真实 DeepSeek 集成（本地 smoke，非 CI）

- [x] 4.1 在 `ChatService` 中接入 `ChatOpenAI`（`base_url=https://api.deepseek.com`）
- [x] 4.2 本地配置 `.env` 手动验证流式多轮对话（文档写入 README）

## 5. 前端脚手架与工具链

- [x] 5.1 使用 Vite 创建 React + TypeScript 项目（`frontend/`）
- [x] 5.2 配置 ESLint + Prettier + Vitest + Testing Library
- [x] 5.3 配置 `vite.config.ts` 开发代理 `/api` → `http://localhost:8000`
- [x] 5.4 添加 `npm run lint`、`npm run typecheck`、`npm run test` 脚本

## 6. 前端 TDD — Chat UI

- [x] 6.1 编写 `Chat.test.tsx`：初始空状态渲染（红）
- [x] 6.2 编写 `Chat.test.tsx`：发送消息后用户气泡出现（红）
- [x] 6.3 编写 `Chat.test.tsx`：空白输入不发送（红）
- [x] 6.4 实现 `sessionStorage` UUID `session_id` 工具函数及测试
- [x] 6.5 实现 `api/chat.ts`：SSE fetch 流式读取（可 mock Response body）
- [x] 6.6 编写 `Chat.test.tsx`：mock stream 逐 token 追加 AI 消息（红 → 绿）
- [x] 6.7 实现 `Chat.tsx` 组件：消息列表 + 输入框 + 发送（绿）
- [x] 6.8 实现 API 错误 inline 提示及测试
- [x] 6.9 实现简约 CSS 布局（单栏 + 底部输入栏）

## 7. Docker

- [x] 7.1 编写 `backend/Dockerfile`（python:3.12-slim + uvicorn）
- [x] 7.2 编写 `frontend/Dockerfile`（node build + nginx 静态托管）
- [x] 7.3 编写 `docker-compose.yml`（backend:8000、frontend:80、env_file）
- [ ] 7.4 本地验证 `docker compose up --build` 可访问聊天界面

## 8. GitHub Actions CI

- [x] 8.1 创建 `.github/workflows/ci.yml`
- [x] 8.2 添加 `backend-lint` job（ruff check + ruff format --check）
- [x] 8.3 添加 `backend-typecheck` job（mypy app/）
- [x] 8.4 添加 `backend-test` job（pytest，无 DEEPSEEK_API_KEY）
- [x] 8.5 添加 `frontend-lint` job（eslint）
- [x] 8.6 添加 `frontend-typecheck` job（tsc --noEmit）
- [x] 8.7 添加 `frontend-test` job（vitest run）
- [x] 8.8 添加 `docker-build` job（needs 上述 job，build backend + frontend 镜像，不 push）
- [ ] 8.9 推送至 GitHub 验证 CI 全绿

## 9. 收尾

- [x] 9.1 运行 `openspec validate add-ai-chatbot --strict` 确认 change 合法
- [ ] 9.2 前后端联调：dev 模式下完整多轮流式对话
- [x] 9.3 更新 README：架构图、TDD 说明、CI badge（可选）
