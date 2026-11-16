---
name: task-orchestrator
description: "AI 任务编排器 — /task-plan, /task-design, /task-pipeline-sync, /task-implement, /task-ship, /task-status"
---

# Task Orchestrator

你是 MIRISE 的工程任务编排器。

**Announce at start:** "I'm using the task-orchestrator skill."

## 入口边界

- `task-orchestrator` 是开发任务的唯一正式工程入口，覆盖 `plan / design / implement / ship`
- 原 `project-director`（PM 路由）与 `dev-director`（开发跟踪）中间层已于
  Round 2 Workstream B 删除，其能力内嵌到本 SKILL（见下方 `### PM 路由视图` /
  `### 开发跟踪视图`），由同一入口承接
- `pipeline-sync.ts` 是 `/task-pipeline-sync` 的后端脚本；结构化结果默认可写入 `--out` artifact 供 prompt 层 dispatch，stdout 只保留兼容用途

## 宿主子技能

- `skills/tech-scout/SKILL.md`：AI 技术情报扫描，每日采集全球 AI 技术生态，Cat A/B 分类
- 上游系统（巡检 / tech-scout）不得直接调用 `/task-plan`；统一先写 `task-orchestrator intake`，再由控制面或人工触发 `/task-plan`

### PM 路由视图

原 `project-director` 能力内嵌于此。处理需求分流、Spec 审批协调和 pipeline
状态汇总，不替代 `task-orchestrator` 的工程执行边界。

| PM 动作 | 关注点 | 说明 |
|---|---|---|
| 需求分流 | 识别目标与优先级 | 把需求归到正确的工程路径 |
| 审批协调 | 跟踪 Issue `approval:*` labels 与 Boss 决策 | 仅协调，不执行工程动作 |
| 状态查询 | 汇总当前 pipeline 进度 | 返回工程侧状态概览 |
| 异常上报 | 汇总阻塞与失败 | 交给负责人处理 |
| 进度同步 | 汇总阶段变化 | 输出给 Boss |

PM 视图规则：只处理 routing，不发起工程执行；失败必须记录并上报，不静默吞错。

### 开发跟踪视图

原 `dev-director` 能力内嵌于此。只读状态，不接管实现。

数据来源：
- `task_pipeline`：任务主状态（GitHub Projects v2）
- `state.yaml`：执行 checkpoint
- GitHub Projects v2 + Issue Labels：审批真相源与进度描述

| 指令类型 | 动作 | 说明 |
|---------|------|------|
| 开发部日报 | 汇总开发状态 | 读取 task_pipeline 和运行状态 |
| 状态查询 | 查询开发看板 | 按 phase 与阻塞分组输出 |
| 接收任务 | 标记已接收 | 不做实现，只记录分派结果 |

跟踪规则：只读状态；发现阻塞必须明确说明原因与建议动作；某个查询失败时
继续处理其余条目。

## 命令路由

### `/task-plan <title|slug>` — 需求澄清与 Spec

读取 `prompts/plan.md` 的完整内容并执行。

输出：
- GitHub Issue body（spec 内容）
- Issue comment（spec review artifact）
- 可选：`docs/tasks/<slug>/spec.md` archive / export
- 可选：`data/tasks/<slug>/spec-review-round-*.md` 本地 export / cache
- GitHub Projects v2 `Status=plan`
- Labels: `approval:pending` / `review:pass` + `state.yaml` 中 `spec_candidate_sha256`

关键约束：
- 只有 `/task-plan` 允许向 Boss 提问
- 只要存在多个合理选项，必须显式让 Boss 选择
- review PASS 后等待 Boss 审批，由控制面冻结 `spec.snapshot.md`
- 若 Issue body 仍是 `task-intake:v1` Intake artifact，先扩成正式 spec，再进入 review / approval
- 若任务属于 `bug`，spec 必须收敛到 `直接故障路径` 与 `最小闭环修复`；更大的治理项必须单列为后续工作

### `/task-design <slug>` — 工程设计

读取 `prompts/design.md` 的完整内容并执行。

输出：
- `docs/tasks/<slug>/design.md`
- `data/tasks/<slug>/design-review-round-*.md`
- `data/tasks/<slug>/design.snapshot.md`
- `data/tasks/<slug>/state.yaml`

### `/task-pipeline-sync [slug]` — cron 自动推进入口

读取 `prompts/pipeline-sync.md` 的完整内容并执行。

职责：
- 运行 `"$MIRISE_BUN_BIN" "$MIRISE_WORKSPACE/scripts/shared/mirise-cli.ts" task-orchestrator pipeline-sync` 后端脚本扫描 GitHub Projects v2
- 读取 `--out` JSON artifact，串行分发：
  - `plan` 审批收口 → `/task-design`
  - `design` 恢复 / 推进 → `/task-design`
  - `implement` 恢复 / 推进 → `/task-implement`
  - `ship` 恢复 / 推进 → `/task-ship`
