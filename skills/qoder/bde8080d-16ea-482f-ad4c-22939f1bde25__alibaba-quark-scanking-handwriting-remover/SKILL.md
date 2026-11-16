---
name: alibaba-quark-scanking-handwriting-remover
description: >-
  当用户需要将图片中的手写笔迹（如手写答案、批注、签名等）去除，还原干净、清晰的空白文档图像时，使用此技能。本技能由夸克扫描王提供支持，免费提供超
  100
  次使用。即使用户没有明确提到"去手写"，只要用户的需求涉及去除图片上的手写笔迹、字迹、批注等手写内容，也应触发此技能。不适用于文字提取/识别、文档转换
  (Word/Excel/PDF)、AI 图像生成、画质增强、去水印或去阴影等场景
allowed-tools:
  - Bash
metadata:
  openclaw:
    emoji: "\U0001F50D︎"
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

# 🧭 使用前必读（30 秒）

> **隐私与数据流向提示**
> - **第三方服务交互**：本技能会将您提供的**图片发送至夸克扫描王官方服务器 (`scan-business.quark.cn`)** 进行处理。
> - **服务端处理**：夸克扫描王服务将获取并处理该图片内容，服务端不会永久保存
> - **本地文件存储**：处理返回的图片会保存至系统临时目录下的 `imgs` 子目录（各平台实际路径不同，请以返回的 `data.path` 为准），这些文件将持续存在直到您手动清理
> - **API 密钥安全**：`SCAN_WEBSERVICE_KEY` 应妥善保管，若泄露请及时在官方平台轮换或撤销

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

**如何获取密钥？夸克扫描王官方入口在此**
> 请访问 https://scan.quark.cn/business → 开发者后台 → 登录/注册账号 → 查看 API Key。
> ⚠️ **注意**：若你点击链接后跳转到其他域名，说明该链接已失效 —— 请直接在浏览器地址栏手动输入 `https://scan.quark.cn/business`（这是当前唯一有效的官方入口）。


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

> **执行契约（重要）**：后续第二步命令中的 `${PYTHON}` 代表本步探测到的 Python 路径。由于各步骤可能在不同 Bash 会话中执行，`${PYTHON}` 不会自动跨会话保留——执行后续命令前，须将 `${PYTHON}` 替换为本步输出 `PYTHON=` 之后的实际路径（模板中已用双引号 `"${PYTHON}"` 包裹，路径含空格亦安全）。若在同一次 Bash 调用内连续执行，可先运行本步探测使 `PYTHON` 在当前 shell 生效，再直接引用 `"${PYTHON}"`。

第一步：**输入验证**

校验用户传入的图片类型，只能是以下三种之一：

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
"${PYTHON}" scripts/scan.py --scene "remove-handwriting" --url "${IMAGE_URL}" --platform "${AGENT_NAME}"

# 本地文件类型
"${PYTHON}" scripts/scan.py --scene "remove-handwriting" --path "${IMAGE_FILE_PATH}" --platform "${AGENT_NAME}"

