---
name: deep-personalization
description: Per-contact email personalization for B2B outreach. Two-tier research (company → person) via parallel Haiku subagents, Sonnet writes per-lead email bodies pushed as custom_fields. Invoke when user says "personalize", "deep personalization", or asks to add hooks to leads before campaign push.
---

# Deep Personalization Skill

Per-contact email sequences grounded in PUBLIC research. Two-tier research (company, then person), per-lead body composition, push to SmartLead with entire email body as custom variable.

## Local Storage

Each run lives in its own folder:

```
sofia/tmp/dp_run_{SEGMENT}_{SENIORITY}_{YYYYMMDD}/
  contacts.json                     ← input leads
  leads_for_push.json               ← final output for SmartLead push
  company_research_cache.json       ← global cache, reused across all chunks in run
  tmp/
    research_chunk_1.json           ← Haiku research agents (30 contacts each)
    research_chunk_2.json
    personalization_chunk_1.json    ← Sonnet writer agents
    personalization_chunk_2.json
```

`tmp/` is cleaned up after successful merge. Root files are kept as run artifacts.

All agent file paths are absolute, rooted at the run folder. Example:
`/Users/user/sales_engineer/sofia/tmp/dp_run_INFPLAT_FOUNDERS_20260503/tmp/research_chunk_1.json`

**Global Company Cache (NEW):** Instead of per-chunk caches, maintain single `company_research_cache.json` at run root. Haiku agents load this at startup, reuse cached domain research, and append new findings. Saves ~15-20% of company research tokens across waves.

## Scaling — Split Pipeline (Haiku research → Sonnet writing)

TWO passes per chunk: Haiku researches → Sonnet writes. **30 contacts per chunk** — Haiku has sufficient context window. Number of research agents = ceil(total / 30). All agents launch in parallel in a single message, 8 agents max per wave.

**Pass 1 — Research (Haiku)**: reads contacts, runs Exa searches (fallback: WebSearch), applies pre-filter (skip obvious defaults), scores, routes to channel, saves `tmp/research_chunk_{N}.json`.

**Pass 2 — Writing (Sonnet)**: reads research chunk, composes email bodies for deep_email contacts only (skips linkedin and generic_email), saves `tmp/personalization_chunk_{N}.json`.

Default-tier contacts: writer copies default text verbatim (no research needed, still goes through writer for schema consistency).

### How to invoke agents

**Research agent (Haiku)** — launch via Agent tool, `run_in_background=true`, one agent per chunk:

```
Agent(
  subagent_type="general-purpose",
  model="haiku",
  run_in_background=True,
  prompt=<research prompt — see template below>,
)
```

Before launching: write contacts for that chunk to `{run_dir}/tmp/research_input_chunk_{N}.json`.
Launch all N agents in a single message (parallel).

**Writer agent (Sonnet)** — launch via Agent tool after research quality gate passes:

```
Agent(
  run_in_background=True,
  prompt=<writer prompt — see template below>,
)
```

Launch all N writer agents in a single message (parallel).

> **Alternative (experimental):** Gemini scripts in `agents/gemini_researcher.py` / `agents/gemini_writer.py`.
> Currently broken — Gemini ignores pre-gathered Exa data (see TODO in gemini_researcher.py).
> Use only if Anthropic API is unavailable.

## Contact Input Schema

Every contact entering the skill MUST have these fields. Validate before chunking — missing names = broken personalization.

**All-columns rule**: ALL columns from the source CSV are preserved at every stage — `contacts.json`, `_identity` in research/writer chunks, and final output files. The table below lists the fields the skill actively uses; any extra columns pass through untouched.

**Value integrity rule**: if a field had a non-empty value in the source CSV, it MUST remain non-empty at every downstream stage. Never overwrite a populated field with an empty string, null, or a placeholder. Only computed fields (e.g. `campaign`, `tier`, `timezone`) may be set or overwritten by the skill.

