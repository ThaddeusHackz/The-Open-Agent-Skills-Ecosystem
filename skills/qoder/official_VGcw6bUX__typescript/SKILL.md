---
name: typescript
description: "TypeScript rules for .ts/.tsx/.mts/.cts: typed boundaries, Bun, import extensions, file headers."
---

* Use [references/EXAMPLE.md](references/EXAMPLE.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

# 1. Overview

* Use this rule for TypeScript-specific work in `.ts`, `.tsx`, `.mts`, and `.cts` files. Preserve typed boundaries, runtime assumptions, import extension style, and file header shape.

---

# 2. Use This Rule When

* editing TypeScript source files
* changing props, request shapes, returned data, or state transitions
* adding or tightening public types

---

# 3. Core Rules

* Preserve typed boundaries.
* Prefer concrete types or `unknown`; do not use `any` casually.
* Type public functions, props, request objects, response objects, and returned values.
* Validate data where it enters or leaves the current unit.
* Normalize reused scalar values once near the top of the block and use the normalized value throughout.

---

# 4. Function Cohesion

**Strong rule:** do not split functions, methods, classes, or code blocks into overly fine-grained pieces. Keep
related statements together as one cohesive chunk unless extraction has a current, concrete reason.

Extract a function only when one of the following is true:

* real duplication exists across multiple call sites
* the current block is so large that a named extraction genuinely aids comprehension
* extraction isolates a real boundary or typed contract

Otherwise, keep the logic inline. A single well-named function with many readable lines is better than many tiny helpers connected only by call chains.

---

# 5. Runtime Execution

* Run TypeScript with `bun`, never `node`, unless the user overrides this for a specific task.
* Use `bun <script>`, `bun -e`, `bun repl`, `bunx`, or `bun x` instead of `node`, `node -e`, or `npx`.
* Use `Bun.file()` and `Bun.write()` for local file content processing only when `fs-mcp` cannot reasonably achieve the goal; never use PowerShell built-ins such as `Get-Content`, `Set-Content`, `Add-Content`, `Out-File`, or redirection operators for that fallback.
* Run `.ts`, `.tsx`, `.mts`, and `.cts` directly with `bun` when possible.

---

# 6. Import and Module Shape

* Preserve explicit import extensions such as `.mts` when the repository already uses them.
* Do not switch ESM and CommonJS styles unless the target runtime boundary requires it.
* Keep exports consistent with the edited file's existing pattern.
* Do not introduce package-manager, bundler, or tsconfig changes for a local type fix unless required.

---

# 7. Validation Focus

* input and output shapes
* caller and consumer assumptions
* async error paths
* type narrowing at external boundaries
* runtime compatibility with Bun

---

# 8. Formatting

* Follow the JavaScript skill for comment and formatting rules unless TypeScript syntax requires otherwise.
* Match repository header fields: `@file`, concise `@description`, `@author`, and `@since`.
* Keep exactly one blank line after a file header block before imports or executable code.
* Use compact standard style with no vertical alignment.
* Keep object keys double-quoted when the surrounding file uses that JSON-like convention.
* Define regex constants at the top of the smallest function, method, or class scope that uses them. Do not hoist regex constants to module scope only to satisfy a linter.
* Use Stroustrup clause layout for `else`, `catch`, and `finally`; never write same-line `} else {`, `} catch {`, or `} finally {`.
* **Always use `{ }` braces for `if`, `else`, `for`, `while`, and `do...while` bodies** — even when the body is a single statement. Never write braceless single-line forms.
* Prefer the Early Return (guard clause) pattern: validate and return/throw at the top, keep the happy path flat at the end. See `references/EXAMPLE.md` → Early Return.

---

# 9. Boundaries

* Do not silence type errors with `as any`, `// @ts-ignore`, or broad assertions.
* Do not rewrite stable JavaScript logic only to satisfy stylistic type preferences.
* Do not claim type safety when the real boundary still accepts unchecked data.
* Do not claim validation that was not run.
