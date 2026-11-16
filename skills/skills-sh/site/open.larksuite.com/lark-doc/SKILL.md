---
name: lark-doc
description: Install the lark-doc skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-doc
---

# docs

## 场景与 Shortcut 路由

CRITICAL：先判断场景，再读取该场景的参考文件；不要在任务开始时一次性读取全部参考文件。每个文件只在首次进入对应阶段时读取一次。

身份：文档操作推荐显式指定 `--as user`。

本地文件引用统一遵循文件访问权限：CWD 内优先使用 `@./相对路径`，其他目录使用 `@绝对路径`。XML 内的相对资源路径先查 CWD；仅文件不存在时再查源 XML 文件所在目录，同名文件以 CWD 为准。内联内容、stdin、在线文档没有源文件目录，不执行回退。

### 文档内容

- 读取 / 摘要 — [`+fetch`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-doc-fetch.md)：先读参考再获取文档。

- 从零创作 — [`创建工作流`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-doc-create-workflow.md)：先完整执行创建工作流，简单任务不是跳过的理由；

- 导入 / 空文档 — [`+create`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-doc-create.md)：仅创建空文档或原样导入用户提供的完整内容时，跳过创建工作流。

- 编辑 / block 直达链接 — [`+update`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/references/lark-doc-update.md)：语义改写、润色、重组、补写或排版均按 update 参考完成。

### 辅助能力