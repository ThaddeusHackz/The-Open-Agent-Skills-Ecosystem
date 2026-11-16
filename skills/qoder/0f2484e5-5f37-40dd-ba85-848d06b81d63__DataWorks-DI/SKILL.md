---
name: dataworks-di-content-parser
description: >-
  Parse and analyze DataWorks data integration (DI) task Content JSON strings.
  Extract source-side configuration including datasource type, datasource name,
  database, table, columns, WHERE conditions, split key, and querySql.
  Handle function-wrapped column expressions, querySql fallback mode, and
  schema-qualified table names. Applicable to Alibaba Cloud private cloud
  (Apsara Stack) versions 3.16.2 and 3.18.6.
  Trigger keywords: DI task, data integration, Content JSON, reader parsing,
  source datasource, integration task.
---

# DataWorks DI Task Content JSON Parser

解析 DataWorks 数据集成任务的 Content JSON，提取源端（reader）配置信息。适用于阿里云专有云 3.16.2 / 3.18.6 环境。

## Content JSON 整体结构

Content 是一个 JSON 对象，核心路径为：

```
root
├── steps[]          ← 步骤数组，包含 reader 和 writer
│   ├── category     ← "reader" 或 "writer"
│   ├── stepType     ← 数据源类型（mysql / oracle / postgresql / odps / oss 等）
│   └── parameter    ← 配置参数对象
│       ├── datasource       ← 数据源名称（优先取此字段）
│       ├── table            ← 表名（可能是 "db.table" 或纯表名）
│       ├── column[]         ← 字段数组（可能是字段名或表达式）
│       ├── where            ← 过滤条件
│       ├── splitPk          ← 切分键
│       ├── querySql         ← 自定义SQL（与 column 互斥）
│       └── connection[]     ← 连接信息（备用取值路径）
│           ├── datasource
│           ├── table[]
│           └── selectedDatabase
└── setting / order  ← 运行时配置，解析时可忽略
```

## 解析规则

### 1. 定位 Reader 步骤

遍历 `steps[]`，找到第一个 `category == "reader"` 的 step。

```python
reader = next(s for s in content["steps"] if s["category"] == "reader")
```

### 2. 提取源端数据源类型

直接取 `reader.stepType`：

| stepType 值 | 含义 |
|---|---|
| `mysql` | MySQL / RDS MySQL |
| `oracle` | Oracle |
| `postgresql` | PostgreSQL |
| `sqlserver` | SQL Server |
| `odps` | MaxCompute |
| `oss` | OSS 对象存储 |
| `ftp` | FTP 文件 |
| `hdfs` | HDFS |
| `hive` | Hive |
| `dm` | 达梦数据库 |
| `gbase` | GBase |
| `adb_mysql` | AnalyticDB MySQL |

### 3. 提取数据源名称

优先级：`parameter.datasource` > `connection[0].datasource`

```python
ds_name = parameter.get("datasource") or connection[0].get("datasource")
```

### 4. 提取数据库名和表名

**路径 A：`parameter.table` 存在**
- 含 `.` → 拆分：`database.table`（如 `ob_fnc_bala_prd.BALA_CUST_DIV_DETAIL`）
- 不含 `.` → 纯表名，database 为空

**路径 B：fallback 到 `connection[0]`**
- 取 `connection[0].table[0]`（注意 table 是数组）
- 若 `connection[0].selectedDatabase` 存在，拼接为 `selectedDatabase.table`
- ⚠️ 此路径属于非标准结构，标记需关注

### 5. 提取字段列表

**情况 A：`parameter.column[]` 存在且非空**

每个元素可能是：

| 格式 | 示例 | 解析方式 |
|---|---|---|
| 纯字段名 | `"CUST_NO"` | 直接使用 |
| 函数包裹 | `"TRIM(CUST_NAME)"` | 递归剥离函数，提取最内层字段名，前缀 `tran:` |
| 常量数字 | `"0"`, `"3.14"` | 标记需关注 |
| 字符串常量 | `"'ACTIVE'"` | 标记需关注 |
| 嵌套函数 | `"UPPER(TRIM(col))"` | 逐层剥离，提取 `col`，前缀 `tran:` |

**可剥离的函数列表**（单字段变换函数）：

```
TRIM, REPLACE, UPPER, LOWER, LTRIM, RTRIM,
SUBSTR, SUBSTRING, CAST, CONVERT, COALESCE, NVL, IFNULL, NULLIF,
TO_CHAR, TO_DATE, TO_NUMBER, DATE_FORMAT,
LPAD, RPAD, LENGTH, LEN, INSTR, REGEXP_REPLACE, DECODE,
ROUND, FLOOR, CEIL, CEILING, ABS, MOD,
GREATEST, LEAST, CHAR, CHR
```

