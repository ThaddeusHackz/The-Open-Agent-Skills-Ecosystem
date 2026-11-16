---
name: issue-triage
description: Use when triaging GitHub security issues — fetch issues by number or range, classify as false positive or true positive, assess patch bypass and related-code vulnerabilities, and then label/retitle/open-close with a brief comment. Triggers on "validate issue N", "triage issues 189-199", "check if issue is exploitable", "close false positive issues".
---

# Issue Triage

End-to-end workflow: fetch -> restate -> security-relationship gate -> fp-check -> bypass/related-code check -> verdict -> one canonical comment.

## Prerequisites

- `gh` CLI authenticated to the target repo
- `/fp-check` skill available at `~/.agents/skills/fp-check/SKILL.md`

## Step 1 — Fetch Issues

```bash
# Single issue
gh api repos/{owner}/{repo}/issues/{number}

# Fetch comments
gh api repos/{owner}/{repo}/issues/{number}/comments
```

Collect for each issue: `number`, `title`, `labels`, `state`, `body`, all comments, upstream repo, commit/PR references, severity labels, and duplicate indicators.

Review requirement: always read **all existing comments** before classifying. Treat them as context, not source of truth.

Duplicate handling:
- Mark as duplicate if it has the `duplicate` label, or an owner-authored `Duplicate of #N` / `Duplicate with #N` comment.
- Skip duplicate issues entirely unless the user explicitly asks to reconcile duplicates.
- Also cluster issues by the same upstream commit, PR, or advisory. If two issues track the same upstream fix, treat them as one underlying case even when labels/comments are inconsistent.

One-comment policy:
- Every triaged issue must end with exactly one canonical verdict comment.
- Look for an existing owner-authored comment marked `<!-- vsa:final-verdict -->` and update it in place.
- If the marker does not exist, prefer editing the existing owner-authored verdict comment into the canonical form.
- Create a new verdict comment only if there is no reusable verdict comment.
- After the canonical comment is updated, delete superseded owner-authored verdict comments so the issue ends with one verdict comment only.

## Step 2 — Restate the Claim

Before analysis, restate the issue in one sentence.

Record:
- Exact vulnerability claim
- Root cause
- Trigger
- Claimed impact
- Threat model: authenticated vs unauthenticated, remote vs local, same-user vs cross-user

If the claim cannot be restated clearly, default to skepticism and verify whether there is a real security assertion at all.

## Step 3 — Security Relationship Gate

Before `fp-check`, answer these questions in writing:
1. What attacker-controlled input exists at runtime?
2. Which execution context is affected: browser, server, worker, CLI, desktop, CI, test, build-time, or admin-only control plane?
3. What trust boundary is crossed?
4. Is the impact cross-user, cross-tenant, cross-privilege, or only same-user correctness/state?
5. Is the vulnerable dependency or code path actually reachable in this repo's deployment model?
6. Is this the same upstream fix as another issue or part of an introduce-then-fix pair in one PR?

If you cannot identify attacker control, a reachable runtime path, and a crossed trust boundary, the default outcome is `FALSE POSITIVE` unless later evidence proves otherwise.

Treat the following as **non-security by default** unless the issue demonstrates a real boundary break:
- Documentation, examples, release tooling, CI, test-only, or dev-only changes
- Dependency bumps where the vulnerable package is not used in the affected runtime
- Browser-only dependency usage for Node/server CVEs, or Node-only usage for browser CVEs
- Build-time or source-controlled route scanning, codegen, filename parsing, or packaging logic
- Admin safety, data-loss prevention, migration robustness, retry/deadlock hardening, or operational correctness fixes
- Framework semantics or path-matching correctness changes without a concrete exploit path
- Same-user UI, cache, or state-resurrection bugs with no cross-user or cross-tenant effect
- Local contexts where the attacker already has equivalent code execution

Proceed only when the issue has a genuine security relationship.

## Step 4 — fp-check the Security Issue

Follow `/fp-check` for each issue that survives Step 3.

Routing:
- Standard verification: clear claim, single component, well-understood bug class
- Deep verification: ambiguous claim, concurrency, cross-component flow, logic/state-machine bug, spec-sensitive behavior

Always fetch the actual patch diff before concluding:

```bash
gh api repos/{owner}/{repo}/commits/{sha} --jq '.files[] | {filename, patch}'
# or
gh pr view {pr} --repo {owner}/{repo} --json files
```

Do not rely on the issue description alone.

