---
name: emas-push-mobile-integration
version: 0.5.7
description: 指导在 Android、iOS、HarmonyOS 原生应用，以及 Flutter、React Native、uni-app、Unity 项目中集成阿里云 EMAS 移动推送 SDK。适用于新建或现有未接入 EMAS 的 App，覆盖 SDK 安装、隐私合规初始化、通知/透传消息、APNs/厂商通道、PushV2 服务端联调、跨端验收与排障。
---

# EMAS 移动推送跨端集成

从”选择实际客户端宿主”开始，再进入共享接入流程和对应平台指南。不要把 Android 代码、iOS APNs 配置、HarmonyOS API 或框架插件配置直接套用到其他端。

## 〇、资料按需加载（必读）

`references/` 目录下所有页面都**只在需要时加载**；不要在提问或预审阶段一次性 `Read` 全部资料。以下规则优先于任何隐式”先读完再说”的倾向：

1. **Android 3.x/4.x 分流**：预审未完成前，不加载 `native-sdk-4x.md` 也不加载 `compatibility/sdk-integration-3x.md`。预审确定 4.x 后加载 `native-sdk-4x.md`；4.x 项目需要 R8/混淆规则时加载 [`proguard-rules.md`](references/android/proguard-rules.md)，**不加载** 30KB 的 3.x 基础接入页。仅当预审确定 3.x 或 3.x→4.x 迁移时才加载 `compatibility/sdk-integration-3x.md` 与 `compatibility/upgrade-to-4x.md`。
2. **厂商通道按需**：`references/android/vendors/` 下的每个厂商文件（xiaomi、huawei、honor、oppo、vivo、meizu、fcm）只在用户于 §一.5 确认要集成该厂商后才加载。预审或提问阶段不加载任何厂商文件；要集成 N 个厂商就读 N 个文件，不读其余。`vendor-overview.md` 与 `vendor-scenarios.md` 只在需要厂商选择判断或场景说明时加载。
3. **发布说明**：`compatibility/release-notes.md` 是历史变更日志，不是接入资料。只在需要当前版本线或某个具体变更点时读取相关小节；不要整页加载。版本线以 Maven 元数据实时查询为准。
4. **辅助弹窗**：`client-apis/popup-activity.md` 主要保存 3.x 回调资料。4.x 项目只在需要 `AndroidPopupActivity` 的 Manifest 注册和中转说明时读取；业务点击处理仍按 `native-sdk-4x.md` 的 `onNotificationOpened`。
5. **客户端 API 子页**：`client-apis/` 各页按实际接入所需加载，不要一次性读取全部；未用到通知统计 API、透传自建通知等能力时不加载对应页。
6. **排障页**：`troubleshooting/build-and-runtime.md` 与 `troubleshooting/error-codes.md` 只在构建或运行期出现对应问题时加载，不在接入起步阶段预读。

违反以上规则的”预读”会显著膨胀会话 token，且经常读到的内容最终用不到。

## 一、输入分析与最小 Demo 门槛

先分析用户描述、当前项目配置和已存在的推送/通知代码，推断已知信息。扫描已有推送/通知代码时排除 `.qoder/skills/`、`oh_modules/`、`node_modules/`、`build/` 等工具、依赖与生成目录；这些目录内的命中不作为"已有推送接入"的证据。不要重复询问已知字段，不索取 AppSecret、AccessKey、Token、证书或厂商密钥的实际值；只确认它们能否通过受控配置提供。

目标是先完成**安全注册和当前调试环境可执行的推送诊断**，再完成物理真机上的最终单设备投递验收。只有会阻止 SDK 集成或当前调试目标的未知输入才是必填；真机不可用只会使最终验收待办，不中断集成。

### 1. Android 原生预审：主动选择 SDK 大版本

