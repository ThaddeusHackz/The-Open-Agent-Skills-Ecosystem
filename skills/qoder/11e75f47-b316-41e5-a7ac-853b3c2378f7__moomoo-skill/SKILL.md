---
name: moomoo-skill
description: Set up and troubleshoot the official Moomoo Global Skills in Qoder for market quotes, market news, sentiment, unusual activity, and paper or live trading.
---

# Moomoo Global Skills

Use the [Moomoo Skills Hub](https://www.moomoo.com/skillhub) and its [official setup guide](https://github.com/MoomooOpen/moomoo-agent-hub/blob/main/docs/moomoo-install.md). Install and authorize tools in the environment that will run them. A cloud agent has its own tools and credentials, separate from the local Qoder client.

## Install in Qoder

1. If the user requests installation, use Node.js 18 or later and run the following command for Qoder. Omit `-g` for a project-only installation. Open a fresh Qoder session afterward so it can discover the new Skills.

   ```bash
   npx skills add MoomooOpen/moomoo-agent-hub#ec092d2b4c21868ae285f65d9b30f7adb44f860e -a qoder -s '*' -g -y
   ```

2. For quotes, trading, or unusual activity, check `moomoo version`. If the command is missing, use the installer for the current operating system from the [official Moomoo CLI repository](https://github.com/MoomooOpen/moomoo-cli#installation). Use the `moomoo` executable and the Global API at `https://webapi.moomoo.com`. For cloud or other headless environments, use the repository's headless sign-in instructions. The user completes OAuth in the browser. Keep tokens and callback URLs out of chat, logs, and shared files.

3. If upgrading from OpenD or the old Python Skills, select the new Skills below and disable the legacy Skills for this agent to avoid ambiguous routing. See the [official migration guide](https://github.com/MoomooOpen/moomoo-agent-hub/blob/main/docs/upgrade-from-opend.md). For `ModuleNotFoundError: No module named 'futu'` in an old anomaly Skill, switch to the matching `moomoo-unusual-*` Skill and check `moomoo unusual --help`.

   If the installed Unusual Skill cannot find its shared CLI runtime guide, use the [guide from the pinned upstream revision](https://github.com/MoomooOpen/moomoo-agent-hub/blob/ec092d2b4c21868ae285f65d9b30f7adb44f860e/skills/unusual-skills/references/cli-runtime.md).

## Choose a Skill

| Task | Official Skill |
| --- | --- |
| Quotes, candlesticks, and market data | `moomoo-quote` |
| News, stock briefings, and community sentiment | `moomoo-news-search`, `moomoo-stock-digest`, `moomoo-comment-sentiment` |
| Technical signals, capital flows, and derivatives activity | `moomoo-unusual-technical-signal-alerts`, `moomoo-unusual-capital-flows`, `moomoo-unusual-derivatives-activity` |
| Paper trading and paper accounts | `moomoo-sim-trading` |
| Live securities trading, crypto, or grid strategies | `moomoo-trading`, `moomoo-crypto`, `moomoo-grid-strategy` |

Read and follow the selected official Skill for the requested operation. Use the paper account for competition practice or setup validation. Live orders require explicit user intent and confirmation for the order details.

## Verify setup

Run `moomoo auth status --format json` and `moomoo check --format json` locally in the execution environment. Check that `moomoo config get api_base` resolves to `https://webapi.moomoo.com`. With a signed-in account, run a read-only quote query such as `moomoo quote US.AAPL --format json`. Use `moomoo unusual --help` to verify the installed CLI exposes the Unusual commands. For a reported empty sentiment result, report that the requested symbol returned no results. For errors, report the specific failing step.