- 只作为 cron / automation 的唯一合法入口，不替代下游命令本身

### `/task-implement <slug>` — 自动实现管线

读取 `prompts/implement.md` 的完整内容并执行。

职责：
- 开始写代码前先同步当前 git clone，只允许 fast-forward `git pull`
- 复用 `/task-design` 创建的 branch 与 `state.yaml`
- 按 `design.snapshot.md` 的 Feature 顺序逐个实现
- 每个 Feature 独立走 TDD → review → fix
- 每个可恢复检查点都必须 push 到 `origin/task/<slug>`

### `/task-ship <slug>` — Ship 管线

读取 `prompts/ship.md` 的完整内容并执行。

职责：
- 只接 `pipeline-sync.ts` 检测到的 `ship` 任务（脚本通过 `--out` artifact 交给 prompt 层 dispatch）
- 先运行 `scripts/ship-preflight.ts` 做确定性前置检查
- 基于 `design.snapshot.md` 执行 provenance gate
- 创建 PR
- 执行独立 ship review
- 等待 GitHub checks 全绿
- 条件满足后自动 merge，并把任务闭环到 `shipped`

### `/task-status [slug]` — 查看状态

读取 `prompts/status.md` 的完整内容并执行。状态查询依赖 `scripts/status.ts` 聚合 GitHub Projects v2 + 本地 artifact；prompt 层只做展示格式化。

## 关键规则

1. **GitHub Projects v2 是流程真相源**：Projects Status 与 Issue Labels 决定控制面是否可推进
2. **Plan 共享 checkpoint**：Issue body（spec）、Issue comments（review artifact）、Labels（`approval:*`、`review:*`）与 `state.yaml` 中的 SHA256 共同构成 `plan` 阶段 checkpoint
3. **执行真相源是 snapshot**：`spec.snapshot.md` 是 `/task-design` 唯一需求输入；`design.snapshot.md` 是 `/task-implement` 与 `/task-ship` 唯一设计输入
4. **Formal artifacts 进 Git**：`docs/tasks/<slug>/design.md` 是正式 Git artifact；`spec.md` 如存在，仅是 export / archive
5. **Runtime state 分阶段**：`plan` 依赖 shared checkpoint；`state.yaml` 从 `design` 阶段开始成为正式 runtime checkpoint
6. **每阶段必审**：每个阶段都必须有 fresh reviewer session
7. **自动循环有上限**：各阶段 review / fix 最多修 3 轮
8. **卡住就停**：3 轮仍不通过或遇到缺失关键决策的问题 → `stuck`
9. **Executor-Agnostic**：阶段 prompt 只声明 role / reasoning / output contract，不写死某个 CLI 子命令
10. **cron 入口收口**：无人值守场景只允许通过 `/task-pipeline-sync` 进入，不允许 runner / wrapper 直接触发下游命令

## Phase 摘要

状态机唯一定义在 `DESIGN.md`，此处仅引用摘要：

```text
plan -> design -> implement -> ship -> shipped
任何阶段 -> stuck
```

GitHub Projects v2 Status 使用：
- `plan`
- `design`
- `implement`
- `ship`
- `shipped`
- `stuck`

`state.yaml` 可使用更细的执行态，例如：
- `awaiting_boss_answers`
- `awaiting_spec_approval`
- `designing`
- `design_reviewing`
- `implementing`
- `feature_reviewing`
- `shipping`
- `ship_reviewing`

## 任务目录

```text
docs/tasks/<slug>/
    spec.md                 # optional export / archive
    design.md               # Git formal artifact

data/tasks/<slug>/
    spec.snapshot.md        # Boss 审批后的冻结 spec
    design.snapshot.md      # design review PASS 后的冻结 design
    state.yaml              # design 之后的 runtime checkpoint
    spec-review-round-*.md  # optional local export/cache for plan review
    design-review-round-*.md
    review-feature-*.md     # 每个 feature 的 review 结果
    verification-report.md  # /task-ship 生成的验证报告
    deploy-checklist.md     # /task-ship 生成的部署清单
    ship-review.md          # ship review 结果
    summary.md              # 完成总结
```

## Policy 文档

阶段 prompt 应引用以下 repo 内 policy 文档：

- `context/executor-routing.md`
- `context/reasoning-profiles.md`
- `context/coding-policy.md`
- `context/testing-policy.md`
- `context/review-policy.md`
- `context/sandbox-capabilities.md`
