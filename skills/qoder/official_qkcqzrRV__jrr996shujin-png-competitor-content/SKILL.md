---
name: seo-competitor-content
description: "竞品内容监测子模块。每周扫描竞品网站的新发布内容（Blog、Docs、Learning、Updates、Help Center），追踪竞品文章排名趋势和估算流量，对排名上升的文章做深度分析。当用户提到'竞品发了什么新东西''竞品的博客''对手最近在做什么内容''竞品排名上升了'时触发。数据源：SEMrush API + web_fetch。"
---

# 竞品内容监测模块

## 核心功能

每周扫描竞品的内容发布动态，追踪其文章的排名和流量变化，对表现上升的文章做深度分析，帮助你理解竞品在做什么以及为什么有效。

## 监测范围

对每个竞品域名，监测以下内容板块（如果存在）：

| 板块 | 常见 URL 路径 | 监测重点 |
|------|-------------|----------|
| **Blog** | `/blog/`、`/articles/`、`/insights/` | 🔴 必监测 — 新文章第一时间通知 |
| **Docs** | `/docs/`、`/documentation/` | 有新功能文档说明时通知 |
| **Learning** | `/learn/`、`/academy/`、`/resources/`、`/guides/` | 教程类内容，往往 SEO 价值很高 |
| **Updates** | `/changelog/`、`/updates/`、`/whats-new/`、`/releases/` | 产品更新，反映竞品功能发展方向 |
| **Help Center** | `/help/`、`/support/`、`/faq/` | 新增帮助文章说明竞品在解决什么用户问题 |

### 首次运行：确认竞品内容板块

首次运行时，需要确认每个竞品的实际 URL 结构：

1. `web_fetch` 竞品首页，分析导航栏中的内容板块链接
2. 尝试访问常见路径（`/blog/`、`/docs/` 等），确认哪些存在
3. 检查竞品 sitemap（`/sitemap.xml`），识别内容板块的 URL 模式
4. 展示给用户确认：

```
竞品 A (competitor.com) 内容板块：
✅ Blog: competitor.com/blog/
✅ Docs: competitor.com/docs/
✅ Updates: competitor.com/changelog/
❌ Learning: 未发现
❌ Help Center: 未发现（可能在子域名 help.competitor.com？）
```

用户确认后保存 URL 模式，后续每周自动扫描。

## 执行流程

### 1. 新内容发现（每周扫描）

**方法 A — SEMrush New Pages API（首选）：**
- 调用 SEMrush Domain Organic Research API
- 筛选过去 7 天新增的有排名页面
- 按 URL 路径归类到各内容板块

**方法 B — Sitemap 差异对比（补充）：**
- `web_fetch` 竞品 sitemap
- 与上周保存的 sitemap 对比，找出新增的 URL
- 按 `<lastmod>` 日期排序

**方法 C — RSS Feed（如有）：**
- 检查竞品是否有 Blog RSS（`/feed/`、`/rss/`、`/blog/feed/`）
- RSS 是最及时的新内容通知方式

三种方法交叉使用，确保不遗漏。

**发现新 Blog 后立即通知：**
```
🆕 竞品新内容提醒

competitor.com 本周发布了 2 篇新 Blog：

1. "How to Build AI Agents for Enterprise"
   URL: competitor.com/blog/ai-agents-enterprise
   发布日期：2026-02-20
   目标关键词（推测）：AI agents enterprise, build AI agent
   ⚠️ 与我们的核心业务词直接竞争

2. "Monthly Product Update: February 2026"
   URL: competitor.com/changelog/february-2026
   发布日期：2026-02-22
   内容：新功能发布——自动邮件回复、团队协作改进
```

### 2. 竞品文章排名追踪

对已知的竞品内容，每周追踪排名变化：

**数据来源：** SEMrush Domain Organic Research API
- 按页面维度拉取竞品各文章排名的关键词
- 与上周数据对比，计算排名变化

**标记规则：**
- 🔥 **快速上升**：某篇文章的核心关键词一周内上升 ≥ 5 位
- 📈 **稳步上升**：连续 3 周排名上升
- 🆕 **新进首页**：之前不在前 10，本周进入前 10
- ⚠️ **抢了我们的位置**：竞品在某关键词上排名超过了我们

### 3. 竞品上升文章深度分析

