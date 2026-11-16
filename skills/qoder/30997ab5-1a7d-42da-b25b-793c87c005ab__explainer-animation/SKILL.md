---
name: explainer-animation
description: 把分镜表/解说文案制作成中文科普动画 MP4（无配音、烧录字幕、BGM + 程序化音效）。Node + hyperframes(GSAP) + ffmpeg 流水线；暗金散景 + 宋体 + 极简隐喻图形风格；字幕驱动节奏、元素变形转场；自带自动质检。用户提到"根据分镜/文案做动画、科普视频、解说动画、知识短视频"，"按参考视频风格做"，"给动画加 BGM/音效"，或给出分镜 CSV 要出视频时使用。
---

# 分镜 → 科普动画

本 skill 自带完成一部高质量科普动画所需的一切：流水线脚本、项目模板、图标与组件库、21 个已验证的场景配方、一部完整示例片（`examples/sleep-demo/`），以及**自动质检脚本 `qa.mjs`**。**不需要参考任何其他项目。**

质量标准（用户验收过的）：
1. 暗金参考风格；**四角留空**；不要装饰性英文，也不要和字幕重复的文字。
2. **信息密度均匀**：按阅读速度排时长，每句字幕期间都有画面动作，没有空镜。
3. **转场有视觉锚点**：换画面时至少有一个元素连续变形、移动或在同一位置交接，不能整屏淡出再淡入。
4. 分镜里写的画面都要做出来；做不了的写明替代方案。

> 如果你不能查看图片：完全依靠 `qa.mjs` 的输出和规划表自检。它会客观检查空镜、稀疏、文字遮挡/过小/越界、四角、锚点、写死时间、节奏。

## 关卡流程（按顺序，每关达标才进下一关）

### 关卡 0 · 读需求
- 读分镜（CSV 或文案）。脚本自动识别表头含"旁白|配音|字幕"的列作为字幕来源；其余列（画面描述、屏幕文字、音效）是设计依据。
- 有参考视频时，抽帧看风格：`bin/ffmpeg -i ref.mp4 -vf "fps=1/2,scale=480:-1,tile=6x4" /tmp/ref%02d.jpg`。不能看图就直接用本 skill 的默认风格（它就是从那类参考视频提炼出来的）。
- BGM：用用户指定的音频，`.ncm` 由 `new-project.sh` 自动解码。用户没给就问；不要加配音。
- 用户说"控制时长、保证信息密度"时，**用 `"pacing": "auto"`，不要手调阅读参数**。

### 关卡 1 · 环境（每个工作区一次）
```bash
bash .claude/skills/explainer-animation/scripts/setup.sh
```
✅ 通过标准：最后一行打印"环境就绪：v22… · hyperframes 0.8.181"。出错时查 `references/pitfalls.md` 的"环境"一节。

### 关卡 2 · 建项目 + 字幕排期
```bash
bash .claude/skills/explainer-animation/scripts/new-project.sh <项目名> <分镜.csv> <成片名> [bgm.ncm|bgm.mp3]
. ./env.sh && node scripts/build-subtitles.mjs <项目名>     # project.json 默认 preview:true，只打印切句与编号
```
1. 看切句结果：每行是「编号、视觉宽度（汉字 1、英文 0.55）、字幕」。含英文时保持 `"split": "v3"`。分镜表会被复制到 `data/<项目>-storyboard.csv`，这是脚本自己的写入。
2. 填 `project.json`：保持 `"pacing": "auto"`；`scenes` 按分镜段落给字幕编号分组（不填则按分镜表每行一个段落自动分组）；`hold` 只加在动画特别多的句子上（结尾句加 2.5–3s）；段内换画面的句子加 `gapBefore` 0.5–0.7；`highlights` 只放关键词（5–10 个）；画面用大字呈现的句子放进 `hideSubs`。删掉 `preview`。
3. 再运行一次 build-subtitles。
✅ 通过标准：没有"⚠ 总时长偏短/偏长"的提示；记下它打印的每句时长（后面写节拍要用）。细则见 `references/pacing.md`。

### 关卡 3 · 镜头规划表（写代码前必须完成）
在 `<项目>/plan.md` 按 `references/planning.md` 写表：每句的画面节拍（偏移秒）、主体尺寸、锚点入/出（**必须选自 `references/recipes.md` 的配方编号**）、音效；再写一份分镜元素覆盖清单。范本：`examples/sleep-demo/plan.md`。
✅ 通过标准：分镜每个画面元素都已标注到某句；每句至少 2 个节拍；每次换画面都写了具体锚点（"淡入淡出"不算）。

### 关卡 4 · 实现（一次一个段落）
- `index.html`：每个段落一个 `<section id="sN" class="clip scene">`，元素用绝对坐标，组件和配方 HTML 直接拷贝 `references/recipes.md`。坐标速算在 recipes.md 文末。
- `assets/timeline.js`：在模板里写，所有工具函数都已就绪（pop/rise/stamp/out/show/draw/loop/cycle/spin/count/gather/scatter/typeIn/focusSlot/sfx，以及 **`box()` 取元素画布坐标、`flyTo(src, dst, t)` 一行完成锚点飞位与交接**）。
- 三条通用规则：① 交接/飞位优先用 `flyTo`，不要手算坐标；② `section > *` 的初始隐藏只管一层，容器里要单独入场的子元素先 `tl.set(…, {opacity:0}, 0)`；③ 层级由 HTML 顺序决定，要压在上面的元素写在后面。
- 缺图标就在 `assets/figures.js` 的 `ICONS` 里加（viewBox 200，只用 path/rect/circle，描边 currentColor）。
- 每写完一个段落就运行：
```bash
node scripts/build-subtitles.mjs <项目> && node scripts/extract-sfx.mjs <项目> && node scripts/qa.mjs <项目>
```
✅ 通过标准：当前段落没有 FAIL，再写下一段。

