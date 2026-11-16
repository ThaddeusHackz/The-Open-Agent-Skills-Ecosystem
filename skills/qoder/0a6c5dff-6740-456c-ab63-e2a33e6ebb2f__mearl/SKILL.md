---
name: mearl
description: 使用 Mearl 复用浏览器登录态，操作或调试网页，模拟设备、时区或 App 客户端环境（含 JSBridge 与容器栈），发送带浏览器身份的 HTTP/MTop 请求，管理本地、远端及 AgentBay（无影）云浏览器与 TDBank 测试账号；也用于安装、更新或卸载 Mearl，以及排查浏览器连接和控制问题。用户未点名 Mearl、只描述这些目标时也应触发；App 客户端或容器模拟仅在明确要求时启用。
version: "2.10.0"
---

# Mearl

## 使用入口

直接通过统一的 `mearl` CLI 操作本机或远端浏览器：

```bash
mearl tab_open --payload '{"url":"https://example.com","reuse":"prefer"}'
mearl page_snapshot --payload '{"tabId":12345,"mode":"viewport"}'
mearl page_click --payload '{"tabId":12345,"selector":"@e3"}'
```

用户已经明确动作和目标、且参数确定时直接调用。action 不明确时运行 `mearl --help`；参数不确定时运行 `mearl <action> --help`。schema 会持续演进，不猜测字段名或类型。只有命令不可用或连接失败时才运行 `mearl check`，正常任务不主动探测、安装或初始化。

管理环境使用 `npx @mearl/setup <install|update|uninstall> [--local] [--cloud|--qoder-cloud] [--mcp]`。Agent 执行 `install` 或 `uninstall` 时附加 `--yes`（或 `--non-interactive`）；人工在终端执行时保留交互选择。普通远端 Agent 使用 `--cloud`，Qoder Cloud Agent 使用 `--qoder-cloud`。安装或连接异常时读取 [环境安装与连接排查](./references/troubleshooting.md)。

`set_device_emulation`、`set_timezone` 等状态设置 action 的成功响应会返回实际生效配置。任务只要求切换状态时，成功响应即结束；用户还要求检查页面内容或视觉效果时才补快照或截图。

## 环境选择

