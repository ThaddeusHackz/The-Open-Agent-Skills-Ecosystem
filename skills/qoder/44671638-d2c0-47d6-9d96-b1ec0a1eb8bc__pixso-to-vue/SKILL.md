---
name: pixso-to-vue
description: 把 Pixso 设计稿还原为可运行的 Vue3 + TypeScript + Element Plus 页面：控件用真实 EP 组件，菜单走 vue-router，图表用 ECharts，弹窗用 el-dialog/el-drawer（高度随内容、居中、只有一个滚动条），全局不滚动、表格表头固定，并用脚本做组件、布局、像素和构建校验。用户提到 Pixso、设计稿还原、UI 还原、D2C、Pixso MCP、按设计图写 Vue 页面时使用。
---

# Pixso → Vue3 + TS + Element Plus 页面还原

交付的是**能用的页面**：组件能交互、菜单能跳转、滚动位置正确，然后才是像素接近。尺寸、颜色、间距、文案全部取自 Pixso 规格数据（spec），不要看截图估。

- `$S` = `~/.qoder/skills/pixso-to-vue/scripts`（脚本是零依赖 Node ESM；浏览器、像素比对依赖从目标项目的 node_modules 解析）。
- `<page>` 是页面目录名，例如 `rule-list`（数据放 `design/rule-list/`）；`<port>` 是本项目 dev server 的端口；`<app>` 是含 package.json 的前端目录。
- 不要提交或重置代码，不要改别的项目，不要关闭占用端口的别人的服务。

## 完成标准

1. `check-page.mjs --phase final` 输出 PASS。它依次执行 semantic（真组件 + 逐个点击菜单）→ layout（四个视口的滚动）→ 整页 visual（含独立结构门禁）→ `npm run build`，任一步失败就停止；多页或共享样式改动还须按步骤 8 全页 final 回归。
2. 交付消息贴出 final 的输出摘要。没跑或没通过，必须写"未完成"并给出原因，不能声称已还原。

## 名词

| 名词 | 含义 |
|---|---|
| spec | `dump-spec` 生成的扁平规格 JSON。写样式的唯一依据。只能用 `spec-query` 分片读，禁止整份 Read |
| manifest | `prepare-page` 在 spec 旁生成的 `spec.manifest.json`，记录路由、分类复核、额度、检查记录。之后所有检查只传它 |
| 区块 / scope | prepare 打印的 `block <id>` 行。`--node <id>` 只检查这一块；不带 `--node` 是整帧 |
| override | manifest 里 `overrides` 对某个节点的人工分类（control / display / chart / image），必须写 `reason` |
| 精修额度 | 三类独立：tuning（`--phase visual`）3 次/scope，diagnose 3 次/scope，finalVisual 2 次/交付周期；已执行的成功/失败均计数，不互相占用，不预留 tuning 给 final |

## 铁律（违反即不合格，semantic 会 FAIL）

