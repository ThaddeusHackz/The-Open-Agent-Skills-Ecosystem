---
name: openplatform-dev
description: fsg-openplatform 开放平台模块开发指南。用于新增第三方系统对接、Retrofit拦截器开发、内部转发接口开发。当需要在开放平台模块新增三方API集成、修改拦截器、添加InnerController接口时使用。
---

# 开放平台模块开发指南

## 模块定位

`fsg-openplatform` 是系统对外统一的三方API集成网关，作为中间层对接多个外部第三方系统。
应用名 `lzkj-openapi`，端口 `29504`，包路径 `com.lzkj.openapi`。

## 已对接系统

| 系统 | Client | Interceptor | Service | InnerController |
|------|--------|-------------|---------|-----------------|
| 北森HR | `IBeiSenServiceClient` | `RetrofitBeiSenInterceptor` | `IBeiSenService` | `BeiSenInnerController` |
| B站人脸 | `IBiliBiliFaceClient` | `RetrofitBiliFaceBatchInterceptor` | `IBiliBiliService` | `BiliBiliController` |
| e签宝 | `IEsignServiceClient` | `RetrofitEsignInterceptor` | `IEsignApiService` | `EsignInnerController` |
| 感恩科技 | `IGratitudeTechClient` | `RetrofitGratitudeTechInterceptor` | `IGratitudeTechApiService` | `GratitudeTechInnerController` |
| IMS灵工中台 | `IImsServiceClient` | `RetrofitInterceptor` | `IImsService` | `ImsInnerController` |
| 简道云文件 | `IJdyFileServiceClient` | `RetrofitJdyFileInterceptor` | — (直接Client调用) | — |
| 简道云结算 | `IJdySltServiceClient` | `RetrofitJdySltInterceptor` | `IJdySltService` | `JdySltController` |
| Moka招聘 | `IMokaServiceClient` | `RetrofitMokaInterceptor` | `IMokaService` | `MokaInnerController` |
| 健合/丝芙兰 | `ISephoraClient` | `RetrofitJianheInterceptor` | — | — |

## 模块架构（5层结构）

新增三方系统对接需按以下5层结构依次创建：

```
Layer 1: Client (Retrofit接口)
    ↓ 绑定
Layer 2: Interceptor (签名/鉴权/日志)
    ↓ 注入
Layer 3: Service 接口 + Impl (业务编排/Token管理/异常处理)
    ↓ 调用
Layer 4: InnerController (内部微服务转发端点)
    ↓ 被调用
Layer 5: 其他微服务通过 Feign 调用 InnerController
```

### 各层职责

| 层 | 包路径 | 职责 |
|----|--------|------|
| Client | `remote.client` | 声明式HTTP接口，`@RetrofitClient` + `@Intercept` |
| Interceptor | `interceptor` | 签名鉴权、请求/响应日志、`LogEvent`事件发布 |
| Service | `remote.service` / `remote.Impl` | Token缓存、结果解析、异常封装 |
| InnerController | `controller.OpenApiDispatchService` | 暴露 `/innerOpenapi/{system}/*` 端点 |
| 数据模型 | `domain.dto` / `domain.vo` / `domain.entity` | 请求/响应DTO、返回VO、持久化Entity |

## 新增三方系统对接流程

以对接 "FooSystem" 为例，完整步骤：

### Step 1: Nacos 配置

在 Nacos 的 `lzkj-openapi` 配置文件中添加：

```yaml
retrofit:
  variables:
    fooUrl: https://api.foosystem.com
```

如果有密钥类配置：

```yaml
otherConfig:
  foo:
    appId: xxx
    appSecret: xxx
```

### Step 2: 创建 Client

路径：`com.lzkj.openapi.remote.client.IFooClient`

关键注解：
- `@Intercept(handler = RetrofitFooInterceptor.class)` — 绑定拦截器
- `@RetrofitClient(baseUrl = "${retrofit.variables.fooUrl}")` — 声明baseUrl

详见 [templates.md](templates.md) 中的 Client 模板。

### Step 3: 创建 Interceptor

路径：`com.lzkj.openapi.interceptor.RetrofitFooInterceptor`

必须继承 `BasePathMatchInterceptor`，实现 `doIntercept(Chain chain)` 方法。

