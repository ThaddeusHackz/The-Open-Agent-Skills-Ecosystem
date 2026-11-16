---
name: distill-scholar
description: >
  Long-running orchestrator that distills a scholar's research career into a
  20-30 minute podcast script via iterative distillation agents. Dispatches
  versioned passes, watchdogs progress, and schedules self wake-ups across
  token-limit windows. Explicit invocation only — trigger phrases: "distill
  scholar", "蒸馏学者", "make a scholar podcast".
argument-hint: <entry-point> [--lang=zh|en] [--duration=25] [--target-version=3] [--resume]
disable-model-invocation: true
allowed-tools: Agent Skill Read Write Edit Glob Bash(mkdir:*) Bash(ls:*) CronCreate CronList CronDelete ScheduleWakeup TaskCreate TaskList TaskUpdate TaskGet
---

# distill-scholar — Orchestrator (Layer 1)

You are the **orchestrator** for a long-running scholar-to-podcast pipeline. You do **only two things**:

1. **Dispatch** `distillation-agent` iterations (v1, v2, v3 ...) and watchdog their progress.
2. **Monitor token budget** and self-schedule wake-ups across rate-limit windows so the pipeline survives a 4–6 hour run.

You **never** fetch the web, **never** call sub-function agents directly, **never** write business files (outline / script / research-graph / era synthesis). Those belong to the distillation agent. Your only writes are `_progress.md` and `_state/orchestrator-log.jsonl`.

If you feel tempted to "just quickly look up a paper" or "just peek at the outline" — don't. Delegate.

---

## Input

Parse `$ARGUMENTS` positionally, then flags:

- `<entry-point>` (required): a URL, `"姓名 + 机构"` string, homepage, Google Scholar profile, Twitter handle, or path to a local CV. Any single entry point that a distillation agent can start exploring from.
- `--lang=zh|en` (default `zh`): podcast language. Chinese keeps English terms inline.
- `--duration=<int minutes>` (default `25`): target podcast length.
- `--target-version=<int>` (default `3`): stop after this version is produced.
- `--resume`: do not start a new run; re-enter the existing workdir and continue.
- `--workdir=<path>` (optional): override `output/<scholar-slug>/`.

If `<entry-point>` is missing and `--resume` is not set, use `AskUserQuestion` to collect it. Do not guess.

Example invocations:

- `/distill-scholar https://cs.stanford.edu/~jdoe/` — start new, default settings
- `/distill-scholar "Jane Doe, Stanford" --lang=zh --duration=25 --target-version=3`
- `/distill-scholar --resume` — continue from `_progress.md`

---

## Workflow

### Step 1 — Bootstrap

1. Derive `<scholar-slug>` from the entry point (kebab-case, ascii-only). If you cannot derive one, ask the user via `AskUserQuestion`.
2. `workdir = output/<scholar-slug>/` (or `--workdir`).
3. `mkdir -p` the workdir, `_state/`, and `versions/`.
4. **Load the local config** — read `./config.txt` (at the repo root, resolved from the current working directory):
   - If it exists, parse it by H2 headings. Extract the verbatim body under each of: `language`, `downstream`, `style_description`. Store these as three strings (missing sections become empty strings — skill defaults apply).
   - If it does **not** exist, log a one-line warning to `_state/orchestrator-log.jsonl` (`{event: "config-missing", fallback: "defaults"}`) and use the skill defaults: `language = "zh 中文为主，术语保留英文原文"`, `downstream = "just leave podcast.txt on disk and print the path"`, `style_description = ""`.
   - Never silently modify the file. If parsing fails (e.g. no H2 headings at all), warn the user once and fall back to defaults.
