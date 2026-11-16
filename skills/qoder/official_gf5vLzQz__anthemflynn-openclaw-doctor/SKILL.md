---
name: openclaw-doctor
version: 2.0.0
description: "Comprehensive OpenClaw diagnostic audit — an agent-on-agent health check. Use when asked to check system health, diagnose issues, or audit OpenClaw subsystems. Covers gateway, security, channels, models, memory, context, heartbeat, hooks, skills, workspace integrity, and network."
user-invocable: true
argument-hint: "<domain or issue to focus on>"
context: fork
allowed-tools: Bash(openclaw *), Bash(tailscale *), Bash(launchctl list*), Bash(stat *), Bash(du *)
---

!openclaw status --all 2>&1 | head -20
!openclaw gateway status 2>&1 | head -10

# OpenClaw Doctor — Comprehensive Diagnostic Audit

You are an agent diagnosing another agent's infrastructure. Run a full 10-domain audit, classify every finding by severity, and produce a structured report with actionable fixes.

**This skill is read-only — never apply fixes, only recommend them.**

## Quick Start

1. Track progress through all 10 domains using the checklist
2. Run each domain's commands, interpret output, classify findings
3. Consult `references/config-reference.md` for recommended values
4. Consult `references/severity-rules.md` for classification rules
5. Present the unified **Health Report** at the end

## Audit Checklist

```
- [ ] Domain 1: Gateway Health
- [ ] Domain 2: Security
- [ ] Domain 3: Channels
- [ ] Domain 4: Auth & Models
- [ ] Domain 5: Memory System
- [ ] Domain 6: Context & Compaction
- [ ] Domain 7: Heartbeat & Cron
- [ ] Domain 8: Hooks & Skills
- [ ] Domain 9: Workspace Integrity
- [ ] Domain 10: System & Network
```

---

## Audit Protocol

Run all 10 domains. Collect findings. Never stop early — the full picture matters.

### Domain 1 — Gateway Health

```bash
openclaw status --all
openclaw gateway status
openclaw update status
```

**Evaluate:**
- Gateway service loaded, running, PID alive
- Latency < 500ms
- Version current vs latest (> 5 behind = WARN, not running = CRITICAL)
- Port 18789 responding, no "Address already in use"

### Domain 2 — Security

```bash
openclaw security audit --deep
stat -f "%Lp %N" ~/.openclaw/openclaw.json
stat -f "%Lp %N" ~/.openclaw/auth-profiles.json
stat -f "%Lp %N" ~/.openclaw/credentials/ 2>/dev/null
stat -f "%Lp %N" ~/.openclaw/state/ 2>/dev/null
```

**Evaluate:**
- Security audit critical/warning/info counts
- Config files should be 600 (not 644 = CRITICAL)
- Credentials/state dirs should be 700
- API keys hardcoded in config vs env vars
- Gateway token auth enabled (no auth = WARN)

### Domain 3 — Channels

```bash
openclaw channels status --probe
```

**Evaluate:**
- Per-channel: enabled / configured / running / probe passes
- Probe failure on configured channel = CRITICAL
- No channels at all = WARN
- DM policy open vs pairing (open = INFO)

### Domain 4 — Auth & Models

```bash
openclaw models status --probe
```

**Evaluate:**
- Primary model probe succeeds (fail = CRITICAL)
- Fallback models configured (none = WARN)
- Image model configured (none = WARN)
- Sub-agent model set to cheaper model (same as primary = INFO)
- Single provider, no diversity = INFO

### Domain 5 — Memory System

```bash
openclaw memory status --deep
openclaw config get agents.defaults.compaction.memoryFlush
openclaw config get agents.defaults.memorySearch
```

**Evaluate:**
- Index health: dirty flag, chunk count, file count
- Flush enabled with thresholds (disabled = WARN)
- Dirty index + 0 chunks = WARN (broken)
- Memory search provider configured (none = WARN)
- Agent name in index matches current agent (mismatch = WARN)

### Domain 6 — Context & Compaction

```bash
openclaw config get agents.defaults.contextPruning
openclaw config get agents.defaults.compaction
```

**Evaluate against `references/config-reference.md`:**
- Pruning mode set (none = WARN; adaptive recommended)
- `keepLastAssistants` set (unset = INFO)
- `reserveTokensFloor` >= 20000 (< 20000 = WARN)
- `memoryFlush.softThresholdTokens` in 4000-8000 (outside = INFO)

