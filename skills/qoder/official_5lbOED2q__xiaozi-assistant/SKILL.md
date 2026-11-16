---
name: xiaozi-assistant
displayName: 虾子能力增强包
description: AI助手能力增强模块集合 - 智能API网关+外挂大脑+记忆系统
version: 1.0.0
type: skill
tags: [openclaw, ai-assistant, api-gateway, memory, automation]
author: xiaozi
---

# 🦐 虾子能力增强包

AI 助手能力增强模块集合，让你的 AI 助手拥有智能路由、外挂大脑、增强记忆等能力。

## 功能特性

### 1. 智能 API 网关
- 支持 11+ API / 93+ 模型
- 自动故障转移
- 任务类型路由

### 2. 外挂大脑管理器
- 多外部 AI 统一调用
- GPT-5 / Opus / Kimi 随意切换
- 按任务类型自动选择

### 3. 三层记忆系统
- L1: 工作记忆 (当前会话)
- L2: 短期记忆 (daily notes)
- L3: 长期记忆 (MEMORY.md)

### 4. HTTP 重试增强
- 指数退避
- 熔断机制
- 超时控制

### 5. 浏览器自动化
- 重试机制
- 失败采集
- 条件等待

## 使用方法

```python
# 智能 API 网关
from mainz.tools.api_gateway import get_gateway

gw = get_gateway()
result = gw.chat([{"role": "user", "content": "你好"}])

# 指定任务类型
result = gw.chat(messages, task="coding")  # 编程
result = gw.chat(messages, task="reasoning")  # 推理
```

## 配置

在使用前，请替换代码中的 `YOUR_API_KEY` 为实际的 API Key。

## 依赖

- Python 3.10+
- requests
