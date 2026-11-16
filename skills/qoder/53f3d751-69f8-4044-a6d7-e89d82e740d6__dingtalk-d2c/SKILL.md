---
name: dingtalk-d2c
description: 将 MasterGo 设计稿转换为钉钉 React 组件代码。当用户提供 MasterGo 设计稿 URL、要求将设计稿还原为代码、或需要基于钉钉 UI 库（dingtalk-design-desktop/mobile）生成 React + TypeScript + Less Module 组件时使用此技能。
---

# 钉钉设计稿转代码（D2C）

基于 MasterGo DSL 数据，结合钉钉官方 UI 库，生成 React + TypeScript + Less Module 组件代码。

**技术栈**：React + TypeScript + Less Module + dingtalk-design-desktop/mobile + dingtalk-theme + @ali/ding-icons

## 前置要求：安装 MasterGo MCP

`mcp__getDsl` 工具由 `@mastergo/magic-mcp` 提供，**使用本技能前必须先完成以下配置**，否则无法调用 getDsl 工具。

**第一步：获取你的 MasterGo Token**

前往 https://mgdone.alibaba-inc.com/ 获取你的安全令牌。

> ⚠️ 注意数据安全：任何拥有该令牌的用户均可获取你 BUC 账号下的设计数据资产，请勿泄露。

**第二步：配置 MCP Server**

在你的 IDE MCP 配置文件中添加以下配置（将 `YOUR_TOKEN` 替换为你自己的令牌）：

```json
{
  "mcpServers": {
    "mastergo-magic-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "@mastergo/magic-mcp",
        "--token=YOUR_TOKEN",
        "--url=https://mgdone.alibaba-inc.com/"
      ],
      "env": {
        "NPM_CONFIG_REGISTRY": "https://registry.npmjs.org/"
      }
    }
  }
}
```

配置完成后重启 IDE，确认 `mcp__getDsl` 工具可用后再继续。

---

## 设计稿要求

使用本技能前，请确保提供的 MasterGo 设计稿满足以下条件：

- **使用钉钉组件库**：设计稿中的组件必须基于钉钉官方组件库（dingtalk-design-desktop / dingtalk-design-mobile）搭建，以确保 DSL 中的 `INSTANCE` 节点能正确映射到对应的钉钉组件
- **符合钉钉 UI 设计规范**：设计稿的颜色、字体、间距等样式应遵循钉钉 UI 设计规范，使用 `dingtalk-theme` 中定义的 Token，以确保生成的代码能正确引用 CSS 变量

> ⚠️ 若设计稿未使用钉钉组件库或不符合钉钉 UI 规范，生成的代码将无法正确映射钉钉组件和 Token，需要大量手动调整。

---

## 第一步：解析设计稿

从设计稿 URL 提取参数并调用 `mcp__getDsl`：

```
URL: https://mgdone.alibaba-inc.com/file/163367033922518?fileOpenFrom=shared&devMode=true&page_id=959%3A32677&layer_id=975%3A52931
→ fileId: 163367033922518
→ layerId: 975:52931（注意 URL decode：%3A → :）
```

调用 `mcp__getDsl(fileId, layerId)`，若返回的 `componentDocumentLinks` 不为空，逐个调用 `mcp__getComponentLink` 获取组件文档。

**分析 DSL 数据时，读取参考文档**：
- 识别组件（`type: "INSTANCE"`）→ 查阅 [references/dingtalk-components.md](references/dingtalk-components.md) 找对应钉钉组件
- 识别 Token（`paint_*`、`font_*`、`effect_*`）→ 查阅 [references/token-mapping.md](references/token-mapping.md) 找对应 CSS 变量

## 第二步：理解项目结构

扫描项目，了解组件目录规范、命名规范、文件结构、路径别名：

```bash
find . -type f \( -name "*.tsx" -o -name "*.ts" \) | grep -v node_modules | head -30
cat tsconfig.json 2>/dev/null | grep -A5 '"paths"'
```

选取 1-2 个现有组件阅读，理解 Props 定义风格、Less Module 使用方式、import 组织顺序。

## 第三步：规划组件并等待确认

按以下原则拆分组件，**输出规划后等待用户确认**，再进入代码生成：

**独立为组件**（满足任一）：DSL 标注为 `INSTANCE`、视觉上独立的功能区块、重复出现超过 2 次、层级深度超过 4 层且有明确语义

**保持内联**：纯样式容器、简单文本/图标组合、与父组件强耦合的局部元素

