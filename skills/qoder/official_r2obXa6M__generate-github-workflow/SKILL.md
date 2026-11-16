---
name: generate-github-workflow
description: "交互式生成 GitHub Actions 工作流。当用户说'生成工作流'、'创建CI/CD'、'配置GitHub Actions'、'自动化部署'、'代码审查工作流'、'/gen-workflow' 时使用本技能。| Interactively generate GitHub Actions workflow files with Qoder Action integration and guide GitHub configuration."
---

# Generate GitHub Workflow — GitHub Actions 工作流生成

> 一句话定义：让 **开发者/DevOps** 在 **项目CI/CD配置阶段** 通过 **回答几个问题** 快速生成 **GitHub Actions 工作流文件并获得 GitHub 配置指引**

---

## 触发条件

当用户说以下内容时触发：

- "帮我生成 GitHub 工作流"、"创建 CI/CD"
- "配置 GitHub Actions"、"自动化部署"
- "代码审查工作流"、"AI Code Review"
- "生成 workflow"、"Qoder Action"
- "/gen-workflow"

---

## 使用场景

### 应该使用

- 新项目需要配置 CI/CD 流水线
- 需要添加 AI 代码审查（Qoder Action）
- 需要自动化部署到 ECS/云服务器
- 需要配置代码质量检查（lint/test/security）
- Workshop 教学中演示 GitHub Actions

### 不应使用

- 已有完善的工作流且无需修改
- 不使用 GitHub（用 GitLab CI / Jenkins 等）
- 只想了解 GitHub Actions 原理（直接回答即可）

---

## 执行步骤

```
1. 询问工作流类型（可多选）
2. 收集项目信息（技术栈/分支/部署目标）
3. 生成工作流 YAML 文件
4. 输出 GitHub 配置指引（Secrets/Permissions）
5. 输出验证方法
```

### 步骤 1：询问工作流类型

提供 3 个代表性模板供选择（可多选），其他类型直接描述需求即可生成：

| 编号 | 工作流类型 | 文件名 | 说明 |
|------|-----------|--------|------|
| **A** | AI 代码审查 | `ai-code-review.yml` | PR 时自动运行 Qoder AI 审查 |
| **B** | CI 测试 | `ci-tests.yml` | 推送/PR 时运行单元测试 |
| **C** | 部署到 ECS | `deploy-ecs.yml` | 自动部署到阿里云 ECS |

> 以上仅为常用示例。如需代码质量检查、GitHub Pages 部署、E2E 测试等其他类型，直接描述需求，按相同流程生成。

### 步骤 2：收集项目信息

根据用户选择的工作流类型，问以下问题：

**通用问题（所有类型）**：
- 主分支名？（默认 `main`）
- 需要监控哪些路径？

**A: AI 代码审查**：
- 审查语言？（默认 Chinese）
- 大型 PR 跳过阈值？（默认 1000 行）

**B: CI 测试**：
- 技术栈？（Python/Node.js/Go 等）
- 代码目录和测试命令？

**C: 部署到 ECS**：
- 触发路径、源目录、目标路径？

### 步骤 3：生成 YAML 文件

在 `.github/workflows/` 目录下生成对应的 YAML 文件。

### 步骤 4：输出 GitHub 配置指引

告诉用户需要在 GitHub 仓库中配置哪些 Secrets 和 Permissions。

### 步骤 5：输出验证方法

说明如何触发工作流并查看结果。

---

## 具体实现

### 模板 A：AI 代码审查（Qoder Action）

```yaml
# AI 代码审查工作流 - 使用 Qoder Action
name: AI Code Review

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [{BRANCH}]
    paths:
      - '**/*.py'
      - '**/*.js'
      - '**/*.ts'
      - '**/*.tsx'
      - '.github/workflows/**'

permissions:
  contents: read
  pull-requests: write
  checks: write

jobs:
  ai-code-review:
    name: Qoder AI Code Review
    runs-on: ubuntu-latest
    steps:
      - name: 📥 检出代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 📏 检查 PR 大小
        id: check_size
        run: |
          LINES=$(jq '.pull_request.additions // 0' < "$GITHUB_EVENT_PATH")
          echo "lines=$LINES" >> $GITHUB_OUTPUT
          if [ "$LINES" -gt {MAX_LINES} ]; then
            echo "skip=true" >> $GITHUB_OUTPUT
          else
            echo "skip=false" >> $GITHUB_OUTPUT
          fi

      - name: 🔍 Qoder AI 代码审查
        if: steps.check_size.outputs.skip == 'false'
        uses: QoderAI/qoder-action@v0
        with:
          qoder_personal_access_token: ${{ secrets.QODER_PERSONAL_ACCESS_TOKEN }}
          prompt: |
            /review-pr
            REPO:${{ github.repository }}
            PR_NUMBER:${{ github.event.pull_request.number }}
            OUTPUT_LANGUAGE: {LANGUAGE}
```

### 模板 B：CI 测试（Python）

