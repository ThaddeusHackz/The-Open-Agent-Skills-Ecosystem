---
name: mml-parser-zhiyisoft
description: MML解析工具技能，通信领域专用TXT解析，全面兼容厂家所有指令，可高效导出CSV、Excel、DB等格式文件。
---

# MML解析工具（知一 Zhiyisoft）

## 技能介绍
**Skill Introduction**

MML解析工具技能，面向通信领域专用 TXT 数据解析，全面兼容厂家所有指令，可高效导出 CSV、Excel/XLSX、DB 等格式文件。通过用户另行安装并配置的知一官方本地解析工具及 MCP Server，在不上传 TXT 正文的前提下，完成版本与身份验证、AI 权益预检、报表选择、解析进度查询和结果导出。社区版本 Skill 压缩包不包含 MCP、Bridge、EXE 或客户端配置。

The MML Parser skill is designed for telecom TXT data, supports all vendor commands, and efficiently exports CSV, Excel/XLSX, DB, and other file formats. It uses the separately installed and configured official Zhiyisoft local parser and MCP Server to verify versions and identity, check AI entitlements, select reports, report parsing progress, and export results without uploading TXT contents. The Community Edition Skill archive contains no MCP, Bridge, EXE, or client configuration.

## 版本与运行要求
**Version and Runtime Requirements**

技能版本：`1.3.8`  
MCP Server/Bridge 版本：`1.3.8`  
解析工具 EXE 要求：必须与云端最新版本完全一致（本版本发布时为 `1.3.8`）。  
+社区版本说明：本压缩包仅包含 Skill 指导、协议说明、界面元数据和图标；不包含 MCP Server、Bridge、EXE、安装脚本或 MCP 配置。

Skill version: `1.3.8`  
MCP Server/Bridge version: `1.3.8`  
Required EXE version: exactly the cloud latest version (`1.3.8` at this release).  
+Community Edition: this archive contains only Skill instructions, protocol guidance, UI metadata, and an icon; it contains no MCP Server, Bridge, EXE, installer, or MCP configuration.

仅使用客户端已经公开的官方 `mml_*` 工具。若 `mml_status` 不可用，立即停止并告知用户需从知一官网下载、安装并配置与云端最新版本完全一致的官方客户端和 MCP Server；社区版本不得自行下载、嵌入、模拟或绕过 MCP。不得点击 GUI、直接调用客户端 EXE、独立解析 TXT、上传 TXT 正文、虚构文件大小、跳过工作流阶段或推断用户已同意。

Use only the official `mml_*` tools already exposed by the client. If `mml_status` is unavailable, stop and tell the user to download, install, and configure the official client and MCP Server whose versions exactly match the cloud latest release. The Community Edition must not download, embed, imitate, or bypass MCP. Never click the GUI, invoke the client EXE directly, parse TXT independently, upload TXT content, invent file sizes, skip a workflow stage, or infer user consent.

## 强制响应纪律
**Mandatory Response Discipline**

对于每次工具返回结果：

For every tool result:

1. 执行其他操作前，先读取 `workflow_stage`、`next_action`、`must_relay`、`user_message` 和 `required_inputs`。  
   Read `workflow_stage`, `next_action`, `must_relay`, `user_message`, and `required_inputs` before doing anything else.
2. 如果 `must_relay=true`，必须先向用户转述 `user_message` 的实质内容，再进行下一次工具调用。  
   If `must_relay=true`, tell the user the substance of `user_message` before the next tool call.
3. 只执行 `next_action`。如果要求停止，则必须停止，不得猜测其他操作。  
   Perform only `next_action`. If it says stop, stop. Do not guess an alternative action.
4. 使用工具计算的文件数量和大小，不得根据文件名或用户描述估算。  
   Use tool-calculated file counts and sizes. Never estimate them from filenames or user prose.
5. 将 `overage_offer`、`entitlement_calculation` 和 `available_reports` 作为权威结果。  
   Treat `overage_offer`, `entitlement_calculation`, and `available_reports` as authoritative.

