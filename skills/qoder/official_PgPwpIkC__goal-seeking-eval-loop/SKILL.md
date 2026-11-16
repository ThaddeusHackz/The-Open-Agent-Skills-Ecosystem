---
name: goal-seeking-eval-loop
description: Run autoresearch-style bounded optimization loops for code, product, data, or pipeline improvement. Use when Codex should define a fixed eval set, objective function, scalar score, hard constraints, incumbent/challenger keep-discard rule, max_cycles, epsilon/convergence criteria, and iterative mutation loop; when users ask for goal-seeking, eval-led iteration, "autoresearch for X", optimization loops, dynamic pipeline tuning, or Codex-native orchestration with up to N subagents. Prefer this skill before creating custom loop frameworks; optionally map the contract to Gas City convergence when an external agent runtime is desired.
tags: [workflow, goal-seeking, evals, orchestration, codex, autoresearch]
---

# Goal-Seeking Eval Loop

Use this skill to turn fuzzy iterative improvement into a disciplined
bounded optimization loop:

```text
fixed eval set -> mutate candidate -> run evaluator -> score objective -> keep/discard -> repeat
```

The skill is orchestration guidance, not a new framework. Keep domain logic in
the target repo, use Codex subagents only when helpful, and make the evaluator
output legible enough that each cycle knows what to improve next.

Default posture: maximize the objective until the loop budget, convergence, or
a strategic blocker stops the run. A first passing gate is a feasibility
milestone, not completion, unless the user explicitly asks for minimum viable
completion.

## Core Contract

Before starting implementation loops, define these artifacts:

1. **Goal**: the product or engineering outcome, in one sentence.
2. **Eval set**: fixed cases that represent success. Do not change them to
   flatter experiments.
3. **Mutable surface**: files, services, prompts, data paths, schemas, UI
   layers, or operational knobs the orchestrator may change.
4. **Frozen surface**: evaluator, scoring rules, production safety rules,
   secrets rules, and anything explicitly out of scope.
5. **Final gate**: one gate with N required criteria. Do not default to phases
   or sub-gates. This is the minimum validity gate, not the optimization
   objective.
6. **Objective function**: scalarized objective to maximize or minimize, with
   weights and penalties. It may summarize a vector `F(x)`.
7. **Constraints / hard gates**: invalid states that cannot be kept even if the
   score improves.
8. **Evaluator result schema**: the JSON fields required by the loop.
9. **Incumbent state**: best valid candidate so far, including score and commit
   or artifact pointer.
10. **Keep/discard rule**: what makes a candidate replace the incumbent.
11. **Loop budget and convergence**: max cycles, epsilon, plateau window, and
    distinct-mutation requirement.
12. **Subagent budget**: max concurrent subagents, ownership boundaries, and
    whether they may edit or only evaluate.
13. **Artifact root**: where loop logs, score JSON, commands, post-mortems, and
    manual evidence are stored.

If any item is missing, write the loop spec before dispatching agents.

Think of the loop in the `~/autoresearch` shape: frozen evaluator and data prep
like `prepare.py`, mutable pipeline/code like `train.py`, and a results ledger
like `results.tsv`. Translate that discipline to the current domain; do not
copy domain-specific code.

## Run Spec

The run spec lives in `run.yaml` or `run.json` under the artifact root. It is
the contract for every cycle, not a note for the first run only. It must define:

- frozen eval set and case identifiers;
- frozen scorer/evaluator command, version, or artifact pointer;
- mutable surfaces the loop may change;
- frozen surfaces the loop must not change;
- hard constraints and final-gate criteria;
- `max_cycles`, `epsilon`, `plateau_window`, and stop conditions;
- objective direction, scalarization rule, objective weights, and penalties;
- incumbent artifact or commit pointer;
- artifact root and expected ledger paths.

If final product quality depends on an LLM or any other stochastic component,
the run spec must also define:

- the live execution path used for acceptance (model/runtime/provider path);
- accepted noise controls (repeats, quorum, replay, tolerance);
- the minimum live-proof evidence required for final acceptance.

