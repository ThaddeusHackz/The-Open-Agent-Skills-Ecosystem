---
name: nextswitch-esl-starter
version: 1.0.3
description: "Integrate and troubleshoot nextswitch-esl-spring-boot-starter (Maven link.thingscloud), which connects a Spring Boot app to NextSWITCH Event Socket Layer (ESL) inbound sockets. Use when working with this starter's types or config: InboundClient, InboundClientBootstrap, InboundClientOption, ServerOption, EslEventHandler, @EslEventName, AbstractInboundClientOptionHandler, IEslEventListener, ServerConnectionListener, EslEvent, EslMessage, CommandResponse, SendMsg, SendEvent, CommandHelper, EslEventUtil, VariableUtil, prefix link.thingscloud.nextswitch.esl.inbound. Covers the Maven dependency, multi-server ESL config, event subscription (CHANNEL_CREATE, CHANNEL_ANSWER, CHANNEL_HANGUP_COMPLETE, HEARTBEAT, DTMF, BACKGROUND_JOB), api/bgapi calls (uuid_record, uuid_transfer, uuid_kill, originate, status), CDR and recording control, and diagnosing auth failures, reconnects, 'not found inbound handler for addr' and hangs. 中文场景：ESL 接入、话单、录音控制、呼叫控制、事件监听、自动装配。"
description_zh: "接入 nextswitch-esl-spring-boot-starter：Spring Boot 连接 NextSWITCH ESL，含依赖与配置、事件订阅与 handler 编写、api/bgapi 呼叫控制、话单与录音，以及认证/重连/超时排错。"
user-invocable: true
argument-hint: "<接入目标，如 订阅 CHANNEL_HANGUP_COMPLETE 出话单>"
---

# NextSWITCH ESL Spring Boot Starter

## Overview

`link.thingscloud:nextswitch-esl-spring-boot-starter` 把 NextSWITCH 的 Event Socket Layer（**inbound 模式**）封装为 Spring Boot 自动装配组件：应用启动时按配置对多台 NS 建立长连接、自动完成 `auth`、自动下发事件订阅，并把收到的 `EslEvent` 按事件名路由到标注了 `@EslEventName` 的 `EslEventHandler` Bean；同时通过 `InboundClient` 下发 `api` / `bgapi` / `sendmsg` / `sendevent` 命令。

