---
name: icms-doc-agent
description: iCMS（鸿雁）与阿里云帮助中心内容写作和管理。当用户需要查询、编写、改写、翻译或审核 iCMS 文档、产品材料和公告，处理 XDITA、文档引用、多语言资源、PlantUML 图示，或处理 Aone 文档需求、缺陷、评审及发布时使用。用户提供 iCMS/帮助中心文档 URL 或相关 Node ID、ABC ID、ditaId、fileId、imageId、Aone 文档工作项 ID 时也适用，无需显式指定 Skill 名称。
---

# icms-doc-agent

iCMS（intelligent Content Management System，鸿雁）内容操作和写作 Skill。使用方可独立安装，在支持 Skill 的 AI 工具中完成本地写作、校验和平台操作。睿知宝 Git/MDX 写作与跨平台迁移使用 `ruizhibao-doc-agent`。

运行环境需要 Python 3.10+。iCMS 操作需要 adoc、适配版本的 Node.js/npm 和阿里内网/BUC；Aone 操作需要 a1 及安装到用户级共享目录的 a1 Skill。帮助中心 SEO 查询、PNG 渲染和 SDK 示例验证的依赖按任务加载，见 `references/platform/dependencies.md`。

## 先确定任务层级

| 层 | 处理内容 | 主要入口 |
|---|---|---|
| L0 运行与安全 | 依赖、认证、工作目录、变更确认 | `references/platform/auth-and-tools.md`、`scripts/doctor.py` |
| L1 平台模型 | ICMS 层级、ID、状态、站点、语言、附件和图片资源 | `references/platform/icms-model.md`、`document-identifiers.md`、`content-lifecycle.md`、`resources.md` |
| L2 原子能力 | 查询/拉取/转换/资源上传与校验/评论/版本/节点等单步操作 | `references/operations/atomic-capabilities.md`、`scripts/cli.py` |
| L3 格式处理 | XDITA 组件、样式、annotated Markdown、流程图与线上 HTML 的确定性转换 | `references/platform/formats.md`、`references/platform/xdita/component-catalog.md`、`references/operations/puml-diagram-rendering.md`、`scripts/{xdita,diagram}/` |
| L4 写作判断 | 架构、语言、术语、文档类型、翻译、盲审 | `references/workflows/{architecture,native-writing,native-review,translate-review}.md`、`references/standards/` |
| L5 业务编排 | 写作、Aone、缺陷、评审、发布 | `references/workflows/` |
| L6 写作支撑 | 术语、产品写作约束、代码示例验证 | `references/operations/optional-capabilities.md` |

先读与任务直接相关的 reference，不要一次加载全部资料。

## 不可混淆的事实源

1. ICMS 未展开、未填充引用的 finalized/draft XDITA 是可编辑源内容的权威表示。
2. 本地 annotated Markdown 是保留 XDITA 组件语义的工作中间格式，不是线上事实源。
3. 帮助中心 HTML 和填充引用后的 XDITA 是渲染/解析视图；conref/xref 已可能被展开或重写，只用于验收，不得替代编辑源。
4. `conref` 以 `mcms_dita_` 开头的美杜莎/MCMS 组件由平台维护；标签、属性、引用 Key、内容和位置均按源 XDITA 原样保留。
5. XDITA `<comment>` 只是选段评论的透明锚点：标签内文本仍是正常正文并正常发布显示；真正的评论内容保存在 `ditaComment` 记录中，不进入线上正文。不得因正文被 `<comment>` 包裹而判定内容缺失或不发布。
6. `adoc icms push` 只推送草稿，不等于 publish；publish 后也不等于缺陷工作项已解决。
7. ABC ID 标识文档，Node ID 定位 ICMS 节点上下文，ditaId 标识某语言的具体内容版本。`nodeId`、`sourceId` 等原始字段必须结合数据源解释，不能只按字段名判断。
8. 当前发布矩阵和发布历史必须分开：`publication-matrix` 回答某篇文档现在有哪些站点/语言在线、下线、隐藏或重定向；`publication-history` 按 URL、ABC ID 或 Node ID 追踪该文档全部历史事件；`list-publish-history` 只查询个人工作台视角的历史。历史成功事件不能证明当前在线。写作中校验 xref 和迁移范围盘点统一使用当前发布矩阵，包括国际站印尼语和法语；源文中的旧引用只能作为候选，位于“下线文档”目录的目标即使仍有站点在线也不得继续引用。
9. 附件以 `fileId`、图片以 `imageId` 作为跨语言逻辑身份；各语言拥有独立物理文件，但 XDITA 必须复用同一附件 ID 或图片相对路径。上传资源不会自动修改 XDITA，资源上传、正文 push 和发布是独立状态转换。
10. 文档反向引用分两层查询：`incoming-topic-references` 按 Node ID 返回编辑源中指向目标节点的 `topicref/conref/xref`；`incoming-link-relations` 按 ABC ID 返回帮助中心发布关系中指向目标文档的 `link/redirect`。两者都不回答目标文档“引用了谁”，响应也不报告总数或分页；发布关系没有当前状态字段，判断引用方是否仍在线必须另查发布矩阵。

