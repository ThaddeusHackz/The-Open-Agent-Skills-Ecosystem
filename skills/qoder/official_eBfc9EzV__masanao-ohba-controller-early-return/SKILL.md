---
name: controller-early-return
description: Invoke when code-developer implements or refactors CakePHP controller actions with deep nesting. Detects nested if/else structures and provides refactoring patterns using early returns and viewBuilder() API to flatten control flow.
---

# Controller Early Return

Detect structural patterns in CakePHP Controllers that prevent early returns, and flatten control flow using the `viewBuilder()` API.

## Goal

Linearize deeply nested Controller actions with guard clauses and early returns to improve readability and maintainability.

## When to Apply

- Implementing new Controller actions
- Refactoring existing Controller actions
- Code review detects deeply nested actions

## Core Problem

When `$this->render()` and `$this->set()` are fixed at the method end, all code paths must reach that point, making early returns impossible.

## Solution: 3-Step Transformation

### Step 1: `render()` → `viewBuilder()->setTemplate()`

`render()` executes rendering immediately, forcing it to the method end. `viewBuilder()->setTemplate()` only declares the template name — CakePHP performs the actual rendering automatically after the action returns. When `redirect()` is returned, the template setting is silently ignored.

### Step 2: Move static `set()` calls to the top

View variables that don't depend on request data should be set before any conditional logic.

### Step 3: Guard clauses for early return

Handle precondition failures with guard clauses to reduce nesting of the happy path.

**Early return decision criteria:**

| Path | Needs View? | Strategy |
|------|------------|----------|
| Precondition failure (missing ID, etc.) | No (redirect) | Early return |
| POST save success | No (redirect) | Early return |
| GET (initial form display) | Yes | Fall-through |
| POST validation error | Yes | Fall-through |
| POST save failure | Yes | Fall-through |

### Transformed Structure

```php
public function edit(): ?\Cake\Http\Response
{
    // Step 1 & 2: Static view setup and template declaration at top
    $this->set('cancel_url', '/some/path');
    $this->viewBuilder()->setTemplate('/Path/To/template');

    // Step 3: Guard clauses — redirect paths return early
    if (!isset($params['id'])) {
        return $this->redirect(['action' => 'index']);
    }

    $entity = $Table->find()->where([...])->first();
    if (empty($entity)) {
        return $this->redirect(['action' => 'index']);
    }

    // POST handling: save success is also redirect → early return
    if (!empty($this->request->getData())) {
        // ... patch, validate, save ...
        if ($saved) {
            return $this->redirect(['action' => 'index']);
        }
        // Validation error / save failure → fall-through
    }

    // All view-rendering paths reach here → dynamic set() in one place
    $this->set(compact('entity'));
    return null;
}
```

## Applicability

| Condition | Apply? |
|-----------|--------|
| `$this->render()` at method end blocks early returns | Yes |
| Nesting 3+ levels deep | Yes |
| No `render()` call, relying on CakePHP auto-rendering | No |
| `autoRender = false` with JSON/file responses only | No |

## Notes

- Dynamic `set()` calls (e.g. `compact('entity')`) should appear once at the method end; all view-rendering paths share this exit point via fall-through
- Always verify existing tests pass after transformation
