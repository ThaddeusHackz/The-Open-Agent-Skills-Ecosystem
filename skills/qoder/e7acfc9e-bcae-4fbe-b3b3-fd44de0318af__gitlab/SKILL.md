---
name: gitlab
description: 封装 glab CLI 操作 GitLab（Issue、MR、CI/CD 流水线、API 调用），当用户需要访问 GitLab、查看合并请求、管理 Issue、分析流水线状态或调用 GitLab API 时触发。
title: GitLab操作
category: 开发工具
---

# GitLab CLI 操作工具

封装 `glab` CLI 的常用操作。

## 技能工作流

glab 技能按需执行，每次操作遵循以下流程：

选择场景子命令 → 构造参数执行 → 解析结果

### 步骤 1：选择场景子命令

根据用户需求选择对应场景的命令。

| 场景 | 入口命令 | 对应章节 |
|------|----------|----------|
| Issue 管理 | `glab issue` | 常见模式（场景1: Issue 管理） |
| MR 管理 | `glab mr` | 常见模式（场景2: MR 管理） |
| CI/CD 流水线分析 | `glab ci` | 常见模式（场景3: CI/CD 流水线分析） |
| GitLab API 调用 | `glab api` | 常见模式（场景4: GitLab API 调用） |

### 步骤 2：构造参数执行

根据场景章节中的命令模板，填充实际的 ID、标签、消息等参数后执行。

### 步骤 3：解析结果

解析命令输出，提取需要的信息回应给用户。

## 核心操作模式

每个操作都遵循以下步骤：
1. **确认命令**：根据场景选择正确的 glab 子命令
2. **构造参数**：填充项目标识、ID、选项等参数
3. **执行命令**：运行 glab 命令
4. **解析结果**：将 JSON 或文本输出转换为结构化信息

## 常用命令

| 命令 | 用途 |
|------|------|
| `glab issue create` | 创建 Issue |
| `glab issue view <id> --comments` | 查看 Issue（含评论） |
| `glab issue view <id> -F json` | 以 JSON 查看 Issue 详情 |
| `glab issue list -F json [--label]` | 查询 Issue 列表 |
| `glab issue note <id> -m "..."` | 添加 Issue 评论 |
| `glab issue update <id> --label "..."` | 添加标签 |
| `glab issue update <id> --unlabel "..."` | 移除标签 |
| `glab issue close <id>` | 关闭 Issue |
| `glab mr view <id>` | 查看 MR 详情 |
| `glab mr list -F json [--state]` | 查询 MR 列表 |
| `glab mr note <id> -m "..."` | 评论 MR |
| `glab mr approve <id>` | 审批 MR |
| `glab ci view` | 查看当前流水线 |
| `glab ci status` | 查看流水线状态 |
| `glab ci jobs` | 列出流水线中的 Job |
| `glab ci job logs <job-id>` | 查看 Job 日志 |
| `glab ci job retry <job-id>` | 重试失败的 Job |
| `glab api <endpoint>` | 调用任意 GitLab REST API |

## 常见模式（场景1: Issue 管理）

### 创建 Issue

```bash
glab issue create \
  --title "功能：添加库存预警功能" \
  --description "## 需求描述\n\n当库存低于阈值时自动触发预警通知。" \
  --label "enhancement,wms" \
  --assignee "@username"
```

### 查看 Issue

```bash
# 查看 Issue 详情和评论
glab issue view 42 --comments

# 以 JSON 格式获取（便于程序化处理）
glab issue view 42 -F json
```

### 查询 Issue 列表

```bash
# 查询所有未关闭的 Issue
glab issue list -F json --state opened

# 按标签筛选
glab issue list -F json --label "bug,critical"

# 查询指定标签
glab issue list -F json --label "wms"
```

### 更新 Issue 状态

```bash
# 添加评论后关闭
glab issue note 42 -m "已在 #123 MR 中修复"
glab issue close 42

# 更新标签
glab issue update 42 --label "wms,ready-for-review"
glab issue update 42 --unlabel "in-progress"
```

## 常见模式（场景2: MR 管理）

### 查看 MR

```bash
# 查看 MR 详情
glab mr view 123

# 查看 MR 变更文件
glab mr diff 123

# 查看 MR 评论
glab mr notes 123
```

### 审查和评论 MR

```bash
# 添加审查评论
glab mr note 123 -m "LGTM，但建议将库存查询加上缓存。"

# 审批 MR
glab mr approve 123
```

### 查询 MR 列表

```bash
# 查询待审查的 MR
glab mr list -F json --state opened --reviewer "@me"

# 查询自己创建的 MR
glab mr list -F json --state opened --author "@me"
```

