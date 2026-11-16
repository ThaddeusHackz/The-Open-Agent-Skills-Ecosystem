---
name: git-ops
description: "Git 操作助手 — 提交代码、推送/拉取代码、新建/切换分支、合并/变基/摘樱桃、撤销修改/硬重置/强制推送、查看状态/差异/日志、暂存管理、标签管理。当用户需要执行任何 git 命令或进行版本控制操作时触发。"
---

# Git 操作助手

## Overview

封装日常 Git 工作流，按照项目编码规范执行版本控制操作。涵盖状态查看、分支管理、代码提交、推送拉取、合并变基、撤销恢复等全流程操作，对危险操作内置安全确认机制。

**触发关键词**：用户说"提交代码"、"push"、"新建分支"、"合并代码"、"撤销修改"、"git 操作"等时触发此 skill。

---

## 安全原则

### 危险操作分级

| 级别 | 操作 | 处理方式 |
|------|------|----------|
| 🟢 安全 | status / diff / log / branch / switch / stash / fetch | 直接执行 |
| 🟡 注意 | commit / push / pull / merge / tag | 执行前展示操作概要，确认后执行 |
| 🔴 危险 | push --force / reset --hard / rebase / cherry-pick | **必须**展示影响范围 + 二次确认后执行 |

### 保护分支规则

以下分支为**保护分支**，云效 Codeup 已在服务端禁止直接推送，本地推送会被拒绝（`GL-HOOK-ERR: protected branch`）：

| 分支 | 直接 push | 直接 push --force | 变更方式 |
|------|-----------|-------------------|----------|
| `main` | ❌ 禁止 | ❌ 禁止 | 必须走 PR / Merge Request 合并 |
| `master` | ❌ 禁止 | ❌ 禁止 | 必须走 PR / Merge Request 合并 |
| `develop` | ⚠️ 二次确认 | ❌ 禁止 | 优先走 PR，紧急场景二次确认 |
| `release/*` | ⚠️ 二次确认 | ❌ 禁止 | 优先走 PR，紧急场景二次确认 |

**关键规则（`main` / `master`）**：

1. 用户要求"推送到 main / master"时，**先阻止本地 push 命令**，改为提示走 PR：
   - 若变更还在保护分支上（`git branch --show-current` == `main`/`master`），先 `git switch -c feature/<...>` 把提交带走，再推 feature 分支
   - 已在非保护分支上：直接 `git push -u origin <feature_branch>` 推特性分支
2. Push 成功后，提示用户**在云效 Codeup 网页发起 Merge Request**（目标分支：`main` / `master`），本 skill 不代替走 MR
3. 云效 Codeup Merge Request 页面：`https://codeup.aliyun.com/{orgId}/{project_path}/change/new?sourceBranch=<feature>&targetBranch=main`

**关键规则（`develop` / `release/*`）**：

- 执行 push 前展示待推送内容 + 用户二次确认
- 强制推送始终禁止，如需 rewrite 历史，必须先解除保护分支再操作

### 执行前检查

每次执行 git 写操作前，必须先运行 `git status --short` 确认工作区状态，避免误操作。

---

## 提交信息规范

### 格式

```
<类型>(<作用域>): <描述> [#issue]
```

### 类型清单

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(mcp-list): 新增 MCP 列表分页查询` |
| `fix` | 修复 Bug | `fix(audit): 修复审计日志查询空指针异常` |
| `docs` | 文档变更 | `docs: 更新 API 接口文档` |
| `style` | 代码格式化（无逻辑变更） | `style: 格式化 Controller 代码` |
| `refactor` | 重构 | `refactor(service): 重构 MCP 服务查询逻辑` |
| `test` | 测试代码 | `test(skill): 新增技能详情页测试用例` |
| `chore` | 构建工具或依赖更新 | `chore: 升级 Spring Boot 版本` |

### 规则

- 描述使用**现在时主动语态**（"新增"而非"已新增"）
- 禁止无意义描述：`"修改代码"`、`"修复bug"`、`"fix"`
- 作用域可选，建议使用模块/组件名
- 关联 Issue 可选：`#112233`

---

## 分支命名规范

| 分支类型 | 命名格式 | 示例 |
|----------|----------|------|
| 功能分支 | `feature/<开发人>-<日期>-<#需求id>-<描述>` | `feature/zhangsan-0510-#112233-wxlogin` |
| 修复分支 | `hotfix/<开发人>-<日期>-<描述>` | `hotfix/zhangsan-0510-fix-null-point` |
| 发布分支 | `release/vX.Y.Z` | `release/v1.2.0` |
| 预发布分支 | `staging` | `staging` |

---

## 功能列表

### 1. 查看状态 (status)

查看当前工作区状态，包括修改、暂存、未跟踪文件。

