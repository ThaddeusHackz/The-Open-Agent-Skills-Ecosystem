---
name: comments
description: "Default numbered one-line `―` dividers; paired outer blocks only for very long code sections."
---

* Use [references/EXAMPLE.md](references/EXAMPLE.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

# 1. Overview

* Use this rule when adding, editing, or preserving comments in code. The goal is scanability, not decoration. Preserve local style while prioritizing numbered one-line `―` divider comments for declarations and logical sections.

---

# 2. Use This Rule When

* adding a new comment to existing code
* editing a block that already uses section comments
* deciding whether a comment is needed
* preserving or extending an existing comment scaffold
* matching divider-comment rhythm in JS, TS, Java, PowerShell, SQL, or similar source files

---

# 3. Core Rules

* **Mandatory:** add a numbered section-divider comment immediately above any function, class, or
* method declaration.
* Apply the smallest complete comment change that solves the request.
* Preserve existing local code shape and comment rhythm unless the request requires change.
* Do not let comment placement drive tiny function, method, or section splits; keep related code blocks cohesive.
* Prefer section-divider comments over casual descriptive comments when a block needs a visible
* boundary.
* Keep comments structural, concise, and purpose-driven.
* Do not add comments that merely restate obvious syntax.
* Do not add numbered section comments above every simple constant, scalar variable, or assignment.
* Do not widen scope into unrelated comment cleanup or repository-wide normalization.
* Preserve untouched comments unless they become incorrect.

---

# 4. Divider Style

* Use the file's local single-line comment prefix such as `//` or `#`.
* The full rendered divider line must be exactly 100 characters, including indentation, comment prefix, number, title, one space before the ruler, and repeated `―`.
* If a title would leave no room for at least three `―` characters within 100 characters, shorten the title without changing its meaning.

* Default top-level divider:

```js
// 1. Normalize input ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
```

* Use paired outer blocks only for very long sections:

```js
// ―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
// title
// ―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
```

* Use repeated `―`, not `-`.
* Use top-level numbers such as `1.` and child numbers such as `1-1.`.
* Keep maximum numbering depth to two levels.
* Keep child comments short, single-line, and compact.
* Split a broad topic before it stretches into long child chains such as `1-10.`.
* Keep divider lines at 100 characters across the repository instead of using file-local ruler lengths.
* Make paired block top and bottom rulers match exactly.

---

# 5. Placement

* Place the comment immediately above the declaration or logical block it describes.
* Always keep exactly one empty line immediately above a one-line divider or paired block opening ruler when it follows code or other content.
* Do not leave two or more empty lines above a divider.

* Do not insert an empty line inside a paired three-line divider block.
* When a paired divider block sits directly above code, code starts on the next line.
* When a one-line divider sits directly above code, code starts on the next line.
* When a top-level divider introduces child comments, one empty line after the divider is allowed.

---

# 6. Comment Content

* Comments should explain block purpose, business meaning, boundary conditions, preservation intent, grouping intent, editability rules, or non-obvious constraints. Do not narrate obvious syntax.

* If one short internal explanation is truly needed inside a block, use a plain single-line comment. This is secondary; section dividers remain primary.

---

# 7. Korean Tone

* When writing Korean comments:

* prefer concise noun-like or clipped statement-like endings
* prefer short, compact wording over full prose sentences
* avoid verbose sentence-final phrasing unless the file already strongly uses that tone

---

# 8. Add Or Skip

* Add a comment only when at least one is true:

* the user explicitly asked for comments
* it is a function, class, or method declaration
* a function or block has multiple logical phases
* the surrounding file already uses section comments
* the business meaning is not obvious from code alone
* a boundary or exclusion rule should be visible

* Skip comments for tiny obvious code that is not a declaration.

---

# 9. Boundaries

* Do not comment every line mechanically.
* Do not translate existing comments unless the request requires it.
* Do not rename sections for style only.
* Do not fabricate intent that is not supported by the code.
* Do not refactor code only to make comment placement easier.
* Prefer no comment over a bad comment.

---

# 10. Relationship To Other Rules

* This rule complements minimal-diff implementation rules and local-style preservation. It does not authorize broad refactoring, cosmetic repository-wide cleanup, unrelated renaming, or comment normalization across untouched files.
