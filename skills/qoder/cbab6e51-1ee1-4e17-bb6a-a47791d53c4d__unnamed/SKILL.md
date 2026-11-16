---
name: spss-cross-tab
description: 基于 SPSS (.sav) 或 CSV 问卷数据生成分群交叉分析表（N Tables + % Tables + Table of Contents）。自动处理跳题逻辑导致的各题 Base 差异，支持灵活定义任意分群条件。输出格式严格遵循市场调研行业标准（深蓝色标题、灰色列头、绿色合计行、0% 百分比格式）。Use when the user wants to generate cross-tabulation tables from SPSS survey data, 分群交叉分析, 问卷数据出表, 人群差异对比.
---

# 问卷分群交叉分析

基于 SPSS (.sav) 或 CSV 数据文件，按用户自定义分群条件，生成包含 **N Tables**（频数）、**% Tables**（百分比）、**Table of Contents**（目录）三个 Sheet 的交叉分析 Excel。

## 核心原则

### 1. 每题独立计算 Base（最重要！）

不同题目因**跳题逻辑**或**缺失值**，有效作答人数不同。**严禁**对同一人群在所有题目上使用固定 Base。这是交叉分析最基本的计算规则。

#### 1.1 如何判断"作答了该题"

```python
# 单选题：该列不为 NaN 即为已作答
answer_mask = df[col].notna()

# 多选题：至少有一个子字段不为 NaN（或不为 0）即为已作答
sub_cols = [c for c in question_cols if c in df.columns]
answer_mask = df[sub_cols].notna().any(axis=1)
```

#### 1.2 Base 计算方式

每道题的 Base = 分群 mask **与** 作答 mask 的交集：

```python
# 正确：每题根据实际作答人数动态计算 Base
valid_mask = df[col].notna()  # 排除未作答
seg_base = int((base_masks[seg_name] & valid_mask).sum())

# 加权版
seg_base = float(df.loc[base_masks[seg_name] & valid_mask, 'weight'].sum())
```

```python
# ❌ 错误：所有题目使用同一个分群总人数作为 Base
seg_base = int(base_masks[seg_name].sum())  # 忽略了跳题逻辑！
```

#### 1.3 典型跳题场景示例

| 题目 | 跳转逻辑 | 实际作答人数（示例） |
|------|---------|-------------------|
| q3（未开卡原因） | 仅 q1=1（从未开通）的人作答 | 715 / 1221 |
| q4（刚到期未续原因） | 仅 q1=2（刚到期）的人作答 | 188 / 1221 |
| q22（觉得值的原因） | 仅 q21=1或2（觉得值）的人作答 | 282 / 1221 |
| q31（京东PLUS原因） | 仅 q30 选了京东PLUS的人作答 | 307 / 1221 |

**结论**：同一份数据中，不同题目的 Base 可能从几百到一千多不等，这是正常的。

#### 1.4 选项频数也必须在作答人群中计算

```python
# 单选题：只在作答了该题的人中统计各选项频数
effective_mask = seg_mask & answer_mask
count = (df.loc[effective_mask, col] == opt_val).sum()

# 多选题：同样只在作答人群中统计
count = (df.loc[effective_mask, col_name].fillna(0) != 0).sum()
```

### 2. 严格遵循参考文件的题目和选项

从参考 Excel 中提取完整的题目列表和选项顺序，**不要**自行推断或改变选项顺序。

```python
# 从参考文件提取题目选项
with open('table_options.json') as f:
    tables = json.load(f)  # [{table_num, question, options}, ...]
```

### 3. 多选题 vs 单选题的处理差异

| 类型 | 识别方式 | 统计方法 |
|------|---------|---------|
| 单选题 | 单个字段，值标签映射 | `df[col] == val` 计数 |
| 多选题 | 多个 `_N` 后缀字段（如 `L7_1`~`L7_10`） | 每个子字段 `== 1` 计数 |
| 矩阵题 | 多个独立子问题（如 `Y3_SQ1`~`Y3_SQ4`） | 每个子问题分别统计，选项拼接为"平台 - 选项" |

### 4. 排除 _输入文本 列

SPSS 导出多选题时，"其他"选项会额外生成 `_输入文本` 列（如 `L7_9_输入文本`），这些列**不参与统计**。

```python
multi_cols = [col for col in df.columns
              if col.startswith(prefix + '_')
              and '输入文本' not in col
              and re.match(r'^' + re.escape(prefix) + r'_\d+$', col)]
```

## 派生分群列（Banner）

从原始字段映射出 8 个分析用分群列，作为交叉表的列变量（Banner）：

