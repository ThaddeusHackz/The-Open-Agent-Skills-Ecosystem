---
name: slack-writer
description: "Draft Slack messages, thread replies, and announcements in the CEO's voice — terser register than email, less formal structure. Use when the CEO says 'send a slack', 'slack [person]', 'post in [channel]', 'draft a slack message', 'reply in the thread', 'announce in [channel]', 'dm [name]'. Produces a ready-to-post message. Runs voice calibration protocol per shared/VOICE_CALIBRATION.md with this skill's Voice Block. DOES NOT fire on 'draft an email' (email-writer), 'write a memo' (memo-writer), 'post to LinkedIn' (linkedin-writer if installed). MANDATORY TRIGGERS: send a slack, slack [person], post in [channel], dm [name], reply in the thread, announce."
voice_block_last_refreshed: 2026-04-21
calibration_level: default
template_version: 1.0.0
---

# Slack Writer

**For:** CEOs who live in Slack and want drafts that sound like them, not like a helpful AI. Slack voice is fundamentally different from email voice — shorter, more casual, uses different conventions.

## Skill Boundary

- **Use `slack-writer` for:** Slack DMs, channel messages, thread replies, announcements.
- **Use `email-writer` for:** anything in email.
- **Use `follow-up-ritual` for:** post-meeting follow-ups even if delivered via Slack (it routes to the right format).

## Writer Contract

Before writing, read `shared/WORKSPACE_API.md`.

**Primary writer for:**
- `[Project]/deliverables/slack_drafts/[YYYY-MM-DD]_[channel-or-recipient]_[topic].md`
- `_hq/voice/corrections-slack-writer.jsonl`

**Appends to:**
- `_hq/data/events.jsonl` — event type `slack_drafted`.

**Reads only:**
- `_hq/data/entities.json`
- `_hq/data/events.jsonl` (prior Slack threads)
- This skill's Voice Block
- `shared/VOICE_CALIBRATION.md`

---

## What It Does

Takes "dm Bailey about moving the call to Thursday" and produces a 2-sentence Slack message in the CEO's voice. Accounts for channel context (public vs. DM, formality level, recent thread content).

## How It Works

### Phase 1 — Input parsing

Accept:
1. **DM instruction:** "DM Bailey about the Thursday call."
2. **Channel post:** "Post in #team about the new client."
3. **Thread reply:** "Reply in the Daniel thread that we'll send by EOD."
4. **Announcement:** "Announce in #all-hands that Sarah joined Acme."

Resolve channels against Slack connector if available. If the channel name is ambiguous, ask once.

### Phase 2 — Context load

- Recipient/channel from `entities.json` / Slack connector
- Last 3-5 messages in the thread/channel for register matching
- Recent interaction history

Channel-type-aware register:
- **DM to close peer:** casual, possibly fragmentary, contractions OK
- **DM to external/newer contact:** still casual but more complete sentences
- **#team channel:** internal voice, terse, emojis OK if the CEO's samples use them
- **#all-hands:** slightly more polished, still short
- **Thread reply:** matches the register of the thread's existing messages

### Phase 3 — Voice-calibrated draft

#### Step 1 — Draft

Target length for Slack is dramatically shorter than email:
- **DM:** 5-25 words typical, max 40
- **Channel message:** 10-40 words, max 60
- **Thread reply:** 5-30 words
- **Announcement:** 30-80 words, can use light formatting (bold, bullets)

Slack-specific Voice Block rules apply (see below). These allow constructions email does not — sentence fragments, lowercase starts if that's the CEO's style, emoji.

#### Step 2 — Critique

Apply universal banned-phrase list + Slack-specific critique:
- Is it too long? Slack readers scan — cut 30% on any draft over 50 words.
- Does it open with filler? Strip it.
- Is the register matching the channel's baseline tone?
- Are there email-isms that don't belong in Slack? ("Best regards" → delete. "Hi [name]" in a DM → usually delete.)

### Phase 4 — Save + present

Save to drafts folder. Present inline with "post, edit, or save?"

### Phase 5 — Log event + correction capture

---

## Voice Block

**Last refreshed:** 2026-04-21
**Calibration level:** default
**Sample count:** 0 (uncalibrated)

### Sentence cadence
- Typical length: 6-15 words
- Fragment OK: yes (Slack convention)
- Short-punch frequency: common

### Openers
- Preferred: get to the point immediately. No greeting in DMs to peers. "Hey [name]" acceptable for less-frequent contacts.
- Avoided: "I hope you're doing well", "Just wanted to reach out", "Hi team,"
- Never use: "Happy to help", "Great question", "I wanted to circle back"

### Vocabulary
- Uses: contractions (we're, I'll, don't, it's), abbreviations (fyi, fwiw, tbh, lmk — but sparingly at default), direct verbs
- Avoids: corporate hedging, formal sign-offs
- Emoji: acceptable for ✅ ❌ 👍 🎯 — at default calibration, used sparingly

### Punctuation
- Em-dashes: occasional
- Ellipses: rare (gives wrong tone)
- Exclamation marks: rare — never more than one per message
- Line breaks: liberal — Slack rewards visual breathing room over dense prose

### Structure
- Lead with: the thing. No windup.
- Length discipline: if the message is over 3 lines, consider whether it should be an email instead.
- Bullet use: acceptable for announcements with 3+ items. Rare in DMs.
- Sign-off: none in DMs. Occasional "—M" in channel posts.

### Tone markers
- Register: casual-professional, efficient
- Hedging: minimal
- Humor: allowed if CEO's samples show it (default: none)

### Taboos (per-skill)
- Never: "please let me know if", "feel free to", "hope this helps", "circling back", "touching base"
- OK despite being on universal list: sentence fragments, lowercase starts, "fyi"

### Examples

**Example 1 — DM to peer:**
```
pushing LOI to tuesday 2pm, cool?
```

**Example 2 — Channel message:**
```
Daniel spec v2.7.1 shipped. Amendments docx in the deliverables folder.
Building out the skill updates next.
```

**Example 3 — Announcement:**
```
Team — Sarah is joining Acme starting Monday. She'll own GTM.

Reach out to introduce yourselves this week. Intro email thread coming
Friday.
```

**Example 4 — Thread reply:**
```
yep. EOD friday works.
```

---

## Staleness

Same rules as universal. Emit notice if stale.

## Connector-aware behavior

If Slack connector is authorized, "post it" dispatches directly. Channel and recipient resolved against Slack workspace. Otherwise, output for copy-paste.
