---
name: model-guard
description: 自动监控反重力模型的配额，并在配额不足时切换至剩余配额最高的模型或回退到原生 gemini-flash 模型。
---

# Model Guard

Automatically monitors Anti-Gravity model quotas and switches the default model to the one with the highest remaining quota. If all Anti-Gravity models are below 20%, it falls back to the native `gemini-flash` model.

## Usage

- **Manual trigger**: `model-guard`
- **Auto trigger**: Designed to be run via `cron` or `heartbeat`.

## Configuration

Edit `guard.js` to change the `THRESHOLD` (default 20%) or `FALLBACK_MODEL`.
