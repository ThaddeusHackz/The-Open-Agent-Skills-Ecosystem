---
name: generator-builder
description: Create or update SEA generator tooling when existing scaffolds do not match the requested output, when a new Nx generator should be bootstrapped with `just generator-new`, or when spec-driven code generation must change in `tools/codegen/` instead of in generated files.
---

# Generator Builder

Create generator changes at the source. Do not patch generated output.

Concrete examples this skill should cover:

- "Create a new SEA Nx generator for a pattern `just generator-list` does not cover."
- "Extend the codegen pipeline so manifests emit a new file shape."
- "Fix last-mile adapter or test scaffolding without editing generated files."

Use the smallest upstream surface that can produce the required result.

## Decision Workflow

1. Run `just generator-list`.
2. If `sea:bounded-context`, `sea:adapter`, or `sea:api-surface` already fits, use that generator instead of creating a new one.
3. If the request changes files under `**/src/gen/**`, `docs/specs/**/*.ast*.json`, `docs/specs/**/*.ir.json`, or `docs/specs/**/*.manifest.json`, stop editing output and route the change upstream.
   Identify the responsible generator system first.
   For manifest shape issues, inspect the related `.manifest.json` producer.
   For IR-level issues, inspect the `.ir.json` producer.
   For behavior issues, inspect the generator pipeline or template source.
   If the source is still unclear, check git history or the owning generator team before editing.
4. Choose the generator system:
   Nx generator for developer-invoked scaffolding in `generators/`
   Python pipeline generator for manifest-driven output in `tools/codegen/`
   Last-mile generator for adapter or test gap filling in `tools/codegen/gen_adapter_template.py` or `tools/codegen/gen_test_template.py`
5. Load only the relevant reference file below before editing:
   For Nx generator work, read [references/nx-generators.md](references/nx-generators.md)
   For pipeline or last-mile work, read [references/python-codegen.md](references/python-codegen.md)
6. Validate the change, then package the skill if you updated this skill itself.

## Generator Inventory

- `generators/generator/`: meta-generator exposed as `sea:generator`
- `generators/bounded-context/`: bounded context scaffold
- `generators/adapter/`: real plus fake adapter pair
- `generators/api-surface/`: API surface scaffold
- `generators/generators.json`: collection registry
- `generators/_utils/shared.ts`: shared naming, tagging, and validation helpers

Primary commands:

- `just generator-list`
- `just generator-new <name> [TYPE]`
- `just generator-bc <name> [scope] [lang]`
- `just generator-adapter <name> <context> [backend]`
- `just generator-api <name> <context> [method]`

### Python generator surfaces

- `tools/codegen/gen.py`: main manifest-to-code pipeline
- `tools/codegen/templates/*.jinja2`: shared emitted file shapes
- `tools/codegen/gen_adapter_template.py`: adapter last-mile generation
- `tools/codegen/gen_test_template.py`: test last-mile generation
- `tools/codegen/gap_report.py`: missing adapter and test detection

## Stop Conditions

Stop and ask instead of guessing when any of these are true:

- The request requires editing generated output directly.
- The new generator duplicates an existing active generator with only naming differences.
- The request mixes two control planes when one upstream generator change would solve it.
- The correct source of truth is unclear between spec, Nx generator, and Python pipeline.

Use this reply format:

```text
I see a problem with the current request: [brief issue].

Options:
1. [recommended path]
2. [alternative]

Which path do you want?
```

## Reusable Contents

This skill uses references, not scripts or assets.

- [references/nx-generators.md](references/nx-generators.md) for Nx generator authoring, registration, and dry-run validation
- [references/python-codegen.md](references/python-codegen.md) for manifest-driven codegen and last-mile workflows

## Validation For This Skill

When updating this skill itself, run:

```bash
python3 .sea/skills/skill-creator/scripts/quick_validate.py .sea/skills/generator-builder
python3 .sea/skills/skill-creator/scripts/package_skill.py .sea/skills/generator-builder /tmp/sea-skill-dist
```

## Related Skills

- `sea-generator-first` for generated-code boundaries and regeneration workflow
- `generator-validate` after changing generator behavior
- `nx-generate` when the task is to run scaffolding, not author a new generator
