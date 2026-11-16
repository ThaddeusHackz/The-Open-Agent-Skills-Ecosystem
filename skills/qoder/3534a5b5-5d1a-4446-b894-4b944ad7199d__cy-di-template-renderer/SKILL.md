---
name: cy-di-template-renderer
description: 指导 AI 渲染 DataWorks 数据集成（DI）任务的 JSON 模板。包括按源库类型选择模板、动态列生成、占位符替换优先级、文件名推算、控制字符校验等最佳实践。适用于 DataWorks 数据集成节点生成、ETL 模板渲染、多源同步配置场景。
---

# DataWorks DI JSON 模板渲染指南

## 1. 模板文件组织

按源库类型和数据流向预置模板文件：

| 源库/场景 | 模板文件名 |
|----------|-----------|
| MySQL → ODPS | `mysql2odps.json` |
| Oracle → ODPS | `oracle2odps.json` |
| DB2 → ODPS | `db22odps.json` |
| OceanBase → ODPS | `ob2odps.json` |
| 达梦 → ODPS | `dm2odps.json` |
| OSS → ODPS（文件采集） | `oss2odps.json` |
| ODPS → OSS（备份） | `odps2oss.json` |

### 加载建议
- 启动时预加载所有 `template/di/*.json` 到内存 Map
- 缓存未命中时降级为磁盘读取
- 模板文件以 UTF-8 编码保存

## 2. 按业务场景选择模板

```
IF INTEGRATION_TYPE = 1 (DB 采集):
    根据 SOURCE_DB_TYPE 选择对应模板
    1 -> mysql2odps.json
    2 -> oracle2odps.json
    3 -> db22odps.json
    4 -> ob2odps.json
    5 -> dm2odps.json

IF INTEGRATION_TYPE = 2 (FILE 采集):
    固定使用 oss2odps.json

IF 备份流程 (BAK):
    固定使用 odps2oss.json
```

## 3. 动态列生成

DI JSON 中的 `column` 数组**不应硬编码**，需要按字段映射表动态生成。

### 查询规则
```sql
SELECT * FROM etl_meta_ods_info
WHERE trg_table_name = ? AND is_enable = 'Y'
ORDER BY src_col_position
```

### 生成逻辑
- **Reader 列**：取 `src_col_name` 列表
- **Writer 列**：取 `trg_col_name` 列表
- **列索引数组**：按 Reader 列长度生成 `[0, 1, 2, ...]`，用于部分模板配置
- **无匹配记录时**：Reader 使用 `["*"]`，Writer 留空

### 示例
```json
{
  "column": [
    {"index": 0, "type": "string"},
    {"index": 1, "type": "string"}
  ]
}
```

## 4. 占位符替换规则

### 替换优先级
```
业务级配置 > 全局公共配置
```

### 核心占位符

#### 全局公共配置来源
| 占位符 | 来源字段 | 说明 |
|-------|---------|------|
| `${PROJECT_NAME}` | ETL_PUBLIC_CONF.PROJECT_NAME | DataWorks 工作空间 |
| `${datasource}` | ETL_PUBLIC_CONF.datasource | OSS 数据源名称 |
| `${encoding}` | ETL_PUBLIC_CONF.encoding | 文件编码 |
| `${fieldDelimiter}` | ETL_PUBLIC_CONF.fieldDelimiter | 转换后列分隔符 |
| `${fieldDelimiterOrigin}` | ETL_PUBLIC_CONF.fieldDelimiterOrigin | 原始列分隔符 |
| `${lineDelimiter}` | ETL_PUBLIC_CONF.lineDelimiter | 转换后行分隔符 |
| `${lineDelimiterOrigin}` | ETL_PUBLIC_CONF.lineDelimiterOrigin | 原始行分隔符 |
| `${ossPath}` | ETL_PUBLIC_CONF.OSS_PATH | OSS 路径模板 |
| `${Rerun}` | ETL_PUBLIC_CONF.Rerun | 重跑权限 |
| `${rerun_ct}` | ETL_PUBLIC_CONF.rerun_ct | 重跑次数 |
| `${rerun_gap_time}` | ETL_PUBLIC_CONF.rerun_gap_time | 重跑间隔 |
| `${is_limit_flow}` | ETL_PUBLIC_CONF.is_limit_flow | 是否限流 |
| `${allow_err_cnt}` | ETL_PUBLIC_CONF.allow_err_cnt | 允许错误记录数 |

