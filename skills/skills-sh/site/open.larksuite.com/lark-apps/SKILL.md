---
name: lark-apps
description: Install the lark-apps skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-apps
---

# apps (v1)

妙搭应用属于用户资产。默认用 `--as user`；认证、scope、exit-10、高风险确认、`_notice` 等通用处理只读 [`../lark-shared/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md)，不要在本 skill 里复制。妙搭应用有两条开发路径：本地开发（拉源码本地写）/ 云端会话（妙搭 AI 生成）。

## 身份与授权

妙搭应用是用户的个人资产，统一 `--as user`（见开头）。已有用户身份可用时直接执行业务命令，不要为了预防权限问题主动重新登录，否则可能中断原任务并触发不必要的设备授权。仅当 CLI 明确返回未登录或缺少本域 scope 时，一次性执行：

```
lark-cli auth login --domain apps
```

因缺权限失败（`error.subtype == "missing_scope"`）时的通用处理见 [`../lark-shared/SKILL.md`](https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md)，同样按 `--domain apps` 授权；授权成功后只恢复原业务操作，不扩展任务范围。

## 意图路由

按具体操作查命令（开发路径先用下方「选择开发路径」判定表定好再进来取命令）：