---
name: compression
description: 用于迭代式 AI 开发循环的预运行提示词压缩脚本，通过压缩提示词文件减少输入令牌数量，支持本地运行、自动备份及即时撤销。
---

# Trinity Compress (Skill)

Pre-run prompt compression for iterative AI dev loops.

**Goal:** reduce input tokens every iteration by compressing prompt files *before* your loop runs.

- Works with Ralph-style loops, agent/skill directories, and most token-billed providers.
- Runs as a **local script** (no model calls).
- Creates **.bak** backups and supports instant undo.

## What it installs into a repo
- `trinity-compress.config.json` — rules + targets
- `scripts/trinity-compress.sh` — compression script
- Makefile snippet (optional): `optimize-prompts`, `optimize-undo`, etc.
- `.gitignore` snippet: ignore `*.bak`
- Installers:
  - `scripts/install.ps1` (Windows)
  - `scripts/install.sh` (bash)

## Requirements
- bash 4+
- `jq`
- `bc`

## Use
1) Install into your repo (copy assets or use the included installer scripts)
2) Run:
   - `bash scripts/trinity-compress.sh balanced`
   - or via Makefile target

## Undo
- Restores all `*.bak` backups from the last run.

## Notes
- This tool does not rewrite code blocks, URLs, file paths, or variable names.
- Aggressive mode may reduce clarity; review before committing.
