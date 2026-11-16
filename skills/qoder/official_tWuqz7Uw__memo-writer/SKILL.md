---
name: memo-writer
description: "Draft internal memos, decision docs, scope docs, and short strategy notes in the CEO's voice — structured, directive, written to persuade or align. Use when the CEO says 'write a memo on', 'draft a decision doc', 'scope doc for', 'strategy memo about', 'position paper', 'write up our thinking on', 'internal memo'. Produces a 1-3 page structured document saved to the project's deliverables folder. Runs voice calibration protocol per shared/VOICE_CALIBRATION.md with this skill's Voice Block. DOES NOT fire on 'one-pager' (that's one-pager-composer — shorter, more visual), 'board update' (board-update-composer — external audience), 'PRD' (pm-prd), 'email' (email-writer). MANDATORY TRIGGERS: memo on, decision doc, scope doc, strategy memo, position paper, write up our thinking, internal memo."
voice_block_last_refreshed: 2026-04-21
calibration_level: default
template_version: 1.0.0
---

# Memo Writer

**For:** CEOs who need to commit thinking to a shareable document — a decision rationale for the team, a scope doc that aligns a project, a strategy memo that frames a direction. Longer than an email, more structured than a Slack message, more textual than a one-pager.

## Skill Boundary

- **Use `memo-writer` for:** internal memos (team/board distribution), decision docs, scope docs, strategy notes, position papers.
- **Use `one-pager-composer` for:** shorter, more visual one-page briefs (headline + 3 key points + rec).
- **Use `board-update-composer` for:** recurring board/investor monthly or quarterly updates.
- **Use `email-writer` for:** anything that would be delivered as an email body.
- **Use `pm-prd` for:** product requirement docs with engineering spec structure.

## Writer Contract

Before writing, read `shared/WORKSPACE_API.md`.

**Primary writer for:**
- `[Project]/deliverables/memos/[YYYY-MM-DD]_[topic].docx` — final memo output.
- `[Project]/deliverables/memos/[YYYY-MM-DD]_[topic].md` — markdown source for review.
- `_hq/voice/corrections-memo-writer.jsonl` — append on correction.

**Appends to:**
- `_hq/data/events.jsonl` — event type `memo_drafted`.

**Reads only:**
- `_hq/data/entities.json`, `events.jsonl`
- Relevant `[Project]/PROJECT_CONTEXT.md` and `PROJECT_BRAIN.md` for project-specific facts
- This skill's Voice Block
- `shared/VOICE_CALIBRATION.md`
- Past memos in the project's memos folder for structural consistency

---

## What It Does

Takes a topic + audience + angle and produces a structured memo that sounds like the CEO wrote it. Handles the common memo types with appropriate structure for each.

## How It Works

### Phase 1 — Memo type detection

Parse the input to identify the memo type — each has a different structure:

**Decision memo** — "I decided X. Here's why. Here's what's next."
Structure: Decision → Context → Options considered → Rationale → Implications → Next steps

**Scope memo** — "Here's what's in, here's what's out."
Structure: Objective → In scope → Out of scope → Success criteria → Timeline → Owners

**Strategy memo** — "Here's how we should think about X."
Structure: Question → Framing → Analysis → Recommendation → Risks → Open questions

**Position paper** — "Here's my view on X."
Structure: Thesis → Evidence → Counterarguments addressed → Conclusion

**Project update memo** — "Here's where we are."
Structure: Status → What's done → What's blocked → What's next → Ask

If type is unclear, ask ONE question: "Decision, scope, strategy, position, or update memo?"

### Phase 2 — Context harvest

- `PROJECT_CONTEXT.md` of the relevant project
- `PROJECT_BRAIN.md` — facts, people, decisions history
- Last 5 events in the project from `events.jsonl`
- Any referenced prior memos

### Phase 3 — Voice-calibrated draft (two-step)

#### Step 1 — Draft

Target length by type:
- **Decision memo:** 300-600 words
- **Scope memo:** 400-800 words (scope docs need precision)
- **Strategy memo:** 600-1000 words
- **Position paper:** 500-900 words
- **Project update memo:** 250-500 words

