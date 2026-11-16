---
name: lark-skill-maker
description: Install the lark-skill-maker skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-skill-maker
---

# Skill Maker

基于 lark-cli 创建新 Skill。Skill = 一份 `SKILL.md`，教 AI 用 CLI 命令完成任务。

## CLI 核心能力

```
lark-cli             # 已注册 API
lark-cli  +                      # Shortcut（高级封装）
lark-cli api   [--data/--params]  # 任意飞书 OpenAPI
lark-cli schema        # 查参数定义
```

优先级：Shortcut > 已注册 API > `api` 裸调。

## 调研 API