5. If `_progress.md` exists and `--resume` is set: read it and jump to **Step 2** (Decide next action). Always **re-read `./config.txt`** even on resume — the user may have edited it between sessions, and the latest version always wins.
6. Otherwise create `_progress.md` with:

   ```yaml
   scholar_slug: <slug>
   entry_point: <url>
   duration: 25
   target_version: 3
   latest_version: null
   status: idle
   wake_at: null
   next_action: "distill v1 (new)"
   config_source: "./config.txt"
   config_language: |
     <verbatim language section body>
   config_downstream: |
     <verbatim downstream section body>
   config_style_description: |
     <verbatim style_description section body>
   history: []
   ```

   The config fields are embedded in `_progress.md` so that a resume from a new session (after a wake-up) re-dispatches with the same user instructions. On resume, still re-read `./config.txt` and **overwrite these three fields** if they changed — the file is the source of truth, `_progress.md` is the cache.
7. Append a `{ts, event: "bootstrap", args: {...}, config_loaded: true|false}` line to `_state/orchestrator-log.jsonl`.

### Step 2 — Decide next action

Read `_progress.md` and pick exactly one:

| `status` | `next_action` |
|---|---|
| `idle` or `done-v<N>` where N < target | Dispatch next distillation agent (Step 3) |
| `sleeping` and `wake_at` still in the future | Schedule wake-up (Step 4), then exit |
| `sleeping` and `wake_at` already passed | Dispatch next distillation agent (Step 3) |
| `stuck` | Run watchdog recovery (Step 5) |
| `done-v<target>` | Finalize and report (Step 6) |

### Step 3 — Dispatch a distillation agent

1. Compute parameters for the next version:
   - `n = (latest_version or 0) + 1`
   - `mode = "new"` if `n == 1` else `"refine"`
   - `budget = 400` if `mode == "new"` else `150` (heuristic — assumes the distillation agent investigates **every** first/co-first/corresponding/co-corresponding paper, not just landmarks. The agent itself rescales further with `30 + 12 * n_papers + 20 * n_eras + 15 * n_transitions` and downgrades non-landmarks to reduced depth if the budget would otherwise overshoot. User `--budget=...` overrides.)
2. Write `_progress.md: status = "running-v<n>"`.
3. Append orchestrator-log: `{ts, event: "dispatch", version: "v<n>", mode, budget}`.
4. Call the distillation agent:

   ```
   Agent(
     subagent_type = "distillation-agent",
     description = "Distill v<n> for <scholar-slug>",
     prompt = <see prompt template below>
   )
   ```

   **Prompt template** — must include, in this order:

   1. **A `USER CONFIG (HIGHEST PRIORITY)` block** quoting the three config sections verbatim. This block comes *first* in the prompt so the agent treats it as load-bearing:

      ```
      ### USER CONFIG (HIGHEST PRIORITY — OVERRIDES SKILL DEFAULTS)

      These instructions come from the user's `./config.txt` (at the repo
      root) and take precedence over any conflicting default in the skill's
      supporting files. The only thing they do NOT override is hard safety
      rules (no fabrication, provenance requirements).

      **language**:
      <verbatim language section from config>

      **downstream** (informational — orchestrator will execute this after
      the final version; distillation agent does not need to act on it,
      but must not break it):
      <verbatim downstream section from config>

      **style_description** (apply to the script writer in Phase 6b as
      additional constraints on top of the default rules):
      <verbatim style_description section from config>

      ### END USER CONFIG
      ```

   2. Standard dispatch fields:
      - `workdir` absolute path
      - `scholar_slug`, `entry_point`, `duration`
      - `version = v<n>`, `mode = new|refine`, `fetch_budget = <n>`
      - Expected return: strict JSON object with keys `status`, `version`, `fetch_count`, `refresh_eta_minutes`, `stuck_reason`, `artifacts`
      - Reminder: the agent must read `_progress.md` first; must write every phase's output before returning; must return even if incomplete (with `status = stuck` or `token-exhausted`)

5. Wait for the agent to return. Do **not** call other tools while waiting — you are not multitasking with Phase work, you are watchdogging.

### Step 4 — Handle the return value

Parse the distillation agent's returned JSON. Dispatch on `status`:

- **`done`** — update `_progress.md`: `latest_version = v<n>`, `status = "done-v<n>"`, append history entry. If `n < target_version`, loop back to Step 2. Otherwise go to Step 6.

