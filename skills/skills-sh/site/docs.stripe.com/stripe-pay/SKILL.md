---
name: stripe-pay
description: Install the stripe-pay skill for your AI agent. Published on docs.stripe.com.
source: https://www.skills.sh/site/docs.stripe.com/stripe-pay
---

# stripe pay

Use `stripe pay` to send money from the authenticated Stripe business to another Stripe business identified by a [Stripe Profile](https://docs.stripe.com/get-started/account/profile.md) handle, for example `@recipient`.

For the financial-account transfer workflow documented here, both the sender and the receiving business must have a [Stripe Profile](https://docs.stripe.com/get-started/account/profile.md). In addition:

- The sender needs a funded [financial account](https://docs.stripe.com/money-management.md).

- The receiver needs an eligible transfer destination linked to their [Stripe Profile](https://docs.stripe.com/get-started/account/profile.md).

If the user needs details about financial accounts, read [Money Management](https://docs.stripe.com/money-management.md). In this workflow, the command resolves the recipient’s payout configuration, which can route the payout to an attached financial account or linked bank account, and reports the fee and delivery timing before confirmation. Don’t assume that a transfer is free or instant.

Eligible transfers take priority. If the sender has no eligible financial account or the recipient has no eligible transfer destination, `stripe pay` offers the recipient’s configured payment link, if available. Insufficient funds and currency errors alone don’t trigger this fallback.

For `status: payment_link_available` and `transfer_sent: false`, give the user `payment_link_url` to complete payment in Checkout, where they must enter the amount and check the currency. Transfer arguments don’t carry over. Don’t report payment success from returning or opening the URL, or rerun with `--yes` to pay the link.

## Safety Rules