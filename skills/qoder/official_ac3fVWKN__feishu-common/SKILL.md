---
name: feishu-common
description: 为 OpenClaw Feishu skills 提供的共享飞书认证和 API 辅助工具，包含租户令牌获取与缓存、重试与超时处理、带令牌刷新功能的已认证请求封装。
---

# feishu-common Skill

## Description
Shared Feishu authentication and API helper for OpenClaw Feishu skills.

Provides:
- Tenant token acquisition and cache
- Retry and timeout handling
- Authenticated request wrapper with token refresh

## Install Requirement
Install this skill before installing or running dependent Feishu skills.

## Usage
Dependent skills should import from `feishu-common`:

```javascript
const { getToken, fetchWithRetry, fetchWithAuth } = require("../feishu-common/index.js");
```

Compatibility alias is also available:

```javascript
const { getToken, fetchWithAuth } = require("../feishu-common/feishu-client.js");
```

## Files
- `index.js`: Main implementation.
- `feishu-client.js`: Compatibility alias to `index.js`.
