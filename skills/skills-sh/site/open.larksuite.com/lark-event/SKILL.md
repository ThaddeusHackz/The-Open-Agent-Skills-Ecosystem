---
name: lark-event
description: Install the lark-event skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-event
---

# Lark Events

>
Prerequisite: Read [`../lark-shared/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md) first for authentication, `--as user/bot` switching, `Permission denied` handling, and safety rules.

## Core commands

Command
Purpose

`lark-cli event list [--json]`
List all subscribable EventKeys

`lark-cli event schema <EventKey> [--json]`
Show an EventKey's params and output schema

`lark-cli event consume <EventKey> [flags]`
Blocking consume; events → stdout NDJSON

`lark-cli event status [--json] [--fail-on-orphan]`
Inspect the local bus daemon status

`lark-cli event stop [--all] [--force]`
Stop the bus daemon

## Common flags