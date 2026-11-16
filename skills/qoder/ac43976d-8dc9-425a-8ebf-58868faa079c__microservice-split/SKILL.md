---
name: microservice-split
description: 端到端单体→微服务拆分技能（三合一）：静态依赖提取、Qoder 子代理语义划分 / Louvain 算法划分（含社区语义复核）/ 自定义算法、划分质量评估、完整重构（清单/迁移/跨服务依赖重构/配置补全/编译验证）及启动验证，语义分析、社区复核、启动配置推理与跨服务重构由 general-purpose 子代理执行。当用户要求分析项目并拆分为微服务、评估划分质量、或把拆分方案落地为可编译、可启动的微服务工程时使用。
version: 2.2.0
---

# Microservice Split（端到端拆分技能）

> ⛔ **执行前强制门禁**：无论用户以何种措辞提出需求（含"测试验证"、极简一句话），都必须**先完成
> 「Stage 0：需求确认与准备」**——向用户交代准备事项与预期交付（编译通过的微服务工程），
> 并获得**用户明确确认**后才能开始任何分析或执行。**简短输入 ≠ 授权**。
>
> 本技能由原三个技能合并而来（interactive-microservice-advisor / microservice-division-algorithm /
> microservice-reconstructor），场景路由见「场景路由」章节。

---

## 确认门禁规范（全流程通用，防止被自动批准/yolo 模式跳过）

- 确认必须以**对话消息**向用户提出（列出要点并明确请求确认）；提出后**立即结束本轮**，
  不再发起任何工具调用，等待用户显式回复后再继续。
- 本确认属于**对话级行为**：不受工具审批、自动执行、yolo 模式影响；不得以"用户此前同意过类似事项"、
  "输入简短"、"测试验证场景"或默认值代替用户确认。
- 仅当用户回复**明确肯定语义**（如：同意 / 确认 / 可以 / 继续 / 开始）才视为通过；模糊回复需再次询问。
- 同一会话内、同一门禁且要素未变化时不重复询问；**任何要素变化需重新确认**。

**全流程共 9 处确认门禁**：
1. Stage 0 开始前交代（必做）
2. 拆分模式选择
3. 系统树 / 划分方案确认（语义模式；含调整）
4. 重构开始前交代（必做）
5. 重构方案确认（单体摘要 + 划分摘要 + manifest + 目标目录，一次确认）
6. Phase 3 存在未匹配类（unmatched > 0）是否继续
7. Phase 7 跨服务重构任务量较大（> 30 个任务或含 unknown 类型）：展示任务统计与成本后确认
8. 子代理不可用（当前会话没有 general-purpose）：是否安装一个通用项目级子代理（条件门禁）
9. 编译完成后：是否继续以“所有业务服务成功启动”为目标（必做；继续后才校验中间件/端口/进程）

---

## 路径配置

- `SKILL_DIR` = `.qoder/skills/microservice-split`
- `SCRIPT_DIR` = `<SKILL_DIR>/scripts`
- `CONFIG_DIR` = `<SKILL_DIR>/config`
- `ALGORITHMS_DIR` = `<SCRIPT_DIR>/algorithms`
- 子代理定义 = `<SKILL_DIR>/agents/cross-service-refactorer.md`（内置在技能目录，随技能分发）

## 输出目录约定（默认布局，可用参数覆盖）

```
<WORKSPACE_DIR>/                      # 默认建议：<TARGET_PATH 同级>/<项目名>-split-workspace/
├── 01-dependencies/                  # classInfo.json, data.json
├── 02-analysis/                      # tag_result.json, sum_detail.json, _progress_status*.json
├── 03-division/                      # system_tree.json, sum_microservice.json, partition*.json,
│                                     # evaluation*.json, shared_detection.json, refactor-waves.json
└── 04-reconstruction/
    ├── microservice-manifest.json
    ├── sum_microservice.json         # 从 03-division 复制（供父 pom 生成器识别 __shared__）
    ├── classInfoNew.json / serviceConfig.json / inter_dependencies.json
    ├── migration-results/  refactor-tasks/
    └── reconstruction-report.json
```

> 生成父 pom 前，先将 `03-division/sum_microservice.json` 复制到 `04-reconstruction/`，
> 保证 `generate_parent_pom.py` 能自动识别 `__shared__` 并生成 `common` 模块。
> **Windows 提示**：建议使用较短的工作区路径（如 `C:\ws\<项目名>-split-workspace`），避免 MAX_PATH 260 限制。

---

## 场景路由

| 用户意图（示例触发） | 执行链路 |
|---|---|
| 完整拆分并重构（"把项目拆成微服务"） | Stage 0 → 1 → 2 → 3 → 4 → 5 |
| 只分析并划分（语义） | Stage 0 → 1 → 2A → 2E → 3 |
| 算法划分（Louvain） | Stage 0 → 1 → 2B → 2E → 3 |
| 自定义算法划分 | Stage 0 → 1 → 2C → 2E → 3 |
| 只看懂/分析代码 | Stage 0 → 1 → 2A（A-1、A-2） |
| 调整已有划分 | Stage 3（tree_manager 调整 → 重跑 A-4） |
| 评估已有划分 | 2E |
| 已有拆分方案，只要重构 | 4（含 4.0 与 Phase 1 门禁）→ 5 |

**前置条件速查**：
- Stage 1：Java 21+（分析器 JAR 以 Java 21 编译；非 Java 项目跳过）；Stage 4 编译 JDK 另按项目版本选择
- 2A：Qoder 子代理（默认 general-purpose；IDE 无此类型时安装项目级 agent，无需 API Key）
- 2B：`01-dependencies/` 依赖数据
- 2C：`ALGORITHMS_DIR` 下含 README.md 的算法目录
- Stage 4：`classInfo.json` + `sum_microservice.json`

---

# Stage 0：需求确认与准备（开始前必做）

当用户提出"拆分微服务"类需求时，**不要立即开始**。先向用户交代以下内容并获得明确确认
（按「确认门禁规范」以对话消息提出并结束本轮）：