| 设计里是 | 必须用 | 禁止 |
|---|---|---|
| 侧栏 / 顶部菜单 | `el-menu router` + `:default-active="route.path"`，每个菜单叶子一条真实路由；菜单、路由、面包屑、标题来自同一份 `NAV`（`templates/router.ts`） | div 菜单；只切 active 变量、URL 不变；没有子项的 `el-sub-menu`；写死面包屑 |
| 输入、下拉、日期、数字、文本域 | `el-input` / `el-select`+`el-option` / `el-date-picker` / `el-input-number` / `el-input type="textarea"` | div、span、图片摆出值或占位符 |
| 表格 | `el-table` + `el-table-column`，数据驱动，表格自己的 body 滚动（`templates/TableModule.vue`）；线条按设计：没有列竖线就不加 `border` 属性，外框用表格根或面板的真实 `border`，线色用 `--el-table-border-color`，只有短表头分隔线才用 `th` 伪元素、尺寸取 spec | div 栅格拼表格、自绘或复制表头；设计无竖线却用 `border` 画整套网格 |
| 按钮、标签、Tabs、分页、单选复选、开关、树、上传、步骤条、进度条、级联、树选择、穿梭框、折叠面板、时间线、描述列表、Alert、Badge、Empty…… | 对应的真实 `el-*` 组件 | 仿制外观、透明的 EP 空壳 |
| 弹窗 / 抽屉 | `templates/DesignOverlay.vue`（真实 el-dialog / el-drawer） | 自己写 `.el-dialog` 定位或固定高度 |
| 折线、柱、饼、雷达等图表（包括 IMAGE 填充的图表） | ECharts（`templates/EChart.vue`，雷达用 `templates/chart-options.ts`），数据写在 mock | 图表图片、导出的 SVG；解析曲线路径或图片反推数据 |
| 小图标 | 导出的精确 SVG + `templates/SvgIcon.vue`（内联，`currentColor`） | `<img>`、背景图、相似的图标库 |
| 照片、插画、位图 logo | 复核确认后用 `<img>` / `el-image` | 没复核就放 `<img>` |

**样式在 EP 组件本身上改**，按顺序尝试，前一层能解决就不往下走：① props / 插槽（图标放 `prefix-icon` / `suffix-icon`）② 全局主题 `element-theme.scss` ③ 组件 CSS 变量（`--el-input-height` 等）④ 自己 class 下的 `:deep(.el-xxx__part)` ⑤ 弹层用 `popper-class` + 不加 scoped 的样式。颜色、字号用 tokens 变量，不写裸色值。

**绝对不要**：

- 把 EP 组件设成 `opacity:0` / `visibility:hidden`，或 `display:none` 它的内部部件，再自己画一个（`ep-hidden` / `ep-gutted`）。
- 在 EP 组件上方绝对定位盖一层，包括 `pointer-events:none` 的（`ep-covered`）。
- 外层 div 画边框背景、把 EP 自己的边框弄透明。
- 在组件旁边用 span 显示值或占位符；值交给 `v-model`、`placeholder`、`el-option`、列数据。
- 为降低像素差，把控件或图表换成图片、SVG、div。
- 把设计稿宽度写成页面 `min-width`；用 `overflow:hidden` / `overflow-x:hidden` 藏住溢出内容。

## 工作流（按顺序；每步的"通过"不满足，不进入下一步）

### 1. 连接 Pixso，确定节点

```bash
node $S/pixso-mcp.mjs list
```

- 失败：停下，请用户打开 Pixso 桌面端并开启 MCP（默认 `http://127.0.0.1:3667/mcp`，可用环境变量 `PIXSO_MCP_URL` 改）。
- 用户给了链接：取 `item-id` 并 URL 解码，`11%3A17324` → `11:17324`。
- 没有链接：`node $S/pixso-mcp.mjs call get_top_level_frames '{"type":"page"}'`，再用 `'{"type":"frame","pageIds":["<pageId>"]}'` 列帧。同名帧拿不准就问用户，不要把所有帧都拉一遍。

### 2. 准备项目和 dev server（每个项目一次）

1. 已有项目：沿用现有 package.json / lock，不升级依赖；`<app>` 就是含 package.json 的前端目录。新项目：按 `references/conventions.md` 的版本基线建 Vite + Vue3 + TS 项目，安装 `vue element-plus echarts vue-router`，开发依赖 `sass playwright pixelmatch pngjs`。
2. `vite.config.ts` 设 `server: { host: '127.0.0.1', port: <空闲端口>, strictPort: true }`，后台常驻启动：`npx vite --host 127.0.0.1 --port <port> --strictPort`。端口被占就换一个，不要关别人的服务；第一次打开确认看到的是本项目。

**通过**：`<app>/package.json` 存在，dev server 能访问。

### 3. 拉数据并 prepare（每页一个目录）

