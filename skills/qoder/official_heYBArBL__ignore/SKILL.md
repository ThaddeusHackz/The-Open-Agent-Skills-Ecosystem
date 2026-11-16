---
name: ignore
description: "Hard read/edit boundary for generated, cached, temporary, and non-source-of-truth paths."
---

# Ignore

* Use [references/example.md](references/example.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

## Purpose

* Reduce noise from generated, cached, temporary, and non-source-of-truth paths.
* Keep exploration, reading, editing, and review focused on stable source files.

## Rule

Unless the user explicitly overrides it, treat the following patterns as a **hard read/edit boundary**.

This means the agent must not:

* explore these paths
* read files from these paths
* edit files in these paths
* use files in these paths as review or source-of-truth inputs

## Ignore Patterns
```markdown
**/.history/**
**/.backup/**
**/.cache/**
**/.tmp/**
**/.sandbox-bin/**
**/temp/**
**/tmp/**
**/cache/**
**/backups/**
**/bin/**
**/obj/**
**/dist/**
**/build/**
**/coverage/**
**/out/**
**/target/**
**/.next/**
**/.nuxt/**
**/.parcel-cache/**
**/.turbo/**
**/release/**
**/node_modules/**
**/vendor/**
**/generated/**
**/log/**
**/logs/**
**/debug/**
**/sandbox.log
**/*.sqlite-shm
**/*.sqlite-wal
**/*.tmp/**
**/*.temp/**
```