| Field | Required | Notes |
|-------|----------|-------|
| `email` | **YES** | SmartLead lead key |
| `first_name` | **YES** | Must be pre-split. Never infer from email. |
| `last_name` | **YES** | Must be pre-split. Never infer from email. |
| `title` | **YES** | Used for tier routing and hook framing |
| `company_name` | **YES** | As it appears in SmartLead `company_name` field |
| `company_domain` | **YES** | Extracted from CSV `website` column — strip scheme + www |
| `social_proof` | **YES** | Pre-set `social_proof` value from CSV "social proof" column. **Verbatim marketing string** ("Whalar, Kolsquare, Billion Dollar Boy") for Step 1 template — NOT a list of lead companies. Never extract company names from this field. |
| `linkedin_url` | recommended | Person research anchor |
| `segment` | **YES** | INFPLAT / IMAGENCY / AFFPERF / SOCCOM — required for campaign name |
| `seniority` | conditional | FOUNDERS / C_SUITE_HEAD / TECHLEAD / ACCOUNT_OPS. May be empty — researcher infers from LinkedIn title → `inferred_seniority`. Writer uses `inferred_seniority` as fallback. Required for campaign name. |
| `country` | **YES** | Full name ("United States") — required for TZ routing → campaign name |
| `company_size` | recommended | Required for tier routing → campaign name; passthrough to `_identity` |
| `timezone` | optional | Legacy field — ignored, TZ derived from `country` |
| `campaign` | — | **Do not set in input.** Writer computes it as `[{tier}_{tz}] c-OnSocial_{segment}_{seniority}` where `tier` and `tz` are derived from `country + company_size + seniority` via `references/campaign-routing.md`. |
| `phone_number` | optional | Passthrough to `_identity` only |

**Pre-flight check (orchestrator)**:
```python
for c in contacts:
    if not c.get("first_name"):
        raise ValueError(f"Missing first_name for {c['email']} — fix source data before running")
    if not c.get("seniority"):
        c["seniority"] = ""  # researcher will infer from LinkedIn; log as WARN
```

### Bounce-Prevention Pre-Flight Gate (mandatory before chunking)

Apply BEFORE building `contacts.json`. Output two files: `preflight_passed.csv` (continue) and `preflight_quarantine.csv` (with `_drop_reason` column).

```python
import re
LINKEDIN_DOMAIN_RE = re.compile(r'(^|\.)linkedin\.com$', re.I)
EMAIL_RE = re.compile(r'^[^@]+@[^@]+\.[^@]+$')

def preflight_drop_reason(row) -> str | None:
    email = (row.get("email") or "").strip()
    if not EMAIL_RE.match(email):
        return "email_format_invalid"
    if str(row.get("email_verified", "")).lower() == "false":
        return "email_not_verified"
    fn = (row.get("first_name") or "").strip()
    if not fn or "*" in fn:
        return "first_name_masked_or_empty"   # last_name masked is OK — emails use [first_name] only
    # linkedin.com domain is OK — research falls back to LinkedIn person research,
    # email sending doesn't need the company domain.
    return None
```

**Rules:**
- `first_name` masked (`*`) or empty → drop. We address recipients by `Hi [first_name],` so masked first_name is unsendable.
- `last_name` masked (`*`) → **keep**. Last name is not used in templates.
- `company_domain == linkedin.com` (or subdomain) → **keep**. Person research can run on LinkedIn URL alone; we don't send to the company domain.
- `email_verified == False` → drop. Hard rule — bounces destroy mailbox reputation.
- `email` not matching format → drop.

Quarantined rows are not deleted — they're written to `preflight_quarantine.csv` with `_drop_reason` so they can be recovered later if data improves.

## Agent Prompt Templates

### Research Agent Prompt (Haiku)

