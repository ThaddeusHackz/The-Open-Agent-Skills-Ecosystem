---
name: hooks
description: "Hook infrastructure alignment: treat configured hooks as required workspace infrastructure, validate via real entrypoint."
---

# Hooks

* Use [references/example.md](references/example.md) as the shared example and formatting reference for this skill.
* Keep new guidance, snippets, and future edits aligned with that file.

---

## Purpose

* Keep workspace hooks aligned with the active configuration.
* Prevent silent bypasses of required hook behavior.
* Preserve reliable hook execution in the default shell environment.

## Applies To

* Hook scripts
* `hooks.json`
* `config.toml` hook integration
* Tasks that change files, flows, or docs coupled to hook behavior
* Validation of hook entrypoints

## Rules

* Treat configured hooks as required workspace infrastructure.
* Preserve hook-related settings unless the user explicitly requests an exception.
* Keep docs, agent instructions, and settings aligned with the active hook flow.
* Prefer validation through the real configured hook entrypoint.
* Prefer interpreter and path choices that are stable in the default shell.
* Do not introduce hidden bypasses, shadow configs, or silent fallbacks.
* If a hook cannot be validated end-to-end, state the exact missing dependency.

## Validation

* Run the real configured entrypoint with a minimal valid payload.
* Confirm interpreter and path resolution in the default shell.
* Confirm expected success or failure signaling.
* Confirm adjacent settings and docs still match the active flow.
