## 1. Taskfile 编写

- [x] 1.1 创建根目录 `Taskfile.yml`，定义 `version: '3'` 与 vars（如代理默认值）
- [x] 1.2 实现 `setup:*` 任务（backend / frontend / all）
- [x] 1.3 实现 `dev:*` 任务（backend / frontend）
- [x] 1.4 实现 `test:*` 任务（backend / frontend / all）
- [x] 1.5 实现 `lint:*` 任务（backend / frontend / all）
- [x] 1.6 实现 `docker:*` 任务（build / up / down / logs）

## 2. 本地验证 Taskfile

- [x] 2.1 运行 `task --list` 确认任务可见
- [x] 2.2 运行 `task test:all` 确认与手动命令结果一致
- [x] 2.3 运行 `task lint:all` 确认通过

## 3. IDE 集成

- [x] 3.1 创建 `.vscode/tasks.json`（Backend Dev、Frontend Dev、Test All、Lint All、Docker Up、Setup All）
- [x] 3.2 为 dev 任务配置 `isBackground` 与 problemMatcher

## 4. 文档

- [x] 4.1 更新 README：go-task 安装、`task --list`、常用任务表格
- [x] 4.2 将「本地开发」章节改为 Task 优先写法

## 5. 收尾

- [x] 5.1 运行 `openspec validate add-dev-tasks --strict`
- [x] 5.2 确认 Taskfile 不破坏现有 CI（CI 仍用 workflow 内联命令）
