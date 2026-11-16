---
version: 2.5.1
description: >
  设计稿像素级还原的测量驱动闭环方法。当用户提供设计稿/效果图/UI 截图要求还原、复刻、1:1 实现、像素级对比、
  高保真还原 HTML/CSS 时使用；即使用户只说"按这张图做出来"，只要强调还原度/细节一致也应使用。
  支持任意设计数据源：截图 / Figma 链接（MCP 直取）/ Figma code+SVG / Mergo zip 包 / MasterGo 图层链接（MCP 直取）/ Done zip / 任意 D2C 引擎产物。
  也支持增量换肤（reskin）：目标页面已有实现 + 新设计稿/新皮肤时，走「增量换肤模式」只还原差异区，未变化区域与素材严格不动，禁止从零重跑。
  还内置样式全集批量截图（style-set.js）：给设计师截页面全部 UI 状态的日/夜手机截图集、本地 mock 后批量截图、
  截样式全集/日夜间对比图、改动后重截对基线回归——h5-style-screenshots 能力已并入本 skill。
compatibility: "Node >=22; pngjs; Chrome 112+; Python 3 (仅 Mergo/Done 解压脚本可选)"
license: MIT
allowed-tools: Bash Read Write Edit Glob Grep SearchCodebase SearchSymbol get_figma_data download_figma_images get_frontend_code get_screenshot get_fonts
metadata:
  tags: pixel-perfect design-restore html-css forensics d2c 像素还原 设计稿 高保真 测量驱动
  category: devtools
  author: zhangbaowen.zbw
name: pixel-restore-next
---

# Pixel Restore — 设计稿 100% 还原闭环

目标：设计稿 → HTML/CSS，收敛到抗锯齿光栅化上限（地板值**逐例实测标定**，不预设数字），所有元素 ink 包围盒 Δ≤1px。
核心原则：**一切用像素数值说话，不用眼睛猜**。

**配套文件**（按需读，不必一次全看）：

- `GENERATE.md` — **生成侧规则（A/B 级输入必读）**：脏节点过滤 / 渲染策略信号表 / 布局推断纪律 / 资源导出验证 / 验证锚点契约
- `PLATFORMS.md` — Figma / Mergo / Done 的取数细节与平台专属坑 + 通用 D2C 产物消费规范
- `PITFALLS.md` — 环境坑、测量可靠性坑、CSS 机制坑、视觉细节清单、生成类坑
- `VERIFY.md` — **验证侧规则（Phase 3/4 必读）**：三层判定 / 语义层与 data-sem-allow 声明补偿 / 双层对比+全局偏移补偿 / judgment 契约 / 收敛熔断 / 基线回归
- `STYLE-SET.md` — **样式全集批量截图**（自 h5-style-screenshots 并入）：给设计截日/夜全集 / 交付走查 / 回归基线；含项目适配配置参考与踩坑手册

## 度量诚实性（最高优先级，违了整套方法就是假的）

pct 可以被作弊，作弊一旦发生，本 skill 的一切结论全部无效：

- **绝不把设计稿图片当页面背景/前景用**，也不切文字块/标签/图标贴图。页面必须是真实 DOM+CSS，否则数字归零但交付物一文不值。**例外**：特殊字体固定文案 / 复合装饰组件按 GENERATE.md §2 权重表裁决允许切图（落地本来就该用图的场景）——但必须逐项自参照声明，切图区的低 diff 不构成还原度证据。
- **照片类资源（头像/封面/未导出的图标缩略图）从设计稿裁切是允许的，但它们是自参照区**：diff 必然近 0，不构成还原度证据；报结果时逐项声明。同源只豁免内容，**不豁免尺寸/位置**——自参照区的 ink bbox 仍要核（实战踩过：照片内容全对但 CSS 尺寸大 4px）。
- 报数一律用 `pct`（分母 = 实际对比像素 cmp）**并带 params**；`pctAll` 会被透明边稀释，仅供历史对照。
- 不得靠"换窗口/换参数"把数字调好看；参数一旦选定，整个任务固定不变（锁定进 task.json，见 Phase 0）。
- **禁止静默降级**：输入数据等级不满足所选档位时，必须向用户声明「当前数据下还原精度上限约为 X」并经用户确认后才继续；禁止 agent 自行降级硬跑。脚本字段缺失同理：规则未生效必须在输出中声明。
- **期望值来源防伪**：expectations.json / 基线只能来自平台数据或上一轮验收产物，**禁止从当前实现页反推**（自己当自己裁判 = 作弊）；semantic-diff.js 拒绝消费 source 为 implementation 的期望值文件。
- **机器护栏的边界（自指声明，v2.1 起明示）**：floor 自登记、floorEvidence、证据注释、data-sem-allow 声明、层产物采集的机器校验全是**存在性检查**——拦得住手滑与遗漏，拦不住蓄意编造（格式正确的假话同样通过存在性检查）。最终兜底始终是 final-compare 人眼验收与交付报告的人工审查；本 skill 的判定结论是「在给定证据下自洽」，不是「被机器证明为真」。

