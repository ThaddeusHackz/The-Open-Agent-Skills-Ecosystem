---
name: everymail
description: "Uses the EveryInfra transactional-email REST API: checks email capabilities and quota, sends or schedules an email, submits a batch, cancels a scheduled message, and reads delivery events. Applicable when the user asks to send transactional email through EveryInfra and has authorized the recipients and content."
version: 1.0.1
---

# EveryMail

EveryMail is REST-only in the current plugin. Do not invent an MCP tool for it. Use
`https://api.everyinfra.com` with `Authorization: Bearer $EVERYINFRA_API_KEY`.

1. Read `GET /api/v1/email/catalog` and, when authenticated, `GET /api/v1/email/usage`.
2. For a single message, use `POST /api/v1/email/send` with catalog-declared fields. Recipients are
   counted across `to`, `cc` and `bcc`; the API does not accept arbitrary `from`, headers or
   attachments.
3. Use `POST /api/v1/email/batch` for a true batch. Scheduled messages must use the single-send
   endpoint so cancellation remains unambiguous.
4. Sending email is an external communication. Do not send until the user has authorized the actual
   recipients and content; preparing a draft is not authorization to dispatch it.
5. Do not log message bodies, verification codes or reset links. Report the returned `message_id`,
   status and quota without exposing private content.

Domain verification, webhook mutation and final dispatch are state-changing operations. Keep their
scope exact and do not broaden API-key permissions automatically.

## Setup in Qoder

This skill reads your EveryInfra key from the `EVERYINFRA_API_KEY` environment variable. If it is missing, ask the user to configure it. This skill calls the REST API at `https://api.everyinfra.com` directly; the catalog endpoint named above works without a key.
