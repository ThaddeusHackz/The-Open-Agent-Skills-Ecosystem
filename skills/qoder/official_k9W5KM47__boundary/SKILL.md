---
name: boundary
description: "Hard read/edit boundary for generated, cached, temporary, and non-source-of-truth paths. Use when Codex must decide which local files are valid source-of-truth inputs for exploration, edits, or review."
---

* Shared examples and formatting reference: [references/EXAMPLE.md](references/EXAMPLE.md).
* Keep new guidance, snippets, and edits aligned with that file.

---

# Purpose

* Reduce noise from generated, cached, temporary, and non-source-of-truth paths.
* Keep exploration, reading, editing, and review focused on stable source files.

---

# Rule

Unless the user explicitly overrides it, treat generated, cached, temporary, and non-source-of-truth paths as a **hard read/edit boundary**.

The agent must not:

* explore these paths
* read files from these paths
* edit files in these paths
* use files in these paths as review or source-of-truth inputs

---

# Pattern Source

* Keep detailed pattern lists in `references/EXAMPLE.md` unless a root controller needs only a compact boundary statement.

---

# Exceptions

* Follow explicit user scope when the task is about generated output, build artifacts, or logs.
* Read ignored paths only when they are the direct subject of the task and no source alternative exists.
* State the exception in the final response when it affects verification or evidence.
