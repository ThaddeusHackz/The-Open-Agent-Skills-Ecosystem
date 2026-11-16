---
name: seo-foundations
description: "Technical backbone for the Career Hub vital loop. Five SEO + website operating standards (technical SEO health / E-E-A-T + linkable-asset link building / programmatic SEO discipline (Schwartz) / Core Web Vitals + perf budgets / operational reliability with SRE primitives). Plus topical-cluster model, intent-mapping, GEO methodology (Princeton KDD 2024), and runbooks library."
metadata:
  family: seo
  owner: seo
  last_reviewed: 2026-04-29
  version: 1.0.0
  related_skills: [marketing-foundations, seo-audit, seo-page-rules, schema-markup, ai-seo, site-architecture]
  kpis:
    - "Indexation ≥90% of launched-pillar URLs in 30d"
    - "Schema validity 100% on templated pages"
    - "Cannibalization <5% of pages with sibling ranking same query"
    - "Anchor diversity <40% exact-match per target URL"
    - "p75 LCP <2.5s, INP <200ms, CLS <0.1 every page type"
  marketing_pillar: 4
  seo_standard: all
  funnel_stage: all
  content_class: all
  maturity_stage: prescriptive
  used_by_stages: [1, 2, 5, 6, 7, 8]
---

# SEO Foundations (Career Hub)

Technical backbone for every stage agent in the vital loop. Read first when scoring opportunities, validating templates, gating Stage 8 verification, or running incident response. Anchored in named research — every rule cites its source.

## When to Use

- Stage 1 Discovery scoring opportunities (Tier 1 indicators, intent-mapping, pSEO gates).
- Stage 2 Strategy writing briefs (intent + template + topical-cluster placement).
- Stage 5 Brand+Guardrail (GEO citation density per Aggarwal et al.).
- Stage 6 Template (schema rules, internal-linking rules, CWV budgets).
- Stage 7 UI (perf budgets, render strategy).
- Stage 8 UX verification (full standards check pre-ship).
- Incident response (runbooks for indexation/traffic/schema/sitemap/CWV regressions).

## Do Not Use When

- Net-new content drafting (use `content/` family).
- Marketing strategy decisions (use `marketing/marketing-foundations`).

## The Five Standards (one-line each, full content in references)

- **Standard A — Technical SEO health**: indexation ≥90% in 30d, schema validity 100%, anchor diversity <40% exact-match, cannibalization <5%, crawl health green. YMYL pages (Pillar 3) require highest trust per Google Search Quality Rater Guidelines.
- **Standard B — E-E-A-T + linkable-asset link building**: AuthorByline coverage 100% on guides + financial tips + role pages, citation density ≥1 per dollar amount (BRAND.md Four-Source Rule), freshness within template SLA, third-party authority targeted. Linkable-asset taxonomy at [reference/linkable-asset-taxonomy.md](reference/linkable-asset-taxonomy.md).
- **Standard C — Programmatic SEO discipline (Schwartz framework)**: from Eli Schwartz's *Product-Led SEO* (2021) — database content + user-generated value + validated demand + the "1,000 useful > 100,000 thin" rule. See [reference/pseo-quality-gates.md](reference/pseo-quality-gates.md).
- **Standard D — Core Web Vitals + perf budgets**: p75 LCP <2.5s, INP <200ms, CLS <0.1. Per-route JS budgets (homepage ≤80KB, tools ≤120KB, role/city/guide ≤60KB, programmatic ≤40KB). RSC-first, `next/image` everywhere, single web font, security headers maintained. See [reference/cwv-budgets.md](reference/cwv-budgets.md).
- **Standard E — Operational reliability (SRE primitives)**: every standard has an SLO, an SLI, and an error budget. Runbooks per common failure type at [reference/runbooks/README.md](reference/runbooks/README.md). DORA-style pipeline metrics. See [reference/excellence-targets.md](reference/excellence-targets.md).

## Topical Authority Model (Pillar-Cluster)

Per HubSpot 2017 + Brian Dean's Topic Cluster architecture. Career Hub already implements this; the model makes it explicit and measurable.

- **Pillar page** = the broad-topic owner (e.g., role hub for "Bartender jobs"). Internal links DOWN to all clusters.
- **Cluster pages** = narrow subtopics (how-to-become, interview-questions, resume-examples, salary-by-city, comparison). Each links UP to the pillar.
- **Cross-cluster links** = sparingly, only when contextually relevant.
- **PageRank flow** modeled per pillar.

Full cluster topology at [reference/topical-cluster-map.md](reference/topical-cluster-map.md). Each pillar in [nextjs-app/docs/PILLARS.md](../../../../nextjs-app/docs/PILLARS.md) is an SEO topical cluster.

## GEO Methodology

Per Aggarwal et al. (Princeton, KDD 2024). The 9 strategies tested in generative engines, ranked by visibility lift:

- citations: +40%
- statistics: +37%
- quotations: +30%
- authoritative tone: +25%
- improved clarity: +20%
- technical terms: +18%
- unique vocabulary: +15%
- fluency + statistics combined: max effect (up to +115% for low-authority sites)
- keyword stuffing: **-10%** (actively harmful)

`brand-lint` enforces the top three at template level: ≥1 citation per dollar amount, ≥1 statistic per H2 section, ≥1 quotation per data-rich page. Stage 5 fails any draft missing these.

Full GEO methodology at [reference/geo-methodology.md](reference/geo-methodology.md). Already partially in [.agents/skills/seo/ai-seo/SKILL.md](../ai-seo/SKILL.md).

## Intent Mapping

Every Strategic Brief tags `intent`. Intent → page type → schema → CTA pattern at [reference/intent-mapping.md](reference/intent-mapping.md). Intent-value multipliers calibrated quarterly from Tier 4 attribution.

## Cannibalization Rules

<5% of pages with a sibling ranking for the same primary query. Detection via `gsc-mcp.query_search_analytics` `query × page` join. Resolution patterns at [reference/cannibalization-rules.md](reference/cannibalization-rules.md).

## Internal Linking Rules

Hub-spoke architecture per pillar. Every page meets:

- min internal links IN per template
- min internal links OUT per template
- anchor diversity <40% exact-match per target URL
- contextual cross-cluster links where appropriate

See [reference/internal-linking-rules.md](reference/internal-linking-rules.md).

## Schema Rules

Required JSON-LD per template type (FAQ + Breadcrumb + Article | Occupation | SoftwareApplication | JobPosting). 100% Rich Results Test validity. Full rules at [reference/schema-rules.md](reference/schema-rules.md).

## Runbooks

Incident response runbooks at [reference/runbooks/README.md](reference/runbooks/README.md):

- `indexation-regression.md`
- `traffic-drop.md`
- `schema-breakage.md`
- `sitemap-drift.md`
- `cwv-regression.md`
- `noindex-accident.md`
- `pseo-thinning.md`

Each runbook follows: detect → classify (S1/S2/S3) → contain → fix → blameless postmortem.

## Quarterly Weight Tuning

Three weight files versioned in git, tuned monthly via `monthly-attribution-review`:

- [reference/excellence-targets.md](reference/excellence-targets.md) — KPI thresholds per pillar/template
- [reference/intent-mapping.md](reference/intent-mapping.md) — intent-value multipliers
- [reference/cwv-budgets.md](reference/cwv-budgets.md) — CWV + bundle budgets
