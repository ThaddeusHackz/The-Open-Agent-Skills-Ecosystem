---
name: layana-email-drafter
description: AI email drafting queue with staff review flow via Resend

name_cn: "邮件起草"
description_cn: "AI 电子邮件起草队列，通过重新发送进行员工审核流程。"---


# Layana Email Drafter Skill

Drafts responses to guest inquiry emails automatically and queues them for human approval. 

## Trigger Details
- **Ingress:** Webhook triggered by incoming email to Layana aliases (via n8n email parse).
- **Execution:** Paperclip calls OpenClaw with parsed body and subject.

## Execution Flow
1. **Context Extraction**:
   - Paperclip extracts sender email and checks Supabase `clients` for matching profiles/VIP history.
2. **Draft Generation**:
   - Uses `Claude-3-5-Sonnet` to generate a polished reply that follows the `{tone_guide}` and `{brand_guidelines}` retrieved from Notion KB.
3. **Queue Creation**:
   - Insterts draft into Supabase `email_drafts` table with `status = 'pending_review'`.
4. **Staff Alerting**:
   - Posts an interactive block to Slack `#staff-copilot` with [Approve], [Edit], or [Reject] buttons.
   - Approval routes to Resend API.

## Prompt Guidelines
- Ensure tone is luxurious, welcoming, and concise. Never use passive voice.
- Default sign-off is "Warm island regards, Layana Customer Experience Team".
