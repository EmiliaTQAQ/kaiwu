# Frontend Quality Guidelines

> Code quality standards for the React frontend.

---

## Required Patterns

### Use Task Runtime APIs

New AI conversation work must use `/api/tasks` through `src/api/tasks.ts`. Do not reintroduce direct `/api/chat` calls from old backup code.

### Preserve Event Flow

When changing task-visible UI, keep the flow aligned:

```text
backend EventStore -> /api/tasks/{id}/events -> useSseEvents -> useAgentTask -> agentEventReducer / agentTaskController -> UI
```

### Keep App As Wiring

`App.tsx` currently owns many state variables, but new feature logic should move into hooks or typed feature components. Avoid making `App.tsx` or `MainStage.tsx` larger unless the change is simple wiring.

### Preserve Product Rules

The following behaviors are product constraints:

- Conversation rename remains available.
- Normal conversation controls differ from image-generation controls.
- AI-generated files are displayed through project library refreshes after `file_saved`.
- Generated image paths must survive conversation reload via markdown image parsing.
- Suggested questions are stored in the message content and restored by `useConversation()`.

---

## Forbidden Patterns

- Copying logic from `src/App.tsx.bak`.
- Adding new `/api/chat` usage.
- Saving task conversations from the frontend during the same task that backend runtime saves.
- Re-parsing SSE frames outside `useSseEvents()`.
- Mutating `messages` arrays directly.
- Adding large new screens inline inside `MainStage.tsx`.
- Disabling conversation rename or upload/history controls as a shortcut.
- Breaking IME composition handling for Enter-to-send.

---

## Verification

Run the production build for frontend changes:

```powershell
Set-Location kaiwu
npm run build
```

For task/SSE changes, also run:

```powershell
python -m compileall kaiwuback/server
```

Manual smoke checks for UI changes:

- Send a normal conversation task and confirm `done` ends loading.
- Stop generation and confirm UI exits loading.
- Load a historical conversation with images and confirm images render.
- Trigger `file_saved` and confirm project files/images refresh.
- Rename a history item from the sidebar menu.
- Switch away and back during an active task to confirm cache restore.

---

## Review Checklist

Before finishing a frontend change:

- Does it align with `docs/specs/Spec-002-SSE事件协议.md` and `docs/specs/Spec-007-Task-Agent-Runtime.md`?
- Are new API calls centralized in `src/api/` or hooks?
- Are new event types handled in the status map, reducer, and controller as needed?
- Are props typed without introducing new broad `any`?
- Are icon buttons labelled with `title` or `aria-label`?
- Are state owner refs kept synchronized?
- Does `npm run build` pass?
