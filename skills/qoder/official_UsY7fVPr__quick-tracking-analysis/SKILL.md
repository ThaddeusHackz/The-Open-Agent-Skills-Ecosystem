---
name: quick-tracking-analysis
displayName: QuickTracking增长分析
description: >
  QuickTracking 增长分析助手，面向 QT 客户提供埋点数据查询与用户增长分析能力。

  【分析模型】支持 10 类 OLAP 分析模型：事件分析（含维度下钻、趋势同环比）、
  漏斗转化、留存分析、分布分析、路径分析、归因分析、会话分析、间隔分析、
  用户属性分析、用户生命周期分析。另支持自定义 SQL 查询。

  【报告能力】可生成数据日报、周报、月报，内置异常预警与看板监控。

  【角色视角】4 种受众视角按需输出差异化报告：
  管理决策（高管/老板）、用户增长（增长/分析）、
  日常看数（一线运营）、通用标准。

  触发词：QT / QuickTracking / Quick A+ / 埋点 / 打点 / 事件分析 /
  漏斗 / 留存 / 转化 / PV / UV / 用户增长 / 日报 / 周报 / 月报 /
  自定义 SQL / 路径 / 归因 / 会话 / 间隔 / 用户属性 / 同环比 /
  看板 / 监控告警 / 异常预警
version: 0.7.2
---

# Quick Tracking 分析能力

QuickTracking 数据能力,**一个自包含 skill**:接入 → 选应用 → 分析 / 出报告。
平台无关 —— 上传到任意宿主(Claude Code / Qoder / deepAgents / 通用 agent),解压即用、零 `pip install`。

## 何时用(触发场景)

用户提到以下任一即用本 skill(即使没说 "skill"):**QuickTracking / Quick A+ / QT 数据**、用户增长数据洞察、**埋点 / 打点数据查询**、用自定义 SQL 查 QT / 跑 SQL 报表,或想查某应用的 **pv/uv/留存/漏斗/转化/路径/分布/会话/归因/用户生命周期**,生成**关键指标日报·周报·月报**,接入 QT / 配置 accessToken / 选择应用。

触发词:事件分析 / 漏斗 / 留存 / 分布 / 路径 / 归因 / 会话 / 间隔 / 用户属性 / 用户生命周期 / 同环比 / 维度下钻 / 关键指标日报 / 看板监控 / 监控告警 / 异常预警 / 自定义 SQL / SQL 查询 / SQL 报告 / 跑 SQL / 创建看板 / 新建看板 / 保存报表 / 存为报表 / 把分析钉到看板 / 人群分析·分群圈选 / 条件过滤(只看 iOS·排除渠道)/ 活动期对比·任意时间段对比 / 小时粒度趋势。

内部分三层(都在 `quicktracking/` 包内,对用户是一个整体):
**gateway**(入口·拦截 gate·owns config)→ **analysis**(场景封装,无状态)→ **core**(读 config 执行 QT OLAP / 看板只读);
`spine` 是框架无关的分发机制(纯机制,gate + 委派,依赖全注入)。架构图见 `assets/skill-architecture.png`,
深入分层/seam 见 [`references/architecture.md`](references/architecture.md)。

## 运行入口(任意平台 —— 命中即走鉴权 + 分析)

命中 skill 后,**统一从 `cli.py` 这一个口调工具**(gate 永远在此强制,输出恒为 JSON):

```bash
python3 cli.py <tool> [--account ACCT] [--json '{...}'] [key=value ...]
python3 cli.py list                 # 列全部工具
```

`cli.py` 在 skill 根:启动时把 skill 根注入 `sys.path`,再 `import quicktracking.*` —— 无需安装。

> **宿主 agent 运行操作手册(怎么一步步驱动 + 决策树 + 错误恢复)→ [`RUNBOOK.md`](RUNBOOK.md)。** 本文件是工具/参数参考,运行时操作流程看 RUNBOOK。

### 标准流程

