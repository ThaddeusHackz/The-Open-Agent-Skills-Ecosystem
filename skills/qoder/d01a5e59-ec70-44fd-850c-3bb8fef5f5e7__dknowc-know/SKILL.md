---
name: "dknowc-know"
slug: "dknowc-know"
displayName: "深知晓"
description: "Qoder Public 版深知晓，为工作场景提供可信安全、精准无幻觉的咨询导办知识服务，覆盖税务社保、法规政策、行业标准，申办各类证照、补贴、资质，以及买房购车、养老育儿、上学就业等公共服务；同时具备分析调研、拟稿写文能力。所有输出内容均可逐项索引于动态更新的各权威机构海量知识网络，并可智能切换任意城市，为工作与办事提供可信赖的本地化精准知识服务。"
---

# 深知晓（Qoder Public 版）

该 skill 用于政务问答场景。Agent 只负责调用本 skill 的脚本，并把脚本输出直接交付给用户；正文内容由深知可信统一接口生成。Qoder Public 版不内置深知可信统一接口 API Key；首次使用时由 Agent 通过 MaaS 注册接口完成手机号注册、验证码确认、API Key 获取和本地配置写入。

## 启动初始化

只要本 Skill 被调用，必须先检查本 Skill 根目录下是否已存在可用的 `config.ini`。如果 `config.ini` 不存在，或调用脚本提示 API Key 缺失，先暂停原任务并向用户说明：

```text
首次使用深知晓需要完成深知可信统一接口账号初始化。你只需要提供手机号和收到的验证码，注册、获取 Key 和本地配置由我处理。
```

然后按两步流程执行：

```bash
node scripts/register.mjs send --phone <手机号>
```

返回 `status=true` 后，暂停并向用户索取收到的 6 位验证码，不得自行编造验证码。

拿到验证码后执行：

```bash
node scripts/register.mjs register --phone <手机号> --vcode <验证码> --organ 个人 --name 用户
```

脚本默认固定 `type=11`（可信统一接口），并自动使用 Qoder 渠道码 `5DBF147C-A4D0-4C3E-AB1A-6C6F5EA39B18`。注册成功后，脚本会自动将 API Key 写入本 Skill 根目录下的 `config.ini`，标准输出不返回完整 Key。不得向用户索要、展示或要求用户手动复制 API Key。配置写入成功后，继续处理用户原任务。

如接口失败、短信发送受限、验证码错误、手机号已注册或用户不希望自动注册，暂停原任务并给出 Qoder 渠道注册链接作为降级方案：

```text
https://platform.dknowc.cn/auth/#/register?channel=5DBF147C-A4D0-4C3E-AB1A-6C6F5EA39B18&type=11
```

## 最高优先级约束

- 每个用户回合最多调用一次 `scripts/gov_chat.py`。
- 必须将用户本轮原始问题逐字作为脚本第一个参数传入。
- 不得改写、总结、翻译、扩写、压缩、拆分或补充用户问题后再传入脚本。
- 即使用户问题中包含多个事项、多个条件或多个子问题，也必须作为一个完整问题一次性传给接口，不得拆成多次查询。
- 例如用户问“物业服务不达标、小区公共收益归属、物业收费等级标准分别说明”时，只能调用一次脚本，`input` 必须是这整句话，不得拆成 3 次接口调用。
- 不得为了补充依据、验证结论、生成要点、生成建议或确认来源而再次调用脚本。
- 如果用户只是追问“你是否用了 skill”“你调用了几次”等元问题，不要再次调用本 skill；直接基于当前对话说明。

## 配置

`config.ini` 只存在于用户本地安装后的 Skill 目录中，不得上传、打包或公开分享。公开包只提供 `config.ini.example`。

本地配置写入后包含：

- `endpoint`: 调用地址，默认 `https://open.dknowc.cn/chat/trusted/unification`
- `api_key`: 由注册脚本自动获取并写入的深知可信统一接口 API Key
- `sz_user_id`: 用户标识。普通使用可留空；如平台分配了用户标识，可填入
- `area`: 默认留空，不主动传入 `area` 字段，由接口根据用户原始问题识别地域
- `safe_answer_scope`: 安全代答范围，`none` 不代答，`risk` 仅高风险代答，`all` 对非安全问题代答
- `safe_answer_type`: 安全代答模式，`active` 积极型，`conservative` 稳妥型
- `credible_chat_scope`: 默认 `all`
- `search_mechanism`: 搜索机制，默认 `autoSearch`
- `interpretation_model`: 解读模型，默认 `autoModel`
- `stream`: 默认 `true`，由脚本读取 SSE 流式返回并只输出清洗后的接口正文
- `material`: 默认 `true`，用于返回正文角标、参考材料、原文段落和源链接
- `item`: 默认 `true`，用于返回公共事项在线办理清单
- `policy`: 默认 `true`，用于返回规范性文件清单
- `traceurl`: 默认 `true`，用于返回可信溯源报告链接

