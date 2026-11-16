---
name: ai-editable-ppt-spec
description: "AI 高颜值全可编辑 PPT 标准化双阶段制作规范 (v2.1)。阶段一：AI 图像生成无文字高清视觉底图；阶段二：python-pptx 叠加可编辑文本框与截图。含截图处理规范（AI看PIL做）、Office 2016 兼容性修复、iSlide 设计模式借鉴、图片清晰度优化。跨平台通用，适用于 QoderWork/Hermes Agent/Trae/Cursor 等任意 AI Agent。触发词：双阶段PPT、可编辑PPT规范、AI视觉底版、高颜值PPT流程、截图处理、PPT配图。"
version: 2.1.0
---

# AI 高颜值全可编辑 PPT 标准化制作规范 v2.1

跨平台通用规范，仅依赖 Python 3 + python-pptx + Pillow + lxml。

## 核心理念

将"高颜值 AI 视觉"与"全可编辑性"解耦为两个独立阶段：

- **阶段一**：AI 图像生成无文字高清视觉底图（PNG），严格预留标题/正文/截图留白区域
- **阶段二**：python-pptx 在底图上叠加独立可编辑文本框 + 截图图层

最终成品：高清 AI 视觉质感 + 所有标题/正文/数据完全可二次编辑。

```
最终 PPTX 成品
├── Layer 3: 截图/图片图层 (可替换、可移动)
├── Layer 2: 可编辑文本框 (标题/正文/数据/页码)
└── Layer 1: AI 视觉底图 (高清、无文字、全铺背景)
```

## 能力依赖（不绑定特定工具）

| 能力需求 | 阶段 | QoderWork 参考 | 通用替代 |
|----------|------|----------------|---------|
| 幻灯片级图像生成 | 阶段一 | baoyu-slide-deck 技能 | ImageGen / DALL·E / Midjourney |
| 插图级图像生成 | 阶段一 | baoyu-article-illustrator 技能 | ImageGen / DALL·E |
| PPTX 组装引擎 | 阶段二 | pptx (PPTX Pro 2.0) 技能 | `pip install python-pptx` |
| HTML 模板快速出稿 | 阶段二(可选) | qoderwork-ppt 技能 | HTML→PPTX 自定义管线 |

## 文件布局

```
project/{topic-slug}/
├── source/source-{slug}.md          # 原始素材
├── phase1-visual/                   # 阶段一产出
│   ├── analysis.md                  # 内容分析报告
│   ├── outline.md                   # 幻灯片大纲 (含 STYLE_INSTRUCTIONS)
│   ├── layout-map.json             # ★ 关键衔接文件：每页留白坐标映射
│   ├── prompts/                     # 图像生成 Prompt 文件
│   └── images/                      # 生成的空白视觉底图 PNG
├── phase2-content/                  # 阶段二工作区
│   ├── content.md                   # 结构化内容文档
│   ├── overlay-script.py            # ★ python-pptx 叠加脚本
│   └── screenshots/                 # 待插入的截图素材
└── output/{topic-slug}.pptx         # 最终产出
```

---

## 阶段一：AI 视觉底版生成

### 留白坐标体系

以 16:9 画布 (13.333" × 7.5" / 1920×1080px @144dpi) 为基准，layout-map.json 记录每页留白区域：

| 留白区域 | 位置 (英寸) | 尺寸 | 用途 |
|----------|-------------|------|------|
| 标题区 | x:0.6 y:0.35 w:12.1 h:1.0 | 全宽顶部 | 页面标题 |
| 副标题区 | x:0.6 y:1.35 w:12.1 h:0.5 | 标题下方窄条 | 副标题/日期 |
| 正文区-全宽 | x:0.6 y:2.0 w:12.1 h:5.0 | 标题下方大区域 | 正文段落/列表 |
| 正文区-左半 | x:0.6 y:2.0 w:5.8 h:5.0 | 左侧半区 | 左文右图布局 |
| 截图展示区 | x:6.9 y:1.8 w:5.8 h:4.5 | 右侧偏上 | 产品截图/演示图 |
| 数据高亮区 | x:0.6 y:2.2 w:12.1 h:3.5 | 中部大区域 | 数据卡片/统计数字 |
| 底部栏 | x:0.6 y:7.0 w:12.1 h:0.35 | 底部窄条 | 页码/来源/脚注 |

### 风格维度系统

| 维度 | 选项 | 底图效果影响 |
|------|------|-------------|
| Texture | clean / grid / organic / pixel / paper | 背景底纹处理 |
| Mood | professional / warm / cool / vibrant / dark / neutral / macaron | 整体色彩方案 |
| Typography | geometric / humanist / handwritten / editorial / technical | 装饰元素风格 |
| Density | minimal / balanced / dense | 装饰元素数量与留白比例 |

