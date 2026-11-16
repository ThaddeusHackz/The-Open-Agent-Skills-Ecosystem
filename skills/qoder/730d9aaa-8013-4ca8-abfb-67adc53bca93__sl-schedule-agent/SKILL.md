---
name: sl-schedule-agent
version: 2.4.0
description: SL scheduling assistant with batch scheduling, risk scanning, workload estimation and smart conversational adjustments via the self-hosted scheduling agent API. All API calls are made in-browser with credentials:include (auto-carries HttpOnly cookies), using fire-and-poll pattern to avoid evaluate_script timeout. Use when the user mentions 批量排期、风险扫描、工时评估、优先级排序、任务分配, or provides VR requirement keys.
description_zh: SL 排期助手：支持批量排期、风险扫描、工时评估，并通过对话智能调整排期方案。在浏览器内直接发起 API 请求（credentials:include 自动携带完整 Cookie 含 HttpOnly），采用「发射+轮询」模式规避超时，排期逻辑全在服务端，skill 只负责 relay 对话、渲染结果。
user-invocable: true
argument-hint: <VR编号1> <VR编号2> ... | 帮我扫描XX项目的风险 | 帮我评估工时 ...
install_method: upload
---

# SL 排期助手

薄 skill：**浏览器内 fetch（credentials:include）→ 发射+轮询 → relay 渲染**。排期/风控逻辑全在服务端，支持通过对话智能调整排期方案。

## 触发条件

满足以下**任意一项**即触发：

- **批量排期**：用户提供 ≥1 个 VR 需求编号（如 `VR260716-305`）或 VAPD 短链，并提到"排期"、"批量排期"、"这几个需求一起排"等
- **风险扫描**：用户提到"风险扫描"、"风险预警"、"帮我看看XX项目的风险"、"这个项目有没有风险"等
- **工时评估**：用户提到"工时评估"、"评估改动量"、"大概要多久"、"工作量估算"等
- **对话调整**：在排期过程中，用户通过自然语言调整方案，如"排除 XX"、"YY 改期到 ZZ"、"重新分配给 AAA"等

## 执行约束

1. **所有 API 调用在浏览器内完成**：通过 `evaluate_script` 发起 `fetch`，使用 `credentials: 'include'` 自动携带完整 Cookie（含 HttpOnly），无需提取 Cookie
2. **发射+轮询模式**：`evaluate_script` 有 ~15s 超时，只负责发射请求（立即返回），结果存 `window` 变量，后续短轮询取结果
3. **排期逻辑全在服务端**：禁止自行预估/排序/分配，禁止调 VAPD 业务接口
4. **确认点在服务端**：agent 回复中带确认引导，skill 原样 relay，**禁止自动确认、禁止自行创建任务**
5. **❗ 扩展引导时少弹窗、少轮询、等用户确认**：检测到扩展未安装时，**先解释**，**再只打开一次**扩展下载页，然后**停下来等用户回复**，不要连续查询产生一堆状态卡片。

## 配置

| 项 | 值 |
|----|----|
| Agent 基地址 | `https://task-manage-prod.vivo.xyz/api`（本地 `http://localhost:8080/api`） |
| 非流式 | `POST {base}/react-agent/chat`，Body `{"message","conversationId"}` |
| 流式（SSE） | `GET {base}/react-agent/chat/stream?message=&conversationId=` |

## Step 0: 浏览器连接器检测（每次执行必须先跑）

### 0.1 一次性检测

执行一次 `qw_query key=qoderwork.settings.connector.builtin.browser`，根据 `extensionConnected` 判断：

| extensionConnected | 动作 |
|-------------------|------|
| true | **就绪** → 直接 Step 1 |
| false | 扩展未连接 → 进入 0.2 引导安装 |

> **关键判断字段只有 `extensionConnected`**。`enabled` 为 false 时先 `qw_action enable` 一次即可，不必反复打开设置页。整个 Step 0 最多调用 **2 次 `qw_query`** 和 **1 次 `qw_action enable`**，避免产生大量状态卡片。

### 0.2 扩展未安装时的友好引导

当 `extensionConnected=false` 时，按以下顺序执行：

**① 先解释，再开窗**

在对话中输出说明（**这是本轮唯一的话**）：

