---
name: transactql
description: Compose a multi-step write to a Clef app as a single atomic Transaction using transactQL (the EdgeQL-style DSL) or transact(ops:) (the explicit Op[] form). Use whenever a fix touches >1 concept / >1 file / requires a precondition / would otherwise be a stack of separate Edit/Write calls. Atomic, idempotent on retry, dryRun-previewable, rolls back on failure.
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "<description of the change you intend to make>"
---

# /transactql

Compose the change described in **$ARGUMENTS** as a single Clef
Transaction. Submit either as a transactQL DSL string or as an
explicit `transact(ops:)` Op[].

Invoke this skill whenever you would otherwise:

- Stack multiple `Edit`/`Write` tool calls to apply a related change
- Call `kernel.invokeConcept` more than once in a row
- Make a change that needs a precondition (etag / version match /
  exists / not_exists / a registered predicate)
- Compose a code refactor with a spec edit and a content write
- Want a `dryRun:true` preview before committing
- Want idempotency on retry (replay safety)

If the change is a single read-only query, use `/debug-with-score`
instead. If it's a single concept action with no preconditions and
no related work, just call `kernel.invokeConcept` directly.

## Two surfaces, one pipeline

Both surfaces compile to the same `Op[] → Transaction → Transactor`
pipeline and return the same `TransactResult { ok, returns,
transaction, error }` envelope.

| Surface | When to use |
|---|---|
| `transactQL(query: "...", idempotencyKey, dryRun)` | Human/LLM-authored multi-step logic. Best when you want template variables, prefix-form `name := (call ...)` captures, `ensure` preconditions, and `select { ... }` shape projection in one string. |
| `transact(ops: [Op,...], idempotencyKey, dryRun)` | Programmatic composition. Each Op is a structured record. Best when you're generating Ops from data or want explicit field names without parsing a string. |

Submission paths (pick whichever your agent has access to):

- **MCP tool** — `mcp__clef-devtools__transaction_submit` (see also
  `mcp__clef-devtools__describe_tools` for the input schema).
- **GraphQL** — `mutation { transact(ops:..., idempotencyKey:...) { ok returns error { code message path } } }` or `mutation { transactQL(query:..., idempotencyKey:...) { ok returns } }`.
- **Direct kernel** — `kernel.invokeConcept('urn:clef/Transaction', 'submit', {...})` from inside a script.
- **Bind /transact endpoint** — `POST /transact` for any deployed concept.

## The 7 Op kinds

Every Op may carry `as: "name"` to capture its result into the
post-commit binding map. Downstream Ops can interpolate
`$<name>.field` / `$<name>.length` into their args. `select { ... }`
in transactQL projects the binding map into the response shape.

| Kind | Shape | Purpose |
|---|---|---|
| `add` | `{ targetConcept, targetEntity, attribute, value }` | Datomic-shaped primitive write — appends an attribute value to an entity. |
| `retract` | `{ targetConcept, targetEntity, attribute, value }` | Primitive remove. Empty `value` drops the attribute entirely (scalar drop); non-empty value targets a single list element. |
| `call` | `{ function: "<Concept>/<action>", args: "<JSON>", as? }` | Concept-action invocation. The action's input/output shape is whatever the concept's spec declares. Most fixes use this kind. |
| `ensure` | `{ targetConcept, targetEntity, predicate, expectedVersion? }` | Precondition. `predicate` is `exists` / `not_exists` / `etag` / `expectedVersion` / a registered predicate-fn name. Checked atomically before commit. |
| `query` | `{ source, filter, as }` | Read entity set inside the tx, captured under `as`. Reads through `setConceptInventoryReader` when wired. Same-tx kind:add overlay applies on top. |
| `forEach` | `{ source, body, as }` | Iterate over a `$<binding>`, dispatching the body sub-Op per row. `$item.field` in args expands per iteration. |
| `queryProgram` | `{ program, as }` | Sealed `QueryProgram` value (scan / filter / sort / project / limit / offset / pure …). Dispatches through the staged-db `QueryExecution` provider so the program sees in-flight tx writes. |

**The two most common patterns:**

1. **Multi-action concept fix** — one `kind:ensure` (precondition)
   followed by N `kind:call` Ops (the change), each `as`-captured
   so a final action can reference the chain.
2. **Read + write atomic** — one `kind:query` capturing the current
   state, followed by `kind:call` Ops that interpolate `$capture.id`
   etc. into their args.

## The 5 ensure precondition kinds

| `predicate` | Semantics |
|---|---|
| `exists` | Entity must exist in `targetConcept` storage at commit time. |
| `not_exists` | Entity must NOT exist (idempotent-create guard). |
| `etag` | Stored etag/hash must match the value in `expectedVersion`. |
| `expectedVersion` | Numeric version must equal `expectedVersion`. |
| `<predicate-fn-name>` | A `Predicate/register`-registered function name; the function is invoked with the current state and must return `true`. Built-ins include `spec-valid?`, `exists?`, `not-exists?`, …. |

