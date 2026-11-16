---
name: voice-audit
description: "Post-draft diagnostic for sermon and book writing. Scans for machine tells, assesses authenticity risk, checks voice continuity against the author's sermon corpus. Fires after writing is complete or when reviewing existing drafts. For during-writing standards, see like-a-human."
---

# Voice Audit — Post-Draft Diagnostics

*Fires after writing. Evaluates what was produced.*

**Relationship to other guardrails:**
- **like-a-human** shapes the *writing* — voice markers, rhythms, vocabulary, theological precision.
- **voice-audit** reviews the *output* — scanning for drift, flagging machine tells, assessing authenticity.
- **careful-not-clever** guards the *content* — verified Scripture, real quotes, grounded theology.

When drift is detected, the response is **restoration, not rewriting.** A few targeted edits to bring the prose back to the author's voice — not a wholesale rewrite that introduces new machine patterns.

---

## Machine Tell Scan

Run this scan against any draft that has been written or edited with AI assistance. These are the specific fingerprints AI leaves.

### Structural tells
- [ ] Uniform sentence length throughout — mid-length sentences with no spikes or drops
- [ ] Paragraph template loops: thesis line → 2-3 supports → tidy restatement, repeated section after section
- [ ] Visible symmetry: every section the same length, every list the same number of items
- [ ] The sandwich: intro promises what it will say, body says it, conclusion summarizes what it said

### Transition tells
- [ ] "Moreover," "Furthermore," "Additionally," "It's worth noting," "In conclusion," "In today's world," "At its core," "In essence," "Let's dive in"
- [ ] Any transition smoother than a gear grind — this voice uses hard pivots: "Now —" "And then Paul pivots." "But here's the thing."

### Word-level tells
- [ ] Hedging stacks: "It's important to note that," "One might argue," "It's worth considering," "It seems like," "Perhaps"
- [ ] Adverb inflation: "truly remarkable," "deeply profound," "incredibly powerful"
- [ ] Decorative adverbs: quietly, deeply, fundamentally, remarkably, arguably, certainly, really, just, literally, genuinely, honestly, simply, actually — cut unless the adverb does work the verb cannot do alone
- [ ] Thesaurus syndrome: three words where one would do
- [ ] Synonym cycling: rotating synonyms for the same referent ("the passage... the text... the pericope... the section") instead of repeating the word or using "it"
- [ ] AI-overrepresented vocabulary:
  - **Hard ban**: *delve, tapestry, landscape (abstract), leveraging, framework, holistic, unpack, resonate, garner, showcase (verb), underscore (verb), encompass, nestled, enduring, featuring, boasts, elevate, facilitate, instrumental, bolstered, spearheading, exemplify, cultivate (figurative), highlight (verb)*
  - **Soft ban** (only when plainly the right word): *robust, comprehensive, pivotal, multifaceted, foster, navigate, crucial, vital, significant, enhance, profound, innovative, realm, narrative, nuanced*
  - **Do not flag**: *sovereign, holy, righteous, justified, sanctified, propitiation, omniscience, nuanced* — confirmed author vocabulary (seminary-trained; verified March 2026)
- [ ] Copula avoidance: "serves as," "stands as," "represents," "constitutes," "marks," "features," "offers" — replace with "is," "are," "has"
- [ ] Vague moral swaps: "brokenness" for sin, "issues" for wrath, "challenges" for idolatry, "struggles" for repentance, "disconnect" for judgment, "fresh start" for justification, "realign" for repent

### Rhythm tells
- [ ] Even sentence length from start to finish
- [ ] Fragment stacking every time emphasis is needed (occasional = human; constant = machine)
- [ ] False variation: complex/simple alternation in a mechanical pattern
- [ ] Syntactic template repetition: three or more consecutive sentences with the same grammatical structure (S-V-O, S-V-O, S-V-O)
- [ ] Rule of three: do all lists happen to have three items? AI defaults to triads. Let the text determine the grouping.

