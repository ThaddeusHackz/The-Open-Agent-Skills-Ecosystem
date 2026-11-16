---
name: freeswitch-esl
description: Build Java services that connect to FreeSWITCH with link.thingscloud:freeswitch-esl, the Netty 4.1 inbound ESL client used without Spring - InboundClientOption, InboundClient.newInstance, IEslEventListener, api and bgapi commands, cluster nodes, Job-UUID, reconnect and thread tuning. Use for Java SE, Servlet containers, Quarkus or any non-Spring runtime, or when the user mentions freeswitch-esl, InboundClient, event socket, mod_event_socket, ClueCon, originate, CHANNEL_HANGUP, CUSTOM events, 呼叫控制, 话单采集, 原生 Java 接入 FreeSWITCH. For Spring Boot auto-configuration, properties or @EslEventName handlers, use the freeswitch-esl-spring-boot-starter skill instead.
---

# FreeSWITCH ESL for plain Java

## Overview

`link.thingscloud:freeswitch-esl` is a Netty 4.1 inbound ESL client. It keeps authenticated connections to one or
more FreeSWITCH servers, pushes events to your `IEslEventListener`, and exposes `api` / `bgapi` commands. No Spring
dependency, JDK 8+ bytecode, latest release `2.2.0` on Maven Central. Netty 5 is unsupported and outbound ESL
(switch-initiated sockets) is out of scope.

Source and examples: `https://github.com/zhouhailin/freeswitch-externals` (mirror on Gitee), modules
`freeswitch-esl` and `freeswitch-esl-example`.

Use the companion `freeswitch-esl-spring-boot-starter` skill whenever the host application is Spring Boot - it wraps
exactly this API as beans instead of hand-built lifecycle code.

## Upstream reference

| Reference | What it shows |
|---|---|
| `README.md` "Summary" | JDK 1.8+, Netty 4.1.x only |
| `README.md` "Notice" | prefer async api, `readTimeoutSeconds=0` disables false-death detection, move slow work off the Netty worker thread |
| `freeswitch-esl-example/src/main/java/link/thingscloud/freeswitch/esl/example/EslInboundClientExample.java` | the whole build-start flow, plus `option.serverAddrOption().first() / .last() / .random()` |
| `README.md` "freeswitch-esl" snippets | `InboundClient.getInstance()`, `InboundClient.getBootstrap()`, runtime `addServerOption` / `removeServerOption` |

## Dependency

```xml

<dependency>
    <groupId>link.thingscloud</groupId>
    <artifactId>freeswitch-esl</artifactId>
    <version>2.2.0</version>
</dependency>
```

It brings `netty-handler`, `netty-transport` and a logback binding through SLF4J. If the application already picked
log4j2 or another binding, exclude `ch.qos.logback:logback-classic`.

## Minimum working client

```java

InboundClientOption option = new InboundClientOption();
option.defaultPassword("ClueCon")
        .addServerOption(new ServerOption("127.0.0.1", 8021))
        .addEvents("all")
        .addListener(new IEslEventListener() {

            @Override
            public void eventReceived(String addr, EslEvent event) {
                System.out.println(addr + " " + event);
            }

            @Override
            public void backgroundJobResultReceived(String addr, EslEvent event) {
                System.out.println(addr + " " + event);
            }
        })
        .serverConnectionListener(new ServerConnectionListener() {

            @Override
            public void onOpened(ServerOption serverOption) {
                System.out.println("---onOpened-- " + serverOption.addr());
            }

            @Override
            public void onClosed(ServerOption serverOption) {
                System.out.println("---onClosed-- " + serverOption.addr());
            }
        });

InboundClient inboundClient = InboundClient.newInstance(option);
inboundClient.start();
```

`shutdown()` is terminal: after it the client cannot be started again, which is what the README means by
"shutdown with JVM".

## Rules that decide whether this works

1. **One `InboundClient` per JVM.** `newInstance(option)` registers the instance in a factory, so the second call
   throws `InboundClientException("InboundClient has been created already")`, and `InboundClient.getInstance()`
   throws `InboundClient is null, you must be create it first.` before any instance exists. Create it once at
   startup and pass the reference around; `getInstance()` exists so that code without dependency injection can still
   reach it. Never create a client inside a request handler, a scheduled job, or a test method that may run twice.
