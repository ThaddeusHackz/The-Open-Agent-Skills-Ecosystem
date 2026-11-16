---
name: generate-structured-content-as-an-llm
description: Generate structured content via an AI agent/LLM that follows predefined formatting, tone, and schema rules. Activate when producing podcast scripts, show notes, PRDs, coding plans, landing pages, structured summaries, or any content requiring deterministic output structure.
---

# Generate Structured Content

Structured content must follow defined formatting rules.

It is not freeform writing.
It must match a required schema.
It must preserve structural integrity.

This skill enforces output discipline.

---

## Documentation

Refer to:

- `06a-content-generation-standards.md`
- `06-agents-standards.md`
- Any relevant template or format document

Use `search-docs` to retrieve the required format before generating content.

---

## Usage

Activate when:

- A fixed template must be followed
- Output must contain required sections
- Tone must be controlled
- Word count must be constrained
- Content must be reusable or machine-parsable

---

## Required Inputs

- Content type (e.g., show notes, PRD, script)
- Required sections
- Tone requirements
- Audience
- Word count constraints
- Source material (if provided)

---

## Implementation Workflow

	•	Identify required structure
	•	Extract key information from source
	•	Map information to required sections
	•	Apply tone constraints
	•	Enforce structural consistency
	•	Validate required sections exist
	•	Ensure no hallucinated facts

---

## Structural Integrity Rules

- All required sections must exist
- Section order must match template
- Headings must match exactly if specified
- No extra sections unless requested
- No missing required fields

---

## Tone Enforcement

- Follow specified voice constraints
- Avoid deviation into generic phrasing
- Avoid unnecessary embellishment
- Maintain clarity and conciseness

---

## Hallucination Control

- Use only provided source material
- Do not invent data
- Do not fabricate references
- Clearly omit unknown details if absent

---

## Example Invocation

> Generate Tuesday podcast show notes using the fixed format:
> - Welcome intro
> - 3 news stories with links
> - Hot Take
> - Workplace Surgery
> - Subscribe CTA
> - Mental wellbeing links
> - Contact links

OR

> Generate a PRD following the Oblong PRD template with strict section headings.

---

## Validation Checklist

Before returning output:

- [ ] Required sections present
- [ ] Structure correct
- [ ] Tone consistent
- [ ] No invented facts
- [ ] Word count respected
- [ ] Formatting clean

---

## Design Principles

- Deterministic structure
- Schema adherence
- Reusable output
- Predictable formatting
- Context-aware but disciplined
