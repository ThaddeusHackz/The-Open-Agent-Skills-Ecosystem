---
name: everyinfra
description: "Routes a task to the right EveryInfra product and uses its MCP or REST contract safely. EveryInfra gives one API key for structured data from 90 platforms (TikTok, Instagram, X, YouTube, LinkedIn, Reddit, Amazon, RedNote, Douyin), 17 web search tools, an OpenAI-compatible AI API, CAPTCHA solving, phone numbers, email and proxies. Applicable when the user mentions EveryInfra or asks which product fits a data, search or automation task."
version: 1.0.1
---

# EveryInfra router

Use the remote `everyinfra` MCP server for capability discovery and the four MCP-enabled product
lines. Use `https://api.everyinfra.com` only for a REST-only product. Never copy the API key into a
prompt, file, command output, log, URL query string, or response; read it from `EVERYINFRA_API_KEY`.

## Route by outcome

- Structured public platform data: EveryData.
- Current web, semantic, academic, forum, page or site retrieval: EverySearch.
- Text completion, extraction, classification, translation or summarization, including cleaning and
  labeling data collected with EveryData: EveryAI, the AI API.
- Captcha or anti-bot challenge solving on a target the user is authorized to access: EverySolve.
- Activation or rental phone number: EveryNumber.
- Transactional email: EveryMail.
- Proxy traffic packages: EveryProxy.

Do not infer a tool from an old document. MCP tool discovery and the REST catalogs are the
runtime truth. If the requested product is unavailable, report that state instead of silently
substituting a different mechanism.

## Common workflow

1. Identify the requested outcome and whether it has external side effects.
2. Use a discovery tool or catalog before the first operation call.
3. Validate required parameters, limits, solution shape and availability.
4. Invoke a state-changing operation only when the user's request authorizes that operation.
5. Read returned `quota`, status and error fields when present; never infer success or
   availability from HTTP 200 or catalog membership alone.
6. Report the useful result and any remaining external action separately.

EveryInfra uses one account and API key across product lines, but product-specific scopes
may still deny a call. A scope error is not a reason to broaden or replace the key automatically.

The former data cleanup tools were retired on 2026-10-09; do not look for them. EveryAI
(`everyinfra_chat`) handles that text work, within per-minute rate limits set for the account.

## Setup in Qoder

1. This skill reads your EveryInfra key from the `EVERYINFRA_API_KEY` environment variable or from the MCP connection configured in Qoder. If the key is missing, ask the user to configure it. Listing tools works without a key.
2. Add the remote MCP server `everyinfra` at `https://api.everyinfra.com/mcp` (Streamable HTTP) in the MCP settings, with the request header `Authorization` set to `Bearer` followed by the key.
3. Open the MCP tool list once to confirm the `everyinfra_*` tools are present. Treat that live list as the runtime truth.
