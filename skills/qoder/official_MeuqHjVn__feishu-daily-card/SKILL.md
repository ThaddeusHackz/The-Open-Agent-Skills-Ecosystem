---
name: feishu-daily-card
description: "飞书群日报卡片美化技能。使用飞书 Schema 2.0 卡片消息格式，创建带分栏布局、彩色标题、数据面板的美观日报。支持AI新闻简报、学习日报、成本日报等多种模板。"
version: 1.0.0
type: skill
tags: [feishu, card, daily-report, lark, notification]
author: Kimi Claw
---

# 飞书群日报卡片美化

将枯燥的纯文本日报升级为美观的飞书卡片消息，支持分栏布局、彩色标题栏、数据面板等丰富的视觉元素。

## 功能特性

- 🎨 **彩色标题栏** — 支持 indigo、blue、green、orange 等配色
- 📊 **分栏布局** — 双栏、三栏等多种布局方式
- 📰 **预设模板** — AI晨报、学习日报、成本日报
- 🔧 **灵活定制** — 基于 Schema 2.0 自由组合元素

## 快速开始

### 1. 安装技能

```bash
openclawmp install skill/@kimiclaw/feishu-daily-card
```

### 2. 使用示例

**发送AI晨报卡片：**

```python
import json
import subprocess

card = {
    "schema": "2.0",
    "config": {"wide_screen_mode": True},
    "header": {
        "template": "indigo",
        "title": {"tag": "plain_text", "content": "📰 AI晨报 | 2026年3月3日"}
    },
    "body": {
        "elements": [
            {"tag": "markdown", "content": "**🔥 今日值得关注**"},
            {"tag": "markdown", "content": "**1️⃣ 大新闻标题**\n• 要点1\n• 要点2"},
            {"tag": "hr"},
            {"tag": "markdown", "content": "**📊 数据面板**"},
            {
                "tag": "column_set",
                "flex_mode": "trisect",
                "columns": [
                    {"tag": "column", "width": "weighted", "weight": 1,
                     "elements": [{"tag": "markdown", "content": "**指标A**\n100"}]},
                    {"tag": "column", "width": "weighted", "weight": 1,
                     "elements": [{"tag": "markdown", "content": "**指标B**\n200"}]},
                    {"tag": "column", "width": "weighted", "weight": 1,
                     "elements": [{"tag": "markdown", "content": "**指标C**\n300"}]}
                ]
            }
        ]
    }
}

# 保存并发送
with open('/tmp/card.json', 'w') as f:
    json.dump(card, f)

subprocess.run([
    "python3", 
    "/root/.openclaw/skills/feishu-card/scripts/send_card.py",
    "--chat-id", "oc_xxx",
    "--card-file", "/tmp/card.json"
])
```

## 卡片元素

| 元素 | 说明 | 示例 |
|------|------|------|
| `markdown` | 富文本内容 | 支持粗体、列表、链接 |
| `hr` | 水平分隔线 | 内容分区 |
| `column_set` | 多栏布局 | bisect(双栏)、trisect(三栏) |
| `header` | 标题栏 | 彩色背景 + 标题文字 |

## 标题栏配色

- `blue` / `wathet` / `turquoise` — 蓝色系
- `green` / `yellow` / `orange` — 暖色系  
- `red` / `carmine` / `violet` — 醒目色
- `indigo` / `purple` / `grey` — 其他

## 模板示例

### AI晨报模板

```json
{
  "schema": "2.0",
  "config": {"wide_screen_mode": true},
  "header": {
    "template": "indigo",
    "title": {"tag": "plain_text", "content": "📰 AI晨报 | YYYY-MM-DD"}
  },
  "body": {
    "elements": [
      {"tag": "markdown", "content": "**🔥 今日值得关注**"},
      {"tag": "markdown", "content": "**1️⃣ 新闻标题**\n• 要点\n• 数据"},
      {"tag": "hr"},
      {"tag": "markdown", "content": "*⏰ 每日自动推送*"}
    ]
  }
}
```

### 学习日报模板

```json
{
  "schema": "2.0",
  "header": {"template": "green", "title": {"tag": "plain_text", "content": "🤖 学习日报"}},
  "body": {
    "elements": [
      {
        "tag": "column_set",
        "flex_mode": "bisect",
        "columns": [
          {"tag": "column", "width": "weighted", "weight": 1,
           "elements": [{"tag": "markdown", "content": "**✅ 今日已学**\n• 内容1\n• 内容2"}]},
          {"tag": "column", "width": "weighted", "weight": 1,
           "elements": [{"tag": "markdown", "content": "**📋 明日计划**\n• 计划1\n• 计划2"}]}
        ]
      }
    ]
  }
}
```

### 成本日报模板

```json
{
  "schema": "2.0",
  "header": {"template": "orange", "title": {"tag": "plain_text", "content": "💰 成本日报"}},
  "body": {
    "elements": [
      {
        "tag": "column_set",
        "flex_mode": "trisect",
        "columns": [
          {"tag": "column", "width": "weighted", "weight": 1,
           "elements": [{"tag": "markdown", "content": "**模型调用**\n¥0.15"}]},
          {"tag": "column", "width": "weighted", "weight": 1,
           "elements": [{"tag": "markdown", "content": "**搜索API**\n¥0.05"}]},
          {"tag": "column", "width": "weighted", "weight": 1,
           "elements": [{"tag": "markdown", "content": "**今日总计**\n**¥0.20**"}]}
        ]
      }
    ]
  }
}
```

## 依赖

- `feishu-card` 技能（飞书卡片发送脚本）
- Python 3.8+

## 参考资料

- [飞书卡片 Schema 2.0 文档](https://open.feishu.cn/document/uAjLw4CM/ukzMukzMukzM/feishu-cards/card-overview)
- [feishu-card 技能](https://openclawmp.cc/asset/feishu-card)

## License

MIT