- 坐标：`link.thingscloud:nextswitch-esl-spring-boot-starter`，当前版本 **1.0.3**（[Maven Central](https://mvnrepository.com/artifact/link.thingscloud/nextswitch-esl-spring-boot-starter)，发布前核对最新版）
- 运行要求：Java 8+、Spring Boot 2.7.x（starter 自身按 2.7.16 编译）、Netty
- 只实现 **inbound** ESL。没有 outbound socket、没有 `mkdir`/xml 事件解析
- 自动装配同时注册在 `META-INF/spring.factories`（Boot 2.x）与 `AutoConfiguration.imports`，一般无需注解；也可在配置类上加 `@EnableNextSwitchEslAutoConfiguration` 显式导入

## 落地四步

1. 加依赖（版本用 property 管理）。
2. 写 `link.thingscloud.nextswitch.esl.inbound` 配置：`servers` + `events` + `default-password`。
3. 写 `EslEventHandler`（每个关心的事件一个 `@Component`）。
4. 需要下发命令时注入 `InboundClient`，**addr 参数永远来自 `option().serverAddrOption()` 或事件回调的 `addr`**。

### 最小可用配置

```yaml
link:
  thingscloud:
    nextswitch:
      esl:
        inbound:
          default-password: ${NS_ESL_PASSWORD}   # 默认值是硬编码的 NextSWITCH098#，必须覆盖
          servers:
            - host: 10.0.0.11        # 必须是字面 IP，见「硬性约束 1」
              port: 7921             # 默认就是 7921
            - host: 10.0.0.12
              port: 7921
              password: ${NS_ESL_PASSWORD_B}
          events:
            - CHANNEL_CREATE
            - CHANNEL_ANSWER
            - CHANNEL_HANGUP_COMPLETE
            - HEARTBEAT
```

`application.properties` 形式同样可用（camelCase / kebab-case 都能绑定），但 `events` 在 properties 里要写成**逗号分隔**，理由见排错第 17 项。完整属性表与两种写法见 `references/config-reference.md`。

### 最小可用 Handler

```java
@Slf4j
@Component
@EslEventName(EventNames.CHANNEL_ANSWER)
public class ChannelAnswerEslEventHandler implements EslEventHandler {

    @Override
    public void handle(String addr, EslEvent event) {
        String uuid = EslEventUtil.getUniqueId(event);
        log.info("answered addr={} uuid={} caller={}",
                addr, uuid, EslEventUtil.getCallerCallerIdNumber(event));
    }
}
```

需要注入 `InboundClient` 或自带 `log` 时，改为继承 `AbstractEslEventHandler`（它已 `@Autowired InboundClient` 并提供 `protected Logger log`）。

`@EslEventName` 的 value 是**数组**，一个 handler 可绑定多个事件名。

## 四个扩展点

自动装配的每个 Bean 都是 `@ConditionalOnMissingBean`，声明同类型 Bean 即整体替换模板。

| 想做什么 | 实现/继承 | 替换掉的默认 Bean |
|---|---|---|
| 改写连接参数（动态服务发现、按环境换 NS） | 继承 `AbstractInboundClientOptionHandler`，实现 `intercept(InboundClientOption)` | `InboundClientOptionHandler` |
| 处理业务事件 | `@Component` + `@EslEventName` 的 `EslEventHandler`（可多个，不参与 `@ConditionalOnMissingBean`） | — |
| 兜底/未订阅事件的处理 | `@EslEventName(EslEventHandler.DEFAULT_ESL_EVENT_HANDLER)` | `defaultEventHandler` |
| 感知上下线（告警、健康检查） | 实现 `ServerConnectionListener` | `ServerConnectionListener` |
| 完全接管事件分发 | 实现 `IEslEventListener` | `IEslEventListenerTemplate` |

**务必继承 `AbstractInboundClientOptionHandler` 而不是直接实现 `InboundClientOptionHandler`**：只有抽象类会把 yml 里的 `servers` / `events` / 缓冲区 / 线程数绑定进 `InboundClientOption`，直接实现等于丢掉全部配置。`intercept()` 在绑定之后执行，可以 `clear()` 再 `addServerOption(...)`。

自定义 `IEslEventListener` 后，`@EslEventName` 路由会失效——分发注册逻辑在模板的 `afterPropertiesSet()` 里，换掉模板就得自己复刻。

## 与官方 README 示例对齐

README 的四个代码块就是本库的四个标准扩展点。新建类时沿用它们的结构，便于与文档、与 `nextswitch` 其他工程对照：

| README 示例类 | 结构 | 对应本技能 |
|---|---|---|
| `ExampleInboundClient` | `@Component` + `@Autowired InboundClient` / `@Autowired InboundClientBootstrap` | 「下发命令」 |
| `InboundClientOptionHandlerExample` | `@Component` + 继承 `AbstractInboundClientOptionHandler`，实现 `intercept(InboundClientOption)` | 「四个扩展点」 |
| `HeartbeatEslEventHandler` | `@Component` + `@EslEventName(EventNames.HEARTBEAT)` + 实现 `EslEventHandler` | 「最小可用 Handler」 |
| `ServerConnectionListenerImpl` | `@Service` + 实现 `ServerConnectionListener` | 「四个扩展点」 |

- 事件 handler 命名沿用 `<事件驼峰>EslEventHandler`（`HeartbeatEslEventHandler`、`ChannelAnswerEslEventHandler`），一个类一个事件名。
- README 的 Maven 片段把版本写成 `${nextswitch-esl.version}`，落地时要在 `<properties>` 里声明实际版本，否则依赖解析失败。
- README 的 `intercept` 示例用 `serverOptions.clear()` 后 `serverOptions.add(...)` 直接改列表：这只在**启动阶段**安全（`start()` 尚未执行）。运行期加节点必须走 `option.addServerOption(...)`，否则不会触发连接。
- README 的 `application.properties` 片段有两处笔误，照抄会踩坑，见排错第 16、17 项。

## 下发命令

`InboundClient` 的每个方法第一个参数 `addr` 都是 **`host:port` 字符串**，用来定位一条已认证的连接。取 addr 只有三种正确方式：

```java
// 1. 随机/固定挑一台（推荐做命令下发）
inboundClient.option().serverAddrOption().random();   // 还有 first() / last()

// 2. 遍历所有 NS（没有内置广播，自己循环）
inboundClient.option().serverOptions().forEach(so -> so.addr());

// 3. 事件回调里带回来的 addr，直接透传，不要自己拼字符串
```

常用形态：

```java
// 同步 api：返回 EslMessage，正文在 getBodyLines()
EslMessage resp = inboundClient.sendSyncApiCommand(addr, "status", null);

// 带超时的同步调用（Web 线程必须用这个重载）
EslMessage brief = inboundClient.sendSyncApiCommand(addr, "sofia", "status profile internal", 3);

// 异步回调，不阻塞调用线程
inboundClient.sendSyncApiCommand(addr, "show", "channels", msg -> log.info("{}", msg));

// bgapi：返回 Job-UUID，结果走 BACKGROUND_JOB 事件
String jobUuid = inboundClient.sendAsyncApiCommand(addr, "originate",
        CommandHelper.cmd("{caller_id=1001}sofia/internal/1001@10.0.0.11").arg("&echo()").toString());

// 命令类响应，判 +OK
CommandResponse ok = inboundClient.setEventSubscriptions(addr, "plain", "ALL");
if (ok.isOk()) { /* ok.getReplyText() */ }

// 控制通话中的通道：SendMsg 必须带 uuid
inboundClient.sendMessage(addr, new SendMsg(uuid)
        .addCallCommand("execute").addExecuteAppName("hangup").addExecuteAppArg("NORMAL_CLEARING"));
```

`CommandHelper.cmd(x).arg(y)` 只负责拼空格分隔的参数串，避免手写 `+ " " +`。

## 硬性约束与排错

按「现象 → 原因」直接定位，多数问题都出在前三条。

1. **`servers[n].host` 必须写字面 IP，不能写域名或 `localhost`。** 连接侧的 addr 由 `InetSocketAddress.getAddress().getHostAddress()` 生成（一定是 IP），而 `ServerOption.addr()` 是 `host + ":" + port` 字符串直拼。写成域名时两边字符串不相等：auth 阶段匹配不上，连接永远停在 `CONNECTED` 不发认证；下发命令则抛 `InboundClientException: not found inbound handler for addr`。
2. **默认端口是 7921。
3. **`servers[n].timeout-seconds` 是断线重连间隔，不是命令超时。** 传 `0` 表示回落到 `default-timeout-seconds`（默认 5）。命令超时只能通过 `sendSyncApiCommand(addr, cmd, arg, timeoutSeconds)` 重载指定。
4. **`sendSyncApiCommand(addr, cmd, arg)` 无超时阻塞**，内部是 `CountDownLatch.await()` + 按 FIFO 配对的响应队列。某条命令没等到回复时（对端不应答、连接中断），调用线程会**永久挂住，重连也不会唤醒它**；该连接的队列同时错位，后续命令会拿到别的命令的响应。Web/业务线程一律用带 `timeoutSeconds` 或 `Consumer` 的重载；带超时的重载只是放弃等待，队列错位仍在，所以异常之后要靠 `closeChannel(addr)` 触发重连换回干净的 handler。
5. **`host` 为空或 `port <= 1` 的 server 会被静默丢弃**（绑定阶段的条件判断），日志里只会看到连了 0 台。
6. **`InboundClient` 是 JVM 单例**，`InboundClient.newInstance(option)` 第二次调用抛 `InboundClientException`。Spring 环境只注入 Bean；纯 Java 用 `newInstance` + `start()`，退出前 `shutdown()`。
7. **BACKGROUND_JOB 拿结果的前提是订阅了它**（或 `ALL`）。`sendAsyncApiCommand` 只给 Job-UUID；结果正文在 `BACKGROUND_JOB` 事件的 `getEventBodyLines()`，用 `Job-UUID` 事件头做关联。`inboundClient.subscribeBackgroundJob()` 可自查是否已订阅。
8. **空闲保活会自己发 `bgapi status`**（`reader-idle` 触发）。若订阅了 BACKGROUND_JOB，会收到它产生的结果事件——业务侧必须按 Job-UUID 或命令名过滤，别当成自己的任务。
9. **只支持 `plain` 事件格式。** `setEventSubscriptions(addr, "xml", ...)` 抛 `IllegalStateException`；`EslEvent` 构造遇到 xml body 同样抛。
10. **事件头已被 URL-decode**，直接读值，不要再解码一次。
11. **`reader-idle-time-seconds` 必须严格小于 `read-timeout-seconds` 且都 > 0**，否则 pipeline 不加 `IdleStateHandler`/`ReadTimeoutHandler`，等于没有空闲检测与读超时（默认 25 / 30 是配好的）。
12. **未命中事件名会走默认 handler**（`DefaultEslEventHandler` 以 `WARN` 打印完整事件）。日志被它刷屏说明订阅列表里有事件没有对应 handler——加一个兜底 handler 或从 `events` 里去掉。
13. **`@EslEventName` 只查「类 → 直接父类」两层**（为了兼容 AOP 代理）。注解贴在更上层的抽象基类、或贴在非 `@Component` 类上都不会生效。
14. **`callback-executor-thread` 当前无实现**（不会创建对应线程池），调它没有效果。
15. Handler 抛异常会被捕获并记 error，不影响其他 listener，也**不会重试**；业务侧自己做幂等。默认在 `publicExecutor` 上并发执行，要求严格顺序时设 `disable-public-executor: true`（同连接事件串行，注意别在 handler 里做长耗时阻塞）。
16. **README 的 properties 片段里 `servers[0]` 之后直接跳到 `servers[2]`，不要照抄。** Spring 绑定索引列表要求下标从 `0` 连续，跳号会让整个 `servers` 绑定失败（表现为连了 0 台）。写 `servers[0]` / `servers[1]`。
17. **README 片段里的 `CHANNEL_DESTORY` 是拼写错误**，正解 `CHANNEL_DESTROY`；订阅错名不会报错，只是永远收不到事件。同时注意 `.properties` 里 `events=CHANNEL_CREATE CHANNEL_DESTROY`（空格分隔）只会被绑定成**一个**列表元素 `"CHANNEL_CREATE CHANNEL_DESTROY"`——拼出的 `event plain` 命令恰好有效，但事件名去重、`addEvents`/`events()` 判断都会失真。properties 请用逗号分隔（`events=A,B`），或改用 yml 列表一项一个事件。

## 验证是否跑通

按顺序确认日志（`link.thingscloud.nextswitch.esl` 包，DEBUG 级别可看到收发的原始报文）：

1. `inbound client will start ...` 与 `connect remote server [10.0.0.11:7921] success.`
2. `Auth response success=true, message=[+OK welcome]`（`success=false` 就是密码错）
3. 自定义 `ServerConnectionListener` 的 `onOpened serverOption : ...`
4. 发一通测试呼叫，看到 `Event addr[10.0.0.11:7921] received [EslEvent: name=[CHANNEL_CREATE] ...]`
5. 若只有 `connect ... failed, cause :` 循环，先查 NS 侧 ESL ACL（`event_socket.conf.xml` 的 `apply-inbound-acl`）和端口，而不是本库配置。

## Resources

- `references/config-reference.md` — 全部配置项、默认值、绑定规则与 `application.properties` 写法
- `references/api-reference.md` — `InboundClient` 全量方法、`EslMessage`/`CommandResponse`/`SendMsg`/`SendEvent`、`InboundClientOption` 流式选项、异常
- `references/event-catalog.md` — `EventNames` 事件清单、`EslEventUtil` 事件头取值、`VariableUtil` 通道变量读取
- `references/recipes.md` — 可直接落地示例：CDR/话单、录音控制、DTMF、originate + Job-UUID 关联、动态增删 NS、心跳探活、非 Spring 用法