```
You are a research agent using the deep-personalization skill.
READ the agent instructions FIRST: /Users/user/sales_engineer/.claude/skills/deep-personalization/agents/research.md

RUN DIRECTORY: {run_dir}

CONTACTS ({chunk_size}):
  [email | first_name | last_name | title | company_name | company_domain | linkedin_url | segment | seniority | timezone | country | company_size | social_proof | phone_number]
  {contact_rows}

⚠️ ALL fields from contacts.json must be included in contact_rows — never strip fields. `social_proof` is a verbatim marketing string (e.g. "Whalar, Kolsquare, Billion Dollar Boy") — do NOT treat it as a list of companies to research.

UNIQUE COMPANIES in this chunk: {unique_company_list}

⚠️ SCHEMA RULES — DO NOT INVENT YOUR OWN FORMAT:

OUTPUT FILE: {run_dir}/tmp/research_chunk_{N}.json

TOP-LEVEL STRUCTURE (mandatory):
{
  "_execution": {"agent_index": N, "started_at": "...", "completed_at": "...", "deep_email": 0, "linkedin": 0, "generic_email": 0},
  "company_research_cache": { "domain.com": { ...company_research object... } },
  "results": {
    "email@domain.com": {
      "_identity": { <EXACT DICT copy of the full input row for this contact — ALL fields including any extra CSV columns, not a string. Never drop keys.> },
      "channel": "deep_email|linkedin|generic_email",
      "multi_angle": true/false,
      "person_quality_score": 0-3,
      "company_quality_score": 0-3,
      "website_scrape": null or { "scrape_status": "ok", "product_summary": "...", "icp_relevant": "yes/unclear/no", "scrape_quality": "good/borderline/thin/empty", "borderline": false, "website_quality_score": 1 },
      "company_research": { "growth_metrics": [], "recent_funding": null, "scale_metrics": [], "public_ceo_quotes": [], "recent_news": [], "historical_signals": [], "product_summary": "...", "business_model_signals": [], "sources": [], "quality_score": 0-3 },
      "person_research": { "career_path": [], "prior_companies": [], "tenure_signals": [], "education": [], "public_quotes": [], "thought_leadership": [], "role_specific_signals": [], "linkedin_posts": [], "linkedin_active": true/false, "sources": [], "quality_score": 0-3 },
      "researched_at": "ISO timestamp",
      "researcher": "haiku-research-{N}"
    }
  }
}

CRITICAL:
- "results" is a DICT keyed by email (lowercase), NOT an array
- "_identity" is a DICT (all input fields), NOT a pipe-separated string
- "channel" is a STRICT ENUM — exactly one of: "deep_email", "linkedin", "generic_email". Any other value is a contract violation.
- If person_quality_score == 0 AND company_quality_score == 0 AND channel != "linkedin" → website_scrape MUST be a populated object (not null). channel = "generic_email" in this case.
- All JSON values must be valid JSON — numbers like "500+" must be quoted strings
- SAVE EVERY CONTACT — never skip any
- SILENCE PROTOCOL: write the file, no chat output
- Contacts with empty `seniority`: attempt to infer from LinkedIn title (see Seniority Inference section in research.md). Save result as `_identity["inferred_seniority"]`. If cannot determine → `"UNKNOWN"`.

TOOLS: Use mcp__exa__web_search_exa, mcp__exa__web_search_advanced_exa (for people: category="people", for company: category="company"), mcp__exa__crawling_exa (primary).
If Exa MCP returns 402 → fall back to WebSearch + WebFetch for the same queries.
```

### Writer Agent Prompt (Sonnet)

```
You are a writing agent using the deep-personalization skill.
READ the agent instructions FIRST: /Users/user/sales_engineer/.claude/skills/deep-personalization/agents/writer.md
READ offer context: /Users/user/sales_engineer/.claude/skills/deep-personalization/references/offer-context.md
READ segment reference: /Users/user/sales_engineer/.claude/skills/deep-personalization/references/{segment}.md
READ campaign routing: /Users/user/sales_engineer/.claude/skills/deep-personalization/references/campaign-routing.md

RUN DIRECTORY: {run_dir}
RESEARCH INPUT: {run_dir}/tmp/research_chunk_{N}.json

OFFER CONTEXT: see references/offer-context.md (single source of truth — do not inline alternatives).
SEGMENT: {segment} — load defaults from references/{segment}.md per role.
STEP COUNT: SOCCOM = 3 (set email_4_body = ""), all others = 4.

⚠️ SCHEMA RULES — DO NOT INVENT YOUR OWN FORMAT:

OUTPUT FILE: {run_dir}/tmp/personalization_chunk_{N}.json

TOP-LEVEL STRUCTURE (mandatory):
{
  "_execution": {"agent_index": N, "started_at": "...", "completed_at": "...", "person": 0, "company": 0, "company_light": 0, "default": 0},
  "results": {
    "email@domain.com": {
      "_identity": { <verbatim copy from research chunk _identity dict — ALL fields, never drop keys> },
      "tier": "...",
      "multi_angle": true/false,
      "confidence": "high|medium|low",
      "email_1_hook_type": "...",
      "email_2_hook_type": "...",
      "facts_cited": ["fact (source)"],
      "sources": ["https://..."],
      "subject_1": "actual subject text (no SmartLead variables)",
      "subject_2": "",
      "subject_3": "",
      "email_1_body": "Hi [first_name],\n\n...",
      "email_2_body": "...",
      "email_3_body": "...",
      "person_quality_score": 0-3,
      "company_quality_score": 0-3,
      "researched_at": "...",
      "researcher": "sonnet-writer-{N}"  
    }
  }
}

CRITICAL:
- "results" is a DICT keyed by email (lowercase), NOT an array
- email_1_body always starts with "Hi [actual_first_name]," — never SmartLead variables
- NO signature in any email_N_body — template appends "Bhaskar from OnSocial" after each variable
- SAVE EVERY CONTACT — never skip any
- SILENCE PROTOCOL: write the file, no chat output
- Contact with empty `seniority`: use `_identity["inferred_seniority"]` for campaign routing and role hook selection. If `inferred_seniority = "UNKNOWN"`: campaign = `[T2_BER] c-OnSocial_{segment}_UNKNOWN`; use `title` field directly for hook framing instead of seniority-specific role opener.
```

