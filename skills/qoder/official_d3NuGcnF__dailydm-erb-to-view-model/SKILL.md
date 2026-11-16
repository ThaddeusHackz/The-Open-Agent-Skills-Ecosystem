---
name: erb-to-view-model
description: "ERB → ViewModel: Extract Ruby logic out of an ERB template"
disable-model-invocation: true
---

# ERB → ViewModel: Extract Ruby logic out of an ERB template

When the user types `/erb-to-view-model`, migrate an ERB template away from instance variables / helper calls by **precomputing** all required values in a Ruby ViewModel under `app/view_models/`, following existing repo conventions.

## 1) Collect required inputs (ask before doing anything)

Before proceeding, ask the user for these parameters (do not proceed until all are provided):

- **ERB template path**: `<erb-path>` (example: `app/views/groups/index.html.erb`)
- **Controller + action**: `<controller>#<action>` (example: `GroupsController#index`)
- **Target ViewModel constant**: `<view-model-constant>` (example: `Groups::IndexViewModel`)
- **Target ViewModel file path**: `<view-model-path>` (example: `app/view_models/groups/index_view_model.rb`)

This command **always** uses the template local variable name `view_model` (it is not configurable).

Also ask for these parameters (strongly recommended; do not proceed without tests):

- **Characterization spec path**: `<spec-path>` (example: `spec/controllers/groups_controller_characterization_spec.rb`)
- **Feature flag constraint**: `<feature-flag>` (example: `groups_index_view_model_migration`)

This command assumes **layout variants are always web-only**.

## 2) Load the current project rules (required)

Read ALL rules in:

```
@.cursor/rules/
```

In addition, these constraints are **part of this command's prompt** and must be followed:

- **ERB → ViewModel migration constraints**
  - Replace **all** instance variables (`@something`) with `view_model.something`
  - Do not use `can?(:...)` in ERB; replace with precomputed `view_model.can_*` flags
  - Do not use `current_user.*` in ERB; replace with precomputed `view_model.current_user_*` or derived flags
  - Do not use `polymorphic_path` / polymorphic links directly in ERB; precompute paths/urls on the ViewModel

- **ViewModels must be "precompute-first"**
  - Use `T::Struct` with `const` values for anything the template reads
  - Prefer `self.init(...)` that computes everything once, then `new(...)`
  - Prefer **booleans** like `has_attachments` (not `has_attachments?`) for conditionals
  - If something can be missing, type it as `T.nilable(...)` and handle nil explicitly

- **No direct model references inside ViewModels**
  - Do **not** store AR models (e.g., `User`, `Group`, `ChatThread`) as `const` values in new/modified ViewModels
  - Store primitives (String/Integer/T::Boolean), precomputed hashes/arrays, or nested ViewModels instead
  - If serialization is needed, precompute the serialized form during `init` (do not serialize at render time)

- **How views should consume ViewModels**
  - Treat ViewModel values as **precomputed data**, not "call-to-compute" methods
  - Preserve safe navigation (`&.`) in templates for nilable ViewModel properties
  - Pass required parameters **explicitly** through initializers; do not implicitly derive them in views
  - Prefer constants like `has_translation` (not `has_translation?`)

- **Controller integration must be thin**
  - Controllers should pass only basic dependencies and delegate business logic (auth, data fetching, derivations) to the ViewModel
  - Avoid service layers for ViewModel creation; move that logic into ViewModels instead

- **Refactor bottom-up**
  - Start at the deepest partial(s), convert them to ViewModels, then backpropagate required parameters up the render tree
  - Goal state: no direct model access in ERB; only ViewModel reads + simple presentation

- **Characterization test golden rule**
  - Characterization specs should be at the **controller** level
  - Must use `render_views`
  - Assertions should be against final HTML (`response.body`)
  - Avoid partial-level view specs and avoid `assigns(...)`-style assertions

- **Ruby method signatures**
  - Do not use default parameters (no `param = nil`, no `param: nil`)
  - Make nilability explicit via `T.nilable(...)` and require callers to pass values explicitly

- **Avoid OpenStruct**
  - Do not use `OpenStruct` in production code or specs for this work; use typed structs, hashes, or verified doubles as appropriate

## 3) Identify existing ViewModel patterns to follow (required)

Use existing converted ViewModels as the primary examples (read before writing new code):

- `@app/view_models/groups/index_view_model.rb` (nested VMs, helpers, permissions)
- `@app/view_models/chats/message_show_view_model.rb` (large precompute init, URLs, flags)
- If your template's domain differs, scan `@app/view_models/` for the closest match.

