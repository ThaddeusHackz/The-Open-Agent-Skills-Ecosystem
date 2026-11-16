---
name: fe-e2e-dev
description: 前端全流程 AI 开发总控——输入前端 spec 目录，自动执行 Spec同步 → 视觉提取 → Plan完善 → 分批编码 → 自检 → 测试 → 提交归档 的端到端流水线，支持断点续跑。当用户要求"前端全流程开发"、"AI 开发迭代"、"按 spec 完成前端需求"或使用 /fe-e2e-dev 时触发。
---

# fe-e2e-dev：前端全流程 AI 开发总控

以一个前端 spec 目录为输入，串联现有 skill 体系，走完"需求同步 → 编码 → 质检 → 测试 → 归档"的完整闭环。
本 skill 是**流程编排者**：上下游各环节均通过调用既有 skill 完成，本 skill 只负责阶段推进、门禁判定、
失败回环与断点续跑，不重复实现任何单环节能力。

## 触发方式

- `/fe-e2e-dev <specDir>` —— 从阶段 1 起执行全流程
- `/fe-e2e-dev <specDir> --from <阶段号>` —— 断点续跑，从指定阶段（1~7）开始
- `/fe-e2e-dev <specDir> --quick` —— 快速模式：编码后仅做 P0 级验证（tsc + build + P0 用例），跳过多视角自检扩展报告

specDir 约定为前端 spec 目录，格式：

```
fe-project/mcp-market-fe-project/specs/{编号}-{名称}/
```

如 `fe-project/mcp-market-fe-project/specs/005-api-key/`。

## 前置条件

- specDir 存在且至少包含 `spec.md`（缺失则终止，提示先运行 `/sync-fe-spec` 初始化）
- 产品需求源位于 `product-project/v{日期}-{版本}/`（如 `product-project/v20260718-0.15/`），
  含 Changelog.md 与 Demo HTML
- 工作目录可执行 `pnpm`（前端项目根：`fe-project/mcp-market-fe-project/`）

## 边界声明

- 编码阶段的硬约束见 [references/coding-rules.md](references/coding-rules.md)，任何一条不得违反
- 阶段 7 推送远端前**必须请用户确认**，未经确认不得 push
- 禁止 force push、禁止推送 release 及 release/xxx 流水线分支（详见 [references/project-conventions.md](references/project-conventions.md)）
- 各下游 skill（自检、测试、归档）只调用不修改其内部逻辑

---

## 七阶段流程

整体链路（全链路细节与产物路径见 [references/pipeline-overview.md](references/pipeline-overview.md)）：

```
1 Spec同步 → 2 视觉提取 → 3 Plan/Tasks完善 → 4 编码执行 ⇄ 5 自检 ⇄ 6 测试 → 7 提交归档
                                                  ↑___________回环修复___________|
```

### 阶段 1：Spec 同步

| 项 | 内容 |
|----|------|
| 输入 | `product-project/v{最新}/Changelog.md`、现有 `{specDir}/spec.md`、`tasks.md` |
| 动作 | 调用 `/sync-fe-spec`，对比产品 Changelog，增量更新 spec.md / tasks.md / api-contracts.md（有新页面/组件时其 Step 4 还会更新 component-map.md） |
| 输出 | 更新后的 spec.md、tasks.md、api-contracts.md、component-map.md（如适用）+ 变更摘要 |
| EXIT GATE | spec 覆盖 Changelog 全部变更项（逐条比对，无遗漏项） |
| 失败处理 | 存在未覆盖变更项 → 重新执行同步补齐；产品物料本身缺失 → 中止并提示用户补充产品版本目录 |

**跳过条件**：无新产品版本（spec.md 顶部"最后同步版本"已是最新）→ 标记 SKIP，直接进入阶段 2。

### 阶段 2：视觉提取

| 项 | 内容 |
|----|------|
| 输入 | `product-project/v{最新}/` 下的 Demo HTML |
| 动作 | Demo HTML 相对上次提取有更新时，调用 `/extract-demo-visual` 提取视觉参数与截图 |
| 输出 | `{specDir}/visual-reference.md`（+ `screenshots/` 截图） |
| EXIT GATE | 无硬门禁（软性阶段） |
| 失败处理 | **仅警告不阻塞**：记录"视觉参考缺失/过期"到进度文件，继续进入阶段 3；编码时以现有 visual-reference.md 或 Demo 源码为准 |

**跳过条件**：Demo 无更新且 visual-reference.md 已存在 → SKIP。

### 阶段 3：Plan/Tasks 完善

