---
name: ux-design-guide
description: "UX/Product design process reference with Pencil MCP integration. Covers Develop→Validate stages where Claude can execute directly. Earlier stages (Discover/Define) handled as input gates. Use when designing screens, apps, or websites, reviewing design deliverables, or needing guidance on design methodology. Triggers on design process, UX flow, wireframe, mockup, design review, information architecture, user journey, design deliverables, design phase."
version: "2.0.0"
scope: public
---

# UX Design Guide

Product design process reference — focused on stages Claude can execute, with input gates for human-led stages.

## Process Model

```
[HUMAN-LED]                          [CLAUDE-EXECUTABLE]
DISCOVER ──► DEFINE ──►              DEVELOP ──► DESIGN ──► DELIVER ──► VALIDATE
 (research)   (problem)               (ideate)    (build)    (handoff)   (measure)
╰── Input Gates (verify done) ──╯    ╰── Full execution with Pencil + code ────────╯
```

**Key principle**: Claude doesn't run user interviews or stakeholder meetings. It verifies those happened, then executes Develop→Validate.

---

## Input Gates (Discover & Define)

Before starting design work, verify these inputs exist. If missing, ask the user to provide them — don't fabricate.

### Gate 1: Research Inputs (from Discover)

Check that the user has:
- [ ] User pain points (3+ backed by evidence: quotes, data, observation)
- [ ] Target audience description or persona
- [ ] Competitive context (who else solves this problem)

**If missing**: "I need research inputs before designing. Can you share user pain points, target audience, or competitive context? Even a few bullet points is enough."

**What Claude CAN do here**: Help organize raw research notes into structured formats (persona template, empathy map, competitive matrix). See `references/methodology.md` Stage 1-2 templates.

### Gate 2: Problem Definition (from Define)

Check that the user has:
- [ ] Problem statement: "[User] needs [capability] because [insight]"
- [ ] Success metrics (at least 1 measurable outcome)
- [ ] Scope decision (MVP vs. feature iteration vs. redesign)

**If missing**: "What problem are we solving, and how will we know it worked? A one-sentence problem statement + one metric is enough to start."

**Pass both gates → proceed to Develop.**

---

## Stage 1: Develop (Ideate)

Diverge: explore multiple solution directions before committing.

| Method | Claude's role | Output |
|--------|--------------|--------|
| Solution brainstorming | Generate 3+ distinct approaches | Ideas list with tradeoffs |
| Mood board | Suggest visual directions based on context | Style references |
| IA / Sitemap | Structure the product's navigation | Sitemap tree |
| Concept sketches | Describe layout approaches in detail | Written wireframe descriptions |

### Claude workflow

1. Review inputs from gates
2. Generate 3+ solution directions (not just one)
3. For each: describe approach, tradeoffs, and which users it serves best
4. User picks direction → proceed to Design

### Exit criteria
- 2+ distinct directions explored
- User has selected which to pursue
- IA/sitemap drafted for chosen direction

---

## Stage 2: Design (Execute)

Converge: build the solution step by step.

### Production sequence
```
IA (Sitemap) → Flow Chart → UI Flow → Wireframe → Mockup → Prototype → Motion → Design System
```

| Step | What | Fidelity | Claude tool |
|------|------|----------|-------------|
| Information Architecture | Sitemap / functional map | Structure | Text / Mermaid |
| Flow Chart | Logic flow with decisions (no UI) | Text + arrows | Mermaid / text |
| UI Flow | Flow + page outlines showing navigation | Low | Pencil |
| Wireframe | B&W layout, element placement | Low | Pencil |
| Mockup (UI Design) | Full visual: color, typography, spacing | High | Pencil |
| Prototype | Interactive click-through | High | Pencil |
| Motion Design | Transitions, micro-interactions | High | Pencil + code |
| Design System | Tokens, components, usage rules | Spec | Pencil + code |

### Pencil MCP workflow (primary tool for this stage)

```
get_editor_state()                  # Check current canvas
get_guidelines("design-system")     # Learn composition rules (or "landing-page" for marketing)
get_style_guide_tags                # Browse available styles
get_style_guide(tags: [...])        # Get visual direction
batch_get(patterns: [{reusable}])   # Discover existing components
batch_design(operations)            # Build screens (max 25 ops/call)
get_screenshot(nodeId)              # Verify result visually
snapshot_layout(problemsOnly: true) # Check for layout issues
```

**Landing pages**: Use `get_guidelines("landing-page")` instead of `"design-system"`.

### Design checklist
- [ ] All states covered: default, hover, active, disabled, error, loading, empty
- [ ] Responsive breakpoints: mobile (375px), tablet (768px), desktop (1440px)
- [ ] Real content (no lorem ipsum in final mockups)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Touch targets >= 44px on mobile
- [ ] Consistent spacing (8px grid)