| 派生列 | 来源字段 | 映射规则 |
|--------|---------|---------|
| 购买力 | H3 | 1,2→3k元以下；3→3k元以上 |
| 88vip | Y1_1 | 1→是；0→否 |
| 购买力×88vip | H3 + Y1_1 | H3≤2→3k元以下；H3≥3且Y1_1=1→3k元以上且88vip；否则→3k元以上且非88vip |
| 性别 | L1 | 1→男；2→女 |
| 年龄1 | L2 | 1~3→30岁以下；4~5→30-40岁；6+→40岁以上 |
| 年龄2 | H1 | 1~4→40岁以下；5+→40岁以上 |
| 年龄3 | L2 | 1~3→30岁以下；4+→30岁以上 |
| 城市等级 | H2 | 1→地级市以上；2→地级市以下 |

## 四种题型处理

| 题型 | 代号 | 识别方式 | 统计方法 |
|------|------|---------|---------|
| 单选题 | S | 单个字段，值标签映射 | `df[col] == val` 计数，val 从值标签获取 |
| 多选二进制 | M | 多个 `_N` 后缀字段（如 `L7_1`~`L7_10`） | 每个子字段 `== 1` 计数 |
| 单选指定值列表 | S_sub | 单个字段，但需按指定值列表统计（非全部值） | `df[col].isin(val_list)` 逐值计数 |
| 矩阵展平 | Y3 | 多个子问题 × 多个选项值，展平为行 | 每个子问题 × 每个值组合为一行，如 Y3_SQ1×值1、Y3_SQ1×值2… |

### 多选题列号不连续问题

多选题的子字段编号可能存在缺号（SPSS 导出时跳过不存在的选项），**严禁**用 `range(1, N+1)` 硬编码生成列名，必须从 metadata 实际列名中获取：

```python
# 错误：假设列号连续
cols = [f'D6_{i}' for i in range(1, 11)]  # D6_4 不存在会报错

# 正确：从 metadata 获取实际存在的列名
actual_cols = [c for c in meta.column_names
               if c.startswith('D6_') and re.match(r'^D6_\d+$', c)]
# 结果: ['D6_1','D6_2','D6_3','D6_5','D6_6','D6_7','D6_8','D6_9','D6_10']（缺4）
```

已知存在缺号的题目：D6（缺4）、D8（缺2）、J6（缺7）、P6（缺2/4/5/7）。

## 分群条件定义

分群条件以字典形式定义，key 为人群名称，value 为 pandas boolean mask：

```python
segments = {
    '月消费3000元以上': df['H3'] == 3,
    '月消费3000元以下': df['H3'].isin([1, 2]),
    '88VIP会员': df['Y1_1'] == 1,
    '月消费3000元以上非88VIP': (df['H3'] == 3) & (df['Y1_1'] == 0),
    '月消费3000元以上且88VIP': (df['H3'] == 3) & (df['Y1_1'] == 1),
}
```

分群可以有任意组合，包括：
- 单字段筛选：`df['L1'] == 1`（仅男性）
- 多字段组合：`(df['H3'] == 3) & (df['Y1_1'] == 1)`（高消费且会员）
- 范围筛选：`df['L2'].isin([2, 3, 4])`（18~35岁）

## 输出格式标准

### Sheet 1: N Tables（频数表）
- 标题行：深蓝色底（#000080）白字，12pt Arial Bold Italic
- 列标题行：浅灰色底（#D6DCE4），11pt 宋体 Bold
- 合计行：浅绿色底（#E2EFDA），11pt 宋体 Bold
- 数字格式：`0`（整数）
- 表间分隔：3 个空行

### Sheet 2: % Tables（百分比表）
- 结构与 N Tables 相同
- 额外包含 **Base 行**（显示各人群有效作答人数）
- 百分比格式：`0%`（整数百分比，如 23% 而非 23.0%）
- 合计行百分比：100%（值为 1.0）

### Sheet 3: Table of Contents（目录）
- 列：N Tables 编号 | % Tables 编号 | 题目描述 | Base 范围 | 样本量

## 工作流程

```
Task Progress:
- [ ] Step 1: 读取数据（SPSS/CSV），获取 metadata 和字段信息
- [ ] Step 2: 定义分群条件
- [ ] Step 3: 获取题目列表和选项（从参考文件或 metadata）
- [ ] Step 4: 建立题目到字段的映射
- [ ] Step 5: 遍历题目计算交叉统计（每题独立 answer_mask）
- [ ] Step 6: 生成 Excel（N Tables + % Tables + TOC）
- [ ] Step 7: ★ 强制自检（见下方清单，必须在交付前完成）
```

## ★ 出表前强制自检清单

**每次生成交叉表后、交付文件前，必须执行以下自检。** 这是防止计算错误的最后一道防线。

### 自检项 1：Base 合理性检查

```python
# 遍历所有题目，打印 Base 值，检查是否因跳题逻辑而有差异
for q_key, bases in all_bases.items():
    total_base = bases.get('总体', 0)
    print(f'{q_key}: Base(总体)={total_base}')
```

