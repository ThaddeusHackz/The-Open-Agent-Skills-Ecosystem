---
name: optimal-architecture-algorithm
description: 架构与算法选型决策引擎。当用户面临技术选型决策时自动触发——包括"选什么数据结构/算法/架构模式/分布式组件/缓存策略/消息队列模式/微服务方案"等对比类提问，或出现"推荐一个方案""用什么最好""X 和 Y 怎么选"等意图。输出：Top-1 推荐 + Top-2 备选 + 适用边界 + 风险警告 + 反直觉纠偏 + 启发式提示。实现即包含验证：推荐本身必须可解释、可追溯、可证伪。不适用于：纯代码实现细节、已指定唯一技术栈后的具体编码、不涉及选型的日常问题。
---

# 架构与算法选型决策引擎

## 定位

本 skill 解决的是"在约束条件下的局部最优选择"问题。它不做穷举式百科，只回答一个具体问题："给定我的场景，现在该用什么？"

核心承诺：
1. 一次调用即可得到可执行的推荐
2. 每个推荐都有约束映射关系（为什么适配）
3. 每个推荐都明确边界（什么时候会失效）
4. 每个推荐都纠偏常见认知偏差

## 目录结构

```
optimal-architecture-algorithm/
├── SKILL.md                         # 本文件：核心协议
├── templates/
│   ├── entry-template.md            # 知识条目模板
│   └── anti-pattern-template.md     # 反直觉条目模板
└── knowledge/
    ├── _index.md                    # 类别索引 + 路由表（含状态列）
    ├── _relations.md                # 条目间关系图谱
    ├── _anti-patterns.md            # 常见认知偏差库
    ├── data-structures.md           # 各类别文件格式统一：
    ├── sorting-searching.md         #   文件头为「条目速览表」（粗筛用），
    ├── graph-algorithms.md          #   其后为条目全文（深读用）；
    ├── distributed-systems.md       #   未建档类别带「状态：TODO stub」横幅
    ├── caching-strategies.md
    ├── message-queue-patterns.md
    └── microservice-architecture.md
```

## 4-Phase 交互协议

```
Phase 1: 约束解析（Parse）
    → 提取 6 维决策向量
    → 检测约束矛盾
    → 识别用户表述中的反直觉假设
    输出：决策向量 V + 已识别反直觉点 + 需要追问的关键项

Phase 2: 路由与匹配（Route & Match）
    → 读 _index.md 确定目标类别（含状态列检查）
    → 状态为 TODO stub 的类别：跳过加载，走 stub fallback
    → 加载 1-2 个就绪类别文件，先读文件头「条目速览表」粗筛候选
    → 深读通过粗筛的条目全文
    → 加载 _relations.md 当涉及跨条目关联时
    → 用定性评分表评估每个候选条目
    输出：候选列表 + 评分矩阵

Phase 3: 验证与告警（Validate & Alert）
    → 偏离检测：用户场景 vs 推荐方案最佳场景
    → 反直觉校验：用 _anti-patterns.md 纠偏
    → 启发式提示：放宽哪个约束可解锁更优方案
    输出：风险警告 + 纠偏提示 + 启发式提示

Phase 4: 输出（Output）
    → 按固定模板输出推荐报告
```

### Phase 1: 约束解析

从用户描述中提取 6 维决策向量：

| 维度 | 取值示例 | 提取规则 |
|------|---------|---------|
| **data_scale** | `tiny`(<1K) / `small`(K) / `medium`(10K-1M) / `large`(1M-100M) / `massive`(>100M) | 从"百万级/千万级/亿级"等量词提取；提取不到时默认 `medium` |
| **read_write** | `read_only` / `read_heavy` / `balanced` / `write_heavy` / `write_only` | 从"读多写少/读写均衡/只写"等词提取；默认 `balanced` |
| **latency** | `sub_ms` / `ms` / `sub_second` / `second` / `batch` | 从"实时/毫秒/秒级/离线批处理"提取；默认 `ms` |
| **consistency** | `strong` / `eventual` / `causal` / `none` | 从"强一致/最终一致/因果一致"提取；默认 `eventual` |
| **resources** | `memory_bound` / `cpu_bound` / `io_bound` / `network_bound` / `unconstrained` | 从"内存受限/CPU密集/IO瓶颈"提取；默认 `unconstrained` |
| **system_scale** | `single_node` / `small_cluster` / `cluster` / `geo_distributed` | 从"单机/集群/跨地域"提取；默认 `small_cluster` |