```bash
# 查看简要状态
git status --short

# 查看详细状态
git status

# 查看分支跟踪信息
git status -sb
```

**执行时机**：每次 git 写操作前必须先执行，确认工作区干净或有预期的变更。

---

### 2. 查看差异 (diff)

查看文件的具体修改内容。

```bash
# 查看工作区与暂存区的差异（未 add 的修改）
git diff

# 查看暂存区与最新 commit 的差异（已 add 未 commit 的修改）
git diff --cached

# 查看工作区与最新 commit 的差异（所有未提交的修改）
git diff HEAD

# 查看两个分支的差异
git diff <branch1>..<branch2>

# 查看某个文件的差异
git diff -- <file_path>

# 仅查看文件名（不显示具体内容）
git diff --name-only
```

**提交前检查**：`git diff --cached` 是提交前的必查步骤，确保不提交范围外的内容。

---

### 3. 查看日志 (log)

查看提交历史记录。

```bash
# 查看最近 N 条提交（简洁模式）
git log --oneline -20

# 查看详细日志（含作者、时间、完整信息）
git log -10

# 图形化展示分支历史
git log --oneline --graph --all -30

# 查看某个文件的修改历史
git log --oneline -- <file_path>

# 查看某段时间的提交
git log --since="2026-07-01" --until="2026-07-07" --oneline

# 查看某个作者的提交
git log --author="zhangsan" --oneline -20

# 搜索提交信息
git log --grep="关键词" --oneline
```

---

### 4. 拉取代码 (pull)

从远程仓库拉取并合并代码到当前分支。

```bash
# 标准拉取（merge 模式，项目默认）
git pull origin <branch>

# 变基拉取（当本地与远程分叉时使用，保持线性历史）
git pull --rebase origin <branch>

# 仅拉取不合并（fetch + 手动决定）
git fetch origin
git log HEAD..origin/<branch> --oneline  # 查看远程新增了哪些提交
```

**分叉处理流程**：

当 `git pull` 提示分叉（diverged）时：

1. `git status --short` — 确认工作区干净
2. `git log --oneline -5` — 查看本地最近提交
3. `git log --oneline -5 FETCH_HEAD` — 查看远程最近提交
4. `git merge-base HEAD origin/<branch>` — 定位共同祖先
5. `git pull --rebase origin <branch>` — 变基拉取
6. 如有冲突 → 解决冲突 → `git add` → `git rebase --continue`
7. 确认无误后，设置默认 merge 模式：`git config pull.rebase false`

---

### 5. 新建分支 (branch)

从当前分支创建新分支。

```bash
# 新建分支并切换
git checkout -b <branch_name>
# 或（推荐，语义更清晰）
git switch -c <branch_name>

# 从指定分支创建
git switch -c <branch_name> <source_branch>

# 从远程分支创建本地跟踪分支
git switch -c <branch_name> origin/<remote_branch>

# 仅创建不切换
git branch <branch_name>
```

**命名提醒**：按分支命名规范创建，如 `feature/zhangsan-0707-#112233-add-mcp-search`。

---

### 6. 切换分支 (switch / checkout)

切换到指定分支。

```bash
# 切换到本地分支（推荐 switch）
git switch <branch_name>

# 切换到远程分支（自动创建本地跟踪分支）
git switch <branch_name>  # 若本地不存在，Git 2.23+ 自动跟踪同名远程分支

# 切换到上一个分支
git switch -

# 列出所有本地分支
git branch

# 列出所有分支（含远程）
git branch -a

# 列出已合并到当前分支的分支
git branch --merged
```

**切换前检查**：如有未提交的修改，提示用户先 commit 或 stash。

---

### 7. 暂存管理 (stash)

临时保存工作区修改，不提交到版本库。

```bash
# 暂存当前修改（含已暂存的）
git stash push -m "描述信息"

# 暂存（包括未跟踪文件）
git stash push -u -m "描述信息"

# 查看暂存列表
git stash list

# 恢复最近一次暂存（保留暂存记录）
git stash apply

# 恢复最近一次暂存（删除暂存记录）
git stash pop

# 恢复指定暂存
git stash apply stash@{2}

# 删除暂存
git stash drop stash@{0}

# 清空所有暂存（危险）
git stash clear
```

---

### 8. 提交代码 (commit)

将暂存区的修改提交到版本库。

**标准提交流程**：

```bash
# Step 1: 查看状态
git status --short

# Step 2: 暂存修改
git add <file1> <file2>          # 指定文件
git add .                         # 全部修改（谨慎，确保无多余文件）

# Step 3: 检查暂存内容（必做）
git diff --cached

# Step 4: 提交
git commit -m "feat(scope): 新增XXX功能"

# Step 5: 确认提交结果
git log --oneline -1
git status --short
```

**追加修改到上次提交**（amend）：