1. **验接入** `python3 cli.py qt_auth_status` —— **永远是第一步,先于一切参数收集**(不要在授权前向用户索要 app_info_id 等业务参数)。未就绪 → 返回 `action:"authorize"` + `needs:[baseUrl,token]` + `prompt` + `saasOptions`(SaaS 预填站点)+ `tokenHint`(token 获取页):**这是一个授权动作,交宿主渲染授权卡片**,**分两步**收齐:
   ⚠️ **两步必须有先后、不能并问**:token 获取链接 = `<第一步选定的 baseUrl>/setting/asyncQa`,**先拿到 baseUrl 才拼得出可点链接**,所以**先收 url、再问 token**。
   - **第一步 · 选 QT 服务地址 baseUrl(endpoint URL)**:返回的 `saasOptions` 给了 SaaS 内置站点——**张北 `https://quickaplus-cn-zhangjiakou.aliyun.com` / 上海 `https://quickaplus-cn-shanghai.aliyun.com`**(每项还带一个可点的 `tokenUrl`),**让用户选一个**;私有化用户则**自填**部署地址(形如 `https://<qt-host>`)。**绝不替用户默认选哪个站点。** 选定后(可先 `qt_onboard` 只落 baseUrl)再进第二步。
     - ⚠️ **必须用宿主原生的「单选问答 / 选项卡」**(选项点一下就把选择当成回复返回的那种,如 AskUserQuestion)——选项 = `saasOptions` 两站点 + 「私有化自填」。**绝不要自己拼一个带「下一步 / 提交」按钮的自定义 HTML 小部件**:宿主通常不给自定义 HTML 的按钮接线,点了没反应、卡死流程。
     - **这张卡上同时挂一行试用引导**(给还没有 QT 的人):用返回的 `trialPrompt`/`trialUrl` 渲成「还没有 QuickTracking?免费试用:<trialUrl>」——别只埋在 prompt 文本里。
   - **第二步 · 填 accessToken**(qt_token / `X-Qt-Token`,用户自带、直接用、不 mint、无 AK):给用户一个**能直接点的链接**——SaaS 用所选站点的 `tokenUrl`,私有化用 `<上一步 baseUrl>/setting/asyncQa`(= 返回的 `tokenHint`,baseUrl 已落盘时它就是具体可点 URL),让用户打开页面复制 token 粘回。token 是自由文本,用纯文字消息收。
   - `ready:true` → 第 3 步。
2. **接入** `python3 cli.py qt_onboard --json '{"baseUrl":"https://quickaplus-cn-zhangjiakou.aliyun.com","accessToken":"<qt_token>"}'`
   —— 把两步收到的 baseUrl + accessToken 一并落盘。`baseUrl` 是 QT 服务地址(endpoint),机制上**SaaS 与私有化同一条路、无 host 白名单**(SaaS 用上面的内置站点地址,私有化填部署地址);accessToken 即 qt_token,**直接用、不 mint、无 AK**。
3. **选应用** 已接入但未选应用时,`qt_auth_status` 与业务工具(经 gate)都返回 `action:"select_app"` + `needs:[app]`:**交宿主渲染选应用卡片**。用 `qt_list_apps`(可 `search=关键词`)列出 → **让用户挑** → `qt_set_default_app app_info_id=<id>`。**绝不自动选第一个**(第一个常是测试应用、无看板;见 AGENTS 不变量 7);**也不要让用户手填 app_info_id**——id 一律从 `qt_list_apps` 结果里挑。选定后,业务工具的 `app_info_id` 即可省略(默认用已选应用,跨应用查询才显式传)。
   - ⚠️ **响应 `select_app` 的唯一正确方式 = 先调 `qt_set_default_app`,再调业务工具**。**严禁**把选中的 `app_info_id` 直接内联进业务工具(如 `qt_daily_report app_info_id=…`)来绕过选应用——内联只对那**一次**调用有效、**不落盘**(`qt_set_default_app` 才走 config 分支 `set_many` 写 `.qt/config.env`;业务工具走 delegated 分支,只消费 app_info_id、**从不持久化**)。绕过的后果:用户**每个任务都要重选一次**(周报选一次、日报又选一次)。
   - **持久化是 cwd 相对的**(`.qt/config.env` 落在当前工作目录)。宿主若每个任务起独立 sandbox/不同 cwd,文件带不过去 → 仍会重选。要跨任务/跨 cwd 记住:**注入环境变量 `QT_DEFAULT_APP`**(进程 env 优先、与 cwd 无关),或让所有任务跑在同一固定工作目录。
