---
name: seo-section-ai-audit
description: Use when producing the ai_visibility slice (`data.ai_visibility.{audit_date, platforms, citability, queries_with_ai, geo_roadmap, kpis}`) for **template ID sec-14** (sidebar/Nubank display number 13) of the Nubank-fidelity HTML report. Replaces legacy `/seo-diagnostico` cluster `ai_visibility` (was stub) with strict W3.4 schema validation pre-persist + disk-cacheable slice + sample mode + modular MCP architecture (gsc-mcp + ahrefs-mcp Brand Radar 7 platforms + dataforseo SERP + WebFetch + memory-mcp + 3 subagents). Triggers on "/seo-section-ai-audit", "ai-audit slice", "visibilidad IA", "GEO/AEO audit", "section 13", "section 14", "sec-14", or when /seo-build-report needs the ai_visibility slice.
---

<execution-protocol>
MODO: EJECUCION DIRECTA — NO PLANIFICACION

Este skill es un PIPELINE DE ANALISIS que produce un slice JSON estricto
(`ai_visibility.{audit_date, platforms, citability, queries_with_ai, geo_roadmap, kpis}`)
que rinde la sec-14 (template ID) — display num 13 en sidebar Nubank — Visibilidad en IA
y Estrategia GEO/AEO del HTML Nubank-fidelity.

**Disambig sec-14 vs sec-13** (fix 2026-05-05): el template path real es
`14-visibilidad-ia/template.njk` (template ID = `sec-14`). El sidebar Nubank lo numera como
`13` porque sec-02 "Datos del Proyecto" no se renderiza independiente (está embebido en
sec-01 Resumen Ejecutivo). Mapping completo: `sec-14 (template ID) → 13 (Nubank display num)`.
sec-13 (template ID) corresponde a Benchmarks (`13-benchmarks/template.njk`, display num 12).
Al leer estas instrucciones, EJECUTAR cada fase haciendo MCP calls reales.

