---
name: ui-control-center
description: 维护本地代理控制 UI，涵盖可靠性、缓存、仪表板、交易标签页以及代理/工作流/技能标签页的管理。
---

# ui-control-center

## Purpose
Maintain the local Agent Control UI: reliability, caching, dashboards, trading tab, agents/workflows/skills tabs.

## Use when
- UI shows stale/wrong state
- Port 8765 conflicts
- Need new tabs/endpoints

## Safety rails
- Local-only binding (127.0.0.1)
- Avoid blocking the event loop: run heavy work in threads

## Checklist
1) Ensure only one server listens on 8765.
2) Add cache-busting for static assets.
3) Keep endpoints resilient to missing files.
4) Log actions to audit.
