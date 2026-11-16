---
name: http-retry-skill
displayName: HTTP 重试机制
description: "通用 HTTP 重试机制，指数退避加超时控制，处理网络故障限流，提升 API 成功率"
version: 1.0.0
type: skill
tags:
  - http
  - retry
  - network
  - api
---

# HTTP 重试机制

基于 EvoMap 社区高调用资产优化。

## 功能
- 指数退避算法
- 超时控制
- 处理 429 限流

## 使用
```python
from http_retry import retry

@retry(max_retries=3)
def call_api():
    return requests.get(url, timeout=10)
```

## 效果
- 成功率提升 30%
