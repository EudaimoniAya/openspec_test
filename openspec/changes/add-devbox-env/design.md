## Context

用户在本机 PowerShell 执行 `task --list` 失败（`task` 未识别），因 go-task 通过 winget 安装后 PATH 未刷新，且各工具分散安装。项目已有 `Taskfile.yml`（go-task）与 `backend/.venv`（uv），需要一层 **Shell 级工具隔离**，保证进入开发环境后 `task`、`uv`、`node` 均可用。

Devbox 通过 Nix 在 shell 内安装包，不污染宿主 OS，与 Taskfile 互补：Devbox 管**工具二进制**，Task 管**项目命令**。

## Goals / Non-Goals

**Goals:**

- `devbox shell` 后可直接运行 `task --list`、`uv --version`、`node --version`
- 新成员 clone 后：`devbox shell` → `task setup:all` → `task dev:*`
- 锁定 devbox 包版本（`devbox.lock`）
- 文档明确 Windows 路径（WSL2 或 Devcontainer）

**Non-Goals:**

- CI 改用 Devbox
- 移除 Taskfile（Devbox 不替代 task）
- 强制 direnv（可选）

## Decisions

### 1. Devbox 与 Task 的分工

```
宿主 OS (Windows/macOS/Linux)
        │
        ▼
  devbox shell          ← OS 级工具：task, uv, node, python
        │
        ▼
  task setup:all        ← 项目级：uv sync, npm install
  task dev:backend      ← 项目命令
```

### 2. devbox.json 包清单

```json
{
  "$schema": "https://raw.githubusercontent.com/jetify-com/devbox/main/.schema/devbox.schema.json",
  "packages": [
    "go-task@latest",
    "uv@latest",
    "nodejs_20@latest",
    "python312@latest"
  ],
  "env": {
    "HTTP_PROXY": "http://127.0.0.1:7897",
    "HTTPS_PROXY": "http://127.0.0.1:7897"
  },
  "shell": {
    "init_hook": [
      "echo 'Devbox shell 已激活 — 可用 task / uv / node'",
      "task --version || true"
    ],
    "scripts": {
      "setup": "task setup:all",
      "test": "task test:all",
      "lint": "task lint:all",
      "dev:backend": "task dev:backend",
      "dev:frontend": "task dev:frontend"
    }
  }
}
```

代理 env 可在 shell 内覆盖；与 Taskfile 的 PROXY 一致（7897）。

### 3. Windows 策略

| 场景 | 做法 |
|------|------|
| **WSL2（推荐）** | 在 WSL 内 `curl -fsSL https://get.jetify.com/devbox | bash`，项目路径 `/mnt/e/projects/openspec_test`，`devbox shell` |
| **Docker Desktop** | `devbox generate devcontainer` 生成 Devcontainer，Cursor/VS Code Reopen in Container |
| **原生 PowerShell** | 不运行 devbox CLI；继续 winget 安装 task 并重开终端，或改用 WSL |

文档必须写清：用户当前 `task` 找不到，**在 WSL 内 devbox shell 可一劳永逸**。

### 4. 与现有 uv .venv 关系

- Devbox 提供 **uv 二进制**和 **python312**
- `backend/.venv` 仍是项目 Python 依赖隔离（`uv sync`）
- 不冲突：devbox shell 内的 `uv` 调用项目 `backend/.venv`

### 5. IDE 集成

- Cursor/VS Code：安装 Devbox 扩展 →「Reopen in Devbox shell environment」（WSL 内）
- 或 Devcontainer 方式
- 现有 `.vscode/tasks.json` 在 devbox shell 终端中运行 `task` 即可

### 6. 文件与 gitignore

```
devbox.json
devbox.lock          # 提交
.devbox/             # 本地缓存，gitignore
.envrc               # 可选：use devbox
```

### 7. 迁移路径

1. 安装 Devbox（WSL2 或 Devcontainer）
2. `devbox install` 生成 lock
3. `devbox shell`
4. `task setup:all` 验证
5. README 更新推荐流程

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| Windows 原生不支持 Devbox CLI | 文档强调 WSL2/Devcontainer；Taskfile 仍作 fallback |
| 首次 devbox 下载 Nix 包较慢 | 文档说明一次性成本；devbox.lock 复现 |
| Devbox + uv .venv 双层隔离困惑 | README 图解分工 |
| WSL 访问 Windows 文件性能 | 项目放 WSL 文件系统内更佳（`~/projects/`） |

## Open Questions

- （已决）Windows 主路径：WSL2 + devbox shell
- （已决）保留 Taskfile，Devbox 只封装工具链与 `devbox run` 快捷脚本
