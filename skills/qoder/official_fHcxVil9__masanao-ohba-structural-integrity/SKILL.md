---
name: structural-integrity
description: Invoke when code-developer, quality-reviewer, or design-architect works on React/TypeScript code. Enforces structural integrity principles — single source of truth, minimal branching, responsibility separation, and derived state patterns. Use as a review checklist and implementation guide for all code changes.
---

# Structural Integrity Standards

## Core Philosophy

Every conditional branch, loop, and exception handler must justify its existence by mapping to a specific functional requirement. Over-abstraction that obscures business logic is as harmful as duplication.

---

## 1. Single Source of Truth

### Types

- Define each type/interface in **one canonical file** — all consumers import from that file
- Use `Pick<T, K>` or `Omit<T, K>` to create partial views instead of declaring local re-definitions
- Never create `FooLike` or local interface copies of an existing type

```typescript
// BAD: local re-declaration
interface NewMessageManagerLike {
  getUnreadCount(group: Message[]): number;
}

// GOOD: derive from canonical type
import { NewMessageManager } from '@/lib/types/newMessageManager';
type Props = { manager: Pick<NewMessageManager, 'getUnreadCount'> };
```

### Constants

- All behavioral values (thresholds, delays, margins, sizes) must be **named constants** in a centralized constants file
- Each constant includes a specification comment explaining what it controls
- No magic numbers in component or hook files

```typescript
// BAD
{ rootMargin: '200px' }
setTimeout(fn, 750);

// GOOD
import { VIEWPORT_PRERENDER_MARGIN_PX, NOTIFICATION_AUTOREAD_FADE_MS } from '@/lib/constants/ui';
{ rootMargin: `${VIEWPORT_PRERENDER_MARGIN_PX}px` }
setTimeout(fn, NOTIFICATION_AUTOREAD_FADE_MS);
```

### Shared Logic

- When two or more files compute the same value, extract to a shared utility
- Utilities must be pure functions — no side effects, no store access
- Place in `lib/utils/` with a descriptive filename matching the function's domain

---

## 2. Minimal Branching and Loops

### Conditional Branches

- Every `if`, ternary, or `switch` must map to a **distinct functional requirement**
- Reduce branching by using data-driven approaches (maps, lookups, array methods)
- Avoid nested conditionals — use early returns or guard clauses
- Ternaries count as conditionals — don't chain or nest them

### Loops

- Avoid redundant iterations — combine related operations into a single pass
- Use `Set.has()` (O(1)) instead of `Array.indexOf()` / `Array.find()` (O(n)) for membership checks
- When iterating collections, prefer declarative methods (`map`, `filter`, `reduce`) over imperative `for` loops

### Exception Handlers

- Every `catch` block must either **log the error** or **propagate it** — never silently swallow
- After handling a cancellation/expected error, `return` immediately — don't fall through to error rendering
- Match catch scope to the operation: don't wrap unrelated code in the same try block

---

## 3. Responsibility Separation

### Component Responsibilities

- **Presentational components** receive all data and actions via props — no direct store access
- **Container components / hooks** own data fetching and state management
- A component that grows beyond ~200 lines likely has multiple responsibilities — extract hooks or sub-components

```typescript
// BAD: Presentational component accessing store directly
function NotificationItem({ notification }) {
  const { markAsRead } = useNotificationStore(); // ← store leak
  ...
}

// GOOD: Actions passed as props
function NotificationItem({ notification, onMarkAsRead, onDelete }) {
  ...
}
```

### Hook Responsibilities

- Each custom hook has **one job** — don't combine pagination logic with project tab computation
- Return a minimal, typed interface — not the entire internal state
- When a hook's return value is consumed by React, use `useState` (not refs + forceUpdate) so React's render cycle detects changes naturally

### File Responsibilities

- Each file exports one primary concern
- Co-locate types with their primary consumer unless shared by 3+ files (then promote to `lib/types/`)
- Co-locate constants with their domain unless shared across domains (then promote to `lib/constants/`)

---

## 4. Derived State

### Selector Pattern

- State that can be computed from other state must be a **selector**, not a manually maintained field
- When store state changes, derived values update automatically through selectors — no manual synchronization across mutation paths

```typescript
// BAD: Manual maintenance in N mutation paths
markAsRead(id) {
  set({ notifications: updated, unreadCount: updated.filter(n => !n.read).length });
}
markAllAsRead() {
  set({ notifications: updated, unreadCount: 0 });
}

// GOOD: Single selector, zero maintenance
export const selectUnreadCount = (state) =>
  state.notifications.filter((n) => !n.read).length;
```

### Version Counter for Ref-Based Hooks

- When a hook stores mutable data in refs (for performance), use a `useState` version counter to trigger React re-renders
- Increment the counter after each mutation
- Never use `forceUpdate({})` — it breaks React's mental model and is invisible to parent components

---

## 5. CSS vs JavaScript

- Visual concerns (transitions, opacity, colors, scrollbar styling) belong in CSS — not `classList.add()` or inline style manipulation
- Use CSS classes toggled by React state, not direct DOM manipulation
- Consolidate related styles in a single CSS file — avoid duplicate inline `<style>` blocks

```typescript
// BAD: DOM manipulation for visual effect
el.classList.add('auto-reading');

// GOOD: React state drives CSS class
<div className={cn('notification-item', isAutoReading && 'auto-reading')} />
```

---

## 6. Resource Management

### Singletons for Shared Resources

- Browser APIs that are expensive to instantiate (Worker, IntersectionObserver) should be **module-level singletons** with a fixed upper bound
- Use `WeakMap<Element, callback>` for callback routing to allow element GC
- Never create per-component instances of expensive resources

### Cleanup

- Every `observe()` must have a corresponding `unobserve()` or `disconnect()` in cleanup
- Every `setTimeout` / `setInterval` must be cleared in the effect cleanup
- Ref Maps that track DOM elements must evict stale entries when the data source shrinks

### Promise Lifecycle

- `cancel()` must reject the promise — deleting a pending entry without rejection leaks the promise and its closures
- Track which resource owns which pending request to avoid cascading failures

---

## Anti-Patterns Summary

| Anti-Pattern | Fix |
|---|---|
| Local type re-declarations | Import from canonical source, use `Pick<>` |
| Magic numbers | Named constants with spec comments |
| Store access in presentational components | Pass actions as props |
| Manual derived state across N paths | Selector function |
| `forceUpdate({})` / `useReducer` hack | Version counter `useState` |
| `classList.add()` for visual effects | CSS class via React state |
| Per-component Worker/Observer | Module-level singleton pool |
| Silent catch blocks | Log or propagate, then return |
| Nested ternaries / chained conditionals | Early returns, guard clauses, data-driven |
| Over-abstraction hiding business logic | Direct implementation with clear responsibility |
