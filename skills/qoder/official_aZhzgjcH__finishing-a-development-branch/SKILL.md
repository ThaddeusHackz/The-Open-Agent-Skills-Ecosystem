---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Pre-flight CI parity → Detect environment → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 0: Update state.json

**On entry** — atomically update the topic's `.superpowers/topics/<NNN>-<slug>/state.json` so a fresh session resumes here. The executor sub-skill (`superpowers:subagent-driven-development` or `superpowers:executing-plans`) should already have set `next_action` to this skill; this step is a safety net for cold-pickup paths.

```bash
TOPIC_DIR="$(ls -dt .superpowers/topics/*/ 2>/dev/null | head -1)"
if [ -f "$TOPIC_DIR/state.json" ]; then
  jq '.next_action = "superpowers:finishing-a-development-branch" | .gate_open_from = null' \
    "$TOPIC_DIR/state.json" > "$TOPIC_DIR/state.json.tmp" \
    && mv "$TOPIC_DIR/state.json.tmp" "$TOPIC_DIR/state.json"
fi
```

**After Step 5 completes** (any option chosen) — atomically clear `next_action` so the topic stops pointing back here:

```bash
[ -f "$TOPIC_DIR/state.json" ] && \
  jq '.next_action = null | .gate_open_from = null' \
    "$TOPIC_DIR/state.json" > "$TOPIC_DIR/state.json.tmp" \
  && mv "$TOPIC_DIR/state.json.tmp" "$TOPIC_DIR/state.json"
```

Any GitHub-side state (PR open, issue closed via `Closes <url>`) is implied by `state.json.github_issue_url` plus the PR's merge state, not tracked locally. Schema lives in `superpowers:using-superpowers`.

### Step 1: Pre-flight CI Parity

**Before presenting options, run every check CI would run.** A passing test command was the old bar — the new bar is "if CI would catch it, catch it here." A PR that lands red on lint, typecheck, or build immediately after `gh pr create` defeats the point of the run; your human partner only learns about the failure when CI annotates the PR. The autonomous mode in particular has no other gate before push.

**Honest framing:** local pre-flight is best-effort, not a guarantee. CI runners can have a different OS, different dependency versions, services your laptop doesn't run, or secrets you don't have. The goal is to catch the *common* failures (lint, typecheck, build, unit tests) before pushing — not to make CI redundant.

#### 1a. Discover the check set

Use the helper that ships beside this skill (`./discover-ci-checks.sh`). It inspects `package.json` scripts (`test`, `lint`, `typecheck`, `build`, `check`, `ci`), `Makefile` targets of the same names, and `.github/workflows/*.yml` `run:` lines, filtering out installs, publishers, deployers, and lines that reference `${{ secrets.* }}`:

```bash
CHECKS="$(./discover-ci-checks.sh)"   # one command per line, deduped, sorted
```

If `$CHECKS` is empty — no `package.json`, no `Makefile`, no workflow files — fall back to the project's test command alone. This skill must never block a PR for a project that ships no CI-parity material:

```bash
[ -z "$CHECKS" ] && CHECKS="$(<your project's test command, e.g. npm test / cargo test / pytest / go test ./...>)"
```

#### 1b. Run every discovered check

```bash
FAILURES=()
while IFS= read -r cmd; do
    [ -z "$cmd" ] && continue
    if output=$(eval "$cmd" 2>&1); then
        echo "[PASS] $cmd"
    else
        FAILURES+=("$cmd")
        echo "[FAIL] $cmd"
        echo "$output" | tail -n 50
    fi
done <<< "$CHECKS"
```

**On all-green** (no entries in `FAILURES`): continue to Step 2.

#### 1c. Failures — interactive mode

If `state.json.autonomous` is `false` or absent, present the list and stop. Do not autofix without consent — your human partner picks which failures are real and which are infra noise:

```
Pre-flight failed:
- npm run lint  (12 ESLint errors in src/foo.ts)
- npm run typecheck  (4 TS errors after the recent refactor)

Tests passed. The PR would land red on CI. What do you want to do?
```

Wait for direction. Do not proceed to Step 2 until your human partner says so.

#### 1d. Failures — autonomous mode

If `state.json.autonomous` is `true`, run a **bounded autofix loop**:

1. For each failing command, dispatch an implementer subagent using the pattern from `superpowers:subagent-driven-development` (the addendum in that skill's `./implementer-prompt.md`). Give it the failing command, its captured output, and the goal: *make this command exit 0 without regressing the others.* The subagent commits its fix on the current branch.
2. After every fix attempt, **re-run the full check set** (Step 1b). One command's "fix" can break another.
3. **Hard ceiling: 3 rounds total.** "Just one more round" is the rationalization that lands red PRs anyway. Do not raise the ceiling under pressure.

If still red after round 3, **stop and hand back**. Do not push, do not open a PR. Write a digest sidecar so resume picks up cleanly:

```bash
TOPIC_DIR="$(ls -dt .superpowers/topics/*/ 2>/dev/null | head -1)"

{
  echo "# Pre-flight failures (after 3 autofix rounds)"
  echo
  for cmd in "${FAILURES[@]}"; do
    echo "## \`$cmd\`"
    echo
    echo '```'
    eval "$cmd" 2>&1 | tail -n 50
    echo '```'
    echo
  done
} > "$TOPIC_DIR/pre-flight-failures.md"