**检查要点**：
- ✅ 不同题目的 Base 应该有差异（反映跳题逻辑）
- ❌ 如果所有题目 Base 完全相同 → 说明没有考虑跳题逻辑，必须修正
- ✅ 条件性题目（如 q3 仅 q1=1 作答）的 Base 应明显小于总样本
- ✅ 所有受访者也作答的题目（如人口学题）Base 可以等于总样本

### 自检项 2：单选题选项合计 = Base

```python
# 对每个单选题，检查各选项频数之和是否等于 Base
for q in single_choice_questions:
    for seg_name in segments:
        option_sum = sum(data[q][opt][seg_name] for opt in q['options'])
        base = bases[q][seg_name]
        assert abs(option_sum - base) < 2, f'{q["key"]} {seg_name}: 选项合计{option_sum} ≠ Base{base}'
```

**检查要点**：
- ✅ 单选题各选项频数之和 = Base（允许 ±1 的浮点舍入误差）
- ❌ 如果不等 → 说明频数计算或 Base 计算有误

### 自检项 3：百分比范围检查

```python
# 检查所有百分比值在 [0%, 100%] 范围内
for q in all_questions:
    for seg_name in segments:
        for opt in q['options']:
            pct = data[q][opt][seg_name] / bases[q][seg_name]
            assert 0 <= pct <= 1.001, f'{q["key"]} {opt} {seg_name}: 百分比{pct:.1%}超出范围'
```

### 自检项 4：多选题合理性检查

```python
# 多选题各选项频数之和通常 > Base（因为可选多项）
# 但至少有一个选项 > 0
for q in multi_choice_questions:
    for seg_name in segments:
        total_selected = sum(data[q][opt][seg_name] for opt in q['options'])
        base = bases[q][seg_name]
        assert total_selected > 0 or base == 0, f'{q["key"]} {seg_name}: Base>0但无人选择任何选项'
```

### 自检项 5：分群列完整性检查

- ✅ 确认包含"总体"列（所有样本的汇总）
- ✅ 各分群列的 Base ≤ 总体 Base（分群是总体的子集）
- ✅ 分群列名称正确、无乱码（检查中文编码是否正确）

### 自检项 6：Sheet 完整性检查

- ✅ N Tables 和 % Tables 两个 sheet 都已生成
- ✅ % Tables 包含 Base 行
- ✅ N Tables 的 Base 行在数据行下方，% Tables 的 Base 行在数据行上方
- ✅ 题目数量正确（排除开放题后全部覆盖）

## 脚本使用

运行 `scripts/spss_cross_tab.py`，配置参数在脚本顶部：

```python
# 配置区
CONFIG = {
    'sav_path': 'path/to/data.sav',
    'options_json': 'path/to/table_options.json',  # 可选，从参考文件提取
    'open_question_nums': {34, 35, ...},            # 排除的题号
    'segments': {...},                               # 分群条件
    'output_path': 'path/to/output.xlsx',
}
```

## 注意事项

1. **值标签匹配**：单选题按值标签的排序顺序匹配选项，而非文字精确匹配
2. **特殊列名**：含连字符的列名（如 `T9-1`）在 SPSS 中可能转为下划线（`T9_1`）
3. **空选项处理**：某选项无人选择时仍保留该行，值为 0
4. **合计行逻辑**：单选题各选项之和 = Base；多选题各选项之和 > Base，合计行始终 = Base

## CSV 数据源补充说明

当数据源为 CSV（而非 SPSS .sav）时，额外注意以下事项：

### 编码检测

CSV 文件可能是 GBK 或 UTF-8 编码。**不要假设编码**，必须先检测：

```python
# 正确做法：尝试多种编码，选择能正确读取的
for enc in ['utf-8', 'utf-8-sig', 'gbk', 'gb18030']:
    try:
        df = pd.read_csv(path, encoding=enc, nrows=5)
        # 检查中文字段是否可读（不是乱码）
        sample = df['gender'].iloc[0]
        if sample and not any(ord(c) > 0xFFFF for c in str(sample)):
            break  # 找到正确编码
    except:
        continue
```

### NaN 处理

- 权重列（weight）的 NaN 应填充为 0：`df['weight'] = df['weight'].fillna(0)`
- 未作答题目的 NaN 在计算时需通过 `answer_mask` 排除，而非简单 `fillna(0)`

### 分群标签获取

从 CSV 读取时，分群标签的中文值需从数据中实际获取，不要硬编码（避免编码差异导致匹配失败）：

```python
# 正确：从数据中获取实际值
gender_vals = df['gender'].dropna().unique()

# ❌ 错误：硬编码中文（可能因编码问题匹配不上）
gender_vals = ['女', '男']  # 如果文件编码不同就会匹配失败
```
