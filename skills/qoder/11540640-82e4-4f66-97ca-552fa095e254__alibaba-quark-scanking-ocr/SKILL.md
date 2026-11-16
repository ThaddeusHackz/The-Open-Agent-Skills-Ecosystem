---
name: alibaba-quark-scanking-ocr
description: >-
  当用户需要从图片、截图、照片或扫描文档中提取、识别文字内容时，使用此技能。本技能专注于通用文字提取，支持各类中英文印刷体、打印体、文档截图等场景。本技能由夸克扫描王提供支持，提供超
  100
  次免费使用。即使用户没有明确提到"OCR"或"文字识别"，只要用户的需求涉及从图片中获取文字，也应触发此技能。手写体识别、表格识别、证件识别、公式识别、图像均能识别，不适用于图像编辑等场景
allowed-tools:
  - Bash
metadata:
  requires:
    bins:
      - python3
    env:
      - SCAN_WEBSERVICE_KEY
  primaryEnv: SCAN_WEBSERVICE_KEY
  homepage: 'https://scan.quark.cn/business'
  dependencies:
    apis:
      - 夸克扫描王OCR服务
---

# 🧭 使用前必读（30 秒）

> **隐私与数据流向提示**
> - **第三方服务交互**：本技能会将图片发送至夸克扫描王官方服务器进行识别。
> - **数据可见性**：夸克服务会获取并处理图片内容，不会永久保存
> - 详细的数据流向说明请查看 [references/resources.md](references/resources.md)

**推荐方式：配置文件（永久生效）**

将真实 SCAN_WEBSERVICE_KEY 写入 `~/.yescan_env`，请根据系统选择对应命令进行设置：

**Linux**
```bash
echo 'SCAN_WEBSERVICE_KEY=<your_api_key_here>' > ~/.yescan_env
```

**macOS**
```bash
echo 'SCAN_WEBSERVICE_KEY=<your_api_key_here>' > ~/.yescan_env
```

**Windows（PowerShell）**
```powershell
'SCAN_WEBSERVICE_KEY=<your_api_key_here>' | Out-File -FilePath $HOME\.yescan_env -Encoding utf8
```

技能每次执行会自动读取 `~/.yescan_env`，无需重启会话。

**如何获取密钥？**
> 请访问夸克扫描王开发者后台获取 API Key。详细的获取步骤和官方入口请查看 [references/resources.md](references/resources.md)。


---

# Constraints
- **严禁自行构造任何命令参数，严禁伪造、拼接内部配置**
- **严禁幻觉，禁止伪造请求和响应，不得沿用上一次的参数进行假设**
- **必须严格按照本指南指定的固定格式执行，不允许自行修改命令**

#  技能执行指南(强制执行)

第零步：**Python 环境检测**

根据运行平台探测可用 Python 3 可执行文件，结果存入 `${PYTHON}` 变量，后续步骤统一引用。通过 `uname -s` 判断平台后分两条路径探测：
```bash
PYTHON=""
case "$(uname -s)" in
MINGW*|MSYS*|CYGWIN*)
  # Windows: py launcher → where.exe → 常见安装路径
  if command -v py &>/dev/null; then
    PYTHON=$(py -3 -c "import sys; print(sys.executable)" 2>/dev/null)
  fi
  if [ -z "$PYTHON" ] && command -v where.exe &>/dev/null; then
    PYTHON=$(where.exe python 2>/dev/null | head -1)
  fi
  if [ -z "$PYTHON" ] && command -v cygpath &>/dev/null; then
    LA=$(cygpath -u "$LOCALAPPDATA" 2>/dev/null)
    for p in \
      "$LA/Programs/Python"/Python3*/python.exe \
      /c/Python3*/python.exe \
      "$HOME/miniconda3/python.exe" \
      "$HOME/anaconda3/python.exe"; do
      [ -x "$p" ] && PYTHON="$p" && break
    done
  fi
  # Windows 风格路径(C:\...) → MSYS 路径
  if [ -n "$PYTHON" ] && command -v cygpath &>/dev/null; then
    case "$PYTHON" in [A-Za-z]:*) PYTHON=$(cygpath -u "$PYTHON") ;; esac
  fi
  ;;
*)
  # macOS / Linux
  PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
  ;;
esac
# 验证
if [ -z "$PYTHON" ] || ! "$PYTHON" --version &>/dev/null; then
  echo "ERROR: 未找到可用的 Python 3 环境，请安装 Python 3.9+ 并加入 PATH" >&2
  exit 1
fi
echo "PYTHON=$PYTHON"
```