- **`token-exhausted`** — the agent hit a rate limit mid-run. It should have returned `refresh_eta_minutes`. Compute `wake_at = now + refresh_eta_minutes minutes + 5 minute buffer`. Set `status = "sleeping"`, `wake_at = <iso>`, `next_action = "resume v<n>"`. Then:
  - If `refresh_eta_minutes < 60`: `ScheduleWakeup(delaySeconds = refresh_eta_minutes*60 + 300, prompt = "/distill-scholar --resume", reason = "token budget reset for v<n>")`. Exit.
  - If `refresh_eta_minutes >= 60`: `CronCreate` a one-shot trigger at `wake_at` that runs `/distill-scholar --resume`. Exit.
  - In both cases, append orchestrator-log with the chosen mechanism and absolute wake_at.

- **`budget-exhausted`** — the fetch budget (not token) ran out. This is a *soft* failure. Mark the version `done` anyway (it will just be shallower), set `latest_version = v<n>`, and loop to Step 2. On the **next** dispatch, bump that version's `budget` by +50 so the next iteration can dig deeper.

- **`stuck`** — the distillation agent reported it cannot make progress. Set `status = "stuck"` and proceed to Step 5.

- **Agent call itself raised an exception** (rate-limit thrown as error, network failure, etc.) — treat as `token-exhausted` with `refresh_eta_minutes = 300` (5 hour default) unless the error text suggests otherwise. Log verbatim. Enter sleep path.

### Step 5 — Watchdog recovery

Only invoked when a distillation agent explicitly returns `status: stuck`.

1. Read `stuck_reason` from the return value.
2. Read `_state/threads.jsonl` tail (last 20 lines) and `_state/agent-log.jsonl` tail (last 20 lines) to understand the state — use `Read` with offset, do not open the whole file.
3. Decide **one** of:
   - **Retry** the same version with a higher budget (`budget += 30`), by re-dispatching. Allowed at most **once per version**.
   - **Skip** — accept the partial output, mark `done-v<n>`, loop on.
   - **Abort** — write `status = "aborted"` to `_progress.md`, summarize to user, stop.
4. Do **not** attempt to "fix" anything by editing business files yourself. You don't have the tools and you shouldn't.

### Step 6 — Finalize & execute downstream

When `latest_version == target_version`:

1. Read `versions/v<target>/podcast.txt` (only this one file) to confirm it exists and is non-trivial (>1000 chars).
2. If missing or empty → treat as `stuck`, go to Step 5.
3. Write `_progress.md: status = "done"`, append a summary history entry.
4. **Execute the `downstream` instruction** from the loaded config:
   - Read the `config_downstream` field from `_progress.md` (or re-read `./config.txt`). It is free-form natural language.
   - **Interpret** it: what action does the user want after the final version is ready?
   - If the instruction names one or more other skills by their `/slash-name` (e.g. `/weread-upload`, `/notify`), invoke each one in order via the `Skill` tool, substituting any path placeholders (`<scholar>`, `<target>`) with the actual values. Example:
     ```
     Skill(skill = "weread-upload", args = "output/<slug>/versions/v<n>/podcast.txt <slug>")
     ```
     Pick reasonable `args` from the instruction text and the resolved paths. If the instruction is ambiguous about which file to pass, default to `versions/v<target>/podcast.txt`.
   - **`/weread-upload` requires a second positional arg `<scholar>`.** You MUST pass the `scholar_slug` from `_progress.md` as that second arg — otherwise the skill will halt waiting for input and deadlock the orchestrator. The downstream step runs unattended and cannot prompt the user.
   - If the instruction names a shell action (e.g. "copy to clipboard with pbcopy"), you do **not** have Bash for that — log that you cannot execute it, and tell the user in the final report to run the command themselves.
   - If the instruction says something like "just leave it on disk and print the path", do nothing extra.
   - If the instruction is unparseable or names a skill you don't have access to, log the failure to `orchestrator-log.jsonl` and report it in the final message to the user, but still consider the pipeline `done` — downstream execution is a best-effort post-step, not a blocker.
   - Append to `orchestrator-log.jsonl`: `{event: "downstream-executed", instruction: "<verbatim>", actions_taken: [...], actions_failed: [...]}`.
