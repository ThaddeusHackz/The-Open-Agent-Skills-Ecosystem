---
name: issue-sprint
description: Rapid iteration on GitHub issues — prioritize, create worktrees, generate prompts for subagents, review PRs, merge, repeat. Use when the user wants to work through multiple issues quickly, says "let's sprint", "batch these issues", or wants to parallelize work across multiple agents.
---

# Issue Sprint

You orchestrate rapid iteration on GitHub issues by:
1. Prioritizing issues
2. Setting up isolated worktrees
3. Generating detailed prompts for subagents
4. Reviewing and merging PRs
5. Cleaning up and moving to next

## Prerequisites

```bash
which gh || echo "Install GitHub CLI: https://cli.github.com/"
git --version
```

## Workflow

### 1. Survey Open Issues

```bash
gh issue list --state open
```

Present issues in a table with priority recommendation:

| Priority | # | Title | Why |
|----------|---|-------|-----|
| 1 | 4 | Bug: X crashes | Bugs first |
| 2 | 7 | Health endpoint | Production needs |
| ... | | | |

**Prioritization heuristics:**
- Bugs before features
- Infrastructure before features (health, logging, auth)
- Security issues high priority
- Dependencies: what unblocks other work
- Quick wins: high value, low effort

Ask user to confirm or reorder.

### 2. Set Up Worktree

For each issue the user wants to work on:

```bash
cd <main-repo>
git worktree add ../<repo>-issue-<N> -b issue-<N>-<short-desc>
gh issue view <N>
```

### 3. Generate Subagent Prompt

Create a detailed prompt for the agent working in the worktree. Structure:

```markdown
# Task: Implement Issue #N — <Title>

## Context

You're working in `<worktree-path>` on branch `<branch-name>`.

<Brief project context>

## The Issue

<Copy issue body>

## Reference Implementation (if any)

<Path to similar code or docs to read first>

## Key Files

- `path/to/file.ts` — description
- `path/to/other.ts` — description

## Implementation Approach

### 1. Step One
<Detailed instructions>

### 2. Step Two
<Detailed instructions>

## Constraints

- Run `<test-command>` to verify changes
- Add tests for new functionality
- Keep changes minimal and focused

## Definition of Done

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests pass
- [ ] Ready for PR

Closes #N
```

**Prompt quality matters.** Include:
- Exact file paths
- Reference code to read first
- Step-by-step approach
- Test commands
- Clear done criteria

Copy to clipboard:
```bash
cat << 'EOF' | pbcopy
<prompt>
EOF
echo "Prompt copied to clipboard"
```

### 4. Track Active Work

Maintain mental model of:
- Which worktrees are active
- Which issues are in progress
- Which PRs are pending review

When user asks "what's next" or "status", show:

| Issue | Branch | Worktree | Status |
|-------|--------|----------|--------|
| #4 | issue-4-recovery | ../repo-issue-4 | PR #20 open |
| #7 | issue-7-health | ../repo-issue-7 | In progress |

### 5. Review PRs

When user shares a PR URL:

```bash
gh pr view <N> --json title,body,state,additions,deletions,files
gh pr diff <N>
```

Review checklist:
- Does it close the issue requirements?
- Code quality (types, error handling, tests)
- Any missing pieces?
- Any bugs or issues?

Provide structured review:
```markdown
## PR Review: #N — <Title>

### ✅ What's Good
- Point 1
- Point 2

### ⚠️ Issues (if any)
- Issue 1
- Issue 2

### Summary
**LGTM** or **Changes needed**
```

### 6. Merge and Cleanup

When PR is approved:

```bash
cd <main-repo>
gh pr merge <N> --squash --delete-branch
git worktree remove ../<worktree-dir>
git branch -d <branch-name> 2>/dev/null
git pull
```

Always in this order — merge deletes remote branch, then remove worktree, then delete local branch.

### 7. Loop

After cleanup, immediately ask: "What's next?"

Show remaining issues and offer to set up the next one.

## Parallel Work

Multiple worktrees can be active simultaneously:
- Set up worktree + prompt for issue A
- While A is being worked on, set up B
- Review A's PR while B is in progress
- Merge A, check on B, set up C

The user orchestrates multiple agents — you help them context-switch efficiently.

## Commands Reference

```bash
# Issues
gh issue list --state open
gh issue view <N>
gh issue close <N> --comment "Fixed in #<PR>"

# Worktrees
git worktree add ../<name> -b <branch>
git worktree list
git worktree remove ../<name>

# PRs
gh pr view <N> --json title,body,files
gh pr diff <N>
gh pr merge <N> --squash --delete-branch
gh pr review <N> --approve --body "LGTM"
gh pr comment <N> --body "Comment"

# Sync
git pull
git fetch
```

## Tips

- **Batch similar issues** — auth issues together, then logging, etc.
- **Quick wins first** — builds momentum
- **Detailed prompts** — 5 min writing saves 30 min debugging
- **Review fast** — don't let PRs pile up
- **Clean as you go** — remove worktrees immediately after merge