PROHIBIDO:
- Escribir archivos de plan
- Describir lo que "harias" sin hacerlo
- Saltar fases o colapsar multiples fases en una respuesta
- Inventar datos sin fundamentarlos en MCP responses reales
- Persistir el slice sin pasar `validateAiAuditSlice()` (schema strict W3.4)
- Producir `platforms` array fuera de [3, 8] items
- Producir `citability.factors` length distinto de 8
- Producir `citability.score` fuera de [0, 10]
- Producir `queries_with_ai` length fuera de [5, 10]
- Producir `geo_roadmap` length distinto de 3 (Fase 1 / Fase 2 / Fase 3)
- Producir `kpis` length distinto de 6
- Saltar STOP gates al Lead — son OBLIGATORIOS (URL sampling, queries shortlist, citability scores)
- Hidear sub-bloques 9.1-9.7 con hl_box azul "honest pendiente" — anti-pattern PROHIBIDO
  (Engram obs #586 — Nubank fidelity strict)
- Procesar raw responses (>50KB) en main context — usar SIEMPRE subagent delegation
  (Patron 1 context-engineering, repo skill 3/7 history empirically validated)

OBLIGATORIO:
- Operador = userEmail prefix del environment (ej: nico.m@puntorojo.com → Nico)
- Memory-first: empezar con `memory-mcp.get-client-summary` (Patron 7)
- OAuth multi-cuenta swap detection en Phase 0.4 (CLAUDE.md cliente row "GSC Property" parens)
- Cross-section detection en Phase 0.5 (read clients/{slug}/sections/*.json)
- 3 STOP gates al Lead: (1) URL sampling Phase 1c, (2) queries shortlist Phase 2c, (3) citability scores Phase 4d
- Subagent delegation OBLIGATORIA para: Brand Radar ai-responses bulk (Phase 3b), DataForSEO SERP bulk (Phase 3a), WebFetch citability multi-URL (Phase 4b)
- Validar slice con `report-builder/lib/ai-audit-validator.js` ANTES de persist (Phase 6)
- Persist en `~/Documents/punto-rojo-clients/{slug}/sections/ai-audit.json` (run real)
  o `report-builder/samples/sections/ai-audit.json` (--sample mode)
- Engram save graceful degrade: si mem_save falla → log warning + continuar (NO bloqueante)

Protocolo: shared/skill-execution-protocol.md
Context engineering: shared/context-engineering.md (Patrones 1, 5, 7)
</execution-protocol>

# /seo-section-ai-audit — AI Visibility slice (Nubank-fidelity)

## Objetivo

Producir un slice JSON estricto `{ ai_visibility: { audit_date, platforms, citability, queries_with_ai, geo_roadmap, kpis } }` que rinde la **sec-14 (template ID) Visibilidad en IA y Estrategia GEO/AEO** — sidebar/Nubank display num **13** — del HTML Nubank-fidelity (`report-builder/sections/C-diagnostico-seo/14-visibilidad-ia/template.njk`, Phase 3.3).

**Modelo recomendado**: Sonnet (cualitativo + structured extraction + multi-source synthesis sobre real data).

**Reemplaza**: cobertura `ai_visibility` del legacy `/seo-diagnostico` cluster (era stub Brand Radar shape obsoleto). La diferencia principal: validación estricta del shape pre-persist via `ai-audit-validator.js` + arquitectura modular (llama MCPs directos sin pasar por `diagnostic-mcp` orchestrator).

---

## Modes

| Mode | Trigger | Source | Output path |
|------|---------|--------|-------------|
| **Real client** (default) | `--client-slug=<slug>` o el Lead invoca desde cwd cliente | gsc-mcp + ahrefs-mcp Brand Radar (7 platforms) + dataforseo SERP + WebFetch + memory-mcp + 3 subagents | `~/Documents/punto-rojo-clients/{slug}/sections/ai-audit.json` |
| **Sample (dev/test)** | `--sample` flag | `report-builder/samples/chedraui-sample.json` (`ai_visibility` block) | `report-builder/samples/sections/ai-audit.json` |
| **Cache** | `--from-cache` flag | Slice JSON persistido | (re-emite sin re-correr MCPs) |
| **Combined** | `--sample --from-cache` | Sample slice persistido | (re-emite del cache) |

---

## Inputs (CLI flags)

```
--client-slug=<kebab-case>           # required en run real
--sample                             # flag, dev/test mode
--from-cache                         # flag, lee slice persistido
--no-engram                          # flag debug, skip engram persistence
--platforms=<list>                   # optional override (default 7 BR platforms)
--queries-shortlist=<N>              # optional, default 7 (queries en template 9.3)
--queries-internal=<N>               # optional, default 20 (queries analizadas internamente)
--url-samples-count=<N>              # optional override del per-industry default
--brand-radar-date-from=<YYYY-MM-DD> # optional, default today-30d
--brand-radar-date-to=<YYYY-MM-DD>   # optional, default today
```

---

## Output (slice JSON)

Schema authoritative: `skills/seo-section-ai-audit/schema.json`. Reference impl: `report-builder/lib/ai-audit-validator.js`.

```json
{
  "ai_visibility": {
    "audit_date": "2026-05-03",
    "platforms": [
      { "name": "Google AI Overviews", "presence": "Parcial", "type": "Mención en queries transaccionales", "frequency": "Media: 3 de 7 queries top con AIO citan al cliente", "status": "warning" }
    ],
    "citability": {
      "score": 2.5,
      "factors": [
        { "factor": "Datos estructurados (Schema.org)", "current": "...", "score": 2, "recommendation": "..." }
      ]
    },
    "queries_with_ai": [
      { "query": "...", "volume": 4400, "ai_overview": "optimal", "we_cited": "critical", "competitors": "Walmart, Soriana", "action": "..." }
    ],
    "geo_roadmap": [
      { "phase": "Fase 1", "weeks": "Semanas 1-4", "actions": ["..."], "deadline": "Mes 1", "impact": "..." }
    ],
    "kpis": [
      { "name": "Citaciones en AI Overviews", "baseline": "~0", "target_3m": "5-10", "target_6m": "20+", "tool": "GSC + monitoreo manual" }
    ],
    "degradation": {
      "cross_section": { "skip_reason": "no prior slices found", "fallback_used": "boilerplate genérico per-industry" }
    }
  }
}
```

**Strict contract guards** (enforced by `validateAiAuditSlice` pre-persist):
- `audit_date` ISO `YYYY-MM-DD`
- `platforms` length [3, 8] (default 7 — Brand Radar coverage)
- `platforms[].status` enum `optimal|acceptable|warning|critical`
- `citability.score` number [0, 10]
- `citability.factors` **exactly 8 items** (canonical Punto Rojo factors)
- `citability.factors[].score` integer [1, 10]
- `queries_with_ai` length [5, 10] (template renders 5-10 rows)
- `queries_with_ai[].ai_overview` AND `.we_cited` enum status
- `queries_with_ai[].volume` non-negative integer
- `geo_roadmap` **exactly 3 items** (Fase 1 / Fase 2 / Fase 3)
- `geo_roadmap[].actions` non-empty array of strings
- `kpis` **exactly 6 items** (canonical Punto Rojo KPIs)
- `degradation` per-source `{skip_reason, fallback_used?}`

---

## Prerequisitos

1. **Cliente provisionado en backend** — `memory-mcp.get-client-summary({slug})` debe devolver 200. Si no → ABORT.
2. **`industry`** snake_case (regex `/^[a-z_]+$/`) — del `get-client-summary`. Determina URL sampling defaults + boilerplate per-industry para roadmap/KPIs degradados.
3. **GSC siteUrl accesible** — `gsc.list_sites` debe incluir el `siteUrl` con la cuenta OAuth actual. **GSC es PRIMARY source para URL sampling + queries pool**; si no accesible → degrade a Ahrefs `site-explorer-top-pages`.
4. **Env vars**: `CRAWL_API_KEY`, `CRAWL_API_BASE_URL`, `AHREFS_API_KEY`, `GA4_REFRESH_TOKEN` (compartido GSC). **DataForSEO** vía MCP built-in.
5. **Repo privado clonado**: `~/Documents/punto-rojo-clients/{slug}/` debe existir para persist en run real (no aplica `--sample`).
6. **OAuth multi-cuenta**: el cliente debe declarar cuenta accesos en `<repo-cliente>/CLAUDE.md` row "GSC Property" parens. Si OAuth activa NO matchea → STOP gate al Lead pidiendo `gsc_reauth` swap (skill 2/7 + 3/7 pattern).

---

## Flujo general (7 phases efectivas + 3 STOP gates)

```
Inicio → Prerequisitos →
  Phase 0: Mode + cache + workflow guards + cross-section context detection
  Phase 1: URL sampling (cascade GSC → STOP gate Lead approval) + Brand Radar bulk (7 platforms × 3 endpoints)
  Phase 2: Queries shortlist (cascade intelligence → GSC filtered → STOP gate Lead 7-10 finales)
  Phase 3: Per-query enrichment (DataForSEO SERP × N + Brand Radar ai-responses × 4 platforms via subagents)
  Phase 4: Citability heurística multi-page (WebFetch × N URLs via subagent → STOP gate Lead aprobar 8 scores)
  Phase 5: Cross-section synthesis (Roadmap + KPIs según context level HIGH/MEDIUM/LOW)
  Phase 6: Build slice via extractor + Schema validation + Persist
  Phase 7: Engram save graceful + Output al Lead
```

---

## Phase 0 — Mode + cache + workflow guards + cross-section detection

> **Working directory**: cwd debe ser raíz del repo `punto-rojo-claude-toolkit`.

### 0.1 Detectar mode

```js
const fs = require('fs');
const path = require('path');
const os = require('os');
const { validateAiAuditSlice } = require('./report-builder/lib/ai-audit-validator');
const { extractAiAuditSlice, extractFromSample } = require('./report-builder/lib/ai-audit-extractor');

const slicePath = sampleMode
  ? path.join('report-builder', 'samples', 'sections', 'ai-audit.json')
  : path.join(os.homedir(), 'Documents', 'punto-rojo-clients', slug, 'sections', 'ai-audit.json');
```

### 0.2 Cache check (early return si `--from-cache`)

```js
if (fromCache && fs.existsSync(slicePath)) {
  const slice = JSON.parse(fs.readFileSync(slicePath, 'utf8'));
  const { valid, errors } = validateAiAuditSlice(slice);
  if (valid) return { slice, slicePath, mode: 'cached', cacheHit: true };
  console.warn(`Cache invalid (${errors.length} errors), regenerating: ${errors.join('; ')}`);
}
```

### 0.3 Sample mode shortcut

```js
if (sampleMode && !fromCache) {
  const samplePath = path.join('report-builder', 'samples', 'chedraui-sample.json');
  const sample = JSON.parse(fs.readFileSync(samplePath, 'utf8'));
  const slice = extractFromSample(sample);
  const { valid, errors } = validateAiAuditSlice(slice);
  if (!valid) throw new Error(`Sample slice invalid:\n  - ${errors.join('\n  - ')}`);
  fs.mkdirSync(path.dirname(slicePath), { recursive: true });
  fs.writeFileSync(slicePath, JSON.stringify(slice, null, 2));
  return { slice, slicePath, mode: 'sample' };
}
```

### 0.4 Workflow guards + OAuth multi-cuenta swap (real client mode)

> **OAuth multi-cuenta (CRITICAL — pattern skill 2/7 + 3/7)**: Punto Rojo usa 2 cuentas Google OAuth (`accesos@puntorojo.com` y `accesos2@puntorojo.com`). Cada cliente declara cuál tiene access en su `<repo-cliente>/CLAUDE.md` row "GSC Property" parens. Si la OAuth actual NO tiene el siteUrl en `list_sites`, **STOP gate al Lead pidiendo swap** antes de degradar.

```js
// 1. Cliente exists
const summary = await mcp.memory.get_client_summary({ slug });
if (summary.error?.code === 404) throw new Error(`Client ${slug} not provisioned in backend`);
const industry = summary.client.industry;
const siteUrl = summary.client.site_url;
const clientHostname = new URL(siteUrl).hostname.replace(/^www\./, '');

// 2. Read cliente CLAUDE.md (canonical for OAuth account hint + competitors)
const clientRoot = path.join(os.homedir(), 'Documents', 'punto-rojo-clients', slug);
const clientClaudeMdPath = path.join(clientRoot, 'CLAUDE.md');
let clientClaudeMd = '';
if (fs.existsSync(clientClaudeMdPath)) {
  clientClaudeMd = fs.readFileSync(clientClaudeMdPath, 'utf8');
}

// 3. Detect expected OAuth account
let expectedAccount = null;
const acctMatch = clientClaudeMd.match(/\|\s*\*\*GSC\s*Property\*\*\s*\|[^|]*\(([Aa]ccesos2?)\)\s*\|/);
if (acctMatch) expectedAccount = acctMatch[1].toLowerCase();

// 4. GSC accessible + OAuth swap detection
const gscSites = await mcp.gsc.list_sites({});
const gscSiteFound = gscSites.sites.some(s =>
  s.siteUrl === siteUrl ||
  s.siteUrl === `sc-domain:${clientHostname}`
);
const degradation = {};
if (!gscSiteFound) {
  if (expectedAccount) {
    console.warn(`⚠️ GSC: ${siteUrl} NO está en la OAuth actual. CLAUDE.md indica cliente en "${expectedAccount}".`);
    console.warn(`   PREGUNTAR al Lead: "¿hacemos swap OAuth a ${expectedAccount}@puntorojo.com con gsc_reauth?"`);
  }
  console.warn(`⚠️ Si swap no se hizo o falló — degradando a Ahrefs site-explorer-top-pages`);
  degradation.gsc = {
    skip_reason: `siteUrl not in accessible GSC properties (expected ${expectedAccount || 'unknown'} account)`,
    fallback_used: 'Ahrefs site-explorer-top-pages',
  };
}
```

### 0.5 Cross-section context detection

Detect availability of prior Phase 8 slices to determine context level for Phase 5 synthesis:

```js
const sectionsDir = path.join(clientRoot, 'sections');
const priorSlices = {};
for (const name of ['tech-audit', 'history', 'foda']) {
  const p = path.join(sectionsDir, `${name}.json`);
  if (fs.existsSync(p)) {
    try {
      priorSlices[name] = JSON.parse(fs.readFileSync(p, 'utf8'));
    } catch (e) {
      console.warn(`Failed to parse ${name}.json: ${e.message}`);
    }
  }
}
const priorCount = Object.keys(priorSlices).length;
const contextLevel = priorCount >= 3 ? 'HIGH' : (priorCount >= 1 ? 'MEDIUM' : 'LOW');
console.log(`Cross-section context: ${contextLevel} (${priorCount} prior slices: ${Object.keys(priorSlices).join(', ') || 'none'})`);
```

### 0.6 Read intelligence files (mandatory + optional)

```js
const intelligence = {};
for (const name of ['perfil', 'objetivos', 'productos-foco', 'competidores', 'estacionalidad', 'contexto-historico']) {
  const p = path.join(clientRoot, 'intelligence', `${name}.md`);
  if (fs.existsSync(p)) {
    intelligence[name] = fs.readFileSync(p, 'utf8');
  }
}

// OPTIONAL override: url-samples.md — if exists, FORCES URL sampling skip GSC flow
const urlSamplesPath = path.join(clientRoot, 'intelligence', 'url-samples.md');
let urlSamplesOverride = null;
if (fs.existsSync(urlSamplesPath)) {
  urlSamplesOverride = parseUrlSamplesMd(fs.readFileSync(urlSamplesPath, 'utf8'));
  console.log(`URL sampling override: ${urlSamplesOverride.length} URLs declared in intelligence/url-samples.md — skipping GSC flow`);
}
```

---

## Phase 1 — URL sampling + Brand Radar bulk

### 1a. Industry-specific URL sampling defaults

```js
const URL_SAMPLE_DEFAULTS = {
  retail_supermercado: 12,  // home + 3 categorías + 3 fichas + 2 promo + 2 ayuda + 1 brand
  retail_general:       10,
  ecommerce:            10,
  telco:                 9,  // home + 3 servicios + 2 fichas equipos + 2 ayuda + 1 brand
  fintech:               8,  // home + 2 productos + 2 educational + 2 calculadoras + 1 brand
  banking:               8,
  saas:                  8,  // home + 2 features + 1 pricing + 2 docs + 2 blog
  blog:                  7,  // home + 5 top articles + 1 about
  default:               8,
};
const urlSampleCount = (flags.urlSamplesCount || URL_SAMPLE_DEFAULTS[industry] || URL_SAMPLE_DEFAULTS.default);
```

### 1b. URL sampling cascade

```js
let sampledUrls = [];

// SHORT-CIRCUIT: intelligence/url-samples.md override
if (urlSamplesOverride && urlSamplesOverride.length >= 3) {
  sampledUrls = urlSamplesOverride.slice(0, urlSampleCount);
  console.log(`Using override URLs from intelligence/url-samples.md (${sampledUrls.length})`);
} else {
  // PRIMARY: GSC search_analytics page+query 90d
  if (!degradation.gsc) {
    const today = new Date();
    const startDate = new Date(today.getTime() - 90 * 86400000).toISOString().slice(0, 10);
    const endDate   = new Date(today.getTime() - 1  * 86400000).toISOString().slice(0, 10);
    const gscData = await mcp.gsc.search_analytics({
      siteUrl, startDate, endDate,
      dimensions: ['page', 'query'],
      rowLimit: 5000,
    });
    sampledUrls = await selectUrlsFromGsc(gscData, {
      clientHostname, count: urlSampleCount, intelligence,
    });
  }

  // FALLBACK 1: Ahrefs site-explorer-top-pages
  if (!sampledUrls.length) {
    const ahrefsPages = await mcp.ahrefs.site_explorer_top_pages({
      target: siteUrl, country: countryCode, limit: urlSampleCount * 2,
    });
    sampledUrls = ahrefsPages.pages.slice(0, urlSampleCount).map((p) => ({
      url: p.url, intent: 'unknown', clicks_90d: 0, top_queries: [],
    }));
    degradation.url_sampling = { skip_reason: 'GSC not accessible', fallback_used: 'Ahrefs site-explorer-top-pages' };
  }

  // FALLBACK 2: sitemap.xml first N
  if (!sampledUrls.length) {
    const sitemapXml = await fetchSitemapXml(siteUrl);
    sampledUrls = parseSitemapUrls(sitemapXml).slice(0, urlSampleCount).map((u) => ({
      url: u, intent: 'unknown', clicks_90d: 0, top_queries: [],
    }));
    degradation.url_sampling = { skip_reason: 'GSC + Ahrefs both failed', fallback_used: 'sitemap.xml top N' };
  }

  // FALLBACK 3: ABORT with STOP gate
  if (!sampledUrls.length) {
    throw new Error('No URLs available — STOP gate al Lead: declarar URLs manualmente en intelligence/url-samples.md');
  }
}
```

### 1c. STOP GATE #1 — Lead approval URL sampling

**OBLIGATORIO**: presentar al Lead las URLs sampled con justificación per-URL. Lead aprueba/edita ANTES de seguir.

```
URL sampling propuesto para auditoría citabilidad ({N} URLs):

1. https://chedraui.com.mx/                                    HOME
   Top queries: chedraui ofertas, chedraui horarios, ...
   Intent dominante: 70% navigational + 30% transactional
   Clicks 90d: 1,120,500

2. https://chedraui.com.mx/c/abarrotes-y-despensa             TRANSACTIONAL
   ...

¿Confirmás estas {N}? ¿O querés agregar/quitar alguna?
```

Lead responde → ajustar `sampledUrls` → recién ahí seguir Phase 1d.

### 1d. Brand Radar bulk — 7 platforms × 3 endpoints

```js
const PLATFORMS_FULL = [
  { id: 'google_ai_overviews', label: 'Google AI Overviews', sov_supported: true },
  { id: 'google_ai_mode',      label: 'Google AI Mode',      sov_supported: false },
  { id: 'chatgpt',             label: 'ChatGPT',             sov_supported: true,  has_questions: true },
  { id: 'gemini',              label: 'Gemini',              sov_supported: true,  has_questions: true },
  { id: 'perplexity',          label: 'Perplexity',          sov_supported: true,  has_questions: true },
  { id: 'copilot',             label: 'Copilot',             sov_supported: true,  has_questions: true },
  { id: 'grok',                label: 'Grok',                sov_supported: true },
];
const platformsToFetch = (flags.platforms ? flags.platforms.split(',').map((id) => PLATFORMS_FULL.find((p) => p.id === id)).filter(Boolean) : PLATFORMS_FULL);

const brand = clientHostname.replace(/\..+$/, '');  // ex: 'chedraui'
const competitors = parseCompetitorsFromIntelligence(intelligence.competidores) || [];
const competitorsCsv = competitors.join(',');
const dateFrom = flags.brandRadarDateFrom || isoDaysAgo(30);
const dateTo   = flags.brandRadarDateTo   || isoDaysAgo(0);
const country  = inferCountryFromIndustry(industry, intelligence.perfil);  // 'mx', 'ar', 'cl', etc.

// 1d.1 mentions-overview — 7 calls (1 per platform)
const mentions = {};
for (const p of platformsToFetch) {
  try {
    const r = await mcp.ahrefs.brand_radar_mentions_overview({
      brand, competitors: competitorsCsv, country,
      data_source: p.id, date_from: dateFrom, date_to: dateTo,
      // Override wrapper select default to include `brand` field (caveat H1 smoke 2026-05-03)
      select: 'brand,only_target_brand,only_competitors_brands,target_and_competitors_brands,no_tracked_brands,total',
    });
    mentions[p.id] = r.metrics;
  } catch (e) {
    mentions[p.id] = { error: e.message };
  }
}

// 1d.2 sov-overview — 5 calls (skip google_ai_overviews + google_ai_mode per docs SoV restriction)
const sov = {};
for (const p of platformsToFetch.filter((pl) => pl.sov_supported && pl.id !== 'google_ai_overviews')) {
  try {
    const r = await mcp.ahrefs.brand_radar_sov_overview({
      brand, competitors: competitorsCsv, country,
      data_source: p.id, date_from: dateFrom, date_to: dateTo,
    });
    sov[p.id] = r.metrics;
  } catch (e) {
    sov[p.id] = { error: e.message };
  }
}

// 1d.3 cited-pages — 7 calls × limit=10, filter post-fetch by clientHostname
const citedPages = {};
for (const p of platformsToFetch) {
  try {
    const r = await mcp.ahrefs.brand_radar_cited_pages({
      brand, competitors: competitorsCsv, country,
      data_source: p.id, date_from: dateFrom, date_to: dateTo, limit: 10,
    });
    citedPages[p.id] = r.pages.map((row) => ({
      url: row.url, responses: row.responses, volume: row.volume,
      is_client: row.url.includes(clientHostname),
    }));
  } catch (e) {
    citedPages[p.id] = { error: e.message };
  }
}
```

**Process-and-discard pattern (Patrón 5)**: extraer fields necesarios inmediatamente, descartar raw responses (each ~500 bytes-2KB).

---

## Phase 2 — Queries shortlist (cascade)

### 2a. Build queries pool — cascade

```js
const queriesInternal = flags.queriesInternal || 20;
const queriesShortlist = flags.queriesShortlist || 7;

let candidatePool = [];

// SOURCE 1: intelligence/productos-foco.md — temas/keywords prioritarios
const focoKws = parseKeywordsFromIntelligence(intelligence['productos-foco']);
candidatePool.push(...focoKws.map((kw) => ({ query: kw, source: 'intelligence/productos-foco', weight: 3 })));

// SOURCE 2: intelligence/objetivos.md — KPIs estratégicos
const objKws = parseKeywordsFromIntelligence(intelligence.objetivos);
candidatePool.push(...objKws.map((kw) => ({ query: kw, source: 'intelligence/objetivos', weight: 3 })));

// SOURCE 3: intelligence/competidores.md — queries donde competidores ganan
const compKws = parseKeywordsFromIntelligence(intelligence.competidores);
candidatePool.push(...compKws.map((kw) => ({ query: kw, source: 'intelligence/competidores', weight: 2 })));

// SOURCE 4: GSC top queries filtered (NO branded, transactional/commercial/informational)
if (!degradation.gsc) {
  const gscQueries = await getTopQueriesFromGsc(siteUrl, brand, /*limit=*/100);
  const filteredGsc = filterQueriesByIntent(gscQueries, brand, ['transactional', 'commercial', 'informational']);
  candidatePool.push(...filteredGsc.slice(0, 30).map((q) => ({
    query: q.query, source: 'gsc-filtered', weight: 1,
    clicks_90d: q.clicks, intent: q.intent,
  })));
}

