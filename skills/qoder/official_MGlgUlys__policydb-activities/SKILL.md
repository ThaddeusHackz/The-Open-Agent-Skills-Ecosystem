---
name: policydb-activities
description: >
  Open Items, activities, and Action Center reference for PolicyDB. Use when working on
  the open_items work tracker, activity logging, bucket transitions, multi-policy linking,
  source promotion (anomaly/inbox/suggestion → open item), the Action Center bucket panel,
  or any code that touches open_items / open_item_policies / activity_log.
---

# Open Items & Activity System

PolicyDB has two tables that work together:

| Table | Role |
|-------|------|
| `open_items` | Central **work tracker** — every issue, follow-up, todo, milestone is one row. Workflow stage = bucket membership. |
| `activity_log` | **Historical thread** — past calls, emails, notes, meetings. Each row optionally links up to an open item via `open_item_id`. |

The old activity_log dual-purpose design (`item_kind='issue'`, `is_renewal_issue`, `follow_up_date` + `follow_up_done`) was retired in migrations 164-167. Open Items is the single source of truth for "what's active and needs attention." Use activity_log only for the historical record threaded under an item.

---

## Table: `open_items` (migration 164)

| Column | Purpose |
|--------|---------|
| `uid` | `OI-NNN` sequential, set by `next_open_item_uid()` |
| `client_id`, `policy_id`, `program_id`, `project_id` | Scope. `policy_id` is the **primary** policy. |
| `bucket_id` | FK to `open_item_buckets` — workflow stage (Intake/In Progress/Waiting/Scheduled/Deferred/Resolved/Closed) |
| `title`, `description` | Subject + long-form context |
| `priority` | `Low` / `Medium` / `Important` / `Urgent` |
| `assigned_to`, `start_date`, `due_date`, `labels` | Standard task fields |
| `client_visible` | `1` to include in client-facing exports |
| `source` | `manual` / `renewal_suggestion` / `anomaly` / `milestone` / `inbox` / `audit` / `import` / `issue_migration` / `followup_migration` |
| `source_ref` | e.g. `anomaly:42`, `inbox:107` — partial unique index prevents duplicate live items per source |
| `is_renewal_issue` | `1` for auto-created per-term renewal issues. Partial unique index on `renewal_term_key` ensures one live item per renewal. |
| `renewal_term_key` | `{policy_uid}` or `program:{program_uid}` — uniqueness scope |
| `resolution_type`, `resolution_notes` | Set when resolved |
| `resolved_at`, `closed_at`, `deleted_at` | Lifecycle timestamps |

### Buckets (migration 164 seed)

| Bucket | sort | done | auto_close_after_days |
|--------|------|------|-----------------------|
| Intake | 0 | 0 | NULL |
| In Progress | 1 | 0 | NULL |
| Waiting | 2 | 0 | NULL |
| Scheduled | 3 | 0 | NULL |
| Deferred | 4 | 0 | NULL |
| Resolved | 5 | 1 | 14 |
| Closed | 6 | 1 | NULL |

`Resolved` items advance to `Closed` after 14 days via `auto_close_resolved_items()` (called on server startup).

---

## Table: `open_item_policies` (multi-policy junction)

```
PRIMARY KEY (open_item_id, policy_id)
```

`open_items.policy_id` is the **primary** policy (shown in row chips, threaded under by activity_log). Additional policies live in `open_item_policies`. The slideover Policies section manages both — adding when no primary is set promotes that policy to primary; removing the primary auto-promotes the first junction entry.

The view `v_issue_policy_coverage` unions:
1. `open_items.policy_id` (direct primary)
2. Program-level: `policies.program_id = open_items.program_id`
3. Junction rows in `open_item_policies`

That view is what queries that need "all policies covered by this item" should use.

### Scope filters

`_scope_filter()` in `web/routes/open_items.py` — when filtering by client_id or policy_id, the query checks all three paths (primary, primary-via-policies, junction). Same in `lookup()` for the inline open-item picker.

---

## Table: `activity_log` (historical thread)

`activity_log` is now write-once historical entries. Key relevant column:

