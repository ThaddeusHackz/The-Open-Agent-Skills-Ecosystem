---
name: fe-code-standards
description: 前端代码规范检查与指导，覆盖HTML语义化、CSS命名与属性顺序、JavaScript命名约定与异步处理、组件化开发（React/Vue）、性能优化、工程化（ESLint+Prettier+Husky+Commitlint）及安全可访问性。在编写前端代码、创建组件、审查代码质量或配置前端工程化工具时自动应用。
---

# 前端代码规范

依据 `fe-rule.md` 规范文件，在前端开发全流程中执行以下标准。

## 命名约定速查

| 对象 | 规范 | 示例 |
|------|------|------|
| 文件夹/页面 | KebabCase | `user-list` |
| 组件 | PascalCase | `UserAvatar` |
| 文件 | camelCase | `userInfo.ts` |
| 变量/函数 | camelCase | `getUserInfo` |
| 常量 | UPPER_SNAKE_CASE | `API_ENDPOINT` |
| class/interface/type | PascalCase | `UserModel` |
| CSS 类名 | kebab-case | `btn-submit` |
| Hook | camelCase | `useUserInfo` |

## HTML 规范

1. 使用语义化标签 `<header>` `<nav>` `<main>` `<section>` `<footer>`，禁止滥用 `<div>` 代替
2. 属性书写顺序：`class` → `id` → `data-*` → 其他属性
3. 统一 2 空格缩进，属性过多时换行对齐
4. `<img>` 必须添加 `alt` 属性

## CSS / Sass 规范

1. 嵌套不超过 3 层
2. 属性书写顺序：布局 → 盒模型 → 视觉 → 文字排版
3. 禁止使用 `!important`，通过选择器优先级或重构解决
4. 响应式优先使用 `min-width`（移动端优先）

## JavaScript 规范

1. 使用 `const`/`let`，禁用 `var`
2. 优先解构赋值：`const { username, email } = user`
3. 异步用 `async/await`，必须 `try/catch` 或 `.catch()` 错误捕获
4. 使用 ES6 Module（`import/export`），一个文件只导出一个主要功能

## 组件化开发

### 目录结构

```
src/
├── assets/          # 静态资源
├── common/          # 公共常量
├── components/      # 项目级组件
├── hooks/           # 自定义 hook
├── layout/          # 布局组件
├── pages/           # 路由页面（KebabCase 目录）
│   └── user-list/
│       └── components/  # 页面级组件（PascalCase 目录）
├── store/           # 状态管理
├── utils/           # 通用工具
└── main.tsx         # 应用入口
```

### 组件设计要点

- Props 使用 TypeScript 定义类型，提供默认值
- 简单状态用组件内 `useState`/`ref`；复杂状态用 Context/Redux/Pinia
- 避免在渲染函数中定义新函数（使用 `useCallback`/`computed`）
- 复杂计算用 `useMemo`/`computed` 缓存

## 性能优化

- 脚本使用 `async` 或 `defer`
- 图片懒加载：`<img loading="lazy">`
- 路由级动态导入：`const Home = lazy(() => import('./Home'))`
- 文件名哈希：`app.[contenthash].js`

## 工程化配置

### 代码格式化

ESLint + Prettier 联合配置：
```json
{
  "extends": ["airbnb", "prettier"],
  "plugins": ["prettier"],
  "rules": { "prettier/prettier": "error" }
}
```

### Git 提交规范

Conventional Commits 格式：
```
feat: 添加用户登录功能
fix: 修复首页样式错位
docs: 更新 README 文档
```

### 提交前校验

Husky + lint-staged 自动检查：
```json
"lint-staged": {
  "*.{js,jsx,ts,tsx,vue}": ["eslint --fix", "prettier --write"]
}
```

## 安全与可访问性

- 避免 `innerHTML`，使用 `textContent`；富文本用 DOMPurify 过滤
- 交互元素添加 `aria-*` 属性，禁用状态设 `aria-disabled="true"`

## 检查清单

代码审查或提交前逐项检查：

- [ ] HTML 使用语义化标签，`<img>` 有 `alt`
- [ ] CSS 无 `!important`，嵌套 ≤ 3 层，属性顺序正确
- [ ] JS 无 `var`，异步有错误捕获
- [ ] 命名符合约定表（文件夹 KebabCase / 组件 PascalCase / 常量 UPPER_SNAKE_CASE）
- [ ] 组件 Props 有 TypeScript 类型定义和默认值
- [ ] 无在渲染函数中定义新函数
- [ ] 提交信息符合 Conventional Commits 格式
