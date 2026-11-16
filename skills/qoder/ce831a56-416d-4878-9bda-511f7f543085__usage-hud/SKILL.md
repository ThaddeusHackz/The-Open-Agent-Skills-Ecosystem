---
name: usage-hud
version: 1.0.0
description: Install, remove, tune, or debug the Qoder CLI status line HUD that shows remaining credits and context window as progress bars.
description_zh: 安装、移除、调整或排查 Qoder CLI 状态栏 HUD（用进度条显示剩余额度与上下文占用）。
user-invocable: true
argument-hint: install | uninstall | 调整条宽 | 加一个字段 | 数字不对
---

# Usage HUD

Manage a status line that renders the remaining Qoder credit balance and the
context window as progress bars.

Rendered line:

```
/Users/pat/projects/app Ultimate [██████░░░░] 64% [████████░░] ~15387/20000
```

Segments, left to right: full working directory (blue), model display name
(yellow), context window remaining as a bar plus percentage (cyan), and the
combined credit balance as a bar plus `~remaining/total` (green above 30%,
yellow 10-30%, red below 10%). Any segment whose data is unavailable is
omitted, so the worst case degrades to just the directory.

## Why the balance is an estimate

This is the constraint that shapes the whole design, so do not "simplify" it
away:

- The JSON that Qoder pipes into a status line command has **no remaining-quota
  field**. It only reports `cost.total_credits`, the spend of the current
  session.
- The CLI calls `GET /api/v2/quota/usage` roughly **once per session start**,
  not per turn. There is no cheap way to trigger a fresh call: `status`,
  `--list-models`, and `--list-sessions` do not fetch it, and starting a real
  session costs an inference call.

So `bin/statusline-hud.sh` scrapes the newest `quota/usage response: {...}` line
out of `~/.qoder/logs/runs/*/qodercli.log` to get an authoritative baseline,
then subtracts the credits this session has spent since that baseline was
taken. Hence the `~` prefix. Running `/usage` emits a fresh log line, which
re-anchors the baseline exactly.

The subtraction anchor is bound to `session_id`, because reusing another
session's anchor would inflate the balance. The estimate is also clamped so it
can never exceed the baseline. Parallel sessions in other terminals are not
visible to this one, so the figure reads low when several are active.

## Installing and removing

Use the bundled commands, which handle the `settings.json` edit and confirm
before writing:

- `/qoder-usage-hud:hud-install`
- `/qoder-usage-hud:hud-uninstall`

Qoder plugin manifests can declare skills, commands, agents, output styles,
workflows, hooks, and MCP servers, but **not** a status line. That is why
enabling the HUD requires a one-time write to the user's `settings.json` rather
than a manifest declaration.

The status line is read at session startup. After installing or removing, the
user must start a new session to see the change.

## Tuning

The script keeps its knobs as constants at the top:

- `BAR_WIDTH` (default `10`) - cells per bar.
- `RESCRAPE_AFTER` (default `30`) - seconds before re-scraping the log for a
  newer baseline. Between scrapes the render is served from
  `$QODER_DIR/hud/usage-state.json`.

Edit the installed copy at `~/.qoder/hud/statusline.sh`. Editing the copy inside
the plugin directory has no effect until the install command is run again.

Fields available in the stdin payload but not currently rendered, in case the
user asks for more: `cost.total_lines_added`, `cost.total_lines_removed`,
`vim.mode`, `agent.name`, `worktree.branch`, `version`, `session_name`, and the
absolute token counts under `context_window`.

## Debugging

Run the script by hand with a synthetic payload:

```bash
printf '%s' '{"session_id":"s","workspace":{"current_dir":"/tmp"},
"model":{"display_name":"Ultimate"},"cost":{"total_credits":12.5},
"context_window":{"remaining_percentage":64}}' | ~/.qoder/hud/statusline.sh
```

To preview a specific balance level, write a synthetic
`$QODER_DIR/hud/usage-state.json` with the `quota.userQuota` and
`quota.orgResourcePackage` values you want, then run the command above.

Common causes when the quota segment is missing entirely:

- `jq` is not installed; the script needs `jq` and `awk`.
- No log under `~/.qoder/logs/runs/` contains a quota response yet. Run
  `/usage` once in a session to emit one.
- The state file is stale or corrupt. Delete
  `$QODER_DIR/hud/usage-state.json`; it is rebuilt on the next render.

Note that `awk` on macOS does not understand `\u` escapes, so the bar glyphs are
written as literal `█` and `░` characters.
