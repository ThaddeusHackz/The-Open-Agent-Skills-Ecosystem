---
name: fileclean
description: 通过移除日期时间戳、哈希值、UUID 和多余符号来清理文件名杂乱，将类似 `report_20230101_a1b2c3d.pdf` 的混乱文件名转换为整洁易读的名称，如 `Report.pdf`。
---

# FileClean

Cleans filename clutter by removing date timestamps, hashes, UUIDs, and excessive symbols, transforming messy filenames like `report_20230101_a1b2c3d.pdf` into clean, readable ones like `Report.pdf`.

## Usage

Preview changes:
```bash
python fileclean.py ~/Downloads ~/Documents --skip-ext pdf jpg
```

Apply changes:
```bash
python fileclean.py myfile.txt --rename
```

## Price

$2.75
