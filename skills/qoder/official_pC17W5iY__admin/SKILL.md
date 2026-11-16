---
name: admin
description: "Add/edit/audit the project's admin task runner — admin.toml commands, regenerating ./admin, or migrating inline code to admin_lib."
---

# /admin — Manifest-Driven Admin Task Runner

**v2 flow (manifest-driven).** The generator writes two files per project:

- **`admin.toml`** — short (~5–25 line) human-edited manifest declaring archetypes, URLs, and any project-specific commands. Committed. **The source of truth.**
- **`./admin`** — self-contained, bundled Python script generated from `admin.toml` + archetype catalog. Also committed. Should not be hand-edited; regenerate instead.

The generator tool is `~/projects/admin-project-tool/admin-gen`. It has three modes:

- **Bootstrap** (no args): detect project stack → write starter `admin.toml` → generate `./admin`
- **`--regenerate`**: reload `admin.toml` and rewrite `./admin` (idempotent; normal loop for adding/changing commands)
- **`--audit`**: diff the on-disk `./admin` against what would be regenerated; exit 0 on clean, 2 on drift; also reports inline code complexity warnings

## Critical rule: after any commit+push to admin-project-tool, reinstall immediately

Any time you commit changes to `~/projects/admin-project-tool` and push them to `main`, **immediately** run:

```bash
bash ~/projects/admin-project-tool/install.sh
```

This syncs `~/.admin/` to the pushed SHA so the next `admin regen` produces a clean `generator_commit` hash instead of failing with "installed from a dirty tree". The full sequence for any admin-project-tool change is: **edit → commit → push → install → regen project**.

Do not skip the push before reinstalling — installing from a commit that isn't on `origin/main` still embeds a dirty SHA.

---

## Critical rule: treat the generator as a black box

**Do NOT read source code under `~/projects/admin-project-tool/` or any detector/archetype `.py` files.** The generator is a program — run it and read its output. You are not expected to understand its internals to use it.

The only files you should read are:
- The project's `admin.toml` (the user's manifest — you'll edit this)
- The project's generated `./admin` (only to show the user or debug a generation failure)
- This skill file

If the generator produces unexpected output or the wrong archetype match, **report the results to the user first**. Only dig into generator source code if the user explicitly asks you to investigate a bug in the generator itself.

---

## Inline code policy (critical — read before making any changes)

**This is the most important rule for working with admin.toml.** Every `[commands.*]` entry with `kind = "python"` is inline code embedded in the manifest. Inline code is a last resort, not a default.

### What is acceptable inline code

A command body that:
- Parses which sub-target the user wants (e.g. `if a in ("mac", "macos"): target = "mac"`)
- Reads `_APPLE_CONFIG` or `_SERVER_CONFIG` with `globals().get(...)`
- Dispatches to a single library function call per target branch
- Is ≤ ~4 logical lines total

Example — **acceptable** (2 lines, single function call):
```toml
[commands.logs]
kind = "python"
run = '''
cfg = globals().get("_APPLE_CONFIG") or {}
device_log_attach(get_ios_log_bundle(cfg, prod=args and args[0] == "--prod"), log_file=LOG_FILE)
'''
```

Example — **also acceptable** (dispatch-only, no logic):
```toml
[commands.test]
kind = "python"
run = "test_server(globals().get('_SERVER_CONFIG') or {})"
```

### What is NOT acceptable inline code

- Any `import` statement (that logic belongs in `admin_lib`)
- Loops (`for`, `while`)
- Multiple `run_cmd(...)` calls (wrap them in a function)
- More than ~4 logical lines of business logic
- Data structure construction, string building, multi-step workflows
- Anything that would look at home in a Python module

Example — **not acceptable** (business logic inline):
```toml
[commands.deploy]
kind = "python"
run = '''
from collections import OrderedDict
server_langs = os.environ.get('SERVER_LANGS', 'node,rust,python,go,claude')
info('Building Docker image...')
rc = run_cmd('docker build --platform linux/amd64 --build-arg LANGS=' + server_langs + ' -t myapp myapp/')
if rc != 0:
    err('Docker build failed'); sys.exit(1)
deploy_host = os.environ.get('DEPLOY_HOST', 'root@myserver')
rc = docker_deploy('myapp', deploy_host, '-p 8080:8080')
if rc != 0: sys.exit(1)
'''
```

