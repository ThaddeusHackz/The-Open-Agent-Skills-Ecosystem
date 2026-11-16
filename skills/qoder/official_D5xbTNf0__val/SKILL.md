---
name: val
description: 此文件作为稳定入口点，供尝试从工作区根目录读取 SKILL.md 的智能体使用。定义了技能实际存放位置及 Calibre 相关的硬性路由规则。
---

# Workspace Skill Entry

This file exists as a stable entry-point for agents that try to read `SKILL.md` from the workspace root.

## Where Skills Actually Live

- Root index: `skills/README.md`
- Calibre read-only: `skills/calibre-catalog-read/SKILL.md`
- Calibre metadata edit: `skills/calibre-metadata-apply/SKILL.md`

## Calibre Routing (Hard Rule)

- Read/search/list/id -> `calibre-catalog-read`
- Metadata edit/fix/update (title/authors/series/series_index/tags/publisher/pubdate/languages) -> `calibre-metadata-apply`
- Never start `calibre-server` from chat flow. Connect to an already-running Content server.

