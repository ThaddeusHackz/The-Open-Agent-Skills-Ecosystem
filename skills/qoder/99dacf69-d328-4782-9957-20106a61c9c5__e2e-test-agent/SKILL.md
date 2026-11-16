---
name: e2e-test-agent
description: 端到端交付2.0阶段六的测试 Agent——输入 spec 目录，从 spec.md/plan.md 生成 API 接口测试用例与浏览器 E2E 测试用例（存入 specDir/test_cases/），随后执行测试（curl 调接口 + Browser Agent 操控浏览器），输出 Bug 清单与执行报告到 specDir/test_reports/。当用户要求"跑测试"、"生成并执行测试"、"测试验证"、自检通过后进入测试阶段、或 /e2e-flow 进入阶段六时使用。
version: 1.0.0
---

# e2e-test-agent：测试 Agent

自检（静态审查）通过后的**动态验证**角色：生成用例 → 真实执行 → 输出报告，一个技能走完。
与自检的分工：自检看代码写得对不对，测试 Agent 验证功能跑起来对不对。

## 触发方式

- `/e2e-test-agent <specDir>` —— 生成用例并执行全部测试
- `/e2e-test-agent <specDir> --gen-only` —— 只生成用例，不执行（simple 级默认行为）
- `/e2e-test-agent <specDir> --run-only` —— 用例已存在，只执行
- `/e2e-test-agent <specDir> --type api` —— 只跑 API 测试（或 `--type e2e` 只跑浏览器测试）

## 边界声明

- 测试针对 **dev 开发环境**执行（执行前将功能分支发布到 dev），禁止对生产环境做任何写操作
- 不修改业务代码；发现 Bug 记录证据，修复由编码会话负责
- 测试数据允许通过接口构造，禁止直接改库删数据
- 存在 P0 Bug 时必须在汇报中明确说明"阻塞归档"

## 执行流程

### 第 1 步：读取环境配置

读取 `.qoder/config/e2e-test-env.md`（模板见 `assets/test-env-config-template.md`）：

- 存在 → 展示配置摘要，让用户确认或覆盖
- 不存在 → 按模板逐项询问用户（后端 API base URL、前端页面 URL、测试账号、认证方式），
  生成配置文件后继续
- 密码优先读配置文件（dev 环境允许明文保存）；配置中缺失时运行时向用户索取

### 第 2 步：读取 spec 上下文

1. `{specDir}/spec.md` → FR 功能需求、SC 成功标准、User Story（Given-When-Then）、Level 分级
2. `{specDir}/plan.md` → 接口定义、模块划分、主流程
3. 若存在 `{specDir}/contracts/` 或 `api-doc.md` → 提取精确的接口路径、请求/响应结构
4. 若存在 `{specDir}/check_reports/04-impact-analysis.md` → 将影响面中标注的风险点纳入用例设计
5. spec.md 缺失 → 终止，提示先走 `/e2e-flow` 补齐

### 第 3 步：生成测试用例

写入 `{specDir}/test_cases/`（模板见 `assets/test-case-template.md`）：

| 文件 | 内容 |
|------|------|
| `api-cases.md` | API 接口测试用例（TC-API-xxx） |
| `e2e-cases.md` | 浏览器 E2E 测试用例（TC-E2E-xxx） |

**用例设计要求：**

- 每条 FR 至少 1 条正向用例；每个接口覆盖：正向 + 必填参数缺失 + 非法参数 + 未认证访问
- User Story 的每个 Given-When-Then 场景转化为 1 条 E2E 用例
- 每条用例必须含：用例 ID、优先级（P0/P1/P2）、前置条件、步骤、预期结果（可断言）
- 优先级判定：核心流程/鉴权/数据安全 = P0；常规功能/边界/异常 = P1；文案/样式 = P2
- 用例总数与 spec 规模匹配，宁精勿滥——每条用例必须可独立执行且断言明确