底图推荐：`clean` 纹理 + `minimal` 或 `balanced` 密度，产生最干净的留白效果。

### 底图 Prompt 关键指令（必须追加）

```
CRITICAL: NO TEXT RENDERING
- Render ZERO text, letters, words, numbers, labels, or typography of any kind
- No titles, no subtitles, no body text, no captions, no page numbers
- No decorative text, no watermark text, no embedded quotes
- Leave all designated blank areas as CLEAN, EMPTY space with only the background texture/color
- This image is a BLANK CANVAS that will have text added later as separate layers
```

### 按页面类型的构图模板

| 页面类型 | 构图特征 | 留白比例 | Builder |
|---------|---------|---------|---------|
| 封面 (Cover) | 视觉焦点居中偏下，四角/边缘装饰 | ~50% 中央 | `build_cover` |
| 目录 (Contents) | 顶部标题+装饰，中部大面积纯净留白 | ~60% | `build_contents` |
| 全宽内容 | 顶部装饰带，中下大面积纯色 | ~70% 中下 | `build_content_full` |
| 左文右图 (Split) | 左侧纯净，右侧视觉区块 | ~55% 左侧 | `build_content_split` |
| 数据展示 (Data) | 深色背景 + 浅色卡片轮廓 | ~45% 卡片内 | `build_data_highlight` |
| 对比页 (Compare) | 双色分区 + 中央分隔 | ~60% 双侧 | `build_comparison` |
| 章节分隔 (Divider) | 左留白 + 右大型装饰 | ~55% 左下 | `build_section_divider` |
| 结尾 (Closing) | 居中聚焦 + 四周渐变 | ~50% 中央 | `build_closing` |

### 阶段一 QA

1. 无文字残留（目视 + OCR）
2. 留白区域完整（reservedZones 内无装饰元素侵入）
3. 风格一致（全 deck 色彩/纹理/元素统一）
4. 分辨率 ≥ 1920×1080 PNG
5. 文件命名 NN-slide-{slug}.png 序号连续

---

## 阶段二：可编辑内容叠加

### 核心代码模式

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn

# 1. 初始化 16:9 画布
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 2. 空白布局 + 铺底图 (Layer 1)
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.shapes.add_picture(bg_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))

# 3. 叠加可编辑文本框 (Layer 2)
tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
tf = tb.text_frame
tf.word_wrap = True
tf.auto_size = MSO_AUTO_SIZE.NONE
tf.margin_left = Inches(0.05)
tf.margin_right = Inches(0.05)
tf.margin_top = Inches(0.02)
tf.margin_bottom = Inches(0.02)
p = tf.paragraphs[0]
r = p.add_run()
r.text = "文本内容"
r.font.name = "Calibri"
r.font.size = Pt(16)
set_ea_font(r, "Microsoft YaHei")  # CJK 东亚字体

# 4. 截图叠加 (Layer 3)
pic = slide.shapes.add_picture(img_path, Inches(x), Inches(y), width=Inches(w))

# 5. 保存 + Office 2016 修复
prs.save(output_path)
fix_slide_size_type(output_path)
```

### CJK 东亚字体设置（唯一允许的 XML 操作）

```python
def set_ea_font(run, ea_font="Microsoft YaHei"):
    """设置东亚字体。python-pptx 不直接支持 CJK 东亚字体 API，
    必须通过 XML a:ea 元素设置。这是本规范中唯一允许的自定义 XML 操作。"""
    rPr = run._r.get_or_add_rPr()
    ea_el = rPr.find(qn("a:ea"))
    if ea_el is None:
        ea_el = rPr.makeelement(qn("a:ea"), {"typeface": ea_font})
        rPr.append(ea_el)
    else:
        ea_el.set("typeface", ea_font)
```

### 溢出防护

```python
CHAR_BUDGET = {
    "cover_title": 60, "cover_subtitle": 90,
    "slide_title": 55, "subtitle": 80,
    "body_full": 500, "body_half": 300,
    "section_head": 40, "data_number": 20,
    "data_label": 40, "quote_text": 260,
    "footer": 80, "bullet_item": 90,
}