对原生 Android 项目，首次提问前必须检查活动源码、已声明的 Gradle/version catalog/本地 AAR 依赖，以及 Gradle、AGP、JDK、Kotlin/Java、AndroidX、minSdk/compileSdk。版本证据优先级是：活动源码和实际 API 使用 → 已声明依赖 → 构建工具链；**不得**用 `app/build/`、APK/AAB 输出、Gradle 缓存或其他生成构件判断当前项目的 SDK 大版本。

- 已声明旧 EMAS 3.x 依赖、3.x 回调/API，或存在明确的旧版兼容约束时，说明证据并走 3.x 保留/4.x 迁移评估。
- 新接入且没有上述约束时，直接以 4.x 作为预选路径；不让用户无依据地选择 3.x/4.x。随后按 [Android SDK 版本选择](references/android/version-selection.md) 固定版本并构建校验系统版本要求。
- 只有 3.x 约束是否保留、或当前工具链能否支持 4.x 仍无法确定时，才用 `AskUserQuestion` 请用户在“保留 3.x”与“迁移到 4.x”间确认。
- 确定 4.x 后、写接入代码前，先执行 [Android 接入前置工程检查](references/android/project-preflight.md)：建议 AGP 8.1 + Gradle 8.0，低于该组合时先做构建验证，确认无 D8/JNA 崩溃；同时验证 `applicationId` 与 EMAS 控制台包名、minSdk/compileSdk、JNA/DataStore 冲突。未通过时只进行仅代码结构接入，不得构建/注册。

### 2. 必填

仅在尚未确定时询问：

- 实际客户端宿主：原生 Android、iOS、HarmonyOS，或 Flutter、React Native、uni-app、Unity；框架项目还需确定实际 Android/iOS 目标。
- 每个目标的应用标识：Android `applicationId`、iOS Bundle ID 或 HarmonyOS 应用标识。
- 是否已有其他推送 SDK、旧版 EMAS、通知展示者或通知点击/深链接处理器；存在时必须确定唯一的初始化、展示和点击处理权。
- 是否存在与应用标识匹配的 EMAS 控制台应用，以及 AppKey/AppSecret 的受控配置可用性。
- 用户同意隐私政策后执行注册、Token 上报的时机。
- Android 的测试环境和 deviceId 方案：模拟器可用于构建、安装、同意 UI、通知权限/通道、初始化/注册、deviceId 展示复制及日志诊断；物理真机只在最终单设备投递、后台/杀进程和已启用厂商通道验收时必需。
- 条件必填：iOS Demo 的 APNs 通道预检。确认客户端 AppKey/AppSecret 的受控注入位置与引用名、APNs 凭据仅托管在 Apple/EMAS 控制台或受控密钥库、当前 Bundle ID、Sandbox/开发或生产环境、凭据类型和 EMAS 映射均可做非敏感校验；不索取任何实际 Secret、证书、私钥或 Token。HarmonyOS Demo 还需基础 Push Kit/Token 前置配置。

### 3. 可选（未回复使用默认值）

| 输入 | 默认值 |
| --- | --- |
| 构建变体 | 当前可运行的开发/调试变体；生产环境延后 |
| 目标地区 | 沿用现有 EMAS 应用区域，不创建或迁移区域 |
| PushV2 服务端归属 | 先用控制台或人工单设备测试；服务端自动化延后 |
| Android 厂商离线通道 | 不启用 |
| iOS 生产 APNs | 仅配置当前 Demo 所需开发环境；生产环境延后 |
| HarmonyOS 进阶通道能力 | 不启用，仅完成基础路径 |
| Notification Extension / 通知扩展 | 不接入 |
| 后台长连接 | 不启用 |
| 自定义通知样式、消息协议 | 使用最小通知或透传载荷 |
| 高级深链接与业务路由 | 复用现有入口；没有时使用最小 Demo 处理器 |
| 灰度、监控、生产迁移 | Demo 成功后再处理 |

未确定的可选项按第 4 节通过交互式提问确认；其中影响离线送达的 Android 厂商离线通道，无论用户是否提及，都在开始执行前按第 5 节确认。

