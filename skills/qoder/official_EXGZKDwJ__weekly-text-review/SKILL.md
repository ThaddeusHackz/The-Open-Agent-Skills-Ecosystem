---
name: weekly-text-review
description: "Code-delivery skill for the copyright review workflow. Use when Vibecode or an operator needs to keep text changes on a weekly `review/text-week-N` branch, roll that branch into a PR against `develop` after 7 days, then start the next weekly branch."
metadata:
  family: code
  owner: engineering
  last_reviewed: 2026-05-06
  version: 1.0.0
---
# Weekly Text Review

This is a code-family delivery skill for the Career Hub copyright-review loop.

## Use When

- the user asks to ship text edits onto the weekly review branch
- the user asks whether the current weekly branch should stay open or become a PR
- Vibecode is applying requested copy changes and needs the correct branch target

## Do Not Use When

- the task is creating brand-new Career Hub content from scratch
- the user wants a normal feature/fix branch that is not part of the weekly text-review cadence
- the user only wants PR wording; use `github-pr-workflow`

## Goal

Maintain exactly one active weekly review branch at a time:

- branch pattern: `review/text-week-N`
- base branch: `develop`
- rollover rule: once the active weekly branch is at least 7 days old, open its PR to `develop`, notify the user, then create the next weekly branch from latest `origin/develop`

## Required Sequence

### 1. Sync Remote State

Always fetch before deciding anything:

- `git fetch origin develop`
- `git fetch origin 'refs/heads/review/text-week-*'`

If `origin/develop` does not exist, create it from latest `origin/main` using the same fallback defined by `github-pr-workflow`.

### 2. Identify The Active Weekly Branch

List all remote weekly branches matching:

- `origin/review/text-week-N`

Rules:

1. parse `N` numerically
2. choose the highest `N` as the active weekly branch candidate
3. if no weekly branch exists, create `review/text-week-1` from `origin/develop`, push it, and use it as the active branch

Do not reuse calendar week numbers. `N` is a monotonically increasing sequence.

### 3. Measure Branch Age

Treat branch age as:

- the timestamp of the oldest commit that exists on the weekly branch and not on `origin/develop`

Practical method:

1. compute `git merge-base origin/develop origin/review/text-week-N`
2. inspect commits after that merge-base on the weekly branch
3. use the oldest unique commit timestamp as the branch creation proxy

Fallback:

- if the branch has no unique commits yet, treat it as not ready for rollover and keep using it

### 4. Decide Reuse vs Rollover

If branch age is less than 7 days:

- switch to the weekly branch locally
- push the requested text changes there
- do not open a PR yet
- notify the user which branch is still active and how many days remain until rollover

If branch age is 7 days or more:

1. switch to the weekly branch
2. verify the diff is still one reviewable weekly text batch
3. run relevant verification via `verification-checklist`
4. invoke `github-pr-workflow` to push/create the PR from `review/text-week-N` to `develop`
5. notify the user with the PR URL and branch name
6. fetch latest `origin/develop`
7. create `review/text-week-(N+1)` from `origin/develop`
8. push the new branch with upstream so future text requests land there
9. notify the user that the next weekly branch is ready

## Branch Rules

- never branch from local `develop` if `origin/develop` is available; branch from `origin/develop`
- never open the PR before the branch has reached the 7-day threshold unless the user explicitly overrides the cadence
- never mix unrelated non-text feature work into `review/text-week-N`
- never create multiple new weekly branches for the same rollover event

## PR Rules

When rollover is due, defer PR mechanics to `github-pr-workflow`.

Required PR shape:

- head: `review/text-week-N`
- base: `develop`
- scope: only that weekly text batch

PR summary should state:

- this branch contains that week's text/content edits for copyright review
- the next weekly branch has been created for incoming requests

## Notification Contract

After acting, always tell the user:

- active branch name
- whether the branch was reused or rolled over
- branch age in days
- PR URL when a PR was created
- next branch name when rollover happened

## Handy Commands

```bash
git fetch origin develop
git fetch origin 'refs/heads/review/text-week-*'
git branch -r --list 'origin/review/text-week-*'
git merge-base origin/develop origin/review/text-week-3
git log --reverse --format='%aI %H' <merge-base>..origin/review/text-week-3
git switch -c review/text-week-4 origin/develop
git push -u origin review/text-week-4
```
