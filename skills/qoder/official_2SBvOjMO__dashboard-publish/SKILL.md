---
name: dashboard-publish
description: Package a self-contained HTML dashboard into the Vault tenant-dashboards ingest contract (DashboardManifestV1 + sandbox-safe HTML). Use after generating a dashboard with /viz when the result needs to be delivered to a Vault tenant.
allowed-tools: Read, Write, Bash, Grep, Glob
version: 1.0.0
---

# Dashboard Publish — Vault Tenant Dashboards Producer

## When to use this skill

The user is asking to:
- "Publish this dashboard to Vault"
- "Get this dashboard into the portal for <client>"
- "Package this for the tenant dashboards system"
- "Convert this viz output into something I can upload"

…and you already have (or are about to generate) an HTML5 dashboard via
`/viz` (or any equivalent producer).

Skip this skill if the user just wants to view the dashboard locally — `/viz`
already produces a viewable HTML file. This skill is specifically for the
**Vault upload contract**.

## Vault contract — the only thing that matters

Vault is the consumer. It exposes `POST /api/dashboards/ingest` (staff-gated)
that accepts JSON `{ manifest, html_base64 }` and renders the HTML inside
`<iframe sandbox="allow-scripts" srcdoc>` with a server-injected meta-CSP of:

```
default-src 'none';
script-src 'unsafe-inline';
style-src 'unsafe-inline';
img-src data:;
connect-src 'none';
font-src data:;
```

Translation:
- **Inline scripts and styles work.** The producer can use Chart.js, Plotly,
  D3, custom JS — as long as it's all inlined into the HTML.
- **External anything fails silently.** No CDN imports. No `<link rel="stylesheet" href="https://…">`.
  No `<img src="https://…">`. No external font imports. No `fetch()`.
- **Images and fonts must be `data:` URIs** if present. The CSP allows
  `img-src data:` and `font-src data:`, nothing else.
- **The iframe is in a null origin.** Even if you wanted to break out, you
  can't reach the parent's Supabase session, cookies, or DOM.

Anything that violates these constraints will *appear* to work locally but
*will not render* inside the portal. That's the bug class this skill exists
to prevent.

## Two-stage validation

Before writing any files, this skill / CLI runs two validators:

### 1. HTML shape (mirrors Vault's `lib/dashboards/htmlValidate.ts`)
- Starts with `<!DOCTYPE html>` (case-insensitive, leading whitespace OK)
- Contains `<head>` and `</head>`
- Size ≤ 5 MB (5 _242 _880 bytes — matches the migration CHECK constraint)

Failure → `invalid_html_shape` or `html_too_large`.

### 2. Self-containment (producer-side gate; no Vault equivalent)
- No `<script src=>`, `<link href=>`, `<img src=>`, etc. unless `data:` or `#fragment`.
- No `<source>`, `<video>`, `<audio>`, `<iframe>`, `<embed>`, `<object data=>`,
  `<track>`, `<input type="image">`, `<video poster>`.
- No CSS `url(http…)` or `@import "http…"`.
- `srcset` entries are split and each URL is checked.

Failure → `external_references_found`. The error includes a list of offending
tags so the producer can fix them.

## Manifest schema (DashboardManifestV1)

The manifest must match Vault's Zod schema exactly:

```json
{
  "schema_version": 1,
  "tenant_slug": "acme",
  "kind": "forecast",
  "slug": "main",
  "title": "Q2 2026 Forecast",
  "version_label": "2026-05-01T00:00:00Z",
  "generator": {
    "skill": "opspal-core:dashboard-publish",
    "skill_version": "1.36.4",
    "model": "claude-opus-4-7",
    "generated_at": "2026-05-01T00:00:00Z"
  },
  "source_fingerprint": {
    "data_as_of": "2026-05-01T00:00:00Z",
    "input_hash": "0123abcd…64hex",
    "row_counts": { "opportunities": 312, "accounts": 42 }
  },
  "html_size_bytes": 184213,
  "html_sha256": "abcd0123…64hex"
}
```

Slug regex: `^[a-z0-9][a-z0-9-]{1,62}$`. Forecast and pipeline kinds **must**
use `slug='main'` — that's how Vault wires the `/t/<slug>/forecast` and
`/t/<slug>/pipeline` redirects to the current published row. Custom kinds
take any compliant slug.

`html_size_bytes` and `html_sha256` are computed by the publisher from the
HTML payload — never accept these from the caller, since drift between
declared size/hash and actual content is a data integrity bug.

## Workflow

### Path A — fresh dashboard from /viz

```bash
# 1. Generate HTML via /viz (existing infrastructure)
/viz template create executive-summary --org $ORG --output ./out/dash.html

# 2. Preview what inlining would do without publishing
node scripts/lib/dashboards/cli.js validate \
  --html ./out/dash.html --inline-assets

# 3. Publish in one shot. When --input-file is JSON of shape
#    { <object>: [...rows] } with timestamp fields on each row, the
#    publisher auto-derives row_counts + data_as_of so they don't need
#    to be passed separately:
node scripts/lib/dashboards/cli.js publish \
  --inline-assets \
  --html ./out/dash.html \
  --tenant $TENANT_SLUG \
  --kind forecast \
  --slug main \
  --title "Q2 2026 Forecast" \
  --input-file ./inputs.json   # → input_hash + row_counts + data_as_of
```

