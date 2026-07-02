# Backend Logging Guidelines

> Current logging conventions for `kaiwuback/`.

---

## Overview

The project currently uses simple `print(..., flush=True)` logging, not the Python `logging` module. Logs are short operational breadcrumbs for local development and debugging long-running AI tasks.

Reference files:

- `server/agent/runtime.py`
- `server/agent/event_store.py`
- `server/llm_client/seedream.py`
- `server/orchestrator/llm_engine.py`
- `server/utils/file_io.py`

---

## Prefixes

Use bracketed prefixes that identify the subsystem:

| Prefix | Used for |
|--------|----------|
| `[TASK]` | Task execution failures and lifecycle issues |
| `[EVENT_STORE]` | MySQL availability and fallback behavior |
| `[INTENT]` | Intent routing decisions and LLM intent failures |
| `[LLM]` | LLM generation failures |
| `[RESPONSE]` | Final Node response length and error flag |
| `[IMG]` / `[IMAGE]` | Image save and generation failures |
| `[SVG]` | SVG generation failures |
| `[FILE]` | Project file save operations |
| `[DB]` | Conversation save failures |
| `[PDF]` | PDF conversion failures |
| `[UPLOAD]` | Upload parsing results |
| `[REPORT]` | Report template/node detection |

New logs should follow the same prefix style.

---

## What To Log

Log compact facts that help reproduce task/runtime failures:

- Task ID and failure summary.
- Provider status code and truncated response text.
- Node ID, response length, and whether an LLM error happened.
- File save location by folder and filename.
- Image style generation failures.
- MySQL fallback activation.
- Upload parse success/failure by filename and page/character counts.

---

## What Not To Log

Never log:

- API keys, tokens, passwords, or Authorization headers.
- Full user conversations.
- Full uploaded file content.
- Full prompts or system prompts.
- Full external provider response bodies.
- Raw image binary data.

If a message is useful but may be long, truncate it to a bounded length as the current code does with provider and exception strings.

---

## Sensitive Data Rule

`docs/specs/Spec-006-API密钥管理(绝对不做).md` applies to logs too. A secret printed to terminal is still a secret exposure.

When adding a new provider or external integration, log provider name and status, not request headers or credentials.

---

## Future Migration

If the project adopts structured logging later, preserve these semantic fields:

- `task_id`
- `node_id`
- `event_type`
- `provider`
- `status`
- `folder`
- `filename`

Do not do a logging framework migration as part of unrelated feature work.
