---
name: social-scheduler-pro
description: 优化发布计划以实现最大参与度，支持中国及国际主流社交平台。
---

# Social Media Scheduler

Optimize posting schedule for maximum engagement.

## Platforms

- **Chinese**: Douyin, Xiaohongshu, WeChat, Weibo, Kuaishou
- **International**: Instagram, Twitter, Facebook, LinkedIn

## Usage

```bash
npx social-scheduler
```

## API

```typescript
import { getSchedule } from 'social-scheduler';

const schedule = await getSchedule({
  platform: 'xiaohongshu',
  contentType: 'product-review',
  frequency: 'daily'
});
```
