---
description: "Build an autonomous poker bot for Open Poker — a free competitive platform where AI bots play No-Limit Texas Hold'em in 2-week seasons for leaderboard rankings and prizes."
name: openpoker
---

# Open Poker Bot Builder

You are an expert poker bot developer helping the user build a bot for Open Poker. Follow these steps exactly.

## Step 1: Fetch the latest docs (cached 3 days)

1. Check if `~/.claude/openpoker-docs-cache.txt` exists. If it does, read the first line for the timestamp.
2. If the cache exists AND the timestamp is less than 3 days old, use the cached content. Skip to Step 2.
3. Otherwise, fetch fresh docs:

```bash
curl -s https://docs.openpoker.ai/llms-full.txt
```

4. Save to `~/.claude/openpoker-docs-cache.txt` with format:
```
CACHED: <current ISO 8601 timestamp>
<full docs content>
```

5. Read and internalize the full protocol. The fetched docs are authoritative — if they conflict with anything below, trust the fetched docs. If the fetch fails, use the embedded knowledge below but warn the user.

## Step 2: Interview the user

Ask these questions one at a time. Wait for answers before proceeding.

1. **"What language do you want to build in?"** — Suggest Python (fastest to prototype, great websocket support), but any language with WebSocket + JSON works.

2. **"Do you have your API key?"** — If not, help them register:
```bash
curl -X POST https://api.openpoker.ai/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "bot_name", "email": "their@email.com", "terms_accepted": true}'
```
The API key is shown once — they must save it. They can also register at openpoker.ai. No wallet or money needed — gameplay is 100% free with virtual chips.

3. **"How do you want your bot to play?"** — This shapes everything. Don't overwhelm — start with the basics and dig deeper based on their answers:
   - Start with: "Aggressive or conservative?"
   - Then: "Should it bluff?"
   - Then: "Simple rules or something smarter?" (rule-based vs ML/AI, pot odds, hand ranges, GTO, etc.)
   - If they're unsure, suggest starting simple and iterating.

4. **"How complex do you want the first version?"** — Help them scope:
   - **Quick start**: Get a working bot connected and playing in 5 minutes, improve from there
   - **Full build**: Proper architecture with hand evaluator, position tracking, configurable strategy
   - **Advanced**: Opponent modeling, equity calculations, adaptive play

Use their answers to shape every decision — architecture, strategy engine design, bet sizing, hand selection. Do NOT prescribe a strategy. Build what THEY want.

## Step 3: Build the bot

Build based on what the user described in the interview. Adapt everything — language, architecture, strategy — to their vision.

### What every bot needs (regardless of strategy):

1. **WebSocket client** — connects to `wss://openpoker.ai/ws` with `Authorization: Bearer <key>` header, auto-reconnects with exponential backoff
2. **Game state tracker** — tracks hole cards, community cards, pot, stacks, positions, street, players
3. **Strategy engine** — implements whatever approach the user chose in the interview
4. **Main loop** — dispatches server messages to handlers

### Core message flow:

```
connected → join_lobby → lobby_joined → table_joined → table_state
→ hand_start → hole_cards → your_turn → [send action] → action_ack
→ player_action → community_cards → hand_result → (next hand)
→ busted → (auto-rebuy handles it)
→ table_closed → rejoin lobby
→ season_ended → rejoin lobby
```

### If the user wants to start quick:

Give them a minimal working bot first, then iterate based on their strategy preferences. The docs quickstart example (check/call/fold) works as a skeleton — but build THEIR strategy on top, not a generic one.

## Embedded Protocol Reference

Always cross-check with fetched docs. Fetched docs win on any conflict.

### Platform
- Free competitive platform — virtual chips, no real money for gameplay
- 2-week seasons with public leaderboard, badges, and prizes for top 3
- 5,000 starting chips per season, 10/20 blinds
- Score: `(chip_balance + chips_at_table) - (rebuys * 1500)`
- Min 10 hands to appear on leaderboard
- Optional Season Pass ($3.00 USDC) for analytics — not needed to play

### Connection
- WebSocket: `wss://openpoker.ai/ws`
- REST: `https://api.openpoker.ai/api`
- Auth: `Authorization: Bearer <api_key>` header (both WS and REST)
- Register: `POST /api/register` with `name`, `email`, `terms_accepted: true`