Memos use prose in paragraphs, NOT bullets-everywhere. The CEO's voice should carry the argument. Bullets appear only where lists are genuinely appropriate (success criteria, open questions, named items).

#### Step 2 — Critique

Apply universal banned-phrase list + memo-specific critique:
- Does the opening paragraph state the thesis/decision in the first 2 sentences? If not, rewrite.
- Is there any paragraph >150 words? Break it.
- Are there bullet lists where prose would carry the argument better? Convert.
- Does the close have a clear next step or ask? If not, add.
- Voice Block structural rules enforced.

### Phase 4 — Produce .docx

Memos are typically shared as .docx. Use the `docx` skill conventions:
- Arial 11pt body
- H1 title (no number)
- H2 for section heads
- Single-spaced with 6pt after paragraphs
- No cover page for internal memos
- Header: "[Topic] — Memo — [Date]"
- Footer: page number

Also save the markdown source alongside for future regeneration and version control.

### Phase 5 — Log event + correction detection

---

## Voice Block

**Last refreshed:** 2026-04-21
**Calibration level:** default
**Sample count:** 0 (uncalibrated)

### Sentence cadence
- Typical length: 15-25 words (longer than email — memo has more room)
- Maximum before breaking: 35 words
- Short-punch frequency: occasional, especially for emphasis at paragraph starts

### Openers
- Preferred: state the thesis. "We should X." "I've decided Y." "Here's the question we need to answer."
- Avoided: "This memo outlines...", "The purpose of this memo is to...", "As we discussed..."
- Never use: "I wanted to write this memo because...", "Hope this memo finds you well"

### Vocabulary
- Uses: direct claims, specific verbs, concrete numbers
- Avoids: "leverage", "synergies", "going forward", "stakeholders" (use actual names), "ecosystem", "holistic"
- Domain-specific: domain terms of the relevant project

### Punctuation
- Em-dashes: occasional for emphasis
- Semicolons: rare but OK for paired clauses
- Parentheticals: occasional (memos tolerate more parentheticals than emails)
- Colons: acceptable before lists or definitions

### Structure
- Lead with: thesis or decision in first 2 sentences of the memo.
- Paragraph length: medium (60-120 words typical). No walls of text.
- Bullet use: reserved for lists of named items, success criteria, questions. Never for the core argument.
- Headers: H2 for major sections. H3 only if needed for a nested subsection.
- Sign-off: none — memos don't need a closing signature in most cases.

### Tone markers
- Register: formal-professional, still direct
- Self-reference: "I" and "we" both used; "I" for personal positions, "we" for collective decisions
- Hedging: moderate (memos acknowledge uncertainty better than emails do) — but commit to a position at the end
- Authority: confident. The CEO writes memos to align people; hedging undermines alignment.

### Taboos (per-skill)
- Never: "it could be argued that", "some might say", "going forward", "move the needle"
- OK despite being on universal list: "stakeholders" (if specific group is named), longer sentences than email allows

### Examples

**Example 1 — Decision memo opener:**
```
# Pricing Decision: Command Room Product Layer

We're pricing the Command Room product at $1,250 one-time, separate from
the customization tier. This memo explains why this structure beats the
alternatives and what it commits us to.

The reasoning is three-fold...
```

**Example 2 — Scope memo opener:**
```
# Chalette Customization Scope — v1

The $10K customization tier includes six specific workstreams. Anything
outside these six moves to the monthly retainer. This memo exists so
both parties — Chalette and the client — know the line before work
starts.

## In scope...
```

**Example 3 — Strategy memo close:**
```
The play isn't to be cheaper than the incumbents. The play is to be the
only option that actually calibrates to how the CEO works. That's a
moat you can't copy with features.

Next step: build the calibration service into a productized offering
by end of Q2. Everything else waits on that.
```

---

## Staleness

Same universal rules.

## Output quality bar

Memos are the highest-stakes writing skill's output — they frequently go to boards, investors, executive teams. Voice calibration at the $10K tier matters most for this skill. Uncalibrated default: ~55% quality (usable but generic). Calibrated: ~90%.
