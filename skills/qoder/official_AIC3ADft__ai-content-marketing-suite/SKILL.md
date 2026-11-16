---
name: ai-content-marketing-suite
displayName: AI内容创作与自动化营销系统
description: 一站式AI内容创作解决方案 - 自动生成、多平台分发、数据分析、智能优化
version: 1.0.0
type: skill
tags: content, marketing, automation, social-media, ai-writing, multi-platform
category: Marketing
---

# AI内容创作与自动化营销系统

> 让AI成为你的内容团队 - 自动创作、智能分发、数据驱动增长

## 概述

本工作流将 OpenClaw 打造成一个全自动内容营销引擎，帮你：

- 🤖 **AI自动创作** - 生成文章、视频脚本、社交媒体帖子
- 📱 **多平台分发** - 一键发布到小红书、抖音、知乎、公众号等
- 📊 **数据分析** - 追踪内容表现，优化创作策略
- 🎯 **智能优化** - 基于数据反馈自动调整内容方向
- ⏰ **定时发布** - 最佳时间自动发布，最大化曝光

## 核心功能

### 1. AI内容创作引擎

**支持的内容类型：**
- 📄 长篇文章（知乎、公众号、博客）
- 📝 短内容（小红书笔记、微博、Twitter）
- 🎬 视频脚本（抖音、B站、YouTube）
- 📧 邮件营销内容
- 🖼️ 图文卡片

**AI创作流程：**
```
热点话题 → 大纲生成 → 内容撰写 → 标题优化 → 标签推荐
```

### 2. 多平台自动分发

**支持平台（13+）：**
| 平台 | 内容类型 | 特点 |
|------|---------|------|
| 小红书 | 图文笔记 | 种草神器 |
| 抖音 | 短视频脚本 | 流量巨大 |
| 知乎 | 专业回答 | 长尾流量 |
| 公众号 | 深度文章 | 私域沉淀 |
| B站 | 中长视频 | 年轻用户 |
| Twitter/X | 短推文 | 国际传播 |
| YouTube | 视频脚本 | 全球受众 |

### 3. 内容数据分析

**追踪指标：**
- 👁️ 阅读量/播放量
- ❤️ 点赞数
- 💬 评论数
- 🔄 转发/分享数
- 👥 粉丝增长
- 🔗 引流转化

### 4. 热点追踪与选题

**热点来源：**
- 微博热搜
- 知乎热榜
- 抖音热门
- 小红书趋势
- Google Trends

### 5. 内容日历管理

**自动化排期：**
```
周一：行业洞察文章
周二：小红书种草笔记
周三：知乎专业回答
周四：抖音视频脚本
周五：周末活动预告
周末：轻松娱乐内容
```

## 所需技能

### 必需技能

- `tavily` 或 `web_search` — 热点搜索与资料收集
- `rss` — 订阅行业资讯
- Cron 任务 — 定时创作与发布
- Telegram/Discord — 通知推送

### 可选技能

- `dalle` 或 `flux` — AI配图生成
- `elevenlabs` — AI语音生成
- `youtube` — 视频数据分析

## 设置指南

### 步骤 1：配置内容数据库

```sql
-- 内容库表
CREATE TABLE content_library (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL,
    platform TEXT NOT NULL,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    scheduled_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ
);

-- 热点追踪表
CREATE TABLE trending_topics (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    source TEXT NOT NULL,
    hotness INTEGER,
    captured_at TIMESTAMPTZ DEFAULT NOW()
);

-- 发布记录表
CREATE TABLE publish_logs (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES content_library(id),
    platform TEXT NOT NULL,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0
);
```

### 步骤 2：初始化AI创作助手

告诉你的 OpenClaw：

```text
你是我的AI内容创作助手。请按以下配置运行：

## 我的内容定位
领域：科技/AI/效率工具
目标受众：25-35岁职场人士
调性：专业但易懂，实用导向

## 内容策略
每周产出：
- 2篇深度长文（知乎/公众号）
- 5篇小红书笔记
- 3个抖音脚本
- 7条Twitter/X动态

## 质量标准
- 每篇内容必须经过事实核查
- 标题要吸引人但不做标题党
- 必须包含实用 actionable insights
```

### 步骤 3：配置发布渠道

```text
## 小红书
- 发布频率：每天1-2篇
- 最佳时间：中午12点，晚上8点
- 内容长度：300-800字

## 知乎
- 发布频率：每周2-3篇
- 最佳时间：晚上9-11点
- 内容长度：2000-5000字

## 抖音
- 发布频率：每天1个脚本
- 最佳时间：早上7-9点，晚上6-8点
- 时长：60-180秒
```

## 使用示例

### 日常操作

```
"今天有什么热点可以写？"
→ 返回今日热点列表 + 选题建议

"帮我写一篇关于AI编程的小红书笔记"
→ 生成完整笔记 + 标题 + 标签 + 配图建议

"分析一下上周的内容表现"
→ 生成数据分析报告 + 优化建议
```

### 批量创作

```
"本周计划：
- 周一：AI趋势分析文章
- 周三：效率工具测评
- 周五：一周AI新闻汇总

请提前准备好这些内容"
→ 按计划生成所有内容 + 设置定时发布
```

## 效果预期

### 30天目标
- 📈 总曝光：10万+
- 👥 新增粉丝：1000+
- 📝 发布内容：50+篇
- 🔥 爆款内容：2-3篇

### 90天目标
- 📈 总曝光：100万+
- 👥 新增粉丝：5000+
- 💰 开始变现收入
- 🏆 成为领域小V

## 风险提示

⚠️ **注意事项**
- 保持原创，避免抄袭
- 遵守各平台社区规范
- 不要过度营销引起反感
- 定期备份内容数据

## 相关资源

- [小红书创作者中心](https://creator.xiaohongshu.com/)
- [知乎创作者手册](https://www.zhihu.com/creator)
- [抖音创作者服务平台](https://creator.douyin.com/)

---
*本 README 由 OpenClaw 资产市场提供*
