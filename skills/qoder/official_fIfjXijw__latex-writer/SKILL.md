---
name: latex-writer
description: |
  Academic paper and professional resume/CV writing skill for macOS.
  Triggers when user wants to: write papers, create resumes/CVs, format LaTeX documents,
  manage citations/bibliography, convert Markdown to PDF, or needs academic formatting help.
  Supports Chinese (ctex), English, IEEE/ACM/custom styles, BibTeX/BibLaTeX.
argument-hint: "[paper|resume] [template] [--lang:en|zh]"
---

# LaTeX Writer Skill

Write academic papers and professional resumes with LaTeX quality output on macOS.

## Quick Start

```bash
# Check dependencies first
~/.claude/skills/latex-writer/scripts/check-deps.sh

# Compile a document
~/.claude/skills/latex-writer/scripts/compile.sh document.tex
```

## Capabilities

### 1. Paper Writing
- IEEE, ACM, and Chinese academic paper templates
- Automatic bibliography management (BibTeX)
- Math equations, figures, tables, algorithms
- Cross-references and citations

### 2. Resume/CV Creation
- Modern, academic, and Chinese resume templates
- ATS-friendly formatting
- Multi-version management by company/role

### 3. Format Conversion
- Markdown → LaTeX → PDF
- LaTeX → DOCX (via Pandoc)
- DOI → BibTeX entry

## Available Templates

### BasicTeX Compatible (Recommended)
These templates work with BasicTeX without additional packages:

| Template | File | Use Case |
|----------|------|----------|
| Chinese Paper | `templates/paper-chinese-basic.tex` | 中文学术论文 (BasicTeX) |
| Chinese Resume | `templates/resume-chinese-basic.tex` | 中文简历 (BasicTeX) |
| IEEE Paper | `templates/paper-ieee.tex` | Conference/journal papers |

### Full Templates (require additional packages)
These require: `sudo tlmgr install biblatex biber fontawesome5 titlesec`

| Template | File | Use Case |
|----------|------|----------|
| Chinese Paper (full) | `templates/paper-chinese.tex` | 中文论文 (biblatex) |
| Modern Resume | `templates/resume-modern.tex` | Professional CV (fontawesome5) |
| Academic CV | `templates/resume-academic.tex` | Academic positions (fontawesome5) |
| Chinese Resume (full) | `templates/resume-chinese.tex` | 中文简历 (fontawesome5) |

## Workflow

### Writing a Paper

1. **Create project structure**
   ```
   paper/
   ├── main.tex        # Main document
   ├── sections/       # Chapter files
   ├── figures/        # Images
   └── references.bib  # Bibliography
   ```

2. **Write content** in LaTeX or Markdown

3. **Compile**
   ```bash
   ~/.claude/skills/latex-writer/scripts/compile.sh main.tex xelatex
   ```

### Creating a Resume

1. **Choose template** based on target (modern/academic/chinese)

2. **Fill in YAML frontmatter** or LaTeX fields

3. **Generate PDF**
   ```bash
   pandoc resume.md -o resume.pdf --pdf-engine=xelatex \
     -V CJKmainfont="Hiragino Sans GB"
   ```

## Chinese Document Guidelines

For Chinese documents, always use XeLaTeX with ctex:

```latex
\documentclass[UTF8,a4paper]{ctexart}
```

Pandoc command for Chinese:
```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V CJKmainfont="Hiragino Sans GB" \
  -V geometry:margin=2.5cm
```

## Bibliography Management

### Add citation from DOI
```bash
~/.claude/skills/latex-writer/scripts/doi2bib.py 10.1145/1234567.1234568 >> refs.bib
```

### Citation styles
- IEEE: `\bibliographystyle{IEEEtran}`
- ACM: `\bibliographystyle{ACM-Reference-Format}`
- APA: Use biblatex with `style=apa`

## Supporting Files

- [reference.md](reference.md) - LaTeX syntax quick reference
- [templates/](templates/) - Document templates
- [scripts/](scripts/) - Build and utility scripts
- [examples/](examples/) - Sample documents

## Error Handling

If compilation fails:
1. Check `check-deps.sh` output for missing packages
2. Look for error in `.log` file
3. Common fixes:
   - Missing package: `sudo tlmgr install <package>`
   - Font not found: Install via Font Book or use fallback
   - Encoding issue: Ensure UTF-8 and use XeLaTeX

## Requirements

- macOS 14+
- BasicTeX (`brew install --cask basictex`) or full MacTeX
- Pandoc (`brew install pandoc`) - optional, for Markdown conversion

### BasicTeX PATH Setup
Add to `~/.zshrc` or `~/.bash_profile`:
```bash
export PATH="/Library/TeX/texbin:$PATH"
```

### Optional Packages (for full templates)
```bash
sudo tlmgr install biblatex biber fontawesome5 titlesec listings
```