### 需要用户准备/确认
1. **目标项目**：本地可访问的 Maven 源码路径。**支持范围**：Spring Boot 2.x / 3.x / 4.0.x
   （含 Boot 的 WAR 工程）。**不支持纯 WAR / 无 Spring Boot 的老应用**（如 web.xml + Servlet/JSP、
   Struts、EJB、Ant 构建）——重构骨架、配置补全与 Feign 均依赖 Spring Boot。Stage 0 检测到
   `packaging=war` 且无 Boot、或存在 `src/main/webapp/WEB-INF/web.xml` 时应**立即告知用户并停止**，
   不要进入分析/重构流程（可建议先迁移到 Spring Boot，或人工拆分）。
2. **运行环境（Java 21 检查协议，必做）**：静态分析器 JAR 要求 **Java 21+**（低于 21 会报
   `UnsupportedClassVersionError`）。先运行跨平台检测脚本：
   ```
   uv run --project <SKILL_DIR> <SCRIPT_DIR>/check_env.py
   ```
   然后按以下顺序处理：
   - **先检测**：
     - macOS / Linux：`/usr/libexec/java_home -V`、`java -version`，并检查
       `~/soft/`、`/Library/Java/JavaVirtualMachines/`、`/usr/lib/jvm/`
     - Windows（PowerShell）：`where.exe java`、`$env:JAVA_HOME`，并检查
       `C:\Program Files\Eclipse Adoptium\`、`C:\Program Files\Java\`、`%USERPROFILE%\.jdks\`
     - 项目内常见位置：`validation/tools/`、`tools/` 下的 JDK 目录
   - **已存在** → 明确告知用户"检测到的 JDK 21+ 及其具体路径"，确认后在当前会话使用：
     - macOS / Linux：`export PATH="<JDK_HOME>/bin:$PATH"`
     - Windows PowerShell：`$env:Path = "<JDK_HOME>\bin;" + $env:Path`
     - Windows CMD：`set PATH=<JDK_HOME>\bin;%PATH%`
     不要重复安装
   - **不存在** → 说明原因与可选方案（① 下载 Temurin 21 到项目本地目录、不改系统环境（推荐）；
     ② 用户自行用 brew/sdkman/winget 安装），**征得用户明确同意后再安装**
     （Windows 下载 zip/msi；macOS/Linux 下载 tar.gz）；安装后验证为 21+
   - 记录最终 java 路径，Stage 1 全程使用。Maven 仅在进入 Stage 4 时必需
   - **编译 JDK 与项目对齐**：Stage 4 使用的 JDK 必须 ≥ 原项目 `java.version`（Boot 3/4 至少 17）。
     若检测到的 JDK 只有 21 而项目 `java.version` 更高（如 25），需提示用户提供对应 JDK；
     不能只用 21 强行编译。Java 21 是 Stage 1 分析器的硬性要求，不是项目的目标版本。
3. **拆分模式**：语义模式（Qoder general 子代理，无需 API Key）/ 内置算法模式（Louvain，零外部调用）/ 自定义算法
4. 建议先验证原项目可基线编译（`mvn -DskipTests compile`），便于后续对比与验证
5. **预期投入**：语义模式约每 12 个文件 1 个子代理（详情+归属各一轮，≤5 并发），
   Token/耗时通常高于外部轻量模型，但无需任何 Key；算法模式零外部调用。大项目（>20 批）
   开始前会展示预计批次数与耗时
6. **子代理可用性（必做）**：确认会话可用 `general-purpose` 子代理；若没有，按
   「子代理可用性检查」询问用户是否安装项目级 agents

### 预期可得到的成果
- 分析结果：静态依赖数据、逐文件标签/摘要、系统树（语义模式）
- 拆分方案：`sum_microservice.json`（服务划分 + 共享库 `__shared__`）+ 质量评估
- 若继续重构：**一个经 `mvn -DskipTests compile` 编译验证通过的多模块微服务工程**
  （交付标准=编译通过；配置好中间件后可继续 Phase 10 启动验证，按端口可连验收；
  internal 接口鉴权、分布式事务等不在本技能范围）

### 语义分析说明（无需外部 LLM 配置）

逐文件标签/摘要与代码归属由 **Qoder 子代理**完成，不再需要 API Key、端点或模型配置。
主代理只负责准备批次、创建子代理、记录进度和合并结果；子代理直接读取源码并把结果写入文件。

- 详情阶段约每 12 个文件 1 个子代理；归属阶段同样分批
- 子代理并发 ≤5；一批失败只重试该批，不影响其他批次
- 主代理不读取源码/任务/结果正文，只接收一行 `done` / `failed`
- 已存在的旧 `.env` 不再被技能读取，可自行删除

### 子代理可用性检查（必做，条件门禁 8）

Qoder CLI 默认提供 `general-purpose`，部分 Qoder IDE 环境可能没有。Stage 0 必须确认：

1. 检查当前会话可用子代理类型中是否有 `general-purpose`
2. **有** → `SUBAGENT_AGENT=general-purpose`
3. **没有** → 向用户说明影响，并询问是否安装**一个**通用项目级子代理：
   ```
   uv run --project <SKILL_DIR> <SCRIPT_DIR>/install_custom_agents.py <工作区>
   ```
   安装后在 `.qoder/agents/` 生成 `microservice-general-purpose`。
   之后所有阶段（A-1/A-4/2B 复核/Phase 7）都用它，使用方式与 built-in
   general-purpose 完全一致：主代理把当前任务对应的说明书全文放入 prompt，
   并传 `taskFile`。
4. 提示用户**重新加载 Qoder IDE / 新建会话**以发现新 agent；
   重载后 `SUBAGENT_AGENT=microservice-general-purpose`
5. 用户拒绝或安装后仍不可用 → 停止语义/重构流程并说明原因，不得退回外部 LLM 配置

> 安装脚本默认不覆盖已有 agent；如需更新使用 `--force`。不为每个阶段创建不同 agent。

---

# Stage 1：静态依赖提取（Java Only，非 Java 项目跳过）

```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/run.py <TARGET_PATH> <01-dependencies 目录> [PACKAGE_NAME]
```

**输出**：`classInfo.json`（原始依赖：dependencies / extendsAndImplements / 源码位置）、`data.json`（带 ID 索引）。
完成后告知用户类数量与依赖边数量。需要 Java 21+。

> **副产物说明**：分析器会在被扫描项目内生成 `fuxi-static-dependency/`（收集项目依赖的第三方 JAR 以构建分析类路径）。
> 属正常副产物：不影响项目源码与构建，可忽略或运行后删除，**不要提交到代码仓库**（仓库根 .gitignore 已忽略该目录）。

---

# Stage 2：划分（三模式，按 Stage 0 选择执行其一）

## 2A：语义划分（Qoder general 子代理）

### A-1 逐文件语义分析

**1. 准备批次**（确定性脚本，不调用 LLM）：
```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/prepare_semantic_batches.py \
  <TARGET_PATH> <02-analysis 目录> --kind details
