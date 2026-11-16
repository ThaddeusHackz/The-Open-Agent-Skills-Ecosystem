---
name: proofreading-style-check
description: "Use when the user wants to proofread, style-check, or QA an article against editorial guidelines. Reads an article file and an editorial-guidelines.md, returns an inline diff plus a findings report. Optional LanguageTool layer for grammar."
version: 0.1.0
license: MIT
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch]
---

# Proofreading + Style Check

Check any markdown article against `editorial-guidelines.md` and `seo-best-practices.md`. Returns two artifacts: an inline-edited copy with suggested changes marked, and a findings report categorized by severity.

## Setup

No required keys. Optional:

- `LANGUAGETOOL_ENDPOINT` (default `https://api.languagetool.org/v2`) — adds a free grammar/spelling pass on top of Claude's native review. Works keyless, or self-host LanguageTool for privacy.

## Inputs

1. **Article path** (required). Glob `posts/*.md` and let the user pick if not specified.
2. **Editorial guidelines path** — default `./editorial-guidelines.md`. If missing, fall back to the shared voice reference and note it.
3. **Severity threshold** — `critical`, `warning`, `suggestion`. Default: report all three.

## Process

### 1. Load inputs

- Read the article.
- Read the editorial guidelines.
- Read `{SKILL_BASE}/../_shared/seo-best-practices.md`.

### 2. Extract rules into a checklist

From the editorial guidelines, pull:
- Banned words/phrases list
- Preferred words and naming conventions
- Sentence length ceiling
- Paragraph length ceiling
- POV (we/you/I/third)
- Contractions policy
- Emoji policy
- Serial comma rule
- Numerals vs words rule
- Reading level target
- Structural defaults for the article's format (how-to / comparison / opinion / case study — infer from the article or ask)

From the SEO best practices, pull the hard rules:
- Primary keyword in first 100 words
- Keyword in H1 and at least one H2
- Exactly one H1, no skipped heading levels
- 2–4 outbound authoritative links
- At least 3 descriptive internal links
- Meta title 50–60 chars, meta description 140–160 chars
- Hero image alt text present and descriptive

### 3. Pass 1 — mechanical checks (deterministic)

Walk the article and flag every occurrence of:
- Banned words (exact match, case-insensitive)
- Wrong product-name casing
- Sentences over the length ceiling
- Paragraphs over the length ceiling
- POV violations (e.g. first-person in a you-mode guideline)
- Missing Oxford commas in lists of 3+ where the rule is set
- Heading-level skips (H2 → H4)
- More than one H1
- Missing frontmatter fields

Each flag becomes a finding with: line number, severity, rule name, the offending text, and a suggested fix.

### 4. Pass 2 — SEO compliance (deterministic)

Check the article against the SEO rules list above. Each violation becomes a `critical` finding.

### 5. Pass 3 — voice and tone (Claude judgment)

Read the whole article and judge voice match. Flag:
- Sections that feel off-brand compared to the guidelines' voice attributes
- Hype-y phrasing that skirts the banned list without matching exact strings
- Weak ledes (the first sentence of a section doesn't state the claim)
- Sections that don't earn their place (could be cut without losing value)
- Missing the "one thing competitors don't cover" originality test
- Closers that don't point to a concrete next action

Each flag is a `warning` or `suggestion`.

### 6. Pass 4 — optional grammar layer

If `LANGUAGETOOL_ENDPOINT` is set, POST the article body to `/check`:

```
POST ${LANGUAGETOOL_ENDPOINT}/check
Content-Type: application/x-www-form-urlencoded

text=<body>&language=en-US&enabledOnly=false
```

Map each match to a finding with severity `suggestion` (grammar) or `warning` (likely errors). Deduplicate against Pass 1 findings.

### 7. Write two artifacts

**Artifact 1: inline-edited copy** at `review/<slug>-edited.md`

Copy of the original with suggested changes marked using `<del>` / `<ins>` HTML tags so diffs are visible in any markdown renderer:

```
The product is a <del>revolutionary</del><ins>category-defining</ins> platform.
```

**Artifact 2: findings report** at `review/<slug>-report.md`

```markdown
# Review: {slug}

_Checked against: {path to editorial-guidelines.md}_
_Date: {YYYY-MM-DD}_

## Summary

- **Critical:** {n} — must fix before publishing
- **Warnings:** {n} — strongly recommended
- **Suggestions:** {n} — worth considering

## Critical findings

### [L{line}] {rule name}
- **Found:** {offending text}
- **Why it matters:** {1 line}
- **Suggested fix:** {fix}

{…}

## Warnings

{same structure}

## Suggestions

{same structure}

## Checklist summary

| Check | Result |
|---|---|
| Primary keyword in first 100 words | ✅/❌ |
| Keyword in H1 | ✅/❌ |
| Keyword in ≥1 H2 | ✅/❌ |
| Exactly one H1 | ✅/❌ |
| No skipped heading levels | ✅/❌ |
| Meta title length (50–60) | ✅/❌ |
| Meta description length (140–160) | ✅/❌ |
| ≥3 internal links | ✅/❌ |
| 2–4 outbound links | ✅/❌ |
| Hero alt text present | ✅/❌ |
| No banned words | ✅/❌ |
| Sentence length within ceiling | ✅/❌ |
| Reading level in target range | ✅/❌ |
| Closer has concrete next action | ✅/❌ |
```

### 8. Print summary to console

5 lines: path to edited file, path to report, counts of critical/warning/suggestion, and a one-line verdict (`ready to publish`, `fix criticals first`, `needs rewrite`).

## Fallbacks

- **No editorial guidelines:** use shared voice reference, note it in the report header. Voice/tone findings are marked `suggestion` only (not `warning`) since the rules weren't user-authored.
- **LanguageTool unavailable:** skip Pass 4, note it in the report.
- **Article has no frontmatter:** still check the body, but flag missing frontmatter as a `critical`.

## Verification

1. Both artifacts exist under `review/`.
2. Findings report has a populated checklist table.
3. Every finding has a line number, severity, rule name, and suggested fix.
4. Running this skill twice on the same unchanged article produces identical reports (deterministic within a run).
