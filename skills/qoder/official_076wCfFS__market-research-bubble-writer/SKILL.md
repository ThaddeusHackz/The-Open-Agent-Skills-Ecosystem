---
name: market-research-bubble-writer
description: "Three-phase market bubble pipeline — scrape → write → insert. In Claude Code dev mode (has Bash + Web tools): runs all three phases via CLI scripts. In engine prod mode (tool-less Sonnet sub-call): runs only the write phase against pre-scraped article text passed in the user message."
version: 1.0.1
---

# Market Research Bubble Writer

You are responsible for producing market event bubble cards. The pipeline has three distinct phases:

1. **Scrape** — gather article text
2. **Write** — produce JSON bubbles from that text
3. **Insert** — persist the bubbles to the engine's SQLite DB

How you execute each phase depends on the runtime:

| Phase             | Claude Code (dev)                                                                                    | Engine prod (Sonnet sub-call)                         |
| ----------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Scrape            | Run `pnpm --silent --filter engine scrape:dev`; fall back to WebSearch + WebFetch if it returns `[]` | Skip — articles arrive in your user message           |
| Write             | Apply the rules below to produce bubble JSON yourself                                                | Apply the rules below to produce bubble JSON yourself |
| Insert            | Run `pnpm --filter engine bubbles:insert <file>`                                                     | Skip — engine inserts your output                     |
| 4. Context update | Skipped — invoke locally via the prod endpoint if needed                                             | Auto after Phase 3 if `inserted >= 1`                 |

The write rules are identical in both runtimes. Only the I/O differs.

---

## Phase 1 — Scrape

### Dev mode (have Bash, WebSearch, WebFetch)