## 必须遵循的工作流
**Required Workflow**

### 1. 验证版本与身份
**1. Verify Version and Identity**

首先调用 `mml_status`；已知实际模型名称时必须一并传入。

Call `mml_status` first with the actual model name when known.

- 如果返回 `software_not_found`，告知用户并调用 `mml_download_latest`，且必须由用户在 Windows 本机确认。  
  For `software_not_found`, tell the user and call `mml_download_latest`; require the native Windows confirmation.
- 如果返回 `software_upgrade_required` 或 `integration_upgrade_required`，停止后续操作，直至 EXE、Skill 和 MCP 与云端最新版本完全一致。  
  For `software_upgrade_required` or `integration_upgrade_required`, stop until EXE, Skill, and MCP exactly match the cloud latest version.
- 如果返回 `user_status=unregistered`，告知用户必须进行本机确认，然后调用 `mml_start_trial`；必须原样转述 `试用期仅XXX天有效`。  
  For `user_status=unregistered`, tell the user that native confirmation is required and call `mml_start_trial`. Relay `试用期仅XXX天有效` verbatim.
- 如果身份为有效激活或试用状态，告知用户身份验证成功并进入文件收集步骤。  
  For a valid activated/trial identity, tell the user identity verification succeeded and move to file collection.
- 如果身份已过期、无效或返回 `device_credential_auth_failed`，转述原因并停止；不得将 HTTP 401 当作未注册。  
  For expired, invalid, or `device_credential_auth_failed`, relay the reason and stop. Never treat HTTP 401 as unregistered.

### 2. 收集本地 TXT 路径
**2. Collect Local TXT Paths**

要求用户提供一个或多个本地 TXT 文件或目录的绝对路径。不得要求用户自行计算文件数量或大小。调用 `mml_preflight`，该工具必须计算并返回：

Ask for one or more absolute local TXT file or directory paths. Do not ask the user to calculate file counts or sizes. Call `mml_preflight`; it must calculate and return:

- `input_file_count`（输入文件数量 / input file count）
- `input_total_bytes` 和 `input_total_size`（输入文件总大小 / total input size）
- `max_file_bytes` 和 `max_file_size`（最大单文件大小 / maximum file size）
- 权益判断结果  
  the entitlement decision
- 必要时返回完整的权益兑换计算过程  
  the full exchange calculation when necessary

### 3. 说明权益判断结果
**3. Explain the Entitlement Decision**

对于 `preflight_completed`，告知用户可信的文件数量、总大小、最大文件大小以及无需兑换权益，然后使用 `preflight_id` 调用 `mml_scan_start`。

For `preflight_completed`, tell the user the trusted file count, total size, maximum file size, and that no exchange is required. Then call `mml_scan_start` with `preflight_id`.

必须严格解释配额：仅包含一个 TXT 的请求不属于批次，不受批次总字节数、批次文件数和每日批次数限制；但解析成功后仍会消耗单文件限制以及每日累计文件数和字节数额度。包含两个或更多 TXT 的请求属于批次，适用全部相关批次限制。

Quota interpretation is strict: a request containing exactly one TXT is not a batch. It is exempt from batch total-bytes, batch file-count, and daily batch-count limits, but it still consumes the single-file and daily cumulative file/byte limits after successful completion. Requests with two or more TXT files are batches and use all applicable batch limits.

对于 `overage_consent_required`：

For `overage_consent_required`:

1. 转述文件数量、总大小和最大文件大小。  
   Relay the file count, total size, and maximum file size.
2. 转述 `entitlement_calculation.calculation_steps` 中的每一行。  
   Relay every line in `entitlement_calculation.calculation_steps`.
3. 说明 `required_units`、`unit_days_cost`、总 `days_cost`、当前限制、请求值以及兑换后的目标限制。  
   State `required_units`, `unit_days_cost`, total `days_cost`, current limits, requested values, and target limits after exchange.
