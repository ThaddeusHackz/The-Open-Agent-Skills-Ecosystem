---
name: quicksort-markdown
description: 按标题名称字母顺序对 Markdown 标题及其嵌套内容进行排序，帮助用户快速可靠地整理笔记。
---

# QuickSort Markdown

Sorts markdown headings and their nested content alphabetically by heading name, helping users organize notes quickly and reliably.

## Usage

Sort a markdown file in place:

```bash
python quicksort_markdown.py notes.md -o sorted_notes.md
```

Sort markdown from stdin:

```bash
cat notes.md | python quicksort_markdown.py | tee sorted.md
```

## Price

$2.50
