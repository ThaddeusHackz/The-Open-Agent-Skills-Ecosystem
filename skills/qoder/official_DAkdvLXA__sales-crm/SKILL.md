---
name: sales-crm
description: Update CRM records, pipeline stages, and follow-ups.
triggers:
  - CRM
  - pipeline
  - sales
  - update record
  - follow-up
---

# Sales CRM

## When to use
- User wants to update CRM
- Move deal through pipeline
- Schedule follow-ups

## Steps
1. Identify record and action
2. Use CRM API if available
3. Confirm update

## Output format
- Confirm what was updated
- New pipeline stage if changed
- Next follow-up date
