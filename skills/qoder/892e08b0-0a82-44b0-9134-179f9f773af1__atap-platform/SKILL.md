---
name: atap-platform
description: 与 Atap 测试平台交互，查询或管理认证、设备与远程操作、任务与任务集、执行结果、Bug、测试数据、文件、AI 报告、人工 Review、客户端、NextCI 和 CLI 更新；并支持端到端业务测试任务（如"用最新 Amap 包跑一次北京到天津的模拟导航并返回结果"）。用户提到 Atap、登录或 Token、设备状态/锁定/远控、执行任务、测试结果、Bug、路线/POI、上传文件、报告审核、PC Agent/客户端、NextCI、更新 CLI，或要求完成一个完整测试业务任务时使用。默认优先使用 HTTP；仅当 HTTP 能力缺失或用户明确指定 CLI 时使用 CLI。
---

# Atap Platform

> **版本标识**：本技能文档随仓库持续更新（`git log --oneline -1` 即当前版本）。atap-client 远程会话加载的是**会话启动时的本地副本，可能已落后于仓库最新版**——续跑/参考历史会话结论时，一律以本副本当前内容为准，不沿用旧会话对接口形态的描述；业务任务汇报中如涉及异常绕行，注明所用文档版本日期。

## 核心原则

1. 默认使用 HTTP。
2. HTTP 已覆盖的同一操作只保留一条默认路径。
3. 仅在 HTTP 能力缺失或用户明确选择 CLI 时使用 CLI。
4. 不因失败自动跨 HTTP/CLI 重试写操作。
5. 根页只定义路由、认证、安全和结果语义；参数以对应参考文件为准。
6. 文档能力清单不代表已对线上环境逐条验证。

## 能力路由

| 用户意图 | 默认资料 | CLI 补充 |
|---|---|---|
| **业务测试任务端到端**（"用某包跑某场景并返回结果"等长程任务） | [workflows/test-task-execution.md](workflows/test-task-execution.md) + [advanced-operations.md](advanced-operations.md) | — |
| 认证、登录、凭证状态 | [reference.md](reference.md) | [cli-auth.md](cli-auth.md) |
| 设备查询、锁定、设备组、远程操作 | [reference.md](reference.md) | [cli-device.md](cli-device.md) |
| 任务、任务集、执行与状态 | [reference.md](reference.md) | [cli-task.md](cli-task.md) |
| 测试结果查询或上传 | [reference.md](reference.md) | [cli-result.md](cli-result.md) |
| Bug 查询、上报、状态或评论 | [cli-bug.md](cli-bug.md) | 同左 |
| 测试数据、计划、账号、POI、路线 | [basic-operations.md](basic-operations.md) | [cli-data.md](cli-data.md) |
| 文件上传 | [cli-file.md](cli-file.md) | 同左 |
| AI 报告 | [cli-report.md](cli-report.md) | 同左 |
| NextCI | [cli-nextci.md](cli-nextci.md) | 同左 |
| 报告人工 Review | [cli-review.md](cli-review.md) | 同左 |
| PC Agent、客户端及客户端组 | [cli-pc_agent.md](cli-pc_agent.md) | 同左 |
| CLI 更新 | [cli-update.md](cli-update.md) | 同左 |
| 平台统计（访问/汇总/设备/AI/Token 成本/周报环比） | — | [cli-stats.md](cli-stats.md) |

HTTP 能力保留在 [reference.md](reference.md) 和 [basic-operations.md](basic-operations.md)。CLI 文档用于补充 HTTP 尚未覆盖的能力，不在本页复刻参数。

