## ADDED Requirements

### Requirement: 聊天流式接口

系统 SHALL 提供 `POST /api/chat/stream` 接口，接受 JSON 请求体 `{ "session_id": string, "message": string }`，并以 `text/event-stream` 格式返回 DeepSeek 生成的流式 token。

#### Scenario: 成功流式响应

- **WHEN** 客户端发送有效 `session_id` 与非空 `message`
- **THEN** 响应状态码为 200，Content-Type 为 `text/event-stream`
- **THEN** 响应体包含若干 `data: {"token": "<片段>"}` 事件
- **THEN** 流结束时发送 `data: [DONE]`

#### Scenario: 缺少 session_id

- **WHEN** 请求体缺少 `session_id` 或为空字符串
- **THEN** 响应状态码为 422

#### Scenario: 缺少 message

- **WHEN** 请求体缺少 `message` 或为空字符串
- **THEN** 响应状态码为 422

### Requirement: 多轮对话上下文

系统 SHALL 对同一 `session_id` 的连续请求保留短期对话历史，并在调用 DeepSeek 时将历史上下文一并传入。

#### Scenario: 第二轮对话携带上下文

- **WHEN** 同一 `session_id` 先发送「我叫小明」并收到完整回复
- **WHEN** 同一 `session_id` 再发送「我叫什么名字？」
- **THEN** AI 回复 SHALL 体现对上一轮「小明」的上下文理解（在 mock 测试中可通过 memory 状态断言）

#### Scenario: 不同 session 隔离

- **WHEN** `session_id=A` 与 `session_id=B` 分别发送消息
- **THEN** 两个会话的记忆 SHALL 互不影响

### Requirement: API Key 配置

系统 SHALL 从环境变量 `DEEPSEEK_API_KEY` 读取 DeepSeek API 密钥；若未配置且未使用测试 override，启动或首次调用 SHALL 返回明确错误。

#### Scenario: 缺少 API Key

- **WHEN** 环境未设置 `DEEPSEEK_API_KEY` 且未注入测试依赖
- **THEN** 聊天请求 SHALL 返回 503 或 500，并包含可识别的错误信息

### Requirement: CORS 支持

系统 SHALL 配置 CORS，允许前端开发服务器（如 `http://localhost:5173`）访问 API。

#### Scenario: 预检请求

- **WHEN** 浏览器从前端 dev origin 发起跨域 POST
- **THEN** 请求 SHALL 不被 CORS 策略阻止

### Requirement: 健康检查

系统 SHALL 提供 `GET /api/health` 返回 `{ "status": "ok" }`。

#### Scenario: 健康检查成功

- **WHEN** 客户端请求 `GET /api/health`
- **THEN** 响应状态码为 200，body 为 `{ "status": "ok" }`
