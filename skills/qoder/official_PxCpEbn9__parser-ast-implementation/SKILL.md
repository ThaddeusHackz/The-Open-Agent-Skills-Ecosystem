---
name: parser-ast-implementation
description: Implement or refactor the Talqor lexer, parser, and AST from the approved grammar while preserving spans, diagnostics, and regression coverage.
argument-hint: [frontend-task]
allowed-tools: Read, Grep, Glob, Edit, Write, MultiEdit, Bash
context: fork
agent: parser-frontend-engineer
effort: high
---
# Parser and AST Implementation

Implement `$ARGUMENTS` from spec to code with zero silent grammar drift.

## Required workflow

1. Read the relevant grammar and any ADRs before editing code.
2. Identify the exact frontend layers touched:
   - lexer
   - parser
   - CST / parse tree
   - AST
   - diagnostics
   - test harness
3. Translate grammar rules into explicit code constructs.
4. Preserve or improve:
   - source spans
   - recovery behavior
   - error messages
   - AST clarity
5. Add or update:
   - positive parse tests
   - negative parse tests
   - AST golden or structural tests if used by the repo
6. If the grammar is unclear, stop and note the ambiguity instead of inventing a rule.

## Supporting files

- [frontend-checklist.md](frontend-checklist.md)
- [test-cases.md](test-cases.md)

## Final output

Summarize:
- spec rules used
- files changed
- invariants preserved
- tests added
- unresolved grammar ambiguity