## Merge Protocol (orchestrator)

Run after all writer agents complete. Merges chunk files into contacts.json and builds output files split by channel.

**Channel routing rules:**
- `deep_email` → `leads_for_push.json` — SmartLead push with per-lead custom_fields from writer
- `linkedin` → `leads_linkedin.json` — GetSales/LinkedIn outreach (no writer ran for these)
- `generic_email` → `leads_generic_email.json` — SmartLead push with default sequence verbatim

```python
all_results = {}       # writer output — deep_email only
all_research = {}      # research output — all channels
all_company_research = {}
for i in range(1, num_writer_agents + 1):
    chunk = load_data(project, f"tmp/personalization_chunk_{i}.json")
    if chunk.success:
        all_results.update(chunk.data.results)
        all_company_research.update(chunk.data.company_research)

# research_chunk_* has channel field for all contacts (including linkedin + generic_email)
for i in range(1, num_research_agents + 1):
    chunk = load_data(project, f"tmp/research_chunk_{i}.json")
    if chunk.success:
        all_research.update(chunk.data.results)

# Update contacts.json
contacts = load_data(project, f"campaigns/{slug}/contacts.json").data
for c in contacts:
    if c["email"].lower() in all_results:
        c["personalization"] = all_results[c["email"].lower()]
    else:
        c["personalization"] = build_default_personalization(c, default_sequence)
    # carry channel from research output
    if c["email"].lower() in all_research:
        c["channel"] = all_research[c["email"].lower()].get("channel", "deep_email")
save_data(project, f"campaigns/{slug}/contacts.json", contacts)

# Persist company research for future runs
run = load_data(project, f"campaigns/{slug}/runs/{run_id}.json").data
for domain, research in all_company_research.items():
    if domain in run["companies"]:
        run["companies"][domain]["research"] = research
save_data(project, f"campaigns/{slug}/runs/{run_id}.json", run)

# Build output files split by channel
leads_deep_email = []
leads_linkedin = []
leads_generic_email = []

for c in contacts:
    channel = c.get("channel", "deep_email")
    p = c["personalization"]
    ident = p.get("_identity", {})
    lead = dict(ident)
    lead["email"] = c["email"]

    if channel == "deep_email":
        lead["custom_fields"] = {
            **ident.get("custom_fields", {}),
            "subject_1": p["subject_1"],
            "email_1_body": p["email_1_body"], "email_2_body": p["email_2_body"],
            "email_3_body": p["email_3_body"], "email_4_body": p.get("email_4_body", ""),
            "social_proof": ident.get("social_proof", ""),  # template string for {{social_proof}} in Step 1 — NOT a company list
            "personalization_tier": p["tier"],
            "multi_angle": "yes" if p["multi_angle"] else "no",
            "personalization_confidence": p["confidence"],
            "email_1_hook": p["email_1_hook_type"], "email_2_hook": p["email_2_hook_type"],
            "facts_cited": "; ".join(p["facts_cited"]),
            "sources": "; ".join(p["sources"]),
        }
        # NOTE: social_proof is in custom_fields only — do NOT add to top-level lead dict.
        # Top-level social_proof looks like a company reference and causes misinterpretation.
        leads_deep_email.append(lead)
    elif channel == "linkedin":
        leads_linkedin.append(lead)
    else:  # generic_email
        lead["custom_fields"] = {**ident.get("custom_fields", {}), "social_proof": ident.get("social_proof", "")}
        leads_generic_email.append(lead)

save_data(project, f"campaigns/{slug}/leads_for_push.json", leads_deep_email)
save_data(project, f"campaigns/{slug}/leads_linkedin.json", leads_linkedin)
save_data(project, f"campaigns/{slug}/leads_generic_email.json", leads_generic_email)
```