Mandatory reachability checks:
- Confirm the vulnerable code path is invoked in the claimed runtime
- Confirm attacker-controlled input reaches the sink or security decision
- Confirm the issue is not only a dependency/advisory mismatch with no in-repo execution path
- Confirm the bug is not only an implementation-correctness fix with no security boundary impact

## Step 5 — Bypass and Related-Code Validation

For issues tied to a patch, validate both:
- whether the patch can be bypassed, and
- whether related code still exposes a valid vulnerability even if the patch path is sound.

Before concluding on bypass, gather enough context to answer:
1. What feature or guarantee is the patch protecting?
2. Which controls does the patch add?
3. Which callers, siblings, alternate parsers, defaults, or compatibility branches are still outside the patch?
4. Is the patch active in the default configuration?
5. Does a relevant standard or RFC require broader protection?

Mandatory related-code checks:
1. Sibling endpoints/handlers reaching the same sink
2. Alternate input forms/parsers that miss patched normalization
3. Shared helpers with unpatched callers
4. Default/fallback/spec-backcompat branches
5. Config-gated protections that are disabled by default

Verdict mapping:
- Bypass confirmed -> `TRUE POSITIVE (bypass confirmed)`
- Patch sound, related path still vulnerable -> `TRUE POSITIVE (related-code vulnerability)`
- Patch sound, no related vulnerability -> `Closed`
- No security relationship or no reachable exploit path -> `FALSE POSITIVE`

If the issue is a patch-advisory mismatch only, do not force it into bypass analysis.

## Step 6 — Verdict and Issue Action

| Verdict | Action |
|---------|--------|
| `FALSE POSITIVE` | Add `false-positive`; close |
| `TRUE POSITIVE (bypass confirmed)` | Keep open; add `bypass-possible` |
| `TRUE POSITIVE (related-code vulnerability)` | Keep/reopen; retitle to `Potential Vulnerability Detected`; replace `finding:patch` with `finding:vuln` |
| `Closed` | Close; keep severity labels only if still accurate |

Additional rules:
- Correct severity labels when the reviewed impact does not match the issue labels.
- Do not use `true-positive`, `vulnerable`, `vulnerability`, or workflow labels.
- If one commit introduced the bug and a later commit in the same PR fixes it, note the timeline explicitly instead of treating both commits as separate vulnerabilities.

Useful commands:

```bash
gh issue edit {number} --repo {owner}/{repo} --add-label "false-positive"
gh issue edit {number} --repo {owner}/{repo} --add-label "bypass-possible"
gh issue edit {number} --repo {owner}/{repo} --remove-label "finding:patch" --add-label "finding:vuln"
gh issue edit {number} --repo {owner}/{repo} --title "[Potential Vulnerability Detected] {source-repo}: {vulnerability type}"
gh issue reopen {number} --repo {owner}/{repo}
gh issue close {number} --repo {owner}/{repo}
gh api repos/{owner}/{repo}/issues/{number}/comments --jq '.[] | {id, user: .user.login, body}'
gh api repos/{owner}/{repo}/issues/comments/{comment_id} -X PATCH --input comment.json
gh api repos/{owner}/{repo}/issues/{number}/comments -X POST --input comment.json
gh api repos/{owner}/{repo}/issues/comments/{comment_id} -X DELETE
```

## Step 7 — Canonical Comment

Keep comments short and evidence-based. Do not paste full analysis.

The final issue thread must contain exactly one canonical verdict comment marked `<!-- vsa:final-verdict -->`.

Preferred template:

```markdown
<!-- vsa:final-verdict -->
**Verdict:** <FALSE POSITIVE | TRUE POSITIVE (bypass confirmed) | TRUE POSITIVE (related-code vulnerability) | Closed>

**Reason:** <1-2 short sentences tied to code, runtime reachability, and trust boundary>
```

Bypass-confirmed template:

```markdown
<!-- vsa:final-verdict -->
**Verdict:** TRUE POSITIVE (bypass confirmed)

**Reason:** <why the patched control can still be avoided>

**How the bypass works:** <concrete path>

**PoC:**
```text
<minimal reproducible request, payload, or steps>
```
```

Requirements:
- A bypass-confirmed verdict must explain the surviving path and include a concrete PoC or practical attack steps.
- If a PoC cannot be safely provided, explicitly state the limitation.
- Update the existing marked comment instead of posting a new verdict comment.

## Step 8 — Summary

After the batch, report:
- Total issues reviewed
- `FALSE POSITIVE` count
- `Closed` count
- `TRUE POSITIVE (bypass confirmed)` count
- `TRUE POSITIVE (related-code vulnerability)` count
- Severity corrections
- Duplicate issues skipped