// SOURCE 5: Ahrefs top organic keywords (cross-validation, optional)
try {
  const ahrefsKws = await mcp.ahrefs.site_explorer_organic_keywords({
    target: siteUrl, country, limit: 30, order_by: 'sum_traffic desc',
  });
  const filteredAhrefs = ahrefsKws.keywords
    .filter((k) => !k.keyword.toLowerCase().includes(brand.toLowerCase()))
    .slice(0, 20);
  candidatePool.push(...filteredAhrefs.map((k) => ({
    query: k.keyword, source: 'ahrefs-organic', weight: 1,
    volume: k.volume, kd: k.keyword_difficulty,
  })));
} catch (e) {
  console.warn(`Ahrefs organic-keywords failed (non-blocking): ${e.message}`);
}

// Dedupe + score composite
const dedupedPool = dedupeQueries(candidatePool);  // group by query, sum weights
const scoredPool = dedupedPool.sort((a, b) => b.weight - a.weight).slice(0, queriesInternal);
```

### 2b. Intent classification per query (regex SEO 2026)

```js
const INTENT_PATTERNS = {
  transactional:           /\b(comprar|precio|barato|oferta|cerca de m[ií]|env[ií]o|promoci[óo]n|descuento|cotiz)\b/i,
  commercial_investigation: /\b(mejor|comparar|vs|review|opiniones|ranking|top \d+|recomendaci[óo]n)\b/i,
  informational:           /\b(qu[ée] es|c[óo]mo|gu[ií]a|tutorial|para qu[ée] sirve|cu[áa]ndo|por qu[ée])\b/i,
  navigational:            new RegExp(`\\b(${escapeRegex(brand)}|login|ayuda|tel[ée]fono|horarios)\\b`, 'i'),
};
function classifyIntent(query) {
  const matches = [];
  for (const [intent, pattern] of Object.entries(INTENT_PATTERNS)) {
    if (pattern.test(query)) matches.push(intent);
  }
  return matches.length ? matches : ['informational'];  // default fallback
}
scoredPool.forEach((q) => { q.intent = classifyIntent(q.query); });
```

### 2c. STOP GATE #2 — Lead shortlist final

**OBLIGATORIO**: presentar 15-25 candidatos con justificación per-query. Lead selecciona 7-10 finales.

```
Queries shortlist propuesto para análisis AI Overview (15-25 candidatos):

