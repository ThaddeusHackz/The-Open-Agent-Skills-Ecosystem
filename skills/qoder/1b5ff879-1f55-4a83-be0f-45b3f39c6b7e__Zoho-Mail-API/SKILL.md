---
name: zoho-mail-api
description: Read, search, draft, and send email through a Zoho Mail account using the Zoho Mail REST API v1. Handles OAuth token caching, account discovery, and a manual-review draft workflow. Use when the user asks to read Zoho Mail, search Zoho email, create a Zoho email draft, send email via Zoho, or check for new Zoho messages.
---

# Zoho Mail API

This skill provides a reusable Python client for the Zoho Mail REST API v1.

## What it does

- Lists inbox messages
- Searches mail using Zoho search syntax
- Reads full message content
- Saves drafts
- Prepares drafts and creates an Apple Reminder (or fallback reminder file) so the user reviews before sending
- Sends email immediately
- Detects new incoming mail using a local state file

## Quick start

1. Ensure the client script is in the current workspace. If it is not, copy it from the skill:

   ```bash
   cp ~/.qoderwork/skills/zoho-mail-api/scripts/zoho_mail_client.py .
   cp ~/.qoderwork/skills/zoho-mail-api/.env.example .
   cp ~/.qoderwork/skills/zoho-mail-api/requirements.txt .
   pip install -r requirements.txt
   ```

2. Fill in `.env` with Zoho OAuth credentials (see setup.md).

3. Verify the configuration:

   ```bash
   python zoho_mail_client.py check-config
   ```

4. Run the desired command.

## Common commands

List inbox messages:

```bash
python zoho_mail_client.py list --limit 10
```

Search messages:

```bash
python zoho_mail_client.py search "from:alice@example.com"
```

Read a message:

```bash
python zoho_mail_client.py get MESSAGE_ID
```

Create a draft:

```bash
python zoho_mail_client.py draft \
  --to recipient@example.com \
  --subject "Subject" \
  --body "<p>Body</p>"
```

Prepare a draft for manual review (creates an Apple Reminder on macOS):

```bash
python zoho_mail_client.py prepare-draft \
  --to recipient@example.com \
  --subject "Review me" \
  --body "<p>Draft body</p>" \
  --due-minutes 30
```

Send an email immediately:

```bash
python zoho_mail_client.py send \
  --to recipient@example.com \
  --subject "Hello" \
  --body "<p>Body</p>"
```

Check for new mail:

```bash
python zoho_mail_client.py check-new
```

## Workflows

### Read or search email

1. Run `check-config` to confirm credentials.
2. Use `list` or `search` to find messages.
3. Use `get MESSAGE_ID` to read the full content.

### Prepare a draft for manual review

1. Use `prepare-draft` to create the draft and a reminder.
2. On macOS, review the Apple Reminder and send the draft from the Zoho Mail web/app UI.
3. On other platforms, the reminder is written to `.zoho_drafts_pending.txt`.

### Detect new mail periodically

Use `check-new`. It stores seen message IDs in `.zoho_mail_state.json` and only prints unseen messages. Schedule it with cron or a QoderWork scheduled task.

## Important notes

- Required OAuth scopes: `ZohoMail.messages.ALL` and `ZohoMail.accounts.READ`.
- One refresh token can cover both scopes, or you can use separate tokens with `ZOHO_REFRESH_TOKEN_MESSAGES` and `ZOHO_REFRESH_TOKEN_ACCOUNTS`.
- Access tokens are cached in `.zoho_tokens.json` to avoid Zoho's refresh-token rate limit.
- The account ID is discovered once and cached in `.zoho_account.json`.
- The inbox folderId is resolved automatically; other folders need a numeric `ZOHO_FOLDER_ID` or `--folder` argument.

## Files

- `scripts/zoho_mail_client.py` — the reusable client and CLI
- `.env.example` — template for credentials
- `requirements.txt` — Python dependencies
- `setup.md` — detailed OAuth setup instructions
