---
name: seo-diagnostico-full
description: Master skill orchestrator. Use when the Lead invokes "/seo-diagnostico-full {slug}" to produce a full Nubank-fidelity diagnóstico HTML for a client. Automates Phase 8 pipeline (8 skills + auto-setup + render) in 1 command, ~2hs wall time. See spec at docs/superpowers/specs/2026-05-04-diagnostico-full-skill-design.md (D1-D14). Coexiste con legacy /seo-diagnostico (6-cluster pipeline). Triggers on "/seo-diagnostico-full", "diagnóstico completo", "full diagnostic for {client}".
model: opus
---

<execution-protocol>
MODO: EJECUCION DIRECTA — NO PLANIFICACION

Este skill es el MASTER ORCHESTRATOR del pipeline Phase 8 completo.
1 input (slug) → 1 output (HTML Nubank-fidelity). ~2hs 18min wall time.

PROHIBIDO ABSOLUTO:
- Mantener slices en el contexto del orquestador (D8) (D10): cada slice es un
  archivo en disco. El orquestador NUNCA lee ni retiene el contenido del slice.
  Solo lee el resultado compacto (~250 tokens) del subagente (status, slice_path,
  cost_units, duration_ms, degradation_count, degradation_summary).
  (D10 — model: Opus 4.7 1M context. Justificacion: calidad Swiss-watch del Lead, ~$2/run.)
- Saltar Phase 0.5 gap scan o Phase 0.6 questionnaire al Lead. Aun si el repo
  cliente ya existe y parece completo — siempre detectar gaps y mostrar inventario.
- Arrancar Phase 3 subagentes antes de que Phase 2 haya retornado `diagnostic_id`.
- Procesar mas de 1 cliente por sesion. Lock por slug (D8) — si el Lead pide
  un segundo slug en la misma sesion, STOP y decirle que abra otra sesion.
- Inventar respuestas al cuestionario. Si el Lead no responde una HARD gate,
  re-preguntar ese punto solo. NUNCA asumir valores por defecto para HARD gates.
- Escribir archivos de plan o describir lo que "harias" sin ejecutar.
- Saltar fases o colapsar multiples fases en una respuesta.
- Auto-aprobar checkpoints (son del Lead).

OBLIGATORIO:
- Toda skill invocada = subagente (Agent tool con buildSubagentPrompt). El
  orquestador NUNCA ejecuta las skills directamente — siempre delega.
- Phase 0 inline + helpers de auto-setup.js via Bash.
- Polling = D14 hibrido: esperar notificaciones de subagentes Phase 3 primero,
  luego single Bash blocking poll del crawl.
- releaseLock(slug) en finally — SIEMPRE, incluso en error fatal.
- Validar HARD gates (Phase 0.5-0.6) antes de Phase 2 (crawl kickoff). Si faltan HARD gates y
  Lead no responde, ABORT con mensaje de costo $0.
- Persistir progress journal despues de cada fase via writeProgressJournal().
- Operador = userEmail prefix (ej: nico.m@puntorojo.com → "Nico").

Protocolo: shared/skill-execution-protocol.md
Context engineering: shared/context-engineering.md (Patrones 1, 2, 4)
Decisiones design D1-D14: docs/superpowers/specs/2026-05-04-diagnostico-full-skill-design.md
</execution-protocol>

# /seo-diagnostico-full — Master Skill Orchestrator

## Objetivo

Producir un diagnóstico SEO completo Nubank-fidelity para un cliente en **1 comando**.

```
Input:  /seo-diagnostico-full {slug} [flags]
Output: ~/Documents/punto-rojo-clients/{slug}/output/{slug}-diagnostico-{period}.html
```

**Wall time estimado**: ~2hs 18min (Phase 0 ~2min + Phase 2 ~5s kickoff +
Phase 3 ~15min paralelo + Phase 4 ~1h 45min crawl + Phase 5 ~10s + Phase 6 ~100s + Phase 7 ~200ms).
(Reorder 2026-05-05: Phase 1 context se movió a Phase 6b — ahora se sintetiza DESPUÉS
de tech-audit/history/ai-audit/competitive/benchmarks así puede leer todas esas slices en
vez de degradar graceful por falta de cross-section data en run from-scratch.)

**Costo estimado**: ~$2 USD Opus orchestrator + ~30K Ahrefs units (~1.5% quota mensual Enterprise).
Cost tracking populate deferido a v2 (D7) — hoy los campos `ahrefs_units` y `estimated_usd`
del run-summary quedan en null hasta que `get_subscription_info` esté disponible en ahrefs-mcp.

**Coexistencia**: este skill NO reemplaza `/seo-diagnostico` (pipeline 6 clusters legacy).
Ambos conviven. Este skill usa las 8 skills Phase 8 modulares + `/seo-build-report`.
(D9 — naming `/seo-diagnostico-full` coexiste con legacy `/seo-diagnostico` de 6-cluster pipeline; prefix `seo-` consistente con el resto del toolkit.)

---

## Inputs

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| `slug` | string (required) | — | kebab-case del cliente (ej: `volaris`). Regex `/^[a-z0-9][a-z0-9-]*$/` |
| `period` | string (optional) | mes actual YYYY-MM | Periodo del reporte. Regex `/^\d{4}-\d{2}$/` |
| `country` | string (optional) | auto-detect Client Hub | ISO 3166-1 alpha-2 lowercase (ej: `mx`). Override del valor en Client Hub |
| `--force` | flag | false | Re-corre todas las skills ignorando slices existentes (D6) |
| `--force-skill={names}` | flag | — | Re-corre skills especificas (comma-separated). Ej: `--force-skill=competitive,ai-audit` |
| `--resume` | flag | false | Retoma desde ultimo progress journal — salta phases con `status:'done'` (D11) |
| `--no-render` | flag | false | Salta render HTML (D5 opt-out). Solo compone assembled.json |
| `--no-open` | flag | false | No auto-abre browser al finalizar (D5 opt-out) |
| `--period={YYYY-MM}` | flag | — | Alternativa a parametro posicional |

**Invocacion tipica**:
```
/seo-diagnostico-full volaris
/seo-diagnostico-full volaris --force
/seo-diagnostico-full volaris --resume
/seo-diagnostico-full volaris --force-skill=competitive --period=2026-05
/seo-diagnostico-full volaris --no-render
```

---

## Phase 0 — Auto-setup

**Duracion estimada**: ~2 min. **Bloqueante para Phase 2 (crawl kickoff)**: sí.

Phase 0 corre inline con helpers de `report-builder/lib/auto-setup.js` via Bash.
NO requiere subagente — el overhead de spawning no vale para operaciones sync de filesystem.

