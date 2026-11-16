---
name: deepline-pre-research
description: Install the deepline-pre-research skill for your AI agent. Published on code.deepline.com.
source: https://www.skills.sh/site/code.deepline.com/deepline-pre-research
---

# deepline-pre-research (renamed to deepline-research)

## Quick Start

```
npm install -g deepline
deepline -h
```

This skill was renamed. `deepline-pre-research` is a temporary alias kept so existing prompts, scripts, and saved commands keep working. It will be removed.

## What to do

Load the `deepline-research` skill and follow it for this request. Do not answer from this file; it contains no instructions of its own.

If the skill loader supports names, invoke `deepline-research`. Otherwise read the entrypoint directly, trying these roots in order and using the first that exists:

```
for candidate in \
  "$PWD/.skills/deepline-research" \
  "$HOME/.claude/skills/deepline-research" \
  "$HOME/.agents/skills/deepline-research"; do
  [ -d "$candidate" ] && { echo "$candidate/SKILL.md"; break; }
done
```

Then tell the user once, in a single line, that `/deepline-pre-research` is now `/deepline-research`, and continue with the actual request.