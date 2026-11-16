---
name: yaml
description: "YAML rules: 2-space indent, quote ambiguous strings, block style for multiline, no plain secrets."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Scope

Use this rule when:

* editing `.yml` or `.yaml` files
* changing CI/CD pipelines, Kubernetes manifests, Docker Compose, or application config
* reviewing configuration drift or schema changes

Treat structure, indentation, and quoting as part of the contract — not cosmetic detail.

---

# Core Rules

* Use 2-space indentation; **never mix tabs and spaces**.
* Quote strings containing special characters: `:`, `{`, `}`, `[`, `]`, `#`, `&`, `*`, `!`, `|`, `>`, `'`, `"`, `%`, `@`, `` ` ``.
* Quote strings that look like other types: `"true"`, `"123"`, `"null"`.
* Prefer block style (`|`, `>`) for multiline strings; avoid escaped `\n` inside quoted strings.
* Do not use anchors (`&`) and aliases (`*`) for complex structures — prefer explicit duplication or templating.
* Keep keys in a consistent order within each map (alphabetical or logical grouping).
* Validate against the target schema after structural changes.

---

# Security

* **Never store plain-text secrets** (passwords, tokens, keys) in committed YAML.
* Use environment variable substitution or secret references.

---

# Formatting

* **Never use vertical alignment.** Do not pad spaces to align values across keys.
* Compact, standard style — no unnecessary whitespace padding.

---

# Validation Focus

* indentation consistency
* unintended type coercion (bare `true`, `yes`, `on`, `null`)
* multiline string formatting
* schema or required-key violations after edits