> **Definicion de path base**: todas las operaciones de Phase 0 usan:
> ```js
> const CLIENT_DIR = path.join(os.homedir(), 'Documents', 'punto-rojo-clients', slug);
> ```
> Los Bash blocks referencian `${CLIENT_DIR}` para paths de archivos del cliente.

### Phase 0.0 — Lock acquisition (D8)

```js
const { acquireLock, releaseLock } = require('./report-builder/lib/auto-setup');

try {
  acquireLock(slug);
  // continuar con Phase 0.1+
} catch (err) {
  // Lock activo (otra sesion corriendo este slug)
  console.error(`❌ Lock activo para ${slug}: ${err.message}`);
  console.error('Abrí otra sesión de Claude si querés correr un cliente diferente.');
  process.exit(1);
}
```

Lock = `.diagnostico-lock-{slug}.json` con TTL 180 min (D8). Stale lock (>180min o corrupt)
se sobrescribe con warning. Lock cross-slug NO — Lead puede correr 2 clientes distintos
en sesiones separadas.

**Bash**:
```bash
node -e "
const { acquireLock } = require('./report-builder/lib/auto-setup');
try {
  const p = acquireLock('${slug}');
  console.log('LOCK_OK:' + p);
} catch (e) {
  console.error('LOCK_FAIL:' + e.message);
  process.exit(1);
}
"
```

Si `LOCK_FAIL` → ABORT. Mostrar mensaje de costo $0. NO continuar.

### Phase 0.0.5 — Backend seed pre-flight (Bug B1 fix v3.37.2)

**Antes** de tocar filesystem o Client Hub, verificar que el slug está seedeado en
el crawl-api backend. Sin esto, Phase 2 falla con `client_not_seeded:<slug>` y
se pierden 15-20 min de bootstrap (Bug B1, post-prosegur-ar empirical).

```js
const { checkClientSeeded, seedClientBackend } = require('./report-builder/lib/auto-setup');

const status = await checkClientSeeded(slug);

if (!status.exists) {
  // Slug no registrado en backend — pero todavía no tenemos hub para seedear.
  // Pull el hub primero (Phase 0.2 anticipada), después seedear.
  const hub = await pullClientHub(slug);
  if (!hub) throw new Error(`Client Hub missing for ${slug} — create the ClickUp doc first`);
  await seedClientBackend(slug, hub);
  console.log(`✅ Backend seedeado (action=created) — Phase 0.0.5 OK`);
} else {
  // Slug ya seedeado → opcional: refresh con hub fresco si Lead pasa --refresh-seed.
  console.log(`✅ Backend ya seedeado (action=skipped) — Phase 0.0.5 OK`);
}
```

**Bash**:
```bash
node -e "
const { checkClientSeeded, seedClientBackend, pullClientHub } = require('./report-builder/lib/auto-setup');
(async () => {
  const status = await checkClientSeeded('${slug}');
  if (!status.exists) {
    const hub = await pullClientHub('${slug}');
    if (!hub) { console.error('SEED_FAIL: client-hub missing'); process.exit(1); }
    const r = await seedClientBackend('${slug}', hub);
    console.log('SEED_OK:created:' + r.client.slug);
  } else {
    console.log('SEED_OK:exists:' + status.slug);
  }
})().catch(e => { console.error('SEED_FAIL:' + e.message); process.exit(1); });
"
```

Requiere env vars `CRAWL_API_BASE_URL` (default `https://sf.puntorojo.com`) +
`CRAWL_API_KEY` (Bearer auth). Ya están seteados si `memory-mcp` funciona.

Si `SEED_FAIL: CRAWL_API_KEY` → ABORT con mensaje claro al Lead.
Si `SEED_FAIL: client-hub missing` → ABORT pidiendo crear el ClickUp doc.

### Phase 0.1 — Repo structure

```js
const { ensureRepoStructure } = require('./report-builder/lib/auto-setup');
ensureRepoStructure(slug);
// Crea (o verifica) intelligence/ sections/ cache/ output/ en ~/Documents/punto-rojo-clients/{slug}/
```

**Bash**:
```bash
node -e "
const { ensureRepoStructure } = require('./report-builder/lib/auto-setup');
ensureRepoStructure('${slug}');
console.log('REPO_OK');
"
```

Idempotente — no falla si los directorios ya existen (D1, repos pre-existentes).

### Phase 0.2 — Pull Client Hub

```js
const { pullClientHub } = require('./report-builder/lib/auto-setup');
const hub = await pullClientHub(slug, { ttlDays: 7 });
// Wrapper sobre client-hub-loader.js existente (skill 7/8 production-proven)
// Cache TTL 7d: si cache/client-hub.json tiene <7 dias, NO llama ClickUp MCP
// Si cache expired o ausente: llama ClickUp MCP y guarda en cache/client-hub.json
```

`hub` es el JSON del Client Hub con campos: `brief.{voice, audience, content_pillars,
business_objectives, marketing_objectives, kpis, competitors[], products_focus[],
audience.interests[]}`, `client_info.{stage, scope, contract, nps_surveys, documents,
ga4_property_id, gsc_property_url, country_code}`.

**Cuando el cache se renueva** (cache miss o expired), el orquestador hace `clickup_search`
+ `clickup_get_document_pages` para leer el doc "Brief" del Client Hub y transforma
el texto en JSON estructurado. Campos canónicos a extraer del doc:

| Campo Brief (texto humano)          | JSON path                                    |
|-------------------------------------|----------------------------------------------|
| Site URL / Sitio web                | `brief.general_info.site_url`                |
| GA4 property ID                     | `brief.technical.ga4_property_id`            |
| GSC property URL                    | `brief.technical.gsc_property_url`           |
| **Cuenta Google Search Console:**   | **`brief.technical.google_oauth_account`** *(B4 fix v3.37.2)* |
| Country / País principal            | `brief.general_info.country_code`            |
| Industry / Industria                | `brief.general_info.industry`                |

> **Bug B4 (v3.37.2)**: el field "Cuenta Google Search Console:" tiene valores
> `accesos@puntorojo.com` o `accesos2@puntorojo.com` (engram obs #604, topic
> `infra/oauth-accounts`). Mapearlo SIEMPRE como `brief.technical.google_oauth_account`
> para que `generateClienteClaudeMd` emita las líneas con el hint `(Accesos)` /
> `(Accesos2)` en `## Setup técnico` y skills GSC/GA4 sepan qué OAuth token usar.
> Sin esto, reauth swaps disparan mid-run y rompen el pipeline.