def guard(text, max_chars):
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars - 1]
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > 0 else cut) + "…"
```

配合 `word_wrap=True` + `auto_size=MSO_AUTO_SIZE.NONE` 防止溢出。

### CJK 字体规范

| 用途 | 拉丁字体 | 东亚字体 | 字号 |
|------|---------|---------|------|
| 封面标题 | Calibri Bold | Microsoft YaHei Bold | 36-48pt |
| 页面标题 | Calibri Bold | Microsoft YaHei Bold | 28-36pt |
| 副标题 | Calibri Light | Microsoft YaHei Light | 14-20pt |
| 正文 | Calibri | Microsoft YaHei | 14-18pt |
| 数据大字 | Calibri Bold | Microsoft YaHei Bold | 40-72pt |
| 页脚/页码 | Calibri Light | Microsoft YaHei Light | 10-12pt |

必须同时设置 `font.name` + `<a:ea>` 东亚字体。中文正文不小于 14pt，行距 1.3-1.5 倍。

### 页面类型 Builder（8 种）

8 种标准 Builder 函数：`build_cover`、`build_contents`、`build_section_divider`、`build_content_full`、`build_content_split`、`build_data_highlight`、`build_comparison`、`build_closing`。

每种 Builder 遵循统一模式：铺底图 → 叠标题文本框 → 叠副标题(可选) → 叠正文/数据 → 叠截图(可选) → 叠页脚(可选)。

主编排器 `build_presentation()` 读取 layout-map.json + content_data，按 slide type 分发到对应 Builder。

完整 Builder 代码参见规范文档 `ai-ppt-production-spec.md` 第五章。

---

## 截图处理规范（PPT 配图专用）

### 核心原则："AI 看，PIL 做"

- **AI 视觉分析**（Qwen-VL 等）：负责理解截图内容、识别关键区域坐标、建议裁剪/标注策略
- **PIL 精准执行**：负责裁剪、等比缩放、合并、画标注（圆圈/箭头/高亮框/编号）

**绝对禁止**：使用 AI 图像编辑模型（qwen-image-edit、wan2.7-image-pro 等）编辑含中文文字的截图。所有 AI 图像编辑模型在编辑含中文文字的截图时都会产生乱码，这是模型固有限制，不是配置问题。

### 中文乱码根因

阿里 4 款图像编辑模型（qwen-image-edit-max/pro、wan2.5-i2i、wan2.7-image-pro）主要基于英文/拉丁文训练，对 CJK 字符的生成能力极差。编辑含中文截图时，模型会尝试"重新生成"文字区域，产生伪汉字乱码。

**唯一安全的 AI 图像编辑场景**：对不含文字的纯图形/照片进行编辑（风格迁移、背景更换、色彩调整）。

### 截图处理流程

```
Step 1: AI 视觉分析 → 输出结构化 JSON（关键区域坐标、裁剪建议、标注位置）
Step 2: 人工审核（可选）→ 调整裁剪/标注策略
Step 3: PIL 精准执行 → crop() / resize(LANCZOS) / paste() / draw.*()
```

### PIL 核心操作

```python
from PIL import Image, ImageDraw, ImageFont

# 裁剪
cropped = img.crop((x1, y1, x2, y2))

# 等比缩放（永远保持宽高比，不拉伸变形）
w, h = cropped.size
new_h = int(h * new_w / w)
resized = cropped.resize((new_w, new_h), Image.LANCZOS)

# 画红色圆圈标注
draw = ImageDraw.Draw(resized)
draw.ellipse([x-30, y-30, x+30, y+30], outline='red', width=3)

# 画箭头 + 三角形头部
draw.line([(x1, y1), (x2, y2)], fill='red', width=3)
draw.polygon([(x2, y2), (x2-10, y2-5), (x2-10, y2+5)], fill='red')

# 写中文编号（使用字体文件）
font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 24)
draw.text((x, y), '①', fill='red', font=font)

# 合并多张截图
canvas = Image.new('RGB', (total_w, total_h), 'white')
canvas.paste(img1, (0, 0))
canvas.paste(img2, (0, img1.size[1] + 10))
```

### 截图筛选标准

**保留**：展示 AI 能力、展示关键结果（重要数字/结论）、展示操作流程、展示对比/变化。

**淘汰**：工具调用日志、营销/落地页、重复截图、低信息密度。

### 图片清晰度优化

**根因**：手机截图分辨率低（宽 578-851px），放大后插值模糊。

**优化优先级**：
1. 重新截取高分辨率桌面截图（最优，根本性解决）
2. Real-ESRGAN AI 超分 2x（spandrel 加载 realesr-general-x4v3.pth，带磁盘缓存）
3. 禁用 PIL UnsharpMask 锐化（降低截图真实感，效果有限）

**关键规则**：对源图做 N 倍超分后再裁剪时，所有下游坐标（裁剪 box、高亮框、圆圈标注）都必须乘以 N 倍，否则标注位置会偏移到错误内容上。

### 标注坐标定位

PPT 配图图标标注坐标必须通过像素扫描 bbox 确定中心，不能从标题文字位置估算。图标通常在标题左侧 20-50px 处，y 坐标因卡片内边距比估算值偏下 20-40px。

### 截图组合排版

右侧 1/3 是工具调用日志（代码行）的截图，裁剪时需限制右边界（如原图 1615 宽时限制到 ~790px），否则 PPT 上出现代码碎片。

---

## Office 2016 兼容性规范

### sldSz type 修复（关键）

python-pptx 默认 `type=screen4x3`，实际 16:9 尺寸会触发 Office 2016 "内容有问题"修复提示。必须后处理修复：

```python
import zipfile, shutil
from lxml import etree

