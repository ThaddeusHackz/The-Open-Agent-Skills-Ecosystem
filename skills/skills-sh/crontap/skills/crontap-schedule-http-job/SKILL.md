---
name: crontap-schedule-http-job
description: >
  Create, update, and verify recurring Crontap HTTP requests with cron or plain
  English, timezones, headers, and JSON bodies. Use when a user wants to
  schedule a webhook, API call, or cloud function through MCP or REST.
license: MIT
metadata:
  version: "1.0.0"
  group: main
  order: 2
  title: Schedule an HTTP job
  summary: Turn any API endpoint, webhook, or cloud function into a recurring request with timing verified before launch.
  bestFor: Webhooks, API calls, and cloud functions
  guide: https://crontap.com/cron-job-monitoring
  guideTitle: Cron job monitoring
  tools: create_schedule,update_schedule,preview_schedule,get_schedule_history
---

# Schedule an HTTP job

## Prerequisites

Before using the required tools, check whether they are available. If any are
missing, stop and offer the user exactly two choices:

1. Connect Crontap MCP at `https://mcp.crontap.com/mcp`. MCP access works on
   every Crontap tier.
2. Configure `$CRONTAP_CLIENT_ID` and `$CRONTAP_API_KEY` for the raw API. Raw
   API access requires Ultra.

Do not silently choose a path or continue until the user selects one.

- Confirm the absolute HTTP or HTTPS endpoint, method, cadence, and IANA
  timezone.
- Ask whether the endpoint needs headers, a JSON body, or an idempotency key.
- Keep credentials out of URLs and logs. Refer to values from a secure store.

## Workflow

1. Preview plain-English cadence and resolve every clarification.
2. Show the resolved cron, timezone, and next runs to the user.
3. Create the schedule with exactly one of `text` or `cron`.
4. For changes, identify the existing schedule and send only changed fields.
5. After execution, inspect retained history and verify the endpoint outcome.

## MCP examples

Preview without saving:

```json
{
  "tool": "preview_schedule",
  "arguments": {
    "text": "every weekday at 09:15",
    "timezone": "Europe/Copenhagen"
  }
}
```

Create a protected JSON request:

```json
{
  "tool": "create_schedule",
  "arguments": {
    "url": "https://app.example.com/api/daily-report",
    "text": "every weekday at 09:15",
    "timezone": "Europe/Copenhagen",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer <secret-from-secure-store>",
      "Content-Type": "application/json"
    },
    "body": {
      "source": "crontap"
    },
    "label": "Daily report"
  }
}
```

Partially update a schedule:

```json
{
  "tool": "update_schedule",
  "arguments": {
    "scheduleId": "<schedule-id>",
    "cron": "30 9 * * 1-5",
    "timezone": "Europe/Copenhagen"
  }
}
```

Omitted update fields preserve the existing configuration, including hidden
request secrets. An empty `headers` object replaces and clears headers.

Read recent runs:

```json
{
  "tool": "get_schedule_history",
  "arguments": {
    "scheduleId": "<schedule-id>",
    "limit": 20
  }
}
```

Use a returned `cursor` unchanged to request the next page.

## REST fallback

Use REST only when MCP is unavailable and the account has Ultra API access.
REST uses `interval`, `verb`, and `data` instead of the MCP aliases.

```bash
curl --fail-with-body https://api.crontap.com/v1/schedule \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "url": "https://app.example.com/api/daily-report",
    "interval": "30 9 * * 1-5",
    "timezone": "Europe/Copenhagen",
    "verb": "POST",
    "headers": {
      "Authorization": "Bearer <secret-from-secure-store>",
      "Content-Type": "application/json"
    },
    "data": {"source": "crontap"},
    "label": "Daily report"
  }'
```

## Verification

- Confirm the saved URL, method, cron, timezone, and next runs.
- Verify the endpoint handles the selected method and returns a success status.
- Inspect history after the first run for status, duration, timeout, and retry
  evidence.

## Safety and plan limits

- Preview local-time schedules before creating them, especially around DST.
- Do not overwrite headers or integrations during an unrelated partial update.
- Make write endpoints idempotent when retries or overlapping calls are
  possible.
- If a plan cap or cadence floor blocks creation, explain the structured
  four-option upgrade ladder and its smallest viable option.

## Troubleshooting

- A clarification response is not a failure. Ask the returned question, then
  preview again.
- A 401 or 403 from the target usually means an expired or malformed endpoint
  credential.
- A timeout means Crontap did not receive a response in time. Check endpoint
  runtime and downstream calls before increasing retries.
- A 404 from MCP means the schedule ID is stale. List schedules before retrying.

## References

- [Crontap Agent Skills catalogue](https://crontap.com/skills)
- [Cron job monitoring](https://crontap.com/cron-job-monitoring)
- [Cron troubleshooting](https://crontap.com/guides/cron-troubleshooting)
- [Cron syntax reference](https://crontap.com/blog/cron-syntax-cheatsheet)
- [Live REST API reference](https://api.crontap.com/docs/)
