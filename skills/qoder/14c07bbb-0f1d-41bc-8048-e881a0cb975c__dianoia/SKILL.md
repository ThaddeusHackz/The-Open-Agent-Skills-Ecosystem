---
name: dianoia
description: "DIANOIA: Diagnostic multi-agent reasoning with file-based workspace. Fans out to K=3 role-diverse proposer subagents (Minimalist, Skeptic, Explorer) in parallel, each writing results to a shared /tmp workspace; a reviewer subagent reads all proposals from files and cross-evaluates; main agent performs conservative synthesis with iterative re-execution (up to S=3). File-based communication prevents context overflow and enables full paper-faithful 4-phase pipeline. Triggers on `/dianoia <task>`, 'use dianoia', 'apply dianoia to ...'. Best for code-generation tasks with hidden tests, structured outputs, or schema-validated payloads."
---

# DIANOIA: File-Based Multi-Agent Reasoning

DIANOIA decomposes multi-agent reasoning gain into three measurable channels:
**coverage** (`G_explore`), **information** (`G_info`), **aggregation**
(`G_aggr`). This skill realises them via **file-based subagent coordination**:
subagents write results to a shared workspace directory; subsequent agents
read from those files instead of receiving bloated prompts. This prevents
context overflow.

---

## Output discipline (HIGHEST PRIORITY — read before anything else)

**The user-visible response MUST contain ONLY the code or JSON the user
asked for. NOTHING ELSE.**

Specifically, your final response must NOT contain:
- "Synthesis mode: ..." or "(synthesis mode: ...)"
- "Winner: M/S/E" or "confidence: ..."
- "DIANOIA Pipeline Complete" or "Phase X results:"
- "Subagent M produced..." or "Reviewer diagnosed..."
- "All three proposers passed" or any pipeline status
- Any sentence explaining your selection reasoning

**Correct** final response example:
```
def foo(x):
    return x + 1
```

**Wrong** final response example:
```
Synthesis mode: selection, winner: M, confidence: 0.98.

def foo(x):
    return x + 1
```

The ONLY exception: if the user explicitly says "show your work" / "explain
your reasoning", then include the trace. Otherwise, emit code and NOTHING
else. This is the #1 regression cause in all prior skill versions — narration
that breaks the host's code extractor.

---

## When to apply

Use DIANOIA on:
- `/dianoia <task>` — explicit slash invocation
- "use dianoia on ..." / "apply DIANOIA to ..."
- code-generation tasks with hidden tests, strict assertions, mocking, or
  exact-string outputs that punish paraphrasing.

**Skip** for trivial one-liner edits, pure information lookup, conversation,
or open-ended writing with no verifier.

---

## Phase 0 — Workspace initialisation

Before launching any subagent, create the workspace:

```bash
DIANOIA_WS="/tmp/dianoia_$(date +%s)_$$"
mkdir -p "$DIANOIA_WS"
```

All subagents will use this directory path. Pass it in every subagent prompt.

---

## Phase 1 — PROPOSE (3 subagents in parallel, targets G_explore)

Launch **three proposer subagents in ONE parallel message** (three Agent
tool-use blocks in a single response). Each proposer:
1. Implements the solution with its role-specific bias
2. Runs the code + tests in its own sandbox
3. Writes the full result to `$DIANOIA_WS/propose_{role}.json`
4. Returns ONLY: `"Done. Results written to $DIANOIA_WS/propose_{role}.json"`

The three roles create negative pairwise correlation (ρ̄ < 0), covering
more of the solution space than IID sampling:

### Proposer M — Minimalist

```
You are the MINIMALIST proposer in the DIANOIA pipeline.

WORKSPACE: {workspace_path}

TASK:
{task_spec}

TESTS:
{tests}

CONSTRAINTS:
- Shortest stdlib-idiomatic implementation. Prefer one-pass loops,
  comprehensions, or single expressions over multi-step logic.
- Trust the happy path. Do NOT add defensive checks unless tests
  explicitly require them.
- Copy any literal strings (exception messages, regex patterns, output
  templates, JSON keys) from the spec CHARACTER-FOR-CHARACTER.

STEPS:
1. Read the tests carefully — they ARE the spec.
2. Write the function.
3. Run the candidate + tests in your sandbox (Bash tool). Capture
   pass-count/total and the FIRST failing assertion if any.
4. Write the following JSON to {workspace_path}/propose_M.json:
   {{
     "role": "M",
     "code": "<full runnable code, no markdown fences>",
     "n_pass": <int>,
     "n_total": <int>,
     "all_pass": <bool>,
     "first_failure": "<traceback excerpt or null>",
     "approach": "<one sentence>"
   }}
5. After writing the file, respond with ONLY this exact text:
   "Done. Results written to {workspace_path}/propose_M.json"
   No other output.
```

### Proposer S — Skeptic

