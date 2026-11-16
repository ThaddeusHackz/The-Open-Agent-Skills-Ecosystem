---
name: lakeboard-to-markdown
description: Convert .lakeboard files (JSON-based mind map format containing test cases) to Markdown and validate the result. Use when the user uploads or references a .lakeboard file, asks to convert lakeboard files to markdown, or mentions converting test case mind maps to text format.
---

# Lakeboard to Markdown

## What is Lakeboard?

`.lakeboard` is a JSON-based mind map format. Each file contains:
- `diagramData.body[]` — tree of nodes (root = `body[0]`)
- Each node: `html` (content), `children[]` (sub-nodes), `note.content` (annotations), `image` (screenshots)

## Quick Start

### Convert + validate a single file (recommended)

```bash
python ~/.qoder/skills/lakeboard-to-markdown/scripts/lakeboard_to_markdown.py "input.lakeboard" "output.md" --validate
```

If no output path is given, a `.md` file with the same name is created in the same directory.

### Batch convert + validate a directory

```bash
python ~/.qoder/skills/lakeboard-to-markdown/scripts/lakeboard_to_markdown.py --batch "/path/to/directory" --output-dir "/path/to/output" --validate
```

Converts all `.lakeboard` files in the directory and validates each one. If `--output-dir` is omitted, `.md` files are written alongside the originals.

### Validate an existing markdown file separately

```bash
python ~/.qoder/skills/lakeboard-to-markdown/scripts/validate_lakeboard_markdown.py "input.lakeboard" "output.md"
```

## Workflow

1. **Read the file**: Use the conversion script above, or read the `.lakeboard` file as JSON.
2. **Run conversion with validation**: Execute the script with `--validate` on the target file(s).
3. **Check validation result** (mandatory, see below):
   - `RESULT: PASS` → proceed to step 4.
   - `RESULT: FAIL` → read the listed issues, fix the markdown (re-convert or manually repair), and **re-run validation until PASS**. Never deliver an unvalidated or failed result.
4. **Report**: Tell the user the output file path(s), a brief summary of what was converted, and the validation result (e.g. "62 node texts, 3 notes, 1 image, 58 parent→child relationships all preserved").

## Validation

Validation is a mandatory step after every conversion. The validator compares the generated markdown against the source `.lakeboard` and checks:

1. **Text content** — every node text line from the lakeboard appears in the markdown.
2. **Notes** — every `note.content` annotation appears in the markdown.
3. **Images** — every `image.src` URL appears in the markdown.
4. **Mind map structure** — every parent→child relationship from the lakeboard tree is preserved in the markdown hierarchy (child content must appear inside the parent's subtree).

Output example:

```
Validating: output.md
  Source:   input.lakeboard

✓ Text content: all 62 node text line(s) present
✓ Notes: all 3 note(s) present
✓ Images: all 1 image(s) present
✓ Structure: all 58 parent->child relationship(s) preserved

RESULT: PASS — markdown content and mind map structure match the lakeboard
```

Exit codes: `0` = PASS, `1` = FAIL. In `--validate` mode the conversion script exits non-zero if any file fails, so failures are never silent.

### If validation fails

1. Read the issue list: missing text lines point to lost content; broken edges point to hierarchy errors (wrong indentation level).
2. Re-run the conversion (preferred), or manually fix the markdown while strictly preserving the original content.
3. Re-run validation and repeat until `RESULT: PASS`.

## Critical Rule: Content Fidelity

**Do not modify, summarize, or omit any content from the original file.** The conversion is format-only:

- All text → preserved verbatim (strip only HTML tags and decode entities like `&amp;` → `&`)
- `<a href="URL">TEXT</a>` → `[TEXT](URL)`
- `note.content` → rendered as blockquote (`>`) under the node
- `image.src` → rendered as `![fileName](src)`
- Tree hierarchy → nested bullet lists (`-`)
- Root node → `# Title` heading
- JSON/code snippets in node content → preserved as-is in code blocks

## Output Format

```
# [Root node title]

- [Level 1 node]
  - [Level 2 node]
    - [Level 3 node]
      > [Note content]
      ![image.png](image_url)
```

## Script Details

`scripts/lakeboard_to_markdown.py` handles:
- JSON parsing of `.lakeboard` files
- Recursive tree traversal from `diagramData.body[0]`
- HTML entity decoding (`&amp;`, `&lt;`, `&gt;`, `&nbsp;`, etc.)
- HTML tag to Markdown conversion (links, divs, spans)
- Zero-width character stripping (U+200B etc.)
- Note and image preservation
- Single file and batch mode, optional `--validate` post-check

`scripts/validate_lakeboard_markdown.py` handles:
- Extracting all node texts, notes, images, and parent→child edges from the lakeboard
- Parsing the markdown back into an indented tree (bullets, headings, code blocks, blockquotes)
- Content completeness checks and structure (edge) checks
- Detailed PASS/FAIL report with problem list

Requires Python 3.6+ (standard library only, no external dependencies).