**幂等规则**：`test_cases/` 已存在时，对比 spec 是否有变更；无变更直接复用，有变更增量更新并保留原用例 ID。

### 第 4 步：部署功能分支到开发环境

测试针对 **dev 环境**执行，执行前确保当前功能分支已发布：

1. 确认代码变更已提交并推送到远程功能分支（feature/xxx）
2. 调用 `/yunxiao-appstack-deploy` 将本次变更涉及的应用（backend / frontend）发布到 **dev** 环境
3. 用 `list_app_release_stage_metadata` 校验实际构建的 releaseBranch / releaseRevision 与功能分支最新 commit 一致
4. dev 环境已是该分支最新部署（分支 + commit 一致）→ 跳过重复发布；发布失败 → 终止测试并汇报

### 第 5 步：执行 API 测试

用 curl 逐条执行 `api-cases.md` 中的用例：

1. **认证准备**：按配置的认证方式获取凭证（登录接口换 token / 用户提供的 API Key）
2. **逐条执行**：发请求 → 比对响应状态码、响应体关键字段与预期断言
3. **判定**：passed / failed（断言不符）/ skipped（依赖阻塞，注明原因）
4. failed 立即记录 Bug（见第 7 步），继续执行不中断
5. 涉及写操作的用例：执行后用查询接口验证数据落库正确性；测试产生的数据在备注中登记

### 第 6 步：执行浏览器 E2E 测试

通过 **Browser 子代理**执行 `e2e-cases.md` 中的用例：

1. 单批次派发不超过 15 条用例，避免子代理上下文过载
2. 先登录一次，后续用例复用登录态；登录态失效自动重登
3. 页面导航优先走导航菜单/页面链接，禁止猜测 URL
4. 遇浏览器原生弹窗用 handle_dialog 自动处理，不等待人工
5. 失败用例必须截图，存 `{specDir}/test_reports/screenshots/`
6. 禁止执行会触发登出的操作（清 token、点登出）——此类用例标记 skip 并归入人工验证清单

### 第 7 步：Bug 记录

发现即记录到 `{specDir}/test_reports/bugs.md`，每条 Bug 必含：

Bug ID、关联用例 ID、优先级、标题、复现步骤、预期 vs 实际、截图（E2E）/请求响应原文（API）、指派对象（前端/后端/产品，按证据判定）、发现时间。

### 第 8 步：生成执行报告

写入 `{specDir}/test_reports/test-report-{YYYYMMDD-HHmmss}.md`（模板见 `assets/test-report-template.md`），包含：

- 测试概要（环境、范围、时长）
- 结果统计（总数/通过/失败/跳过、通过率、按类型 API/E2E 分列）
- 失败用例明细 + Bug 汇总
- 用例执行清单（每条用例的最终状态，禁止遗漏）
- 需人工验证清单（无法自动化的用例 + 原因 + 验证要点）

### 第 9 步：结果判定与汇报

| 结果 | 判定 | 动作 |
|------|------|------|
| 0 Bug | **PASS** | 可进入收尾归档 |
| 仅 P2 | **PASS_WITH_ISSUES** | 记录在案，不阻塞归档 |
| 有 P1 | **CONDITIONAL_PASS** | 建议修复后用 `--run-only` 重测失败用例 |
| 有 P0 | **FAIL** | **阻塞归档**，修复后必须重测 |

向用户汇报：判定结果、通过率、Bug 清单（按优先级）、报告路径。FAIL 时列出阻塞项与修复建议顺序。

## Level 分级差异

| 项 | standard | simple |
|----|----------|--------|
| 用例生成 | API + E2E 全量 | 仅生成用例文档（--gen-only） |
| 执行 | API + E2E 自动执行 | 人工执行，技能不跑 |
| 报告 | 完整执行报告 | 无（用例文档即产出） |

## 目录产出

```
{specDir}/
├── test_cases/
│   ├── api-cases.md
│   └── e2e-cases.md
└── test_reports/
    ├── test-report-*.md
    ├── bugs.md
    └── screenshots/
```