## 环境准备

- 依赖 **Node ≥ 22**（截图脚本用全局 `WebSocket` 走 CDP，低版本直接 ReferenceError）、`pngjs` + 本机 Chrome（112+，`--headless=new`）。pngjs 解析规则：node require 从**脚本所在目录**向上查找（与 cwd 无关）——项目级用法能借到项目 node_modules；全局 clone 用法在 `~/.qoder/skills/pixel-restore-next/` 里 `npm i` 即可（package.json 已声明 pngjs，.gitignore 已含 node_modules/）；/tmp 下的一次性脚本则加 `NODE_PATH=$HOME/.qoder/skills/pixel-restore-next/node_modules`。
- 平台支持：**仅在 macOS 实测**。脚本无平台 API（node/python 跨平台），但 Chrome 路径、fish/沙箱条目、`/tmp` 工作目录都是 macOS 语境——Windows/Linux 用 `CHROME_PATH` 指定浏览器、工作目录换本机临时目录、`run.sh` 需 sh（Git Bash/WSL）或绕过它直调 node。这是**独立 git 仓库分发的 skill**，clone 到 `~/.qoder/skills/pixel-restore-next/` 即全局可用。
- 所有 node 命令前加 `NODE_OPTIONS=""`；脚本用绝对路径调用，**不要拷进项目**。
- 其余环境坑（终端吞命令、fish 限制、沙箱可写范围）见 `PITFALLS.md` 一节。

## 产物目录纪律（项目内零污染，强制）

本方法会产生大量中间文件（shot/diff/放大图/并排图/一次性脚本/解包的设计包），**全部放项目外**：

- 工作目录一律 `/tmp/pixel-restore/<任务名>/`（沙箱允许写 /tmp）。页面 HTML、切图、shot.png、diff.png、cmp-*.png、放大图、一次性 .sh/.py 全放这里。
- 脚本写出位置：shot-diff/final-compare 写到 **HTML/shot 所在目录**，crop-cmp 写到 **shot 所在目录**，zoom-* 显式传出路径 —— 只要 HTML 在 /tmp，产物就全在 /tmp。
- **唯一可以进项目的是最终代码**（按下文「落地」节移植进真实组件）。
- /tmp 会自动清（macOS 周期任务默认清 3 天未访问的文件 + 重启也清）：收尾时把成果落地成项目代码，并把关键结论（终值 CSS、pct、待办）写回任务总结/记忆，别依赖中间文件长存。
- 一次性测量脚本只维护**一个** `measure.sh`（改窗口就改它），不要攒 measure2/3/4…（多副本会参数漂移，事后无从分辨哪个是最新——本条规则作者自己都违反过）

## 坐标系（最先确立，最大坑）

全程只用 **canvas（1x 页面坐标）** 交流：

| 空间 | 含义 | 换算 |
|---|---|---|
| img | 设计稿 PNG 原始像素（sc 倍导出 + 导出边距） | img = canvas*sc + (ox,oy) |
| canvas | 页面 1x 坐标 | shot.png = canvas*dpr |

- ox,oy = 设计稿导出边距（**img 空间像素**，常见 0 或 24，含阴影/透明边），用 alpha bbox 或已知元素位置确认一次。换算只有一条：`img = canvas*sc + (ox,oy)`——别把 ox 当 canvas 偏移套成 `(ox+canvas)*sc`（实战踩过：Figma 导出稿 ox=24 套错公式，取窗偏 24/32 img px，位图 MSE 匹配一度误判「Figma 裁切与 cover 不符」）。
- **别假定 2x**：导出倍率必为整数。取一行 CJK 正文 ink 高 h，正确 sc 应使 h/sc 落在常见整数字号（12/14/16）**且**卡片 ink 宽/sc 落在合理移动端宽度（351-375），两条件交叉定 sc。
- 所有脚本支持任意倍率：`ox,oy[,sc[,dpr]]`（默认 2,2），如 3x 稿传 `24,24,3`；shot-diff 用第 9 参 sc。
- 自己写一次性测量脚本时，**先写清用哪个空间**。

## Phase 0：数据门禁（v2.0 新增，最先做）

拿到输入先定**数据完整性等级**，它决定生成侧能走多深、语义层有没有期望值可用：

| 输入 | 等级 | 生成侧深度 | 语义层期望值来源 |
|---|---|---|---|
| Figma MCP（Framelink/官方） | A | 完整 Phase 1（GENERATE.md） | get_figma_data 权威值 |
| MasterGo / Done MCP | A | 完整 Phase 1 | JsonDom 图层树 + 逐节点截图资产 |
| Mergo zip | A | 完整 Phase 1 | 图层数据 |
| Figma code+SVG / REST API | A- | 完整 Phase 1，资源手动补 | code/CSS 值 |
| Done zip / 任意 D2C 直出 HTML | B+ | 解析数据模型→结构重写 | 内联 style 提取 |
| 仅有 D2C 产物 HTML（无源数据） | B- | 同上 | 从 HTML 反推，**标注自证风险**（期望=产物自身，只能抓实现漂移，不能抓产物本身的错） |
| 纯截图 | C | 跳过 Phase 1，走像素取证 | 无（语义层降级，只跑像素+结构两层） |

