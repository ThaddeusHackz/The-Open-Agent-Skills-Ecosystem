---
name: fake-server-protocol-validation
description: Use when implementing, reviewing, or testing a fake/stub database protocol server such as FakeSentinel, FakeMySQL, fake mongos, or Redis Cluster emulation. Forces golden real-server protocol comparison, protocol-aware response reads, command matrix classification, and explicit known-delta signoff instead of trusting high-level SDK behavior.
allowed-tools: Bash(go test *) Bash(rg *) Read
---

# Fake Server Protocol Validation

## Hard Rules

1. **Compare against a real server.** A fake server is not compatible until the same raw request has been sent to both real and fake implementations.
2. **Validate protocol frames, not only SDK results.** Client SDKs can hide fallback, retries, and tolerant parsing.
3. **Use a protocol-aware reader.** Read exactly one complete response according to the protocol grammar; never read "N lines" or "until timeout".
4. **Classify every delta.** Each command is `full match`, `known content delta`, `known type delta`, or `blocker`.
5. **Client-consumed fields are mandatory.** A fake may omit unused metadata only after the supported client read set is listed and verified.
6. **Unknown type mismatch blocks merge.** Do not accept `+` vs `*`, `$` vs `-`, OK vs ERR, or equivalent protocol type drift without explicit architecture signoff.
7. **Final report must separate matches, known deltas, and blockers.**

## When To Invoke

Use this skill when:

- implementing a fake / stub database protocol service
- reviewing a fake server PR
- adding golden protocol tests for FakeSentinel, FakeMySQL, fake mongos, Redis Cluster emulation, or similar services
- debugging a client that silently fails or behaves differently against the fake service
- someone says "the SDK test passed" but no raw protocol comparison exists

Common trigger phrases: `fake server protocol compat check`, `fake server RESP validation`, `golden protocol comparison`, `FakeSentinel compatibility`.

## Workflow

1. **Start both services**
   - Real server: the closest supported upstream version.
   - Fake server: the implementation under review.
   - Keep fixtures minimal and deterministic.

2. **Send identical raw requests**
   - Use the same command bytes for real and fake.
   - Include happy paths and negative paths.

3. **Read one complete response**
   - RESP: simple string / error / integer = one line; bulk string = length + bytes; array = recursive elements.
   - Other protocols: use packet/header length rules.
   - A timeout is a test failure, not a successful read strategy.

4. **Normalize only volatile values**
   - Allowed: generated IDs, timestamps, endpoint addresses, bulk length markers when payload is compared separately.
   - Not allowed: protocol type, array shape, error-vs-success semantics, required client fields.

5. **Classify each command**

| Category | Meaning | Review Action |
|---|---|---|
| `full match` | Frame type and normalized payload match | Accept |
| `known content delta` | Same frame type; documented content difference | Accept only if client-read fields are covered |
| `known type delta` | Frame type differs with explicit architecture reason | Rare; needs owner signoff |
| `blocker` | Unknown delta, missing required field, or wrong type | Fix before merge |

6. **Verify client field coverage**
   - List the fields read by each supported client/library.
   - Prove those fields exist in the fake response.
   - Add a subtest for field coverage if the response intentionally omits real-server metadata.

## Review Checklist

Before approving:

- [ ] Real server and fake server are both exercised.
- [ ] The test sends the same raw request to both.
- [ ] The reader is protocol-aware and does not wait for timeout as normal control flow.
- [ ] Every supported command appears in a command matrix.
- [ ] Negative/error paths are included.
- [ ] All client-consumed fields are listed and verified.
- [ ] Every accepted delta has a reason.
- [ ] The final report clearly distinguishes matches, known deltas, and blockers.

## Closeout Format

Use a specific closeout:

```text
Protocol validation passed: real and fake services compared with raw requests; reader is protocol-aware; command matrix has N full matches and M documented known deltas; supported client fields are covered; no unclassified type mismatch remains.
```

Avoid vague closeouts:

```text
Fake server works with the client.
```

## Related Docs

- `docs/addon-fake-server-protocol-validation-guide.md`