- 移动视口、移动 UA 或触摸事件使用 `set_device_emulation`；新建页面可在 `tab_open` 中传 `emulation`，让首屏直接生效。
- 只有用户明确要求模拟 App、客户端、容器环境、JSBridge 或容器栈时，才使用 `set_app_profile` 或 `tab_open.appProfile`。完整端模拟在同一个 `set_app_profile` 调用中传 `emulation`；只需桥注入时省略它。不能因页面是 H5、包含唤端链接、检测到客户端分支或普通操作失败而自行升级为容器模拟。
- 用户要求“云浏览器”、无影/无影云浏览器或 AgentBay 时，按 AgentBay 云浏览器处理；通过 connector 接入的远端浏览器不属于 AgentBay。只咨询配置或能力时不启动实例；执行任务前读取 [AgentBay 云浏览器接入](./references/api-browser-setup.md#agentbay)。
- 用户明确要求 AgentBay 串流入口、VNC/noVNC 地址或沙箱浏览器访问地址时，读取 [浏览器初始化与管理](./references/api-browser-setup.md#browser-instances)，并对指定浏览器运行 `mearl check --browser <id|名称>`。不要用进程扫描或端口探测替代该能力，也不要在普通检查中主动获取入口；返回的 `browserAccess.url` 按敏感信息处理。

AgentBay 只按任务目标选择一种会话模式：

1. **托管命名实例**：需要由当前宿主管理 Session、Context 和计费生命周期时，用 `name + provider: "agentbay"`。连接运行中的同名实例用 `reuse: "require"`；只有目标不存在时也允许创建才用 `reuse: "prefer"`。任务完成后用启动响应中的全局 `browserId` 调用 `browser_close`；持久化实例会保留为 `stopped`，只有用户明确要求删除 Profile 时才传 `deleteProfile: true`。
2. **Session attachment**：需要操作其他宿主创建的确切运行中 Session 时，用 `sessionId`。同步 Cookie 时通过 `--browser <本地来源 browserId>` 选择来源。任务完成后对启动响应中的全局 `browserId` 调用 `browser_release`；不要调用 `browser_close`。

## 浏览器控制工作流

同一任务取得目标 `tabId` 后，只要该 Tab 仍存在且仍是操作目标，后续快照、交互、导航和排障都显式复用它。不要为继续操作同一页面再次调用 `tab_open`。尚无可用 `tabId` 且已知 URL 时，调用一次 `tab_open` 并传 `reuse: "prefer"`；开发者指令给出当前对话绑定 Tab 时，同时传为 `openerTabId`。

1. **准备页面**：按上节选择桌面、移动或明确要求的 App 环境。首次进入或导航完成后调用一次 `page_snapshot`。长列表优先 `viewport`，已知区域使用 `rootSelector` / `rootRef`，查找单个文案或角色使用 `query`，只有确需全貌时才用 `full`。
2. **执行动作**：优先使用 `page_click`、`page_type`、`page_scroll`、`page_drag` 等结构化 action。每次快照后只使用该次返回的新 `@ref`；页面或 DOM 变化后重新建立快照。容器或 iframe 内通过 `page_eval` 得到的坐标传给 point 时使用 `coordinateSpace: "active-frame"`。
3. **判断结果**：先检查 `action.success`。`action.stage: "precondition"` 表示动作未派发，应按 `error` 修正参数或刷新快照，不读取已省略的 `observation` / `diagnostics`。成功后结合目标解析、`observation`、`navigation` 和 `openedTabs` 判断业务效果；后者已提供可继续操作的 `tabId`，无需再调用 `tab_list`。需要动作期间的 error logs、业务 requests 或埋点时显式传 `diagnostics`。
4. **按需观察**：仅在 `fullSnapshotRecommended: true` 时按 `snapshotReasons` 获取最小范围快照。滚动的 `moved` 只证明位置变化，下一步需要读取新视口时再取 viewport 快照。视觉任务、Canvas、跨域 iframe 或纯视觉变化使用 `page_screenshot`。`changed: true` 但 effects 为空不等于失败。
5. **验证终态**：对照用户要求检查当前 URL、标题和必要范围的页面内容；视觉终态使用截图。动作成功、发生导航或到达中间页面都不能单独证明任务完成。

不要在每次动作后固定执行 `page_wait`、`page_snapshot` 或 `page_screenshot`。无需 DOM/导航观察时可传 `observe: false`；显式传入 `diagnostics` 时仍会返回诊断增量。无前置动作的独立等待才使用 `page_wait`。

`browser_release` 不是常规任务收尾。按 `sessionId` 接入 AgentBay 的任务必须用它收尾：它会移除本机 attachment，同时保留云端 Session、页面和已写入的 Cookie。其他浏览器只在用户明确要求结束调试、退出接管或清理会话资源时调用；该动作会立即清除设备/时区模拟、会话级 Mock、录制和持续采集。用户要求的终态依赖这些效果时必须保持控制，不能释放。

## 操作约束

- 默认后台操作，不为读取、快照、截图或普通交互抢占用户焦点。只有用户要求前台展示，或任务明确依赖真实用户手势且后台操作失败时才激活页面。
- 结构化 action 无法取得所需状态时，用一次只读 `page_eval` 返回最小必要信息，拿到 selector 后回到结构化 action；直接修改 DOM 或合成事件仅作最后手段。
- hover 后立即点击等无需中间判断的紧密序列使用一次 `run_actions`；需要根据每一步变化决策时逐步调用普通 action。
- CLI 截图使用 `--output <绝对路径>` 保存后交给图像查看能力，不把 base64 stdout 放进上下文。大体积 payload 使用 `--payload-file` 或顶层字段的 `"@<绝对路径>"` 文件引用。
- Agent 为读取参考或排障主动打开的过程 Tab，确认不再使用时可按已知 `tabId` 关闭；不关闭复用的既有页面、用户原有页面或承载任务终态的页面。
- `browser_list` 默认聚合本机和远端 connector。后续优先使用返回的完整实例名称；名称重名、短名歧义或需要交付精确目标时使用全局 `browserId`，不要依赖名称片段模糊匹配。

## 专用 Skill 路由

用户提供内部内容站、Figma、LogInsight 或 FlyEye 的链接和相应领域任务时，读取 [相关 Skill 路由](./references/related-skills.md)。只有站点或业务对象与任务意图同时匹配时才使用专用 Skill；普通浏览、点击、截图或网页调试继续使用 Mearl。

匹配的专用 Skill 已在当前会话可用时，遵循其说明完成领域任务，Mearl 只提供底层浏览器或登录态能力。未安装时最多提示一次名称和收益；未经用户明确同意不代为安装。用户拒绝、要求继续或专用 Skill 不适用时，立即回到通用工作流。

<a id="references"></a>

## 场景参考

- [常规网页自动化](./references/api-page-automation.md)：打开页面、快照、交互、等待、导航、上传与批量动作
- [页面排障与视觉验证](./references/api-page-debugging.md)：选中元素、iframe、JavaScript 与截图
- [接口与埋点调试](./references/api-request-debugging.md)：HTTP/MTop、权限、请求采集、埋点与 Mock
- [浏览器初始化与管理](./references/api-browser-setup.md)：connector、浏览器选择与普通/托管浏览器生命周期
- [页面测试环境准备](./references/api-page-environment.md)：设备、App、时区模拟与 Cookie
- [身份与测试账号](./references/api-identity-accounts.md)：当前用户信息与 TDBank
- [相关 Skill 路由](./references/related-skills.md)：按站点和任务意图使用专用 Skill
- [环境安装与连接排查](./references/troubleshooting.md)：本机、CDP、远端 connector 与 Qoder 配对