This should be a function `deploy_server_docker(cfg)` in `admin_lib/rust.py` (or equivalent module), called from the command as `deploy_server_docker(globals().get("_SERVER_CONFIG") or {})`.

### When the audit flags inline code

The audit command (`init-admin --audit`) reports:
- **Moderate** (4–8 logic lines, or has loops/imports): "consider wrapping in an admin_lib function"
- **Migrate required** (> 8 logic lines): "migrate logic to admin_lib or a new archetype"
- **Inline file present** (`[inline] file = "admin_inline.py"`): always flagged — inline files are a migration target, not a pattern

When the audit flags a command, **do not ignore it**. Present the finding to the user and propose a migration plan before proceeding.

---

## Migration playbook: from inline code to admin_lib / archetype

When you find inline code that needs to be moved, follow this decision tree:

### 1. Identify what the code does

Read the inline run string and classify it:
- Is it project-specific logic that other projects would never need? → may belong in `admin_lib` as a helper
- Is it a generic pattern other Apple/Rust/Docker/etc. projects would want? → belongs in an archetype template or `admin_lib` function
- Is it the same as what an archetype already provides, but slightly tweaked? → the archetype probably needs a new config key

### 2. Choose where it goes

| Logic type | Where to put it |
|---|---|
| New sub-target for an existing command (e.g. `build server`) | Add handler to archetype template, add new `admin_lib` function, add config key to `[server]`/`[apple]` |
| New wrapper for a generic operation (docker deploy, cross-compile, etc.) | Add function to the appropriate `admin_lib/` module |
| Entirely new command class (new deploy target, new service type) | New archetype, or new command added to existing archetype |
| Project-specific one-off that can't be generalized | `kind = "shell"` if it's a shell command, or a ≤4-line dispatch if unavoidable |

### 3. Implement in admin-project-tool

The source repo is `~/projects/admin-project-tool`. Key directories:
- `admin_lib/` — Python module files bundled into `./admin`. Add functions here.
- `archetypes/` — Archetype definitions. Add new commands or extend templates here.
- `gen/manifest.py` — Add new config table keys (like `[server]`) here.
- `gen/render.py` — Emit new `_CONFIG` dicts from new manifest tables here.

After making changes, run `bash install.sh --force` in the admin-project-tool repo to deploy, then regenerate the project's `./admin`.

### 4. Migration example

Before (complex inline code in admin.toml):
```toml
[commands.build]
kind = "python"
run = '''
from collections import OrderedDict
target = args[0] if args else None
_targets = OrderedDict([('mac', 'macOS'), ('ios', 'iOS'), ('server', 'all platforms')])
if not target:
    target = pick_target(_targets, 'Build which target?')
    if not target: return
if target in ('mac', 'macos'):
    info('Building macOS...')
    rc = xcodebuild_filtered('App.xcodeproj', 'app-macos', 'Debug', 'platform=macOS')
    if rc != 0: err('Build failed'); sys.exit(rc)
    ok('macOS build succeeded')
elif target == 'server':
    rc, _ = build_multiplatform('myserver', [...])
    sys.exit(rc)
'''
```

After (archetype template with library functions):
```toml
# admin.toml — just config, no logic
archetypes = ["apple"]
modules = ["core", "rust", "docker"]

[apple]
mac_scheme = "app-macos"
...

[server]
dir = "myserver"
binary = "myserver"
```

The archetype generates `build` as a python command whose body is:
```python
build_mac(cfg, force=force)    # or build_ios, build_server — chosen by target picker
```

---

## Instructions

Follow these phases. Do NOT skip phases or auto-confirm on behalf of the user.

### Phase 0: Update the generator (always run first)

Before doing anything else, bring the admin-project-tool repo to a clean HEAD of main. Do these steps in order:

**Step 0a — Check for outstanding work**

```bash
git -C ~/projects/admin-project-tool status
```

If there are uncommitted changes or untracked files:
- Show the user what's dirty.
- Offer to commit and push the outstanding work before pulling.
- Do NOT pull over uncommitted changes — that risks a dirty merge and a dirty `generator_commit` SHA embedded in the next regenerated `./admin`.