| Column | Purpose |
|--------|---------|
| `open_item_id` | FK to the open item this activity threads under (NULL for unattached entries) |

Legacy columns (`item_kind`, `follow_up_date`, `follow_up_done`, `disposition`, `issue_status`, `issue_severity`, `issue_uid`, `is_renewal_issue`, `merged_from_issue_id`, etc.) are still present for backwards compatibility but are **not used** by the active code paths after the open_items refactor. Treat them as dead.

The slideover renders `activity_log` rows joined by `open_item_id` as the activity thread. New entries are created via `POST /activities/log` with `open_item_id` set.

---

## Key Routes — `web/routes/open_items.py`

```
GET    /open-items                       global bucket-grouped view
GET    /open-items/panel                 scoped HTMX fragment
GET    /open-items/lookup                JSON for inline pick-or-create combobox
POST   /open-items                       create
POST   /open-items/quick-log             one-shot Resolved item + threaded activity
GET    /open-items/{id}/slideover        full edit slideover
PATCH  /open-items/{id}                  patch one or more fields (form-encoded)
POST   /open-items/{id}/move             change bucket
POST   /open-items/{id}/complete         resolve (with resolution_type / notes)
POST   /open-items/{id}/reopen           back to In Progress
POST   /open-items/{id}/delete           soft-delete

POST   /open-items/{id}/checklist                  add
POST   /open-items/{id}/checklist/{cid}/toggle     toggle
POST   /open-items/{id}/checklist/{cid}/delete     delete

POST   /open-items/{id}/policies                       add policy to junction
POST   /open-items/{id}/policies/{policy_id}/remove    remove from junction (auto-promotes if primary)

POST   /open-items/promote/anomaly/{id}      anomaly → open_item
POST   /open-items/promote/inbox/{id}        inbox row → open_item (marks inbox processed)
POST   /open-items/promote/suggestion/{id}   suggested_activities row → open_item
```

PATCH semantics:
- Empty string for date fields → NULL
- Empty/`"0"` for `client_id`/`policy_id`/`program_id`/`project_id` → NULL
- Reassigning `client_id` wipes `open_item_policies` (cross-client links are invalid)

---

## Slideover & Panel UI

| Template | Purpose |
|----------|---------|
| `open_items/_panel.html` | Bucket-grouped panel — global view shows client+policy pickers in the new-item form |
| `open_items/_row.html` | Single row — title (contenteditable), priority, due, assigned, client/policy chips, `+N` badge for additional policies |
| `open_items/_slideover.html` | Full edit panel: bucket/priority/visibility/dates/policies/labels/checklist/description/activity thread/resolve |
| `open_items/_policies_section.html` | Primary + Also pills with × remove and "Add policy" select. Refreshes via partial after add/remove. |
| `open_items/_checklist.html` | Per-item checklist |

### Action Center

The Action Center (`/action-center`) embeds the global open-items panel as the default tab. Other tabs in the More menu: Inbox, Activities, Scratchpads, Anomalies, Activity Review, Data Health.

The legacy "Focus Queue" / "Follow-ups" UI was retired with the open_items refactor. Items are sorted by bucket → due date → created.

### Source promote flow

Anomalies, inbox rows, and audit suggestions become open items via the promote endpoints. Each:
1. Reads the source row
2. Calls `queries.create_open_item()` with `source` and `source_ref` set
3. Marks the source row processed/logged
4. Returns `{"ok": True, "open_item_id", "uid"}`

The partial unique index on `(source, source_ref)` prevents creating two live items from the same source.

---

## Domain Module — `src/policydb/open_items.py`

Pure-function helpers (no I/O ownership). Keep aligned with migration 164 seed.

| Function | Purpose |
|----------|---------|
| `bucket_id_by_name(conn, name)` | Resolve bucket name → id; raises ValueError if unknown |
| `get_buckets(conn)` | All buckets in workflow order |
| `move_to_bucket(conn, oi_id, bucket_name, *, resolution_type=None, resolution_notes=None)` | Bucket transition — sets `resolved_at`/`closed_at` based on bucket flags |
| `auto_close_resolved_items(conn, *, today=None)` | Advance Resolved items past `auto_close_after_days` to Closed. Called on startup. |
| `is_late(due_date)`, `is_high_priority(priority)` | Predicates |

