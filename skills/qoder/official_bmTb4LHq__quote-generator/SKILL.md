---
name: quote-generator
description: 一个简单技能，用于向智能体响应、报告或日志中注入励志或技术性引语。适用于“个性”注入和打破机械式的单调感。
---

# Quote Generator

**Version:** 1.0.0
**Author:** OpenClaw Evolution (Cycle #2597)

## Description
A simple skill to inject inspirational or technical quotes into agent responses, reports, or logs. 
Useful for "personality" injection and breaking up robotic monotony.

## Usage

### Get a random quote (text)
```bash
node skills/quote-generator/index.js
```

### Get a random quote (json)
```bash
node skills/quote-generator/index.js --format json
```

### Write to file
```bash
node skills/quote-generator/index.js --output /tmp/quote.txt
```
