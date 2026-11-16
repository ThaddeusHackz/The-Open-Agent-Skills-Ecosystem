---
name: deepline-engine
description: Install the deepline-engine skill for your AI agent. Published on code.deepline.com.
source: https://www.skills.sh/site/code.deepline.com/deepline-engine
---

# Deepline Engine

## Quick Start

```
npm install -g deepline
deepline -h
```

## CLI resolution

Run `deepline` when it is available. If the shell reports that command is missing, use `<workspace-root>/.deepline/runtime/bin/deepline` (or the npm-created `.cmd` shim on Windows). If neither exists, follow `https://code.deepline.com/INSTALL.md` to set up Deepline.

Build an engine from the state machine the user defines.

An engine is an orchestrator Deepline Play that accepts an input, determines its state, calls the transition Play for that state, and produces a new state. The durable data plane lives in Customer DB: every state has an input table and an output table. The output of one transition can become the input to the next state.

The user owns the states, transition rules, transformations, and terminal behavior. This skill owns the reusable structure for turning those decisions into a replay-safe Play. Infer routine names, schemas, advancement behavior, and implementation details from the request and repository conventions. Ask only when missing information would force the engine to invent substantive business policy or create an unsafe side effect. Do not import an outbound workflow, GTM recipes, provider choices, or domain-specific policy unless the user asks for them.