4. 询问用户是否同意兑换所述激活天数。  
   Ask whether the user agrees to exchange the stated activation days.
5. 用户拒绝则停止；用户同意则调用 `mml_confirm_overage`，且仍必须由用户在 Windows 本机确认。  
   If the user declines, stop. If the user agrees, call `mml_confirm_overage`; the native Windows confirmation remains mandatory.
6. 兑换成功后，转述消耗天数并调用 `mml_scan_start`。  
   After successful exchange, relay the consumed days and call `mml_scan_start`.

不得仅因用户最初的解析请求看似允许，就调用 `mml_confirm_overage`。

Never call `mml_confirm_overage` merely because the original parse request sounded permissive.

### 4. 扫描报表
**4. Scan Reports**

调用 `mml_scan_start`，然后按照 `poll_after_seconds` 调用 `mml_job_status`，直至扫描完成或失败。

Call `mml_scan_start`, then call `mml_job_status` after `poll_after_seconds` until scanning completes or fails.

扫描完成后：

When scanning completes:

1. 向用户提供完整的 `available_reports` 清单。  
   Tell the user the complete `available_reports` list.
2. 询问用户需要导出哪些报表。  
   Ask the user which reports to export.
3. 接受明确的报表名称清单，或用户明确要求导出全部报表。  
   Accept either an explicit report-name list or an explicit request for all reports.
4. 不得默认选择全部报表，也不得传入 `available_reports` 中不存在的报表。  
   Never silently choose all reports. Never pass a report not present in `available_reports`.

### 5. 说明选项并应用推荐默认值
**5. Explain Options and Apply Recommended Defaults**

解析前向用户说明以下选项。如果用户未要求非默认值，直接使用推荐默认值，不要针对每项设置分别提问。

Before parsing, tell the user these options. If the user has not requested a non-default value, use the recommended default directly without asking a separate question for every setting.

- 输出格式：`csv`（推荐，透明且便于检查）、`xlsx`（工作簿）或 `db`（SQLite 数据库）。  
  Output format: `csv` (recommended; transparent and easy to inspect), `xlsx` (workbook), or `db` (SQLite database).
- 拆分模式：`partial`（推荐，仅拆分已识别结构）、`all` 或 `none`。  
  Split mode: `partial` (recommended; split only recognized structures), `all`, or `none`.
- 压缩：`false`（推荐，可直接检查和追溯）或 `true`。  
  Compression: `false` (recommended; directly inspectable and traceable) or `true`.

推荐默认值为 `output_format=csv`、`split_mode=partial` 和 `compress=false`。输出路径始终为必填项，报表选择没有隐含默认值。

Recommended defaults are `output_format=csv`, `split_mode=partial`, and `compress=false`. The output path is always required. Report selection has no implicit default.

### 6. 开始解析并报告进度
**6. Parse and Report Progress**

使用已完成的 `scan_job_id`、输出路径、所选报表和设置调用 `mml_parse_start`。必须传入以下两种形式之一：

Call `mml_parse_start` with the completed `scan_job_id`, output path, selected reports, and settings. Pass either:

- `reports=[...]`；或  
  `reports=[...]`; or
- 仅当用户明确选择全部报表后，传入 `select_all_reports=true`。  
  `select_all_reports=true` only after the user explicitly chose all reports.

然后按照返回的 `poll_after_seconds`（通常为 5 秒）轮询 `mml_job_status`。

Then poll `mml_job_status` according to the returned `poll_after_seconds` (normally 5 seconds).

- 告知用户解析已从 `progress_percent=0` 开始。  
  Tell the user parsing has started at `progress_percent=0`.
- 运行期间至少每隔 `user_update_after_seconds`（通常为 30 秒）报告 `stage`、`progress_percent`、`status_text` 和 `elapsed_seconds`。  
  While running, report `stage`, `progress_percent`, `status_text`, and `elapsed_seconds` at least every `user_update_after_seconds` (normally 30 seconds).
