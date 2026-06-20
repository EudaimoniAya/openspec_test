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

## 本地开发

### 1. 环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
```

### 2. 后端

```bash
cd backend
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173

### 4. Smoke 测试（真实 DeepSeek）

配置 `.env` 后，在前端发送消息，应看到流式 AI 回复。多轮对话会保留同一标签页内的上下文。

## 测试与质量

### 后端

```bash
cd backend
pytest -v
ruff check .
ruff format --check .
mypy app/
```

### 前端

```bash
cd frontend
npm run test
npm run lint
npm run typecheck
```

CI 中**不调用**真实 DeepSeek API，全部使用 mock。

## Docker

```bash
docker compose up --build
```

- 前端: http://localhost:8080
- 后端: http://localhost:8000

## CI

GitHub Actions（`.github/workflows/ci.yml`）在 push/PR 时运行：

- backend: ruff lint/format、mypy、pytest
- frontend: eslint、tsc、vitest
- docker-build: 构建 backend 与 frontend 镜像（不 push）

## TDD 说明

1. 先编写失败测试（红）
2. 实现最小代码使测试通过（绿）
3. 必要时重构

后端 API 测试通过 `dependency_overrides` 注入 mock LLM；前端通过 mock `fetch` 模拟 SSE 流。

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | FastAPI, LangChain, langchain-openai (DeepSeek) |
| 前端 | React 19, TypeScript, Vite |
| 测试 | pytest, Vitest, Testing Library |
| 质量 | ruff, mypy, ESLint, Prettier |
| 容器 | Docker, docker-compose, nginx |
