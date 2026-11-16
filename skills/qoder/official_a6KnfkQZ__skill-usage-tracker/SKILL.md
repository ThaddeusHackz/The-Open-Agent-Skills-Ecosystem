---
name: skill-usage-tracker
description: 自动追踪和审计技能使用情况，确保强制规则被执行。通过读取规则文件、检查回复规范、记录违规行为及生成每日报告来实现自动化管理。
---

# Skill Usage Tracker

## Purpose
自动追踪和审计 skill 使用情况，确保强制规则被执行。

## Integration
- 读取 SKILL_USAGE_RULES.md 获取强制规则
- 检查每次回复是否符合规范
- 记录违规到 skill_violations.log
- 生成每日使用报告

## Usage
无需手动调用，系统会自动在每次回复后执行检查。
