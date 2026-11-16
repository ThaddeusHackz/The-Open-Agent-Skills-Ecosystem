---
name: generate-qoder-hooks
description: "生成 Qoder Hooks 命令拦截模板。当用户说'生成Hook'、'创建命令拦截'、'拦截危险命令'、'Qoder安全配置'、'/gen-hooks' 时使用本技能。| Generate Qoder Hooks templates for command interception and security control."
---

# Generate Qoder Hooks — 命令拦截模板生成

> 一句话定义：让 **开发者/团队管理员** 在 **项目安全配置阶段** 通过 **交互式问答 + 模板生成** 快速创建 **Qoder Hooks 命令拦截脚本和 settings.json 配置**

---

## 触发条件

当用户说以下内容时触发：

- "帮我生成 Hook"、"创建 Qoder Hook"
- "拦截危险命令"、"命令拦截"、"命令黑名单"
- "Qoder 安全配置"、"安全策略"
- "block command"、"command filter"
- "/gen-hooks"

---

## 使用场景

### 应该使用

- 新项目初始化，需要配置命令安全策略
- 团队需要定制命令黑名单（如禁止 `rm`、`DROP TABLE` 等）
- Workshop/培训场景，需要演示 Hooks 拦截机制
- 需要为已有 Hooks 添加新的拦截规则

### 不应使用

- 已有完善的 Hook 配置且无需修改
- 需要拦截的不是终端命令（如文件操作拦截，应使用其他机制）
- 只想了解 Hooks 原理（直接回答即可，不需要生成文件）

---

## 执行步骤

```
1. 询问拦截场景（预设模板 or 自定义）
2. 收集要拦截的命令/模式
3. 选择脚本类型（sh / ps1 / 两者都要）
4. 生成 Hook 脚本 + settings.json 配置
5. 输出验证指南
```

### 步骤 1：询问拦截场景

向用户确认需求类型：

| 场景 | 预设规则 | 适用团队 |
|------|---------|---------|
| **基础安全** | `rm -rf`、`git push --force`、`DROP TABLE`、`format`、`mkfs` | 所有团队 |
| **金融合规** | 基础安全 + `curl`外发、`scp`传输、`env`泄露、敏感文件访问 | 金融/合规项目 |
| **Workshop教学** | 基础安全 + 自定义演示命令拦截 | 培训场景 |
| **自定义** | 用户指定 | 高级用户 |

### 步骤 2：收集拦截模式

向用户确认要拦截的命令列表：
- 命令关键词（如 `rm`、`drop`）
- 正则模式（如 `rm\s+-rf`）
- 是否区分大小写

### 步骤 3：选择脚本类型

| 系统 | 脚本类型 | 文件名模板 |
|------|---------|-----------|
| Linux/macOS/Git Bash | Shell | `block-{name}.sh` |
| Windows PowerShell | PowerShell | `block-{name}.ps1` |
| 跨平台 | 两者都生成 | `.sh` + `.ps1` |

### 步骤 4：生成文件

生成以下文件到 `.qoder/hooks/` 目录：

1. **Hook 脚本**（`.sh` 和/或 `.ps1`）
2. **settings.json 片段**（追加到 `hooks.before_run_command`）
3. **audit.log**（如不存在则创建空文件）

### 步骤 5：输出验证指南

告诉用户如何测试 Hook 是否生效。

---

## 具体实现

### Shell 脚本模板（.sh）

```bash
#!/bin/bash
# 功能：拦截 {DESCRIPTION}
# 生成日期：{DATE}
# 位置：.qoder/hooks/block-{NAME}.sh

# 读取输入（Qoder 传入 JSON 格式）
INPUT=$(cat)

# 提取要执行的命令
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')

# === 命令黑名单 ===
BLOCKED_PATTERNS="{PATTERNS}"

# 检查命令是否匹配黑名单
if echo "$COMMAND" | grep -qiE "$BLOCKED_PATTERNS"; then
  echo "❌ 命令已被安全策略拦截: $COMMAND" >&2
  echo "💡 规则: {DESCRIPTION}" >&2
  echo "🔒 如需执行，请联系管理员调整 .qoder/hooks/ 配置" >&2

  # 写入审计日志（如果路径存在）
  LOG_FILE=".qoder/hooks/audit.log"
  if [ -d "$(dirname "$LOG_FILE")" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] BLOCKED: $COMMAND | Rule: {NAME}" >> "$LOG_FILE"
  fi

  exit 2  # 阻断执行
fi

# 安全检查通过
exit 0
```

### PowerShell 脚本模板（.ps1）

