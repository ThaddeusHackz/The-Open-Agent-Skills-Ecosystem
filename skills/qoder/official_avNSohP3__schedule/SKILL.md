---
name: schedule
description: Find free time on your calendar and schedule meetings. Queries availability across calendars, scores flexibility of existing meetings, and suggests optimal slots. Use when the user says "find time with [person]", "schedule a meeting", "when am I free", or "find a slot".
---

# Schedule

Find open time on your calendar, check availability across multiple people, and schedule meetings. Handles the full flow: check calendars → score conflicts → suggest slots → create event.

## Connectors

| Connector | Required | Purpose |
|-----------|----------|---------|
| [Google Workspace](../../guides/connectors.md#google-workspace) | Yes | Google Calendar (read events, check free/busy, create events), Contacts (look up attendees) |

Examples below show `gws` CLI syntax, but the workflow works with any Google Workspace connector. Claude will adapt the API calls for your setup.

## Configuration

> Load `config.md` for calendar IDs and preferences. Load `env.md` for shared values.

Edit `config.md` with your calendar IDs, timezone, and scheduling preferences.

## Modes

| User says | What happens |
|-----------|-------------|
| "When am I free Tuesday?" | Check your calendars, show open slots |
| "Find time with Sarah" | Check both calendars, suggest mutual availability |
| "Schedule a 30min with the team" | Find slot → suggest → create event with invite |

## How This Works

### Finding Free Time (Personal)

Query all your calendars for the requested time range. Filter to working hours, round to clean :00/:30 boundaries, drop slots shorter than 30 minutes.

**Output two formats depending on context:**

Readable summary (default):
```
You're pretty open Wednesday afternoon. Biggest blocks:
- Tuesday: 10–11:30am, 2–4pm
- Wednesday: all afternoon (1–5pm)
- Thursday: 9–10am only
```

Paste-ready format (when the user needs something to send):
```
All times [TZ]
- Tue 3/31: 10–11:30a | 2–4p
- Wed 4/1: 1–5p
- Thu 4/2: 9–10a
```

### Scheduling With Others

**Step 1: Confirm what you're looking for.** Echo back: attendees, duration (default 30 min), time range (default next 5 business days). Wait for confirmation before any lookups.

**Step 2: Resolve attendees.** Look up email addresses via contacts. If not found, ask. Run lookups in parallel.

**Step 3: Query calendars in parallel.** One query per person, all at once. Use events list for full details (needed for flexibility scoring). Fall back to free/busy if you get access denied on someone's calendar.

**Step 4: Score flexibility.** Not all conflicts are equal. A 1:1 sync is easy to move; an all-hands is not. Score every conflict:

| Factor | More flexible | Less flexible |
|--------|--------------|---------------|
| Meeting size | 2 people | 6+ people |
| Type | 1:1, sync, focus time | interview, client, all-hands |
| Organizer | They organized it (easy to move) | Someone else organized it |

**Step 5: Suggest slots.** Rank by total impact:
1. No conflicts for anyone (best)
2. Only flexible conflicts (all movable)
3. Mixed flexibility
4. Fixed conflicts (last resort)

Within each tier, prefer mid-morning (10–11:30am) and mid-afternoon (2–3:30pm), Tue–Thu, with buffer around existing meetings.

**Step 6: Create event.** After confirmation, create with calendar invite and video meeting link.

## Calendar Event Interpretation

When reading calendars, apply these rules:

| Event property | Interpretation |
|----------------|---------------|
| Declined events | Ignore — doesn't block availability |
| Transparent events | Ignore — doesn't block calendar |
| OOO / vacation | Hard blocker — never suggest slots during these |
| Travel blocks | Hard blocker |
| "Tentative" response | Soft conflict — treat as flexible |
| Working location events | Informational only — not blockers |

## Customization Notes

- **Calendar IDs** — Edit `config.md` with all calendars to check (work, personal, shared).
- **Working hours** — Default 9am–5pm. Adjust in config for your schedule.
- **VIP list** — Add names/emails of people whose meetings should never be scheduled over (your boss, key clients, etc.).
- **Flexibility keywords** — The scoring uses meeting title keywords. Add keywords common in your org (e.g., "standup", "retro", "sprint planning").
- **Video meeting** — Default creates a Google Meet link. Remove if you prefer no auto-link.
