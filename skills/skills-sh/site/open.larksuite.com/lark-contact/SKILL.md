---
name: lark-contact
description: Install the lark-contact skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-contact
---

## 选哪个命令

user 身份和 bot 身份是两条完全独立的路径。先确定当前身份,再按下表选命令:

想做什么
user 身份
bot 身份

按姓名 / 邮箱搜员工拿 open_id
[`+search-user`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-contact-search-user.md)
不支持

按关键词搜索当前用户可见的机器人 / 智能体
[`+search-bot`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-contact-search-bot.md)
不支持

已知 open_id 取他人资料
`+search-user --user-ids <id>`
[`+get-user --user-id <id>`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-contact-get-user.md)

查看自己
`+get-user` 或 `+search-user --user-ids me`
不支持

查同事的个人状态 / 签名
`user_profiles batch_query`
不支持

已知 open_id 只是想发消息 / 排日程,不必经过 contact —— 直接 [`lark-im`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-im/SKILL.md) / [`lark-calendar`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-calendar/SKILL.md)。

### 名字没说清是人还是机器人 / 智能体

用户给的名字常常不表明类型。例如「和 reviewDuck 约个会」里的 reviewDuck 可能是同事昵称,也可能是机器人。

- 名字含 bot / agent / AI / 助手 / 机器人 / 智能体 / assistant 等明显特征时,反过来先搜机器人更快

- 不确定的话两边都搜一下