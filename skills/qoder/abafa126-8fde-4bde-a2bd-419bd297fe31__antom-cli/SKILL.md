---
name: antom-cli
version: 0.1.0
description: >-
  Antom CLI Skill installs, verifies, authenticates, troubleshoots, and safely operates every capability exposed by the current installed Antom CLI from natural-language requests. Use when users ask to install, set up, log in to, troubleshoot, or execute any Antom CLI command or workflow. Do not use for SDK integration coding or general Antom product questions that do not require CLI installation or execution.
description_zh: >-
  Antom CLI Skill 根据用户的自然语言请求安装、验证、登录、排障并安全运行当前已安装 Antom CLI 暴露的全部能力。适用于用户要求安装、配置、登录、排障或执行任意 Antom CLI 命令与工作流。不适用于无需安装或执行 CLI 的 SDK 集成编码或一般 Antom 产品问答。
---

# Antom CLI Installer and Operator / Antom CLI 安装与执行助手

## English operating guide

Turn the user's request into a verified Antom CLI installation, authentication state, or command result. Do not stop at describing capabilities when the user asked to install or execute something.

Help-driven discovery is a preflight for using the full installed CLI, not a Help-only mode or a command allowlist. After Help verifies the current command path and parameters, execute the requested Basic, Antom, Resource, or other current/future command-group capability, subject only to the authorization and safety gates below.

Read the supporting references progressively:

- When Antom CLI is missing, broken, or being upgraded, read [Installation and login](references/installation-and-login.md).
- Before discovering or running any Antom command, read [Help-driven command execution](references/help-driven-usage.md).
- When the user asks what the Skill can do or requests examples, read [Usage examples](references/usage-examples.md).

For every operation:

1. Identify whether the user wants installation, authentication, capability discovery, a read-only query, or a state-changing action.
2. Check `command -v antom`. If installed, verify `antom version` and `antom --help`; do not reinstall unless explicitly requested.
3. Discover the exact command path and parameters from `antom --help`, then the matching group and leaf Help. When the shorter Help omits details, run the full Help for the discovered path—for example, `antom help report download-list` only after root Help confirms that path. Examples never override the installed version's Help.
4. Before API calls, verify the active identity with `antom whoami --json`. Do not switch profiles or add `--live` unless explicitly requested.
5. Use only user-provided or securely available business values. Never invent amounts, currencies, IDs, callback URLs, tokens, or example values.
6. Execute read-only operations when intent is clear. Before Live access or any state-changing action, show a redacted preview, run Help-supported dry-run when available, and obtain final confirmation immediately before execution.
7. Report the CLI path/version, environment, profile, redacted command, result, safe reference ID, and next step. State explicitly when no real business operation was executed.

Safety invariants:

- Never request or expose private keys, access tokens, full card numbers, CVV, or signatures in chat, commands, logs, or generated files.
- Never pipe an uninspected remote installer directly to a shell by default. Download, inspect, explain the target, and confirm before installation.
- Do not describe filesystem modification, change, or creation timestamps as the CLI installation time. Report an installation date only when an authoritative installer or package-manager record provides it.
- Never automatically retry a timed-out or unknown state-changing request. Query the original request state first and preserve its idempotency ID.
- A command shown in official documentation is an example, not proof that the installed CLI version or current merchant profile supports it. Verify with current Help and the actual response.

## 中文操作说明

把用户意图落实为可验证的 Antom CLI 安装、认证或命令执行结果。不要只介绍 CLI 能力；当用户要求安装或运行时，应实际推进到安装验证、登录或命令结果，除非缺少用户确认、必要业务参数或外部权限。

Help 驱动是为了动态发现并使用当前 CLI 的全部能力，不是“只查看 Help”的模式，也不是命令白名单。Help 确认真实命令路径和参数后，应继续执行用户要求的 Basic、Antom、Resource 以及当前或未来版本新增命令组能力，但仍须遵守下述授权与安全门禁。

## 必读参考

- CLI 未安装、安装异常或用户要求安装/升级时，读取 [安装与登录](references/installation-and-login.md)。
- 只要要查询能力或运行命令，就读取 [Help 驱动的命令执行](references/help-driven-usage.md)。
- 用户询问使用示例或需要展示典型场景时，读取 [双语使用示例](references/usage-examples.md)。

参考文件提供操作流程，不是固定命令清单。当前机器上的根 Help、逐层命令 Help 和完整 Help 是命令、参数与枚举的最终依据。例如，仅当根 Help 已确认 `report download-list` 路径后，才运行 `antom report download-list --help` 和 `antom help report download-list`。

## 工作流

### 1. 明确本次目标

判断用户要的是：

- 安装或验证 CLI
- 登录、切换身份或排查认证
- 查看当前版本支持什么
- 预览或执行一项 Antom 操作

如果用户只是询问说明，回答说明；如果用户要求安装或执行，不得停留在命令介绍。只询问会改变执行结果且无法从 Help、当前 Profile 或现有文件中获得的信息。

### 2. 检查并按需安装

先运行：

```bash
command -v antom
```

- 已找到：运行 `antom version --json`；若当前版本不支持 JSON，再运行 `antom version`。然后运行 `antom --help` 验证 CLI 可用。除非用户明确要求升级或重装，不要覆盖现有安装。
- 未找到：按 [安装与登录](references/installation-and-login.md) 执行官方安装流程。先查看安装器 Help/内容和安装目标，再经用户确认运行；安装后必须验证 `antom version` 与 `antom --help`。

