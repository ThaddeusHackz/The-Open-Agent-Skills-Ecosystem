---
name: expert-recruit-mail
description: 连接钉钉邮箱，把收件箱里与「QoderWork 专家套件招募」相关的报名邮件全部过一遍——逐封落库到钉钉AI表格、按邮箱查重、跑审核滤网定状态、归类目标岗位。当用户说"处理专家招募邮件/过一遍报名邮件/审核专家报名/同步招募邮箱"时使用。
version: 1.0.0
---

# 专家招募邮件处理 Pipeline

用钉钉 `dws` 命令读邮箱 → 把招募相关邮件逐封写入 3 张钉钉 AI 表格 → 审核定状态。所有命令直接作为 Bash 工具调用。

## 固定常量（钉钉AI表格「专家套件共创」）

```
BASE = YQBnd5ExVEjea40qC2X2KOlyJyeZqMmz

专家主表       zYD801l : 邮箱地址=HoEnYus 专家姓名=NvhgS0D 行业=LftfhUH 岗位=QYDKkBy
                        工作年限=HB2TdIM 当前状态=xqkytOo 一级目标岗位=5YyArGP 二级目标岗位=sRPZhWi
沟通记录表     Z9Kz1Xl : 邮箱地址=QPclkoC 时间戳=GSpVX8z 邮件主题=eOslSuP 邮件正文=ifKKJrF
目标岗位需求表 hERWDMS : 一级岗位=01ZM8y7 二级岗位=bDxXdb5 需求数=6xmH0Jh 已交付专家数=h9scIZG 已交付专家邮箱=IkiBkqV
```

`当前状态` 单选取值：`审核未通过` / `报名通过未提交` / `跟进中` / `已提交`（写入只能用这 4 个）。
`一级/二级目标岗位` 单选取值必须先从目标岗位需求表查出真实分类名再填（见步骤 0）。

## Pipeline 步骤

### 0. 准备
- 取邮箱：`dws mail mailbox list --format json` → 选用户企业邮箱地址记为 EMAIL（多个则向用户确认）。
- 取分类表：`dws aitable record query --base-id BASE --table-id hERWDMS --limit 100 --format json` → 得到全部「一级岗位/二级岗位」组合，作为归类候选集。

### 1. 搜招募邮件（收件箱，翻页取全）
```bash
dws mail message search --email EMAIL \
  --query '(subject:报名 OR subject:专家 OR body:专家套件 OR body:报名) AND folderId:2' \
  --size 50 --format json
```
- 取返回的 `messages[].id`；`nextCursor` 非 `$` 则带 `--cursor <nextCursor>` 继续翻页直到 `$`。
- 命中宽松无妨，正文解析阶段再判定是否真为报名邮件。

### 2. 逐封取正文
```bash
dws mail message get --email EMAIL --id <messageId> --format json
```
提取：发件人邮箱 FROM、主题、正文、日期。

### 3. 落沟通记录表（先留痕，无论审核结果）
```bash
dws aitable record create --base-id BASE --table-id Z9Kz1Xl \
  --records '[{"cells":{"QPclkoC":"FROM","GSpVX8z":"2026-06-03","eOslSuP":"主题","ifKKJrF":"正文全文"}}]' --format json
```

### 4. 按邮箱查重
```bash
dws aitable record query --base-id BASE --table-id zYD801l \
  --query 'filter: 邮箱地址 = "FROM"' --format json
```
- **命中（老专家）**：不重审，保持/按现状态流转，跳到下一封。
- **未命中（新专家）**：从正文解析三核心字段 `行业 / 岗位 / 工作年限`（报名格式：行业|岗位|N年，例 `广告/创意|策略总监|7年`），进入步骤 5。

### 5. 审核滤网（有序两道闸）
1. **年限闸**：`工作年限 > 3` 才过；`≤ 3`（含 3 年整）→ 当前状态=`审核未通过`。
2. **归类闸**：能否归入步骤 0 的某个「一级+二级岗位」组合；能→当前状态=`报名通过未提交` 并填一级/二级目标岗位；归不进→`审核未通过`。
- 三核心字段缺任一 → 直接 `审核未通过`。

### 6. 写专家主表（新专家新增一行）
```bash
dws aitable record create --base-id BASE --table-id zYD801l \
  --records '[{"cells":{"HoEnYus":"FROM","NvhgS0D":"姓名","LftfhUH":"行业","QYDKkBy":"岗位原文","HB2TdIM":7,"xqkytOo":"报名通过未提交","5YyArGP":"设计","sRPZhWi":"工业/产品设计"}}]' --format json
```
- `审核未通过` 时只写邮箱/姓名/三核心字段+状态，目标岗位留空。

### 7. 回查验证 + 汇总
- 写完按邮箱 `record query` 回查确认真生效（无权限会假性 success）。
- 汇总报告：本次处理 N 封、新增 M 位专家、各状态分布、跳过的老专家数。

## 关键约束（务必遵守）
- `--records` 的 JSON 必须**单行 inline 字面量**，禁止 `--records "$(cat file)"`（host hook 不触发会返回 pending 占位符）。
- record 写入 `cells` 的 key 用 **fieldId**（如 HoEnYus），不是字段名。
- 单选字段（当前状态/一级/二级目标岗位）只能写**已存在的选项名**，先查再填。
- `行业/岗位` 是自报原文，用文本原样写，不做枚举。
- 沟通记录表**只追加、永不更新**；专家主表靠邮箱查重保证一人一行。
- 发任何外发邮件前需人工确认，本 skill 默认**只读邮件+写表**，不自动发件。