1. mejor super para despensa semanal méxico
   Source: intelligence/competidores + gsc-filtered (weight 3)
   Intent: commercial_investigation
   Volume: 4400 (Ahrefs)
   Justificación: cliente NO ranking pero competidores capturando

2. promociones supermercado hoy
   Source: gsc-filtered
   Intent: transactional
   Clicks 90d (cliente): 850
   ...

¿Cuáles 7-10 querés analizar? (decime los números separados por coma)
```

Lead responde → filtrar `scoredPool` a las queries seleccionadas → seguir Phase 3.

---

## Phase 3 — Per-query enrichment (subagent delegation)

### 3a. DataForSEO SERP × N queries (via subagent)

**LAUNCH subagent** (general-purpose) con prompt:

```
Llamá mcp__dataforseo__serp_organic_live_advanced para CADA una de estas {N} queries del cliente {slug}:

[lista de queries seleccionadas en Phase 2c]

Para CADA query, usá:
  language_code: '{language}'
  location_name: '{country_full_name}'
  depth: 20

Para CADA response extraé:
  - query (string)
  - ai_overview_present (boolean): true si items.find(t => t.type === 'ai_overview') existe
  - we_cited (boolean): true si aiOverview.references[].domain === '{clientHostname}'
  - competitors_in_aio (string[]): subset de competitors[] presentes en aiOverview.references[].domain
  - paa_count (integer): items.filter(t => t.type === 'people_also_ask').length
  - related_searches (string[]): items.find(t => t.type === 'related_searches')?.items?.slice(0,5)
  - aio_references_count (integer): aiOverview?.references?.length || 0

