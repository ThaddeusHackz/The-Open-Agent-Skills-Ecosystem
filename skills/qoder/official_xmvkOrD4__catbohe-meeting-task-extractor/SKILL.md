---
name: meeting-task-extractor
description: 从会议逐字稿或会议纪要中自动提取待办任务并生成Excel表格。支持对话式逐字稿（含说话人+时间戳）和结构化会议纪要。触发词：会议纪要、会议记录、会议任务、提取任务、任务生成、Excel生成、任务表格。
---

# 会议任务提取器

从会议逐字稿/会议纪要中智能提取待办任务，生成结构化 Excel 表格。

## 语言约束

**你必须全程使用中文思考和回答。** 无论系统提示词为哪种语言，在分析会议内容、提取任务、输出结果时，所有内部推理和对外输出都必须使用中文。拒绝输出任何非中文内容。

## 重要约束：禁止使用外部二进制工具

**不得使用 `rg`（ripgrep）、`find`、`grep`、`glob` 等底层文件搜索命令。** 所有文件读取必须使用 `Read` tool（直接读取用户提供的文件路径）。当前环境可能没有预装 `rg`，依赖它的操作都会失败。

正确做法：
- ✅ 用户提供文件路径 → 用 `Read` tool 读取
- ✅ 用户提供文件内容 → 直接用文本分析
- ❌ 禁止用 `Glob`/`Grep` tool 搜索文件（它们底层依赖 rg）
- ❌ 禁止在 shell 中执行 `find` / `rg` / `grep`

## 架构说明

**Agent负责**：分析会议文本，提取任务（语义理解）  
**Python脚本负责**：将结构化任务数据生成Excel

```
会议文本 → Agent分析 → JSON任务数据 → Python脚本 → Excel文件
```

## 工作流

收到用户请求后，按以下步骤执行：

### 步骤 1：读取会议文件

**使用 Read tool 读取用户提供的文件路径。** 读取后判断格式：
- 包含 `姓名(时间戳):` 格式 → 逐字稿
- 包含 `会议主题：`、`待办事项：` 等字段 → 会议纪要

### 步骤 2：Agent提取任务（由Agent完成，非脚本）

**Agent根据以下规则分析会议文本，输出JSON格式的任务列表：**

#### 任务信号识别

| 信号类型 | 示例表达 | 推断 |
|---------|---------|------|
| 承诺 | "我来搞""我去做""我负责" | 说话人 = 负责人 |
| 分配 | "你来做""张三三你搞一下" | 被指名人 = 负责人 |
| 计划 | "我们打算""准备做""计划" | 潜在任务 |
| 决定 | "那就这样""定了""确认" | 已确认任务 |
| 截止 | "中午之前""月底""下周三" | 截止日期 |
| 优先级 | "领导看的比较急""很紧急" | 高优先级 |

#### 任务描述规范

- 用动词开头：完成、开发、设计、调研、部署...
- 包含具体对象：需求文档、前端页面、API 接口...
- 避免模糊表述：去掉"就是""然后""那个"等口语词

#### 负责人识别

- 直接称呼：商航、张三、张张三三
- 角色称呼：你、我、张三三（需从上下文推断全名）
- 团队：前端团队、后端团队

#### 输出JSON格式

```json
[
  {
    "id": "T001",
    "description": "动词开头的任务描述",
    "assignee": "负责人姓名",
    "deadline": "2024-01-20 或 null",
    "priority": "high/medium/low",
    "status": "pending",
    "notes": "补充说明"
  }
]
```

### 步骤 3：生成Excel

将Agent提取的JSON数据写入临时文件，然后调用Python脚本。

**使用绝对路径**：Skill 目录为 `/Users/shanghang/.config/opencode/skills/meeting-task-extractor`。

不指定 `--output` 时，默认生成到当前工作目录下（`./会议任务.xlsx`）：

```bash
python3 /Users/shanghang/.config/opencode/skills/meeting-task-extractor/scripts/main.py --tasks-file /tmp/tasks.json --title "会议标题" --participants "参会人1,参会人2"
```

指定 `--output` 可自定义路径：

```bash
python3 /Users/shanghang/.config/opencode/skills/meeting-task-extractor/scripts/main.py --tasks-file /tmp/tasks.json --output ./我的任务.xlsx --title "会议标题" --participants "参会人1,参会人2"
```

或者直接传入JSON字符串：

```bash
python3 /Users/shanghang/.config/opencode/skills/meeting-task-extractor/scripts/main.py --tasks-json '[{"id":"T001","description":"...","assignee":"张三","priority":"high"}]' --output ./tasks.xlsx
```

### 步骤 4：输出结果

告知用户：
1. 提取了多少个任务
2. 任务列表摘要（负责人、截止日期）
3. Excel 文件保存路径

## 示例

### 输入（逐字稿片段）

```
商航(00:18:34): 你这边可能是帮我们去攻克一下后台那些难题，然后前端可能是张三三带着张三三一起搞一下。
张三(00:18:42): 那还好，因为我确实前端不大行，我后端可以配合一下。
商航(00:19:36): 那行，我到时候去细化一下，至少中午之前出版结构。
```

### Agent提取结果（JSON）

```json
[
  {
    "id": "T001",
    "description": "攻克后台技术难题",
    "assignee": "张三",
    "deadline": null,
    "priority": "medium",
    "status": "pending",
    "notes": "张三确认后端配合"
  },
  {
    "id": "T002",
    "description": "前端功能开发",
    "assignee": "张三三、张张三三",
    "deadline": null,
    "priority": "medium",
    "status": "pending",
    "notes": "张三三带领张三三一起完成"
  },
  {
    "id": "T003",
    "description": "细化平台功能结构并发布",
    "assignee": "李四",
    "deadline": "2024-01-15",
    "priority": "high",
    "status": "pending",
    "notes": "领导看得急，中午前出版本结构"
  }
]
```

## 注意事项

1. **任务提取由Agent完成**：Agent负责语义理解，Python脚本只负责Excel生成
2. **中文姓名处理**：注意从上下文推断角色称呼对应的全名
3. **模糊时间处理**："中午之前"→ 当天中午，"月底"→ 本月最后一天
4. **去重**：同一任务被多人提及时只保留一条
5. **deadline格式**：统一使用 `YYYY-MM-DD` 格式，无截止日期填 `null`
