# Improve gitignore

## Goal

完善根目录 `.gitignore`，让本地密钥、运行缓存、构建产物、AI 生成产物和平台运行态默认不再进入 Git 状态噪音，避免误提交敏感信息或大批生成文件。

## Requirements

- 保留现有忽略规则，包括 `.codex/`、Python/Node/IDE/OS/对话数据规则。
- 忽略 `.env` 和 `.env.*`，但允许提交安全模板 `.env.example`。
- 补充常见 Python 缓存、虚拟环境、测试/覆盖率产物。
- 补充常见 Node/Vite 构建、缓存、包管理调试日志。
- 忽略 Kaiwu 后端运行生成目录：`kaiwuback/project-files/`、`kaiwuback/project-images/`、`kaiwuback/conversations/`。
- 忽略 Trellis 本地运行态，但不忽略 `.trellis/spec/`、`.trellis/workflow.md`、`.trellis/tasks/` 等项目规范/任务文件。
- 不执行 `git rm --cached`，不改变已跟踪文件状态。

## Acceptance Criteria

- [ ] `git check-ignore` 能命中 `.env`、`.env.local`、`kaiwuback/project-files/*`、`kaiwuback/project-images/*`、Python/Node 缓存产物。
- [ ] `git check-ignore` 不应忽略 `.env.example`。
- [ ] `.gitignore` 分组清晰，可读性高。
- [ ] 不触碰业务代码。

## Definition of Done

- `.gitignore` 已更新。
- 运行 `git check-ignore` 验证关键规则。
- 如无代码变化，不需要跑前后端构建。

## Out of Scope

- 不从 Git 索引移除已经跟踪的 `project-files/` 或 `project-images/` 历史产物。
- 不修改 `.trellis/.gitignore`，除非根规则无法覆盖本任务目标。
- 不改 `.codex/` 是否应跟踪的策略；本任务保留当前根 `.gitignore` 中已有 `.codex/` 规则。

## Technical Notes

- 当前根 `.gitignore` 已包含 `.env.local`、Python/Node 基础缓存、IDE/OS、`conversations/`、`.venv/`、`.codex/`。
- `.trellis/.gitignore` 已忽略 `.developer`、`.runtime/`、`.agents/`、缓存和临时文件。
- 当前 `kaiwuback/.env.local` 已被 `.gitignore:2` 命中。
- 当前 `kaiwu/dist/` 已被 `dist/` 命中。
- 现有 `kaiwuback/project-files/` 和 `kaiwuback/project-images/` 中大量文件已被 Git 跟踪；新增 ignore 规则不会自动取消跟踪。
