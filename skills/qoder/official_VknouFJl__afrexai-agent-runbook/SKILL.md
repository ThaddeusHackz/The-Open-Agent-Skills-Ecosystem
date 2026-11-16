---
name: afrexai-agent-runbook
description: 为部署 AI 代理生成一份可直接投入生产使用的运维手册，涵盖部署前检查、分阶段发布流程（影子/监督/自主模式）、监控仪表盘、回滚程序、成本管理及事件响应模板。
---

# Agent Ops Runbook

Generate a production-ready operations runbook for deploying AI agents. Covers pre-deployment checklists, shadow mode → supervised → autonomous rollout stages, monitoring dashboards, rollback procedures, cost management, and incident response templates.

## When to Use
- Deploying an AI agent to production
- Building monitoring and alerting for agent systems
- Creating rollback procedures for autonomous workflows
- Estimating and controlling agent operational costs

## Instructions

When the user asks for an agent ops runbook or deployment plan:

1. Ask which agent function they're deploying (support, sales, document processing, etc.)
2. Ask about their risk tolerance (conservative, moderate, aggressive rollout)
3. Generate a complete runbook with:
   - Pre-deployment checklist specific to their function
   - 3-stage rollout plan with metrics and gates
   - Monitoring alerts (critical + warning thresholds)
   - Rollback procedures (3 levels: prompt, feature, full)
   - Cost estimates based on their expected volume
   - 90-day implementation timeline
   - Incident response template

4. Include specific metric targets:
   - Accuracy vs human baseline: >90%
   - Error rate: <2%
   - Cost per task benchmarks by function
   - Human escalation rate: 5-15%

5. Flag risks specific to their industry (compliance, PII, financial accuracy)

Output format: Markdown document ready to share with engineering and ops teams.
