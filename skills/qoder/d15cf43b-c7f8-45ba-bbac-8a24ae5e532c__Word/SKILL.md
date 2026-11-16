---
name: alibaba-quark-scanking-word
description: 当用户需要将图片、截图或扫描件转换为 Word 文档（.docx）时，使用此技能。适用于包含复杂排版、合同或图文混排内容的图片或扫描件，可尽量还原原始版式并生成可编辑的 Word 文档。本技能由夸克扫描王提供转换支持。即使用户未明确提到格式转换，只要用户的需求涉及将图片内容转换为可编辑的 Word 文档（.docx），也应触发此技能。请勿用于提取纯文本或识别文字内容、转 Excel/PDF、图像增强处理或从零创建文档
metadata: {"openclaw":{"emoji":"🔍︎","requires":{"bins":["python3"],"env":["SCAN_WEBSERVICE_KEY"]},"primaryEnv":"SCAN_WEBSERVICE_KEY"},"homepage":"https://scan.quark.cn/business","dependencies":{"apis":["https://scan-business.quark.cn"]}}
---

# 🧭 使用前必读（30 秒）

> **隐私与数据流向提示**
> - **第三方服务交互**：本技能会将您提供的**图片发送至夸克扫描王官方服务器 (`scan-business.quark.cn`)** 进行识别。
> - **服务端处理**：夸克扫描王服务将获取并处理该图片内容，服务端不会永久保存
> - **本地文件存储**：识别返回的文件会保存至系统临时目录（如 `/tmp`），这些文件将持续存在直到您手动清理
> - **API 密钥安全**：`SCAN_WEBSERVICE_KEY` 应妥善保管，若泄露请及时在官方平台轮换或撤销
> - **图片来源**：仅限用户明确指定的图片文件

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
python3 scripts/scan.py --scene "image-to-word" --url "${IMAGE_URL}"

# 本地文件类型
python3 scripts/scan.py --scene "image-to-word" --path "${IMAGE_FILE_PATH}"

# BASE64类型
python3 scripts/scan.py --scene "image-to-word" --base64 "${IMAGE_BASE64}"
```
- 把`${IMAGE_URL}`/`${IMAGE_FILE_PATH}`/`${IMAGE_BASE64}`替换为真实值
- 直接执行命令，不增删任何参数，不修改JSON，不加引号，不换行

第三步：**结果透出**：
这是整个技能中最关键的规则，因为下游系统会直接解析你的输出作为结构化数据。任何加工都会导致解析失败。

- 执行完成后，*原样返回执行结果*，不修改，不翻译，不美化，不总结

**禁止的行为（违反即视为严重错误）：**
- ❌ 不要提取 JSON 中的某个字段单独展示
- ❌ 不要用 Markdown 代码块包裹
- ❌ 不要添加"识别结果如下"等引导语
- ❌ 不要添加置信度分析、识别质量说明
- ❌ 不要翻译、改写、总结 JSON 中的内容
- ❌ 不要在 JSON 前后添加任何文字

**唯一正确的做法：** 把脚本的 stdout 输出（完整的 JSON 字符串）直接粘贴为你的回复。

- 成功 失败均直接透出，不重试


## ⛔ 不适用场景（When Not to Use）

> 本技能**不支持**以下场景，请勿尝试：

| 不支持的场景 | 原因 | 建议替代方案 |
|------------|------|------------|
| **转 Excel/PDF** | 本技能仅支持转 Word | 请使用对应的转 Excel 或转 PDF 专项技能 |
| **视频处理** | 仅支持单张静态图片 | 先提取视频帧，再逐帧处理 |
| **批量处理** | 每次调用仅限单张图片 | 如需批量，请循环调用或联系管理员 |
| **实时摄像头流** | 非实时流处理架构 | 使用专用视频处理服务 |
| **超大图片（>5MB）** | API 限制 | 先压缩或裁剪后再处理 |
| **非图片格式** | 仅支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp | 先转换为支持的图片格式 |

---

## ⚠️ 重要注意事项

1. **禁止修改固定格式**，只能替换图片占位符
2. **图片大小限制：本地文件不超过5MB，支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp 格式**
3. **客户端脚本增强**：成功转换时，脚本会自动将返回的 `FileBase64` 解码保存为本地 `.docx` 文件，并在 JSON 的 `data` 中追加 `"path"` 字段。

---

## 🔗 相关资源
- [夸克扫描王开放平台](https://scan.quark.cn/business)

## 📁 文件结构
- `SKILL.md` —  本文档（意图分析 + 通用规范）
- `scripts/scan.py` —  主执行脚本 (Python 3.9+)
- `scripts/common/*.py` —  基础类库
