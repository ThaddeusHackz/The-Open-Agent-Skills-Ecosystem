---
name: deepline-research
description: Install the deepline-research skill for your AI agent. Published on code.deepline.com.
source: https://www.skills.sh/site/code.deepline.com/deepline-research
---

# Deepline Research

## Quick Start

```
npm install -g deepline
deepline -h
```

## CLI resolution

Run `deepline` when it is available. If the shell reports that command is missing, use `<workspace-root>/.deepline/runtime/bin/deepline` (or the npm-created `.cmd` shim on Windows). If neither exists, follow `https://code.deepline.com/INSTALL.md` to set up Deepline.

Before the first Deepline fanout in a task, run `deepline billing balance` as
one standalone command and wait for it to finish. Never submit it beside
another Deepline command.

Find the highest-signal GTM data sources, public evidence, and market language for a research or enrichment job before building the pipeline. This is a standalone Deepline skill that should behave like `last30days` with a GTM data lens: broad source coverage, recency, community signals, citations, source stats, and a grounded "What I learned" synthesis. In Deepline, the report first explains what the research found; only after that does it translate the findings into Deepline tool contracts, private/proprietary joins, and Deepline-facing cost.