### 4. 通过交互式提问收集未确定输入

分析完成后，先用一段简短文本陈述已确认的事实，不罗列问题清单；然后把每个未确定输入转换成 agent 的交互式提问（如 AskUserQuestion 工具），让用户直接选择，而不是输出纯文本问题等待回复。

**硬门禁**：只要仍有任何未确定的必填项，或当前平台相关的可选项，本轮回复必须实际调用 `AskUserQuestion`；禁止只写“需要确认”“将提问”等过渡文本后以 `end_turn` 结束。必须等到提问工具返回选择结果，才能进入计划、编辑或其他集成执行；首次调用将不超过四项的相关问题合并提出。

- 必填与可选项的未确定输入都通过提问工具提出。
- 必填项的每个问题给出具体候选选项（如“改为 EMAS 应用包名 / 新建匹配的 EMAS 应用”），不留开放空答。
- EMAS 控制台应用匹配问题必须让用户逐字核对应用标识：选项形如“控制台包名与项目应用标识完全一致 / 不一致（请提供控制台包名）/ 尚未创建”。不得只问“是否已创建应用”——用户按记忆确认会掩盖包名不匹配，问题会推迟到注册或投递阶段才暴露，迫使中途改动应用标识。
- 原生 Android 的测试环境问题必须提供精确选项“用本地模拟器验证”“使用物理 Android 真机”“暂未准备调试设备”。将“本地模拟器”“模拟器调试”等同义自定义回答按“用本地模拟器验证”处理；该选项后继续集成，不再追问会导致暂停的真机前置问题。
- 选择模拟器或暂未准备物理真机时，继续完成 SDK 集成与可执行诊断，并明确记录“物理真机最终验收待办”；禁止将“暂缓集成”作为默认或因真机缺失自动生成的选项。
- 可选项只问与当前平台和需求相关的，按类别合并为少量问题；每题把默认值作为带推荐标记的选项，用户跳过或选默认即按默认继续。
- 单次提问数量超过工具上限时分批提问；与当前端无关的项（如 iOS 项目问 Android 厂商通道）不问。
- 提问中不出现 AppSecret、AccessKey、Token、证书等实际值，只确认其受控可用性。
- 用户选择 APNs、FCM 或任一 Android 厂商通道后，**下一轮** `AskUserQuestion` 必须确认：客户端配置和控制台/服务端凭据分别存于何种受控位置、非敏感配置引用名，以及可否完成元数据预检；在此之前不得读取所选通道的详细资料、添加通道依赖、初始化/注册或测试投递。可选位置仅描述类型，例如 CI/Secret Manager、未跟踪的本地 `.xcconfig`/属性文件、Apple/EMAS/厂商控制台托管；绝不读取或输出其中的实际值。
- 元数据预检只检查当前变体应用标识、EMAS 应用映射、配置引用是否存在并会在缺值时失败；APNs 另检查 Bundle ID、环境、凭据类型及 EMAS 上传/映射状态，FCM/厂商通道只检查所选通道要求的非敏感项目/应用标识和引用解析状态。任一项不可用时明确逐项记录缺失条件，继续路径仅限安全注入接口和业务路由等**仅代码结构接入**；不得宣称远程注册、Token 上报、EMAS deviceId、实际送达或验收成功。

必填与可选都没有未确定项时，不提问，直接进入对应平台资料。

### 5. 开始执行前的通道凭据与离线投递确认

目标端存在离线投递通道（Android 厂商/FCM、iOS APNs）且用户选择接入时，必须在写任何通道代码前先完成第 4 节的受控位置确认和元数据预检：

