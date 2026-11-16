---
name: cy-dataworks-compat
description: 指导 AI 在阿里云专有云 3.16.2/3.18.6 环境下正确处理 DataWorks OpenAPI 兼容性问题。涵盖 ListFiles 兼容、endpoint 注册、节点归属校验、异步接口轮询、SDK 版本约束等最佳实践。适用于 DataWorks 专有云部署、API 调用、SDK 集成场景。
---

# DataWorks 专有云 OpenAPI 兼容指南

适用环境：阿里云专有云 3.16.2 / 3.18.6
SDK 版本：aliyun-java-sdk-dataworks-public 5.0.0 + aliyun-java-sdk-core 4.7.1

## 1. Endpoint 注册（必须）

专有云 endpoint 与公有云不同，**必须**通过 `DefaultProfile.addEndpoint` 手动注册：

```java
DefaultProfile.addEndpoint(regionId, "dataworks-public", endpoint);
```

- `regionId`：专有云实际 region（如 `dataworks-public`）
- `endpoint`：专有云实际地址（如 `dataworks-public-vpc.xxx`）

> 不注册会报 endpoint 找不到错误。

## 2. ListFiles API 兼容

### 问题
专有云 SDK 的 ListFiles 请求**不支持** `setExactFileName` 方法。

### 解决方案
使用 `setKeyword` 模糊匹配 + 精确名称过滤：

```java
ListFilesRequest request = new ListFilesRequest();
request.setProjectId(projectId);
request.setKeyword(fileName); // 模糊匹配
// 遍历结果精确过滤
for (File file : response.getData().getFiles()) {
    if (fileName.equals(file.getFileName())) {
        return file;
    }
}
```

### 注意事项
- Keyword 匹配范围较广，必须做精确名称二次过滤
- 分页查询时需遍历所有页，PageNumber 从 1 开始

## 3. 节点归属校验

### 问题
专有云 SDK **无** `getAbsoluteFolderPath` 方法，无法通过文件夹路径判断节点归属。

### 解决方案
通过 `businessId` 比对校验节点归属：

```java
// 1. 获取当前业务流程的 businessId
Long currentBusinessId = findOrCreateBusiness(projectId, businessName);

// 2. 通过 ListFiles 查询文件的 businessId
Long fileBusinessId = file.getBusinessId();

// 3. 比对
if (currentBusinessId.equals(fileBusinessId)) {
    // 归属正确，跳过
} else {
    // 节点名冲突，需人工处理
    throw new RuntimeException("节点归属冲突");
}
```

> **禁止**依赖文件夹路径拼接来判断归属，专有云路径规则与公有云不同。

## 4. CreateFile 异步处理

CreateFile 是**异步接口**，调用成功后文件不会立即可见。

### 处理流程
1. 调用 CreateFile，获取 fileId
2. 轮询 ListFiles（每 1s 一次，最多 15 次）等待文件可见
3. 查到文件后校验 businessId 确认归属正确
4. 超过 15s 仍未查到则报错

```java
for (int i = 0; i < 15; i++) {
    Thread.sleep(1000);
    File file = queryFileByName(projectId, fileName);
    if (file != null) {
        // 校验 businessId
        return file;
    }
}
throw new RuntimeException("节点创建超时");
```

## 5. SubmitFile 异步处理 + GetDeployment 轮询

SubmitFile 是**异步接口**，返回 `deploymentId`，需轮询发布状态。

### 处理流程
1. 调用 SubmitFile，获取 deploymentId
2. 通过 GetDeployment 轮询（每 2s 一次，最多 30 次 = 60s）
3. 状态判断：
   - `Status=0`：就绪，继续等待
   - `Status=1`：成功，继续下一步
   - `Status=2`：失败，抛出异常并附带错误信息

```java
for (int i = 0; i < 30; i++) {
    Thread.sleep(2000);
    GetDeploymentResponse resp = getDeployment(projectId, deploymentId);
    Integer status = resp.getData().getDeployment().getStatus();
    if (status == 1) return; // 成功
    if (status == 2) throw new RuntimeException("发布失败: " + resp.getData().getDeployment().getErrorMessage());
}
throw new RuntimeException("发布超时");
```

### 提交顺序（关键）
**必须**按拓扑顺序提交节点（上游先于下游）：
```
起始节点(VS_) → 信号监测(CK_DB_) → DI节点(T_) → ODS转存(ODS_) → 结束节点(VE_)
```
否则 DataWorks 会报错：`当前节点依赖的父节点输出名不存在`。

## 6. API 重试机制

所有 API 调用必须包装重试逻辑：

### 规则
- 最大重试：3 次
- 退避策略：指数退避（1s → 2s → 4s）
- **可重试**异常：Throttling / ServiceUnavailable / InternalError / SystemBusy / HTTP 5xx（500/502/503/504）/ 超时 / 连接异常
- **不可重试**异常：参数错误、权限不足等业务逻辑错误 → 直接抛出

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

## 7. 文件 ID 缓存与已提交节点缓存

### 文件 ID 缓存（ListFiles 预加载）
- 启动时分页 ListFiles 加载项目全部文件到 `Map<projectId, Map<fileName, fileId>>`
- 新建文件同步写入缓存
- BAK 工作空间按需加载（首次使用时）
- 缓存未命中时降级为 API 查询
- **并发安全**：内层用 ConcurrentHashMap；computeIfAbsent 内禁止操作外层缓存（防 Recursive update）

### 已提交节点缓存（ListNodes 预加载）
- 启动时分页 ListNodes（ProjectEnv=PROD）加载已提交节点到 `Map<projectId, Set<nodeName>>`
- 只有 SubmitFile 成功的节点才有 NodeId
- 提交前检查缓存：已提交则跳过
- 缓存未命中降级为 ListNodes 精确查询

## 8. 文件类型常量

| 节点类型 | FileType 值 |
|---------|------------|
| VIRTUAL（虚拟节点） | 99 |
| SHELL（Shell 脚本） | 6 |
| DI（数据集成） | 23 |

## 9. 常见错误码与处理

| 错误码/现象 | 原因 | 处理 |
|------------|------|------|
| `1201111368: 父节点输出名不存在` | 节点提交顺序错误 | 按拓扑顺序提交 |
| ListFiles 返回空 | 专有云不支持 ExactFileName | 改用 Keyword + 精确过滤 |
| endpoint 找不到 | 未注册专有云 endpoint | addEndpoint 注册 |
| `Parse exception` (DDL) | MaxCompute DDL 子句顺序错误 | 按 列定义→COMMENT→PARTITIONED BY→LIFECYCLE 顺序 |
| GetDeployment Status=2 | 发布包执行失败 | 查看 ErrorMessage 定位原因 |

## 10. 检查清单

在专有云环境部署 DataWorks 相关应用时，逐项确认：

- [ ] Endpoint 已通过 DefaultProfile.addEndpoint 注册
- [ ] ListFiles 使用 setKeyword + 精确过滤（非 setExactFileName）
- [ ] 节点归属通过 businessId 校验（非文件夹路径）
- [ ] CreateFile 后有异步等待逻辑（轮询 ListFiles）
- [ ] SubmitFile 后有 GetDeployment 轮询逻辑
- [ ] 节点按拓扑顺序提交
- [ ] 所有 API 调用有重试 + 退避包装
- [ ] 缓存使用 ConcurrentHashMap，避免 Recursive update
