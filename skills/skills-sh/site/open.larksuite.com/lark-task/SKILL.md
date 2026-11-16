---
name: lark-task
description: Install the lark-task skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-task
---

# task (v2)

CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md)，其中包含认证、权限处理

## 命令选择与渐进式发现（必读）

执行任何 Task 命令前，必须先确认能力真实存在，禁止根据用户意图自行拼接或猜测 `+<verb>`：

- 先将用户意图与下方 Shortcut 表精确匹配。只有表中明确列出的 shortcut 才可直接选择；参数不确定时读取对应 reference 或运行该 shortcut 的 `--help`。

- 没有精确匹配、或无法确认当前版本是否支持时，先运行 `lark-cli task --help`，以当前 CLI 输出的命令列表为准。

- help 中存在匹配 shortcut 时，使用 help 列出的完整 shortcut token（例如 `+create`）运行 `lark-cli task <shortcut> --help`，再按真实 flag 执行。

- help 中没有匹配 shortcut 时，不得尝试相似的 `+<verb>`；从 help 中选择原生 resource，运行 `lark-cli task <resource> --help` 确认 method，再运行 `lark-cli schema task.<resource>.<method>` 获取参数结构，最后调用 `lark-cli task <resource> <method> ...`。

- 遇到 `unknown_subcommand` 时必须停止猜测或尝试变体，回到第 2 步重新发现能力。

shortcut 名称只能来自本 Skill 的 Shortcut 表或 `lark-cli task --help`；原生 resource/method 以逐级 help 为准，参数名、类型和嵌套结构以 method schema 为准。