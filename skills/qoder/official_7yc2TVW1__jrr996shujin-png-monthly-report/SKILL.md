---
name: seo-monthly-report
description: "月度 SEO 竞争情报汇总报告子模块。汇总当月的关键词排名、内容表现、竞品动态数据，生成 React 交互看板，包含月环比对比和行动建议清单。当用户提到'生成月度报告''本月 SEO 总结''出报告''月度看板'时触发。输出格式为 React 交互看板（.jsx 文件）。"
---

# 月度汇总报告模块

## 核心功能

月底汇总所有子模块数据，生成一份 React 交互看板。这不是简单的数据堆砌——而是帮你快速看清"这个月发生了什么、接下来该做什么"。

## 数据输入

在生成月度报告前，先按顺序调用其他三个子模块获取当月数据：

1. **keyword-ranking** → 当月关键词排名历史、报警事件、新发现关键词
2. **content-performance** → 内容表现汇总、衰退清单、新内容追踪、更新提醒
3. **competitor-content** → 竞品新内容清单、排名变化、上升文章分析、内容缺口

## React 看板结构

生成一个完整的 `.jsx` 文件，包含以下 Tab 页：

### Tab 1：总览仪表板（Overview）

**核心 KPI 卡片（月环比）：**

| KPI | 说明 | 对比 |
|-----|------|------|
| 总自然点击量 | Google Search Console | vs 上月 |
| 总曝光量 | Google Search Console | vs 上月 |
| 平均 CTR | 点击/曝光 | vs 上月 |
| 平均排名 | 所有追踪关键词的平均位置 | vs 上月 |
| 前 10 关键词数 | 排名在首页的关键词数量 | vs 上月 |
| 估算流量 | SEMrush | vs 上月 |

每个 KPI 卡片用颜色指示变化方向：绿色上升、红色下降、灰色持平。

**排名分布饼图：**
- #1-3 位关键词数量
- #4-10 位
- #11-20 位
- #20+ 位
与上月对比。

**本月报警事件时间线：**
按日期排列的报警事件（排名大幅下滑、竞品超越等），可点击查看详情。

### Tab 2：关键词详情（Keywords）

**排名变化表格（可排序、可筛选）：**

| 关键词 | 类别 | Google 排名 | Bing 排名 | 月初→月末 | 变化 | 竞品A | 竞品B |
|--------|------|------------|----------|----------|------|-------|-------|
| ... | A/B/C/D | #X | #X | #X→#Y | ↑↓ | #X | #X |

支持：
- 按类别（A/B/C/D）筛选
- 按变化幅度排序（看最大涨跌）
- 按搜索引擎（Google/Bing）切换
- 搜索关键词

**关键词趋势折线图：**
选择任意关键词，显示过去 4 周的排名趋势折线。品牌和竞品在同一图上对比。

**新发现的关键词机会：**
本月通过 SEMrush 和 Search Console 发现的新关键词，标注搜索量和当前排名。

### Tab 3：内容表现（Content）

**内容表现热力图：**
X 轴为时间（周），Y 轴为文章，颜色深浅表示点击量变化——一眼看出哪些文章在涨、哪些在跌。

**衰退内容清单：**
标记为衰退的文章列表，包含：
- 文章标题和 URL
- 下降幅度
- 可能原因
- 建议动作
- 最后更新日期

**新文章观察追踪：**
本月新发布文章的表现进展，是否达到预期。

**更新提醒队列：**
需要更新的文章清单，按紧急程度排序。

### Tab 4：竞品动态（Competitors）

**竞品新内容时间线：**
按日期展示竞品本月发布的所有内容，按板块（Blog/Docs/Updates 等）用标签颜色区分。

**竞品排名变化 Top 10：**
排名上升最多的竞品文章，附深度分析摘要。点击可展开完整分析。

**关键词争夺地图：**
可视化展示品牌和竞品之间的关键词争夺关系：
- 我们独占的关键词（绿色）
- 竞品独占的关键词（红色）
- 双方都有排名的争夺词（黄色，标注各自排名）

**竞品估算流量趋势：**
过去 3 个月的竞品流量变化趋势图。