The eval set must be materialized before mutation begins. "Materialized" means
the run spec points to concrete case records, fixtures, URLs, prompts, input
rows, or artifact IDs that the evaluator can actually consume. A prose-only
intent such as "test many jurisdictions" or "try representative cases" is not a
frozen eval set. If the fixed cases are still missing, the next action is eval
set construction, not product or pipeline mutation.

Every cycle post-mortem must reread `run.yaml` or `run.json` before choosing the
next mutation. If the proposed mutation changes the eval set, scorer, objective
weights, hard constraints, or frozen surfaces, stop and treat it as a new or
materially changed objective that requires Objective Preflight before any
mutation continues.

Every cycle must also write exact replayable commands to
`<artifact-root>/cycles/<NNN>/commands.txt`. This file is mandatory evidence.
For each command, record:

- full command line;
- command working directory (`cwd`);
- inputs consumed (files, fixtures, prompts, IDs);
- outputs/artifacts produced (paths, result files, logs);
- environment/context notes needed for replay.

Placeholders like "see shell history", "same as before", or omitted cwd/input
details are not allowed.

When the objective depends on per-case extraction, classification, or scored
evidence quality, each cycle must also emit structured audit artifacts, using
these names or clearly equivalent names declared in the run spec:

- `before-after-deltas.json`: per-case incumbent vs candidate deltas, net
  deltas, and regressions.
- `evidence-ledger.json`: source-cited evidence for every scored claim, slot,
  classification, or upgrade, including citation/location/method; if evidence
  is missing, record the missing-evidence reason.
- `blocker-queue.json`: blocker class counts, affected cases, dominant
  blocker, and highest-leverage next cases.
- `aggregate.json` or cycle summary fields for `mutation_class` and
  `mutation_surface`; routing-enabled loops must also include
  `dominant_route_class` and `recommended_next_mutation_surface`.

Artifacts used to justify improvement must be fresh for the candidate being
evaluated. A post-mortem should cite these structured files and key IDs, not
only prose descriptions.

When the loop optimizes a multi-stage product pipeline, the run spec must also
declare any routing, diagnostic, proxy-validation, and post-mortem criteria
artifacts required by the sections below. Do not let a scalar score stand in for
pipeline diagnosis when the next mutation could belong to different subsystems.
After Objective Preflight and any required routing/proxy diagnostics pass, the
orchestrator continues autonomously through candidate cycles until a declared
stop condition is reached. Passing those diagnostics is permission to proceed
under the run spec, not a pause for another approval.

## Objective Preflight / Evaluator Sanity

Before the first mutation, run Objective Preflight when the objective, scorer,
weights, eval set, or hard constraints are new or materially changed. The goal
is to prove the evaluator can reject bad candidates and detect meaningful
improvement before agents optimize against it.

Preflight must replay the scorer against at least one of:

- prior artifacts from earlier runs, including known failures and known better
  incumbents when available;
- synthetic adversarial cases designed to trigger specific failure modes;
- an unchanged baseline and a small controlled perturbation with expected
  objective direction.

The preflight must prove the objective responds to these failure modes:

- saturated average score: average/aggregate metrics cannot stay high when
  important slices fail;
- fake precision: decimal or rubric detail does not imply reliability when
  evidence is missing or weak;
- hard gate failures: binary invalid states fail even when the scalar score is
  otherwise high;
- one-slice overfit improvement: improving one slice while regressing others is
  penalized or rejected;
- stochastic noise: repeated or replayed runs show the score delta is larger
  than expected noise before keep/discard;
- objective delta vs incumbent: the scorer reports candidate score, incumbent
  score, direction, and delta using the run spec's objective rule.

Record the preflight command, artifacts, expected outcome, actual outcome, and
pass/fail verdict under `<artifact-root>/baseline/`. If preflight fails, do not
mutate the product or pipeline; fix the evaluator, scorer, or run spec first.
If post-mortem evidence later shows the scorer rewards the wrong product
behavior, stop product mutation immediately and run Objective Preflight again
after scorer repair before any new candidate cycles.

When Objective Preflight passes, and any run-spec-required routing or proxy
diagnostics also pass, continue autonomously until `max_cycles_reached`,
`convergence_stability`, `strategic_blocker`, `unsafe_or_invalid_search_space`,
or explicit user interruption. Do not insert a permission pause merely because
preflight or diagnostics completed.

