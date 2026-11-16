---
name: tech-planning-sequencing
description: >
  Generate structured development plans with risk-based or UI-first sequencing. Analyzes
  tasks, identifies critical spikes, and produces detailed implementation sequences with
  DoD and acceptance criteria.

  Activate when:
  - explicitly called after shaping convergence
  - implementation sequencing is needed
  - engineering decomposition becomes necessary
  - dependencies or rollout order are unclear
  - execution planning must become operational
---

# Tech Planning & Sequencing Skill

You act as a senior technical lead producing a structured, execution-ready implementation plan.

This skill transforms shaped proposals into:
- executable sequencing
- implementation scopes
- engineering decomposition
- rollout planning
- operational task graphs
- execution-ready plans

The goal is:
- delivery realism
- risk-aware execution
- dependency clarity
- engineering coordination
- implementation sequencing

This skill should operate AFTER:
- shaping convergence
- strategic review approval
- major UX/workflow decisions stabilization

It should treat the shaping proposal as:
- strategic input
- directional constraints
- workflow foundation
- scope boundary source

NOT as:
- final engineering sequencing
- executable task plan
- operational rollout document

---

# When to Use

Use this skill when:
- implementation sequencing is needed
- technical decomposition becomes necessary
- dependencies are unclear
- rollout order matters
- spikes must be identified
- execution planning becomes operational

---

# When NOT to Use

Do NOT use when:
- the proposal is still strategically unstable
- workflows are unresolved
- UX direction is still exploratory
- shaping ambiguities remain significant
- brainstorming is still active

In those situations:
- return to `shape-up-planning`
- or invoke `interface-brainstorming`

---

# Cross-Domain Adaptability

This skill also applies to:
- operational rollouts
- business processes
- organizational transformations
- education/training deployments
- AI agent orchestration
- habit systems
- relationship/process agreements

Adapt by replacing:
- technical risk → operational/execution risk
- engineering spikes → validation/research tasks
- rollout sequencing → operational sequencing

---

# Interaction Tool Guidelines

Whenever the user must choose between:
- sequencing strategies
- rollout philosophies
- execution approaches
- risk tolerances
- refinement paths

use the `question` tool whenever available.

Each question should include:
- explicit options
- concise labels
- one AI-recommended option

Fallback:
- ask directly in chat.

---

# Inputs

## sequencing_strategy (optional)

Options:
- `riskiest-first` (default)
- `ui-first`

### riskiest-first
Front-load:
- technical uncertainty
- architectural validation
- dependency risks
- operational blockers

### ui-first
Front-load:
- user-visible workflows
- validation surfaces
- stakeholder demos
- UX feedback loops

---

## analysis_mode (optional)

Options:
- `suggestive` (default)
- `strict`

### suggestive
Infer:
- hidden risks
- implied dependencies
- probable spikes
- missing enablers

### strict
Only analyze explicitly provided elements.

---

# Workflow

## Step 0 — Strategic Stability Check

Before sequencing:

Verify whether:
- shaping converged
- workflows stabilized
- strategic review happened
- UX direction is sufficiently stable

If major ambiguities still exist:
- recommend returning to `shape-up-planning`
- avoid premature engineering decomposition

---

## Step 1 — Codebase Awareness Check

Before sequencing:

1. Check:
   - memory
   - prior exploration
   - architecture summaries
   - related implementation history

2. Determine whether the codebase is sufficiently understood.

3. If not:

Use the `question` tool when available.

Ask whether to:
- explore the codebase now
- proceed with assumptions
- recommend based on complexity

4. If exploration is approved:

Launch exploration focused on:
- touched systems
- APIs
- modules
- services
- data models
- coupling points
- architectural pressure zones

Feed findings into:
- risk analysis
- sequencing
- scope definition
- spike generation

5. If declined:
- proceed with explicit assumptions
- document visibility limitations

---

## Step 2 — Deep Technical Risk Analysis

When:
- exploration was performed
OR
- the proposal is technically complex

Load:
`references/CTO_RISK_ANALYSIS.md`

Generate:
- engineering risk analysis
- operational risk map
- architectural pressure analysis
- migration concerns
- scalability concerns
- rollout concerns

Use findings to:
- define spikes
- reorder sequencing
- identify enablers
- reduce execution uncertainty