**Step 0b — Ensure you're on main**

```bash
git -C ~/projects/admin-project-tool branch --show-current
```

If the branch is not `main`, tell the user and ask whether to switch. Do not proceed on a feature branch unless the user explicitly confirms.

**Step 0c — Pull from origin**

```bash
git -C ~/projects/admin-project-tool pull origin main
```

If the pull fails (network error, merge conflict), report it to the user and stop — do not proceed with a potentially stale generator.

**Step 0d — Reinstall**

After pulling, always reinstall so `~/.admin/` reflects the current HEAD:

```bash
bash ~/projects/admin-project-tool/install.sh
```

**Post-commit reinstall rule:** Any time you commit changes to `admin-project-tool` and push them to `main`, immediately run `bash ~/projects/admin-project-tool/install.sh` on the current machine. This ensures the installed generator matches the committed SHA and future `--audit` runs produce a clean `generator_commit` hash.

---

The generator binary is at `~/projects/admin-project-tool/admin-gen` (not `~/.admin/init-admin` — ignore that path). Use it directly for all generator calls:

```bash
~/projects/admin-project-tool/admin-gen --audit      . --force-dirty
~/projects/admin-project-tool/admin-gen --regenerate . --force-dirty
~/projects/admin-project-tool/admin-gen              .               # bootstrap
```

### Phase 1: Detect current state

1. Check `~/projects/admin-project-tool/admin-gen` exists. If not, tell the user to clone the repo.
2. Check the project for `admin.toml` and `./admin`:
   - **Neither exists** → bootstrap flow (Phase 2a)
   - **Both exist** → regenerate / audit flow (Phase 2b)
   - **Only `./admin` exists, no `admin.toml`** → this is a v1 (pre-manifest) project. Offer `--from-existing` migration (once that flag ships — tracked as an open issue). Until then, treat as bootstrap and warn the user the existing `./admin` will be overwritten.
   - **Only `admin.toml` exists, no `./admin`** → run `--regenerate`

### Phase 2a: Bootstrap (no admin.toml)

1. Run `~/projects/admin-project-tool/admin-gen .` — it detects the stack, writes `admin.toml`, and generates `./admin`. **Do not explore the project yourself to guess the archetype — the detectors do this.**
2. Read the generated `admin.toml` and show it to the user along with the detector match (printed in the generator's stdout).
3. Check for inline code warnings in the output. If any are emitted, address them before moving on (see "Inline code policy" above).
4. Point them at any TODO shell strings (the `simple` fallback archetype uses placeholder `echo 'TODO: …'` commands that need to be filled in).
5. **Apply standard command ordering** (see Phase 2c below) — archetypes define their own order which is usually wrong. Always reorder after bootstrap.

### Phase 2b: Regenerate / Audit (admin.toml exists)

1. Run `~/projects/admin-project-tool/admin-gen --audit . --force-dirty` first to check for drift and inline code issues.
   - **Exit 0, clean** → nothing to do unless the user is explicitly asking for a change.
   - **Exit 2, drift** → the on-disk `./admin` was hand-edited, or the archetype catalog / `admin_lib` has moved since the last regen. Show the user the unified diff and ask whether they want to regenerate (throwing away the hand edits) or keep the drift.
   - **Inline code warnings** → these are printed before the exit code regardless. Present them to the user and propose a migration plan for any flagged commands.
2. To update after the user edits `admin.toml`, run `~/projects/admin-project-tool/admin-gen --regenerate . --force-dirty`.

### Phase 2c: Standard command ordering

After any bootstrap or regeneration, check `./admin --help` and ensure commands appear in this order. If they don't, explicitly define all commands in `[commands.*]` blocks in `admin.toml` (this overrides the archetype's order) and set `archetypes = []` if needed to prevent the archetype from re-imposing its order.

**Required order:**
```
build
dev
deploy

test
vet
fmt
clean
docs
```

The blank line between `deploy` and `test` is conceptual grouping (build/run/ship, then quality/docs) — not literally blank in the TOML, just the mental model for ordering.

