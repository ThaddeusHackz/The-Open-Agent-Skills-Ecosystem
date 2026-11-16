---
name: metric-definition-helper
description: Draft reviewable metric contracts before SQL, dashboards, or reporting. Use when defining a KPI, resolving competing business definitions, documenting grain and exclusions, clarifying time logic, or preparing a metric for stakeholder signoff and downstream implementation.
---

# Metric Definition Helper

Prefer a clear metric contract over clever implementation details.

## Work in this order

1. Restate the business purpose of the metric.
2. Identify the owner, audience, and decision supported.
3. Define grain, formula, numerator, denominator, and time logic.
4. Document inclusions, exclusions, and edge cases.
5. Surface unresolved choices explicitly.
6. End with a validation plan and signoff questions.

## Default output shape

Return sections in this order:

### 1) Metric purpose
- business question answered
- primary audience
- decision supported
- business owner

### 2) Metric contract
- metric name
- unit of measure
- grain
- formula in plain language
- numerator
- denominator if applicable
- time window and attribution logic

### 3) Scope rules
- inclusions
- exclusions
- edge cases
- segmentation dimensions that matter

### 4) Example records
Give compact examples of what counts and what does not count.

### 5) Open decisions
Call out disputes or choices such as:
- active status definition
- timezone boundary
- late-arriving data treatment
- bot / test / internal traffic exclusion

### 6) Validation plan
Include checks such as:
- compare with prior definition
- sample record walkthroughs
- time-series sanity check
- reconciliation to trusted source

## Guardrails

- Do not hide ambiguity.
- Do not let convenient SQL stand in for business truth.
- Do not treat a metric as final without owner review.
- If ownership is missing, flag it as a governance gap.

## Prompt scaffold

```text
Metric name:
Business purpose:
Current definition (if any):
Competing definitions or disputes:
Primary owner / stakeholder:
Important dimensions:
Known exclusions:
Time logic / timezone:
```

## Review standard

Mark output as ready only when it includes:
- metric purpose
- contract
- exclusions / edge cases
- open decisions
- validation plan
