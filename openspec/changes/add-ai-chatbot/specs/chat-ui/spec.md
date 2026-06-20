## ADDED Requirements

### Requirement: 聊天消息展示

界面 SHALL 以简约布局展示用户消息与 AI 回复，区分发送方（用户 / AI）。

#### Scenario: 初始空状态

- **WHEN** 用户首次打开页面且尚无消息
- **THEN** 界面 SHALL 显示空聊天区域与可用输入框

#### Scenario: 用户发送消息

- **WHEN** 用户输入非空文本并点击发送或按 Enter
- **THEN** 用户消息 SHALL 立即出现在消息列表中
- **THEN** 输入框 SHALL 被清空

### Requirement: 流式打字效果

界面 SHALL 在收到 SSE 流式响应时，将 token 逐段追加到当前 AI 消息，呈现打字机效果。

#### Scenario: 流式渲染

- **WHEN** 后端返回多个 token 事件
- **THEN** AI 消息气泡 SHALL 随 token 到达逐步变长
- **THEN** 流结束（收到 `[DONE]`）后 SHALL 停止追加

#### Scenario: 流式进行中指示

- **WHEN** AI 回复尚未结束
- **THEN** 界面 MAY 显示加载或光标指示（可选，不阻塞功能）

### Requirement: 会话标识

前端 SHALL 为每个浏览器标签页生成并持久化唯一 `session_id`（存于 `sessionStorage`），并在每次聊天请求中携带。

#### Scenario: session 复用

- **WHEN** 用户在同一标签页发送多条消息
- **THEN** 所有请求 SHALL 使用相同 `session_id`

#### Scenario: 新标签页新会话

- **WHEN** 用户在新浏览器标签页打开应用
- **THEN** SHALL 生成不同的 `session_id`

### Requirement: 错误展示

当 API 返回错误或网络失败时，界面 SHALL 向用户展示可读的错误提示，且不崩溃。

#### Scenario: API 错误

- **WHEN** 聊天请求返回 4xx/5xx
- **THEN** 界面 SHALL 显示错误消息（如 toast 或 inline 提示）

#### Scenario: 空输入拦截

- **WHEN** 用户尝试发送空白消息
- **THEN** 界面 SHALL 不发送请求

### Requirement: 简约视觉

界面 SHALL 保持简约：单栏聊天区 + 底部输入栏，无登录、无模型切换、无侧边栏。

#### Scenario: 布局约束

- **WHEN** 用户查看页面
- **THEN** 主要区域 SHALL 仅包含标题（可选）、消息列表、输入框与发送按钮