- Android 厂商/FCM：若未提供必要配置，先说明仅 EMAS 自有通道在进程结束或被系统回收后无法及时收到通知，部分厂商系统后台送达也不可靠；让用户选择接受限制先完成基础通道 Demo，或准备该通道的受控配置再集成。选择集成时，先核验项目/应用标识、非敏感引用名及其解析状态，再读取该厂商页面。
- iOS APNs：先核验当前 Bundle ID、开发或生产环境、正常签名构建的 Push Notifications entitlement、APNs 凭据类型及 Apple/EMAS 控制台映射；客户端 AppKey/AppSecret 只能从受控构建配置引用，APNs 私钥或证书不得进入项目。任何一项未满足时，只能进行本地注入或仅代码结构接入，不得注册、上报 Token、读取 EMAS deviceId 或声称真实 APNs 送达。

用户明确确认且预检通过后才开始对应通道集成；已明确不需要离线送达时跳过 Android 厂商/FCM 确认。HarmonyOS Push Kit 属于其 Demo 的条件必填，未提供时按同样方式说明限制并确认 Demo 范围。

来源和版本更新规则见 [资料来源与更新规则](references/shared/source-authority.md)。

## 二、所有 App 先走共享流程

无论新项目还是尚未接入 EMAS 的既有 App，按此顺序执行：

1. 识别真实 Android/iOS/HarmonyOS 宿主、应用标识、已有推送依赖和通知/点击路由；原生 Android 先执行本页第 1 节的 3.x/4.x 预审。
2. 核对 EMAS 应用与当前 Demo 环境；选定 APNs、FCM 或厂商通道时，先完成受控位置确认与元数据预检（应用标识、EMAS 映射、配置引用；APNs 再含环境、签名 entitlement 和控制台映射），不将 AppSecret、服务端 AccessKey、证书、Token 或厂商密钥写入仓库。
3. 预检通过后按平台资料完成 SDK、系统能力和通道配置；按隐私政策控制 `register`、Token 上报及后台连接的时机。预检未通过时只完成安全注入接口和业务路由等仅代码结构接入，逐项记录缺失条件，不执行或宣称注册/送达验证。
4. 每次新增或升级 SDK、厂商通道依赖后，立即执行一次构建，校验其对最低系统版本的要求（Android minSdk、iOS deployment target、HarmonyOS API 版本）；要求高于项目当前配置时，先让用户决定是否提升，再继续写接入代码。构建或包管理工具不在 PATH 时，先按平台资料的工具链发现步骤定位官方安装位置（如 DevEco Studio 内置 ohpm/hvigor）再执行；不得仅因 PATH 缺失跳过构建，把编译验证留给用户。
5. 让平台回调只进入应用统一的“消息、通知展示、通知打开”业务处理器。
6. 在当前调试环境读取 deviceId 或平台 Token 并完成可执行诊断；Android 模拟器可完成构建、注册、通知 UI 与日志检查。启动本机模拟器时**禁止 `-no-window`**，让用户能看到安装、同意弹窗和通知栏等真实过程；可保留 `-no-audio`、`-no-boot-anim` 等不影响画面可见性的参数。iOS Simulator 不得一概认定为不能接收 APNs：只有满足 Apple 当前支持条件、正常签名的开发构建含 `aps-environment=development`、APNs/EMAS Sandbox 映射已核验、用户已同意通知、系统 Token 与 `CloudPushSDK.registerDevice` 成功时，才可通过 EMAS 控制台或 PushV2 对 Simulator deviceId 做真实开发 APNs 投递；`xcrun simctl push` 只用于本地 payload/UI/delegate/点击路由注入，必须标为“非 APNs、非 EMAS”。物理真机可用后再完成后台/杀进程、冷启动、生产环境和已启用厂商通道的最终验收；不可用时记录为待办，不停止集成。
7. SDK 接入与当前调试环境的本地诊断完成后，在要求用户点击设备 UI、继续设备操作或作出完成结论**之前**，必须实际调用 `AskUserQuestion`，让用户选择“我自行测试（推荐：输出交接命令）”或“请 Agent 协助测试”。选择自行测试后，停止未获授权的设备/控制台操作，立即输出第 六 节的手动交接；选择 Agent 协助测试后，只执行基于已探测工程配置的安全、可观察构建/部署/启动/日志操作，隐私/通知授权、物理设备交互和 EMAS 控制台远程投递仍由用户完成或明确授权。设备、凭据或远程投递前置缺失时，也必须提供此选择，但测试状态记录为 pending。
8. 无论测试方式，按第 六 节输出“测试交接与会话收尾”及“控制台/PushV2 测试参数清单”：包括实际已验证证据、未完成用例、基于工程探测值的手动命令和本次实际设置的非敏感参数；不要求用户提供未配置字段，也不凭空猜测命令。

