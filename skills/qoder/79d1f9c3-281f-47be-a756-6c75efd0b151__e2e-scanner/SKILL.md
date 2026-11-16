---
name: e2e-scanner
description: 端到端交付 2.0 的"统计&Loop"扫描器。对 specs 目录做 4+1 扫描（spec 完整性、自检结果汇总、Session 统计、问题热点、Agent 端到端生成判定），并对 workItemId 调云效二次校验，输出周期性扫描报告驱动物料改进。当用户要求"扫描 specs"、"跑一次 e2e 扫描"、"统计 Agent 生成达标率"或需要 Loop 周期性盘点时使用。
version: 1.0.0
---

# E2E Scanner — 4+1 统计&Loop 扫描

对 spec 目录群做《端到端交付2.0》定义的 4+1 扫描，产出 markdown 报告，作为 Loop 飞轮的数据源（对照 `.specify/memory/constitution.md` 原则 VI）：

1. **spec 完整性检查** — 逐个 spec 目录核对必须件/推荐件，输出缺失清单
2. **检查结果汇总** — 解析各 `check_reports/check.summary.md` 的 `overall_result`
3. **Session 统计** — 解析 `session/conversation-log.md` 元数据表（用户轮次/助手消息数），标记轮次异常高（>30）的需求
4. **问题热点** — 聚合 check_reports 中高频违反的规则编号（RULE-x / BAN-x），产出物料改进建议
5. **(+1) Agent 端到端生成判定** — 4 硬性条件逐项判定（workItemId 格式有效 + spec.md 内容达标 + plan.md 内容达标 + check.summary.md 有 overall_result），输出达标率

## 触发方式

- `/e2e-scanner <specsRoot>` — 扫描指定 specs 根目录（如 `fe-project/mcp-market-fe-project/specs`），可传多个
- `/e2e-scanner --all` — 遍历全仓库所有名为 `specs` 的目录并扫描

## 执行流程

### 第 1 步：运行 scan.py

纯 Python3 无第三方依赖。报告输出到 `test-project/loop-reports/{YYYYMMDD}-e2e-scan-report.md`（日期用当天）：

```bash
# 指定 specsRoot（可多个）
python3 .qoder/skills/e2e-scanner/assets/scan.py \
  --roots <specsRoot1> [<specsRoot2> ...] \
  --repo <仓库根目录> \
  --output test-project/loop-reports/{YYYYMMDD}-e2e-scan-report.md

# 全仓库模式
python3 .qoder/skills/e2e-scanner/assets/scan.py \
  --all --repo <仓库根目录> \
  --output test-project/loop-reports/{YYYYMMDD}-e2e-scan-report.md
```

- exit 0 = 成功；exit 1 = 参数错误或未发现 spec 目录（把 stderr 原样反馈给用户）
- 同日重跑直接覆盖同名报告

### 第 2 步：workItemId 云效二次校验（agent 层）

scan.py 只校验字段**存在与格式**（非占位符、长度 ≥3）。对报告中格式有效的每个 workItemId，由 agent 调用 yunxiao MCP 的 `get_work_item` 校验云效可匹配：

- **匹配成功** — 不动报告判定，可在汇报中附上工作项标题佐证
- **匹配失败 / MCP 调用异常** — 仅标记 **warning**（在报告"Agent 端到端生成判定"节末尾追加一行 `> ⚠ warning: {spec 目录} 的 workItemId {id} 未能在云效匹配`），**不改变达标判定基线，不阻塞扫描**
- 没有任何格式有效的 workItemId 时跳过本步

### 第 3 步：解读与汇报

向用户汇报（不要只贴报告路径）：

1. 扫描范围与 spec 目录总数
2. Agent 端到端生成达标率（n/total）
3. 必须件缺失最严重的目录 TOP 3 与缺什么
4. 问题热点结论：高频违反规则 → 对应的物料改进建议（补判例 / 改规则 / 改模板）
5. 报告文件路径

## 判定口径（与 constitution.md 对齐）

| 条件 | 口径 |
|------|------|
| workItemId | spec.md 头部 `**Work Item**: [id](url)`，id 非占位符（workItemId/xxx/todo/tbd 等）且长度 ≥3 |
| spec.md / plan.md 内容达标 | 非空行 ≥15 且含至少一个二级标题 |
| check_reports 达标 | check.summary.md 存在且能解析出 `overall_result: PASS/CONDITIONAL_PASS/FAIL` |
| 必须件 | spec.md、plan.md、check_reports/check.summary.md、check_reports/00-main-chain-report.md、session/conversation-log.md |
| 推荐件 | tasks.md、research.md、data-model.md |

## 注意事项

- 只读扫描：除写报告文件外，不修改任何 spec 目录内容
- 存量 spec 目录缺件是常态，报告如实反映即可，不要替用户补造产出物
- Session 统计依赖 `/session-log-export` 生成的元数据表格式（`| Session | 导出时间 | 用户轮次 | 助手消息数 | 脱敏项 |`），无归档的目录显示"无 session 归档"
