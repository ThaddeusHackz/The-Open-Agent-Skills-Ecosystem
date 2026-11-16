---
name: pwsh
description: "PowerShell rules: paths as data, Join-Path over concatenation, avoid Invoke-Expression, check LASTEXITCODE."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Scope

Use this rule when:

* editing `.ps1` scripts
* composing native command calls from PowerShell
* handling filesystem paths, arguments, and exit codes
* structuring numbered script sections (setup, global state, run-flow blocks)

Treat paths and native command arguments as structured data, not interpolated shell text.

---

# Core Rules

* **Do not use PowerShell built-in file content commands** such as `Get-Content`, `Set-Content`, `Add-Content`, `Out-File`, or redirection operators for local file processing. Use `fs-mcp` first; use `bun`, `bun -e`, `bun repl`, `Bun.file()`, and `Bun.write()` only when `fs-mcp` cannot reasonably achieve the goal.
* **Never use C-style index-based `for` loops.** Use `ForEach-Object`, the `foreach` statement over a collection, or pipeline iteration.
* Treat paths as data — prefer `Join-Path`, `Split-Path`, and explicit path helpers over manual string concatenation.
* Distinguish PowerShell parsing from native command execution.
* Prefer direct invocation with `&` and separated arguments over a single large command string.
* **Never use `Invoke-Expression`.**
* Check `$LASTEXITCODE` after native commands when relevant.
* Fail clearly on missing files, invalid paths, invalid arguments, or missing tools.

---

# Script Structure

When a script uses numbered top-level sections separated by ruler lines:

* Wrap grouped script-level statements inside `& { ... }` blocks.
* Do not leave loose assignments or calls at the top level when the surrounding sections are wrapped.
* Use `$global:` variables for state shared across numbered setup sections and between class methods.
* Do not leave shared state in bare variables when the surrounding script already uses `$global:`-based initialization blocks.

---

# Function Cohesion

**Strong rule:** do not split scripts, functions, methods, or code blocks into overly fine-grained pieces. Keep
related statements together as one cohesive chunk unless extraction has a current, concrete reason.

Extract a function only when one of the following is true:

* real duplication exists across multiple call sites
* the current block is so large that a named extraction genuinely aids comprehension
* extraction isolates a real boundary or responsibility

Otherwise, keep the logic inline. A single well-named function with many readable lines is better than many tiny helpers connected only by call chains.

---

# Performance

* For local file content reads, writes, and transforms, use `fs-mcp` first.
* Use `Bun.file(path).text()`, `Bun.file(path).bytes()`, `Bun.write(path, content)`, `bun -e`, or `bun repl` only when `fs-mcp` is unavailable, insufficient, or materially less reliable for the goal.
* Use PowerShell only to launch `bun` or native tools and to pass paths and arguments as structured data.
* If `bun` is unavailable or incompatible, state the fallback reason before using another runtime or API.

---

# Formatting

* **Never use vertical alignment.** Do not pad spaces to align assignments, parameter declarations, or hash table entries into columns.
* Use exactly one space on both sides of binary operators (`=`, `-eq`, `-ne`, `-gt`, `-ge`, `-lt`, `-le`, `+`, `-`, `*`, `/`, `%`, `-and`, `-or`, etc.).
* Do not pad spaces to line up `=` or any operator across adjacent lines.
* **Use Stroustrup clause layout** for `else`, `elseif`, `catch`, and `finally` — they always start on a new line after the closing brace. Never write `} else {`, `} elseif (...) {`, `} catch {`, or `} finally {`.
* When section headers use a paired ruler block, the section body should start with `& {` on the line immediately after the bottom ruler.
* **Always use `{ }` braces for `if`, `else`, `elseif`, `foreach`, `for`, and `while` bodies** — even when the body is a single statement. Never write braceless single-line forms.
* Prefer the Early Return (guard clause) pattern: validate and return at the top, keep the happy path flat at the end. See `references/EXAMPLE.md` → Early Return.
* Compact, standard style — no unnecessary whitespace padding.

---

# Validation Focus

* parser validity
* path handling correctness
* native command argument boundaries
* exit-code handling
* script-level section block integrity (`& { ... }` wrapping, shared `$global:` state visibility)