### Substance tells
- [ ] Everything important, nothing specific: "This powerful passage reveals deep truths about the human condition"
- [ ] Interchangeable illustrations that could be swapped into any other sermon
- [ ] Correct but bloodless exposition: text explained, sinner never cornered, heart never pierced
- [ ] No rough edges: every paragraph resolves cleanly, every transition is smooth
- [ ] Comfort arrives before conviction has had time to land
- [ ] -ing tailing: sentences ending with participial editorializing ("reflecting broader trends," "highlighting its importance," "underscoring the significance"). Cut the -ing clause or make it its own sentence.
- [ ] False ranges: "from X to Y" where X and Y are not on a meaningful scale
- [ ] Assembled terminology: theological terms stacked without showing what they mean for the person in the pew
- [ ] Dead metaphor: one metaphor used more than twice across the sermon — use it once at its pressure point, then move on
- [ ] One-point dilution: the same argument restated multiple times without adding depth or evidence
- [ ] Synthetic earnestness: "But here's the truth:" / "Perhaps the most striking thing is..." followed by a restatement, not new content. Distinguish from genuine gear-shifts by checking what follows.

### Seam detection
- [ ] One or more paragraphs shift to a more abstract, polished, or consultant-like register while the rest sounds like the preacher
- [ ] Paragraphs whose sentences all open the same way when the author's pattern uses varied openings
- [ ] A section that feels "inserted" rather than grown from the surrounding argument

### Announcement-before-move scan
Search for sentences that narrate what the next sentence is about to do instead of making the move directly. These are throat-clearing sentences that pad the transitions.

**Grep pattern** (run against the manuscript):
```
"I need to tell you|I want to tell you|I have to tell you|Let me tell you|Let me show you|Let me read you|Let me be clear|Let me push back|I want to say something|I need to say|I want you to (see|hear|feel|know|notice|understand)|I need you to (see|hear|feel|know|notice|understand)|And I'll tell you what|Hear me on .* because"
```

- [ ] Every hit is a presumptive flag
- [ ] For each hit, ask: does this sentence announce a move, or make a move?
- [ ] If announce — cut the sentence and start with the content
- **Threshold:** Zero hits is the target. One or two in a sermon of 5,000+ words is acceptable if the sentence is doing genuine pastoral work. More than three means the draft is leaning on announcements instead of turns.

### Image-density scan
Count images, metaphors, and surprise phrases per paragraph in the application and climactic sections.

- [ ] Zero images per paragraph — voice may be flat
- [ ] One image per paragraph — sharp, keep it
- [ ] Two images per paragraph — borderline, verify each does distinct work
- [ ] Three or more images per paragraph — over-imagery, cut the most clever one and keep the most concrete
- **Test:** If two images name the same thing, keep the more concrete one. The concrete image is what a person in the room writes. The abstract image is what a machine writes to sound like one.

### Assumed-familiarity scan
Search for claims about what the congregation has heard, remembers, or has been taught. Every hit must be verified against sermon-map or date-map.

**Grep pattern** (run against the manuscript):
```
"many of you know|many of you remember|you know this|some of you remember|we preached|we spent|we talked about|as I've said|you've heard me|when we were in|you all know|thirty-nine weeks|[0-9]+ weeks"
```

- [ ] Every hit must be verified: does the referenced sermon exist, and did it actually develop the specific point being claimed?
- [ ] If the sermon exists but didn't develop the claimed angle — rewrite to cite the passage directly without claiming shared memory
- [ ] If the claim cannot be verified — cut it
- **Default:** *"Psalm 42"* works as well as *"When we preached Psalm 42."* Congregation-history references are ornamental. When in doubt, leave them out.

---

## Voice Continuity Check

Compare the draft against the author's existing sermon corpus. The baseline voice (established in Romans 13b through Romans 15a and the thief on the cross sermon) has these markers:

### Must be present
- **Compressed declarative chains:** "Same crimes. Same sentence. Same nails. Same slow suffocation."
- **Antithetical parallelism:** "Not correction. Not condescension. Not rolling our eyes… We owe them *weight-bearing*." **Cap: 1-2 per sermon.** If more than 2 instances appear, flag the weakest and cut it. This pattern earns force by being rare.
- **Text-first orbit:** Quote → unpack → re-quote. The prose doesn't leave the passage for long.
- **Gear-shift markers:** "Now —" "Hear me:" "And here's the thing:" "Let me say this gently:"
- **Direct pastoral address:** "Some of you..." tied to concrete, plausible lives — the addict, the estranged parent, the diagnosis, the war-zone marriage.
- **Shrinking sentences at climax:** "Today. With me. Paradise." "Cast it off."
- **Pause-and-pivot after intensity:** "Something else was happening. Someone was opening his eyes."
- **The refrain:** "The night is far gone. The day is at hand." woven organically.