**约束矛盾检测**：

如果同时出现以下不可能三角，立即指出并停止推荐，要求用户调整约束：
- `latency=sub_ms` + `consistency=strong` + `system_scale=geo_distributed`（CAP 不可能三角）
- `resources=memory_bound` + `data_scale=massive` + `latency=sub_ms`（必须牺牲精确度）
- `read_write=write_heavy` + `consistency=strong` + `latency=sub_ms`（必须分片或异步化）

**追问规则（硬性上限）**：

- 最多追问 **1 轮**，最多 **2 个问题**
- 只追问影响推荐结果的关键维度（data_scale / read_write / latency / consistency）
- 如果追问后仍无法提取，使用默认值并在输出中**显式列出假设**
- 不允许因约束缺失而拒绝输出

**反直觉假设识别**：

读取 `_anti-patterns.md`，检查用户原始描述中是否包含这些模式：
- "二分查找一定比哈希快" → 命中 AP-001
- "微服务一定比单体灵活" → 命中 AP-002
- "强一致一定比最终一致安全" → 命中 AP-003
- "Redis 一定比数据库快" → 命中 AP-004
- 命中后在 Phase 3 输出中引用对应纠偏内容

### Phase 2: 路由与匹配

**类别路由**：

读取 `knowledge/_index.md`，根据用户问题中的关键词确定目标类别：

| 用户问题关键词 | 目标类别 |
|--------------|---------|
| 去重/计数/近似的成员查询 | `data-structures` |
| 排序/搜索/TopK | `sorting-searching` |
| 最短路径/图遍历/依赖/推荐 | `graph-algorithms` |
| 共识/一致性/分片/复制 | `distributed-systems` |
| 缓存/命中/过期/淘汰 | `caching-strategies` |
| 队列/事件流/发布订阅/异步 | `message-queue-patterns` |
| 服务拆分/边界/通信/治理 | `microservice-architecture` |

**加载策略**：
- 大多数查询只加载 **1 个类别文件**
- 仅当问题明确跨类别（如"分布式缓存一致性"涉及 `caching-strategies` + `distributed-systems`）时加载 2 个
- 严禁一次性加载全部 7 个类别文件
- 加载后先读文件头的**条目速览表**（条目 / 子类 / 核心问题 / 最佳场景快照）做候选粗筛，只深读通过粗筛的条目全文；速览表即"命中时的一手数据"，无需全量深读
- **stub fallback**：目标类别在 `_index.md` 状态列为 `TODO stub` 时，不加载该文件，基于通用知识推荐，并在输出的「引用来源」处显式标注"该类别知识库尚未建档，本推荐未引用知识条目"，禁止伪造引用

**评分方式（定性评分表）**：

不使用 AI 心算数值，改用定性等级：

| 维度 | Strong Match | Match | Weak Match | Mismatch |
|------|-------------|-------|-----------|----------|
| **场景适配** | 用户所有关键维度落在条目最佳场景区间内 | 大部分维度匹配，1 个维度轻微偏离 | 关键维度部分偏离 | 核心维度冲突 |
| **复杂度可接受** | 在当前 data_scale 下，条目复杂度完全可接受 | 可接受，但需要优化 | 可接受，但接近上限 | 不可接受 |
| **运维成本** | 单机/无状态/已验证 | 需要少量配置 | 需要集群/调优 | 需要自研/重运维 |

排序规则：
1. Strong Match 数量多者优先
2. 无 Mismatch 者优先
3. 运维成本低者优先
4. 取 Top-3；Top-1 为推荐，Top-2/3 为备选

