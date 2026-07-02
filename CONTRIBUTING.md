# Kaiwu 多人协作指南

本文档约定团队在 Kaiwu 仓库中的分支、提交、PR、合并、冲突处理和 AI 协作方式。目标是减少互相覆盖、减少合并冲突，并让每一次变更都能被追踪、回滚和复盘。

## 基本原则

1. `main` 始终保持可运行，不直接在 `main` 上开发。
2. 一个分支只做一类事情，例如一个功能、一个修复、一次文档更新。
3. 小步提交，小 PR 合并。优先让 Review 变简单。
4. 合并前先同步 `main`，合并后再删除已完成分支。
5. 不提交密钥、构建产物、缓存、本地运行状态和生成目录。
6. 不覆盖别人未合并的改动。遇到不确定的冲突，先沟通再处理。

## 分支模型

推荐分支命名：

| 类型 | 示例 | 用途 |
| --- | --- | --- |
| `feature/*` | `feature/task-runtime-dashboard` | 新功能 |
| `fix/*` | `fix/task-event-retry` | Bug 修复 |
| `docs/*` | `docs/collaboration-guide` | 文档更新 |
| `chore/*` | `chore/gitignore-cleanup` | 工具、配置、依赖维护 |
| `codex/*` | `codex/readme-docs` | AI 辅助开发分支 |

创建新分支前先同步：

```powershell
git switch main
git pull --ff-only
git switch -c feature/your-change
```

如果本地 `main` 无法 `--ff-only`，说明本地已有额外提交或历史分叉，不要强推或 reset，先确认当前状态：

```powershell
git status
git log --oneline --graph --decorate -20
```

## 日常开发流程

```powershell
git status
git fetch --prune
git switch main
git pull --ff-only
git switch -c feature/your-change
```

开发过程中保持提交粒度清晰：

```powershell
git status
git diff
git add <files>
git commit -m "feat: add task progress panel"
```

推送并创建 PR：

```powershell
git push -u origin feature/your-change
```

## 提交信息规范

推荐使用 Conventional Commits 风格：

| 前缀 | 示例 | 用途 |
| --- | --- | --- |
| `feat:` | `feat: add task retry button` | 新功能 |
| `fix:` | `fix: prevent duplicate SSE events` | Bug 修复 |
| `docs:` | `docs: add collaboration guide` | 文档 |
| `chore:` | `chore: update gitignore rules` | 工程维护 |
| `refactor:` | `refactor: split task event reducer` | 不改变行为的重构 |
| `test:` | `test: cover task state transitions` | 测试 |

提交建议：

- 一个 commit 表达一个完整意图。
- 不把无关文件混进同一个 commit。
- 不提交 `.env`、`.env.local`、`node_modules/`、`dist/`、`.codex/`、`.trellis/.runtime/`。
- 修改 API、任务事件、节点路由或环境变量时，同步更新 README 或相关文档。

### 中文多段提交模板

推荐用多段 `-m` 写清楚「一句话摘要、整体说明、分模块改动、验证方式、协作者」。提交标题保持简短，提交正文使用中文，方便团队成员快速 Review。

所有提交必须包含至少一行有效 `Co-Authored-By: Name <name@example.com>`，用于标记参与该变更的人或 AI 协作者。没有协作者信息的提交不应合并。

命令模板：

```powershell
git commit `
  -m "<type>(<scope>): <一句话说明>" `
  -m "<本次变更的目标、背景或整体效果。>" `
  -m "主要改动：" `
  -m "- <模块/路径>：<具体改动>" `
  -m "- <模块/路径>：<具体改动>" `
  -m "测试：" `
  -m "- <验证命令或未运行原因>" `
  -m "Co-Authored-By: <协作者姓名> <<协作者邮箱>>"
```

示例：

