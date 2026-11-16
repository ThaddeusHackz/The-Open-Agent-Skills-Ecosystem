---
name: debug-with-score
description: Answer debugging and navigation questions about a Clef codebase by querying Score (the code-as-data layer). Use for "where is X defined", "who uses Y", "impact of changing Z", "trace this stack", "what syncs fire on Concept/action", or any question that benefits from code-as-data introspection. Score-first; falls back to Read/Grep only when Score genuinely can't answer.
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "<question, symbol, file path, stack trace, or concept name>"
---

# /debug-with-score

Use Score to answer the user's question **$ARGUMENTS**.

Invoke this skill whenever the user asks:

- "Where is `X` defined?"
- "Who calls `Y`?"
- "What's the impact of changing `Z.ts`?"
- "Trace this stack trace."
- "What syncs fire on `Concept/action`?"
- "Show me everything about `Concept`."
- "Which views target schema `S`?"
- "Why is this test failing — walk me through the flow."

Or any other question that benefits from code-as-data introspection.

## Score-first protocol

Score exposes a **GraphQL-first** surface. Reach for these in order:

1. **`score_query(graphql, variables?, connection?)`** — typed multi-hop
   GraphQL queries. Reach for this when you know what you want. Single
   round-trip across the joined Score graph.
2. **Navigator (`score_show` / `score_list` / `score_traverse` /
   `score_back`)** — stateful breadcrumb walk for when you're orienting
   and don't have the schema in your head. `score_show` profiles a single
   entity; `score_list` browses a kind; `score_traverse` drills along a
   relation; `score_back` pops the breadcrumb stack.
3. **`flow_trace(flowId, connection?)`** — always-loaded shortcut for
   "what actually happened in this run". Bundles FlowTrace tree +
   RuntimeFlow steps + DTG overlay in one envelope.
4. **Cite the source.** Every claim should include `file:line` from
   Score's response.
5. **Show the call.** End your answer with the literal `score_query` /
   `score_show` / `flow_trace` call you ran so a human can reproduce.
6. **Fall back to Read/Grep** only when Score genuinely returns
   null/empty for a question that should have an answer (and file the
   gap).

> **Tip.** GraphQL is for when you know the schema. Navigator is for
> when you're orienting. Reach for Navigator first when exploring;
> switch to `score_query` when you know what you want.

## Connection-aware

Every promoted tool (`score_query`, `score_show`, `score_list`,
`score_traverse`, `score_back`, `flow_trace`, `transaction_submit`,
`transactql`) accepts an optional **`connection: "<profile>"`**
parameter. Without it, calls run against the in-process kernel that
booted the MCP server. With it, calls route through `Connection/invoke`
to a running clef-base at the named profile's endpoint (token loaded
from OS keychain). See CLAUDE.md "Connecting to a running clef-base"
and `docs/cli/auth.md` for setup (`clef auth login <profile>
--endpoint <url>`).

Every recipe below accepts `connection: "<profile>"` as an additional
argument to target a remote instance.

## Quick recipes — GraphQL

> **"Where is concept X defined?"**
>
> ```
> score_query("{ concept(name: \"X\") { conceptName purpose stateFields { name type } actions } }")
> ```
>
> Returns `{ data: { concept: { ... } | null } }`. If `null`, the
> concept name is unknown to the index — try `score_list(kind:
> "concept")` to browse.

> **"Who triggers `User/register`? Who does it affect?"**
>
> ```
> score_query("{ action(concept: \"User\", name: \"register\") { triggeringSyncs { name effects { concept { name } action } } affectingSyncs { name triggers { concept { name } action } } } }")
> ```
>
> `triggeringSyncs` are syncs whose `when` matches this action;
> `affectingSyncs` fire effects targeting it.

> **"Show me the source of `User/register`."**
>
> ```
> score_query("{ action(concept: \"User\", name: \"register\") { source variants { name } handler { handlerFile } } }")
> ```
>
> `source` returns the exact handler method body; `handler.handlerFile`
> gives the file path.

> **"Tell me everything about `User/register` in one query."**
>
> ```
> score_query("{ action(concept: \"User\", name: \"register\") { source variants { name } handler { handlerFile methodName } triggeringSyncs { name effects { concept { name } action } } affectingSyncs { name } } }")
> ```

> **"What does concept X depend on, and what depends on X?"**
>
> ```
> score_query("{ concept(name: \"X\") { dependsOn { name } dependents { name } } }")
> ```

> **"Find syncs connecting X and Y."**
>
> ```
> score_query("{ syncs(involves: [\"X\", \"Y\"]) { name annotation triggers effects file } }")
> ```

> **"Search for concepts mentioning Z."**
>
> ```
> score_query("{ concepts(filter: \"Z\") { name purpose } }")
> ```
>
> Or `score_list(kind: "concept")` to browse all of them.