```
可选：`--batch-files 12` / `--batch-chars 100000`；默认按路径排序切批，单文件截断到 15K 字符。
输出 `semantic-tasks/_manifest.json`、`task_<i>.json`，以及文件数/批次数/平均文件数。
**批次数 > 20 时**先向用户展示预计子代理数、并发和大致耗时，确认后再启动。

**2. 创建子代理**：主代理读取 `agents/semantic-analyzer.md` 全文一次；对每个未完成批次创建
`SUBAGENT_AGENT`（默认 general-purpose；无则由 Stage 0 安装通用 agent）子代理（波内 ≤5 并发），
传入 `taskFile=<绝对路径>`。子代理读取源码，写 `task_<i>.result.json`，只回复一行。
失败批次重试一次；可随时查看进度：
```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/prepare_semantic_batches.py \
  <TARGET_PATH> <02-analysis 目录> --kind details --status
```

**3. 合并**：
```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/merge_semantic_results.py <02-analysis 目录> --kind details
```
检查 `_merge_report.json`：`coverage=100%`、`errors=[]` 才继续。覆盖不足时重跑缺失批次；
确需部分结果时加 `--allow-partial` 并向用户确认。
**输出**：`tag_result.json`、`sum_detail.json`（与旧版格式一致）。大文件由子代理截断至 ~15K 字符。

### A-2 理解并呈现项目

读取 `sum_detail.json`，按标签分组（endpoint/service/model/persistence/integration/utils/support）
呈现：系统用途、业务域、技术架构。

### A-3 系统树构建与确认（⛔ 门禁 3）

1. 询问划分偏好（服务数建议 3-8、团队约束、边界、共享关注点）
2. 提出子系统/领域/能力方案（覆盖全部功能），**等待用户明确确认**
3. 写入 `03-division/system_tree.json` 并校验：
   ```
   uv run --project <SKILL_DIR> <SCRIPT_DIR>/tree_manager.py validate <03-division 目录>
   ```
   树结构：`System → subsystems[] → domains[] → capabilities[]`（每级含 name/summary）。

### A-4 代码归属

**1. 准备批次**（以 `03-division/system_tree.json` 为输入；树变更会自动使旧批次失效）：
```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/prepare_semantic_batches.py \
  <TARGET_PATH> <03-division 目录> --kind belong
```

**2. 创建子代理**：读取 `agents/ownership-analyzer.md` 全文一次；对未完成批次创建
`SUBAGENT_AGENT`（默认 general-purpose；无则由 Stage 0 安装通用 agent）子代理（≤5 并发），
传入 `taskFile=<绝对路径>`；子代理写 `task_<i>.result.json`，只回复一行。失败批次重试一次；可用 `--status` 查看进度
（命令同上，追加 `--kind belong --status`）。

**3. 合并**：
```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/merge_semantic_results.py <03-division 目录> --kind belong
```
检查 `_merge_report.json` 的覆盖率和错误；**输出**：`microservice_result.json`、`sum_microservice.json`。
呈现：每子系统文件数、未匹配文件、置信度分布；不满意 → Stage 3 调整后重跑本步。

### A-5 共享类检测（语义模式与算法模式对齐，必须执行）

> 语义模式：A-4 之后执行。算法模式：Stage 3 最终 sum 确认后执行；方案调整后重跑。

```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/extract_shared_classes.py <03-division 目录>
```
规则：①未归属（被引用或位于基建包，如 common/config/base/security 等）；②位于基建包且被其他服务的类引用。
业务类跨服务引用**不会**被移入共享库（应由重构阶段变为 Feign / 本地 DTO）。
原文件自动备份 `sum_microservice.pre-shared.json`（已存在时使用带时间戳的备份名），明细写入 `shared_detection.json`。
若 `__shared__` 已存在（手工预置或重跑），脚本会将其作为候选集**合并**（幂等），不会跳过。
若检测到**共享库反向依赖**（common 中的类依赖业务服务中的类，输出 `reverse_dependencies`），
**必须向用户展示并确认处理方式**（推荐：将被依赖类纳入 `__shared__`，或调整划分避免共享类引用业务类），
确认后才进入 Stage 3——带着反向依赖进入迁移会导致 common 无法编译。
检测到共享类时向用户展示后进入 A-6 / 2E。

### A-6 语义模式评估

语义模式的 `sum_microservice.json` 保存的是文件路径，先转换为 `partition.json` 再评估：
```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/sum_to_partition.py \
  <03-division>/sum_microservice.json <03-division>/classInfo.json \
  <03-division>/partition_from_sum.json

uv run --project <SKILL_DIR> <SCRIPT_DIR>/evaluate.py \
  --partition <03-division>/partition_from_sum.json \
  --class-info <03-division>/classInfo.json \
  --output <03-division>/evaluation.json
```
默认包含 `__shared__` 分区（与历史对比口径一致）；需要只看业务服务时加 `--exclude-shared`
生成另一份 partition 再评估。资源文件会跳过，报告中的 class 数可能小于 `sum` 文件数。

## 2B：Louvain 算法划分 + 语义复核

### 2B.1 社区划分

```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/split.py \
  --class-info <01-dependencies>/classInfo.json \
  --output <03-division>/partition.json --seed 42
