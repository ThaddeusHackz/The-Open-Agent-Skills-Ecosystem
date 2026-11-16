---
name: ddd-check
description: "Use whenever reviewing Java code that uses com.alibaba.fa.framework.ddd base classes for DDD compliance — even if the user only says 'check my changes', 'review this', or 'is this OK'. Trigger before commit, after rebase, during code review, architecture audit, or whenever the user mentions 'DDD check', 'full audit', 'check entire project', 'architecture review', 'check compliance', or asks about layer violations. Do NOT use when the project does not use the com.alibaba.fa.framework.ddd base classes, for a one-line fix with no layer/dependency impact, or for formatting/style-only changes — this skill checks architecture, not style."
license: MIT
compatibility: Requires git and a POSIX shell (bash/zsh). Only for Java projects using com.alibaba.fa.framework.ddd base classes.
allowed-tools: Read Grep Glob Bash
metadata:
  version: "0.3.0"
  user-invocable: "true"
  argument-hint: "[full | base-branch | directory]"
---

# DDD Compliance Check

Check Java code against the DDD layer rules. Two modes selected by argument:

- **`/ddd-check`** — incremental, changed files only (default)
- **`/ddd-check full`** — every Java file in the project
- **`/ddd-check main`** — incremental, diff against a specific branch
- **`/ddd-check full src/`** — full mode scoped to a directory

## Current State

Before Step 1, gather the current state by running:

```bash
git branch --show-current
git diff HEAD --name-only --diff-filter=ACMR 2>/dev/null | grep '\.java$' || echo '(none)'
find . -name "*.java" -not -path "*/target/*" -not -path "*/test/*" 2>/dev/null | wc -l
```

## References

All paths relative to this SKILL.md. Read each file at the timing indicated:

**Rule files — read when checking the corresponding layer:**
- `references/domain-layer.md` — read when checking `**/domain/**` files
- `references/application-layer.md` — read when checking `**/application/**` files
- `references/adaptor-layer.md` — read when checking `**/adaptor/**` files
- `references/infrastructure-layer.md` — read when checking `**/infrastructure/**` files
- `references/client-layer.md` — read when checking `**/client/**` files
- `references/model-layer.md` — read when checking `**/model/**` files
- `references/anti-patterns.md` — always read (all modes)

**Educational — read when the user needs context or onboarding:**
- `references/base-classes-reference.md` — read when unsure about base class contracts or exception strategies
- `references/overview.md` — read when the user asks "what is this DDD framework" or needs the big picture
- `references/anemic-vs-ddd.md` — read when explaining why a pattern is wrong, or when the user asks "why not just a service with getters/setters"
- `references/quick-start-tutorial.md` — read when the user wants to build a new DDD feature end-to-end

## Helper Scripts

Use these scripts for quick pre-commit or CI gate checks — they cover a subset of rules via grep/static analysis without needing the full skill workflow:

- `scripts/check-layer-deps.sh [project-root]` — detect forbidden cross-layer imports. Run before commit or in CI to catch dependency violations early.
- `scripts/check-identity.sh [project-root]` — verify identity handling: `setId()` on aggregates/entities must stay confined to `infrastructure` (backfilling the DB-generated id after insert), never called from `application`/`adaptor`. Run when touching aggregate or Repository code.
- `scripts/check-naming.sh [project-root]` — verify DDD naming conventions (suffixes, prefixes). Run after creating new domain classes.

## Workflow

### Step 1 — Pick mode & collect files

Parse the arguments the user passed when invoking the skill (e.g. `/ddd-check full src/`) to determine mode — early classification avoids reading files that won't be checked:
- First argument is `full` → **Full mode**. If a second argument is provided, scope to that directory.
- First argument is any other value → **Incremental mode**, treat it as base branch ref.
- No arguments → **Incremental mode**, default base.

**Incremental — collect changed files:**

When a base branch is provided:
```bash
git diff <base-branch>...HEAD --name-only --diff-filter=ACMR | grep '\.java$'
```

When no base is provided, default to uncommitted changes:
```bash
git diff HEAD --name-only --diff-filter=ACMR | grep '\.java$'
```

