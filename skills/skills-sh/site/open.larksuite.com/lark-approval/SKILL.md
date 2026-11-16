---
name: lark-approval
description: Install the lark-approval skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-approval
---

CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../lark-shared/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md)，其中包含认证、权限处理

所有命令默认 `--as user`（审批是人的动作）。调用前先按需读取 references 下对应的文件，查参数结构，不要猜字段；references 是第一信息源，只有在 reference 未覆盖的原生 / 高级场景下，才额外用 `lark-cli ... --help`、`lark-cli schema` 等方式补充确认字段。

## 路由优先级（先判断是不是审批，再选命令）

审批待办不是飞书任务。只要用户的核心对象是审批单据 / 审批待办 / 审批实例，就优先使用 `lark-approval`，不要让渡给 `lark-task`。

### 明确归 `lark-approval` 的高优先级语义

出现以下任一语义时，优先走 `lark-approval`：

- 审批待办 / 审批单据 / 审批实例 / 审批意见 / 审批定义

- 同意 / 拒绝 / 转交 / 退回 / 撤回 / 催办 / 加签 / 抄送

- 待办列表 / 待办单据 / 已发起审批 / 已办审批 / 审批详情 / 同意可编辑

判定规则： 只要最终动作是对审批单据做同意、拒绝、转交、退回、撤回、催办、加签、抄送、查详情、查已发起/已办/待办，就归 `lark-approval`。只有当用户处理的是非审批类任务/待办时，才走 [`lark-task`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-task/SKILL.md)。