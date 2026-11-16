---
name: mkt-content-create
description: This skill should be used when the user asks to "create content", "write a content brief", "make content for", "create platform-native content", "create social post", "write content from IMC plan", or mentions content creation, creative briefs, or platform-native content. For copy polish/headlines, use mkt-copywriting instead.
license: MIT
metadata:
  author: hungv47
  version: "2.1.0"
---

# Content Creation

*Communicate Track — Step 3 of 4. Turns IMC angles into production-ready content with A/B variants.*

## Inputs Required
- Angle + channel from `.agents/mkt/imc-plan.md` (or user-provided)

## Output
- `.agents/mkt/content/[slug].md`

## Quality Gate
Before delivering, verify:
- [ ] Hook communicable in ≤8 words (if you can't summarize what it says in 8 words, it's too complex)
- [ ] Hook passes 3-question test: visual? falsifiable? uniquely yours?
- [ ] CTA follows formula: [action verb] + [what they get] (not "Learn More" or "Click Here")
- [ ] A/B variant changes exactly ONE element — and hypothesis states what you'd learn if B wins

## Chain Position
Previous: `mkt-imc` | Next: `mkt-attribution`

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If available, read for product details and accuracy.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `imc-plan.md` | mkt-imc | **INTERVIEW.** Ask: angle, channel, placement, awareness stage. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `icp-research.md` | mkt-icp-research | VoC language for copy |
| `product-context.md` | mkt-copywriting | Product details for accuracy |

Read `.agents/mkt/imc-plan.md` if it exists — pull angle, hook type, awareness stage, channel. If it doesn't exist, interview:
1. "What angle are we creating content for?"
2. "What channel and placement?"
3. "What awareness stage is the audience at?"

**WebSearch directive:** Before writing, verify current platform specs: `"[platform] [format] specs [year]"` (e.g., "LinkedIn carousel specs 2026"). See [references/platform-specs.md](references/platform-specs.md) for baseline reference.

---

## Step 1: Write the Hook

The hook stops the scroll. Write the exact text.

| Hook Type | Pattern | Example |
|-----------|---------|---------|
| Question | "Have you ever [relatable]?" | "Have you ever spent more time reporting than doing?" |
| Bold claim | "[Controversial statement]" | "Your meetings problem isn't meetings." |
| How-to | "How to [outcome] without [sacrifice]" | "How to ship 2x faster without hiring" |
| Story | "I [action] and [surprise]" | "I cut meetings 80%. Output doubled." |
| Data | "[Surprising stat]" | "31 hours/month in unproductive meetings" |
| Contrarian | "Stop [common advice]" | "Stop tracking velocity." |

**Test the hook:** Run it through the 3-question test. If any answer is no, rewrite before continuing.

---

## Step 2: Write the Body

Write the ACTUAL copy — not an outline, not a description.

**Video:** Timestamped script with text-on-screen, voiceover, and visual direction.
**Static post:** Complete caption, every word.
**Carousel:** Every slide, cover to CTA.
**Thread:** Every post, numbered.

---

## Step 3: Write the CTA

| Stage | Pattern | Example |
|-------|---------|---------|
| Unaware | Discover | "See why this matters →" |
| Problem Aware | Explore | "Discover the fix →" |
| Solution Aware | Compare | "See how we're different →" |
| Product Aware | Try | "Start free trial →" |
| Most Aware | Act | "Start now — first month free →" |

Include: exact CTA text, destination, tracking parameters.

---

## Step 4: A/B Variant

Create variant B that changes exactly ONE element:

| What to Test | When | What You Learn if B Wins |
|-------------|------|------------------------|
| Hook | Default — always test the hook first | Audience responds more to [B's approach] than [A's] |
| CTA | Hook is strong, conversion is weak | [B's framing] reduces friction better |
| Format | Engagement is low despite good hook | Audience prefers [B's format] on this platform |
| Angle framing | Testing different emotional entry points | [B's emotion] resonates more than [A's] |

---

## Step 5: Asset Checklist

What the production team needs. Be specific about dimensions, formats, and brand assets.

---

## Artifact Template

```markdown
---
skill: mkt-content-create
version: 1
date: [today's date]
status: draft
---

# Content: [Title]

**Date:** [today]
**Skill:** mkt-content-create
**Angle:** [from IMC plan]
**Channel:** [platform + placement]
**Stage:** [awareness level]

## Hook

[Exact hook text]

**3Q Test:** Visual: [Y/N] | Falsifiable: [Y/N] | Uniquely ours: [Y/N]

## Body

[Complete copy — every word, slide, or timestamp]

## CTA

- **Text:** [exact CTA copy]
- **Destination:** [URL or action]
- **Tracking:** [UTM parameters]

## A/B Variant

| Element | A (Main) | B (Variant) |
|---------|----------|-------------|
| [Hook/CTA/Format] | [Original] | [One change] |

**Test hypothesis:** If B wins, it means [specific learning about the audience].

## Asset Checklist

- [ ] [Asset with specs]
- [ ] [Asset with specs]
- [ ] [Brand assets needed]

> On re-run: rename existing artifact to `[slug].v[N].md` and create new with incremented version.
```

---

## Worked Example

```markdown
# Content: Status Update Waste — LinkedIn Carousel

**Date:** 2026-03-13
**Skill:** mkt-content-create
**Angle:** "Engineering teams lose 12 hrs/week to status updates nobody reads"
**Channel:** LinkedIn carousel, @brand
**Stage:** Problem Aware

## Hook

"Your team loses 12 hours a week to status updates nobody reads."

**3Q Test:** Visual: Y (12 hours, status updates) | Falsifiable: Y (12 is a specific, checkable number) | Uniquely ours: Y (cites our research data)

## Body

- Slide 1: "Your team loses 12 hours a week to status updates nobody reads."
- Slide 2: "Here's where those hours go:" [pie chart visual]
- Slide 3: "4 hrs — writing updates for managers who skim them"
- Slide 4: "3 hrs — standups where 8 people wait to give 30-second updates"
- Slide 5: "3 hrs — switching between tools to piece together who's doing what"
- Slide 6: "2 hrs — 'quick syncs' that could have been a dashboard"
- Slide 7: "The fix isn't better updates. It's fewer updates with better visibility."
- Slide 8: CTA slide

## CTA

- **Text:** "See how teams ship without status theater →"
- **Destination:** /product/visibility
- **Tracking:** utm_source=linkedin&utm_medium=organic&utm_campaign=status-waste&utm_content=carousel-v1

## A/B Variant

| Element | A (Main) | B (Variant) |
|---------|----------|-------------|
| Hook | "Your team loses 12 hrs/week..." (Data) | "I stopped doing standups. Here's what happened." (Story) |

**Test hypothesis:** If B wins, our audience responds more to personal narrative than statistics on LinkedIn.

## Asset Checklist

- [ ] 8 slides, 1080×1350px (LinkedIn carousel format)
- [ ] Slide 2: pie chart showing hour breakdown
- [ ] Brand fonts + colors applied to all slides
- [ ] Logo on slides 1 and 8
```

---

## References

- [references/examples.md](references/examples.md) — Complete worked examples with full copy
- [references/platform-specs.md](references/platform-specs.md) — Platform dimensions, limits, native patterns