jq '.next_action = "superpowers:finishing-a-development-branch"
    | .gate_open_from = "superpowers:finishing-a-development-branch"' \
   "$TOPIC_DIR/state.json" > "$TOPIC_DIR/state.json.tmp" \
  && mv "$TOPIC_DIR/state.json.tmp" "$TOPIC_DIR/state.json"
```

End the run with: "Pre-flight blocked after 3 autofix rounds — see `pre-flight-failures.md`. Resume the topic when unblocked."

### Step 2: Detect Environment

**Determine workspace state before presenting options:**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

This determines which menu to show and how cleanup works:

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based (see Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options (no merge) | No cleanup (externally managed) |

### Step 3: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

**Autonomous mode.** If the topic's `state.json.autonomous` is `true`, do NOT ask. Use the auto-detected base branch above. If neither `main` nor `master` matches, treat as a hard blocker: append a `## Blocker` section to `.superpowers/topics/<NNN>-<slug>/assumptions.md` describing the missing base branch, set `gate_open_from = "superpowers:finishing-a-development-branch"` (preserve `next_action` and `autonomous`), and end the run with "Blocked at base-branch resolution — see `assumptions.md`. Resume the topic when unblocked."

```bash
jq '.gate_open_from = "superpowers:finishing-a-development-branch"' \
  "$TOPIC_DIR/state.json" > "$TOPIC_DIR/state.json.tmp" \
  && mv "$TOPIC_DIR/state.json.tmp" "$TOPIC_DIR/state.json"
```

### Step 4: Present Options

**Autonomous mode.** If the topic's `state.json.autonomous` is `true`, skip this menu entirely. Pre-flight verified in Step 1 (any failure short-circuits there); environment detected in Step 2; base branch resolved in Step 3. Default directly to **Option 2** (push + create PR) and proceed to Step 5. Your human partner reviews via the PR — that is the only checkpoint in autonomous mode.

If the menu is needed, choose by environment from Step 2.

**Normal repo and named-branch worktree — present exactly these 4 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Detached HEAD — present exactly these 3 options:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)
3. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>

# Only after merge succeeds: cleanup worktree (Step 6), then delete branch
```

Then: Cleanup worktree (Step 6), then delete branch:

```bash
git branch -d <feature-branch>
```

#### Option 2: Push and Create PR

**If the topic's `state.json.github_issue_url` is non-null**, the work originated from a GitHub issue (via `superpowers:publishing-issues` or `superpowers:receiving-issue`). Embed `Closes <issue-url>` in the PR body — GitHub natively links the PR to the issue and [auto-closes it on merge](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) into the default branch. No scripted `gh issue close`/`gh issue comment` needed.

First, resolve the current topic folder. Prefer the slug the current session has been working in — the agent knows this from context. If the session context has been cleared or the branch is being picked up cold, fall back to the most-recently-modified topic folder, and confirm with the user if more than one plausible candidate exists:

```bash
# Resolve current topic (most recently modified folder under .superpowers/topics/)
TOPIC_DIR="$(ls -dt .superpowers/topics/*/ 2>/dev/null | head -1)"

CLOSES_LINE=""
if [ -n "$TOPIC_DIR" ] && [ -f "$TOPIC_DIR/state.json" ]; then
  ISSUE_URL=$(jq -r '.github_issue_url // empty' "$TOPIC_DIR/state.json")
  [ -n "$ISSUE_URL" ] && CLOSES_LINE="Closes $ISSUE_URL"
fi

# Fold any documented assumptions (from autonomous-mode runs) into the PR body.
# If assumptions.md is absent or empty, the section is omitted entirely.
ASSUMPTIONS_SECTION=""
if [ -n "$TOPIC_DIR" ] && [ -s "$TOPIC_DIR/assumptions.md" ]; then
  ASSUMPTIONS_SECTION=$'## Assumptions\n\n'"$(cat "$TOPIC_DIR/assumptions.md")"$'\n'