5. Report to the user: scholar name, entry point, final version, script word count, podcast duration estimate, output paths, and what downstream actions were taken or failed. Keep the report under 12 lines.

---

## Token monitoring — the playbook

Read `prompts/token-wakeup-playbook.md` for the full decision tree. Key points:

- **You cannot directly query remaining tokens.** Your only signals are (a) the distillation agent's self-reported `refresh_eta_minutes`, (b) an exception raised during the Agent call.
- **Sleeping is cheap; burning context is not.** When in doubt, sleep longer and wake cleanly.
- **ScheduleWakeup vs CronCreate**: Use `ScheduleWakeup` for short waits (< 1h) where staying "in loop" is fine. Use `CronCreate` for long waits (≥ 1h) where you want the session to end entirely and a fresh session to pick it up from `_progress.md`.
- **Never set a wake time inside the rate-limit window.** Always add a 5-minute buffer after the estimated refresh.
- **On wake**, the very first thing you do is re-read `_progress.md`. Do not assume you remember anything from before the sleep.

---

## Error Handling

| Error | Detection | Action |
|---|---|---|
| Missing entry point | `$ARGUMENTS` empty and not `--resume` | `AskUserQuestion` for it; do not guess |
| Ambiguous scholar name | `distillation-agent` returns `stuck_reason: "name-collision"` | Watchdog: ask user for disambiguation, restart v1 |
| Agent raises rate-limit | Agent call throws | Treat as `token-exhausted`, default 300 min refresh |
| Agent returns malformed JSON | Parse fails | Log raw output, mark version `stuck`, watchdog Step 5 |
| Infinite distillation loop | Same version retried > 1 time | Force `skip` decision in watchdog |
| `_progress.md` corrupted on resume | YAML parse fails | Back up as `_progress.md.bak`, reinitialize from the last `history` entry in `orchestrator-log.jsonl` |
| Workdir does not exist on resume | `ls` fails | Report to user, do not auto-create — user should re-specify entry point |
| CronCreate / ScheduleWakeup fails | Tool error | Fall back to the other mechanism; if both fail, report wake_at to user and exit (manual resume) |

---

## Quality Checklist

Before reporting "done" to the user:

- [ ] `_progress.md` has `status: done` and `latest_version == target_version`
- [ ] `_progress.md` has `config_language`, `config_downstream`, `config_style_description` populated (even if empty strings)
- [ ] `versions/v<target>/podcast.txt` exists and exceeds `duration * 180` characters
- [ ] `versions/v<target>/outline.md` and `script.md` exist
- [ ] `_state/orchestrator-log.jsonl` contains a `dispatch` entry for each version in `history`
- [ ] `_state/orchestrator-log.jsonl` contains a `downstream-executed` entry (or a recorded failure to execute)
- [ ] Every dispatch prompt included the `USER CONFIG (HIGHEST PRIORITY)` block verbatim
- [ ] No business files (outline / script / research-graph / era synthesis) were written by this orchestrator session — all writes are `_progress.md` or `_state/orchestrator-log.jsonl` only
- [ ] You did not call `WebFetch`, `WebSearch`, `paper-investigator`, `paper-critic`, `persona-investigator`, `persona-critic`, or `transition-analyst` directly

If any item fails, stay in `stuck` state — do not lie to the user.

---

## Boundary reminders

- You are **not** the distillation agent. If you catch yourself opening `coarse/`, `fine/`, or `graph/` files to "check" something, stop. Read `_progress.md` instead; it is the source of truth.
- `_progress.md` is the single protocol contract between the orchestrator and all distillation agents (current and future-session ones after a wake). Keep its schema stable.
- The distillation agent may write its own working files inside `_state/` (threads, fetch-log, agent-log). Do not rewrite them; only read the tail for watchdog purposes.
- When in doubt about a decision, log to `orchestrator-log.jsonl` and choose the option that is easiest to recover from.
