---
name: git-merger
description: 智能分析和解决 Git 合并/变基冲突，逐文件审查两边内容后做出合理决策并自动循环处理直到完成。当用户遇到 git merge/rebase 冲突、要求合并代码、解决冲突、或继续 rebase 时触发。
title: GIT冲突智能合并
category: 开发
---

# Git 冲突智能合并

分析 Git 合并/变基中的每个冲突，基于内容语义和业务上下文做出合理决策（而非盲目选择某一方），自动循环处理直到完成。

## 技能工作流

调用 `todo_write` 工具创建待办任务：

检测状态 → 分析冲突 → 决策判断 → 执行解决 → 验证/继续 → 全局扫描

### 步骤 1：检测状态

确定当前处于 merge 还是 rebase，列出所有冲突文件：

```bash
# 检测操作类型
git status | head -5

# 列出冲突文件
git status --short | grep "^UU\|^AA\|^DD\|^U \|^ U"

# 统计冲突数量
git diff --name-only --diff-filter=U | wc -l
```

根据冲突数量选择模式：
- ≤5 个文件 → 逐个审查模式
- >5 个文件且用户要求自动 → 自动循环模式
- >5 个文件但用户未明确 → 先询问用户

### 步骤 2：分析冲突

对每个冲突文件，提取冲突标记位置并读取两边内容：

```bash
grep -n "<<<<<<< HEAD\|=======\|>>>>>>>" <file>
```

**必须分析的内容**：
1. HEAD（ours）侧的实际内容
2. 传入（theirs）侧的实际内容
3. 传入侧的 commit message（揭示改动意图）

### 步骤 3：决策判断

**核心原则：以内容正确性为准，不盲目选择某一方。**

**决策树**：

```
冲突两边内容
  ├── 一边有内容，一边为空
  │   ├── 有内容侧是必要配置（数据库、Redis、密钥等）→ 保留有内容侧
  │   ├── 有内容侧是功能代码/测试用例 → 保留有内容侧
  │   └── 传入侧明确删除（commit message 说明要删除）→ 保留空侧
  │
  ├── 两边都有内容，内容不同
  │   ├── 架构/配置类文件
  │   │   ├── 生产配置 → 保留连接生产环境的版本
  │   │   ├── CI/CD 配置 → 保留与项目架构一致的版本
  │   │   └── 环境配置 → 保留对应环境的正确连接值
  │   ├── 代码文件
  │   │   ├── 一边是新架构重构，一边是旧代码 → 保留新架构
  │   │   ├── 一边功能更完整 → 保留更完整的版本
  │   │   └── 两边改了不同功能 → 手动合并两边
  │   └── 测试/文档资产
  │       ├── 一边覆盖更多用例 → 保留更完整的版本
  │       └── 两边有独立内容 → 手动合并两边
  │
  └── 文件路径变更（重命名/移动）
      └── 保留目标路径下的正确内容
```

**决策输出格式**：

向用户说明每个冲突的分析结果：

```
**冲突分析**：
- **HEAD**：{描述 HEAD 侧内容}
- **传入**（commit "{message}"）：{描述传入侧内容}

**判断**：{选择哪边及理由}
```

### 步骤 4：执行解决

**单文件解决**：

```bash
# 保留 ours（HEAD）
git checkout --ours <file> && git add <file>

# 保留 theirs（传入）
git checkout --theirs <file> && git add <file>

# 手动合并：用 SearchReplace 工具编辑文件移除冲突标记后 git add
```

**批量解决**（相同决策的多文件）：

```bash
git checkout --ours file1 file2 file3 && git add file1 file2 file3
git checkout --theirs file1 file2 file3 && git add file1 file2 file3
```

### 步骤 5：验证与继续

```bash
git status --short | grep "^UU\|^AA\|^DD" || echo "No remaining conflicts"
```

- **merge 操作**：无冲突后等待用户确认再 commit
- **rebase 操作**：无冲突后自动继续 `GIT_EDITOR=true git rebase --continue`
- 如果 rebase 产生新冲突，回到步骤 2 循环处理

### 步骤 6：全局扫描残留冲突标记

