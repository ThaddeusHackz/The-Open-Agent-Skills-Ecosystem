---
name: python
description: "Python rules: type hints, pathlib, f-strings, specific exceptions, dataclasses over plain dicts."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Scope

Use this rule when:

* editing Python source files (`.py`)
* changing function signatures, data models, or module boundaries
* writing scripts, services, or CLI tools in Python

Favor explicit, readable code with clear ownership of data flow and error handling.

---

# Core Rules

* **Never use index-based `for` loops** (`for i in range(len(lst))`). Use `for item in iterable`, comprehensions, `enumerate()`, `zip()`, or `map()`/`filter()`.
* Use type hints for all public function signatures.
* Prefer `pathlib.Path` over `os.path`.
* Use f-strings for interpolation; avoid `%` formatting and `str.format()`.
* **Never use mutable default arguments.** Use `None` and assign inside the function.
* Prefer `dataclass` or `TypedDict` over plain dicts for structured data.
* **Never use bare `except:`.** Catch specific exceptions.
* Use `with` statements for all resources implementing `__enter__` / `__exit__`.
* Group imports: stdlib → third-party → local, separated by blank lines.

---

# Function Cohesion

**Strong rule:** do not split functions, methods, classes, or code blocks into overly fine-grained pieces. Keep
related statements together as one cohesive chunk unless extraction has a current, concrete reason.

Extract a function only when one of the following is true:

* real duplication exists across multiple call sites
* the current block is so large that a named extraction genuinely aids comprehension
* extraction isolates a real boundary or typed contract

Otherwise, keep the logic inline. A single well-named function with many readable lines is better than many tiny helpers connected only by call chains.

---

# Null Safety

* Do not return `None` where a typed value is expected without documenting it.
* Prefer `Optional[T]` or `T | None` and check before use.

---

# Formatting

* Follow the Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
* Follow PEP 8; use Black or Ruff when available.
* Maximum line length: 88 characters (Black default).
* Class names: `PascalCase`. Functions and variables: `snake_case`. Constants: `UPPER_SNAKE_CASE`.
* **Never use vertical alignment.** Do not pad spaces to align assignments, dict entries, or imports into columns.
* Use exactly one space on both sides of binary operators (`=`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `+`, `-`, `*`, `/`, `%`, etc.).
* Do not pad spaces to line up `=` or any operator across adjacent lines.
* Compact, standard style — no unnecessary whitespace padding.
* **Always use the indented multi-line block form for `if`, `elif`, `else`, `for`, `while`, and `with` bodies.** Never write single-line colon-body forms such as `if x: return`.
* Prefer the Early Return (guard clause) pattern: validate and return/raise at the top, keep the main logic flat at the end. See `references/EXAMPLE.md` → Early Return.

(Python uses indentation rather than braces, so Stroustrup clause layout does not apply directly. Keep `elif`, `else`, `except`, and `finally` aligned with their leading keyword on a fresh line, as required by the language.)

---

# Validation Focus

* mutable default arguments
* missing type hints on public interfaces
* bare except clauses
* resource leaks (files, sockets, connections not closed)