**业务任务剧本路由**：用户请求完成一个端到端测试业务任务（意图识别→定位测试项→准备数据/包/设备→把测试项组装进任务→触发→汇报结果）时，一律按 [workflows/test-task-execution.md](workflows/test-task-execution.md) 的通用 Loop 执行（测试场景是参数，导航等具体场景只是示例）；剧本用到的测试项/用例/任务组装/包解析/触发/跟踪接口参数以 [advanced-operations.md](advanced-operations.md) 为准。**意图是一串自然语言 App 操作时**（"打开高德地图，从当前位置导航到天安门"——不检索既有测试项/用例，而是让平台 AI 操作智能体在真机执行该操作序列），按剧本"AI 用例执行通道"执行，默认走 instruction 透传（意图转写为操作步骤 → 注入 ti=854 专项脚本AI生成器的 `instruction` 参数）；仅当用户明确要求把意图添加/沉淀到平台时，才 `ai/actionscript/add` 创建用例 → 以 resourceIdList 注入 ti=1265（用例集 1222 体系，只认用例 ID）。剧本各阶段信息缺失或候选不唯一时报错返回，不猜测关键参数。**默认触发即达（2026-10-29 用户确认）**：触发成功拿到 requestId 后，拼接执行详情页链接 `https://atap.amap.com/v1/testresult/redirectToExecutionDetailPageByJobRequestId?jobRequestId=<requestId>` 随汇报输出即结束，**不轮询任务状态**——"把执行结果返回给我"类诉求同样由链接满足（用户打开链接查看执行过程与结果；测试任务异步、远程执行且可能耗时长，一直轮询不合适）；仅当用户明确要求**持续跟踪执行状态/等待终态汇报**时才按剧本阶段 7 跟踪分支轮询。**执行预算纪律（对稳定性至关重要）**：① 接口/参数连续 3 次尝试未命中即报错返回，不猜 URL 不放宽条件——先查文档确认接口存在再调用；② "任意/随便选一个" = 首个满足硬性条件的命中即选定；③ 全量列表等大响应先落文件再提取字段，禁止整体读入上下文；④ 长程任务写运行状态文件断点续跑（稳定路径 `~/.atap/run-state/`，勿用 /tmp），写操作恢复时先查证平台现状不重复提交；⑤ **时间预算**：截止时间解析顺序 = 环境变量 `ATAP_DEADLINE` → 会话上下文文件中的截止时间字段 → **默认本轮消息接收时间 + 30 分钟**；拿到后倒推阶段配额并预留 3-5 分钟收尾，剩余时间不足时立即收尾汇报（已触发则输出链接即止，不启动注定截断的轮询）——宁可提前收尾，不可零汇报全损；⑥ **续跑/历史结论纠偏**：历史会话日志或旧对话上下文中的"接口形态、目录范围、组装策略、执行策略"类结论以当前文档为准重新核对（续跑进入下一阶段前重读 SKILL.md 剧本路由段），旧结论只作线索不作依据。发现平台接口缺口/绕行时记录进 run-state 与汇报。

**经验沉淀路由**：剧本任务 COMPLETED 且用例全 PASS 后，按剧本阶段 8 把本次实测事实写入 [experiences/](experiences/README.md)（固定 schema、去重键、禁止凭证/猜测入库）；写条目即本地 commit（`experience:` 前缀，自动），push 一律等用户明示；多用户环境下经验经 `exp/*` 分支 + MR 由维护者合并并蒸馏（GitLab 消费者需 Developer 角色，main 为 protected branch）。任务失败不沉淀——失败经验走失败分析。

## 通道选择

按以下顺序选择执行路径：

1. 用户明确指定 HTTP 或 CLI 时，使用指定通道。
2. 用户未指定时，先检查 HTTP 参考文件是否覆盖该操作。
3. HTTP 已覆盖时使用 HTTP；否则读取相应 `cli-*.md` 后使用 CLI。
4. 同一操作不得同时给出两个默认方案。
5. 写操作失败后不得自动换通道再次提交。
6. 无法确定操作是否已提交时，先查询当前状态，不得盲目重试。

## 认证

### 个人凭证优先级

按以下顺序寻找个人凭证：

1. 用户本轮明确提供的个人 Token 或环境变量 `ATAP_TOKEN`
2. `~/.atap/config.json`
3. 当前工作目录 `.env`
4. `~/atap-client/.token`

HTTP 使用 `token` 请求头。不得把 Token 放入 URL、命令输出、日志、预览或最终回答。

CLI 自身只读 `~/.atap/config.json`：使用 CLI 时按上述优先顺序解析个人凭证，来源不是 `config.json` 的（如 `ATAP_TOKEN`）先执行 `atap auth login --token "$ATAP_TOKEN"` 写入 CLI 配置再运行业务命令（远程非交互，直接执行，无需用户确认；token 字面值不得出现在命令文本、日志或回答中）；`ATAP_TOKEN` 有值时以其为准，全部来源无值时报错返回。详见 [cli-auth.md](cli-auth.md) "CLI 凭证获取流程"。

### 凭证缺失处理

只接受个人凭证，不提供任何共享身份兜底：

- 未发现任何个人凭证时立即报错返回，提示用户提供个人 token（个人中心 - Token管理）。
- 发现个人凭证但认证无效、损坏或过期时，立即停止并提示更新凭证，不切换其他来源。
- “个人”“我的”等身份相关查询与所有写操作都必须使用个人凭证。
- 不得把权限不足误判成无凭证。
- 不得在文档、脚本或回答中存放任何共享 token。

## 写操作安全门（远程非交互执行）

执行环境为远程环境，执行过程中无法与用户交互确认。**用户的任务请求即视为执行授权：写操作直接执行，不设"先展示摘要、等用户确认后再执行"的中途确认步骤。**

执行任何创建、修改、删除、上传、导入、锁定、释放、运行、远程控制、批量操作或更新前，必须先完成内部核对（不通过则不执行）：

- 操作对象及其规范 ID
- 将使用的通道
- 完整关键参数
- 批量数据规模（行数/字节数）
- 可见副作用
- 是否可能不可逆或触发外部执行

以下情况不执行，直接报错返回，在返回中说明问题并等用户补充指示：

