---
name: vbn-creative-writing
description: >-
  Generates narrative content for vbn-game NPC/character JSON (biography,
  personality, appearance, timeline, VO quotes, relationships, discipline notes).
  Gothic-noir 1994 Phoenix voice; no dice/mechanical language. Use when writing
  or expanding NPC prose, VO lines, ST notes, or translating traits into behavioral
  narrative.
---
# SKILL: vbn-game NPC Creative Writing
**Version:** 1.1  
**Scope:** Styles Agent / Creative Writing System  
**Reference:** Art Bible Part XII — Creative Writing System

---

## Purpose

This skill generates narrative content for vbn-game NPC JSON records. It targets specific fields in the NPC/character template and produces prose that matches the vbn-game gothic-noir, 1994 Phoenix aesthetic — never mechanical summaries, never modern language, never dice terminology.

---

## Triggers (When to Use This Skill)

**Use this skill when the user or task involves:**
- Writing or expanding `biography`, `personality`, `appearance`, `timeline`, `backgroundDetails`, `relationships`, `quotes`, or `disciplines[].notes`
- Generating VO lines, taglines, or voice-over for a character
- Producing ST-facing narrative notes
- Translating mechanical data (traits, flaws, discipline levels) into behavioral prose
- Phrases like "write biography", "NPC backstory", "character VO", "vbn-game narrative", "1994 Phoenix prose", "gothic noir description"

**Do not use this skill for:**
- Stat generation or mechanical balance
- Database schema or JSON structure decisions
- Portrait or image prompt generation (use portrait/Part I skill)
- Full cinematic script production (use Part II / cinematic skill)

---

## Mandatory Flow

When using this skill:

1. **Read this SKILL.md fully** — especially Pre-Flight Checklist and the target field’s prompt.
2. **Run the Pre-Flight Checklist** — confirm clan, field, tone, era, MET language, metaplot.
3. **Load reference docs if needed** — Clan Voice and voice registers: [agents/style_agent/docs/Art_Bible_XII_CREATIVE_WRITING_SYSTEM__.md](agents/style_agent/docs/Art_Bible_XII_CREATIVE_WRITING_SYSTEM__.md).
4. **Fill the Master Prompt Template** (below) with character data, then use the **Field-Specific Prompt** for the target field.
5. **Run Quality Gates** on the output before delivering.

---

## Pre-Flight Checklist

Before generating any content, confirm:

- [ ] Clan identified → apply Clan Voice Guide (Art Bible XII, Section 6)
- [ ] Target field identified → apply correct voice register (Section 4)
- [ ] Tone pillar selected (Seduction / Deception / Decay / Desert Isolation / Moral Irony)
- [ ] Era locked: 1994 Phoenix. No post-1994 events, no internet, no cell phones
- [ ] MET language confirmed: no dice, no dots, no successes, no difficulties
- [ ] Metaplot filter applied: Gangrel still in Camarilla. Revised-era events haven't happened.

---

## Master Prompt Template

**Copy the block below, fill every `[bracket]` from the character/NPC data, then append the chosen Field-Specific Prompt and generate.**

```
You are writing narrative content for vbn-game, a Vampire: The Masquerade LARP 
chronicle set in 1994 Phoenix, Arizona. Gothic noir aesthetic. Desert heat. 
Pre-internet. Laws of the Night Revised (MET) system — no dice, no dot ratings.

CHARACTER:
- Name: [name]
- Clan: [clan]
- Generation: [number]
- Nature / Demeanor: [nature] / [demeanor]
- Concept: [concept]

TARGET FIELD: [field name]
VOICE REGISTER: [Tight Third-Person / Micro-Scene / Voice-Over / ST-Facing Prose]
TONE PILLAR: [Seduction / Deception / Decay / Desert Isolation / Moral Irony]

CLAN VOICE NOTE: [one sentence on this clan's voice character from the guide]

INPUT DATA:
[paste existing biography stub, trait list, discipline list, or whatever mechanical 
data you're translating — this is the source, not the output]

TASK:
[specific instruction — e.g., "Write a 4-paragraph biography" or 
"Write 3 VO quotes — one for introduction, one for threat, one for vulnerability"]

CONSTRAINTS:
- No dice rolls, dot ratings, or mechanical language in output
- No cell phones, internet, or post-1994 references  
- No direct emotional exposition — show behavior, not feeling
- No melodrama or heroic framing
- 1994 Phoenix geography must feel real and specific
- MET terminology only if mechanical context is unavoidable (ST notes only)
```

---

## Field-Specific Prompts

### Biography
```
Write a [3–6] paragraph biography for [name], a [generation]th-generation [clan].

Structure:
- Para 1: Mortal life — one image, one loss, one thing they carried into the night
- Para 2: Embrace/ghouling — who, where, why it felt wrong even then
- Para 3: The years between — what shaped them before Phoenix
- Para 4: Phoenix arrival — specific year, specific neighborhood, first impression
- Para 5–6: Current state — what they want, what they're afraid of, what they're hiding

Voice: Tight Third-Person Limited. Active verbs. Short sentences under pressure.
Anchor every paragraph to a place, a year, or a sensory detail.
Never summarize. Every paragraph is a scene, not a report.
```

---

### Timeline Entries
```
Write [N] timeline entries for [name].

Each entry format:
YEAR: [2–4 sentences. One image. One action. One emotional residue. Leave it open.]

Required entries:
- Mortal birth era (one defining moment, not a date)
- Embrace or ghouling night
- Phoenix arrival
- One defining crisis or turning point

Voice: Micro-Scene. Present tense or close past. Never resolved.
```

---

