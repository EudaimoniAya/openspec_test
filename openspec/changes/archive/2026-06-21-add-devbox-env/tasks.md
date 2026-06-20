## 1. Devbox 配置

- [x] 1.1 创建 `devbox.json`（go-task、uv、nodejs_22、python312、env 代理；nodejs_20 改为 nodejs_22 以使用 cache 预编译包）
- [x] 1.2 运行 `devbox install` 生成 `devbox.lock`
- [x] 1.3 配置 `shell.scripts`（setup / test / lint / dev:backend / dev:frontend）
- [x] 1.4 更新 `.gitignore` 忽略 `.devbox/`

## 2. 验证 Devbox Shell

- [x] 2.1 在 devbox shell 内执行 `task --list` 成功
- [x] 2.2 在 devbox shell 内执行 `devbox run test` 成功
- [x] 2.3 在 devbox shell 内执行 `task setup:all` 成功

## 3. Windows / IDE 支持

- [x] 3.1 文档：WSL2 安装 Devbox 与进入项目路径说明
- [x] 3.2 可选：运行 `devbox generate devcontainer` 并文档化 Cursor Devcontainer 流程（README 已文档化；生成命令需在本地 Docker 可用时执行）
- [x] 3.3 可选：添加 `.envrc`（`use devbox`）供 direnv 用户

## 4. 文档更新

- [x] 4.1 更新 README：Devbox 优先快速开始、与 Task/uv .venv 分工图
- [x] 4.2 说明原生 PowerShell 下 `task` 找不到的解决方式（WSL devbox 或重开终端刷新 PATH）

## 5. 收尾

- [x] 5.1 确认 CI 不变（仍用 GitHub Actions 内联 uv/npm）
- [x] 5.2 运行 `openspec validate add-devbox-env --strict`