输出格式：
```
📦 组件规划
├── 主组件: {PageName}/index.tsx
└── 子组件: {PageName}/components/
    ├── {SubComponent1}/index.tsx - {功能描述}
    └── ...
```

## 第四步：生成代码

从底层到顶层生成（子组件 → 主组件）。

**组件模板**：
```tsx
import React from 'react';
import { Button } from 'dingtalk-design-desktop';       // PC 端组件按需引入
import { NavBar } from 'dingtalk-design-mobile';         // 移动端组件按需引入
import { AddOutlined } from '@ali/ding-icons';           // 图标按需引入
import styles from './ComponentName.module.less';

interface ComponentNameProps {
  // 明确定义所有 Props，禁止使用 any
}

const ComponentName: React.FC<ComponentNameProps> = ({ prop1 }) => {
  return <div className={styles.container}>{/* 内容 */}</div>;
};

export default ComponentName;
```

**Less Module 模板**：
```less
.container {
  // Token 变量格式：--common_xxx / --theme_xxx / --extended_xxx（不是 --dt-xxx）
  color: var(--common_level1_base_color);
  background: var(--common_bg_color);
  
  // 布局来自 DSL flexContainerInfo
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}
```

**Token 使用规则**：
- DSL 有 `token` 字段 → 查 [references/token-mapping.md](references/token-mapping.md) 找 CSS 变量
- DSL 无 `token` 但有色值 → 直接使用色值并注释来源
- 图片 URL → 直接用作 `src` 或 `background-image`

**图标使用规则**（查阅 [references/dingtalk-components.md](references/dingtalk-components.md) 的图标章节）：
- DSL 节点 `name` 如 `outlined/icon_common/Add_L_outlined` → `import { AddOutlined } from '@ali/ding-icons'`
- 命名规则：去掉路径前缀和尺寸后缀，转 PascalCase，加风格后缀（Outlined/Filled）

**布局规则**：
- `flexContainerInfo` → 生成 flex 布局
- `layoutStyle.width/height` → 直接用 px 值
- `flexGrow: 1` → `flex: 1`；`relativeX/Y` → Flex 布局下忽略

**移动端特殊处理**：

实现移动端设计稿时，以下两类系统级 UI 元素**不需要实现**，直接跳过对应 DSL 节点：

- **系统状态栏（Status Bar）**：位于页面顶部，显示信号强度、WiFi、电量、系统时间等系统信息的区域。在 DSL 中通常命名为 `StatusBar`、`status-bar`、`系统状态栏` 等
- **底部安全区（Home Indicator / Safe Area）**：位于页面底部，用于适配全面屏手机底部手势条的留白区域。在 DSL 中通常命名为 `HomeIndicator`、`home-indicator`、`SafeArea`、`安全区` 等

> 这两类元素属于系统原生 UI，在实际 App 运行时由系统自动渲染，前端代码无需实现。

## 第五步：质量检查

生成后逐项检查：
- [ ] 所有 Props 有明确 TypeScript 类型，无 `any`
- [ ] Less Module className 引用正确（`styles.xxx`）
- [ ] 钉钉 UI 组件按需 import（desktop 或 mobile，不混用）
- [ ] 图标从 `@ali/ding-icons` 按需 import，命名格式正确
- [ ] Token 使用正确格式（`var(--common_xxx)` 等，不是 `--dt-xxx`）
- [ ] 布局与 DSL flexContainerInfo 一致

## 第六步：输出总结

```
✅ 代码生成完成

📁 生成文件：
  - {路径}/index.tsx
  - {路径}/index.module.less

🧩 使用的钉钉组件：dingtalk-design-desktop: Button, ...
🎨 Token 数量：颜色 X 个，字体 X 个
⚠️ 注意事项：{需要用户手动处理的事项}
```

## 重要约束

- **Token 优先**：有 `token` 字段的样式必须用 CSS 变量，不能硬编码色值
- **等待确认**：组件规划完成后必须等用户确认再写代码
- **按需引入**：所有组件和图标必须按需引入
- **禁止猜测**：DSL 中没有的交互逻辑不要自行添加

## 参考文档

- **组件映射**：[references/dingtalk-components.md](references/dingtalk-components.md) — 识别到 DSL 中有 INSTANCE 节点或需要映射钉钉组件/图标时读取
- **Token 映射**：[references/token-mapping.md](references/token-mapping.md) — 分析 DSL styles 中的 Token 时读取
