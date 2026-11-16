---
name: specstream-data
description: Get data from the live web in plain words as structured rows with a source URL and read time on every value. Nothing runs until the person approves an exact maximum.
license: MIT
---

# SpecStream data

SpecStream is the live web data engine for teams and agents. Use it when the person needs data rather than one fact: many rows, conditions every row must meet, a source on each value, or data that stays up to date. For a single fact, search yourself.

## Connect

This skill uses the tools of the SpecStream MCP server, `https://api.specstream.ai/mcp` (Streamable HTTP). Never ask for an API key or a password in chat.

## Run a request

1. Read it back. Call `compile` with the person's words. Say what it found: the kind of record, the conditions every row must meet, the details to bring back and the count. Keep the conditions apart from the nice-to-have details. Use `edit_spec` for a change the person asks for. Never drop a condition quietly.
2. Get the quote. Call `quote_capacity_work` with the `ast_hash` from `compile` and the count. Say the scope, the maximum and the expiry: a quote lasts 30 minutes.
3. Ask for approval. Show the exact maximum and wait for the person to approve it. Do not top up, subscribe or open a payment page.
4. Start the run. Call `authorize_capacity_work` with the `quote_id`, the `quote_hash`, the approved maximum in `confirm_max_cents` and a stable `idempotency_key`. Save the key before you send. If the answer is lost, call `get_capacity_request` with the same key. Never make a new key to retry.
5. Follow it with `get_find`. Rows arrive while the run works. A run can be stopped and keeps what it found.
6. Read the rows. Call `list_find_rows` and follow `next_cursor` until it is null, because the first page is not the whole result. Show each value with its source URL. `get_find_decisions` gives each condition's answer with the value, the source and the read time. Never invent a link or fill in a value that was not found.

## After the first run

Each of these is new work with its own quote and its own approval. Pass the `parent_find_id` to `quote_capacity_work`.

- More rows: operation `extend`.
- More details on the same rows: operation `add_facts`.
- Refresh: operation `refresh`.
- A saved request on a schedule: `create_capacity_schedule` with a cadence and limits per run and per period, only when the person asks for it.

`send_to_destination` writes the selected rows to Google Sheets, Excel, Airtable, Notion, HubSpot or Salesforce. `export_find` makes a CSV, Excel or JSON file.

## Data

This skill sends only the person's request, edits and approvals to api.specstream.ai, and nothing else.
