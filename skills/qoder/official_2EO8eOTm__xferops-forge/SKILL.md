---
name: xferops-forge
description: Forge MCP技能已拆分为三个专注型技能：forge-dev-workflow用于日常开发循环，forge-board-admin用于项目管理，forge-setup用于首次安装与配置。拆分旨在精简上下文并提高建议的可操作性。
---

# Forge Skills

The Forge MCP skill has been split into three focused skills. Use the one that matches your intent:

| Skill | When to use |
|-------|-------------|
| [`forge-dev-workflow`](./forge-dev-workflow/SKILL.md) | Picking up tickets, moving them through columns, linking PRs, commenting — the daily dev loop |
| [`forge-board-admin`](./forge-board-admin/SKILL.md) | Managing projects, columns, and team membership |
| [`forge-setup`](./forge-setup/SKILL.md) | First-time install and configuration, or when health check fails |

## Why three skills?

Loading 26 tools + docs for every ticket comment is wasteful. Each skill now covers only the tools and workflow guidance relevant to a specific intent, keeping context lean and guidance actionable.
