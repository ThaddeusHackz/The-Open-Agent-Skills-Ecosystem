---
name: writing-style-learner
description: 帮助用户从提供的文档（需求文档、技术规范、会议纪要）中提取写作风格特征，并将其保存为可重用的风格指南。
---

# Style Learner

## When to Use

Use this skill when user wants to:
- Learn/improve writing style from provided documents
- Extract writing patterns from technical documents
- Build a personal or team writing guide

## Description

Helps users extract writing style characteristics from provided documents (requirements docs, technical specs, meeting notes) and save them as reusable style guides.

## Features

1. **Style Extraction** - Analyze documents and extract writing characteristics
2. **Batch Learning** - Learn from multiple documents and find common patterns
3. **Structured Output** - Generate standardized style records
4. **Memory Storage** - Save to MEMORY.md or specified location

## Usage

```
user: Learn this document's style https://xfmkp6q7le.feishu.cn/wiki/xxx -as "Oldtimer"

user: Learn these 3 docs as team style
https://xfmkp6q7le.feishu.cn/wiki/xxx
https://xfmkp6q7le.feishu.cn/wiki/yyy
https://xfmkp6q7le.feishu.cn/wiki/zzz
```

## Parameters

- `doc_url`: Feishu document link (single or multiple)
- `author_name`: Author name (optional)
- `doc_type`: Document type (requirements/technical/meeting/other)
- `mode`: single / batch / team

## Output Dimensions

Extracted style includes:
- Title hierarchy (# ## ### usage)
- Paragraph organization (Background → Solution → Todo)
- Code block preferences (cpp/json/python/plaintext)
- Table usage patterns
- Tone (casual vs formal)
- High-frequency vocabulary
- Layout habits (whitespace, lists)
- Collaboration elements (@mentions, references)
