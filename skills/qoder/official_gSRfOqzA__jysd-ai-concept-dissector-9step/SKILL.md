---
name: concept-dissector-9step
description: Deep concept learning and explanation via a strict 9-step "Concept Dissector" workflow (Overview, Definition, Deconstruct, Mechanism, Ecology, Comparison, Practice, Critique, Synthesis). Use when users ask to understand, teach, benchmark, or critically evaluate a concept and need clear boundaries ("what it is NOT"), trade-offs, practical MRE, pitfalls, and intuitive analogy.
---

# Concept Dissector (9-Step)

Use this skill to convert any abstract concept into structured, teachable knowledge. Enforce all 9 steps in order and do not skip steps.

## Input Contract

Collect or infer:
- `Concept`: target concept to dissect.
- `Context` (optional): domain, scenario, or use case (for example: K-12 English learning, distributed systems deployment).
- `Audience` (optional): learner level and background.
- `Depth` (optional): quick scan or deep dive.

If `Concept` is missing, ask for it first. If `Context` or `Audience` is missing, proceed with reasonable defaults and state assumptions briefly.

## Output Contract

Always output exactly 9 sections with `###` headings and this order:

### 1. 整体观照 (Macro Overview)
- Explain the origin problem and historical/contextual motivation in 1-2 sentences.
- State target users or target scenarios.

### 2. 本质界定 (Essence & Boundaries)
- Give a rigorous genus-differentia definition.
- Add `What it is NOT`: list 1-2 easily-confused concepts and clarify boundaries.
- Provide a short "是/非" contrast.

### 3. 结构拆解 (Structural Anatomy)
- Decompose into core components/modules/syntax units.
- Show hierarchy or dependency (list or Markdown tree).

### 4. 原理探微 (Underlying Mechanism)
- Explain why it works through causal chain.
- For technical topics: explain data flow/algorithm logic.
- For language/humanities: explain pragmatic or cognitive assumptions.

### 5. 生态位评估 (Ecological Niche)
- Place the concept in the larger knowledge stack.
- Identify upstream prerequisites and downstream unlocked capabilities.
- Mention typical integration path with existing systems/workflows.

### 6. 横向比较 (Horizontal Benchmarking)
- Compare with 1-2 alternatives in a Markdown table.
- Required dimensions: strengths, weaknesses, trade-offs, suitable scenarios.
- Make the "killer advantage" and "cost paid" explicit.

### 7. 实践操刀 (Minimal Practice)
- Provide one MRE (minimal reproducible example) that can be executed or practiced quickly.
- Add a `Friction Point` subsection with common beginner pitfalls and how to avoid them.
- If user gives a specific scenario, tailor this section to that scenario first.

### 8. 批判评估 (Critical Critique)
- List limitations, failure boundaries, and maturity risks.
- Explain where this concept is unsuitable or harmful if misused.

### 9. 合成内化 (Intuitive Synthesis)
- Re-express the full concept using one powerful everyday analogy.
- Ensure a cross-domain learner can get an "Aha" moment.
- If user gives a specific audience, tailor analogy to that audience.

## Language and Style Rules

- Use concise, rigorous, professional language.
- Include key terms as `English (中文)` pairs where relevant.
- Avoid vague claims and generic praise.
- Prefer evidence, mechanism, and operational detail.
- Keep each section focused; no section should be empty.

## Quality Checklist (Before Responding)

Verify all items:
- All 9 sections exist with `###` headings and correct order.
- Step 2 includes explicit `What it is NOT`.
- Step 6 is a Markdown comparison table.
- Step 7 includes both MRE and `Friction Point`.
- Step 8 contains failure boundaries.
- Step 9 includes one concrete analogy.
- If scenario/audience was provided, Step 7 and Step 9 are adapted.

## Default Response Skeleton

Use this structure directly:

```markdown
### 1. 整体观照 (Macro Overview)
[痛点与背景]

### 2. 本质界定 (Essence & Boundaries)
- 核心定义:
- What it is NOT:
- 是/非对照:

### 3. 结构拆解 (Structural Anatomy)
[组件、层级、依赖]

### 4. 原理探微 (Underlying Mechanism)
[因果链/运行机制]

### 5. 生态位评估 (Ecological Niche)
[上下游与系统占位]

### 6. 横向比较 (Horizontal Benchmarking)
| 维度 | 当前概念 | 对照概念A | 对照概念B |
| --- | --- | --- | --- |
| 优势 |  |  |  |
| 局限 |  |  |  |
| 代价/Trade-off |  |  |  |
| 适用场景 |  |  |  |

### 7. 实践操刀 (Minimal Practice)
- MRE:
- Friction Point:

### 8. 批判评估 (Critical Critique)
[失效边界与风险]

### 9. 合成内化 (Intuitive Synthesis)
[高洞察隐喻]
```