| 项 | 内容 |
|----|------|
| 输入 | `{specDir}/spec.md`、`plan.md`（可能缺失/空模板）、`component-map.md`、`api-contracts.md` |
| 动作 | ① plan.md 缺失或为空模板时，基于 spec.md 补齐：模块划分、接口定义、主流程设计；② 校验 component-map.md（组件 → 文件路径映射表）与 api-contracts.md 的完整性——spec 中每个页面/组件都应有落盘路径映射，每个前端调用的接口都应有契约条目 |
| 输出 | 完善后的 plan.md；完整性校验结论 |
| EXIT GATE | component-map.md 与 api-contracts.md 均存在且完整 |
| 失败处理 | 二者缺失或不完整 → **中止流程**，输出"待补字段清单"（缺哪个组件的路径映射、缺哪个接口的契约、缺哪些字段定义），请用户补齐后用 `--from 3` 续跑 |

> 范本参考：`specs/001-homepage-visual-refactor/` 是目前唯一 6 件套齐全（含 plan.md、component-map.md、visual-reference.md）的 spec，可作为补齐 plan.md 的结构参照。

### 阶段 4：编码执行

| 项 | 内容 |
|----|------|
| 输入 | `{specDir}/tasks.md`、plan.md、component-map.md、api-contracts.md、visual-reference.md |
| 动作 | 按 tasks.md 的 **Phase 分批**编码（tasks.md 无 Phase 划分时按 **User Story** 分批）；每批严格遵循 [references/coding-rules.md](references/coding-rules.md) 硬约束 |
| 输出 | 源码变更 + tasks.md 勾选进度更新 |
| EXIT GATE | 每批完成后在 `fe-project/mcp-market-fe-project/` 下运行：① `pnpm exec tsc --noEmit` —— 类型错误**零新增**（存量基线 5 个已知错误，见 coding-rules）；② `pnpm build` —— 构建成功 |
| 失败处理 | 验证失败 → 定点修复（只改本批引入问题的文件）→ 重验；同一批**三次仍失败** → 中止，输出错误清单（文件 + 错误信息 + 已尝试的修复），请用户介入 |

编码风格、文件落盘、禁令等硬约束全部收敛在 coding-rules.md，此处不重复。

### 阶段 5：自检

| 项 | 内容 |
|----|------|
| 输入 | specDir + 阶段 4 产生的代码变更（git diff） |
| 动作 | 调用 `/e2e-self-check {specDir}`，以独立视角做多角色质检 |
| 输出 | `{specDir}/check_reports/`（check.summary.md + 主链路报告 + 三视角报告） |
| EXIT GATE | overall_result 为 PASS 或 CONDITIONAL_PASS |
| 失败处理 | **FAIL** → 带着 check_reports 的问题清单回到阶段 4 定点修复（`--fix-scope` 限定为问题涉及的文件，禁止扩大修改面），修复后**重跑自检**（回环上限见下方"回环重试上限"）；**CONDITIONAL_PASS** → 可继续进入阶段 6，但将 MAJOR 问题记录到进度文件，归档汇报中提示 |

**`--quick` 模式下的行为**：与触发段描述一致，本阶段按 e2e-self-check 的 simple 级执行——只做主链路检查（check.summary.md + 00-main-chain-report.md），**跳过 01~03 三视角扩展报告与 04 影响面报告**；EXIT GATE 判定规则不变。

### 阶段 6：测试

| 项 | 内容 |
|----|------|
| 输入 | specDir、`test-project/test-config.md`（测试环境地址/账号） |
| 动作 | ① 用例准备：首次（无既有用例）调用 `/generate-test-cases`；已有用例且本轮 spec 有变更 → 调用 `/update-test-cases` 增量同步；② 执行：调用 `/e2e-test-agent {specDir}` 跑 API + 浏览器 E2E 测试 |
| 输出 | `{specDir}/test_cases/`、`{specDir}/test_reports/`（Bug 清单 + 执行报告）；双版本用例同步到 `test-project/ai-version/` + `manual-version/` |
| EXIT GATE | **P0 用例全部通过** |
| 失败处理 | 出现 P0 Bug → 回环阶段 4 定点修复 → 重跑**受影响用例**（复用已生成用例，`/e2e-test-agent {specDir} --run-only`，仅重执行不重新生成）；非 P0 Bug 记录到 Bug 清单，不阻塞（--quick 模式下仅执行 P0 用例） |

**回环重试上限**（适用于 5→4→5 与 6→4→6 两类回环）：同一阶段的回环修复**最多 2 轮**。第 2 轮后自检仍 FAIL / 仍有 P0 Bug 未通过 → **中止流程**，向用户汇报剩余问题清单（问题描述 + 证据 + 已尝试的修复），由用户决定后续处理；回环轮次记录在进度文件对应阶段的 `note` 中。此上限独立于阶段 4 内部的编译层"同一批三次验证失败即中止"规则，二者并行生效。

### 阶段 7：提交归档

| 项 | 内容 |
|----|------|
| 输入 | 全部代码变更 + spec 产物变更 |
| 动作 | 见下方步骤 ①~⑤ |
| 输出 | feature 分支提交并推送、test 分支合并推送、`{specDir}/session/conversation-log.md` |
| EXIT GATE | 推送成功 + 会话归档落盘 |
| 失败处理 | push 被拒 → 先 `git pull --rebase` 同步后重推；仍失败输出远端错误信息请用户处理，**禁止 force push** |

