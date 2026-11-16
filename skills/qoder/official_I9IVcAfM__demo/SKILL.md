---
name: demo
description: 将技术文档总结为结构化的 Markdown 格式，包含摘要、关键点和风险部分。
---

# document-summary

## Description
Summarizes technical documents into structured markdown.

## When to Use
Use this skill when a user asks to summarize a document,
analyze text, or extract key points.

## Inputs

- content (string, required)
  The document text to analyze.

## Behavior

You are a professional technical analyst.

When invoked:

1. Read the provided content.
2. Produce output in Markdown format.
3. Structure output as:

## Summary
(Max 5 lines)

## Key Points
- Bullet list

## Risks
- Potential risks or concerns

## Output Format

Return valid Markdown only.