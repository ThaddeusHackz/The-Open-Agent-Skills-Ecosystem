---
name: v-fullstack-dev
description: V 0.5.2 fullstack development (vlang.io, compiler at ~/v). Covers syntax pitfalls, veb web server + templates, db.sqlite ORM, x.json2 + net.http, concurrency (go/chan/select), C FFI (mmap/SIMD via #include+@[c_extern]), and OpenAI-compatible LLM wiring. Load whenever a task touches V language / veb / vweb / V CLI / V database / V module / V testing / V build, or a project root has v.mod. Each topic's deep detail lives in *.md — read the relevant one on demand.
version: 1.0.0
author: OWL Agent
license: MIT
---

# V 0.5.2 Fullstack Dev (v-fullstack-dev)

This skill is the consolidated entry point for V fullstack work. The main file
holds the **highest-frequency pitfalls** per topic; deep detail + copy-paste
recipes are in `*.md` — load them when you actually hit that area.

## When to load
- Project root has `v.mod`, OR task involves V / veb / V CLI / V database /
  V module / V testing / V build.
- A V compile error mentions one of: `or block`, `immutable`, `unexpected extra
  attributes`, `no such table`, `cannot convert`, `missing ':' after mut`.
- An OpenAI-compatible `/chat/completions` call returns HTTP 400 / streams oddly.

## Topic index (read the reference on demand)
- `syntax.md` — immutability, `!`/`?` split, structs, slices, strings,
  enums, closures, time, const, pcre, file I/O, `v vet` quirks.
- `veb_templates.md` — route attributes, Context struct, `$veb.html()`
  scope, static handler, i18n, SSE, HTTP integration tests, template `@if` trap.
- `db_orm.md` — sqlite ORM: primary-key types, `insert` or-block,
  `delete` where, `select` has no ORDER BY, receiver/column name clash, test
  isolation, stale-binary trap, wiring store into veb.
- `json_http.md` — `x.json2` decode/encode, `net.http` body quirk
  (use curl), SSE streaming with `on_progress_body`, OpenAI wire format basics.
- `concurrency.md` — `go`/`chan`/`select`, closure-capture copy
  semantics, `sync.Mutex` (no `defer`), `?fn` optional fn-pointer fields.
- `openai_llm.md` — the three wire-format 400 bugs (type/parameters/
  tool_call_id), system-first rule, SSE token streaming, curl bisection recipe.
- `c_ffi_mmap.md` — `#include`, `fn C.xxx()`, `unsafe { cast() }`, mmap
  pattern, `$if` platform conditionals, SIMD C interop. **C linking uses
  `#include "x.c"` + `@[c_extern]` — `#flag x.o` does NOT link.** §9b is the
  high-performance 1BRC recipe (memchr scan, integer temps, open-addressing
  hash, `-no-bounds-checking`, mmap prefault).

================================================================================
## SYNTAX — top pitfalls (detail: syntax.md)
================================================================================
- **`!T` (Result) vs `?T` (Option) are SPLIT.** `foo()?` propagation only legal
  when the enclosing fn returns `?T`. Fn returning `!T` must use `or { return err }`.
- **Struct mutability:** `mut` fields go in a `mut:` section, NOT `mut field`.
  A `pub:` field is IMMUTABLE — mutable-but-readable state needs `mut:` + a `pub fn`
  getter returning a copy. Only ONE `pub:` and ONE `mut:` section per struct.
- **`mut` args only for arrays/maps/structs/pointers — NOT scalars.** Use a local
  `mut` var instead.
- **slice assignment needs `.clone()`:** `a = b[..]` → `a = b[..].clone()` (fires
  for plain `[]string` too).
- **strings are single-quoted.** `s == ''` not `s.len == 0` (vet warning). `s[0..n]`
  is STRICT substr — guard `if s.len > n` first or it PANICS.
- **`defer` DOES exist in 0.5.2** — `defer { cleanup() }` is valid (verified in the 1BRC mmap unmap path). Use it for RAII-style cleanup.
- **`strings` must be imported** for `strings.new_builder()`; `Builder` is a value type (`mut buf := strings.new_builder(n)`), methods are `write_string/write_byte/str()/clear()`.
- **closure capture is COPY semantics:** `fn [mut x](..){ x<<.. }` does NOT mutate
  the caller's `x`. Use explicit recursion / return values, never a callback that
  collects (e.g. `os.walk` callback can't fill an outer array).
- **pcre:** `import regex.pcre`; `re.find(s)` → `?Match`, read groups with
  `m.get(i) ?string` (NOT `m[i]`). `find_from(s,pos)` finds first match at/after
  pos; check `m.start == pos` to anchor. **Look-ahead `(?=…)` is BROKEN under
  find/find_from in this build — returns no match. Avoid it.**
- **`v vet` requires every `pub fn` to have a `//` doc comment**, and `s == ''`
  over `s.len == 0`.

================================================================================
## VEB / TEMPLATES — top pitfalls (detail: veb_templates.md)
================================================================================
- **Route attr (0.5.1):** use `@['/path']` (GET inferred) or `@['/path'; post]`
  for POST-with-path. `@[post: '/path']` / `@[get: '/path']` PANIC at startup
  (`unexpected extra attributes`). Path params (`/x/:id`) hit a codegen quirk —
  prefer `?id=` query params (`ctx.query['id']`).
- **Context struct:** `run_at[A, X]` needs `X` embedding `veb.Context` as a field
  literally named `Context`. Handler 2nd param is `mut ctx WebCtx`, not `veb.Context`.
- **Template vars come from the HANDLER'S LOCAL SCOPE**, not App/Context fields.
  Declare data as locals (`countries := ...`) then reference `@countries`.
- **`$veb.html()` resolves relative to COMPILE-TIME cwd** — pass an explicit path
  like `'internal/server/templates/index.html'` and build from project root with
  `v -o bin/x cmd/x/main.v`.
- **`@(fn())` is BROKEN** in this build — compute derived values as handler locals,
  use `@var`. `@css '/x.css?v=1'` breaks the parser — use plain `<link>` tags.
- **Static files:** `App` must EMBED `veb.StaticHandler`; `handle_static` PANICS
  on unknown extensions (`.bak`, `.tmp`) — keep the static dir clean.
- **`veb.tr` returns value WITH trailing newline** — `.trim('\n')` it.

================================================================================
## DB / ORM — top pitfalls (detail: db_orm.md)
================================================================================
- **String primary key:** `id string @[primary]` (ORM infers TEXT). NEVER
  `string @[primary; sql: text]` — the unquoted `sql: text` makes `create table`
  silently fail (swallowed by `or {}`), later `select` errors `no such table`.
- **`int` primary key is a TRAP:** ORM writes `id=0` every insert → 2nd row UNIQUE
  conflict. Use `string @[primary]` and generate a unique id yourself
  (`time.now().unix_nano().str()`).
- **`insert ... into T` or-block must be NON-EMPTY and return `int`:**
  `or { 0 }`. `update`/`delete`/`select` accept bare `or {}`.
- **`delete` requires a `where` clause** (no bare `delete from T`). For truncate use
  the raw `s.db.exec('DELETE FROM T') or {}`.
- **`select` has NO `order by`** — select all, sort in V.
- **`where` bare identifiers resolve to the RECEIVER var name BEFORE the column
  name.** If a method's receiver is named `ts` and the table has a `ts` column,
  `where ts >= 0` errors cryptically. Rename the receiver (`st`).
- **Test isolation:** never point tests at a fixed on-disk DB — use a unique temp
  path per call or counts drift across `v test` runs.
- **Stale binary trap:** after editing `.v`, ALWAYS rebuild (`v -o bin/x ...`)
  before running — a stale binary looks like a storage bug.

================================================================================
## JSON / HTTP — top pitfalls (detail: json_http.md)
================================================================================
- **Use `x.json2`** for typed JSON: `x.json2.decode[T](body) !T` (generic),
  `x.json2.encode[T](val, json2.EncoderOptions{})` (2-arg, NO 1-arg encode).
  Map index needs `or {}` even when sure the key exists.
- **`net.http` `Request` builder quirk:** building `net.http.Request{...}` then
  `req.do()` and reading `.body` can fail with `assignment mismatch: 0 values`
  (compiler mis-treats `.body` as void). Reliable fallback: `os.execute('curl -s
  --max-time 10 ...')` and parse `res.output` (also satisfies the system-tool /
  exec-gate discipline). Top-level `http.get(url)` is fine for simple GETs.
- **HTML-escape any LLM/user text before injecting into a template or SSE HTML.**

================================================================================
## CONCURRENCY — top pitfalls (detail: concurrency.md)
================================================================================
- **`go` + `chan` + `select`** exist; `spawn` cannot take mutable non-reference
  args — pass a `&T` reference or a struct holding the data.
- **Closure capture is COPY** (see syntax) — a `go fn [mut x](){}` mutating `x`
  does not sync back. Share via a `chan` or a `sync.Mutex`-guarded struct.
- **`defer` DOES exist in 0.5.2** — `defer { mu.unlock() }` is valid (verified in the 1BRC mmap unmap path). Use it for RAII-style cleanup; only fall back to explicit unlock if a scope-specific order is needed.
- **`?fn` optional fn-pointer field** must be called with `?`: `t.run?(args)` returns
  the bare `Ret` (no `or` needed).

================================================================================
## OPENAI-COMPATIBLE LLM — top pitfalls (detail: openai_llm.md)
================================================================================
When wiring a ReAct agent to any OpenAI-compatible `/v1/chat/completions` (Shangtang
sensenova, OpenRouter, Ollama, vLLM, …) in V 0.5.1, THREE wire-format bugs cause
HTTP 400 even when `v vet` is clean:
1. **`type` field serializes as `ty`** → tag it `ty string @[json: 'type']`.
2. **`parameters` must be a JSON OBJECT, not a string** → type it `json2.Any`,
   build via `json2.decode[json2.Any]('{...}') or { json2.Any{} }`. **Cover EVERY
   tool def** (tools spread across files — `patch.v`'s `patch` tool is the classic
   miss). Verify with `grep -rn '"parameters":"' agent/` → must be ZERO matches.
3. **Tool-result messages need `tool_call_id`** matching the assistant turn's
   `tool_calls[].id`, else `400 invalid tool_call_id`. `messages` must be
   `[]json2.Any` (not `[]map[string]string`); first message must be `role: system`.
- **Streaming (SSE):** use `http.Request` + `on_progress_body`; the callback is
  COPY-semantics (don't accumulate state inside it — re-parse `resp.body` after
  `do()`). Shangtang emits `reasoning` BEFORE `content` — capture both.
- **401 = key problem; 400 = wire-format problem.** Bisect with curl (see reference).

================================================================================
## Workflow
- Prefer stdlib (`~/v/vlib/`: yaml, json, regex.pcre, db.sqlite) over hand-rolling.
  `import yaml` — do NOT hand-roll a YAML parser.
- Anchor runtime paths to `os.executable()` + `v.mod` sentinel, not `os.getwd()`.
- Gate: `v fmt -w . && v vet . && v -silent test .` before declaring done.
