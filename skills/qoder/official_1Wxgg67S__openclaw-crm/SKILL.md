---
name: openclaw-crm
description: 面向本地的客户关系管理系统，用于跟踪潜在客户、交易、后续跟进和销售漏斗。采用带 WAL 模式的 SQLite 数据库，通过 Commander 提供命令行界面。
---

# openclaw-crm

Local-first CRM for tracking leads, deals, follow-ups, and pipeline. Uses SQLite with WAL mode, CLI via Commander.

## Quick Start
- `cd skills/crm && npm install`
- Run `node src/cli.js lead add "John Doe" --email john@example.com`
- Generate interchange: `node src/cli.js refresh`

## Integration
Use `exec` tool: `crm lead list`, `crm deal add "New Deal" --contact abc123 --value 10000`

Interchange files in workspace/interchange/crm/ for cross-agent sharing.