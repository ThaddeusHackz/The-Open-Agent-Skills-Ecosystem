---
name: yunxiao-appstack-deploy
description: 通过云效 AppStack API 发布应用到指定环境。当用户要求发布/部署/上线某个应用到 dev/test/uat/pre/prod 环境时使用此技能。触发词：发布、部署、上线、deploy、发dev、发测试、发生产。
version: 1.1.0
---

# 云效 AppStack 应用发布

## 应用名称解析

技能执行前先读取项目配置文件 `.qoder/config/appstack-deploy.json`，获取应用名称映射：

```json
{
  "apps": {
    "frontend": "前端appName",
    "backend": "后端appName"
  }
}
```

用户说"发前端/发后端"时，从配置文件自动映射为对应 appName。

**如果配置文件不存在**：向用户询问完整的 appName，并提示用户可创建配置文件以便后续免输入。

## 输入参数

用户提供以下信息（如缺少则询问）：

- **应用名称**（appName）：自动从配置文件映射，或询问用户
- **发布分支**（branchName）：如 `main`、`master`、`feature/xxx`
- **目标环境**：dev / test / uat（预发）/ pre（预生产）/ prod（生产）
- **关联工作项**（workItems，可选）：云效组织若开启"变更必须关联工作项"策略，需用户提供工作项 ID（形如 `nx-xxxxxxxx` 或纯数字）；本 skill 已内置规避方案（详见步骤 4）

## 完整流程

### 步骤 1：获取组织信息

调用 `mcp__yunxiao__get_current_organization_info`（无参数），获取：
- `lastOrganization` → organizationId
- `userId` → ownerId

### 步骤 2：获取代码仓库信息

调用 `mcp__yunxiao__list_application_sources`：
- 参数：`organizationId`, `appName`
- 从返回结果提取：
  - `sn` → appCodeRepoSn
  - `identifier` → 仓库标识（如 `busyming_mcp_backend`），后面 params 要用
  - `repoUrl` → 仓库地址

### 步骤 3：获取发布流程和阶段

调用 `mcp__yunxiao__list_app_release_workflows`：
- 参数：`organizationId`, `appName`
- 从返回的 `releaseStages` 数组中，根据用户指定的环境匹配阶段：

| 用户说 | 匹配阶段名 | 标签 |
|--------|-----------|------|
| dev / 开发 | 开发阶段 | dev |
| test / 测试 | 测试阶段 | test |
| uat / 预发 | 预发阶段 | prepub |
| pre / 预生产 | 预生产阶段 | production（第4个） |
| prod / 生产 | 生产阶段 | production（第5个） |

- 记录 `releaseWorkflowSn`（流程 SN）和匹配阶段的 `sn`（releaseStageSn）

**注意**：pre 和 prod 的标签都是 `production`，需按 `order` 字段区分（order=4 是预生产，order=5 是生产）。

### 步骤 4：决策 appReleaseSn（关键改进）

云效可能开启"变更必须关联工作项"组织策略（`ChangeRequestMustBindWorkItem`，HTTP 422），直接创建 CR 会失败。按下述优先级尝试：

#### 4.1【首选】复用已有 CR

调用 `mcp__yunxiao__list_appstack_change_requests`：
- 参数：`organizationId`, `appName`, `pageSize: 30`, `state: ["DEVELOPING", "INTEGRATING", "RELEASED"]`
- 若 `records` 非空，取第一条的 `sn` 作为 `appReleaseSn`
- 已 RELEASED 的 CR 也可复用（步骤 5 通过 `params.branchRepoInfo` 覆盖为目标分支，不受 CR 原分支限制）

#### 4.2【次选】新建 CR（需工作项）

调用 `mcp__yunxiao__create_appstack_change_request`：
- 参数：
  - `organizationId`, `appName`
  - `appCodeRepoSn`：步骤 2 的 sn
  - `branchName`：用户指定的分支
  - `ownerId`：步骤 1 的 userId
  - `title`：如 `"发布{环境}-{分支名}"`
  - **`workItems`：字符串数组，形如 `["nx-xxxxxxxx"]`，不可为空数组、不可省略**

**报错处理**：
- 422 `ChangeRequestMustBindWorkItem`：向用户索要工作项 ID 后重试；当前 token 通常无 `search_workitems` 权限（403），不要尝试自动搜索工作项
- 403：token 的「变更」权限不是「读写」，让用户升级