> 首次使用批量排期需要安装一次浏览器扩展，用于携带 VAPD 登录态，之后无需重复安装。请点击下面的 Chrome 扩展商店地址，点击「添加至 Chrome」安装；装好后直接回复「继续」，我就会接着排期。
>
> 地址偶尔可能被拦截，在浏览器多刷新几次即可

然后执行 `qw_action enable`（如果 `enabled=false`）。**不要打开连接器设置页，也不要用 `browser_navigate` 导航到任何 QoderWork 内置页面**。

**② 提供扩展下载地址**

弹出说明后，直接把 Chrome 扩展商店地址发给用户，让用户自己点击安装：
```
https://chromewebstore.google.com/detail/qoder-browser-connector/gblapfbnbicdckfhkllcnfleiemhmgeb
```

> 同一个排期任务里，商店页和设置页**最多各开一次**。不要连续开、不要重复弹。

**③ 停下来等用户回复**

不要自动轮询、不要每 5 秒查一次状态。直接等待用户回复。

用户可能回复：
- 「继续」/「好了」/「已安装」→ 进入 0.4
- 「连不上」/「没反应」→ 进入 0.3 诊断

### 0.3 安装问题诊断

如果用户表示已安装但无法继续，执行一次 `qw_query` 确认状态后给出明确指引：

> 扩展尚未连接，可能原因：
> 1. 还未点击「添加至 Chrome」；
> 2. 扩展已安装但未固定/未启用（看 Chrome 右上角拼图图标，点开把 Qoder 扩展固定）；
> 3. 当前 Chrome 没有登录 VAPD；
> 4. 扩展装在了另一个 Chrome 用户上。
>
> 处理完任意一项后，回复「继续」即可。

### 0.4 用户回复后继续

用户回复「继续」后，**只执行一次** `qw_query`：
- `extensionConnected=true` → 进入 Step 1
- `extensionConnected=false` → 回到 0.3 给出诊断，不再自动打开商店页

## Step 1: 确认 VAPD 登录态

扩展已连接 = Cookie 就绪（用户已在 Chrome 中登录 VAPD，`credentials: 'include'` 自动携带）。直接跳到 Step 2。

若后续 API 返回 not_login / 403 → 提示用户在 Chrome 中刷新 VAPD 页面重新登录，重试一次。

## Step 2: 输入规整

- VR 编号直接透传
- 短链（`vapd.vivo.xyz/s/xxx`）→ 浏览器导航短链，**只从落地页读取 VR 编号文本**，再透传编号
- 视角：用户已指明则附加"，后端视角"等；未指明不附加（服务端默认后端）

## Step 3: 发起排期对话（发射 + 流式轮询）

1. 生成 `conversationId = "qw-batch-<时间戳>"`，整个排期会话保持不变
2. 首条 message 示例：`批量排期 VR260716-305 VR260720-189，后端视角`

### 3.1 发射请求

`evaluate_script` 立即返回，不等 fetch 完成。这里使用 `ReadableStream`  reader 在页面内持续解析 SSE，把已收到的 content 段落实时追加到 `window._job.delta`，完整内容累积到 `window._job.full`。

```js
() => {
  const convId = 'qw-batch-<时间戳>';
  const msg = encodeURIComponent('<message>');
  window._job = { convId, done: false, error: null, full: '', delta: '' };
  const decoder = new TextDecoder();
  let buffer = '';
  fetch('{base}/react-agent/chat/stream?message=' + msg + '&conversationId=' + convId, {
    credentials: 'include'
  }).then(r => {
    const reader = r.body.getReader();
    function pump() {
      return reader.read().then(({ done, value }) => {
        if (done) { window._job.done = true; return; }
        buffer += decoder.decode(value, { stream: true });
        let idx;
        while ((idx = buffer.indexOf('\n')) >= 0) {
          const line = buffer.slice(0, idx).trim();
          buffer = buffer.slice(idx + 1);
          if (line.startsWith('data:')) {
            try {
              const json = JSON.parse(line.slice(5));
              if (json.type === 'content' && json.content) {
                window._job.full += json.content;
                window._job.delta += json.content;
              }
            } catch (e) {}
          }
        }
        return pump();
      });
    }
    return pump();
  }).catch(e => {
    window._job.error = e.message;
    window._job.done = true;
  });
  return convId;
}
```

### 3.2 轮询取增量

