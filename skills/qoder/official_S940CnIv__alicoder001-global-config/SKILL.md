---
name: global-config
description: Generic cross-skill defaults and interaction rules for Alicoder001 skills. Use when you need neutral communication defaults, project assumptions, and skill priority outside the Codex-specific startup self-heal flow. For Codex AGENTS.md or .agents/CONTEXT.md repair, use codex-precision.
---

# Global Configuration

> Secondary helper for neutral defaults across skills.

## Interaction Defaults

- Mirror the user's tone and technical depth.
- Ask up to 2 clarifying questions when requirements are ambiguous.
- Confirm constraints that affect output (stack, environment, timeline).
- Default conversation to the user's language.
- Keep reusable skill artifacts (`SKILL.md`, scripts, references) in English unless explicitly requested otherwise.

## Project Context Detection

**NEVER ask these questions:**
- "What programming language?"
- "What is your tech stack?"
- "Do you want guided setup?"
- "What framework are you using?"

**Instead, auto-detect from these files:**

| File | What to Detect |
|------|----------------|
| `package.json` | Dependencies, scripts, framework |
| `tsconfig.json` | TypeScript project |
| `.agents/CONTEXT.md` | Full project context |
| `GEMINI.md` | Agent rules |
| `next.config.*` | Next.js project |
| `vite.config.*` | Vite project |
| `nest-cli.json` | NestJS project |

**Detection logic:**
1. Check if context files exist and use them silently.
2. Check `package.json` dependencies and infer stack.
3. If no context found, proceed with reasonable defaults for immediate task execution.
4. If Codex-specific startup repair is needed, route to `codex-precision`.
5. If context is missing and the task clearly needs explicit project-level setup, trigger `project-init` recovery flow with one short confirmation.

**Routing boundary (important):**
- `global-config` sets defaults and routing only.
- `codex-precision` owns AGENTS.md, `.agents/CONTEXT.md`, self-heal rules, and Codex guardrail repair.
- `project-init` handles explicit setup and full recovery requests.
- If setup/context recovery intent is detected, delegate instead of running setup questions here.

> **Rule**: If you cannot detect, proceed with the task. Do not block.

## Language Policy

- Do not ask a generic language preference question in normal task flow.
- Exception: setup-style onboarding (for example `project-init`) must ask one language confirmation at the start when the first user message is non-English.
- For Uzbek first messages in setup/recovery, use: `O'zbekcha davom etamizmi?`
- After language is confirmed once, do not repeat the language question in the same setup flow.

## Global Rules

### Code Style
- Prefer TypeScript with strict mode when TypeScript is used.
- Follow naming conventions from `typescript`.
- Apply mobile-first responsive design for UI work.

### Communication
- Be concise and professional.
- Use code examples for non-trivial explanations.
- Format responses in markdown.

### Local Skill Capture
- Support both explicit save triggers: `@save-skill` and `skillga saqla`.
- Treat these triggers as a request to persist project-specific guidance as a local skill.
- Ask one short confirmation before writing: `Save this as a local skill? (yes/no)`.
- Save using the standard local path: `.agents/skills/local/<skill-name>/SKILL.md`.
- If a matching local skill already exists, update/merge it instead of creating duplicates.

### Error Handling
- Wrap async code in try-catch where failures are expected.
- Provide helpful error messages.
- Log errors appropriately.

### Security
- Never expose secrets or API keys.
- Validate all user inputs.
- Use environment variables.

---

## Skill Priority Order

When multiple skills apply, follow this order:

1. **codex-precision** - First for Codex startup audit, context repair, and execution guardrails
2. **project-init** - Explicit setup/context regeneration
3. **global-config** - Generic defaults and routing guardrails
4. **agent/reasoning** - Before any complex task
5. **agent/planning** - For task decomposition
6. **core/** skills - Foundation
7. **arch/** skills - Architecture decisions
8. **frontend/** or **backend/** - Implementation
9. **perf/** - Optimization
10. **agent/** - Other agent behaviors

---

## Session Memory

Remember these across the conversation:
- Project type and stack (Next.js, NestJS, etc.).
- Constraints and priorities (performance, accessibility, SEO).
- Key files and structure discussed.

---

## Quick Reference

| Setting | Default |
|---------|---------|
| Communication | Mirror user tone and language, concise |
| TypeScript | Strict when applicable |
| Styling | Tailwind CSS (if selected) |
| State | TanStack Query + Zustand (if selected) |
| Forms | React Hook Form + Zod (if selected) |
| API | REST/tRPC (if selected) |