完整决策表和上线约束见 [既有 App 首次接入](references/shared/existing-app-integration.md) 与 [应用身份、凭据与隐私合规](references/shared/app-identity-and-consent.md)。

**进入平台步骤的最小门槛**：仅需完成本节“必填”中适用的未知项和当前端的条件必填项。可选项采用默认值，不阻塞 SDK 集成或单设备推送 Demo。

## 三、完成共享流程后选择客户端路径

| 场景 | 入口 | 必做事项 |
| --- | --- | --- |
| 原生 Android | [Android SDK 版本选择](references/android/version-selection.md) | 先做 3.x/4.x 预审，再配置通知、厂商通道、R8/ABI |
| 原生 iOS | [iOS SDK](references/ios/native-sdk-integration.md) | APNs、Xcode capabilities、Token 上报、通知 delegate |
| 原生 HarmonyOS | [HarmonyOS SDK](references/harmonyos/native-sdk-integration.md) | `@aliyun/push`、`UIAbility`、通知授权、点击生命周期 |
| Flutter | [Flutter 插件](references/cross-platform/flutter.md) | Dart 桥接 + Android/iOS 宿主配置 |
| React Native | [React Native 插件](references/cross-platform/react-native.md) | JS 桥接 + Android/iOS 宿主配置 |
| uni-app | [uni-app 插件](references/cross-platform/uni-app.md) | DCloud 插件 + Android/iOS 宿主配置 |
| Unity | [Unity 插件](references/cross-platform/unity.md) | C# 桥接 + Android/iOS 构建配置 |

框架项目先阅读 [跨平台插件与原生宿主边界](references/cross-platform/overview-and-native-ownership.md)。当前官方插件资料不提供 HarmonyOS 插件路径；HarmonyOS 走原生 SDK。

## 四、平台补充入口

- **Android**：先完成 [SDK 版本选择](references/android/version-selection.md)，再查看 [厂商通道](references/android/vendors/vendor-overview.md) 的厂商选择、原生厂商 SDK 和场景说明；构建、安装与运行环境问题见 [构建与运行排障](references/android/troubleshooting/build-and-runtime.md)。
- **iOS**：[APNs、能力与注册](references/ios/apns-capabilities-and-registration.md)、[消息与通知处理](references/ios/notification-and-message-handling.md)、[Notification Extension](references/ios/notification-extension.md)、[排障](references/ios/troubleshooting.md)。
- **HarmonyOS**：[Push Kit Token](references/harmonyos/push-kit-third-token.md)、[通知与生命周期](references/harmonyos/notification-and-lifecycle.md)、[扩展与后台连接](references/harmonyos/extension-and-background-connection.md)、[排障](references/harmonyos/troubleshooting.md)。

## 五、服务端 PushV2

客户端注册并取得测试标识后，服务端按 [PushV2 接口接入指南](references/shared/server-pushv2-guide.md) 构造请求。

- `Target.Platform` 必须匹配实际目标：`ANDROID`、`IOS` 或 `HMOS`。
- 通知、透传、在线透传加离线通知、定时和持续推送各自使用对应 `PushTask` 结构。
- Android、iOS、HarmonyOS 通知字段不可互换；平台特有字段只写入对应载荷。
- 上线前遵守 [投递策略与配额](references/shared/delivery-policy-and-quotas.md)，尤其是 Android 厂商与 HarmonyOS 的消息分类限制。

## 六、验收与排障