When uncommitted diff is empty, fall back to branch diff vs main — covers the common case of reviewing a branch after everything is already committed, not just mid-edit:
```bash
git diff main...HEAD --name-only --diff-filter=ACMR | grep '\.java$'
```

No Java files changed → report "No changed Java files to check." and stop.

**Full — collect all files** (use the scoped directory if given, else `.`):
```bash
find <dir> -name "*.java" -not -path "*/target/*" -not -path "*/test/*" | sort
```

No Java files found → report "No Java source files found." and stop.

### Step 2 — Classify each file by layer

Classifying first lets the checker load only the relevant rule files, keeping context focused:

| Package pattern | Layer | Rule file |
|---|---|---|
| `**/domain/**` | Domain | `references/domain-layer.md` |
| `**/application/**` | Application | `references/application-layer.md` |
| `**/adaptor/**` | Adaptor | `references/adaptor-layer.md` |
| `**/infrastructure/**` | Infrastructure | `references/infrastructure-layer.md` |
| `**/client/**` | Client | `references/client-layer.md` |
| `**/model/**` | Model | `references/model-layer.md` |

Files not matching any pattern (full mode only) → flag as "Unclassified".

### Step 2.5 — Classify Application services by operation mode

Application-layer rules differ by operation mode (write vs read vs calculate) — the same action (e.g. calling Repository directly) is a violation in one mode and correct in another. Classify each `**/application/**` service class before checking, using these static signals:

| Signal | Mode | Rule part in `application-layer.md` |
|---|---|---|
| extends `ApplicationCmdService` | **Command (Write)** | Part B |
| extends `ApplicationQueryService`, class name starts with aggregate name (`{Aggregate}QueryAppService`) | **Query (Read)** | Part C |
| extends `ApplicationQueryService`, class name starts with a verb (`{Verb}QueryAppService`) | **Calculate** | Parts D/E |

When signals conflict (e.g. extends `ApplicationCmdService` but name says `Query`), flag the mismatch itself and check against the mode implied by the base interface — the interface is the framework contract, the name is convention.

### Step 3 — Read rule files

Load rules lazily to avoid context bloat on incremental checks:

- **Incremental:** load only the rule files matching the layers found. Always load `references/anti-patterns.md`.
- **Full:** load all rule files.

### Step 4 — Check each file

Validate per-file so violations are reported with exact location and fix:

**Large project strategy (full mode, >30 files):** Process one layer at a time to avoid context overflow. Order: Domain → Application → Infrastructure → Adaptor → Client → Model → Unclassified.

For each file, validate against:
1. **Structural** — correct base class, correct package, correct naming.
2. **Dependency** — no forbidden cross-layer imports.
3. **Anti-patterns** — cross-check anti-patterns rules.
4. **Identity** — `BaseEntity.isAppended()` (`id == null`) is the insert-vs-update discriminator; `setId()` is public but only infrastructure may call it (to backfill the DB-generated id after insert) — flag `application`/`adaptor` calling `setId()` on an aggregate/entity.
5. **Event** — domain events published only in aggregate or Repository, not in application/adaptor.
6. **Composition** — aggregate root properties must be Entity or Value types; plain types (String, Long, etc.) are forbidden as direct aggregate properties.
7. **Operation mode** (application layer only) — check the file against the rule part matching its Step 2.5 mode, and flag mode mismatches: write calls in a Query/Calculate service, a Cmd service that only reads, calculate classes named after aggregates (see key-checks-by-layer.md Application section).

Incremental: do NOT check unchanged files.

### Step 5 — Cross-file analysis (full mode only)

After individual checks, cross-file analysis catches violations invisible at file level (missing impls, circular deps, naming drift):

1. **Repository coverage:** every `{Business}Repository` interface in domain has a `{Business}RepositoryImpl` in infrastructure.
2. **Converter coverage:** every aggregate with a RepositoryImpl has a corresponding Converter.
3. **Dependency direction:** no circular dependencies; dependency flows inward (adaptor → application → domain ← infrastructure).
4. **Naming consistency:** DomainService prefix matches Repository prefix matches RepositoryImpl prefix matches Converter prefix.
5. **Model isolation:** client layer has no imports from model layer.

