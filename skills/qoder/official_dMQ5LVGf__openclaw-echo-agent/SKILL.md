---
name: openclaw-echo-agent
description: EchoAgent 是一个与 OpenClaw 兼容的最小化技能，旨在作为构建和发布 OpenClaw 代理的参考示例。它接受文本输入，使用工具进行处理并返回确定性输出，设计供其他 OpenClaw 代理使用，可安全地嵌入多代理工作流中进行链式调用。
---

# EchoAgent

EchoAgent is a minimal OpenClaw-compatible skill.

## What it does
- Accepts text input
- Uses a tool to process it
- Returns deterministic output

## Use case
This skill is intended as a reference example for building
and publishing OpenClaw agents.

## Entry point
agent.py

## Interoperability

This skill is designed to be used by other OpenClaw agents.

### Input
- text (string)

### Output
- result (string)

This agent can be safely chained inside multi-agent workflows.
