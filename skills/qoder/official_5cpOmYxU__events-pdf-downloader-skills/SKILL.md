---
name: pdf-downloader
description: Download articles, papers, docs, or webpages as local PDF files. Use when the user asks to download a PDF, save an article/page/link as PDF, fetch a paper by title or URL, or preserve an online page offline. Prefer direct PDF download when a URL resolves to a PDF; otherwise generate an offline PDF from the webpage content and include the source URL.
---

# PDF Downloader

## Workflow

1. Identify the best source URL.
   - If the user gives a URL, use it directly.
   - If the user gives only a title, search the web and prefer official or primary sources.
   - If there is a direct `.pdf` link or `Content-Type: application/pdf`, download it directly.
2. Save final files under `output/pdf/` unless the user gives another destination.
3. Run the bundled script:

```bash
python3 ~/.codex/skills/pdf-downloader/scripts/download_pdf.py "$URL" --output-dir output/pdf
```

4. Validate the result:
   - Check file size and page count with `pypdf`.
   - Render a thumbnail with `qlmanage` on macOS when available, or open/inspect another quick preview if available.
   - Confirm the title/source URL appears in generated offline PDFs.
   - For generated webpage PDFs, scan the first page visually when possible. Latin-heavy pages should use normal Latin word wrapping, not CJK character wrapping; CJK-heavy pages should still render with CJK-capable fonts.
5. Reply with absolute clickable file paths and note whether the file was directly downloaded or generated from the webpage.

## Blocked Pages

Some sites block direct Python requests but are still readable through browser/search tooling. If the script fails with `403`, challenge pages, empty content, or missing article text:

1. Use browsing/search to retrieve the article text from the official page.
2. Save a temporary Markdown file with title, source URL, date/author if known, headings, paragraphs, bullets, code blocks, tables, and image captions.
3. Convert it with:

```bash
python3 ~/.codex/skills/pdf-downloader/scripts/download_pdf.py --markdown tmp/article.md --source-url "$URL" --output-dir output/pdf --filename article-name.pdf
```

This fallback is an offline webpage capture, not an official PDF. Say that clearly.

## Script Notes

- `scripts/download_pdf.py` writes a `.pdf`; for generated webpages it also writes a sibling `.md`.
- Use `--filename name.pdf` for stable names.
- Use `--title "Title"` when the source page lacks a clean title.
- The script chooses reader-friendly fonts automatically: English/WinAnsi pages prefer built-in Helvetica with normal LTR wrapping; mixed Unicode pages use local TTF fonts when needed; CJK-heavy pages prefer CJK-capable fonts and only then use CJK wrapping. If no local TTF is available, it falls back to built-in PDF fonts or `STSong-Light` for CJK.
- If a generated PDF looks cramped, regenerate it with the current script before trying manual fixes; older outputs may have used CJK wrapping for English pages.
- If the source page contains dynamic images or video, preserve captions/source links rather than trying to embed media unless the user asks for a visual archive.
