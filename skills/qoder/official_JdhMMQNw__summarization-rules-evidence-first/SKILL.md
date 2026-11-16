---
id: 65-context-token-optimization-summarization-rules-evidence-first
name: Summarization Rules (Evidence First)
description: Evidence-first summarization rules - start with evidence/data before conclusions, reducing tokens and increasing credibility
version: 1.0.0
status: Active
owner: AI Engineering Team
last_updated: 2025-02-15
category: AI-RAG
tags: [summarization, evidence-first, token-optimization, credibility]
stack: [Not Applicable]
difficulty: Beginner
---

# Summarization Rules (Evidence First)

## Skill Profile

- [ ] DevOps
- [ ] Backend
- [ ] Frontend
- [x] AI-RAG
- [ ] Security Critical

## Overview

Summarization rules that prioritize evidence over conclusions - show important data first, then summarize. This reduces token usage and increases credibility.

## Why This Matters

- **Credibility**: Evidence first = more credible
- **Efficiency**: Cut long explanations
- **Actionable**: See data clearly
- **Verifiable**: Can be checked

## Core Concepts & Rules

### 1. Traditional vs Evidence-First

#### ❌ Traditional (Conclusion First)

```
"The system is experiencing performance issues due to several factors
including high database load, inefficient queries, and memory leaks.
Based on our analysis, we recommend the following improvements..."

(150 tokens, vague)
```

#### ✅ Evidence-First

```
Performance Issues:
- DB CPU: 95% (normal: <70%)
- Slow queries: 15 (>1s each)
- Memory: 8GB → 12GB in 2 hours

Fix: Add indexes, optimize queries, fix leak in auth.ts:45

(40 tokens, specific)
```

**Savings: 73%**

### 2. Core Rules

#### Rule 1: Data Before Interpretation

```
❌ "The API is slow"
✅ "API response time: 2.5s (SLA: <500ms)"

❌ "Many users affected"
✅ "1,247 users (12% of active users)"

❌ "Database is overloaded"
✅ "DB connections: 95/100, CPU: 87%"
```

#### Rule 2: Numbers Over Adjectives

```
❌ "Very slow"
✅ "2.5s (5x slower than baseline)"

❌ "High error rate"
✅ "Error rate: 5.2% (normal: 0.1%)"

❌ "Significant improvement"
✅ "Response time: 2s → 500ms (75% faster)"
```

#### Rule 3: Specific Over General

```
❌ "Several files changed"
✅ "3 files: auth.ts, db.ts, config.ts"

❌ "Recent issues"
✅ "Issues in last 24h: 12 (P0: 2, P1: 10)"

❌ "Multiple errors"
✅ "Errors: 'Invalid token' (80%), 'Timeout' (20%)"
```

## Inputs / Outputs / Contracts

### Inputs

- Data and evidence
- Metrics and measurements
- Error messages and logs
- Code snippets
- Task requirements

### Outputs

- Evidence-first summaries
- Specific metrics
- Actionable recommendations
- Token-efficient reports
- Verifiable information

### Contracts

- **Input Validation**: All inputs must be valid data/evidence
- **Output Format**: Summaries follow evidence-first standards
- **Token Budget**: Summaries respect configured token limits
- **Evidence Guarantee**: All summaries start with evidence/data
- **Verifiability**: All claims are measurable and verifiable

## Skill Composition
* **Depends on**: [anti-bloat-checklist](../anti-bloat-checklist/SKILL.md), [prompt-library-minimal](../prompt-library-minimal/SKILL.md)
* **Compatible with**: [retrieval-playbook-for-ai](../retrieval-playbook-for-ai/SKILL.md), [context-pack-format](../context-pack-format/SKILL.md)
* **Conflicts with**: None
* **Related Skills**: [skill-generator](../../00-meta-skills/skill-generator/SKILL.md), [prompting-patterns](../../61-ai-production/prompting-patterns/SKILL.md)

## Quick Start

### Quick Reference Table

| Task | Minimal Prompt | Tokens |
|------|---------------|--------|
| Bug report | `Fix: [error]` | 2 |
| Performance issue | `Metric: [value]` | 3 |
| Code review | `Review for bugs, performance:` | 4 |
| Generate | `Function: [description]` | 2 |
| Refactor | `Refactor for [goal]:` | 3 |
| Test | `Tests ([cases]):` | 2 |
| Document | `Document:` | 1 |
| Optimize | `Optimize for [metric]:` | 3 |
| Debug | `Error: [message]. Fix?` | 3 |

## Assumptions

- Evidence is available and accurate
- Metrics are measurable
- Conclusions follow from evidence
- Token cost is a consideration
- Credibility is important

## Compatibility

- **AI Models**: GPT-4, Claude, etc.
- **Data Types**: Metrics, logs, code, errors
- **Output Formats**: Text, tables, lists
- **Domains**: All domains applicable

## Test Scenario Matrix

| Scenario | Input | Expected Output | Verification |
|----------|-------|-----------------|--------------|
| Bug report | Error message | Evidence-first summary | Token count reduced |
| Performance issue | Metrics | Data-driven summary | Token count reduced |
| Code review | Code diff | Specific issues | Token count reduced |
| Status update | Progress data | Evidence-based update | Token count reduced |

## Technical Guardrails

### Summary Requirements

- All summaries MUST start with evidence
- All summaries MUST use specific numbers
- All summaries MUST avoid adjectives
- All summaries MUST be specific over general

### Evidence Requirements

- All evidence MUST be measurable
- All evidence MUST be verifiable
- All evidence MUST be accurate
- All evidence MUST be relevant

