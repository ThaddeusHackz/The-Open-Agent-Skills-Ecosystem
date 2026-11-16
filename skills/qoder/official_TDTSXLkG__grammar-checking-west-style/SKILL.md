---
name: grammar-checking-west-style
description: Use when grammar-checking mathematical (Theoretical Computer Science) LaTeX articles to ensure they follow Douglas B. West's stylistic and grammatical rules.
---

# Grammar Checking According to West

## Overview
This skill provides a rigorous set of rules for mathematical writing in LaTeX, specifically tailored for Theoretical Computer Science (TCS), based on "The Grammar According to West" by Douglas B. West. It aims to make mathematical writing transparent, logically consistent, and accessible.

## When to Use
- Reviewing LaTeX manuscripts for TCS conferences or journals.
- Checking for "double-duty" definitions (e.g., "Let $G=(V,E)$ be a graph").
- Ensuring notation and terminology are precise (e.g., "maximum" vs. "maximal").
- Correcting common errors in English usage by non-native speakers in a mathematical context.

## Core Rules & References

This skill is organized into four detailed reference guides. When editing a file, always reference these numbered items in a temporary `fixes-applied.md` file.

1.  **[Mathematical Style](style.md)**: Rules 1–27 (Syntax, logic, structure).
2.  **[Terminology & Notation](terminology.md)**: Rules 28–57 (Graph theory, lists, operators).
3.  **[English Usage](english.md)**: Rules 58–81 (Grammar, punctuation, style).
4.  **[Non-Native Speakers](non-native.md)**: Rules 82–92 (Common errors, translations).

### Quick Check / Red Flags
- **Rule 4, 5**: Let $G=(V,E)$ or Let $A=B$ (Double-duty definition). This is the most common error.
- **Rule 8**: Sentence starting with notation.
- **Rule 13**: "Since... then" or "Since... so".
- **Rule 44**: "Connected components" (Redundant).
- **Rule 45**: "Maximal" (inclusion) vs "Maximum" (cardinality).
- **Rule 62**: Naked "This" (Subject without a noun).

## Workflow for Edits

1.  **Read** the LaTeX file.
2.  **Identify** violations using the numbered rules in the reference files.
3.  **Apply** fixes to the original file.
4.  **Create** a temporary file `fixes-applied.md` listing each fix and its rule number.

### Example `fixes-applied.md`
| Line | Original | Fixed | Rule # |
| :--- | :--- | :--- | :--- |
| 12 | Let $G=(V,E)$ be a graph. | Let $G$ be a graph. | 5 |
| 45 | $G$ is bipartite. | The graph $G$ is bipartite. | 8 |
| 67 | $G$ has 4 connected components. | $G$ has 4 components. | 44 |
| 89 | This implies that... | This inequality implies that... | 62 |