```

可选参数：`--static-call-weight N`（默认 2）、`--static-inherit-weight N`（默认 3）、
`--min-service-size N`（默认 2）、`--seed N`（固定可复现）。
**输出**：`partition.json`（`{"服务ID": ["类全限定名", ...]}`）与 `partition_named.json`。
展示每个服务包含的类。

### 2B.2 语义分析（必须，供社区复核使用）

如果 `<02-analysis>/tag_result.json` 不存在，先按 A-1 执行详情语义分析：
`prepare_semantic_batches.py --kind details` → 语义子代理 → `merge_semantic_results.py`。
（不需要构建系统树；这一步只生成逐文件 tag/summary。）

### 2B.3 碎片化判定与社区复核

```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/prepare_community_review.py <03-division 目录> \
  --target-max <用户目标服务数上限，默认 8>
```
脚本输出：
- `fragmentation.json`：社区数、大小、小社区占比、CV、`fragmented` 与原因
- `refinement-tasks/task_<i>.json`：每社区一个语义复核任务

**总是**读取 `agents/community-refiner.md` 并创建 `SUBAGENT_AGENT` 子代理（每任务一个，
≤5 并发），读取 community/allCommunities/fragmentation，输出**建议**：
```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/merge_community_suggestions.py <03-division 目录>
```
生成 `refinement-proposal.json`。**只生成建议，不修改 partition**；建议在 Stage 3 展示，
由用户决定是否采纳。默认要求所有复核任务完成；部分完成需 `--allow-partial` 并明确告知。

### 2B.4 生成 Stage 3/4 输入

```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/partition_to_services.py \
  --partition <03-division>/partition.json \
  --class-info <01-dependencies>/classInfo.json \
  --target-path <TARGET_PATH> \
  --names <03-division>/partition_named.json \
  --output <03-division>/sum_microservice.json
```
随后执行 2E 评估；算法模式最终以该 `sum_microservice.json` 进入 Stage 3。
若用户采纳复核建议，需要先人工调整 partition/sum 并重新评估（当前不做自动应用）。
A-5 在 Stage 3 确认最终方案后执行；若方案调整，重跑 A-5。

## 2C：自定义算法划分

算法位于 `ALGORITHMS_DIR/<name>/`（含 README.md 即有效）。流程：
1. 扫描并列出可用算法（内置示例：`louvain`、`label_propagation`）
2. 读取该算法 README（算法说明/前置条件/运行命令/输出格式），**以其为准**
3. 按 README 构造命令执行（替换路径占位符）；README 提及可选参数时询问用户
4. 校验 `sum_microservice.json` 存在且格式为 `{ "ServiceName": ["file_path", ...] }`，展示结果
5. 新增算法：在 `ALGORITHMS_DIR/` 新建目录 + README（含输出契约），下次自动发现

## 2D：运行时依赖增强（已移除）

> 本技能已移除 SkyWalking/Docker 运行时依赖采集支线（无 Docker、无 bash 依赖）。
> 当前仅支持静态依赖划分；如需运行时数据，请作为独立扩展自行提供并评估可行性。

## 2E：划分评估与对比（2B.4 或 A-6 生成 partition 后执行）

```
uv run --project <SKILL_DIR> <SCRIPT_DIR>/evaluate.py --partition <partition.json> \
  --class-info <01-dependencies>/classInfo.json --output <03-division>/evaluation.json
