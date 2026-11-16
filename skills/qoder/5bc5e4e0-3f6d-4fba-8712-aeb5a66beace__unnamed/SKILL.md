---
name: "workday-query"
description: "查询指定日期是否为工作日，支持具体日期（2025-01-01）和相对日期（本周五、下周一、今天、明天等）"
version: "2.0.0"
tags: ["workday", "holiday", "calendar", "bpm"]
triggers:
  - 用户想查询某天是不是工作日
  - 用户想查询节假日或调休信息
  - 用户询问本周五/下周一等相对日期的工作状态
---

# workday-query

查询指定日期是否为工作日，支持具体日期（2025-01-01）和相对日期（本周五、下周一、今天、明天等）

## When to use

- 用户想查询某天是不是工作日
- 用户想查询节假日或调休信息
- 用户询问本周五/下周一等相对日期的工作状态

## How to execute

This skill is **prompt-based**. Follow the instructions below to execute it directly.

### Prompt Instructions

你正在执行 workday-query（工作日查询）技能。请严格按照以下步骤操作：

**步骤 1：识别日期**
从用户输入中提取要查询的日期描述。支持以下格式：
- 具体日期：2025-01-01、2025/01/01、2025.01.01、2025年1月1日、2025.6.25
- 相对日期：今天、明天、昨天、后天、前天、大后天、大前天
- 周表达式：本周一、本周五、下周一、上周三、周日等
- 混合表达：用户可能说"2026.6.25是工作日吗？"，需从中提取日期部分

**步骤 2：转换为标准日期**
将识别到的日期描述转换为 yyyy-MM-dd 格式：
- 具体日期：直接格式化为 yyyy-MM-dd
- 相对日期：基于当前日期计算偏移量（今天=当前日期，明天=+1天，后天=+2天，昨天=-1天，前天=-2天，大后天=+3天，大前天=-3天）
- 周表达式：计算目标星期几对应的日期（本周X=本周的星期X，下周X=下周的星期X，上周X=上周的星期X；周一=1，周日=7）

**步骤 3：调用 MCP 工具**
调用 query_workdays 工具（MCP 服务器名：bpm-workday），参数：
- start_date：步骤 2 转换后的日期（yyyy-MM-dd 格式）
- end_date：与 start_date 相同（查询单日）

**步骤 4：解释返回结果**
MCP 工具返回 JSON 数据，包含 workdays 数组。取数组第一个元素的 flag 字段判断日期类型：
- flag = 1：工作日
- flag = 2：休息日
- flag = 3：节假日（如果返回中包含 holiday_name 字段，则一并展示节假日名称）

如果返回格式为 {"is_workday": true/false, "is_holiday": true/false}，则：
- is_holiday = true：节假日
- is_workday = true 且 is_holiday = false：工作日
- is_workday = false 且 is_holiday = false：休息日

**步骤 5：格式化回答**
用简洁的中文回答用户，参考格式：
"您查询的日期是 **yyyy-MM-dd**（用户原始描述），该日为 **工作日/休息日/节假日（名称）**。"

注意：
- 如果用户输入中未包含明确日期，请反问用户提供具体日期
- 如果查询失败，请如实告知并建议重试
- 不要添加多余空行或换行符

### Required MCP Tools

| MCP Server | Transport | Endpoint | Tool | Parameters |
|------------|-----------|----------|------|------------|
| bpm-workday | streamable-http | https://mobile-bpm.vivo.xyz:9010/bpmformapi/v1/mcp | query_workdays | start_date, end_date |
