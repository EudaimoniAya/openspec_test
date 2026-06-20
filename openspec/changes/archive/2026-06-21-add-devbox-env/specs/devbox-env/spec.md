## ADDED Requirements

### Requirement: Devbox 配置文件

项目 SHALL 在仓库根目录提供 `devbox.json`，声明开发所需 Nix 包（至少包含 go-task、uv、nodejs、python312）。

#### Scenario: 安装 Devbox 包

- **WHEN** 开发者在项目根目录执行 `devbox install`
- **THEN** SHALL 根据 `devbox.json` 解析并锁定依赖到 `devbox.lock`

#### Scenario: 锁定文件进版本控制

- **WHEN** 开发者查看 Git 跟踪文件
- **THEN** `devbox.lock` SHALL 被提交；`.devbox/` 本地缓存 SHALL 被忽略

### Requirement: Devbox Shell 统一工具链

开发者 SHALL 可通过 `devbox shell` 进入隔离 shell，其中 `task`、`uv`、`node` 命令 SHALL 可直接执行，无需依赖宿主 PATH 中的 winget/scoop 安装。

#### Scenario: Shell 内 task 可用

- **WHEN** 开发者在 `devbox shell` 中执行 `task --list`
- **THEN** SHALL 成功列出 Taskfile 中定义的任务

#### Scenario: Shell 内 uv 可用

- **WHEN** 开发者在 `devbox shell` 中执行 `uv --version`
- **THEN** SHALL 输出版本信息

### Requirement: Devbox Run 脚本

`devbox.json` SHALL 定义 `shell.scripts`，将常用操作委托给 Taskfile（如 setup、test、lint、dev:backend）。

#### Scenario: 快捷测试

- **WHEN** 开发者执行 `devbox run test`
- **THEN** SHALL 等价于在项目根目录执行 `task test:all`

#### Scenario: 快捷启动后端

- **WHEN** 开发者执行 `devbox run dev:backend`
- **THEN** SHALL 等价于 `task dev:backend`

### Requirement: 代理环境变量

Devbox shell SHALL 支持配置 HTTP/HTTPS 代理（默认与本项目 7897 一致），且 SHALL 可在 shell 内被覆盖。

#### Scenario: 默认代理

- **WHEN** 开发者进入 devbox shell 且未覆盖 env
- **THEN** `HTTP_PROXY` SHALL 可用于 docker 等需要代理的命令

### Requirement: Windows 开发指引

README SHALL 说明 Windows 上 Devbox 需 WSL2 或 Devcontainer，并 SHALL 提供从 PowerShell 迁移到 `devbox shell` 的步骤。

#### Scenario: Windows 用户文档

- **WHEN** Windows 用户阅读 README Devbox 章节
- **THEN** SHALL 找到 WSL2 安装、Devbox 安装、`devbox shell` 进入方式的说明
