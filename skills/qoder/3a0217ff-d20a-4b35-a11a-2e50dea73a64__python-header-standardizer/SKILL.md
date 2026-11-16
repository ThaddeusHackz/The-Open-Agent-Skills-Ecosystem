---
name: "python-header-standardizer"
description: "Standardizes Python file headers to a uniform format. Supports custom templates via .python-header.yaml. Automatically applies when creating new .py files. Reads .python-header.yaml for author info and optional custom template. Invoke when user asks to standardize/add/correct/customize Python file headers."
---

# Python Header Standardizer

将 Python 文件头部统一为标准格式。

## 配置文件

在项目根目录创建 `.python-header.yaml`，Agent 处理前会先读取此文件：

```yaml
# Python 文件头部配置
# 请修改以下字段为你自己的信息
ide: "VSCode"          # 可选: VSCode, PyCharm, Cursor, Sublime, Jupyter, 其他
author: "Your Name"
email: "your@email.com"

# 自定义头部模板（可选）
# 不提供则使用内置默认模板
# 可用变量见 template_variables
template: |
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-
  # ===============================================================================
  # @File   : {相对路径}
  # @IDE    : {ide}
  # @Author : {author}
  # @Email  : {email}
  # @Date   : {YYYY/M/D HH:MM}
  # @Desc   : {描述}
  # ===============================================================================

# 模板变量说明（仅供文档参考，不参与逻辑执行）
template_variables:
  相对路径: "文件相对于项目根目录的路径，自动计算"
  ide: "IDE 名称，从 ide 字段读取"
  author: "作者名，从 author 字段读取"
  email: "邮箱，从 email 字段读取"
  "YYYY/M/D HH:MM": "当前时间，格式 YYYY/M/D HH:MM"
  描述: "文件功能描述，自动推断（20字以内）"
```

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `ide` | `"VSCode"` | IDE 名称 |
| `author` | `"Unknown"` | 作者名 |
| `email` | `""` | 邮箱 |
| `template` | 内置默认模板 | 自定义头部模板（可选），多行字符串，变量用 `{变量名}` 包裹。不提供则使用内置默认模板 |
| `template_variables` | — | 变量说明清单（仅文档用途，不参与逻辑） |

若配置文件不存在，Agent 会自动创建模板并提示用户。

## 标准头部模板

### 内置默认模板

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ===============================================================================
# @File   : {相对路径}
# @IDE    : {ide}
# @Author : {author}
# @Email  : {email}
# @Date   : {YYYY/M/D HH:MM}
# @Desc   : {描述}
# ===============================================================================
```

### 自定义模板

若 `.python-header.yaml` 中提供了 `template` 字段，则使用自定义模板代替内置默认模板。
模板中的变量占位符（如 `{相对路径}`、`{author}` 等）会被自动替换为实际值。
可用变量及说明见 `.python-header.yaml` 中的 `template_variables`。

## 自动模式：新建文件

当 Agent 使用 Write 工具创建 `.py` 文件时，必须自动在文件内容开头插入标准头部。

### 前置检查：配置文件

在使用 Write 创建 `.py` 文件前，先检查项目根目录是否存在 `.python-header.yaml`：

- **存在**：读取配置，检查 `template` 字段
  - 有 `template` → 使用自定义模板
  - 无 `template` → 使用内置默认模板
- **不存在**：自动创建配置文件，写入默认模板（含 `template` 字段填入内置默认模板），提示用户修改，然后继续处理

**默认模板**：

```yaml
# Python 文件头部配置
# 请修改以下字段为你自己的信息
ide: "VSCode"          # 可选: VSCode, PyCharm, Cursor, Sublime, Jupyter, 其他
author: "Your Name"
email: "your@email.com"

# 自定义头部模板（可选）
# 不提供则使用内置默认模板
# 可用变量见 template_variables
template: |
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-
  # ===============================================================================
  # @File   : {相对路径}
  # @IDE    : {ide}
  # @Author : {author}
  # @Email  : {email}
  # @Date   : {YYYY/M/D HH:MM}
  # @Desc   : {描述}
  # ===============================================================================

# 模板变量说明（仅供文档参考，不参与逻辑执行）
template_variables:
  相对路径: "文件相对于项目根目录的路径，自动计算"
  ide: "IDE 名称，从 ide 字段读取"
  author: "作者名，从 author 字段读取"
  email: "邮箱，从 email 字段读取"
  "YYYY/M/D HH:MM": "当前时间，格式 YYYY/M/D HH:MM"
  描述: "文件功能描述，自动推断（20字以内）"
