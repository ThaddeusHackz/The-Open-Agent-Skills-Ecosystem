---
name: failure
description: "Failure analysis: establish reproduction path, capture first symptom, confirm break point before patching."
---

* Use [references/EXAMPLE.md](references/EXAMPLE.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

# 1. Overview

* Use this rule when behavior is failing and the fix is not yet justified. The goal is to confirm the break point before patching symptoms.

---

# 2. Use This Rule When

* runtime errors occur
* tests fail
* builds break
* a route, command, or workflow regresses
* a bug report describes incorrect behavior without a confirmed cause

---

# 3. Analysis Order

* establish the smallest reliable reproduction path
* capture the first clear symptom
* trace the shortest evidence-backed execution path
* identify the first plausible break point
* validate hypotheses one by one
* patch only after the cause is confirmed

---

# 4. Output To Recover Before Fixing

* reproduction path
* first visible symptom
* likely or confirmed break point
* evidence supporting the diagnosis
* remaining uncertainty

---

# 5. Practical Rules

* Start from the failing path, not from architecture guesses.
* Separate the first break point from downstream noise.
* Prefer one short hypothesis list over many loose possibilities.
* Re-run the original failing path after the fix when execution is available.

---

# 6. Boundaries

* Do not patch before the root cause is confirmed.
* Do not confuse a downstream stack trace with the actual origin.
* Do not skip reproduction when one can be established locally.

