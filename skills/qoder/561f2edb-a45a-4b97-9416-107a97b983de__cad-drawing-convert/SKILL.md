---
name: cad-drawing-convert
slug: cad-drawing-convert
display_name: CAD图纸转换
display_name_en: CAD Drawing Convert
displayName: CAD 图纸与文档格式转换
summary: DXF/DWG 转 PDF/SVG、两版图纸对比、PDF/Office 日常互转，全程本机离线执行，文件不出门。
description: CAD 图纸与文档本地格式转换，全程本机执行不上传文件。核心能力 DXF/DWG(CAD) → PDF 白底黑线高清渲染（黑白单色、A0-A4 纸张、多布局导出、批量目录转换、零白边、DPI 可调、中文不乱码，DWG 自动调用 ODA 转换）；独有 SVG 矢量输出、dxfinfo 图纸体检、dxfdiff 两版图纸对比（新增红/删除蓝）；配套 PDF 合并（书签）/拆分/抽页/加密、PDF 转 Word/文本/图片/PPT/Excel 表格、Word/Excel/PPT 转 PDF、图片合并为 PDF、文本生成 PDF。Use when the user asks to convert DXF or DWG drawings to PDF/SVG, batch convert drawings, compare two drawing versions, merge or split PDFs, encrypt PDFs, convert PDF to Word/Excel/images, convert Office documents to PDF, or process drawing files locally offline. 关键词：DXF、DWG、CAD、图纸、转PDF、dxf2pdf、dxfdiff、对比、批量转换、布局、黑白打印、合并、拆分、抽页、加密、提取表格、pdf转word、pdf转excel、office转pdf、图片转pdf、SVG、离线、本地。不用于：扫描件表格提取（用 AI 多模态读图）、CAD 图纸内容识别（用图纸识图类技能）。
description_zh: DXF/DWG 图纸转 PDF 白底黑线高清渲染，支持黑白、批量、多布局、中文、水印、图层过滤、两版对比（含标注 DIMENSION 与文字变更清单）；PDF 家常互转带加密源解密（--password）；图纸交付包一键流与 A1/A2 多图拼版打印。全程本机文件不出门。
description_en: Convert DXF/DWG drawings to print-ready PDF locally with white background, monochrome mode, batch processing, multi-layout export, CJK font mapping, watermark, layer filtering and two-version diff comparison (including DIMENSION anchors and a text-change ledger). Includes PDF merge/split/extract/encrypt, encrypted-source reading (--password), PDF to Word/Excel/images/PPT, Office to PDF, a one-command deliverable pack (batch + merge + bookmarks + page footers) and multi-sheet impose-to-A1 printing. Files never leave your machine.
version: 1.0.0
author: fangcun
license: MIT
agent_created: true
examples_zh:
- "把这份 DXF 图纸转成黑白 PDF，A4 横向"
- "这两个版本的图纸改了哪里"
- "把目录下所有 DXF 批量转 PDF 合并成交付包"
examples_en:
- "Convert this DXF drawing to a monochrome landscape A4 PDF"
- "What changed between these two drawing versions?"
- "Batch convert all DXF files in this folder into one deliverable PDF"
compatibility: "Requires Python 3.10+. Install dependencies as needed: pip install ezdxf matplotlib pymupdf pdf2docx python-pptx reportlab pypdf pdfplumber openpyxl Pillow. office2pdf additionally requires local MS Office or LibreOffice. (China mainland users: if PyPI is slow, append -i https://mirrors.aliyun.com/pypi/simple/)"
metadata:
  version: "1.0.0"
---

# CAD 图纸转换

DXF 图纸转 PDF（白底黑线、可黑白、可调 DPI），外加一套 PDF/Office 日常互转。全部本地执行，文件不出本机。

## 何时使用

- 拿到 `.dxf` 图纸要转 PDF 打印、存档、发人（没有装 AutoCAD 的机器也能转）
- 拿到的是 `.dwg`：也支持——脚本自动调用本机 ODA File Converter（免费）转成 DXF 后走完整流程，批量模式也吃 `*.dwg`。未安装 ODA 会拦截并给下载指引：
  https://www.opendesign.com/guestfiles/oda_file_converter
- 图纸要黑白打印（`--monochrome`）
- 图纸要转 SVG 矢量图（网页/文档内嵌，无限缩放不糊）或 PNG 图片
- 转换前想先看图纸概况（`dxfinfo` 体检：图层、实体、字体风险）
- 批量合并/拆分/抽取 PDF 页
- PDF 转 Word、提取文本、导出图片、生成 PPT
- PDF 里的原生表格转 Excel
- Word/Excel/PPT 转 PDF（本机需有 Office 或 LibreOffice）
- 多张图片合成一个 PDF、文本生成 PDF

