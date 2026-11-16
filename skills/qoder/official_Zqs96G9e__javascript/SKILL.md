---
name: javascript
description: "JavaScript/TypeScript rules: const/let only, template literals mandatory, vanilla JS over jQuery."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Scope

Use this rule when:

* editing JavaScript or TypeScript files
* changing props, request shapes, returned data, or state transitions
* touching frontend or Node runtime logic

Preserve typed boundaries, state-flow clarity, and the local repository's component and module shape.

---

# Core Rules

* Preserve typed boundaries. Prefer concrete types or `unknown`; do not use `any` casually.
* Keep state, rendering, business rules, and data shaping from collapsing together without need.
* Check props, request/response shapes, returned data, and state transitions before editing.
* Validate with the smallest sufficient lint, type, or test surface.
* Validate at the real boundary where data enters or leaves the current unit.
* Normalize reused scalar values once near the top of the block and use the normalized value throughout.

---

# Runtime Execution

* Run JS/TS with `bun`, never `node`, unless the user overrides this for a specific task.
* Use `bun <script>`, `bun -e`, `bun repl`, `bunx`, or `bun x` instead of `node`, `node -e`, or `npx`.
* Use `Bun.file()` and `Bun.write()` for local file content processing only when `fs-mcp` cannot reasonably achieve the goal; never use PowerShell built-ins such as `Get-Content`, `Set-Content`, `Add-Content`, `Out-File`, or redirection operators for that fallback.
* Run `.ts`, `.tsx`, `.mts`, and `.cts` directly with `bun` when possible.

---

# Function Cohesion

**Strong rule:** do not split functions, methods, classes, or code blocks into overly fine-grained pieces. Keep
related statements together as one cohesive chunk unless extraction has a current, concrete reason.

Extract a function only when one of the following is true:

* real duplication exists across multiple call sites
* the current block is so large that a named extraction genuinely aids comprehension
* extraction isolates a real boundary or contract

Otherwise, keep the logic inline. A single well-named function with many readable lines is better than many tiny helpers connected only by call chains.

---

# Syntax Rules

* **Never use `var`.** Use `const` by default; use `let` only when reassignment is necessary.
* Declare variables at the narrowest possible scope.
* Use template literals for all string interpolation; never concatenate with `+` when a variable or expression is involved.
* Prefer `Object.assign(target, { key: value })` when applying changes to an existing object and mutation is intentional. For immutable copies, use object spread instead of an empty-object `Object.assign` target.
* Prefer optional chaining (`?.`) for nullable nested property or method access.
* **Never use index-based `for` loops.** Prefer `forEach`, `map`, `filter`, `reduce`, `for...of`, or `for...in`.
* Prefer arrow functions for callbacks.
* Define regex constants at the top of the smallest function, method, or class scope that uses them. Do not hoist regex constants to module scope only to satisfy a linter.
* Object keys must be double-quoted.
* Extract variables before IIFEs; minimize IIFE usage.
* Prefer vanilla JS over jQuery. Use jQuery only when the project already depends on it and removal is out of scope.

---

# Comments

* Follow the `comments` skill for section divider comments.
* For standalone scripts, wrappers, and runtime entry files, add a JSDoc file header at the top unless the local file class already uses a different established pattern.
* Match the repository header fields: `@file`, concise `@description`, `@author`, `@since`.
* Add brief Korean comments above non-obvious logical blocks.
* Use concise noun-like or clipped statement-like endings.
* Do not narrate obvious syntax.
* Keep section numbering to two levels.
* Do not number every simple constant or variable.

---

# Formatting

* Follow the Google JavaScript Style Guide: https://google.github.io/styleguide/jsguide.html
* Keep exactly one blank line after a file header block before imports or executable code.
* **Never use vertical alignment.**
* Use exactly one space around binary operators.
* Do not pad spaces to line up `=` or any operator across adjacent lines.
* **Use Stroustrup clause layout** for `else`, `catch`, and `finally` — they always start on a new line after the closing brace. Never write `} else {`, `} catch {`, or `} finally {`.
* **Always use `{ }` braces for `if`, `else`, `for`, `while`, and `do...while` bodies** — even when the body is a single statement. Never write braceless single-line forms.
* Prefer the Early Return (guard clause) pattern: validate and return/throw at the top, keep the happy path flat at the end. See `references/EXAMPLE.md` → Early Return.
* Compact, standard style — no unnecessary whitespace padding.

---

# Validation Focus

* input and output shapes
* state transitions
* async error paths
* caller and consumer assumptions
* boundary uncertainty vs. stable in-app invariants
* one guard at the contract edge, then direct use inside the normalized flow
