# Backend Database Guidelines

> Database patterns and conventions for `kaiwuback/`.

---

## Overview

The backend uses direct PyMySQL access, not an ORM. Database connection settings are centralized in `server/config.py`, and `server/persistence/database.py` exposes `get_db()` plus conversation CRUD helpers.

Reference files:

- `kaiwuback/server/persistence/database.py`
- `kaiwuback/server/agent/event_store.py`
- `kaiwuback/server/config.py`
- `docs/sql/2026-07-01-agent-tasks-events.sql`
- `docs/specs/Spec-007-Task-Agent-Runtime.md`

---

## Stores

### Conversations

Conversation data is stored in MySQL tables named `conversations` and `messages`, and each saved conversation also writes a markdown copy under `MD_STORE`.

Local pattern:

- `save_conversation()` inserts one conversation row, inserts all message rows, writes a markdown file, then updates `md_file_path`.
- `append_conversation_messages()` appends messages without deleting existing history.
- `update_conversation_messages()` fully replaces an existing conversation's messages.
- `delete_conversation()` deletes the markdown file if present before deleting the database row.

### Agent Tasks And Events

Task data is stored in `agent_tasks` and `agent_events`.

Local pattern:

- `EventStore.ensure_schema()` creates the task/event tables if needed.
- `EventStore.create_task()` stores the normalized task input as JSON.
- `EventStore.write_event()` assigns monotonically increasing per-task `seq` values.
- `TaskService.stream_events()` streams events ordered by `seq`.

The `EventStore` in-memory fallback exists only so local development can boot when MySQL is unavailable. Do not use it as a product persistence strategy.

---

## Query And Transaction Patterns

Follow the existing explicit transaction shape:

```python
db = get_db()
try:
    with db.cursor() as cur:
        cur.execute(...)
    db.commit()
finally:
    db.close()
```

Use `pymysql.cursors.DictCursor` when returning named fields to API code, as in `get_task()` and `list_conversations()`.

Use `json.dumps(..., ensure_ascii=False)` for task payloads and event payloads so Chinese business content is preserved.

---

## Schema And Migration Conventions

Current task/event schema is mirrored in:

- `server/agent/event_store.py`
- `docs/sql/2026-07-01-agent-tasks-events.sql`

When changing schema:

- Update both the runtime schema creation code and the SQL document.
- Keep `agent_events` uniquely indexed by `(task_id, seq)`.
- Keep `agent_tasks` indexed by conversation, status, and update time.
- Preserve `utf8mb4` character set and collation for Chinese content.

---

## Naming Conventions

- Tables use lowercase plural nouns: `conversations`, `messages`, `agent_tasks`, `agent_events`.
- Columns use lowercase snake_case: `conversation_id`, `message_count`, `created_at`, `updated_at`.
- Index names should describe table and fields, such as `idx_agent_events_task`.
- Foreign keys should be explicit when persistence depends on cascade behavior, as in `fk_agent_events_task`.

---

## Sensitive Data

Do not store API keys or external provider tokens in database rows, markdown exports, event payloads, or log messages.

`docs/specs/Spec-006-API密钥管理(绝对不做).md` is the source of truth for secret handling. API keys currently use environment variables loaded from `kaiwuback/.env`; never add real keys to source code or committed docs.

---

## Common Mistakes

- Writing task-visible SSE output without first persisting an `agent_events` row.
- Updating conversation state both from the frontend and backend for the same task. For task-driven conversations, backend `AgentRuntime` is the save owner and the frontend listens for `conversation_saved`.
- Forgetting to close DB connections in `finally`.
- Changing task statuses without `require_transition()`.
- Treating the memory fallback as equivalent to MySQL persistence.
