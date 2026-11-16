---
name: mcp-auto-test
description: MCP 服务自动化测试 — 直连 SSE 连通性测试、Dify 注册验证、Qoder 配置同步、报告生成
---

# MCP 服务自动化测试

## Overview

本 skill 是 MCP 服务的端到端自动化测试工具，覆盖 **直连 SSE 连通性验证**、**Dify 平台注册**、**Qoder 配置同步** 三大能力。与通用的 qa-e2e-runner 分离，专门处理 MCP 协议层面的测试，确保所有 MCP 服务在 Dify 平台上可正常注册、授权和调用，同时通过直连 SSE 端点验证服务本身的可用性。

**触发关键词**：用户说"测试 MCP 连通性"、"注册 MCP"、"MCP 测试"时触发此 skill。

---

## 工具脚本位置

所有脚本均位于 `test-project/mcp测试工具/` 目录下：

| 脚本 | 用途 |
|------|------|
| `dify_smart_mcp.py` | Dify 一键注册（主入口），自动登录 + 创建 + 授权 + 刷新，依赖 `dify_auto_mcp.py` |
| `dify_auto_mcp.py` | Dify 底层注册库，支持手动子命令 create/list/delete/auth/refresh/tools |
| `mcp_connectivity_test.py` | 直连 SSE 端点的连通性测试，不依赖 Qoder 配置 |
| `qoder_auto_mcp.py` | Qoder MCP 配置管理（仅读写 mcp.json 文件），支持 create/list/delete/batch-create |

---

## 执行流程

### 阶段一：环境准备

#### 1.1 读取项目配置

从 `test-project/test-config.md` 读取以下配置：

- 测试环境 URL（如 `https://dev-portal.busyming.com/subapp/mcp-market-fe/home`）
- Dify 控制台地址（默认 `https://test-metis.busyming.com`）
- Dify 登录账号密码（环境变量 `DIFY_EMAIL`、`DIFY_PASSWORD`）
- Workspace ID

#### 1.2 获取 MCP 服务清单

两种方式（优先使用方式 A）：

**方式 A — 从配置文件读取**：

从 `test-project/test-config.md` 中读取已知的 SSE 地址列表。当前已知的 5 个 CV 类 MCP 服务：

| 服务名 | SSE 端点 | 说明 |
|--------|----------|------|
| `pallet-cv-mcp-real` | `{gateway}/pallet-cv-mcp-real/sse` | 托盘类 CV 算法 |
| `product-cv-mcp-real` | `{gateway}/product-cv-mcp-real/sse` | 商品类 CV 算法 |
| `environment-cv-mcp-real` | `{gateway}/environment-cv-mcp-real/sse` | 环境类 CV 算法 |
| `personnel-cv-mcp-real` | `{gateway}/personnel-cv-mcp-real/sse` | 人员类 CV 算法 |
| `goods-shelf-cv-mcp-real` | `{gateway}/goods-shelf-cv-mcp-real/sse` | 货架类 CV 算法 |

默认网关地址：`https://test-ai-gateway.busyming.com/mcp-servers/`

**方式 B — 通过浏览器 agent 获取**：

访问测试环境 MCP 列表页，抓取当前已注册的 MCP 服务列表及其 SSE 地址。

#### 1.3 确认测试范围

向用户展示待测服务清单，包括：
- 服务名称
- SSE 端点地址
- 预期工具数量

**必须等待用户确认后再执行后续阶段。**

---

### 阶段二：Qoder 配置同步（轻量）

> 本阶段仅做配置文件同步，确保 Qoder 的 mcp.json 与网站服务清单保持一致。**不提示重启 Qoder，不通过 Qoder 调用工具。** 实际验证全部走直连 SSE（阶段三）。

#### 2.1 检查已配置服务

```powershell
python test-project/mcp测试工具/qoder_auto_mcp.py list
```

检查 Qoder 当前已配置的 MCP 服务列表，对比阶段一获取的服务清单。

#### 2.2 添加缺失服务配置

如有缺失服务，使用 `qoder_auto_mcp.py` 添加（仅写 mcp.json 文件）：

```powershell
python test-project/mcp测试工具/qoder_auto_mcp.py create --name <服务名> --url <sse_url>
```

或使用批量创建：

```powershell
python test-project/mcp测试工具/qoder_auto_mcp.py batch-create --services <json配置>
```

> **备注**：配置写入仅作为"确保 Qoder 配置与网站同步"的辅助操作，后续不依赖 Qoder 进行任何工具调用验证。

---

### 阶段三：直连 SSE 全量测试（核心）

#### 3.1 检查测试图片清单

测试前先检查是否存在图片清单文件 `test-project/mcp测试工具/mcp工具测试图片清单.md`。

