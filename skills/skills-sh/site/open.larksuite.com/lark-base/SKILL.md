---
name: lark-base
description: Install the lark-base skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-base
---

# Base

普通 Base 是数据容器，由一棵 Base Block 资源树和 Base 级配置组成。`folder`、`table`、`docx`、`dashboard`、`workflow` 都是 Block 类型；Advanced Permission / Role 是 Base 级配置，不属于 Block。Table 是其中承载业务数据的核心 Block。Workspace 是组织 Base 与 BaseApp 的外层容器；BaseApp（AppMode）通过 Page 和组件组织 Base 数据，不是 Base 的别名。

## 身份选择（优先）

操作 Base 优先使用 `--as user`；用户明确要求应用身份时使用 `--as bot`。权限失败按 `lark-shared` 以原身份修复 scope 或资源 ACL；只有用户明确同意更换操作者时才切换身份。

## 进入前必做：解析目标实体

开始操作前先确定 `base_token` 和目标实体类型；上下文已提供 `<bitable>` / `<base_refer>` 标签及资源 ID 时直接使用。其余情况按意图选择入口：

- URL 或分享链接： `lark-cli base +url-resolve --url '<url>' --as user`。Base URL 根据返回的 `resource_type` / `block_type` 及 `table_id`、`view_id`、`record_id`、`dashboard_id`、`workflow_id`、`docx_token`、`share_token` 等坐标进入对应模块；BaseApp `/app/` URL 返回 `app_token`，并在链接携带时返回 `workspace_token` 和 `page_id`。实体类型以解析结果为准。

- Base 标题或关键词： `lark-cli base +title-resolve --title '<keyword>' --as user`。单一结果直接取得 `base_token`；多个候选结合标题、所有者和更新时间消歧，仍无法唯一确定时请用户选择。随后按下方 Base Block 资源模型定位目标实体。

- 已有 Base 候选列表： 用户要列出已有 Base 候选，且需要按最近访问、owner、创建人、时间、类型等维度筛选/排序时，转 `lark-cli drive +search --doc-types bitable --as user`。按标题/关键词定位单个 Base 仍用 `+title-resolve`。常见候选列表命令：

- 最近访问：`lark-cli drive +search --doc-types bitable --sort open_time --opened-since 3m --page-size 20 --as user`

- 只列我拥有的：加 `--mine`；如果要列“我创建的”，用 `--created-by-me`。

- 从候选项拿到 URL 或 token 后，再用 `+url-resolve` 或 `+base-get` 进入 Base 业务命令。

- BaseApp： 优先使用真实 `/app/` URL；已有 `workspace_token` 时可用 `+workspace-entity-list --type baseapp` 定位。两者都没有时请用户补充应用链接或 Workspace，不按名称全局猜测 `app_token`。