---
name: aliyun-domain
description: Manage Alibaba Cloud domains, ICP filing, DNS, and Wan Xiao Zhi website building through MCP tools. Use for domain availability, prices or cost estimates, registration, renewal, transfers, DNS, security locks, contacts and registrant templates; ICP filing; or AI website operation. Also use to plan a domain operation or decide its next safe step from supplied results, including template approvals, real-name privacy, permission errors, rate limits, unknown write outcomes and pending tasks, even when no cloud call is requested. Support first-use authorization and domain-to-website delivery through MCP. Exclude production incident diagnosis, registry operations, competitor-price research, and generic source-code or shell tasks.
license: Apache-2.0
metadata:
  domain: aiops
  owner: aliyun-domain-team
  contact: keven.yef@alibaba-inc.com
  execution-surface: aliyun-domain-mcp
  mcp-server: aliyun-domain-mcp
---

# Alibaba Cloud Domain

Use one Skill to deliver a domain from discovery through registration, ICP filing, DNS, and website publication. Execute every product operation through MCP tools provided by the `aliyun-domain-mcp` server; never replace MCP tools with raw OpenAPI, SDK, HTTP, CLI, or console automation.

## MCP server configuration

This Skill requires the `aliyun-domain-mcp` MCP server:

```json
{
  "mcpServers": {
    "aliyun-domain-mcp": {
      "command": "npx",
      "args": [
        "mcp-remote-alibaba-cloud",
        "https://openapi-mcp.cn-hangzhou.aliyuncs.com/s/Domain/domain/2dd2d6410b8648938effea0a177280e6/mcp"
      ]
    }
  }
}
```

Discover available tools with `mcp_list`. Inspect a tool's input schema with `mcp_get` before calling. Invoke tools with `mcp_call`. All domain tool names use the `mcp__aliyun_domain__` prefix.

## Route before loading details

Load only the reference that matches the current intent.

| Intent | MCP tool namespace | Load |
|---|---|---|
| Search, pricing, registration, renewal, transfer, ownership, governance, audit, or DNS | `mcp__aliyun_domain__*` general tools | [Domain operations](references/domain.md) |
| ICP consultation, filing entry, filing status, or successful filing data | `mcp__aliyun_domain__icp_*` | [ICP filing](references/icp.md) |
| AI website creation, conversation, project, material, domain binding, preview, or deployment | `mcp__aliyun_domain__wxz_*` | [Website building](references/website.md) |
| A request spanning domain, ICP, DNS, and website stages | Multiple namespaces above | [Cross-product lifecycle](references/lifecycle.md), then only the active product reference |

## Cross-product orchestration

- **Products:** coordinate domain registration and management through `mcp__aliyun_domain__*` tools, ICP filing through `mcp__aliyun_domain__icp_*` tools, DNS through `mcp__aliyun_domain__dns_*` tools, and AI website building through `mcp__aliyun_domain__wxz_*` tools.
- **Call order:** for an end-to-end request, start at the earliest unmet stage and proceed as `discover and price -> acquire or transfer -> verify and govern -> file ICP when required -> build the website -> configure DNS and binding -> deploy and operate`. Load [Cross-product lifecycle](references/lifecycle.md) for the detailed stage contract, then load only the reference for the active stage.
- **Decision criteria:** skip a stage only when current MCP readback proves it is complete. Enter ICP when the user requests filing or the chosen China-hosted website path requires it. Change DNS only after the destination and intended records are known. Deploy only after preview, binding, and certificate state are explicit. Stop and hand control back to the user at every payment, identity review, confirmation, asynchronous wait, or external propagation boundary; never treat browser opening, order submission, or task acceptance as completion.

Load these shared references only when needed:

- Login, local identity, profile reuse, or OAuth failure: [Authentication](references/authentication.md)
- Any write, payment, deletion, transfer, DNS, publication, or credential-sensitive task: [Safety and confirmation](references/safety.md)
- A failed MCP tool call or uncertain completion: [Error recovery](references/error-recovery.md)
- Permission planning or `Forbidden.RAM`: [RAM permissions](references/ram-policies.md)
- Contacts, templates, real-name review, email, ICP personal data, or saved execution reports: [Private data and secure inputs](references/privacy-and-input.md)

Do not load all references preemptively.

## Supplied-state decisions

For an explanation or recovery plan based on supplied results, use those results without starting MCP server checks, login, cloud reads, or hypothetical writes. Distinguish `evidence_source=supplied_state` from `runtime_verified`; a sound decision is not proof that an API ran. Preserve any supplied target and task/plan identifiers, but ask for missing identifiers instead of generating them. Use the relevant domain and safety/error reference only; a known failed precondition or missing input is a handoff, not an instruction to manufacture a fixture, even when no cloud call is requested.

## Fail-closed execution invariant