def fix_slide_size_type(pptx_path):
    """修复 sldSz type 属性：screen4x3 → screen16x9"""
    tmp = pptx_path + ".tmp"
    with zipfile.ZipFile(pptx_path, 'r') as zin, \
         zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'ppt/presentation.xml':
                root = etree.fromstring(data)
                ns = 'http://schemas.openxmlformats.org/presentationml/2006/main'
                for sldSz in root.iter(f'{{{ns}}}sldSz'):
                    sldSz.set('type', 'screen16x9')
                data = etree.tostring(root, xml_declaration=True,
                                      encoding='UTF-8', standalone=True)
            zout.writestr(item, data)
    shutil.move(tmp, pptx_path)
```

此函数只修改 presentation.xml 内容，保留 ZIP 中所有其他文件（包括缩略图）。

### XML 操作白名单

| 允许 | 代码模式 |
|------|---------|
| CJK 东亚字体 | `rPr.append(ea_el)` (在 `a:rPr` 内添加 `a:ea`) |

| 禁止 | 原因 | 替代方案 |
|------|------|---------|
| 删除/重建 `p:spPr` | 元素顺序违反 OOXML schema | 创建时直接设置属性 |
| 修改 `a:prstGeom` 实现圆角 | Office 2016 校验严格 | 不使用圆角 |
| Re-zipping 并删除文件 | Content_Types.xml 引用丢失 | 用 fix_slide_size_type 只改内容 |
| frosted panel 半透明蒙版 | spPr 子元素操作不稳定 | 在阶段一底图中直接绘制 |

### 保存规范

必须使用 `prs.save()` 直接保存。禁止自定义 re-zipping（会导致 Office 2016 文件损坏）。

### 对比度保障

由于 frosted panel 不可用，文字可读性必须在阶段一解决：在底图 Prompt 中要求留白区域为"纯净纯色背景"，深色底 + 白色/浅色文字组合最佳。

---

## iSlide 设计模式借鉴

### 配色公式

```
专业数据报告 = 暗色主色(70%) + 对比辅色(20%) + 高亮色(10%)
```

| 风格 | 主色 | 辅色 | 高亮色 | 适用场景 |
|------|------|------|--------|---------|
| 深蓝商业 | `#333F50` | `#9BDDDD` | `#E9886B` | 严肃报告、投资路演 |
| 紫金科技 | `#4A3350` | `#CF6857` | `#EDBF5F` | 商业报告、科技发布 |
| 青绿活力 | `#79BAB4` | `#D24852` | `#79B670` | 轻松话题、社会分析 |

关键规律：暗色调始终是主色基座；青绿色系高频出现适合数据辅助色；金色/橙红专用于数据高亮。

### 排版层级 T1-T5

| 层级 | 字号 | 用途 | 字重 | 颜色 |
|------|------|------|------|------|
| T1 大标题 | 44-54pt | 封面/章节 | Bold | 主色/白色 |
| T2 页面标题 | 18-24pt | 每页标题 | Bold | 主色 |
| T3 数据标签 | 12-16pt | 百分比/数值 | Regular | 高亮色 |
| T4 正文 | 10-12pt | 说明文字 | Regular | 深灰 |
| T5 脚注 | 8-10pt | 数据来源 | Light | 浅灰 |

### 版式结构

```
顶部色带/标题区 → 核心视觉区域(60-70%面积) → 数据来源脚注 → 品牌署名
```

不设页码，靠内容自然流动引导阅读。封面→分节→数据页→结论页的叙事弧结构。

### 六大视觉叙事技巧

1. **大字报数据**：关键数据 44-72pt 超大字号，震撼传达
2. **对比叙事**：Before vs After，用高亮色标记变化
3. **人物角色化**：3-4 类角色各配图标+数据卡片
4. **时间轴叙事**：横向时间线+端点标记+连接线
5. **数据来源标注**：每页底部 Source: XXX（8-10pt 灰色）
6. **渐进信息层次**：透明度 33-50% 创建视觉深度

