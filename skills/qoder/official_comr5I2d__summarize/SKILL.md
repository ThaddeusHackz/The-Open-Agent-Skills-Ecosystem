---
name: summarize
description: "Summarize session/branch changes from git and conversation. Use for 'summarize', 'summarize the branch', 'summarize the session', or PR description drafts."
---

# Summarize

Generate a concise, pasteable summary of what was built and decided this session. Combines two sources:

- **Branch diff** — git commits and file changes since the branch diverged from main (if in a git repo with changes)
- **Session context** — what was discussed, decided, or resolved in this conversation

Either source alone is valid. When both exist, synthesize them into one unified summary rather than two separate sections.

## Output format

A Markdown unordered list (`-` bullets). Each bullet:
- Starts with `- **Bold Category Label** —`
- Followed by a plain-English explanation of what was built or decided, naming the key files/components where relevant
- One bullet per logical area of work (not per commit, not per file, not per conversation topic)
- Aim for 5–12 bullets total
- No headers, no sections, no markdown beyond the `- **Label** —` pattern

Example shape:
```
- **CLI** — bin/entry.mjs + src/orchestrator/ supervises the three subprocesses with wait-for-file and wait-for-TCP gates so the client never proxies into a not-yet-ready backend.
- **Mocks** — mock-server.ts, mock-redis.ts, mock-realtime.ts. Ships both in-memory and real-Redis variants; full Redis API parity including transactions.
- **Decision** — Deferred the Redis persistence layer to the next milestone; current implementation is in-memory only by design.
```

## Procedure

1. Gather context — run these in parallel where applicable:
   - Check if inside a git repo: `git rev-parse --git-dir 2>/dev/null`
   - If yes: `git log --oneline origin/main..HEAD` — commits on branch
   - If yes: `git diff origin/main --stat` — files changed
   - If yes: `git diff origin/main -- '*.md' '*.json'` (limited) — scan CLAUDE.md, package.json for orientation
   - Check if a followups file exists at `~/.claude/followups/<project>.md` and skim the most recent session section
   - Review the current conversation for decisions made, problems solved, or directions chosen that wouldn't be obvious from the diff alone

2. If git data is available, read a representative sample of changed files — focus on entry points, new modules, key types. Don't read every file; use the stat output to identify clusters.

3. Write the summary — synthesize both sources into a single unified list:
   - Group by logical area of work (CLI, mocks, UI, config, tooling, decisions, etc.)
   - Name real file paths when the change is code-level
   - For session-only items (decisions, investigations, ruled-out approaches): use labels like **Decision**, **Investigation**, or **Approach** — explain the *why*
   - If there are no git changes at all, focus entirely on session context: what was explored, decided, or learned
   - Make it useful to someone who wasn't in the session

4. Write the summary file:
   - Ensure `~/.claude/summaries/` exists (`mkdir -p ~/.claude/summaries`)
   - Prune old summaries: keep the 10 most recent files in `~/.claude/summaries/`, delete the rest
   - Filename: `~/.claude/summaries/summary-YYYY-MM-DD-HHMMSS.md` using current local time
   - Write the summary there

5. Print the full summary to chat so the user can copy-paste it.

6. Report a one-line link to the file (e.g. `Written to ~/.claude/summaries/summary-2026-05-08-143022.md`)
