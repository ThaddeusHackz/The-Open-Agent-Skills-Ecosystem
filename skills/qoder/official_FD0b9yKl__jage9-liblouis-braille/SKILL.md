---
name: liblouis-braille
description: Guides users through translating and back-translating text and files using Liblouis on Linux. Use whenever a user asks to convert text to braille, braille to text, mentions grade 1/grade 2/UEB, requests lou_translate commands, or needs batch conversion of files to Unicode braille. Prefer the bundled wrapper scripts for deterministic, repeatable CLI behavior.
license: MIT
compatibility: Requires Linux and Liblouis installed with lou_translate available on PATH.
metadata:
  version: 1.0.0
---

# Liblouis Braille Translation (CLI)

Guide the user through translating and back-translating text and files using Liblouis via the bundled scripts in `./scripts`.

This skill focuses strictly on translation and back-translation. It does not perform document layout, pagination, or embossing workflows.

Bundled scripts assumed:
- `scripts/louis_phrase.sh`
- `scripts/louis_file.sh`
- `scripts/louis_batch.sh`
- `scripts/louis_list_tables.sh`

---

## Workflow

### Step 0: Preflight

Before translating, run:
```
command -v lou_translate && lou_translate --version
```

If missing, stop and ask the user whether to install Liblouis first.

---

### Step 1: Determine Direction

Ask or infer:

- Forward (text → braille)
- Backward (braille → text)

If the user does not specify, default to:

- Forward translation

---

### Step 2: Select Table

If the user specifies:
- Grade 1 → prefer tables containing `g1`
- Grade 2 → prefer tables containing `g2`
- UEB → prefer UEB-labeled tables
- Region (US/UK/etc.) → match region

If the exact table name is unknown:

Run:
```

./scripts/louis_list_tables.sh

```

Or filter:
```

./scripts/louis_list_tables.sh --contains en --contains g2

```

If multiple candidates exist:
- Present them clearly
- Ask the user to choose
- Do not guess silently

If nothing is specified and a common US English table exists:
- Default to `en-us-g2.ctb`
- Clearly state that assumption

If the user requests BRF (ASCII braille) output:
- Use display table `en-us-brf.dis`
- Combine as `en-us-brf.dis,en-us-g2.ctb`

For Unicode braille output:
- Use display table `unicode.dis`
- Combine as `unicode.dis,en-us-g2.ctb`

---

### Step 3: Use the Appropriate Script

#### Phrase Translation

Text → Braille:
```

./scripts/louis_phrase.sh --table en-us-g2.ctb --forward "Hello world"

```

Braille → Text:
```

./scripts/louis_phrase.sh --table en-us-g2.ctb --backward "⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙"

```

If no text argument is provided, the script reads from stdin.

Direct `lou_translate` equivalents:
```
lou_translate --forward unicode.dis,en-us-g2.ctb <<< "Hello world"
lou_translate --forward en-us-brf.dis,en-us-g2.ctb <<< "Hello world"
```

---

#### Single File Translation

Text → Braille:
```

./scripts/louis_file.sh --table en-us-g2.ctb --forward --in input.txt --out output.brl.txt

```

Braille → Text:
```

./scripts/louis_file.sh --table en-us-g2.ctb --backward --in input.brl.txt --out output.txt

```

BRF output example:
```
./scripts/louis_file.sh --table en-us-g2.ctb --display en-us-brf.dis --forward --in input.txt --out output.brf
```

Always:
- Use new output filenames
- Do not overwrite unless explicitly requested

---

#### Batch Folder Translation

Text → Braille:
```

./scripts/louis_batch.sh 
--table en-us-g2.ctb 
--forward 
--in-dir ./chapters 
--out-dir ./braille_out 
--glob "*.txt" 
--suffix ".brl.txt"

```

Braille → Text:
```

./scripts/louis_batch.sh 
--table en-us-g2.ctb 
--backward 
--in-dir ./braille_out 
--out-dir ./text_out 
--glob "*.brl.txt" 
--suffix ".txt"

```

The batch script:
- Uses null-delimited loops to safely handle spaces
- Writes outputs to the output directory (flat structure)
- Never deletes source files

---

### Step 4: Verify Result

For phrase translation:
- Suggest back-translation to confirm round-trip accuracy.

Example:
```

./scripts/louis_phrase.sh --table en-us-g2.ctb --backward "⠞⠑⠭⠞"

```

For file translation:
- Back-translate a sample line.
- Or inspect the first few lines of output.

---

## Safety Rules

- Do not install packages unless the user explicitly asks.
- Do not delete or overwrite user files.
- Always write outputs to new files or directories.
- Clearly state assumptions about table and direction.
- If table selection is ambiguous, ask the user before proceeding.

---

## Troubleshooting

If translation output is empty or unchanged:
- Confirm `lou_translate` is installed and on PATH.
- Confirm the selected table exists.
- Confirm a valid display table is available (common: `unicode.dis`, `en-us-brf.dis`).

If you see an error like `unrecognized option '--display-table'`:
- Use `DISPLAY,TABLE` syntax instead (e.g., `en-us-brf.dis,en-us-g2.ctb`).
- The bundled wrapper scripts already handle this.

If contractions appear incorrect:
- Switch between `g1` and `g2`.
- Confirm whether the user wants UEB.

If punctuation or formatting appears wrong:
- Try a different locale table.
- Confirm the target braille standard.

If output is a single long line in BRF:
- This is expected from `lou_translate`; wrapping/pagination is a separate step.

---

## Response Format

When using this skill, always:

1. State assumptions (direction, table used).
2. Provide the exact script command(s).
3. Show output file paths or resulting text.
4. Provide a short verification step if appropriate.