每 **3–5 秒** 轮询一次，取 `window._job.delta` 中新累积的内容并清空 delta，同时带回 `done` / `error` 状态。

```js
() => {
  if (!window._job) return JSON.stringify({ status: 'NO_JOB' });
  const delta = window._job.delta;
  window._job.delta = '';
  return JSON.stringify({
    status: window._job.done ? (window._job.error ? 'ERROR' : 'DONE') : 'STREAMING',
    error: window._job.error || null,
    content: delta,
    full: window._job.full
  });
}
```

### 3.3 渲染策略

- 轮询返回 `STREAMING` 且 `content` 非空时，把 `content` **原样 relay** 给用户（追加到当前轮次的输出里，不要 paraphrase）
- 轮询返回 `DONE` 时，本次输出结束；若最后还有 `content`，先 relay 再结束
- 轮询返回 `ERROR` 时，把错误信息 relay 给用户，并按 Step 5 处理
- 若 `content` 为空且仍在 `STREAMING`，继续轮询，不要发送空消息

> 注意：流式内容是逐步拼接的，可能包含未闭合的 Markdown 表格。skill 只负责原样 relay，不修正格式；最终 agent 会输出完整的确认引导和 `[SCHEDULE_OVERVIEW]` 块。

## Step 4: relay 渲染与确认循环

1. 将 agent 回复**原样渲染**给用户（含预估列表、优先级排序、排期总览表与确认引导），不 paraphrase、不重排。流式场景下按 Step 3.3 边收边 relay。
2. **SCHEDULE_OVERVIEW JSON 转文本**：当一轮流式输出 `DONE` 后，如果 `window._job.full` 包含 `[SCHEDULE_OVERVIEW] ... [/SCHEDULE_OVERVIEW]` JSON 块，则**优先按以下规则解析并转换成纯文本任务明细**，再 relay 给用户：
   - 截取 JSON 内容，解析为对象（`totalRequirements`、`requirementSummaries`、`assignments`、`perspective`、`totalPersonDays` 等）
   - 按 `requirementSummaries` 顺序输出每个需求：
     ```
     <requirementKey> <requirementTitle>（<负责人>）

     <任务1标题> — <startDate> ~ <endDate>，<personDays>人天
     <任务2标题> — <startDate> ~ <endDate>，<personDays>人天
     ...
     ```
   - 负责人优先取该需求下所有 `assignments` 中共同/主要的 `assignee`；若同一需求下任务负责人不同，可在每行任务后补充 `（<assignee>）`
   - 转换完成后，在末尾追加原确认引导语（如“请确认是否按此排期创建任务？回复「确认创建」即可，也可以继续调整。”），不再把原始 JSON 块展示给用户
   - 如果 JSON 解析失败或块内容异常，**回退为原样 relay**原始 agent 回复（含 JSON 块）
3. 等待用户回复。在**同一排期会话内**，用户的话分为三类：
   - **排期相关**："确认创建"、调整指令（"排除 XX"、"YY 改期到 ZZ"、"ZZ 调整给 AAA" 等）→ 以发射 + 流式轮询模式发往同一 conversationId
   - **agent 支持的其它查询/操作**：例如 "查看当前项目的技能评分"、"给 XX 技能打分"、"技能评分规则是什么" 等 → **同样原样转发给同一 conversationId**，由 agent 处理并 relay 回复
   - **明确放弃**："不排了"、"取消"、"放弃" → 调 `POST {base}/react-agent/chat/abort` 中断会话
4. 循环 relay，直到 agent 返回创建结果明细（成功/失败清单）或用户明确放弃
5. 结束汇报：创建成功的任务编号（VTxxx）+ 失败项及原因

> 原则：在排期会话进行中，**不要用自己的通用能力（如 `qw_query` 查 QoderWork 设置、查 VAPD 等）去回答用户**；统一把话语权交给 agent，只充当 relay。

## Step 5: 异常处理

| 场景 | 处理 |
|------|------|
| not_login / 403 | 提示用户在 Chrome 中刷新 VAPD 页面确认登录态，重试一次 |
| Agent 503 / 网络不通 | 告知服务不可达 |
| 单轮超 10 分钟 | 提示用户拆小批次 |
| 用户中途放弃 | 调 `POST {base}/react-agent/chat/abort` 中断会话 |
| 扩展断连 | 提示用户检查 Chrome 扩展是否启用，刷新页面后重试 |
