---
name: markdown
description: "Markdown rules: ATX headings, fenced code blocks with language tag, consistent heading hierarchy."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Scope

Use this rule when:

* writing or editing `.md` files
* authoring READMEs, changelogs, or documentation pages
* reviewing Markdown for formatting consistency

Prioritize clarity, consistent structure, and predictable rendering.

---

# Core Rules

* Use ATX headings (`#`, `##`, `###`); never use setext underline style.
* Do not skip heading levels.
* Leave exactly one blank line before and after headings, code blocks, and lists.
* Use fenced code blocks (` ``` `) with an explicit language tag.
* Keep one list-marker style per local list block — do not mix `-`, `*`, `+` inside the same list.
* Use reference-style links when the same URL appears more than once.
* Maximum line length: 120 characters in prose (does not apply inside code blocks).
* Keep table columns aligned with padding spaces for readability.
* Do not use raw HTML unless rendering requires it and Markdown lacks an equivalent.

---

# H2 Divider Convention

When a maintained instruction doc is organized into repeated `##` sections, place a `---` divider before each `##`:

```md
---

## Section Title
```

Rules:

* the divider line must be exactly `---`
* one blank line between the divider and the `##` heading
* do not mix `---` with longer custom ruler lines in the same document
* once adopted, apply consistently across the whole file

---

# Skill Doc Conventions

* `SKILL.md` keeps a single H1 title at the top.
* Place the shared `references/EXAMPLE.md` reference block immediately under the H1 as a two-item unordered list (pointer + alignment reminder).
* Start the main body at `##`; nest with `###` and `####` only as needed.
* Use plain headings by default. Preserve manual prefixes such as `## 1.` or `### 1-1.` only when the existing file already uses a numbered taxonomy or ordered examples.
* In `references/EXAMPLE.md`, start with `# Examples` and the shared intro before the example body.

---

# Tone

* Write in active voice; prefer short declarative sentences.
* Use numbered lists only for true sequential steps; prefer plain headings or unordered lists for maintained guidance.
* Avoid filler words: "basically", "simply", "just", "note that".

---

# Formatting

* Follow the Google Markdown Style Guide: https://google.github.io/styleguide/docguide/style.html
* **Never use vertical alignment** outside of pipe-table columns.
* Compact, standard style — no unnecessary whitespace padding.

---

# Validation Focus

* consistent heading hierarchy (no skipped levels)
* code blocks with language tags
* broken or redundant links
* trailing whitespace, mixed local list markers, inconsistent numbering
* `---` divider precedes each `##` section in maintained instruction docs that adopt the convention
