---
name: lark-markdown
description: Install the lark-markdown skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-markdown
---

# markdown (v1)

CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md)，其中包含认证、权限处理

## 快速决策

-
身份：Markdown 文件通常属于用户云空间资源，优先使用 `--as user`。如为自动化场景，或应用已创建并持有目标文件权限，可按场景使用 `--as bot`。首次以 `user` 身份访问前执行 `lark-cli auth login`

-
`markdown +create` / `+overwrite` 失败时，先判断是不是身份和权限问题：`bot` 更常见的是 app scope 或目标目录 ACL，`user` 更常见的是用户授权或用户 ACL；不要不加判断地来回切身份重试。

-
用户要上传、创建一个原生 `.md` 文件，使用 `lark-cli markdown +create`

-
用户要比较原生 `.md` 文件的历史版本差异，或比较远端 Markdown 与本地草稿，使用 `lark-cli markdown +diff`

-
用户要读取 Drive 里某个 `.md` 文件内容，使用 `lark-cli markdown +fetch`

-
用户要对 Markdown 文件做局部文本替换 / 正则替换，优先使用 `lark-cli markdown +patch`

-
用户要覆盖更新 Drive 里某个 `.md` 文件内容，使用 `lark-cli markdown +overwrite`

-
用户要先拿 Markdown 文件的历史版本号，再做比较/下载/回滚，先用 [`lark-drive`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-drive/SKILL.md) 的 `lark-cli drive +version-history`

-
用户要把本地 Markdown 导入成在线新版文档（docx），不要用本 skill，改用 [`lark-drive`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-drive/SKILL.md) 的 `lark-cli drive +import --type docx`

-
用户要对 Markdown 文件做rename / move / delete / 搜索 / 权限 / 评论等云空间（云盘/云存储）操作，不要留在本 skill，切到 [`lark-drive`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-drive/SKILL.md)

-
`markdown +create` / `+overwrite` 命中 `missing scope`、`permission denied`、`not found`、`quota_exceeded`、`version limit` 时，默认停止重试并按报错 hint 处理；只有 `rate_limit`、`server_error` 或临时网络错误才做有限退避重试。

-
`markdown +create` 的目标参数不要猜：Drive 文件夹用 `--folder-token`，Wiki 节点用 `--wiki-token`。如果用户给的是 URL，可以直接传完整 URL；CLI 会归一成 token。不要把 doc/sheet/wiki URL 放进 `--folder-token` 试错。