> **"Resolve this stack trace to concepts + AST."**
>
> ```
> score_query("query Q($t: String!) { resolveStackTrace(text: $t) { frame { file line astNode { kind text startLine endLine } astAncestors { kind text } } concept actionName handler { handlerFile } } }",
>   variables: "{\"t\": \"<stack-trace-text>\"}")
> ```
>
> Each frame carries the **exact AST node** at the error site
> (e.g., `await_expression` inside an `if_statement` inside the
> `register` method) plus an ancestors chain. Tree-sitter is
> initialized at boot; first call returns real AST data.

> **"Which step in this flow caused the failure?"**
>
> ```
> score_query("query Q($t: String!, $f: String!) { correlateStackTrace(text: $t, flowId: $f) { isFailing frame { astNode { kind text } } matchedStep { variant syncName } } }",
>   variables: "{\"t\": \"<stack>\", \"f\": \"<flowId>\"}")
> ```
>
> Joins resolved frames with flow records by `(concept, action)` and
> sets `isFailing: true` on the cascade-leaf record whose variant is
> non-ok — the single-shot answer to "which step caused this error".

> **"What happened in this run?"**
>
> ```
> flow_trace(flowId: "<flowId>")
> ```
>
> Always-loaded primary tool. For finer projection use:
>
> ```
> score_query("{ flowTraceFull(flowId: \"<flowId>\") { trace steps dtgOverlay } }")
> ```
>
> Every `kernel.invokeConcept` returns a `flowId`.

> **"Trace an HTTP endpoint to its concepts."**
>
> ```
> score_query("{ interface(name: \"<name>\") { endpoints { path method concept action } } }")
> ```

> **"What handlers + actions exist for X?"**
>
> ```
> score_query("{ handler(concept: \"X\") { handlerFile actionEntities { name source variants { name } } astTree } }")
> ```

> **"Find all widgets / themes / views."**
>
> ```
> score_query("{ widgets { name file } themes { name file } views { clefViewName file } }")
> ```

## Quick recipes — Navigator browse

> **"Profile a single concept (with all related items)."**
>
> ```
> score_show(kind: "concept", name: "X")
> ```
>
> Then drill into actions / syncs / handler:
>
> ```
> score_traverse(relation: "actionEntities", target: "register")
> score_traverse(relation: "triggeringSyncs", target: "<sync-name>")
> score_back()
> ```

> **"Profile an action."** (MAG-SC-3/4)
>
> ```
> score_show(kind: "action", name: "User/register")
> ```
>
> Returns variants, fixtures, source, `handler.methodName`,
> `triggeringSyncs[]`, `affectingSyncs[]` in one payload.

> **"Inspect a runtime flow."** (MAG-SC-3/4)
>
> ```
> score_show(kind: "flow", name: "<flowId>")
> ```
>
> Same envelope as `flow_trace(flowId: ...)` but reachable via
> `score_traverse` from a step / runtimeconcept.

> **"Drill into the AST node at a position."** (MAG-SC-3/4)
>
> ```
> score_show(kind: "astnode", name: "handlers/ts/user.handler.ts:42:6")
> ```
>
> Returns `kind`, `text`, `startLine`, `endLine`, ancestors[].
> Traverse to parent / child astnodes and the owning handler.

> **"What's the live runtime registration for X?"** (MAG-SC-3/4)
>
> ```
> score_show(kind: "runtimeconcept", name: "urn:clef/User")
> ```
>
> Live runtime registration: `uri`, `registrationTime`,
> `sourceFile`, `status`. Traverses to spec `concept`, `handler`,
> and `runtimeSyncs` it triggered.

> **"Inspect a DTG node."** (MAG-SC-3/4)
>
> ```
> score_show(kind: "dtgnode", name: "<id>")
> ```
>
> DTG node profile: `kind`, `type`, `schema`, ancestors,
> descendants, owning action.

> **"Drill from cursor."**
>
> ```
> score_show(kind: "concept", name: "User")
> score_traverse(relation: "actionEntities", target: "register")
> score_traverse(relation: "triggeringSyncs", target: "notify-on-register")
> score_back()
> ```
>
> The breadcrumb walk: every `score_show` push, `score_back`
> pops, `score_traverse` drills along a typed relation. Reach
> for this when orienting; switch to `score_query` when you
> know what you want.

> **"List everything of a kind."**
>
> ```
> score_list(kind: "concept")
> score_list(kind: "sync")
> score_list(kind: "action")
> ```

## Stack-trace workflow (full)

Stack-trace resolution is an input parser, not a navigable entity —
use `score_query` first, then walk into the failing frame's entity
via `score_show`:

1. **Resolve** —
   ```
   score_query("query Q($t: String!) { resolveStackTrace(text: $t) { frame { file line astNode { kind text startLine endLine } astAncestors { kind text } } concept actionName handler { handlerFile } } }",
     variables: "{\"t\": \"<stack>\"}")
   ```
