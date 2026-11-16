---
name: ai-news-workflow
description: 本技能收集人工智能行业新闻（RSS + 网页），进行过滤、去重和分类，可选通过豆包（火山引擎 Ark）生成中文标题及约 80 字的摘要（推荐 60-100 字，硬上限约 110 字），并导出 Excel 表格和 Word 简报。
---

# AI News Workflow

This skill collects AI industry news (RSS + web pages), filters/deduplicates/classifies them, optionally generates Chinese titles & ~80-char summaries(recommended 60-100,hard cap ~110) via Doubao (Volcengine Ark), and exports Excel tables + a Word briefing.

## How to run
- Entry: `skill_entry.py`
- Init (optional): `python skill_entry.py --init`
- Run: `python skill_entry.py`

## Inputs
Put these files under `./input/`:
- 企业名单.xlsx
- source_config.xlsx
- web_source_config.xlsx (optional)

## Outputs
Generated under `./output/`:
- Excel: `./output/excel/`
- Word: `./output/word/`

## Optional: Ark API
Provide API key via environment variable:
- `ARK_API_KEY`

Model can be selected at runtime:
- `python skill_entry.py --model <MODEL_NAME>`