**禁止静默降级**：数据等级不满足所选档位（如 C 级数据要求 A 档像素级验收）时，必须向用户声明「当前数据下还原精度上限约为 X」，用户确认后才继续。

**task.json（Phase 0 强制落盘，工作目录根）**：`{task, workdir, input:{type,source,grade}, params:{vw,vh,dpr,sc,ox,oy}, locked:true}`——参数锁定即写进 task.json，全流程脚本与报数优先读它，防跨轮参数漂移。

## 输入场景路由

能力全保留、不绑死平台；平台数据只用于**加速**，截图像素闭环始终是最终裁决。

**Step 0 平台询问**：收到设计稿后先问是哪个平台（Figma / Mergo / Done / 纯截图），按 `PLATFORMS.md` 的指引告诉用户怎么取数，再进路由行。上下文已明确（已贴 code/SVG、已说平台）就**跳过询问**。

**平台直出的 HTML（Done D2C 类）不是页面，只是数据源**：拿它的几何/颜色/文案/图标，结构自己重写（流式布局+组件复用+语义标签，悬浮件 fixed、吸顶 sticky）。

| 用户能提供 | 走的流程 |
|---|---|
| 仅设计稿截图（最常见） | 完整像素取证闭环 Phase 1-3 + 自放大确认 + 图标试画闭环 |
| 截图 + 平台 code（Figma Copy as code 等） | code 提权威值替代 Phase 1 大部分采样 → 闭环校准布局 |
| 再 + 图标矢量（Copy as SVG） | 图标零迭代，仅剩布局联动校准 |
| **Figma 链接 + 环境挂 Figma MCP** | **Figma 场景首选**：`get_figma_data` 一次拿布局/颜色/字体权威值，`download_figma_images` 拿图标 SVG/位图，Phase 1 大部分可跳、图标零迭代；细节见 PLATFORMS.md Figma 节 |
| 仅 Figma 链接（无 MCP） | 链接读不了（403 需登录）→ 引导贴 code/SVG，或给只读 token 走 REST API |
| **Mergo zip 包** | **最强路径**：内含设计稿原图 + 全量图层几何/样式 + 真实切图，Phase 1 几乎可跳 |
| **MasterGo / Done 图层链接 + 环境挂 MasterGo MCP** | **Done 场景首选**：`get_frontend_code` json 拿全量图层树（组件全展开），`get_screenshot` 逐节点拿资产+整页原图，位图缺失问题不存在；细节与坑单见 PLATFORMS.md Done 章 MCP 节（已实战跑通：375×812 pct 8.30） |
| **Done zip 包**（D2C 直出 HTML） | 几何/颜色/文案/图标齐全，但产物是**画板快照**：位图缺失、全 absolute、写死宽高 → **只当取数源，结构自己重写**（已实战跑通） |
| **已有实现 + 新设计稿（换肤/reskin）** | **增量换肤模式**：走下方「增量换肤模式」章节 Phase R0-R3，只改差异区，禁止从零还原整页（实战教训：从零跑会把已正确的既有素材误覆盖改错） |

**先问再画纪律**：仅截图输入且涉及图标/矢量形状时，**先问用户**（选项：我提供 SVG/code vs 你照着截图画）再动工——用户能给矢量时手绘迭代全是浪费。

**先问字体纪律**：文字区测出 ink 宽与回退字体差很多时，先怀疑设计用了特殊字体（压缩体/手写体/艺术体）→ **先问用户**（选项：我提供字体文件 vs 用默认字体接受宽度差异），**不要用 transform 缩放凑宽度**（会压细竖笔画，详见 PITFALLS 三节）。

**提问措辞纪律（所有询问）**：用户是选项主语（「我提供 XX」「我只有截图」「先修这几张」），agent 称「你」；选项里不出现 agent 内部术语（forensics/pct/收敛地板），后果用一句大白话放 description。

## 增量换肤模式（已有实现 + 新设计稿）

**触发识别**：目标页面/组件已有实现（线上或仓库内），任务是「按新设计稿换皮肤/调整 UI」，不是从零建页。此模式下从零跑完整还原流程既浪费 token/时间，又高风险——会把本来正确的区域改错（实战：既有素材被误覆盖，且只盯设计稿的验证全程未发现）。

**第一铁律：不动区严格不动**。默认全部区域不变，只有【变化区清单】内的条目允许改；顺手「优化」未变化区是禁止项。

### Phase R0：现状基线 + 差异归因（代替 Phase 1 取证）