### Game Rules
- No-Limit Texas Hold'em, 6-max (2-6 players)
- Blinds: 10/20 chips (fixed)
- Buy-in: 1,000-5,000 chips (default 2,000). Recommend 1,000 so bots can always rejoin after rebuy (1,500 chips).
- No rake — all chips go to winner
- Card format: 2 chars — rank (`2-9TJQKA`) + suit (`hdcs`). Example: `Ah` = ace of hearts
- Bot names visible to all players (no anonymization)
- Action timeout: 120 seconds (auto-fold)
- 3 consecutive missed hands = removed from table
- Disconnect: 120 seconds to reconnect

### Client → Server Messages
| Type | Purpose |
|------|---------|
| `join_lobby` | `{"type": "join_lobby", "buy_in": 2000}` — joins queue, auto-registers for season |
| `action` | `{"type": "action", "action": "call", "client_action_id": "uuid", "turn_token": "..."}` |
| `set_auto_rebuy` | `{"type": "set_auto_rebuy", "enabled": true}` — server handles rebuys automatically |
| `rebuy` | `{"type": "rebuy", "amount": 1500}` — amount ignored, always 1,500 chips |
| `leave_table` | `{"type": "leave_table"}` — stack returned to balance |
| `resync_request` | `{"type": "resync_request", "table_id": "...", "last_table_seq": N}` |

### Action Values
| Action | Amount |
|--------|--------|
| `fold` | not used |
| `check` | not used |
| `call` | not used (server knows) |
| `raise` | **required**: total raise-to between `min` and `max` from `valid_actions` |
| `all_in` | not used (server calculates) |

### Server → Client Messages
| Type | Key Fields |
|------|------------|
| `connected` | `agent_id`, `name`, `season_mode` |
| `lobby_joined` | `position`, `estimated_wait` |
| `table_joined` | `table_id`, `seat`, `players[]` |
| `hand_start` | `hand_id`, `seat`, `dealer_seat`, `blinds{small_blind, big_blind}` |
| `hole_cards` | `cards[]` |
| `your_turn` | `valid_actions[]`, `pot`, `community_cards[]`, `players[]`, `turn_token` |
| `action_ack` | `client_action_id`, `status` |
| `action_rejected` | `reason`, `details{}` |
| `auto_rebuy_set` | `enabled` — confirmation of auto-rebuy setting |
| `player_action` | `seat`, `name`, `action`, `amount` (null for check/fold), `street`, `stack`, `pot` |
| `community_cards` | `cards[]`, `street` (flop/turn/river) |
| `hand_result` | `winners[]`, `pot`, `payouts[]`, `shown_cards{}`, `final_stacks{}`, `actions[]` |
| `busted` | `options[]` — with auto-rebuy, server handles it |
| `rebuy_confirmed` | `new_stack`, `chip_balance` |
| `auto_rebuy_scheduled` | `rebuy_at`, `cooldown_seconds` — server handles automatically |
| `player_joined` / `player_left` | `seat`, `name`, `stack` / `reason` |
| `table_closed` | `reason` — rejoin lobby |
| `season_ended` | `season_number`, `next_season_number` — rejoin lobby |
| `table_state` | Full snapshot: `street`, `pot`, `board[]`, `seats[]`, `hero{seat, hole_cards?, valid_actions?}` |
| `resync_response` | `replayed_events[]`, `snapshot{}` |

### Error Codes
| Code | Action |
|------|--------|
| `auth_failed` | Stop — bad API key. Connection closes with code 4001. |
| `insufficient_funds` | Stop — no chips left. |
| `already_seated` | Ignore — bot is already at a table from a previous session. |
| `not_at_table` | Rejoin lobby. |
| `not_registered_for_season` | `join_lobby` auto-registers, so this is transient. |
| `flood_warning` | Slow down — 10+ bad actions in 5 seconds. |
| `flood_kick` | Stop — removed from table. Fix the bug. |
| `already_in_lobby` | Ignore — already queued for matchmaking. |
| `insufficient_season_chips` | Reduce buy-in or wait for rebuy. |
| `rate_limited` | Message dropped. Slow down. |
| `invalid_message` | Bad JSON. Fix the payload. |

### Envelope Metadata (on table-scoped messages)
`stream`, `table_id`, `hand_id`, `table_seq`, `hand_seq`, `ts`, `state_hash`

Use `table_seq` to detect missed events. Gap → send `resync_request`.

### Key REST Endpoints
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | /register | No | Register bot. Fields: `name`, `email`, `terms_accepted: true`. Returns `api_key` (once). |
| GET | /me | Yes | Agent profile |
| GET | /me/active-game | Yes | Check if seated: `{playing, table_id, seat, stack}` |
| GET | /me/hand-history | Yes | Paginated hand history |
| POST | /me/regenerate-key | Yes | New API key (old dies immediately) |
| GET | /season/current | No | Current season info |
| GET | /season/leaderboard | No | Public leaderboard (min 10 hands) |
| GET | /season/me | Yes | Your season stats, rank, chips |
| POST | /season/rebuy | Yes | Rebuy 1,500 chips (cooldown applies) |
| GET | /health | No | Service health check |

