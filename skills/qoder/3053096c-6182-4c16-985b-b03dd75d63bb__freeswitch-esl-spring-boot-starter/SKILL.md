---
name: freeswitch-esl-spring-boot-starter
description: Auto-configure FreeSWITCH ESL inside Spring Boot 2, 3 and 4 with link.thingscloud:freeswitch-esl-spring-boot-starter - link.thingscloud.freeswitch.esl.inbound properties, injected InboundClient, @EslEventName event handlers, AbstractInboundClientOptionHandler, ServerConnectionListener, runtime cluster endpoints, EnableFreeswitchEslAutoConfiguration. Use when a Spring Boot application must subscribe to or control FreeSWITCH, or the user mentions freeswitch-esl starter, InboundClient bean, EslEventHandler, 事件订阅, 呼叫控制, 话单, Spring Boot 接入 FreeSWITCH. For non-Spring Java services use the freeswitch-esl skill.
---

# FreeSWITCH ESL Spring Boot starter

## Overview

`link.thingscloud:freeswitch-esl-spring-boot-starter` turns the Netty inbound ESL client into auto-configured beans:
bind `link.thingscloud.freeswitch.esl.inbound.*`, get a started `InboundClient`, and route events to
`EslEventHandler` beans by event name. The starter pulls `freeswitch-esl` transitively, so declare only the starter.

Latest release `2.2.0`, Java 8 bytecode, one artifact for Spring Boot 2.7, 3 and 4.
Source and examples: `https://github.com/zhouhailin/freeswitch-externals`, modules
`freeswitch-esl-spring-boot-starter` and `freeswitch-esl-spring-boot-starter-example`.

## Upstream reference

| Example file | What it demonstrates |
|---|---|
| `.../starter/example/ExampleApplication.java` | plain `@SpringBootApplication`; `@EnableFreeswitchEslAutoConfiguration` is shown commented out for older Boot lines |
| `.../starter/example/ExampleInboundClient.java` | injecting `InboundClient` and `InboundClientBootstrap` |
| `.../starter/example/HeartbeatEslEventHandler.java` | `@EslEventName(EventNames.HEARTBEAT)` handler implementing `EslEventHandler` |
| `.../starter/example/ReScheduleEslEventHandler.java` | extending `AbstractEslEventHandler` and sending `sendSyncApiCommand(addr, "version", null)` from a handler |
| `.../starter/example/ExampleInboundClientOptionHandler.java` | extending `AbstractInboundClientOptionHandler` and overriding `intercept` |
| `.../starter/example/ServerConnectionListenerImpl.java` | connection callbacks via `@Service` |
| `.../starter/example/controller/DemoController.java` | REST endpoints for `addServerOption`, `removeServerOption`, `serverOptions` |
| `.../starter/example/src/main/resources/application.yml` | `defaultPassword`, `performance`, `servers` list, `events: - all` |
| `.../starter/example/src/test/java/.../ExampleApplicationTests.java` | `@SpringBootTest` context load check |
| `README.md` "application.properties" | index-style keys such as `servers[0].host`, plus the `performanceCostTime` / `eventPerformanceCostTime` pair |

## Wire it up

1. Dependency:

```xml

<dependency>
    <groupId>link.thingscloud</groupId>
    <artifactId>freeswitch-esl-spring-boot-starter</artifactId>
    <version>2.2.0</version>
</dependency>
```

2. Configuration. Only `host` is required per server; `port` defaults to `8021` and the password to
   `default-password`. Both index style (`servers[0].host=...`) and list style work.

```yaml
link:
  thingscloud:
    freeswitch:
      esl:
        inbound:
          default-password: ClueCon
          performance: false
          performance-cost-time: 200
          servers:
            - host: 127.0.0.1
              port: 8021
              timeout-seconds: 5
            - host: 127.0.0.2
          events:
            - HEARTBEAT
            - CHANNEL_HANGUP_COMPLETE
```

3. One handler per event name:

```java

@Slf4j
@Component
@EslEventName(EventNames.CHANNEL_HANGUP_COMPLETE)
public class HangupEslEventHandler implements EslEventHandler {

    @Override
    public void handle(String addr, EslEvent event) {
        String uuid = event.getEventHeaders().get("Unique-ID");
        String cause = event.getEventHeaders().get("Hangup-Cause");
        log.info("hangup addr[{}] uuid[{}] cause[{}]", addr, uuid, cause);
    }
}
```

4. Send commands through the injected client:

```java

String addr = inboundClient.option().serverAddrOption().random();
EslMessage version = inboundClient.sendSyncApiCommand(addr, "version", null);
String jobId = inboundClient.sendAsyncApiCommand(addr, "originate",
        "sofia/gateway/gw/1001 &playback(/sounds/Hello-Welcome.wav)");
```

## Spring Boot 2 / 3 / 4

| Boot line | Auto-configuration |
|---|---|
| 2.7, 3.x, 4.x | works out of the box - registered in `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` |
| 2.0 - 2.6 | add `@EnableFreeswitchEslAutoConfiguration`; those versions do not read the `imports` file |

The starter uses only `@Configuration`, `@ConditionalOn*` and JavaBean-bound `@ConfigurationProperties`, with no
`javax.*` or `jakarta.*` import - that is why one artifact covers all three lines and why property keys never
change. Boot 3 and 4 need JDK 17+ for their own baseline while the library stays Java 8 bytecode.

