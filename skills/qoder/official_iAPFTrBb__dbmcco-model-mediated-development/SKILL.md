---
name: model-mediated-development
description: Use when designing or building systems with AI/model calls, semantic routing, model memory, agent workflows, tool use, or model-owned decisions where coding agents might add rules, heuristics, regexes, thresholds, fallbacks, or hidden deterministic judgment.
---

# Model-Mediated Development

## Doctrine

**Model owns judgment. Code earns exceptions.**

Model-mediated architecture keeps semantic judgment in model-owned layers while
code provides reliable context, tools, schemas, memory access, execution,
evidence, governance, and audit.

Code may structure, validate, execute, persist, observe, enforce explicit
policy, and manage budgets. Code should not infer meaning unless the
architecture explicitly delegates that responsibility and records why.

## Model Agency Violation

Use violation language for architecture drift. These are not style comments;
they mean the implementation is breaking model-mediated architecture.

Primary trigger: **model agency violation**

Aliases: **agency violation**, **heuristic violation**, **fallback violation**,
**model owns that**.

If the user says any trigger phrase, stop implementation immediately. Answer:

1. What deterministic code is making or altering a semantic judgment?
2. Why should that judgment belong to the model, user, or explicit policy?
3. What should code own instead?
4. What model-mediated replacement preserves agency?
5. Is this an explicit deviation? If yes, where is it logged and when is it
   revisited?

Do not continue coding until the violation is resolved or the user approves a
tracked deviation.

## Design-First Phase

Before building, map the model-mediated shape:

- Decisions: what judgments exist?
- Owners: model, user, code, or explicit policy?
- Model surface: small, large, reasoning, non-reasoning, vision, tuned, or
  general?
- Memory: none, now-context, mid-term state, deep memory, artifacts, retrieval,
  or State System state objects?
- Orchestration: single coordinator, sequential chain, parallel specialists,
  adversarial evaluator, persona roles, or router mesh?
- Contracts: freeform, structured output, tool calls, artifacts, or
  schema-validated proposals?
- Constraints: cost, latency, context budgets, permissions, approval gates,
  evidence requirements, and policy boundaries?
- Deviations: what deterministic semantic exceptions are intentional, scoped,
  owned, and revisitable?

Default stance: semantic interpretation, routing, prioritization, timing,
relevance, risk judgment, quality judgment, summarization, classification,
escalation, and next-action choice are model-owned unless proven otherwise.

For high-uncertainty model architecture or serious drift findings, use:
`/Users/braydon/projects/experiments/docs/model-mediated/MODEL_MEDIATED_ARCHITECTURE_PANEL.md`.

## Implementation Discipline

During coding, the main failure mode is quietly moving model-owned judgment into
deterministic code.

Treat these as suspicious until proven mechanical:

- regex or keyword intent detection
- category maps for semantic routing
- hardcoded thresholds for priority, timing, relevance, risk, or quality
- fallback branches that replace, override, or rescue model judgment
- context prefetching, filtering, or withholding based on semantic assumptions
- model output rewriting instead of schema validation plus model repair
- static model, agent, or tool routing based on semantic rules
- "safety" behavior that is really an unreviewed product or policy decision
- qualitative feedback collapsed into hidden numeric scores, fixed weights,
  keyword rules, or thresholds
- accepted learning encoded directly in app code instead of represented as
  state, memory, policy, prompt/context, or an explicit deviation

Constrain models through contracts, tools, schemas, budgets, policies, and
evaluators, not hidden behavioral heuristics in application code.

## Qualitative Judgment Guardrail

For apps involving prospect fit, outreach quality, meeting nuance, authorship,
visual taste, brand fit, or relationship development, preserve qualitative
judgment as model-interpretable evidence.

Do not turn judgments like "this reply is real engagement", "this idea sounds
like the wrong author", or "this visual matches the brand but not the campaign"
into app-local thresholds, regexes, category maps, or score formulas.

The allowed pattern:

1. Code stores source evidence and human/model feedback.
2. Model interprets meaning and emits a schema-validated proposal.
3. Governance decides whether approval is required.
4. Accepted learning becomes state, memory, policy, prompt/context, or an
   explicit tracked deviation.
5. Code executes accepted effects and records artifacts.

## Violation Taxonomy

| Violation | Meaning |
| --- | --- |
| Judgment violation | Code decides intent, priority, relevance, timing, tone, risk, quality, or next action. |
| Heuristic violation | Code uses regex, keywords, thresholds, category maps, or scoring rules for semantic behavior. |
| Fallback violation | Code silently substitutes behavior when model output is absent, uncertain, inconvenient, or invalid. |
| Context violation | Code preloads, filters, or withholds context instead of exposing memory/tools and letting the model request what it needs. |
| Routing violation | Code chooses model, agent, persona, or tool path by semantic rules instead of model-mediated routing. |
| Output violation | Code rewrites, filters, or fixes model decisions instead of validating schema and asking the model to repair. |
| Deviation violation | Deterministic semantic logic is added without an explicit, scoped, revisitable deviation. |

## Ecosystem Boundaries

Use the existing ecosystem instead of inventing local process:

- **Speedrift / Driftdriver:** change-level quality and drift review. It should
  run model-mediation drift checks and emit findings such as possible model
  agency violations.
- **State System:** durable interpreted state and agent/project memory. It
  records recurring violation patterns, architecture decisions, deviations,
  unresolved meaning, and evidence-backed learning.
- **Workgraph:** execution state and follow-up work. It owns remediation tasks,
  dependencies, claims, validation, and completion.
- **GitHub:** code and collaboration record: commits, branches, PRs, issues,
  review comments, checks, releases, and source history.

Speedrift findings become evidence. State System interprets durable meaning.
Workgraph executes follow-up work.

## Deviation Handling

Deterministic semantic logic can exist only as an explicit exception.

A deviation records:

- violated or modified model-mediated principle
- deterministic behavior being allowed
- rationale and evidence
- scope and owner
- start date and review or sunset date
- migration path back to model-owned judgment, if applicable

Use direct language: "This is a model agency deviation because code is deciding
X. It is temporarily allowed because Y. It will be revisited at Z."

## References

- `/Users/braydon/projects/experiments/braydon-workspace-skills/docs/plans/2026-04-30-model-mediated-development-skill-direction.md`
- `/Users/braydon/projects/experiments/docs/model-mediated/2026-04-30-model-mediated-speedrift-implementation-plan.md`
- `/Users/braydon/projects/experiments/docs/model-mediated/MODEL_MEDIATED_ARCHITECTURE_PANEL.md`
- `/Users/braydon/projects/experiments/docs/model-mediated/MODEL_MEDIATED_REFERENCE_ARCHITECTURE.md`
- `/Users/braydon/projects/experiments/docs/model-mediated/MODEL_MEDIATED_COOKBOOK.md`
- `/Users/braydon/projects/experiments/docs/model-mediated/MODEL_MEDIATED_CONFORMANCE_TESTS.md`
- `/Users/braydon/projects/experiments/docs/model-mediated/MODEL_MEDIATED_ROUTER_MEMORY_GOVERNANCE.md`
- `/Users/braydon/projects/experiments/docs/model-mediated/MODEL_MEDIATED_DEVIATION_REGISTER.md`
