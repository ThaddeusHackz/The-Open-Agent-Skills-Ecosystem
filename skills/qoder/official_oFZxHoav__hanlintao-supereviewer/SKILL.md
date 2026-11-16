---
name: "SupeReviewer"
description: "Check Chinese-English mixed editing compliance in Word documents per CY/T 154-2017 and generate Excel reports. Invoke when user uploads a .docx file and asks to review Chinese text containing English words, phrases, or sentences against editorial standards."
dependencies: "python>=3.8, python-docx>=0.8.11, openpyxl>=3.0.0"
---

# SupeReviewer

SupeReviewer helps editors and writers inspect Chinese Word documents that contain embedded English content, ensuring compliance with the Chinese publishing standard **CY/T 154-2017** (*Editing Specifications for Chinese Publications with Interpolated English*). It scans `.docx` files, detects potential violations, and exports a structured Excel report.

## When to Apply

Use this skill whenever:
- A user uploads or references a Word document and asks to "check", "review", "inspect", or "proofread" Chinese-English mixed content.
- The user explicitly mentions "夹用英文" (interpolated English), "编辑规范" (editorial standards), or "CY/T 154".
- The desired output is an Excel file listing issues found in the document.

## Rules Overview

The inspector evaluates the following categories (derived from `resources/guideline.md`):

1. **Punctuation**
   - Chinese sentences containing English words/phrases should end with Chinese punctuation (e.g., `。`, `？`, `！`).
   - Complete English sentences inside Chinese text should be wrapped in Chinese quotation marks (`""`), but their *internal* punctuation must remain English-style.
   - English commas, semicolons, colons, parentheses, dashes, and ellipsis inside quoted English must be half-width.
   - Enumeration of English items inside Chinese should use Chinese顿号 (`、`).

2. **Spacing**
   - Spaces around interpolated English are optional but must be **consistent** throughout the document.
   - No space should appear between English text and adjacent Chinese punctuation.

3. **Capitalization**
   - Common English words/phrases embedded in Chinese sentences should be lowercase unless they are proper nouns or start a complete quoted sentence.

4. **Line Breaks**
   - English words should not be hyphenated arbitrarily at line ends; if break is unavoidable, use standard English hyphenation rules.

5. **Typography**
   - English book/periodical titles should be in *italics*, not Chinese book-title marks (`《》`).
   - English article titles should be in regular type inside Chinese quotation marks.

6. **Numbers & Units**
   - Arabic numerals should be half-width and consistent in font with the English text.

## Workflow

1. **Receive** the `.docx` file path from the user.
2. **Run** the inspection script (`scripts/review_docx.py`) via Python execution.
3. **Return** a summary of findings and the path to the generated `.xlsx` report.

## Script Usage

```bash
python scripts/review_docx.py <input.docx> [output.xlsx]
```

- `<input.docx>`: The Word document to inspect.
- `[output.xlsx]`: Optional output path. Defaults to `<input>_review.xlsx`.

## Output Format (Excel)

The generated workbook contains one sheet with columns:

| Column | Meaning |
|--------|---------|
| `Paragraph` | Paragraph number in the document |
| `Text Snippet` | Surrounding context of the issue |
| `Issue Type` | Category: Punctuation, Spacing, Capitalization, Typography, Number/Unit, or Other |
| `Severity` | Warning or Error |
| `Suggestion` | Recommended correction |
| `Rule Ref` | Reference to CY/T 154-2017 clause |

## Resources

- `resources/guideline.md` — Full text of CY/T 154-2017 for detailed reference.