- 将 `progress_percent` 视为整个任务的进度：本地并发解析占 0–95%，导出占 95–99.5%，只有全部输出文件成功发布后才能达到 100%。  
  Treat `progress_percent` as whole-job progress: concurrent local parsing occupies 0–95%, export occupies 95–99.5%, and 100% is valid only after every output file is successfully published.
- `stage_progress_percent` 表示当前阶段内部进度。不得用猜测的文件数量百分比替代按字节加权的整体进度。  
  `stage_progress_percent` is the progress within the current stage. Never replace the byte-weighted whole-job percentage with a guessed file-count percentage.
- 阶段变化、任务失败或任务完成时也必须立即报告。  
  Also report immediately when the stage changes, the task fails, or the task completes.
- 未返回预计完成时间时，不得虚构 ETA。  
  Do not invent an ETA when none is returned.

### 7. 报告完成结果
**7. Report Completion**

对于 `parse_completed`，立即告知用户解析和导出已完成。说明生成的输出路径、所选报表、输入文件数量和总大小、输出格式、拆分模式、压缩选项、耗时、身份与配额状态，以及遥测已上传或待上传状态。

For `parse_completed`, immediately tell the user parsing and export finished. Include generated output paths, selected reports, input file count and total size, output format, split mode, compression choice, elapsed time, identity/quota state, and telemetry uploaded/pending state.

云端审计状态在最终解析授权时变为 `processing`，只有成功用量事件上传后才变为 `completed`。解析失败时报告 `failed`，且不消耗每日 TXT 数量、字节数或批次数。如果因网络不可用导致遥测待上传，应说明签名后的本地队列重试后，云端配额与记账数据才可能更新。

Cloud audit status changes from `processing` at final parse authorization to `completed` only when the successful usage event is uploaded. A failed parse reports `failed` and consumes no daily TXT count, bytes, or batch count. If telemetry is pending because the network is unavailable, explain that cloud quota/accounting may update after the signed local queue is retried.

## 安全与配额规则
**Security and Quota Rules**

- 仅接受用户选择的本地路径。  
  Accept only local paths selected by the user.
- 仅使用官方 EXE，或使用经过公开清单验证、SHA-256 和 PE 文件头均匹配的 HTTPS 下载文件。  
  Use only the official EXE or a manifest-verified HTTPS download with matching SHA-256 and PE header.
- 不得直接调用客户端 EXE。调用必须使用由用户另行安装且与云端发布清单一致的官方 MCP Server/Bridge；客户端会验证其直接父进程 SHA-256，并使用由云端签名、有效期 90 秒、仅可使用一次且绑定设备密钥和请求摘要的授权。  
  Never invoke the client EXE directly. Calls must use the separately installed official MCP Server/Bridge that matches the cloud release manifest; the client validates its direct parent process SHA-256 and consumes a cloud-signed, 90-second, one-use authorization bound to the device key and request digest.
- 不得向授权服务器发送 TXT 正文；遥测仅使用文件基本名称和汇总元数据。  
  Never send TXT bodies to the licensing server. Telemetry uses basenames and aggregate metadata only.
- 不得泄露激活码、令牌、凭据、密钥、原始指纹、硬件标识、客户或订单数据、异常堆栈以及本地日志。  
  Never expose activation codes, tokens, credentials, keys, raw fingerprints, hardware identifiers, customer/order data, tracebacks, or local logs.
- 只有已激活用户才能兑换激活天数；以服务器签名、短时有效且仅可使用一次的兑换方案为权威依据。  
  Only activated users may exchange activation days. Treat the signed, short-lived, one-time server offer as authoritative.
- 云端预检失败时必须安全关闭，绝不绕过版本、身份、配额、同意或遥测控制。  
  Treat cloud preflight failure as fail-closed. Never bypass version, identity, quota, consent, or telemetry controls.
- 诊断响应或新增 AI 客户端时读取 `references/protocol.md`。  
  Read `references/protocol.md` when diagnosing responses or adding an AI client.
