# Frontend Development Guidelines

> Project-specific frontend rules for `kaiwu/`.

---

## Overview

Kaiwu's frontend is a Vite + React + TypeScript app under `kaiwu/`. The current UI is a single-page desktop workspace for OPC entrepreneurs, with task-driven AI conversation, project library, skills, image/video/coding workspaces, and settings.

Current architecture:

- `src/App.tsx` owns top-level state and wires hooks/components.
- `src/api/` owns API helpers and task API types.
- `src/hooks/` owns task transport, event reduction, conversation orchestration, and conversation cache.
- `src/features/chat/` owns chat UI.
- `src/features/layout/` owns sidebar, main stage, and modals.
- `src/data.ts`, `src/types.ts`, and `src/utils.ts` hold static config, shared types, and markdown rendering.

---

## Guidelines Index

| Guide | Description | Status |
|-------|-------------|--------|
| [Directory Structure](./directory-structure.md) | Current Vite/React source layout and feature boundaries | Filled |
| [Component Guidelines](./component-guidelines.md) | Component, props, styling, icons, animation, and accessibility patterns | Filled |
| [Hook Guidelines](./hook-guidelines.md) | Custom hooks, task transport, SSE parsing, reducers, and fetch conventions | Filled |
| [State Management](./state-management.md) | App state ownership, refs, task cache, server state, and image mode rules | Filled |
| [Quality Guidelines](./quality-guidelines.md) | Required checks, forbidden patterns, and frontend review checklist | Filled |
| [Type Safety](./type-safety.md) | Strict TypeScript organization, API types, and runtime guard patterns | Filled |

---

## Pre-Development Checklist

Before changing frontend code:

1. Read [Directory Structure](./directory-structure.md).
2. Read the guide matching your work:
   - UI component: [Component Guidelines](./component-guidelines.md)
   - Hook/API/event flow: [Hook Guidelines](./hook-guidelines.md)
   - State or conversation behavior: [State Management](./state-management.md)
   - Types: [Type Safety](./type-safety.md)
   - Any frontend change: [Quality Guidelines](./quality-guidelines.md)
3. Read the frozen project specs that own the behavior:
   - SSE protocol: `docs/specs/Spec-002-SSE事件协议.md`
   - Task runtime: `docs/specs/Spec-007-Task-Agent-Runtime.md`
4. Ignore `src/App.tsx.bak` and `src/styles.css.bak` when learning current patterns.

---

## Verification

Use the existing build as the main frontend check:

```powershell
Set-Location kaiwu
npm run build
```

For backend-integrated UI changes, also compile the backend:

```powershell
python -m compileall kaiwuback/server
```
