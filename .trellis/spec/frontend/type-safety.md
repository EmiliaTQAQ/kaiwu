# Frontend Type Safety

> TypeScript conventions for `kaiwu/src/`.

---

## Compiler Settings

The frontend uses strict TypeScript:

- `strict: true`
- `allowJs: false`
- `isolatedModules: true`
- `jsx: react-jsx`
- `moduleResolution: Bundler`

Reference: `kaiwu/tsconfig.json`

New frontend code must compile under `npm run build`.

---

## Type Organization

Use the current ownership pattern:

- Shared UI/domain unions: `src/types.ts`
- API task contracts: `src/api/tasks.ts`
- Component-specific props and local helper types: near the component file
- Hook-specific option/result types: near the hook file

`types.ts` derives several unions from `data.ts`:

- `Direction`
- `SettingsSection`
- `SkillCategory`

Follow that pattern when a union is backed by a static config list.

---

## API Types

Task API types live in `src/api/tasks.ts`:

- `AgentTaskStatus`
- `AgentTask`
- `AgentTaskDebug`
- `CreateTaskPayload`
- `CreateTaskResponse`
- `AgentTaskEvent`

When backend task payloads or event fields change, update these types and the relevant reducer/controller together.

`AgentTaskEvent` intentionally has an index signature because backend event payloads differ by event type. Narrow by `event.type` before reading event-specific fields.

---

## Runtime Validation

The project currently does not use Zod/Yup/io-ts. Runtime validation is lightweight and local:

- `apiJson<T>()` throws on non-OK HTTP status.
- `getErrorMessage()` normalizes unknown caught errors.
- `parseConversationMessages()` guards JSON parsing for embedded suggestions.
- `useSseEvents()` ignores malformed SSE JSON frames.

If adding complex external data, add local guards or introduce a validation library only as a scoped architecture decision.

---

## Avoiding `any`

Avoid new `any` types. Existing debt:

- `MainStageProps = Record<string, any>`
- `AgentTaskEvent` index signature
- `import.meta as any` in `api/client.ts`

Do not spread this pattern into new components. Prefer explicit prop types like `ConversationPanelProps` and `AppSidebarProps`.

---

## Common Patterns

- Use `Dispatch<SetStateAction<T>>` for setter props.
- Use `RefObject<T | null>` for DOM refs passed to components/hooks.
- Use small local `MutableRef<T>` aliases for plain mutable refs passed into hooks.
- Use string literal unions for view modes and task statuses.
- Use `unknown` in catch handlers and normalize before rendering.

---

## Common Mistakes

- Adding API response fields in backend without updating `api/tasks.ts`.
- Reading `event.foo` in controller code without checking `event.type`.
- Adding `any` to silence prop drilling errors instead of extracting a typed component.
- Defining a union type manually when it should derive from `data.ts`.
