## 1. pyproject 与 uv 初始化

- [x] 1.1 在 `backend/pyproject.toml` 添加 `[project.dependencies]` 与 `[dependency-groups].dev`
- [x] 1.2 运行 `uv lock` 生成 `backend/uv.lock`
- [x] 1.3 运行 `uv venv --python 3.12` 与 `uv sync --dev` 创建 `backend/.venv`
- [x] 1.4 更新 `.gitignore` 忽略 `backend/.venv/`

## 2. 验证项目内环境

- [x] 2.1 使用 `uv run pytest -v` 确认全部后端测试通过
- [x] 2.2 使用 `uv run ruff check .` 与 `uv run ruff format --check .` 通过
- [x] 2.3 使用 `uv run mypy app/` 通过

## 3. 清理与文档

- [x] 3.1 运行 `uv export --no-dev -o requirements.txt` 更新 Docker 用 requirements（或标记弃用）
- [x] 3.2 删除或归档 `requirements-dev.txt`，避免与 uv 重复
- [x] 3.3 更新 README：uv 安装、`uv sync`、`uv run` 开发流程
- [x] 3.4 添加「全局/Conda 误装包清理」章节（pip uninstall 指引，不自动执行）

## 4. CI 迁移

- [x] 4.1 在 `.github/workflows/ci.yml` 添加 `astral-sh/setup-uv@v5`
- [x] 4.2 backend-lint/typecheck/test 改为 `uv sync --frozen --dev` + `uv run`
- [ ] 4.3 推送后确认 GitHub Actions 全绿（本地改动尚未 push，push 后于 GitHub 查看 CI）

## 5. Docker 更新与验证

- [x] 5.1 更新 `backend/Dockerfile` 使用 uv + `uv.lock` 安装依赖
- [x] 5.2 本地执行 `docker compose up --build` 验证前后端可访问（代理 7897 下构建成功；8080 与 /api/health 正常）
- [x] 5.3 勾选 `add-ai-chatbot` 遗留任务 7.4（docker compose 验证）

## 6. 收尾

- [x] 6.1 使用 uv 环境完成 dev 模式前后端联调（`add-ai-chatbot` 任务 9.2）
- [x] 6.2 运行 `openspec validate migrate-backend-uv-venv --strict`
- [x] 6.3 确认 `add-ai-chatbot` 任务 8.9 已由用户推送完成并勾选