`session_id` 默认留空。只有需要多轮对话上下文管理时，才通过配置或 `--session-id` 动态传入。

不要把任何真实 API Key 写入公开仓库或公开分发包。不要把 `knowledgeServiceType` 改成 `credibleRecall`。深知晓固定使用：

```json
{
  "knowledgeServiceType": "credibleChat",
  "credibleChatScope": "all"
}
```

## 调用方式

```bash
python3 {baseDir}/scripts/gov_chat.py "社保迁移怎么办理？"
```

常用调试：

```bash
python3 {baseDir}/scripts/gov_chat.py "社保迁移怎么办理？" --show-payload
python3 {baseDir}/scripts/gov_chat.py "社保迁移怎么办理？" --json-only
python3 {baseDir}/scripts/gov_chat.py "社保迁移怎么办理？" --auto-request-id
python3 {baseDir}/scripts/gov_chat.py "深圳公积金提取需要什么材料？" --material --item
python3 {baseDir}/scripts/gov_chat.py "整理新能源汽车补贴政策文件清单" --policy --credible-chat-scope all
python3 {baseDir}/scripts/gov_chat.py "北京市有哪些租房优惠政策？" --traceurl
```

输出默认是人类可读文本；需要给其他程序消费时使用 `--json-only`，会输出聚合后的结构化 JSON。需要链路排查时使用 `--auto-request-id` 或显式传 `--request-id`。

## 执行与转发规则

- 必须调用 `scripts/gov_chat.py` 获取回答，不要绕过脚本自行回答。
- 一次用户请求只执行一次脚本命令；禁止连续执行多条 `gov_chat.py` 命令。
- 脚本默认使用 `stream=true` 调用可信统一接口，由脚本逐行读取 SSE，只把清洗后的 `content` 片段输出给用户；不要自行读取或改写流式中间片段。
- 拿到脚本 stdout 后，必须将 stdout 作为最终回复主体直接返回给用户。
- 不要基于脚本输出再二次总结、改写、压缩、扩写、表格化或补充建议。
- 不要自行生成“维权图”“核心要点速览”“实用建议”“补充提示”等脚本输出之外的内容。
- 脚本输出会直接从接口正文开始；不得额外添加“回复内容”“核心要点”等标题。
- 如果脚本调用失败，原样说明错误信息，并建议用户稍后重试或检查配置。

## 地域规则

- 默认不传 `area` 字段。
- 不要因为用户提到城市、省份或区域，就额外添加 `--area` 参数。
- 地域识别交给可信统一接口根据用户原始问题处理。
- 只有用户明确要求调试某个地域参数，或接口产品/开发要求临时验证地域字段时，才使用 `--area`。

## 参数选择规则

- 默认使用 `credibleChatScope=all`。
- 默认保持 `item=true`，让接口可返回公共事项在线办理清单。
- 默认保持 `policy=true`，让接口可返回规范性文件清单。
- 不要根据用户问题动态切换 `credibleChatScope`、`item` 或 `policy`，除非用户明确要求调试参数。
- 默认保持 `traceurl=true`，在回复结尾输出可信溯源报告链接，方便用户打开完整溯源页面核验回答依据。
- 用户要求快速结论时，可使用 `--interpretation-model fastModel`；用户要求深度分析、对比或研判时，可使用 `--interpretation-model deepModel`。

## 跨渠道稳定回复规则

深知晓的最终回复以脚本输出为准，脚本内部以接口返回内容为准，只做必要的格式清洗，不对正文内容做二次改写、重组或摘要。

- 面向用户回复时，正文沿用接口 `resp.content`。
- 仅清洗影响聊天窗口阅读的格式：移除 HTML 标签和 `[^1^]` 这类引用角标。
- 不在聊天窗口额外重组“参考依据”“事项清单”或“政策文件清单”，避免与可信溯源报告内容口径不一致。
- 如果接口返回 `traceUrl`，必须在用户回复结尾输出“可信溯源报告”及完整链接。
- 用户需要核验来源、查看原文、对照依据时，引导用户打开可信溯源报告。

推荐格式：

```text
这里输出接口返回正文的格式清洗版，不额外改写内容。

可信溯源报告
https://yun.dknowc.cn/wlcb/trace-report/?id=...
```

## 输出原则

- 办理步骤、条件、材料、渠道、依据等正文内容由接口返回，Agent 不自行补充。
- 涉及政策依据时，保持配置中的 `material=true`。
- 默认保持 `item=true` 和 `policy=true`，Agent 不需要根据问题额外判断是否开启。
- 默认不把“原文清单/召回结果”作为聊天窗口体验，来源核验以可信溯源报告为准。
