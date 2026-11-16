---
name: code-review-checklist
description: Review code changes for correctness, security, compatibility, maintainability, and missing tests. Use when asked to review a diff, pull request, patch, or implementation before merge.
---

# Code Review Checklist

## Workflow

1. Inspect the changed files and nearby code paths before judging the diff.
2. Prioritize correctness, data loss, security, compatibility, and user-visible regressions.
3. Use `references/review-rubric.md` when a structured severity rubric is needed.
4. Run `scripts/list_changed_files.sh` when a Git workspace is available and the user wants a quick changed-file inventory.
5. Return findings first, ordered by severity, with file and line references when available.
6. Include missing tests and residual risk after the findings.