PERSISTÍ el array completo a `report-builder/output/proof-{slug}-serp-aio.json` (o `report-builder/samples/output/serp-aio.json` en --sample mode).

RETORNAR solo: confirmación + bytes escritos + 1-line summary (X/N queries con AIO present, Y/N con we_cited).

NO leer responses raw en tu contexto — process-and-discard inmediato.
```

El subagent procesa ~25 SERP responses (~1.25MB raw) y retorna ~500 chars.

### 3b. Brand Radar ai-responses × 4 platforms (via subagent)

**LAUNCH subagent** (general-purpose) con prompt:

```
Llamá ahrefs-mcp `brand-radar-ai-responses` para CADA una de estas 4 platforms (chatgpt, gemini, perplexity, copilot):

Args:
  brand: '{brand}'
  competitors: '{competitorsCsv}'
  country: '{country}'
  data_source: <platform>
  date_from: '{dateFrom}'
  date_to: '{dateTo}'
  limit: 20
  select: 'question,response,links,volume'

IMPORTANTE — drift docs vs API (validado smoke 2026-05-03):
  Las cols disponibles reales son: search_queries, links, volume, data_source, tags, question, response, country.
  NO usar 'cited_url_exact' (docs lo lista pero API rejected — empirical).

Para CADA platform aggregar:
  - questions_total (integer): rows.length
  - brand_mentioned_count (integer): count rows donde response.toLowerCase().includes('{brand}')
  - urls_cited_from_client (Array<{question, url, volume}>): rows where links[].url contains '{clientHostname}'
  - top_questions (Array<{question, volume, brand_mentioned, links_count}>): top 5 by volume
  - competitors_cited_count (object): per-competitor mention count