If your input file has a different shape (top-level array, primitive,
or mixed value types), explicit `--row-counts` and `--data-as-of` flags
are required. The CLI errors with a clear hint pointing at the right flag.

If you'd prefer to inspect the inlined HTML before publishing, run the
`inline` subcommand to produce a transformed file you can hand-check:

```bash
node scripts/lib/dashboards/cli.js inline \
  --html ./out/dash.html \
  --out  ./out/dash-inlined.html
```

### Path B — re-publishing an existing artifact

If staff already has an HTML + a manifest hand-written, validate the pair
before uploading:

```bash
node scripts/lib/dashboards/cli.js validate --html ./prior.html
# Review prior.manifest.json against the schema above; missing fields will
# be rejected by Vault's Zod schema with `invalid_manifest`.
```

## Asset inlining (`--inline-assets`)

`/viz` today emits CDN `<script src>` tags by default — Chart.js via
jsdelivr, Leaflet via unpkg, SheetJS via cdn.sheetjs.com, Mermaid via
jsdelivr. Vault's render CSP blocks all of those.

The asset inliner closes the gap: when `inlineAssets: true` (CLI flag
`--inline-assets`), the publisher runs an HTTP-fetch+rewrite pass before
validation. For each allowlisted `<script src>` and `<link rel="stylesheet">`
tag, it fetches the URL once (disk-cached at `~/.cache/opspal/dashboard-assets/`)
and replaces the tag with `<script>…inlined…</script>` or
`<style>…inlined…</style>`.

The inliner refuses to fetch from anything outside the allowlist
(`cdn.jsdelivr.net`, `unpkg.com`, `cdn.sheetjs.com` by default). It also
refuses to inline assets larger than the per-asset cap (default 5 MB) so
the resulting HTML can't blow past Vault's total cap. Errors fail loudly
— silent rewriting would mask producer bugs.

Pipeline order with inlining enabled:

```
viz HTML ──► [inline-assets] ──► [shape] ──► [self-containment] ──► [manifest] ──► write
                  ↑
        fetches CDNs once,
        caches on disk
```

If the post-inlining HTML still fails self-containment (e.g. the inlined
Leaflet stylesheet contains a `url()` reference to an external image),
the validator catches it and the publish fails. That's the right
behavior — those would silently fail at render time anyway.

## What this skill does NOT do (yet)

- **Upload to Vault.** The first cut intentionally writes files to disk
  only. Once Vault's service-token CLI ships (Vault slice S1.3) we'll add a
  `--upload` flag that POSTs to the ingest endpoint with a Bearer token.
  Until then, take the two files and paste them into Vault's manual upload
  form at `/admin/clients/<slug>?tab=dashboards`.
- **Generate the underlying HTML.** That's `/viz`'s job.
- **Recursively inline images/fonts referenced from inlined CSS.** If a
  fetched stylesheet contains `url(http…)` references to images, the
  self-containment validator will flag those and publish will fail. The
  producer needs to choose libraries with self-contained CSS, or pre-inline
  those references in the source HTML before publishing.

## Common failures and what they mean

| Code | Meaning | Fix |
|---|---|---|
| `invalid_html_shape` | Missing/malformed doctype or `<head>` | Producer is emitting fragments, not a full HTML5 doc. |
| `html_too_large` | > 5 MB | Reduce inlined data or images. Plotly's largest bundle is ~3.5 MB; trim payload. |
| `external_references_found` | CDN/external refs detected | Inline the dependency or use a pre-bundled producer. |
| `invalid_manifest` | Field missing/malformed | Check the field name in the error — slug regex, kind enum, ISO 8601, sha256 hex are common offenders. |

## Files

- `scripts/lib/dashboards/integrity.js` — sha256 + size helpers
- `scripts/lib/dashboards/fingerprint.js` — canonical input hash + data_as_of resolver
- `scripts/lib/dashboards/asset-inliner.js` — fetch + inline allowlisted CDN refs
- `scripts/lib/dashboards/self-containment-validator.js` — external-ref detector
- `scripts/lib/dashboards/html-shape-validator.js` — doctype/head/size checks
- `scripts/lib/dashboards/manifest-builder.js` — DashboardManifestV1 schema + builder
- `scripts/lib/dashboards/publisher.js` — orchestrator (inline → validate → manifest → write)
- `scripts/lib/dashboards/cli.js` — CLI entry
- `commands/dashboard-publish.md` — slash-command reference

## See also

- Vault spec: `RevPal-Vault/docs/superpowers/specs/2026-05-01-tenant-dashboards-html-design.md`
- Vault implementation plan: `RevPal-Vault/docs/superpowers/plans/2026-05-01-tenant-dashboards-html.md`
- Existing producer: `commands/viz.md`, `agents/web-viz-generator.md`, `scripts/lib/web-viz/output/StaticHtmlGenerator.js`
