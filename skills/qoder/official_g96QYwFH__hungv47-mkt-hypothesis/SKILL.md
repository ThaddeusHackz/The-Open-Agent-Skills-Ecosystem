---
name: mkt-hypothesis
description: This skill should be used when the user asks to "form hypotheses", "test assumptions", "prioritize what to investigate", "what should we check first", or mentions hypothesis development, data requirements, or testability after completing a diagnosis. Requires diagnosis.md to exist.
license: MIT
metadata:
  author: hungv47
  version: "1.1.0"
---

# Hypothesis Development & Data Planning

*Problem Track — Step 2 of 3. Turns logic tree leaves into ranked, testable hypotheses with data requirements.*

## Inputs Required
- Logic tree from `.agents/mkt/diagnosis.md`

## Output
- `.agents/mkt/hypotheses.md`

## Quality Gate
Before delivering, verify:
- [ ] Every hypothesis follows If/Then/Because format
- [ ] Every "then" clause names a specific metric or observable data point
- [ ] Every hypothesis has a named data source (not "check analytics" — which tool, which report)
- [ ] Hypotheses are ranked by testability (easiest to test first)

## Chain Position
Previous: `mkt-diagnosis` | Next: `mkt-root-cause`

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If missing: **INTERVIEW.** Ask the user 8 product questions (what, who, problem, differentiator, proof points, pricing, objections, voice) and save to `.agents/mkt/product-context.md`. Or recommend running `mkt-copywriting` to bootstrap it.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `diagnosis.md` | mkt-diagnosis | **STOP.** "Run mkt-diagnosis first to define the problem with a logic tree." |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | mkt-copywriting | Better hypothesis framing |

Read `.agents/mkt/diagnosis.md`. Quote the problem statement and list the leaf nodes.

---

## Step 1: Form Hypotheses

For each leaf of the logic tree:

> **If** [this cause is true], **then** we'd see [specific observable evidence], **because** [mechanism that explains why].

### What Makes a Strong Hypothesis

| Element | Weak | Strong |
|---------|------|--------|
| **If** | "onboarding is bad" | "onboarding emails are being spam-filtered since the domain migration on Jan 15" |
| **Then** | "conversion drops" | "day-1 email open rate dropped below 20% (was 45%)" |
| **Because** | "emails matter" | "the new sending domain has no reputation, triggering ESP spam filters" |

The "then" must be something you can look up in a specific tool. The "because" must explain the mechanism — it's what you learn from if the hypothesis is wrong.

---

## Step 2: Map Data Requirements

For each hypothesis:

| Hypothesis | Deciding Data Point | Confirming Evidence | Rejecting Evidence | Source (Tool → Report) | Owner |
|------------|-------------------|--------------------|--------------------|----------------------|-------|
| [If/Then/Because] | [Single data point that decides] | [What you'd see if true] | [What you'd see if false] | [e.g., "GA4 → Acquisition → Traffic by source"] | [Person] |

**WebSearch directive:** Before finalizing, search `"[topic] common causes" OR "[metric] drop reasons [industry]"` to check if you're missing any high-probability hypotheses. Also search `"[competitor name] [recent change]"` if external factors might be at play.

---

## Step 3: Rank by Testability

Rank hypotheses by: (a) how quickly you can get the data, AND (b) how much of the gap it would explain if confirmed.

| Priority | Hypothesis (short name) | Data Available Now? | Potential Gap Explained | Test Time |
|----------|------------------------|--------------------|-----------------------|-----------|
| 1 | [Easiest + highest impact] | Yes / Partial / No | ~X% | [Hours/Days/Weeks] |
| 2 | ... | ... | ... | ... |

**Logic:** Test what you can test TODAY first. Eliminate hypotheses fast. Don't spend weeks on #4 when #1 takes an hour to check.

---

## Artifact Template

On re-run: rename existing artifact to `hypotheses.v[N].md` and create new with incremented version.

```markdown
---
skill: mkt-hypothesis
version: 1
date: {{today}}
status: draft
---

# Hypotheses

**Problem:** [problem statement from diagnosis]

## Hypotheses (Ranked by Testability)

### 1. [Short name] — Priority: HIGH
**If** [cause], **then** [observable evidence], **because** [mechanism].
- **Deciding data:** [specific data point]
- **Source:** [Tool → Report → Metric]
- **Owner:** [person/team]
- **Confirming:** [what you'd see if true]
- **Rejecting:** [what you'd see if false]
- **Potential gap explained:** ~X%

### 2. [Short name] — Priority: HIGH
[Same format]

### 3. [Short name] — Priority: MEDIUM
[Same format]

## Next Step

Gather data for hypotheses #1 and #2. Then run `mkt-root-cause` to analyze findings.
```

---

## Worked Example

**From diagnosis:** Weekly signups are 200 instead of 350 (43% gap). Inflection: homepage redesign + ad targeting change 8 weeks ago.

```markdown
# Hypotheses

**Date:** 2026-03-13
**Skill:** mkt-hypothesis
**Problem:** Weekly signups 200 instead of 350 (43% gap, 8 weeks)

## Hypotheses (Ranked by Testability)

### 1. Tracking broken on new homepage — Priority: HIGH
**If** the homepage redesign broke the signup tracking pixel, **then** GA4 shows a sudden drop in recorded signups coinciding with the deploy date while server-side signup records remain stable, **because** the new page template may not include the tracking script.
- **Deciding data:** Compare GA4 signup events vs. database signups for the last 8 weeks
- **Source:** GA4 → Events → sign_up AND production database signup count
- **Owner:** Engineering
- **Confirming:** GA4 shows drop but DB signups are flat
- **Rejecting:** GA4 and DB both show the same drop
- **Potential gap explained:** ~100% (if tracking, not real decline)

### 2. Ad targeting change reduced quality — Priority: HIGH
**If** the ad targeting change brought lower-intent visitors, **then** paid traffic volume stayed flat but paid visitor signup rate dropped, **because** broader targeting reaches people less likely to convert.
- **Deciding data:** Signup rate by traffic source (paid vs organic) before/after change
- **Source:** GA4 → Acquisition → Traffic source → Conversion rate
- **Owner:** Marketing (paid team)
- **Confirming:** Paid conversion rate dropped; organic stable
- **Rejecting:** Both paid and organic dropped equally
- **Potential gap explained:** ~50%

### 3. Homepage redesign reduced conversion — Priority: MEDIUM
**If** the new homepage is less clear or trustworthy, **then** homepage-to-signup conversion rate dropped for ALL traffic sources equally, **because** the new design may lack social proof or clear value proposition.
- **Deciding data:** Homepage → signup conversion rate, by traffic source, before/after
- **Source:** GA4 → Pages → Homepage → Next page flow
- **Owner:** Product/Design
- **Confirming:** All-source conversion dropped on homepage specifically
- **Rejecting:** Conversion dropped only for paid traffic (→ targeting issue, not homepage)
- **Potential gap explained:** ~40%

## Next Step

Gather data for #1 (takes 30 minutes — compare GA4 vs DB). Then #2 (segment paid vs organic in GA4). Run `mkt-root-cause` with findings.
```

---

## References

- [references/hypothesis-guide.md](references/hypothesis-guide.md) — If/Then/Because templates by problem type
