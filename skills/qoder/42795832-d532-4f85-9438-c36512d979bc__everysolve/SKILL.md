---
name: everysolve
description: "Discovers and solves CAPTCHA challenges through EveryInfra for targets the user is authorized to access. Applicable when a legitimate testing, registration or automation flow is blocked by Turnstile, reCAPTCHA, hCaptcha, an image challenge or another listed challenge type (52 types)."
version: 1.0.1
---

# EverySolve

Use `everyinfra_list_captcha_types` before `everyinfra_solve_captcha`.

1. Confirm that the target and automation are within the user's authorized scope.
2. Discover the exact `type`, required fields, optional fields, current availability and solution
   shape. A token, cookie, text answer, number, field map, point list or box list requires a different
   application step.
3. Check whether the type requires the caller's proxy. Cookie-bound solutions must be solved and
   consumed from the required network identity.
4. Pass only the selected type's declared parameters to `everyinfra_solve_captcha`.
5. Apply the solution only to the intended target and flow. Do not reuse tokens or cookies across
   unrelated targets.
6. Read the explicit status and error fields; the response is the evidence for a particular call.

Do not downgrade an unsupported challenge to a visually similar type. Report unavailable inventory
or a missing required parameter instead of making repeated calls on guesses.

## Setup in Qoder

1. This skill reads your EveryInfra key from the `EVERYINFRA_API_KEY` environment variable or from the MCP connection configured in Qoder. If the key is missing, ask the user to configure it. Listing tools works without a key.
2. Add the remote MCP server `everyinfra` at `https://api.everyinfra.com/mcp` (Streamable HTTP) in the MCP settings, with the request header `Authorization` set to `Bearer` followed by the key.
3. Open the MCP tool list once to confirm the `everyinfra_*` tools are present. Treat that live list as the runtime truth.