拦截器两种模式：
- **纯日志模式**：仅记录请求/响应日志，发布 `LogEvent`（参考 `RetrofitGratitudeTechInterceptor`）
- **签名鉴权模式**：在日志基础上增加签名计算，修改请求Header（参考 `RetrofitEsignInterceptor`）

关键约定：
- 必须通过 `ApplicationEventPublisher` 发布 `LogEvent` 事件（异步持久化到 `log_remote` 表）
- `LogEvent` 必须设置的字段：`businessType`, `url`, `reqType`(固定`Constants.COMMON_ONE`), `createdTime`, `title`, `serverCode`, `requestMethod`, `reqHeaders`, `param`
- 读取请求体用 `okio.Buffer`，读取响应体后必须用 `ResponseBody.create()` 重新构建（因为 `string()` 会消费流）

详见 [templates.md](templates.md) 中的 Interceptor 模板。

### Step 4: 创建 Service 接口 + 实现

接口路径：`com.lzkj.openapi.remote.service.IFooService`
实现路径：`com.lzkj.openapi.remote.Impl.FooServiceImpl`

Service 层职责：
- 注入 Client，调用 Retrofit 方法
- 管理 Token 缓存（如需要）
- 解析三方返回结果，统一异常处理
- 返回业务层需要的数据

### Step 5: 创建 InnerController

路径：`com.lzkj.openapi.controller.OpenApiDispatchService.FooInnerController`

关键约定：
- `@RequestMapping("/innerOpenapi/foo")` — 统一路径前缀
- `@ResultAdvice` — 响应增强注解
- 每个方法加 `@Log(title = "xxx", businessType = BusinessTypeEnum.INNER)` — 操作日志
- GET 用 `@GetMapping`，POST 用 `@PostMapping` + `@RequestBody`

详见 [templates.md](templates.md) 中的 Controller 模板。

### Step 6: 数据模型

- 请求 DTO：`domain.dto.FooXxxReqDto`（或直接使用 `fsg-common-interface` 中的共享 DTO）
- 返回 VO：`domain.vo.FooResultVO`（三方原始返回包装）
- 业务 VO：按需创建

## 拦截器开发要点

### 响应体读取（必须遵守）

```java
ResponseBody originalBody = response.body();
String bodyStr = "";
if (originalBody != null) {
    bodyStr = originalBody.string();  // 消费流
    // 必须重新构建响应体，否则下游无法读取
    ResponseBody newBody = ResponseBody.create(bodyStr, originalBody.contentType());
    response = response.newBuilder().body(newBody).headers(response.headers()).build();
}
```

### LogEvent 发布（必须遵守）

```java
LogEvent saveEvent = new LogEvent();
// ... 设置各字段 ...
try {
    response = chain.proceed(request);
    // ... 设置响应字段 ...
} catch (IOException e) {
    // ... 设置异常字段 ...
} finally {
    publisher.publishEvent(saveEvent);  // 必须在 finally 中发布
}
```

### multipart 文件上传场景

对于 multipart 文件上传（如简道云文件上传），拦截器中**不能**读取请求体（会触发二进制流读取导致乱码），需跳过 body 读取。同时可在 Client 方法上添加 `@Logging(enable = false)` 禁用 retrofit-spring-boot-starter 的日志打印。

## Nacos 配置项约定

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `retrofit.variables.{system}Url` | 三方系统baseUrl | `retrofit.variables.fooUrl` |
| `otherConfig.{system}.appId` | 三方应用ID | `otherConfig.foo.appId` |
| `otherConfig.{system}.appSecret` | 三方应用密钥 | `otherConfig.foo.appSecret` |

配置在 Nacos 的 `lzkj-openapi` 应用下，按环境（dev/test/prod）区分 namespace。

## 关键依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| `retrofit-spring-boot-starter` (lianjiatech) | 2.3.13 | Retrofit Spring Boot 集成核心框架 |
| `retrofit` (squareup) | 2.11.0 | Retrofit 底层库 |
| `hutool-all` | 5.8.38 | 工具库 |

## 日志记录规范

- 拦截器层：通过 `LogEvent` 事件异步持久化到 `log_remote` 表
- Service 层：`log.info` 记录关键业务参数和返回状态码，`log.error` 记录异常
- Controller 层：`@Log` 注解自动记录操作日志
- 日志格式：`log.info("描述，param1={}，param2={}", val1, val2)` — 使用占位符，不用字符串拼接

## 代码模板

完整的代码模板请参考 [templates.md](templates.md)。
