---
name: extract-demo-visual
description: 从产品Demo HTML原型中提取视觉参数和截图，生成 visual-reference.md。当产品Demo更新后需要同步视觉规范到前端Spec时使用。
---

# Demo 视觉提取

从产品 HTML 原型中提取关键视觉参数，生成结构化的视觉参考文档，使 AI 工具无需打开 Demo 即可正确实现前端样式。

## 触发场景

- 产品发布新版本 Demo 后
- 前端实现与 Demo 视觉不一致时
- 新增页面/组件需要视觉对齐时

## 执行流程

### Step 1: 定位 Demo 文件

1. 查找最新版本的产品 Demo 目录：
   ```
   product-project/v{最新版本}/mcp应用平台-demo/mcp应用平台/MCP应用平台.html
   ```
2. 如果用户指定了版本路径，使用用户指定的路径

### Step 2: 启动 Demo 并截图

1. 在 Demo 目录下启动 HTTP 服务器：
   ```bash
   cd product-project/v{version}/mcp应用平台-demo/mcp应用平台
   python -m http.server 8080
   ```
2. 使用 Browser agent 打开 `http://localhost:8080/MCP应用平台.html`
3. 逐页截图（按路由遍历）：
   - `#/` — 首页
   - `#/mcp` — MCP 列表页
   - `#/skill` — Skill 列表页
   - `#/agent` — Agent 列表页
   - `#/item/{id}` — 详情页（取第一个 MCP 服务）
   - `#/docs` — 接入文档页
   - `#/audit` — 审计中心
4. 截图保存路径：`fe-project/mcp-market-fe-project/specs/{feature}/screenshots/`

### Step 3: 提取视觉参数

从 Demo 的 HTML/CSS 中提取以下信息：

| 提取项 | 说明 | 输出格式 |
|--------|------|----------|
| 色彩体系 | CSS变量、渐变色、文字色 | 表格（变量名、色值、用途） |
| 字体体系 | 字号、字重、行高 | 表格（场景、font-size、font-weight） |
| 间距体系 | padding、margin、gap | 表格（场景、值） |
| 圆角体系 | border-radius | 表格（场景、值） |
| 阴影体系 | box-shadow | 表格（场景、值） |
| 布局模式 | flex/grid 参数 | 代码块（CSS） |
| 背景/渐变 | 渐变定义、光斑效果 | 代码块（CSS） |

### Step 4: 生成 visual-reference.md

将提取的参数按以下结构输出到前端 spec 目录：

```
fe-project/mcp-market-fe-project/specs/{feature}/visual-reference.md
```

文件结构：
```markdown
# 视觉参考：{Feature名称}

**来源**: product-project/v{version}/... 
**提取日期**: {当前日期}

## 截图索引
| 页面 | 截图路径 | 说明 |
|------|----------|------|
| ... | ... | ... |

## 全局设计系统
### 色彩体系
...
### 字体体系
...

## 各页面/区块视觉规范
### 首页 Hero 区
...
### 卡片组件
...
```

### Step 5: 清理

停止 HTTP 服务器。

## 输出物

- `visual-reference.md` — 结构化视觉参数文档
- `screenshots/` — 页面截图文件（可选）

## 注意事项

- Demo 使用 Babel standalone 浏览器编译 JSX，必须通过 http:// 访问
- 提取参数时优先从 inline style 对象读取（Demo 不使用外部 CSS 文件）
- 如果 Demo 中使用了 CSS 变量，记录变量名和实际值的对应关系
- 颜色值统一使用十六进制格式（如 #E62129），透明色用 rgba() 格式
