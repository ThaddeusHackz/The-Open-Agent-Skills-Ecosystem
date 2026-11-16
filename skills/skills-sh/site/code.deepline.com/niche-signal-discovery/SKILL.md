---
name: niche-signal-discovery
description: Install the niche-signal-discovery skill for your AI agent. Published on code.deepline.com.
source: https://www.skills.sh/site/code.deepline.com/niche-signal-discovery
---

# niche-signal-discovery (renamed to deepline-scoring)

## Quick Start

```
npm install -g deepline
deepline -h
```

This skill was renamed. `niche-signal-discovery` is a temporary alias kept so existing prompts, scripts, and saved commands keep working. It will be removed.

## What to do

Load the `deepline-scoring` skill and follow it for this request. Do not answer from this file; it contains no instructions of its own.

If the skill loader supports names, invoke `deepline-scoring`. Otherwise read the entrypoint directly, trying these roots in order and using the first that exists:

```
for candidate in \
  "$PWD/.skills/deepline-scoring" \
  "$HOME/.claude/skills/deepline-scoring" \
  "$HOME/.agents/skills/deepline-scoring"; do
  [ -d "$candidate" ] && { echo "$candidate/SKILL.md"; break; }
done
```

Then tell the user once, in a single line, that `/niche-signal-discovery` is now `/deepline-scoring`, and continue with the actual request.