### 百炼迁移完成后的 ICMS 边界

- 百炼（SFM / Model Studio）迁移已经完成。自 `2026-08-25 23:30`（Asia/Shanghai）起，ICMS 不再是百炼帮助中心的内容或发布源，只用于追溯迁移前的历史 XDITA、版本、引用和发布行为；当前写作、导航、下线、重定向和发布转交 `ruizhibao-doc-agent` 与百炼现行 Git 工程。
- ICMS 在该时间点及以后即使显示发布成功，帮助中心也会因 ICMS 来源门禁而不消费。此类记录仅是 ICMS 操作历史，不得作为帮助中心上线成功、当前正文、现网版本或增量范围的证据。
- 收到百炼 ICMS URL、Node ID、ABC ID 或 ditaId 时只执行 R0 历史查询。百炼的 ICMS push、review 和 publish 已退出当前维护范围；相关内容变更应转到现行睿知宝 Git 工程。只有用户以后明确修改这条切换政策，才能重新评估 ICMS 写操作，普通任务授权不能隐式覆盖本边界。不得用截止时间后的矩阵/历史覆盖睿知宝 MDX。

详细关系见 `references/platform/formats.md`、`references/platform/document-identifiers.md` 和 `references/platform/content-lifecycle.md`。

## 运行前检查

先将包含本 `SKILL.md` 的目录记为 `SKILL_DIR`。以下命令中的 `$SKILL_DIR` 都指该目录，不指仓库根目录。

```bash
python3 "$SKILL_DIR/scripts/doctor.py"
```

或使用统一入口：

```bash
"$SKILL_DIR/bin/icms-doc-agent" doctor
```

定位规则：

- 通过当前 Skill 文件位置确定 `SKILL_DIR`，不依赖仓库名或本机绝对路径。
- 任务产物写入 `ICMS_DOC_WORKDIR`；未设置时写入调用方当前目录下的 `.icms-doc-agent/`，绝不写入 Skill 目录。旧变量 `ALIYUN_DOC_WORKDIR` 仅作兼容回退。
- `adoc icms pull` 会在进程当前目录创建合集工作区且不支持指定输出目录。单独使用本 Skill 时必须先建立 `ICMS_DOC_WORKDIR` 下的任务子目录并以其作为进程 `cwd`；跨 Skill 调用时使用上层业务 Skill 持有的任务目录。禁止从仓库根目录、目标工程或 Skill 目录直接执行 `pull`。
- `a1` 优先使用 `A1_BIN`，其次使用 `PATH`，不查找特定 AI 应用目录。
- `adoc` 优先使用 `ADOC_BIN`，其次使用 `PATH`。
- 不复制 `~/.adoc`、`~/.config/a1`、浏览器 Cookie、SSO ticket 或任何本地 `.env`。
- ICMS REST 默认复用 adoc 登录状态；收到明确的 401 后自动续期、写回 adoc 配置并将原请求重试一次。只有长期登录会话失效时才要求 `adoc auth login`。
- 依赖检查不等于安装授权。先运行 `doctor --task <icms|aone|diagram|seo>`，按 `references/platform/dependencies.md` 确认缺失项和安装/升级计划后再执行；a1 Skill 安装和更新显式指定 `--location "$HOME/.agents/skills"`。
- 可信 KE 由使用方按 `references/platform/local-config.md` 指定；按文档实际 `spaceId` 取稳定身份名单，缺失时不授予 KE 身份。名单存放在 Git 忽略的本地配置中，测试和示例使用张三、李四等虚拟身份。