```bash
node $S/pixso-mcp.mjs call get_screenshot '{"guid":"<id>"}' design/<page>/shot      # 生成 design/<page>/shot_0.png
node $S/dump-spec.mjs '<id>' design/<page>/spec.json
node $S/prepare-page.mjs --spec design/<page>/spec.json --url http://127.0.0.1:<port>/<route> --app <app> --design design/<page>/shot_0.png
node $S/spec-query.mjs design/<page>/spec.json components
```

- 节点 id 含 `:` 或 `;`，命令行里一律加单引号。
- `--url` 是这个页面的真实路由（还没写代码也先定好路径），不要用 `/` 打开别的页面。
- 设计改了要重新 dump；有旧复核时 prepare 要求 `--reset-reviews`，只作废分类、保留已用额度，重做步骤 4；不能借此清空失败记录。
- prepare 输出中需要处理的行：`REVIEW unknown-control`、`REVIEW <id>`（待复核 IMAGE）、`REVIEW misalign`、`WARN table-overflow`、`OVERLAY`、`Classification issues`。
- components 每个控件行的 `props:` 来自 Pixso 变体属性，直接照写（如 `size="large" type="primary" disabled placeholder="请输入"`），不要从截图猜状态；Hover / Focus 变体不写。

### 4. 分类复核（不能跳过）

**unknown-control**（带交互名称但没识别出的组件实例），逐个判断：

1. 它是 Element Plus 已有的某种组件（输入、选择、切换、展开、导航、反馈）→ 写 control override，`controlKind` 只能取下面这些值：
   `table pagination daterange date time cascader tree-select autocomplete mention input-number color-picker select textarea input checkbox radio segmented switch slider rate upload transfer tabs collapse steps timeline dropdown menu breadcrumb progress tree drawer dialog popconfirm popover tooltip calendar descriptions carousel anchor affix backtop form alert badge avatar empty result skeleton statistic countdown link button tag`
2. 确认它没有任何交互，只是展示（标题、说明、卡片、统计排版）→ 写 display override，reason 说明为什么没有交互。
3. 判断不了 → 问用户。不要默认当成 display，也不要先用 div 写出来。

**pending IMAGE**（IMAGE 填充，尚不确定是图表还是图片）：每个只看一次小预览，再写 override。

```bash
node $S/export-icons.mjs design/<page>/previews p1='<id>':png@1 --spec design/<page>/spec.json --preview
```

预览图只用于判断，不能引用进页面。嵌套实例 id 导出失败时，对它所在的区块调用 `get_screenshot` 存到 `design/<page>/previews/` 看一次；仍判断不了就问用户。

在 manifest 的 `overrides` 里写复核结果（键是 spec 节点 id，下面的 id 只是格式示例）：

```json
"overrides": {
  "12:301": {"kind": "control", "controlKind": "rate", "reason": "设计系统的评分控件，可点选星级"},
  "12:388": {"kind": "display", "reason": "只展示状态摘要，没有输入或点击"},
  "50:19095": {"kind": "chart", "chartKind": "radar", "reason": "预览确认是多维指标雷达图"},
  "60:12": {"kind": "image", "category": "photo", "reviewed": true, "reason": "预览确认是人物照片"}
}
```

- `category` 只能是 `photo` / `illustration` / `logo`；`chartKind` 是 ECharts 类型（line / bar / pie / radar …）。
- 已经被识别成控件的节点不能改成 display；IMAGE 节点只能复核为 chart 或 image。
- 写完重新跑 prepare。

**REVIEW misalign**（相邻的带边框/阴影面板同一条边差 1–4px，例如表格底边 1014、右侧面板 1017）：设计稿多半是手误，照抄会在页面上露出错位的底线。在 manifest 顶层 `alignment` 里逐组决定，prepare 行里已给出可复制的写法：

```json
"alignment": {
  "742:6637/bottom": {"to": 1017, "reason": "与相邻面板同边对齐（设计误差）"}
}
```

