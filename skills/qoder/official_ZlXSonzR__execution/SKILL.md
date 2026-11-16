---
name: execution
description: "Smallest complete change rule: preserve local code shape, extend existing patterns, no speculative extraction or cleanup."
---

* Use [references/EXAMPLE.md](references/EXAMPLE.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

# 1. Overview

* Use this rule for ordinary implementation work. Keep changes small, direct, and aligned with the target repository's existing code shape.

---

# 2. Use This Rule When

* editing existing code
* adding small features or fixes
* deciding whether to extract helpers or restructure control flow
* judging whether a comment, rename, or cleanup is actually in scope

---

# 3. Core Rules

* Apply the smallest complete change that solves the request.
* Preserve existing structure, naming, control flow, and file layout unless the request requires change.
* Extend existing patterns before introducing new layers or helpers.
* Keep simple flows inline.
* **Strong rule:** do not split methods, functions, classes, scripts, or code blocks into overly fine-grained pieces.
* Keep related statements together as one cohesive chunk unless extraction has a current, concrete reason.
* When a code change needs comment edits, apply the `comments` skill and keep the comment surface local.
* Do not split straightforward logic into tiny helpers, wrappers, abstractions, or layers without a real current need.
* Do not widen scope into unrelated cleanup, renaming, or speculative refactoring.
* Treat stable local style as part of the contract.
* Fail clearly with contextual errors instead of hiding uncertain behavior.
* Use only real APIs, files, types, and runtime behavior.
* Do not add defensive validation that duplicates guarantees already established by nearby code or stable local contracts.

---

# 4. Code Shape Guidance

* Match the repository's established grouping rhythm, indentation density, and line-wrapping style.
* Preserve existing section-comment scaffolding when the file uses it for scanability.
* For brace-based languages, use Stroustrup clause layout: close the preceding block, then start `else`, `catch`, or `finally` on the next line.
* Do not rewrite a file into a cleaner-looking but differently grouped shape just to satisfy a generic style instinct.
* Avoid formatter-like prettifying of object layout, JSX layout, section comments, or line breaks when the local file already has a stable rhythm.
* Keep unrelated code unchanged even when nearby style differs from your preference.
* Keep one guard at the unstable boundary.
* Reuse normalized values instead of re-checking the same contract repeatedly.
* Do not widen a small fix into broad defensive cleanup.

---

# 5. When Extraction Is Allowed

* Create a helper, wrapper, extracted method, or new layer only when it:

* removes real duplication
* isolates unavoidable complexity
* protects a clear boundary
* satisfies an actual contract or test seam

---

# 6. Boundaries

* Do not fabricate APIs or runtime behavior.
* Do not normalize a whole file when only a local edit is needed.
* Do not treat cosmetic consistency as sufficient reason for broad edits.
