## Why

项目已有 backend（uv）、frontend（npm）、Docker Compose 等多套命令，分散在 README 中，开发者需记忆路径与参数。需要统一的 **Task** 入口，在终端一条命令即可执行常见开发与质量检查操作。

## What Changes

- 新增根目录 **`Taskfile.yml`**（[go-task](https://taskfile.dev/)），封装：
  - 环境初始化（`uv sync`、npm install）
  - 本地开发（backend / frontend / 全栈）
  - 测试与 lint（backend / frontend / 全部）
  - Docker compose 启停与构建
- 新增 **`.vscode/tasks.json`**，将 Task 映射为 Cursor/VS Code「运行任务」，支持一键启动
- 更新 **README**：以 `task <name>` 作为推荐入口，保留原生命令作为参考
- **Non-goals**：不替换 CI workflow；不引入 Makefile 与 npm workspaces  monorepo 改造

## Capabilities

### New Capabilities

- `dev-tasks`：统一任务入口——开发、测试、lint、Docker 的标准化命令与 IDE 集成

### Modified Capabilities

- `dev-tooling`：本地开发流程文档与推荐命令从「分散 shell 片段」改为「Task 优先」

## Impact

- **新增文件**：`Taskfile.yml`、`.vscode/tasks.json`
- **修改文件**：`README.md`
- **依赖**：开发者需安装 go-task（`task` CLI）；CI 不依赖 Taskfile
- **平台**：Taskfile 需兼容 Windows（PowerShell/cmd）与现有代理场景（Docker 可选 env）