```

**提示用户**：

```
已自动创建 .python-header.yaml 配置文件，请修改以下字段：
- ide: VSCode / PyCharm / Cursor / Sublime 等
- author: 你的名字
- email: 你的邮箱
- template: 可选，自定义头部模板
```

**.gitignore 处理**：

自动创建 `.python-header.yaml` 时，同时执行：
1. 检查项目根目录是否存在 `.gitignore` 文件
2. 若不存在，创建 `.gitignore` 文件
3. 若 `.gitignore` 中不包含 `.python-header.yaml`，将其追加写入
4. 无需检查项目是否为 Git 仓库，直接操作

### 新建文件流程

1. 读取 `.python-header.yaml`（不存在则按上述流程自动创建）
2. 计算字段值：
   - `@File`：新文件路径相对于项目根目录，用 `/`
   - `@IDE` / `@Author` / `@Email`：从配置读取，缺失用默认值
   - `@Date`：当前时间，格式 `YYYY/M/D HH:MM`
   - `@Desc`：根据用户创建文件的上下文（文件名、对话意图）自动推断简短中文描述，20 字以内
3. 使用 Write 工具一次性写入：标准头部 + 空行 + 用户指定的代码内容

**重要**：只有在使用 Write 工具创建新文件时才触发自动模式。使用 Edit 工具追加内容时不触发。

## 执行流程

### 1. 读取配置

首先读取项目根目录 `.python-header.yaml`。若文件不存在，自动创建模板（含 `template` 字段填入内置默认模板）并处理 `.gitignore`，提示用户填写，然后继续处理。缺失字段使用默认值。

**模板选择**：
- 配置中存在 `template` 字段 → 使用自定义模板
- 配置中无 `template` 字段 → 使用内置默认模板
- 配置文件不存在 → 自动创建后使用内置默认模板继续处理

### 2. 确定处理范围

- **指定文件**：用户明确给出文件路径，直接处理
- **批量处理**：用户要求处理全部或指定目录时，使用 Glob 扫描 `*.py`，排除 `__pycache__`、`.venv`、`venv`、`node_modules`、`.git` 等目录。先统计文件数，告知用户后确认再执行。

### 3. 处理每个文件

对每个 Python 文件，按以下决策树处理：

```
Read 文件内容
    │
    ├─ 已有标准头部（10 行格式，包含 @File/@IDE/@Author/@Email/@Date/@Desc）？
    │     ├─ @Date 为空？ → 用 Edit 填入当前时间（格式 YYYY/M/D HH:MM）
    │     ├─ @Desc 为空？ → 根据文件名和代码内容推断简短描述，用 Edit 填入
    │     └─ 两者都有值？ → 跳过
    │
    ├─ 有其他格式头部（以 # 开头的注释块，含 @File/@Author/@Date 等标记）？
    │     └─ 用 Edit 移除旧头部 → 在文件开头插入完整标准头部
    │
    └─ 无头部？
          └─ 在文件开头插入完整标准头部
```

**字段填充规则**：

| 字段 | 方式 |
|------|------|
| `模板来源` | 优先使用 `.python-header.yaml` 中的 `template` 字段，不存在则使用 SKILL.md 内置默认模板 |
| `@File` | 取文件路径相对于项目根目录的部分，统一用 `/`。例如 `d:\WorkPlace\Pycharm\cv_utils\cv_utils\__init__.py` → `cv_utils/__init__.py` |
| `@IDE` | 从配置文件读取，缺失默认 `"VSCode"` |
| `@Author` | 从配置文件读取，缺失默认 `"Unknown"` |
| `@Email` | 从配置文件读取，缺失默认 `""` |
| `@Date` | 保留原有值；若为空则填入当前时间，格式 `YYYY/M/D HH:MM` |
| `@Desc` | 保留原有值；若为空则根据文件名和代码内容推断，用中文描述，20 字以内 |

**shebang 处理**：若文件第一行已有 `#!/usr/bin/env python3`，头部模板中不再包含 shebang 行，从 `# -*- coding: utf-8 -*-` 开始。模板中 shebang 行的 `3` 对应 Python 3，若文件使用其他版本请保留原 shebang。

**头部与代码之间**：保留一个空行。

### 4. 输出报告

处理完成后，按以下格式汇总：

```
=== 头部处理完成 ===
新增：N 个文件
更新 @Date：N 个文件
更新 @Desc：N 个文件
跳过（已标准）：N 个文件
移除旧格式头部：N 个文件
```

## 异常处理

- 配置文件缺失：自动创建 `.python-header.yaml` 模板（含 `template` 字段）并处理 `.gitignore`，提示用户填写，然后继续处理
- 字段缺失：使用默认值
- 文件不存在：跳过并告警，继续处理其他文件
- 文件非 UTF-8：尝试 UTF-8 读取，失败则跳过并告警
- 文件为空：仅写入头部模板
- `@Date` 格式异常：不修改，保留原值
- 项目根目录无法确定：提示用户明确指定

## 注意事项

- 使用 Edit 工具时，`old_string` 必须精确匹配文件内容，注意缩进和换行
- 批量处理时逐个文件处理，每处理完一个报告进度
- 不要修改头部以外的任何代码