0. **已实现模块盘点（最高优先级，漏了=灾难）**：设计稿里出现的**每个独立画板/状态/模块**，先 grep 代码确认项目是否已实现；已实现且视觉与新稿一致的，直接进【不动区清单】，**禁止重写、禁止重切素材、禁止改一行代码**（实战：已按新稿实现的模块被当「旧皮肤」重写——整卡合成切图被拆散重组、切图标题被改成 CSS 文字、原切图文件被误删，全部回滚收场）。判定口诀：**先问「现状实现了吗」，再问「现状和新稿一样吗」，两个都「是」就一行都不许碰。**
1. **截现状基线**：用 dev server / 线上页截当前实现 `baseline.png`，视口参数与设计稿对齐；动态数据场景用 mock 参数对齐设计稿场景（天数/状态）。
2. **整图 diff**：新设计稿 vs baseline 跑 shot-diff → heatTop 热区 = 候选变化区；无热区模块 = 不动区。
3. **逐热区归因分类**（落进 task.json `reskin.changes`）：`asset` 纯素材替换（几何不变）/ `value` CSS 值变化（颜色/字号）/ `geometry` 位置尺寸变化 / `structure` 模块增删。
4. 产出**变化区清单 + 不动区清单**给用户确认后才动工——新旧设计稿一致的区域占比往往很高，确认清单是防误伤的第一道闸。

### Phase R1：素材替换审计（覆盖现有素材前的强制门禁）

0. **现状已一致 = 禁覆盖**：同名素材的原版内容可能**已经是新稿**（实战：原版素材本就是新稿样式，被盲切覆盖成另一版）。覆盖前先答「原版与新稿视觉一致吗」——一致即移出替换清单，连文件都不要碰。
1. **切对图层**：设计平台里图标/按钮常是「底容器 + 矢量子层」嵌套（MasterGo 组件实例 / Figma component），对矢量子层截图会丢底框——切图前看图层树，确认选中**完整视觉单元**；切出图尺寸量级异常（现有 84px vs 切出 1024px）是切错层的强信号。
2. **新旧并排对比**：内容（含底框/容器）/ 尺寸 / ink bbox / 透明边四项核对；「设计稿与现状一致」的素材直接移出不替换清单。
3. 审计并排图留档工作目录，交付报告附替换清单。

### Phase R2：最小化差异区还原

- `asset`/`value` 类只换文件/改值，不动 DOM 与布局规则；`geometry`/`structure`  类才走 B 档点测闭环。
- CSS 单位按项目既有约定换算（rpx/vw 基准），不从零推布局。

**切图使用纪律（R2 全程适用，换肤与从零还原同守）**：

1. **有整体切图 = 直接用，禁止拆散重组**：设计稿里本身是一张合成图的（含特殊字体标题+装饰贴纸的整卡），整体导出整体用；禁止拆成「背景图 + 若干小切图 + CSS 文字/样式」自行拼装——拼装必引入字体/位置/抗锯齿偏差，且把设计师已合成的成果倒退成低保真零件。
2. **特殊字体一律切图**：标题/艺术字（普惠体 ExtraBold、变形字、描边字等设计字形）必须走切图，禁止 CSS 文字模拟；数字类特殊字体也**不擅自实现**——须设计方提供字体包且经用户同意后才可 @font-face。
3. **CSS/文字仅限动态数据**：只有接口下发或状态派生的内容（天数、进度、列表、价格）允许前端文字/样式实现；设计稿上的静态文案若用特殊字体，同样按第 2 条切图。

### Phase R3：双向验证（缺一不算完）

1. **对齐验证**：变化区 vs 新设计稿（crop-cmp 区域并排）。
2. **回归验证**：改动后整页 vs `baseline.png`，**不动区必须零差异**（仅抗锯齿噪点）——shot-diff 把 baseline 当 design 跑，sc=截图 dpr（基线回归口径见 PITFALLS 二节）；不动区出现集中热块 = 误伤，立即回滚该区域。
3. 全局 final-compare 验收，附两张清单的执行结果。

## 精度档位（先选定，决定流程与成本）

不是所有还原都要 100% 像素级——逐像素闭环的 token 成本是固定的重投入，按用户「要多还原」选档：

| 档 | 流程 | token 量级 | 精度 | 适用 |
|---|---|---|---|---|
| **A 档 像素级** | 下方完整 Phase 1-3 闭环 | 60-150k | 100% 像素级（bbox Δ≤1） | 验收严苛、对外页、需交付 pct 证据 |
| **B 档 高保真** | 看图直出初稿 → 1 次全局 diff → 对热区点测 2-3 处 → 局部修 → 再 1 次确认 | 25-45k | ~95%（结构准、局部 1-2px 容差） | 大多数场景：要高保真但不逐像素验收 |
| **C 档 快速** | 看图一次出稿，不跑测量 | 10-20k | 目测级 | demo、内部页、「差不多就行」 |

