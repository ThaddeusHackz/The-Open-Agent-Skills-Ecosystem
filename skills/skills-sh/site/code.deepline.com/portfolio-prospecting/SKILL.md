---
name: portfolio-prospecting
description: Install the portfolio-prospecting skill for your AI agent. Published on code.deepline.com.
source: https://www.skills.sh/site/code.deepline.com/portfolio-prospecting
---

# Portfolio/VC Prospecting

## Quick Start

```
npm install -g deepline
deepline -h
```

This is a recipe shortcut. It pre-selects the portfolio-prospecting recipe but the deepline-gtm governs the entire session.

## Execution order

- Invoke `deepline-gtm` using the Skill tool.

- Follow the meta-skill's full routing instructions - analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.

- Follow the meta-skill's routing gate for this recipe. Read the portfolio-prospecting recipe at `../deepline-gtm/recipes/portfolio-prospecting.md` (relative to this file) only when that gate routes you to it. Conditional access and safety checks still apply.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.