**Bash**:
```bash
node -e "
const { pullClientHub } = require('./report-builder/lib/auto-setup');
pullClientHub('${slug}').then(hub => {
  console.log('HUB_OK:' + JSON.stringify({
    client_name: hub.client_info?.name ?? hub.brief?.general_info?.client_name ?? '${slug}',
    country_code: hub.client_info?.country_code ?? null,
    competitors_count: hub.brief?.competitors?.length ?? 0
  }));
}).catch(e => {
  console.error('HUB_FAIL:' + e.message);
  process.exit(1);
});
"
```

Si `HUB_FAIL` → ABORT (Client Hub es prerequisito para intelligence files y gap detection).
Mostrar instruccion: crear el doc en ClickUp + re-correr.

### Phase 0.3 — Generate intelligence files (D1)

Loop de 6 mappers via `generateIntelligenceFile`:

```js
const { generateIntelligenceFile } = require('./report-builder/lib/intelligence-generator');

const INTELLIGENCE_FILES = [
  'perfil.md',
  'objetivos.md',
  'competidores.md',
  'estacionalidad.md',
  'productos-foco.md',
  'contexto-historico.md'
];

for (const fileName of INTELLIGENCE_FILES) {
  await generateIntelligenceFile(slug, fileName, hub);
}
```

**Merge inteligente (D1)**: cada archivo tiene 2 zonas delimitadas por HTML comments:
- `<!-- BEGIN client-hub:auto -->` ... `<!-- END client-hub:auto -->` → OVERWRITE con data fresca Client Hub
- `<!-- BEGIN team-learnings:preserve -->` ... `<!-- END team-learnings:preserve -->` → PRESERVAR siempre

Si el archivo no existe → generado desde 0 con ambas secciones.
Si el archivo existe sin markers (legacy migration) → backup → regenerar.

**Bash** (loop secuencial — safer con merge-sections que re-lee archivos entre iteraciones):
```bash
node -e "
const path = require('path');
const os = require('os');
const { generateIntelligenceFile } = require('./report-builder/lib/intelligence-generator');
const CLIENT_DIR = path.join(os.homedir(), 'Documents', 'punto-rojo-clients', '${slug}');
const hub = require(CLIENT_DIR + '/cache/client-hub.json');
const files = ['perfil.md','objetivos.md','competidores.md','estacionalidad.md','productos-foco.md','contexto-historico.md'];
(async () => {
  for (const f of files) {
    await generateIntelligenceFile('${slug}', f, hub);
  }
  console.log('INTEL_OK');
})().catch(e => { console.error('INTEL_FAIL:' + e.message); process.exit(1); });
"
```

### Phase 0.4 — Generate CLAUDE.md (B3 fix v3.37.2)

```js
const { generateClienteClaudeMd } = require('./report-builder/lib/auto-setup');
generateClienteClaudeMd(slug, hub);
// Escribe a ~/Documents/punto-rojo-clients/{slug}/CLAUDE.md (sin prefix `cliente`,
// sin espacio — convención del proyecto, alineada con chubb/, chedraui/, banco-falabella/).
// Render template con brief.general_info + {{ASK_LEAD}} markers para campos missing.
// Si CLAUDE.md ya existe → merge (preserva ediciones manuales del equipo).
```

**Bash**:
```bash
node -e "
const { generateClienteClaudeMd } = require('./report-builder/lib/auto-setup');
const hub = require('${CLIENT_DIR}/cache/client-hub.json');
generateClienteClaudeMd('${slug}', hub);
console.log('CLAUDE_MD_OK');
"
```

### Phase 0.5 — Detect gaps

```js
const { detectGaps } = require('./report-builder/lib/auto-setup');
const gaps = detectGaps(slug, hub);
// Retorna { hard: [], soft: [], mid_pipeline: [] }
// 2-arg signature — lib.detectGaps(slug, hub) lee intel files internamente si necesita
```

**HARD gates** (3, bloquean run si no están en Client Hub ni en respuesta Lead):
- `ga4_property_id` — regex `/^\d{6,12}$/`
- `gsc_property_url` — starts with `https://` o `sc-domain:`
- `country_code` — regex `/^[a-z]{2}$/` ISO 3166-1 alpha-2

Si `gaps.hard.length === 0` Y `gaps.soft.length === 0` Y `gaps.mid_pipeline.length === 0`
→ saltar Phase 0.6 questionnaire, mostrar `✅ Client Hub completo — arrancando pipeline`.

**Bash**:
```bash
node -e "
const { detectGaps } = require('./report-builder/lib/auto-setup');
const hub = require('${CLIENT_DIR}/cache/client-hub.json');
const gaps = detectGaps('${slug}', hub);
console.log('GAPS:' + JSON.stringify(gaps));
"
```

### Phase 0.6 — Mass questionnaire al Lead (D4)

**Solo se muestra si hay gaps detectados en Phase 0.5.**

Single batch al inicio — unico interaction point antes de arrancar el pipeline.
Mostrar el template siguiente VERBATIM (con `{ClientName}` y datos reales de gap detection):

#### 🔴 OBLIGATORIO antes de generar el cuestionario (Bug 3 fix post-chedraui)

ANTES de imprimir el cuestionario al Lead, ejecutar estos 2 pasos en orden estricto:

1. **Leer `cache/client-hub.json` completo** del cliente activo:
   ```js
   const hub = JSON.parse(require('fs').readFileSync(
     `${repoBase}/${slug}/cache/client-hub.json`, 'utf8'
   ));
   ```

2. **Citar VERBATIM** los valores reales del cache en CUALQUIER sección del cuestionario que liste contenido del Client Hub (competitors, kpis, products_focus, marketing_objectives, audience.interests, etc.)
   - Si `brief.competitors[]` tiene N items → listá esos N items exactos (no más, no menos, no inventes nombres)
   - Si un campo del cache es `null` o missing → mostrá `(no especificado en Client Hub)` (NO inventar)
   - Si la lista del cache tiene names que no son de la industria — citalos igual (el Lead Hub es source of truth)

#### 🚨 PROHIBIDO ABSOLUTO (anti-pattern Lead — Engram obs #586 + obs #660)

- ❌ Sufijos como `"asumo"`, `"creo que"`, `"probablemente"` en cualquier valor del cuestionario
- ❌ Listar competidores que NO están literalmente en `brief.competitors[]` del cache
- ❌ Omitir competidores que SÍ están en `brief.competitors[]`
- ❌ Reemplazar nombres con sinónimos genéricos o mexicanizar marcas (HEB, Costco) cuando no están en el cache
- ❌ "Auto-confirmar" datos del Client Hub sin haberlos leído del archivo
- ❌ Sustituir prosa libre del cliente por estructura inventada (ej: convertir un string `business_objectives` en un array de bullets sin pedir permiso al Lead)

