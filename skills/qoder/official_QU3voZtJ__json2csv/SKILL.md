---
name: json2csv
description: 将 JSON 文件转换为 CSV 格式，智能展平嵌套对象和数组，使数据可在电子表格和分析平台中使用。
---

# JSON to CSV Converter

Converts JSON files to CSV format with intelligent flattening of nested objects and arrays, making data usable in spreadsheets and analytics platforms.

## Usage

```bash
# Convert a JSON file to CSV
python json2csv.py data.json output.csv

# Example input (data.json):
# [
#   {"name": "Alice", "info": {"age": 30, "tags": ["engineer", "admin"]}},
#   {"name": "Bob", "info": {"age": 25, "tags": ["analyst", "user"]}}
# ]

# Output (output.csv):
# info.age,info.tags.0,info.tags.1,name
# 30,engineer,admin,Alice
# 25,analyst,user,Bob
```

## Price

$2.00