PERSISTÍ el aggregate completo a `report-builder/output/proof-{slug}-ai-responses.json` (o sample equivalent).

RETORNAR solo: per-platform 1-line summary (questions_total, brand_mentioned_pct, urls_cited count) + bytes escritos.

NO leer responses raw en tu contexto.
```

El subagent procesa ~80 ai-responses rows (~1MB+ raw) y retorna ~1KB JSON aggregate.

### 3c. Read subagent outputs

```js
const serpAioPath = sampleMode
  ? 'report-builder/samples/output/serp-aio.json'
  : `report-builder/output/proof-${slug}-serp-aio.json`;
const aiResponsesPath = sampleMode
  ? 'report-builder/samples/output/ai-responses.json'
  : `report-builder/output/proof-${slug}-ai-responses.json`;

const serpAioData     = JSON.parse(fs.readFileSync(serpAioPath, 'utf8'));
const aiResponsesData = JSON.parse(fs.readFileSync(aiResponsesPath, 'utf8'));
```

---

## Phase 4 — Citability heurística multi-page

### 4a. Industry-specific factor weights (8 canonical factors, all clients)

```js
const CITABILITY_FACTORS_CANONICAL = [
  { id: 'schema',        factor: 'Datos estructurados (Schema.org)' },
  { id: 'direct_answer', factor: 'Formato de respuesta directa' },
  { id: 'eeat',          factor: 'Autoridad temática (E-E-A-T)' },
  { id: 'freshness',     factor: 'Frescura y actualización' },
  { id: 'headings',      factor: 'Estructura semántica (headings)' },
  { id: 'stats',         factor: 'Contenido estadístico y cifras' },
  { id: 'faq',           factor: 'Cobertura FAQ exhaustiva' },
  { id: 'topic_authority', factor: 'Interconexión temática (Topic Authority)' },
];
```

### 4b. WebFetch multi-URL heurísticas (via subagent)

**LAUNCH subagent** (general-purpose) con prompt:

```
Para CADA una de estas {N} URLs sampleadas del cliente {slug}:

[lista de sampledUrls aprobadas en Phase 1c]

Llamá WebFetch con prompt extraction structurado:
  - schemas_detected: lista de @type values found in JSON-LD
  - schemas_count: integer
  - has_dateModified: boolean (schema dateModified OR "Última actualización" visible)
  - has_byline: boolean (author byline + Author schema)
  - h1_count, h2_count, h3_count: integers
  - has_tldr: boolean (1er párrafo <100 palabras + answer-format)
  - has_faq: boolean (FAQPage schema OR detectable FAQ section)
  - internal_links_count: integer
  - cifras_count: count of numbers/stats in main content (regex ~10+ digit groups)

Aggregate per-factor (avg across URLs, scored 1-10):
  - schema:        0 schemas across N URLs = 1/10. 5+ unique types = 8/10. Linear scale.
  - direct_answer: % URLs with TL;DR. 0%=1/10, 100%=10/10.
  - eeat:          % URLs with byline. 0%=2/10 (brand baseline), 100%=10/10.
  - freshness:     % URLs with dateModified. 0%=1/10, 100%=9/10.
  - headings:      % URLs with H1 + structured H2/H3 hierarchy. 0%=1/10, 100%=8/10.
  - stats:         avg cifras_count per URL. 0=2/10, 10+=8/10.
  - faq:           % URLs with FAQ schema or detectable FAQ section. 0%=1/10, 100%=10/10.
  - topic_authority: avg internal_links_count. <20=2/10, 50+=6/10, 100+=8/10.

Per-factor "current" string: descripción concisa de findings (ej: "0/12 URLs con FAQPage schema; bloque FAQ no detectado en home ni categorías").
Per-factor "recommendation" string: acción concreta basada en findings.

PERSISTÍ el aggregate completo a `report-builder/output/proof-{slug}-citability.json`.

RETORNAR solo: per-factor 1-line summary (factor, avg score) + total avg + bytes escritos.

NO leer raw HTML responses en tu contexto.
```

### 4c. Read citability subagent output + compute aggregate score

```js
const citabilityPath = sampleMode
  ? 'report-builder/samples/output/citability.json'
  : `report-builder/output/proof-${slug}-citability.json`;
const citabilityRaw = JSON.parse(fs.readFileSync(citabilityPath, 'utf8'));

const draftFactors = CITABILITY_FACTORS_CANONICAL.map((f) => ({
  factor: f.factor,
  current: citabilityRaw[f.id]?.current || 'Sin datos.',
  score: citabilityRaw[f.id]?.score || 1,
  recommendation: citabilityRaw[f.id]?.recommendation || 'Revisar manualmente.',
}));
const draftScore = Number((draftFactors.reduce((a, f) => a + f.score, 0) / draftFactors.length).toFixed(1));
```

### 4d. STOP GATE #3 — Lead approval citability scores

**OBLIGATORIO**: presentar los 8 draft scores con justificación. Lead confirma o edita.

```
Citability scores propuestos (auditoría heurística sobre {N} URLs):

1. Datos estructurados (Schema.org):       2/10
   Current: 0 schemas detected across 12 URLs (home + categorías + fichas + ayuda + brand)
   Recommendation: Implementar FAQPage en top 30 categorías, Recipe schema en sección recetas, HowTo en guías

2. Formato de respuesta directa:           1/10
   ...

Score promedio: 2.5/10