- `dev` = run the project locally (e.g. `go run ./cmd/...`, `python app.py`, `npm run dev`)
- `docs` = serve docs locally with hot reload so the user can read them in a browser. **Single command, no sub-targets** — e.g. `kind = "shell"` + `run = "npm run docs:dev"` for VitePress, `run = "mkdocs serve"` for MkDocs, `run = "go doc -http=:6060"` for Go. Do *not* wire `build`/`preview`/`deploy` of docs into admin unless the user explicitly publishes a static docs site somewhere — for local viewing those are noise.
- Not every project has every command — omit ones that don't apply, but keep the relative order of those that do.

**Preferred ordering mechanism — group + priority:**

Add `group` and `priority` integers to each `[commands.*]` entry. Commands sort by `(group, priority, name)`; spacers appear **automatically** between groups. This scales across archetypes because each command declares its own position — no central list to update when commands are added.

Standard layout (two groups, spacer between them):

```toml
[commands.build]
desc = "Build"; steps = ["build"]; group = 1; priority = 10

[commands.dev]
desc = "Run dev server"; steps = ["run-dev"]; group = 1; priority = 20

[commands.deploy]
desc = "Deploy"; steps = ["deploy"]; group = 1; priority = 30

[commands.test]
desc = "Run tests"; steps = ["test"]; group = 2; priority = 10

[commands.vet]
desc = "Vet"; steps = ["vet"]; group = 2; priority = 20

[commands.fmt]
desc = "Format"; steps = ["fmt"]; group = 2; priority = 30

[commands.clean]
desc = "Clean"; steps = ["clean"]; group = 2; priority = 40
```

Group 1 = primary (build / run / ship). Group 2 = quality / housekeeping. The spacer between groups is emitted automatically — no `order` field needed.

Omit commands that don't apply, but keep the relative order of those that do. Defaults (`group=0`, `priority=0`) produce alphabetical order with no spacers — fine for simple projects with ≤3 commands.

**Legacy alternative — explicit `order` list:** still supported for projects that already use it, but prefer group/priority for new manifests.

```toml
order = ["build", "dev", "deploy", "---", "test", "vet", "fmt", "clean", "docs"]
```

`"---"` is the separator token. Manifest `order` wins over archetype order; commands not in the list auto-append after.

### Phase 3: Env var discovery (if the manifest uses `${VAR}`)

If `admin.toml` or any generated command references `${VAR}` placeholders, run `./admin env` to list referenced vars and their current state (set / default / UNSET required). Tell the user which env vars they need to export before commands will work.

### Phase 4: Post-generation file setup

After generation succeeds:

1. **`.gitignore`** — ensure `tmp/` is ignored (the generator creates `tmp/.gitignore` automatically, which covers this). Also ensure `*.local.*` is in `.gitignore` (covers `.claude/CLAUDE.local.md`, `config.local.toml`, `settings.local.json`, and any other `.local.` files). Do not add `CLAUDE.local.md` as a literal name — the glob is the correct form.
2. **`.claude/skills/read-logs.md`** — create if missing (template below)
3. **`.claude/CLAUDE.local.md`** — create or update with the dev process guidance (see Phase 5 below)
4. **Project `CLAUDE.md`** — if it references `admin.sh` or a v1 template name, update to reference `./admin` and mention `admin.toml` is the source of truth
5. **Docs site, if present** — if the project has a `docs/` site (VitePress or otherwise), make sure two things are true:
   - `admin.toml` has a single `[commands.docs]` shell command running the dev server (`run = "npm run docs:dev"` for VitePress). No sub-targets. Add to the `order` array between `clean` and `icons`/`logs`/`reload`.
   - Project `CLAUDE.md` has a `## Documentation` section pointing at the docs site and listing which doc files to keep current.

   If either is missing or shaped differently (e.g., `[commands.docs]` has sub-targets, or CLAUDE.md just says "see docs/" without the update-when table), invoke `/docs` — it owns the docs convention. Don't fix it from the admin skill alone.

**Audit checks for file locations** — when auditing an existing project, verify:
- `.claude/CLAUDE.local.md` exists (not `CLAUDE.local.md` at the project root — that was the old incorrect location)
- `.gitignore` contains `*.local.*` (not a literal `CLAUDE.local.md` entry — migrate it to the glob)
- If `CLAUDE.local.md` exists at the root, move its content to `.claude/CLAUDE.local.md` and remove the root file

