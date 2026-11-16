---
name: everyproxy
description: "Uses the EveryInfra traffic-package proxy REST API: reads the package catalog, orders an authorized rotating or sticky proxy allocation, checks provisioning status and retrieves one-time proxy credentials. Applicable when the user asks to order or check an EveryInfra proxy package."
version: 1.0.1
---

# EveryProxy

EveryProxy is REST-only in the current plugin. Do not invent an MCP tool for it. Use
`https://api.everyinfra.com` with `Authorization: Bearer $EVERYINFRA_API_KEY`.

1. Read the `GET /api/v1/proxy/catalog` response. Select a live package by `gb`, `kind`,
   `region` and optional `sticky_minutes`; packages are sized by traffic, not by session minutes.
2. `POST /api/v1/proxy/order` creates an order and may return credentials immediately. The user's
   request must authorize the package and region before ordering.
3. For asynchronous provisioning, inspect `GET /api/v1/proxy/order/{order_id}` without `deliver`.
   Status inspection must not be turned into a new order.
4. Use `?deliver=1` only when the user intends to accept delivery. Delivery can expose
   the password exactly once.
5. Move credentials only to the user-approved secret destination. Never print them in normal chat,
   command logs, screenshots, source files or Git history.
6. Report the order status. If delivery failed, create a new
   order only with user authorization.

## Setup in Qoder

This skill reads your EveryInfra key from the `EVERYINFRA_API_KEY` environment variable. If it is missing, ask the user to configure it. This skill calls the REST API at `https://api.everyinfra.com` directly; the catalog endpoint named above works without a key.