¿Confirmás o ajustás alguno? (decime "ok" o "ajustar factor X a score Y")
```

Lead responde → ajustar `factors` + recompute `score` → seguir Phase 5.

---

## Phase 5 — Cross-section synthesis (Roadmap + KPIs)

### 5a. Build platforms from Brand Radar aggregates

```js
const platforms = platformsToFetch.map((p) => {
  const m = mentions[p.id];
  const s = sov[p.id];
  const ai = aiResponsesData?.[p.id];
  return synthesizePlatformRow({
    platform: p, mentions: m, sov: s, aiResponses: ai,
    citedPages: citedPages[p.id], brand, clientHostname,
  });
});
```

### 5b. Build queries_with_ai (top N from shortlist)

```js
const queriesShortlistRows = serpAioData.queries.slice(0, queriesShortlist).map((q) => {
  const aioStatus = q.ai_overview_present ? 'optimal' : (q.paa_count > 0 ? 'warning' : 'critical');
  const weCitedStatus = q.we_cited ? 'optimal' : (q.competitors_in_aio.length > 0 ? 'critical' : 'warning');
  return {
    query: q.query,
    volume: q.volume || 0,
    ai_overview: aioStatus,
    we_cited: weCitedStatus,
    competitors: q.competitors_in_aio.slice(0, 4).join(', ') || '—',
    action: synthesizeAction({ query: q, aioStatus, weCitedStatus }),
  };
});
```

### 5c. Build geo_roadmap (3 fases) — cross-section synthesis

```js
const roadmapBoilerplatePerIndustry = {
  retail_supermercado: {
    phase1_actions: [
      'Implementar FAQPage schema en top 30 categorías ecommerce',
      'Agregar Product + Offer + Brand schema con dateModified en fichas',
      'Crear template de "respuesta directa" para equipo de contenido',
      'Auditar y corregir heading structure en top 30 categorías',
    ],
    phase2_actions: [
      'Workshop GEO #1 con equipo de contenido del cliente',
      'Crear/optimizar 15 categorías con checklist AEO completo',
      'Desarrollar 3 pillar pages (definir clusters según intelligence/productos-foco)',
      'Agregar bloques FAQ a 50 categorías existentes',
    ],
    phase3_actions: [
      'Workshop GEO #2: revisión de resultados y ajustes',
      'Implementar monitoreo automatizado de citaciones IA (Brand Radar)',
      'Expandir checklist AEO a todo contenido nuevo',
      'Producir reportes propios: índices de precios, ranking categorías',
      'Crear glosario retail/abarrotes como recurso citable',
    ],
  },
  // ... otros industries
  default: { /* generic boilerplate */ },
};

const geo_roadmap = buildRoadmap({
  industry, contextLevel, priorSlices, intelligence,
  draftFactors, queriesShortlistRows, citedPages,
  boilerplate: roadmapBoilerplatePerIndustry[industry] || roadmapBoilerplatePerIndustry.default,
});

if (contextLevel === 'LOW') {
  degradation.cross_section = {
    skip_reason: 'no prior slices found in clients/{slug}/sections/',
    fallback_used: 'boilerplate genérico per-industry — sin synthesis cross-section',
  };
}
```

**Cross-section synthesis rules**:
- HIGH: Phase 1 actions absorben tech-audit issues críticos (schema markup gaps, H1 missing, etc.). Phase 2 absorbe foda oportunidades AI-related. Phase 3 timing alineado con history estacionalidad si disponible.
- MEDIUM: synthesis solo desde slices disponibles. Resto = boilerplate per-industry.
- LOW: 100% boilerplate per-industry + flag degradation visible al Lead.

### 5d. Build kpis (6 canonical PR KPIs)

```js
const kpis = [
  {
    name: 'Citaciones en AI Overviews',
    baseline: deriveBaseline_AIOcitations({ queriesShortlistRows }),  // ej "~0 (solo branded)"
    target_3m: '5-10 queries', target_6m: '20+ queries',
    tool: 'GSC + monitoreo manual',
  },
  {
    name: `Menciones en ChatGPT/${platforms[2]?.name || 'GPT Search'}`,
    baseline: deriveBaseline_chatgpt({ aiResponsesData, brand }),
    target_3m: '10+ queries', target_6m: '25+ queries',
    tool: 'Ahrefs Brand Radar / manual',
  },
  {
    name: 'Citaciones en Perplexity con enlace',
    baseline: deriveBaseline_perplexity({ aiResponsesData, brand, clientHostname }),
    target_3m: '5+ queries', target_6m: '15+ queries',
    tool: 'Monitoreo manual / API',
  },
  {
    name: 'Score de citabilidad (auditoría interna)',
    baseline: `${draftScore}/10`,
    target_3m: '5/10', target_6m: '7/10',
    tool: 'Auditoría trimestral interna',
  },
  {
    name: 'Categorías con checklist AEO completo',
    baseline: '0',
    target_3m: '30 categorías', target_6m: '60+ categorías',
    tool: 'Tracking interno',
  },
  {
    name: 'Schema FAQPage implementado',
    baseline: deriveBaseline_FAQpages({ draftFactors }),  // ej "0 páginas"
    target_3m: '30 páginas', target_6m: '80+ páginas',
    tool: 'Schema validator + GSC',
  },
];
```

---

## Phase 6 — Build slice via extractor + Schema validation + Persist

```js
const slice = extractAiAuditSlice({
  sources: {
    meta: { client_slug: slug, site_url: siteUrl, industry, audit_date: new Date().toISOString().slice(0, 10) },
    platforms,                   // synthesized rows from Phase 5a
    citability: {                // approved by Lead in Phase 4d
      score: draftScore,
      factors: draftFactors,
    },
    queries_with_ai: queriesShortlistRows,  // top N from Phase 5b
    geo_roadmap,                 // synthesized in Phase 5c
    kpis,                        // synthesized in Phase 5d
    degradation,                 // per-source flags
  },
});

const { valid, errors } = validateAiAuditSlice(slice);
if (!valid) {
  throw new Error(`AI audit slice validation failed:\n  - ${errors.join('\n  - ')}`);
}

fs.mkdirSync(path.dirname(slicePath), { recursive: true });
fs.writeFileSync(slicePath, JSON.stringify(slice, null, 2));
```

---

## Phase 7 — Engram save graceful + Output al Lead

**Engram save**:
```js
try {
  await mem_save({
    title: `AI audit slice ${slug}`,
    type: 'decision',
    topic_key: `sections/ai-audit/${slug}`,
    scope: 'project',
    content: `audit_date=${slice.ai_visibility.audit_date}, citability_score=${slice.ai_visibility.citability.score}, platforms=${slice.ai_visibility.platforms.length}, queries=${slice.ai_visibility.queries_with_ai.length}, context_level=${contextLevel}, degradation=${Object.keys(slice.ai_visibility.degradation || {}).join(',') || 'none'}, generated_at=${new Date().toISOString()}`,
  });
} catch (e) {
  console.warn(`Engram save failed (non-blocking): ${e.message}`);
}
```

**Output al Lead** (aplica para los 4 modes):

```
AI Visibility slice generado para {cliente}:
Mode: {sample | sample-cached | real | real-cached}
Cross-section context: {HIGH | MEDIUM | LOW} ({N} prior slices: {tech-audit, history, foda})

🤖 Plataformas IA ({N} cubiertas via Brand Radar):
  Top SoV cliente:        {sov_top.platform} {sov_top.pct}%
  Worst presence:         {worst.platform} (status: {worst.status})

📊 Citabilidad:
  Score:                  {citability.score} / 10
  Critical factors (≤2):  {N} de 8
  Top recommendation:     {top_factor.recommendation}

