---
name: neo4j-modern-cypher-query-guide
description: Generate and refactor Neo4j 5.x Cypher for querying, graph construction, local Neo4j Desktop 2 import workflows, and graph analysis. Use when users mention Neo4j, Cypher, graph database, knowledge graph, deprecated syntax migration, or query performance.
license: MIT
metadata:
  author: alen
  version: "3.0.0"
---

# Neo4j Modern Cypher Query Guide

Production-grade guidance for Neo4j 5.x Cypher generation and migration.
This skill is optimized for AI-assisted workflows and enterprise consistency.

## When to Apply

Use this skill when tasks involve:

- Writing modern Cypher queries for Neo4j 5.x
- Migrating legacy Cypher to supported syntax
- Building nodes and relationships with deterministic `MERGE` patterns
- Generating Python scripts for Neo4j Desktop 2 data import
- Producing graph analysis queries and interpretation templates

## Rule Categories by Priority

| Priority | Category                    | Impact   | Prefix         |
| -------- | --------------------------- | -------- | -------------- |
| 1        | Compatibility and Safety    | CRITICAL | `compat-`      |
| 2        | Query Construction          | HIGH     | `query-`       |
| 3        | Read Patterns and Analytics | HIGH     | `read-`        |
| 4        | Data Import Workflows       | MEDIUM   | `import-`      |
| 5        | Troubleshooting             | MEDIUM   | `troubleshoot-`|

## Quick Reference

- `rules/compat-deprecated-syntax.md`
- `rules/query-modern-construction.md`
- `rules/read-subqueries-and-qpp.md`
- `rules/import-desktop2-python.md`
- `rules/troubleshoot-common-errors.md`

## Required Output Standard

For migration requests, return:

1. `Issue(s)` - why the old query is invalid or risky
2. `Modern Query (Neo4j 5.x)` - ready-to-run Cypher
3. `Rationale` - concise explanation of key changes

For generation requests, return:

1. `Cypher` (parameterized where possible)
2. `Validation Query` (to verify imported graph)
3. `Optional Performance Notes` (`PROFILE`, indexing, null-safe sort)

## Additional Resources

- Full compiled handbook: `AGENTS.md`
- Structure and contribution guide: `README.md`
