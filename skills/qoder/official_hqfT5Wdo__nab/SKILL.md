---
name: nab
description: >
  Manage YNAB (You Need A Budget) budgets, accounts, categories, and
  transactions using the nab CLI. Use when the user wants to review spending,
  set up or adjust a budget, create or categorize transactions, check account
  balances, or interact with YNAB data in any way — even if they say "budget"
  or "finances" without mentioning YNAB or nab directly.
compatibility: Requires the nab CLI binary and a YNAB API access token.
metadata: { "author": "gtg922r", "version": "0.1.0", "openclaw": { "requires": { "bins": ["nab"], "env": ["YNAB_ACCESS_TOKEN"] }, "primaryEnv": "YNAB_ACCESS_TOKEN", "homepage": "https://github.com/gtg922r/nab" } }
---

# nab — YNAB CLI for Agents

nab is an agent-first CLI client for the YNAB API. It outputs structured JSON by default, supports schema introspection, and provides dry-run safety rails for all mutations.

## Setup

Authenticate with a YNAB access token:

```bash
export YNAB_ACCESS_TOKEN="your-token"  # env var (preferred)
nab auth setup                          # or interactive config
nab auth status                         # verify
```

## Safety Rules

These are non-negotiable. Violating them risks data loss.

1. **Always `--dry-run` before mutations.** Run the command with `--dry-run` first, show the user what will happen, then re-run without it.
2. **Always confirm with the user** before executing creates, updates, or deletes.
3. **Use `--fields` to limit output.** Large budgets return megabytes of JSON — select only the fields you need.
4. **Never fabricate IDs.** Always look up real IDs from list commands first.
5. **Dates must be `YYYY-MM-DD`.** No other format is accepted.

## Command Structure

```
nab [global-flags] <resource> <action> [flags]
```

### Global Flags

| Flag | Short | Default | Purpose |
|------|-------|---------|---------|
| `--budget` | `-b` | `last-used` | Budget ID or `last-used` |
| `--output` | `-o` | `json` | `json`, `table`, `csv`, `ndjson` |
| `--fields` | | | Comma-separated field filter |
| `--dry-run` | | `false` | Preview mutations without executing |
| `--yes` | `-y` | `false` | Skip confirmation prompts |
| `--quiet` | `-q` | `false` | Suppress non-essential output |

### Resources

| Resource | Actions | Notes |
|----------|---------|-------|
| `budget` | `list`, `get`, `settings` | Start here to find budget IDs |
| `account` | `list`, `get`, `create` | Needed for transaction creation |
| `category` | `list`, `get`, `create`, `update`, `budget` | `budget` sets monthly allocation |
| `transaction` | `list`, `get`, `create`, `update`, `delete`, `import` | Core CRUD + bank import |
| `payee` | `list`, `get`, `update` | Name management |
| `month` | `list`, `get` | Monthly budget snapshots |
| `scheduled` | `list`, `get`, `create`, `update`, `delete` | Recurring transactions |
| `schema` | `list`, `<resource>` | Introspect field definitions |
| `config` | `show`, `set` | Configuration management |
| `auth` | `setup`, `status` | Authentication |

## Amount Convention

- **JSON output and `--json` payloads**: milliunits (API native). `$50.00` = `50000`. Outflows are negative.
- **Convenience flags** (`--amount`): currency units. `--amount 50` = $50.00.
- **Table output**: formatted currency for display.

| Dollars | Milliunits |
|---------|------------|
| $1.00 | 1000 |
| $50.00 | 50000 |
| -$25.50 | -25500 |
| $1,000.00 | 1000000 |

## Quick Patterns

### Start a session

```bash
nab budget list --fields id,name
nab account list --fields id,name,type,balance
```

### Create a transaction

```bash
# 1. Look up IDs
nab account list --fields id,name
nab category list --fields id,name

# 2. Dry-run
nab transaction create --dry-run --json '{
  "account_id": "<uuid>",
  "date": "2024-01-15",
  "amount": -50000,
  "payee_name": "Grocery Store",
  "category_id": "<uuid>"
}'

# 3. Execute after user confirms
nab transaction create --json '{...}'
```

### Review spending

```bash
nab transaction list --since 2024-01-01 --fields date,payee_name,category_name,amount
nab month get 2024-01 --fields name,budgeted,activity,balance
```

### Set a category budget

```bash
nab category budget <category-id> 2024-02-01 500 --dry-run
nab category budget <category-id> 2024-02-01 500
```

### Introspect before acting

```bash
nab schema transaction   # See all fields, endpoints, examples
nab schema list           # List all available schemas
```

### Delta polling (efficient change detection)

```bash
nab transaction list --since-last   # First call fetches all, stores server_knowledge
nab transaction list --since-last   # Subsequent calls return only changes
```

## Gotchas

- `budget get` without `--fields` returns the **entire budget** — can be very large. Always use `--fields`.
- Category `list` returns categories **nested inside groups**. Flatten with jq: `jq '.data.category_groups[].categories[]'`
- Month argument for `category budget` must be first-of-month: `2024-02-01`, not `2024-02`. Month argument for `month get` is `YYYY-MM`.
- `--since-last` cannot combine with `--account`, `--category`, or `--payee` filters.
- Credit card balances are typically **negative** (they represent debt).
- Hidden/deleted items are included in list responses. Filter with jq: `select(.hidden == false and .deleted == false)`.
- `to_be_budgeted` in month data is your "Ready to Assign" amount.

## Error Handling

```json
{"error": {"code": "404.2", "type": "resource_not_found", "message": "...", "hint": "..."}}
```

Exit codes: 0=success, 1=general, 2=auth, 3=validation, 4=API error, 5=not found.

## When to Load References

- Read [commands reference](references/commands.md) for detailed flags, fields, and examples for a specific resource.
- Read [workflows reference](references/workflows.md) for multi-step spending review or budget setup procedures.
- Read [schemas reference](references/schemas.md) for complete field definitions, account types, goal types, and create/update payloads.