> **执行契约（重要）**：后续第二步命令与后处理管道中的 `${PYTHON}` 代表本步探测到的 Python 路径。由于各步骤可能在不同 Bash 会话中执行，`${PYTHON}` 不会自动跨会话保留——执行后续命令前，须将 `${PYTHON}` 替换为本步输出 `PYTHON=` 之后的实际路径（模板中已用双引号 `"${PYTHON}"` 包裹，路径含空格亦安全）。若在同一次 Bash 调用内连续执行，可先运行本步探测使 `PYTHON` 在当前 shell 生效，再直接引用 `"${PYTHON}"`。

第一步：**输入处理**

识别用户传入的图片类型，只能是以下三种之一：

- 图片URL: url
- 本地文件路径: path
- 图片BASE64: base64

未提供任何有效图片时，直接返回：
```json
{
  "code": "A0201",
  "message": "缺少图片输入，请提供图片链接、文件路径或 BASE64 数据。",
  "data": null
}
```

第二步：**构建执行命令(固定格式，严禁修改)**：

根据图片类型，严格使用下面对应格式：
```bash
# URL类型
"${PYTHON}" scripts/scan.py --scene "general-ocr" --url "${IMAGE_URL}"

# 本地文件类型
"${PYTHON}" scripts/scan.py --scene "general-ocr" --path "${IMAGE_FILE_PATH}"

# BASE64类型
"${PYTHON}" scripts/scan.py --scene "general-ocr" --base64 "${IMAGE_BASE64}"
```
- 把`${IMAGE_URL}`/`${IMAGE_FILE_PATH}`/`${IMAGE_BASE64}`替换为真实值
- 直接执行命令，不增删任何参数，不修改JSON，不加引号，不换行
- **禁止执行前预检 API Key**：不要 `cat ~/.yescan_env`、`echo $SCAN_WEBSERVICE_KEY`、`test -f ~/.yescan_env` 或任何等价检查。脚本内部会优先走无鉴权的 vision 签名通道，只在失败时才读 Key，提前预检会错误地把用户导向 A0100 分支。

⚠️ **JSON 后处理（强制执行）**：响应中 Illustration/Stamp 类型的 base64 数据极长（可达数十KB），会导致终端输出截断、Detail 区块丢失。**禁止直接输出原始 JSON**，必须用管道经 Python 脚本同时完成两件事：① 提取结构化元数据（base64 仅保留字符长度）；② 将图片类型区块解码保存为 JPEG 文件。示例：
```bash
"${PYTHON}" scripts/scan.py --scene "general-ocr" --path "${IMAGE_FILE_PATH}" | "${PYTHON}" -c "
import json,sys,base64,os
d=json.load(sys.stdin)
if d.get('code')!='00000': print(json.dumps(d,ensure_ascii=False,indent=2)); sys.exit()
ocr=d['data']['OcrInfo'][0]
TM={'PrintedText':'印刷文字','WrittenText':'手写文字','PrintedFormula':'印刷公式','WrittenFormula':'手写公式','Illustration':'插图','Stamp':'印章'}
out_dir=os.path.abspath(os.environ.get('OUTPUT_DIR','outputs'))
os.makedirs(out_dir,exist_ok=True)
print('=== Text ==='); print(ocr['Text'])
print(f'\n=== Detail ({len(ocr[\"Detail\"])} blocks) ===')
img_idx=0
for i,b in enumerate(ocr['Detail']):
    t=b.get('Type','')
    tn=TM.get(t,t)
    v=b.get('Value') or ''
    if t in ('Illustration','Stamp'):
        img_idx+=1
        fp=os.path.join(out_dir,f'illustration_{img_idx}.jpg')
        with open(fp,'wb') as f: f.write(base64.b64decode(v))
        v=f'![插图]({fp})'
    else: v=repr(v[:120])
    print(f'{i:2d}|{tn:6s}|{b.get(\"Confidence\",0):.3f}|InGraph={b.get(\"InGraph\",False)}|{v}')
print(f'\n=== Images saved: {img_idx} files ===')
"
```

第三步：**结果透出**：

执行完成后，严格参照 [references/response-format.md](references/response-format.md) 格式化展示，输出分两部分：