**After merge, report counts:**
- `deep_email`: N leads → `leads_for_push.json`
- `linkedin`: N leads → `leads_linkedin.json` (route to GetSales separately)
- `generic_email`: N leads → `leads_generic_email.json` (route to generic SmartLead campaign)

## Sequence Template (upload to SmartLead once per campaign)

The template is a thin shell — all content lives in per-lead custom_fields.

**Step 1:**
```
subject: {{subject_1}}
body:
{{email_1_body}}

Bhaskar from OnSocial

Trusted by {{social_proof}}
```
Note: `\n\n` before "Bhaskar" and before "Trusted by" — verify in SmartLead UI after upload that the blank lines render (not merged). If merged, re-save.

**Step 2:** `subject: ""` (reply thread)
```
{{email_2_body}}

Bhaskar from OnSocial
```

**Step 3:** `subject: ""`
```
{{email_3_body}}

Bhaskar from OnSocial
```

**Step 4:** `subject: ""`
```
{{email_4_body}}

Bhaskar from OnSocial
```

## social_proof

Pre-set in source CSV as `social_proof` column. Passed through to leads_for_push.json as-is. Used in Step 1 template signature only.

**Never put `{{social_proof}}` inside `email_N_body`** — SmartLead does not resolve nested variables.

## Quality Gate — Post-Research Protocol

After ALL research agents complete, run this protocol before asking user to approve writers.

### Step 1 — Validate chunk files

Check that all `tmp/research_chunk_{N}.json` files exist and are non-empty. For each chunk:
- Count contacts in `results` dict (keyed by email)
- Flag any `channel` value outside `{"deep_email", "linkedin", "generic_email"}` — CONTRACT VIOLATION. Trigger cleanup retry on those contacts.
- Flag any contact where `channel == "generic_email" AND website_scrape is null` — invariant broken, scrape fallback was skipped. Trigger cleanup retry.
- Flag any contact where `person_quality_score=0 AND company_quality_score=0 AND channel != "linkedin" AND website_scrape is null` — same invariant, different entry point.
- Flag any contact where `channel == "generic_email" AND (person_quality_score >= 2 OR company_quality_score >= 2)` — REVERSE invariant. Should have been deep_email. Trigger cleanup retry.
- Auto-recompute `multi_angle = (person_quality_score >= 1 AND company_quality_score >= 1)` for every contact. If agent's value differs → patch silently, log as anomaly (not retry-worthy).
- `campaign` field in `_identity` is expected to be empty at this stage — writer assigns it. Do NOT patch or flag it here.

### Step 2 — Compute coverage stats

```python
from collections import Counter
channels = Counter(v.get("channel") for v in all_results.values())
multi = sum(1 for v in all_results.values() if v.get("multi_angle"))
total = len(all_results)
deep_email_pct = channels["deep_email"] / total * 100
invalid_channels = [e for e, v in all_results.items() if v.get("channel") not in {"deep_email", "linkedin", "generic_email"}]
```

### Step 3 — Analyze suspicious findings

For each anomaly below, don't just flag it — **explain what happened and rate severity**:

| Anomaly | Likely cause | Severity |
|---------|-------------|----------|
| `channel` value outside `{deep_email, linkedin, generic_email}` | Contract violation — agent wrote an invalid channel string | High — downstream writer will skip or crash on this contact |
| `channel = "generic_email"` with `website_scrape=null` | Agent skipped mandatory scrape fallback for zero-signal contact | High — invariant broken, writer has nothing to work with |
| Chunk has far fewer cached domains than unique companies | Agent reused cache from a previous run or skipped company research | High — research may be thin for those contacts |
| `deep_email` < 40% of total | Most contacts lack public footprint — consider restricting to senior-only roles | Context-dependent |
| Chunk exec stats don't add up | Agent hallucinated summary stats | Low — stats are decorative, actual channels in `results` are authoritative |
| Contacts missing from results | Agent skipped contacts | High — those leads will get no personalization |

Pull 3 random high-confidence samples (`deep_email`, combined P+C score ≥ 3) and show:
- Name, company, channel, P/C scores
- One company signal (product_summary or recent_news)
- One person signal (career_path or role_specific_signals)

### Step 4 — Save report as MD

**Always save the report to `{run_dir}/research_report.md`** — never only print it in chat.

Use this template:

```markdown
# DP Research Report — {SEGMENT} {SENIORITY}
**Run:** `{run_dir_name}`
**Segment:** {segment} | **Seniority:** {seniority}
**Date:** {date} | **Contacts:** {total} ({note on deduplication if any})

---

## Campaigns

| Campaign | Contacts |
|----------|----------|
| `[T2_BER] c-OnSocial_...` | N |
| `[T2_NY] c-OnSocial_...` | N |

---

## Coverage

| Channel | Contacts | % |
|---------|----------|---|
| `deep_email` | N | N% |
| `linkedin` | N | N% |
| `generic_email` | N | N% |
| invalid ⚠️ | N | N% |
| **Multi-angle** (deep_email only) | **N** | **N%** |

**deep_email: N%** → writer agents will run on this subset only.

> [Interpretation: explain WHY the split looks the way it does — e.g. "Low deep_email% is normal for ACCOUNT_OPS, ops roles have thin public footprint."]

---

## Suspicious Findings

[For each anomaly found — include only if something actually flagged. If clean, write "None."]

### ⚠️ {anomaly title}
**What happened:** {concrete description — which chunk, how many affected}
**Why:** {root cause}
**Severity:** Low / Medium / High
**Impact:** {what this means for personalization quality}
**Recommended action:** {fix now / accept / skip}

---

## Sample — High-Confidence Contacts

### {Name} — {Company}
`{tier}` | P={score} C={score} | {title} | {country} | `{campaign}`

- **Company:** {product_summary snippet}
- **Signal:** {recent_news or growth_metrics}
- **Person:** {career_path or role_specific_signals}
- **Hook angle:** {what the writer should focus on}

[repeat for 2 more samples]

---

## Chunk Stats

| Chunk | Contacts | P | C | CL | D+DC | Domains cached |
|-------|----------|---|---|----|------|----------------|
| 1 | N | N | N | N | N | N |
...

---

## Decisions Needed

- [ ] **Channel contract violations ({N} contacts):** Invalid `channel` value or `generic_email` with null `website_scrape`. Run cleanup retry? (only show if N > 0)
- [ ] **linkedin ({N} contacts):** No writer — route to GetSales/LinkedIn outreach separately. Confirm.
- [ ] **generic_email ({N} contacts):** No writer — default sequence verbatim → `leads_generic_email.json`. Confirm.
- [ ] **Writer agents:** Approve launch of {N} writer agents for `deep_email` contacts?
- [ ] **[any other open question]**
```

### Step 5 — Report in chat

After saving the file, post this summary in chat:

```
Ресёрч готов — {N} из {N_input} контактов обработано
Отчёт: {run_dir}/research_report.md

── Каналы ──────────────────────────────
  deep_email     {N} ({pct}%)   ← writers запустятся на них
  generic_email  {N} ({pct}%)
  linkedin       {N} ({pct}%)
  ⚠️ invalid     {N} ({pct}%)   ← (только если > 0)

── Качество deep_email ─────────────────
  Person ≥ 2     {N} ({pct}%)
  Company ≥ 2    {N} ({pct}%)
  Multi-angle    {N} ({pct}%)
  Оба = 0        {N} ({pct}%)   ← риск тонкой персонализации

── Seniority ───────────────────────────
  FOUNDERS       {N}
  C_SUITE_HEAD   {N}
  TECHLEAD       {N}
  UNKNOWN        {N}   ← (только если > 0)

── Тайтлы — топ-5 ──────────────────────
  CEO            {N}
  CTO            {N}
  Head of Data   {N}
  ...

── Кампании ────────────────────────────
  [T1_NY] c-OnSocial_INFPLAT_FOUNDERS    {N}
  [T2_BER] c-OnSocial_INFPLAT_FOUNDERS   {N}
  ...

⚠️ {count} аномалий — детали в отчёте
```

