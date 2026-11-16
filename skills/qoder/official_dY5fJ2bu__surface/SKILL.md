---
name: surface
description: "Surface analysis: map entry points, callers, dependencies, and contract edges before implementing."
---

* Use [references/EXAMPLE.md](references/EXAMPLE.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

# 1. Overview

* Use this rule to map only the implementation surface that matters. The goal is to find the nearest entry point, caller chain, dependency edge, and contract boundary without drifting into whole-repo exploration.

---

# 2. Use This Rule When

* locating the entry point for a requested change
* assessing blast radius before implementation
* checking coupled callers, DTOs, mappers, configs, or command arguments
* deciding which files are truly in scope

---

# 3. Exploration Order

* start at the requested file, symptom, or entry point
* identify direct callers and consumers
* trace immediate dependencies and outputs
* inspect contract edges that the change can break
* stop when the implementation surface is clear enough

---

# 4. Contract Edges To Check

* method signatures
* DTO or payload shapes
* mapper parameters
* query result shapes
* props and returned data
* config keys
* CLI arguments
* filesystem path conventions

---

# 5. Practical Rules

* Start from the concrete change point first.
* Prefer nearby evidence over distant architecture.
* Separate true in-scope files from possible follow-up files.
* Keep a short list of coupled files that must move with the change.
* Stop exploring once the worker is unblocked and the surface is clear.

---

# 6. Boundaries

* Do not map the whole repository without evidence.
* Do not turn surface analysis into a redesign plan.
* Do not keep reading distant modules once the contract surface is already understood.