## Single-Gate Rule

The default abstraction is **one final gate with N criteria**.

```text
Final gate:
- criterion A
- criterion B
- criterion C
- criterion D
```

Passing one criterion is progress only. Passing the whole final gate means the
candidate is feasible. In optimization mode, feasibility does not stop the run;
it creates or updates the incumbent.

After every cycle:

1. read evaluator `passed`;
2. if false, read `failing_criteria` and `dominant_blocker`;
3. choose one or two mutation targets that directly address the dominant
   blocker;
4. rerun the evaluator;
5. if feasible and the objective improves enough, promote the candidate to
   incumbent;
6. stop only when max cycles are exhausted, convergence is stable, a strategic
   blocker appears, or the run was explicitly configured as
   `minimum_viable_completion`.

Use phases only when the user or domain spec explicitly asks for them. If a
domain spec uses phases, it must still say whether passing one phase means
`STOP_FOR_REVIEW` or `AUTO_CONTINUE`.

## Optimization Contract

Model the loop like AutoML:

```text
x_n = candidate pipeline/configuration/code state at cycle n
F(x_n) = objective vector
Obj(x_n) = scalarized objective score derived from F(x_n)
C(x_n) = hard constraints / feasibility checks
```

The orchestrator searches for the best valid incumbent:

```text
incumbent = best valid x seen so far
for cycle in 1..max_cycles:
    candidate = mutate(incumbent, dominant_blocker or exploration_policy)
    evaluate candidate
    if C(candidate) fails:
        discard or repair; record diagnostic
    elif Obj(candidate) improves over incumbent by >= epsilon:
        keep candidate as incumbent
    else:
        discard or keep only as diagnostic; count toward convergence window
```

Required optimization fields in `run.json`:

```json
{
  "mode": "bounded_global_optimization",
  "objective": "maximize product-quality score",
  "objective_direction": "maximize",
  "objective_weights": {
    "quality": 1.0,
    "complexity_penalty": -0.2
  },
  "frozen_eval_set": "artifacts/evals/<feature-key>/eval_cases.json",
  "frozen_scorer": "artifacts/evals/<feature-key>/scorer.py",
  "mutable_surfaces": ["src/pipeline/", "prompts/"],
  "hard_constraints": ["no_secret_access", "no_static_demo_output"],
  "max_cycles": 10,
  "epsilon": 2.0,
  "plateau_window": 3,
  "artifact_root": "artifacts/evals/<feature-key>/",
  "pass_gate_is_feasibility_only": true,
  "stop_on_gate_pass": false,
  "convergence_requires_distinct_mutation_targets": true
}
```

Use `minimum_viable_completion` as an alternate mode only when the user
explicitly asks to stop once the final gate passes. Do not infer that mode from
a pass/fail gate, and do not treat it as a convergence stop inside
`bounded_global_optimization`.

## Incumbent / Challenger Rule

Track an incumbent separately from the latest cycle. Failed experiments are
useful evidence but should not overwrite the best known valid state.

Keep a candidate when it:

- satisfies hard constraints;
- improves the objective by at least `epsilon`; or
- closes a hard gate and does not reduce objective quality beyond the domain's
  allowed tolerance.

Discard or revise a candidate when it:

- violates a hard constraint;
- regresses the objective beyond allowed tolerance;
- improves a proxy metric while failing the product objective;
- adds complexity or brittleness with no material objective gain.

A candidate cannot replace the incumbent when artifacts required to audit the
claimed improvement are missing, stale, or only described in prose. Treat that
as a discard or repair, even if the scalar score improved.

Branch discipline is required. A discarded candidate must not silently become
the mergeable branch state. After discard, do one of:

- revert the candidate from the mergeable branch;
- isolate it on a diagnostic-only branch/worktree;
- keep it in place only when explicitly marked non-mergeable in artifacts and
  handoff.

PR eligibility must point to either:

- the best kept incumbent; or
- an explicitly documented diagnostic PR that is marked non-mergeable.

All else equal, prefer the simpler candidate. Small improvements that add large
custom-code or operations burden should pay an explicit complexity penalty.

## Stop Conditions