1. Run `pnpm --silent --filter engine scrape:dev > /tmp/market-articles.json` via Bash. (`--silent` suppresses pnpm's own task-header lines from stdout, keeping the file pure JSON.)
2. If the file is non-empty and contains a non-empty JSON array, use it as input to Phase 2.
3. If the script errors or prints `[]`, fall back to **WebSearch + WebFetch** — run 15–20 queries across the categories below, then WebFetch the 2–3 highest-signal articles in full. Build an in-memory equivalent of the scraper output (one record per article with `url`, `title`, `publishedAt`, `body`).

   **DeFi and Base ecosystem**
   - `"DeFi news" site:thedefiant.io`
   - `"Base chain" OR "Base ecosystem" news today`
   - `"crypto" site:dlnews.com`
   - `"DeFi protocol" TVL OR launch OR exploit today`
   - `"Aerodrome" OR "Aave" OR "Uniswap" latest`

   **Regulatory and governance**
   - `crypto governance OR regulatory today`
   - `"tokenized" OR "RWA" OR "onchain" site:cointelegraph.com`

   **Macro and geopolitical**
   - `"Federal Reserve" OR "interest rates" OR "credit event" crypto DeFi impact`
   - `geopolitical OR sanctions OR conflict crypto market today`

   **TradFi and RWA**
   - `"Treasury yield" OR "10-year yield" OR "credit spreads" today site:ft.com OR site:wsj.com`
   - `"Ondo" OR "BUIDL" OR "Superstate" OR "Pendle" OR "OpenEden" tokenized today`
   - `"tokenized treasuries" OR "tokenized money market" OR "RWA yield" today`
   - `"S&P 500" OR "Nasdaq" OR "VIX" risk today`

   **AI and tech macro**
   - `"AI" "capex" OR "data center" OR "energy" site:ft.com OR site:wsj.com`
   - `"AI bubble" OR "AI valuation" OR "AI earnings" today`
   - `"AI agents" crypto OR DeFi OR "on-chain"`

4. If neither source yields any text, stop the entire pipeline — do not produce bubbles, do not call insert.

### Prod mode (no tools)

The user message contains pre-scraped article text. Use it as input to Phase 2. There is no Phase 1 work to do.

---

## Phase 2 — Write bubbles

### Select events

Identify every distinct event in the input that meets the priority criteria below. No upper cap — emit one bubble per genuine event. Skip duplicates and stories that don't match any priority category. Priority order:

1. Exploits, hacks, oracle failures, depegs — signal strength depends on phase; see Signal Strength Rules
2. Liquidity crises, leverage unwinds, counterparty failures — always `signalStrength: "high"`
3. Macro / geopolitical events with confirmed DeFi liquidity or collateral transmission — same urgency as exploits
4. AI macro events — major earnings results (Nvidia, Microsoft, Google, Meta), capex announcements or reversals, bubble-burst signals (valuation resets, funding freezes, large layoffs), AI regulatory interventions, AI-native crypto or RWA products with material on-chain presence. Skip: product launches, open letters, internal company drama, opinion pieces.
5. Major TVL shifts (>10% in 7 days on a notable protocol)
6. New protocol or market launches on Base
7. Significant wallet activity (large position opens/closes by a whale or treasury)
8. Governance decisions with material protocol impact
9. Volume spikes (>2× 7-day average on a pair or protocol)
10. Regulatory actions or rulings with DeFi exposure

Discard events older than 48 hours unless still actively developing.

### Write each card

**Headline** — 10–15 words, prefer the lower end. Human voice. Curiosity or mild urgency. No action directives ("buy", "sell", "you should"). No clickbait — the headline must be accurate.

**Description** — 2–4 sentences. Expand the headline with the _so what_: scale, context, implication. Persuasive and charged. Still no action directives. Include a specific number or data point where available.

**Metadata** — used by the read path to match bubbles against user portfolios. Be precise.

- `tickers`: token symbols directly involved in the event. Canonical symbols only (`ETH`, `USDC`, `OP`). Use `[]` only when the event is genuinely token-agnostic (e.g. a broad regulatory ruling, a macro shock with no specific asset). Do not use `[]` as a fallback when unsure — if the article names tokens, list them. A `[]` here means the bubble reaches every user regardless of their holdings.
- `protocols`: protocol names directly involved. Canonical names only (`Aave`, `Aerodrome`, `Uniswap`, `Lido`, `Curve`, `Compound`, `Pendle`, ...). Same rule as tickers: use `[]` only when the event has no specific protocol affiliation, not as a default. A `[]` here means the bubble reaches every user regardless of which protocols they use.
- `positionTypes`: which position types this bubble applies to. Allowed values: `"token"`, `"rwa"`, `"lending"`, `"lp"`. Default to `[]` — most events affect all position types equally. Restrict only when the bubble is genuinely scoped to a specific position kind (e.g. an LP-only impermanent-loss event → `["lp"]`; an RWA yield update → `["rwa"]`; a borrow-rate change → `["lending"]`). Do not restrict simply because a ticker or protocol appears — use `[]` when in doubt.
- `chains`: chain names involved. Allowed values: `Ethereum`, `Base`, `Arbitrum`, `Optimism`, `Polygon`, `Avalanche`, `BNB`, `Scroll`, `zkSync`, `Linea`. Use empty array if unclear. Names outside this list will be dropped by the engine — do not invent new ones.
- `eventType`: one of `tvl_shift | wallet_activity | new_launch | volume_spike | governance | price_move | exploit | depeg | oracle_issue | liquidity_crisis | leverage_unwind | counterparty_failure | macro | geopolitical | regulatory`
- `signalStrength`: `high | medium | low` — see Signal Strength Rules below
- `sentiment`: `bullish | bearish | neutral`
- `sourceUrl`: canonical URL of the source article. If a story has no clear source URL, drop the card.
- `publishedAt`: ISO 8601 timestamp from the source. If unavailable, use the current timestamp.

Do not include an `id` field — the engine generates UUIDs server-side.

### Bubble shape (example)

```json
{
  "headline": "Aave V3 sees $200M USDC outflow as Base lending rates compress",
  "description": "Lender deposits on Aave V3's Base market dropped 18% over 24 hours after rates fell below sUSDe yields. The flow appears to be discretionary capital seeking higher fixed yield, not a credit event. Outstanding borrows are unchanged.",
  "sourceUrl": "https://thedefiant.io/...",
  "tickers": ["USDC"],
  "protocols": ["Aave"],
  "positionTypes": ["lending"],
  "chains": ["Base"],
  "eventType": "tvl_shift",
  "signalStrength": "medium",
  "sentiment": "neutral",
  "publishedAt": "2026-04-26T08:30:00Z"
}
```

### Output

**Dev mode**: write the JSON array to `/tmp/market-bubbles.json` via the Write tool. No fenced block — just the JSON file.

**Prod mode**: return a single JSON array inside one ```json fenced block. No preamble, no explanation, no second block. The engine's parser strips the fence and inserts the array.

---

## Phase 3 — Insert (dev mode only)

After Phase 2 has written `/tmp/market-bubbles.json`:

```bash
pnpm --filter engine bubbles:insert /tmp/market-bubbles.json
```

The script prints `{ "attempted": N, "inserted": N, "ignored": N }`. Report those counts back to the user.

In prod mode there is no Phase 3 — the engine handles insertion after parsing your output.

---

## Phase 4 — Context update

After Phase 3 inserts at least one bubble, the engine invokes you a second time to roll the newly inserted bubbles into a long-arc macro context file (`engine/src/agent/memory/market-research/market-context.md`). This phase is signalled by a `---PHASE 4: CONTEXT UPDATE---` prefix in the user message, followed by the current `market-context.md` content and a `---NEWLY INSERTED BUBBLES---` block containing the bubble JSON.

Phase 4 does not run in dev mode via this skill — invoke the prod endpoint locally if you need to exercise it.

### Sectors

The context file has six fixed top-level sections in this exact order. Never reorder, rename, merge, or invent new sectors.

| Section heading                | Scope                                                                  |
| ------------------------------ | ---------------------------------------------------------------------- |
| `## Crypto / Digital Assets`   | BTC, ETH, altcoins, DeFi protocols, on-chain volumes                   |
| `## RWA / Tokenization`        | Tokenised real-world assets, T-bills on-chain, institutional DeFi      |
| `## Macro / Rates`             | Fed policy, inflation, rate environment, USD strength                  |
| `## Geopolitics / Energy`      | Wars, sanctions, oil/gas, commodity shocks                             |
| `## Equities / Risk Sentiment` | S&P, Nasdaq, VIX, AI capex cycle and bubble dynamics, risk-on/off mode |
| `## Regulation / Policy`       | MiCA, SEC actions, global crypto regulation, policy shifts             |

A sector with no active narrative carries a single `(no active themes)` line as its body.

### Theme unit

The unit per sector is an **active theme** — a long-arc narrative (e.g. "Middle East conflict", "AI capex bubble", "Fed cutting cycle", "MiCA enforcement phase"), not a dated event entry. Each theme has:

- **Title** — short noun phrase, used as the `###` heading
- **`_Last updated: YYYY-MM-DD_`** — mandatory, on the line immediately following the `###` heading; refreshed every time the theme is amended or re-affirmed
- **Body** — structured bullets in this exact order:
  - `- **Facts:**` — concrete data points (numbers, dates, named entities) describing current state. One paragraph or short list.
  - `- **Structural:**` — _optional_ — longer-arc shifts (multi-month patterns, regime changes, cumulative institutional moves). Omit when the theme has no structural layer beyond its facts.
  - `- **So what:**` — one or two sentences naming the actionable interpretation. This line is lifted verbatim by downstream agents — it must stand alone and be decision-relevant.
- Total length ≤ ~120 words per theme. Body describes _current state_, not a changelog.

Themes persist as long as they remain macro-relevant (often months) and get amended over time.

#### Theme example

```markdown
### BTC ETF flows reaccelerating

_Last updated: 2026-04-30_

- **Facts:** US spot BTC ETFs +$2.1B over 8 days through Apr 23 → $58B cumulative / $102B AUM. IBIT $61B. BTC $77–78k, -25% YTD. Apr 29 reversal: $89.68M single-day outflow.
- **Structural:** T. Rowe TKNZ imminent (first active multi-asset spot crypto ETF). AIMCo $219M MSTR purchase Apr 30 — first sovereign-pension BTC-linked allocation.
- **So what:** Institutional absorption thesis intact through drawdown. Sovereign pension via MSTR is now a pattern, not an outlier.
```

### Update verbs

Before deciding to update, consult `references/materiality-checklist.md` (delivered in your system prompt alongside this skill). If the newly inserted bubbles do not meet any criterion, return the sentinel — see Output contract.

When the bubbles are material, you have exactly three allowed verbs:

1. **Extend** — amend an existing theme's body to incorporate the new material info; bump `_Last updated_` to today's date.
2. **Open** — add a new theme under the appropriate sector with today's date.
3. **Propose closure** — for any theme whose `_Last updated_` is > 60 days old, either:
   - **Refresh** — bump `_Last updated_` to today and add one short note ("still ongoing, no material change") if the theme is still genuinely active, OR
   - **Propose archive** — append a `_Closure proposed: YYYY-MM-DD — reason: …_` line directly below `_Last updated_`. The theme stays in the file for human review.

### Hard prohibitions

- Never delete a theme.
- Never move a theme to the archive file — archive moves are a manual human step.
- Never reorder, rename, or merge the six sector headings.
- Never invent a new sector heading.
- Never write raw JSON into the context file — output is markdown only.
- Never reference a specific user's portfolio or holdings — content is identical for every reader.

### Output contract

Return **exactly one** of the following, with no preamble, commentary, or extra text:

1. The literal string `NO_UPDATE` (and nothing else) when the newly inserted bubbles do not meet the materiality checklist.
2. The **full updated `market-context.md` file** as markdown — all six sectors preserved in order, every theme's `_Last updated: YYYY-MM-DD_` line present and immediately following its `###` heading, every theme body conforming to the **Facts / Structural? / So what** bullet structure. No top-level `_Last updated:_` line — each theme self-dates.

Do not output a partial diff. Do not wrap your output in a code fence — the engine strips fences defensively, but a clean unfenced markdown file is preferred.

---

## Writing rules

- Every headline and description must be accurate to the source. Do not embellish facts.
- Persuasion comes from juxtaposition, scale, and specificity — not from urgency language ("act now", "don't miss").
- Never reference any user's portfolio or holdings. Content must be identical for every reader.
- Source attribution is required. No URL → no card.

---

## Signal Strength Rules

| eventType              | `high`                                                                                              | `medium`                                            | `low`                                                                       |
| ---------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------- |
| `exploit`              | Active, uncontained drain with funds still at risk                                                  | Exploit contained, recovery underway                | Post-incident coordination, governance response, or funds already recovered |
| `depeg`                | >1% deviation from peg on a major stablecoin or LST                                                 | Minor deviation, recovering                         | Noise / brief                                                               |
| `oracle_issue`         | Actively exploited or causing wrong on-chain pricing                                                | Degraded / lagging, not yet exploited               | Monitoring alert only                                                       |
| `liquidity_crisis`     | Confirmed run on lending market or AMM, withdrawals paused or LP exit cascade                       | Elevated but contained outflows                     | Routine rebalancing                                                         |
| `leverage_unwind`      | Cross-margin cascade or large liquidation chain across protocols                                    | Single-protocol forced unwind                       | Isolated liquidations                                                       |
| `counterparty_failure` | Confirmed insolvency, bankruptcy filing, or asset freeze                                            | Solvency concerns flagged, not confirmed            | Rumor / unverified                                                          |
| `macro`                | Fed decision, rate move, or liquidity event with direct DeFi collateral or stablecoin supply impact | Indirect macro signal (inflation print, employment) | Background noise                                                            |
| `geopolitical`         | Active conflict or sanctions with commodity/inflation chain reaching crypto                         | Escalation risk flagged, chain not yet confirmed    | Political noise without clear DeFi transmission                             |
| `governance`           | Vote materially changes protocol economics, fee model, or security posture                          | Parameter update with moderate impact               | Proposal only, no vote yet                                                  |
| `tvl_shift`            | >10% on a notable protocol in 7 days                                                                | 5–10%                                               | <5%                                                                         |
| `volume_spike`         | >2× 7-day average                                                                                   | 1.5–2×                                              | <1.5×                                                                       |
| `wallet_activity`      | Large open/close by a known whale or protocol treasury                                              | Notable but not outsized                            | Routine                                                                     |
| `new_launch`           | Major protocol or Base-native launch with significant capital commitment                            | Testnet / early access                              | Announcement only                                                           |
| `price_move`           | >20% in 24h on a mid/large cap                                                                      | 10–20%                                              | <10%                                                                        |
| `regulatory`           | Enforcement action, ban, or binding ruling                                                          | Proposed rule / consultation                        | Commentary                                                                  |

`macro` and `geopolitical` with confirmed DeFi transmission are treated with the same urgency as `exploit`. Cluster signals (e.g. macro shock + `leverage_unwind` + `liquidity_crisis` on the same day) are always `high`.

---

## RWA Futureproofing

> Not yet implemented. No action required. Documenting forward-looking changes so the schema and skill can evolve in lockstep.

When RWA coverage is added:

- Expand sourcing to include Ondo Finance, BlackRock BUIDL, Superstate, OpenEden, Backed Finance, RWA.xyz.
- Add event types: `rwa_launch | rwa_yield_update | rwa_tvl_shift | rwa_redemption_event | rwa_issuer_update`
- Add `assetClass` field: `token | rwa | stablecoin | other`. Current cards default to `token`.
- Add `issuer` field for RWA cards — issuers (Ondo, BlackRock, Superstate) are not interchangeable; the matcher needs issuer, not just ticker.
- RWA assets use their canonical on-chain ticker (`OUSG`, `USDY`, `BUIDL`) in `tickers`.
