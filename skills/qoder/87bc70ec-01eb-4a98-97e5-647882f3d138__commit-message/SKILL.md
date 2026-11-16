---
name: commit-message
description: 检测项目 git hooks 环境并配置四钩子工作流，通过 qodercli AI 生成 Conventional Commits 提交信息并提交。当用户说"commit"、"提交"、"commit init"、"commit update"时使用。
---

# commit-message

`init` 模式配置环境，`update` 模式同步脚本更新，默认模式日常提交。全程静默，仅输出最终结果。详细规则见 [reference/REFERENCE.md](reference/REFERENCE.md)，init 规则见 [reference/INIT.md](reference/INIT.md)，update 规则见 [reference/UPDATE.md](reference/UPDATE.md)。

## 使用方式

| 场景 | 命令 | 流程 |
|------|------|------|
| Qoder IDE 聊天框 | `/commit-message` | skill 全自动：分析 diff → 生成 message → 写 CHANGELOG → 提交 |
| 终端 | `git commit` | hook 自动：AI 生成 message → 编辑器确认 → 写 CHANGELOG → 校验 → 提交 |

两条路径都会自动写 CHANGELOG.md（由 post-commit 钩子并入提交），push 时 pre-push 钩子检查所有待推送 commit。

## 四钩子工作流

```
git add → git commit → prepare-commit-msg(AI生成+写CHANGELOG) → 编辑器确认 → commit-msg(校验) → 提交 → post-commit(CHANGELOG并入提交)
git push → pre-push(检查所有待推送commit) → 全部合格则推送
```

## init 模式（环境配置）

首次使用执行 `/commit-message init`，检测框架、安装依赖、配置四钩子、激活钩子（`npx husky install`）、验证 `core.hooksPath`（若有 prettier 则创建 `.prettierignore`），详细流程读 [reference/INIT.md](reference/INIT.md) 执行。

## update 模式（同步更新）

skill 脚本有更新后，把主本同步到已 init 的项目，并验证钩子环境（`core.hooksPath`、shebang、若有 prettier 则检查 `.prettierignore`），详细流程读 [reference/UPDATE.md](reference/UPDATE.md) 执行。

## 日常提交模式（默认）

1. 运行 `python scripts/generate_commit.py` 收集改动（回退：`git diff --cached --stat` + `git diff --cached -U0`）。暂存区为空直接终止。
2. 分析 diff，提炼所有改动点，确定 type/scope，生成信息。单一改动点只写 subject，多改动点加 body 逐条列出。
3. 写 `CHANGELOG.md`（规则见 [reference/CHANGELOG_RULE.md](reference/CHANGELOG_RULE.md)）→ `git add CHANGELOG.md`
4. `SKIP_AI_COMMIT=1 git commit -m "<message>"`（skill 已生成 message，跳过 hook 的 AI 生成，commit-msg 校验仍生效）

最终输出：
```
提交完成

<type>(<scope>): <subject>

提交了 N 个文件：
- <文件路径> — <改动说明>
```

如有误用 `git commit --amend`。

## 规则

- type：feat/fix/refactor/style/chore/docs/perf/test/ci/build，多类型取主要类型
- subject：中文，不超过 50 字，不加句号
- scope：从文件路径取模块名，跨模块省略
- 单一改动点只写 subject 不加 body，多改动点加 body 逐条列出
- 暂存区为空直接终止
- 不遗漏改动点，按功能粒度组织
