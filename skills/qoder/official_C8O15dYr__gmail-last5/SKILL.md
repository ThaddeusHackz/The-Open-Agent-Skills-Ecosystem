---
name: gmail_last5
summary: "Show the last 5 unique emails in the inbox using gog"
command: gmail_last5
command-dispatch: model
description: 使用 gog 工具搜索并显示收件箱中最后 5 封唯一邮件的列表，包含发件人、主题和日期信息。
---

# gmail_last5

When the user runs `/skill gmail_last5`, do this:

1) Run a `gog gmail search` for the inbox, max 5 newest.
2) Parse the JSON results.
3) Reply with a concise list: sender + subject + date (if present).

Use this command (account may be omitted if default is configured; prefer explicit):

```bash
gog gmail search "in:inbox" --max 5 --json --results-only --account william.kettle@neuralshift.co.uk
```

If the command fails, ask the user to confirm which Gmail account is authenticated in gog.