## 风险分级

| 级别 | 示例 | 执行原则 |
|---|---|---|
| R0 读取 | 查询文档、Aone、评论、版本、发布历史；抓线上页面 | 可直接执行并报告来源 |
| R1 本地产物 | 转换 XDITA/MD、生成报告、修改工作副本 | 保留源备份并验证 |
| R2 草稿变更 | push、create-version、create-node、附件/图片上传、Aone update/comment | 展示目标和参数；用户已明确要求该变更时执行，否则先确认 |
| R3 流程状态 | publish、pass/finish review、mark fixed、revoke、取消指定待发布任务 | 用户已明确要求该动作时直接执行；成功后重新查询状态 |
| R4 破坏性 | delete node/draft/workitem、覆盖 finalized、取消全部待发布任务等批量外部写入 | 用户已明确要求删除/覆盖/取消全部的精确范围时执行；逐项解析、记录并验证 |

任何凭证只允许由现有 CLI/环境读取；日志和错误输出必须脱敏。

### 确认只收集一次

确认用于明确动作和目标范围，而不是重复收集同一句口令。明确授权后继续核验目标与状态，既避免无意义的重复询问，也防止将原授权延伸到新的对象或操作；动作、目标或范围发生变化时重新确认。

- 用户当前请求以明确动词和范围要求外部变更（例如“撤回中英文评审并删除草稿”），即视为已确认该请求内的 R3/R4 动作。只读解析出的 Node ID、语言和 ditaId 与标题、范围一致时，展示目标后直接执行，不再要求用户重复回复“确认”。
- “逐项确认”表示写前逐项解析目标、核对状态并写后逐项回查，不表示对同一明确请求逐项追问。
- 先按来源解析 ID：帮助中心 URL、线上 `window.globalData.nodeId` 和搜索表 `node_id` 是 ABC ID；ICMS 内容 URL 的 `n=`、Map tree 和 adoc `--node-id` 是 Node ID，URL 的 `m=` 是预期根 Map ID。ICMS 内容 URL 必须交给 `resolve-doc-id --url` 做来源感知解析，禁止直接传给只支持帮助中心 URL 的 `adoc icms query doc --url`。只有裸数字且没有来源上下文时，才同时尝试 Node ID 和 ABC ID。若只有一个候选与标题、语言、空间和 Map 一致，可视为唯一解析结果；若标题不符、存在多个候选、范围扩大或用户只说“处理/清理”而未明确动作，停止并请求澄清。
- 普通文档任务优先接收 URL、ABC ID 或 Node ID，再用只读查询解析 ditaId、topicId 和评审流程 ID；不要在接口尚未需要时要求用户提供内部 ID。`map_dir` 的 `sourceId` 例外表示子 Map ID，必须走结构解析规则。
- CLI 的 `--yes` 表示 agent 已根据以上规则确认授权；R4 仍需额外 `--force`，防止命令误触。
- 取消待发布任务必须取得动作明确的授权。“分析、检查、处理、清理待发布列表”只授权读取和诊断；只有用户明确说“取消/结束/删除发布任务”才授权取消。按 `changeRequestId` 展示预检快照后执行；用户明确要求“全部”时才可使用 `--all --yes --force`，预检后新增任务不继承原授权。

## 任务路由

### 查询 ICMS、工作台或文档元数据

读：

- `references/platform/icms-model.md`
- `references/platform/document-identifiers.md`
- `references/operations/atomic-capabilities.md`
- 需要精确端点时再读 `references/platform/icms-api/endpoints.md`

优先顺序：adoc 已覆盖的操作用 adoc；未覆盖的 REST 操作用 `scripts/icms/cli.py`。

### 查询、上传或校验附件和图片

读：

- `references/platform/resources.md`
- `references/operations/atomic-capabilities.md`
- `references/platform/xdita/component-catalog.md`
- 需要精确接口时追加 `references/platform/icms-api/endpoints.md`