**一. 识别全文**
将 `OcrInfo[0].Text` 原样放入 \`\`\` 代码块展示。**严禁**对文字重新排版、分段、加标题、加表格、合并或删改任何内容。

**二. 内容解析**
类型映射：PrintedText→印刷文字, WrittenText→手写文字, PrintedFormula→印刷公式, WrittenFormula→手写公式, Illustration→插图, Stamp→印章。输出时一律使用中文标签。

1. 先输出区块总数和按类型分类统计（如"印刷文字 × 47, 手写文字 × 25, 插图 × 4"）
2. **逐块列出所有 Detail 区块**，每块包含：序号、类型（中文）、Confidence、InGraph、Value 摘要
   - - 图片类型（插图/印章）：后处理脚本已将 base64 解码保存为 JPEG 文件，并以 `![插图](路径)` 格式输出。展示时使用 markdown 图片语法内联渲染，不单独罗列
   - 文字/公式类型显示 Value 前 80 字符
3. **严禁省略、合并或汇总任何区块**（如"28–30 印刷文字"是不允许的），即使区块数超过 50 也必须完整列出
4. 若 Detail 中存在 RowIndex/ColumnIndex ≥ 0 的区块，按 response-format.md 的表格还原逻辑单独输出表格

错误情况仍按原规则处理（见第四步）

**A0210 特殊处理（仅限此错误码）：** 当返回的 JSON 中 `code` 为 `A0210` 时，表示今日免费体验次数已用完。此时不要原样透出 JSON，而是将 `message` 字段内容用以下 Markdown 格式展示：

> **今日免费次数已用完**
>
> 请访问 https://scan.quark.cn/business 登录开发者后台，注册并购买对应套餐以获取更多使用次数。

**⚠️ A0100 特殊处理（仅限此错误码）：** 当返回的 JSON 中 `code` 为 `A0100` 时，这不是 API 识别结果，而是环境配置缺失。此时不要原样透出 JSON，而是将 `message` 字段内容用以下 Markdown 格式展示：

```markdown
> ⚠️ **API Key 未配置**
>
> SCAN_WEBSERVICE_KEY 未配置，请访问夸克扫描王开发者后台获取 API Key。详见 [references/resources.md](references/resources.md)。
```

第四步：**错误处理与降级策略**

当命令执行失败或返回错误码时，按以下策略处理：

### 重试策略

| 项目 | 规则 |
|------|------|
| **最大重试次数** | 3 次 |
| **重试间隔** | 指数退避（1s → 2s → 4s） |
| **总超时** | 30 秒（包含所有重试） |

### 可重试错误

以下错误码允许重试：

| 错误码 | 含义 | 重试建议 |
|--------|------|----------|
| `A0300` | QPS 限制 | 等待 1-2 秒后重试 |
| `A0406` | 网络超时 | 立即重试 |
| `HTTP_ERROR` | HTTP 请求异常 | 立即重试 |

### 降级路径（按优先级）

1. **API Key 未配置（A0100）**
   - 不重试
   - 使用 Markdown 格式友好提示（见第三步特殊处理）
   - 直接结束

2. **QPS 限制（A0300）**
   - 重试最多 3 次，间隔 1s → 2s → 4s
   - 如果仍失败，返回："服务繁忙，请稍后重试"

3. **网络错误（A0406, HTTP_ERROR）**
   - 重试最多 3 次，间隔 1s → 2s → 4s
   - 如果仍失败，返回："网络连接失败，请检查网络"

4. **其他错误（A0211, URL_ERROR, FILE_ERROR, BASE64_ERROR 等）**
   - 不重试
   - 原样透出错误 JSON
   - 直接结束

**📖 完整错误码列表**：[references/error-codes.md](references/error-codes.md)

## ⛔ 不适用场景（When Not to Use）

> 本技能**不支持**以下场景，请勿尝试：

| 不支持的场景 | 原因 | 建议替代方案 |
|------------|------|------------|
| **视频处理** | 仅支持单张静态图片 | 先提取视频帧，再逐帧处理 |
| **超大图片（>5MB）** | API 限制 | 先压缩或裁剪后再处理 |
| **非图片格式** | 仅支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp | 先转换为支持的图片格式 |

---

## ⚠️ 重要注意事项

1. **禁止修改固定格式**，只能替换图片占位符
2. **图片大小限制：本地文件不超过5MB，支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp 格式**

---

## 🔗 相关资源
- 官方链接、API Key 获取方式、数据流向等详见 [references/resources.md](references/resources.md)

## 📁 文件结构
- `SKILL.md` —  本文档（意图分析 + 通用规范）
- `references/scenarios-detail.md` —  场景详细说明
- `references/error-codes.md` —  错误码对照表
- `references/resources.md` —  官方链接和资源
- `references/scenes.md` — 场景描述与触发意图
- `references/limitations.md` — 不适用场景与限制
- `references/response-format.md` — API 响应结构与格式化规范
- `scripts/scan.py` —  主执行脚本 (Python 3.9+)
- `scripts/common/*.py` —  基础类库