In bounded optimization mode, stop only on:

- `max_cycles_reached`;
- `convergence_stability`: objective improvement `< epsilon` for
  `plateau_window` consecutive materially distinct mutation attempts;
- `strategic_blocker`: a decision, dependency, missing credential, external
  outage, or safety rule prevents continued search;
- `unsafe_or_invalid_search_space`: further mutation would violate frozen
  surfaces or product safety;
- explicit user interruption.

Do not stop only because the candidate passed the feasibility/final gate.

## Evaluator Result Schema

Prefer JSON that can drive the next cycle without interpretation by memory:

```json
{
  "passed": false,
  "scalar_score": 67.5,
  "dimension_scores": {
    "coverage": 18,
    "analysis": 14
  },
  "hard_gate_failures": [],
  "failing_criteria": ["analysis_below_threshold"],
  "dominant_blocker": "analysis_gap",
  "candidate_next_mutation_target": "analysis",
  "objective_score": 72.5,
  "incumbent_score": 70.0,
  "objective_delta": 2.5,
  "keep_decision": "keep",
  "mutation_class": "evidence_recovery",
  "mutation_surface": "source_acquisition",
  "dominant_route_class": "SOURCE_WINDOW_BLOCKED",
  "recommended_next_mutation_surface": "source_acquisition",
  "convergence_state": {
    "epsilon": 2.0,
    "plateau_count": 0,
    "plateau_window": 3
  },
  "verdict": "blocked",
  "notes": "analysis lacks source-bound parameter table"
}
```

Required per-slice fields:

- `slice_id`
- `passed`
- `scalar_score` or `score`
- `dimension_scores` or `dimensions`
- `hard_gate_failures`
- `failing_criteria`
- `dominant_blocker`
- `verdict`

Optional fields:

- `candidate_next_mutation_target`
- `objective_score`
- `incumbent_score`
- `objective_delta`
- `keep_decision`
- `mutation_class`
- `mutation_surface`
- `dominant_route_class`
- `recommended_next_mutation_surface`
- `convergence_state`
- `notes`
- `diagnostics`

For routing-enabled loops, `dominant_route_class` and
`recommended_next_mutation_surface` are required aggregate fields even though
they are optional for single-stage evaluator results.

`scalar_score` is the evaluator's slice-level quality score. `objective_score`
is the scalarized optimization target after any weights or penalties; if a
domain does not define a separate objective, use `scalar_score` as the
objective. Incumbent comparison must use `objective_score` when present.

Candidate mutation target is advisory. The orchestrator owns the final
`next_mutation_target` in the post-mortem/cycle plan.

Use domain-specific verdicts only in the domain spec. The generic skill
vocabulary is:

```text
approved
blocked
rejected
unclassified_failure
```

## Multi-Stage Pipeline Routing

If the product has sequential subsystems, the evaluator must help the
orchestrator decide which subsystem to mutate next. Examples include
`source -> extraction -> handoff -> analysis -> review`, retrieval-augmented
answering, ETL-to-UI pipelines, or any workflow where a downstream failure may
be caused by an upstream data gap.

The run spec must define:

- the subsystem chain, in order;
- route classes, with the meaning of each class;
- which mutation surfaces are allowed for each route class;
- the diagnostic command or artifact that assigns routes;
- how route transitions count as progress;
- what to do when the route is ambiguous or unclassified.

Each routing-enabled cycle must emit `blocker-routing.json` or an explicitly
declared equivalent. Required per-case routing fields:

- `slice_id` or case identifier;
- `route_class`;
- `route_confidence` or a reason-coded confidence bucket;
- `subsystem_chain_position`;
- `recommended_mutation_surface`;
- `upstream_dependency`, if any;
- `downstream_probe_status`, if available;
- `route_transition` when comparing incumbent to candidate.

Required aggregate routing fields in `aggregate.json`, cycle summary fields, or
an explicitly declared equivalent:

- `dominant_route_class`;
- `recommended_next_mutation_surface`.

Route classes are domain-specific, but must be specific enough to distinguish
upstream data failures from downstream analysis or presentation failures. For
example:

```text
SOURCE_WINDOW_BLOCKED
EXTRACTION_BLOCKED
ANALYSIS_HANDOFF_BLOCKED
ANALYSIS_REASONING_BLOCKED
READY_OR_PASSING
UNCLASSIFIED_FAILURE
```

If the orchestrator cannot distinguish between two or more subsystem blocker
classes, the next cycle must build or run the diagnostic that can distinguish
them. Mutating the easiest visible surface before routing is known is
search-policy failure unless the cycle is explicitly marked exploratory.

Once required routing diagnostics pass, the routing artifact's
`dominant_route_class` and `recommended_next_mutation_surface` drive the next
cycle decision unless the post-mortem records a higher-leverage pivot. This is
an autonomous next-cycle decision, not a permission checkpoint.

For routing-enabled loops, a kept cycle should show either scalar improvement,
hard-gate closure, or a useful route transition such as:

```text
SOURCE_WINDOW_BLOCKED -> EXTRACTION_BLOCKED
EXTRACTION_BLOCKED -> ANALYSIS_HANDOFF_BLOCKED
ANALYSIS_HANDOFF_BLOCKED -> READY_OR_PASSING
```

The post-mortem must cite the routing artifact and explain why the next
mutation target follows from the dominant route or from a documented
higher-leverage pivot.

## Proxy Validation

If the objective optimizes an intermediate proxy for downstream product value,
the run spec must say how that proxy will be validated. A proxy may be useful,
but it cannot silently become the product objective.

Examples:

- extraction slot or join score as a proxy for economic-analysis quality;
- retrieval coverage as a proxy for answer quality;
- adapter contract pass rate as a proxy for user-visible workflow success;
- UI snapshot score as a proxy for task completion.

The run spec must define:

- the proxy metric and the downstream product metric it is supposed to improve;
- when correlation or non-regression is checked;
- accepted noise controls for stochastic downstream probes;
- the artifact that records proxy-vs-downstream movement.

Use `proxy-correlation.json` or an explicitly declared equivalent when a proxy
drives keep/discard decisions. The artifact should record, per case, the proxy
delta, downstream outcome delta, and whether the proxy movement helped,
stalled, or contradicted product value. If a proxy improves for repeated cycles
while downstream product quality does not improve, stop product mutation and
re-run Objective Preflight or mark the proxy as diagnostic-only.

## Mutation Causality Isolation

The loop must be able to learn which mutation caused a score or route change.
When multiple pipeline subsystems can affect the same outcome, mutate one
subsystem per cycle by default and freeze the others.

Examples:

- freeze analysis prompts while changing source windows or extraction code;
- freeze extraction outputs while changing analysis prompts or reviewer rubrics;
- freeze data fixtures while changing UI rendering or handoff presentation.

A candidate that changes multiple subsystem surfaces in the same cycle cannot
replace the incumbent unless one of these is true:

- the run spec explicitly allows that combination;
- the cycle is tagged `vertical_slice_repair` and the post-mortem explains why
  a coupled change is necessary.

Otherwise, treat the candidate as diagnostic-only or discard it, even if the
scalar score improved. Record causality violations in the post-mortem and in
the aggregate artifact when possible.

For multi-stage causality isolation, the default maximum is one subsystem or
mutation surface per cycle. Use multiple surfaces only when the run spec permits
that combination or the cycle is tagged `vertical_slice_repair`. When the run
spec permits a coupled mutation, it must declare the fresh artifacts used to
attribute improvement to each changed surface.

## Postmortem Criteria

Each run spec must predeclare how the final post-mortem will assign progress
verdicts. This prevents narrative verdicts from drifting after the loop sees
the outcome.

Required run-spec fields:

```yaml
postmortem_criteria:
  required_in_run_spec: true
  preflight_required: true
  final_postmortem_required: true
  verdict_scale:
    - MASSIVE_PROGRESS
    - MATERIAL_PROGRESS
    - INCREMENTAL_PROGRESS
    - FRAMEWORK_ONLY
    - FAILED
```

Objective Preflight must reject a run spec whose required post-mortem criteria
are missing, non-numeric where numeric thresholds are needed, or not tied to
concrete evaluator fields.

Use domain-specific thresholds, but preserve these generic meanings:

- `MASSIVE_PROGRESS`: the final gate passes, hard constraints hold, required
  live/manual proofs pass, and evidence artifacts support the claimed product
  improvement.
- `MATERIAL_PROGRESS`: predeclared material thresholds are met, hard
  constraints hold, and the final gate does not pass.
- `INCREMENTAL_PROGRESS`: the objective or at least one product metric improves
  below material thresholds without hard-constraint regression.
- `FRAMEWORK_ONLY`: evaluator, logging, runner, or tooling improved, but no
  predeclared product metric or route state moved materially.
- `FAILED`: no valid incumbent, hard-constraint regression, unsupported or
  synthetic/mock-only product proof, or unclassified final failure.

Do not define `MASSIVE_PROGRESS` as "final gate OR easier alternative criteria"
unless the domain spec explicitly defines a separate full product gate with the
same evidentiary strength. By default, massive means the full final gate passed.

## Defaults

Use these defaults unless the user overrides them:

- **Implementation model**: `gpt-5.3-codex`
- **Reasoning effort**: `medium`
- **Max concurrent implementation subagents**: `2`
- **Max concurrent evaluator subagents**: `1`
- **Total subagent cap per loop**: `3`
- **Max cycles**: `10`
- **Epsilon**: `2.0`
- **Plateau window**: `3`
- **Max mutation surfaces per cycle**: `2` for single-stage or independent
  surfaces; `1` for multi-stage causality isolation unless the run spec or
  `vertical_slice_repair` permits a coupled mutation.
- **Artifact root**:
  - repo work: `docs/evals/<feature-key>/` or `artifacts/evals/<feature-key>/`
  - local-only exploration: `/tmp/goal-seeking-eval-loop/<run-id>/`

For higher-risk work, lower the subagent cap and increase evaluation depth.
For broad but independent implementation surfaces, the user may raise the cap.

## Final Acceptance

Write the minimum validity gate before the first mutation. It must include:

- required eval cases or slice count;
- minimum aggregate score;
- minimum approved/successful cases;
- required live/manual checks, if any;
- hard gates that must be resolved by final acceptance;
- maximum tolerated final unclassified failures, normally `0`;
- what happens when the full gate fails.

Example:

```text
Final gate:
- run 5 fixed vertical slices
- average scalar_score >= 80
- every slice has hard_gate_failures == []
- every non-approved slice has failing_criteria and dominant_blocker
- at least 3/5 approved outputs
- admin/API verification evidence stored
- public/manual verification evidence stored
- final unclassified_failure count == 0
- if gate fails, run another cycle targeting dominant_blocker
```

Intermediate hard gates and unclassified failures may appear while the loop is
learning. They must be classified in the next post-mortem before they can guide
a kept mutation. Final acceptance is stricter.

Then write the optimization target and stop rules. The loop is complete only
when a stop condition is met, not when the minimum validity gate first passes.

## Loop Shape

Use this loop:

```text
1. Establish or load baseline score and initial incumbent, if any.
2. Read run.yaml/run.json and confirm eval, scorer, objective, constraints,
   mutable surfaces, and artifact root are unchanged or have passed Objective
   Preflight.
3. Read the previous cycle post-mortem, if any.
4. Run or inspect the evaluator output.
5. Diagnose failing_criteria and dominant_blocker.
6. Choose one mutation target for multi-stage causality isolation; otherwise
   choose one or two mutation targets.
7. Dispatch up to N subagents by outcome, not file.
8. Integrate and review changes.
9. Rerun eval set or failed cases plus regressions.
10. Compare the candidate to the incumbent, not just the previous cycle.
11. Keep if objective improves by at least epsilon, a hard gate closes without
    unacceptable objective regression, or the domain spec explicitly allows a
    diagnostic keep.
12. Discard, revise, or open a focused repair task if it does not.
13. Write the cycle post-mortem and next-cycle plan.
14. Record score, verdict, failing criteria, hard gates, artifacts, and next
    mutation target.
15. Stop only on max cycles, convergence stability, strategic blocker,
    unsafe/invalid search space, or explicit user interruption.
```

Do not run loops that only produce activity. Every loop must produce a scored
delta and a keep/discard decision.

## Stochastic Criteria