#### Validación post-cuestionario (autocheck antes de imprimir)

Antes de mostrar el cuestionario al Lead, verificar:
- Sección "📋 DECISIONES" lista N competitors → `brief.competitors.length === N` (exact match)
- Cualquier valor citado del Client Hub → comparar contra el cache JSON literal

Si hay mismatch → ABORTAR la presentación, releer `cache/client-hub.json`, regenerar.



---

```
🔧 Cuestionario inicial — {ClientName}

Encontré algunos gaps en el Client Hub que necesito resolver antes de arrancar.
3 son críticos (sin esto NO puedo correr), 2 son recomendados (mejoran calidad).

═══════════════════════════════════════════════════════
🔴 CRÍTICOS (bloqueantes)
═══════════════════════════════════════════════════════

1. GA4 property ID
   (formato: 123456789, en GA4 admin → property settings)
   ➜ ¿Cuál es?

2. GSC property URL exacta
   ¿Es "https://{site_url}" (URL prefix) o "sc-domain:{domain}"?
   ➜ Pegá la URL exacta

3. País principal (ISO 3166-1 alpha-2 lowercase)
   ➜ ¿"mx", "ar", "cl", "co", otro?

═══════════════════════════════════════════════════════
🟡 RECOMENDADOS (degradan calidad si saltás, podés decir "skip")
═══════════════════════════════════════════════════════

4. Estacionalidad: ¿meses de alta temporada para {ClientName}?
   (ej: "dic-ene, jul, mar" o "no aplica" o "skip")

5. Brand voice tone:
   formal / casual / aspiracional / técnico / mixto / skip

═══════════════════════════════════════════════════════
📋 DECISIONES (no bloqueantes pero valen confirmar)
═══════════════════════════════════════════════════════

6. Competidores: Client Hub tiene {N} ({Lista}).
   Nubank §6 quiere 3-6. ¿OK con estos {N}, o querés ajustar?
   ➜ Respondé "OK", o "agregar X", o "quitar Y"

═══════════════════════════════════════════════════════

Respondé los 6 puntos en 1 mensaje (1 línea por punto).
Cuando los tenga todos, arranco el pipeline (~2hs).
```

---

**Adaptar el cuestionario** a los gaps reales: si `ga4_property_id` ya está en Client Hub,
omitir punto 1. Si `country_code` ya está, omitir punto 3. Solo mostrar los gaps detectados
+ soft recomendados + mid_pipeline confirmacion.

**Validacion de respuestas Lead**:
- HARD inválida (regex fail) → re-preguntar SOLO ese punto puntualmente.
  Ejemplo: `Ese GA4 property ID no matchea el formato (6-12 dígitos). ¿Es "123456789" o similar?`
- SOFT inválida → re-preguntar o aceptar "skip" explícito.
- Ambigua → re-preguntar con clarification puntual.
- NUNCA inventar respuesta para HARD gate. NUNCA asumir default para HARD gate.

**Persistencia de respuestas (Phase 0.7)** — antes de arrancar Phase 2 (crawl kickoff):
- Respuestas HARD → `cliente CLAUDE.md` (campos técnicos) + `intelligence/*.md` (secciones "Datos validados")
- Respuestas SOFT → `intelligence/estacionalidad.md` (seasonality) + `intelligence/perfil.md` (brand voice)
- Respuestas mid_pipeline → `intelligence/competidores.md`
- Cache `client-hub.json` NO se modifica (es snapshot ClickUp original)

### Phase 0.7 — Inventario slices existentes (D6)

```js
const { inventorySlices } = require('./report-builder/lib/auto-setup');
const inv = inventorySlices(slug);
// Retorna array: [{ name, audit_date, age_days, degradation_count, status, slice_path }]
// status (8 valores post Bug 2 fix):
//   'fresh' | 'fresh_degraded' | 'stale' | 'stale_degraded'
// | 'unaged' | 'unaged_degraded' | 'missing' | 'corrupt'
```

#### Decision matrix por status (Bug 4 fix post-chedraui)

| Status | Default action | Override |
|--------|----------------|----------|
| `fresh` | SKIP (slice válido, reusar) | `--force` o `--force-skill={name}` para re-correr |
| `fresh_degraded` | SKIP con warning (slice válido pero N degradations) | `--force-skill={name}` para refrescar |
| `stale` | SKIP con warning (>30d) | `--force-skill={name}` recomendado |
| `stale_degraded` | SKIP con warning (>30d + N deg) | `--force-skill={name}` fuertemente recomendado |
| **`unaged`** (Bug 2 fix) | **RUN — tratar como `missing`** | `--accept-unaged` para forzar SKIP |
| **`unaged_degraded`** | **RUN — tratar como `missing`** | `--accept-unaged` para forzar SKIP |
| `missing` | RUN | (no aplica) |
| `corrupt` | RUN (regenerar slice) | (no aplica) |

**Por qué `unaged` se trata como `missing` por default**: si un slice no tiene `audit_meta.audit_date`, es de un schema viejo o se generó sin metadata. El render mezclaría data de eras distintas → output inconsistente. Mejor regenerar.

#### Mostrar al Lead

```
Inventario slices existentes para {slug}:
  ✓ context.json       (3 days old, 0 deg)             → SKIP
  ✓ tech-audit.json    (3 days old, 0 deg)             → SKIP
  ✓ competitive.json   (8 days old, 2 deg)             → SKIP (corré --force-skill=competitive para refrescar)
  ✗ ai-audit.json      (no existe)                      → RUN
  ⚠ history.json       (no audit_meta — slice viejo)    → RUN (tratado como missing; --accept-unaged para skip)
  ✓ benchmarks.json    (5 days old, 0 deg)             → SKIP
  ⚠ foda.json          (no audit_meta — slice viejo)    → RUN
  ✗ action-plan.json   (no existe)                      → RUN

Plan: correr N skills + render. Costo estimado: ~XK units, ~Ymin wall.
¿Continuar? [Y/n]
```

Esperar confirmacion Lead **solo si hay slices SKIP** (informativo non-blocking si todo es RUN).

#### Flags

- `--force`: re-corre TODO. Inventario mostrado pero NO se pregunta (se re-corre todo).
- `--force-skill={names}`: re-corre solo esas skills. Otras se skip si `fresh`/`stale`, RUN si `unaged`/`missing`/`corrupt`.
- `--accept-unaged`: tratá `unaged` slices como SKIP en lugar del default RUN. Útil para re-render rápido sin regenerar slices viejos.
- `--resume`: saltar inventario, leer progress journal directamente.