不要把“给出安装链接”当成安装任务已完成。若被权限、网络、系统架构或 `PATH` 阻塞，应定位原因并给出已验证的下一条恢复命令。

### 3. 只用 Help 发现命令

执行任何 Antom 动作前，从根命令开始逐层读取 Help：

1. `antom --help`
2. 对根 Help 中匹配用户目标的候选命令组运行 `--help`，例如 `antom report --help`
3. 对候选组中匹配的叶子命令运行 `--help`，例如 `antom report download-list --help`
4. 若叶子 Help 省略可选参数、提示 `list all: antom help ...`，或用户需求涉及条件字段，再运行该路径的完整 Help，例如 `antom help report download-list`

`antom --map` 只能作为快速总览，不能替代逐级 Help。不得依据旧版本快照、记忆或示例名称发明命令、参数、枚举值或默认行为。Help 中找不到的命令，应说明已检查的当前版本和路径，不得模拟为 CLI 已支持。

### 4. 检查身份和环境

需要调用 Antom API 时运行：

```bash
antom whoami --json
```

若没有可用 Profile，先运行 `antom login --help`，再按该版本给出的登录方式帮助用户完成登录。除非用户明确要求，否则不切换 Profile、不添加 `--live`。始终在预览和结果中标明 Test/Live 与 Profile；标识符只在必要时脱敏展示。

### 5. 从 Help 组装请求

- 从完整 Help 提取 Usage、Required Parameters、条件必填字段、合法枚举、单位和示例。
- 只使用用户提供、现有安全文件包含或当前上下文能可靠确定的业务值；不得生成金额、币种、交易 ID、请求 ID、回跳地址或授权 Token。
- 复杂请求优先使用权限受限的临时 JSON 文件和 Help 中声明的 `--data-file`；不要把秘密放在命令行或日志中。
- Help 声明支持 `--dry-run` 时，变更命令先 dry-run。Help 未声明的选项不得添加。

### 6. 预览、确认并执行

只读查询在用户意图明确时可以直接执行。会创建、修改、撤销业务对象，移动资金，变更 Token/Vault/Profile，或访问 Live 的命令，在真实执行前必须：

1. 展示脱敏命令、环境、Profile、目标、金额/币种、请求 ID 和预期影响；
2. 展示 dry-run 结果（若当前 Help 支持）；
3. 取得紧邻执行的最终确认；
4. 参数未变化时只执行一次真实命令。

默认添加当前 Help 支持的 `--json`，交互式命令除外。以退出码判断命令成功与否；JSON/stdout 是业务数据，stderr 是诊断信息。不得因为输出看似合理而忽略非零退出码。

### 7. 交付可核验结果

返回简洁结果表：

| 字段 | 内容 |
|---|---|
| CLI | 路径和版本 |
| Environment | Test 或 Live |
| Profile | Profile 名称；必要时脱敏 |
| Operation | 实际安装、登录、查询或变更动作 |
| Command | 脱敏后的实际命令 |
| Result | Success、Pending、Failed、Unknown 或 Not executed |
| Reference ID | 可安全展示的请求/交易 ID |
| Next step | 无需操作，或一条已验证的恢复/查询命令 |

若只完成安装、Help 检查或 dry-run，明确写明“未发起真实业务调用”。

## 安全与恢复门禁

### 安装安全

- 只使用 [安装与登录](references/installation-and-login.md) 中的 Antom 官方文档和官方下载地址。
- 不默认把网络响应直接交给 shell 执行。优先下载到临时文件，检查脚本来源、内容和 Help，再展示目标路径并确认执行。
- 文件的修改、变更或创建时间不等于 CLI 安装时间；只有安装器或包管理器提供权威记录时才能报告安装日期。
- 安装到系统目录、修改 shell 启动文件或使用管理员权限前必须说明影响并确认。优先选择安装器 Help 支持的用户可写目录。
- 安装完成后重新解析实际二进制路径，防止旧版本或同名程序遮蔽新安装。

### 敏感数据

- 不要求用户在聊天中粘贴私钥、Access Token、完整卡号、CVV 或签名。
- 手工登录只接受私钥文件路径，不读取或回显私钥内容。
- 临时请求文件使用最小权限，完成后安全清理；最终结果与错误信息中的 Token、卡号、Client ID、商户号和签名必须脱敏。
- 原始生产卡数据不得经 Agent 对话或 CLI 参数处理。

### 幂等、超时与重试

- 保留原幂等请求 ID，不得为了重试擅自换新 ID。
- 变更调用出现超时、网络错误或未知状态时不得自动重发。先通过当前 Help 发现对应查询或诊断命令，并查询原请求状态。
- 只读网络请求最多自动重试一次；持续失败时返回退出码、脱敏错误类别和恢复建议。
- 认证或签名失败时停止业务调用，先通过 `antom login --help` 与 `antom whoami --json` 修复身份。
- 参数非法时重新读取该叶子命令的简短与完整 Help；例如对已确认的报表下载路径运行 `antom report download-list --help` 和 `antom help report download-list`，核对必填、枚举、金额最小单位与 JSON 层级。

## 能力边界

- 不绕过 CLI 直接拼装 Antom HTTP API 请求。
- 命令存在只证明当前 CLI 提供入口，不证明当前商户合同、地区、支付方式或 Profile 已开通；成功 API 响应才能证明可用。
- 不把浏览器回跳当成支付终态；使用当前 Help 提供的查询命令或异步通知确认。
