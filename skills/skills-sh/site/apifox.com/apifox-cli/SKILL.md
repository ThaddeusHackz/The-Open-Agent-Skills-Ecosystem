---
name: apifox-cli
description: Install the apifox-cli skill for your AI agent. Published on apifox.com.
source: https://www.skills.sh/site/apifox.com/apifox-cli
---

# Apifox CLI

用 Apifox CLI 完成用户请求；不要凭记忆拼 payload，优先让 CLI 的 `--help`、`cli-schema`、`cli-schema validate`、`agentHints.nextSteps` 驱动下一步。

## 新会话检查

- 首次处理 Apifox CLI 任务时，先轻量确认 CLI 可用：`apifox --version`、`apifox --help`。

- 如果 `apifox` 不存在或无法输出版本，先安装 CLI：`npm i -g apifox-cli@latest --registry=https://registry.npmmirror.com/`。

- 安装后执行 `apifox login --with-token <TOKEN>` 登录。API 访问令牌可在 Apifox 客户端或网页端「用户头像 → 账号设置 → API 访问令牌」创建。

- 不要每次默认升级；只有命令返回版本过低/unknown command/参数缺失疑似旧版导致，或用户任务依赖新能力时，才建议升级。

## 基础用法

```
apifox --help
apifox  --help
apifox   --help
```