```java

@SpringBootApplication
@EnableFreeswitchEslAutoConfiguration
public class App {
}
```

A missing `InboundClient` bean means the starter is not on the classpath, the prefix is misspelled, or you are on
Boot 2.0 - 2.6 without the `@Enable` annotation above.

## The five beans and what replacing them costs

`FreeswitchEslAutoConfiguration` is guarded by `@ConditionalOnClass(InboundClient.class)` and declares each bean with
`@ConditionalOnMissingBean`:

| Bean | Default | Consequence of defining your own |
|---|---|---|
| `InboundClientOptionHandler` | `DefaultInboundClientOptionHandlerTemplate` | yours becomes the single place where the option is built |
| `IEslEventListener` | `IEslEventListenerTemplate` | **you lose the whole `@EslEventName` routing table** - register handlers instead |
| `ServerConnectionListener` | `ServerConnectionListenerTemplate` (logs open and close) | only one such bean is used; there is no `List` aggregation, so fan out inside your bean |
| `InboundClient` | `newInstance(option)`, `initMethod = "start"`, `destroyMethod = "shutdown"` | the auto-configured client disappears; you own start and shutdown |
| `InboundClientBootstrap` | thin wrapper around the client | rarely needed |

Never call `InboundClient.newInstance(...)` yourself inside a Boot application: the auto-configuration already
created the JVM-wide instance, so a second `newInstance` throws
`InboundClientException("InboundClient has been created already")`. Two Spring contexts in one JVM (for example a
running app plus a `@SpringBootTest`) hit the same wall - share one context per test class.

## Handler rules

- Implement `EslEventHandler`, or extend `AbstractEslEventHandler` to inherit a protected `inboundClient` and a `log`
  named after the concrete class.
- `@EslEventName` takes `String[] value()`, so one bean can serve several event names; every handler registered for a
  name runs, in injection order.
- Routing is an exact match on `event.getEventName()`, so custom events all arrive as `CUSTOM` - register `CUSTOM`
  once and branch on `event.getEventHeaders().get(EslEventHandler.SUB_EVENT_HEADER_KEY)` (`Event-Subclass`).
- `@EslEventName(EslEventHandler.DEFAULT_ESL_EVENT_HANDLER)` marks a catch-all that replaces the WARN-logging
  default handler.
- Put the annotation on the class. The lookup falls back to the superclass, so `@Transactional` or `@Async` CGLIB
  proxies still route.
- `BACKGROUND_JOB` must be in `events` for job output to arrive; the template funnels both `eventReceived` and
  `backgroundJobResultReceived` into the same handler table.
- Handlers run on the shared `public-executor-thread` pool by default. Keep `disable-public-executor: false` and hand
  slow work to your own executor; `true` moves handlers onto the Netty I/O thread.
- Use `EventNames.*` constants. The README snippets spell the destroy event `CHANNEL_DESTORY`; the real constant is
  `EventNames.CHANNEL_DESTROY`, and a typo here silently subscribes to nothing.

## Building the option from code

`AbstractInboundClientOptionHandler.getOption()` maps properties into `InboundClientOption` and then calls
`intercept(option)`. Override it to load servers from a database or config center:

```java

@Slf4j
@Component
public class ClusterInboundClientOptionHandler extends AbstractInboundClientOptionHandler {

    @Override
    protected void intercept(InboundClientOption option) {
        List<ServerOption> serverOptions = option.serverOptions();
        log.info("serverOptions before : {}", serverOptions);
        serverOptions.clear();
        serverOptions.add(new ServerOption("127.0.0.8", 8021));
        log.info("serverOptions after  : {}", serverOptions);
    }
}
```

Property-driven server entries are skipped unless `host` is non-blank **and** `port > 1`, the usual reason "the
client started but never connected to this server".

## Commands and cluster endpoints

All `InboundClient` methods take `addr` as `host:port` of an `AUTHED` server; use
`option().serverAddrOption().first() / .last() / .random()` or the `addr` handed to a handler. `closeChannel(addr)`
closes the ESL connection, not a call - use `uuid_kill` with the channel UUID. Details in
`references/esl-command-basics.md`.

The upstream `DemoController` shows the runtime cluster pattern worth copying into your own admin endpoints:

```java

inboundClient.option().addServerOption(new ServerOption(host, port));
ServerOption serverOption = inboundClient.option().serverOptions().get(0);
inboundClient.option().removeServerOption(serverOption);
return inboundClient.option().serverOptions().toString();
```

## Verify

```java

@SpringBootTest
class EslWiringTest {

    @Autowired
    InboundClient inboundClient;

    @Test
    void bound() {
        assertThat(inboundClient.option().serverOptions()).isNotEmpty();
        assertThat(inboundClient.option().events()).contains("HEARTBEAT");
    }
}
```

A connection-refused line in the log is expected when no switch answers - the context still starts and the client
retries. Add `logging.level.link: DEBUG` to see subscriptions, and turn on `performance` with
`performance-cost-time` to log slow handlers.

## Resources

- `references/spring-boot-starter.md` - all 17 configuration keys with defaults and real semantics, bean override
  table, handler and option-handler patterns, `ConnectState` lifecycle, Boot 2.0 - 2.6 note, diagnostics.
- `references/esl-command-basics.md` - address rules, sync versus `bgapi`, command list, event header fields,
  Job-UUID correlation, originate and channel-control recipes, FreeSWITCH-side checklist.
- Companion skill `freeswitch-esl` for the same client without Spring.