If a criterion depends on an LLM, model judge, stochastic search result, or
other non-deterministic process, do not keep or discard primarily from a single
lucky run. Before stochastic criteria affect keep/discard, use at least one:

- three or more repeats with score range recorded;
- cached identical-input replay;
- reviewer quorum from two or more independent passes;
- a deterministic proxy that the domain spec accepts.

Record the noise-control method in the cycle post-mortem. This is a loop
invariant, not a separate final-gate criterion.

If `run.yaml` or `run.json` says final product quality depends on a stochastic
component, final acceptance must execute the real live path with accepted noise
controls. Deterministic surrogate scoring in that case is readiness-only and
cannot be treated as final acceptance proof. If the live path cannot be run,
return a strategic blocker instead of declaring acceptance.

## Progression And Mutation

Each cycle must be guided by the last cycle's evidence. Use this post-mortem:

```markdown
## Cycle N Post-Mortem

### Gate Status
- passed:
- failing_criteria:
- hard_gate_failures:
- dominant_blocker:

### Run Spec Check
- run_spec_path:
- frozen_eval_set_unchanged:
- frozen_scorer_unchanged:
- objective_weights_unchanged:
- mutable_surfaces_respected:
- hard_constraints_unchanged:
- artifact_root:
- objective_preflight_required:
- objective_preflight_artifact:

### Score Delta
- incumbent_before:
- candidate_after:
- objective_delta:
- before_after_deltas_artifact:
- evidence_ledger_artifact:
- blocker_queue_artifact:
- mutation_class:
- mutation_surface:
- dominant_route_class:
- recommended_next_mutation_surface:
- kept/discarded:

### Incumbent State
- incumbent_commit_or_artifact:
- candidate_commit_or_artifact:
- new_incumbent:

### What Improved

### What Regressed

### Root Cause

### Mutation Chosen For Cycle N+1

### Why This Mutation Should Improve The Score

### Regression Cases To Rerun

### Budget State
- cycles_used:
- max_cycles:
- budget_exhausted:

### Convergence State
- epsilon:
- plateau_count:
- plateau_window:
- distinct_mutation_target:
- stop_condition_if_any:

### Skill/Runbook Lessons

### Stop/Strategy Questions
```

The cycle post-mortem writes the next-cycle decision. It does not imply a
permission pause, review gate, or required founder approval unless the
post-mortem declares a stop condition or the run spec explicitly requires
`STOP_FOR_REVIEW`.

Only mutate surfaces that plausibly address the dominant blocker, unless the
orchestrator explicitly identifies a higher-leverage pivot. If two consecutive
cycles fail to improve the same blocker, change strategy instead of repeating
similar patches.

Each cycle must target the dominant blocker class from the prior
post-mortem/evaluator unless the post-mortem records a higher-leverage pivot.
Repeating low-friction downstream mutations while hard source/provenance gates
or upstream blocker classes remain unresolved is search-policy failure and must
be recorded as such.

## Scoring Rules

Use a scalar score for comparability, but never let it hide unsafe failures.
Prefer 100-point rubrics with 4-7 dimensions.

Example:

```text
score / 100:
- 20 data coverage and provenance
- 15 adapter or contract fidelity
- 25 product output validity
- 15 citation/reviewer grounding
- 15 persistence/admin visibility
- 10 public/HITL readiness or classified diagnostic
```

Hard gates should be binary. Examples:

- unclassified failure at final acceptance
- fixture-only proof for a live-data gate
- missing provenance for material claims
- bypassing the canonical path
- unsafe secret access
- static/demo output used as product proof
- mocked model used for final acceptance when live behavior is required

Use `scripts/aggregate_scores.py` when you have JSON slice results and want a
deterministic aggregate.

## Subagent Pattern

Use subagents only when the user explicitly allows them. The orchestrator keeps
architecture, final integration, and keep/discard authority.

Recommended split:

- **Worker agents**: make bounded mutations to disjoint surfaces.
- **Evaluator agents**: run or inspect eval output and classify blockers.
- **Orchestrator**: chooses mutation targets, resolves conflicts, reruns final
  gates, commits, and reports the next decision surface.

Prompt subagents with:

- goal and current score;
- eval cases and hard gates;
- owned files or owned outcome;
- forbidden surfaces;
- validation commands;
- required artifact format.

Do not let different subagents edit the same unstable surface in the same loop.

When using Codex subagents, default implementation workers to
`gpt-5.3-codex` with `medium` reasoning. Use fewer agents when ownership is not
cleanly separable. The orchestrator should not delegate final acceptance,
architecture decisions, or merge authority.

## Artifacts And Logging

Initialize an artifact directory before the baseline run. Use
`scripts/init_run_artifacts.py` for local directories, or create the same shape
inside the repo when artifacts should be committed.

Recommended layout:

```text
<artifact-root>/
  run.json or run.yaml
  baseline/
    command.txt
    objective_preflight.md
    results.json
    logs/
  cycles/
    001/
      plan.md
      prompts/
      commands.txt
      results.json
      aggregate.json
      before-after-deltas.json
      evidence-ledger.json
      blocker-queue.json
      postmortem.md
      logs/
      screenshots/
    002/
      ...
  final/
    report.md
    aggregate.json
```

Store enough evidence to debug without rerunning immediately:

- eval input cases and version;
- commands run;
- raw logs or links to logs;
- slice result JSON;
- aggregate score JSON;
- commit SHA or sanitized `git diff --no-color` output for kept changes;
- post-mortem and next-cycle plan;
- screenshots/manual verification artifacts when UI is involved.

For evidence-quality objectives, validate that each cycle's post-mortem cites
the structured delta, evidence-ledger, blocker-queue, and mutation summary
artifacts. A command log plus prose-only narrative is not enough to audit a
claimed improvement.

Committed logs should use tracked extensions such as `.txt` or `.md`, not
extensions commonly ignored by repos such as `.log`. If storing a diff, sanitize
it or keep the commit SHA instead. Record the command working directory and keep
artifact paths relative to the repo root.

Do not store secrets. Redact tokens, cookies, API keys, and private credentials
from artifacts. Before committing artifacts, run a targeted scan for obvious
secret patterns such as `Bearer `, `op://`, `api_key`, `password`, `token`, and
long opaque credential-looking values.

## Codex-Native Vs Gas City

Use Codex-native orchestration when:

- the user wants all work inside the current Codex flow;
- the loop is exploratory or early;
- subagents are available in the current runtime;
- the orchestrator needs tight product judgment after each loop.

Use Gas City convergence later when:

- the loop needs long-running durable state outside the current Codex session;
- you need external LLM providers or non-Codex agents;
- iteration/gate state should live in Gas City artifacts and Beads;
- the workflow should continue unattended across sessions.

Gas City already provides bounded convergence loops, gates, artifacts, and
formula-based orchestration. Do not rebuild those primitives in a product repo.
This skill supplies the loop contract and domain scoring; Gas City can be one
runtime for that contract.

Read `references/gascity.md` when deciding whether to use Gas City.
Read `references/autoresearch.md` when designing the keep/discard loop.

## Output Template

When creating a loop plan, return:

```markdown
## Goal

## Eval Set

## Mutable Surface

## Frozen Surface

## Final Gate

## Objective Function

## Objective Preflight

## Constraints / Hard Gates

## Evaluator Result Schema

## Score Rubric

## Keep/Discard Rule

## Subagent Plan

## Loop Budget And Convergence Criteria

## Artifact Root

## Baseline Command

## Post-Mortem Template

## First Loop
```

## Domain Examples

Domain-specific verdicts should live in the domain plan, not the generic skill.
For an economic-analysis product, a domain plan might add:

```text
approved_quant_ready
approved_qualitative_only
approved_unable_to_estimate_with_source_bound_diagnosis
data_gap
adapter_gap
analysis_gap
persistence_gap
admin_gap
public_gap
model_gap
```

## Final Report

End each loop with:

- score before and after;
- kept/discarded decision;
- files or surfaces changed;
- failing criteria;
- dominant blocker;
- next mutation target;
- remaining hard-gate failures;
- budget state.

If the loop hits a strategic blocker, stop and name the single decision needed.
If the loop stops for convergence, state the incumbent, epsilon, plateau window,
and the distinct mutation targets that failed to improve it.
