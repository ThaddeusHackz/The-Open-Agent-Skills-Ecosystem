---
name: xlsx
description: Use when the user wants to inspect, query, summarize, aggregate, or visualize local spreadsheet data from .xlsx, .xlsm, .csv, or .tsv files using natural language questions, trend analysis, anomaly checks, or local HTML chart output.
---

# XLSX Skill

Handle spreadsheet analysis directly. Stay read-only by default and do not modify the source file.

## Task Routing

| Task | Method | Guide (required) |
|------|--------|------------------|
| **READ** - preview structure and sample rows | `scripts/read.py` | `references/output-format.md` |
| **INFER** - infer column roles and candidate semantics | `scripts/infer_columns.py` | `references/intent-routing.md` |
| **QUERY** - answer natural-language questions with pandas | `scripts/query_analyze.py` | `references/intent-routing.md` + `references/data-cleaning-rules.md` |
| **VISUALIZE** - export local HTML charts | `scripts/visualize.py` | `references/chart-selection.md` |

**Guide is mandatory.** Before running any task script, read the corresponding Guide file(s) under `SKILL_DIR/`. The Guide defines output interpretation, parameter selection, cleaning rules, and task-specific constraints. Do not skip this step or improvise from memory.

## Working Rules

1. **Read the Guide first.** Match the task to Task Routing, then open every listed Guide file before calling the script.
2. Always inspect structure first with `read.py` before answering a non-trivial question.
3. Keep the workflow read-only unless the user explicitly asks for a derived artifact such as a chart HTML file or JSON result.
4. Prefer the provided scripts over ad-hoc one-off analysis code.
5. When the question is ambiguous, make the smallest reasonable assumption and state it in the answer.
6. Every answer must include a conclusion, not only raw numbers or a dumped table.

## Recommended Flow

1. Identify the task type from Task Routing.
2. Read the corresponding Guide file(s) for that task.
3. Run `read.py` to discover sheets, columns, row counts, and sample data.
4. Run `infer_columns.py` when the question depends on column meaning or type inference; read `references/intent-routing.md` before running.
5. Let the outer agent decide analysis type, columns, sorting, Top N, and chart requirements.
6. Use `query_analyze.py` with explicit parameters for the analysis; read `references/intent-routing.md` and `references/data-cleaning-rules.md` before running.
7. Use `visualize.py` when a chart file is needed; read `references/chart-selection.md` before running.
8. Return the conclusion, key metrics, assumptions, and artifact path if one was created.

## `query_analyze.py` Parameters

`--analysis-type` must be one of: `summary`, `grouped_rank`, `trend`, `share`, `anomaly`.

Do **not** use invented values like `grouped`. Category + metric comparison (e.g. "按产品展示金额") maps to `grouped_rank`.

| User intent | `--analysis-type` | Key flags |
|-------------|-------------------|-----------|
| Overall stats on one column | `summary` | `--metric` |
| Group-by category, rank, Top N, bar chart | `grouped_rank` | `--metric`, `--dimension`; optional `--sort-order`, `--top-n` |
| Share / proportion | `share` | `--metric`, `--dimension` |
| Time trend | `trend` | `--metric`, `--time-dimension`, `--time-granularity` |
| Outliers | `anomaly` | `--metric` |

## Row Filters (`--filter`)

Use `--filter` to restrict rows **before** any analysis. Repeat for multiple conditions; all conditions are combined with AND.

| Syntax | Meaning |
|--------|---------|
| `<列名>=<值>` | equals |
| `<列名>!=<值>` | not equals |
| `<列名>><值>` | greater than |
| `<列名>>=<值>` | greater than or equal |
| `<列名><<值>` | less than |
| `<列名><=<值>` | less than or equal |
| `<列名>~<值>` | contains |
| `<列名>=<值1>,<值2>` | in list |

If the value itself contains `=`, only the first operator is used as the split point.

## Utility Scripts

```bash
python3 SKILL_DIR/scripts/read.py <文件路径> --json
python3 SKILL_DIR/scripts/infer_columns.py <文件路径> --json
python3 SKILL_DIR/scripts/query_analyze.py <文件路径> --sheet <工作表名> --analysis-type grouped_rank --dimension <分组列> --metric <数值列> --filter '<维度列>=<值>' --json
python3 SKILL_DIR/scripts/query_analyze.py <文件路径> --sheet <工作表名> --analysis-type trend --metric <数值列> --time-dimension <时间列> --time-granularity month --filter '<时间列>>=<起始值>' --chart --chart-type line --json
python3 SKILL_DIR/scripts/visualize.py <文件路径> --sheet <工作表名> --chart bar --x <维度列> --y <数值列> --output <输出路径>.html
```

## Supported Analysis Patterns

- Sheet preview and schema discovery
- `grouped_rank`: grouped sums with sorting and Top N
- `summary`: single-column count, sum, mean
- Monthly or daily `trend` analysis when a date-like column is present
- `share` and `anomaly` on numeric columns
- Row filters via `--filter` (e.g. `<列名>=<值>`, `<列名>><值>`) applied before analysis
- Local bar, line, pie, histogram, scatter, and heatmap export

## Deliverable Contract

Text answers should include:

- the final conclusion
- the columns, sheet, and aggregation used
- assumptions or fallback choices
- the local chart path when a chart was exported
