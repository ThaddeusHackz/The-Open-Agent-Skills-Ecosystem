---
name: enable-chatlog-rule
description: "自动在 .qoder/rules 或 AGENTS.md 中添加对话日志保存规则。当用户说'添加chatlog规则'、'保存对话记录'、'对话日志统计'、'记录AI对话'、'/enable-chatlog' 时使用本技能。| Auto-inject a chatlog rule into .qoder/rules or AGENTS.md so every AI conversation is persisted for statistics."
---

# Enable Chatlog Rule — 对话日志规则注入

> 一句话定义：让 **团队管理者/讲师** 在 **项目初始化或规范升级时** 通过 **交互式问答** 快速在 `.qoder/rules/` 或 `AGENTS.md` 中 **注入对话日志保存规则**，使所有 AI 对话可追溯、可统计

---

## 触发条件

当用户说以下内容时触发：

- "添加 chatlog 规则"、"保存对话记录"
- "记录 AI 对话"、"对话日志"、"对话统计"
- "chatlog"、"conversation log"
- "所有对话保存到文件"
- "/enable-chatlog"

---

## 使用场景

### 应该使用

- 项目需要追踪 AI 对话历史用于复盘或统计
- Workshop/培训场景需要收集学员与 AI 的交互记录
- 团队要求所有 AI 操作可审计
- 需要统计 AI 使用频率、Token 用量、任务完成率等指标

### 不应使用

- 项目已配置了完善的 chatlog 规则
- 只想查看单次对话历史（直接翻阅即可）
- 需要实时流式日志（应使用专门的 observability 工具）

---

## 执行步骤

```
1. 询问规则注入位置（.qoder/rules/ 还是 AGENTS.md）
2. 询问日志保存格式和内容范围
3. 询问存储路径和命名规则
4. 生成规则内容并写入目标文件
5. 输出验证方法和统计建议
```

### 步骤 1：询问注入位置

向用户确认规则写入位置：

| 位置 | 优点 | 适用场景 |
|------|------|---------|
| `.qoder/rules/chatlog-rule.md` | 独立文件，易维护，Qoder 自动加载 | **推荐**：团队项目、长期使用 |
| `AGENTS.md`（追加章节） | 与项目导航合并，一目了然 | 简单项目、快速配置 |
| 两者都写 | 双重保障 | 重要项目 |

**默认**：如果用户未明确选择，默认写入 `.qoder/rules/chatlog-rule.md`。

### 步骤 2：确认日志格式和内容

| 格式 | 说明 | 适用场景 |
|------|------|---------|
| **Markdown**（默认） | 人类可读，便于 Review | 培训/Workshop |
| **JSONL** | 结构化，便于程序解析统计 | 数据分析、自动化报表 |
| **两者都要** | Markdown 归档 + JSONL 统计 | 企业级审计 |

日志应包含的内容：

| 字段 | 必选 | 说明 |
|------|------|------|
| 时间戳 | ✅ | 对话开始/结束时间 |
| 任务摘要 | ✅ | 一句话描述本次对话完成了什么 |
| 涉及文件 | ✅ | 创建/修改/读取的文件列表 |
| 关键决策 | 可选 | 重要的技术决策和理由 |
| Token 用量 | 可选 | 输入/输出 Token 数（如可获取） |
| 用户评价 | 可选 | 用户对本次交互的满意度 |

### 步骤 3：确认存储路径

| 选项 | 路径 | 说明 |
|------|------|------|
| **项目内**（默认） | `.chatlog/` 或 `chatlog/` | 跟随项目版本控制 |
| **临时目录** | `.tmp/chatlog/` | 不纳入 Git |
| **自定义** | 用户指定 | 灵活配置 |

文件命名规则：`{YYYY-MM-DD}-{序号}.{md|jsonl}`
例如：`2026-04-11-001.md`、`2026-04-11-001.jsonl`

### 步骤 4：生成规则内容

根据收集的信息生成规则文件。

### 步骤 5：输出验证方法

告诉用户如何验证规则生效。

---

## 具体实现

### 规则模板 A：.qoder/rules/chatlog-rule.md

> **关键**：规则文件必须包含 `trigger: always_on` frontmatter，否则 Qoder 不会加载。

```markdown
---
trigger: always_on
---

# Chatlog 对话日志规则

## 规则说明

每次 AI 对话结束时，**必须**将本次对话摘要保存到项目的 `{LOG_DIR}/` 目录。

## 日志保存要求

### 触发时机

- 每次对话中完成了**实质性工作**（代码修改、文件创建、问题分析等）后
- 用户明确表示当前任务结束时
- 对话即将结束前（作为最后一步）

### 日志内容（Markdown 格式）

在 `{LOG_DIR}/` 下创建文件，命名为 `{YYYY-MM-DD}-{HHmm}.md`：

\```markdown
# 对话日志 {YYYY-MM-DD HH:mm}

## 任务摘要
[一句话描述本次对话完成了什么]

## 涉及文件
- [创建] path/to/new-file
- [修改] path/to/changed-file
- [读取] path/to/read-file

## 关键决策
- [决策1及理由]

## 耗时
- 开始：{开始时间}
- 结束：{结束时间}

## 备注
[其他需要记录的信息]
\```

### 日志内容（JSONL 格式，可选）

同时追加一行到 `{LOG_DIR}/sessions.jsonl`：

\```json
{"timestamp":"{ISO8601}","summary":"...","files_created":[],"files_modified":[],"files_read":[],"decisions":[],"duration_minutes":0}
\```

## 注意事项

- 日志文件由 AI 自动创建，无需用户手动操作
- `{LOG_DIR}/` 目录不存在时自动创建
- 敏感信息（密码、Token、密钥）**禁止**写入日志
- 日志内容应简洁，每条不超过 50 行
```

