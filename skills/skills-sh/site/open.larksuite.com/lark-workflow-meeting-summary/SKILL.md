---
name: lark-workflow-meeting-summary
description: Install the lark-workflow-meeting-summary skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-workflow-meeting-summary
---

# 会议纪要汇总工作流

CRITICAL — 开始前 MUST 先完整读取 [`../lark-shared/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md) 和 [`../lark-meeting/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-meeting/SKILL.md)。认证、身份和权限以 lark-shared 为准；会议与产物关系、产物选择和逐字稿路由以 lark-meeting 为准。

## 适用场景

- "帮我整理这周的会议纪要" / "总结最近的会议" / "生成会议周报"

- "看看今天开了哪些会" / "回顾过去一周开了哪些会"

## 前置条件

仅支持 user 身份。执行前确保已授权：

```
lark-cli auth login --domain vc        # 基础（查询+纪要）
lark-cli auth login --domain vc,drive   # 含读取纪要文档正文、生成文档
lark-cli auth login --domain vc,drive,minutes  # 含无 note_id 时的妙记备选路径
```