---
name: hk101-living-rag
description: 基于本地文本/标记语言的简单 RAG。
---

# claw-rag
Simple RAG over local text/markdown.

## Inputs
- query (string): question to answer.
- docsPath (string, optional): folder of docs (default ./docs relative to CWD).
- k (number, optional): number of top matches (default 3).

## Output
- answer: synthesized answer from matches.
- matches: [{path, score, snippet}...]

Requires: OPENAI_API_KEY in env.
