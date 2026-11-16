---
name: envato-comment-task-to-sheet
description: 本技能分析 ThemeForest / CodeCanyon 的评论，并将其转换为结构化的开发任务。它对评论类型进行分类，分配优先级，提取技术细节，并输出一个专为直接推送到 Google 表格而设计的 JSON 对象。
---

# Envato Comment → Task → Google Sheet

## Overview

This skill analyzes ThemeForest / CodeCanyon comments and converts them into structured development tasks.

It classifies the comment type, assigns priority, extracts technical details, and outputs a JSON object designed to be pushed directly into Google Sheets.

## Input Parameters

- product_name
- product_url
- product_type (wordpress_theme | html_template | code_script)
- comment_text
- comment_url (optional)
- customer_name (optional)

## Output

Structured JSON task object formatted for Google Sheets row insertion.

## Classification Types

- bug
- feature_request
- support_question
- update_required
- refund_risk
- positive_feedback

## Priority Rules

- Fatal error / site break → critical
- Refund mention → critical
- Broken feature → high
- Feature request → medium
- Question → low

## Use Case

- Automate support workflow
- Track product health
- Improve update planning
- Reduce missed issues