---
name: alibaba-quark-scanking-question-ocr
description: >-
  当用户需要识别习题、考题、试卷题目图片，将题目图片转化为可编辑的结构化文本时使用此技能。本技能由夸克扫描王提供支持，免费提供超 100 次使用。即使用户没有明确提到"题目识别"，只要用户的需求涉及从图片中提取题目内容，也应触发此技能。不适用于纯文字提取、图像生成、图像编辑等场景
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
      - 'https://scan-business.quark.cn'
---

# 使用前必读（30 秒）

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
- **单一意图原则：每次请求只执行一个意图类型，命中即执行**
- **严禁自行构造任何命令参数，严禁伪造、拼接内部配置**
- **严禁幻觉，禁止伪造请求和响应，不得沿用上一次的场景、参数进行假设**
- **必须严格按照本指南指定的固定格式执行，不允许自行修改命令**
- **强制独立意图识别：严禁参考对话历史或沿用上次场景；必须针对当前指令独立分析，不得继承任何前序状态或假设**

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

> **执行契约（重要）**：后续第三步命令中的 `${PYTHON}` 代表本步探测到的 Python 路径。由于各步骤可能在不同 Bash 会话中执行，`${PYTHON}` 不会自动跨会话保留——执行后续命令前，须将 `${PYTHON}` 替换为本步输出 `PYTHON=` 之后的实际路径（模板中已用双引号 `"${PYTHON}"` 包裹，路径含空格亦安全）。若在同一次 Bash 调用内连续执行，可先运行本步探测使 `PYTHON` 在当前 shell 生效，再直接引用 `"${PYTHON}"`。

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

第二步：**意图匹配&场景确定**
- 本技能仅支持题目识别场景
- 所有题目识别请求均使用 `question-ocr` 场景

第三步：**构建执行命令(固定格式，严禁修改)**：

先切到本技能目录（即本 SKILL.md 所在目录），再根据图片类型使用对应命令：
```bash
cd <本技能目录>

# URL类型
"${PYTHON}" scripts/scan.py --scene "question-ocr" --url "${IMAGE_URL}"

# 本地文件类型
"${PYTHON}" scripts/scan.py --scene "question-ocr" --path "${IMAGE_FILE_PATH}"

# BASE64类型
"${PYTHON}" scripts/scan.py --scene "question-ocr" --base64 "${IMAGE_BASE64}"
```
- `<本技能目录>` 替换为本 SKILL.md 文件的绝对路径所在目录
- 把`${IMAGE_URL}`/`${IMAGE_FILE_PATH}`/`${IMAGE_BASE64}`替换为真实值
- 直接执行命令，不增删任何参数，不修改JSON，不加引号，不换行
- **禁止执行前预检 API Key**：不要 `cat ~/.yescan_env`、`echo $SCAN_WEBSERVICE_KEY`、`test -f ~/.yescan_env` 或任何等价检查。脚本内部会优先走无鉴权的 vision 签名通道，只在失败时才读 Key，提前预检会错误地把用户导向 A0100 分支。

第四步：**结果透出**：

当命令执行成功（`code` 为 `"00000"`）时，脚本已预处理所有统计值。按以下模板输出：

## 一、识别全文

（遍历 data.blocks 数组，每个区块一段，**加粗展示**）

**区块 {index+1}：** {full_text，公式用 `$...$` 渲染，插图显示为 [插图]}

## 二、区块概要

| Block | 题号 | Detail数 | 类型分布 | 内容概要 |
|-------|------|---------|---------|----------|
（遍历 data.blocks 数组，每区块一行；题号从 question_no 取，无则为 "--"）

## 三、区块明细

（遍历 data.blocks 数组，每个区块一个子标题）

### 区块 {index+1}（{detail_count} 个元素）
类型分布：{types 键值对拼接，如"印刷文字 x 37, 插图 x 2"}

| 序号 | 类型 | 置信度 | 内容 |
|------|------|--------|------|
（遍历 details 数组，每元素一行）

**格式规则**：
- **置信度**：直接输出 `confidence` 字段值；为 `null` 时显示 `--`
- **内容**：类型含"公式"的行用 LaTeX 渲染（`$...$`）；插图行直接用 markdown 图片语法内联渲染；其他行直接输出 `value`，超 80 字符截断
- 不添加任何额外总结或评论