Apply this state machine to every operation: `intent -> preflight -> preview_succeeded -> awaiting_confirmation -> execute_once -> verify`. Read-only operations may omit preview and confirmation, but not identifier validation or result verification.

1. Freeze an intent envelope before the first operational tool call: selected credential source, product namespace, exact user-supplied target identifiers, requested action, before/after values, and any price, duration, payment route, plan ID, or publication channel. Readbacks may resolve a missing identifier, but they must never replace an identifier the user supplied. If the exact target is missing, inaccessible, externally managed, or ambiguous, stop and ask for the correct target or account.
2. Advance only on structured MCP tool evidence for the same intent envelope. A tool name in the response, an attempted invocation, an OAuth callback, an error message that mentions an expected field, or a different resource's successful readback is not success.
3. Treat authentication unavailable, profile conflict, target mismatch, unsupported tool, failed or incomplete preview, missing fresh confirmation, and ambiguous write outcome as terminal for the current step. A non-retryable internal error is also terminal; a generic `next_action` does not override `retryable=false`. Return the confirmed state and the next safe MCP tool call; do not switch credentials, targets, namespaces, or execution surfaces to keep going, including for extra discovery or diagnosis after a failure.
4. High-risk and financial confirmation is valid only after a successful current preview exposes the exact impact. Earlier broad instructions such as "执行到底" are not post-preview approval. If the runtime cannot collect a reply, present the preview and stop.

Use [Safety and confirmation](references/safety.md) for the evidence and confirmation rules, [Authentication](references/authentication.md) for OAuth terminal states, and [Error recovery](references/error-recovery.md) for the only permitted recovery paths.

## Operating contract

1. Use `mcp_get` to inspect a tool's input schema before first use when argument names are uncertain. Do not guess argument names or values; never call a generated OpenAPI action or substitute another product's tool.
2. Let the MCP server resolve the credential source internally. The server can reuse parent-resolved standard AK/STS credentials or manage China-site OAuth. Use `mcp__aliyun_domain__auth` to check local credential context and `mcp__aliyun_domain__whoami` to verify the selected cloud identity. Keep the selected profile/configuration store fixed across related calls. Never request, read, print, or persist an AK, SK, bearer token, OAuth token, transfer code, identity document, or payment secret. Never rebuild a profile using `aliyun configure set`, credential flags, or shell variable defaults.
3. Do not pass region or endpoint arguments during normal use. The MCP server owns the China-site endpoint and `cn-hangzhou` routing.
4. Read-only tools may run after intent and identifiers are clear. For writes, require a successful MCP preview for the frozen intent envelope, explain its impact, obtain a fresh user confirmation, then execute the confirmed tool call exactly once with the required confirmation arguments.
5. Parse `status`, `ok`, identifiers, task IDs, `next_step`, and error codes from tool output. Check semantic success before advancing: a field name or planned tool call appearing in failed output is not evidence that the step succeeded. Use [Error recovery](references/error-recovery.md) for bounded waits and a resumable final state.
6. Report what changed, what did not change, how it was verified, and any remaining user action. Include a compact `skill_result`, evidence source, underlying tool status/error, write effect, and next step; do not rename the tool status to make it look successful. End the current step after missing-input, confirmation or external handoff; do not leave a background wait for a reply.
7. Before a personal-data write, require the actual input and required fields supported by the tool. A label such as a company name is not a complete registrant profile. Ask for the missing non-secret input; do not invent contact details or reuse an unrelated template to satisfy the request.
8. Execute conditional follow-up reads only when successful discovery returns their required identifiers. An empty successful account query completes that query scope. Return the missing prerequisite for unexecuted steps; do not invent targets or keep querying the same empty list. For a supplied-state decision or explanation, a supplied-state decision reasons from that evidence without logging in or executing the hypothetical write.

## Scope boundaries

This Skill owns customer-facing domain MCP tool operation and orchestration. It does not own:

- Production failure diagnosis, logs, databases, EPP traces, or source-code root-cause analysis.
- Registry onboarding, certificate rotation, registry balances, or production EPP operations.
- Competitor registrar price crawling or market analysis.
- Generic React, backend, or infrastructure coding that does not use `mcp__aliyun_domain__wxz_*` tools.
- Direct OpenAPI or SDK execution when the MCP server lacks a tool. Report the gap instead of bypassing MCP.

## Completion check

Before declaring success, verify all applicable points:

- The MCP server is accessible and responding.
- The tool's input schema supports every argument used.
- Credential selectors remained consistent.
- User-supplied target identifiers were not replaced by discovered resources.
- Each high-risk step received the confirmation required by the tool and this Skill.
- Every executed write is backed by a successful same-target preview rather than tool-name matching.
- Each asynchronous operation reached a terminal state or is explicitly handed off with a task ID and next tool call.
- No credential or sensitive value appears in the response or saved artifacts.
- The final answer distinguishes submitted, accepted, completed, browser-opened, and externally propagated states.
