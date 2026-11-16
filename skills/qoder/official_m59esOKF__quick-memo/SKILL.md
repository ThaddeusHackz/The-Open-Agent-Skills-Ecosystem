---
id: GGbood/quick-memo
owner_id: GGbood
name: quick-memo
description: 快速备忘录 - 帮用户快速记录临时想法到 memory 文件
version: 1.0.0
icon: "\U0001F4E6"
author: GGbood
---

# 快速备忘技能

当用户说"记一下"、"记住这个"、"快速备忘"或类似内容时，使用此技能。

## 功能
- 将用户的临时想法快速记录到 `memory/quick-memos.md`
- 自动添加时间戳
- 支持追加新条目

## 使用方法

1. 检查 `memory/quick-memos.md` 是否存在，不存在则创建
2. 将用户要记录的内容追加到文件末尾
3. 格式：
   ```markdown
   ## [YYYY-MM-DD HH:mm] 简短标题
   
   内容...
   
   ---
   ```
4. 告诉用户已记录成功

## 示例

用户："记一下，明天要买咖啡"
→ 记录到 quick-memos.md，回复"✅ 已记下：明天要买咖啡"

用户："记住这个想法：可以用 local-brain 替代记忆搜索"
→ 记录到 quick-memos.md，回复"✅ 已保存你的想法"

## 注意
- 保持简洁，不要啰嗦
- 时间戳用 Asia/Shanghai 时区
- 如果用户没给标题，自动生成一个简短的