4. **分析** —— ⚠️ **事件/属性 key 必须真实,禁止猜**(对**所有模型**通用,不只 query):
   - **事件 key**:`qt_query`/`qt_trend`/`qt_drill_down`/`qt_funnel`/`qt_retention`/`qt_distribution`/`qt_path`/`qt_session`/`qt_interval`/`qt_attribute`/`qt_user_lifecycle`/`qt_anomaly_attribution` **及 `qt_save_report`** 全是 key 驱动 —— 事件 key 必须来自 **`qt_list_events`**(列出该 app 真实事件,如 `$$_page`(页面浏览)/ `$$_app_start` / `$$_cntrl` / 自定义 code)**或用户明确给出**;**禁止凭空猜**(如把"页面浏览"写成 `pv` → 查空)。
   - **维度属性 key**(`group_by` / filter / `qt_attribute`)同理:用 **`qt_list_properties(event_key)`** 拿真实维度 key + `subClass` + `propertyType`(group_by 要带 subClass,如 `[[key,名,subClass]]`;channel 等非 event/user 维度再带第 4 位 propertyType,或**直接把 qt_list_properties 的返回行传给 group_by**),或从用户 / 看板 schema 取,**别猜**。(人群/分群 crowd 是另一套 userFilter,本工具不返。)
   - **指标 = 事件 × `calc`(PV/UV 在这里,不在事件 key)**:同一事件按「主体 × 口径」组合 —— 设备:`uv`(去重数/UV)· `pv`(次数/PV)· `uv_avg`(人均);账号:`user_uv` · `user_pv` · `user_uv_avg`;实体EID:`euv` · `epv` · `euv_avg`。**真实可用组合用 `qt_list_preset_indicators(event_key)` 发现**(别背别猜,calc 命名不规则:人均是 `uv_avg` 非 `pv_avg`、实体前缀是 `e`)。indicator 第 3 位给 calc(`["$$_page","次数","pv"]`)或 dict `{"key":"$$_page","name":"次数","calc":"pv"}`(`qt_query`/`qt_trend`/`qt_save_report` 通用);**别把 `pv` 当事件 key**;形态传错会**显式报错**,不再静默兜默认 uv。
   - **时间窗语义(通用)**:`days=N` 是滚动窗口 —— 最近 N 个**完整天、止于昨天**(今天是部分天,混入会让趋势末点骤降、环比偏低;按 QT 站点日界 UTC+8 算)。**查某一天** → `date_range=("YYYY-MM-DD","YYYY-MM-DD")`(同一天);**要看今天** → 显式把 `date_range` 传到今天。问"今天的量"却不传范围 → 拿到的是**止于昨天**的数据,别误读。
   - **条件查询(filter / 人群)**:`qt_query`/`qt_trend`/`qt_drill_down`/`qt_funnel`/`qt_retention`/`qt_distribution`/`qt_session` 支持 `common_filter=[[key,op,value(,名)]…]`(条件 AND;op:`=`/`!=`/`like`(包含)/`!like`/`>`/`<`/`between`/`null`/`!null`…;value 传 list 即多选)——"只看 iOS""排除某渠道"用它;**维度 key/归属别猜**,首选把 `qt_list_properties` 的返回行加 `{op,value}` 直接传。**人群/分群**:先 `qt_list_segments` 列出已保存人群 → 返回行(或人群名)传 `segment=`;`segment_contain=False` = 排除该人群(如排除内部员工)。
   - **任何模型返回空,先怀疑 key 不对**、用 `qt_list_events` 核对,**绝不编数**。
   例:`python3 cli.py qt_list_events --json '{"search":"页面"}'` → 拿到 `$$_page` → `python3 cli.py qt_query --json '{"indicators":[["$$_page","页面浏览"]],"days":7}'` / `qt_daily_report` / …(`app_info_id` 可省 = 已选应用;跨应用才显式传)。未接入 / 未选应用 → 返回 `{"ok":false,"action":"authorize|select_app","needs":[...]}` 引导,**不崩**。

## 对外工具(运行时都经 gateway)