- 键是 `<节点id>/<top|right|bottom|left>`；`to` 只能取该组已有的值；确属有意错开才写 `{"keep": true, "reason": "..."}`。
- 对齐后，spec-query、semantic、layout、visual、final 全部用对齐后的规格和基准图（`snap=bottom+3` 标出移动过的节点，贴边的子节点一起移动）。页面按对齐后的数值写，不要按原始像素写。
- 未决定时 semantic FAIL `design-misalign`，visual 不会运行。

**通过**：prepare 输出 `unknown controls 0`、`pending IMAGE 0`、`misalign 0`，并且没有 `Classification issues`。

### 5. 搭外壳和共享层（每个项目只做一次）

1. 先读 `references/layout-scroll.md`，再从 `templates/` 复制：`tokens.scss`、`element-theme.scss`、`index.scss`、`AppLayout.vue`、`AppSidebar.vue`、`router.ts`（→ `src/router/index.ts`）、`PagePlaceholder.vue`、`SvgIcon.vue`，按需复制 `EChart.vue`、`chart-options.ts`、`TableModule.vue`、`DesignOverlay.vue`、`design-scene.ts`。
2. `NAV` 按设计菜单填写（文案、层级、顺序一致）；当前页面设为 `DEFAULT_PATH`；还没还原的页面指向 `PagePlaceholder`；没有子项的一级菜单用 `el-menu-item`。
3. tokens 用 `spec-query tokens` 的结果填写，再映射到 `--el-*` 变量。
4. 图标导出：`node $S/export-icons.mjs src/assets/icons <name>='<id>' ... --spec design/<page>/spec.json`；实例内的嵌套节点（id 形如 `I11:1;8:2`）用 `export-nested.mjs`，参数相同。脚本拒绝导出图表、控件和大于 96×96 的区块，被拒绝说明该用组件实现。

**通过**：跑一次 `node $S/check-page.mjs --manifest design/<page>/spec.manifest.json --phase smoke`。此时还没写的区块会报 `fake-*`，这是正常的；但不能有 `vue-runtime` / `runtime-*` 报错，菜单和外壳要能显示。

### 6. 逐块编码

```bash
Q="node $S/spec-query.mjs design/<page>/spec.json"
$Q outline --depth 3        # 骨架：容器和组件实例
$Q node '<区块id>' --depth 4  # 当前区块子树
$Q texts '<区块id>'           # 当前区块文案、字号、行高、颜色
$Q at <x> <y>               # 坐标处的节点（把差异位置映射回节点）
```

- 一次只取一个区块：查询 → 写代码 → smoke（本块的 `fake-*` 应该消失）→ visual `--node <区块id>` → 下一块。未受改动影响的已完成块不重复查询；共享改动必须回归所有已还原页。
- autolayout 对应 flex：`al=H|V` → `flex-direction`，`gapN` → `gap`，`p上,右,下,左` → `padding`，`SPACE_BETWEEN` → `justify-content: space-between`，交叉轴 `CENTER` → `align-items: center`。更多字段对照见 `references/conventions.md`。
- 新 tab 样式和媒体查询必须限定到该 tab/root；不要用共用 `@media (max-width:1600px)` 把过滤栏 gap16 改 gap8，波及已完成 tab。flex gap 前先重置 el-button / el-form-item 默认 margin。
- 文字的 `font-size` 和 `line-height` 成对写；Regular = 400，Bold = 700。
- 数据放 `views/<page>/mock.ts`，文案逐字照抄设计；列表数据支持 dev 下的 `?mockRepeat=N`（写法见 conventions.md）。
- 写 EP 组件前读 `references/element-plus-pitfalls.md` 对应小节。
- D2C（`design_to_code`）默认不用；只有某个子结构看 spec 也看不懂时，对那一个子节点调用并 grep 需要的片段。
- 禁止整份 Read：`spec.json`、`design/mcp/*`、D2C 产物、完整 report.md。用 `spec-query` 或 grep 取片段。

### 7. 检查与修正

