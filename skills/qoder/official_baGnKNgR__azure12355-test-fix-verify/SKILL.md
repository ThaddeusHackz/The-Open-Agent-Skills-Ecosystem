---
name: test-fix-verify
description: Intelligent code testing, fixing, and verification assistant. Automatically executes appropriate testing and verification workflows based on different types of code changes. Use when verifying code changes - Backend API modifications require unit tests and build checks - Frontend changes require build checks and browser debugging with optional skip for trivial style changes - Configuration file changes require dependency installation and build checks - Code refactoring requires full test suite and lint checks - New feature development requires writing tests, running tests, and browser testing
---
# Test Fix Verify

## Overview

智能代码测试修复验证助手，根据不同的代码改动类型自动执行相应的测试和验证流程。

## Workflow Decision Tree

首先分析代码改动类型，确定使用哪个验证场景：

```
1. 检查 git diff 或用户描述
   │
   ├── 后端 API 改动？
   │   └── 场景 1: Backend API
   │
   ├── 前端组件改动？
   │   └── 场景 2: Frontend
   │
   ├── 配置文件改动？（package.json, tsconfig.json, .env 等）
   │   └── 场景 3: Configuration
   │
   ├── 代码重构（结构变化但功能不变）？
   │   └── 场景 4: Refactoring
   │
   └── 新功能开发？
       └── 场景 5: New Feature
```

## Scene 1: Backend API Changes

**触发条件：** 后端 API 路由、控制器、服务层代码修改

**验证步骤：**

1. **编写单元测试**

   - 识别修改的 API 端点或函数
   - 为每个修改点编写单元测试
   - 包括正常场景和边界条件
2. **运行单元测试**

   ```bash
   # 示例命令（根据项目调整）
   pnpm test
   pytest
   go test ./...
   ```
3. **构建检查**

   ```bash
   pnpm run build
   cargo build
   ```
4. **验证输出**

   - 确保所有测试通过
   - 确保构建成功
   - 如有失败，分析错误并修复

## Scene 2: Frontend Changes

**触发条件：** 前端组件、页面、样式修改

**验证步骤：**

1. **检查改动范围**

   - 如果仅是细微颜色/样式调整（如 `color: #fff` → `color: #f0f0f0`），跳过浏览器验证
   - 其他情况继续完整流程
2. **构建检查**

   ```bash
   pnpm run build
   # 或
   pnpm build
   ```
3. **浏览器调试验证**

   ```bash
   pnpm run dev
   # 或
   pnpm dev
   ```

   - 使用 Chrome MCP 工具打开浏览器
   - 导航到相关页面
   - 截图验证实际效果
   - 测试交互功能
4. **验证输出**

   - 构建成功无警告
   - 浏览器中视觉效果正确
   - 交互功能正常

## Scene 3: Configuration Changes

**触发条件：** `package.json`, `tsconfig.json`, `.env`, `vite.config.ts`, `next.config.js` 等配置文件修改

**验证步骤：**

1. **安装依赖**

   ```bash
   pnpm install
   # 或
   pnpm install
   ```
2. **构建检查**

   ```bash
   pnpm run build
   ```
3. **验证输出**

   - 依赖安装成功无冲突
   - 构建成功
   - 如构建失败，检查配置语法和兼容性

## Scene 4: Code Refactoring

**触发条件：** 代码重构、结构优化、不改变功能的修改

**验证步骤：**

1. **Lint 检查**

   ```bash
   pnpm run lint
   # 或
   pnpm lint
   ```
2. **运行完整测试套件**

   ```bash
   pnpm test
   # 或
   pnpm test
   ```
3. **验证输出**

   - Lint 无错误和警告
   - 所有测试通过（确保功能未改变）
   - 如有测试失败，重构可能引入了行为变化

## Scene 5: New Feature Development

**触发条件：** 新增功能、新组件、新页面

**验证步骤：**

1. **编写测试**

   - 为新功能编写单元测试
   - 覆盖主要使用场景
   - 包含边界条件和错误处理
2. **运行测试**

   ```bash
   pnpm test
   ```
3. **浏览器测试验证**

   ```bash
   pnpm run dev
   ```

   - 启动开发服务器
   - 使用 Chrome MCP 工具
   - 手动测试新功能
   - 截图记录验证结果
4. **验证输出**

   - 测试通过
   - 浏览器中功能正常工作
   - UI/UX 符合预期

## Common Practices

### 识别改动类型

使用以下命令分析改动：

```bash
# 查看改动文件
git diff --name-only

# 查看改动详情
git diff

# 查看最近改动
git status
```

### 错误处理

- 测试失败：分析错误信息，定位问题代码，修复后重新运行
- 构建失败：检查语法、依赖、配置，逐步修复
- Lint 错误：按建议修复代码风格问题

### 自动修复

某些错误可尝试自动修复：

```bash
# ESLint 自动修复
pnpm run lint -- --fix

# Prettier 格式化
pnpm run format
```

### Chrome MCP 工具使用

浏览器验证时使用的工具：

- `chrome_navigate`: 打开页面
- `chrome_screenshot`: 截图验证
- `chrome_read_page`: 读取页面内容
- `chrome_click_element`: 测试交互
