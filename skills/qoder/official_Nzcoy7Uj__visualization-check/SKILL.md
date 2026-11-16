---
name: "visualization-check"
description: "Visualization check. Invoke when need to verify each output has corresponding web UI, data renders correctly, and user interactions work properly."
---

# 可视化检查 Skill

## 概述

此 Skill 用于检查项目的每个输出是否都有对应的网页端可视化展示，确保用户能够看到所有重要的数据和状态。

## 调用时机

- 需要验证功能模块是否有 UI 展示时
- 需要检查数据是否正确渲染时
- 需要验证用户交互是否正常时

## 检查项目

### 1. 功能模块可视化检查

| 功能模块 | 数据输出 | UI 组件 | 可视化状态 |
|---------|---------|---------|-----------|
| 项目创建 | 项目元数据 | ProjectCreationWizard | ✓/✗ |
| 工作流状态 | 节点状态、进度 | WorkflowPanel | ✓/✗ |
| 研究进度 | 阶段、消息、进度条 | ResearchProgress | ✓/✗ |
| 思考日志 | AI 思考过程 | ThinkingLog | ✓/✗ |
| 文件树 | 项目文件结构 | FileTree | ✓/✗ |
| 编辑器 | 文件内容 | CodeEditor | ✓/✗ |
| 草稿预览 | 当前草稿 | DraftPreview | ✓/✗ |

### 2. 数据渲染检查

检查每种数据类型是否正确渲染：

#### 文本数据
- [ ] 项目标题正确显示
- [ ] 故事前提正确显示
- [ ] 错误消息正确显示

#### 状态数据
- [ ] 工作流状态正确映射到 UI
- [ ] 进度条正确更新
- [ ] 加载状态正确显示

#### 列表数据
- [ ] 文件树正确渲染
- [ ] 最近项目列表正确显示
- [ ] 思考日志正确追加

#### 流式数据
- [ ] SSE 事件实时更新 UI
- [ ] 打字机效果正常
- [ ] 进度动画流畅

### 3. 用户交互检查

| 交互类型 | 触发方式 | 预期响应 | 状态 |
|---------|---------|---------|------|
| 点击按钮 | 鼠标点击 | 执行操作 | ✓/✗ |
| 表单输入 | 键盘输入 | 数据绑定 | ✓/✗ |
| 文件选择 | 点击文件 | 打开编辑 | ✓/✗ |
| 暂停/继续 | 点击按钮 | 工作流控制 | ✓/✗ |
| 步骤导航 | 点击下一步 | 验证+跳转 | ✓/✗ |

### 4. 状态反馈检查

检查用户操作是否有适当的反馈：

- [ ] 按钮点击有 loading 状态
- [ ] 操作成功有成功提示
- [ ] 操作失败有错误提示
- [ ] 长时间操作有进度指示

### 5. 响应式布局检查

- [ ] 桌面端布局正确
- [ ] 侧边栏折叠正常
- [ ] 面板切换正常
- [ ] 模态框显示正常

## 检查流程

### 步骤 1：识别所有数据输出

```javascript
// 从 store 中识别所有状态
const storeState = {
    currentProjectPath,  // → 文件路径显示
    projectMeta,         // → 项目信息面板
    workflowState,       // → 工作流状态面板
    thinkingLog,         // → 思考日志面板
    researchProgress,    // → 研究进度面板
    projectFiles,        // → 文件树
    openFiles,           // → 编辑器标签页
    ...
}
```

### 步骤 2：检查每个输出的 UI 组件

```vue
<!-- 检查是否有对应的组件 -->
<template>
  <!-- 项目信息 → ProjectCreationWizard / ProjectInfo -->
  <!-- 工作流状态 → WorkflowPanel -->
  <!-- 研究进度 → ResearchProgress -->
  <!-- 思考日志 → ThinkingLog -->
  <!-- 文件树 → FileTree -->
  <!-- 编辑器 → CodeEditor -->
</template>
```

### 步骤 3：验证数据绑定

```vue
<!-- 检查数据是否正确绑定 -->
<div>{{ projectMeta?.title }}</div>
<div>{{ workflowState?.current_draft }}</div>
<div v-for="log in thinkingLog">{{ log }}</div>
```

### 步骤 4：测试用户交互

使用 Playwright 模拟用户操作：
1. 点击按钮
2. 填写表单
3. 选择文件
4. 检查响应

## 输出格式

```
# 可视化检查报告

## 功能模块覆盖
- 总模块数：X
- 有可视化：Y
- 缺失可视化：Z

| 模块 | 数据 | UI | 状态 |
|-----|------|-----|------|
| ... | ... | ... | ✓/✗ |

## 数据渲染
- 文本数据：✓/✗
- 状态数据：✓/✗
- 列表数据：✓/✗
- 流式数据：✓/✗

## 用户交互
- 按钮点击：✓/✗
- 表单输入：✓/✗
- 文件选择：✓/✗
- 工作流控制：✓/✗

## 状态反馈
- Loading 状态：✓/✗
- 成功提示：✓/✗
- 错误提示：✓/✗
- 进度指示：✓/✗

## 缺失的可视化
1. 数据：XXX → 建议添加：XXX组件
2. ...

## 发现的问题
1. ...
2. ...
```

## 工具使用

- 使用 `Read` 检查组件代码
- 使用 `Grep` 搜索数据绑定
- 使用 `mcp_Playwright_*` 进行交互测试
- 使用 `mcp_Playwright_playwright_screenshot` 截图验证