```powershell
# 功能：拦截 {DESCRIPTION}
# 生成日期：{DATE}
# 位置：.qoder/hooks/block-{NAME}.ps1

# 读取输入（Qoder 传入 JSON 格式）
$input = $input | ConvertFrom-Json
$command = $input.tool_input.command

# === 命令黑名单 ===
$blockedPatterns = @({PS_PATTERNS})

foreach ($pattern in $blockedPatterns) {
    if ($command -match $pattern) {
        Write-Error "❌ 命令已被安全策略拦截: $command"
        Write-Error "💡 规则: {DESCRIPTION}"
        Write-Error "🔒 如需执行，请联系管理员调整 .qoder/hooks/ 配置"

        # 写入审计日志
        $logFile = ".qoder/hooks/audit.log"
        if (Test-Path (Split-Path $logFile)) {
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            Add-Content -Path $logFile -Value "[$timestamp] BLOCKED: $command | Rule: {NAME}"
        }

        exit 2  # 阻断执行
    }
}

# 安全检查通过
exit 0
```

### settings.json 配置片段

```jsonc
{
  "hooks": {
    "before_run_command": [
      ".qoder/hooks/block-{NAME}.sh"
    ]
  },
  "security": {
    "enable_command_filtering": true,
    "log_blocked_commands": true,
    "block_log_path": ".qoder/hooks/audit.log"
  }
}
```

**MUST**：如果 `settings.json` 已存在，使用 `search_replace` 将新脚本路径**追加**到 `before_run_command` 数组中，不要覆盖已有配置。

---

## 输出格式

### 正常输出

生成文件后输出：

```markdown
## ✅ Qoder Hooks 已生成

### 生成的文件

| 文件 | 用途 |
|------|------|
| `.qoder/hooks/block-{name}.sh` | Shell 拦截脚本 |
| `.qoder/hooks/block-{name}.ps1` | PowerShell 拦截脚本 |

### settings.json 已更新

已将 `block-{name}.sh` 添加到 `hooks.before_run_command` 数组。

### 验证方法

在 Qoder 中尝试执行被拦截的命令，应看到：
> ❌ 命令已被安全策略拦截: {示例命令}

### 拦截规则一览

| 模式 | 示例命令 | 说明 |
|------|---------|------|
| {pattern} | {example} | {description} |
```

### 拒答

```markdown
## ℹ️ 无需生成 Hook

当前场景不需要命令拦截：
- [ ] 原因说明

**建议**：{替代方案}
```

---

## 约束与红线

### 硬性规则

- 脚本 **MUST** 以 `exit 0`（通过）或 `exit 2`（阻断）结尾，不允许其他退出码
- 脚本 **MUST** 从 stdin 读取 JSON 并用 `jq` 提取 `.tool_input.command`
- **MUST NOT** 在脚本中执行任何命令本身，仅做匹配判断
- **MUST NOT** 拦截 `git status`、`git diff`、`ls`、`cat` 等只读安全命令
- 审计日志 **SHOULD** 记录时间戳、被拦截的命令、匹配的规则名

### 决策规则

1. 用户未指定脚本类型时，默认生成 **.sh**（Git Bash 在 Windows 也能用）
2. 用户提到"Windows"或"PowerShell"时，额外生成 **.ps1**
3. 拦截模式超过 10 个时，建议拆分为多个 Hook 脚本（按职责分组）
4. settings.json 不存在时，创建完整的初始配置文件

---

## 关联文档

- Hooks 配置指南：`.qoder/hooks/CONFIG_GUIDE.md`
- Hooks 使用说明：`.qoder/hooks/README.md`
- 现有示例脚本：`.qoder/hooks/block-dangerous-commands.sh`
- Qoder Settings：`.qoder/settings.json`

---

## 常见错误

### 错误 1：脚本没有读取 stdin

**现象**：Hook 不生效，命令直接执行
**原因**：忘记用 `INPUT=$(cat)` 从 stdin 读取 Qoder 传入的 JSON
**正确做法**：脚本首行必须读取 stdin，然后用 `jq` 提取命令

### 错误 2：exit code 不对

**现象**：Hook 运行了但没有阻断命令
**原因**：使用了 `exit 1` 而非 `exit 2`
**正确做法**：只有 `exit 2` 才会阻断命令执行，`exit 0` 表示通过，其他码行为未定义

### 错误 3：settings.json 中路径写错

**现象**：Hook 脚本存在但不被调用
**原因**：`before_run_command` 中的路径与实际文件路径不匹配
**正确做法**：使用相对于项目根目录的路径，如 `.qoder/hooks/block-xxx.sh`
