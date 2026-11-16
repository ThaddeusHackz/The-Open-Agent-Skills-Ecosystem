---
name: picqer-fulfillment
description: 一个仅支持 JSON 格式的 API 接口，用于从 Picqer 系统获取包含 KPI、拣货单、库存和收入在内的完整仪表盘数据。该工具提供多个命令（如 dashboard.fetch, picklists.fetch 等）以获取特定维度的业务数据，并严格遵循安全策略，API 密钥本地存储且仅限 Tailscale 访问。
---

# FutureFulfillment Picqer Dashboard v2

JSON-only API for dashboard data. No markdown responses.

## Commands

All commands return JSON. No chat explanations.

### `dashboard.fetch`
Returns complete DashboardData object with KPIs, picklists, stock, and revenue.

**Input:** `{ "command": "dashboard.fetch", "filters": { "dateFrom": "2024-01-01", "dateTo": "2024-01-31", "picker": "", "client": "" } }`

### `picklists.fetch`
Returns only picklists data (open, closed, picker stats).

**Input:** `{ "command": "picklists.fetch", "filters": {} }`

### `stock.fetch`
Returns stock movements with slow/fast mover categorization.

**Input:** `{ "command": "stock.fetch", "filters": {} }`

### `revenue.fetch`
Returns revenue per client for sell-stock clients.

**Input:** `{ "command": "revenue.fetch", "filters": {} }`

## Response Format

Always returns JSON. Example success:
```json
{
  "kpis": { "openPicklists": 42, "closedPicklists": 128, ... },
  "picklists": { "open": [...], "closed": [...], "pickerStats": [...] },
  "stock": { "rows": [...] },
  "revenue": { "perClient": [...] },
  "filtersUsed": { ... }
}
```

Example error:
```json
{ "error": "Picqer API not configured" }
```

## Security

- API key only in local .env file
- No credentials in OpenClaw config
- Access via Tailscale only
