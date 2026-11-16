---
name: everynumber
description: "Uses the EveryInfra phone-number REST API for activation and rental numbers: reads the catalog, orders an authorized verification number, polls the received code, cancels an unused activation and reads order history. Applicable when the user needs a verification number for an account they are authorized to register."
version: 1.0.1
---

# EveryNumber

EveryNumber is REST-only in the current plugin. Do not invent an MCP tool for it. Use
`https://api.everyinfra.com` with `Authorization: Bearer $EVERYINFRA_API_KEY`.

## Activation flow

1. Read `GET /api/v1/sms/catalog`. Select the exact `country` and service string from it.
2. `POST /api/v1/sms/number` with `country`, `product` and optional `voice` or `reuse`.
3. Preserve the returned `order_id`. Poll
   `GET /api/v1/sms/code/{order_id}` at a reasonable interval.
4. An activation completes when a code is successfully retrieved, not when the number is
   allocated. Read the returned status fields.
5. If the number is no longer needed before settlement, call
   `POST /api/v1/sms/cancel/{order_id}` so inventory is released.

## Rental flow

Use `GET /api/v1/sms/rental/catalog` before `POST /api/v1/sms/rental`. Rentals take effect at order
time and cannot be cancelled or renewed. Because this cannot be undone, obtain explicit user intent
for the country and term before ordering. Treat received codes and messages as sensitive one-time
credentials and do not store them in logs or project files.

## Setup in Qoder

This skill reads your EveryInfra key from the `EVERYINFRA_API_KEY` environment variable. If it is missing, ask the user to configure it. This skill calls the REST API at `https://api.everyinfra.com` directly; the catalog endpoint named above works without a key.