### 关卡 5 · 整体质检
```bash
. ./env.sh
(cd <项目> && npx hyperframes lint)        # 0 error
node scripts/qa.mjs <项目>                  # 0 FAIL；WARN（角色太小、大字压图、字号偏小、画面偏空）逐条看，能改就改
```
能看图的话再抽帧复核，**重点抽转场进行到一半的时刻**：
`. ./env.sh && (cd <项目> && npx hyperframes snapshot --at <各转场中点> --no-end --describe false -o /tmp/snap)`（必须先加载 env.sh，否则报 Node 版本过低），然后看 `/tmp/snap/contact-sheet*.jpg`。对照 `references/qa-checklist.md`。

### 关卡 6 · 出片
```bash
./render.sh <项目> high      # 自带字幕排期→音效提取→质检关卡→混音→渲染→封装；3 分钟片约 5–10 分钟，放后台运行
```
✅ 通过标准：`output/<成片名>.mp4` 为 1920×1080、30fps、h264+aac；响度约 −15 LUFS（`bin/ffmpeg -i 成片 -vn -af ebur128 -f null - 2>&1 | grep -A6 Summary`）。

### 关卡 7 · 交付说明（简体中文）
写清：成片/字幕路径与规格；时长及与分镜的差异和原因；各段画面与转场锚点；qa 结果；音效替代项；BGM 来源与版权提醒；哪些已验证、哪些需要用户亲自看/听；如何修改和重新出片。

## 必须遵守（复核中发现的失败模式）

| 禁止 | 正确做法 |
|---|---|
| 时间写成固定数字 `pop('#x', 42.25)` | 一律 `c(i)+偏移` / `e(i)-偏移`；qa 会把固定数字判为 FAIL |
| 注释写"A 变成 B"，代码只有 `out(A)` + `pop(B)` | 用 `flyTo(A, B, t)` 或照配方 tween `x/y/scale/left/width`，在同一时刻交接显隐 |
| 跳过分镜里难做的画面（曲线、交叉点、对比图） | 用 R4/R5/R7 等配方做出来；实在做不了就写进交付说明 |
| 手调 readBase/readPerChar，导致节奏过快 | `"pacing": "auto"` |
| 画面只有一个小元素在中央 | 主体 ≥ 300px；用阵列、图表、卡片撑满主区（y 200–760） |
| 标签文字 < 24px，或文字互相压住 | 标签 ≥ 28px，关键数字 ≥ 56px；qa 会检查遮挡和字号 |
| 在四角放标题、章节名、Logo、装饰 | 四角留空，标签行放在顶部居中 |
| 段落之间整屏淡出再淡入 | 用 transitions.md 里的锚点模式 |
| 结尾大字下面留着压暗的旧画面 | 先 `out()` 清场，再出大字（R21）；qa 会给 WARN |
| 小人缩得很小（<110px）当道具用 | 保持 220×280，最少 `.pawn.sm`；qa 会给 WARN |
| 为了通过 qa 加无意义的抖动 | 每个节拍都要对应字幕内容（计数、高亮、标注、印章、变形） |

## 参考资料（按需读）
- `references/recipes.md`：21 个场景配方（标题卡、擂台、三卡对比、曲线图、双柱、阵列收拢、仪表、编号要点、流程链、印章与盾牌、计划表、碎裂、齿轮、时间线、镜头推进、角色走位、结尾图标、双曲线交叉图、翻牌、物件飞进手里、两行逐字结尾），可直接拷贝。
- `references/planning.md`：规划表格式与规则。
- `references/style-guide.md`：配色、角色、组件尺寸速查、构图数字、四角与文字规则（参考视频的四角有内容时，仍以四角留空为准）。
- `references/pacing.md`：切句、自动节奏、目标时长公式。
- `references/transitions.md`：锚点机制与模式；qa 如何判定锚点。
- `references/sound.md`：34 种合成音效、BGM 闪避/静音段、混音验收。
- `references/pitfalls.md`：环境、hyperframes、GSAP、字幕的坑。
- `references/qa-checklist.md`：自动质检项 + 人工复核项。
- `examples/sleep-demo/`：完整示例（storyboard.csv、project.json、plan.md、index.html、timeline.js）。运行方法：`bash .claude/skills/explainer-animation/scripts/new-project.sh sleep-demo .claude/skills/explainer-animation/examples/sleep-demo/storyboard.csv 睡眠科普示例 <bgm>`，再把示例的 index.html、project.json、assets/timeline.js 覆盖进去。

## 环境规则
安装依赖用 `npm i --yes --legacy-peer-deps`；不主动启动 dev 服务；不输出环境变量；不擅自 git 提交。渲染是本地文件生成，不是部署；要发布上线时走 super-publish 流程。