**A0100 特殊处理（仅限此错误码）：** 当返回的 JSON 中 `code` 为 `A0100` 时，这不是 API 识别结果，而是环境配置缺失。此时不要原样透出 JSON，而是将 `message` 字段内容用以下 Markdown 格式展示：

```markdown
> **API Key 未配置**
>
> SCAN_WEBSERVICE_KEY 未配置，请访问夸克扫描王开发者后台获取 API Key。详见 [references/resources.md](references/resources.md)。
```

**A0210 特殊处理（日配额耗尽）：** 当返回的 JSON 中 `code` 为 `A0210` 时，表示今日免费次数已用完。此时将 `message` 字段内容用以下 Markdown 格式展示：

```markdown
> **今日免费体验次数已用完**
>
> 请前往 https://scan.quark.cn/business 登录开发者后台，注册并购买对应套餐以获取更多使用次数。
```

第五步：**错误处理与降级策略**

当命令执行失败或返回错误码时，按以下策略处理：

### 重试策略

| 项目 | 规则 |
|------|------|
| **最大重试次数** | 3 次 |
| **重试间隔** | 指数退避（1s -> 2s -> 4s） |
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
   - 触发前置：**必须**先实际执行 `scripts/scan.py` 并收到脚本返回的 `code: "A0100"`；不得凭 `~/.yescan_env` 是否存在自行判决
   - 不重试
   - 使用 Markdown 格式友好提示（见第四步特殊处理）
   - 直接结束

2. **QPS 限制（A0300）**
   - 重试最多 3 次，间隔 1s -> 2s -> 4s
   - 如果仍失败，返回："服务繁忙，请稍后重试"

3. **网络错误（A0406, HTTP_ERROR）**
   - 重试最多 3 次，间隔 1s -> 2s -> 4s
   - 如果仍失败，返回："网络连接失败，请检查网络"

4. **其他错误（A0211, URL_ERROR, FILE_ERROR, BASE64_ERROR 等）**
   - 不重试
   - 原样透出错误 JSON
   - 直接结束

### 成功条件

- HTTP 状态码 200
- 响应 JSON 包含 `code: "00000"`
- 响应包含有效的 `data` 字段

### 失败条件

- HTTP 状态码非 200
- 响应 JSON 解析失败
- 响应 `code` 非 "00000"
- 超过最大重试次数
- 超过总超时 30 秒

**完整错误码列表**：[references/error-codes.md](references/error-codes.md)

## 场景快速索引

| 序号 | 场景名称 | scene 标识 | 适用场景关键词 |
|------|----------|-----------|---------------|
| 1 | 题目识别 | `question-ocr` | 题目、考题、习题、试卷、作业 |

**查看完整场景说明**：[references/scenarios-detail.md](references/scenarios-detail.md)

## 不适用场景（When Not to Use）

> 本技能**不支持**以下场景，请勿尝试：

| 不支持的场景 | 原因 | 建议替代方案 |
|------------|------|------------|
| **纯文字提取** | 本技能专注题目识别 | 使用通用 OCR 技能 |
| **公式识别** | 本技能不专注公式结构 | 使用公式识别技能 |
| **表格识别** | 本技能不处理表格 | 使用表格识别技能 |
| **视频处理** | 仅支持单张静态图片 | 先提取视频帧，再逐帧处理 |
| **超大图片（>5MB）** | API 限制 | 先压缩或裁剪后再处理 |
| **非图片格式** | 仅支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp | 先转换为支持的图片格式 |

---

## 重要注意事项

1. **禁止修改固定格式**,只能替换场景标识和图片占位符
2. **严禁自行构造 --scene 参数值，必须使用本文档指定的场景名**
3. **图片大小限制：本地文件不超过5MB，支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp 格式**

---

## 相关资源
- 官方链接、API Key 获取方式、数据流向等详见 [references/resources.md](references/resources.md)

## 文件结构
- `SKILL.md` —  本文档（意图分析 + 通用规范）
- `references/scenarios-detail.md` —  场景详细说明
- `references/error-codes.md` —  错误码对照表
- `references/resources.md` —  官方链接和资源
- `scripts/scan.py` —  主执行脚本 (Python 3.9+)
- `scripts/common/*.py` —  基础类库
