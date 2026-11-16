---
name: mkt-initiative-prioritize
description: This skill should be used when the user asks to "prioritize initiatives", "score initiatives", "ICE scoring", "rank ideas", "which should we do first", or mentions initiative prioritization, ICE framework, or deciding between options.
license: MIT
metadata:
  author: hungv47
  version: "1.1.0"
---

# Prioritize Initiatives (ICE Scoring)

*Solution Track — Step 2 of 4. Ranks initiatives with evidence-backed ICE scoring.*

## Inputs Required
- Initiative list from `.agents/mkt/initiatives.md`

## Output
- `.agents/mkt/prioritized-initiatives.md`

## Quality Gate
Before delivering, verify:
- [ ] Every score (I, C, E) has a one-sentence evidence citation — no naked numbers
- [ ] Scores are differentiated: no more than 2 initiatives share the same total ICE score
- [ ] ≤3 initiatives above cut line (force constraint even if team wants more)
- [ ] Each "proceed" initiative has: named owner, target metric with baseline, kill criteria

## Chain Position
Previous: `mkt-initiative-generate` | Next: `mkt-funnel-planner`

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If missing: **INTERVIEW.** Ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/mkt/product-context.md`. Or recommend running `mkt-copywriting` to bootstrap it.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `initiatives.md` | mkt-initiative-generate | **STOP.** "Run mkt-initiative-generate first to create the initiative list." |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `targets.md` | mkt-funnel-planner | Scoring calibration |

Read `.agents/mkt/initiatives.md`. List the initiatives.

---

## Step 1: Rank BEFORE Scoring

**Critical:** Rank all initiatives from most to least promising FIRST, based on gut + evidence. Then assign scores. This prevents the "everything is a 6" clustering problem.

Ask the user: *"If you could only do ONE of these, which would it be? And after that one?"*

Force-rank all initiatives 1 through N before scoring.

---

## Step 2: Score Each Initiative

Score 1-10 on three dimensions. **Every score needs a one-sentence evidence citation.**

| Dimension | 1-3 | 4-6 | 7-10 |
|-----------|-----|-----|------|
| **Impact** — How much will it move the target metric? | Minor, barely noticeable | Meaningful improvement | Significant or transformative |
| **Confidence** — How sure are we? | Gut feeling, no data | Some supporting data | Direct evidence, proven playbook |
| **Ease** — How easy to execute? | Multi-team, months | Moderate effort, manageable | Small team, quick turnaround |

**Bad:** "Impact: 7"
**Good:** "Impact: 7 — paid traffic is 60% of signups, and the old targeting had 3.5% conversion vs. current 1.2%"

**WebSearch directive:** If the user lacks evidence for a score, search for supporting data: `"[tactic] conversion improvement case study"`, `"[similar company] [tactic] results"`, `"[metric] improvement benchmark"`

ICE Score = I + C + E (sum). Scores should reflect the forced ranking from Step 1 — if you ranked it #1, its ICE should be highest.

---

## Step 3: Cut Line

Ask: **"How many can you execute well simultaneously?"**

Push for honesty:
- Solo/2-person team: 1-2
- Small team (3-5): 2-3
- Growth team (5+): 3-4

For each initiative, assign a decision:

| Decision | Meaning |
|----------|---------|
| **Proceed** | Start this week. Has owner, metric, kill criteria. |
| **Park** | Promising, but can't resource now. Revisit after current batch. |
| **Kill** | Not worth doing. State why clearly. |

---

## Step 4: Validate "Proceed" Initiatives

For each "Proceed" initiative, confirm:
- [ ] Owner named (a person, not "the team")
- [ ] Target metric has a numeric baseline
- [ ] Kill criteria: "Stop if [metric] < [threshold] after [duration]"
- [ ] Can begin execution within 1 week

If any check fails, resolve it now — don't proceed with gaps.

---

## Artifact Template

On re-run: rename existing artifact to `prioritized-initiatives.v[N].md` and create new with incremented version.

```markdown
---
skill: mkt-initiative-prioritize
version: 1
date: {{today}}
status: draft
---

