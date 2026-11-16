---
name: proofread
description: Proofreading workflow for academic manuscripts and papers.
---

# Proofread Academic Writing

Run the mandatory proofreading protocol on papers or manuscripts. Produces a report of all issues WITHOUT editing any source files.

## Steps

1. **Identify files to review:**
   - If `$ARGUMENTS` is a specific filename: review that file only
   - If `$ARGUMENTS` is `all`: review all files in `manuscripts/` and `Quarto/` (if it exists)
   - If `$ARGUMENTS` is a file in `manuscripts/`: treat as manuscript (not slides)
   - If `$ARGUMENTS` is empty or ambiguous and multiple files exist, ask the user to choose conversationally. Do not use `request_user_input` here because the selection may be multi-file and Codex question UI is single-choice only.

2. **For each file, read `agents/proofreader.md`, then spawn a `default` subagent** that applies that proofreading protocol and checks for:

   **GRAMMAR:** Subject-verb agreement, articles (a/an/the), prepositions, tense consistency
   **TYPOS:** Misspellings, search-and-replace artifacts, duplicated words
   **LAYOUT ISSUES:** Overfull hbox (LaTeX slides/manuscripts), content exceeding slide boundaries (Quarto), table/column overflow in manuscripts
   **CONSISTENCY:** Citation format, notation, terminology, variable names matching table column names
   **ACADEMIC QUALITY:** Informal language, missing words, awkward constructions

3. **Produce a detailed report** for each file listing every finding with:
   - Location (line number or section heading)
   - Current text (what's wrong)
   - Proposed fix (what it should be)
   - Category and severity

4. **Save each report** to `quality_reports/`:
   - For `.tex` slide files: `quality_reports/FILENAME_report.md`
   - For `.qmd` slide files: `quality_reports/FILENAME_qmd_report.md`
   - For manuscript files: `quality_reports/FILENAME_proofread.md`

5. **IMPORTANT: Do NOT edit any source files.**
   Only produce the report. Fixes are applied separately after user review (see `rules/proofreading-protocol.md`).

6. **Present summary** to the user:
   - Total issues found per file
   - Breakdown by category
   - Most critical issues highlighted