```bash
# 修改还未 push 的最近一次提交信息
git commit --amend -m "feat(scope): 修正后的提交信息"

# 追加文件到最近一次提交（不改信息）
git add <new_file>
git commit --amend --no-edit
```

> ⚠️ **禁止对已 push 的提交使用 amend**，会导致历史分叉。

---

### 9. 推送代码 (push)

将本地提交推送到远程仓库。

```bash
# 推送当前分支到远程同名分支（首次推送自动建立跟踪关系）
git push -u origin <branch_name>

# 推送当前分支（已建立跟踪关系）
git push

# 推送到指定远程分支
git push origin <local_branch>:<remote_branch>

# 删除远程分支
git push origin --delete <branch_name>
```

**推送前检查**：

1. `git status --short` — 确认工作区状态
2. `git branch --show-current` — 若当前处于 `main` / `master`，**必须**先切到 feature 分支再推：`git switch -c feature/<owner>-<date>-<desc>`
3. `git log origin/<branch>..HEAD --oneline` — 查看待推送的提交
4. 若目标为 `main` / `master`：**拒绝执行直接 push**，改推特性分支后提示用户在云效 Codeup 网页发起 Merge Request
5. 若目标为 `develop` / `release/*`：展示待推送内容并请求二次确认

---

### 10. 合并代码 (merge)

将指定分支合并到当前分支。

```bash
# 标准合并（保留合并记录）
git merge <source_branch>

# 合并并压缩为单个提交
git merge --squash <source_branch>
git commit -m "feat(scope): 合并XXX功能分支"

# 仅合并不自动提交（可检查后手动提交）
git merge --no-commit --no-ff <source_branch>

# 中止合并（冲突时放弃）
git merge --abort
```

**冲突解决流程**：

1. `git merge <branch>` — 执行合并
2. 如有冲突 → `git status` 查看冲突文件
3. 手动编辑冲突文件，解决 `<<<<<<<` / `=======` / `>>>>>>>` 标记
4. `git add <resolved_files>` — 标记已解决
5. `git commit` — 完成合并提交（或 `git merge --continue`）
6. 如需放弃 → `git merge --abort`

---

### 11. Rebase 变基

🔴 **危险操作** — 将当前分支的提交嫁接到目标分支之上，重写提交历史。

```bash
# 将当前分支变基到目标分支
git rebase <target_branch>

# 交互式变基（编辑、压缩、重排、删除提交）
git rebase -i HEAD~3

# 变基到远程分支
git rebase origin/<branch>
```

**变基前必须确认**：

