---
name: everyai
description: "Runs text work through the EveryInfra OpenAI-compatible AI API: cleaning or labeling collected data, summarization, translation, classification, extraction and rewriting. Applicable when the user asks to process collected records or text through EveryInfra."
version: 1.0.1
---

# EveryAI

Use the MCP tool `everyinfra_chat`.

1. Build an OpenAI-style `messages` array with only the context required for the task.
2. Use a model value only when it appears in the live MCP schema; otherwise keep the server default.
3. Do not send secrets, credentials, private source documents or personal data unless the user has
   explicitly placed that data and this processing in scope.
4. Validate the returned content against the requested format. A fluent answer is not evidence that
   a factual claim is current; use EverySearch when current verification is required.
5. If the response reports that the account is not enabled for the AI API, tell the user to check
   their EveryInfra account instead of retrying.

For direct OpenAI-compatible SDK use, the REST base is `https://api.everyinfra.com/api/v1`; the
plugin should still prefer MCP when its tool is available.

## Cleaning collected data

The former data cleanup tools were retired on 2026-10-09. To clean, deduplicate, classify, extract
or summarize records collected with EveryData, pass the relevant fields to `everyinfra_chat`,
describe the output format, and validate the result before using it. About 20,000 tokens of input
per request is reliable; split longer inputs into chunks. Per-minute rate limits apply per account
(all keys on the account combined); after a
rate-limit error, wait before retrying.

## Setup in Qoder

1. This skill reads your EveryInfra key from the `EVERYINFRA_API_KEY` environment variable or from the MCP connection configured in Qoder. If the key is missing, ask the user to configure it. Listing tools works without a key.
2. Add the remote MCP server `everyinfra` at `https://api.everyinfra.com/mcp` (Streamable HTTP) in the MCP settings, with the request header `Authorization` set to `Bearer` followed by the key.
3. Open the MCP tool list once to confirm the `everyinfra_*` tools are present. Treat that live list as the runtime truth.
