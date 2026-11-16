---
name: cy-dataworks-node-deploy
description: 指导 AI 通过 DataWorks OpenAPI 完成业务流程和调度节点的创建、更新、提交与发布。涵盖文件 ID 缓存、已提交节点缓存、异步接口轮询、拓扑顺序提交、跨空间部署、API 重试等最佳实践。适用于 DataWorks 自动化部署、节点管理、工作流发布场景。
---

# DataWorks 节点部署与发布指南

适用环境：阿里云专有云 3.16.2 / 3.18.6 或公有云
SDK 版本：aliyun-java-sdk-dataworks-public 5.0.0 + aliyun-java-sdk-core 4.7.1

## 1. 部署流程总览

```
创建业务流程 (CreateBusiness)
    ↓
创建节点文件 (CreateFile) — 异步
    ↓
等待文件可见 (ListFiles 轮询)
    ↓
设置节点 OutputList (UpdateFile)
    ↓
提交到运维中心 (SubmitFile) — 异步
    ↓
轮询发布状态 (GetDeployment)
```

## 2. 业务流程管理

### 2.1 创建业务流程

```java
CreateBusinessRequest request = new CreateBusinessRequest();
request.setProjectId(projectId);
request.setProjectIdentifier(projectName);
request.setBusinessName(businessName);
```

### 2.2 查询业务流程

使用 `ListBusiness` 按 keyword 模糊查找，再精确匹配名称：

```java
ListBusinessRequest request = new ListBusinessRequest();
request.setProjectId(projectId);
request.setKeyword(businessName);
// 遍历结果精确匹配 businessName
```

### 2.3 获取或创建

推荐实现 `findOrCreateBusiness(projectId, projectName, businessName)`：
1. 先 ListBusiness 查询
2. 存在则返回 businessId
3. 不存在则 CreateBusiness

## 3. 文件/节点操作

### 3.1 文件类型常量

| 节点类型 | FileType 值 |
|---------|------------|
| VIRTUAL（虚拟节点） | 99 |
| SHELL（Shell 脚本） | 6 |
| DI（数据集成） | 23 |

### 3.2 创建节点 (CreateFile)

```java
CreateFileRequest request = new CreateFileRequest();
request.setProjectId(projectId);
request.setFileName(nodeName);           // 大写
request.setFileType(fileType);           // 99/6/23
request.setContent(content);             // 节点内容
request.setBusinessId(businessId);
request.setInputList(inputList);         // 上游依赖
request.setOutputList(outputList);       // 输出名
request.setParaValue(paraValue);         // 调度参数
request.setCronExpression(cron);         // Cron 表达式
```

### 3.3 CreateFile 异步等待

CreateFile 是异步接口，调用后需轮询等待文件可见：

```java
for (int i = 0; i < 15; i++) {
    Thread.sleep(1000);
    File file = queryFileByName(projectId, fileName);
    if (file != null) {
        // 校验 businessId 归属
        return file;
    }
}
throw new RuntimeException("节点创建超时：" + fileName);
```

### 3.4 更新节点 (UpdateFile)

#### 更新节点内容
```java
UpdateFileRequest request = new UpdateFileRequest();
request.setProjectId(projectId);
request.setFileId(fileId);
request.setContent(newContent);
```

#### 更新 OutputList（修复依赖连线）
```java
UpdateFileRequest request = new UpdateFileRequest();
request.setProjectId(projectId);
request.setFileId(fileId);
request.setOutputList(outputList);
```

> OutputList 更新失败建议 WARN 但不阻断流程；Content 更新失败应抛异常。

### 3.5 节点归属校验

**禁止**依赖文件夹路径拼接判断归属（专有云 SDK 无 `getAbsoluteFolderPath`）。

通过 `businessId` 比对：

```java
Long currentBusinessId = findOrCreateBusiness(...);
Long fileBusinessId = file.getBusinessId();

if (!currentBusinessId.equals(fileBusinessId)) {
    throw new RuntimeException("节点归属冲突，需人工处理");
}
```

## 4. 节点提交与发布

### 4.1 提交节点 (SubmitFile)

```java
SubmitFileRequest request = new SubmitFileRequest();
request.setProjectId(projectId);
request.setFileId(fileId);
request.setComment("submit by automation");
// 返回 deploymentId
String deploymentId = response.getData().getDeployment().getDeploymentId();
```

### 4.2 GetDeployment 轮询

```java
for (int i = 0; i < 30; i++) {
    Thread.sleep(2000);
    GetDeploymentResponse resp = getDeployment(projectId, deploymentId);
    Integer status = resp.getData().getDeployment().getStatus();
    if (status == 1) return;          // 成功
    if (status == 2) throw new RuntimeException("发布失败: " + resp.getData().getDeployment().getErrorMessage());
}
throw new RuntimeException("发布超时");
```