## 何时不用

- **DWG 但 ODA 未装**：DWG 会被直接拦截并提示先装 ODA File Converter（见上"何时使用"），此时按指引进安装或先让用户手动转 DXF
- **PDF 后处理加水印/加解密**：`--watermark` 只在 CAD 渲染出图时叠加，给现成 PDF 加水印、加密解密不在能力范围
- **扫描版 PDF 提表格**：没有文字层，让 AI 多模态直接读图更准
- **图纸内容识别**（抽位号、设备表、图例）：用图纸识图类技能，本技能只管转格式
- **已装 wpscli 的常规办公转换**：wpscli（金山官方）排版引擎质量更好，优先它。本技能的价值在断网环境、涉密图纸不出本机、零账号零付费、以及多布局/黑白/纸张级输出控制

## 命令

脚本路径相对于本 SKILL.md 所在目录：`scripts/cad_convert.py`

### DXF → PDF（核心）

```bash
python scripts/cad_convert.py dxf2pdf 图纸.dxf
python scripts/cad_convert.py dxf2pdf 图纸.dxf -o 输出.pdf
python scripts/cad_convert.py dxf2pdf 图纸.dxf --monochrome          # 黑白出图
python scripts/cad_convert.py dxf2pdf 图纸.dxf --dpi 600             # 高清
python scripts/cad_convert.py dxf2pdf 图纸.dxf --paper A4            # A0-A4 指定纸张
python scripts/cad_convert.py dxf2pdf 图纸.dxf --pad 0               # 贴图框零白边（打印用）
python scripts/cad_convert.py dxf2pdf 图纸.dxf --layout Layout1      # 指定布局(paperspace)
python scripts/cad_convert.py dxf2pdf 图纸.dxf --layout all          # 全部布局各出一份
python scripts/cad_convert.py dxf2pdf 图纸目录 --batch               # 批量: 目录下全部 DXF/DWG
python scripts/cad_convert.py dxf2pdf 图纸.dxf --watermark "仅供XX项目使用"   # 半透明斜角水印
python scripts/cad_convert.py dxf2pdf 图纸.dxf --only-layer 标注      # 只保留指定图层
python scripts/cad_convert.py dxf2pdf 图纸.dxf --hide-layer 家具 轴线 # 隐藏指定图层（可多个）
```

### DXF → SVG / PNG / 体检 / 两版对比

```bash
python scripts/cad_convert.py dxf2svg 图纸.dxf                        # 矢量 SVG，无限缩放
python scripts/cad_convert.py dxf2svg 图纸.dxf --layout all           # 全部布局
python scripts/cad_convert.py dxf2png 图纸.dxf --dpi 300              # PNG 图片
python scripts/cad_convert.py dxfinfo 图纸.dxf                        # 体检：版本/布局/图层/实体统计
python scripts/cad_convert.py dxfinfo 图纸.dxf --json                 # JSON 输出（供脚本/AI 消费）
python scripts/cad_convert.py dxfdiff 旧版.dxf 新版.dxf               # 两版对比：旧蓝/新红/共有灰
python scripts/cad_convert.py dxfdiff 旧版.dxf 新版.dxf -o 对比.pdf   # 指定输出
python scripts/cad_convert.py dxfdiff 旧版.dxf 新版.dxf --csv 变更.csv  # 导出变更清单（含文字变更对账）
python scripts/cad_convert.py dxfinfo 图纸.dxf --html 体检.html       # 可视化体检报告（图层色块+统计表）
```