### 规则模板 B：AGENTS.md 追加段落

```markdown

---

## 📝 对话日志规则（Chatlog）

> 所有 AI 对话必须留痕，便于复盘和统计

### 规则

每次对话完成实质性工作后，在 `{LOG_DIR}/` 目录创建日志文件：

- **文件名**：`{YYYY-MM-DD}-{HHmm}.md`
- **内容**：任务摘要 + 涉及文件 + 关键决策
- **格式**：Markdown（人类可读）

### 约束

- ❌ 禁止记录密码、Token、密钥等敏感信息
- ❌ 禁止修改已有日志文件
- ✅ 目录不存在时自动创建
- ✅ 每条日志不超过 50 行
```

### .gitignore 配置

如果 chatlog 目录不需要纳入版本控制，提示用户在 `.gitignore` 中添加：

```
# AI 对话日志（不纳入版本控制）
chatlog/
.chatlog/
```

如果需要纳入版本控制（如 Workshop 场景），则不添加。

### 操作流程

1. **确认目标文件存在**：
   - `.qoder/rules/`：若目录不存在则创建
   - `AGENTS.md`：若文件不存在则创建
2. **写入规则内容**：使用 `create_file` 或 `search_replace` 工具
3. **创建 chatlog 目录**（如不存在）
4. **更新 .gitignore**（按用户选择）
5. **写入一条示例日志**验证路径可用

---

## 输出格式

### 正常输出

```markdown
## ✅ Chatlog 规则已配置

### 规则写入位置

| 文件 | 状态 |
|------|------|
| `.qoder/rules/chatlog-rule.md` | ✅ 已创建 |
| `{LOG_DIR}/` 目录 | ✅ 已创建 |

### 规则内容摘要

- **日志格式**：{Markdown / JSONL / 两者}
- **存储路径**：`{LOG_DIR}/`
- **命名规则**：`YYYY-MM-DD-HHmm.md`
- **纳入 Git**：{是/否}

### 验证方法

完成一次 AI 对话后，检查 `{LOG_DIR}/` 目录下是否自动生成了日志文件。

### 统计方法建议

- **对话次数**：统计 `{LOG_DIR}/` 下文件数量
- **活跃天数**：统计日志文件中不重复的日期
- **高频文件**：从日志中提取"涉及文件"做词频统计
- 如使用 JSONL 格式，可用 `jq` 或 Python 脚本批量分析
```

### 拒答

```markdown
## ℹ️ 无需添加 Chatlog 规则

项目中已存在对话日志配置：
- [已有规则文件路径]

**建议**：如需调整，直接编辑该文件即可。
```

---

## 约束与红线

### 硬性规则

- **MUST NOT** 在日志中记录任何密码、API Key、Token、密钥等敏感信息
- **MUST NOT** 修改或删除已有的日志文件（只追加）
- **MUST NOT** 覆盖已存在的 `.qoder/rules/chatlog-rule.md`，应提示用户确认
- **MUST** 检查 AGENTS.md 中是否已有 chatlog 相关段落，避免重复添加
- 日志文件 **SHOULD** 控制在 50 行以内，避免冗长

### 决策规则

1. 用户未指定位置时，默认写入 `.qoder/rules/chatlog-rule.md`
2. 用户未指定格式时，默认使用 Markdown
3. 用户未指定路径时，默认使用 `.chatlog/`
4. Workshop 场景建议纳入 Git；企业项目建议 .gitignore 排除

---

## 关联文档

- Qoder Rules 配置：`.qoder/rules/`（项目级 AI 行为约束）
- 项目导航：`AGENTS.md`
- CoPaw 对话存储参考：`dialog/YYYY-MM-DD.jsonl`（CoPaw 原生格式）
- Qoder Settings：`.qoder/settings.json`

---

## 常见错误

### 错误 1：规则写了但 AI 不执行

**现象**：规则文件存在，但对话结束时没有生成日志
**原因**：规则文件缺少 `trigger: always_on` frontmatter
**正确做法**：在 `.qoder/rules/chatlog-rule.md` 文件顶部添加 `---\ntrigger: always_on\n---` frontmatter，使 Qoder 将其注入 `<always_on_rules>`

### 错误 2：日志中包含敏感信息

**现象**：日志文件中出现了 API Key 或密码
**原因**：规则中未明确禁止记录敏感信息
**正确做法**：规则中必须包含"禁止记录密码、Token、密钥"的红线约束

### 错误 3：日志文件过大

**现象**：单个日志文件超过 100 行，难以阅读
**原因**：记录了完整对话而非摘要
**正确做法**：日志应只包含摘要信息（任务描述 + 涉及文件 + 关键决策），不要复制完整对话
