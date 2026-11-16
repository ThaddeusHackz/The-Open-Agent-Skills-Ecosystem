---
name: dataclaw-tools
displayName: DataClaw 工具集
version: 1.0.0
description: 将 OpenClaw 会话数据导出、匿名化并分享到 Hugging Face 的完整工具链。包含5个独立脚本，支持查看状态、发现项目、准备数据、导出JSONL、推送到Hugging Face全流程。
type: skill
tags: [dataclaw, data-export, huggingface, anonymization, openclaw, session-data, data-sharing]
triggers:
  - dataclaw
  - data export
  - huggingface
  - session data
  - 匿名化
  - 数据导出
  - 会话分享
author: Kimi Claw
license: MIT
---

# DataClaw 工具集

将 OpenClaw 会话数据导出、匿名化并分享到 Hugging Face 的完整工具链。

## 核心功能

| 功能 | 脚本 | 说明 |
|------|------|------|
| 查看状态 | `dataclaw-status` | 检查配置和系统状态 |
| 发现项目 | `dataclaw-discover` | 扫描本地 OpenClaw 项目 |
| 准备数据 | `dataclaw-prep` | 匿名化处理会话数据 |
| 导出 JSONL | `dataclaw-export` | 导出为训练数据格式 |
| 推送 HF | `dataclaw-push` | 上传到 Hugging Face |

## 适用场景

- 📊 将 OpenClaw 会话转换为训练数据集
- 🔒 匿名化敏感信息后分享数据
- 🤖 为模型训练准备对话数据
- 📁 备份和迁移会话历史

## 安装

```bash
openclawmp install skill/@dataclaw-tools
```

## 快速开始

### 1. 查看状态

```bash
dataclaw-status
```

### 2. 发现本地项目

```bash
# 发现所有项目
dataclaw-discover

# JSON 格式输出
dataclaw-discover --json
```

### 3. 导出数据

```bash
# 导出所有项目
dataclaw-export

# 指定输出路径
dataclaw-export -o ~/my_sessions.jsonl

# 导出特定项目
dataclaw-export --project openclaw
```

### 4. 推送到 Hugging Face

```bash
# 需要 Hugging Face 账号
dataclaw-push ~/my_sessions.jsonl --repo username/dataset-name
```

## 完整工作流

```bash
# 1. 检查状态
dataclaw-status

# 2. 发现项目
dataclaw-discover

# 3. 准备数据（匿名化）
dataclaw-prep

# 4. 导出
dataclaw-export -o ~/sessions.jsonl

# 5. 推送
dataclaw-push ~/sessions.jsonl --repo myusername/openclaw-sessions
```

## 配置

配置文件位置：`~/.config/dataclaw/config.json`

```json
{
  "source": "openclaw",
  "thresholds": {
    "maxSizeKB": 500,
    "maxLines": 300
  },
  "compression": {
    "keepMessages": 100,
    "createBackup": true
  }
}
```

## 依赖

- Python 3.8+
- dataclaw (`pip install dataclaw`)
- huggingface_hub (用于推送功能)

## 数据来源

基于 dataclaw 开源项目：https://github.com/peteromallet/dataclaw

## 许可证

MIT License
