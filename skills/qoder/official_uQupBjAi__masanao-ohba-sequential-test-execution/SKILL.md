---
name: sequential-test-execution
description: Invoke as a PreToolUse hook on Bash commands to prevent concurrent test runs. Detects running test containers before launching new test processes, blocking execution with feedback if another test is active to ensure isolation.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            COMMAND=$(echo "${TOOL_INPUT:-{}}" | jq -r '.command // empty')
            [[ -z "${COMMAND}" ]] && exit 0
            # テストコマンド判定
            echo "${COMMAND}" | grep -qE \
              'docker[ -]compose.*-f.*test.*run|phpunit|jest|pytest|composer test|npm test|^TEST_ONLY=' \
              || exit 0
            # 実行中テストコンテナ確認
            for f in docker-compose.test.yml docker-compose.test.yaml; do
              [[ -f "$f" ]] || continue
              RUNNING=$(docker compose -f "$f" ps --status running --format json 2>/dev/null \
                | jq -r 'select(.Service=="web") | .Name' 2>/dev/null || true)
              if [[ -n "$RUNNING" ]]; then
                echo "BLOCKED: Test container already running: $RUNNING" >&2
                echo "Wait for it to complete before starting another test run." >&2
                exit 2
              fi
            done
            exit 0
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            COMMAND=$(echo "${TOOL_INPUT:-{}}" | jq -r '.command // empty')
            [[ -z "${COMMAND}" ]] && exit 0
            echo "${COMMAND}" | grep -qE 'docker[ -]compose.*-f.*test.*run' || exit 0
            LOG_DIR="${TMPDIR:-/tmp}/claude-workflow"
            mkdir -p "${LOG_DIR}" 2>/dev/null || true
            EXIT_CODE=$(echo "${TOOL_OUTPUT:-{}}" | jq -r '.exit_code // "unknown"' 2>/dev/null || echo "unknown")
            echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Test done. Exit: ${EXIT_CODE}" \
              >> "${LOG_DIR}/test-execution.log" 2>/dev/null || true
            exit 0
---

# Sequential Test Execution

Ensures test runs execute one at a time to prevent resource conflicts.

## Core Principle

> **One Test Run at a Time**
>
> Test environments share databases, ports, and network resources.
> Concurrent test execution causes migration conflicts, port collisions,
> and flaky test results.

## Detection Method

Uses Docker container state (not file locks) to detect running tests:

- **Self-recovering**: `docker compose run --rm` auto-removes containers on exit
- **No stale locks**: `docker ps` reflects actual running state
- **Graceful degradation**: If Docker is unavailable, tests proceed normally

## Hook Behavior

### PreToolUse (Bash)

1. Extract command from `TOOL_INPUT`
2. Check if command is a test execution command
3. Query `docker-compose.test.yml` for running `web` containers
4. **Running container found** → `exit 2` (block with message)
5. **No running container** → `exit 0` (allow)

### PostToolUse (Bash)

1. Only triggers on `docker compose` test commands
2. Logs completion timestamp and exit code to `$TMPDIR/claude-workflow/test-execution.log`
3. Always `exit 0` (informational only)

## When Blocked

If a test run is blocked:

1. Wait for the existing test container to complete
2. Retry the test command after completion
3. Do NOT force-remove the running container

## Test Command Patterns Detected

```
docker compose -f docker-compose.test.yml run ...
phpunit
jest
pytest
composer test
npm test
TEST_ONLY=...
```
