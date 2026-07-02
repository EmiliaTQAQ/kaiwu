# Backend Development Guidelines

> Project-specific backend rules for `kaiwuback/`.

---

## Overview

Kaiwu's backend is a FastAPI service under `kaiwuback/`. The current architecture is task-driven:

- `main.py` creates the FastAPI app and registers route modules.
- `server/api/` defines thin HTTP boundaries.
- `server/agent/` owns task lifecycle, persisted events, and runtime orchestration.
- `server/nodes/` and `server/intent/` own Node metadata, prompts, routing, and dependency rules.
- `server/llm_client/`, `server/tools/`, `server/utils/`, and `server/persistence/` provide capability, file, and database infrastructure.

The authoritative product/architecture decisions live in `docs/specs/`. Trellis specs translate those frozen decisions into day-to-day coding guidance for agents.

---

## Guidelines Index

| Guide | Description | Status |
|-------|-------------|--------|
| [Directory Structure](./directory-structure.md) | FastAPI, task runtime, node, utility, and capability boundaries | Filled |
| [Database Guidelines](./database-guidelines.md) | PyMySQL access, task/event persistence, migrations, transaction handling | Filled |
| [Error Handling](./error-handling.md) | API error envelopes, task failure events, image/report partial failures | Filled |
| [Logging Guidelines](./logging-guidelines.md) | Current `print(..., flush=True)` conventions and sensitive-data limits | Filled |
| [Quality Guidelines](./quality-guidelines.md) | Required checks, forbidden patterns, and backend review checklist | Filled |

---

## Pre-Development Checklist

Before changing backend code:

1. Read [Directory Structure](./directory-structure.md).
2. Read the topic-specific guide for the area you touch:
   - Database/task persistence: [Database Guidelines](./database-guidelines.md)
   - API/runtime failures: [Error Handling](./error-handling.md)
   - Observability changes: [Logging Guidelines](./logging-guidelines.md)
   - Any backend change: [Quality Guidelines](./quality-guidelines.md)
3. Read the frozen project spec that owns the behavior:
   - Node routing: `docs/specs/Spec-001-Node拆分与依赖链.md`
   - SSE events: `docs/specs/Spec-002-SSE事件协议.md`
   - Intent matching: `docs/specs/Spec-003-Intent识别策略.md`
   - API keys: `docs/specs/Spec-006-API密钥管理(绝对不做).md`
   - Task runtime: `docs/specs/Spec-007-Task-Agent-Runtime.md`
4. Ignore `*.bak` files and generated files under `project-files/` or `project-images/` when learning current architecture.

---

## Verification

Use the narrowest reliable check for the backend change:

```powershell
python -m compileall kaiwuback/server
```

For cross-layer task/SSE work, also build the frontend:

```powershell
Set-Location kaiwu
npm run build
```