```bash
C="node $S/check-page.mjs --manifest design/<page>/spec.manifest.json"
$C --phase smoke                                   # 真组件、图片分类、ECharts 实例、运行时报错（不点菜单）
$C --phase layout                                  # 四视口 + 8倍数据；同排控件 gap 保持设计值，换行/隐藏另报未验证
$C --phase visual --node '<区块id>'                 # 区块像素比对；不带 --node 是整帧
$C --phase diagnose --node '<区块id>' --probe '.selector'   # 查一个元素的盒子和计算样式
$C --phase diagnose --node '<区块id>' --box x,y,w,h         # 放大对比一个小区域（坐标相对该次 visual 的截图）
```

- 看到 FAIL / WARN 代码，查 `references/check-codes.md` 找原因和修法。
- 修正顺序：smoke 和 layout 的 FAIL 先修（不消耗视觉/诊断额度），再看 visual 的独立结构门禁：`border-missing` / `border-mismatch` / `control-geometry` / `control-gap`。layout 还要求设计中同边对齐的相邻面板在四个视口都对齐（`panel-edge-misaligned`，容差 1px）：并排面板用同一个 flex 行 + `align-items: stretch` 或相同高度来源，不要各写固定高度。
- 几何容差 2px；边框在邻像素 1px 内匹配，不是“1px 边框可直接接受”。structure FAIL 或边框未确认禁止 PASS / CONVERGED；`solid=0` / 低 non-text 不能证明边框正确。
- 边框优先 `border` + `box-sizing:border-box`，不把原生控件边框搬到外壳；阴影/outline 必须实际可见并通过结构门禁，inset 阴影可能被白色表格遮住。
- 结构通过后看 `non-text`（目标 < 0.1%）和文本问题；显著的位置、颜色、字号、字重差必须修。文本严格容差 2px，CONVERGED 仅字形测量可放宽至 3px；这不放宽控件几何/gap，也不豁免缺线、错色；图表仅绘图区遮罩。
- `CONVERGED` 表示本 scope 收敛，不等于残余全是 AA；共享改动后仍须回归。源码没改就重跑 visual 会被拒绝（不扣额度）。
- 对应类别额度用完就停；未过门禁必须报未完成，不能只记残余就交付。不要换参数、新建脚本、改 manifest 或加验收例外开关绕过。
- 检查只用 check-page / check-all。禁止直接运行 `semantic-check / layout-check / visual-diff / probe / crop-compare`，禁止自己写像素扫描、截图拼接脚本。
- 同一个 manifest 不要并行跑多个检查；dev server 不可达时按提示启动它，不要反复重试同一命令。
- smoke / layout 只缓存相同输入的 PASS；失败不缓存，源码或输入变化后不能沿用旧 PASS。

### 8. final 与交付

```bash
node $S/check-page.mjs --manifest design/<page>/spec.manifest.json --phase final
node $S/check-all.mjs --phase final --root design      # 多页及共享改动后，全页 semantic/layout/visual/build
```

- final 必须整帧（不带 `--node`），finalVisual 独立 2 次/交付周期。相同输入 final 被拒绝；失败后必须实质修复源码/设计等，才可用剩余一次复验，URL/channel 变化不算修复。成功交付后源码变化才开启新 final 周期，不把 final 当调试手段。
- 共用 tokens、EP 主题、AppLayout、通用组件或 CSS 媒体查询改动后，必须 check-all final 所有已还原页，包含已完成 tab；不能只跑批量 smoke。只复用相同源码/spec/design/tools 的完整 final PASS，失败不缓存。
- 设计帧截图外的文本若标为“未验证”，当前 final 会失败；补齐真实设计输入或修复源码后再验，不能仅写说明就交付。