```
You are the SKEPTIC proposer in the DIANOIA pipeline.

WORKSPACE: {workspace_path}

TASK:
{task_spec}

TESTS:
{tests}

CONSTRAINTS:
- Be defensive. Explicit loops over comprehensions when edge cases exist.
- Before writing code, list the edge cases you will guard: empty input,
  single element, zero, negative, None, very large, unicode, mocked
  side effects, exception paths.
- Pay special attention to mocking conventions if the tests use them
  (MagicMock, side_effect, return_value, patch decorators).
- Copy literal strings from the spec character-for-character.

STEPS:
1. Read the tests carefully — they ARE the spec.
2. List edge cases the tests probe.
3. Write the function with guards for each.
4. Run candidate + tests in sandbox. Capture pass-count/total and
   first failure if any.
5. Write the following JSON to {workspace_path}/propose_S.json:
   {{
     "role": "S",
     "code": "<full runnable code, no markdown fences>",
     "n_pass": <int>,
     "n_total": <int>,
     "all_pass": <bool>,
     "first_failure": "<traceback excerpt or null>",
     "edge_cases": ["<list of edge cases addressed>"],
     "approach": "<one sentence>"
   }}
6. After writing the file, respond with ONLY this exact text:
   "Done. Results written to {workspace_path}/propose_S.json"
   No other output.
```

### Proposer E — Explorer

```
You are the EXPLORER proposer in the DIANOIA pipeline.

WORKSPACE: {workspace_path}

TASK:
{task_spec}

TESTS:
{tests}

CONSTRAINTS:
- Take an unconventional algorithmic approach. If the obvious solution
  is iteration, try recursion or functools. If the obvious solution is
  a dictionary, try sorted arrays. If the obvious approach is
  imperative, try a declarative/functional style.
- Explore alternative libraries or stdlib modules others might miss
  (itertools, collections, operator, contextlib, etc.).
- Still must pass the tests — creativity does NOT excuse incorrectness.
- Copy literal strings from the spec character-for-character.

STEPS:
1. Read the tests carefully — they ARE the spec.
2. Identify the "obvious" approach, then deliberately choose a different
   algorithm or pattern.
3. Write the function.
4. Run candidate + tests in sandbox. Capture pass-count/total and
   first failure if any.
5. Write the following JSON to {workspace_path}/propose_E.json:
   {{
     "role": "E",
     "code": "<full runnable code, no markdown fences>",
     "n_pass": <int>,
     "n_total": <int>,
     "all_pass": <bool>,
     "first_failure": "<traceback excerpt or null>",
     "alternative_to": "<what the 'obvious' approach would have been>",
     "approach": "<one sentence about your unconventional choice>"
   }}
6. After writing the file, respond with ONLY this exact text:
   "Done. Results written to {workspace_path}/propose_E.json"
   No other output.
```

---

## Phase 2 — EXECUTE (implicit)

Execution is embedded in Phase 1: each proposer runs its own sandbox and
records pass/fail. This gives per-arm `G_info` without a separate phase.
The execution results live in the proposal JSON files.

---

## Phase 3 — REVIEW (1 subagent, after Phase 1 completes, targets G_info)

Launch ONE reviewer subagent. It reads all proposal files and produces a
cross-evaluation. The reviewer writes to `$DIANOIA_WS/review.json` and
returns only a status line.

```
You are the DIANOIA cross-reviewer. Three proposer agents (M=Minimalist,
S=Skeptic, E=Explorer) have produced candidates and run them through
sandboxes. Your job is to diagnose and decide — NOT to write code.

WORKSPACE: {workspace_path}

STEPS:
1. Read these files:
   - {workspace_path}/propose_M.json
   - {workspace_path}/propose_S.json
   - {workspace_path}/propose_E.json
   (Use the Read tool or Bash cat to read them.)

2. For each candidate, assess:
   - Did it pass all tests? (check "all_pass" field)
   - If not, what is the root cause from "first_failure"?
   - What are its strengths and weaknesses?

3. Make your decision following this priority:
   a) If EXACTLY ONE candidate passes all tests: pick it. winner=that role.
   b) If MULTIPLE candidates pass all tests: pick the most idiomatic/robust.
   c) If NO candidate passes all tests:
      - Identify the candidate closest to passing (highest n_pass).
      - Identify the single smallest concrete defect (one line/branch).
      - Check if another candidate already has the correct version of
        that line (donor for a graft).
      - Specify the minimal patch: which line to add/replace/delete.

4. Write the following JSON to {workspace_path}/review.json:
   {{
     "winner": "M" | "S" | "E" | "graft",
     "winning_code": "<verbatim from the chosen candidate, or null if graft>",
     "scores": {{
       "M": {{"pass_rate": "n_pass/n_total", "strengths": "...", "weaknesses": "..."}},
       "S": {{"pass_rate": "n_pass/n_total", "strengths": "...", "weaknesses": "..."}},
       "E": {{"pass_rate": "n_pass/n_total", "strengths": "...", "weaknesses": "..."}}
     }},
     "graft": null OR {{
       "scaffold": "M" | "S" | "E",
       "donor": "M" | "S" | "E" | null,
       "patch": "<exact line(s) to add/replace/delete>",
       "rationale": "<one sentence>"
     }},
     "synthesis_mode": "selection" | "selection+repair" | "rescue",
     "confidence": 0.0..1.0,
     "diagnosis": "<one-paragraph analysis of why proposals succeeded or failed>"
   }}

5. After writing the file, respond with ONLY this exact text:
   "Done. Review written to {workspace_path}/review.json"
   No other output.

CRITICAL RULES:
- Do NOT modify any code. You diagnose and recommend — you don't implement.
- Do NOT paraphrase exception messages or regex literals. Quote them
  character-for-character.
- If a passing candidate exists, prefer SELECTION over GRAFT. Working
  code is finished code.
- Keep "winning_code" as the EXACT string from the proposal file — no
  reformatting, no added imports, no style changes.
```