# Prioritized Initiatives

## Forced Ranking (gut + evidence)

1. [Name] — most promising because [reason]
2. [Name]
3. [Name]
...

## ICE Scoring

| Rank | Initiative | I | C | E | ICE | Key Evidence |
|------|-----------|---|---|---|-----|-------------|
| 1 | [Name] | [score] | [score] | [score] | [sum] | [One-sentence evidence for top-scoring dimension] |
| 2 | ... | ... | ... | ... | ... | ... |

## Decisions

| Initiative | Decision | Owner | Target Metric (Baseline) | Kill Criteria |
|------------|----------|-------|-------------------------|---------------|
| [Name] | Proceed | [Person] | [Metric]: [current] | Stop if [metric] < [threshold] after [duration] |
| [Name] | Park | — | — | — |
| [Name] | Kill | — | — | Reason: [why] |

**Cut line:** [N] initiatives proceeding. Team capacity: [context].

## Next Step

Run `mkt-funnel-planner` to set targets for each "Proceed" initiative.
```

---

## Worked Example

```markdown
# Prioritized Initiatives

**Date:** 2026-03-13
**Skill:** mkt-initiative-prioritize

## Forced Ranking

1. Restore + Refine Paid Targeting — fastest fix for biggest root cause
2. Restore Homepage Social Proof — fast, addresses second root cause
3. Homepage A/B: Old vs New — definitive answer on redesign impact
4. Landing Page per Ad Group — higher effort but compounds with #1
5. Intent-Qualifying Ad Creative — interesting but less certain
6. Dedicated Onboarding for Paid — too complex for now

## ICE Scoring

| Rank | Initiative | I | C | E | ICE | Key Evidence |
|------|-----------|---|---|---|-----|-------------|
| 1 | Restore Paid Targeting | 8 | 8 | 9 | 25 | I:8 — paid is 60% of traffic, old targeting converted at 3.5% vs 1.2% now |
| 2 | Restore Social Proof | 7 | 7 | 9 | 23 | C:7 — Wayback shows old page had logos+testimonial that new page removed |
| 3 | Homepage A/B | 6 | 9 | 7 | 22 | C:9 — direct comparison eliminates guessing about redesign impact |
| 4 | LP per Ad Group | 7 | 6 | 5 | 18 | I:7 — message match lifts are well-documented (CXL: 20-50% improvement) |
| 5 | Intent Ad Creative | 5 | 4 | 6 | 15 | C:4 — no precedent with our audience, hypothesis only |
| 6 | Paid Onboarding | 7 | 3 | 3 | 13 | E:3 — needs eng + dynamic content, 4+ weeks |

## Decisions

| Initiative | Decision | Owner | Target Metric (Baseline) | Kill Criteria |
|------------|----------|-------|-------------------------|---------------|
| Restore Paid Targeting | **Proceed** | Sarah | Paid conversion: 1.2% | Stop if <2% after 10 days |
| Restore Social Proof | **Proceed** | James | Homepage bounce: 52% | Stop if >48% after 7 days |
| Homepage A/B | **Park** | — | — | Do after #1 and #2 ship |
| LP per Ad Group | **Park** | — | — | Revisit if paid targeting fix isn't enough |
| Intent Ad Creative | **Kill** | — | — | Too uncertain; paid targeting fix addresses the same root cause more directly |
| Paid Onboarding | **Kill** | — | — | Too complex for current team capacity |

**Cut line:** 2 initiatives proceeding. Team: 3-person growth team.

## Next Step

Run `mkt-funnel-planner` to set targets for Restore Paid Targeting and Restore Social Proof.
```

---

## References

- [references/ice-scoring-rubric.md](references/ice-scoring-rubric.md) — Detailed scoring calibration with scored examples