2. **Correlate to flow** (when you have a `flowId`) —
   ```
   score_query("query Q($t: String!, $f: String!) { correlateStackTrace(text: $t, flowId: $f) { isFailing frame { astNode { kind text } } matchedStep { variant syncName } } }",
     variables: "{\"t\": \"<stack>\", \"f\": \"<flowId>\"}")
   ```
3. **Walk into the failing frame** —
   ```
   score_show(kind: "astnode", name: "<file>:<line>:<col>")
   score_traverse(relation: "handler", target: "<handler-id>")
   ```
4. **Pull the full flow context** —
   ```
   flow_trace(flowId: "<flowId>")
   ```

## Cross-surface preview — the Pilot debugging peer

When the Pilot debugging-peer PRD lands, the same GraphQL surface
gains live-UI roots (`pageSnapshot`, `widget`, `overlays`, …) so a
single `score_query` can join live UI state with the spec graph —
e.g., "show me the widget instance, its bound concept action, the
sync that fired on click, and the resulting flow" in one query.
The Navigator gains corresponding kinds. Today's spec-side recipes
remain unchanged; the live-UI roots compose alongside them. See
`docs/plans/pilot-debugging-peer-prd.md`.

## When you've identified the fix — handing off to writes

Score is read-only. Once you know what to change, **never write the
fix as a stack of `Write` / `Edit` calls** — compose it as a
`Transaction`. The canonical write surfaces are:

- `transaction_submit(ops: [...], idempotencyKey: ..., connection?: "<profile>")` — explicit Op[] form.
- `transactql(query: "...", idempotencyKey: ..., connection?: "<profile>")` — EdgeQL-style DSL string.

Both compile to the same `Op[] → Transaction → Transactor` pipeline,
return the same `TransactResult { ok, returns, transaction, error }`
envelope, and accept `dryRun: true` for preview. Both honor the same
`connection:` parameter as the read tools.

Op kinds you'll typically reach for from a debug context:

- `kind:call` — invoke a concept action by name. E.g.
  `ScoreMutation/addVariant`, `SpecEdit/insertAction`,
  `Refactor/refactorByPattern`, `Article/create`, …
- `kind:ensure` — typed precondition (`exists` / `not_exists` /
  `etag` / `expectedVersion` / `predicate`).
- `kind:query` / `kind:queryProgram` — read inside the tx, capture
  via `as: "name"`, reference downstream as `$name.field`.
- `kind:add` / `kind:retract` — primitive Datomic-shaped writes for
  state shape changes.

When a stack trace points at a missing variant + a sync that needs a
new effect + a content row that needs to flip, those are three
sub-mutations — express them as **one** `transaction_submit()` (or
`transactql()`) so the fix is atomic and reviewable.

For the full reference, see CLAUDE.md "Write Semantics —
Transaction-as-Data + transactQL" and `docs/plans/write-semantics-prd.md`.

## Output style

- Lead with the answer. "Defined at `path/to/file.ts:42`."
- Bullets, not paragraphs.
- Cite every claim with `file:line` from the GraphQL response.
- End with a single trailing line showing the call you used:
  `via score_query("{ action(concept: \"User\", name: \"register\") { source } }")`.

## When NOT to use Score

- Free-text doc questions ("how does the kernel work?") → read `CLAUDE.md`.
- Cross-repo questions → Score is single-repo today.
- Live UI state in a running app — until the Pilot debugging-peer
  PRD lands, use `pilot/where` / `pilot/snapshot` directly. Score's
  static index doesn't yet cover live-UI roots.
- Git history / blame → use `git log` and `git blame`.

## Anti-patterns

- Do **not** grep for concept actions — use
  `score_query("{ concept(name: \"X\") { actions } }")`.
- Do **not** grep for cross-concept references — concepts are
  independent. Use
  `score_query("{ syncs(involves: [\"X\"]) { name effects } }")`
  to find the sync wiring.
- Do **not** read `.concept` files to understand structure — use
  `score_query("{ concept(name: \"X\") { ... } }")` which provides
  parsed, validated, cross-referenced data.
- Do **not** read `.handler.ts` files to find action code — use
  `score_query("{ action(concept: \"X\", name: \"Y\") { source } }")`.
- Do **not** manually parse stack traces — use `score_query` with
  the `resolveStackTrace(text:)` root.
- Do **not** manually trace sync chains — use `flow_trace` (or
  `score_query("{ flowTraceFull(flowId: \"...\") { ... } }")`).
- Do **not** reach for the deprecated REST verbs (`ScoreApi/getConcept`,
  `ScoreApi/getHandler`, `ScoreApi/listSyncs`,
  `ScoreApi/getDependencies`, `ScoreApi/getActionSource`,
  `ScoreApi/traceFlow`, `ScoreApi/correlateStackTrace`,
  `ScoreApi/resolveStackTrace`, `ScoreApi/traceEndpoint`). They
  duplicate `score_query` GraphQL roots and are slated for removal.