### VO Quotes
```
Write 3–5 voice-over quotes for [name].

Required mix:
- 1 introduction quote (how they enter a room, how they introduce the world)
- 1 threat quote (what they sound like when they have leverage)
- 1 vulnerability quote (the one sentence they'd never say out loud, but we hear anyway)
- Optional: 1 faction/political quote, 1 about the mortal world they've lost

Voice: First-person. Confessional. Max 2 sentences each.
Inflect with [clan] voice character.
Reflects the tension between nature ([nature]) and demeanor ([demeanor]).
```

---

### Appearance
```
Write an appearance description for [name].

Short summary (1 sentence): What registers first. Not beauty — specificity.

Detailed description (2–3 paragraphs):
- Para 1: Physical presence — height, build, how they occupy space
- Para 2: Wardrobe — specific 1994 Phoenix detail. One clan visual motif.
- Para 3: The wrong thing — what the eye catches that the mind can't quite name

Voice: Tight Third-Person Limited.
Never generic beauty descriptors. Name the specific detail that makes them memorable.
Clan motif: [reference Art Bible Part I clan visual rules]
```

---

### Background Details
```
Write narrative flavor for [name]'s backgrounds.

For each background with a rating > 0:

RESOURCES ([rating]): What does this wealth look like physically? Where does it live?
ALLIES ([rating]): Who are they? What's the unspoken cost of the relationship?
RETAINERS ([rating]): Name them. Give each one detail. They're people, not furniture.
HERD ([rating]): Where does [name] feed? What does the ritual feel like?
STATUS ([rating]): How is status held? What political fiction maintains it?
CONTACTS ([rating]): What networks? What does [name] have to give to keep them?

Voice: ST-Facing Prose or Micro-Scene depending on what fits.
Be specific. Name names, places, amounts where it creates texture.
```

---

### Relationships
```
Write relationship entries for [name]'s key relationships.

For each relationship, produce:
{
  "name": "[character name]",
  "tone": "[ally/rival/thrall/asset/threat/ghost/unknown]",
  "history": "[1–2 sentences: how they met, what it cost, what it became]",
  "hook": "[1 sentence that creates a scene if a player pulls this thread]"
}

Voice: ST-Facing Prose. Specific. Behavioral — not 'she trusts him' but 'she lets him 
stand behind her, which she does for no one else.'
```

---

### Discipline Aesthetics
```
Write aesthetic notes for [name]'s disciplines.

For each discipline:
DISCIPLINE NAME (Level [N]):
[2–3 sentences describing how this power manifests for THIS character specifically.
What does it look like? What does it sound like in the room? What do witnesses notice?
Reference: Cinematic System subtle discipline rules (Part II, Section 9).]

Never describe mechanical effects. Describe phenomenology — what is experienced.
Clan expression: [how this clan typically expresses this discipline aesthetically]
```

---

### Personality Narrative (ST-Facing)
```
Write a personality profile for [name] for Storyteller use.

Structure:
- Para 1: How they present (demeanor: [demeanor]) — the performance
- Para 2: How they actually behave (nature: [nature]) — where the mask slips
- Para 3: The gap between the two — what that tension produces in scenes

Voice: ST-Facing Prose. Direct. Name the behavior, not the feeling.
Include: what they want, what they're afraid of, what they'd sacrifice and what they won't.
```

---

## Quality Gates

Before accepting any generated content, verify:

**Tone**
- [ ] Reads like 1994 Phoenix, not generic gothic
- [ ] Supernatural is subtle, not spectacle
- [ ] Emotional truth is shown, not stated

**Language**
- [ ] Zero dice/dot/success language
- [ ] Zero post-1994 references
- [ ] No internet, cell phones, or modern tech

**Clan Voice**
- [ ] Voice register matches clan guide
- [ ] Nature/demeanor tension is present or implied

**Field Standards**
- [ ] Correct voice register used for this field
- [ ] Length appropriate to field type
- [ ] At least one Phoenix-specific anchor (place, street, year, sensory detail)

**Metaplot**
- [ ] No post-1994 VtM metaplot events referenced
- [ ] Gangrel still in Camarilla
- [ ] Giovanni, Assamite, and other clan politics reflect pre-Revised status

---

## Negative Output Rules

Reject and rewrite if output contains:

- Direct emotional exposition ("She felt grief...")
- Mechanical language ("her Manipulation is high...")  
- Generic gothic description without Phoenix specificity
- Anachronistic references (internet, cell phones, post-1994 slang)
- Melodrama or heroic framing
- Purple prose untethered from character or place
- Metaplot events that haven't happened yet
- Comedy that breaks gothic tone
- Any description of Disciplines as powers rather than experiences

---

## Reference Files

| Path | Purpose |
|---|---|
| [agents/style_agent/docs/Art_Bible_XII_CREATIVE_WRITING_SYSTEM__.md](agents/style_agent/docs/Art_Bible_XII_CREATIVE_WRITING_SYSTEM__.md) | Primary system reference (voice registers, clan voice, CWS) |
| [agents/style_agent/docs/Valley_by_Night_Art_Bible_Master_Edition.md](agents/style_agent/docs/Valley_by_Night_Art_Bible_Master_Edition.md) | Part II Cinematic System (discipline aesthetics); Part I portrait/clan visuals |
| [reference/Scenes/Character Teasers/Valley_by_Night_Cinematic_Intro_Guide.md](reference/Scenes/Character%20Teasers/Valley_by_Night_Cinematic_Intro_Guide.md) | VO format and tonal pillars |
| [reference/Books/LofNR/lotnr_lexicon.md](reference/Books/LofNR/lotnr_lexicon.md) | MET terminology reference |
| Character/NPC JSON schema in use | Target field structure (e.g. character_agent or reference JSON); no dice/dot language in output |

---