```
指标：模块度 Q（>0.3 较好）、内聚度（趋近 1）、耦合度（趋近 0）、平衡性 CV（越低越均匀）。
支持对任意 partition（含语义模式的转换结果）评估，用于语义 vs 算法对比。

---

# Stage 3：划分确认与调整（⛔ 门禁 3 的确认环节）

1. 展示 `sum_microservice.json` 映射：服务数、每服务文件数、职责、横切关注点、未匹配文件；
   算法模式同时展示质量指标、`fragmentation.json` 和 `refinement-proposal.json`。
   **语义复核建议只作为决策依据，不自动修改 partition/sum**；用户选择保留原方案或按建议人工调整。
2. **等待用户确认**；需要调整时使用 `tree_manager.py`（语义模式）：

| 操作 | 命令 |
|---|---|
| 查看树 | `tree_manager.py show <03-division 目录>` |
| 移动领域/能力 | `tree_manager.py move <目录> --source "Sub1/Dom" --target "Sub2"` |
| 合并子系统 | `tree_manager.py merge <目录> --sources "A,B" --name "New" --summary "..."` |
| 增/删/改名 | `add` / `remove` / `rename`（见脚本 help） |

调整后重跑 A-4（及 A-5）更新归属，再次确认。算法模式若按建议调整了 partition/sum，
重跑 `partition_to_services.py`、`evaluate.py` 和 A-5。
3. 用户确认后 → 若需重构进入 Stage 4；否则进入 Stage 5 输出划分结果。

---

# Stage 4：重构（原 microservice-reconstructor 全流程）

> **交付标准**：`targetProjectPath` 下的多模块微服务工程，**`mvn -DskipTests compile` 编译通过**。
> 运行期联调、internal 接口鉴权、分布式事务等不在本技能范围（列入报告 nextSteps）。

## 4.0 重构开始前交代（⛔ 门禁 4，必做，等待用户同意）

- **交付物与验收标准**：如上；含编译修复自动进行（最多 3 轮）
- **需要准备**：Maven 与可用构建依赖网络；建议先验证目标项目基线可编译；足够磁盘空间
- **将执行的操作**：只读取原单体（不修改）、只写入新目录；跨服务依赖将产生 Feign Client / 本地 DTO /
  共享库（common）；可能新增无鉴权的 internal 接口
- **仅在用户明确同意后**，才进入 Phase 1

## Phase 1：输入验证与准备

**1.1 必需输入**（缺失先询问）：
| 参数 | 说明 |
|---|---|
| `monolithProjectPath` | 原单体项目根目录 |
| `targetProjectPath` | 重构输出根目录（不得等于/覆盖原项目） |
| `classInfoPath` | `classInfo.json` |
| `splitResultPath` | `sum_microservice.json` |

可选：`manifestPath`（默认 `04-reconstruction/microservice-manifest.json`）、
`resultDir`（默认 `04-reconstruction/`）。

**1.2 扫描原单体**：构建工具（Maven/Gradle）、根 pom + 所有子模块 pom、groupId/artifactId/version、
resources 配置、主启动类位置。
**技术栈识别（重要，由 Agent 读取 pom 完成，不交给脚本）**：
- 逐个读取根 pom 与子模块 pom，确定原工程**实际使用的** Spring Boot / Spring Cloud / Java 版本
  及 `javax`/`jakarta` 命名空间；需解析 `${...}` 属性引用
- Spring Boot：parent、`<spring-boot.version>`、`spring-boot-dependencies` BOM
- Spring Cloud：`<spring-cloud.version>` 或 `spring-cloud-dependencies` BOM；若确实未声明，由
  Agent 根据实际 Boot 版本选择兼容的 release train，并标注 `springCloudVersionSource=derived-from-boot`
- Java：`java.version` / `maven.compiler.release|source|target`；Boot 3/4 至少 17
- 命名空间：查看源码 import（Boot 3/4 为 `jakarta.*`，Boot 2 为 `javax.*`）
- 支持 Spring Boot 2.x / 3.x / 4.0.x；无法确认时**询问用户**，不要猜默认版本
- **传统 WAR / 无 Boot**（`packaging=war` 且未声明 Boot，或存在 `WEB-INF/web.xml`）→ 明确告知
  当前不支持并停止；建议用户**先迁移到 Spring Boot 再拆分**（保持 C 方案，不扩展老 WAR 适配）
- 结果写入 manifest 顶层 `techStack`（见 Phase 2），并纳入门禁 5 展示；Gradle 项目仍不支持

**1.3 分析拆分方案并确认（⛔ 门禁 5，与 manifest 合并一次确认）**：
读取 `splitResultPath`，识别服务数/每服务文件/未分配文件/是否含 `__shared__`/serviceNames；
展示给用户：单体摘要 + 划分摘要 + **技术栈结论（Boot/Cloud/Java/namespace 及版本来源）** +
**建议 manifest**（服务名/basePackage/端口）+ 目标目录。
若含 `__shared__`：说明共享类数量与含义（将进入 common 共享库，保持原包名）。
**等待用户确认后继续**。

## Phase 2：生成微服务清单（manifest）

由主代理直接生成（不调用脚本）：
1. 从构建文件提取 projectName/groupId/version/javaVersion
2. 写入 `techStack`（来自 Phase 1.2 的 Agent 推断结果）：
   ```json
   "techStack": {
     "springBootVersion": "3.5.14",
     "springCloudVersion": "2025.0.3",
     "javaVersion": "17",
     "namespace": "jakarta",
     "springBootVersionSource": "parent:pom.xml",
     "springCloudVersionSource": "derived-from-boot"
   }
   ```
3. 规范化服务名：小写 + `-` 连接 + 以 `-service` 结尾（如 用户服务→user-service），结果必须稳定
4. `basePackage` = groupId + "." + 服务关键词；端口从 18081 起逐一分配
5. `__shared__` 存在时，在 services 最前添加：
   `{ "serviceName": "common", "basePackage": "<原项目根包名>", "port": 0 }`
6. 写入 manifest（格式见上）

## Phase 3：生成迁移映射

```
python <SCRIPT_DIR>/prepare_migration_mapping.py <classInfoPath> <splitResultPath> <manifestPath> <resultDir>/classInfoNew.json
```
- 匹配 sum 文件路径 ↔ classInfo 全限定名；按 basePackage 计算新包名/新路径
- `__shared__` 处理：`newServiceName="common"`、保持原全限定名与原路径（仅复制到 common/）、
  业务类对共享类的引用视为 intra、import 不改
- 无 `__shared__` 时自动检测共享类（未分配但被引用者，按引用服务生成 `qualifiedName@service` 副本）
- 区分 intra / inter 依赖
检查输出：`sharedClasses` > 0 时展示；**`unmatchedClasses` > 0 时展示清单并确认是否继续（⛔ 门禁 6）**；
失败则停止并报告。

## Phase 4：生成项目骨架

1. 创建目标目录（common 模块优先，再各服务）
2. **生成父 pom（脚本只渲染，不做版本探测/推断）**：
   ```
   python <SCRIPT_DIR>/generate_parent_pom.py <manifestPath> <targetProjectPath>/pom.xml \
     [--boot-version <v>] [--cloud-version <v>] [--java-version <v>]
   ```
   - 版本读取 `manifest.techStack`（Phase 1.2 由 Agent 读 pom 推断并经门禁 5 确认）
   - 缺少 `springBootVersion` / `springCloudVersion` / `javaVersion` 时脚本直接失败
     （`missing_tech_stack`）；此时回到 Phase 1.2 让 Agent 重新读取 pom 补全，不得套用默认值
   - 可选参数仅用于用户明确指定目标版本；正常情况下不传
   - 脚本不维护 Spring Boot ↔ Spring Cloud 映射表；兼容性判断由 Agent 负责
3. **生成服务配置**：`python <SCRIPT_DIR>/generate_service_config.py <manifestPath> <resultDir>/serviceConfig.json`
   （会把 `techStack` 传给 Phase 7 的任务文件）

## Phase 5：批量文件迁移（纯机械，脚本完成）

```
python <SCRIPT_DIR>/batch_migrate.py <resultDir>/classInfoNew.json <monolithProjectPath> <targetProjectPath> <resultDir>/migration-results
```
- 共享库类：原样复制到 `common/`（不改 package/import）
- 业务类：复制到对应服务、改 package、改同服务 import、共享库 import 不变、跨服务 import 保留（待重构）
检查：total/succeeded/failed；**必须检查 `residualReferences`**（>0 = 不在预期跨服务清单内的旧包引用，
多为静态分析漏检，编译期人工复核）；不修改原项目。

## Phase 6：提取跨服务依赖

```
python <SCRIPT_DIR>/extract_inter_dependencies.py <resultDir>/classInfoNew.json <resultDir>/inter_dependencies.json
```
展示总数/类型数量；为 0 可跳过 Phase 7。

## Phase 7：跨服务依赖重构（脚本 + 子代理）

**7.1 任务准备**：
```
python <SCRIPT_DIR>/prepare_refactor_tasks.py <resultDir>/inter_dependencies.json <targetProjectPath> <resultDir>/serviceConfig.json <resultDir>/refactor-tasks
```
- 高置信度类型（utility/enum/constants/exception）→ 脚本直接 localize（零 token）
- 其余（dto/entity/inheritance/service_interface/service_impl/mapper/config/unknown）→ 生成 `task_<i>.json`
- 无法解析的依赖（内嵌/成员类型、文件缺失、共享库类型）会被**前置过滤**并计入 `prefilteredSkipped`
- 脚本会自动清理同目录上一轮的 `task_*` / `task_*.result.json` 与旧 `refactor-waves.json`；禁止多轮产物混用
- 检查 `scriptHandled` 与 `needsSubagent` 数量

**7.1.5 任务量与成本确认（⛔ 门禁 7）**：当任务数 > 30 或含 unknown 类型时，
向用户展示：任务总数、类型分布、预计波次数与并发、涉及的服务对与大致耗时/上下文成本；
**确认后**才启动子代理。

**7.2 冲突分组波次**：
```
python <SCRIPT_DIR>/group_refactor_tasks.py <resultDir>/refactor-tasks
```
输出 `refactor-waves.json`：同波次内无文件冲突（可并行），**波次之间必须串行**；
文件包含**任务集指纹**——每次重新生成任务后**必须重新运行本脚本**（任务集变化指纹即变化）。
对波次内每个任务，**用技能内置的说明书创建 `SUBAGENT_AGENT` 子代理**（默认 general-purpose；
建议波内一次并行创建 ≤5 个；不支持并行时按波次串行同样正确）：
```
子代理指令 = <SKILL_DIR>/agents/cross-service-refactorer.md 全文（主代理读一次后复用）
taskFile = <resultDir>/refactor-tasks/task_<i>.json
targetRoot = <targetProjectPath>
```
任务文件包含 `techStack`（Boot/Cloud/Java 版本与 `namespace`）；子代理读取源码自主选择策略
（feign/localize/local-dto/skip），**新增代码的命名空间必须与 techStack/源码一致**（Boot 3/4 → jakarta），
只回复一行 `done` / `failed: 原因`。
**上下文管控（极其重要）**：
- 只回复一行、不追问不展开；不在对话中累积/总结子代理输出
- 只记进度数字（"已完成 X/Y"），每 20 个任务打印一次
- 失败任务记下索引，继续下一个
- 若回复不符协议，以 `task_<i>.result.json` 为准，不阻塞流程

**7.3 汇总**：
```
python <SCRIPT_DIR>/summarize_refactor_results.py <resultDir>/refactor-tasks
```
检查 succeeded/partialSuccess/failed；失败项查看 `manualReviewItems`。

## Phase 8：配置补全（主代理执行，先整体分析再统一补全）

**8.1 扫描**：根 pom **及所有子模块 pom**（依赖/插件/Java 版本/版本属性）、主启动类注解
（@SpringBootApplication/@EnableFeignClients/@MapperScan 等）、application*.yml、profile、logback、
MyBatis XML、其他资源。
**技术栈一致性（重要）**：以 manifest 的 `techStack` 与原工程 pom 为准，**保持原技术栈代际**：
Boot 3/4 使用 `jakarta.*`，不得把原代码/新代码改成 `javax.*`；Spring Cloud 版本来自实际声明或
按实际 Boot 推导的结果；Java 版本取原工程 `java.version`。不得为了"能编译"而降级 Boot/Cloud。
**8.2 服务 pom**：正确 parent；`common` 依赖（若存在）；Web 依赖；原项目关键依赖（JPA/MyBatis/Redis 等）；
有 Feign 时加 `spring-cloud-starter-openfeign`（Boot 3/4 同样适用，版本由父 pom 的 Cloud BOM 管理，
不要写死版本）；`spring-boot-maven-plugin`。原工程为多模块时，由 Agent 读取各子模块 pom，
补齐类实际使用到的依赖，并在服务 pom 中显式写出原工程实际版本（或把所需 `*.version` 属性
加入父 pom 的 `<properties>`）；不要依赖父 pom 生成器复制版本属性。
**8.3 共享库 common/pom.xml**：提取框架级依赖（ORM/工具库/日志/缓存等）；不确定时保守地把原项目
依赖都加入。**主启动类**：`<PascalCase 服务名>Application`，含 `@SpringBootApplication` 与 main；
有 Feign → `@EnableFeignClients`。**@MapperScan**：扫描包通常指向原业务包，必须改为各服务新包
（如 `<serviceBasePackage>.modules.*.mapper`）；若位于 common，应移除并改由各服务启动类声明
（否则编译通过但运行期 Bean 缺失）。
**8.4 application.yml**：`spring.application.name`=manifest 服务名、`server.port`=manifest 端口；
迁移数据源/Redis/MQ/注册配置/profile/日志/自定义配置。**保持原工程的配置键与代际**（如 Boot 3
的 `spring.data.redis.*` 不要改回 `spring.redis.*`；Boot 4 同理）；Feign 目标地址：
```yaml
services:
  user-service:
    url: http://localhost:18081