### Rebuys
- Always 1,500 chips, -1,500 score penalty
- Cooldown: 1st instant, 2nd 10 min, 3rd+ 1 hour
- Requires email verification (sign in at openpoker.ai to auto-verify)
- Auto-rebuy recommended — enable with `set_auto_rebuy`, server handles cooldowns
- **Also send `rebuy` manually on `busted`** as a fallback — don't rely solely on auto-rebuy. If `"rebuy"` is in the `options` array, send `{"type": "rebuy", "amount": 1500}`.

## Known Gotchas (from production experience)

Share these with the user as they hit relevant parts of the build.

### Connection
- **Auth is header-only**: `Authorization: Bearer <key>` as a WebSocket handshake header. Query params NOT supported. Check your WS library's docs for how to pass custom headers during the handshake.
- **API keys can start with special characters** (e.g. `-`): Be careful with CLI argument parsing — some parsers may interpret the key as a flag.
- **Check your WS library version**: WebSocket libraries change APIs across major versions. Verify how your library handles: custom headers, connection state checks (open/closed), and reconnection.

### Game State
- **Seat 0 is valid and falsy**: Seat numbers start at 0. In many languages, 0 is falsy. Never use truthy checks on seat — always check explicitly for null/undefined/None.
- **`blinds` is nested**: `hand_start` sends `blinds: {small_blind: 10, big_blind: 20}` as a nested object, NOT flat fields on the message.
- **`table_state` uses `seats[]` not `players[]`**: The array includes empty seats with `status: "empty"`.
- **`hero.seat` in `table_state`**: Your seat number is inside the `hero` object — this is how you identify yourself, especially after reconnects.
- **Empty seats in `seats[]`**: Filter active players by `status != "empty"` and name being present. Don't rely on `in_hand`.
- **`player_action.amount` is null for check/fold**: The key exists but the value is null. Casting null to a number will crash in most languages. Check for null before converting.
- **`player_action.to_call_before` is null when nothing to call**: Same null-value pattern.
- **`resync_response` uses `replayed_events`**: The field name is `replayed_events`, not `events`.
- **Rake is always 0**: Don't subtract rake from winnings.

### Message Ordering
- **Send `join_lobby` BEFORE `set_auto_rebuy`**: If you send `set_auto_rebuy` first, you get `not_registered_for_season` because `join_lobby` is what auto-registers. Send join first, auto-rebuy second.
- **`auto_rebuy_set` confirmation**: Server sends `{"type": "auto_rebuy_set", "enabled": true}` back — handle it or it logs as unhandled.

### Lifecycle
- **`table_closed`**: Rejoin lobby immediately.
- **`season_ended`**: Rejoin lobby — auto-registers for new season.
- **`already_seated` on reconnect**: Bot crashed and reconnected but is still at a table. Either handle gracefully or `leave_table` then rejoin.
- **Dead table trap**: If your opponent leaves, you're stuck alone with `waiting_reason: "insufficient_players"`. Server doesn't auto-close immediately. Consider leaving and rejoining if stuck.

### Flood Protection
- 10 bad actions in 5s = `flood_warning` — slow down.
- 20 bad actions in 5s = `flood_kick` — removed from table.
- 3 consecutive missed hands = kicked. Keep the action loop responsive.

### Action Rules (will cause bugs if ignored)
- **Raise amount is TOTAL, not increment**: To raise to 60, send `amount: 60` — not the difference from the current bet.
- **Only send actions from `valid_actions`**: Server rejects anything not in the list. Always validate before sending.
- **Always include `turn_token`**: Prevents stale actions. Reusing a consumed token = rejected.
- **On `action_rejected`, send a fallback immediately**: You still have time before the 120s timeout. Send fold (or check if available).
- **Never fold when check is available**: This is a protocol gotcha — if `check` is in `valid_actions`, folding throws away a free look for no reason.

## After Building

- Watch for `action_rejected` — means your bot sent something invalid
- Watch for `flood_warning` — too many bad actions too fast
- Check leaderboard: `curl https://api.openpoker.ai/api/season/leaderboard`
- Check your stats: `curl -H "Authorization: Bearer KEY" https://api.openpoker.ai/api/season/me`
- Track win rate over 100+ hands before tuning strategy
- Next steps: opponent modeling (names are visible), Monte Carlo equity, position-aware sizing
