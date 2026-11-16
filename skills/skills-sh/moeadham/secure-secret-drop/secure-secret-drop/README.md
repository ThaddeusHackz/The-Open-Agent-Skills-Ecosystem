# Secure Secret Drop

Dead-simple secret sharing with an AI agent. It uses Cloudflare's free Quick Tunnels to generate a temporary public capability URL backed by an HTTP origin bound only to `127.0.0.1`, so you can securely drop a secret, password, or credential—then have it disappear.

![Secure Secret Drop form](assets/secure-secret-drop.png)

## Requirements

- A local AI agent that can run shell commands and read a `SKILL.md`
- Python 3
- `cloudflared`

No Cloudflare account, domain, or login is required. If `cloudflared` is missing, the skill guides the agent through installing it from an official source.

## Install

```bash
npx skills add moeadham/secure-secret-drop
```

## Use it

Just say:

> Send me a secure drop link.

Your agent will send you a temporary, single-use public capability URL. Open it, enter the requested secret, submit it, and reply that you are done.

## What to expect

- The link expires automatically and accepts one submission.
- Secret values are not printed in chat or command output.
- Submitted bytes go directly from the short-lived receipt to the explicitly approved destination file; they are not placed in model context.
- Existing destination keys are not replaced without explicit approval.
- Temporary forms can be cancelled at any time.
- macOS and Linux are supported.

Cloudflare terminates HTTPS for the temporary Quick Tunnel, so it is part of the trust boundary. This skill is intended for short-lived development secret handoffs.