```powershell
git commit `
  -m "style(ui): 统一基础设计令牌与控件规范" `
  -m "新增全局品牌色、圆角、阴影、动效与焦点令牌，统一基础 UI 组件的控件尺寸和状态反馈。" `
  -m "主要改动：" `
  -m "- app/globals.css：新增 brand、radius、shadow、motion、focus-ring 令牌，并复用到背景、动效和滑杆焦点" `
  -m "- components/ui/button：统一按钮圆角、尺寸、禁用态和过渡时长" `
  -m "- components/ui/card：统一卡片圆角、间距、标题字重和阴影" `
  -m "- components/ui/dialog：统一弹窗圆角、阴影和打开关闭动效" `
  -m "- components/ui/input：统一输入框高度、背景、禁用态和焦点规则" `
  -m "- components/ui/badge：收敛徽标圆角和颜色过渡" `
  -m "测试：" `
  -m "- npm run lint" `
  -m "- npm run build" `
  -m "Co-Authored-By: Codex <codex@example.com>"
```

协作者必须使用完整格式：

```text
Co-Authored-By: Name <name@example.com>
```

提交前必须检查：

- 至少有一行 `Co-Authored-By: Name <name@example.com>`。
- 姓名和邮箱都不能为空。
- 不要提交空的 `Co-Authored-By:` 行。
- 多位协作者可以写多行 `Co-Authored-By`。

### scope 建议

| scope | 适用范围 |
| --- | --- |
| `frontend` | `kaiwu/src/**` 前端整体变更 |
| `ui` | 前端样式、组件、交互细节 |
| `api` | 前后端 API 合约、请求封装、路由 |
| `task` | 任务运行时、SSE、状态机、取消/重试 |
| `agent` | 节点、意图识别、Prompt、LLM 编排 |
| `db` | 数据库 schema、持久化、迁移 SQL |
| `docs` | README、CONTRIBUTING、Trellis 规范等文档 |
| `config` | `.gitignore`、环境变量模板、构建配置 |

分模块写提交正文时，优先写真实路径或稳定模块名，例如：

```text
主要改动：
- kaiwu/src/hooks：调整任务事件订阅与重试状态
- kaiwuback/server/api：补充任务取消接口错误处理
- docs/sql：新增任务事件表索引

测试：
- npm run build
- python -m compileall kaiwuback/server
```

如果没有运行测试，也要写明原因：

```text
测试：
- 未运行前后端构建：仅修改协作文档
```

## PR 规范

每个 PR 建议包含：

- 变更目的：为什么要改。
- 变更范围：改了哪些模块或文档。
- 验证方式：运行过哪些命令。
- 风险说明：是否影响 API、数据库、任务流、SSE、环境变量。
- 截图或录屏：涉及 UI 时提供。

合并前检查：

```powershell
git diff --check
```

前端变更：

```powershell
cd kaiwu
npm run build
```

后端变更：

```powershell
cd kaiwuback
python -m compileall server
```

文档或 `.gitignore` 变更通常不需要跑前后端构建，但需要说明未运行构建的原因。

## 合并策略

### 什么时候用 rebase

适合个人 feature 分支，且没有其他人基于你的分支继续开发。

优点：历史线性、PR 更干净。

```powershell
git fetch origin
git rebase origin/main
```

解决冲突后：

```powershell
git add <resolved-files>
git rebase --continue
```

如果已经把分支推到远端，rebase 后推送使用：

```powershell
git push --force-with-lease
```

只对自己的分支使用 `--force-with-lease`。不要对多人共享分支强推。

### 什么时候用 merge

适合多人共享分支、长期分支，或需要保留完整合并节点的情况。

```powershell
git fetch origin
git merge origin/main
```

解决冲突后：

```powershell
git add <resolved-files>
git commit
git push
```

### PR 合并方式

推荐：

- 小 PR：使用 Squash and merge，让 `main` 历史简洁。
- 多 commit 且每个 commit 有独立价值：使用 Merge commit。
- 不建议在多人协作仓库里随意使用 Rebase and merge，除非团队明确要求线性历史。

## 冲突处理流程

发生冲突时，不要急着删文件或覆盖文件。按下面流程处理：

1. 确认当前状态。

```powershell
git status
```

2. 查看冲突文件。

```powershell
git diff --name-only --diff-filter=U
```

3. 打开冲突文件，处理标记。

```text
<<<<<<< HEAD
当前分支内容
=======
被合并分支内容
>>>>>>> origin/main
```

4. 逐个文件判断保留哪部分，必要时同时保留并手工整合。

5. 解决后检查。

```powershell
git diff --check
git status
```

6. 继续 rebase 或完成 merge。

```powershell
git add <resolved-files>
git rebase --continue
```

或：

```powershell
git add <resolved-files>
git commit
```

7. 运行相关检查，再推送。

冲突处理原则：

- 不确定业务含义时先问对应作者。
- 不用 `git checkout -- <file>` 粗暴覆盖别人的改动。
- 不用 `git reset --hard` 清理工作区，除非团队明确确认可以丢弃本地改动。
- 对生成文件冲突，优先确认是否应该被 `.gitignore` 排除。

## 常用恢复命令

取消 rebase：

```powershell
git rebase --abort
```

取消 merge：

```powershell
git merge --abort
```

临时保存本地改动：

```powershell
git stash push -m "wip: describe current work"
git stash list
git stash pop
```

查看某个文件是谁改的：

```powershell
git blame <file>
```

查看分支图：

```powershell
git log --oneline --graph --decorate --all -30
```

## Trellis 与 AI 协作

本项目使用 Trellis 管理开发上下文，协作时请注意：

- 开始代码或文档变更前，先阅读 `AGENTS.md` 和 `.trellis/workflow.md`。
- 涉及后端时阅读 `.trellis/spec/backend/index.md`。
- 涉及前端时阅读 `.trellis/spec/frontend/index.md`。
- 涉及跨层任务流、SSE、状态、复用时阅读 `.trellis/spec/guides/index.md`。
- `.trellis/spec/` 记录长期规则，应该随架构决策一起维护。
- `.trellis/tasks/` 可以记录任务 PRD、研究和上下文，团队应约定是否随 PR 提交。
- `.trellis/.runtime/`、`.trellis/.developer`、`.codex/` 属于本地状态，不应提交。

AI 辅助开发时：

- 明确告诉 AI 当前任务范围和禁止修改的文件。
- 让 AI 在提交前列出实际改动和验证命令。
- 不让 AI 自动提交未识别的脏文件。
- Review 时优先看 API 合约、SSE 事件、数据库迁移、环境变量和生成产物。

## 文件所有权建议

为了降低冲突，建议按区域拆分负责人：

| 区域 | 路径 | 建议负责人 |
| --- | --- | --- |
| 前端工作台 | `kaiwu/src/features/`, `kaiwu/src/hooks/` | 前端负责人 |
| 前端 API 类型 | `kaiwu/src/api/`, `kaiwu/src/types.ts` | 前后端共同 Review |
| 后端任务运行时 | `kaiwuback/server/agent/` | 后端负责人 |
| 后端 API | `kaiwuback/server/api/` | 后端负责人 |
| 意图与节点 | `kaiwuback/server/intent/`, `kaiwuback/server/nodes/` | Agent 负责人 |
| 数据库 | `docs/sql/`, `kaiwuback/server/persistence/` | 后端负责人 |
| 项目规范 | `.trellis/spec/`, `AGENTS.md`, `CONTRIBUTING.md` | 团队共同 Review |

多人同时修改同一区域时，先拆分任务边界，避免两个 PR 同时改同一个大文件。

## 合并前最终清单

- [ ] 当前分支基于最新 `main`。
- [ ] `git status` 中没有无关文件。
- [ ] `.env`、生成产物和本地运行状态没有进入暂存区。
- [ ] 前端或后端相关检查已运行。
- [ ] README、CONTRIBUTING 或 Trellis spec 已随行为变化更新。
- [ ] commit message 包含有效 `Co-Authored-By: Name <email>`。
- [ ] PR 描述包含变更范围、验证方式和风险说明。
