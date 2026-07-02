<!-- TRELLIS:START -->
# Trellis Instructions

These instructions are for AI assistants working in this project.

This project is managed by Trellis. The working knowledge you need lives under `.trellis/`:

- `.trellis/workflow.md` - development phases, when to create tasks, skill routing
- `.trellis/spec/` - package- and layer-scoped coding guidelines (read before writing code in a given layer)
- `.trellis/workspace/` - per-developer journals and session traces
- `.trellis/tasks/` - active and archived tasks (PRDs, research, jsonl context)

If a Trellis command is available on your platform (for example `/trellis:finish-work` or `/trellis:continue`), prefer it over manual steps. Not every platform exposes every command.

If you're using Codex or another agent-capable tool, additional project-scoped helpers may live in:

- `.agents/skills/` - reusable Trellis skills
- `.codex/agents/` - optional custom subagents

Managed by Trellis. Edits outside this block are preserved; edits inside may be overwritten by a future `trellis update`.

<!-- TRELLIS:END -->

# Kaiwu Agent Notes

本项目是曜势科技 Kaiwu：前端在 `kaiwu/`，后端在 `kaiwuback/`，面向 OPC 创业者提供需求洞察、商业方案、产品创造和营销推广工作流。

## 开始前

- 先按 Trellis 当前任务状态行动；代码或文档变更前读取相关 `.trellis/spec/`。
- 已冻结业务决策在 `docs/specs/`，开发速查在 `docs/00-文件索引-开发速查.md`。
- 不要从 `*.bak`、`project-files/`、`project-images/` 学当前架构；这些是历史备份或生成产物。

## 架构边界

- 后端入口 `kaiwuback/main.py` 只做 FastAPI app 和路由注册；新业务放到 `server/api/`、`server/agent/`、`server/nodes/`、`server/intent/`、`server/tools/`、`server/utils/` 等对应层。
- AI 对话新流程走 `/api/tasks` + `/api/tasks/{id}/events`；`/api/chat` 只保留兼容，不新增业务逻辑。
- 前端 `kaiwu/src/App.tsx` 主要负责状态持有和 wiring；新复杂 UI 优先拆到 `src/features/*`，新副作用优先放到 `src/hooks/*`。
- 前端事件链是 `useSseEvents -> useAgentTask -> agentEventReducer / agentTaskController -> UI`，不要在组件里重复解析 SSE。

## 业务硬约束

- API 密钥、Token、密码不能写入源码或提交记录；密钥走环境变量或 `kaiwuback/.env`。
- AI 生成文件必须保留双归档：对应分类文件夹 + `AI 对话产出`。
- 普通对话按钮和 AI 生图按钮必须区分；AI 视频、AI 编程沿用普通对话按钮。
- 对话重命名功能必须保留。
- 任务驱动对话由后端保存，前端通过 `conversation_saved` 更新会话 ID 和历史列表。

## 常用验证

后端语法检查：

```powershell
python -m compileall kaiwuback/server
```

前端构建：

```powershell
Set-Location kaiwu
npm run build
```

跨前后端任务/SSE 改动通常需要两个检查都跑。