查询详情和验证语言资源是 R0；上传新逻辑资源或为既有逻辑 ID 补传语言实体是 R2。上传前先执行 `--dry-run`，正式上传必须有用户对精确资源范围的明确授权并传 `--yes`。资源命令不得输出 OSS 签名 URL、上传 policy、STS 凭证或 callback。上传成功后再单独修改 XDITA、push 并回拉验证，不能把已上传解释为已写入或已发布文档。

### 生成或重绘流程图、时序图

读：

- `references/operations/puml-diagram-rendering.md`
- 图片需要上传 ICMS 时追加 `references/platform/resources.md`

本地 `.puml` 是流程语义的单一事实源，使用 `diagram validate/render` 生成 SVG/PNG。内置样式统一为 `default`；调用方可用 `--style-file` 深度覆盖样式。当前只承诺 reference 中列出的常用序列图子集，未支持语法默认阻断并报告行号，禁止静默丢弃流程节点。生成图片是 R1；上传、写入 XDITA、push 和发布仍是互相独立的外部状态变更。

### 转换或直接修改 XDITA

读：

- 属于帮助中心内容变更时，先读 `references/workflows/writing.md` 确定语言和版本范围
- `references/platform/formats.md`
- `references/platform/xdita/component-catalog.md`
- `references/platform/xdita/ANNOTATION_GUIDE.md`
- 修改结构时追加 `ANNOTATION_MODIFICATION_GUIDE.md`
- finalized 基线定点重建时追加 `references/operations/xdita-targeted-edits.md`

本路由只决定编辑表示和格式验证，不缩小内容生产的语言范围。小范围定点修订优先直接修改 XDITA，但默认仍分别处理同一文档的中文和英文版本。只有首次写作、大范围架构调整或跨语言重写时才进入 annotated Markdown 管线。每次回转都运行 round-trip 验证。

定点修改不得以已有草稿作为内容基线。先用 `icms finalized-snapshot` 固定上一
finalized 的未填充 XDITA，再以声明式计划重放本次确认的变更。取消普通文档 conref
并保留内容、给已有元素设置 `props="china|intl"`、给精确行内片段包装站点条件时，
使用 `xdita apply-operations`，不要为单篇文档临时编写整页构建脚本。该命令只替换
计划覆盖的精确字节范围，操作报告必须保留 finalized 基线身份和每个精确目标；候选
仍需运行既有 round-trip、结构和 MCMS 校验。`mcms_dita_*` 平台托管 conref 永不取消。

本 Skill 必须独立解释和处理 ICMS/XDITA。跨平台迁移不能成为理解 XDITA 组件的前置条件；目标平台转换规则由目标平台 Skill 持有。

### iCMS 内产品材料和公告文章的翻译

适用于 iCMS 托管内容，不限帮助中心文档。进入下面的写作和 XDITA 流程，同时读取 `references/workflows/translate-review.md`：产品事实优先、术语一致、保留字段、条件与步骤归属，按纯文本或 XDITA 载体处理结构，不扩大商业主张或改写指标含义。译文写入本次任务的独立工作副本，不固定输出文件名，不覆盖其他任务；push、评审和发布分别授权。

### 新建、修改、改写或翻译帮助中心文档

读 `references/workflows/writing.md` 和 `references/workflows/xdita-pipeline.md`，再根据当前阶段加载 `architecture.md`、`native-writing.md` 或 `native-review.md`。根据文档语义类型加载：

- 通用写作原则：`references/standards/common/writing-principles.md`；组织内容时再读 `writing-patterns.md`，涉及表格或 Tab 选型、标题、相关文档时，按需读取对应文件
- 仅目标语言的 `references/standards/common/language-configs/<lang>.md`，不读取全部语言规范
- `references/standards/doc-types/<type>.md`
- 对应产品资料（如存在）

Tablestore SDK 入口与实践教程分别加读 `references/standards/products/tablestore/sdk-landing.md`、`solution.md`，不把其中的类型和接口当作其他产品默认值。
Tablestore SDK reference 文档额外读取 `references/standards/products/tablestore/sdk-reference.md`；SDK landing 引用和跨语言标题分别按同目录的 `sdk-reference-landings.md`、`sdk-reference-titles.md` 处理。处理时序模型时，追加读取 `references/products/tablestore/timeseries.md`。
处理 SQL 查询时，追加读取 `references/products/tablestore/sql-query.md`。
处理局部事务时，追加读取 `references/products/tablestore/local-transactions.md`。
处理智能语音交互（NLS）文档时，追加读取
`references/products/nls/maintenance-and-release.md`，按最新内容核验站点能力及 AI 增量，
不以历史版本差异或条件标签推断国际站不支持；发布遵循通用矩阵保持策略。