当检测到竞品某篇文章排名显著上升时，自动进行深度分析。这是本模块最有价值的功能——你不只知道"竞品涨了"，还要知道"为什么涨了"。

**分析维度：**

#### a) 标题写法
- `web_fetch` 获取页面 HTML
- 提取 `<title>` 和 `<h1>`
- 分析：长度、是否包含关键词、是否有数字/年份、是否有情感词、问句还是陈述句
- 与我们同主题文章的标题对比

#### b) 内容结构
- 提取 H1-H4 标题层级，生成大纲
- 统计字数
- 检查是否有 FAQ 区块
- 检查是否有 Table of Contents
- 检查列表和表格的使用情况
- 与我们同主题文章的结构对比

#### c) 内容深度
- 分析覆盖了哪些子话题（从 H2/H3 标题推断）
- 是否有我们没覆盖的子话题 = 内容缺口
- 是否使用了原始数据、案例研究、专家引用

#### d) Schema Markup
- 检查使用了哪些 Schema 类型
- 是否有 FAQ Schema、Article Schema、HowTo Schema
- 与我们的 Schema 实现对比

#### e) 外链分析
- 调用 SEMrush Backlinks API，查看该页面的外链数量和来源
- 是否有高权重网站链接到它
- 是否有最近的新外链（可能是排名上升的原因）

#### f) 估算流量
- SEMrush 的估算月流量
- 流量趋势（过去 3 个月变化）

**深度分析输出：**
```
📊 竞品上升文章分析

文章：competitor.com/blog/ai-agents-enterprise
排名变化：核心词 "AI agents for enterprise" #18 → #6（上升 12 位，进入首页）

【标题】"How to Build AI Agents for Enterprise in 2026: Complete Guide"
  - 长度：58 字符 ✅
  - 含年份 "2026" ✅
  - 含 "Complete Guide" 激发点击 ✅
  - 我们的标题："AI Agent Guide" — 太短，缺乏具体性

【内容结构】
  字数：4,200 词（我们的同主题文章：2,100 词）
  标题层级：H1→H2(8个)→H3(15个) — 结构清晰
  FAQ 区块：有（6 个问答）
  表格：有（3 个功能对比表）
  
【我们没有覆盖的子话题】
  - "Enterprise Security Considerations"
  - "ROI Calculation for AI Agent Deployment"
  - "Integration with Existing CRM Systems"
  → 这些是内容缺口，建议补充

【Schema】
  - Article Schema ✅
  - FAQ Schema ✅（我们没有 ❌）
  - BreadcrumbList ✅

【外链】
  总外链：47 个
  最近 30 天新增：12 个
  高权重来源：TechCrunch、Product Hunt
  → 新外链可能是排名上升的主要原因

【建议动作】
  1. 我们的同主题文章需要扩充到 4000+ 词
  2. 补充 Enterprise Security、ROI 计算、CRM 集成三个子话题
  3. 添加 FAQ 区块和 FAQ Schema
  4. 更新标题，加入年份和更具体的描述
  5. 争取外链——可联动 aeo-content-strategy 分析相关社区讨论
```

### 4. 估算流量汇总

每周输出竞品的估算流量变化：

- 竞品域名整体估算流量（SEMrush Traffic Analytics API）
- 各内容板块的流量占比
- 与上周对比的变化趋势

## 输出格式

### 每周调用时

```
🔍 竞品内容监测周报（2026-02-17 ~ 2026-02-23）

━━ competitor.com ━━

🆕 新发布内容（2 篇）：
  [Blog] "How to Build AI Agents for Enterprise" — 2/20
  [Changelog] "February 2026 Product Update" — 2/22

🔥 排名上升文章（1 篇需要关注）：
  /blog/ai-agents-enterprise
  "AI agents for enterprise" #18→#6 ⬆️12
  → 深度分析已生成（见上方）

📈 整体估算流量：45,200/月（上周 43,800，+3.2%）

⚠️ 抢了我们位置的关键词：
  "best AI productivity tool" — 竞品 #4，我们 #7
```

### 被月度报告调用时

输出结构化数据：
- 当月竞品新发布内容完整清单
- 排名变化显著的文章及分析
- 竞品月度估算流量趋势
- 竞品抢走的关键词清单
- 我们的内容缺口汇总
