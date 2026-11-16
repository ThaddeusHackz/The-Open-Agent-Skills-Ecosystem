---
name: ixlab
description: Use when the user wants to design or redesign a page, flow, feature, component, or design system with IxLab's artifact-driven workflow, or when implementing UI from IxLab design artifacts.
---

# IxLab

IxLab is the universal entry point for the project.

Use this skill when the user wants IxLab to drive design work, design-system work, or implementation work from persisted design artifacts.

This file must be usable as a standalone entry point. If platform-specific wrappers or nested skills are unavailable, follow the workflow in this file directly.

## Canonical Source Of Truth

The canonical IxLab files live at the repository root:

- `SKILL.md`
- `AGENTS.md`
- `agents/`
- `skills/`
- `templates/`
- `references/`
- `commands/`
- `config/`

Generated platform adapters under `.claude/`, `.agents/`, and `.cursor/` should mirror these files and should not become the primary edit surface.

## Route The Task

- If the user wants to create or update `design/system.md`, read `skills/ixlab-design-system/SKILL.md`.
- If the user wants to implement UI from IxLab artifacts, read `skills/ixlab-engineer/SKILL.md`.
- For any page, flow, feature, system, or component design task, read `skills/ixlab-orchestrator/SKILL.md`.

## Default Config Fallback

If `config/ixlab.config.md` does not exist, use these defaults:

- `mode: standard`
- `web_search: false`
- `image_search: false`
- `figma_mcp: false`
- `critic_between_phases: true`
- `critic_model: sonnet`

In `full` mode, always behave as if `critic_between_phases: true`.

## Core Workflow

For design work, follow this sequence unless the user explicitly narrows scope:

1. Read `config/ixlab.config.md` when present.
2. Resolve the correct design entity.
3. Reuse existing artifacts when they already cover the same entity.
4. Run UX Researcher logic and produce `design/entities/{entity}/ux.md`.
5. Run Design Critic logic if the mode requires a gate.
6. Create or update `design/system.md` before UI work when the design system is missing or stale.
7. Run UI Designer logic and produce `design/entities/{entity}/ui.md`.
8. Run Design Critic logic again if the mode requires a gate.
9. If the user wants implementation, switch to engineer behavior and implement from the artifacts.

## Critical Behavior Rules

- Read `config/ixlab.config.md` when it exists and treat it as the default execution profile unless the user overrides it.
- Treat the unit of work as a design entity, not just a page.
- Persist artifacts inside `design/` whenever the task is about IxLab-driven design work.
- Reuse existing artifacts before creating new ones.
- In environments without native subagents, emulate the workflow sequentially by reading the canonical files under `agents/`.
- If the brief is underspecified, surface input gaps early instead of silently inventing context.
- If the brief is missing critical information, stop and ask concise follow-up questions before writing a misleading artifact.
- If you proceed with assumptions, record them explicitly inside the artifact.
- Do not skip empty, loading, error, disabled, permission, or recovery states when they are relevant.
- Do not treat optional research tools as guaranteed. They are conditional.

## Conditional Capabilities

- Use web research only when configuration enables it and the runtime actually exposes search.
- Use image reference search only when configuration enables it and the runtime actually exposes it.
- Use Figma context only when configuration enables it and the runtime actually exposes it.
- Use docs MCP or equivalent documentation context only when the runtime actually exposes it and the current task depends on framework or component-library specifics.
- If any optional capability is unavailable, continue with the base IxLab workflow instead of blocking.

## MCP and Research Rules

- Prefer trusted, primary, or high-signal sources when using web research.
- Keep external queries narrow and directly tied to the current artifact or implementation decision.
- Treat Figma context as supporting evidence, not as a substitute for IxLab artifacts.
- Treat docs MCP results as implementation guidance, not as a reason to ignore the design artifacts.
- Never make the core IxLab flow depend on optional MCP availability.

## Task-Specific Fallback

If nested skills are unavailable, apply these rules directly:

- Design task: run UX -> Critic -> UI -> Critic according to mode.
- Design-system task: create or update `design/system.md` using the design-system template.
- Implementation task: read `design/system.md`, `ux.md`, and `ui.md` before touching code, then preserve state coverage and interaction intent.

## Canonical Artifact Contract

- `design/system.md`
- `design/entities/{entity}/ux.md`
- `design/entities/{entity}/ui.md`
- `design/components/{component}.md`

## Finish Condition

IxLab work is complete only when the next consumer of the artifact or code does not need to guess the intent, missing states, or scope boundaries.
