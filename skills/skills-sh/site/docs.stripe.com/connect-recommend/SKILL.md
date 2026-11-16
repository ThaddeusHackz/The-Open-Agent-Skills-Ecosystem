---
name: connect-recommend
description: Install the connect-recommend skill for your AI agent. Published on docs.stripe.com.
source: https://www.skills.sh/site/docs.stripe.com/connect-recommend
---

## Connect recommend

Recommend the right Stripe Connect integration configuration. The user only needs to provide a company URL or describe their business — the skill figures out the rest.

### Interaction model

User must confirm interactions. Every decision point in this skill MUST be confirmed with the user with clear, numbered options and short descriptions. One question at a time — never overwhelm the user.

Auto-act on low-cost actions. Never ask permission for:

- Generating the markdown recommendation plan — just generate it

- Scanning the codebase — just scan it

- Reading reference files — just read them

Never end with passive text. Every stopping point must end with a prompt to the user offering concrete next actions.

### Terminology rules (user-facing output)

Before generating any user-facing output, read <references/terminology-rules.md>. Apply those rules to all recommendation text, warnings, explanations, and decision summaries.