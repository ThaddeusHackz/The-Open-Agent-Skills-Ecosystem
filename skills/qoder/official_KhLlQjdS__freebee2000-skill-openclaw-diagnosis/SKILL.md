---
name: skill-openclaw-diagnosis
description: OpenClaw Gateway 自动化诊断与修复。当用户报告 OpenClaw 异常、Gateway 无法启动、启动很慢、进程崩溃、端口占用、或需要执行健康检查时使用。触发场景包括：(1) "Gateway 起不来"、"启动很慢"、"进程挂了"；(2) "OpenClaw 出错"、"openclaw 问题"；(3) 需要执行状态检查、日志查看、重启操作。
---

# OpenClaw 自动化诊断

## 诊断流程

遇到 OpenClaw 问题，按以下流程自动诊断：

```
1. 运行诊断脚本 → 2. 根据结果修复 → 3. 验证结果
```

### Step 1: 执行诊断

```bash
# 一键诊断（检查所有关键指标）
powershell -ExecutionPolicy Bypass -File <SKILL_PATH>\scripts\check_gateway_status.ps1
```

诊断项目：
- 进程状态（node 进程是否存在）
- 端口 18789（是否被占用、是否监听）
- 健康检查端点（Gateway 是否响应）
- Watchdog 计划任务（是否配置、运行状态）
- Bonjour/mDNS 配置（是否禁用）

### Step 2: 根据结果修复

| 诊断结果 | 执行脚本 |
|----------|----------|
| Bonjour 导致启动慢 | `disable_bonjour.ps1` |
| 进程未运行/崩溃 | `restart_gateway.ps1` |
| 端口被占用 | `restart_gateway.ps1 -Force` |
| 需要查看详细日志 | `check_gateway_logs.ps1 -Lines 100` |

### Step 3: 验证结果

修复后重新运行诊断脚本确认问题解决。

---

## 脚本索引

| 脚本 | 用途 |
|------|------|
| `check_gateway_status.ps1` | 一键诊断 Gateway 状态 |
| `check_gateway_logs.ps1` | 查看 Gateway 日志 |
| `restart_gateway.ps1` | 干净重启 Gateway |
| `disable_bonjour.ps1` | 禁用 Bonjour（解决启动慢） |

---

## 常见问题速查

### Gateway 启动很慢（>1分钟）
**根因**: Bonjour/mDNS 在 Windows 卡在 announcing 状态
**诊断**: 检查 `discovery.mdns.mode` 是否为 `off`
**修复**: `disable_bonjour.ps1`

### Gateway 无法访问
**诊断**: 检查端口 18789 和健康端点
**修复**: `restart_gateway.ps1`

### 端口 18789 被占用
**根因**: 旧 Gateway 实例未完全退出
**修复**: `restart_gateway.ps1 -Force`

### 进程似乎在运行但 UI 打不开
**诊断**: `check_gateway_logs.ps1` 查看最新错误
**常见错误**: `ERROR_ELEVATION_REQUIRED`（权限问题）、端口冲突

---

## 关键路径（需根据实际安装位置修改）

- Gateway 配置: `%USERPROFILE%\.openclaw\openclaw.json`
- Gateway 启动脚本: `%USERPROFILE%\.openclaw\gateway.cmd`
- Gateway 日志目录: `%USERPROFILE%\.openclaw\logs`
- Watchdog 计划任务: `OpenClawGatewayWatchdog`
