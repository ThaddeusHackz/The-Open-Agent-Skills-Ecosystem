---
name: e2e-scenario-design
description: Use when an agent:claude-code task asks for E2E scenario design for a story, including QA E2E specs under specs/qa/, User Manual specs under specs/manual/, follow-up task identification, no-change close decisions, and User Manual publication instruction checks.
---

# e2e-scenario-design

Act as a Playwright Planner for a story. Read the story Issue, acceptance
criteria, and the story diff, then create or update scenario design specs for
QA E2E and User Manual coverage.

## Inputs

- Story Issue body, comments, and Acceptance Criteria.
- The story diff, normally `git diff origin/<target>...HEAD` or the task PR
  diff supplied by Orchestra.
- Existing specs under `specs/qa/` and `specs/manual/`.
- Existing tests under `tests/qa/` and `tests/manual/`.
- Existing generated manual output under `manual/`, when present.

## Scope

- Create or update QA E2E plans under `specs/qa/`.
- Create or update User Manual plans under `specs/manual/`.
- Identify follow-up implementation tasks for QA test implementation or Manual Generator.
- Identify Healer follow-up tasks when generated QA / Manual tests fail after
  implementation.
- Update the story Issue Test Design section with spec paths and follow-up task
  issue numbers when the task asks you to maintain the story record.
- Check whether this repository has local User Manual publication instructions
  outside the vibe-coding managed blocks.

## Out of Scope

- Implementing QA E2E tests under `tests/qa/`.
- Implementing Manual generation tests under `tests/manual/`.
- Changing Playwright config, reporters, sync scripts, rollout scripts, or CI.
- Choosing an SSG or deployment path for generated Manual files.
- Backfilling specs for unrelated existing features.

## Directory Contract

QA and Manual specs are independent sources:

- QA E2E specs: `specs/qa/<feature>.md`
- User Manual specs: `specs/manual/<feature>.md`

Do not put Manual copy in QA specs. Do not put regression-test-only coverage in
Manual specs.

## Frontmatter

Every spec starts with frontmatter:

```yaml
---
story: 123
feature: checkout
---
```

Use an array when one spec intentionally covers multiple stories:

```yaml
---
story: [123, 124]
feature: checkout
---
```

## Scenario IDs

Use `<spec-file>:<scenario-number>`.

- `<spec-file>` is the file stem under `specs/qa/` or `specs/manual/`.
- `<scenario-number>` is the Planner hierarchy number, such as `1.1` or `2.3`.
- Example: `checkout:1.2`.

Keep scenario IDs stable when editing existing scenarios. Add new IDs only for
new scenarios.

## QA Spec Format

Use Playwright Planner Markdown:

```md
---
story: 123
feature: checkout
---

# Checkout QA

## Application Overview

<Short overview of the user-facing flow and relevant state.>

## Test Scenarios

### 1. Guest Checkout
**Seed:** `tests/qa/seed.spec.ts`

#### 1.1 Complete checkout with valid card
**Scenario ID:** `checkout:1.1`

**Steps:**
1. Open the checkout page.
2. Fill valid customer information.
3. Submit payment.

**Expected Results:**
- The order confirmation is visible.
- The order number is displayed.
```

## Manual Spec Format

Use Playwright Planner Markdown with reader-facing Manual fields:

```md
---
story: 123
feature: checkout
---

# Checkout Manual

## Application Overview

<Short overview of the reader-facing workflow.>

## Manual Scenarios

### 1. Guest Checkout
**Seed:** `tests/manual/seed.spec.ts`

#### 1.1 Complete checkout with valid card
**Scenario ID:** `checkout:1.1`

**Reader Goal:**
Complete a purchase without signing in.

**Steps:**
1. Open the checkout page.
2. Fill valid customer information.
3. Submit payment.

**Manual Copy:**
Use the checkout page to enter customer and payment details. After submission,
the confirmation page displays the order number.

**Screenshots:**
- checkout-form
- order-confirmation
```

## Follow-up Task Templates

When a QA scenario needs an implementation test, first inspect the repo's existing
test stack and use its paths, commands, fixtures, and conventions. Do not assume
`tests/qa/` or Playwright unless the repo already uses that structure for QA.
Create a task with this shape:

```md
## Goal
Implement the QA coverage for `<scenario-id>` using this repo's existing test stack.

## Scope
- `<existing-test-path-for-feature>`
- Source spec: `specs/qa/<feature>.md`

## Acceptance Criteria
- [ ] The test includes comments for `spec:` and `seed:`.
- [ ] The test preserves `Scenario ID: <scenario-id>`.
- [ ] `<repo-test-command>` passes for the added or updated test.

## 関連
- Refs #<story>
```

When a Manual scenario needs a generated Manual test or prose adjustment, create
a task with this shape:

```md
## Goal
Generate or update the User Manual scenario for `<scenario-id>`.

## Scope
- `tests/manual/<feature>.spec.ts`
- Source spec: `specs/manual/<feature>.md`
- Generated review target: `manual/<feature>.md`

## Acceptance Criteria
- [ ] The test includes comments for `spec:` and `seed:`.
- [ ] The test preserves `story`, `feature`, and `scenario_id` annotations.
- [ ] Screenshots are attached with stable names from the Manual spec.
- [ ] `npx playwright test --config=playwright.manual.config.ts` produces the expected Manual markdown and screenshots.

## 関連
- Refs #<story>
```

Use `agent:claude-code` for local prose, test generation, UI exploration, test
design, or multiple files. Codex should only orchestrate the task and review the
output.

## Manual Publication Check

User Manual の公開方式は、このリポジトリの routing / build / deploy /
static asset 管理に合わせる。共通テンプレートから framework 固有の出力先
や route を推測しない。

If local publication instructions are missing or outdated:

1. Do not decide a framework-specific publication path inside the Manual
   implementation task.
2. Create a separate task to inspect routing / build / deploy / static assets.
3. Record the publication contract outside the vibe-coding managed blocks in
   both root `AGENTS.md` and root `CLAUDE.md` when both Codex and Claude need
   the rule. If the rule is Claude-only, record it in root `CLAUDE.md` and add
   a pointer from root `AGENTS.md`.

## No-impact Close Path

If the story has no QA E2E or User Manual impact, or existing specs / tests /
Manual output already cover the story without changes:

1. Record the reason in the story Issue `Test Design` section.
2. State that no `specs/qa/` or `specs/manual/` changes are required, or that
   existing coverage is sufficient.
3. Close the scenario design task without creating implementation tasks.

## Planner / Generator / Healer Consistency

This skill complements the Playwright agents generated by
`npx playwright init-agents --loop=claude`:

- Create QA plans under `specs/qa/` with this skill unless this repository
  explicitly defines a QA planner agent.
- Use `playwright-manual-planner` for Manual plans under `specs/manual/` when
  that agent is present; otherwise create Manual plans with this skill.
- For QA specs, create follow-up implementation tasks that use the repository's
  existing test stack and available agents; do not assume a QA Generator agent
  unless the repository defines one.
- For Manual specs, use generated Manual Generator / Healer agents only when
  they are present. A Healer task must include the failing test name, command
  output, and whether it may edit test code or must report a product defect.
- Keep the Planner heading hierarchy and step/expected-result structure.
- Add vibe-coding frontmatter, scenario IDs, seed references, and follow-up task
  links as required by this skill.
