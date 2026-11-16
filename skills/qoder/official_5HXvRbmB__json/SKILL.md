---
name: json
description: "JSON rules: double-quoted keys, no trailing commas, no comments, 2-space indent, validate against schema."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Scope

Use this rule when:

* editing `.json` files: `package.json`, `tsconfig.json`, API schemas, config files
* reviewing JSON payloads sent to or received from APIs
* generating or transforming JSON programmatically

JSON has no comments and strict syntax — every character is load-bearing.

---

# Core Rules

* Keys must be double-quoted strings; never unquoted or single-quoted.
* **No trailing commas** on the last element of an object or array.
* **No comments.** Use `.jsonc` if the target tool supports it; otherwise document intent elsewhere.
* Keep key order stable within objects; do not reorder without reason.
* Use `null` explicitly for absent values; do not omit keys that are part of a defined schema.
* Validate structure against the applicable schema (JSON Schema, OpenAPI, tsconfig schema) after edits.
* Minify only for transport or output artifacts; keep source files pretty-printed.

---

# Formatting

* **Never use vertical alignment.** Do not pad spaces to align values across keys.
* 2-space indentation.
* One space after colon: `"key": value`. No extra padding.
* Arrays of simple scalars may be single-line if they fit within 80 characters.
* Objects with more than two keys use one key-value pair per line.

---

# Validation Focus

* trailing commas
* type mismatches (string where number expected, etc.)
* missing required keys after edits
* schema or contract drift between producer and consumer