```
**8.5 其他资源**：logback-spring.xml、MyBatis XML、必要 SQL。

## Phase 9：构建验证与修复

1. 在 `targetProjectPath` 根执行：`mvn -q -DskipTests compile`（或逐服务）
2. 失败 → 读错误 → 修复（缺 import / 未解析类型 / 缺依赖）→ 重编译
3. **最多 3 轮**。语义级修复（删类/合并类/改接口行为）按当前策略**自主执行**并记录到 manualReviewItems；
   若 3 轮后仍失败 → 停止并报告问题清单
4. 结构验证：
   ```
   python <SCRIPT_DIR>/validate_project_structure.py <targetProjectPath> <manifestPath>
   ```
   检查每服务：pom、主启动类、配置文件、Java 源文件、Feign 配置（如需）
5. **编译通过后必须询问用户**（⛔ 门禁 9，对话级，提出后结束本轮）：
   > 编译已通过。是否继续以“所有业务服务成功启动”为目标进行 Phase 10 启动验证？
   > 继续后我会先扫描本项目实际需要的中间件，**只列出检测到的项**并给出配置方式；
   > 不需要的中间件不会提。继续还需要你允许技能启动/终止 Java 进程。
   > 不继续则以编译级工程交付，并在报告中标记 startupValidation=skipped。
   - 用户拒绝/未确认 → 跳过 Phase 10，进入最终报告
   - 用户同意 → 进入 Phase 10

## Phase 10：启动验证（门禁 9 继续后执行）

### 10.1 证据扫描（脚本辅助，不是结论）

```
python <SCRIPT_DIR>/scan_startup_config.py <targetProjectPath> <manifestPath> <resultDir>
```
脚本只机械提取配置 key/当前值（脱敏）与 pom 依赖，生成：
- `startup-evidence.json`：候选类型与 key，**明确标记 non-authoritative**
- `startup-config.md`：候选证据说明
- `startup-values.env`：候选值模板（默认不覆盖已有文件；`--force` 可重置）

**不要把脚本候选直接当成用户需求**；必须进入 10.2 由 Agent 复核。

### 10.2 Agent 推理实际依赖

创建 `<resultDir>/startup-config-task.json`（主代理直接写）：
```json
{"targetRoot":"...","evidencePath":"<resultDir>/startup-evidence.json",
 "outputPath":"<resultDir>/startup-analysis.json",
 "services":[{"serviceName":"...","port":18081,"configFiles":["..."]}]}