### Phase 3: 验证与告警

**偏离检测**：

对 Top-1 推荐，逐条检查用户决策向量 V 与条目`最佳场景`的匹配情况：
- 任何维度偏离 → 输出风险警告（格式见输出模板）
- 核心维度（data_scale / latency / consistency）偏离 → 必须给出降级建议

**反直觉校验**：

将 Phase 1 识别到的反直觉点，与 `_anti-patterns.md` 中的条目对应：
- 输出"纠偏：{用户原话} 实际上 {正确理解}"
- 如果推荐本身恰好印证了用户的反直觉假设，要特别标注

**启发式提示**：

扫描评分矩阵，寻找"放宽一个约束即可升级推荐"的机会：
- "如果你能接受 `consistency=eventual`，则 {某方案} 的复杂度从 O(n) 降到 O(log n)"
- "如果 `data_scale` 能从 `massive` 降到 `large`，则 {某方案} 可直接使用成熟组件而非自研"
- 必须给出量化收益，禁止空泛提示

### Phase 4: 输出格式

```markdown
## 推荐方案：{名称}

**核心理由**：{1-2 句，直接映射到用户的约束条件}

### 场景匹配度

| 维度 | 你的约束 | 推荐方案最佳场景 | 匹配结果 |
|------|---------|----------------|---------|
| 数据规模 | {value} | {value} | Strong Match / Match / Weak Match / Mismatch |
| 读写比例 | {value} | {value} | ... |
| 延迟要求 | {value} | {value} | ... |
| 一致性 | {value} | {value} | ... |
| 资源约束 | {value} | {value} | ... |
| 系统规模 | {value} | {value} | ... |

### 三维度评估

| 维度 | 推荐 {A} | 备选 {B} | 备选 {C} |
|------|---------|---------|---------|
| 场景适配 | Strong Match | Match | Weak Match |
| 复杂度可接受 | 可接受 | 可接受 | 接近上限 |
| 运维成本 | 低 | 中 | 高 |

### 风险警告（仅当存在偏离时）

> 你的约束在 **{维度}** 上偏离该方案最佳场景：
> {具体风险描述}
> 降级建议：{备选方案 + 需要接受的 tradeoff}

### 反直觉纠偏（仅当命中时）

> {用户原话/隐含假设} → 实际上 {正确理解}。
> 该推荐 {验证/反驳} 了这个假设。

### 启发式提示

> 如果你能调整 **{约束}**（从 {当前} 放宽到 {建议}），
> {更优方案} 将表现显著更优：{量化收益}。

### 做出的假设

- {假设1：用户未说明，按默认值处理}
- {假设2：}

### 引用来源

- {推荐条目来源：knowledge/xxx.md #条目名}
- {反直觉来源：knowledge/_anti-patterns.md #AP-xxx}
```

## 知识条目规范

每个条目必须严格遵循 `templates/entry-template.md`，包含 10 个字段：

1. 名称
2. 类别
3. 核心问题
4. 时间复杂度
5. 空间复杂度
6. 最佳场景（6 维向量表示）
7. 优势
8. 劣势/陷阱
9. 反直觉提示
10. 落地案例
11. 相关条目（graph 关系）
12. 替代方案对比

最佳场景必须使用 6 维向量的标准取值，例如：

```markdown
- **最佳场景**：
  - data_scale: medium ~ large
  - read_write: read_heavy ~ balanced
  - latency: ms
  - consistency: eventual
  - resources: memory_bound
  - system_scale: single_node ~ small_cluster
```

## 关系图谱规则

`knowledge/_relations.md` 用于表达条目间关系，格式：

```markdown
### {关系类型}: {条目 A} → {条目 B}

- **关系**：{is_alternative_to / commonly_used_with / successor_of / tradeoff_with}
- **说明**：{一句话解释}
```

