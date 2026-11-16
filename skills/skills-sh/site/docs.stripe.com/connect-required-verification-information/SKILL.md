---
name: connect-required-verification-information
description: Install the connect-required-verification-information skill for your AI agent. Published on docs.stripe.com.
source: https://www.skills.sh/site/docs.stripe.com/connect-required-verification-information
---

## Instructions

The human-accessible version of this documentation allows the user to select connected account fields and regions using a form, and then makes API requests to fetch and display the requirements a connected account with the selected configuration and region must provide. Follow these instructions to fetch the same information.

### Interaction contract

Terminology used in this document:

- `field`: a setup input such as `platformCountry`, `accountCountry`, or `capabilities`

- `option`: a presented selectable option for a field

- `value`: the option the user selects, or the free-response value the user provides for a field

Every time you ask the user to provide a value for a field:

- use a multiple-choice question; never stop at a plain free-form prompt or wait for raw chat input

- if you need free user input, instruct the user to use the question’s free-response field

- for long option lists, explicitly say that any value from the full validated list is still accepted through the free-response field

- if the user already provided a valid answer in an earlier message, use that instead of asking again