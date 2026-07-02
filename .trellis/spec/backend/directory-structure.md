# Backend Directory Structure

> How `kaiwuback/` backend code is organized.

---

## Runtime Shape

`kaiwuback/main.py` is the FastAPI entrypoint. It should stay small: create `app`, install CORS, register route modules, expose `/api/health`, and keep the deprecated `/api/chat` compatibility endpoint.

Reference files:

- `kaiwuback/main.py`
- `kaiwuback/server/api/routes_tasks.py`
- `kaiwuback/server/agent/runtime.py`
- `docs/specs/Spec-007-Task-Agent-Runtime.md`

Do not move new business logic into `main.py` or `/api/chat`. New frontend-facing AI work goes through `/api/tasks` and task events.

---

## Directory Layout

```text
kaiwuback/
├── main.py                         # FastAPI app wiring only
├── requirements.txt
├── report_templates/               # HTML report templates and logo assets
├── skills-files/                   # External skill packs shown by /api/skills
└── server/
    ├── api/                        # Thin FastAPI route registration modules
    ├── agent/                      # TaskService, AgentRuntime, EventStore, state machine
    ├── intent/                     # Intent recognition, follow-up detection, dependency rules
    ├── llm_client/                 # LLM provider registry and provider wrappers
    ├── nodes/                      # Node metadata registry and system prompts
    ├── orchestrator/               # Legacy LLM/report/export orchestration bridges
    ├── persistence/                # Conversation database access and markdown export
    ├── tools/                      # Tool registry and concrete tool adapters
    └── utils/                      # File, markdown, SVG, session, and compatibility helpers
```

Generated user artifacts are stored outside source code:

- `kaiwuback/conversations/`
- `kaiwuback/project-files/`
- `kaiwuback/project-images/`

These folders are data outputs, not coding examples.

---

## API Modules

Route files use `register_*_routes(app)` and keep request validation near the HTTP boundary.

Current examples:

- `server/api/routes_tasks.py` registers task create/debug/events/cancel/retry endpoints.
- `server/api/routes_files.py` registers project file, image, upload, and download endpoints.
- `server/api/routes_conv.py` registers conversation CRUD and manual save endpoints.
- `server/api/routes_skills.py` reads skill metadata from `SKILLS_DIR`.

When adding an endpoint:

- Put it in the closest existing `routes_*.py` file, or create a new `routes_<domain>.py`.
- Register the new route module once in `main.py`.
- Keep orchestration in `server/agent/`, `server/orchestrator/`, `server/tools/`, or `server/utils/`, not inside the route function.

---

## Task Runtime Modules

The task pipeline is the current backend backbone:

- `server/agent/task_service.py` creates, starts, cancels, retries, and streams tasks.
- `server/agent/runtime.py` performs routing, Node execution, event emission, image generation, export bridges, and conversation saving.
- `server/agent/event_store.py` persists `agent_tasks` and `agent_events`, with an in-memory fallback for local development.
- `server/agent/state_machine.py` defines valid task status transitions.
- `server/agent/context_builder.py` normalizes HTTP request data into a task payload.

New task-visible behavior must emit events through `EventStore.write_event()` before the frontend sees it. The SSE endpoint reads stored events; it is not the business executor.

---

## Node And Intent Modules

Node changes are multi-file changes:

- Add/edit Node metadata and prompts in `server/nodes/prompts.py`.
- Keep structured metadata access in `server/nodes/registry.py`.
- Update trigger words, dependency rules, and prerequisite indicators in `server/intent/recognizer.py`.
- Keep behavior aligned with `docs/specs/Spec-001-Node拆分与依赖链.md` and `docs/specs/Spec-003-Intent识别策略.md`.

Node IDs are stable product contracts: `node0`, `node1`, `node1.5`, `node2`, `node3`, `node3.1`, `node4`, `node5`, `export`, `summary`, and `fallback`.

---

## Capability And Utility Boundaries

Use the local capability boundaries before adding new helpers:

- LLM providers: `server/llm_client/router.py` and provider wrappers.
- Future external tools: `server/tools/registry.py` with `ToolSpec`.
- File generation and dual archive: `server/utils/file_io.py`.
- Conversation CRUD: `server/persistence/database.py`.
- Markdown and report rendering: `server/utils/markdown.py`, `server/reports.py`, `server/utils/handbook_renderer.py`.

`server/utils/common.py` is a compatibility re-export layer. Do not add new implementation there; add implementation to the real utility module and only re-export if old imports require it.

---

## Naming Conventions

- Python modules and functions use `snake_case`.
- Route modules use `routes_<domain>.py`.
- Registration functions use `register_<domain>_routes(app)`.
- Task statuses use lowercase strings from `state_machine.py`.
- SSE event types use lowercase snake_case, matching `docs/specs/Spec-002-SSE事件协议.md`.
- Project library folder names must match the existing Chinese folder names exactly, especially `AI 对话产出`.

---

## Current Anti-Patterns

- Do not learn architecture from `kaiwu/src/App.tsx.bak` or any `*.bak` file.
- Do not add new business behavior to `/api/chat`; it is a compatibility bridge.
- Do not bypass task events by streaming direct ad hoc SSE frames from new code.
- Do not add new helpers to `server/utils/common.py` as a dumping ground.
- Do not remove the dual-archive behavior for AI-generated files.
