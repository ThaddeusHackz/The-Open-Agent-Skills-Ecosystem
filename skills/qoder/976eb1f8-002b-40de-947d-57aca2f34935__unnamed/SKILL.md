---
name: alibaba-quark-scanking-rectify
description: 当用户需要对图像进行自动矫正（如透视校正、水平对齐）并智能裁剪多余边缘，以获得规整、清晰、便于阅读或存档的标准矩形文档图像时，使用此技能。本技能由夸克扫描王提供支持。即使用户没有明确提到"裁剪矫正"，只要用户的需求涉及把拍歪的图片扶正、裁掉多余边缘、矫正透视变形，也应触发此技能。不适用于文字提取/识别、文档转换 (Word/Excel/PDF)、AI 图像生成、画质增强或去水印去阴影等场景
metadata: {"openclaw":{"emoji":"🔍︎","requires":{"bins":["python3"],"env":["SCAN_WEBSERVICE_KEY"]},"primaryEnv":"SCAN_WEBSERVICE_KEY"},"homepage":"https://scan.quark.cn/business","dependencies":{"apis":["https://scan-business.quark.cn"]}}
---

# 🧭 使用前必读（30 秒）

> **隐私与数据流向提示**
> - **第三方服务交互**：本技能会将您提供的**图片发送至夸克扫描王官方服务器 (`scan-business.quark.cn`)** 进行处理。
> - **服务端处理**：夸克扫描王服务将获取并处理该图片内容，服务端不会永久保存
> - **本地文件存储**：处理返回的图片会保存至系统临时目录（如 `/tmp/imgs`），这些文件将持续存在直到您手动清理
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
python3 scripts/scan.py --scene "image-crop-rectify" --url "${IMAGE_URL}" --platform "${AGENT_NAME}"

# 本地文件类型
python3 scripts/scan.py --scene "image-crop-rectify" --path "${IMAGE_FILE_PATH}" --platform "${AGENT_NAME}"

# BASE64类型
python3 scripts/scan.py --scene "image-crop-rectify" --base64 "${IMAGE_BASE64}" --platform "${AGENT_NAME}"
```
- 把`${IMAGE_URL}`/`${IMAGE_FILE_PATH}`/`${IMAGE_BASE64}`替换为真实值
- 把 `${AGENT_NAME}` 替换为你当前运行的 Agent 平台名称（如 openclaw、hermes、qoderWork、wukong、coze、claudecode 等），无法确定时填 `community`
- 直接执行命令，不增删任何参数，不修改JSON，不加引号，不换行

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
| **画质增强/去水印/去阴影等** | 本技能仅支持裁剪矫正 | 请使用对应的图像增强专项技能 |
| **文字提取/识别** | 本技能不处理文字识别 | 请使用 OCR 类技能 |
| **文档转换 (Word/Excel/PDF)** | 本技能不做格式转换 | 请使用文档转换类技能 |
| **视频处理** | 仅支持单张静态图片 | 先提取视频帧，再逐帧处理 |
| **超大图片（>5MB）** | API 限制 | 先压缩后再处理 |
| **非图片格式** | 仅支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp | 先转换为支持的图片格式 |

---

## ⚠️ 重要注意事项

1. **禁止修改固定格式**，只能替换图片占位符
2. **图片大小限制：本地文件不超过5MB，支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp 格式**
3. **客户端脚本增强**：成功处理时，脚本会自动将返回的 `ImageBase64` 解码保存为本地图片文件，并在 JSON 的 `data` 中返回 `{"path": "/tmp/imgs/xxx.png"}` 字段。

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