提交步骤（借助 `/git-ops` 执行，遵循其安全分级）：

1. **Conventional Commits 中文提交**，遵循本项目两笔惯例：
   - 第一笔：源码变更 `feat(模块): 中文描述` / `fix(模块): 中文描述`
   - 第二笔：构建产物 `build: 更新 dist 构建产物`（dist 下被跟踪文件，见 coding-rules）
2. **推送前必须请用户确认**（展示分支名、提交列表、目标远端），未确认不得 push
3. push 当前 feature 分支（如 `feature/v0.15`）
4. merge 到 **test 分支**并推送（普通 merge，非 fast-forward 亦可）。
   ⚠️ **release 分支已废弃不可推送**；**禁止触碰 release/xxx 流水线分支**；**禁止 force push**（详见 project-conventions.md）
5. 调用 `/session-log-export {specDir}` 归档本次会话到 `{specDir}/session/`

---

## 断点续跑

进度持久化到 `{specDir}/.fe-flow-progress.json`，每个阶段结束（PASS/SKIP/FAIL）时立即写入：

```json
{
  "specDir": "fe-project/mcp-market-fe-project/specs/005-api-key/",
  "mode": "full",
  "stages": {
    "1": { "status": "PASS", "outputs": ["spec.md", "tasks.md"], "time": "2026-07-31T10:00:00+08:00" },
    "2": { "status": "SKIP", "outputs": [], "time": "2026-07-31T10:02:00+08:00", "note": "Demo 无更新" },
    "3": { "status": "PASS", "outputs": ["plan.md"], "time": "2026-07-31T10:10:00+08:00" }
  },
  "current": 4
}
```

规则：

- `status` 取值：`PASS` / `SKIP` / `FAIL` / `IN_PROGRESS`
- 恢复时（`--from` 或检测到进度文件后询问用户）：跳过 `PASS`/`SKIP` 阶段，从 `current` 或用户指定阶段继续
- 回环修复（5→4、6→4）时把阶段 4 重置为 `IN_PROGRESS` 并在 `note` 中记录回环原因
- 这是**纯流程指令**：由 Agent 按本文档读写 JSON 推进，不引入任何执行器脚本
- 全流程完成后进度文件保留，作为本轮迭代的执行留痕

## 与现有 skill 的协作关系

| 位置 | Skill | 何时调用 | 关系 |
|------|-------|----------|------|
| 上游 | `/sync-fe-spec` | 阶段 1 | 只调用，产出 spec 增量更新 |
| 上游 | `/extract-demo-visual` | 阶段 2 | 只调用，产出 visual-reference.md |
| 编码规范 | `fe-code-standards` | 阶段 4 | 只读取其规范作为编码依据 |
| 下游 | `/e2e-self-check` | 阶段 5 | 只调用，产出 check_reports/ |
| 下游 | `/generate-test-cases` | 阶段 6（首次） | 只调用，产出双版本测试用例 |
| 下游 | `/update-test-cases` | 阶段 6（增量） | 只调用，同步用例变更 |
| 下游 | `/e2e-test-agent` | 阶段 6（执行） | 只调用，产出 test_cases/ + test_reports/ |
| 下游 | `/git-ops` | 阶段 7 | 只调用，执行提交/推送/合并 |
| 下游 | `/session-log-export` | 阶段 7 | 只调用，归档 session/ |

以上 skill 均位于 `.qoder/skills/`，本 skill **只调用不修改**它们的任何文件。

## 汇报格式

全流程结束（或中止）时向用户汇报：

```
## fe-e2e-dev 执行汇报 — {specDir}

| 阶段 | 状态 | 关键产出 |
|------|------|----------|
| 1 Spec同步   | PASS/SKIP | 变更 n 项 |
| 2 视觉提取   | PASS/SKIP/WARN | visual-reference.md |
| 3 Plan完善   | PASS | plan.md |
| 4 编码执行   | PASS | n 个文件，tsc 零新增，build 成功 |
| 5 自检       | PASS/CONDITIONAL_PASS | check_reports/（MAJOR n 个） |
| 6 测试       | PASS | P0 全过，遗留非 P0 Bug n 个 |
| 7 提交归档   | PASS | commit x2、push feature + test、session/ |

遗留事项：{CONDITIONAL_PASS 的 MAJOR 项 / 非 P0 Bug / TODO 契约清单}
```

## 引用

- [references/coding-rules.md](references/coding-rules.md) —— 阶段 4 编码执行硬约束
- [references/pipeline-overview.md](references/pipeline-overview.md) —— spec 体系全链路梳理与产物路径表
- [references/project-conventions.md](references/project-conventions.md) —— 项目约定速查（命令/分支/提交/测试环境）