Full details in the MD file — don't repeat anomaly descriptions in chat.

## Post-Research Checkpoint

Runs immediately after Quality Gate passes. Prepares up to three deliverables (only those that apply), saves them to `{run_dir}/checkpoint/`, then asks user to approve writer launch.

**Conditional skip:** if `generic_email` count is 0 AND `linkedin` count is 0 (i.e. all contacts routed to `deep_email`), skip Document 1 and Document 2 — they would be empty. Still produce Document 3 (DP Examples) for spot-check before writer launch. Report in chat: `"Checkpoint: only deep_email contacts (N) — skipping generic/linkedin docs, examples saved → checkpoint/dp_examples.md. Approve writer launch?"`.

### Checkpoint Document 1 — SmartLead CSV (generic_email only)

`generic_email` contacts are ready to push now — no writer needed (default sequence verbatim).

For each `generic_email` contact, compute campaign name via `build_campaign_name()` from `references/campaign-routing.md`:
- Use `inferred_seniority` if `seniority` is empty
- `inferred_seniority = "UNKNOWN"` → campaign = `UNKNOWN` (still included in the combined file)

**One combined CSV for all generic_email contacts:**
```
{run_dir}/checkpoint/smartlead_generic.csv
```

**CSV Schema:**

| Column | Required | Notes |
|--------|----------|-------|
| `first_name` | **YES** | Real data only — never infer from email |
| `last_name` | **YES** | Real data only — never infer from email |
| `email` | **YES** | SmartLead lead key |
| `company_name` | **YES** | Real data only |
| `website` | **YES** | Real data only (company domain with scheme) |
| `linkedin_url` | **YES** | Real data only |
| `Company location` | **YES** | Full country name ("United States") — real data only |
| `title` | **YES** | Real data only |
| `Segment` | **YES** | INFPLAT / IMAGENCY / AFFPERF / SOCCOM — real data only |
| `social proof` | **YES** | Имя колонки в CSV. Real data only. При пуше в SmartLead → `custom_fields["social_proof"]` → резолвится как `{{social_proof}}` в шаблоне |
| `seniority` | **YES** | May be researcher-inferred — but must be present (no blanks) |
| `timezone` | **YES** | Derived from `Company location` by researcher |
| `company_size` | **YES** | Real data only |
| `campaign tier` | **YES** | Computed: `[tier_tz] c-OnSocial_{segment}_{seniority}` |
| `phone_number` | optional | Passthrough only — may be empty |

**Rule:** every column marked **YES** must be non-empty with real data. No placeholders, no nulls, no empty strings. `phone_number` is the only column that may be blank.

**In chat after saving**: run the **SmartLead Approval Gate** (3-table format) from `references/campaign-routing.md` — same protocol as for `leads_for_push.json`. The gate handles:

- Pre-approval existence check (`smartlead_list_campaigns()`)
- Table 1 (as-is), Table 2 (proposed moves), Table 3 (after optimization)
- Consolidation when any campaign < 50 leads
- NEW vs existing campaign approval
- Hold/pending for sub-threshold groups → `{run_dir}/pending/{campaign_name}.json`

Do NOT inline a separate breakdown here — single source of truth lives in `campaign-routing.md::SmartLead Approval Gate`. Apply it identically to `checkpoint/smartlead_generic.csv` (research-stage) and `leads_for_push.json` (post-writer).

```
generic_email — {N} контактов → checkpoint/smartlead_generic.csv
→ proceed to SmartLead Approval Gate (see campaign-routing.md)
```

### Checkpoint Document 2 — GetSales CSV (linkedin only)

`linkedin` contacts go to GetSales. One CSV per segment, 49-column schema per `getsales-formatting.md`.

```
{run_dir}/checkpoint/getsales_{segment}.csv
```