rebase/merge 全部完成后，必须全局扫描确认无残留冲突标记（`<<<<<<<`、`=======`、`>>>>>>>`），否则会导致编译失败：

```bash
grep -rn "<<<<<<<" --include="*.java" --include="*.yml" --include="*.yaml" \
  --include="*.ts" --include="*.tsx" --include="*.md" --include="*.feature" \
  --include="*.sh" --include="*.conf" \
  fengqun-scm-service/ fengqun-scm-api/ fengqun-scm-admin/src/ \
  fengqun-scm-tms/src/ fengqun-scm-pda/src/ test-plan-karate/ \
  .agents/ AGENTS.md 2>/dev/null \
  | grep -v node_modules | grep -v target | grep -v dist \
  || echo "✅ 全局无残留冲突标记"
```

如果发现残留，用 Python 脚本批量清理（保留 HEAD 侧内容）：

```python
import re, os
pattern = re.compile(r'<<<<<<< HEAD[^\n]*\n(.*?)=======\n.*?>>>>>>>[^\n]*\n', re.DOTALL)
for f in <file_list>:
    content = open(f).read()
    if '<<<<<<<' in content:
        open(f, 'w').write(pattern.sub(r'\1', content))
```

## 自动循环模式

当用户明确要求自动完成或冲突全是同类型时，执行循环脚本：

```bash
bash scripts/resolve_loop.sh ours
bash scripts/resolve_loop.sh theirs
```

循环脚本自动检测冲突 → 按策略解决 → continue rebase → 重复直到完成。

**限制**：混合类型冲突（同时有配置文件、代码文件、测试文件）禁止全量自动，必须逐个审查。

## 常见冲突模式速查

| 模式 | 特征 | 典型决策 |
|------|------|----------|
| 新增 vs 空 | HEAD 新增了配置/代码，传入为空 | 保留 HEAD |
| 空 vs 新增 | HEAD 为空，传入新增了功能 | 保留传入 |
| 重构 vs 旧代码 | 一边已迁移到新包/新文件，一边改旧路径 | 保留新架构 |
| 同文件不同环境 | 数据库 URL、密钥等环境相关值不同 | 保留目标环境的值 |
| CI 配置差异 | 部署方式不同（Jenkins vs kubectl） | 保留与项目架构一致的版本 |
| 测试资产覆盖 | 同一测试文件两边版本不同 | 保留覆盖更完整的版本 |

## 使用说明

### 交互式解决（推荐）

用户说「帮我合并下代码」「又有冲突了」「看下怎么合并」时，逐个审查冲突文件并按决策树解决。

### 自动循环解决

用户说「你来操作吧」「自动完成」或冲突数量 >10 且类型相同时，使用 `scripts/resolve_loop.sh` 批量处理。

### 示例

- `帮我合并下代码，采用传入的更改` → 分析后保留 theirs
- `又有冲突了，看下怎么合并` → 逐个分析每个冲突
- `你来操作吧，我不想手动继续了` → 自动循环解决

## 错误处理

| 错误场景 | 处理方案 |
|----------|----------|
| 存在未解决的合并状态（needs merge） | 先执行 `git merge --abort` 或 `git reset --hard HEAD` 清理 |
| 冲突文件包含二进制文件 | 提示用户手动处理，不自动选择 |
| rebase 超过最大轮次 | 停止循环，提示用户检查 `git status` |
| 手动合并后仍有冲突标记残留 | 用步骤 6 全局扫描并批量清理 |
| rebase 后编译失败（Unresolved compilation） | 全局扫描 `<<<<<<<` 标记，说明有文件在 rebase 中漏掉了冲突解决 |

## 禁止事项

- ❌ 不分析内容直接 `git checkout --ours` 或 `--theirs`
- ❌ 对生产配置（数据库、Redis、密钥）盲目选择
- ❌ 在用户未明确要求时全量自动解决混合类型冲突
- ❌ merge 操作完成后未经用户确认直接 commit
- ❌ 忽略 rebase 过程中的 dropped commit 信息

## 参考资料

- 决策树详解 → [references/decision-rules.md](references/decision-rules.md)