| 工具 | 类别 | 输出 |
|---|---|---|
| `qt_auth_status` / `qt_onboard` / `qt_auth_unbind` / `qt_list_apps` / `qt_set_default_app` / `qt_set_default_role`(报告默认角色:选一次落盘、后续报告自动复用,对称选应用) | 授权·配置 | JSON |
| `qt_list_events`(列出 app **真实事件 key** —— **所有分析模型**取数前都用它对齐 key,**别猜**) | 元数据/发现 | payload |
| `qt_list_properties`(列出某事件的**真实维度属性 key**:event/user/channel… —— group_by / filter / attribute 对齐用;含 subClass,group_by 要带上) | 元数据/发现 | payload |
| `qt_list_preset_indicators`(列出某事件的**真实预置指标**:属性×calc 组合,如 次数(pv)/去重数(uv)/人均 —— 把 PV/UV/账号/实体 术语发现化,**免背 calc**) | 元数据/发现 | payload |
| `qt_list_segments`(列出 app **已保存人群/分群** —— 返回行直接作分析工具的 `segment=` 入参,**别手编 reportId**) | 元数据/发现 | payload |
| `qt_query`(事件·多指标;`time_unit=hour` 可看小时粒度) / `qt_drill_down`(维度下钻;附 **`groups_ranked` 降序排行** + `top_n`,明细 rows 不截) / `qt_trend`(趋势+同环比;`compare` 还可传 `(from,to)` **任意对照期**,返回 `compare.series` 逐日对比线) | 即时查询 | payload |
| `qt_funnel`(漏斗) / `qt_retention`(留存) / `qt_distribution`(分布) / `qt_path`(路径) | 即时查询 | payload |
| `qt_session`(会话) / `qt_interval`(间隔) / `qt_attribute`(用户属性) / `qt_user_lifecycle`(生命周期) / `qt_anomaly_attribution`(归因) | 即时查询 | payload |
| `qt_sql`(**自定义 SQL 原样执行**,SQL 控制台同源链路;仅 SELECT/WITH + 本地危险模式预拦(禁系统库/表函数/基础设施函数),**仅查本应用业务数据**;ClickHouse 方言,结果上限 1000 行 —— 命中上限时返回里带 **`truncated:true`**,勿对截断结果求和/去重下结论) | 即时查询 | payload |
| `qt_daily_report`(**默认 = 应用级标准日报**,五区:基础流量 KPI≤5+各自趋势+日环比 → 基础校验(人均访问/跳出率) → ≤3 核心漏斗(跨板收集,显式 `funnel_steps` 优先) → 留存 → 异常波动;**空数据出空态占位卡、不消失**;`traffic_indicators`/`quality_calcs` 可按行业自定义;`scope=board` 为看板日报) / `qt_weekly_report` / `qt_monthly_report` | 报告 | **HTML** |
| `qt_sql_report`(多条自定义 SQL → 日周报同款 HTML:按数据形状自动出 KPI 卡/折线/饼图/排行/**漏斗**(windowFunnel+`##TOTAL##` 形态)/表格,**明细永不丢**(全量+分页平铺在图下)+ 原始 SQL 折叠留档;**SQL 原样执行**,安全约束同 `qt_sql`(见下)) | 报告 | **HTML** |
| `qt_board_monitor`(看板监控:5 预置规则 + tri-state 防假绿;宿主/cron 定时调) | 监控 | **HTML** |
| `qt_create_board`(新建看板到「我的看板」) / `qt_save_report`(把刚跑的分析存为报表并钉到用户选的看板) | 创建 | payload |

- **10 类 OLAP 模型全部可即时查询**:event(query/下钻/趋势)、funnel、retention、distribution、path、attribution、session、interval、attribute、userlifecycle —— 各工具入参/输出形态见 [`references/data-shapes.md`](references/data-shapes.md)。
- 即时查询 = 结构化 payload(框架渲卡片);报告类 = HTML。宿主不自带渲染时,日/周/月报、`qt_sql_report` 与 `qt_board_monitor` 可传 `out=<绝对路径>` → 工具直接落 HTML、返回里带 `htmlPath`(免去 import 内部 render)。
- **自定义 SQL**(`qt_sql` / `qt_sql_report`):SQL **原样执行**——skill 不改写业务逻辑,时间范围等条件就是 SQL 里写的;周期化由上层 agent 改写日期,skill 不猜。**安全(纵深防御 + 真边界):本地预拦危险模式(系统库 `system.*`/`information_schema`、表函数 `url·file·remote·s3·mysql` 等、基础设施函数 `version·hostName·dictGet`)→ 命中抛错;但本地正则可绕过,真正的租户/库隔离由服务端引擎语义校验(ClickHouse SQL 语法树)强制 —— `qt_sql` 仅可查本应用所属库的业务数据,跨库/系统表/表函数一律被拒。** 其余约束如实暴露:仅 SELECT/WITH(写操作显式拒绝)、engine 交互上限 1000 行(LIMIT 写更大也截断)、禁 `SELECT *`、分号分隔只执行最后一条。`qt_sql_report` 的 `period_label` 仅是展示文案,不参与执行。
- **报告耗时预期**:报告/重看板查询走 OLAP 异步轮询,同步等待**可达数分钟、无进度输出属正常** —— 勿过早判超时中断重跑(会加重后端负载)。周/月报 overview 自带 `insights`(KPI 涨跌摘要)+ `alerts`(异常预警,与日报口径一致)。
- **报告 `scope`**(日/周/月报通用,**默认 `overview`**):`overview` = 跨看板核心 KPI 总览 + 每看板迷你趋势图(`board_ids` 可省 → 自动挑有内容看板,**无需先选看板**,适合"生成周报"这类泛请求);`board` = 聚焦单看板的完整报告(KPI + 趋势/漏斗/留存/分布等**完整图表**,需 `board_id`;缺则返回 `needs:[board]`+推荐,让用户选、**不自动选**)。返回 dict 带 **`kind`**(`overview`/`report`)→ **宿主据 `kind` 选 `render_overview` / `render_report`**(HTML 由宿主渲染)。用户想深看某个看板 → 用 `scope=board`。
- **报告周期(按类型固定,别混淆,更别用错工具)**:`qt_daily_report` = **数据日当天**(KPI=当天值)+ 近 7 天趋势作上下文;`qt_weekly_report` = **近 7 天**;`qt_monthly_report` = **近 30 天**(均截至 `anchor`,默认今天)。**按用户说的时间窗选工具**:"过去30天 / 近一个月 / 月报" → `qt_monthly_report`;"过去7天 / 近一周 / 本周 / 周报" → `qt_weekly_report`;"昨天 / 某天 / 今天 / 日报" → `qt_daily_report`。**任意自定义天数**(如近 14 天)→ 用 `qt_query` / `qt_trend` 传 `days=N` 或 `date_range`,**别硬套日/周/月报**(否则标题周期对不上,如把"过去30天"塞给日报)。
- **自定义报告周期(周/月报)**:默认窗口如上(月报=近 30 天**滚动**窗口,非自然月)。两个可选入参覆盖默认:`calendar_month=true`(**月报专用**:取 `anchor` 所在**自然月** 1 号 ~ anchor —— 月末跑=完整当月如 5/1~5/31、月中跑=MTD)、`date_range=("YYYY-MM-DD","YYYY-MM-DD")`(**任意自定义周期**,如每月 15 号→次月 14 号;周/月报通用,优先级高于 `calendar_month`)。**日报不适用**(单日);标题按真实区间渲染、自动反映所选窗口。
- **报告角色 `role`**(日/周/月报通用,可选)——**按受众**出差异化报告,3 角色 × 3 周期 = 9 种(内容区块组合 + 视觉主题各异,周期定深度 日<周<月):
  - ⚠️ **role 像选应用一样:选一次 → 落盘默认 → 后续自动复用,不必每次澄清。** 首次出报告且**无默认角色**(`qt_auth_status` 的 `defaultRole` 为空)、用户又没点明受众 → **先澄清一次**(渲染角色卡:管理决策/用户增长/日常看数/通用标准)→ `qt_set_default_role role=<选中>` 落盘 → 之后 `qt_*_report` 由 spine **自动带上该角色、不再问**。"这次要管理视角"→ 单次传 `role=management`(不改默认);"以后都按增长看"→ `qt_set_default_role role=growth` 换默认。能从话里判定受众的**首次直接 `qt_set_default_role`、不必问**:老板/高管/经营复盘→`management`、增长/拉新/转化/留存→`growth`、运营看数/排查/明细→`ops`、通用/不分角色→`standard`。**绝不静默猜一个 role**(实测踩坑:没问就选 `ops`)。
  - `role=management`(**管理决策**,给高管/老板):全局 KPI(周期聚合)+ 同/环比 + 大盘趋势 + 健康度;exec 深蓝主题、少而精。
  - `role=growth`(**用户增长**,给增长/分析):AARRR 漏斗 + 留存 cohort + 关键转化漏斗;growth 青绿主题。
  - `role=ops`(**日常看数**,给一线运营):明细 KPI + 排行/占比/分布 + 逐日明细表 + 异常预警;ops 中性+告警主题、高密度。
  - 默认用平台预置事件(通用);`funnel_steps`(AARRR 事件序列,如 `[["viewDetail","看详情"],["addCar2","加购"],["joinMember2","入会"]]`)/ `retention` / `traffic_indicators` 可覆盖为业务事件。例:`python3 cli.py qt_monthly_report role=growth`(增长月报)。
- **报告呈现规范(图文并茂 + 干净,自行拼装 HTML 报告时同样适用)**:报告要**图文并茂**——**漏斗转化用漏斗图**、趋势用趋势图、占比用环形/饼图、对比用条形图,**别只堆表格数据**(内置 `qt_*_report` 已是离线 ECharts 图表化输出:funnel 区块走 ECharts `type:"funnel"` 漏斗图)。**面向用户的报告里不得出现方法论标签 / 知识库索引 / 内部工具名**(如 `对比法`/`RARRA` 之类方法 chip、正文里的 `qt_path`/`qt_distribution` 等脚手架名)——那是内部对齐用的,业务报告须干净。
- **报告分两层:模板固定结构 + 方法论动态生成分析判断**(`qt_*_report` 一把出 HTML、**不依赖读任何文档**——方法论已是代码规则、代码是真源):
  - **模板层(固定)**:`_compose_role_report` 定区块池/顺序/角色差异(KPI/健康度环/SVG 漏斗/留存/分布);固定的是**结构**,不是文案。
  - **分析层(动态·代码级)**:`_attach_insights` 给每块结构化洞察「**观察→判断→候选假设→动作**」(假设带"可能/通常"对冲、渲成独立『假设』标签 = 候选非结论);`_role_focus_section` 是**角色转换器**(同一事实→ management「经营风险与决策建议」/ growth「增长实验建议」/ ops「运营排查清单」)。这层让自动报告**不沦为换皮静态表**。
  - **agent 自由发挥槽(opt-in,更深个案补充、非每份必需)**:`narrative="<本期叙事>"`→「📝 本期概述」;`append_sections=[{type:"prose"|"progress"|"radar"|"compare_bars"|"table", …}]`→追加行动/OKR/行业模型区块(同主题渲染)。**只在填槽时**读 [`references/report-playbook.md`](references/report-playbook.md)(在代码已给的判断**之上**补个案归因/定制动作/行业模型,不重复);[`references/analysis-methodology.md`](references/analysis-methodology.md) = 全量 KB·仅深度查阅、非模板依赖。
  - **铁律**:方法论只塑判断,不得作方法标签 chip / 知识库索引(RARRA/小军师 等)露在用户报告;无数据支撑只写候选假设(措辞留余地)。
- `qt_onboard`:**唯一接入 = 两字段直绑**(`baseUrl` + `accessToken`)→ 落 `.qt/config.env` + 返回 `remember`。`baseUrl` 是 QT 服务地址(endpoint URL),SaaS 与私有化同一条路、不区分站点(SaaS 内置地址 / 私有化部署地址均可);`auth.resolve_base_url` 只读 `QT_BASE_URL`。
- 异动检测已由 `qt_board_monitor`(看板监控)产品化替代(早期 `qt_anomaly_detect` 冻结);异动**归因**(`qt_anomaly_attribution`)独立保留。
- **鉴权失败(token 失效 / 被拒,HTTP 401/403)→ 所有业务工具返回 `action:"authorize"`**:只走重新授权,**不提供任何取数 / 报告 / 创建能力**(鉴权失败时只剩授权逻辑)。取数失败 / 网络不通 → 如实报错;**报告取数全空也抛错、绝不返空壳供宿主编造**。
- 各业务工具复用哪个底座 Builder、报告分区/渲染细节 → [`references/data-shapes.md`](references/data-shapes.md)。

### ⚠️ 参数形态速查(AI 首调高发踩坑 —— 形态/参数名传错会**显式报错**或查空,别按直觉猜)

事件/属性入参**绝大多数是「列表/元组」,不是 dict**:只有 `qt_query`/`qt_trend`/`qt_save_report(type=event)` 的 `indicators` 兼容 dict(走 `event_indicator_fields`);**`qt_funnel`/`qt_retention`/`qt_distribution`/`qt_anomaly_attribution` 一律列表,塞 dict 必崩**(它们直接 `x[0]/x[1]` 索引)。下列入参均为**必填位置参数**:

| 工具 | 必填入参 | ✅ 正确形态 | ❌ 高发错 |
|---|---|---|---|
| `qt_funnel` | `steps`(≥2 步) | `[["$$_app_start","启动"],["$$_page","浏览"]]` = `[[key,名[,sub_class]],…]` | `[{"key":…,"name":…}]` / dict / 裸串 → `ValueError`(必列表) |
| `qt_retention` | `init_event` + `return_event` | `init_event=["$$_app_start","启动"]`、`return_event=["$$_page","浏览"]` = `[key,名[,sub_class]]` | 参数名写 `start_event`/`revisit_event` → 报错;**真名只有 `init_event`+`return_event`** |
| `qt_distribution` | `indicator`(**三元组**) | `["$$_page","浏览","pv"]` = `[key,名,calc]`,**calc 不可省** | 两元素 / 省 calc → `ValueError`;别用 `event_key=` |
| `qt_anomaly_attribution` | `target_event` + `touchpoints` | `target_event=["$$_page","浏览"]`、`touchpoints=[["$$_app_start","启动"],…]` = `[key,名[,event_type]]` | 纯字符串 `"$$_page"` → 报错 |
| `qt_board_monitor` | `board_id` | `board_id="<板ID>"`(从日/周报输出或 `recommend_report_boards` 取,**不自动选**) | 省略 → `TypeError: missing … board_id` |
| `qt_save_report` | `board_id`+`name`+`analysis` | `analysis.type` **仅 `event`/`funnel`/`retention`**(结构见 data-shapes) | `type="trend"` 等 → `ValueError 暂不支持` |

> 上表只列**形态高发坑**入参;时间窗(`days` 默认 7 / `date_range`)、`app_info_id`(默认=已选应用)等通用可选参数照常可省,完整入参见 [`references/data-shapes.md`](references/data-shapes.md)。

## config 契约(单一 store,摘要)

config 来源抽象成 `ConfigStore`,唯一实现 `FileConfigStore` —— **环境变量优先读 + 配置永远落盘**(无模式开关):

- **读** —— `.qt/config.env`(KEY=VALUE)hydrate 进 env,但**进程 env 永远赢**(绝不覆盖已有 env)→ 宿主注入的 `QT_SESSION_TOKEN`/`QT_BASE_URL` 优先、文件作回落。
- **写** —— onboard / 选应用等配置落 `.qt/config.env`(**AK 密钥拒绝落盘**),后续 cli 调用读得到。
- 沙箱**只注 `QT_BASE_URL`(endpoint)+ `QT_SESSION_TOKEN`**,无需任何模式变量;token 不落盘也能用(env 直读),onboard 后落盘则跨子进程都读得到。
- 完整 env 契约表(`QT_BASE_URL`/`QT_SESSION_TOKEN`)→ [`references/env-config.md`](references/env-config.md)。

## 看板取数(深契约)

看板走 `/qt/hsf/board/**`,有 groupType(PREDEFINE/USERDEFINE)、boardId 大小写、viewType 选取等真实环境实证的坑 ——
**做看板/报告相关取数前先读** [`references/board-api.md`](references/board-api.md)。

## 验证与发布

- 开发自检:`python3 smoke_test.py`(离线冷启动全量自检,以脚本输出计数为准)/ `--online`(真实站点,需 `QT_BASE_URL` + `QT_SESSION_TOKEN`)。
- 发布交互验收:像用户一样对话走一遍,见 [`VERIFY.md`](VERIFY.md)(只需 baseUrl + accessToken)。
- 发布打包:`bash package.sh` —— 只打这一个 skill 目录,自动排除 `.env` / `.qt-token.json` / `.qt/` / `__pycache__` 等本地态。
- ⚠️ 取数要出网到 QT endpoint;app 由用户指定,**绝不自动选 `list_apps` 第一个**。

## 改代码前

读 [`AGENTS.md`](AGENTS.md)(组共享不变量 + 各层"改/不改"边界)。第三方依赖只有 `requests`(底座 `qt_analysis` 的 HTTP 客户端)。
