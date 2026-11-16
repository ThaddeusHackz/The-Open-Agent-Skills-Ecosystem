---
name: seo-health
description: "Specialist tool that wraps `pnpm seo:audit` + adds cannibalization detection (GSC query × page join), anchor diversity scan, schema validity check, pSEO uniqueness ratio per template, intent-mismatch detection. Used by Stage 1 Discovery + Stage 8 UX."
metadata:
  family: ops
  owner: seo
  last_reviewed: 2026-04-29
  version: 1.0.0
  related_skills: [seo-foundations, traffic-monitor, indexation-monitor, opportunity-discovery]
  kpis:
    - "Cannibalization <5% of pages with sibling ranking same query"
    - "Anchor diversity <40% exact-match per target URL"
    - "Schema validity 100% on templated pages"
    - "pSEO uniqueness ratio ≥40% per template"
  marketing_pillar: 4
  seo_standard: A_B_C
  kpi_tier: 1
  funnel_stage: all
  maturity_stage: diagnostic
  used_by_stages: [1, 8]
---

# SEO Health

Diagnostic specialist tool. Wraps existing `pnpm seo:audit` script and adds:

- **Cannibalization detection** (GSC `query × page` join)
- **Anchor diversity scan** (built-HTML scan per target URL)
- **Schema validity check** (Rich Results Test API on templated pages)
- **pSEO uniqueness ratio per template** (sample-pairwise content similarity)
- **Intent-mismatch detection** (brief intent vs SERP intent of ranking pages)

## When to Use

- Stage 1 Discovery weekly — surfaces `cannibalization_consolidation` + `schema_fix` + intent-mismatch opportunities.
- Stage 8 UX post-ship — verify shipped opportunity didn't introduce new cannibalization or schema issues.
- Ad-hoc: incident-response when investigating ranking regression.

## Do Not Use When

- Need general traffic snapshot — use `traffic-monitor`.
- Need indexation-only check — use `indexation-monitor`.
- Need CWV measurement — use `web-vitals`.

## Inputs

- `gsc-mcp.query_search_analytics` with `dimensions: ['query', 'page']` for cannibalization
- Built HTML from `pnpm smoke` or production fetch
- Schema validation via Rich Results Test API
- `seo-foundations/reference/topical-cluster-map.md` for cluster-level anchor diversity scope
- `seo-foundations/reference/intent-mapping.md` for intent verification

## Workflow

### 1. Cannibalization detection

```
cannibalized_queries = []
for each query with impressions ≥ 100 in last 28d:
    pages_ranking_top20 = distinct pages from GSC query × page
    if count(pages_ranking_top20) ≥ 2:
        cannibalized_queries.append({query, pages, impressions, positions})

corpus_cannibalization_rate = len(cannibalized_queries) / total_queries_with_top20
```

Pass: <5%. Warn: 5-10%. Fail: >10% = S2 incident.

### 2. Anchor diversity scan

For each target URL with ≥3 incoming internal links:

- Scan built HTML for all anchors pointing to the URL.
- Compute exact-match anchor share = anchors-with-text-equal-to-primary-keyword / total-anchors.
- Pass: <40%. Warn: 40-50%. Fail: >50% = S3.

### 3. Schema validity

For each templated page:

- Run Rich Results Test API.
- Pass: 100% valid. Any failure on launched template = S1 incident.

### 4. pSEO uniqueness ratio (per Eli Schwartz framework)

For each pSEO template (e.g., city-role pages):

- Sample 20 pages.
- Compute pairwise content similarity (word-shingle Jaccard).
- uniqueness_ratio = 1 - mean(pairwise similarity).
- Pass: ≥40%. Warn: 30-40%. Fail: <30% = `pseo-thinning.md` runbook.

### 5. Intent-mismatch detection

For each Strategic Brief shipped 30d ago:

- Pull GSC queries the page actually ranks for.
- Map dominant query intent (using `intent-mapping.md`).
- Compare to brief's tagged intent.
- Flag mismatches as `90_10_class: schema_fix` opportunities for next Discovery.

## Output Contract

Markdown block at `nextjs-app/docs/reports/<date>/seo-health.md`:

```markdown
## SEO Health Report — <date>

### Cannibalization
- Corpus rate: X% (target <5%)
- Top 5 cannibalized queries: <table>
- Resolution recommendations: <consolidate / canonicalize / differentiate / noindex>

### Anchor Diversity
- URLs flagged with >40% exact-match: <count>
- Top 5 over-optimized targets: <table>

### Schema Validity
- Templated page pass rate: X% (target 100%)
- Failing templates: <list>

### pSEO Uniqueness
| Template | Uniqueness ratio | Status |
|---|---|---|
| city-role-page | 0.42 | PASS |
| state paycheck | 0.51 | PASS |
| ... | ... | ... |

### Intent Mismatches (post-ship)
- Briefs with intent mismatch at 30d: <count>
- Surface as ctr_rescue opportunities: <list>
```

## Reporting

Every run appends to `_index.json` with `agent: ops/seo-health`.

If any S1/S2 condition triggered, escalate to `incident-response` playbook → matched runbook in `seo-foundations/reference/runbooks/`.

## References

- [seo-foundations/reference/cannibalization-rules.md](../../seo/seo-foundations/reference/cannibalization-rules.md)
- [seo-foundations/reference/internal-linking-rules.md](../../seo/seo-foundations/reference/internal-linking-rules.md)
- [seo-foundations/reference/schema-rules.md](../../seo/seo-foundations/reference/schema-rules.md)
- [seo-foundations/reference/pseo-quality-gates.md](../../seo/seo-foundations/reference/pseo-quality-gates.md)
- [seo-foundations/reference/intent-mapping.md](../../seo/seo-foundations/reference/intent-mapping.md)
