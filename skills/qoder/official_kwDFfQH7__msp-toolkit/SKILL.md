---
name: msp-toolkit
description: IT 多租户服务提供商工作流的核心工具，涵盖 Azure/M365 审计、NPU 监控及健康检查功能。
---

# MSP Toolkit Skill

description: Essential tools for IT MSP workflows – Azure/M365 audits, NPU monitoring, health checks.

metadata: {"clawdbot":{"emoji":"🔧","os":["linux"]}}

## Core Functions
- msp-dashboard.py: Daily Azure/M365 status.
- healthcheck: Firewall/SSH/update audits.
- nuc-reset.sh: NPU reboot script.

## Setup
npm install clawhub
clawhub publish /home/cc/.openclaw/workspace/skills/msp-toolkit