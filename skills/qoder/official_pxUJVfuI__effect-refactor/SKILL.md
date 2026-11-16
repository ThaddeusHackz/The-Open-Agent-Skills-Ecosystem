---
name: effect-refactor
description: Refactor React useEffect code when reviewing or fixing unnecessary Effects, derived state in Effects, event logic inside Effects, prop-to-state syncing, parent-child synchronization, or brittle Effect dependency chains. Use for requests like "clean up this useEffect", "remove unnecessary effects", "refactor effect logic", or "is this Effect needed?"
---

# effect-refactor

Refactor `useEffect` with the React guidance from **You Might Not Need an Effect**.

## Goal

Prefer render-time derivation, event handlers, keys, lifted state, `useMemo`, or `useSyncExternalStore` when they model the behavior more directly than an Effect.

Use Effects only when synchronizing with an **external system**, such as:
- network requests
- browser/DOM APIs
- timers
- subscriptions
- third-party widgets
- storage or other non-React mutable sources

## Refactor checklist

For each `useEffect`, identify **why** it runs:

1. **Derived value?**
   - If it computes something from props/state, calculate it during render.
   - Remove redundant state like `fullName`, `filteredItems`, `footer`, `isValid`, etc.

2. **Expensive pure calculation?**
   - Use `useMemo` instead of state + Effect.
   - Only keep `useMemo` when the calculation is measurably expensive.

3. **User interaction?**
   - If the logic should happen because the user clicked, submitted, dragged, or typed, move it into the event handler.
   - Typical examples: POST requests, toasts, analytics for a button click, navigation, parent callbacks.

4. **Resetting state on prop change?**
   - Reset the whole subtree with a `key` when appropriate.
   - If only one piece of state needs adjustment, prefer deriving from props/state or storing an ID instead of a full object.

5. **Keeping parent and child in sync?**
   - Prefer lifting state up or calling parent callbacks directly in the same event.
   - Avoid child `useEffect(() => onChange(...))` patterns unless there is a real external synchronization need.

6. **External subscription?**
   - Prefer `useSyncExternalStore` over manual subscription Effects when subscribing to external mutable stores.

7. **Data fetching?**
   - Effects are valid for fetch synchronization when the request should follow visible state/props.
   - Add cleanup to avoid race conditions.
   - If the app/framework offers server data loading or a dedicated cache layer, prefer that.

8. **Effect chain?**
   - Collapse chains of Effects into a single event-driven state transition or render-time derivation.

## Common rewrites

### 1) Derived state in an Effect → calculate during render

```tsx
const [fullName, setFullName] = useState("");
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);
```

Rewrite to:

```tsx
const fullName = `${firstName} ${lastName}`;
```

### 2) Filter/map/sort in an Effect → render or `useMemo`

```tsx
const [visibleTodos, setVisibleTodos] = useState([]);
useEffect(() => {
  setVisibleTodos(getFilteredTodos(todos, filter));
}, [todos, filter]);
```

Rewrite to:

```tsx
const visibleTodos = getFilteredTodos(todos, filter);
```

Or if expensive:

```tsx
const visibleTodos = useMemo(() => getFilteredTodos(todos, filter), [todos, filter]);
```

### 3) Event-specific logic in an Effect → move to handler

```tsx
useEffect(() => {
  if (product.isInCart) {
    showNotification(`Added ${product.name}`);
  }
}, [product]);
```

Rewrite by calling shared logic from the event handler that caused the change.

### 4) Reset on prop change in an Effect → `key`

```tsx
useEffect(() => {
  setComment("");
}, [userId]);
```

Rewrite to a keyed inner component:

```tsx
return <Profile key={userId} userId={userId} />;
```

### 5) Child notifying parent in Effect → same-event update

```tsx
useEffect(() => {
  onChange(isOn);
}, [isOn, onChange]);
```

Rewrite to:

```tsx
function updateToggle(nextIsOn: boolean) {
  setIsOn(nextIsOn);
  onChange(nextIsOn);
}
```

### 6) External store subscription → `useSyncExternalStore`

```tsx
const isOnline = useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
```

### 7) Fetching in an Effect → keep, but add cleanup

```tsx
useEffect(() => {
  let ignore = false;

  fetchResults(query, page).then((json) => {
    if (!ignore) setResults(json);
  });

  return () => {
    ignore = true;
  };
}, [query, page]);
```

## Review heuristics

When refactoring, prefer these outcomes:
- fewer state variables
- fewer Effects
- fewer dependency-array fights
- data flow that is obvious from props + state
- event logic staying inside the event that caused it
- no stale render followed by immediate corrective render

## Output expectations

When using this skill on a code change:
- identify each Effect as **keep**, **rewrite**, or **delete**
- explain the reason in one line
- choose the smallest safe refactor
- preserve behavior unless the current behavior is clearly buggy
- mention any remaining valid Effects and what external system they synchronize with

## Good trigger prompts

- `/skill:effect-refactor`
- `Refactor this useEffect`
- `Do I need this Effect?`
- `Remove unnecessary effects from this component`
- `Clean up prop-to-state syncing here`
- `Replace this effect chain with something simpler`