关系类型必须标准化为：
- `is_alternative_to`：可互相替代
- `commonly_used_with`：常搭配使用
- `successor_of`：演进/升级关系
- `tradeoff_with`：同一问题的不同 tradeoff 选择

当 Top-1 推荐涉及关系时（如选了 CQRS 可能需要 Event Sourcing），在输出中追加"关联建议"。

## 反直觉机制

`_anti-patterns.md` 中每个条目格式：

```markdown
### AP-{编号}: {反直觉表述}

- **常见说法**：{用户常挂在嘴边的错误认知}
- **正确理解**：{一句话纠偏}
- **典型后果**：{信了会有什么后果}
- **相关条目**：{哪些推荐方案涉及此纠偏}
- **触发关键词**：{哪些词命中此反直觉}
```

Phase 1 通过关键词匹配识别；Phase 3 输出引用。

## Bootstrap 策略

冷启动不需要 200+ 条目。最小可用集：

| 类别 | 最小条目数 | 优先收录标准 |
|------|-----------|-------------|
| data-structures | 8 | Bloom Filter, HyperLogLog, B+ Tree, LSM Tree, Trie, Skip List, Hash Table, Bitmap |
| sorting-searching | 6 | QuickSort, TimSort, Radix Sort, Binary Search, Inverted Index, B-Tree |
| graph-algorithms | 5 | Dijkstra, A*, Topological Sort, PageRank, Union-Find |
| distributed-systems | 6 | Raft, Paxos, Gossip, 2PC, CRDT, Vector Clock |
| caching-strategies | 5 | LRU, LFU, W-TinyLFU, Write-Through, Cache-Aside |
| message-queue-patterns | 5 | Pub-Sub, Work Queue, Event Sourcing, DLQ, Exactly-Once |
| microservice-architecture | 5 | CQRS, Saga, BFF, Strangler Fig, Circuit Breaker |

新增条目流程：
1. 复制对应模板
2. 按标准取值填写 6 维最佳场景
3. 追加到类别文件末尾
4. 同步更新该类别文件头部的**条目速览表**（一行：条目 / 子类 / 核心问题一句话 / 最佳场景快照）
5. 更新 `_index.md` 状态列的条目数（首次建档时将 `TODO stub` 改为 `就绪（N 条目）`）
6. 如有必要，在 `_relations.md` 添加关系

## 无匹配 Fallback

如果所有候选条目都是 `Mismatch`：

```markdown
## 未找到直接匹配

当前知识图谱中没有与你约束完全匹配的方案。可能原因：
- 你的场景过于特殊或前沿
- 约束组合存在内在矛盾
- 知识库尚未覆盖该领域

**建议**：
1. 检查约束是否存在矛盾（见上方"约束矛盾检测"）
2. 放宽一个关键约束后重试
3. 或提供该领域的一个参考实现，我可以帮你生成新条目
```

## 与现有 Skill 的协同

| Skill | 协同方式 | 触发边界 |
|------|---------|---------|
| `requirement-clarify` | 当约束提取需要追问时使用；本 skill 只追问 1 轮，复杂澄清交给 requirement-clarify | 本 skill 优先自行提取，提取失败再调用 |
| `devil-advocate` | 用户可要求"杠精审查一下这个选型"，对推荐做 8 维度审查 | 本 skill 输出后由用户触发 |
| `coding-standards` | coding-standards 管"怎么写"；本 skill 管"用什么写" | 不重叠 |
| `codebase-design` | codebase-design 管模块接口；本 skill 管内层算法 | 先后关系：先选型，再设计模块 |
| 记忆「七原则」 | 在最终输出前做快速校验：是否存在因"实现复杂"而被排除的更优方案 | 嵌入 Phase 3 |

## 验收标准

一个成功的推荐必须满足：
1. 输出包含 Top-1 + 至少 1 个备选
2. Top-1 的每个关键维度都给出匹配结果
3. 存在偏离时必须输出风险警告和降级建议
4. 命中反直觉假设时必须输出纠偏
5. 未说明的约束必须列出假设
6. 必须引用具体知识条目路径