- 操作对象或 ID 不明确、候选不唯一
- 必填参数缺失，无法构造合法请求
- 用户请求与默认安全参数冲突且未明确要求覆盖
- 参考文件与用户输入冲突

默认安全参数（用户请求中明确指定时按用户指定执行）：

- `forceKillJob=false`
- `requireIdle=true`
- 不抢占其他用户持有的锁
- 不终止正在运行的任务以获取设备
- 非幂等写操作不自动重试
- 写操作失败后不自动换通道重试（见"通道选择"）

执行后在结果中如实报告：执行对象、关键参数、结果与副作用；失败时返回完整错误信息，不截断、不改写。

## CLI 执行约定

- CLI 前提：仅当任务需要 CLI 专属操作时才检查 CLI，纯 HTTP 任务不涉及。调用 CLI 前先实测 `ATAP_SKIP_UPDATE=1 ATAP_TELEMETRY=0 atap --version`（`command -v` 依赖 PATH，不可仅凭它断定未安装）；**未安装时不执行任何安装命令**（CLI 不经公开源分发，环境未预装则装不上），按 [cli-update.md](cli-update.md) 报告不可用并改走 HTTP 通道完成等价操作；CLI 专属且无 HTTP 等价的能力如实报错返回，不虚构替代方案。

所有常规 CLI 调用设置：

```bash
ATAP_SKIP_UPDATE=1 ATAP_TELEMETRY=0 atap ...
```

- 默认读取完整 JSON。
- 不默认使用 `--quiet` 或人类可读输出。
- 先读取相应 `cli-*.md`，以其中签名和参数为准。
- 不根据根页示例猜测命令或参数。
- CLI 自更新是独立能力，仅在用户明确提出"更新 CLI"时执行。
- 不使用不存在的 `ATAP_NO_UPDATE`。

## 查询与展示

- 列表默认只展示最相关的 5–10 行，并给出总数。
- 候选对象不唯一时不猜测 ID，停止执行并在返回中列出候选，等用户指定。
- 不为缩短输出而丢弃状态、所有者、时间或关键计数字段。
- 已完成任务默认查询最近 2 天。
- 已完成任务查询最长允许 31 天；这是技能安全策略，不是已证实的服务端限制。
- 超过 31 天时拒绝并请用户缩小范围，不静默截断、拆分或扩大时间范围。

## 异步执行与轮询

- 使用参考文件规定的追踪 ID 查询状态。
- 轮询必须有最大次数或截止时间，并采用有界间隔。
- 批量执行需轮询全部实例，不能以首个实例代表整体结果。
- 超时后报告最后已知状态及未完成实例，不继续无限等待。
- `COMPLETED` 只表示执行结束，不等于测试 `PASS`。
- `UNEXECUTED` 是终态，不能继续按运行中状态轮询。

## ID 规范

以下 ID 不得互换或仅按数值猜测：

- `jobId`
- `jobRequestId`
- `jobExecutionId`
- `taskExecutionId`
- `testResultId`
- `reportId`
- `reviewId`
- `groupId`
- `deviceId`

调用前根据操作对象和参考文件核对 ID 类型。响应字段含义不明确时停止并报错返回，不把一个 ID 填入另一个 ID 参数。

## 路线与字段处理

- 路线途经点的规范格式为 `lon,lat|lon,lat`。
- 收到分号分隔数据时，按规则转换为竖线格式后直接执行，结果中附转换后预览。
- 字段名、别名、配置定义或用户值发生冲突时停止并报错返回。
- 不根据列顺序或相似名称擅自覆盖字段。
- 导入计划数据前先读取目标计划字段定义并校验映射。

## 结果解释

报告任务结果时区分：

- 请求是否受理
- 执行是否结束
- 执行状态
- 用例 PASS/FAIL/跳过/未执行计数
- 是否仍有实例未完成
- 可用的结果、报告或 Review 标识

不得仅凭 HTTP 成功、CLI 退出码为零或状态 `COMPLETED` 宣称测试通过。

## 参考文件

所有参考文件均由本页直接引用，只使用一层引用：

- [reference.md](reference.md)
- [basic-operations.md](basic-operations.md)
- [advanced-operations.md](advanced-operations.md)
- [workflows/test-task-execution.md](workflows/test-task-execution.md)
- [examples.md](examples.md)
- [cli-auth.md](cli-auth.md)
- [cli-device.md](cli-device.md)
- [cli-task.md](cli-task.md)
- [cli-result.md](cli-result.md)
- [cli-bug.md](cli-bug.md)
- [cli-data.md](cli-data.md)
- [cli-file.md](cli-file.md)
- [cli-report.md](cli-report.md)
- [cli-nextci.md](cli-nextci.md)
- [cli-review.md](cli-review.md)
- [cli-pc_agent.md](cli-pc_agent.md)
- [cli-update.md](cli-update.md)
- [cli-stats.md](cli-stats.md)
