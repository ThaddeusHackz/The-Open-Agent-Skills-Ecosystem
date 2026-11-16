---
name: inline-js
description: 读取指定 JS 文件并压缩（minify），将压缩后的代码插入到当前打开文件的光标位置。当用户说"压缩插入"、"内联JS"、"inline JS"、"把XX压缩进来"时触发。
---

# 内联压缩 JS

读取目标 JS 文件 → terser 压缩 → 插入到当前文件光标位置。适用于 AutoJS6 `$remote` 单文件部署场景，将依赖模块内联到主脚本中。

## 触发方式

- `/inline-js <文件路径>`
- 用户说"压缩插入"、"内联 JS"、"inline JS"、"把 XX 压缩进来"

## 参数

- **文件路径**（必填）：要压缩的 JS 源文件路径，支持绝对路径或工作区相对路径
- **当前打开文件**：压缩结果插入的目标文件（即用户当前编辑的文件）

## 执行步骤

### 第 1 步：确认参数

1. 从用户输入中提取目标 JS 文件路径
2. 确认当前打开的文件（即插入目标）
3. 如果用户未提供文件路径，使用 AskUserQuestion 询问

### 第 2 步：压缩 JS 文件

使用 `npx terser` 压缩目标文件：

```powershell
npx terser --compress --no-mangle -- "<目标文件绝对路径>"
```

> 如果 npx 不可用或 terser 执行失败，使用以下 Node.js 内置方案作为降级：
>
> ```powershell
> node -e "const fs=require('fs');const code=fs.readFileSync('<目标文件绝对路径>','utf8');const minified=code.replace(/\/\/.*$/gm,'').replace(/\/\*[\s\S]*?\*\//g,'').replace(/\n\s*\n/g,'\n').replace(/^\s+/gm,'').trim();process.stdout.write(minified);"
> ```
>
> 这个降级方案只做基础压缩（去注释、去空行、去缩进），不如 terser 彻底，但不依赖额外包。

### 第 3 步：包装为 IIFE

将压缩后的代码包裹在立即执行函数表达式（IIFE）中，避免污染全局作用域：

```javascript
// === 内联自: <原始文件名> (已压缩) ===
(function(){
<压缩后的代码>
})();
// === 内联结束: <原始文件名> ===
```

> **注意**：如果目标文件使用 `exports.xxx = ...` 导出，改用以下包装方式，将 exports 映射到全局：
>
> ```javascript
> // === 内联自: <原始文件名> (已压缩) ===
> (function(){
> var exports = {};
> <压缩后的代码>
> Object.assign(global, exports);
> })();
> // === 内联结束: <原始文件名> ===
> ```
>
> 判断方法：如果目标文件中包含 `exports.` 或 `module.exports`，使用 exports 包装方式。

### 第 4 步：插入到光标位置

1. 读取当前打开的文件内容
2. 在光标所在位置插入包装后的压缩代码
3. 使用 SearchReplace 工具，以光标附近的文本作为锚点完成插入

> 如果无法精确定位光标，将代码插入文件开头（第 1 行之前）。

## 示例

用户输入：`/inline-js utils.js`

执行流程：
1. 读取 `utils.js`，确认当前打开文件为 `test.js`
2. `npx terser --compress --no-mangle -o ".tmp_min.js" -- "utils.js"` → 输出到临时文件
3. Node.js 脚本检测 exports → IIFE 包装 → 拼接到 `test.js` 开头（或替换已有内联块）
4. 删除 `.tmp_min.js` 临时文件

## 注意事项

- 压缩后的代码可读性极低，仅用于部署场景，不要用于源码管理
- 如果目标文件非常大（如 utils.js 2900+ 行），压缩后仍可能有数千行，提醒用户确认是否继续
- 同一文件不要重复内联，插入前检查是否已存在相同来源的内联块
