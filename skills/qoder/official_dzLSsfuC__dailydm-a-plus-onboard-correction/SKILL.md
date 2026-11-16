---
name: a-plus-onboard-correction
description: Generate one-off Ruby scripts to correct Attendance Plus entities for a district after onboarding. Use when the user says "a-plus-onboard-correction", "correct A+ entities", "fix absence codes", "add non-instructional days", "change school year dates", "update tier thresholds", or describes attendance configuration changes needed for a customer.
---

# Attendance Plus Onboard Correction

Generate one-off Ruby scripts to correct A+ entity configuration for a district. These scripts are throwaway artifacts -- copied to `tmp/` on the target environment, dry-run to verify, then applied.

## Step 1: Triage the Request

Parse the user's request into one or more entity corrections. A single request often contains multiple corrections.

| Business Language | Entity Type | Reference | Template |
|---|---|---|---|
| "code X needs is_suspension changed", "change absence type", "remap codes" | Absence code update | `references/absence-codes.md` | `assets/absence-code-update.md` |
| "add code ISS", "create new absence code", table of new codes | Absence code create | `references/absence-codes.md` | `assets/absence-code-create.md` |
| "remove code X", "retire/disable code", "discard obsolete codes" | Absence code discard | `references/absence-codes.md` | `assets/absence-code-discard.md` |
| "school X has different start/end date", "earlier/later start/end" | Calendar: school year creation | `references/calendar.md` | `assets/calendar.md` (Mode 1) |
| "add November 4th as non-attendance day", "add closure dates" | Calendar: NID addition | `references/calendar.md` | `assets/calendar.md` (Mode 2 or 3) |
| "change tier thresholds", "add/remove tier", "adjust tier labels" | Tier update | `references/tiers.md` | `assets/tier-update.md` |

Always read `references/domain-api.md` for API signatures, key types, and schema.

## Step 2: Gather Required Inputs

For every correction, you need at minimum:

- **District ID** (always required)
- Entity-specific inputs (detailed in each template's "Required Inputs" section)

If the user hasn't provided enough information, ask before generating. Common gaps:

- Absence code create: missing fields in the table (is_suspension, exclude_from_days_absent, etc.)
- School year: unclear whether start date, end date, or both differ from the district
- NID addition: missing reason (default to `:non_enrollment` if not specified)

## Step 3: Determine Script Composition

Corrections compose into scripts following these rules:

| Combination | Scripts |
|---|---|
| Absence code updates + creates + discards | **One script** with phases |
| School year creation + NID additions | **One script** (inherently coupled) |
| Tier threshold/label changes | **One script** (always separate) |
| Codes + calendar in same request | **Two separate scripts** |
| Codes + tiers in same request | **Two separate scripts** |
| Calendar + tiers in same request | **Two separate scripts** |

When generating multiple scripts, output them sequentially with clear separators and distinct filenames.

## Step 4: Generate Each Script

For each script to generate:

1. Read `references/domain-api.md` for API signatures and schema
2. Read the entity-specific `references/` file for domain constraints and pitfalls
3. Read the relevant `assets/` template(s) for structural patterns
4. Compose the script using `assets/script-skeleton.md` as the wrapper

## Step 5: Output the Script and Execution Guidance

### Filename Convention

`<district_id>-<short-description>.rb` (e.g., `3192-school-years.rb`, `1475-update-codes.rb`)

### Execution Instructions

After generating each script, remind the user to:

1. Copy the script to `tmp/` on the target environment
2. Dry run first: `ruby tmp/<filename>.rb`
3. Review the output table carefully
4. Apply only if output looks correct: `ruby tmp/<filename>.rb apply`
5. Monitor Sidekiq jobs after applying
6. Check the Attendance Plus UI for updated sync timestamps

See `references/domain-api.md` for observability details (DataSync records, Sidekiq Web UI, Attendance Plus UI).