---

## Phase 1 — DEPRECATED (context se movió a Phase 6b)

**Reorder 2026-05-05**: Phase 1 originalmente corría `/seo-section-context` ANTES de las
slices upstream que necesita para enriquecer (snapshot_rows, kpi_cards, executive,
priorities, personas/journey). En un run from-scratch eso producía un `context.json`
degradado que nunca se rerunneaba después.

**Solución**: context se generá ahora en **Phase 6b** (después de benchmarks), cuando
todas las cross-section slices (tech-audit, history, ai-audit, competitive, benchmarks)
ya están persistidas en disco. Ver Phase 6b abajo para el código del subagente.

**Backward compat**: el contrato de `/seo-section-context` ya documenta que las
cross-section reads son SOFT (degradación graceful). Eso sigue siendo cierto si el
Lead corre `/seo-section-context` standalone. El reorder solo afecta al master
`/seo-diagnostico-full` para garantizar que el run completo produzca un context
ENRIQUECIDO con cross-section data, no degradado.

**Numeración**: Phase 1 queda como hueco semántico (no se renumeran las phases siguientes
para evitar romper progress journals existentes con `runId` activos en `--resume` mode).
El `writeProgressJournal` skip Phase 1 entirely.

---

## Phase 2 — Tech-audit kickoff (async)

**Duracion estimada**: ~10s kickoff (5s start + 5s validate). **NO bloqueante** — crawl corre en background.

Iniciar diagnostic SF via `diagnostic-mcp.start-diagnostic` con profile `retail-discovery`
+ country override (D3), **luego validar via 1 poll inicial** (Bug B7 fix v3.37.2 — sin
este poll, el lock marca `success` aunque los sources backend devuelvan `client_not_seeded`).

```js
// Via MCP tool call — NO subagente (es 1 call simple, no hay logica de skill)
const startResult = await callMcp('diagnostic-mcp', 'start-diagnostic', {
  slug,
  country,                          // override Bright Data residential proxy
  profile: 'retail-discovery'       // perfil SF estandar para diagnostico completo
});
const diagnostic_id = startResult.data.diagnostic_id;

// Bug B7 fix v3.37.2: validar el kickoff con 1 poll antes de marcar success.
// Pre-fix: Phase 2 marcaba 'success' solo porque POST devolvió 202 con id —
// el polling subsiguiente revelaba `client_not_seeded` en los 5 sources y se
// perdía la señal. El lock mentía y re-runs skipeaban Phase 2.
await sleep(5000); // dar 5s al backend para arrancar source workers
const validateStatus = await callMcp('diagnostic-mcp', 'get-diagnostic-status', {
  id: diagnostic_id
});
const sources = validateStatus?.data?.sources ?? {};
const hardSkips = Object.entries(sources).filter(([_, s]) => {
  // Treat `client_not_seeded` (any variant) + auth failures as hard fail.
  // Soft skip_reasons (oauth_reauth_required, no_data) NO bloquean kickoff —
  // se marcan como degradation pero el run sigue.
  return /client_not_seeded/.test(s?.skip_reason || '')
      || /backend_unauthorized/.test(s?.skip_reason || '');
});

if (hardSkips.length > 0) {
  writeProgressJournal(slug, runId, 2, {
    phase: 'tech-audit-kickoff',
    status: 'failed',
    diagnostic_id,
    duration_ms: /* elapsed */,
    degradation_count: hardSkips.length,
    degradation_summary: hardSkips.map(([source, s]) => `${source}: ${s.skip_reason}`)
  });
  // STOP el run aquí — Phase 0.0.5 debió haber detectado esto, así que es
  // probablemente un race condition o source backend roto. Surface al Lead.
  throw new Error(`Phase 2 kickoff failed validation: ${hardSkips.map(([s]) => s).join(', ')} not seeded`);
}

// Soft degradations OK — anotar en el journal pero seguir.
const softDegrade = Object.entries(sources)
  .filter(([_, s]) => s?.skip_reason)
  .map(([source, s]) => `${source}: ${s.skip_reason}`);

writeProgressJournal(slug, runId, 2, {
  phase: 'tech-audit-kickoff',
  status: 'success',
  diagnostic_id,
  duration_ms: /* elapsed */,
  degradation_count: softDegrade.length,
  degradation_summary: softDegrade
});
```

**Bash** (via MCP stdio — patrón establecido en `scripts/mcp-stdio.cjs`):

Si el MCP tool no está disponible directamente, invocar via JSON-RPC:
```bash
# 1. Kickoff
node scripts/mcp-stdio.cjs diagnostic-mcp start-diagnostic \
  '{"slug":"${slug}","country":"${country}","profile":"retail-discovery"}'

# 2. Esperar 5s + validar (Bug B7 fix)
sleep 5
node scripts/mcp-stdio.cjs diagnostic-mcp get-diagnostic-status \
  "{\"id\":\"${diagnostic_id}\"}"
# Inspect data.sources.<each>.skip_reason — abort si client_not_seeded.
```

Guardar `diagnostic_id` en variable de sesion. Es necesario en Phase 4 para el poll.

Si `start-diagnostic` falla:
- Retry 1x con backoff 30s
- Si falla 2x → mark phase2 `failed`, continuar con `diagnostic_id = null`
- Phase 5 tech-audit se ejecutará con `crawl_failed` en su degradation

Si la validación post-kickoff (Bug B7 fix) detecta `client_not_seeded` en cualquier source:
- mark phase2 `failed` con degradation_summary explícito
- STOP el run y surface al Lead — esto NO debería pasar si Phase 0.0.5 corrió OK,
  indica race condition backend o source worker roto
- El Lead puede re-correr el skill con `--resume` después de fixear el backend

---

## Phase 3 — Parallel skills (run_in_background × 3)

**Duracion estimada**: ~15min wall (maximo de los 3 paralelos). **Bloqueante para Phase 5**: sí (via Phase 4 wait).

Spawn 3 subagentes SIMULTANEAMENTE con `run_in_background: true` (D3):

```js
const { buildSubagentPrompt, parseSubagentResult } = require('./report-builder/lib/orchestrator-runtime');

const sharedCtx = { slug, country, period, repo_path: `~/Documents/punto-rojo-clients/${slug}` };

// Spawn paralelo — NO await individual, collect task_ids
const task_history    = Agent({ subagent_type: 'general-purpose', prompt: buildSubagentPrompt('seo-section-history',     sharedCtx), run_in_background: true });
const task_ai_audit   = Agent({ subagent_type: 'general-purpose', prompt: buildSubagentPrompt('seo-section-ai-audit',    sharedCtx), run_in_background: true });
const task_competitive = Agent({ subagent_type: 'general-purpose', prompt: buildSubagentPrompt('seo-section-competitive', sharedCtx), run_in_background: true });
```

