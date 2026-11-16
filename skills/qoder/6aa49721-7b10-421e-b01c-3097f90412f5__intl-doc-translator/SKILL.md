---
name: intl-doc-translator
description: |
  Translate product documentation content into all required international site languages. 
  Use when the user provides content and asks to translate for international site (国际站) 
  product documentation updates, or says 国际站翻译/多语言翻译/文档翻译/translate documentation/
  multi-language translation/international site translation.
metadata:
  short-description: 国际站产品文档多语言翻译 | Multi-language translation for international product docs
---

# 国际站产品文档多语言翻译

将产品文档内容翻译成国际站所需的所有目标语言，确保术语一致性、格式完整性和语言专业性。

## 触发场景

当用户提出以下请求时触发：

**中文关键词**：
- "国际站翻译"、"多语言翻译"、"文档翻译"、"翻译文档"
- "翻译成多种语言"、"国际站文档更新"
- 用户提供内容并说明是国际站产品文档

**英文关键词**：
- "translate documentation"、"multi-language translation"
- "international site translation"、"translate to multiple languages"
- "localize documentation"

## 目标语言列表

按以下语言顺序翻译，每种语言使用对应的语言代码标注：

| 序号 | 语言 | 代码 |
|------|------|------|
| 1 | 英语 (English) | en |
| 2 | 葡萄牙语 - 巴西 (Português do Brasil) | pt-BR |
| 3 | 简体中文 | zh-CN |
| 4 | 繁体中文 | zh-TW |
| 5 | 日语 (日本語) | ja |
| 6 | 土耳其语 (Türkçe) | tr |
| 7 | 法语 (Français) | fr |
| 8 | 德语 (Deutsch) | de |
| 9 | 印尼语 (Bahasa Indonesia) | id |
| 10 | 西班牙语 (Español) | es |
| 11 | 越南语 (Tiếng Việt) | vi |
| 12 | 韩语 (한국어) | ko |
| 13 | 泰语 (ภาษาไทย) | th |

## 翻译工作流

### 步骤 1：确认翻译范围

1. 接收用户提供的待翻译文本
2. 确认内容类型（产品文档、API 文档、用户指南等）
3. 确认目标语言（默认全部 13 种，或按用户指定）
4. 如内容超过 2000 字，告知用户将分批翻译

### 步骤 2：术语识别与预处理

1. 识别并记录以下术语（翻译时保持一致）：
   - 产品名称（如 SLS、阿里云等）
   - 技术术语（如 Logstore、Project 等）
   - 品牌名称
2. 检查是否有官方译名表，如有则优先使用

### 步骤 3：逐语言翻译

按目标语言列表顺序逐一翻译，每种语言输出格式：

```markdown
## [语言名称] (代码)

翻译后的内容...
```

### 步骤 4：格式保持

翻译时严格保留：
- Markdown 格式（标题层级、列表、表格）
- 代码块及代码内容（不翻译代码）
- 链接结构（URL 不变，链接文本可翻译）
- 图片引用（alt 文本可翻译）
- 特殊符号和标记

### 步骤 5：质量验证

完成翻译后，执行以下检查：

1. **完整性检查**：确认所有目标语言都已翻译，无遗漏
2. **格式检查**：对比原文，确认格式结构一致
3. **术语一致性**：检查同一术语在各语言版本中是否一致
4. **长度合理性**：各语言版本长度应与原文相当（±30%）

如发现以下问题，主动告知用户：
- 某语言翻译后长度异常（过短或过长）
- 发现无法确定译法的术语
- 原文中有歧义或模糊表述

## 翻译原则

### 语言风格

- **官方书面风格**：使用正式、专业的书面语言，避免口语化、随意化表达
- **准确严谨**：准确传达原文含义，不遗漏、不曲解任何信息
- **符合目标语言习惯**：遵循各语言的官方文档写作规范和表达习惯
- **术语一致性**：技术术语、产品名称、品牌名保持一致，使用官方译名或保留原文

### 具体要求

- 使用正式的书面语体，避免口语、语、网络用语
- 句子结构完整、逻辑清晰，符合官方文档的严谨性要求
- 技术术语在各语言版本中保持一致性
- 保留原文的格式结构（标题层级、列表、代码块、链接等）
- 产品名称和品牌名不翻译，除非有官方译名
- 如原文中有不确定如何翻译的术语，标注并询问用户

## 输出示例

```markdown
## 英语 (en)

# Product Overview

This product provides...

## 葡萄牙语 - 巴西 (pt-BR)

# Visão Geral do Produto

Este produto fornece...

## 简体中文 (zh-CN)

# 产品概述

本产品提供...
```

## 注意事项

- 如果用户只要求翻译部分语言，按用户指定的语言翻译
- 如果内容很长（超过 2000 字），分批翻译并告知用户进度（如"已完成 5/13 种语言"）
- 翻译完成后，询问用户是否需要调整任何语言的译文
- 如用户提供了术语表或风格指南，优先遵循用户要求
- 代码块中的内容不翻译，仅翻译注释（如用户要求）

## 验证方式

翻译完成后，向用户确认：

1. 已翻译的语言数量
2. 是否有术语需要调整
3. 是否需要重新翻译某个语言版本
4. 是否需要导出为特定格式（如 Markdown 文件、Excel 对照表等）