### Tab 5：行动建议（Action Plan）

这是报告最核心的 Tab——不是数据，是**接下来该做什么**。

**自动生成的行动建议清单：**

每条建议包含：
- **优先级**：🔴 高 / 🟡 中 / 🟢 低
- **建议内容**：具体要做什么
- **原因**：为什么要做这个
- **预期影响**：做了之后预计能改善什么
- **关联数据**：支持这条建议的数据来源

**建议生成规则：**

| 数据信号 | 生成的建议 | 优先级 |
|----------|-----------|--------|
| 核心关键词排名持续下滑 | 更新对应文章内容和 Schema | 🔴 |
| 竞品新文章抢了我们的关键词排名 | 分析竞品文章，补充我们的内容缺口 | 🔴 |
| 内容衰退标记触发 | 刷新该文章 + 检查技术问题 | 🟡 |
| 标题含过期年份 | 更新标题和内容 | 🟡 |
| 发现新关键词机会（竞品有我们没有） | 创建新内容覆盖该关键词 | 🟡 |
| Bing 排名远低于 Google | 优化 Bing 收录，提交 sitemap 到 Bing Webmaster | 🟡 |
| 竞品在某主题排名上升且我们无对应内容 | 联动 aeo-content-strategy 挖掘长尾问题并创建内容 | 🟢 |

**联动提示：**

当行动建议涉及到其他 skill 时，明确标注：
```
🔗 建议 #3 可联动执行：
   → 调用 aeo-content-strategy：挖掘 "enterprise AI agent" 相关的 Reddit 讨论和长尾问题
   → 调用 seo-aeo-diagnostics：对 /blog/ai-agent-guide 页面做技术诊断
```

## 技术实现注意事项

### React 看板技术栈

```
- React（函数组件 + Hooks）
- Tailwind CSS（核心样式类）
- Recharts（折线图、饼图、柱状图）
- 数据直接内嵌在组件中（因为是静态报告，不需要 API 调用）
- Tab 切换用 useState 控制
- 表格支持排序和筛选
```

### 数据组织

将所有子模块收集的数据整合为一个 `reportData` 对象，结构如下：

```javascript
const reportData = {
  meta: {
    brand: "品牌域名",
    competitors: ["竞品1", "竞品2"],
    period: "2026-02",
    generatedAt: "2026-02-28"
  },
  overview: {
    kpis: { clicks, impressions, ctr, avgRank, top10Keywords, estimatedTraffic },
    kpisPrevMonth: { ... },  // 上月数据用于环比
    alerts: [{ date, type, message, severity }]
  },
  keywords: {
    tracked: [{ keyword, category, googleRank, bingRank, change, competitor1Rank, competitor2Rank, weeklyHistory }],
    newOpportunities: [{ keyword, volume, currentRank, source }]
  },
  content: {
    articles: [{ url, title, clicks, impressions, avgRank, trend, lastUpdated }],
    decaying: [{ url, title, declinePercent, reason, suggestedAction }],
    newArticles: [{ url, title, publishDate, currentRank, status }],
    updateQueue: [{ url, title, reason, urgency }]
  },
  competitors: {
    newContent: [{ competitor, url, title, date, type, targetKeywords }],
    risingArticles: [{ url, title, keywordChange, analysis }],
    keywordBattle: { brandOnly, competitorOnly, contested },
    trafficTrend: [{ month, brandTraffic, competitor1Traffic, competitor2Traffic }]
  },
  actionPlan: [{ priority, action, reason, expectedImpact, linkedSkill }]
};
```

### 配色方案

```
品牌色：蓝色系（#3B82F6）
竞品色：红色系（#EF4444）和橙色系（#F59E0B）
上升/正面：绿色（#10B981）
下降/负面：红色（#EF4444）
中性：灰色（#6B7280）
背景：深色（#111827）或浅色（#F9FAFB）——根据用户偏好
```

## 交付方式

1. 生成 `.jsx` 文件到 `/mnt/user-data/outputs/`
2. 文件命名：`seo-monthly-report-YYYY-MM.jsx`
3. 同时输出对话内摘要——给不想看看板的场景提供快速总结
