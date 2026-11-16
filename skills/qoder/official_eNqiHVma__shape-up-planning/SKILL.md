---
name: shape-up-planning
description: >
  Strategic shaping and scope definition for products, systems, workflows,
  services, organizational initiatives, and complex solution proposals.

  Activate automatically when:
  - brainstorming must become actionable
  - scope or delivery boundaries are unclear
  - risks and assumptions need shaping
  - implementation direction feels ambiguous
  - product/service/system direction needs strategic framing
  - sequencing or UX exploration depends on clearer shaping
---

# Shape Up Planning

A strategic shaping skill inspired by Shape Up principles.

This skill transforms raw ideas into:
- scoped proposals
- strategic framing
- implementation-aware shaping
- risk maps
- operational boundaries
- sequencing foundations

The goal is NOT detailed specification writing.

The goal is:
- shaping
- reducing ambiguity
- exposing trade-offs
- clarifying scope
- identifying risks early
- preparing coherent downstream execution

---

# Cross-Domain Adaptability

This skill applies beyond digital products.

It can shape:
- workflows
- services
- operational systems
- AI agents
- organizational processes
- education/training systems
- behavioral systems
- habits and routines
- relationship/process agreements
- physical experiences

Adaptation guidance:
`./references/cross-domain-adaptation.md`

---

# Context Reconstruction

Before asking questions:

1. Infer as much context as possible from:
   - current request
   - session history
   - prior brainstorming
   - referenced plans/specs
   - implied workflows
   - business/operational signals

2. Reconstruct internally:
   - likely goals
   - stakeholders
   - tensions
   - workflows
   - assumptions
   - constraints
   - likely job-to-be-done

Avoid asking users to restate existing context.

---

# Progressive Clarification Principle

Prefer:
- explicit assumptions
- provisional shaping
- iterative refinement

over blocking for complete information.

Only ask follow-up questions when missing information would materially affect:
- scope
- operational viability
- sequencing
- feasibility
- workflow architecture
- risk assessment

Detailed rules:
`./references/clarification-rules.md`

---

# Strategic Alternatives Rule

Generate strategic alternatives when useful.

Focus on:
- workflow strategy
- operational ownership
- rollout philosophy
- automation boundaries
- integration approach
- responsibility distribution
- scope shape

Do NOT generate detailed UI proposals here.

If interaction/workflow complexity becomes important:
- recommend the `interface-brainstorming` skill
- reconcile the selected direction back into shaping

Detailed escalation rules:
`./references/risk-analysis-framework.md`

---

# Evolutionary Exploration (Optional)

When the proposal would benefit from:
- broader possibility exploration
- discovery of non-obvious paths
- stepping-stone thinking
- ecosystem thinking
- evolutionary experimentation
- future opportunity generation

recommend invoking:
`evolution-strategy`

Use especially when:
- the problem space is highly uncertain
- innovation paths are unclear
- the proposal risks converging too early
- multiple future trajectories may exist

Do not invoke automatically for straightforward implementation shaping.

---

# Core Principles

All shaping should prioritize:
- KISS
- DRY
- progressive disclosure
- convention over configuration
- delivery realism
- asymmetric risk reduction
- focused scope
- sustainable complexity

Avoid:
- speculative over-engineering
- vague MVPs
- uncontrolled extensibility
- “platform thinking” too early
- feature soup

Detailed principles:
`./references/shaping-principles.md`

---

# Main Responsibilities

The skill should:
1. Clarify the problem
2. Reveal assumptions
3. Expose risks
4. Define scope boundaries
5. Identify linchpins
6. Shape coherent solution direction
7. Prevent scope explosion
8. Prepare downstream UX and implementation work

---

# Required Output Structure

Generate:

1. 🤔 unanswered questions and unexplored issues
2. 🧭 strategic shaping alternatives
3. 📝 structured shape up proposal
4. 📋 tracking and sequencing guidance

Detailed structure rules:
`./references/proposal-structure.md`

Risk analysis framework:
`./references/risk-analysis-framework.md`

---

# Tool Usage Rules

## Question Tool

Before final consolidation or strategic review:

- identify meaningful ambiguities
- resolve critical gaps
- ask only materially impactful questions

Whenever the `question` tool is available:
- always use it instead of raw chat questions

Every strategic question should include:
- explicit options
- one AI-recommended option

If unavailable:
- ask in chat using the same structure.

Detailed rules:
`./references/clarification-rules.md`

---

## Todo Tracking

If `todowrite` is available:
- always use it for actionable tracking
- continuously update todo status as shaping progresses
- mark completed decisions/questions explicitly
- add newly discovered risks, dependencies, and follow-ups
- remove obsolete todos when scope changes
- keep the todo list aligned with the latest shaped proposal state

Treat the todo list as a living operational memory for the shaping process.

Organize todos by:
- shaping
- risks
- UX decisions
- sequencing
- technical investigations

If unavailable:
- provide structured textual todos.

---

# Sequencing Integration

If the `tech-planning-sequencing` skill is available:

Recommend invoking it AFTER:
- shaping convergence
- strategic review approval
- interface convergence (if applicable)

Purpose:
- implementation sequencing
- dependency mapping
- vertical slicing
- risk-first ordering
- rollout sequencing
- engineering decomposition

The technical planning phase should transform the shaped proposal into:
- an executable implementation strategy
- engineering-ready scopes
- operational sequencing

Do not treat shaping itself as the executable implementation plan.

Detailed sequencing rules:
`./references/sequencing-and-persistence.md`

---

# Strategic Review Phase

Before technical planning:

Invoke `submit_plan` tool for:
- strategic review
- product validation
- UX/workflow validation
- scope refinement
- stakeholder annotations

Input:
- complete shape up spec created

Purpose:
- validate the shaped direction
- resolve workflow concerns
- refine rules and constraints
- confirm strategic coherence

This review should happen BEFORE:
- deep technical sequencing
- engineering decomposition
- execution planning

The reviewed shaping proposal becomes the strategic input for:
`tech-planning-sequencing`

After approval:
- remain in planning/plan mode
- continue into technical sequencing and implementation planning
- avoid transitioning into build/execution mode yet

---

# Persistence Rules

Persist ONLY after:
- user approval
- strategic review completion
- major ambiguity resolution

Suggested convention:

```text
./docs/{YYYY-MM-DD}_{spec-name}.md
```

Detailed persistence rules:
`./references/sequencing-and-persistence.md`

---

# Output Expectations

Strong outputs:
- reduce ambiguity
- expose trade-offs
- narrow scope intelligently
- create implementation clarity
- integrate UX implications
- preserve strategic coherence

Weak outputs:
- vague MVPs
- generic feature lists
- fake certainty
- UI-first thinking too early
- broad unbounded scope
- premature platform abstractions

# References

- `./references/cross-domain-adaptation.md`
- `./references/clarification-rules.md`
- `./references/risk-analysis-framework.md`
- `./references/shaping-principles.md`
- `./references/proposal-structure.md`
- `./references/sequencing-and-persistence.md`
