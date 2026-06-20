## Why

Windows 原生 PowerShell 中 `task`、`uv` 等工具依赖本机 PATH 安装（如 winget 后需重开终端），导致「命令找不到」和团队环境不一致。需要 **Devbox** 在单个 shell 内提供 OS 级、可复现的开发工具链，与现有 Taskfile 配合，一条命令进入统一环境。

## What Changes

- 新增根目录 **`devbox.json`**，通过 Nix 包声明：`go-task`、`uv`、`nodejs`、`python312` 等
- 新增 **`devbox.lock`**（提交 Git）锁定包版本
- 配置 **`shell.init_hook`**：进入 shell 时提示、可选自动 `task setup:all` 检查
- 配置 **`shell.scripts`**：`devbox run dev`、`devbox run test` 等快捷脚本，内部调用 Taskfile
- 更新 **README**：Devbox 安装与 `devbox shell` 作为**推荐入口**（优先于本机 winget）
- 可选 **`.envrc`**（direnv + `use devbox`）实现 cd 进目录自动激活
- **Windows 说明**：Devbox CLI 需 **WSL2** 或 **Devbox Devcontainer**（Docker Desktop）；原生 PowerShell 不直接运行 devbox

## Capabilities

### New Capabilities

- `devbox-env`：Devbox shell 内统一工具链、与 Taskfile 集成、跨机器可复现

### Modified Capabilities

- `dev-tasks`：文档与推荐流程改为「先 `devbox shell`，再 `task`」

## Impact

- **新增**：`devbox.json`、`devbox.lock`、可选 `.envrc`
- **修改**：`README.md`、`.gitignore`（如 `.devbox/`）
- **不影响**：CI（GitHub Actions 仍用 ubuntu + uv/npm）、应用业务代码
- **用户环境**：Windows 用户需 WSL2 或 Devbox Devcontainer；解决当前 `task` 未进 PATH 的问题

## Non-Goals

- 用 Devbox 替换 Docker 生产部署
- 在 CI 中引入 Devbox（保持现有 workflow）
- 原生 Windows 无 WSL 的完整 Devbox CLI 支持（官方尚未成熟）
