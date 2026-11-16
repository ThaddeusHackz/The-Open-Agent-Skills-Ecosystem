---
name: shelly-competitor-analyzer
description: 在几分钟内分析任何公司的竞争地位。输入公司名称或 URL，即可生成一份结构化报告，涵盖其业务内容、定价策略、社交媒体影响力及最新动态。
---

# Competitor Analyzer

Analyze any company's competitive position in minutes. Takes a company name or URL and produces a structured report covering what they do, pricing, social presence, and recent news.

## Usage

```
./analyze.sh <company_name_or_url>
```

### Example
```
./analyze.sh "Notion"
./analyze.sh "https://linear.app"
```

## Output

A structured competitive analysis report with:
- **Company Overview** — What they do, market position
- **Pricing Analysis** — Plans, tiers, free tier details
- **Social Presence** — Twitter, LinkedIn, GitHub activity
- **Recent News** — Latest announcements, funding, launches
- **Strengths & Weaknesses** — Quick SWOT-lite summary

## Requirements

- `curl` (standard)
- Internet access for web searches
- Works best when run by an AI agent with `web_search` tool access

## How It Works

The script uses web search queries to gather intel, then formats results into a clean markdown report. When run by an OpenClaw agent, it leverages the `web_search` tool for richer results. Standalone mode uses curl + DuckDuckGo.