```
读取 `agents/startup-config-analyzer.md`，用 `SUBAGENT_AGENT` 创建一个分析子代理。
它结合配置文件、pom、客户端初始化代码和（可选）启动日志，输出 `startup-analysis.json`：
- `required`：启动确实需要、且状态为 configured/needs_values/missing_config/needs_review
- `optional`：仅运行时按需使用、启动不阻塞
- 不确定的标 `needs_review`，不要猜

**只向用户展示 required 中 `needs_values`/`missing_config` 的项**；例如项目只用 MySQL/Redis
就只问这两项，不主动提 MQ/ES。

Agent 还要识别**非中间件**的启动阻塞，例如：无数据库代码的服务被 DataSourceAutoConfiguration
要求 DataSource、缺少 JDBC 驱动、某个 starter 传递引入了不需要的自动配置。此类问题输出
`status=missing_config/needs_review` + 推荐修复（如 `spring.autoconfigure.exclude`），
不要向用户索要无关的数据库/中间件。

### 10.3 引导用户补值并生成隔离配置

1. 明确告诉用户 `startup-values.env` 的**绝对路径**；敏感值写入该文件，不通过聊天传递
2. 非敏感值（host/port/database/user）可在对话中提供，由 Agent 写入模板
3. Agent 根据 `startup-analysis.json` 生成/调整 `<resultDir>/startup-config/<service>/application.properties`；
   可借助 `apply_startup_config.py` 作为加速器，但必须按分析结果删掉 optional 项
4. OSS/MinIO/Alipay 等复杂 SDK 配置由 Agent 引导用户补充对应 key
5. 用户拒绝提供/缺少关键值时，标记 blocked，不假装启动成功

### 10.4 启动 → 诊断 → 迭代

1. 启动（见 10.5）
2. 若失败/超时：
   - 读取 `startup/<service>.log`，区分中间件缺失、配置错误、代码/端口问题
   - 将日志路径加入 `startup-config-task.json` 的 `logPaths`，重跑 10.2 分析
   - 只针对新发现的 required 缺口询问用户并更新覆盖配置
   - 最多 3 轮；不要反复询问已经配置好的项
3. 仍失败 → 标记 blocked/failed，保留日志与未解决项

### 10.5 启动与报告

```
python <SCRIPT_DIR>/startup_services.py <targetProjectPath> <manifestPath> <resultDir> \
  --timeout 120 --config-dir <resultDir>/startup-config \
  --values <resultDir>/startup-values.env