剥离规则：取函数第一个参数，递归直到得到纯标识符（`^[A-Za-z_][A-Za-z0-9_]*$`）。

**情况 B：`parameter.column[]` 不存在或为空 → querySql 模式**

- 取 `parameter.querySql`（可能是字符串或 JSON 数组）
- 若是数组，用 `; ` 拼接
- 从 SQL 中用正则提取 FROM 后的表名：`(?i)\bfrom\s+([a-zA-Z_]\w*(?:\.\w+)?)`
- ⚠️ querySql 模式强制标记需关注

### 6. 提取 WHERE 条件

直接取 `parameter.where`，注意可能含调度参数如 `${TX_DATE}`。

### 7. 提取切分键

取 `parameter.splitPk`，空字符串视为无效（置 null）。

## 输出字段映射

| 输出字段 | JSON 路径 | 说明 |
|---|---|---|
| source_datasource_type | `reader.stepType` | 源端数据源类型 |
| source_datasource_name | `reader.parameter.datasource` → fallback `connection[0].datasource` | 数据源名称 |
| source_database | 从 `table` 或 `connection[0]` 拆分 | 数据库/Schema 名 |
| source_table | 从 `table` 或 `connection[0]` 拆分 | 表名 |
| source_where | `reader.parameter.where` | WHERE 条件 |
| source_split_pk | `reader.parameter.splitPk` | 切分键（空=无效） |
| source_columns | `reader.parameter.column[]` 原始 JSON | 原始字段数组 |
| parsed_source_columns | 解析后字段名，`@\|@` 分隔 | 处理后字段列表 |
| needs_attention | `Y`/`N` | 是否需人工关注 |

## 需关注标记规则

以下情况标记 `needs_attention = "Y"`：
1. 使用了 `connection[]` fallback 路径取值
2. 使用了 `querySql` 模式（无 column 数组）
3. column 中包含常量（数字/字符串）
4. column 表达式无法解析出字段名
5. column 数组为空且无 querySql

## 专有云 3.16.2 / 3.18.6 注意事项

1. **API 版本**：使用 `v20200518` API（ListFiles / GetFile / GetBusiness / ListNodes）
2. **endpoint 注册**：专有云必须显式注册 endpoint：
   ```java
   DefaultProfile.addEndpoint(regionId, regionId, "dataworks-public", endpoint);
   ```
3. **ListFiles 兼容**：`FileType=23` 表示数据集成任务
4. **InputList 解析**：上游依赖格式为 `project.workspaceId.nodeId`，取最后一段作为 nodeId
5. **SDK 约束**：使用 `aliyun-java-sdk-dataworks-public`，注意专有云 SDK 版本可能与公有云不同
6. **querySql 格式差异**：专有云部分版本的 querySql 为 JSONArray 而非字符串，需同时兼容

## 示例解析

**输入 Content JSON（reader 段）：**
```json
{
  "stepType": "mysql",
  "parameter": {
    "datasource": "DB_ASS_OB_FNC_BALA_PRD",
    "column": ["TA_ACK_SERNO", "TRIM(CUST_NAME)", "'ACTIVE'"],
    "connection": [{
      "datasource": "DB_ASS_OB_FNC_BALA_PRD",
      "table": ["BALA_CUST_DIV_DETAIL"],
      "selectedDatabase": "ob_fnc_bala_prd"
    }],
    "where": "DATE_FORMAT(CREATE_TIME,'%Y%m%d') = '${TX_DATE}'",
    "splitPk": ""
  },
  "category": "reader"
}
```

**解析输出：**

| 字段 | 值 |
|---|---|
| source_datasource_type | `mysql` |
| source_datasource_name | `DB_ASS_OB_FNC_BALA_PRD` |
| source_database | （空，因 parameter.table 不存在，走 connection fallback） |
| source_table | `ob_fnc_bala_prd.BALA_CUST_DIV_DETAIL`（connection fallback 拼接） |
| source_where | `DATE_FORMAT(CREATE_TIME,'%Y%m%d') = '${TX_DATE}'` |
| source_split_pk | null（空字符串视为无效） |
| parsed_source_columns | `TA_ACK_SERNO@\|@tran:CUST_NAME@\|@'ACTIVE'` |
| needs_attention | `Y`（使用了 connection fallback + 含字符串常量） |

## 使用方式

当用户提供 DI 任务的 Content JSON 时，按上述规则解析并输出结构化结果。可用于：
- 批量审计数据集成任务的源端配置
- 识别需要人工关注的非标准任务（querySql 模式、复杂函数表达式）
- 生成源端数据源清单报表
- 辅助 DI 任务迁移和治理