### Phase 5: Dev process documentation

Ensure the project has a `.claude/CLAUDE.local.md` (gitignored via `*.local.*`) with a dev process section. The content should be tailored to the project's reload capabilities:

**For projects with native hot reload** (Vite, webpack HMR, Next.js fast refresh, Air for Go, etc.):
```markdown
## Dev process

`./admin dev` runs the development server with hot reload. It stays running — do not start a second instance. If it's already running, edits are picked up automatically; no action needed after code changes.

Before running `./admin dev`, check whether it's already running:
- Look for `/tmp/admin-run.pid` — if present, a dev process is active
- Do not run `./admin dev` again; the running process will pick up file changes
```

**For projects without hot reload** (compiled binaries, scripts that must be restarted):
```markdown
## Dev process

`./admin dev` builds and runs the project. It uses a PID file at `/tmp/admin-run.pid` and listens for SIGUSR1 to trigger a rebuild without restarting the process.

After making code changes:
1. Check if `./admin dev` is running: look for `/tmp/admin-run.pid`
2. If running: send `./admin reload` to trigger a rebuild — do NOT kill and restart
3. If not running: start it with `./admin dev`

**Never orphan the dev process.** If you must stop it, use `./admin dev` Ctrl-C or send SIGTERM to the PID in `/tmp/admin-run.pid`. Do not kill it and leave the PID file stale — the next `./admin dev` will fail to start cleanly.

**Never run two dev processes simultaneously.** If `/tmp/admin-run.pid` exists and the process is alive, use `./admin reload` instead of starting a new one.
```

If the project uses `./admin dev` for a one-shot operation (compiles and exits, like `go install .`), omit the dev process section entirely — it doesn't apply.

Also ensure `*.local.*` is in `.gitignore`.

### Phase 6: Commit

Ask the user if they want to commit `admin.toml` and `./admin` together. They should always be committed in the same commit so provenance (`generator_commit` SHA) stays coherent.

---

## Key mental-model notes

- **`admin.toml` is the source of truth.** Hand-edits to `./admin` are drift. Escape hatch for project-specific code is `[inline] file = "admin_inline.py"` in the manifest, not editing the generated script. **`[inline]` is itself a migration target — the audit flags it.**
- **Archetypes are composable mixins.** `archetypes = ["docker-unraid", "apple"]` is valid and produces a merged command set. Later archetype wins on conflicts; manifest `[commands]` wins over all archetypes.
- **Env vars are runtime.** `${VAR}` and `${VAR:-default}` in manifest strings are passed through to the generated script as literals and resolved by `admin_lib.core.resolve_env()` when commands run. Never expand them at generation time.
- **`generator_commit` is the repo SHA of `admin-project-tool`** at the time of last regeneration. The audit compares SHAs to tell the user whether the generator itself has moved since the manifest was last regenerated.
- **Python 3.11+ required** everywhere (stdlib `tomllib`). The generated `./admin` starts with a runtime guard.
- **Config tables drive archetype behavior.** `[apple]` and `[server]` tables in admin.toml are emitted as `_APPLE_CONFIG` and `_SERVER_CONFIG` dicts in the generated script. Archetype commands read these at runtime — adding a key to the table is how you configure archetype behavior without inline code.

---

## Per-command env injection (`env` table)

Any `[commands.X]` block can declare an `env` table. The generated command function calls `_apply_cmd_env(...)` before running its steps, setting those env vars into the process environment. Values support `${VAR:-default}` expansion.

```toml
[commands.deploy]
steps = ["deploy"]
env = { ADMIN_LOCAL = "${DEPLOY_LOCAL:-false}" }

[commands.dev]
steps = ["dev"]
env = { ADMIN_LOCAL = "true" }   # dev is always local
```

### The `DEPLOY_LOCAL` / `ADMIN_LOCAL` pattern (Unraid deploy)

The `docker-unraid` and `unraid-plugin` archetypes ship with env injection already wired on their remote commands (`deploy`, `logs`, `diff`, `install-template`). The mapping is:

```
DEPLOY_LOCAL (machine-specific .env) → ADMIN_LOCAL (checked by ssh_cmd / scp_to / _is_local_host)
```

