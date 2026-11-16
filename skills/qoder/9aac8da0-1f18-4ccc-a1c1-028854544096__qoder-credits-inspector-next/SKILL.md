---
name: qoder-credits-inspector-next
description: Qoder 原生的 Credits 消耗体检器。扫描本机 ~/.qoder 会话日志里的真实 credits
  计费字段，检查使用习惯、定位消耗大户（超长对话/高价模型跑简单任务/子代理蔓延/常驻文件膨胀/定时任务高价档），产出文字诊断摘要 + Chart.js
  单文件 HTML 仪表盘与可落地优化建议。报告只展示 credits 与使用行为，不展示 token 数与单价系数。当用户说 Qoder credits
  消耗快、省 credits、token 优化、额度不够用、消耗大户、用量分析、credits 体检/报告/诊断时触发。
version: 0.2.0
---
# Credits 消耗体检器（Qoder）

帮用户**检查使用习惯 → 定位 Credits 消耗大户 → 给优化建议**。产出两件套：对话里的文字诊断摘要 + 可分享的 HTML 仪表盘。

Qoder 的会话日志带**真实计费字段**（assistant 记录的 `message.usage.credits`，实扣值），所以体检以 credits 为主口径。消耗大户有六类：① 超长对话（轮次越多每轮重发历史越大）；② 高价模型跑简单任务（本机实测单价可差几十倍）；③ 子代理蔓延（并行 subagent 各自完整跑上下文与工具链，成本随并行度线性涨）；④ 常驻文件 MEMORY.md / AGENTS.md 每轮注入；⑤ 定时任务跑高价档；⑥ 单轮上下文占用过高（触发压缩重算）。报告不展示 token 数与单价/倍数，避免外发时暴露价格系数。

## 省 Credits 纪律（本 skill 自身必须遵守）

- **一次跑通，别探索**：按下面 4 步顺序执行，不要中途反复试错或读脚本源码。
- **大响应只落盘、不展开**：`qoder_cron` 的 list 响应含每个任务的完整 instruction 文本，直接把响应写进 `data/cron.json`，**不要**把 JSON 读进上下文。
- **产物不回读**：`qoder_sessions.json`、`qoder-credits-report.html` 由脚本消费，**不要** cat / Read 进上下文；只看脚本打印的几行摘要。
- **按需加载参考**：分类/阈值/模型别名说明在 `references/tuning.md`，踩坑与验证清单在 `references/pitfalls.md`——**仅在需要调参或排错时才 Read**，平时不加载。

## Steps

### Step 1: 采集定时任务（落盘，不展开）

调用 builtin 工具 `qoder_cron action=list`，把整个响应写入 `$WORKSPACE/data/cron.json`（`{success, tasks:[...]}`，build_report.py 自动读 `.tasks`）。
本机没有可读的额度接口（额度数据在加密的 `~/.qoder/.auth/` 下），报告按真实消耗 + 日均呈现，不硬套 quota 百分比。

### Step 2: 扫描本体会话（真实 credits）

```bash
python3 ~/.agents/skills/qoder-credits-inspector-next/scripts/collect_qoder.py \
  --days 30 --output "$WORKSPACE/data/qoder_sessions.json"
```
扫 `~/.qoder/projects/**/*.jsonl`（含 `subagents/agent-*.jsonl`，子代理默认计入——它们带独立 credits），按 UUID 去重，采每会话真实 credits、轮次、峰值上下文占用、模型别名、清洗后标题，以及报告深链所需的 `session_id` / `request_set_id`。

### Step 3: 生成 HTML 仪表盘

```bash
python3 ~/.agents/skills/qoder-credits-inspector-next/scripts/build_report.py \
  --days 30 --data-dir "$WORKSPACE/data" \
  --output "$WORKSPACE/outputs/qoder-credits-report.html" --user "工号（花名）"
```
`--user` 可选（缺省头部不展示）。脚本生成后**自动用系统默认浏览器打开报告**；不需要打开时加 `--no-open`。

报告里「消耗大户 Top 10」的会话标题是深链，点击可在 Qoder 打开对应会话（子代理会跳到所属主会话）。协议自动按本机客户端注册的 scheme 选择：Global 用 `qoder://chat/open?sessionId=...&requestSetId=...`，CN 用 `qoder-cn://...`；可用 `--link-scheme qoder|qoder-cn` 覆盖。

### Step 4: 交付

1. 报告已由脚本在默认浏览器打开；仍给出 HTML 路径便于回看。
2. 给文字诊断摘要（客观、短、可落地），别只甩文件：

```
最近 N 天消耗 X credits（日均 Y；主会话 A / 子代理 B），M 个会话。
消耗大户：① 超长对话 K 个超 100 轮、吃 P% credits（举 1-3 个标题）；② 高价模型跑简单任务；③ 子代理占 C%；④ AGENTS.md/MEMORY.md 偏大。
建议（按收益排序）：对话 10-15 轮就新开；简单任务切轻量/Flash 档；批量子代理任务先小范围试跑；常驻文件低频条目下沉。
```

## 诊断后执行优化（需用户点头，详见 references/tuning.md）

- **模型换档**：Qoder 客户端手动切（本 skill 无换档接口）；按仪表盘「模型用量分布」与任务复杂度给建议。
- **定时任务降价**：`qoder_cron action=update`，patch 是**合并**语义（只传要改字段，instruction 原样保留）。
- **常驻文件精简**：MEMORY.md / AGENTS.md 是普通文件，直接 Edit/Write 精简（Qoder 无 memory 专用工具）。
- **断重型 MCP**：引导用户在设置里断，或用 `mcp-config` skill。

## Troubleshooting

排错、口径坑（credits 语义、input 含 cache_read、子代理去重）、验证清单见 `references/pitfalls.md`（按需 Read）。
