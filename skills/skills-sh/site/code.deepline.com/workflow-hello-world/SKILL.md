---
name: workflow-hello-world
description: Install the workflow-hello-world skill for your AI agent. Published on code.deepline.com.
source: https://www.skills.sh/site/code.deepline.com/workflow-hello-world
---

# Cloud Workflow Triggers

This is a recipe shortcut. It pre-selects the workflow-hello-world recipe but the deepline-gtm governs the entire session.

## Execution order

- Invoke `deepline-gtm` using the Skill tool.

- Follow the meta-skill's full routing instructions - analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.

- Additionally read the workflow-hello-world recipe at `../deepline-gtm/recipes/workflows-hello-world.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.