完成任一端接入后，按 [跨端验收矩阵](references/shared/verification-matrix.md) 测试：同意隐私后的注册、deviceId/Token、前台消息和通知、后台/冷启动点击、通知授权变化、离线通道及对应 PushV2 载荷。

排障顺序固定为：应用标识和环境 → 凭据与系统能力 → 初始化/注册状态 → deviceId/Token → 平台通道 → PushV2 参数。不要通过重复注册或重复发通知掩盖配置问题。

Android 运行时 `NoClassDefFoundError` 而依赖树中已有该库时，先用 `dependencyInsight` 核查变体解析再下版本兼容结论；错误能否忽略以受影响功能的端到端验证为准，详见 [构建与运行排障](references/android/troubleshooting/build-and-runtime.md)。

### 测试交接与会话收尾

选择自行测试或 Agent 协助测试后，结束会话前都必须一次性输出：

1. **证据状态**：逐项列出“仅代码结构、注册已验证、本地注入已验证、远程请求已发出但未观察、远程送达已验证、物理设备最终验收、pending”中适用的状态，以及每项的实际证据与未完成条件。SDK 启动、系统 Token、`registerDevice` 或 Android 注册成功只能证明注册；`xcrun simctl push` 只能证明本地注入。只有已发出 EMAS 控制台/PushV2 远程请求，且目标设备实际观察到通知，才可称“远程送达已验证”。
2. **用户手动命令**：仅从已检查的工程生成可复制命令。Android 要先确认 Gradle wrapper、模块/variant、APK、`applicationId`、启动 Activity 和 ADB serial；iOS 要先确认 `.xcworkspace` 或 `.xcodeproj`、scheme、正常签名 Debug app 路径、Bundle ID 和 Simulator UDID；HarmonyOS 只有在工程和官方工具链已提供可验证的构建、部署、日志入口时才给命令。未知值标为 `<待确认>`，禁止猜测默认 `:app`、包名、Activity、scheme、UDID、产物路径或使用其他项目的路径。跨端项目必须回到实际 Android/iOS 原生宿主生成命令。
3. **命令范围**：Android 输出实际 variant 的 Gradle 构建、`adb install`、`am start`、PID/`logcat` 和适用的单设备 PushV2 检查；iOS 输出 `xcodebuild`、`simctl install`、`simctl launch --console`、`simctl spawn log stream`，只有存在本地 `.apns` payload 时才输出 `simctl push`，并标为“非 APNs、非 EMAS”。命令不得含密钥、Token、证书或服务端 AccessKey。
4. **有界诊断**：对每个未变化的配置状态，至多收集一次正常签名构建、配置/entitlement、注册日志和远程投递证据。证据不足时报告具体缺口并标 pending；除非用户修改配置或提供新证据，不得通过重复构建、重装、重注册、二进制字符串/符号探查来延长排障或制造验证结论。

详细命令边界见 [Android 构建与运行排障](references/android/troubleshooting/build-and-runtime.md)、[iOS APNs 验证](references/ios/apns-capabilities-and-registration.md) 和 [跨端验收矩阵](references/shared/verification-matrix.md)。

### 完成集成后必须输出的测试参数清单

接入代码与当前调试环境验证完成后，**必须在同一条回复**内给出一份可直接粘贴到 EMAS 控制台或 PushV2 调用脚本的参数清单，不要等用户追问。只列出本次接入**实际设置或已知**的字段；未配置的字段不要编造占位。Android 清单通常包含：

- `AppKey`（来自 EMAS 控制台应用；不写出实际密钥，仅标"已配置"或"待用户填入"）
- `Target.Type = DEVICE`、`Target.Platform = ANDROID`、`Target.Value = <已捕获的 deviceId，或"测试页长按复制">`
- 通知消息载荷：`Notification.Title`/`Body` 示例文本、`Notification.Android.ChannelId`（与应用代码中 `NotificationChannel` 的 ID 完全一致）、`Notification.Android.VendorChannelActivity`（点击通知打开的 Activity 全限定类名，对应 Manifest 中声明的处理入口）、`Notification.Android.ExtParameters`（若接入代码用到了 extraMap 路由）
- 透传消息载荷：`Message.Title`/`Body`（若接入了 `onMessage`）
- 已启用的每个厂商通道对应的额外字段（如华为 `Android.Huawei.*`、小米 `Android.Xiaomi.*`、FCM `Android.GCM.*` 等），按各厂商接入页实际写入的值列出

