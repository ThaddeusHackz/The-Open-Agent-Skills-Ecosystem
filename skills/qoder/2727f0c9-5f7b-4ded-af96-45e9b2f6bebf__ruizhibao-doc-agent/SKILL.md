---
name: ruizhibao-doc-agent
description: 睿知宝（RaaS Knowledge Buddy，RKB）文档工程维护。当用户需要初始化 RKB 文档工程、编写 MDX 或 docs.json、维护导航和资源、校验、预览、发布，或操作 RKB CLI 与文档发布分支时使用，无需显式指定 Skill 名称。按需启用 iCMS 内容迁移、帮助中心交付和多空间共享仓库模块。
---

# 睿知宝文档工程

默认服务原生 RKB 文档写作。先确定交付目标，再读取对应模块；组件和 CLI 标准随本 Skill 静态分发，不在使用时拉取内部源码或自动更新知识。

## 开始任务

1. 读取目标仓库的 `AGENTS.md`，确认请求是分析、修改、准备提交还是发布；权限不相互包含。
2. 从当前 Git worktree 和 origin 确定仓库，不使用本地检出目录名推断产品、环境或文档空间。
3. 运行 `bin/ruizhibao-doc-agent project discover --repo <repo>`。以实际 `docs.json` 所在目录作为内容根；单空间也不能假设内容在仓库根，允许任意深度。嵌套根必须明确选择。
4. 读取仓库的 `.ruizhibao-doc-agent.json`（可选）；缺失表示原生写作，并从各 docs.json 的 language 自动推导中英文同步责任范围。模块选择及字段见 [项目配置](references/project-policy.md)。不凭 cn/intl 目录自动启用帮助中心或共享仓库。
5. 按当前阶段只读运行 `doctor --task native|rkb|history|publish|migration`：本地写作与静态门禁用 `native`，RKB 校验/本地 dev 用 `rkb`，仅查询发布历史用 `history`，预览 Pipeline/正式发布用 `publish`，iCMS 迁移用 `migration`。首次初始化用 `project init` 预览。工具缺失时按 [依赖](references/dependencies.md)处理，安装/升级必须有相应授权。

iCMS 迁移采用显式站点内容根：中国站和国际站分别绑定自己的根，同站点各语言共享该根。目录名及父级层级由产品配置，不固定为 `cn/intl`；与原生写作不同，迁移不把仓库根 `.` 作为站点根，两个站点根不能重合或互相嵌套。详细字段见迁移契约。

## 按任务读取

| 任务 | 必读内容 |
|---|---|
| 原生初始化、写作、导航、资源 | [平台模型](references/platform-model.md)、[写作](references/writing.md)、[组件标准](references/mdx-component-catalog.md) |
| 开发分支、合并基线、准备提交或推送 | [Git 生命周期](references/git-branch-lifecycle.md) |
| 格式/链接检查、预览或发布 | [交付](references/validate-and-release.md)、[RKB CLI](references/rkb-cli.md) |
| 帮助中心或双发 | 加读 [帮助中心交付](references/help-center.md) |
| 多空间共享仓库 | 加读 [共享仓库](references/shared-repository.md) |
| iCMS 导入 | 加读 [迁移流程](references/migrations/icms-to-ruizhibao/workflow.md)、契约、组件映射、样式映射；仅此模块依赖 icms-doc-agent |
| 能力入口检索 | [原子能力](references/atomic-capabilities.md) |
| 打包 Skill 或同步到写作仓库 | [分发与同步](references/distribution.md) |

## 默认执行原则

- 修改前刷新远端 master，使用短且有需求语义的任务分支，如 `fix/table-wrap`、`docs/sdk-options`。允许 worktree；不占用其他会话的分支。提交和推送前再次刷新并合并最新基线，冲突先处理。
- 以 MDX 相对内容根的真实路径确定 slug。导航决定展示组织，不得顺手改变存量 path、slug 或文件，以免导航调整破坏已有访问地址和入链。files-only 正文可直接访问，无须强制入导航。
- 原生组件按静态组件契约使用，帮助中心交付另取其支持子集；迁移保守转换规则不反向限制原生写作，也不因原生能力更多而自动改变迁移表达。
- Card、数学公式仍处于待发布状态，不能用于新交付；`{#id}` 自定义标题语法不受支持，采用标题旁 `<span id="anchor"></span>`。普通文本的字面美元符写成 `\$`，代码中的美元符保持原样。
- 只检查本轮文件及依赖，变更锚点检查入链；新增/删除/路由/导航调整执行全局路由和目录一致性检查。验证范围随影响范围扩大，避免局部校验漏掉全局路由冲突，也避免小改动触发无关的全量重编译。明确要求完整审计时用 `repository-guard --full`。
- 默认根据仓库全部有效 `docs.json` 和 `navigation.languages` 推导各站点已配置的中英文版本，同一逻辑文档跨站点同步维护；不是只检查本次选中的内容根。缺少同步变体时阻断，缩小范围或按站点分支维护须有 KE 显式确认。同步写作不代表同时发布，共享仓库仍禁止关联空间并发发布。
- 查询、预检不授权 commit/push/preview/publish，因为查看候选结果不等于同意写入远端或改变线上内容。准备提交只做检查并展示文件、敏感信息检查结果及拟定提交信息；等待最终授权。预览与正式发布分别授权，一次发一个空间。
- 发布前查询关联空间活动任务并重新核验目标。已确认的共享仓库发布到非 origin 推导空间时，使用封装内的临时 RKB API 适配器，不要求新用户修改 origin 或全局空间。适配器不兼容、配置未确认、历史查询失败或状态未知时停止，不能换目标绕过门禁。适用版本与退出条件见 [RKB CLI](references/rkb-cli.md)。
- 帮助中心交付、多空间共享均需研发侧配置，可联系技术支持。iCMS 切换帮助中心前，必须确认帮助中心已阻断消费 iCMS 发布；不能将 iCMS 仍可发布等同于帮助中心仍应消费。
- 暂存与报告写入调用方 Git 忽略的 `.ruizhibao-doc-agent/<task>/`，或显式 `RUIZHIBAO_DOC_WORKDIR`。产品迁移 target、专用适配器、快照和历史决策由使用方维护，不进入本分发包。
- 不把凭证、个人路径、真实人员样例、内部研发文档或实现仓库复制进 Skill。默认安装目录为 `~/.agents/skills`。

## 维护与验证

代码块首尾留白规范见写作参考；`repository-guard` 通过 `codeBlockWhitespaceAnomalies` 检查本轮 MDX，不自动清洗有语义的空白。

维护本 Skill 时读取 skill-creator。新增规则必须同时更新说明、执行能力与代表性测试；保持平台原子能力、可选模块和产品配置分离。维护者可依据受权访问的实现提取静态标准，分发包不依赖内部源码、Git 拉取或自动更新服务。

```bash
python3 -m unittest discover -s <skill>/tests -p 'test_*.py'
<skill>/bin/ruizhibao-doc-agent doctor --task native
```

修改迁移转换器还运行 iCMS 的 round-trip、xref smoke、CLI safety 测试；结果只写所属工作区。对真实平台验证限于本次授权范围，不为测试发起发布。