**如果存在图片清单** → 进入 **真实图片测试模式**（推荐）：
1. 解析清单中的「工具与测试图片映射」表，获取每个工具对应的测试图片 COS 路径
2. 对每个工具，使用对应的真实图片进行 `tools/call` 调用测试（而非仅发送 `tools/list`）
3. 验证返回结果是否包含有效数据（`success=true`，有具体结果字段）

**如果不存在图片清单** → 退回到 **tools/list 连通性测试模式**：
- 仅通过 `tools/list` 验证服务可达性和工具列表完整性
- 在报告中标注"仅 tools/list 测试，未使用真实图片验证"

#### 3.2 运行测试脚本

```powershell
python test-project/mcp测试工具/mcp_connectivity_test.py --report
```

常用参数：
- `--report`：生成 Markdown 测试报告
- `--service <name>`：仅测试指定服务
- `--gateway <url>`：自定义网关地址

#### 3.3 测试流程（每个服务 4 步）

1. **可达性检测**：连接 SSE 端点，获取 session endpoint
2. **初始化握手**：发送 `initialize` 请求 + `notifications/initialized` 通知
3. **工具列表获取**：发送 `tools/list`，获取全部工具清单
4. **全工具逐一调用**：对获取到的 **全部工具** 逐一调用，验证返回结果（这是唯一验证工具可调用的途径）

#### 3.4 真实图片测试参数构造

**常规工具**（使用 `cosPath` 参数）：

从图片清单映射表中获取工具对应的 COS 路径，构造 `tools/call` 请求参数。脚本会自动从工具的 `inputSchema` 中提取图片参数名（优先 `filePath`），使用清单中的真实图片路径替换默认路径。

示例（detectLightSwitch）：

```json
{
  "filePath": "mcp工具测试图片/开关灯检测.jpg"
}
```

**特殊工具 `detectIsolationNet`**（使用 `imageUrl` + `id` 参数）：

该工具的参数格式与其他 CV 工具不同，不接受 `cosPath`，而是接受直链 URL：

```json
{
  "imageUrl": "https://img9.kcimg.cn/imga/1/1276/1276974.jpg_1200xx.jpg",
  "id": "test-001"
}
```

> **注意**：`detectIsolationNet` 不在图片清单映射表中（因其参数格式不同），需使用固定的直链 URL 进行测试。有效测试图片 URL：`https://img9.kcimg.cn/imga/1/1276/1276974.jpg_1200xx.jpg`

#### 3.5 返回结果验证

对 `tools/call` 的返回结果进行有效性验证：

- **成功判定**：响应中包含 `success=true` 或有效结果字段（如 `personCount`、`anomaly`、`lightStatus` 等具体业务字段）
- **失败判定**：响应超时、返回错误信息、或结果字段为空

#### 3.6 默认测试图片（回退用）

当图片清单不存在或某工具在清单中无对应图片时，使用以下默认图片路径：

```
product-inventory/prod/bigdata/OTMX001/20260522/sku_1779438980716_20260522_163620717_3n0qoy.png
```

---

### 阶段四：Dify 侧注册与验证

#### 4.1 环境变量准备

确保以下环境变量已设置：

```powershell
$env:DIFY_EMAIL = "<Dify登录邮箱>"
$env:DIFY_PASSWORD = "<Dify登录密码>"
```

#### 4.2 批量注册 MCP 服务

对每个 MCP 服务执行一键注册：

```powershell
python test-project/mcp测试工具/dify_smart_mcp.py <sse_url> --force-refresh --cookie-jar "$env:TEMP\dify_mcp_cookie.jar" --auth-env "$env:TEMP\dify_mcp_auth.env"
```

参数说明：
- `<sse_url>`：MCP 服务的完整 SSE 端点地址
- `--force-refresh`：强制刷新工具列表（即使已注册也重新拉取）
- `--cookie-jar`：登录 cookie 持久化路径（使用 `$env:TEMP` 而非 `/tmp`）
- `--auth-env`：认证信息环境变量文件路径

#### 4.3 验证注册状态

注册完成后，逐一检查每个服务：
- 授权状态（是否已 auth）
- 工具数量（与预期对比）
- Provider 状态是否正常

```powershell
python test-project/mcp测试工具/dify_auto_mcp.py list
python test-project/mcp测试工具/dify_auto_mcp.py tools --provider <provider_id>
```

#### 4.4 注册失败处理

如果出现注册失败（特别是 HTTP 500 错误）：

1. 记录失败的服务名和错误信息
2. 提示用户：**需先在 Dify UI 中手动删除该 Provider 的旧记录，然后重新运行注册**
3. 不要自动重试，避免重复创建

---

### 阶段五：生成测试报告

#### 5.1 输出位置

```
test-project/test-reports/mcp-connectivity-report-{YYYYMMDD}.md
```

#### 5.2 报告格式