**Costo estimado por skill paralela**:
- skill 3/8 history: ~3K Ahrefs units
- skill 4/8 ai-audit: ~5K Brand Radar units
- skill 5/8 competitive: ~20K Ahrefs units

**Error policy**: si 1 de los 3 subagentes falla, los otros 2 CONTINUAN. Orquestador NO
retry automatico en paralelo (cada skill gestiona sus retries internos). Marca Phase 3 como
`partial` en el journal. Sigue a Phase 4 con los 2 slices exitosos.

Guardar task IDs en journal:
```js
writeProgressJournal(slug, runId, 3, {
  phase: 'parallel-skills',
  status: 'running',
  task_ids: { history: task_history.id, ai_audit: task_ai_audit.id, competitive: task_competitive.id },
  duration_ms: 0,
  degradation_count: 0,
  degradation_summary: []
});
```

---

## Phase 4 — Wait gate (D14 hibrido)

**Duracion estimada**: ~1h 45min (dominado por SF crawl). **Bloqueante para Phase 5**: sí.

D14 hibrido en 2 pasos:

### Step 4.1 — Notification-driven: esperar 3 subagentes Phase 3

**NO hacer polling activo**. Los 3 subagentes completan via notificacion de Claude Code
(el runtime notifica cuando un `run_in_background` task completa). El orquestador recibe
las 3 notificaciones y parsea cada resultado:

```js
// Esperar las 3 notificaciones (orden de llegada indeterminado, OK)
const results3 = await waitAllAgents([task_history, task_ai_audit, task_competitive]);

const phase3Results = results3.map(r => parseSubagentResult(r));
const phase3Status = phase3Results.every(r => r.status === 'success') ? 'success' : 'partial';
writeProgressJournal(slug, runId, 3, {
  phase: 'parallel-skills',
  status: phase3Status,
  results: phase3Results,
  duration_ms: /* max elapsed */,
  degradation_count: phase3Results.reduce((s, r) => s + r.degradation_count, 0),
  degradation_summary: phase3Results.flatMap(r => r.degradation_summary)
});
```

### Step 4.2 — Single Bash blocking poll del crawl

Despues de que los 3 subagentes completaron (Step 4.1 done), single Bash call que bloquea
hasta que el crawl SF termine:

```bash
node report-builder/lib/orchestrator-runtime.js poll-crawl ${diagnostic_id}
```

Este Bash bloquea ~1h 45min. Timeout hard: 2hs.

```js
const crawlResult = await Bash({
  command: `node report-builder/lib/orchestrator-runtime.js poll-crawl ${diagnostic_id}`,
  timeout: 7200000  // 2h hard timeout
});
```

El `pollCrawlStatus` dentro de `orchestrator-runtime.js` imprime por stdout:
```
⏳ SF crawl en progreso: 35% (1247/3500 URLs) — ETA ~75 min
```
(carriage return — output transient, NO acumula en contexto del orquestador).

**Retry policy en poll**: `get-diagnostic-status` error transitorio → retry 3x con
backoff 30s/60s/120s. Si falla 3 veces → mark crawl `failed`, continuar Phase 5 con
`degradation.crawl_failed`.

Si `diagnostic_id === null` (kickoff fallido en Phase 2) → saltar Step 4.2, continuar.

Guardar resultado en journal:
```js
writeProgressJournal(slug, runId, 4, {
  phase: 'wait-gate',
  status: crawlResult.exit === 0 ? 'success' : 'partial',
  diagnostic_id,
  crawl_status: crawlResult.stdout,   // solo el final state
  duration_ms: /* elapsed */,
  degradation_count: crawlResult.exit !== 0 ? 1 : 0,
  degradation_summary: crawlResult.exit !== 0 ? ['crawl_failed_after_retry'] : []
});
```

---

## Phase 5 — Tech-audit slice

**Duracion estimada**: ~10s. **Bloqueante para Phase 6**: sí.

Subagente `/seo-section-tech-audit` consume el `crawl_id` de Phase 2.
Este skill lee el `consolidated_json` del backend via `diagnostic-mcp.get-diagnostic-status`
y produce `sections/tech-audit.json`.

```js
const techAuditPrompt = buildSubagentPrompt('seo-section-tech-audit', {
  slug,
  country,
  period,
  repo_path: `~/Documents/punto-rojo-clients/${slug}`,
  diagnostic_id   // from Phase 2 — puede ser null si crawl failed
});

const phase5Result = parseSubagentResult(
  await Agent({ subagent_type: 'general-purpose', prompt: techAuditPrompt })
);
writeProgressJournal(slug, runId, 5, { ...phase5Result, phase: 'tech-audit' });
```

Si `diagnostic_id === null` → incluirlo en el prompt para que la skill degrade graceful
(clusters 3 y 5 del diagnóstico sin SF data, cobertura ~70% en vez de ~95%).

Si Phase 5 falla: retry 1x con backoff 60s. Si falla 2x → mark failed + continuar.

---

## Phase 6 — Synthesis cascade (sequential)

**Duracion estimada**: ~70s total. **Bloqueante para Phase 7**: sí.

3 skills de sintesis en secuencia (cada una depende de slices previos):

### Phase 6a — Benchmarks (skill 6/8)

Sprint 0+C scoring layer. Lee tech-audit + competitive + ai-audit + history slices.

```js
const phase6a = parseSubagentResult(
  await Agent({ subagent_type: 'general-purpose',
    prompt: buildSubagentPrompt('seo-section-benchmarks', {
      slug, country, period, repo_path: `~/Documents/punto-rojo-clients/${slug}`
    })
  })
);
writeProgressJournal(slug, runId, '6a', { ...phase6a, phase: 'benchmarks' });
```

**Costo**: ~500 Opus tokens. No llama MCPs externos.
**Max totals**: 70/70/60 (Opción A — 7 criterios técnicos/contenido × 10, 6 criterios autoridad × 10).

### Phase 6b — Context (skill 7/8) ⬅ NUEVA POSICIÓN (reorder 2026-05-05)

Sintesis Opus. Lee intelligence files + tech-audit + history + ai-audit + competitive +
benchmarks slices (TODAS ya disponibles a esta altura). Produce `sections/context.json`
con snapshot_rows + kpi_cards + executive + priorities + personas + journey ENRIQUECIDOS
con cross-section data — NO degradado.

