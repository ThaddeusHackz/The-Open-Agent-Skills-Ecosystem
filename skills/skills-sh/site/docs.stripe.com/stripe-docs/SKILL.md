---
name: stripe-docs
description: Install the stripe-docs skill for your AI agent. Published on docs.stripe.com.
source: https://www.skills.sh/site/docs.stripe.com/stripe-docs
---

Use `stripe docs` instead of fetching [docs.stripe.com](https://docs.stripe.com/.md) content directly with `curl` or `WebFetch`. If you don’t have the CLI installed, [install the Stripe CLI](https://docs.stripe.com/cli/install).

Always use the latest CLI version. If the current CLI version is less than v1.50.9, you must [upgrade](https://docs.stripe.com/cli/install) to access gated documentation.

- Fetches Markdown automatically

- Fetches gated documentation. Users must log in using `stripe login` to access gated documentation.

- Purpose-built for agents and terminal workflows

## Read a page by its web path

```
stripe docs /payments
```

## Search documentation by keyword

```
stripe docs search "payment intents"
```