## Workflow

### 1. Introspect the schema

If you don't already know the Op input shape or the available
sub-mutation kinds, call:

```graphql
{ __type(name: "OpInput") { inputFields { name type { name } } } }
{ __type(name: "OpKind") { enumValues { name description } } }
{ __type(name: "SubMutationKind") { enumValues { name description } } }
```

Or via MCP: `mcp__clef-devtools__describe_tools` then look at the
Transaction schema. Discover `<Concept>/<action>` candidates with
`/debug-with-score` (`ScoreApi/listConcepts`, `getConcept`).

### 2. Compose the Transaction

Pick `transactQL` if you want the DSL ergonomics; pick `transact()`
if you're generating Ops programmatically. **Always** include an
`idempotencyKey` (auto-generated when omitted, but be explicit when
you might retry). The handler library has `newUlid()` /
`newUuidV7()` in `runtime/ids.ts`.

### 3. Preview with dryRun

Add `dryRun: true`. The pipeline runs every step short of commit:
validates Op[] types, evaluates preconditions on staged-db, dispatches
sub-mutations into the staging overlay, computes the rollback chain,
and returns the would-be `transaction.status: "tentative"` plus the
`returns` shape. **Show this to the user before confirming.**

### 4. Confirm and submit

Re-submit with `dryRun: false`. The Transactor commits atomically
or returns a typed `WriteError` and walks the rollback chain in
reverse via `Restore/restoreChange`.

### 5. Read the envelope

```
{
  ok:               Bool       // true ↔ committed
  returns:          JSON       // post-commit binding map (select projection)
  transaction:      { status: "committed" | "tentative" | "rolled-back", commitId: ULID, ... }
  error?:           { code, message, path, kind, cause? }
  qualityDelta?:    { scanRan: Bool, newFindings: [...], ... }
  changes?:         [{ before, after, ... }]   // from MutateResult envelope
}
```

When `ok: false`, `error.code` (REST-convention alias for `kind`)
identifies the failure class — see WriteError catalog below.

## The transactQL DSL

```text
with $title := "Hello", $author := "alice"
  article := (call Article/create({article: "art-1", title: $title, body: "hi", author: $author}))
  ensure article exists
select { article { id title } }
```

Grammar at a glance:

- **`with $a := <literal>, $b := <literal> …`** — template variables.
  Comma OR whitespace separators. Substitute via `$a` / `$a.field`
  / `$a.length` into Op args.
- **Top-level statements** — `insert`, `call`, `update`, `delete`,
  `ensure`, `select`. `insert User { … }` compiles to `kind:add`
  (or `kind:call <Concept>/create` if a tx-function is registered).
  `call C/a({…})` is the explicit form.
- **Captures** — both `<expr> as <name>` (suffix) and
  `<name> := (<expr>)` (prefix) accept `insert` / `call` / `update`
  / `delete`. Multi-binding shorthand: `with $a := 1 $b := 2`
  (whitespace-separated).
- **`ensure`** — same five precondition kinds as `Op{kind:ensure}`.
  `targetConcept` flows through as part of the ensure.
- **`select { alias: binding { fields }, … }`** — shape projection
  over the post-commit binding map. Shorthand `{ binding { fields } }`
  (alias defaults to binding name) supported.
  `select { v1, v2, v3 }` projects the bound values verbatim.

Errors short-circuit to `WriteError(code: malformed)` with
line/column position.

## Worked example — three concerns, one transaction

A real fix from `probe-dsl-stress workflow 45`: refactor every
`console.x(...)` to `logger.x(...)` AND add a new variant to a
spec AND create a content row, all atomically.

```graphql
mutation {
  transact(ops: [
    { kind: call, function: "Refactor/refactorByPattern",
      args: "{\"query\":\"(member_expression object: (identifier) @obj (#eq? @obj console))\",\"replacement\":\"logger\",\"language\":\"typescript\",\"files\":\"runtime/sample.ts\",\"dryRun\":false}",
      as: "refactor" },
    { kind: call, function: "ScoreMutation/addVariant",
      args: "{\"concept\":\"User\",\"action\":\"register\",\"variant\":\"crossSide\"}",
      as: "specEdit" },
    { kind: call, function: "Article/create",
      args: "{\"article\":\"cross-1\",\"title\":\"…\",\"body\":\"…\",\"author\":\"alice\"}",
      as: "created" }
  ], idempotencyKey: "ulid-01J9R…") {
    ok returns transaction { status } error { code message path }
  }
}
```

Same payload as transactQL:

```graphql
mutation {
  transactQL(query: "
    refactor := (call Refactor/refactorByPattern({query: \"…\", replacement: \"logger\", language: \"typescript\", files: \"runtime/sample.ts\"}))
    specEdit := (call ScoreMutation/addVariant({concept: \"User\", action: \"register\", variant: \"crossSide\"}))
    created  := (call Article/create({article: \"cross-1\", title: \"…\", body: \"…\", author: \"alice\"}))
    select { refactor { diff }, specEdit { id }, created { article } }
  ", idempotencyKey: "ulid-01J9R…") {
    ok returns
  }
}
```

If any of the three fails, the whole transaction rolls back through
`Restore/restoreChange` — no partial refactor, no orphan spec edit.

## Tx-functions you'll typically reach for

Every `kind:call function: "<X>/<y>"` resolves to a registered
concept action. The most-used ones from a fix-side context:

| Function | Purpose |
|---|---|
| `ScoreMutation/createConcept` | Wholesale new `.concept` file |
| `ScoreMutation/addAction` | Add an action to an existing concept |
| `ScoreMutation/addVariant` | Add a variant to an existing action |
| `ScoreMutation/insertStateField` | Add a state field |
| `ScoreMutation/insertFixture` | Add a fixture for a variant |
| `ScoreMutation/insertInvariant` | Add an `example` / `forall` / `always` / `never` invariant |
| `SpecEdit/insert*` | Lower-level versions of the above (used by orchestrator) |
| `Refactor/refactorByPattern` | Tree-sitter S-expression query + replacement, files glob, language. Composes with everything else atomically. |
| `Refactor/findReplaceInFiles` | Plain string find/replace across a glob |
| `Refactor/renameSymbol` | Rename a symbol (Score-aware) |
| `SyncEdit/createFile` / `appendEffect` / `deleteFile` | `.sync` file mutations |
| `DeployEdit/addConcept` / `addSync` | `deploy.yaml` mutations |
| `Article/<action>`, `User/<action>`, etc. | Any application concept's actions are callable by name. |

Discover the full set with `__type(name: "SubMutationKind") { enumValues { name } }`.

## WriteError catalog

When `ok: false`, `error.code` will be one of:

| Code | When |
|---|---|
| `precondition_failed` | An `ensure` Op's predicate evaluated false at commit time. |
| `conflict_at` | etag / version mismatch with concurrent committer. |
| `invariant_violated` | A spec invariant fired during the staged commit. |
| `unauthorized` | Caller lacks permission for the requested write. |
| `rate_limited` | Server-side write rate limit hit. |
| `unavailable` | Backend (storage/transport) unavailable. |
| `duplicate` | Same `idempotencyKey` + DIFFERENT params — by design, prevents accidental double-apply on retry with mutated state. |
| `not_found` | An Op referenced an entity that doesn't exist. |
| `malformed` | Op[] failed type-check (unknown `kind`, missing required field, parse error in transactQL DSL). `error.path` will point to the line:col. |
| `type_error` | Spec/handler signature mismatch (e.g., wrong argument shape for a tx-function). |

Same `idempotencyKey` + same params → cached response with original
`returnsJson` + real `commitId` (Stripe-pattern replay).

## Anti-patterns

- **Don't stack `Write`/`Edit` calls** for related changes. Compose
  them as one Transaction so the fix is atomic and reviewable.
- **Don't omit `idempotencyKey`** when the call could be retried.
  Use `runtime/ids.ts` `newUlid()` / `newUuidV7()`.
- **Don't skip `dryRun:true`** on user-confirmable changes. The
  preview is free.
- **Don't read with raw kernel calls before a write** — use a
  `kind:query` Op so the read is consistent with the staged-db
  overlay (it sees in-flight writes from same-tx earlier Ops).
- **Don't paste plaintext idempotency keys from past runs** — they
  will return cached responses or `duplicate` errors.
- **Don't use `transactQL` for single-step actions** that have no
  preconditions and no related work. Just call the action directly.

## Output style

When invoked:

1. State the planned change in one line.
2. Show the composed `transactQL` (or `transact()`) payload.
3. Note that you'll preview with `dryRun:true` first.
4. After dryRun: report the `transaction.status`, `returns`, and
   the rollback plan; ask the user to confirm.
5. After commit: report `commitId`, `qualityDelta` (if any), and
   the post-commit `returns` shape.

## Related skills

- `/debug-with-score` — find what to fix; this skill applies the
  fix.
- `/create-concept`, `/create-implementation`, `/create-sync`,
  `/create-derived-concept`, `/create-widget`, `/create-theme`,
  `/create-suite`, `/configure-deployment` — single-target
  scaffolding skills. They know to compose multi-file outputs as
  Transactions internally; this skill is for the cross-target
  composition layer above them.