## 常见模式（场景3: CI/CD 流水线分析）

### 查看流水线状态

```bash
# 查看当前分支的流水线
glab ci view

# 查看最近流水线列表
glab ci list

# 查看指定流水线的 Job 状态
glab ci jobs
```

### 分析流水线失败

```bash
# 查看失败 Job 的日志
glab ci job logs <job-id>

# 重试失败 Job
glab ci job retry <job-id>
```

### 从 GitLab URL 分析 Job 或流水线

当用户提供类似 `https://git.ifengqun.com/xxx/xxx/-/jobs/12345` 的链接时：

```bash
# 1. 提取项目路径和 Job ID
# 2. 调用 API 获取 Job 详情
glab api "/projects/:id/jobs/12345"

# 3. 获取 Job 日志
glab ci job logs 12345
```

项目 ID 可通过以下方式获取：
```bash
glab api "/projects/:encoded_path" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])" -- 替换为URL编码的项目路径
```

## 常见模式（场景4: GitLab API 调用）

当标准子命令不满足需求时，使用 `glab api` 直接调用 GitLab REST API。

### 获取 Pipeline 和 Job 信息

```bash
# 获取项目流水线列表
glab api /projects/:id/pipelines

# 获取流水线的 Job 列表
glab api /projects/:id/pipelines/<pipeline-id>/jobs

# 获取单个 Job 详情
glab api /projects/:id/jobs/<job-id>
```

### 项目相关

```bash
# 获取项目信息
glab api /projects/:id

# 获取项目变量
glab api /projects/:id/variables

# 获取项目成员
glab api /projects/:id/members/all
```

### API 调用选项

```bash
# POST 请求
glab api -X POST /projects/:id/merge_requests \
  -f source_branch=feature/xxx \
  -f target_branch=main \
  -f title="新功能"

# 分页（默认第一页，每页 20 条）
glab api /projects/:id/pipelines?per_page=100\&page=1

# JSON 输出（可用 jq 或 python3 解析）
glab api /projects/:id/pipelines | python3 -c "import sys,json; data=json.load(sys.stdin); [print(p['id'], p['status']) for p in data]"
```

## 异常处理

### glab 未安装

如果 `glab --version` 检查失败，执行以下步骤：

1. 告知用户 glab 未安装，无法执行 GitLab 操作
2. 运行安装指引：查看 `references/install-guide.md`，按对应系统的安装步骤操作
3. 安装完成后，执行 `glab auth login` 完成身份验证
4. 验证安装：`glab --version && glab auth status`

### 命令执行失败

| 错误 | 原因 | 处理方式 |
|------|------|----------|
| `Error: not authenticated` | 未登录或 token 过期 | 运行 `glab auth login` 重新登录 |
| `Error: not a git repository` | 不在 Git 仓库目录 | 确认在执行 glab 命令前已 cd 到项目目录，或使用 `-R <project>` 指定项目 |
| `400 Bad Request` | 参数错误 | 检查命令参数是否正确 |
| `404 Not Found` | 资源不存在或无权限 | 确认 ID/路径正确，检查是否有访问权限 |
| `API rate limit exceeded` | 请求过于频繁 | 等待后重试，或加入 `sleep 1` 间隔 |

### 指定项目参数

当不在项目目录中时，使用 `-R` 参数指定项目：

```bash
glab -R https://git.ifengqun.com/ai-launch/fengqun-scm issue list -F json
```

## 使用说明

### 前置条件

- 已安装 glab CLI（安装指引见 [references/install-guide.md](references/install-guide.md)）
- 已通过 `glab auth login` 完成登录
- 在 Git 仓库目录内执行（或使用 `-R` 指定项目）

### 在仓库内执行

克隆了仓库的目录中，glab 自动根据 Git remote 识别项目：

```bash
cd /path/to/project
glab issue list -F json
```

### 不在仓库内执行

```bash
glab -R https://git.ifengqun.com/namespace/project issue view 42
```

### JSON 输出处理

优先使用 `-F json` 输出格式，配合 python3 或 jq 解析：

```bash
glab issue list -F json | python3 -c "
import sys, json
issues = json.load(sys.stdin)
for i in issues:
    print(f'#{i[\"iid\"]} {i[\"title\"]} ({i[\"state\"]})')
"
```

## 禁止事项

- 不创建或修改 git 仓库配置（git config）
- 不执行破坏性操作（如删除 Issue/MR、force push）除非用户明确要求
- 不批量重试/操作流水线
- 不修改用户已有的 glab 配置