默认语言范围：KE 负责简体中文和英文的同步写作，其他语言由横向团队或自动化流程根据中文或英文翻译。因此，KE 未明确限定语言时，帮助中心文档生产同步处理简体中文和英文；只给出其中一种语言的 URL、源文档或问题描述不视为单语限定。只有“只处理中文”、“只修改英文”等明确要求才缩小语言范围。繁体中文、日语、印尼语和巴西葡萄牙语等其他语言默认不处理。详细规则见 `references/workflows/writing.md`。

处理顺序：核实材料 → 按需安排内容结构 → 写作 → 根据风险检查 → 转回 XDITA 并验证 → push。表达优化不能改变语义；局部小改无需自动重构全文或安排两人评审。具体检查范围见 `native-review.md`。默认不 publish。

### 处理 Aone 文档需求

读：

- `references/platform/aone-a1.md`
- `references/workflows/aone-writing.md`
- `references/schemas/aone-analysis.md`

使用 `a1 project workitem` 获取详情、评论、活动、附件和关系。先归一化为稳定 schema，再进行可行性判断。

### 修复 ICMS 缺陷工单

仅转交工作项不进入文档修复流程：使用 `update-work-item --handler-emp-id`，按[原子能力](references/operations/atomic-capabilities.md)预检、授权和回查；它不同于文档评审人的 `update-reviewer`。

读 `references/workflows/icms-bug-fix.md`。脚本只负责拉取、落盘、push 和状态更新；是否为真实错误及如何修复由 agent 根据 XDITA 和上下文判断。只有文档真正发布后才能 mark fixed。

### 批量评审待评审文档

先读 `references/platform/formats.md` 和
`references/platform/xdita/component-catalog.md`，区分编辑源与渲染结果，了解条件标签、
隐藏内容，以及正文评论锚点与独立评论记录的区别。再读
`references/workflows/icms-review.md` 和其中的评审标准。只对确认的事实错误提交评论，
不因风格偏好退回评审。提交 pass/finish 属 R3。

### 核验帮助中心页面或查询 SEO

读 `references/platform/online-help.md`，用 `fetch-online` 获取同站点、同语言的真实正文。HTTP 200 不代表有正文，风控壳、SSR 与 hydration 差异不能作为内容缺失结论。需要 SEO 元数据时追加 `references/platform/dataworks-sql.md`，用 `help-center-seo` 批量读取产品快照。两项均为只读查询，按任务指定产品、站点和语言范围。

### 发布、撤回、取消待发布任务、关闭工单

读 `references/workflows/publish-and-state.md`。把 push、review、publish、resolve 看成四个独立状态转换，每步重新查询验证。

publish 仍须获得明确授权。迭代已有文档时，若 KE 未限定站点，必须通过 `publish-document` 按语言保留当前直接在线且未重定向的中国站/国际站矩阵；只有中国站就只发中国站，只有国际站就只发国际站，两站都在线才发两站。当前没有直接在线目标时不得猜测，新文档或扩站必须由 KE 明确指定站点；完整规则见 `references/workflows/publish-and-state.md`。

智能语音交互（NLS）同样遵循上述矩阵保持策略。发布前按产品规则核验站点条件内容，
不能因历史 `china` 标签或版本差异跳过国际站目标。

## 统一命令入口