1. ✅ 工作区干净（`git status --short` 无输出）
2. ✅ 当前分支若是保护分支（main / master / develop / release/*），展示影响范围并请求二次确认
3. ✅ 如分支已 push，了解变基会改变历史

**冲突解决流程**：

1. `git rebase <branch>` — 执行变基
2. 如有冲突 → `git status` 查看冲突文件
3. 手动解决冲突
4. `git add <resolved_files>` — 标记已解决
5. `git rebase --continue` — 继续变基
6. 如需放弃 → `git rebase --abort`

**变基后推送**：需使用 `git push --force-with-lease`（比 `--force` 更安全）。

---

### 12. Cherry-pick 摘樱桃

🔴 **危险操作** — 将指定提交应用到当前分支。

```bash
# 摘取单个提交
git cherry-pick <commit_hash>

# 摘取多个提交（按顺序）
git cherry-pick <hash1> <hash2> <hash3>

# 摘取一段提交（不含起始，含结束）
git cherry-pick <start_hash>..<end_hash>

# 摘取但不自动提交
git cherry-pick --no-commit <commit_hash>
```

**冲突解决流程**：

1. `git cherry-pick <hash>` — 执行摘取
2. 如有冲突 → 手动解决
3. `git add <resolved_files>` — 标记已解决
4. `git cherry-pick --continue` — 继续
5. 如需放弃 → `git cherry-pick --abort`

---

### 13. 撤销修改 (restore)

撤销工作区或暂存区的修改。

```bash
# 撤销工作区修改（未 add 的文件）— 丢弃修改，不可恢复
git restore <file_path>
git restore .                    # 全部文件

# 撤销暂存（已 add 未 commit，回到未 add 状态，保留修改）
git restore --staged <file_path>
git restore --staged .           # 全部文件

# 恢复到指定 commit 的版本
git restore --source=<commit_hash> <file_path>
```

> ⚠️ `git restore` 会**丢弃**工作区修改，操作前确认是否需要先 stash。

---

### 14. 硬重置 (reset --hard)

🔴 **危险操作** — 将当前分支重置到指定位置，**丢弃**之后的所有提交和修改。

```bash
# 重置到指定 commit（丢弃该 commit 之后的所有提交和修改）
git reset --hard <commit_hash>

# 重置到远程分支状态（放弃所有本地提交和修改）
git reset --hard origin/<branch>

# 软重置（保留修改在工作区，仅移动 HEAD）
git reset --soft <commit_hash>

# 混合重置（保留修改但取消暂存，默认模式）
git reset --mixed <commit_hash>
```

**执行前必须**：

1. 🔴 展示将被丢弃的提交：`git log --oneline <target_hash>..HEAD`
2. 🔴 展示将被丢弃的修改：`git status --short`
3. 🔴 询问用户是否确认
4. 建议先备份：`git branch backup-<date>` 创建备份分支

**误操作恢复**：

```bash
# 查看引用日志（90 天内的操作记录）
git reflog

# 找到误 reset 前的 commit hash，重置回去
git reset --hard <commit_hash_from_reflog>
```

---

### 15. 强制推送 (push --force)

🔴 **危险操作** — 用本地分支覆盖远程分支，远程原有提交会被丢弃。

```bash
# 安全强制推送（推荐）— 仅当远程没有新提交时才覆盖
git push --force-with-lease origin <branch>

# 暴力强制推送（不推荐）— 无条件覆盖
git push --force origin <branch>
```

**规则**：

1. 🔴 **禁止**对 `main` / `master` 使用任何形式的强制推送（Codeup 服务端已拦截，本地也不应尝试）
2. 🔴 对 `develop` / `release/*` 使用强制推送时，展示影响范围并请求二次确认
3. 🔴 执行前展示远程将被覆盖的提交：`git log origin/<branch>..HEAD --oneline` 和 `git log HEAD..origin/<branch> --oneline`
4. ✅ 优先使用 `--force-with-lease` 而非 `--force`
5. ✅ rebase 或 amend 后需要强制推送时，必须先确认远程无他人新提交

---

### 16. 标签管理 (tag)

为特定提交打标签，通常用于版本发布。

```bash
# 查看所有标签
git tag

# 查看匹配标签
git tag -l "v1.*"

# 创建轻量标签
git tag v1.0.0

# 创建附注标签（推荐，含作者、日期、信息）
git tag -a v1.0.0 -m "发布版本 1.0.0"

# 给历史提交打标签
git tag -a v1.0.0 <commit_hash> -m "发布版本 1.0.0"

# 推送单个标签到远程
git push origin v1.0.0

# 推送所有标签
git push origin --tags

# 删除本地标签
git tag -d v1.0.0

# 删除远程标签
git push origin --delete v1.0.0
```

---

## 工作流程

### 日常开发流程

```
1. git switch main && git pull                             # 切到主分支并拉取最新
2. git switch -c feature/dev-0707-#123-add-feature         # 创建功能分支（禁止直接在 main 上开发）
3. ... 开发代码 ...
4. git status --short                                       # 查看修改
5. git diff                                                 # 检查差异
6. git add <files>                                          # 暂存
7. git diff --cached                                        # 检查暂存内容（必做）
8. git commit -m "feat(scope): 新增XXX功能"                # 提交
9. git push -u origin feature/dev-0707-#123-add-feature    # 推送特性分支（禁止推 main）
10. 提示用户在云效 Codeup 网页创建 Merge Request → 目标 main # ⚠️ 不代替走 MR
```

### 紧急修复流程

```
1. git switch main && git pull                             # 从主分支拉取最新
2. git switch -c hotfix/dev-0707-fix-urgent-bug            # 创建修复分支
3. ... 修复代码 ...
4. git add <files> && git commit -m "fix(scope): 修复XXX紧急问题"
5. git push -u origin hotfix/dev-0707-fix-urgent-bug       # 推送 hotfix 分支
6. 提示用户在云效 Codeup 网页创建 Merge Request → 目标 main # ⚠️ 不代替走 MR
7. MR 合入后由发布负责人打 tag（v1.2.1 等），本 skill 不代打 tag
```

### 合并前自检流程

```
1. git switch main && git pull                             # 确保目标分支最新
2. git switch <feature_branch>
3. git rebase main                                          # 变基到最新 main
4. 如有冲突 → 解决 → git add → git rebase --continue
5. git push --force-with-lease origin <feature_branch>     # 推送变基后的特性分支
6. 提示用户在云效 Codeup 网页更新 MR
```

---

## 快速命令参考

```bash
# 一键查看完整状态
git status -sb && echo "---" && git log --oneline -5

# 提交前自检
git status --short && git diff --cached

# 查看当前分支的所有跟踪信息
git branch -vv

# 查看远程仓库信息
git remote -v

# 清理已合并的本地分支（除 main/master/develop）
git branch --merged | grep -v -E "main|master|develop" | xargs -r git branch -d

# 查看文件修改历史
git log --oneline --follow -- <file_path>
```
