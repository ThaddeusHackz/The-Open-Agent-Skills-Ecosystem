#!/usr/bin/env bash
# Run a harvest python step, tee output to harvest-logs/, and on failure
# emit a GitHub annotation (readable via the REST API) with the log tail.
set -uo pipefail
SCRIPT="$1"; shift || true
mkdir -p harvest-logs
NAME="$(basename "$SCRIPT" .py)"
OUT="harvest-logs/${NAME}_stdout.txt"
python3 "$SCRIPT" "$@" 2>&1 | tee "$OUT"
ec=${PIPESTATUS[0]}
if [ "$ec" -ne 0 ]; then
  CONTEXT="disk: $(df -h . | tail -1 | awk '{print $4" free"}'); "
  CONTEXT+="files: $(find skills -name SKILL.md 2>/dev/null | wc -l) skills on disk; "
  TAIL="$(tail -n 14 "$OUT" | tr '\t' ' ' | tr '\n' '|' | cut -c1-1300)"
  echo "::error title=${NAME} failed (exit ${ec})::${CONTEXT}${TAIL}"
fi
exit "$ec"