Key fields:
- `list_name` = `"{SEGMENT} Without Email {YYYY-MM-DD}"`
- `tags` = segment code: INFPLAT → `INFLUENCER_PLATFORMS`, IMAGENCY → `IM_FIRST_AGENCIES`, etc.
- `linkedin_nickname` = extracted from `linkedin_url` via `linkedin\.com/in/([^/?]+)`
- `work_email` = empty (LinkedIn-only contacts)
- `cf_competitor_client` = `social_proof`
- All `cf_message*`, `cf_personalization*` = empty (filled manually later)

### Checkpoint Document 3 — DP Examples MD

```
{run_dir}/checkpoint/dp_examples.md
```

**Top 3 — highest P+C score (deep_email only):**
For each: name, company, title, seniority, P score, C score, top company signal, top person signal, proposed hook type.

**Bottom 3 — lowest P+C score still qualifying as deep_email (just at threshold):**
For each: same fields + why it barely qualified + risk of thin personalization.

**Unknown seniority (first 5, if any):**
What was inferred, confidence level, what signals were found.

### Checkpoint Report in Chat

Short summary only — docs are the source of truth:

```
Checkpoint готов.

SmartLead CSV (generic_email):     {N} контактов → checkpoint/smartlead_generic.csv
GetSales CSV (linkedin):           {N} контактов → checkpoint/getsales_{segment}.csv
DP Examples:                       checkpoint/dp_examples.md

Запускать writers? ({N} deep_email контактов)
```

Do NOT repeat channel breakdown or anomaly list in chat — those are already in `research_report.md`.

## Channel Distribution Targets

| Channel | Target % | When assigned |
|---------|--------:|--------------|
| `deep_email` | 50-70% | person_q ≥ 2, or company_q ≥ 2, or both ≥ 1 |
| `linkedin` | 5-20% | T1 contact, linkedin_active, no deep data |
| `generic_email` | 10-30% | zero-signal, no active LinkedIn |

If `generic_email` exceeds 50% → WARN: contacts mostly lack public footprint. Consider restricting to senior-only roles.

## Anti-Patterns

- **Hook stacking**: career_path + concrete_number + math in one paragraph → reads like a dossier, not an email. ONE hook per opener.
- **Fake numbers as filler**: "10x growth" with no source → if recipient knows it's wrong, kills credibility AND deliverability.
- **Praise without context**: "I admire your work" — flattery, not personalization. Cite WHAT you read.
- **Long icebreakers**: >3 sentences → reader skims past the value prop.
- **Identical openers across contacts at same company**: if two people both get "growing 600% in a year means..." → comparing notes exposes the templating. Vary role-framing.
- **Personalizing low-tier as if high-tier**: thin signal stretched into a full custom email reads worse than honest default. quality_score < 2 → use default tier, don't fake it.
- **Re-researching across runs**: company research is persistent. Don't re-WebSearch a company already in `companies[domain].research`.
- **Callback openers in Email 2**: "as I mentioned in my last email..." → reads as desperate follow-up. Open Email 2 with fresh context as if it's the first touch on that angle.

## User Feedback Integration

Apply immediately when user gives feedback mid-session:
- "Make hooks shorter" → cap icebreaker at 2 sentences
- "Don't use math" → drop `math_on_their_data` from hook priority
- "More casual tone" → adjust subagent prompt
- "Don't personalize Emails 2-4" → composition writes only Email 1
- "Increase default threshold" → require quality_score ≥ 3 for person tier

## Agent Files

| File | Purpose |
|------|---------|
| `agents/research.md` | Instructions for Haiku researcher (primary) |
| `agents/writer.md` | Instructions for Sonnet writer (primary) |
| `agents/gemini_researcher.py` | Experimental: Gemini 3 Flash researcher (broken — see TODO in file) |
| `agents/gemini_writer.py` | Experimental: Gemini 3.1 Pro writer |

## Reference Files

| File | Purpose |
|------|---------|
| `references/{segment}.md` | **Per-segment reference** (e.g. `infplat.md`). Contains: default subjects (authoritative), sequence templates (verbatim bodies per role), gold standards, and anti-patterns. Writer reads ONE file per run — no split between sequences and quality-standards. |
| `references/campaign-routing.md` | Campaign name builder: TZ mapping, size tier, naming convention. Orchestrator uses at pre-flight to set `campaign` field per contact. |
