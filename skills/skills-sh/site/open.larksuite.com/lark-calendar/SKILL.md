---
name: lark-calendar
description: Install the lark-calendar skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-calendar
---

# calendar (v4)

开始前先读 [`../lark-shared/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md)（认证、权限处理）。

CRITICAL — 凡涉及预约日程/会议室、调整时间或查询/搜索会议室，第一步 MUST 读 [`references/lark-calendar-schedule-meeting.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-calendar-schedule-meeting.md)。仅编辑字段（改标题/描述）或增删参会人（不涉及时间和会议室）时可跳过，直接读 [`references/lark-calendar-update.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-calendar-update.md)。

## 身份

按日程归属选身份：

- 查看/管理登录用户本人的日程 → `--as user`（默认，绝大多数场景）。

- 查看/管理 bot 自己创建/拥有的日程 → `--as bot`

对话人称映射：「我」= 登录用户，「你」= 应用（bot）；作为字段取值的人称（参会人、会议 owner 等）不参与身份判定，如「你创建日程，邀请我、会议 owner 为我」→ `--as bot` 创建，登录用户仅作参会人与会议 owner。