默认建议 **B 档**；用户明确要「像素级 / 1:1 / 逐像素验收」才上 A 档；赶时间/内部工具用 C 档。选档与「先问再画 / 先问字体」纪律不冲突——任何档位涉及图标矢量 / 特殊字体仍先问用户。

### B 档「看图直出 + 点测」流程

1. **看图直出**：读设计稿直接写 HTML/CSS 初稿（布局 / 颜色 / 字号按视觉判断），跳过 Phase 1 逐块采样。基础模板自带 `<meta name="viewport">`（缺了移动端按 980 排版）；有平台数据时**逐容器核对 sizing 模式（hug/fill/fixed），线条类节点宽度取 `strokeWeight` 而非 `dimensions`**（后者是矢量形状几何宽，描边居中后视觉 ink = strokeWeight）——hug 被 block/flex stretch 默认占满、细线 1px/2px 误读都是高发错误，且低 alpha 下像素闭环检不出（见 PITFALLS 二节盲区条目），只能靠这一步兜底。
2. **1 次全局 diff**：`run.sh` 跑首版，拿 `pct + heatTop`，确认大结构到位（pct 量级符合预期即可，不追求地板）。
3. **点测热区**：只对 heatTop 前 2-3 个带跑 `forensics bbox` 拿 Δ，区分「视 觉看错」还是「测量微调」——只改实测偏的，不逐块抠。**带内多元素时逐元素开窗归因**：一个 25px 带里混着文字/图标/位图时，禁凭「带内有文字」把整带热值归给地板——非文字元素逐个 bbox 后才允许宣布残余是地板（实战漏过 16px 的按钮对齐错误）。shot-diff 输出的 `heatDetail` 已自动做带内列投影聚类+逐簇双图 bbox，先看它再决定开哪些窗。
4. **1 次确认**：改完再跑 1 次 `run.sh`，结构区 pct 进入 B 档预期（视觉高度接近，残余多为抗锯齿 / 字体地板）即收。
5. **验收**：`final-compare` 并排图给用户，声明档位与残余差异；若要继续抠进像素级，随时可转 A 档补 Phase 2 闭环。

**B 档纪律**：视觉判断只是初稿——具体字号 / 间距 / 颜色 hex 有疑问一律点测，不凭印象定；点测仍守度量诚实性（pct 带 params、自参照区声明）。有平台权威值（Figma MCP / code、Mergo 图层）时初稿直接按权威值写，整体成本偏区间下限。

## 工作流

```
Phase 0 数据门禁 → Phase 1 节点分析（仅 A/B 级，GENERATE.md）→ Phase 2 直出初稿 → Phase 3 闭环迭代（三层判定）→ Phase 4 验收
```

下文小节「Phase 1 取证首版 / Phase 2 闭环迭代 / Phase 3 验收」对应上方总流程的 Phase 2/3/4——纯截图（C 级）输入走完整像素取证闭环；A/B 级输入先按 GENERATE.md 做节点分析（脏过滤→渲染策略→资源策略→锚点），再用 figma-skeleton/数据模型直出初稿（替代大部分取证采样），闭环阶段增加语义层判定。

### Phase 1：取证首版

1. `forensics bbox` 对每个独立 ink 块逐个测设计稿 bbox → 直接得 margin/padding/font-size/line-height 初值（bbox 高 ≈ 行内 ink 高；字号由 ink 高反推，CJK 10px 字 ink 高≈10）。暗底白字用 `light` 谓词。Phase 1 还没有 shot：脚本签名必须两个文件，**把设计稿传两遍**、只看 design 行。
2. 图片资源从设计稿原图裁切（img 空间坐标），不要找占位图；这些区域是**自参照区**。
3. 颜色逐 px 采样（`row`）：背景、渐变（按通道拟合多停靠点）、文字色、半透明底色。
4. 图标：先按「先问再画纪律」确认来源；自绘才走 `map` ASCII 图看真实形状——**不要凭印象画**。
5. 有平台数据（Figma code / Mergo 图层）时，本阶段大部分采样可跳过，直接用权威值。

### Phase 2：闭环迭代

```bash
sh <skill>/scripts/run.sh <design.png> <page.html> [ox oy vw vh dpr sc]   # 截图+diff，输出 pct/params/热点带
NODE_OPTIONS="" node <skill>/scripts/forensics.js <design> <shot> <ox,oy[,sc[,dpr]]> bbox <pred> <x0,x1,y0,y1>
NODE_OPTIONS="" node <skill>/scripts/crop-cmp.js  <design> <shot> <ox,oy[,sc[,dpr]]> <name,x,y,w,h>
```