```markdown
# MCP 连通性测试报告

- **测试日期**：YYYY-MM-DD HH:MM:SS
- **测试人员**：AI 自动化测试
- **网关地址**：https://test-ai-gateway.busyming.com/mcp-servers/
- **测试方式**：真实图片测试 / 仅 tools/list 测试

## 测试结果总览

| 维度 | 服务名 | 工具数 | 通过数 | 结果 |
|------|--------|--------|--------|------|

## 一、直连 SSE 连通性测试

### 服务名
- 端点可达性：✅/❌
- 协议握手：✅/❌
- 工具列表获取：✅/❌
- 工具调用结果表（每个工具的成功/失败/超时状态，标注是否使用真实图片）

## 二、Dify 平台注册与授权

### 服务名
- 注册状态（成功/失败）
- 授权状态
- 工具导入数量
- 错误信息（如有）

## 三、Qoder 配置同步状态

| 服务名 | 配置状态 | 备注 |
|--------|----------|------|
（仅列出配置同步结果，无工具调用结果）

## 四、问题与建议

- 列出所有发现的问题
- 给出修复建议

## 五、网关非标准行为说明

- 列出网关层面的非标准 MCP 协议行为（如有）
```

#### 5.3 报告生成方式

直连 SSE 部分使用 `mcp_connectivity_test.py --report` 自动生成（报告中需标注使用真实图片测试还是仅 tools/list 测试）；Dify 部分由 skill 汇总阶段四的结果后追加写入报告；Qoder 配置同步状态由阶段二的结果生成简要列表。

---

## 注意事项

### 全自动执行

**整个测试流程无需人工介入，不需要重启 Qoder。** 直连 SSE 测试和 Dify 注册均为自动化执行，Qoder 配置同步仅写文件，不依赖 Qoder 运行时。

### MCP 工具全覆盖

**每个服务的全部工具都必须测试，不得仅选取单个代表工具。** 这是硬性要求。

### 真实图片测试优先

**当图片清单 `mcp工具测试图片清单.md` 存在时，必须使用真实业务图片进行 tools/call 调用测试，禁止仅通过 tools/list 判断工具可用性。** 图片清单中包含每个工具对应的真实测试图片 COS 路径，应按映射关系逐一调用验证。`detectIsolationNet` 因参数格式不同（使用 `imageUrl` 直链而非 `cosPath`），使用固定测试 URL `https://img9.kcimg.cn/imga/1/1276/1276974.jpg_1200xx.jpg` 进行验证。

### Windows 环境适配

- 使用 `curl.exe` 而非 `curl`（PowerShell 中 `curl` 是 `Invoke-WebRequest` 的别名）
- 临时文件路径使用 `$env:TEMP` 而非 `/tmp`
- PowerShell 中使用分号 `;` 分隔命令，不使用 `&&`
- Python 脚本执行时使用 `python` 命令

### 临时文件清理

执行完毕后，删除所有临时文件：
- `$env:TEMP\dify_mcp_cookie.jar`
- `$env:TEMP\dify_mcp_auth.env`
- 其他执行过程中产生的临时文件

### 截图规则

- 仅在发现 Bug 时截图
- 截图保存到 `test-project/bug-reports/screenshots/` 目录
- 文件名格式：`mcp-{服务名}-{问题类型}-{时间戳}.png`

### 超时设置

| 操作 | 超时时间 |
|------|---------|
| SSE 连接 | 10s |
| 初始化握手 | 15s |
| 工具调用 | 30s |
| POST 请求 | 10s |

### Dify 已知问题

- 若 Provider 已存在但状态异常（HTTP 500），需先在 Dify UI 中手动删除再重新注册
- `ADMIN_API_KEY` 需手动在 Dify 自部署环境中启用
- Console API MCP 管理端点有时返回 HTTP 500，需排查是否为平台故障

---

## 快速命令参考

```powershell
# 直连 SSE 全量测试 + 生成报告
python test-project/mcp测试工具/mcp_connectivity_test.py --report

# 直连 SSE 测试单个服务
python test-project/mcp测试工具/mcp_connectivity_test.py --service pallet-cv-mcp-real

# Dify 一键注册单个服务
python test-project/mcp测试工具/dify_smart_mcp.py "https://test-ai-gateway.busyming.com/mcp-servers/pallet-cv-mcp-real/sse" --force-refresh --cookie-jar "$env:TEMP\dify_mcp_cookie.jar" --auth-env "$env:TEMP\dify_mcp_auth.env"

# 查看 Qoder 已配置的 MCP 服务（配置同步检查用）
python test-project/mcp测试工具/qoder_auto_mcp.py list

# 添加 Qoder MCP 配置（仅写文件，无需重启）
python test-project/mcp测试工具/qoder_auto_mcp.py create --name <服务名> --url <sse_url>

# 查看 Dify 已注册的 Provider 列表
python test-project/mcp测试工具/dify_auto_mcp.py list
```