### Quality Requirements

- All summaries MUST be actionable
- All summaries MUST be clear
- All summaries MUST be concise
- All summaries MUST be credible

## Security Threat Model

### Threats Addressed

- **Misleading summaries**: Evidence-first approach
- **Vague conclusions**: Specific data
- **Unverified claims**: Verifiable evidence
- **Token waste**: Efficient summaries

### Mitigation Strategies

- Always start with evidence
- Use specific metrics
- Avoid vague language
- Make claims verifiable
- Keep summaries concise

## Domain-Specific Modules

### Evidence Gatherer Module

```typescript
export interface Evidence {
  metric: string;
  value: number | string;
  baseline?: number;
  unit?: string;
}

export class EvidenceGatherer {
  gather(metrics: string[], data: Record<string, any>): Evidence[] {
    return metrics.map(metric => ({
      metric,
      value: data[metric],
      baseline: this.getBaseline(metric),
      unit: this.getUnit(metric),
    }));
  }

  private getBaseline(metric: string): number {
    // Get baseline for metric
    return 0;
  }

  private getUnit(metric: string): string {
    // Get unit for metric
    return '';
  }
}
```

### Summary Generator Module

```typescript
export function generateEvidenceSummary(
  evidence: Evidence[],
  conclusion: string
): string {
  const evidenceSection = evidence.map(e =>
    `- ${e.metric}: ${e.value}${e.baseline ? ` (baseline: ${e.baseline})` : ''}${e.unit ? ` ${e.unit}` : ''}`
  ).join('\n');

  const conclusionSection = conclusion ? `\n\nConclusion: ${conclusion}` : '';

  return evidenceSection + conclusionSection;
}
```

### Token Analyzer Module

```typescript
export function countTokens(text: string): number {
  // Approximate token count (4 chars per token)
  return Math.ceil(text.length / 4);
}

export function calculateSavings(before: number, after: number): number {
  return ((before - after) / before) * 100;
}
```

## Release, Rollback & Ops Notes

### Release Process

1. Define evidence-first rules
2. Create summary templates
3. Implement evidence gathering
4. Test with sample data
5. Deploy to production
6. Monitor token usage
7. Adjust rules as needed

### Rollback Procedure

1. Revert summary format changes
2. Restore previous format
3. Monitor quality impact
4. Roll back if necessary

### Operational Procedures

- **Summary monitoring**: Track token usage
- **Quality checks**: Verify credibility
- **Template updates**: Improve based on feedback
- **Evidence validation**: Ensure accuracy

## Code Quality & Documentation

### Summary Standards

- Start with evidence/data
- Use specific numbers
- Avoid adjectives and vague language
- Be specific over general
- Make conclusions actionable

### Documentation Requirements

- Document all summary rules
- Provide examples for each rule
- Include templates for common tasks
- Track token savings
- Document best practices

## Agent Directives & Error Recovery

### Agent Behavior Rules

1. **Always** start with evidence
2. **Always** use specific numbers
3. **Always** avoid adjectives
4. **Always** be specific over general
5. **Always** make conclusions actionable

### Error Recovery Patterns

| Error Type | Detection | Recovery |
|------------|-----------|----------|
| Vague summary | Poor AI response | Add specific data |
| Too verbose | High token count | Apply evidence-first rules |
| Missing evidence | Incomplete summary | Add measurable data |
| Quality issue | Poor credibility | Add verifiable claims |

## Agent Prompt Pack

### Evidence-First Prompts

```
"Create an evidence-first summary for {task} that:
- Starts with specific data/metrics
- Uses numbers over adjectives
- Is specific over general
- Makes conclusions actionable
- Is concise and token-efficient"
```

### Summary Generation Prompts

```
"Generate a summary that:
- Shows evidence first
- Includes specific metrics
- Avoids vague language
- Provides actionable conclusions
- Uses tables for comparisons"
```

### Evidence Gathering Prompts

```
"Gather evidence for {task} that:
- Collects specific metrics
- Measures before/after values
- Identifies root causes
- Provides verifiable data
- Tracks token savings"
```

## Definition of Done

Evidence-first summary is complete when:

- [ ] Summary starts with evidence
- [ ] All metrics are specific
- [ ] All adjectives are removed
- [ ] Conclusions are actionable
- [ ] Evidence is verifiable
- [ ] Token count is optimized
- [ ] Quality is maintained
- [ ] Format is consistent
- [ ] Best practices followed

## Anti-patterns

1. **Burying the lede**: Starting with conclusions
2. **Vague quantifiers**: "Many users", "Several issues"
3. **Opinion without evidence**: "The code is poorly written"
4. **No specific metrics**: "Performance is slow"
5. **Long explanations**: Verbose descriptions
6. **Adjectives over numbers**: "Very slow", "High error rate"
7. **General statements**: "Things are moving in right direction"
8. **Unverifiable claims**: Statements without evidence

## Reference Links

- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Evidence-Based Writing](https://writing.colostate.edu/evidence-based)

## Versioning & Changelog

### v1.0.0 (2025-02-15)
- Initial release of Summarization Rules (Evidence First) skill
- Traditional vs Evidence-First comparison
- Core rules (3 rules)
- Templates (Bug Report, Performance Issue, Code Review)
- Examples (Incident Report, Status Update)
- Formatting rules (tables, lists, code blocks)
- Constraints (length, format, style)
- Best practices (5 sections)
- Quick reference
- Measurement and tracking
- Anti-patterns (4 patterns)
- Quick checklist
- Summary