- **语义层（A/B 级输入每轮必跑）**：`NODE_OPTIONS="" node <skill>/scripts/semantic-diff.js <page.html> <sk-expectations.json> [vw,vh,dpr]`——computedStyle/textContent 对期望值逐属性比对（0 容差清单 + 声明容差），抓像素层盲区（低 alpha 细线、近白渐变、文案/取值错误）与字体回退。退出码 0=过 / 1=有违规 / 2=异常；报告落 semantic-report.json。
- **三层判定（AND 关系）**：语义层全过 AND 像素层 pct ≤ max（实测地板+0.3, 地板×1.15）（混合裕度）AND 结构层逐元素 bbox Δ≤1，任一不达标即归因修复。
- `heatTop` 直接给出差异最大的带（含 css y 区间）→ 对该带跑 `bbox` 拿 Δx/Δy/Δw/Δh → 修 CSS。
- **判字重/描边粗细用 ink 数（bbox 的 n）**，不要目视（放大看和 1x 看结论会翻转）：design n 比 shot 大 30%+ → 升一档字重或 +0.2 描边。
- **判间距用 `runs` 列段**：文字段间空隙 = 右padding+gap+左padding，反解 gap。
- 修 CSS 前先自问：是参数没调对，还是**写法错**？先查 `PITFALLS.md` 的 CSS 机制类。

### 跨阶段工具箱（Phase 1/2 随时用）

**自己放大确认（不要等用户给细节图）**

- `zoom-region.js <png> <x0,y0,x1,y1> <scale> <out.png>` 最近邻放大（8x 合适）→ Read 该 PNG 肉眼看；design 与 shot 用**同一 canvas 窗口**各裁一张成对对照。
- 分工：放大图判**形状**（尾巴方向、缺口深浅、圆角、凹口宽窄），ASCII 同窗对照判**数值**；放大图看出差异后回 ASCII 复核再改，防窗口错位误判。

**图标高清细节闭环**

1. `icon-regions.js` 连通域 bbox 定位图标（img 空间），打 1x/2x ASCII 提几何。
2. 换算进 viewBox（比例 = 图标 ink 宽 / 设计 ink 宽），写候选 path。
3. 候选 path 渲成 120px 大 SVG 截图，ASCII 与细节图同形状对照，合格后应用到页面。
4. 终验用**同窗 ASCII 数值对照**，不要靠 4x 小图目视（小图预览会系统性误判位置）。
5. 白色小元素易被邻近内容污染：用连通域隔离，或固定窗内比白色 run；±1px 即停。

### Phase 3：验收

- 所有区域 bbox Δ≤1（Δw/Δh≤2）且并排图形状一致。某处 Δ=2 且半步阻尼下反复振荡 → 归噪声地板，记录停手。
- `final-compare.js <design> <shot> <ox,oy[,sc[,dpr]]> [out]` 生成整图并排 1:1 给用户确认。
- 交付报告：`pct + params + 自参照区清单 + 剩余已知差异`，不只报一个好看数字。

## 收敛纪律（防过调）

- **地板要实测标定，不要背数字**：残余 pct 是设计工具与 Chrome 抗锯齿/字体光栅化差异造成的地板，**每个 case 不同**——实测例（各自任务独立标定，禁止互套）：Figma 截图路线历史任务 ≈7.2，Figma MCP 卡片（校准任务1）≈9.5，Mergo zip（校准任务3）≈0.3，纯截图（校准任务4）≈12.5；同「Figma」不同路线都差出量级。到底信号：①heat 已均匀撒在文字/描边边缘、无集中块；②所有区域 bbox Δ≤1。两者满足即停，不看绝对值。
- ±1-2px ink 波动是噪声；**振荡时半步阻尼**（测得需 +3 先给 +1.5）。
- 每轮 pct 记小表看趋势：连两轮不降或降后回升 → 停手换方向（重测/换窗口/换谓词），不在同一参数上硬推。
- 修复优先级：先修 heat 贡献最大的带（面积大×密度高），小区域最后。
- 看到脚本 `WARN`（窗口超图等）那轮数字直接作废，先修窗口再谈。

## 批量场景（多张稿）

- 每张用**相同参数**跑，汇总「张名 | pct」表 → 用用户视角把表给用户，问先修哪些；不要自作主张全修。
- 共用组件（同一模板）先修一张，其余复用 CSS，只校准数据差异（文字长度/图片）。

## 样式全集与回归基线（交付侧，详见 STYLE-SET.md）

还原/修复完成后，用 `scripts/style-set.js` 对**真实项目页面**（dev server + mock）出日/夜卡片级样式全集：

- **交付走查**：全集直接给设计侧按名索引；mock 标题带 `【N 样式名】` 前缀文件名自动含义化。
- **回归基线**：验收通过后固化全集；后续样式改动同配置重截，**未改动卡片必须零差异**，有差异 = 误伤回归。
- 与 freeze-baseline 互补：freeze-baseline 固化 /tmp 验收件（对设计稿回归）；style-set 固化交付形态（对项目回归）。
- 每个项目首次使用需生成适配配置（桥 stub/主题注入/选择器/懒加载/干扰元素 5 问，见 STYLE-SET.md），之后只跑截图。


## 落地：还原产物 ≠ 可上线代码

设计稿是**单一宽度、单一数据、单一主题的静态快照**；为凑像素而生的 magic px 上线会碎。落地必做：