#### 业务配置来源
| 占位符 | 来源字段 | 说明 |
|-------|---------|------|
| `${FLW_NAME}` | ETL_JOB_CONF.FLW_NAME | 业务流程名 |
| `${IS_SIGNAL}` | ETL_JOB_CONF.IS_SIGNAL | 是否信号触发 |
| `${SIGNAL_NAME}` | ETL_JOB_CONF.SIGNAL_NAME | 信号名称 |
| `${SRC_CODE}` | ETL_JOB_CONF.SRC_CODE | 系统编码 |
| `${SRC_TABLE_NAME}` | ETL_JOB_CONF.SRC_TABLE_NAME | 源表名 |
| `${WHERE_COND}` | ETL_JOB_CONF.WHERE_COND | 过滤条件 |
| `${SPLIT_KEY}` | ETL_JOB_CONF.SPLIT_KEY | 拆分键 |
| `${ODS_TAB_NAME}` | ETL_JOB_CONF.ODS_TAB_NAME | ODS 目标表名 |
| `${TAB_NAME_T}` | 计算 | ODS 前两位替换为 T_ |
| `${TABLE_TYPE}` | ETL_JOB_CONF.TABLE_TYPE | ODS 算法类型 |
| `${PRI_KEY_NAME}` | ETL_JOB_CONF.PRI_KEY_NAME | 主键字段 |
| `${cronExpress}` | ETL_JOB_CONF.cronExpress | Cron 表达式 |
| `${dd_param}` | ETL_JOB_CONF.DD_PARAM | 调度参数 |
| `${conc_num}` | ETL_JOB_CONF.conc_num | DI 并发数 |
| `${IS_CREATE_TAB}` | ETL_JOB_CONF.IS_CREATE_TAB | 是否建表 |
| `${TABLE_LIFECYCLE}` | ETL_JOB_CONF.TABLE_LIFECYCLE | 生命周期 |
| `${IS_SUBMIT}` | ETL_JOB_CONF.IS_SUBMIT | 是否提交 |
| `${IS_BAK}` | ETL_JOB_CONF.IS_BAK | 是否备份 |
| `${REMARK}` | ETL_JOB_CONF.REMARK | 表备注 |

#### 字段映射来源
| 占位符 | 来源 | 说明 |
|-------|------|------|
| `${SRC_COLUMN_LIST}` | ETL_META_ODS_INFO | Reader 列列表 |
| `${TRG_COLUMN_LIST}` | ETL_META_ODS_INFO | Writer 列列表 |
| `${ODPS_COLUMN_INDEX_LIST}` | 计算 | 列索引数组 |
| `${COLUMNS_DEFINITION}` | ETL_META_ODS_INFO | ODS 建表字段定义 |
| `${COLUMNS_DEFINITION_STRING}` | ETL_META_ODS_INFO | SRC 临时表字段定义 |
| `${SOURCE_DB_NAME}` | ETL_META_ODS_INFO | 源数据源名 |
| `${SOURCE_SCHEMA}` | ETL_META_ODS_INFO | 源 Schema |
| `${FULL_TABLE_NAME}` | 计算 | schema.table 或 table |

#### 文件名相关
| 占位符 | 来源 | 说明 |
|-------|------|------|
| `${FILE_NAME}` | FileNameResolver | OSS 文件名 |
| `${FILE_NAME_OK}` | FileNameResolver | .ok 文件名 |
| `${bizdate}` | ETL_JOB_CONF.DD_PARAM | 业务日期 |

## 5. 特殊替换逻辑

### OSS_PATH 二级替换
`OSS_PATH` 配置中可能包含 `${SRC_CODE}` 占位符，需要先替换为业务编码，再注入模板上下文。

```java
String ossPath = publicConfig.getOssPath();
ossPath = ossPath.replace("${SRC_CODE}", job.getSrcCode());
context.put("ossPath", ossPath);
```

### FULL_TABLE_NAME 拼接
```java
if (StringUtils.isNotBlank(schema)) {
    fullTableName = schema + "." + tableName;
} else {
    fullTableName = tableName;
}
```

### 空值处理
占位符对应值为空时，保留原样不替换，不影响其他变量。

## 6. FILE_NAME 推算规则

### 规则
当 `FILE_NAME` 为空时，按以下模式推算：

```
S_{SRC_CODE}_{SRC_TABLE_NAME}_{ADD|ALL}_${YYYYMMDD}_01_01.dat
```

### ADD vs ALL
| TABLE_TYPE | 文件后缀 |
|-----------|---------|
| 3 / 5 | ADD |
| 6 | ALL |

### OK 文件名
将 `.dat` 替换为 `.ok`；无 `.dat` 后缀则直接追加 `.ok`。

```java
String okFileName = fileName.replace(".dat", ".ok");
if (!okFileName.endsWith(".ok")) {
    okFileName += ".ok";
}
```

## 7. 控制字符校验

模板替换前必须校验变量值是否包含非法控制字符（ASCII 0-31），发现时抛出明确异常并指明变量名。

> Shell 模板中的换行应使用转义形式 `\n`，不能包含字面换行符（ASCII 10）。

## 8. 备份流程特殊处理

备份流程（BAK）读取 ODPS 写入 OSS，Reader 数据源可能因环境不同而变化。

### 建议
- 公共配置中增加 `BAK_MC_DATASOURCE` 字段
- `odps2oss.json` 模板中使用 `${bakMcDatasource}` 占位符
- 非备份流程默认使用 `odps_first`

## 9. 检查清单

渲染 DI JSON 前确认：

- [ ] 已按源库类型/场景选择正确模板
- [ ] 字段映射查询包含 `is_enable = 'Y'` 条件
- [ ] Reader/Writer 列按 `src_col_position` 排序
- [ ] OSS_PATH 已完成 `${SRC_CODE}` 预替换
- [ ] `${FILE_NAME}` 已按规则推算（为空时）
- [ ] 所有变量值不含非法控制字符
- [ ] 备份流程的 `bakMcDatasource` 已正确设置
