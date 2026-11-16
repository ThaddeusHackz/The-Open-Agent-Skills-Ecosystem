---
name: lark-shared
description: Install the lark-shared skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-shared
---

# lark-cli 共享规则

所有 `lark-*` skill 共享的底座：身份、认证、输出契约与高风险操作。

## 通用准则

-
调用前先确认用法：执行前读对应 reference 或跑 `--help`，别猜 flag 盲调。

-
身份决定你代表谁操作：`--as user` 代表用户本人（能看到、也能操作其日历、云空间/云盘/云存储等个人资源），`--as bot` 代表应用自己，应用级操作，只能访问bot自己的资源，bot 查用户资源会返回空成功而非报错。动手前先搞清楚身份`identity`。身份模型和权限管理 → [`lark-shared-identity-and-permissions.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-shared-identity-and-permissions.md)。

-
授权 / 配置类 URL 必须配二维码：当命令输出 `verification_url`、`verification_uri_complete`、`console_url` 等 URL 字段时，必须用 `lark-cli auth qrcode` 生成并在回复中展示，URL 在前二维码在后；优先生成 PNG（`--output`），仅当用户明确要求时才使用 ASCII（`--ascii`）。URL 原样转发——不编解码、不加标点、不重拼 query，二维码和链接请一起展示给用户。

-
`--format json`（默认）下，判断成功用 `ok == true`（或进程退出码 0），不要用 `code == 0`：成功信封没有顶层 `code` / `msg` 字段，`code` 只出现在错误信封的 `error` 内。按 OpenAPI 老格式 `{"code": 0, "msg": "ok"}`判断会把所有成功调用误判为失败——封装写入类命令时尤其危险。JSON 输出契约 → [`lark-shared-output-contract.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-shared-output-contract.md)。

## 安全规则

- 禁止输出密钥（appSecret、accessToken等）到终端明文。