### Exit criteria
- All screens and states covered
- Prototype passes internal walkthrough without confusion
- Visual QA via `get_screenshot` shows no layout issues

---

## Stage 3: Deliver (Handoff)

Prepare complete specs for engineering.

### Handoff process (in order)

1. **Walk through** — Describe all screens and flows. Surface edge cases early.
2. **Annotate** — Add specs for anything non-obvious (spacing, states, transitions).
3. **Export assets** — Use `export_nodes` for icons/images to agreed naming convention.
4. **Confirm buildability** — Engineering confirms they can build without further questions. This is the exit criterion.
5. **Stay available** — Expect 2-3 rounds of clarification during build.

### Pencil tools for Deliver

| Task | Tool |
|------|------|
| Final visual QA | `get_screenshot` |
| Export assets | `export_nodes(format: "png"/"svg")` |
| Check layout specs | `snapshot_layout` |
| Extract variables | `get_variables` |

### Handoff artifacts

| Artifact | Content |
|----------|---------|
| Annotated specs | Spacing, font sizes, color values |
| Asset export | Icons, images, cut assets |
| Interaction spec | States, edge cases, error handling |
| Motion annotation | Duration, easing curves, triggers |
| Design Tokens | Variables for design system integration |

### Exit criteria
- Engineering confirms specs are buildable without follow-up questions

---

## Stage 4: Validate (Measure)

Verify design effectiveness post-launch.

| Method | Claude's role | Output |
|--------|--------------|--------|
| Usability testing | Design test plan, analyze results | Test report |
| A/B testing | Define variants, analyze winner | Comparison report |
| Analytics review | Interpret metrics vs. success criteria from Gate 2 | Data analysis |
| Heuristic review | Audit against UX principles | Issue list with severity |

### Exit criteria
- Key success metrics measured against baseline (from Gate 2)
- Iteration backlog prioritized

### Post-Validate iteration
Iteration backlog feeds a scoped mini-cycle — usually re-entering at Develop or Design, not a full restart. Use the loop-back table below.

---

## Iteration & Loop-back

Double Diamond is non-linear. Loop back when:

| Trigger | Go back to |
|---------|-----------|
| Validation reveals users can't complete core task | Design (revisit flows/layout) |
| Usability test reveals misunderstood user goal | Input Gates (reframe problem) |
| Engineering flags a constraint that breaks the design | Design → Deliver (renegotiate scope) |
| New competitive product changes landscape | Develop (re-explore alternatives) |
| Key metrics fall below baseline post-launch | Design or Input Gates (depends on root cause) |
| A/B test fails without clear reason | Run targeted research → Develop |

**Rule**: Loop back one stage at a time. If you skip two stages back, something was missed — acknowledge it.

---

## Quick Start Guide

### Where to start

| Your situation | Start here |
|----------------|-----------|
| New product, blank slate | Input Gates → Develop |
| Know the problem, exploring solutions | Develop |
| Solution decided, need to build it | Design |
| Design done, prepping for engineering | Deliver |
| Already shipped, measuring results | Validate |
| Live product with post-launch issues | Validate → loop-back table |
| Mid-project pivot (stakeholder redesign) | Input Gates (re-validate problem) |
| Severely time-boxed (< 1 day) | Design (minimum viable artifact) |

### Depth by project type

| Project type | Stages | Safe to skip |
|--------------|--------|-------------|
| MVP / 0-to-1 | All, lightweight | None — but keep each stage short |
| Feature iteration | Develop → Deliver | Input Gates: if recent research (< 3 months) exists |
| Small UI change | Design → Deliver | Everything upstream: scope is purely visual |
| Redesign | All, full depth | Nothing — a redesign that skips research is just a reskin |

**Skip rule**: A stage is safe to skip only if its output already exists and is current (< 3 months old).

### Solo vs. team

| Context | Adjustments |
|---------|------------|
| **Solo** | Skip workshops. Replace with: solo sketching + async feedback. Shorten research to desk research + 3-5 interviews. |
| **Small team (2-3)** | Async workshops (Miro/FigJam). Assign stage ownership. Weekly sync at stage gates. |
| **Large team (4+)** | Formal stage gate sign-off. Shared component library from Design onward. Dedicated handoff owner. |

**Regardless of size**: exit criteria still apply. A solo designer meets them without the meeting.

---

## Common Pitfalls

- Skipping Define: jumping to solutions without understanding the problem
- Wireframe fidelity creep: wireframes should be ugly and fast
- No validation: shipping without measuring
- Design System too early: build components after 3+ screens share patterns
- Fabricating research: if you don't have user data, say so — don't invent personas

---

## References

For detailed methodology per stage (interview guides, templates, frameworks), see `references/methodology.md`.