**`ADMIN_LOCAL=true`** tells all SSH/scp/rsync operations in `admin_lib` to run locally instead of connecting over SSH. This is the mechanism — `_is_local_host()` in `remote.py` checks it first, before any IP comparison.

**When to set `DEPLOY_LOCAL=true`:** in the project's `.env` (machine-specific, gitignored) on any machine that IS the Unraid host — whether running bare on Unraid or inside a Docker dev container on Unraid with the socket mounted.

**When not to set it:** on a Mac or remote workstation deploying to Unraid over the network. Leave `DEPLOY_LOCAL` unset (defaults to false) and SSH/scp work normally.

**Setup for any `docker-unraid` project:**
1. Add to `.env.example` (committed, documents the var):
   ```
   DEPLOY_LOCAL=    # set to true when running from the Unraid host itself
   ```
2. Add to `.env` on the Unraid host (gitignored):
   ```
   DEPLOY_LOCAL=true
   ```
3. Regenerate `./admin` — the archetype handles the rest.

**Secondary detection (no config needed):** `_is_local_host()` also compares IPs via `hostname -I`, so it still works when running bare on the Unraid host and `DEPLOY_LOCAL` isn't set. The env var is the explicit escape hatch for when IP comparison fails (e.g., inside a container where `hostname -I` returns the bridge IP, not the host's Tailscale IP).

## File-based log tailing (`[logs]` section)

The manifest supports a top-level `[logs.<target>]` section that emits a `./admin logs` command for tailing log **files** (not processes). Use this when the project writes to one or more well-known log files — whether an append-only file, a rotating file, or a file that's truncated and rewritten in place ("circular-buffer" style). It does not care what produced the file.

### Manifest shape

```toml
[logs.app]
dev  = "./tmp/app.log"                                                                  # string = local path
prod = { path = "/var/log/app.log", host = "${APP_HOST}", user = "${APP_USER:-root}" }  # table = remote
default_env = "dev"                                                                     # optional; else TUI picker / --env required

[logs.worker]
local = "./tmp/worker.log"                                                              # single env auto-selected; no picker
```

Rules:
- Each env value is **either** a string (local path) **or** a table with a required `path` and optional `host` + `user`.
- `host` present = tail remotely via `ssh [-l user] host 'tail … path'`. Missing = local file.
- `${VAR}` / `${VAR:-default}` placeholders work anywhere (path, host, user) and resolve at run time.
- `default_env` is optional. Omit to require `--env` when the target has multiple envs (or let the TUI pick).
- If a manifest `[logs]` section defines `logs`, it supersedes any archetype-supplied `logs` command (e.g. `docker-unraid` has its own ssh-based `logs`). The manifest wins.

### CLI

```
./admin logs                     # TUI picker over log targets
./admin logs <target>            # follow from end, default env
./admin logs <target> --env prod # explicit env
./admin logs <target> --tail 500 # print last 500 lines, then follow
./admin logs <target> --all      # print whole file, then follow
./admin logs <target> --no-follow    # one-shot; combine with --tail or --all
```

Default behavior is **follow from end** — no history dump unless asked. Follow mode reopens the file on inode change or size shrink, so it handles both log rotation and truncation-style circular buffers. Remote tailing uses `tail -F` so the remote side handles rotation.

### When to suggest adding `[logs]`

- The user has one or more log files whose paths they can name.
- They want to stream those logs from `./admin` without remembering paths or writing shell aliases.
- They have dev vs. prod environments for the same logical log (with possibly different paths and hosts).

### What `[logs]` is **not**

- Not a log-aggregator, formatter, or filter. It's a file-streaming shortcut.
- No `--since <duration>` time-based filter. Use `--tail N` to bound output.
- Not a replacement for hooking into a live process (e.g. `docker logs -f`) — for that, an archetype shell command is still the right shape.

## v1 projects (no `admin.toml`)

These still exist until migrated. A v1 `./admin` is a bundled single file with a `# @bundled` header but no companion `admin.toml`. Don't hand-audit these — they predate v2 and will be migrated with `--from-existing` (not yet implemented; tracked as an open issue). Until then, regenerating a v1 project from scratch is the only option, which overwrites the existing script.

---

## Logging system