### Must be absent
- Stacked intensifier adverbs
- AI-overrepresented vocabulary (see Machine Tell Scan)
- "Moreover / Furthermore / In conclusion" transitions
- Road-map paragraphs that announce what's coming
- Hedged assertions where the text speaks declaratively
- Therapeutic vocabulary substituting for biblical terms

### Drift indicators
If three or more of the "must be present" markers are missing, or two or more of the "must be absent" items appear, the draft has drifted from the author's voice. Flag specific locations and suggest minimal restoration edits.

---

## Structural Continuity Check

Voice Continuity (above) checks sentence-level markers. This check
covers the *liturgical structure* of the sermon — recurring elements
that anchor the voice across sermons even when the prose markers are
all in place. Confirmed by manuscript audit of seven older sermons
(Eph 2, Gen 1-2, Jonah 4, Luke 15, Titus 1, Psalm 51, Missions and
Hell). See `like-a-human` Native moves section for the source.

### Special-occasion exception (apply first)

Before running the regular check, identify whether the sermon is
occasion-specific. The "Must be present" list below describes
**Sunday morning exposition**. Special-occasion sermons follow
different liturgical shapes and the regular structural list is
suspended for them.

Recognized special occasions:

- **Easter / Resurrection Sunday** — resurrection-focused close,
  often pivots through a marker like *"That's what Easter is all
  about."*
- **Christmas / Advent** — incarnation focus, often interleaved with
  carols and readings.
- **Funerals, weddings, baptisms** — service shape comes from the
  occasion itself.
- **VBS Sunday, communion-only services, holiday-tied sermons**
  (Thanksgiving, Memorial Day, etc.) — the surrounding service
  element drives the shape.

For these sermons, audit instead by asking:

- Does the sermon honor the occasion frame? (Easter ends on the
  resurrection; Christmas on the incarnation; funeral on the gospel
  for the bereaved.)
- Is the gospel still present in some form? Even on Easter the call
  is present, just resurrection-shaped rather than the standard
  invitational cluster.
- Voice Continuity Check (above) still applies — sentence-level
  markers don't get a pass for the occasion.

**Two markers should still appear even on special occasions**,
because they are voice-signature rather than liturgical-frame:

- At least one congregational engagement marker
- A translation move if a technical term is introduced

**Drift flag (occasion-mismatch):** If a regular Sunday sermon shows
the absences characteristic of a special occasion (no people group,
no Bible cue, no closing cluster) but does *not* identify itself as
a special occasion in its own text, that is real drift, not
exception. Flag.

---

### Must be present

- **A current-events or fresh-observation opening.** A recent news
  story, cultural moment, or personal observation locates the sermon
  in the room's actual week. If the sermon opens with a doctrinal
  abstract instead, flag.
- **A Bible-handling cue in invitational register.** Some form of
  *"If you have a Bible, and I hope you have…"* / *"While you're
  turning there…"* / *"Open with me to…"* before the main text. If
  absent, the opening has been smoothed.
- **The People Group of the Week paragraph.** Named unreached group,
  one short cultural/historical context paragraph, three to four
  specific prayer requests. Position: between the opening cue and
  the main exposition. If missing, flag — this is liturgical
  signature, not optional ornament.
- **At least one congregational engagement marker.** *"Amen?"*,
  *"Say it with me"*, *"Take out a pen"*, *"Don't raise your hand,
  but…"*, or equivalent. If the entire sermon expects silent
  listening, the voice has drifted toward lecture.
- **An invitational gospel-call cluster at the close.** Multiple
  doors open: gospel call, rededication, membership, baptism, altar
  opening, prayer for the persecuted Church, communion. The exact
  template should vary; the cluster shape should not.
- **A translation move at least once.** After a technical
  theological term, a plain-English gloss flagged with a tag
  (*"fancy way of saying…"*, *"five-dollar word"*, *"that is, …"*).
  If the doctrinal vocabulary stays untranslated, the voice has
  drifted toward seminary register.

### Drift indicators

- If the sermon lacks the current-events opening *and* the Bible
  cue, the opening has been over-written.