- magic 值（`margin-left:80.5px`、`top:-1px`、固定高度）换回**布局规则**（flex/gap/space-between/项目间距变量），仅保留必要微调。
- 用**长文本/短文本/缺图/超长昵称/大号数字**各跑一次，确认不溢出不错行；有夜间模式则颜色走主题变量。
- 图片换回真实远程地址与占位/失败态；设计稿裁图仅用于还原验证。
- **落地代码必须重新取证**：三层判定证明的是 /tmp 里的验收件，不是移植后的交付件。落地改造完成后，设计稿仍在 → 对设计稿重跑一次闭环；设计稿不在 → 用 freeze-baseline 基线跑回归（VERIFY §6）。未重验的落地代码不算完成。
- 还原用的静态 HTML 留在 /tmp 作为依据，**不当交付物、不入仓库**。

## 何时不用本 skill

- 用户只要"差不多的实现"或赶时间：直接写，别上闭环（这套很贵）。
- 页面主体是动态长列表/真实接口数据：只对**单卡片/单模块**跑闭环，不对整页跑。
- 只有低保真线稿/手绘草图（本身不是像素真相）：像素对比无意义。

## 收尾自检清单（全部勾上才算完）

- [ ] （换肤任务）走了增量换肤模式：变化区/不动区清单经用户确认，每个覆盖素材有新旧并排审计留档，不动区 vs baseline 回归零差异。
- [ ] （换肤任务）被替换素材完成三级清理（scss/tsx 引用、import+preload、文件本身），文件删除已逐一 ls 验证生效；按稿写死的固定偏移/宽度已在数据极值（最小/最大数据、另一实验分组、最长文案）下回归。
- [ ] （换肤任务）已实现模块盘点完成：设计稿里每个独立画板/状态/模块都已 grep 代码确认现状；已实现且与新稿一致的模块零改动（未重写、未重切素材、未删文件）。
- [ ] 整体切图未被拆散重组：含特殊字体/装饰合成的切图整图使用；无特殊字体被 CSS 文字模拟；无未经用户同意的字体包引入；CSS/文字实现仅限动态数据。
- [ ] 报了 `pct + params`，并声明了**自参照区**与剩余已知差异。
- [ ] （A/B 级输入）语义层 semantic-diff 通过、semantic-report.json 已落盘；页面 data-node/data-module 锚点未被删除/改名；task.json 参数全程未漂移。
- [ ] 没把设计稿当背景/贴图用；出现过 WARN 的那轮数字没当结论。
- [ ] 中间产物全在 `/tmp/pixel-restore/...`，`git status` 干净，项目里只有最终代码。
- [ ] 要上线的代码已按「落地」节改造并做过多数据验证。
- [ ] 落地后的最终代码已重新取证（重对设计稿或对基线回归）——闭环结论只覆盖 /tmp 验收件，不自动覆盖交付件。
- [ ] 手机模拟件（状态栏/Home 指示条）未还原，且对比区已避开这些带。
- [ ] 缺失的设计资源（未导出切图等）已向用户指名要。
- [ ] 验收交付后已提示用户清理本次 `/tmp/pixel-restore/<任务>` 目录（`rm -rf` 该目录即可；macOS 也会自动清 /tmp，但主动清能立即释放空间，且避免旧 shot/diff/heat 被下次任务误读）。

## 脚本（均在 `scripts/`，绝对路径调用）