**Por qué se movió acá** (era Phase 1): originalmente corría primero y todas las
cross-section reads daban miss → context se persistía con `degradation.skip_reason:
'cross_section_missing'`. Ahora corre después de las 5 slices upstream que necesita.

```js
const phase6b = parseSubagentResult(
  await Agent({ subagent_type: 'general-purpose',
    prompt: buildSubagentPrompt('seo-section-context', {
      slug, country, period, repo_path: `~/Documents/punto-rojo-clients/${slug}`
    })
  })
);
writeProgressJournal(slug, runId, '6b', { ...phase6b, phase: 'context' });
```

**Costo**: ~30s wall + Opus tokens (no MCPs externos para measurement; ClickUp Client
Hub ya está cacheado por Phase 0.6 — reutiliza `cache/client-hub.json` sin re-llamar MCP).

Si Phase 6b falla: retry 1x con backoff 60s. Si falla 2x → mark `failed` + continuar
(context slice tiene shape esperado con `degradation.skip_reason: 'skill_failed_after_retry'`,
template renderea con hl_box yellow CTA al Lead).

### Phase 6c — FODA (skill 1/8)

Sintesis Opus. Lee benchmarks + competitive + history + ai-audit + context slices
(context ya disponible desde Phase 6b).

```js
const phase6c = parseSubagentResult(
  await Agent({ subagent_type: 'general-purpose',
    prompt: buildSubagentPrompt('seo-section-foda', {
      slug, country, period, repo_path: `~/Documents/punto-rojo-clients/${slug}`
    })
  })
);
writeProgressJournal(slug, runId, '6c', { ...phase6c, phase: 'foda' });
```

**Costo**: ~800 Opus tokens. Sintesis pura — NO MCPs.

### Phase 6d — Action Plan (skill 8/8)

Sintesis Opus final. Lee 6 slices upstream (incluye context de Phase 6b) + ClickUp Client Hub.
Emite `data.{access_requirements, onboarding_checklist, next_steps, scoring.roadmap}` para sec-16 a sec-19.

```js
const phase6d = parseSubagentResult(
  await Agent({ subagent_type: 'general-purpose',
    prompt: buildSubagentPrompt('seo-section-action-plan', {
      slug, country, period, repo_path: `~/Documents/punto-rojo-clients/${slug}`
    })
  })
);
writeProgressJournal(slug, runId, '6d', { ...phase6d, phase: 'action-plan' });
```

**Si skill 8/8 no está disponible**: continuar con warning — sec-16/19 degradan en template.

---

## Phase 7 — Render + output

**Duracion estimada**: ~200ms. **Bloqueante**: no (es el paso final).

### Phase 7a — Build report

Subagente `/seo-build-report` lee los 8 slices de disco, compone `assembled-{period}.json`
y genera el HTML.

```js
const buildReportPrompt = buildSubagentPrompt('seo-build-report', {
  slug,
  country,
  period,
  repo_path: `~/Documents/punto-rojo-clients/${slug}`
});

const phase7Result = parseSubagentResult(
  await Agent({ subagent_type: 'general-purpose', prompt: buildReportPrompt })
);
writeProgressJournal(slug, runId, 7, { ...phase7Result, phase: 'render' });
```

Output: `~/Documents/punto-rojo-clients/{slug}/output/{slug}-diagnostico-{period}.html`

Si Phase 7 falla → ABORT con mensaje detallado. `assembled.json` ya existe en disco;
Lead puede correr `/seo-build-report {slug} {period}` aparte para re-intentar el render.

### Phase 7b — Auto-open browser (D5)

```bash
# Windows — intento de apertura en browser
start "" "~/Documents/punto-rojo-clients/${slug}/output/${slug}-diagnostico-${period}.html"
```

```js
// Con try/catch para entornos headless
try {
  await Bash({ command: `start "" "${htmlPath}"` });
} catch {
  console.log(`(headless — no auto-open). Path: ${htmlPath}`);
}
```

Omitir si `--no-open` flag activo.

### Phase 7c — Final summary

Imprimir resumen via `formatFinalSummary(phaseResults, runMeta)`:

```js
const { formatFinalSummary, aggregateRunCost } = require('./report-builder/lib/orchestrator-runtime');

const runCost = aggregateRunCost(phaseResults);
const summary = formatFinalSummary(phaseResults, {
  slug,
  run_id: runId,
  period,
  html_path: htmlPath,
  wall_time_ms: Date.now() - startedAt,
  ...runCost
});
console.log(summary);
```

**Output de ejemplo**:
```
✅ /seo-diagnostico-full volaris — COMPLETADO

  Run ID:    2026-05-05-a1b2c3d4
  Periodo:   2026-05
  HTML:      ~/Documents/punto-rojo-clients/volaris/output/volaris-diagnostico-2026-05.html
  Wall time: 2hs 21min
  Costo est: ~28.5K Ahrefs units, ~$1.8 USD Opus

  Phases:
    Phase 0  ✓ setup        (2min 3s)
    Phase 2  ✓ crawl kickoff (4s) → diagnostic_id: abc-123
    Phase 3  ✓ history + ai-audit + competitive (14min 32s, paralelo)
    Phase 4  ✓ wait gate    (1h 43min, 0 retries)
    Phase 5  ✓ tech-audit   (9s)
    Phase 6  ✓ benchmarks + context + foda + action-plan (98s)
    Phase 7  ✓ render       (183ms)

  Degradaciones: 2
    - history: GSC data partial (last 90d only, not 12m)
    - benchmarks: SimilarWeb data unavailable (API key needed)

  Report: abierto en browser
```

Guardar run-summary en disco:
```bash
node -e "
const fs = require('fs');
const summary = ${JSON.stringify(runSummaryObject)};
const p = '${CLIENT_DIR}/output/run-summary-${period}-${runId}.json';
fs.writeFileSync(p, JSON.stringify(summary, null, 2));
console.log('SUMMARY_OK:' + p);
"
```

(D12 — `run-summary-{period}-{run_id}.json` acumula histórico, NO sobrescribe — cada run tiene su propio `run_id` único.
D13 — el HTML output `{slug}-diagnostico-{period}.html` y `assembled-{period}.json` SÍ sobrescriben — solo conservan el último; los run summaries son los que acumulan.)

---

## Cleanup (finally)

**SIEMPRE ejecutar**, incluso en error fatal (D8):

```js
try {
  // ... todo el pipeline ...
} finally {
  const { releaseLock } = require('./report-builder/lib/auto-setup');
  releaseLock(slug);
}
```

**Bash**:
```bash
node -e "
const { releaseLock } = require('./report-builder/lib/auto-setup');
releaseLock('${slug}');
console.log('LOCK_RELEASED');
"
```