- If the People Group of the Week is missing, flag immediately —
  this is the most reliable structural signature and has appeared
  in every audited sermon.
- If the gospel-call closing is *the same four-clause "If X, come
  talk to me" template* as the previous sermon, flag for variation.
  The cluster is native; the exact template is overuse (cf.
  `like-a-human` Voice-audit findings).
- If congregational engagement markers are absent across an entire
  sermon, the voice has drifted toward lecture and needs at least
  one restored.

### Restoration

Most missing structural elements can be restored with a short
insertion at the canonical position. Don't expand the rest of the
sermon to "balance" — the pre-existing prose is already calibrated.

---

## Conviction Check

For each major movement of the sermon, ask:

1. **What sin or unbelief is this confronting?** If the answer is only "we're all broken / busy / distracted," conviction has been flattened. Replace with text-shaped names.

2. **Is there a clear call?** Repent, come, confess, forgive, flee, put on, cast off. If a section only explains but never summons, it has lost its edge.

3. **Is there direct pastoral address?** At least once per major movement, the sermon should look at someone specific: "Some of you who..." If "we" is doing all the work, conviction has been averaged out.

4. **Has the conditional voice crept in?** Scan for "might," "could," "may," "tends to" where the author would say "is," "does," "will." Keep conditionals only where the text itself frames hypotheticals.

5. **Does comfort arrive too early?** The law should have time to land before the gospel relieves it. If conviction and comfort share a paragraph, the tension has been collapsed.

---

## Cadence Check

Identify the 1-2 moments in the sermon that should be the hottest points. At those spots, check:

1. **Are sentences actually shorter?** If the climax has the same sentence length as the setup, it has been flattened.

2. **Is there anaphora or antithesis?** "He didn't... He didn't... He didn't..." or "Not... Not... Not... But..." If absent at key moments, the author's native rhythm has been smoothed.

3. **Is there a pause-and-pivot?** After the peak, does one quiet sentence pull the room close? If the high moment rolls straight into explanation, a native move has been lost.

4. **Do gear-shift markers appear?** "Now —" "Hear me:" before or after key transitions? If not, the draft reads like an essay, not a sermon.

5. **Does the breath test pass?** Can each paragraph be read aloud in one or two breaths? If not, it was built for silent reading, not preaching.

---

## Doctrinal Sharpness Check

1. **Biblical vocabulary present?** Where the text says sin, wrath, judgment, repentance, justification, adoption, sanctification — are those words on the page? Or have they been swapped for therapeutic equivalents?

2. **Contrasts drawn?** For every key doctrinal statement, is there a "not... but..." antithesis? If you can't form one, the doctrine may be too vague.

3. **TED talk test.** Take the biggest claim in the sermon. Could it be the centerpiece of a secular leadership talk with zero offense? If yes, either anchor it explicitly to the text or replace it with something that cannot survive outside the world of Romans, cross, resurrection, judgment.

4. **Corporate retreat test.** Could a paragraph be read unchanged at a corporate retreat with nods and no discomfort? If yes, it has been flattened.

5. **Text tethering.** For every doctrinal claim, is there a clear "Look at verse..." or a direct quotation? If doctrine floats free of the passage, pull it back.

---

## Authenticity Risk Assessment

After completing all checks, assign an overall rating:

**Authenticity Risk: Low / Medium / High**

Evaluate based on:
- Machine tell density (how many items flagged in the scan)
- Voice continuity (how many markers are present/absent)
- Conviction integrity (does the sermon corner and summon, or only explain?)
- Cadence integrity (does the sermon build and breathe, or flatline?)
- Doctrinal precision (sharp biblical words or vague therapeutic ones?)
- Sermonic cliché density ("friends," "beloved," "here's the thing")
- Emotional register accuracy (does anger sound like anger, or like disappointment?)

**High risk if:**
- More than 5 machine tells flagged
- Three or more voice markers missing
- No direct pastoral address in the entire sermon
- Climactic moments have the same sentence length as setup
- Biblical terms consistently replaced with therapeutic language
- The piece has no seams — no place where the author changed direction or left a tension unresolved
- The prose could survive in a secular context with no Bible reference

**Output:** Flag specific locations. Suggest 3-5 minimal restoration edits. Do not rewrite the sermon. Restore the voice.

*This assessment is internal and never published.*