iOS 清单按本次实际配置列出 `Target.Type = DEVICE`、`Target.Platform = IOS`、已捕获的 EMAS deviceId（或获取路径）、`Notification.Ios.ApnsEnv`、`Badge`、`Music`、`ExtParameters` 和点击路由字段；AppKey 只标“已配置/待配置”，APNs 私钥、证书和服务端 AccessKey 一律不输出。仅当已完成正常签名、系统 Token、`registerDevice` 与 EMAS 映射预检时，才给出 Simulator Sandbox 或物理设备的真实单设备投递参数；`simctl push` 本地注入不属于 APNs/EMAS 测试，不得伪装成 PushV2 参数。HarmonyOS 按对应平台的 `Hmos` 字段给出同样的清单。清单后附一段说明：用户可在控制台“推送高级接口”或 [PushV2 接口接入指南](references/shared/server-pushv2-guide.md) 的示例请求体中替换上述字段发起单设备测试；物理真机可用后必须再跑第 六 节用例 3/4，真机不可用时保留为待办。

### 模拟器启动规则

本机启动 Android 模拟器用于验证时，`emulator -avd <name>` **不要加 `-no-window`**——用户需要看到安装、同意弹窗、通知栏等真实交互过程。可保留 `-no-audio`、`-no-boot-anim`、`-no-snapshot` 这类不影响画面可见性的加速参数；前台运行即可，不必用 `nohup` 后台化。

### iOS Simulator 测试证据边界

iOS Simulator 只允许报告以下三种明确状态，不得把它们混用：

1. **仅代码结构接入**：通道凭据预检、Apple 平台条件、正常签名/entitlement、APNs/EMAS 映射、通知同意、系统 Token 或 `registerDevice` 任一项未满足；只能验证安全注入接口和业务路由，逐项列出缺失条件，不报告注册或送达成功。
2. **本地注入测试**：使用 `xcrun simctl push` 注入 `.apns` payload，只能证明通知 UI、`UNUserNotificationCenterDelegate`、payload 解析和点击路由；结果必须标为“非 APNs、非 EMAS”，不能证明 DeviceToken、`registerDevice`、EMAS deviceId 或 PushV2 送达。
3. **真实 Sandbox APNs/EMAS 测试**：Apple 当前支持 Simulator APNs 的主机、Xcode 和运行时条件已核验，使用正常签名的开发构建（含 `aps-environment=development`），并完成 Bundle ID、APNs 凭据、EMAS 映射、通知授权、系统 Token 和 `CloudPushSDK.registerDevice`。此时才可用 EMAS 控制台或开发环境 `IOS` PushV2 向该 Simulator 的 EMAS deviceId 投递。

`CODE_SIGNING_ALLOWED=NO` 的构建不能用作第 3 类的任何证据。即使第 3 类通过，物理设备仍须完成后台/终止态、冷启动、生产 APNs 与最终交付验收。

## 七、参考索引

| 分类 | 入口 |
| --- | --- |
| 共享流程、来源、验收 | [shared/](references/shared/) |
| Android 原生与兼容资料 | [android/](references/android/)，接入前必读 [工程检查](references/android/project-preflight.md)，调试面板见 [debug-info-panel.md](references/android/debug-info-panel.md) |
| iOS 原生 | [ios/](references/ios/) |
| HarmonyOS 原生 | [harmonyos/](references/harmonyos/) |
| Flutter、React Native、uni-app、Unity | [cross-platform/](references/cross-platform/) |