fi
```

Before pushing, draft a reviewer-friendly title and body. The PR's job is to help reviewers — write so a reviewer reading nothing else gets the gist:

- **Title:** under 70 chars; imperative or summary style; derive from the branch's commits, not invented prose.
- **Summary:** scan the commits since base (`git log <base-branch>..HEAD --oneline`). Extract design intent and the *why* — not mechanics obvious from the diff. Call out non-obvious interactions or dependencies.
- **Test Plan:** distinguish what's already covered by automated tests from any manual step a reviewer should run.
- **Assumptions** (auto-included when `$ASSUMPTIONS_SECTION` is non-empty): folded from `.superpowers/topics/<NNN>-<slug>/assumptions.md`. Surfaces best-judgment calls made by the implementer in autonomous mode so reviewers can flag misinterpretations.
- **Risk** (optional): include only when there's something a reviewer should specifically watch — schema migrations, breaking API changes, perf-sensitive paths, security-sensitive code. Skip for routine changes; omit the section entirely.

Then push and create the PR, embedding `$CLOSES_LINE` and `$ASSUMPTIONS_SECTION` when present:

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR (unquoted EOF so variables expand; placeholders use <...> to avoid shell expansion)
gh pr create --title "<commit-derived title, under 70 chars>" --body "$(cat <<EOF
## Summary
<2-3 bullets: design intent and the why; not mechanics from the diff>

## Test Plan
- Automated: <what tests cover this; e.g., "Ran npm test; all pass">
- [ ] Reviewer manual check: <specific step, if any — omit this bullet when no manual step is needed>

$ASSUMPTIONS_SECTION
## Risk
<only when non-trivial: migrations, breaking changes, perf-sensitive paths; otherwise omit this section entirely>

$CLOSES_LINE
EOF
)"
```

Auto-close triggers when the PR merges into the repo's default branch. Works for any linked issue — milestone slice, bug report, feature request, etc. Milestones stay open until all their issues close — also handled natively by GitHub.

**Do NOT clean up worktree** — your human partner needs it alive to iterate on PR feedback.

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Then: Cleanup worktree (Step 6), then force-delete branch:
```bash
git branch -D <feature-branch>
```

### Step 6: Cleanup Workspace

**Only runs for Options 1 and 4.** Options 2 and 3 always preserve the worktree.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**If `GIT_DIR == GIT_COMMON`:** Normal repo, no worktree to clean up. Done.

**If worktree path is under `.worktrees/`, `worktrees/`, or `~/.config/superpowers/worktrees/`:** Superpowers created this worktree — we own cleanup.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**Otherwise:** The host environment (harness) owns this workspace. Do NOT remove it. If your platform provides a workspace-exit tool, use it. Otherwise, leave the workspace in place.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | yes | - |
| 3. Keep as-is | - | - | yes | - |
| 4. Discard | - | - | - | yes (force) |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Skipping pre-flight CI parity**
- **Problem:** Tests pass locally but CI also runs lint, typecheck, build — the PR opens, CI immediately turns red, and your human partner finds out from a failure badge instead of from you
- **Fix:** Run `./discover-ci-checks.sh` and execute every command before Step 2; in autonomous mode, autofix bounded at 3 rounds

**Raising the autofix ceiling under pressure**
- **Problem:** "One more round will get it" rationalizes past 3 rounds, then either takes 7 rounds or lands a red PR anyway
- **Fix:** 3 rounds is the hard ceiling — write `pre-flight-failures.md`, mark the topic blocked, hand back

**Open-ended questions**
- **Problem:** "What should I do next?" is ambiguous
- **Fix:** Present exactly 4 structured options (or 3 for detached HEAD)

**Cleaning up worktree for Option 2**
- **Problem:** Remove worktree your human partner needs for PR iteration
- **Fix:** Only cleanup for Options 1 and 4

**Deleting branch before removing worktree**
- **Problem:** `git branch -d` fails because worktree still references the branch
- **Fix:** Merge first, remove worktree, then delete branch

**Running git worktree remove from inside the worktree**
- **Problem:** Command fails silently when CWD is inside the worktree being removed
- **Fix:** Always `cd` to main repo root before `git worktree remove`

**Cleaning up harness-owned worktrees**
- **Problem:** Removing a worktree the harness created causes phantom state
- **Fix:** Only clean up worktrees under `.worktrees/`, `worktrees/`, or `~/.config/superpowers/worktrees/`

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Open a PR with red pre-flight (autonomous loop hits ceiling → stop, do not push)
- Raise the 3-round autofix ceiling under pressure
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Remove a worktree before confirming merge success
- Clean up worktrees you didn't create (provenance check)
- Run `git worktree remove` from inside the worktree

**Always:**
- Verify tests before offering options
- Run the full pre-flight check set (not just tests) before pushing or merging
- Detect environment before presenting menu
- Present exactly 4 options (or 3 for detached HEAD)
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only
- `cd` to main repo root before worktree removal
- Run `git worktree prune` after removal

## Integration

**Called by:**
- **superpowers:subagent-driven-development** (Step 7) - After all tasks complete
- **superpowers:executing-plans** (Step 5) - After all batches complete

**Dispatches:**
- **superpowers:subagent-driven-development** (autonomous mode only, Step 1d) - reuses the implementer-prompt pattern as the autofix subagent during the bounded pre-flight loop

**Pairs with:**
- **superpowers:using-git-worktrees** - Cleans up worktree created by that skill (when superpowers owns it)
- **superpowers:receiving-issue** - Reads `state.json.github_issue_url` under the topic folder and embeds `Closes <issue-url>` in the PR body so GitHub natively links the PR and auto-closes the issue on merge (milestones stay open until all their issues close — also handled natively)