```yaml
name: CI Tests

on:
  push:
    branches: [{BRANCH}]
    paths: ['{BACKEND_DIR}/**']
  pull_request:
    branches: [{BRANCH}]
    paths: ['{BACKEND_DIR}/**']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 🐍 安装 Python
        uses: actions/setup-python@v5
        with:
          python-version: '{PYTHON_VERSION}'

      - name: 📦 安装依赖
        run: |
          cd {BACKEND_DIR}
          pip install -r requirements.txt

      - name: 🧪 运行测试
        run: |
          cd {BACKEND_DIR}
          {TEST_COMMAND}
```

### 模板 C：部署到 ECS

```yaml
name: Deploy to ECS

on:
  push:
    branches: [{BRANCH}]
    paths: ['{DEPLOY_PATH}']
  workflow_dispatch:
    inputs:
      confirm:
        description: '确认部署'
        required: true
        default: 'yes'

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch' && github.event.inputs.confirm == 'yes' || github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4

      - name: 📤 上传文件到 ECS
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.ECS_HOST }}
          username: ${{ secrets.ECS_USER }}
          password: ${{ secrets.ECS_PASSWORD }}
          source: "{SOURCE_DIR}"
          target: "{TARGET_DIR}"

      - name: 🚀 远程执行部署脚本
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.ECS_HOST }}
          username: ${{ secrets.ECS_USER }}
          password: ${{ secrets.ECS_PASSWORD }}
          script: |
            {DEPLOY_SCRIPT}
```

---

## 输出格式

### 正常输出

生成文件后输出：

```markdown
## ✅ GitHub Actions 工作流已生成

### 生成的文件

| 文件 | 类型 | 触发条件 |
|------|------|---------|
| `.github/workflows/{name}.yml` | {类型} | {触发说明} |

### ⚙️ GitHub 配置指引

请在 GitHub 仓库中完成以下配置：

#### 1. 配置 Secrets

进入 **Settings → Secrets and variables → Actions → New repository secret**

| Secret 名称 | 值 | 用于 |
|-------------|-----|------|
| `QODER_PERSONAL_ACCESS_TOKEN` | Qoder 个人令牌 | AI 代码审查 |
| `ECS_HOST` | ECS 服务器 IP | 部署 |
| `ECS_USER` | SSH 用户名 | 部署 |
| `ECS_PASSWORD` | SSH 密码 | 部署 |

> 💡 Qoder 令牌获取：登录 Qoder → Settings → Personal Access Token → Generate

#### 2. 配置 Permissions

进入 **Settings → Actions → General → Workflow permissions**

- 选择 **Read and write permissions**
- 勾选 **Allow GitHub Actions to create and approve pull requests**

#### 3. 验证方法

- **AI 代码审查**：创建一个 PR，查看 Actions 标签页是否触发审查
- **CI 测试**：推送代码到 {branch}，查看测试是否通过
- **部署**：推送到触发路径，或手动触发 workflow_dispatch
```

### 拒答

```markdown
## ℹ️ 建议使用其他 CI/CD 工具

当前项目使用 {tool}，不使用 GitHub Actions。

**替代方案**：
- GitLab CI：`.gitlab-ci.yml`
- Jenkins：`Jenkinsfile`
```

---

## 约束与红线

### 硬性规则

- **MUST** 使用 `actions/checkout@v4`（不低于 v4）
- **MUST** 使用 `actions/setup-python@v5`、`actions/setup-node@v4`
- AI 代码审查 **MUST** 设置 `permissions.checks: write`，否则会报 "Resource not accessible by integration"
- AI 代码审查 **MUST** 设置 `env.FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`
- 部署工作流 **MUST** 包含 `workflow_dispatch` 手动触发入口
- **MUST NOT** 在 YAML 中硬编码密钥、密码、Token
- **MUST NOT** 生成 `git push --force` 相关步骤

### 决策规则

1. 用户未指定分支时，默认 `main`
2. Python 默认 `3.11`，Node 默认 `20`
3. PR 跳过阈值默认 `1000` 行，审查语言默认 `Chinese`
4. 部署工作流默认同时支持自动触发和手动触发
5. 用户需求不在 A/B/C 模板中时，根据描述灵活生成 YAML，遵循相同的约束红线

---

## 关联文档

- Qoder Action 文档：https://docs.qoder.com/zh/cli/qoder-action
- Qoder Action 仓库：https://github.com/QoderAI/qoder-action
- GitHub Actions 文档：https://docs.github.com/en/actions
- 项目现有工作流示例：`.github/workflows/ai-code-review.yml`
- 部署文档：`main-project/docs/DEPLOY-GITHUB-ACTIONS.md`

---

## 常见错误

### 错误 1：AI 审查报 "Resource not accessible by integration"

**现象**：Qoder Action 执行成功但无法发布审查结果
**原因**：缺少 `permissions.checks: write` 权限
**正确做法**：在工作流顶部添加 `permissions` 块，包含 `contents: read`、`pull-requests: write`、`checks: write`

### 错误 2：Node.js 版本警告

**现象**：日志中出现 "Node.js 16 actions are deprecated" 警告
**原因**：某些 Action 依赖旧版 Node.js
**正确做法**：添加 `env.FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`

### 错误 3：部署工作流触发范围过大

**现象**：任何文件修改都触发部署
**原因**：`on.push` 没有配置 `paths` 过滤
**正确做法**：使用 `paths` 限定只有特定目录变更才触发，如 `paths: ['demo/**']`
