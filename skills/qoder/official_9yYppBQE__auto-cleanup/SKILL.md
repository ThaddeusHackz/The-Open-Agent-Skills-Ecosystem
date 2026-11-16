---
name: auto-cleanup
description: 定期清理workspace下的临时文件，保持环境整洁
---

# auto-cleanup Skill

## 用途
定期清理workspace下生成的临时文件，保持环境整洁。

## 清理规则

### 保留（不删除）
- `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`, `IDENTITY.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`, `MEMORY.md` - 系统文件
- `memory/` - 记忆文件夹
- `skills/` - 技能文件夹
- `.git/` - Git配置
- `.openclaw/` - OpenClaw配置

### 清理（删除）
- `*.md` - 任务生成的markdown文件（除系统文件外）
- `openclaw-images/` - 图片缓存
- `*.json` - 临时JSON文件（除配置文件外）

## 使用方法

### 手动执行
```bash
# 清理7天前的临时文件
python3 /root/.openclaw/workspace/skills/auto-cleanup/cleanup.py --days 7

# 预览要清理的文件（不删除）
python3 /root/.openclaw/workspace/skills/auto-cleanup/cleanup.py --days 7 --dry-run
```

### 自动执行（定时任务）
每周日凌晨3点执行：
```bash
openclaw cron add --name "清理临时文件" --schedule "0 3 * * 0" --command "python3 /root/.openclaw/workspace/skills/auto-cleanup/cleanup.py --days 7"
```

## 注意事项
- 默认保留7天内的文件
- 执行前会预览要删除的文件
- 使用 --yes 参数直接执行不确认
