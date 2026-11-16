---
name: book-summary
description: 生成播客风格的书籍摘要。将书籍内容转化为包含核心观点和可操作要点的引人入胜的音频脚本。
---

# book-summary

Generate podcast-style summaries of books. Convert book content into engaging audio scripts with key ideas and actionable takeaways.

## What it does

- Generate podcast-style scripts from book summaries
- Extract 3 key ideas with narratives
- Create actionable takeaways
- Estimate podcast duration
- Format as single-narrator audio script

## Installation

```bash
clawhub install book-summary
```

## Usage

```javascript
const BookSummarySkill = require('book-summary');
const skill = new BookSummarySkill();

const result = skill.generatePodcastSummary({
  title: 'Atomic Habits',
  author: 'James Clear',
  summary: 'Small changes compound into big results...'
});
```

## Output

Podcast script with:
- Hook (opening)
- Intro (context)
- 3 Key Ideas (with takeaways)
- Synthesis (connection)
- Call to Action

## License

MIT
