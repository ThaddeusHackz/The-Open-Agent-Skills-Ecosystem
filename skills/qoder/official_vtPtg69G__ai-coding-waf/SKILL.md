---
name: ai-coding-waf
description: "AI Coding 成熟度评估（可视化交互版）。触发后在编辑器内嵌浏览器中打开交互式评估页面，支持表单填写、雷达图、Markdown 报告一键复制。| Visual interactive version of AI Coding maturity assessment with embedded browser UI."
---

# AI Coding WAF — 可视化交互版

> 一句话定义：通过**浏览器内嵌交互页面**完成 WAF 六支柱成熟度评估，支持分步表单、雷达图展示和 Markdown 报告一键复制。

---

## 触发条件

- "评估一下我们团队 AI Coding 水平"
- "成熟度评估"、"WAF 评估"
- "我们现在算 L 几？"
- "/ai-coding-waf"

---

## 执行步骤

本 SKILL 通过启动本地 HTTP 服务器，在编辑器内嵌浏览器中打开交互式评估页面。

```
1. 后台启动 Python HTTP 服务器，服务本 Skill 目录
2. 使用 run_preview 在编辑器中打开评估页面
3. 引导用户在页面中完成评估
4. 用户可复制 Markdown 报告粘贴回对话
```

### 步骤 1：启动本地服务

使用 `run_in_terminal` 以**后台模式**启动 HTTP 服务器：

```powershell
python -m http.server 18765 --directory "<SKILL_DIR>"
```

- `<SKILL_DIR>` 为本 Skill 所在目录的绝对路径（即包含 `assess.html` 的目录）
- 端口：`18765`（避免与其他服务冲突）
- 模式：`is_background: true`

### 步骤 2：打开预览

使用 `run_preview` 工具：

- **URL**：`http://localhost:18765/assess.html`
- **Name**：`AI Coding 成熟度评估`

### 步骤 3：引导用户

向用户说明：

> 评估页面已在右侧预览窗口打开。请按照 4 个步骤完成评估：
> 1. **基本信息** — 填写团队名称、规模、工具使用时长
> 2. **快速门控** — 4 个门控问题定位大致级别
> 3. **六支柱评估** — 每支柱选择 L1~L5 行为锚点
> 4. **评估报告** — 查看雷达图和改进路径
>
> 完成后点击「📋 复制到剪贴板」获取 Markdown 报告。

### 步骤 4（可选）：AI 解读

如果用户将报告粘贴回对话，可结合 v1 版本的支柱×模式导航映射提供深度解读和具体行动建议。

---

## 页面功能

交互式评估页面（`assess.html`）内置以下能力：

| 功能 | 说明 |
|------|------|
| 分步表单 | 4 步进度条引导，逐步填写 |
| 行为锚点 | 每支柱 L1~L5 完整行为描述供选择 |
| 自动门控 | 门控问题实时计算定位级别 |
| 雷达图 | Canvas 绘制六支柱雷达图 |
| 评估结论 | 木桶原理定级 + 最薄弱支柱识别 |
| 90天路径 | 基于最薄弱支柱的改进时间线 |
| Markdown 报告 | 完整报告一键复制到剪贴板 |

---

## 与 v1 的关系

| 维度 | v1（聊天版 `ai-coding-maturity-assess`） | v2（可视化版 `ai-coding-waf`） |
|------|------------|--------------|
| 交互方式 | 对话问答 | 浏览器表单 |
| 评估逻辑 | 完全一致 | 完全一致 |
| 依赖 | 无 | Python 3（HTTP 服务器） |
| 适用场景 | 快速评估、无浏览器环境 | 演示展示、团队共同填写 |

---

## 约束

- 所有评估逻辑在客户端 JavaScript 中完成，**不依赖外部 API**
- 评估规则与 v1 完全一致：WAF 六支柱、木桶原理、行为锚点
- 仅需 Python 3 用于启动 HTTP 服务器
- 页面零外部依赖，纯 HTML/CSS/JS