状态说明：
- `0`：就绪/处理中
- `1`：成功
- `2`：失败

### 4.3 拓扑顺序提交（关键）

必须按依赖顺序提交，上游先于下游：

```
起始节点(VS_) → 信号监测(CK_DB_) → DI节点(T_) → ODS转存(ODS_) → 结束节点(VE_)
```

否则 DataWorks 报错：`1201111368: 当前节点依赖的父节点输出名不存在`。

## 5. 文件 ID 缓存

### 5.1 设计目标

避免每次操作都调用 ListFiles，提升性能。

### 5.2 缓存结构

```java
Map<Long, Map<String, Long>> fileIdCache;
// projectId -> (fileName -> fileId)
```

### 5.3 加载策略

- 启动时分页 ListFiles 预加载主工作空间全部文件
- BAK 工作空间按需加载（首次使用时）
- 新建文件后同步写入缓存
- 缓存未命中时降级为 API 查询

### 5.4 并发安全

- 内层缓存使用 `ConcurrentHashMap`
- `computeIfAbsent` 内禁止操作外层缓存，防止 `Recursive update`
- `buildFileIdMap` 抽离为纯函数，不操作外层缓存

## 6. 已提交节点缓存

### 6.1 设计目标

避免重复 SubmitFile，跳过已提交节点。

### 6.2 缓存结构

```java
Map<Long, Set<String>> submittedNodeCache;
// projectId -> Set<nodeName>
```

### 6.3 加载策略

- 启动时分页 ListNodes（ProjectEnv=PROD）预加载
- 只有 SubmitFile 成功过的节点才有 NodeId
- BAK 工作空间按需加载
- 缓存未命中时降级为 ListNodes 精确查询

### 6.4 提交判断

```java
if (submittedNodeCache.get(projectId).contains(nodeName)) {
    // [SKIP-SUBMIT] 已提交
} else {
    SubmitFile(...);
    markNodeSubmitted(projectId, nodeName);
}
```

## 7. 跨工作空间部署

### 7.1 场景

主流程部署到主工作空间，备份流程（BAK）部署到备份工作空间。

### 7.2 实现方式

```java
deployFlow(job, flowDef, nodeContents, strategy, 
           mainProjectId, mainProjectName, isSubmit);

deployFlow(job, bakFlowDef, bakNodeContents, strategy, 
           bakProjectId, bakProjectName, isSubmit);
```

### 7.3 跨空间依赖

BAK DI 节点的 InputList 需要包含主工作空间的 ODS Shell 节点输出：

```
${mainProjectName}.${odsNodeName}
```

## 8. API 重试机制

所有 DataWorks API 调用必须包装重试逻辑：

| 项目 | 规则 |
|------|------|
| 最大重试 | 3 次 |
| 退避间隔 | 指数退避：1s → 2s → 4s |
| 可重试异常 | Throttling / ServiceUnavailable / InternalError / SystemBusy / HTTP 5xx / 超时 / 连接异常 |
| 不可重试异常 | 参数错误、权限不足等业务错误 → 直接抛出 |

```java
private <T> T executeWithRetry(Supplier<T> action, String actionName) {
    int maxRetries = 3;
    for (int attempt = 0; attempt <= maxRetries; attempt++) {
        try {
            return action.get();
        } catch (Exception e) {
            if (!isRetryable(e) || attempt == maxRetries) throw e;
            long delay = (long) Math.pow(2, attempt) * 1000;
            Thread.sleep(delay);
        }
    }
}
```

## 9. 常见错误与处理

| 错误码/现象 | 原因 | 处理 |
|------------|------|------|
| `1201111368: 父节点输出名不存在` | 提交顺序错误 | 按拓扑顺序提交 |
| CreateFile 后 ListFiles 查不到 | 异步延迟 | 轮询等待 15s |
| GetDeployment Status=2 | 发布失败 | 查看 ErrorMessage |
| 节点归属冲突 | 同名节点在其他流程下 | 人工处理 |
| 缓存 Recursive update | computeIfAbsent 内操作外层缓存 | 抽离纯函数，避免内层 put |

## 10. 检查清单

部署 DataWorks 节点前确认：

- [ ] 业务流程已存在或已创建
- [ ] 文件 ID 缓存已预加载
- [ ] 节点名称统一大写
- [ ] InputList / OutputList 格式正确
- [ ] 节点按拓扑顺序提交
- [ ] SubmitFile 后已轮询 GetDeployment
- [ ] BAK 流程的 projectId/projectName 已配置
- [ ] 跨空间依赖使用 `${projectName}.${nodeName}` 格式
