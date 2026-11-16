---
name: aliyun-dts-job-manager
description: 创建、查询和管理阿里云数据传输服务 DTS 的数据库同步任务，覆盖同步链路创建、运行状态和同步进度查看、任务重命名，以及任务启动、暂停、恢复和结束。用户提到 DTS、DTS 任务/实例/链路、数据同步、数据库同步、数据迁移期间的全量或增量同步、面向异地数据灾备的跨地域实时同步，或“把一个数据库的数据同步到另一个数据库”时使用。支持以下数据库组合的数据同步：RDS MySQL、PolarDB MySQL 和 PolarDB-X 2.0 之间；RDS PostgreSQL 与 PolarDB PostgreSQL 之间；MongoDB 副本集之间。
---

# 阿里云 DTS 任务管理

## 核心范围

仅创建和管理同账号的单向云数据库同步任务，且源库和目标库必须属于[支持的同步链路](references/supported-links.md#directed-link-groups)。数据库实例或集群、接入方式和所属地域遵循[源库与目标库配置](references/database-instance-configuration.md)；同步对象和参数遵循 [DbList](references/db-list.md)与 [Reserve](references/reserve.md)。

双向或反向同步、跨账号任务、迁移、订阅、数据校验和未登记引擎均不在管理范围内。可以只读查询此类任务，但必须在写操作前停止。

## 核心安全要求

- 不得在对话中接收或处理密钥、凭据、令牌或授权码。身份认证和数据库凭据分别遵循[设置](references/setup.md)与[数据库凭据与连接测试](references/credentials-and-security.md)。
- 每次管理操作前，必须展示脱敏后的目标、关键参数、操作及其计费或生命周期影响，并取得明确确认。计划、参数或操作变化后必须重新确认。
- 核实上一次操作结果前，不得重试管理操作。购买结果不明确时，遵循[恢复流程](references/job-creation.md#purchase-ambiguity-recovery)。
- 只能执行与用户请求匹配且已列入 [API 允许列表](references/api-allowlist.md)的调用。

## 核心工作流

### 创建同步任务

1. 选择已登记的单向链路，按[创建输入要求](references/job-creation.md#creation-choice-elicitation)保留已明确的有效值，仅询问缺失、无效或有歧义的值。运行脚本或调用服务前，解析所有不依赖当前价格的必需非密钥输入，并遵循[目标端已有对象策略](references/reserve.md#existing-destination-object-policy)。
2. 按[准备计划与安全续跑](references/job-creation.md#prepare-and-safe-resume)完成 Profile 检查、报价、v1 计划编译、凭据预检查和两端连接测试。问题修复后续跑原尝试，不得重建公共输入。
3. 仅根据准备阶段返回的面向用户复核内容展示[创建复核](references/job-creation.md#customer-facing-creation-output-requirements)，取得用户对未变化计划的明确确认。修改或取消时，按[待确认计划生命周期](references/job-creation.md#pending-plan-lifecycle)结束旧尝试；修改后启动新尝试。
4. 按[创建流程](references/job-creation.md#purchase-configure-start-workflow)执行已确认且内部绑定未变化的计划，由受控工作流重测连接、购买、配置、启动并观察状态。预检查失败后停止后续管理操作；创建结果不明确或要求核对时，只能按[只读核对流程](references/job-creation.md#attempt-reconciliation)处理同一尝试。

### 查询任务状态

阅读[任务状态](references/job-status.md)，使用其中规定的首选只读快照获取不含密钥的状态摘要。按[标准阶段映射](references/job-status.md#stage-mapping-table)、延迟和预检查规则解释结果，不得根据未知代码推断任务阶段。

用户只提供任务名称时，先按[任务名称定位规则](references/job-status.md#job-name-resolution)做大小写敏感的精确唯一匹配。只有唯一匹配时才可将返回的任务 ID 和实例 ID 用于后续查询或管理；不得选择模糊查询的第一条结果。

### 管理任务生命周期

先通过任务 ID 或精确任务名称定位目标并查询当前状态。根据[任务生命周期](references/job-lifecycle.md)说明操作影响，取得明确确认后执行一次，再查询服务端状态验证结果。

查询、检查或暂停请求不授权结束任务。

## 按任务加载参考文档

| 用户意图 | 需要阅读 |
| --- | --- |
| 验证安装、配置、OAuth 或服务访问 | [设置](references/setup.md) |
| 比较规格或报价 | 先阅读[设置](references/setup.md)，再阅读[实例规格与价格](references/instance-classes-and-pricing.md) |
| 创建任务：选择链路和补全输入 | [支持的同步链路](references/supported-links.md)、[任务创建输入要求](references/job-creation.md#creation-choice-elicitation) |
| 创建任务：进入对应配置阶段 | 按需阅读[源库与目标库配置](references/database-instance-configuration.md)、[DbList](references/db-list.md)、[Reserve](references/reserve.md)、[实例规格与价格](references/instance-classes-and-pricing.md#billing-and-quote-requirements)和[数据库凭据与连接测试](references/credentials-and-security.md) |
| 列出、按名称定位或检查任务状态、查看预检查结果 | [任务状态](references/job-status.md) |
| 重命名或管理生命周期 | [任务生命周期](references/job-lifecycle.md)，并通过[任务状态](references/job-status.md)验证当前状态 |
| 调用 DTS API | 调用前阅读 [API 允许列表](references/api-allowlist.md) |

不得一次加载所有创建类参考文档。