- `dxf2svg`：真矢量输出（path 元素），网页内嵌、文档插图、无限放大不糊；转换前自动映射中文字体
- `dxfinfo`：转换前先体检——版本、布局数、图层及配色、实体类型统计、中文样式缺字体的风险提示。用户只说"看看这图纸"或转换前要决策时用它；`--html 报告.html` 另存一页可视化体检单（图层色块+统计表，可直接发群里）
- `dxfdiff`：设计变更审查利器——几何签名对比（类型+坐标容差1e-3），差异叠加渲染一张图（旧版删除=蓝、新版新增=红、两版共有=灰），终端同步给差异摘要（按类型统计）。支持 TEXT/MTEXT/LINE/CIRCLE/ARC/LWPOLYLINE/POINT/**DIMENSION**（锚点+实测值签名：改位置/改尺寸都能检出；SOLID 同画）；文字另开账：同位置改内容/纯新增/纯删除单独计数展示，`--csv 变更清单.csv` 导出（设计变更通知单素材）
- 图层过滤 `--only-layer` / `--hide-layer` 互斥（only 优先），图层名先用 `dxfinfo` 查；图层不存在 `[WARN]`，过滤后全空报错拦截。水印 `--watermark` 半透明不遮挡图纸，批量+水印直接组合用

- 输出默认与源文件同目录同名；`--layout all` 每个布局一份 `原名_布局名.pdf`
- `--paper` 省略时按 DXF 布局自带图纸尺寸，无则 A3 横向；图形纵向更长自动切竖版
- `--batch` 输出到 `目录/pdf_out/`，已转换且比源新的自动跳过，可反复执行做增量
- 渲染带非空校验：图形范围异常或文件过小会输出 `[WARN]`，此时必须人工打开 PDF 确认，不要直接交付
- 输入 `.dwg` 直接拦截并提示用 ODA File Converter 转换
- 错误处理：损坏/假后缀文件、输出目录不存在等统一报人话不吐堆栈；排查时加 `--debug` 看完整堆栈
- 已知限制：三维实体（3DSOLID）、光栅图像嵌入的保真度有限；中文依赖字体映射（脚本已自动处理，映射时会打 `[INFO]`）

### PDF 合并 / 拆分 / 抽页 / 加密

```bash
python scripts/cad_convert.py pdfmerge -d 图纸目录                    # 目录内全部 PDF 按文件名合并
python scripts/cad_convert.py pdfmerge -i a.pdf b.pdf c.pdf -o 合并.pdf
python scripts/cad_convert.py pdfmerge -i a.pdf b.pdf --no-bookmarks # 不要书签
python scripts/cad_convert.py pdfsplit 文件.pdf --pages-per-file 2    # 每 2 页一个文件
python scripts/cad_convert.py pdfextract 文件.pdf --pages 1 3 5 -o 抽取.pdf   # 页码从 1 开始
python scripts/cad_convert.py pdfencrypt 文件.pdf --user-pw 密码      # 打开密码
python scripts/cad_convert.py pdfencrypt 文件.pdf --owner-pw 密码     # 权限密码（可看不可改）
```

- pdfmerge 默认按源文件名生成 PDF 书签（大纲），几十份图纸合并后导航不迷路；`--no-bookmarks` 关闭
- pdfsplit / pdfextract 会把源文件书签按页码平移保留到产物
- pdfencrypt 用 AES 加密，两种密码可单用或同用
- **读加密源**：pdf2word / pdf2txt / pdf2img / pdf2ppt / pdf2xlsx / pdfmerge / pdfsplit / pdfextract 都支持 `--password 打开密码`（读已被加密的 PDF 源用；给 PDF 设密码是 pdfencrypt 的 --user-pw/--owner-pw，别混淆）

### 图纸交付包（pack，一键流）

```bash
python scripts/cad_convert.py pack 图纸目录 -o 交付包.pdf              # 目录 DXF/DWG → 单张 PDF
python scripts/cad_convert.py pack 图纸目录 --monochrome --paper A4    # 黑白 + 指定纸张
python scripts/cad_convert.py pack 图纸目录 --watermark "仅供XX项目使用" # 每页中文水印（半透明斜角）
python scripts/cad_convert.py pack 图纸目录 --no-footer               # 不盖页脚（默认每页盖"图名 · 页码"）
```

- 流程：目录内 DXF/DWG 批量转 PDF → 按文件名排序合并 → 自动书签 → 每页页脚（图名+页码，pymupdf 内置中文字体）→ 单张交付 PDF
- 输出默认 `目录名_交付包.pdf`；转不出的文件如实列 `[FAIL]` 清单不静默吞；目录里混入的 PDF 会被忽略（先自己转好不属 pack 职责）
- 水印在 CAD 渲染时逐张叠加（非后处理），中文字形走本机字体（宋体/黑体/微软雅黑），缺字自动回退西文默认

### 多图拼版打印（impose）

```bash
python scripts/cad_convert.py impose 图纸目录 -o 拼版.pdf             # 拼 A1（默认）
python scripts/cad_convert.py impose 图纸目录 --paper A2              # 目标纸张 A0-A4
python scripts/cad_convert.py impose 图纸目录 --margin 8 --gutter 4   # 边距/拼缝 mm
```

- 货架排样：按高矮排序、行内并排、装满换行换页，省纸；DXF/DWG 自动先转 PDF（复用 pack 转换链，黑白/水印参数照传），目录里现成 PDF 直接并入
- 每格下方小字标图名，单张图页面即成一个书签——发打印店直接按页打
- 不做逐页旋转：横竖混排会留缝但不重叠（横竖差别大的图建议分两次拼）

### PDF → 其他格式

```bash
python scripts/cad_convert.py pdf2word 报告.pdf
python scripts/cad_convert.py pdf2txt 报告.pdf
python scripts/cad_convert.py pdf2img 报告.pdf --dpi 200
python scripts/cad_convert.py pdf2ppt 报告.pdf
python scripts/cad_convert.py pdf2xlsx 数据表.pdf      # 仅原生矢量表格
```

### 其他 → PDF

```bash
python scripts/cad_convert.py office2pdf 方案.docx     # 也可 xlsx / pptx
python scripts/cad_convert.py img2pdf a.jpg b.png -o 合并.pdf
python scripts/cad_convert.py txt2pdf 说明.txt
```

## 依赖安装

首次使用按命令安装对应依赖（全部装齐也可以）：

```bash
pip install ezdxf matplotlib          # dxf2pdf
pip install pymupdf                   # pdf2txt / pdf2img / pdf2ppt
pip install pdf2docx                  # pdf2word
pip install python-pptx               # pdf2ppt
pip install reportlab                 # txt2pdf
pip install pypdf                     # pdfmerge / pdfsplit / pdfextract / pdfencrypt
pip install pdfplumber openpyxl       # pdf2xlsx
pip install Pillow                    # img2pdf
```

清华源缺 ezdxf 时换阿里镜像：

```bash
pip install ezdxf matplotlib -i https://mirrors.aliyun.com/pypi/simple/
```

### DWG 支持：安装 ODA File Converter（仅处理 DWG 时需要）

DXF 无需此步。要让脚本自动转换 DWG，装免费的 ODA File Converter：

**给人看的路径**：到 https://www.opendesign.com/guestfiles/oda_file_converter 下载 Windows 版 MSI（约 60MB），双击默认路径安装完即可，脚本自动检测。

**给 Agent 的路径（实测踩过的坑，照做少走弯路）**：

1. 直链不在页面 `<a>` 标签里，抓页面 HTML 搜 `guestfiles/get?filename=`。Windows 包真实文件名是 **`ODAFileConverter_QT6_vc16_amd64dll.msi`（不带版本号）**——搜索结果里 25.12/26.x 等带版本号的链接全是 404：
   `https://www.opendesign.com/guestfiles/get?filename=ODAFileConverter_QT6_vc16_amd64dll.msi`
2. 下载约 33MB 才是真 MSI（OLE 文件头 `ÐÏà¡±á`；若返回 33KB 的 HTML 是被 cookie 同意页拦截，带 referer 重试）。
3. 静默安装**需要管理员权限**，无人值守时两个坑：`msiexec /i <msi> /qn` 直接跑会 Error 1925（权限不足）；msiexec 不认正斜杠路径（Error 2343），必须反斜杠。备选 per-user 模式：`msiexec /i <msi> ALLUSERS="" MSIINSTALLPERUSER=1 TARGETDIR="<用户目录下自选路径>" /qn`——但装完 ezdxf 默认检测不到（只认 `Program Files\ODA\ODAFileConverter\ODAFileConverter.exe`），需设置 ezdxf options 的 `odafc-addon/win_exec_path` 指向实际 exe。
4. **最省事：让用户自己双击 MSI**（弹 UAC 点"是"），装完重跑即可。不要替用户折腾静默安装。

检测是否已装：`python -c "from ezdxf.addons import odafc; print(odafc.is_installed())"`

office2pdf 环境探测：脚本先试 MS Office COM（docx2pdf），失败再试 LibreOffice（soffice）。两者都没有时报错并给出下载地址——不要替用户静默降级成别的方案。

## 输出纪律

- 转换产物一律落在源文件同目录（或用户指定路径），不要写到临时目录让用户找不到
- 批量操作先列清单再执行；目录合并会按文件名排序，结果文件名要告诉用户
- 每次转换完成报告：输出路径 + 实体数/页数/表格数 + 文件大小
- dxf2pdf 出现 `[WARN]` 时不视为成功，必须人工核验后再交付
- `[SKIP]` 是增量跳过属正常；`[FAIL]` 的文件清单要如实报告，不要静默吞掉