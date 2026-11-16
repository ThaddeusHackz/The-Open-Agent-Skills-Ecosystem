---
name: active-learner
description: 实现主动学习协议（R3）。允许代理将课程编程式地内化到 MEMORY.md 中，并生成结构化的“寻求帮助”请求。
---

# Active Learner

**Version:** 1.0.0
**Author:** OpenClaw Evolution (Cycle #2597)

## Description
Implements the Active Learning Protocol (R3). Allows the agent to programmatically internalize lessons into `MEMORY.md` and generate structured "ask for help" requests.

## Usage

### Internalize a Lesson
```bash
node skills/active-learner/index.js internalize --id "L1" --category "Protocol" --text "Lesson content here..."
```

### Ask for Help
```bash
node skills/active-learner/index.js ask --text "I don't understand X..."
```
