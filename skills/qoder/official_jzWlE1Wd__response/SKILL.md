---
name: response
description: "Final response format: Korean-first, plain text, four-section order (Process / Checks / Issues / Updates)."
---

* Use [references/EXAMPLE.md](references/EXAMPLE.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

# 1. Overview

* Use this rule for final user-facing responses. Keep reporting short, markdown-formatted, Korean-first, and structurally consistent.

---

# 2. Use This Rule When

* sending the final answer
* summarizing implementation and verification
* reporting changed files and remaining risks

---

# 3. Required Section Order

* `● Process`
* `● Checks`
* `● Issues`
* `● Updates`

---

# 4. Formatting Rules

* Final responses are written in Korean by default.
* Emit the final response as markdown.
* Use numbered list items (`1.`) for content lines within each section.
* Write each `Updates` item as `1. \`[path]\` : detail`.
* Use abbreviated paths such as `../merge.ps1`, `../mapper.xml`, `../agent_completion.py`.
* Use inline code (backticks) for file paths and technical terms.
* Do not use hyphenated numbering such as `1-1.`, `1-30.`, or `2-4.` for final-response list items.
* Default to flat ordered lists such as `1.`, `2.`, `3.` in every section.

---

# 5. Content Priorities

* lead with what changed
* show what was actually checked
* separate real issues from routine notes
* list only changed files under `Updates`

