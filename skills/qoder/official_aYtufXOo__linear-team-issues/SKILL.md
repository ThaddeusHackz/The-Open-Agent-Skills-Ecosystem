---
name: linear-team-issues
description: Fetch Linear issues for a specific team using the Linear GraphQL API and produce a Markdown snapshot (non-completed tasks, titles, and details). Use when you need to pull all open tasks from Linear into a .md file for agile status review.
---

# Linear Team Issues Snapshot

## Goal
Produce a Markdown snapshot of all non-completed issues for a specific Linear team.

## Inputs
- Linear Personal API key in `LINEAR_API_KEY` (or pass `--api-key`)
- Team identifier (team name, key, or UUID)

## Run
```
python3 skills/linear-team-issues/scripts/linear_team_issues.py --team "Team Name"
```

## Options
- `--output path/to/file.md` (default: `project-status/linear-tasks-YYYY-MM-DD.md`)
- `--exclude-state completed` (repeatable; default excludes `completed`)
- `--page-size 100` (pagination size)
- `--desc-limit 400` (truncate descriptions; default 400 chars)
- `--full-description` (do not truncate)
- `--no-description` (skip descriptions)

## Output
Markdown file with:
- Header summary (team, filters, counts)
- Counts by state type and status
- Issues grouped by status with key fields (title, state, priority, assignee, project, labels, URL, short description)

## Notes
- The script fetches all non-completed issues regardless of time range.
- Archived issues are excluded by default by Linear unless explicitly requested.