#### 4.3【兜底】省略 appReleaseSn 直接执行

若 4.1 / 4.2 都拿不到 CR sn，且应用历史无任何 CR 记录（例如前端类应用），可在步骤 5 的 `execution` 中**不传** `appReleaseSn` 字段直接触发（云效 API 该字段为可选）。通过步骤 6 的 metadata 校验实际使用的分支/commit 是否正确即可。

### 步骤 5：执行发布阶段

调用 `mcp__yunxiao__execute_app_release_stage`：
- 参数：
  - `organizationId`, `appName`
  - `releaseWorkflowSn`：步骤 3 获取
  - `releaseStageSn`：步骤 3 匹配的阶段 sn
  - `execution`：
    ```json
    {
      "appReleaseSn": "步骤4拿到的CR sn（4.3路径可省略此字段）",
      "params": {
        "{identifier}": "{branchName}",
        "branchRepoInfo": "[{\"sign\":\"{identifier}\",\"repo\":\"{repoUrl}\",\"name\":\"{identifier}\",\"baseBranch\":{\"branchName\":\"{branchName}\"},\"featureBranchs\":[],\"appName\":\"{appName}\",\"appstackMode\":\"FREE_BRANCH_MODE\"}]"
      }
    }
    ```

**params 关键字段说明**：
- `{identifier}`：步骤 2 获取的仓库标识（如 `busyming_mcp_backend`），值设为分支名
- `branchRepoInfo`：JSON 字符串，`baseBranch.branchName` 设为目标分支名
- `appstackMode`：固定为 `"FREE_BRANCH_MODE"`

**如果只传 `{"branch": "main"}` 会不生效，流水线仍用仓库默认分支！**

返回值中记录 `pipelineRunId`（即执行序号 executionNumber，步骤 6 会用到）。

### 步骤 6：查询执行状态与结果验证

**6.1 轮询状态**

调用 `mcp__yunxiao__list_app_release_stage_runs`：
- 参数：`organizationId`, `appName`, `releaseWorkflowSn`, `releaseStageSn`, `sort: "desc"`, `perPage: 1`
- 检查最新一条记录的 `state`：`RUNNING` / `SUCCESS` / `FAILED`

如果仍在 `RUNNING`，等待 30~60 秒后重新查询，最多轮询 4~6 次（约 2~4 分钟）。

**6.2 SUCCESS 后校验分支/commit**

调用 `mcp__yunxiao__list_app_release_stage_metadata`（推荐用它做发布结果核对，而不是 `get_app_release_stage_pipeline_run`——后者经常返回空对象）：
- 参数：`organizationId`, `appName`, `releaseWorkflowSn`, `releaseStageSn`, `executionNumber`（即步骤 5 的 pipelineRunId）
- 核对返回的 `releaseBranch` 和 `releaseRevision` 是否与目标分支和最新 commit 一致

**6.3 FAILED 处理**

- **首次失败大概率是瞬态构建问题**：用同一套参数再执行一次 `execute_app_release_stage`（重触发流水线），实践中前端发布首次失败后原参重发即通过
- 如果连续两次失败：`get_pipeline_run` 通常报 403（token 无流水线查看权限），改用云效 Web 端查看流水线日志定位构建错误
- `retry_app_release_stage_pipeline` 需要 `jobId`，而 `get_app_release_stage_pipeline_run` 常返回空对象拿不到 jobId，因此**不建议依赖 retry 接口**，直接重发 `execute_app_release_stage` 更可靠

## 前后端一次性发同一分支

用户要求"发前后端到 dev / 同分支发布"时，对配置文件中的 `frontend` 和 `backend` 两个 appName 分别执行完整流程（步骤 1~6），可并行触发步骤 5，最后各自轮询状态。

## 注意事项

- Token 权限要求：「变更」和「研发阶段」必须为「读写」
- **`search_workitems` 常返回 403**，不要用它自动查工作项；工作项 ID 需用户提供
- 已 `RELEASED` 状态的 CR 仍可复用（params.branchRepoInfo 会覆盖 CR 原分支），无需为每次发布创建新 CR
- 发布 prod 前建议先确认 test/uat 阶段已通过
- `pipelineId` 和 `pipelineRunId` 返回的是 number 类型，查流水线详情需转 string
- 发布 SUCCESS 后如涉及 DDL 迁移，先执行迁移脚本（应保证幂等）再重启后端服务