```
- 默认先 `mvn -B -ntp -DskipTests package`，再 `java -jar` 逐个启动
- 端口可连 = `started`；common/port=0 跳过
- 无 jar/端口占用 → `blocked`；进程退出/超时 → `failed`/`timeout`
- 全部业务服务 `started` 才标记启动验证成功；否则列出每个服务状态与日志路径

## Phase 11：输出最终报告

写入 `<resultDir>/reconstruction-report.json`，结构：
```json
{
  "status": "success | partial_success | failed",
  "monolithProjectPath": "...", "targetProjectPath": "...",
  "phases": {
    "manifest": {"status": "...", "details": "..."},
    "migration": {"status": "...", "total": 0, "succeeded": 0, "failed": 0},
    "crossServiceRefactor": {"status": "...", "total": 0, "succeeded": 0, "failed": 0},
    "configCompletion": {"status": "...", "details": "..."},
    "buildValidation": {"status": "...", "details": "..."},
    "startupValidation": {"status": "success | partial_success | failed | skipped",
                          "started": 0, "blocked": 0, "failed": 0,
                          "reportPath": "..."}
  },
  "services": [{"serviceName": "", "port": 0, "fileCount": 0, "hasPom": true,
                "hasMainClass": true, "hasConfig": true, "hasFeignClients": false,
                "buildStatus": "success | failed", "issues": []}],
  "crossServiceSummary": {"totalDependencies": 0, "resolvedByFeign": 0,
                          "localizedTypes": 0, "manualReviewItems": []},
  "outputStructure": "...", "nextSteps": [], "warnings": []
}
```
向用户展示：总体状态、各服务状态表、跨服务处理摘要、目录结构、下一步建议。

---

# Stage 5：输出与交付

1. 汇总：划分方案（服务数/每服务职责/共享类/未匹配）、评估指标（如已运行）、重构报告路径
2. 明确交付边界：编译级交付；列出 nextSteps（启动方式、人工审查项、运行期建议）
3. 产物路径索引（01-dependencies / 02-analysis / 03-division / 04-reconstruction / 目标工程）

---

## 共享库机制说明（`__shared__`）

当拆分方案包含 `__shared__`：共享类 → `common` 模块（**保持原始包名与路径直接复制**），
业务类按 basePackage 重命名；共享类的引用通过 Maven 依赖解析、import 不变。
好处：消除框架类跨服务依赖、避免重命名连锁修改、保证单一定义。
> `__shared__` 键名不可更改。

## 子代理

所有子代理说明书均内置在 `<SKILL_DIR>/agents/`；默认使用 general-purpose 子代理，
Qoder IDE 无此类型时由 Stage 0 安装为项目级 agent。主代理读取说明书全文一次，
然后只传 `taskFile`（及必要路径）。

**所有阶段共用一个通用子代理**：默认 `general-purpose`；IDE 无此类型时安装
`microservice-general-purpose`。每个阶段只是传给它的说明书不同，使用方式不变。

| 用途 | 说明书（作为 prompt 传入） |
|---|---|
| A-1 逐文件标签+详情 | `agents/semantic-analyzer.md` |
| A-4 代码归属 | `agents/ownership-analyzer.md` |
| 2B Louvain 社区语义复核（只建议） | `agents/community-refiner.md` |
| Phase 10 启动配置推理 | `agents/startup-config-analyzer.md` |
| Phase 7 跨服务重构 | `agents/cross-service-refactorer.md` |

- 子代理输出写 `task_<i>.result.json`，只回复一行 `done` / `failed: 原因`
  （回复不符协议时以结果文件为准，不阻塞流程）
- 语义/归属子代理只读源码、不修改；跨服务子代理可修改目标工程
- `file-migrator` 子代理已废弃（Phase 5 由 batch_migrate.py 完成）

## 使用的脚本一览

| 脚本 | 阶段 | 用途 |
|---|---|---|
| `run.py` | 1 | 静态依赖提取（唯一入口） |
| `prepare_semantic_batches.py` | 2A | 扫描文件、切分详情/归属批次、续跑状态 |
| `merge_semantic_results.py` | 2A | 校验并合并子代理结果（四个 JSON） |
| `tree_manager.py` | 2A/3 | 系统树 CRUD/校验 |
| `extract_shared_classes.py` | 2A | 语义/算法模式共享类检测 |
| `algorithms/louvain/algorithm_split.py` | 2B/2C | 算法模式划分（含共享检测/命名） |
| `split.py` | 2B | Louvain 划分（static） |
| `evaluate.py` | 2E | 划分质量评估 |
| `prepare_migration_mapping.py` | 4-P3 | classInfoNew |
| `generate_parent_pom.py` | 4-P4 | 父 pom 渲染（版本来自 Agent 写入的 manifest.techStack） |
| `generate_service_config.py` | 4-P4 | serviceConfig |
| `batch_migrate.py` | 4-P5 | 批量迁移（含残留自检） |
| `extract_inter_dependencies.py` | 4-P6 | 跨服务依赖提取 |
| `prepare_refactor_tasks.py` | 4-P7 | 任务准备（机械类型直接处理） |
| `group_refactor_tasks.py` | 4-P7 | 冲突分组波次 |
| `summarize_refactor_results.py` | 4-P7 | 结果汇总 |
| `validate_project_structure.py` | 4-P9 | 结构验证 |
| `scan_startup_config.py` | 4-P10 | 扫描候选配置证据（非结论），生成值模板 |
| `apply_startup_config.py` | 4-P10 | 按 Agent 确认结果生成隔离覆盖配置（可选加速器） |
| `startup_services.py` | 4-P10 | 打包并启动业务服务，按端口可连验收 |
| `install_custom_agents.py` | 0 | IDE 无 general-purpose 时安装通用项目级子代理 |
| `partition_to_services.py` | 2B/3 | partition → sum_microservice（算法模式桥接） |
| `sum_to_partition.py` | 2A-A6 | sum_microservice → partition（语义模式评估桥接） |
| `prepare_community_review.py` | 2B | 碎片化指标 + 社区语义复核任务 |
| `merge_community_suggestions.py` | 2B | 合并建议为 refinement-proposal（不改 partition） |

## 错误处理

- 语义批次失败 → 只重试失败批次；`prepare_semantic_batches.py --status` 查看进度，
  `_merge_report.json` 查看缺失/错误；覆盖不足时不得默认继续
- `java not found / UnsupportedClassVersionError` → 按 Stage 0「Java 21 检查协议」处理
- `generate_parent_pom.py` 报 `missing_tech_stack` → 回到 Phase 1.2，由 Agent 重新读取根 pom + 子模块
  pom 推断实际版本并写入 manifest.techStack；仍无法确认时询问用户，禁止使用默认版本
- 文件迁移失败 → 记录失败，继续后续文件
- 跨服务重构失败 → 记录失败，继续后续依赖
- 编译失败 → 最多 3 轮自动修复；仍失败停止并报告
- Phase 1-4 关键失败（输入/方案文件缺失）→ 停止并报告
- 子代理结果 JSON 非法/字段缺失 → merge 拒绝；修复结果文件或重跑该批次

## 约束与规则

- 严格按阶段顺序执行；后一步优先复用前一步输出
- 不修改原单体项目任何文件；不擅自引入不兼容框架；不做大规模业务逻辑重写
- 不改变原工程技术栈代际：Boot/Cloud/Java 版本与 `javax`/`jakarta` 命名空间必须与应用实际一致
  （支持 Boot 2.x/3.x/4.0.x）；版本由 Agent 读取 pom 推断，脚本不内置版本映射表
- 不引入复杂 fallback/熔断机制（除非原项目已有）
- 可运行优先：配置无法精确拆分时保守复制；依赖无法解析时先保证编译通过并记入 manualReviewItems

## 成功标准

1. 每个微服务有 pom.xml、主启动类、配置文件（name/port 正确）
2. 源文件全部迁移；跨服务依赖已处理（Feign/本地化/人工清单）
3. 至少一次 Maven 编译验证（本次交付标准=编译通过）
4. 如执行 Phase 10：各业务服务端口可连；缺依赖/失败需有明确报告
5. 生成最终重构报告
部分成功：大部分服务可编译 + 少量跨服务依赖待人工 + 明确问题清单与修复建议。

## 依赖与环境

- Python（uv 自动管理，`pyproject.toml`）：networkx、python-louvain
- 外部：Java 21+（Stage 1 静态分析器硬性要求）、Stage 4 编译 JDK（≥ 原项目 `java.version`，
  Boot 3/4 ≥ 17）、Qoder general-purpose 或项目级自定义子代理（语义模式）、Maven 与构建依赖网络
- 语义模式**不需要** API Key / `.env` / 外部模型端点

## Token/成本优化

- 大文件由子代理截断 ~15K 字符；按文件数/字符数切批
- 算法模式零外部调用；语义/归属任务与结果均落盘，支持断点续跑
- 子代理上下文管控（一行回复、只记进度）；主代理不读源码正文