Si `releaseLock` falla (archivo ya borrado por otro proceso) → ignorar silenciosamente.
El lock tiene TTL 180min — expirará solo si no se puede borrar.

---

## Error recovery

Ver detalle completo: `references/error-recovery.md`

### Tipo 1 — Errores de configuracion (HARD gates fail Phase 0)

ABORT antes de Phase 2 (crawl kickoff). Costo $0. Lock liberado. Progress journal NO escrito.

```
❌ /seo-diagnostico-full {slug} ABORTADO en Phase 0.5

Faltan datos críticos en Client Hub que NO puedo asumir:
  • GA4 property ID (necesario para skill 5/8 competitive)
  • GSC property URL exacta (formato sc-domain: vs https://)

Acción requerida:
  1. Editar Client Hub | {ClientName} → Brief → "Technical Setup"
  2. Completar campos: ga4_property_id, gsc_property_url
  3. Re-correr /seo-diagnostico-full {slug}

Costo consumido: $0 (no se inició el pipeline)
```

### Tipo 2 — Errores transitorios mid-pipeline

**Phases sequenciales (5, 6a, 6b, 6c, 6d)**:
- Retry 1x con backoff 60s
- Si falla 2x → mark `failed`, continuar
- Slice queda con `degradation.skip_reason: 'skill_failed_after_retry'`

**Phase 3 (paralelo)**:
- Si 1 de 3 falla → los otros 2 continuan
- Orquestador NO retry automatico en paralelo
- Phase 3 queda `partial`

**Phase 4 (polling)**:
- Retry 3x con backoff 30s/60s/120s en `get-diagnostic-status` transitorios
- Si falla 3x → mark crawl `failed`, continuar con `crawl_failed` degradation

**Phase 7 (render)**:
- ABORT — assembled JSON ya OK; Lead corre `/seo-build-report {slug} {period}` aparte

### Tipo 3 — Errores fatales (orquestador crash)

Lock residual: proxima invocacion detecta stale lock (>180min) → overwrite con warning.
Progress journal queda parcial.

Recovery: `/seo-diagnostico-full {slug} --resume`

---

## Cost tracking

Ver detalle completo: `references/cost-tracking.md`

Constantes `PRICING` exportadas desde `orchestrator-runtime.js`:

```js
// orchestrator-runtime.js exports
const PRICING = {
  AHREFS_UNITS_PER_USD: 250_000,   // Enterprise 2M/mes ÷ ~$8/mes
  OPUS_TOKENS_PER_USD: 50_000,     // ~$15/M input + $75/M output, promedio ~$20/M
  SIMILARWEB_CALLS_PER_USD: 100    // estimado segun tier
};

// Por skill (estimados, D7 soft cap warning si >2x)
const SKILL_COST_ESTIMATES = {
  'seo-section-context':     { ahrefs: 0,      opus_tokens: 2_000,  usd: 0.04  },
  'seo-section-tech-audit':  { ahrefs: 0,      opus_tokens: 1_500,  usd: 0.03  },
  'seo-section-history':     { ahrefs: 3_000,  opus_tokens: 1_000,  usd: 0.03  },
  'seo-section-ai-audit':    { ahrefs: 5_000,  opus_tokens: 1_500,  usd: 0.05  },
  'seo-section-competitive': { ahrefs: 20_000, opus_tokens: 2_000,  usd: 0.10  },
  'seo-section-benchmarks':  { ahrefs: 0,      opus_tokens: 500,    usd: 0.01  },
  'seo-section-foda':        { ahrefs: 0,      opus_tokens: 800,    usd: 0.016 },
  'seo-section-action-plan': { ahrefs: 0,      opus_tokens: 1_000,  usd: 0.02  },
  'seo-build-report':        { ahrefs: 0,      opus_tokens: 300,    usd: 0.006 },
  'orchestrator':            { ahrefs: 0,      opus_tokens: 15_000, usd: 0.30  },
  // TOTAL estimado: ~28K Ahrefs, ~25.6K Opus tokens, ~$0.57 USD + orchestrator
};
```

Si run real excede 2x estimate de alguna skill → log warning en `degradation_summary` de esa
phase. NO abortar (D7). Cost tracking populate empírico deferido a v2 (requiere
`get_subscription_info` en ahrefs-mcp).

---

## Resume strategy

Ver detalle completo: `references/orchestration-flow.md`

### `--resume`

Lee `.diagnostico-progress.json` del ultimo run. Salta phases con `status: 'done'`.
Retoma desde `current_phase`.

```bash
/seo-diagnostico-full volaris --resume
```

Output informativo:
```
📋 Resume detectado:
   Last run: 2026-05-05-a1b2c3d4 (interrumpido en Phase 3)
   Phases completed: [0, 1, 2]
   Phases pending: [3 partial — 2/3 done, 4, 5, 6, 7]

Reanudando desde Phase 3 (re-corriendo skill 4/8 ai-audit que quedó incompleta)...
```

Phase 0 siempre re-corre aunque el journal diga done (lock + structure validation es barato).

### `--force` / `--force-skill={names}`

Re-corre todo o skills especificas. Ignora slices existentes + progress journal para esas skills.

```bash
/seo-diagnostico-full volaris --force
/seo-diagnostico-full volaris --force-skill=competitive
/seo-diagnostico-full volaris --force-skill=competitive,ai-audit
```

`--force-skill` acepta nombres sin prefix `seo-section-` (ej: `competitive` = `seo-section-competitive`).
Cache `client-hub.json` se respeta si dentro de TTL.

### Default (sin flags) — Inventario informativo

Ver Phase 0.7 — inventario + confirmacion Y/n del Lead antes de arrancar.

---

## References

- `references/auto-setup-flow.md` — Phase 0 detalle completo (lock, repo, Client Hub, intelligence merge, detectGaps algoritmo)
- `references/orchestration-flow.md` — Phases 1-7 detalle + diagrama de paralelismo + D14 hibrid poll pseudocode
- `references/lead-questionnaire.md` — Catalogo completo de questions + validators + persistencia targets por tipo de gap
- `references/error-recovery.md` — 3 tipos de errores + retry policy + abort messages exactos
- `references/cost-tracking.md` — Phase X cost estimates + PRICING constants + soft cap policy + v2 roadmap

Spec completo con decisiones D1-D14: `docs/superpowers/specs/2026-05-04-diagnostico-full-skill-design.md`
Schema run-summary: `skills/seo-diagnostico-full/schema.json`
Libs: `report-builder/lib/auto-setup.js`, `report-builder/lib/intelligence-generator.js`, `report-builder/lib/orchestrator-runtime.js`