```bash
"$SKILL_DIR/bin/icms-doc-agent" doctor
"$SKILL_DIR/bin/icms-doc-agent" aone get <workitem-id>
"$SKILL_DIR/bin/icms-doc-agent" aone comments <workitem-id>
"$SKILL_DIR/bin/icms-doc-agent" aone activity <workitem-id>
"$SKILL_DIR/bin/icms-doc-agent" icms <icms-ops-subcommand> [args...]
"$SKILL_DIR/bin/icms-doc-agent" icms resolve-doc-id --abc-id <id> --lang-id 1 --lang-id 2 --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms document-authors --node-id <id> --lang-id 1 --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms incoming-topic-references --node-id <id> --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms incoming-link-relations --abc-id <id> --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms verify-mcms --doc-id <ditaId> --node-id <nodeId> --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms publication-history --abc-id <id> --target intl:id-ID --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms attachment-detail --file-id <fileId> --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms image-detail --image-id <imageId> --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms upload-attachment --space-id <spaceId> --lang-id 1 --file <path> --dry-run --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms upload-image --image-id <imageId> --lang-id 2 --file <path> --dry-run --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms verify-image-language --image-id <imageId> --lang-id 2 --expected-sha256 <sha256> --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms finalized-snapshot --node-id <id> --lang-id 1 --output finalized-zh.json --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms list-wait-publish --space-id <id> --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms cancel-wait-publish --change-request-id <id> --dry-run --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms publish-document --node-id <id> --lang-id 1 --lang-id 2 --dry-run --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms submit-review --node-id <id> --lang-id 1 --root-map-id <id> --space-id <id> --review-type R3 --reviewers <ids> --dry-run
"$SKILL_DIR/bin/icms-doc-agent" icms finalize-document --node-id <id> --lang-id 1 --lang-id 2 --dry-run --pretty
"$SKILL_DIR/bin/icms-doc-agent" icms revoke-review --node-id <id> --lang-id 1 --lang-id 2 --yes
"$SKILL_DIR/bin/icms-doc-agent" diagram validate --input flow.puml --style default --json
"$SKILL_DIR/bin/icms-doc-agent" diagram render --input flow.puml --output flow.png --svg-output flow.svg --report render-report.json --style default
"$SKILL_DIR/bin/icms-doc-agent" xdita to-md --xdita source.xdita --output-dir conversion
"$SKILL_DIR/bin/icms-doc-agent" xdita to-xdita --markdown conversion/annotated.md --output final.xdita
"$SKILL_DIR/bin/icms-doc-agent" xdita apply-operations --baseline-snapshot finalized.json --plan changes.json --output candidate.xdita --report apply.json
"$SKILL_DIR/bin/icms-doc-agent" xdita review-context --input rendered.xdita --pretty
"$SKILL_DIR/bin/icms-doc-agent" fetch-online <url>
"$SKILL_DIR/bin/icms-doc-agent" help-center-seo --help
```

查看完整帮助：

```bash
"$SKILL_DIR/bin/icms-doc-agent" --help
```

## 写作与平台原则