Every `./admin` command writes its terminal output to a **named log file** in `tmp/`. The file name reflects the full subcommand route:

| Command run | Log file |
|---|---|
| `./admin dev ios` | `tmp/dev-ios.log` |
| `./admin dev device` | `tmp/dev-device.log` |
| `./admin dev mac` | `tmp/dev-mac.log` |
| `./admin deploy mac` | `tmp/deploy-mac.log` |
| `./admin build ios` | `tmp/build-ios.log` |
| `./admin test server` | `tmp/test-server.log` |
| `./admin somecommand` | `tmp/somecommand.log` |

By default, **up to 3 previous runs are retained** as `.log.1`, `.log.2`, `.log.3` (most recent = `.1`). The current run is always the plain `.log` file.

### `./admin logs` — universal log tailer

Every generated `./admin` script has a built-in `logs` command that tails log files by filter:

```
./admin logs                  # picker of all *.log files in tmp/, sorted by recency
./admin logs dev              # filter to files containing "dev", tail if one match
./admin logs dev ios          # filter "dev-ios", tail tmp/dev-ios.log directly
./admin logs deploy mac       # filter "deploy-mac", tail tmp/deploy-mac.log
```

- Args are joined with `-` to form the filter string (substring match on basename)
- If one match → tail immediately; multiple → interactive picker; zero → show all
- Accepts filename with or without `.log` extension as filter

### When the user says "check the logs"

1. Determine which command was most recently run (ask or infer from context)
2. Read `tmp/<cmd>-<subcmd>.log` directly — don't run `./admin logs` yourself, just `Read` the file
3. Previous run is at `tmp/<cmd>-<subcmd>.log.1` if needed

**Build problem** (didn't launch, crash on start): read from the top (first 80 lines)
**Runtime bug** (launched but something went wrong): read from the bottom (last 80 lines)
Don't read the full file unless targeted reads didn't give enough info.

### Configuring logging in admin.toml

```toml
[logging]
enabled = true      # false → disable all file logging
dir = "tmp"         # log directory (default: tmp)
retain = 3          # number of old copies to keep (default: 3, 0 = overwrite)
```

Per-command overrides in any `[commands.<name>]` table:
```toml
[commands.dev]
log_file = "tmp/custom.log"   # explicit path override
log_retain = 0                 # per-command retention
log = false                    # disable logging for this command
```

### `tmp/` directory

All log files are in `tmp/` which is git-ignored (`tmp/.gitignore` contains `*`). Rotated copies (`.log.1`, `.log.2`, `.log.3`) are also in `tmp/`. Only the current log is available to tail from a live session.

---

## read-logs.md Template

If `.claude/skills/read-logs.md` doesn't exist, create it:

```markdown
---
name: read-logs
description: Read runtime logs from the last ./admin dev or other command. Use when the user says they ran the app and something didn't work, or when you need to check what happened during the last run.
---

# Read Logs

Admin commands write output to named log files in `tmp/`. The file name reflects the subcommand route:
- `./admin dev ios` → `tmp/dev-ios.log`
- `./admin dev device` → `tmp/dev-device.log`
- `./admin deploy mac` → `tmp/deploy-mac.log`
- `./admin build ios` → `tmp/build-ios.log`
- `./admin somecommand` → `tmp/somecommand.log`

Previous runs are retained as `.log.1`, `.log.2`, `.log.3` (most recent = `.1`).

## Strategy

Determine which command was last run, then read the corresponding file. Determine whether this is a **build problem** or a **runtime/logging problem**, then read accordingly.

### Build problem (app didn't launch, crash on start)
Read from the **top** of the log file (first 80 lines). Look for:
- `error:` lines from build tools
- `BUILD FAILED` or equivalent
- Crash output immediately after launch

### Runtime / behavior bug (app launched but something went wrong)
Read from the **bottom** of the log file (last 80 lines). The user typically quits after observing the bug.

### If you need more context
- Read the full file only if the targeted read didn't give enough info
- Check the previous run at `.log.1` if the current log is empty or unrelated
- Search for specific error patterns

### What NOT to do
- Don't read the entire log file upfront if it's large
- Don't ask the user to paste logs — just read the file
- Don't run `./admin logs` to view logs — use the Read tool directly on the file
```
