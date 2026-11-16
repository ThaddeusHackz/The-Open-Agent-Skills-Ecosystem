---
name: mkt-root-cause
description: This skill should be used when the user asks to "analyze the evidence", "test hypotheses against data", "review hypothesis results", "we gathered the data", or mentions root cause analysis, hypothesis verdict, or evidence review after gathering data for hypotheses. Requires hypotheses.md to exist.
license: MIT
metadata:
  author: hungv47
  version: "1.1.0"
---

# Root Cause Analysis

*Problem Track — Step 3 of 3. Reviews evidence against hypotheses and identifies the root cause.*

## Inputs Required
- Hypotheses from `.agents/mkt/hypotheses.md`
- User-provided data or data files for each hypothesis

## Output
- `.agents/mkt/root-cause.md`

## Quality Gate
Before delivering, verify:
- [ ] Every hypothesis has a verdict: Confirmed, Rejected, or Inconclusive
- [ ] Every verdict cites a specific number or data point (not "seems like" or "probably")
- [ ] Root cause statement includes gap percentage (e.g., "explains ~60% of gap")
- [ ] Every Inconclusive item has a concrete next step (what data, where, who)

## Chain Position
Previous: `mkt-hypothesis` | Next: `mkt-initiative-generate`

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If missing: **INTERVIEW.** Ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/mkt/product-context.md`. Or recommend running `mkt-copywriting` to bootstrap it.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `hypotheses.md` | mkt-hypothesis | **STOP.** "Run mkt-hypothesis first to develop testable hypotheses." |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | mkt-copywriting | Industry context for data interpretation |

Read `.agents/mkt/hypotheses.md`. Quote the ranked hypotheses.

Then ask: **"What did you find for each hypothesis? Share data, screenshots, reports, CSVs, or describe what you saw."**

If user provides data files, read and analyze them directly — don't ask the user to summarize data you can read yourself.

If user hasn't gathered data yet:
- Use WebSearch for publicly available evidence: `"[competitor] launch [date range]"`, `"[industry] [metric] trend [year]"`, `"[tool name] outage [date]"`
- Point them to the specific sources listed in the hypotheses file

---

## Step 1: Verdict Per Hypothesis

For each hypothesis:

| Verdict | Criteria | What to Write |
|---------|----------|--------------|
| **Confirmed** | Evidence matches the "then" clause and supports the "because" | "[Data point] confirms: [what it shows]. Mechanism supported." |
| **Rejected** | Evidence contradicts the "then" clause | "[Data point] shows [opposite of prediction]. Cause eliminated." |
| **Inconclusive** | Evidence is ambiguous or insufficient | "[What we found]. Need: [specific additional data], from [source], owned by [who]." |

Be direct. "The data doesn't support this" is useful. "It's hard to tell" is not.

---

## Step 2: Root Cause Statement

Synthesize confirmed hypotheses:

> **Root Cause 1 (~X% of gap):** [Cause], evidenced by [specific data]. [Mechanism].
> **Root Cause 2 (~Y% of gap):** [Cause], evidenced by [specific data]. [Mechanism].
> **Unexplained (~Z%):** [What's still unknown]. Next step: [what to investigate].

Gap percentages should roughly sum to 100%. They don't need to be precise — "~60%" is fine. The point is to show which cause matters most.

---

## Step 3: Next Steps

| Situation | Action |
|-----------|--------|
| Clear root cause(s) identified | "Run `mkt-initiative-generate` to brainstorm solutions targeting: [root cause]" |
| Inconclusive items remain | "Before generating solutions, gather: [specific data]. Then re-run this skill." |
| Multiple root causes, different sizes | "Address Root Cause 1 first (~X% of gap). It's the highest-leverage fix." |

---

## Artifact Template

On re-run: rename existing artifact to `root-cause.v[N].md` and create new with incremented version.

```markdown
---
skill: mkt-root-cause
version: 1
date: {{today}}
status: draft
---

# Root Cause Analysis

**Problem:** [problem statement]

## Verdict Table

| # | Hypothesis | Verdict | Evidence | Gap |
|---|-----------|---------|----------|-----|
| 1 | [Short name] | Confirmed / Rejected / Inconclusive | [Specific data cited] | ~X% |
| 2 | ... | ... | ... | ... |

## Root Cause Statement

**Root Cause 1 (~X% of gap):** [Cause], evidenced by [data].
[One sentence explaining the mechanism.]

**Root Cause 2 (~Y% of gap):** [Cause], evidenced by [data].
[One sentence explaining the mechanism.]

**Unexplained (~Z%):** [Description]. Next data needed: [what], from [where].

## Next Step

Run `mkt-initiative-generate` targeting:
1. [Root cause 1 — specific aspect to solve]
2. [Root cause 2 — specific aspect to solve]
```

---

## Worked Example

**User provides data for the signup decline hypotheses:**
- "Checked DB vs GA4 — both show the same drop. Tracking is fine."
- "Paid traffic conversion dropped from 3.5% to 1.2%. Organic is still at 4.1%."
- "Homepage bounce rate increased from 35% to 52% for all traffic."

```markdown
# Root Cause Analysis

**Date:** 2026-03-13
**Skill:** mkt-root-cause
**Problem:** Weekly signups 200 instead of 350 (43% gap)

## Verdict Table

| # | Hypothesis | Verdict | Evidence | Gap |
|---|-----------|---------|----------|-----|
| 1 | Tracking broken | **Rejected** | GA4 and DB both show same drop (200/week). Tracking is working correctly. | 0% |
| 2 | Ad targeting reduced quality | **Confirmed** | Paid conversion dropped from 3.5% to 1.2% (66% decline). Organic stable at 4.1%. Paid traffic is 60% of total. | ~55% |
| 3 | Homepage redesign reduced conversion | **Confirmed** | Bounce rate up from 35% to 52% across ALL sources. Even organic visitors are bouncing more, suggesting the page itself is the problem. | ~35% |

## Root Cause Statement

**Root Cause 1 (~55% of gap):** Ad targeting change brought low-intent visitors, evidenced by paid conversion dropping 66% while organic held steady. The broader targeting reaches people outside the ICP.

**Root Cause 2 (~35% of gap):** Homepage redesign reduced trust/clarity, evidenced by bounce rate rising 17 points across all traffic sources. The new page likely lacks the social proof or clear value prop of the old design.

**Unexplained (~10%):** Minor variance, possibly seasonal. No action needed.

## Next Step

Run `mkt-initiative-generate` targeting:
1. Paid targeting — restore or improve audience quality
2. Homepage — restore trust signals and clarify value proposition
```

---

## References

None needed — this skill's framework is simple. The hypothesis-guide.md in mkt-hypothesis covers the upstream methodology.