- 先确定“谁做什么”，再写条件和结果；官方文档不用研发口语。
- 技术事实、平台行为和写作规范分开：事实进入产品/平台 reference，表达规则进入 standards。
- 新增的公网链接和语境化 xref 使用明确 link text；ICMS 源 XDITA 中已有且目标仍有效的自闭合站内 xref 由平台根据 `xRefVOList` 解析标题，纯往返时按原样保留。当前发布矩阵判定目标失效时，替换目标属于必要的内容修订，不受纯往返保留规则限制。
- 新增和本次修改范围内保留的跨文档 xref 按 `writing.md` 的可见范围检查：当前交付站点/语言与引用及祖先条件共同决定需要在线的目标。查询可覆盖四个组合，但不强制单站分支的引用也覆盖另一站；下线目录和失效目标仍不得沿用，不为绕过校验给正文随意加标签。
- 新增附件或图片时，先上传并验证当前生产范围内每种语言的物理文件，再把同一 `fileId` 或 `../images/p<imageId>.<ext>` 写入各语言 XDITA。附件和图片的签名 URL 都不是稳定正文地址，禁止持久化；完整不变量见 `references/platform/resources.md`。
- 流程图和时序图以 `.puml` 为语义源，使用 `diagram render --style default` 生成 SVG/PNG；视觉差异通过经过校验的 `--style-file` 表达，不手工修改派生图片。中英文图中文字分别本地化并渲染，上传与引用仍按图片资源流程处理。
- 新建节点时，create-node 创建节点骨架并按节点名称生成初始 Node Slug；title、topictitle、searchtitle、keywords 和 XDITA 中的 slug 镜像由写作阶段补齐。发布前还要按规范确认中文“别名”对应的共享 Node Slug。
- `keywords` 是用字符串承载的关键词数组，所有语言都使用半角逗号 `,` 分隔数组项。中文正文使用全角标点的规则不适用于这个结构分隔符；不得把中文 `keywords` 中的半角逗号改成全角逗号 `，`。
- 以现有节点为锚点新建文档前，先从根 Map 树确认锚点类型。`map_dir`（手册）是根 Map 中对子 Map 的引用，必须使用 `create-node-under-map-dir`，不得把根 `mapId` 与锚点 Node ID 直接作为 `create-node` 的 `mapId/parentId`。
- 新建节点的评审类型按“显式 `--review-type` → 实际目标手册配置 → 系统默认 R1”解析。R1=默认评审（编辑+技术），R2=专业评审（一审+二审+技术），R3=轻量评审（单一评审人）；`map_dir` 必须继承 `sourceId` 指向的子手册。完整字段矩阵见 `references/workflows/icms-review.md`。
- `adoc query` 的 Node Slug 是各语言共用的线上 URL slug；发布接口把它作为 `nodeAlias`，不从英文 XDITA 单独取 slug。中文“别名”读取 xMetaList slug，但写作时必须让 `<head>` meta slug 与 xMetaList slug 完全一致。create 时按规范设置目标值；modify 默认沿用，只有明确迁移 URL 时才修改。
- Agent 发布 ICMS 文档统一使用 `icms publish-document`，不直接调用底层 `adoc icms publish`。封装会在正式请求前查询当前发布矩阵并逐语言派生精确站点，避免一次普通迭代把中国站单站或国际站单站扩成双站；正式发布后还会回查 ditaId、版本和意外扩站。
- targeted modify 跳过架构重排；targeted create 默认仍执行架构设计，除非用户显式要求跳过。
- 迭代文档默认保持中英文版本同步：先对中文 finalized 使用 `create-version` 创建目标版本，再对英文 finalized 使用 `adoc icms push --new-version --version-type <type>` 对齐中文版本；不要对英文直接使用 `create-version`。英文零版本使用 `create-en-draft`。完整分支见 `references/workflows/writing.md`。
- 迭代版本的需求元数据按来源二选一：能获取 Aone ID 的 Aone 需求只关联 `aoneId`，不再填写 `reason`；非 Aone 需求不填写 `aoneId`，`reason` 只概括主要变更点，不罗列逐项改动。版本类型仍按变更性质单独填写。完整规则见 `references/workflows/writing.md`。
- ICMS 文档完成 create/modify/translate/bugfix 并写入服务端后，最终答复按文档返回可点击的 ICMS 验证链接。中英文同时修改时，每篇文档只返回中文 ICMS 链接；显式单语修改时，返回实际修改语言的链接。标签写清内容变更范围、链接所属语言、版本和状态；不能只给 ID 或帮助中心公网 URL。完整输出模板见 [最终答复中的 ICMS 验证链接](references/workflows/writing.md#最终答复中的-icms-验证链接)，端点说明见 `references/operations/atomic-capabilities.md`。
- `--override` 原位覆盖 finalized 只有英文支持，且不会留下新版本记录，属于 R4；只有 KE 明确选择不保留版本记录或明确要求英文原位覆盖时使用。中文 finalized 即使传 `--override` 也会自动创建新版本，不能用它实现中文原位覆盖。

## 失败处理

1. 认证失败：停止写操作，给出 `adoc auth login` 或 `a1 auth login --buc`，不回显 ticket。
2. push 冲突：重新 pull 最新服务端版本、重新应用本地改动，再验证并 push；不得绕过并发保护。
3. push 曾成功但内容稍后回退：先检查当前服务端内容和 `gmtSave`，优先排查仍打开的 ICMS 编辑页用旧快照整篇自动保存覆盖；不要误判为 `in_revision` 无法 push，也不要先撤评审、建版本或反复换写接口。用户关闭/刷新页面并要求重推后，从当前服务端内容重新应用修改，再用 adoc push。
4. 格式验证失败：保留源文件和失败报告，不把不完整 XDITA 推送到 ICMS。
5. Aone JSON 字段变化：保存脱敏原始响应，更新 adapter，不让下游工作流直接依赖原始字段。
6. 外部系统部分成功：逐项重新查询，报告成功/失败边界，不把整批描述为成功。
