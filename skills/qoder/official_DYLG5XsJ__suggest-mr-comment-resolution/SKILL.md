---
name: suggest-mr-comment-resolution
description: >-
  Fetch all unresolved comments from a GitLab MR, deeply assess each
  comment's validity, and present a summary table with suggested
  fixes/responses. When the user approves ("go ahead" or equivalent),
  implement the fixes only — committing and pushing is handled separately
  by /suggest-commits. Use when the user says "suggest MR comment resolutions",
  "review MR comments", "what are the MR comments", "assess review feedback",
  "look at MR comments", or provides a GitLab MR URL with open discussions.
---

# Suggest MR Comment Resolutions

Fetch unresolved MR discussions, deeply assess each one, and present a
suggestion table. When the user approves, implement all fixes and stop.
**Committing and pushing is handled by `/suggest-commits`. The user also
handles replies and resolving threads themselves.**

## Prerequisites

- GitLab MCP tools (check first; if unavailable, explain and link to
  https://agoda.atlassian.net/wiki/spaces/JTBS/pages/850958266/Cursor+IDE+Setup+Guide#List-of-useful-MCP-servers)
- If GitLab MCP token is expired, fall back to `curl` with a personal access
  token (ask the user if not already in the conversation)
- **Pagination**: GitLab discussions API paginates at 100 items. Always check
  `x-total-pages` header and fetch all pages before reporting — missed
  comments on later pages are easy to overlook.

## Workflow

Use a todo list to track progress through each phase.

### Phase 1 — Fetch unresolved discussions

1. Get MR data (title, branch, changed files).
2. Fetch all pages of discussions (`?per_page=100&page=N`); filter to
   **unresolved only**.
3. For each unresolved discussion, capture:
   - Discussion ID and note ID
   - Author
   - File path and line number
   - Full comment body
   - Replies already posted in the thread

### Phase 2 — Deep assessment of each comment

For **every** unresolved comment, before touching any code:

1. **Is the feedback correct?**
   - Read the actual source code on the branch at the referenced lines.
   - Check types, schema, tests, and callers/consumers.
   - Verify the reviewer's claim against reality.

2. **Is it related to our changes?**
   - Only suggest fixes for comments directly related to code we changed.
   - Do NOT suggest fixes for unrelated files or major architectural changes
     outside our scope.

3. **Classify each comment:**
   - **Fix** — valid feedback on code we changed; requires a code edit.
   - **Reply** — question, clarification, or feedback that needs a
     contextual response but no code change.
   - **Dismiss** — feedback is incorrect or not applicable; suggest a
     polite reply explaining why.
   - **Escalate** — unclear or ambiguous; needs user clarification.

### Phase 3 — Present suggestion table (STOP HERE)

Present a summary table:

| # | Note ID | File:Line | Reviewer | Classification | Suggested Action |
|---|---------|-----------|----------|----------------|-----------------|

Then for each item, explain:
- **Fix items**: What should be changed, why the feedback is valid, and the
  proposed approach. Implement the fix immediately after presenting the table
  if the user says "go ahead" or equivalent — do NOT wait for explicit
  per-item approval unless the user asks.
- **Reply items**: The proposed reply text the user can copy-paste.
- **Dismiss items**: Why the feedback is not applicable and a proposed polite
  reply.
- **Escalate items**: What is unclear and what the user needs to decide.

**After presenting the table:**

When the user says "go ahead" or equivalent, treat that as approval to
implement only — no further confirmation at each step:

1. Implement all **Fix** items in code.
2. **Verify compilation and tests:**
   - Run the TypeScript compiler (or equivalent) on changed files to ensure
     no type errors were introduced or left unresolved.
   - Search for all callers/consumers of any renamed or removed symbol and
     update them before running the compiler.
   - Run the relevant test suite scoped to changed files; fix any failures
     before proceeding.
3. Stop. Remind the user to run `/commit-changes` to commit and push.

Do NOT commit, push, or monitor the pipeline — that is the user's next step
via `/commit-changes`. Do NOT post replies, resolve threads, or mark
discussions as resolved — the user does those themselves.

## Key Principles

- **Assess first, change second.** Never blindly implement reviewer feedback.
  Verify it against the actual code, types, and schema.
- **Implement fixes, leave replies to the user.** Apply code changes; let
  the user post replies and resolve threads themselves.
- **Scope to our changes.** Only fix comments on code we authored or
  modified. Suggest replies for out-of-scope comments.
- **Follow existing patterns.** Don't introduce new abstractions or
  workarounds. Stay consistent with the codebase.
- **Validate against schema/types.** When a comment is about nullability
  or type correctness, check the actual schema (OpenAPI, protobuf, etc.)
  before deciding.