Constants:
- `PRIORITIES = ("Low", "Medium", "Important", "Urgent")`
- `BUCKET_INTAKE`, `BUCKET_IN_PROGRESS`, `BUCKET_WAITING`, `BUCKET_SCHEDULED`, `BUCKET_DEFERRED`, `BUCKET_RESOLVED`, `BUCKET_CLOSED`
- `DEFAULT_BUCKET_ORDER` — tuple in display order

`queries.create_open_item()` is the canonical insert. Caller commits.

---

## Renewal Auto-Resolve

When a policy reaches a terminal renewal status (e.g., "Bound"), `auto_resolve_renewal_issue()` (still called from `renew_policies.py` and `bind_order.py`) resolves the renewal-term open item. The implementation now operates on `open_items` directly — no more `activity_log` issue headers.

Look for `auto_resolve_renewal_issue` in the code rather than relying on the old call chain (`ensure_renewal_issues`, `cascade_program_renewal_close`, `sync_renewal_issue_severity` were retired).

---

## Auto-Purge

`_purge_old_logs()` in `db.py` runs on every server startup, deleting `audit_log` and `app_log` rows older than `log_retention_days` (default 730 days = 2 years).

`auto_close_resolved_items()` likewise runs on startup, advancing Resolved → Closed.

---

## Config Keys

| Key | Default | Purpose |
|-----|---------|---------|
| `open_item_resolution_types` | (list) | Picklist for resolution capture |
| `activity_types` | (list) | Picklist for activity log entries |

The legacy keys (`renewal_issue_auto_create`, `focus_score_weights`, `stale_auto_close_days`, `follow_up_dispositions`, `issue_severities`, etc.) may still appear in config.py but no longer drive active behavior.

---

## Key Files

| File | Purpose |
|------|---------|
| `src/policydb/open_items.py` | Domain helpers (bucket lookups, move, auto-close) |
| `src/policydb/queries.py` | `create_open_item()`, `auto_close_resolved_items()` thin wrapper |
| `src/policydb/web/routes/open_items.py` | All HTTP routes (CRUD, slideover, junction, source promote) |
| `src/policydb/web/templates/open_items/*.html` | Panel, row, slideover, checklist, policies section |
| `src/policydb/migrations/164_open_items.sql` | Schema (tables + indexes + bucket seed) |
| `src/policydb/migrations/migration_165.py` | Python migration: existing followups + issues → open_items |
| `src/policydb/views.py` | `v_issue_policy_coverage` (open_item_id → policy_id) |
| `src/policydb/web/routes/action_center.py` | Hosts the open-items panel as default tab |

---

## Migration Notes

- 164: created `open_items`, `open_item_buckets`, `open_item_checklist`, `open_item_scratchpad`, `open_item_policies`, added `activity_log.open_item_id`
- 165 (Python): copied open follow-ups and open issues from `activity_log` into `open_items`, copied `issue_policies` → `open_item_policies`
- 166: dropped legacy tables (`issue_policies`, `escalation_dismissals`, `mandated_activity_log`, etc.)
- 167: shim columns added back for legacy queries that hadn't been retired yet (treat columns as deprecated)

---

## Common Pitfalls

- **Don't read `item_kind` / `follow_up_done` / `disposition`** — the data is still there but the system doesn't use it. Read from `open_items` instead.
- **`policy_id` on `open_items` is the primary**, not the only one. Use `v_issue_policy_coverage` (or check the junction explicitly) when computing coverage.
- **Reassigning the client wipes the junction**. The PATCH handler does this server-side; client-side just trigger the PATCH and reload the slideover.
- **Source-promote endpoints rely on the partial unique index** on `(source, source_ref)`. Don't bypass it with raw INSERTs — use `queries.create_open_item()`.
- **`renewal_term_key` uniqueness only applies to live items** (`is_renewal_issue=1 AND deleted_at IS NULL AND closed_at IS NULL`). Resolved items still in the 14-day window count as live.
