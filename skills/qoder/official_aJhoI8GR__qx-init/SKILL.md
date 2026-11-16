---
name: qx-init
description: >-
  Bootstraps or refreshes the `AGENTS.md` / `CLAUDE.md` instruction files of
  the current project. In fresh mode (neither file present), scans the project,
  asks targeted questions about description and non-default tooling, then
  generates `AGENTS.md` (canonical) + `CLAUDE.md` (= `@AGENTS.md` import). In
  existing mode (at least one file present), audits the existing files against
  best practices (default-tooling mentions, section ordering, dead refs,
  300-line soft limit), writes a factual audit report to `.agents/init/`, then
  refreshes `AGENTS.md` with user-validated section-by-section choices. Use
  when the user asks to initialize, bootstrap, refresh, or challenge the
  agent-instruction file pair of a project.

  FR triggers: initialiser AGENTS.md, initialiser CLAUDE.md, bootstrap
  consignes IA, challenger CLAUDE.md, rafraîchir consignes IA, init projet,
  créer fichier consignes agent.
---

# Skill: /qx-init — Bootstrap or refresh AGENTS.md / CLAUDE.md

## Output language

Respond in the language of the user's most recent message. The skill's
instructions are written in English for clarity and ecosystem consistency,
but every artifact the user sees — review comments, plan content, research
findings, file contents — must match the user's language.

## Process

### 1. Run the scan

Run from the **root of the target project** (current workspace). The script takes no argument and writes no file:

```bash
bash <SKILL_DIR>/scripts/scan.sh
```

Replace `<SKILL_DIR>` with the actual path to the skill directory (the one containing this `SKILL.md`). Do not rely on a tool-specific `!` / magic-run syntax: explicitly run the command in the terminal.

The script's stdout is a structured Markdown report. Stderr contains warnings (READ them: missing README, missing `.agents/`, monorepo, `.gitignore` drift) — they inform follow-up questions, never block the flow.

If the script exits with a non-zero status, abort the skill. Display the stderr output to the user. Do not fall back to LLM-only heuristics.

After the scan completes, also extract the `Verdict:` value from the `## Branch naming signals` block (one of: `not-a-git-repo`, `insufficient-signal`, `documented-and-coherent`, `undocumented-coherent-pattern`, `undocumented-no-pattern`, `documented-but-drift`). This verdict drives one extra conditional question in mode `fresh` and one extra conditional challenge in mode `existing` — see the inserts below in step 3. Skip silently when the verdict is `not-a-git-repo`, `insufficient-signal`, `documented-and-coherent`, or `undocumented-no-pattern`.

### 2. Read the canonical skeleton

**Before generating or refreshing any content, you MUST read `<SKILL_DIR>/references/skeleton.md`.** It contains:

- The 6-section canonical structure of `AGENTS.md` (ordering and content rules per section).
- Verbatim wordings of "hard" and "medium" rules to inject (translatable to the user's language).
- Inclusion / exclusion rules for the "Stack & non-default tooling" section.
- Anti-patterns to detect and correct.
- The invariant rule on the `AGENTS.md` / `CLAUDE.md` file pair.

### 3. Branch on mode

Read the `## Mode` block of the scan report.

#### Mode `fresh` (no existing files)

Single Q&A phase, 3–5 questions max:

1. **Project description (always)**: show the candidates from `## Description candidates` of the scan side by side. Ask the user to pick one or write a new 1–3 sentence description.
2. **Non-default tooling (only if needed)**: if the scan detected tools, ask whether any should be excluded from section 4, or if any are missing.
3. **Project-specific hard rule (only if user signals one)**: ask if the project has a non-standard hard rule to add to section 2 (often: no).
4. **Branch naming convention (only if verdict = `undocumented-coherent-pattern`)**: show the dominant pattern from the scan and 2–3 concrete branch examples (pick from the most recent branches listed in the scan). Ask: (a) document this pattern as a sub-bullet of section 6; (b) document a variant the user types in; (c) skip — do not document.

Then proceed to step 4.

#### Mode `existing` (at least one file present)

**Phase 1 — Audit:**

1. Create `.agents/init/` if it does not exist.
2. Write the audit report to `.agents/init/audit-YYYY-MM-DD.md` using today's ISO date. The report contains:
   - **Files detected**: path, line count, last modification, last commit hash + date, current `CLAUDE.md` content if 1 line.
   - **Conformance**: from the scan's `## Conformance check` block — sections present/missing, total lines vs 300-line soft limit, default-tooling mention count, dead-ref count, `CLAUDE.md` normalization status.
   - **Items to challenge**: one bullet per anti-pattern detected. Map each to the corresponding question to ask in phase 2.
   - If the scan verdict is `undocumented-coherent-pattern` or `documented-but-drift`, append a bullet: `**Branch naming** — verdict <verdict>: <one-line summary including the dominant pattern, the branches-inspected count, and the doc state>. Question phase 2: see corresponding challenge below.`
3. After writing the file, output a 3–5 line chat summary:
   - Path of the audit file (absolute).
   - Total lines vs limit.
   - Number of items to challenge.

**Phase 2 — Refresh:**

Q&A challenge — only on detected anti-patterns. Examples:

- "The scan detected N mentions of default commands (`npm install`, `git status`, …) in `AGENTS.md`. (a) remove all, (b) keep only those with a project-specific override, (c) keep as-is?"
- "The current description is `<text>`. Still accurate, or replace with `<scan candidate>` / write a new one?"
- "`CLAUDE.md` contains content beyond `@AGENTS.md` (X lines). Migrate the content into `AGENTS.md` and reduce `CLAUDE.md` to `@AGENTS.md`? (recommended)"
- For each existing block that does not map to sections 1–6 and is longer than 5 lines: "Preserve in section 7 'Project-specific knowledge'? (yes / drop / move to section X)"
- **Branch naming (only if verdict = `undocumented-coherent-pattern`)**: "The scan detected `<pattern>` on N/M branches but no documentation in `AGENTS.md`. (a) add as a sub-bullet in section 6; (b) add with a variant `<user-typed>`; (c) do not document."
- **Branch naming (only if verdict = `documented-but-drift`)**: "`AGENTS.md` documents `<doc-pattern, summarized by the LLM from the existing text>`, but the scan sees no dominant pattern (or a different one) on N/M branches. (a) keep doc, plan a manual cleanup of divergent branches; (b) replace doc with the real pattern observed; (c) reformulate the doc to accept both."

Then proceed to step 4.

### 4. Generate `AGENTS.md`

Following `references/skeleton.md`:

- Section order is non-negotiable.
- Translate verbatim hard/medium rules to the user's language while preserving intent.
- Include only non-default tools in section 4.
- Aim for ≤ 300 lines. If over, ask the user which medium/low sections to compress before writing.
- If the user confirmed a branch-naming convention in step 3 (mode `fresh` Q4 or mode `existing` phase 2 challenge), include a sub-bullet in section 6 of the form: `Branch naming: <pattern>. Examples: <2–3 real branch names taken from the scan>.`

Show the generated content **section by section** in chat. Wait for user validation (or amendments) on each section before moving to the next. Then assemble the final document.

### 5. Write the file pair

The final state must always satisfy the invariant: both files exist, `AGENTS.md` is canonical, `CLAUDE.md` contains exactly `@AGENTS.md`.

| Initial state | Action |
|---|---|
| Neither file | Write both. |
| Only `AGENTS.md` | Overwrite `AGENTS.md` with the refresh output. Create `CLAUDE.md` with one line: `@AGENTS.md`. |
| Only `CLAUDE.md` (with content) | Treat its content as canonical material to migrate; the `AGENTS.md` generated in step 4 already incorporates it. Write `AGENTS.md`. Overwrite `CLAUDE.md` with one line: `@AGENTS.md`. |
| Both exist | Overwrite `AGENTS.md`. Normalize `CLAUDE.md` to `@AGENTS.md` (overwrite if it differs). |

### 6. Final report

Output a concise summary:
- Files written (paths).
- Audit file path (mode existing only).
- Total lines of `AGENTS.md`.
- Pending warnings from the scan (`.agents/` not gitignored, monorepo detected, etc.) — recommend manual follow-up actions if relevant.

## Error handling

| Case | Behavior |
|---|---|
| `scan.sh` exits non-zero | Display stderr and abort. No fallback. |
| `AGENTS.md` > 1000 lines | Warn in audit, propose to split the refresh into multiple passes (3–4 sections per pass). |
| README missing AND no description candidate | Ask the user for a description in free-form input (no candidate displayed). |
| Monorepo detected (multiple manifests) | Warn explicitly: "Monorepo detected — `qx-init` only generates the root `AGENTS.md`. A future `qx-init-scope` skill will handle sub-packages." |
| `.agents/` not in `.gitignore` | Warn in the final report. Do **not** modify `.gitignore` automatically. |
| `CLAUDE.md` already equals `@AGENTS.md` exactly | Leave `CLAUDE.md` untouched (idempotent). |

## Writing rules

- Use the user's language for all human-readable output.
- No greetings, no pleasantries, no meta-commentary on the skill itself.
- Validate section by section before writing, but keep messages concise.
- The audit report (mode existing) is a deliverable: structured, factual. Do not include recommendations beyond the detected anti-patterns.
- Never silently truncate to fit the 300-line limit — always ask the user which sections to compress.