### 底图 Prompt 增强

```
DESIGN PRINCIPLES:
- 暗色主色+对比高亮色配色体系，70/20/10 比例
- 数据展示区纯色背景，确保文字可读
- 装饰元素集中在页面边缘，中央保持干净
- 几何/扁平/矢量风格，不用照片级写实
- 底部预留 0.5" 灰色条带用于来源标注
- 视觉密度：balanced
```

---

## 执行流程

```
阶段零：采集主题/受众/页数/风格 → analysis.md
    ↓
阶段一：outline.md → layout-map.json → Prompt → 图像生成 → QA
    ↓
阶段二：content.md → overlay-script.py → prs.save() → fix_slide_size_type() → QA
    ↓
阶段三：文本校验 → 视觉抽检 → Office 2016 兼容性验证 → 交付
```

## 成品验证

```python
from pptx import Presentation
prs = Presentation("output/{topic-slug}.pptx")
print(f"{len(prs.slides)} slides OK")
for i, slide in enumerate(prs.slides, 1):
    texts = [shape.text for shape in slide.shapes if shape.has_text_frame]
    print(f"  Slide {i}: {len(texts)} text elements")

# Office 2016 兼容性验证
import zipfile; from lxml import etree
with zipfile.ZipFile("output/{topic-slug}.pptx") as z:
    sldSz = etree.fromstring(z.read('ppt/presentation.xml')).find(
        '{http://schemas.openxmlformats.org/presentationml/2006/main}sldSz')
    assert sldSz.get('type') == 'screen16x9', f"Wrong type: {sldSz.get('type')}"
    print("sldSz type: OK (screen16x9)")
```

## 跨平台执行

| 平台 | 图像生成 | python-pptx | 特殊说明 |
|------|---------|-------------|---------|
| QoderWork | ImageGen / baoyu-slide-deck | pptx 技能 | 支持最完整 |
| Hermes Agent | 平台内置或外部 API | pip install | 确保 Python 环境 |
| Trae | MCP 图像生成工具 | pip install | MCP 协议集成 |
| Cursor / Cline | 外部 API (DALL·E) | pip install | 需配置 API Key |
| 通用 Python | 任意图像生成 API | pip install | 最低依赖环境 |

通用依赖：`pip install python-pptx Pillow lxml`

## iSlide 工具评估

**结论：不纳入自动化管线。** 无公开 API、不支持无文字底图生成、无 CLI/headless 模式。仅适合作为人工设计灵感参考（模板灵感、配色参考）。

## python-pptx 踩坑汇总

1. Windows 终端输出中文 PPTX 文件名会乱码，用 ASCII 友好文件名
2. AI 底图标题/正文区有装饰元素导致文字可读性差 → 在阶段一 Prompt 中解决留白纯净度
3. `save` 后二次 zip 重打包（剥离缩略图）会导致 Office 2016 报"内容有问题" → 应直接 `prs.save()`
4. 默认 sldSz type=screen4x3，16:9 尺寸须后处理改为 screen16x9
5. frosted panel 和 re-zip 均导致损坏
6. `add_shape` 后用 `find()` 修改 spPr 子元素因命名空间解析产生非法节点 → 需 remove 旧 spPr 后用 lxml 完整重建（但 Office 2016 下仍不稳定，建议避免）
7. overlay-script.py 的 BASE 路径必须是 `dirname(dirname(__file__))`，因为脚本在 phase2-content/ 子目录，而图片在 phase1-visual/images/
8. Windows 下从 Bash/CMD 创建 PowerShell 脚本需 UTF-8+BOM 编码，否则中文解析失败
9. 复杂 PowerShell 脚本必须写入 .ps1 文件后用 -File 执行，不可用 -Command（$变量会被 shell 吃掉）

## 版本记录

| 版本 | 变更 |
|------|------|
| v1.0 | 初始版本：双阶段流程、四项技能协作、Prompt 模板、叠加代码库、QA 体系 |
| v1.1 | 补全页面类型：目录页/全宽内容/对比页 Builder，章节分隔/结尾页底图 Prompt |
| v2.0 | 跨平台泛化；Office 2016 兼容性规范；sldSz 修复；XML 操作白名单；禁用 frosted panel；iSlide 评估 |
| v2.1 | 新增截图处理规范（AI看PIL做）；图片清晰度优化方案；iSlide 设计模式借鉴附录；踩坑汇总 |