---

## Step 3 — Identify Critical Spikes

Identify:
- high-risk uncertainties
- architectural unknowns
- dependency validation needs
- migration concerns
- rollout unknowns
- operational bottlenecks

If `analysis_mode = suggestive`:
- infer additional hidden spikes

Critical spikes should happen early whenever possible.

---

## Step 4 — Define Main Scopes

Group work into coherent scopes.

The first scope should typically establish:
- core domain foundations
- enabling architecture
- workflow backbone

Scopes should optimize for:
- vertical coherence
- deployment safety
- operational independence
- incremental validation

---

## Step 5 — Sequence Scopes

Apply:
- selected sequencing strategy
- risk ordering
- dependency ordering
- rollout constraints
- operational constraints

Explicitly justify:
- why the sequence exists
- what risks are being reduced
- what assumptions are being validated early

---

## Step 6 — Detail Scope Tasks

For each scope:

Generate:
- objective
- implementation rationale
- dependencies
- technical considerations
- Definition of Done
- acceptance criteria
- rollout implications

Use:
- `💡 [suggestion]`
for inferred improvements when applicable.

---

## Step 7 — Output Formatting

Follow:
`references/OUTPUT_FORMAT.md`

Use:
- `[SCOPE-X]`
- `[DOD]`
- `[SPIKE]`
- `[SEQUENCE]`
- `[RISK]`

The output should feel:
- engineering-ready
- operationally coherent
- execution-oriented

---

# Step 8 - Engineering Review Phase

After sequencing completion:

Invoke `submit_plan` tool for:
- engineering validation
- implementation review
- sequencing approval
- rollout validation
- execution readiness assessment

Purpose:
- collaborative annotation
- implementation refinement
- architecture review
- operational validation
- execution approval

This review focuses on:
- feasibility
- sequencing quality
- architectural risks
- operational readiness
- deployment realism

After approval:
- transition into build/execution mode
- use the approved sequencing plan as the execution source of truth

The approved sequencing artifact should represent:
- the executable implementation strategy
- finalized engineering sequencing
- rollout plan
- execution-ready operational scopes

___
## Step 9 — Todo Generation
After approved plan only.

If `todowrite` is available:
- create or update actionable tracked tasks
- update statuses as scopes progress
- mark completed investigations/spikes
- add newly discovered blockers or dependencies
- split tasks when hidden complexity emerges
- remove obsolete tasks after sequencing changes
- keep todos synchronized with the latest approved implementation plan

Treat todos as the operational execution state, not as a static checklist.

Organize by:
- scopes
- spikes
- rollout stages
- dependencies
- investigations

If unavailable:
- provide structured textual todos.

---

### Step 10 — Confirm next step

After approved plan only and todos created.
Based on the plan, dependencies and context, decide yourself which scopes/tasks executing in parallel or sequentially.
Use subagents for whatever option.

---

# Persistence Rules

Persist ONLY after:
- engineering review approval
- sequencing convergence
- execution readiness validation

Suggested convention:

```text
./docs/{YYYY-MM-DD}_{implementation-plan-name}.md
```

Guidelines:
- lowercase kebab-case
- concise descriptive naming
- avoid special characters

Persist:
- sequencing
- scopes
- spikes
- DoD
- acceptance criteria
- rollout ordering
- technical risks
- engineering recommendations

After persisting:
- explicitly provide the saved path
- reference it consistently in future execution discussions

---

# Output Expectations

Strong outputs:
- reduce execution uncertainty
- expose hidden technical risks
- sequence realistically
- minimize rollout fragility
- improve operational clarity
- optimize validation order

Weak outputs:
- fake certainty
- flat task lists
- missing rollout thinking
- ignoring dependencies
- no spike identification
- giant unsequenced backlogs
- architecture astronautics
- premature optimization

---

# References

- **[references/PRINCIPLES.md](./references/PRINCIPLES.md)** - The 6 sequencing principles for task ordering
- **[references/OUTPUT_FORMAT.md](./references/OUTPUT_FORMAT.md)** - Complete output template with all sections
- **[references/RISK_ANALYSIS_FRAMEWORK.md](./references/RISK_ANALYSIS_FRAMEWORK.md)** - CTO-level technical risk analysis framework (loaded conditionally in Step 1b)
