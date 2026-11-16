---
name: pitch-writer
description: Writes personalised pitch emails to journalists for PR firm clients. Use when asked to write, draft, or improve a pitch email, media outreach, or journalist email. Triggers on "pitch", "pitch email", "media outreach", "write to journalist", "email to press". Always read the client's CLAUDE.md and journalists.md before writing. Always end with human approval flag.
---

# Pitch Writer

You write pitch emails that journalists read. Short, specific, relevant.
You never write generic pitches. Every pitch connects the story to what
that specific journalist actually covers.

Before writing, read:
1. Client CLAUDE.md — story, key messages, do-not-mention
2. Client journalists.md — who you're pitching and their beat
3. firm-knowledge/pitch-formats.md — which format to use

---

## The Cardinal Rules of Pitch Emails

1. **Under 180 words.** If it can't be said in 180 words, the story isn't clear enough yet.
2. **One story per pitch.** Never combine two announcements.
3. **Lead with why this journalist, why this story.** Show you know their beat.
4. **No attachments on first contact.** Offer to send materials if they're interested.
5. **One clear ask.** Coverage, an interview, or a call — pick one.
6. **Never send from info@ or press@.** Always from a named person.

---

## Pitch Formats by Story Type

### Format 1: News Hook (Breaking or Time-Sensitive)
Use when: Funding round, product launch, major hire, significant milestone
Best for: Tier 1 daily news outlets, wires

```
Subject: [Specific news hook] — exclusive / embargo [date if applicable]

[Journalist first name],

[Firm client] just [specific thing happened]. [The number or fact that makes it real].

This is the [first / largest / only] [relevant context for why it matters to their readers].

[One sentence on why you're coming to them specifically — their beat, a recent piece they wrote.]

Happy to send the full release + arrange a call with [Spokesperson name] before the embargo lifts.

[Your name]
[Title]
[Phone]
```

### Format 2: Exclusive Offer
Use when: You have a story worth offering exclusively to one outlet first
Best for: Tier 1 target outlets, building journalist relationships

```
Subject: Exclusive: [Story angle] — [Company name]

[Journalist first name],

I have an exclusive for you on [topic] — [one sentence on why it's a story for their readers].

[Company] is [specific thing] — [the number or fact]. [One sentence of context].

You'd have the story until [date/time]. Happy to arrange an interview with [Spokesperson].

Worth a conversation?

[Your name]
```

### Format 3: Feature Angle
Use when: No hard news — pitching a trend story, profile, or thought leadership piece
Best for: Magazines, features desks, long-lead publications

```
Subject: [Trend or angle] — source for your [beat] coverage

[Journalist first name],

[Reference a specific recent piece they wrote or topic they cover.]

[One sentence connecting that angle to your client's story or expertise.]

[Client name]'s [specific experience or data point] might be useful background
for a feature on [topic]. [Spokesperson name] has [specific credential or insight
that's relevant to the story].

No announcement — just flagging if you're working on anything in this space.

[Your name]
```

### Format 4: Data / Research Lead
Use when: Client has proprietary data, survey results, or research findings
Best for: Data-driven journalists, trade press, business press

```
Subject: Data: [Specific finding] — [Client name] research

[Journalist first name],

[Client name] surveyed [N] [audience] and found [specific, surprising finding].

[One sentence on why this matters to their readers or challenges a common assumption.]

Full dataset available. [Spokesperson name] available to discuss methodology and findings.

[Your name]
```

---

## Personalisation Rules (Ranked by Value)

**Level 1 — Reference their specific work (highest value)**
"Your piece on [topic] from [month] — specifically [specific point they made]
— is what made me think of you for this."

**Level 2 — Reference their beat accurately**
"You cover [specific beat], and this is the first time [specific thing relevant to that beat]."

**Level 3 — Reference recent relevant coverage**
"You've covered [company or trend] before — this follows directly from that story."

**Level 4 — Relevance by outlet/audience**
"[Outlet]'s readers skew [description], and this is directly relevant to [specific reason]."

Never use: Generic compliments ("Love your work!"), vague beat references ("you cover tech"),
or flattery that makes it obvious you haven't read them.

---

## Subject Line Rules

- Under 50 characters
- Specific: "Acme raises $40M" not "Exciting news from Acme"
- State the format if relevant: "Exclusive:", "Data:", "Embargo [date]:"
- No clickbait, no all caps, no exclamation marks

**Good subject lines:**
- "Exclusive: Acme raises $40M — available before Thursday"
- "Data: 67% of CFOs plan to cut SaaS spend in Q2"
- "Source: fintech consolidation trend — Beacon COO available"

**Bad subject lines:**
- "EXCITING NEWS FROM ACME CORP!!!"
- "Quick question for you"
- "Press release attached"

---

## Tiering the Pitch List

Always produce three pitch variants when pitching the same story:

**Tier 1 — Top target (Exclusive or first-look offer)**
- Personalised to that specific journalist
- Exclusive offer or embargo date
- Direct offer of spokesperson interview

**Tier 2 — Standard outreach (Personalised by beat)**
- Personalised to their beat and recent coverage
- Standard timing (no exclusive)
- Offer to send materials

**Tier 3 — Trade press (Sector relevance)**
- Shorter, more direct
- Lead with sector relevance, not the announcement
- Offer to send full release

---

## MCP-Enhanced Personalisation (When Reporter MCP Available)

When the `reporter` MCP server is connected, enhance personalisation with live data
before writing each pitch:

### Fresh Article References
- Call `get_recent_articles` for each target journalist (last 90 days, topic filtered to client's sector)
- Use the most relevant returned article for Level 1 personalisation — reference their specific recent work
- This replaces reliance on the static articles in journalists.md, which may be stale

### Data-Driven Angle Matching
- Call `find_pitch_angles` with the journalist name, story summary, and client key messages
- The tool returns a recommended angle based on what the journalist actually covers
- Use the recommended angle to shape the pitch opener, not a generic beat reference

### Pitch Timing
- Call `analyze_pitch_timing` for each Tier 1 journalist
- Include the recommended send window in the delivery notes (e.g., "Pitch Tuesday AM — Jordan publishes Wednesdays")

### Personalisation Verification
- If a pitch references a specific article, verify it exists via `get_recent_articles`
- Flag any personalisation reference older than 6 months as stale — find a fresher one

### If MCP Is Not Available
Write pitches using articles and angles from journalists.md as usual.
Add a note: "Personalisation based on cached journalist data — verify articles are still current."

---

## Before Delivering

Check:
- [ ] Under 180 words per pitch
- [ ] Personalisation references something specific to each journalist
- [ ] Subject line is under 50 characters and specific
- [ ] Spokesperson named matches client CLAUDE.md approved list
- [ ] No claims not in the approved release or client CLAUDE.md
- [ ] Do-not-mention items absent
- [ ] Three variants produced (Tier 1, Tier 2, Trade)

End every pitch batch with:

---
⚠️ AWAITING HUMAN APPROVAL — DO NOT DISTRIBUTE
Review each pitch above. Personalise further where needed.
Send from your own email client — not from this system.
