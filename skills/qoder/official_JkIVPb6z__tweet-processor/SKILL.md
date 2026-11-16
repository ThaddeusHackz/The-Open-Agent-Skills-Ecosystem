---
name: tweet-processor
description: 从推文链接中提取并分类见解，生成结构化笔记。当用户发送推文 URL 时，自动导航、提取关键信息（工具、技术、人物、心得），并按类别追加到指定目录的文件中。
---

# Tweet Processor Skill

Extract and categorize insights from tweet links into structured notes.

## Usage

When user sends a tweet URL, automatically:
1. Navigate to the tweet
2. Extract key insights (tools, tech, people, learnings)
3. Categorize into tweet-notes/ files
4. Append with proper formatting

## Input

- Tweet URL (any x.com or twitter.com link)

## Output

Appends to:
- `tweet-notes/tools.md` — Software, services, APIs discovered
- `tweet-notes/tech.md` — Development techniques, workflows
- `tweet-notes/design.md` — UI/UX insights
- `tweet-notes/people.md` — Accounts to follow
- `tweet-notes/misc.md` — Other valuable insights

## Format

```markdown
## [Brief Title]
**Date:** YYYY-MM-DD
**URL:** [tweet URL]
**Key takeaway:** [What matters]
**Why it matters:** [Brief context]

---
```

## Rules

- Be selective — only genuinely useful insights
- Skip fluff and noise
- One insight can go into multiple files if relevant
- Always include the source URL
- Use today's date