🔎 Queries con AI Overview ({N} analyzed, top {N_shortlist} en template):
  AIO present:            {aio_count} / {N}
  We cited:               {cited_count} / {N}
  Competitors in AIO:     {competitors_in_aio_count} / {N}

📋 Roadmap GEO 3 fases:
  Cross-section enriched: {true | false}
  Total actions:          {action_count}

🎯 KPIs (6 canonical):
  Baseline citability:    {citability.score}/10
  Baseline AIO citations: {aio_baseline}

⚠️ Degradation:           {none | gsc:fallback | cross_section:LOW boilerplate | ...}

Slice persistido: {slicePath} ({size} KB)
{Engram save: OK / FAILED — graceful}

{If contextLevel === 'LOW':}
SUGERENCIA: Para roadmap+KPIs más ricos, corré /seo-section-tech-audit, /seo-section-history y /seo-section-foda primero, después re-run /seo-section-ai-audit. El cross-section synthesis va a inyectar issues técnicos detectados + trends + oportunidades FODA en el roadmap.

Próximo: /seo-build-report consume este slice + slices de otras secciones para componer consolidated_json final.
```

---

## MCPs utilizados

| MCP / Tool | Phase | Uso |
|------------|-------|-----|
| `memory-mcp.get-client-summary` | 0.4 | metadata + industry |
| `gsc-mcp.list_sites` | 0.4 | check siteUrl accesible + OAuth swap detection |
| `gsc-mcp.search_analytics` (page+query 90d) | 1b | **PRIMARY URL sampling** + queries pool |
| `gsc-mcp.gsc_reauth` | 0.4 | auto-reauth + OAuth swap |
| `ahrefs-mcp.brand-radar-mentions-overview` | 1d.1 | 7 calls × 50u = 350u — mentions distribution per platform |
| `ahrefs-mcp.brand-radar-sov-overview` | 1d.2 | 5 calls × 50u = 250u — SoV per platform |
| `ahrefs-mcp.brand-radar-cited-pages` | 1d.3 | 7 calls × 100u = 700u — top URLs cited cross-platform |
| `ahrefs-mcp.brand-radar-ai-responses` | 3b (subagent) | 4 calls × ~600u = ~2400u — chatgpt-style questions per platform |
| `ahrefs-mcp.site-explorer-organic-keywords` | 2a | optional — top organic for queries pool augment |
| `ahrefs-mcp.site-explorer-top-pages` | 1b fallback | si GSC degraded |
| `mcp__dataforseo__serp_organic_live_advanced` | 3a (subagent) | $0.001 × N queries = $0.015-$0.025 — AI Overview detection |
| `WebFetch` | 4b (subagent) | $0 × N URLs — citability heurísticas multi-page |
| Subagent #1 (DataForSEO SERP processor) | 3a | process N SERP responses → 500-byte/query aggregate |
| Subagent #2 (Brand Radar ai-responses processor) | 3b | process 4 platforms × 20 rows → 1KB JSON aggregate |
| Subagent #3 (WebFetch citability processor) | 4b | process N URL responses → 800-byte aggregate |

**NO usar directamente**: `diagnostic-mcp.start-diagnostic` — esta skill es modular (decisión arquitectural Phase 8 2026-05-02).

---

## Tests

`report-builder/test/seo-section-ai-audit.test.js` — strict acceptance tests (validator + extractor sample mode + extractor production + edge cases).

```bash
cd report-builder && node --test test/seo-section-ai-audit.test.js
```

---

## Costos estimados (run productivo)

| Source | Cost | Notes |
|--------|------|-------|
| Ahrefs brand-radar (mentions+sov+cited+ai-responses, 7 platforms) | ~3,700 units | ~0.18% del quota mensual Enterprise 2M |
| DataForSEO SERP (15-25 queries) | ~$0.025 | live_advanced ~$0.001/call |
| GSC search_analytics + list_sites | $0 | free quota |
| WebFetch (8-12 URLs) | $0 | built-in |
| memory-mcp | $0 | backend internal |
| Subagents (×3) | tokens | ~80K tokens budget total |

**Total**: ~$0.50 USD por skill run productivo + 3,700 Ahrefs units. Para 10 clientes/mes = ~37K units = 1.85% quota.

---

## Diferencias vs `/seo-diagnostico` (legacy parcial)

| Aspecto | `/seo-diagnostico` cluster ai_visibility | `/seo-section-ai-audit` (Phase 8) |
|---------|------------------------------------------|-----------------------------------|
| Platform coverage | 1-3 platforms estimadas | **7 platforms** Brand Radar full coverage |
| Citability | Hardcoded boilerplate | **Heurística multi-page** + STOP gate Lead |
| URL sampling | Solo home | **GSC + intent classification** + Lead approval |
| Queries with AI | Top branded fixed | **Cascade intelligence + GSC filtered** + STOP gate Lead |
| AI Overview detection | NO | **DataForSEO SERP per query** |
| Cross-platform AI responses | NO | **Brand Radar ai-responses 4 platforms** |
| Cross-section synthesis | NO | **3 levels HIGH/MEDIUM/LOW** based on prior slices |
| Roadmap/KPIs | Generic boilerplate | **Cross-section enriched** when context HIGH |
| Schema validation | Soft | **Strict** via `validateAiAuditSlice` pre-persist |
| Output target | consolidated_json via diagnostic-mcp | Disk JSON + engram opcional |
| Architecture | Backend orchestrator | **Modular** — MCPs directos + 3 subagents |
| Cache | No | `--from-cache` flag |
| Sample mode | No | `--sample` flag |
| Auto-reauth | No | Yes (GSC, OAuth multi-cuenta swap) |

---

## References

- `report-builder/lib/ai-audit-validator.js` — schema enforcement (cero deps)
- `report-builder/lib/ai-audit-extractor.js` — single boundary fix, normaliza outputs + sample-mode shortcut
- `skills/seo-section-ai-audit/schema.json` — JSON Schema authoritative
- `report-builder/sections/C-diagnostico-seo/14-visibilidad-ia/template.njk` — Nunjucks template Phase 3.3 que consume este slice
- `report-builder/samples/sections/ai-audit.json` — sample slice persistido (--sample mode output)
- `templates/intelligence/url-samples.md` — opcional override per-cliente para forzar URL sampling
- `docs/superpowers/specs/2026-05-03-ai-audit-mcp-smoke-report.md` — smoke report empírico de los 8 sources
- Engram: obs #586 (Nubank fidelity strict), #592 (Phase 8 methodology), #594 (modular arch), #607 (smoke ai-audit)