交付消息包含：页面地址；改动的文件；final 输出摘要（semantic 控件/图表与 WARN、layout、structure/边框确认、non-text/文本问题、build）；明确全部 global 不滚，page 模块只纵滚，fill 数据区在模块内滚，并列出表格在哪些视口内部横滚；`layoutExceptions`、override 和 `alignment` 决定的理由；门禁允许的残余与 `report/side-by-side.png` 链接。未验证范围导致 final FAIL 就报未完成；设计未画的交互态（hover、展开）用 EP 默认并说明。

## 特殊场景

**滚动**（写布局前定好，细节见 `references/layout-scroll.md`）：

- html、body、#app、外壳、main 在两个方向都不滚动；长内容放页面内的 `<el-scrollbar data-scroll-module="page">`，它只能纵向滚动。
- 横向滚动只允许出现在表格内部，或标了 `data-scroll-module="<模块名>"` 的业务模块内部。
- 表格要滚动时，用 `el-table` 的 `height` 或 `max-height`，表头固定，只滚内容；不要用 el-scrollbar 包整张表。
- 设计宽度下表格不得横向滚动：列宽合计大于容器内容宽（prepare 报 `WARN table-overflow`）时，留一列只写 `min-width` 不写 `width`。只有设计确实画了横向滚动条，才在 manifest 顶层写 `"layoutExceptions": [{"selector": ".xxx-table", "reason": "设计画了横向滚动条"}]`。

**弹窗 / 抽屉**（prepare 打印 `OVERLAY` 行时）：

- 用 `templates/DesignOverlay.vue`，把 OVERLAY 行的 box、viewport 填进去。宽度取设计值；**高度不写设计稿的像素值**，由内容撑开，上限是百分比 `max-height`（OVERLAY 行给出，默认 80vh–100vh，可传 `max-height="85vh"`）；弹窗上下左右居中。
- 只允许一个滚动条：只有弹窗 body 滚动，遮罩、外层、header、footer 都不滚。body 里不要再放 el-scrollbar、`overflow:auto` 的 div 或带 height/max-height 的 el-table。弹窗里的表格二选一：表格用 max-height 自己滚、body 不滚；或表格不限高、由 body 滚。
- 打开状态用 `templates/design-scene.ts`：`const open = useDesignScene('<key>')`，prepare 的 `--url` 带上 `?scene=<key>`（只在 dev 生效）。弹窗挂在父页面路由上，不新建假路由。
- 识别错了：在 manifest 写 `"overlay": "none"` 或 `{"form": "dialog", "panelId": "<id>", "reason": "..."}`，重新 prepare。

**图表**：容器宽高 = components 给的 chart 框，`grid` = plot 区相对 chart 框的偏移，字体字号颜色显式写进 option，`animation:false`。曲线形状大致像就行，不解析路径，不追虚线相位和抗锯齿。

**多页面 / 子 agent**：共享层（tokens、element-theme、AppLayout、AppSidebar、router NAV、templates 拷出的通用组件）只由主 agent 修改。外壳稳定后可以把页面分给子 agent，每个只改自己的 `views/<page>/` 和 `design/<page>/`；需要改共享层就报告给主 agent。

## 何时停下来问用户

- Pixso MCP 连不上，或找不到目标帧、同名帧无法区分。
- unknown-control 或 IMAGE 看了预览仍无法判断语义。
- EP 组件确实做不到设计效果（已经试过变量和 `:deep`）——说明差异，问用户能否接受，不要换成 div。
- 额度用完仍有显著差异、final 失败且原因不在页面代码（如构建环境问题）。
- 需要升级已有项目依赖、改别的项目、占用或关闭别人的端口。

## 参考文件（用到时再读）

| 文件 | 什么时候读 |
|---|---|
| `references/layout-scroll.md` | 写外壳和页面根布局之前；layout FAIL 时 |
| `references/element-plus-pitfalls.md` | 写某个 EP 组件之前读对应小节 |
| `references/conventions.md` | 新建项目、定目录结构、写 tokens 和 mock 时 |
| `references/check-codes.md` | 任何检查输出 FAIL / WARN 时 |