### Domain 7 — Heartbeat & Cron

```bash
openclaw config get agents.defaults.heartbeat
openclaw cron list
openclaw cron status
```

Read `~/.openclaw/workspace/HEARTBEAT.md` to check if it has actual tasks.

**Evaluate:**
- Heartbeat enabled + HEARTBEAT.md empty = WARN (burning tokens)
- Heartbeat interval >= pruning TTL = WARN (cache expires before heartbeat)
- Cron scheduler not running when jobs exist = WARN
- No heartbeat / no cron = INFO (may be intentional)

### Domain 8 — Hooks & Skills

```bash
openclaw hooks list
openclaw skills list
openclaw plugins list
```

**Evaluate:**
- Hooks: count ready vs error (errors = WARN)
- Skills: count ready vs blocked vs disabled
- Plugins: loaded vs error (errors = WARN)
- Many skills blocked by same missing dep = INFO

### Domain 9 — Workspace Integrity

Check `~/.openclaw/workspace/` for required files:

| File | Required | Missing = |
|------|----------|-----------|
| AGENTS.md | Yes | CRITICAL |
| SOUL.md | Yes | CRITICAL |
| USER.md | Yes | CRITICAL |
| SESSION-STATE.md | Yes | CRITICAL |
| IDENTITY.md | Yes | CRITICAL |
| TOOLS.md | Yes | CRITICAL |
| HEARTBEAT.md | Yes | CRITICAL |
| BOOTSTRAP.md | **No** (should be absent) | WARN if present |

**Additional checks:**
- IDENTITY.md filled in vs template placeholders (template = WARN)
- Config backup accumulation (`~/.openclaw/openclaw.json.bak*` > 5 = INFO)

### Domain 10 — System & Network

```bash
tailscale status
tailscale serve status 2>/dev/null
launchctl list 2>/dev/null | grep openclaw
du -sh ~/.openclaw/
du -sh ~/.openclaw/logs/ 2>/dev/null
```

**Evaluate:**
- Tailscale daemon running, version match (mismatch = WARN)
- LaunchAgent loaded
- Log dir total size (> 10MB error log = WARN)
- Total `.openclaw/` disk usage (> 1GB = WARN)

---

## Report Template

After all 10 domains, present this:

```markdown
## OpenClaw Health Report — {YYYY-MM-DD}

**Version:** {from status --all}  |  **Gateway:** {running/stopped}  |  **Uptime:** {if available}

### Summary
| Severity | Count |
|----------|-------|
| CRITICAL | N     |
| WARNING  | N     |
| INFO     | N     |
| PASS     | N     |

### Findings

#### CRITICAL
- [C1] {Domain}: {finding} — `{fix command}`

#### WARNING
- [W1] {Domain}: {finding} — `{fix command}`

#### INFO
- [I1] {Domain}: {finding} — {recommendation}

#### PASS
- {Domain}: All checks passed

### Value-Add Opportunities
- {opportunity} — {impact} — {effort estimate}

### Quick Fix Script
```bash
# Review before running — generated from CRITICAL and WARNING findings
{fix commands, one per line, commented with finding ID}
```
```

**Report rules:**
- Every domain appears (findings or PASS)
- CRITICAL and WARNING include fix commands
- INFO includes recommendations
- Quick Fix Script only has CRITICAL + WARNING fixes
- Note when a fix should use `openclaw-admin` change discipline

---

## Execution Guidelines

- **Parallel where possible:** Run independent commands together
- **Platform awareness:** On Linux use `stat -c "%a %n"` instead of `stat -f "%Lp %N"`
- **Graceful failures:** If a command fails, note as INFO and continue — never abort
- **No mutations:** Never run `config set`, `--fix`, `gateway restart`, or any write operation
- **Cross-reference:** Use `references/config-reference.md` and `references/severity-rules.md`

## References

- `references/config-reference.md` — Recommended values, file permissions, CLI commands
- `references/severity-rules.md` — Classification rules for CRITICAL/WARNING/INFO/PASS

## Related Skills

- **`openclaw-admin`** — Apply fixes using verify-apply-verify-restart-test discipline
- **`openclaw-maintain`** — Daemon ops, updates, cron, log rotation
- **`openclaw-extend`** — Add plugins, channels, nodes, webhooks