If the ViewModel needs Rails helpers (paths, formatting), prefer the typed adapter pattern used in Groups:

- `@app/view_models/groups/helper_interface.rb`
- `@app/view_models/groups/helper_adapter.rb`

## 4) Baseline safety: characterization test first (required)

Follow `@.cursor/rules/rspec/controller-characterization-test-golden-rule.mdc`:

- **Heavily prefer** a controller-level characterization spec to exist for `<controller>#<action>` before changing any ERB/ViewModel code.
- If you cannot find an existing characterization spec for this controller/action:
  - Create one first using `@prompts/erb_characterization_tests.md`
  - Put it at `<spec-path>` (or the repo's established characterization spec location for that controller)
  - Run it and confirm it passes
  - Do **not** proceed with the ERB/ViewModel migration until this safety net exists and is green

- Add or extend a **controller-level** characterization spec at `<spec-path>` (preferred: reuse an existing one)
- Ensure it uses `render_views`
- Assert against `response.body` HTML (not instance variables, not partial-level specs)
- Cover the key states that are likely to regress during migration:
  - Empty state vs populated state
  - Permission-gated UI sections
  - Web-only rendering behavior (this command assumes no app layout variants)

Run the spec and confirm it passes before changing the ERB or ViewModel code.

## 5) Perform a bottom-up migration (required)

Follow `@.cursor/rules/view_models/hierarchy-refactoring.mdc`:

1. **Trace the render tree**
   - From `<erb-path>`, list every rendered partial and the locals it expects.
   - Start migrating the deepest partial(s) first, then work upwards.

2. **Build or extend ViewModels**
   - Create/modify `<view-model-path>` so it is a `T::Struct` with **precomputed `const` values**
   - Add `self.init(...)` with **explicit parameters** (no default args)
   - If a value can be nil, type it `T.nilable(...)` and pass nil explicitly from the caller
   - Do not use `OpenStruct`

3. **Do not add direct model references to new ViewModels**
   - Prefer primitives (String/Integer/T::Boolean), precomputed hashes, and child view models.
   - If an existing ViewModel already exposes models for backward compatibility, do not expand that pattern. Keep model exposure minimal and isolated.

4. **Update controller creation**
   - Make the controller thin: it should gather only the basic dependencies and call `<view-model-constant>.init(...)`.
   - Prefer rendering with a local named `view_model`:

```ruby
render :index, locals: { view_model: @view_model }
```

If the controller has multiple render branches (app vs web), keep them consistent in how they pass the ViewModel.

## 6) Refactor the ERB and partials to consume the ViewModel (required)

In `<erb-path>` and its partials:

- **Replace instance variables**: `@something` → `view_model.something`
- **Replace helper calls with precomputed values**:
  - Paths/URLs: `polymorphic_path(...)` → `view_model.some_path`
  - Formatting: `simple_format`, `auto_link`, pluralization text, etc. → `view_model.some_html` / `view_model.some_text`
- **Replace authorization and current-user access**:
  - `can?(...)` → `view_model.can_*`
  - `current_user.*` → `view_model.current_user_*` or other precomputed flags
- **Replace complex conditions** with booleans:
  - `if thing.present?` → `if view_model.has_thing`
- **Collections**:
  - `render partial: ..., collection: models` → `collection: view_model.child_view_models, as: :view_model`
- **Safe navigation**:
  - Preserve `&.` in templates for nilable ViewModel properties (don't "tighten" callsites).

## 7) Verification and cleanup (required)

- Run the characterization spec again; it should pass unchanged.
- Run any directly related controller specs touched by `<controller>#<action>`.
- Ensure the ERB contains no `@variable` access and no direct `can?` / `current_user.*` / `polymorphic_path` calls per `erb/template-viewmodel-migration.mdc`.
- For any Ruby files changed, ensure no new default parameters were introduced (see `ruby-no-default-params.mdc`).

## 8) Output format (required)

Structure the response as:

```markdown
## ERB → ViewModel migration

### Inputs
- ERB: <erb-path>
- Controller/action: <controller>#<action>
- ViewModel: <view-model-constant> (<view-model-path>)
- Template var: view_model

### Render tree
- [List partials, top to bottom]

### Changes made
- [File list + 1-line summary each]

### Rule compliance notes
- [Call out any tricky spots and which rule/pattern you followed]

### Test plan
- [Exact rspec commands run and outcomes]
```
