---
name: spreadsheet-tie-out
description: Use when writing, validating, or comparing an xlsx for a payment-audit report. Verifies E7 == SUM(AZ2:AZ{N}), R47 rollup == partner totals, byte-identity vs a prior build, and zero-formula-errors via LibreOffice recalc. Forks Anthropic's xlsx skill; adds payment-specific tie-out math. Zero tolerance for formula errors and template byte-changes.
when-to-use: |
  Trigger when the user:
    - writes to an xlsx file (partner commission template, ProForma, rollup)
    - validates an xlsx output before upload or hand-off
    - compares two xlsx files for byte-identity across a region
    - sees or suspects a formula error (#REF!, #DIV/0!, #VALUE!, #NAME?, #NUM!, #N/A, #NULL!)
    - normalizes templates and needs E7 == SUM(AZ2:AZ{N}) confirmed
  Do NOT trigger when:
    - ingesting an xlsx as read-only (use processor-report-parser)
    - doing Google Sheets API work (different tool — use scripts/gdrive_update_sheet.py)
---

# spreadsheet-tie-out

Fork of Anthropic's xlsx skill, specialized for Pay Theory commission/ProForma xlsx outputs.
Adds payment-specific tie-out math on top of the upstream formula-error scanner.

Companion files:
- `scripts/recalc.py` — LibreOffice headless recalc + formula-error scanner (forked from Anthropic).
- `scripts/tie_out.py` — THE new deliverable. Schema-mode tie-outs + byte-identity diff across two xlsx regions.
- `scripts/preserve_template.py` — copy formatting / merged-cells / column-widths from a blank template onto a filled workbook, without touching cell values.
- `references/financial_color_coding.md` — blue / black / green / red / yellow convention.
- `references/xlsx_anti_patterns.md` — 12-item checklist (data_only+save, AZ/BA gotchas, col-letter math, etc.).

## 5-Phase Body

### 1. Scope
Identify the target xlsx, target sheet, and the target region (either a schema name from
`data/excel_schemas.json` or an explicit A1 range like `A1:Z100`). For commission
work, the schema is usually `internal_commissions_partner_sheet_2026`,
`carefeed_commission_template_2026`, `caregrove_partner_report_march_2026`, or
`proforma_canonical_2026`.

### 2. Execute
Write or fill via `openpyxl`. ALWAYS open the workbook with `data_only=False` (default)
so formulas survive round-trips. After writes, reapply formatting from the
blank template via `scripts/preserve_template.py`.

### 3. Validate
In this order:
1. `python3 scripts/recalc.py <xlsx>` — LibreOffice recalculates every formula
   and reports `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#NULL!`, `#NUM!`, `#N/A`.
   If any error is returned, STOP. Do not upload. Fix the root cause.
2. `python3 scripts/tie_out.py --file <xlsx> --schema <schema_name>` — confirms the
   schema-specific tie-outs (E7 == SUM(AZ2:AZ{N}) for internal commissions,
   Q22+Q24 == payout for Caregrove partner report, etc.).
3. Optional byte-identity check: `python3 scripts/tie_out.py --file-a <old>.xlsx
   --file-b <new>.xlsx --region <A1:Z100> [--sheet S]`.

### 4. Report
Emit a tie-out memo with: variances vs tolerance threshold ($0.01 default),
exception list (cells whose computed value disagrees with the schema assertion),
and, for rollup rebuilds, a roll-forward table showing per-partner deltas.

### 5. Follow-up
If ANY formula error is found, or if the schema tie-out fails outside tolerance:
STOP. Do not upload. Fix the root cause in the builder, not in the xlsx. Re-run
Phases 2-3 until clean.

## Requirements for Outputs (inherited from Anthropic xlsx skill)

1. **Zero formula errors.** No `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#NULL!`,
   `#NUM!`, `#N/A` in any cell after recalc.
2. **Preserve existing templates byte-for-byte in unchanged regions.** Use
   `preserve_template.py` after every write.
3. **Financial color conventions** (see `references/financial_color_coding.md`):
   blue = hardcoded input, black = formula, green = cross-sheet link,
   red = external file link, yellow = assumption/review.
4. **Never hardcode a computed value where a formula would work.** If the value
   is a sum/product/vlookup, write the formula, not the pre-computed number.
5. **Pay Theory internal commission rollup rule**:
   `E7 == SUM(AZ2:AZ{N})` where `N = B6 + 1` (merchant count + header row).
   Tolerance: `$0.01`.
6. **ProForma rule**: every partner sheet uses the canonical F-AG layout
   (Jan 2025 = F, Feb 2026 = U, Dec 2026 projected = AF, 2026 Annual = AG).
   Rollup rows must reference cells in the SAME column letter as the rollup
   cell itself (e.g. cell `U60 = SUM(<partners>!U57)`, not mixed columns).

## Anti-pattern WRONG / CORRECT blocks

### WRONG — `data_only=True` + `save()`
```python
wb = openpyxl.load_workbook(path, data_only=True)
# ... edits ...
wb.save(path)   # DESTROYS every formula — they become static values
```
**Why it's fatal:** `data_only=True` loads the cached result of each formula.
Saving writes that cached number back, overwriting `=SUM(...)` with `12345.67`.
The workbook loses its formulas permanently. Next time the template refreshes,
numbers don't update.

### CORRECT
```python
wb = openpyxl.load_workbook(path)   # default: formulas preserved
# ... edits ...
wb.save(path)
```

### WRONG — hardcoding a computed sum
```python
ws[f"AZ{N+1}"] = 12345.67   # pre-computed in Python
```

### CORRECT — write the formula
```python
ws[f"AZ{N+1}"] = f"=SUM(AZ2:AZ{N})"
```

### WRONG — col 52 = "BL"
```python
# Off-by-one. Column 52 is "AZ", not "BL".
# See src/excel_schemas.py :: col_letter for the canonical mapping.
```

### CORRECT
```python
from src.excel_schemas import col_letter
assert col_letter(52) == "AZ"
assert col_letter(53) == "BA"
```

### WRONG — reading AZ2 as the partner total
```python
partner_total = ws["AZ2"].value   # WRONG: AZ2 is the FIRST merchant, not the rollup
```

### CORRECT
```python
merchant_count = ws["B6"].value
last_row = merchant_count + 1
partner_total = ws["E7"].value           # canonical rollup cell
# equivalent:
# partner_total = sum(ws.cell(row=r, column=52).value or 0 for r in range(2, last_row + 1))
```

## Quality Bar
- Every output workbook passes `recalc.py` with zero errors.
- Every commission/ProForma workbook passes `tie_out.py --schema <name>` with
  all assertions within `$0.01`.
- Every template rewrite passes `tie_out.py --file-a <backup> --file-b <new>
  --region <unchanged_region>` byte-clean.
