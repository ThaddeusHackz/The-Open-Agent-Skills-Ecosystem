---
name: dashboard-ui
description: Expert dashboard, admin panel, and operational console design, redesign, and frontend QA. Use when Codex needs to build or improve analytics dashboards, admin panels, settings consoles, account consoles, billing consoles, monitoring or observability dashboards, customer-support inboxes, content moderation queues, ML experiment trackers, feature-flag consoles, internal tools, ops consoles, table-heavy interfaces, dashboard QA, dashboard redesign, or skill-mix evaluation for operational UI work.
---

# Dashboard UI

Use this skill to make dashboards faster to scan, easier to act on, and harder to ship broken. Dashboards are operational tools — they exist so users can see status, decide, and act, not so they can be impressed.

## Load References

Always load FIRST:

- `references/principle.md` — first-principles: a dashboard is a CONTROL SURFACE, not a presentation layer. The operator's 7-question silent monologue drives every layout decision.

Then:

- For any dashboard generation or redesign: read `references/workflow.md`, `references/patterns.md`, and `references/qa-checklist.md`.
- For critique or audit of an existing dashboard: also read `references/anti-patterns.md` (human failure modes) and `references/anti-slop.md` (AI-generated dashboard failure modes — required reading when an LLM is generating the dashboard).
- For specific surfaces (tables, filters, charts, command bars, detail pages, settings, forms, navigation, IA): load the matching `references/<surface>.md` when those files exist. If they do not yet exist, fall back to `references/patterns.md` plus this SKILL.md.
- For state coverage (empty, loading, error, success, feedback, support): load the corresponding `references/states/<state>.md` when present, otherwise apply the State Coverage step in `references/workflow.md`.
- For combining with `ui-ux-pro-max`, `ui-styling`, `motion-ui`, or `brand`: read `references/composability.md` and the Skill Mix Rule section below.
- For evidence-based rule grounding: read `references/captures-evidence.md` to see which captured Mobbin app confirms each rule, plus the open capture targets.
- For named interaction patterns: read `references/interaction-patterns.md` (sidebar-nav-categorised, view-switcher, three-pane-mail, cmd+k-palette, j/k-row-navigation, optimistic+undo-toast, status-pill-semantic, etc.) anchored to captured Mobbin slugs.

## Use This Skill To

- design or restructure an analytics console, admin panel, account or settings console, billing/usage console, monitoring or observability dashboard, customer-support inbox, moderation queue, ML experiment tracker, feature-flag console, internal ops tool, or any table-heavy operational interface;
- audit or redesign an existing dashboard that has drifted into a marketing layout or a card wall;
- specify state coverage (empty, loading, error, success, feedback, support) for an operational surface;
- run frontend QA on a dashboard implementation against an operational checklist, not a marketing one.

## Core Workflow

1. Capture the operational brief: who uses this, in what role, with what permissions, on what frequency, under what time pressure, and against which data scale.
2. List the user roles and pick the primary one. Different roles get different defaults, not different dashboards stacked on top of each other.
3. Enumerate the primary jobs the surface must support: monitor, find, decide, act, configure, audit. Pick one primary job per surface.
4. Decide the information architecture: top-level sections, surface hierarchy, and what lives at the index vs the detail level.
5. Choose navigation: top, side, or hybrid. Lock in breadcrumb, command-bar, and search behavior so the user is never lost.
6. Choose the primary surface for the index page: table, card grid, board, list, chart-led, or mixed. Default to a table when the data is row-shaped and actionable.
7. Design secondary surfaces: detail page or drawer, settings, modals or sheets, bulk actions, command palette.
8. Cover all states: empty (first-run, no-results, no-permission), loading (skeleton, progressive, optimistic), error (full-page, inline, retry), success and confirmation, feedback, and support entry points.
9. Define motion: subtle, status-driven, never decorative. Reserve motion for state changes, focus, async results, and reduced-motion fallbacks.
10. Run final QA from `references/qa-checklist.md`, including responsive (desktop-first 1440/1024, sensible 768; mobile only when the operational use case is real), accessibility, keyboard, and performance budgets.

## Skill Mix Rule

When multiple UI skills are active, this skill owns operational logic: information density, surface choice, table behavior, filters, saved views, state coverage, permissions, keyboard, and audit visibility. Let broader UI skills improve craft, accessibility, component quality, and visual polish, but do not let them override the surface's primary job, table-vs-card decision, density, or state coverage.

Before finalizing, run a short mix check:

- Does the dashboard still have one clear primary job per surface?
- Did visual polish reduce information density below what the role actually needs?
- Did motion or animation slow down repeat tasks?
- Did a brand or design-system rule push a marketing hero, hero-scale type, or decorative chart onto an operational page?
- Did `ui-ux-pro-max` or `ui-styling` push a card wall where a table belongs?
- Are empty, error, loading, and permission states still present and useful?

If a marketing-leaning skill is active (for example `landing-page-ui`), this skill takes precedence on any page that is behind login and used for repeat operational work.

## Validation

For implemented dashboards, verify at minimum:

- one clear primary job on the index surface;
- table or list density appropriate for the role (compact, comfortable, or roomy chosen on purpose);
- filters are visible and recoverable; saved views persist;
- empty, loading, error, and no-permission states are designed, not default;
- last-updated or refresh time is shown on any data surface;
- bulk actions and at least one keyboard shortcut for the primary action;
- detail pages or drawers expose actions, audit trail, and related records;
- responsive behavior at 1440, 1024, and 768; mobile only when the role actually uses it on mobile;
- no decorative charts, no marketing hero, no logo wall on the operational surface;
- accessibility basics: semantic landmarks, focus order, contrast, labeled controls.

If Playwright is available, use screenshots or DOM checks at desktop-first widths. If not, explicitly state that visual verification was not run.

## Limits

- This skill does not own marketing pages, pricing pages, or signed-out flows. Route those to `landing-page-ui`.
- This skill does not invent a design system. It assumes one exists or that `ui-styling` or `ui-ux-pro-max` is supplying components.
- Many references in this skill are corpus synthesis until `/scripts/mobbin/capture_dashboard.mjs` is run; pattern signals remain authoritative.