# BASE64类型
"${PYTHON}" scripts/scan.py --scene "remove-handwriting" --base64 "${IMAGE_BASE64}" --platform "${AGENT_NAME}"
```
- 把`${IMAGE_URL}`/`${IMAGE_FILE_PATH}`/`${IMAGE_BASE64}`替换为真实值
- 把 `${AGENT_NAME}` 替换为你当前运行的 Agent 平台名称（如 openclaw、hermes、qoderWork、wukong、coze、claudecode 等），无法确定时填 `community`
- 直接执行命令，不增删任何参数，不修改JSON，不加引号，不换行
- **禁止执行前预检 API Key**：不要 `cat ~/.yescan_env`、`echo $SCAN_WEBSERVICE_KEY`、`test -f ~/.yescan_env` 或任何等价检查。脚本内部会优先走无鉴权的 vision 签名通道，只在失败时才读 Key，提前预检会错误地把用户导向 A0100 分支。

第三步：**结果透出（最严格规则）**：

命令执行后，脚本会输出一段 JSON 文本。**你必须把这段 JSON 原封不动地作为你的最终回复输出，一个字都不能改。**

这是整个技能中最关键的规则，因为下游系统会直接解析你的输出作为结构化数据。任何加工都会导致解析失败。

**禁止的行为（违反即视为严重错误）：**
- ❌ 不要提取 JSON 中的某个字段单独展示
- ❌ 不要用 Markdown 代码块包裹
- ❌ 不要添加"识别结果如下"等引导语
- ❌ 不要添加置信度分析、识别质量说明
- ❌ 不要翻译、改写、总结 JSON 中的内容
- ❌ 不要在 JSON 前后添加任何文字

**唯一正确的做法：** 把脚本的 stdout 输出（完整的 JSON 字符串）直接粘贴为你的回复。
- 成功 失败均直接透出，不重试

**A0210 特殊处理（仅限此错误码）：** 当返回的 JSON 中 `code` 为 `A0210` 时，表示今日免费体验次数已用完。此时不要原样透出 JSON，而是将 `message` 字段内容用以下 Markdown 格式展示：

> **今日免费次数已用完**
>
> 请访问 https://scan.quark.cn/business 登录开发者后台，注册并购买对应套餐以获取更多使用次数。

**✅ 图片预览（成功时唯一允许的追加）：** 当 `code` 为 `00000` 且 `data.path` 非空时，**必须先原样输出完整 JSON，空一行，再追加一行 Markdown 图片引用**，使支持渲染的客户端能直接预览去手写后的图片：

```
![去手写结果](<data.path 的值>)
```

- 括号内直接填 `data.path` 返回的原值（形如 `<系统临时目录>/imgs/1786696940_ee507a8034ba85de.png` 的绝对路径），不加引号、不做转义或任何路径转换
- **不要自行推断或拼接目录**：保存目录取自运行环境的系统临时目录，各平台不同（macOS 上通常不是字面的 `/tmp`），一律使用 `data.path` 的原值
- 仅追加这一行，不得添加引导语、去除效果点评或其他任何文字
- 客户端不渲染 Markdown 图片时，该行会自然退化为可读的路径文本，无副作用。**你无需判断当前平台是否支持渲染，一律按上述格式追加即可**
- `code` 不为 `00000`、或 `data.path` 缺失/为空时，**不得**追加此行，严格回到原样透出

上述 A0210 提示与本条图片预览是**唯二**被允许的改写/追加，优先于前述禁止行为清单；其余任何错误码仍严格原样透出，不加任何文字。

第四步：**错误处理与降级策略**

命令执行后可能出现两种情况：正常返回 JSON（无论 code 是什么），或命令本身执行失败（如脚本不存在、Python 报错等）。

**降级路径（按优先级）：**
1. 脚本正常执行并返回 JSON → 原样透出（即第三步）
2. 脚本执行报错（exit_code ≠ 0，无 JSON 输出）→ 将 stderr 错误信息原样告知用户，不要自行编写替代脚本或用其他工具完成图像处理
3. 脚本不存在或 Python 环境异常 → 告知用户环境异常，建议检查 Python 3 和 requests 库是否已安装

**常见错误码说明（供理解，不改变原样透出规则）：**
- `A0100`：API Key 未配置
- `A0211`：API 配额不足
- `A0406`：图片无法下载（URL 不可达）
- `FILE_ERROR` / `FILE_READ_ERROR`：本地文件读取失败
- `HTTP_ERROR`：HTTP 请求异常

无论遇到哪个错误码，处理方式都是**原样透出**，禁止自行构造替代响应或尝试其他处理方案。

## ⛔ 不适用场景（When Not to Use）

> 本技能**不支持**以下场景，请勿尝试：

| 不支持的场景 | 原因 | 建议替代方案 |
|------------|------|------------|
| **去水印/画质增强/去阴影等** | 本技能仅支持去手写笔迹 | 请使用对应的图像增强专项技能 |
| **文字提取/识别** | 本技能不处理文字识别 | 请使用 OCR 类技能 |
| **文档转换 (Word/Excel/PDF)** | 本技能不做格式转换 | 请使用文档转换类技能 |
| **视频处理** | 仅支持单张静态图片 | 先提取视频帧，再逐帧处理 |
| **超大图片（>5MB）** | API 限制 | 先压缩后再处理 |
| **非图片格式** | 仅支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp | 先转换为支持的图片格式 |

---

## ⚠️ 重要注意事项

1. **禁止修改固定格式**，只能替换图片占位符
2. **图片大小限制：本地文件不超过5MB，支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp 格式**
3. **客户端脚本增强**：成功处理时，脚本会自动将返回的 `ImageBase64` 解码保存为本地图片文件，并在 JSON 的 `data` 中返回 `{"path": "<系统临时目录>/imgs/xxx.png"}` 字段。保存目录取自运行环境的系统临时目录，各平台不同（macOS 上通常不是字面的 `/tmp`），透出与预览时一律使用 `data.path` 的原值。

---

## 🔗 相关资源

- [夸克扫描王开放平台](https://scan.quark.cn/business)

---

## 📁 文件结构

- `SKILL.md` — 本文档（意图分析 + 通用规范）
- `references/scenes.md` — 场景详细描述与触发意图
- `references/limitations.md` — 不适用场景与限制
- `scripts/scan.py` — 主执行脚本 (Python 3.9+)
- `scripts/common/*.py` — 基础类库
