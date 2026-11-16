---
name: xlsx
description: "Use when a spreadsheet file is the primary input or output, including opening, reading, editing, fixing, creating, converting, cleaning, or restructuring .xlsx, .xlsm, .csv, or .tsv data into a spreadsheet deliverable; do not use when the primary deliverable is Word, HTML, standalone Python, a database pipeline, or Google Sheets API integration."
---

* Use [references/EXAMPLE.md](references/EXAMPLE.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

# 1. All Excel files

# 1-1. Professional Font

* Use a consistent, professional font (e.g., Arial, Times New Roman) for all deliverables unless otherwise instructed by the user

# 1-2. Zero Formula Errors

* Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

# 1-3. Preserve Existing Templates (when updating templates)

* Study and EXACTLY match existing format, style, and conventions when modifying files
* Never impose standardized formatting on files with established patterns
* Existing template conventions ALWAYS override these guidelines

---

# 2. Financial models

# 2-1. Color Coding Standards

* Unless otherwise stated by the user or existing template

## 2-1-1. Industry-Standard Color Conventions

* **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
* **Black text (RGB: 0,0,0)**: ALL formulas and calculations
* **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
* **Red text (RGB: 255,0,0)**: External links to other files
* **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

# 2-2. Number Formatting Standards

## 2-2-1. Required Format Rules

* **Years**: Format as text strings (e.g., "2024" not "2,024")
* **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
* **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
* **Percentages**: Default to 0.0% format (one decimal)
* **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
* **Negative numbers**: Use parentheses (123) not minus -123

# 2-3. Formula Construction Rules

## 2-3-1. Assumptions Placement

* Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
* Use cell references instead of hardcoded values in formulas
* Example: Use =B5*(1+$B$6) instead of =B5*1.05

## 2-3-2. Formula Error Prevention

* Verify all cell references are correct
* Check for off-by-one errors in ranges
* Ensure consistent formulas across all projection periods
* Test with edge cases (zero values, negative numbers)
* Verify no unintended circular references

## 2-3-3. Documentation Requirements for Hardcodes

* Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
* Examples:
  * "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  * "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  * "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  * "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

---

# 3. XLSX Creation, Editing, and Analysis

---

# 4. Overview

* A user may ask you to create, edit, or analyze the contents of an .xlsx file. You have different tools and workflows available for different tasks.

---

# 5. Important Requirements

* **Microsoft Excel Required for Formula Recalculation**: You can assume Microsoft Excel is available for recalculating formula values using the `scripts/recalc.py` script. The script automatically configures Excel on first run, including in sandboxed environments where Unix sockets are restricted (handled by `scripts/office/soffice.py`)

---

# 6. Reading and analyzing data

# 6-1. Data analysis with pandas

* For data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

---

# 7. Excel File Workflows

---

# 8. Critical: Use Formulas, Not Hardcoded Values

* **Always use Excel formulas instead of calculating values in Python and hardcoding them.** This ensures the spreadsheet remains dynamic and updateable.

# 8-1. Incorrect - Hardcoding Calculated Values

```python

# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

# 8-2. Correct - Using Excel Formulas

```python

# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

* This applies to ALL calculations - totals, percentages, ratios, differences, etc. The spreadsheet should be able to recalculate when source data changes.

---

# 9. Common Workflow

* **Choose tool**: pandas for data, openpyxl for formulas/formatting
* **Create/Load**: Create new workbook or load existing file
* **Modify**: Add/edit data, formulas, and formatting
* **Save**: Write to file
* **Recalculate formulas (MANDATORY IF USING FORMULAS)**: Use the scripts/recalc.py script

```bash
   python scripts/recalc.py output.xlsx
```

* **Verify and fix any errors**:
   * The script returns JSON with error details
   * If `status` is `errors_found`, check `error_summary` for specific error types and locations
   * Fix the identified errors and recalculate again
   * Common errors to fix:
     * `#REF!`: Invalid cell references
     * `#DIV/0!`: Division by zero
     * `#VALUE!`: Wrong data type in formula
     * `#NAME?`: Unrecognized formula name

# 9-1. Creating new Excel files

```python

# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

# 9-2. Editing existing Excel files

```python

# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

---

# 10. Recalculating formulas

* Excel files created or modified by openpyxl contain formulas as strings but not calculated values. Use the provided `scripts/recalc.py` script to recalculate formulas:

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

* Example:

```bash
python scripts/recalc.py output.xlsx 30
```

* The script:

* Automatically sets up Microsoft Excel macro on first run
* Recalculates all formulas in all sheets
* Scans ALL cells for Excel errors (#REF!, #DIV/0!, etc.)
* Returns JSON with detailed error locations and counts
* Works on both Linux and macOS

---

# 11. Formula Verification Checklist

* Quick checks to ensure formulas work correctly:

# 11-1. Essential Verification

* [ ] **Test 2-3 sample references**: Verify they pull correct values before building full model
* [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK)
* [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)

# 11-2. Common Pitfalls

* [ ] **NaN handling**: Check for null values with `pd.notna()`
* [ ] **Far-right columns**: FY data often in columns 50+
* [ ] **Multiple matches**: Search all occurrences, not just first
* [ ] **Division by zero**: Check denominators before using `/` in formulas (#DIV/0!)
* [ ] **Wrong references**: Verify all cell references point to intended cells (#REF!)
* [ ] **Cross-sheet references**: Use correct format (Sheet1!A1) for linking sheets

# 11-3. Formula Testing Strategy

* [ ] **Start small**: Test formulas on 2-3 cells before applying broadly
* [ ] **Verify dependencies**: Check all cells referenced in formulas exist
* [ ] **Test edge cases**: Include zero, negative, and very large values

# 11-4. Interpreting scripts/recalc.py Output

* The script returns JSON with error details:

```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

---

# 12. Best Practices

# 12-1. Library Selection

* **pandas**: Best for data analysis, bulk operations, and simple data export
* **openpyxl**: Best for complex formatting, formulas, and Excel-specific features

# 12-2. Working with openpyxl

* Cell indices are 1-based (row=1, column=1 refers to cell A1)
* Use `data_only=True` to read calculated values: `load_workbook('file.xlsx', data_only=True)`
* **Warning**: If opened with `data_only=True` and saved, formulas are replaced with values and permanently lost
* For large files: Use `read_only=True` for reading or `write_only=True` for writing
* Formulas are preserved but not evaluated - use scripts/recalc.py to update values

# 12-3. Working with pandas

* Specify data types to avoid inference issues: `pd.read_excel('file.xlsx', dtype={'id': str})`
* For large files, read specific columns: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
* Handle dates properly: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`

---

# 13. Code Style Guidelines

* **IMPORTANT**: When generating Python code for Excel operations:

* Write minimal, concise Python code without unnecessary comments
* Avoid verbose variable names and redundant operations
* Avoid unnecessary print statements

# 13-1. For Excel files themselves

* Add comments to cells with complex formulas or important assumptions
* Document data sources for hardcoded values
* Include notes for key calculations and model sections
