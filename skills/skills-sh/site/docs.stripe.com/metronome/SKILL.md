---
name: metronome
description: Install the metronome skill for your AI agent. Published on docs.stripe.com.
source: https://www.skills.sh/site/docs.stripe.com/metronome
---

Metronome API base: `https://api.metronome.com`. Authenticate with a Bearer token in the `Authorization` header. Always use Contracts (not legacy Plans) for new integrations.

## Integration routing

Building…
Recommended API
Details

Ingesting usage events
`POST /v1/ingest` (batch)
[Send usage events](https://docs.metronome.com/guides/events/send-usage-events.md), the [API quickstart](https://docs.metronome.com/guides/get-started/api-quickstart.md), the [Ingest API reference](https://docs.metronome.com/api-reference/usage/ingest-events.md), and [Set ingest aliases](https://docs.metronome.com/api-reference/customers/create-or-update-customer-ingest-aliases.md)

Defining what to measure
Billable Metrics API
[Create billable metrics](https://docs.metronome.com/guides/implement-metronome/core-concepts/create-billable-metrics.md)

Enterprise pricing agreements
Contracts + Rate Cards
[Provision a customer contract](https://docs.metronome.com/guides/implement-metronome/core-concepts/provision-contract.md), [Create and manage rate cards](https://docs.metronome.com/guides/implement-metronome/core-concepts/create-manage-rate-cards.md), and the [Create a contract](https://docs.metronome.com/api-reference/contracts/create-a-contract.md) and [Add rates](https://docs.metronome.com/api-reference/rate-cards/add-rates.md) API references

Mid-term contract changes
Contract Edits
[Edit a contract](https://docs.metronome.com/guides/pricing-packaging/make-pricing-changes/edit-contract.md), [Contract edits and overrides](https://docs.metronome.com/guides/pricing-packaging/make-pricing-changes/edit-or-override-a-contract.md), and [Manage contract lifecycle](https://docs.metronome.com/guides/customers-billing/manage-customers/manage-customer-lifecycle.md)

Invoice lifecycle and finalization
Invoices API
[How Metronome invoices work](https://docs.metronome.com/guides/implement-metronome/core-concepts/how-invoicing-works.md)

Prepaid or postpaid commitments and one-off top-ups
Commits + Credits
[Apply credits and commits to contracts](https://docs.metronome.com/guides/pricing-packaging/apply-credits-and-commits/create-a-pre-paid-commit.md) and [Payment-gated commits](https://docs.metronome.com/guides/pricing-packaging/apply-credits-and-commits/manual-payment-gated-commits.md)

Syncing invoices to Stripe
Stripe billing provider config
[Invoice with Stripe](https://docs.metronome.com/integrations/invoice-integrations/stripe.md)

Prepaid balances, auto-recharge, spend alerts, and thresholds
Notifications API
[Set prepaid balance thresholds](https://docs.metronome.com/guides/customers-billing/optimize-customer-experience/prepaid-balance-thresholds.md), [Enforce spend thresholds](https://docs.metronome.com/guides/customers-billing/optimize-customer-experience/set-customer-spend-control.md), and [Threshold notifications](https://docs.metronome.com/guides/pricing-packaging/apply-credits-and-commits/alerts.md)

Read the linked page before answering any integration question or writing code; the links return plain Markdown. If no row fits, use the [documentation index](https://docs.metronome.com/llms.txt) to find the right page, and append `.md` to the page URL to fetch it as Markdown.

## Operational workflows