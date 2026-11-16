---
name: java
description: "Java rules: explicit contracts, null safety with Optional, no speculative methods, Java 11 baseline."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Constraints

* **Java 11 baseline.** Do NOT use features introduced after Java 11: records, sealed classes, pattern matching for `instanceof`, text blocks, switch expressions (`->`), `var` in lambda parameters.
* **NEVER use `var`.** Always declare the explicit type for every local variable.

---

# Scope

Use this rule when:

* editing Java services, controllers, repositories, DTOs, or mappers
* changing method signatures or returned shapes
* tracing caller impact across Java layers

---

# Layering Boundary

* Business logic and utility processing belong in **Java**.
* SQL/XML are for data retrieval and persistence only.
* Format conversion, string manipulation, conditional branching, calculation, and code mapping must be implemented in Java — not in queries.
* SQL functions (`CASE WHEN`, `IF()`, `IFNULL()`, `CONCAT()`, `DATE_FORMAT()`, `NOW()`, `LEFT()`, `RIGHT()`) are allowed only for simple display-level transformations, never for business rules.

---

# Core Rules

* Treat method signatures, DTO fields, and mapper parameters as contract surfaces; verify caller impact before changing them.
* Prefer explicit, readable branches over clever compression.
* Do not introduce speculative helpers, wrappers, or utility classes.
* Do not create new methods unless explicitly requested — inline within an existing method first.
* Trust internal code paths. Guard against null only at system boundaries (user input, external API responses, DB results). Avoid blanket NPE-defense null checks.

---

# Method Extraction and Code Cohesion

**Strong rule:** do not split methods, functions, classes, or code blocks into overly fine-grained pieces. Keep
related statements together as one cohesive chunk unless extraction has a current, concrete reason.

Extract to a private method **only** when one of the following is true:

* real duplication exists
* the current method is so long that a named extraction genuinely aids comprehension
* extraction protects a real boundary or contract

Otherwise, keep the logic inline. A single well-named method with forty readable lines is better than five eight-line helpers connected only by call chains.

---

# Null Safety

* **Never return `null`.** Return `Optional<T>` or `Collections.emptyList()`.
* Use `Objects.requireNonNull()` for required parameters.
* **Never use `String.valueOf(obj)`.** Use `Objects.toString(obj, "")` so the null fallback is explicit and `"null"` strings cannot leak into output.

---

# Resource Management

* ALWAYS use try-with-resources for `AutoCloseable`.

---

# Immutability

* Do **not** add `final` to fields or local variables as a default habit.
* Return defensive copies of mutable state.

---

# Exception Handling

* Catch SPECIFIC exceptions; never `Exception` or `Throwable`.
* Never leave a catch block empty — log or rethrow with context.

---

# Collections & Control Flow

* Declare by interface: `List<T>`, not `ArrayList<T>`.
* **Prefer basic syntax over Stream or Collection APIs.** Unless the user explicitly requests it, use traditional `for` loops and `if` statements instead of `stream()`, `map`, `filter`, `collect`, `forEach`, or other functional-style APIs.
* Use `StringBuilder` inside loops
* Use `String.format()` for complex concatenation.

---

# Formatting

* Follow the Google Java Style Guide: https://google.github.io/styleguide/javaguide.html
* **Never vertically align** declarations, fields, annotations, or assignments into columns.
* Use exactly one space on both sides of every binary operator (`=`, `==`, `!=`, `>`, `>=`, `<`, `<=`, `+`, `-`, `*`, `/`, `%`, `&&`, `||`, etc.).
* Do not pad spaces to line up `=` or any operator across adjacent lines.
* Do not use tabs, repeated spaces, or column alignment for visual formatting.
* **Use Stroustrup clause layout** for `else`, `catch`, and `finally` — they always start on a new line after the closing brace. Never write `} else {`, `} catch {`, or `} finally {`.
* **Always use `{ }` braces for `if`, `else`, `for`, `while`, and `do-while` bodies** — even when the body is a single statement. Never write braceless single-line forms.
* Prefer the Early Return (guard clause) pattern: validate and return/throw at the top, keep the happy path flat at the end without extra nesting. See `references/EXAMPLE.md` → Early Return.
* Compact, standard style. No unnecessary whitespace padding.

---

# Validation Focus

* changed method contracts
* DTO field shape and nullability expectations
* mapper interface and XML alignment
* controller or service callers affected by the change

---

# Build

* **Do NOT run Gradle compile or test commands** (`./gradlew compileJava`, `./gradlew test`, etc.). Validation is limited to code-level review only.
