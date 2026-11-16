---
name: oee-ai-cost-tracker
description: 一款用于追踪 AI API 调用、生成支出报告并提供路由建议以降低成本的工具，支持日志记录、多维度报表分析及命令行使用。
---

# 🐾 AI Cost Tracker — Know What You Spend

> by Odin's Eye Enterprises — Ancient Wisdom. Modern Intelligence.

Track every AI API call, generate spend reports, and get routing suggestions to cut costs.

## What It Does

1. **Logs** every API call with model, tokens, cost to JSONL
2. **Reports** spending by model, time period, and use case
3. **Suggests** cheaper model routing based on task complexity

## Trigger Phrases

- "how much have I spent on AI"
- "AI cost report"
- "track this API call"
- "show AI spending"
- "cost breakdown"

## Usage

### Logging (in your code)
```python
from tracker import log_usage
log_usage(model="claude-3-haiku", input_tokens=500, output_tokens=200, task="humanize")
```

### Reports
```bash
# Full spend report
python report.py

# Last 7 days
python report.py --days 7

# By model
python report.py --by-model
```

## Files

- `tracker.py` — logging library, import into your tools
- `report.py` — CLI dashboard for spend analysis
- `pricing.json` — model pricing data (update as needed)

## Requirements

- Python 3.10+ (stdlib only)
- No API keys needed (this tracks YOUR usage)

## For Agents

To check spending: `python report.py`
To log usage from other tools: `from tracker import log_usage`

<!-- 🐾 Odin's ravens count every coin -->
