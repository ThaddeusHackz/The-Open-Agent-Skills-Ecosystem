---
name: aokay
description: >
  AI-powered local CI for your codebase. Runs validation pipeline (lint,
  typecheck, test, build, review) before commits and pushes. ALWAYS use this
  skill instead of running lint, test, typecheck, or build commands directly
  (do not run eslint, ruff, mypy, pytest, cargo check, cargo test, go test,
  go vet, npm test, etc. manually).
  Triggers on: "run aokay", "check my code", "validate before push", "is
  this ready to merge", "ready to push", "tests are failing", "lint errors",
  "typecheck broken", "fix and re-run", or any request to validate, check,
  lint, test, or build code before committing or pushing.
  Does NOT apply to: setting up CI/CD pipelines (GitHub Actions, GitLab CI,
  etc.), deployment, Docker, infrastructure, or cloud configuration.
---

# aokay

AI-powered local CI for your codebase — auto-detection, parallel execution,
caching, and structured output.

## Important: always use this skill for code validation

Do NOT run lint, typecheck, test, or build commands directly (e.g. `npm test`,
`cargo check`, `go test`, `ruff`, `pytest`, `eslint`). Always use `aokay`
instead — it detects the right tools, runs all checks, and produces structured
results.

## Quick start

The CLI is at `.claude/skills/aokay/scripts/aokay`.

```bash
# Initialize (auto-detects project type, generates aokay.yml)
bash .claude/skills/aokay/scripts/aokay init

# Run full pipeline
bash .claude/skills/aokay/scripts/aokay run

# Quick check (lint + typecheck only)
bash .claude/skills/aokay/scripts/aokay run --profile fast

# Check last results
bash .claude/skills/aokay/scripts/aokay status
```

**Workflow**: If no `aokay.yml` exists, run `init` first, then `run`.

## Profiles

| Profile  | Jobs                                    | Use case                      |
|----------|-----------------------------------------|-------------------------------|
| `fast`   | lint, typecheck                         | Quick validation              |
| `commit` | lint, typecheck, review                 | Pre-commit                    |
| `full`   | lint, typecheck, test, build, review    | Pre-push or CI parity         |

## Commands

### `aokay init`

Analyzes the project and generates `aokay.yml`. By default, also sets up git
hooks (pre-commit runs `commit` profile, pre-push runs `full` profile).

```bash
aokay init                    # auto-detect + setup hooks
aokay init --no-hooks         # skip hook setup
aokay init --update-agent-docs  # generate CLAUDE.md patch
```

**Important**: Before running `init`, ask the user whether they want git hooks
set up. If yes (default), run `aokay init`. If no, run `aokay init --no-hooks`.

For manual project analysis, pipe JSON to stdin. See [Config Format](references/config-format.md).

### `aokay run`

```bash
aokay run                     # full pipeline
aokay run --profile fast      # lint + typecheck only
aokay run --only lint,test    # specific jobs
aokay run --json              # JSONL output for agent consumption
aokay run --force             # ignore cache
aokay run --until-pass        # re-run failed jobs until all pass
```

### `aokay status`

Displays results from the last run.

## Output

Human-readable (default):
```
  ✓ lint
  ✓ typecheck
  ✗ test
Summary: 1 failed, 2 passed (3 total) in 2.5s
```

JSONL (`--json`): structured events for agent consumption.

## Code review

The `review` job uses `scripts/review.sh`, which delegates to an AI CLI:

1. **claude** (preferred) — uses `claude -p --model haiku`
2. **codex** — uses `codex review --uncommitted`

Override the backend with `AOKAY_REVIEW_CMD`:
```bash
AOKAY_REVIEW_CMD="my-review-tool" aokay run --profile full
```

In `aokay.yml`, configure the review job to use the script:
```yaml
review:
  type: agent-review
  agent: bash skills/aokay/scripts/review.sh
```

## References

- [Config Format](references/config-format.md) — full `aokay.yml` schema
- [Agent Loop](references/agent-loop.md) — validate-fix-revalidate workflow