| 脚本 | 用途 |
|---|---|
| `run.sh` | **常用入口**：截图+整图 diff，输出 pct/pctAll/params/heatTop + JUDGMENT 摘要行（已封好 NODE_OPTIONS）；未传的参数回落 page.html 同目录 task.json（Phase 0 参数锁定） |
| `shot-diff.js` | run.sh 的内核；参数 CLI > task.json > 硬默认（paramSource 逐键声明来源；task.json 可记 floor 实测地板供 JUDGMENT 判定）；产出 shot.png/diff.png/pixel-result.json（judgment 缺省采集）；等 fonts.ready+图 片就绪；设计稿盖不住对比区或 ox/oy 为负直接报错。输出含 `heatDetail`：top3 热带自动分区归因（带内列投影聚类 + 逐簇 bbox 的 dx/dy/dw/dh/nRatio + 簇均色差 dMean——\|dx\|/\|dy\|≥2=位置偏，nRatio 差>30%=字重/尺寸，都小但 bad 高=地板，dMean>30=偏色非地板；边缘簇「仅单侧有 ink」多为阴影在导出稿 alpha<200 被 notwhite 过滤的伪影） |
| `forensics.js` | bbox / runs / map / row 四件套（窗口顺序 **x0,x1,y0,y1**；row 例外：`row <y> <x0,x1>` 无 pred；超图或 pred 写错会报警） |
| `crop-cmp.js` | 区域 4x 并排对比图（cx,cy 是左上角；输出到 shot 所在目录） |
| `zoom-region.js` | 裁区域最近邻放大成 PNG（自己放大看细节，Read 直接查看） |
| `zoom-shot.js` | 纯截图，可指定 vw/vh/dpr（放大试画闭环、响应式宽度自检） |
| `scroll-shot.js` | **滚动后拍视口**（验证 fixed/sticky 悬浮件是否真的不随页滚） |
| `region-diff.js` | **分区 diff**：自参照区/文字区矩形由参数给出（`"x0,y0,x1,y1;…"` canvas 坐标），输出全页/自参照/结构区 pct，防占位图污染指标 |
| `icon-regions.js` | 连通域 bbox（图标定位）+ 区域 ASCII 图（**img 空间，窗口顺序 x0,y0,x1,y1，与 forensics 相反**） |
| `final-compare.js` | 整图并排 1:1（Phase 3 验收） |
| `unzip-design.py` | 解设计平台 zip（修中文文件名混合编码，定位 preview/index.html） |
| `mergo-extract.py` | 从 Mergo index.html 抽全量图层数据成 JSON |
| `mergo-inventory.py` | 图层数据拍平成可读清单（`--keys` 字段、`--raw <名>` 原始 JSON） |
| `figma-skeleton.js` | Figma MCP `get_figma_data` 原文（tree/json）→ HTML 骨架（带 data-node/data-module 锚点）+ 七区核对报告 + **expectations.json**（语义层期望值）。初稿几何直出来自 Figma 数据而非目测，迭代轮次因此收敛；报告条目是必核清单不是可选项。已经真实 get_figma_data 输出 live 校准（悬空引用/命名样式/负 gap/相对定位自动补全） |
| `filter-dirty-nodes.mjs` | **脏节点过滤**（GENERATE.md §1 规则表：隐藏/零尺寸/透明/画布外/空容器/名称标记）：吃 Framelink tree/json 或 Mergo d.json，出统计 + 规格化节点树（--out nodes.json）；字段缺失的规则不生效且必声明 |
| `semantic-diff.js` | **语义层比对**：CDP 采集 [data-node] 元素 computedStyle/textContent vs expectations.json（0 容差 + 声明容差），含字体加载检测与 hug 文本宽度回退疑似警报（hug 文本宽只走 >10% NOTE、不做 ±1px 硬比——引擎 text metrics 差 1-4px 是常态，硬比必伪违规且无豁免通道）；拒绝消费 source=implementation 的期望值；data-sem-allow 声明补偿（违规降级 ⚖ compensated 单独列出，须附像素证据） |
| `bounds-diff.js` | **结构层快查**（VERIFY §1）：[data-node] DOM bounds vs nodes.json 设计 bbox，selector 级 Δx/Δy/Δw/Δh；支持 data-sem-allow 同轴补偿降级 ⚖；Framelink 树缺绝对坐标时自动只比尺寸并声明覆盖（禁止静默降级）。定位加速用，ink bbox（forensics）仍是最终裁决 |
| `judgment.js` | **P3 三层自动汇总**（VERIFY §4/§5）：自动采集 task.json + pixel-result.json/semantic-report.json/bounds-report.json → judgment-{module}.json（verdict/failedLayer/自动归因 A-F/fixSuggestions）+ judgments/ 跨轮历史 + fix-log；缺失层记 pass:null 跳过不断流；收敛检测（stall 趋势窗/regress/oscillation 振荡（fix-log 同元素 delta 符号反转）/硬上限 3 轮/熔断含最低点回升）自动出信号；**诚实性护栏**：跑了 pixel 未登记 floor、floor 缺 floorEvidence 都会打 [honesty] WARN 且 pixel pass 挂起（后者 verdict 不得 PASS，防编造 floor 直通）；--pixel 内联 JSON 无 mtime 可检新鲜度也打 WARN；自动归因 D 需「不集中+覆盖≥70%+簇温和」三条件（缺一保守归 B），实测 task.json 贯通轮 pct 7.82 逐位一致 |
| `freeze-baseline.sh` | **基线定稿**（VERIFY §6）：`sh freeze-baseline.sh <workdir> <task> [state]` 把验收产物固化到 ~/.cache/pixel-restore/baselines/<task>/<state>/（shot.png+task.json+各层 report+judgment+meta.json；沙箱内 ~/.cache 不可写时设 `PIXEL_RESTORE_BASELINE_DIR` 改道，见 PITFALLS 一节）；回归模式 run.sh 把基线 shot 当 design（**sc=冻结时 dpr 通常 2，不是 1**——sc=1 降采样产假数字；params 变了必须重对设计稿） |
| `style-set.js` | **样式全集批量截图**（自 h5-style-screenshots 并入，详见 STYLE-SET.md）：零依赖 headless Chrome CDP 引擎，对真实项目页面（dev server + mock）按卡片/整页 × 日/夜多主题批量出高清图 + 样式清单.md；项目差异全部在目标项目的 shot.config.js 适配配置里，引擎本身任何项目不用改；交付走查与回归基线两用 |