### Step 6 — Report

Before emitting the report, self-check every finding against this list; fix or drop findings that fail, then re-check:

1. Cites a specific rule-file section (e.g. `domain-layer.md §A.3`) — no uncited findings.
2. States a concrete fix, not just the problem.
3. Does not contradict the Gotchas section (e.g. flagging read-mode Repository access or ResultDO usage).
4. Severity matches the Severity table criteria.

**Incremental format:**
```
## DDD Check (incremental): {branch} → {n} files (base: {base-ref})

### {FilePath}.java — {Layer}
🔴 CRITICAL: {problem}. Fix: {fix}. (ref: {rule-file} §{section})
🟡 HIGH: {problem}. Fix: {fix}. (ref: {rule-file} §{section})

### Summary
- {n} files checked
- {x} violations (C: {a}, H: {b}, M: {c}, L: {d})
```

**Full format:**
```
## DDD Check (full): {project} → {n} files

### Domain — {count} files
#### {FilePath}.java
🔴 CRITICAL: {problem}. Fix: {fix}. (ref: {rule-file} §{section})

### Cross-Layer Findings
🔴 CRITICAL: {finding}

### Summary
- {n} files checked across {m} layers
- {x} violations (C: {a}, H: {b}, M: {c}, L: {d})
- Cross-file issues: {count}
```

Only report real problems — don't list clean files. Zero violations → "All {n} files pass DDD checks."

## Severity

| Level | Criteria | Why this level |
|---|---|---|
| **CRITICAL** | Architecture violation — wrong layer dependency, domain depends on infrastructure, missing required base class, Repository without Impl, circular dependency. | Breaks the dependency inversion that DDD relies on; cascading failures if not fixed before merge. |
| **HIGH** | Rule violation — wrong naming, wrong exception mode, any design pattern in domain, `setId()` called outside infrastructure, naming inconsistency. | Compiles and runs but silently degrades domain isolation; becomes expensive to fix as more code depends on the wrong pattern. |
| **MEDIUM** | Convention deviation — anemic entity, missing Field wrapper, model layer referenced by client, missing Converter. | Works today but blocks future capabilities (dirty tracking, model evolution); fix is low-risk and mechanical. |
| **LOW** | Style — missing `@Override`. | No runtime impact; improve readability only. |

## Key Checks by Layer

See [`references/key-checks-by-layer.md`](references/key-checks-by-layer.md) — read during Step 4 alongside the per-layer rule files for a quick-reference checklist.

## Example Reports

- [Incremental with violations](examples/reports/incremental-report.md)
- [Incremental clean](examples/reports/clean-report.md)
- [Full with violations](examples/reports/full-report.md)
- [Full clean](examples/reports/full-clean-report.md)

## Gotchas

Counter-intuitive facts that cause wrong verdicts without them — read before flagging anything:

- `BaseAggregate` itself has **no id field** — identity lives on the root Entity (public `getId()`/`setId()`). Do not flag an aggregate for "missing id".
- Query (read-mode) services calling Repository directly is the **correct** pattern — only Command mode must go through DomainService. Do not flag it.
- Application-layer flow control (checking Adaptor results, early returns with error codes) is scene orchestration, **not** forbidden business logic. Business logic = aggregate state transitions, calculation formulas, rule matching.
- **Both** exception approaches are compliant: throw checked `BizException` (default) or return `ResultDO` (on-demand). Do not flag ResultDO usage as a violation.
- Framework DTO base is `BaseDto`, **not** `BaseDTO` — Java is case-sensitive; check `extends` clauses exactly.
- `FieldSet.removeAll()` and `FieldList.addAll(index, c)` are **known framework source bugs** — user code avoiding them (element-by-element removal, tail-append) is a workaround, not a violation.
- `@Passthrough` cuts both ways: a field no method references and lacking the annotation → flag; a field **with** the annotation that IS referenced → also flag (contradicts its own declaration).

## Important

- Reference the specific rule section when flagging (e.g. "domain-layer.md §A.3").
- Suggest the exact fix, not just the problem.
- Incremental: do NOT check unchanged files.
- Full large projects: process layer-by-layer to avoid context overflow.
