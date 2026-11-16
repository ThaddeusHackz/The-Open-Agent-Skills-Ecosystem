---
name: git-push-merge
description: 将当前本地分支推送并合并到指定的远程目标分支。通过 GitLab API 自动创建合并请求并执行合并，最后切换到目标分支并清理临时分支。
---

# Git Push & Merge to Target Branch

## Description
将当前本地分支推送并合并到指定的远程目标分支。通过 GitLab API 自动创建合并请求并执行合并，最后切换到目标分支并清理临时分支。

## Arguments
- `<target-branch>`: 目标分支名称（如 `dev`、`master`、`main`）

## Execution Steps

### 1. 获取当前分支信息
```bash
git branch --show-current
```
记录当前分支名称为 `CURRENT_BRANCH`。

### 2. 检查当前分支是否有远程跟踪分支
```bash
git ls-remote --heads origin {CURRENT_BRANCH}
```
- 如果输出非空 → 远程分支已存在（走**分支 A 流程**）
- 如果输出为空 → 远程分支不存在（走**分支 B 流程**）

### 3. 获取 GitLab 访问令牌
使用 `git credential fill` 获取仓库凭证：
```bash
echo "url={REMOTE_HOST}" | git credential fill
```
其中 `REMOTE_HOST` 从 `git remote get-url origin` 提取（取域名部分）。

然后通过 OAuth2 获取访问令牌：
```bash
curl.exe -s --request POST "{REMOTE_URL}/oauth/token" --data "grant_type=password&username={USERNAME}&password={PASSWORD}"
```
记录返回的 `access_token`。

### 4. 查找 GitLab 项目 ID
```bash
curl.exe -s "{REMOTE_URL}/api/v4/projects?search={PROJECT_NAME}&per_page=20" -H "Authorization: Bearer {ACCESS_TOKEN}"
```
从返回结果中匹配 `path_with_namespace` 与远程仓库路径一致的项目，记录其 `id`。

### 5. 执行分支流程

---

#### 分支 A 流程（远程分支已存在）

**5A.1 创建临时分支**
```bash
git checkout -b {CURRENT_BRANCH}-temp
```

**5A.2 推送临时分支到远程**
```bash
git push -u origin {CURRENT_BRANCH}-temp
```

**5A.3 创建合并请求（GitLab API）**

使用 `curl.exe --%` 和 `--data` 传递 JSON（PowerShell 兼容性）：
```bash
curl.exe --% -s --request POST "{REMOTE_URL}/api/v4/projects/{PROJECT_ID}/merge_requests" -H "Authorization: Bearer {ACCESS_TOKEN}" -H "Content-Type: application/json" --data "{\"source_branch\":\"{CURRENT_BRANCH}-temp\",\"target_branch\":\"{TARGET_BRANCH}\",\"title\":\"Merge {CURRENT_BRANCH}-temp into {TARGET_BRANCH}\"}"
```
记录返回的 `iid`（合并请求编号）。

**5A.4 合并合并请求**

等待 5 秒让 GitLab 准备合并状态：
```bash
timeout 5
```

然后执行合并：
```bash
curl.exe --% -s --request PUT "{REMOTE_URL}/api/v4/projects/{PROJECT_ID}/merge_requests/{IID}/merge" -H "Authorization: Bearer {ACCESS_TOKEN}"
```
验证返回的 `state` 为 `"merged"`。

**5A.5 切换到目标分支并拉取最新代码**
```bash
git checkout {TARGET_BRANCH}
git pull origin {TARGET_BRANCH}
```

**5A.6 清理临时分支**
```bash
git branch -d {CURRENT_BRANCH}-temp
git push origin --delete {CURRENT_BRANCH}-temp
```

---

#### 分支 B 流程（远程分支不存在）

**5B.1 直接推送当前分支到远程**
```bash
git push -u origin {CURRENT_BRANCH}
```

**5B.2 创建合并请求（GitLab API）**
```bash
curl.exe --% -s --request POST "{REMOTE_URL}/api/v4/projects/{PROJECT_ID}/merge_requests" -H "Authorization: Bearer {ACCESS_TOKEN}" -H "Content-Type: application/json" --data "{\"source_branch\":\"{CURRENT_BRANCH}\",\"target_branch\":\"{TARGET_BRANCH}\",\"title\":\"Merge {CURRENT_BRANCH} into {TARGET_BRANCH}\"}"
```
记录返回的 `iid`。

**5B.3 合并合并请求**

等待 5 秒后执行合并：
```bash
timeout 5
```
```bash
curl.exe --% -s --request PUT "{REMOTE_URL}/api/v4/projects/{PROJECT_ID}/merge_requests/{IID}/merge" -H "Authorization: Bearer {ACCESS_TOKEN}"
```
验证返回的 `state` 为 `"merged"`。

**5B.4 切换到目标分支并拉取最新代码**
```bash
git checkout {TARGET_BRANCH}
git pull origin {TARGET_BRANCH}
```

**5B.5 清理当前分支**
```bash
git branch -d {CURRENT_BRANCH}
git push origin --delete {CURRENT_BRANCH}
```

---

## Important Notes

1. **PowerShell 兼容性**: 所有包含 JSON 的 `curl` 命令必须使用 `curl.exe --%` 以确保参数正确传递，避免 PowerShell 引号解析问题。
2. **凭证安全**: 使用 `git credential fill` 获取凭证，不要硬编码用户名密码。
3. **合并等待**: 创建 MR 后需等待数秒让 GitLab 计算合并状态，否则合并可能失败。
4. **错误处理**:
   - 如果 OAuth2 认证失败（401），提示用户检查 Git 凭证配置
   - 如果项目查找返回 404，提示用户检查远程仓库地址
   - 如果 MR 创建返回 "Bad Request"，检查 PowerShell 引号转义
   - 如果合并返回冲突错误，提示用户手动解决冲突
5. **分支命名**: 临时分支使用 `{CURRENT_BRANCH}-temp` 后缀，确保不与已有分支冲突。