---

## Phase 4 — SYNTHESIZE (main agent, targets G_aggr)

After the reviewer subagent returns, YOU (the main agent) read ONLY
`$DIANOIA_WS/review.json` and act on it. This is the only file you need
to read — keeping your context minimal.

### Decision logic:

1. **`synthesis_mode == "selection"` and `winner` is M/S/E:**
   Take `winning_code` verbatim. Do NOT rewrite, reformat, or "improve".
   Working code that passes tests is finished code. Emit it immediately.

2. **`synthesis_mode == "selection+repair"` and `winner` is M/S/E:**
   The winner passes all tests. Take it verbatim. (The "+repair" label
   means the reviewer noted minor issues but the code still passes.)
   Emit it immediately.

3. **`synthesis_mode == "rescue"` or `winner == "graft"`:**
   No candidate passes all tests. Apply the reviewer's graft:
   - Take the scaffold candidate's code (read from the relevant
     `propose_{scaffold}.json` file)
   - Apply the patch literally as specified
   - Run the patched code in your sandbox
   - If it passes: emit it
   - If it fails: do ONE focused repair on the diagnosed line, re-run
   - If still failing after one repair: read all 3 proposal files, take
     the best-passing candidate, and try one more synthesis attempt
   - Cap at S=3 total sandbox iterations. After 3 failures, return the
     best-passing candidate as-is.

### Iterative synthesis loop (for rescue/graft only):

```
for attempt in 1..3:
    apply_patch_or_repair()
    run_in_sandbox()
    if passes:
        emit(code)
        break
    else:
        diagnose_from_error()
        # next iteration targets the specific failure
if all_attempts_fail:
    emit(best_passing_candidate_code)
```

### Emit rule (CRITICAL — re-read the Output Discipline section above):

After deciding the final code, your ENTIRE visible response is the code.
- If host expects `{"code": "..."}`: emit that JSON and STOP.
- If host expects plain code: emit the code and STOP.
- Do NOT prepend ANY text before the code. Not one word. Not one line.
- Do NOT append ANY text after the code.
- Specifically NEVER emit: "Synthesis mode:", "Winner:", "confidence:",
  "All proposers passed", "I selected", "The reviewer recommended".
- Your scratchpad/thinking can contain reasoning. Your visible output
  cannot. Violation of this rule is the #1 cause of benchmark regression.

---

## File workspace summary

| File | Written by | Read by |
|------|-----------|---------|
| `propose_M.json` | Proposer M subagent | Reviewer subagent |
| `propose_S.json` | Proposer S subagent | Reviewer subagent |
| `propose_E.json` | Proposer E subagent | Reviewer subagent |
| `review.json` | Reviewer subagent | Main agent |

The main agent's context sees only:
- Three one-line status confirmations from proposers
- One one-line status from reviewer
- The content of `review.json` (compact, ~500 tokens)

Total context cost: ~600 tokens. Compare to the previous approach where
3 full proposals + execution traces consumed 3000-6000 tokens in the
parent context.

---

## Anti-patterns

- **Spawning proposers sequentially.** All three MUST be in one parallel
  message (three Agent tool-use blocks). Sequential launch loses
  wall-clock parallelism.
- **Reading proposal files in the main agent.** Only read `review.json`.
  The reviewer already synthesised the cross-evaluation. Reading proposal
  files directly wastes context.
- **Rewriting the winning candidate.** Working code is finished code.
  The main agent's job is to SELECT or APPLY A LITERAL PATCH.
  Paraphrasing exception messages is the #1 silent regression.
- **Emitting skill-internal narration.** The host parses the response with
  a strict contract; any extra prose breaks JSON/code extraction.
- **Spending synthesis tokens on reasoning before code.** Emit the host's
  contract FIRST. Reasoning lives in scratchpad.
- **Ignoring the reviewer's recommendation.** Trust the reviewer unless
  you have sandbox evidence it's wrong. The reviewer has read all three
  proposals; you have not.
- **Over-patching during rescue.** The graft targets ONE diagnosed defect.
  Do not cascade into "while I'm here" cleanups.