2. **Every command takes `addr` first, formatted exactly `host:port`, and that server must be `AUTHED`.** There is no
   "any server" overload. Resolve it from `option().serverAddrOption().first()`, `.last()` or `.random()` - as the
   example does - or reuse the `addr` your listener received. Failure strings are
   `not found inbound handler for addr : ...` (unknown address) and
   `inbound handler is not authed for addr : ...` (connected but not authenticated).
3. **`close(addr)` and `closeChannel(addr)` close the ESL socket, not a phone call.** To hang up a channel send the
   `uuid_kill` command with the channel UUID.
4. **Unsubscribed events never arrive.** `BACKGROUND_JOB` (or `all`) is required for `backgroundJobResultReceived` to
   fire, and `subscribeBackgroundJob()` reports whether it is active. `sendAsyncApiCommand` returns the Job-UUID
   immediately, so keep a `Job-UUID -> correlation id` map to match the later result event.
5. **Custom events arrive as `CUSTOM`.** All of them share that event name, so branch inside the listener on
   `event.getEventHeaders().get("Event-Subclass")`.
6. **Use `EventNames.*` constants, not string literals.** Note that the README snippets spell the destroy event
   `CHANNEL_DESTORY`, which FreeSWITCH does not know; the real constant is `EventNames.CHANNEL_DESTROY`.
7. **`originate` and anything that waits on a call must go out as `bgapi`.** This is Notice item 1 in the README, and
   the implementation backs it up: sync commands take a per-connection `syncLock`, enqueue a callback and block until
   the reply pops the FIFO queue, so one slow `api originate` stalls every other sync command against that `addr`.
8. **Slow listener code blocks the shared executor, and can block I/O.** Listeners run on `publicExecutor` by
   default. Setting `disablePublicExecutor(true)` runs them directly on the Netty worker thread - that is the
   optimisation the README mentions, and it is only safe once every blocking statement has left the listener.
   Listener exceptions are caught and logged and cannot kill the connection.
9. **`defaultTimeoutSeconds` is the reconnect delay, not a command timeout.** It controls how long the client waits
   before retrying a `FAILED` or `CLOSED` server; per-server `ServerOption.timeoutSeconds(n)` overrides it, and `0`
   means "inherit the default" (5 seconds).
10. **Half-open detection needs both timeouts in order.** The idle and read-timeout handlers are added to the
    pipeline only when `0 < readerIdleTimeSeconds() < readTimeoutSeconds()` (defaults 25 and 30), and `SO_KEEPALIVE`
    is off, so `readTimeoutSeconds(0)` genuinely means "a silently dead connection is never noticed".
11. **Cluster edits at runtime work, event edits do not behave the same way.** `option().addServerOption(...)` on a
    started client connects immediately and `removeServerOption(...)` closes that connection. But
    `option().addEvents(...)` afterwards sends a new subscription containing **only the names added by that call**,
    which replaces the switch-side list - declare the full event set up front, or re-add everything you want active.

## Verify without a switch

Nothing prevents startup when no server answers; the client retries in the background:

```java

InboundClient client = InboundClient.newInstance(option);
client.start();
client.option().serverOptions().forEach(s ->
        System.out.println(s.addr() + " state=" + s.state() + " connects=" + s.connectTimes()));
```

`ConnectState` is the contract: `AUTHED` allows commands, `CONNECTING` / `CONNECTED` are transitional, `FAILED` and
`CLOSED` mean the reconnect loop is running, `AUTHED_FAILED` means the password was rejected, `SHUTDOWN` is terminal.
A rising `connectTimes()` with `state=FAILED` means the address, port, firewall or `listen-ip` is wrong; the log line
`Rejected by acl ...` means the switch ACL refused the caller. Set `logging.level.link` to `DEBUG` to see
connections, subscriptions and every event.

Against a live switch, `version` is the cheapest round trip:

```java

String addr = inboundClient.option().serverAddrOption().first();
System.out.println(EslHelper.formatEslMessage(inboundClient.sendSyncApiCommand(addr, "version", null)));
```

## Resources

- `references/api.md` - `InboundClient` method list, `InboundClientOption` builder, `EslEvent` / `EslMessage` /
  `CommandResponse` accessors, header field cheat sheet, command recipes, FreeSWITCH-side checklist.
- `references/threads-and-performance.md` - thread map, sync-command serialisation, buffer and frame limits, timeout
  semantics, monitoring flags, symptom-to-action table.
