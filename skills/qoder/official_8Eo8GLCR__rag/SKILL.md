---
name: rag
description: "Use when the task involves planning, scaffolding, documenting, indexing, evaluating, or extending a retrieval-augmented knowledge base for company knowledge."
---

* Use [references/EXAMPLE.md](references/EXAMPLE.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

# 1. Overview

* Use this skill to build or extend an evidence-backed RAG knowledge base for company projects, DB tables, business processes, and glossary terms. Prove retrieval quality on a seed set before expanding coverage.

---

# 2. Use This Rule When

* designing the initial `knowledge_base/` layout
* drafting or correcting project, table, process, or glossary documents
* planning or reviewing local embedding, chunking, retrieval, or eval scripts
* defining evaluation questions, pass criteria, and rollout gates
* deciding where RAG settings belong in this skill package

---

# 3. Output Order

* Inventory and scaffolding
* Seed documentation
* Local prototype indexing
* Coverage expansion
* Optional agent or tool integration

---

# 4. Phase Contracts

* Inventory: list target sources, create the minimum `knowledge_base/` layout, and define
* `knowledge_base/_schema.md`.
* Seed docs: start with the smallest high-value project and core tables; read real source before
* drafting.
* Prototype indexing: chunk by document section, attach stable metadata, and expose a bounded local
* retrieval check.
* Expansion: expand by project batch and re-run eval after each batch.
* Integration: expose retrieval only after documentation and local eval are stable.

---

# 5. Evidence Rules

* Follow Plan -> Explore -> Implement -> Verify -> Finalize for each phase.
* Never document a project, table, column, relationship, or business rule without source evidence.
* Cite the source file path or explicit inference origin in every generated document.
* Mark unknown fields as `UNVERIFIED`.
* Ask one narrow question only when correctness cannot be inferred from the repository surface.

---

# 6. Content Rules

* Use lowercase snake_case filenames.
* Keep one project README per project, one table per file, one process per file, and one glossary
* term per file.
* Keep each document in one language.
* Prefer short, concrete sentences over broad boilerplate.
* Separate confirmed facts from inferred behavior.
* Each document should help a new teammate answer a real question.

---

# 7. Recommended Layout

```md
knowledge_base/
  _schema.md
  _eval/questions.jsonl
  _tools/
  projects/<project_name>/README.md
  tables/<schema>/<table_name>.md
  processes/<process_name>.md
  glossary/<term>.md
```

---

# 8. Document Requirements

* Project docs state purpose, major users, entry points, related tables/processes, caveats, and evidence.
* Table docs state purpose, lifecycle, columns, relationships, business rules, caveats, and evidence.
* Process docs state trigger, ordered steps, outcomes, related projects, touched tables/APIs, and caveats.
* Glossary docs define the term, confusing nearby terms, and where the term appears.

---

# 9. Index And Eval Rules

* Prefer section-boundary chunking using `##` headings.
* Keep one table document as one chunk unless it becomes too large for reliable retrieval.
* Track `type`, `project`, `schema`, `legacy`, and `source_path` metadata when available.
* Store generated index artifacts under `knowledge_base/_index/` and keep them out of version control.
* Maintain `knowledge_base/_eval/questions.jsonl`.
* Add at least 20 curated questions before claiming prototype quality.
* Do not claim retrieval quality without reporting the measured pass rate.

---

# 10. Config Surface

* Keep skill instructions in `SKILL.md`.
* Keep shared examples in `references/EXAMPLE.md`.
* Keep agent manifest metadata in `agents/openai.yaml`.
* Use the stable `interface` manifest block shown in [references/EXAMPLE.md](references/EXAMPLE.md).
* Add `dependencies` only when a real external dependency is required.
* Place indexing, retrieval, or eval defaults in the real tool or project config that consumes them.

---

# 11. Quality Rules

* Small and verifiable beats broad and speculative.
* Prefer a seed set that passes retrieval checks over a large undocumented catalog.
* Avoid copy-pasted prose that says nothing concrete.
* Keep content reversible until the eval proves quality.
