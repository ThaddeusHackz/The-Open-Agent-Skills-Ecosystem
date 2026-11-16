---
name: seo-build-report
description: Use AFTER the 8 Phase 8 section skills (/seo-section-foda, /seo-section-tech-audit, /seo-section-history, /seo-section-ai-audit, /seo-section-competitive, /seo-section-benchmarks, /seo-section-context, /seo-section-action-plan) have written their JSON slices to ~/Documents/punto-rojo-clients/{slug}/sections/. This is a THIN ORCHESTRATOR that composes the slices into the assembled JSON consumed by report-builder/generate-report.js. It does NOT measure data — it reads slices from disk, deep-merges them, and renders the single-file HTML deliverable.
---

<execution-protocol>
MODO: EJECUCION DIRECTA — NO PLANIFICACION

Este skill es un ORQUESTADOR THIN con 7 fases secuenciales (0..6).
NO hace measurements: lee 7 slices de disco, los compone, llama 1 CLI.

PROHIBIDO:
- Llamar Ahrefs / GSC / GA4 / DataForSEO / diagnostic-mcp directamente. Toda la data
  ya vive en los slices `~/Documents/punto-rojo-clients/{slug}/sections/*.json`.
  Si un slice falta o esta stale, STOP / WARN — NO regenerar la data inline.
- Inventar data para campos que ningun slice cubre (ej. access_requirements,
  onboarding_checklist). Usar `{ available: false }` o array vacio para que el
  template degrade graceful.
- Pushear a git sin confirmacion EXPLICITA del Lead (Fase 5).
- Persistir o copiar archivos al pr-toolkit con working tree dirty — abortar y
  pedir commit/stash primero.
- Saltar fases o colapsar multiples fases en una sola respuesta.

OBLIGATORIO:
- Operador = userEmail prefix del environment (ej: nico.m@puntorojo.com → "Nico").
  NUNCA usar `cliente-CLAUDE.md.Lead` como nombre del operador. Ver
  `shared/skill-execution-protocol.md` §Regla 6.
- Validar slug + period al inicio (Fase 0) — si falla, STOP.
- Respetar checkpoints del Lead en Fase 3 (pre-render) y Fase 5 (pre-push).
- Citar la fuente de cada slice (`sections/foda.json`, `sections/context.json`, etc.).
- Si action-plan slice no existe → STOP con `"Run /seo-section-action-plan first."`
  (skill 8/8 shipped v3.35.0 — slice REQUIRED igual que las otras 7).
  El flag `--no-action-plan` es DEV-ONLY (skip explícito para iteración rápida sin
  esperar el slice action-plan). En run productivo: NO usar `--no-action-plan`.

Protocolo: shared/skill-execution-protocol.md
Context engineering: shared/context-engineering.md (Patron 5 process-and-discard)
</execution-protocol>

# /seo-build-report — Orquestador thin de slices Phase 8

## Objetivo

Componer los 7-8 JSON slices Phase 8 en un assembled JSON canonico (shape de
`samples/chedraui-sample.json`) y disparar `generate-report.js` para producir el
HTML profesional single-file.

**Thin orchestrator**: NO mide nada. NO llama APIs externas. NO consume
`consolidated_json` del backend. Las skills `/seo-section-*` ya hicieron el
trabajo pesado y dejaron sus slices en disco.

**Modelo recomendado**: Sonnet (orquestacion + merge + 1 subprocess call —
ningun razonamiento pesado).

**Entregables**:

1. HTML local en `report-builder/output/{slug}-diagnostico-{period}.html` —
   share-able por email/drive a clientes externos.
2. (Opcional) URL hosted `https://pr-toolkit.puntorojo.com/reports/{slug}/{period}` —
   auth-gated `@puntorojo.com`, para equipo interno.

**Diferencia vs `/seo-reporte`**: `/seo-reporte` hace consultas ad-hoc de
performance y resuelve findings pendientes. Este skill **empaqueta** los slices
ya producidos en un entregable visual profesional. Son complementarios.

---

## Inputs

| Parametro | Tipo | Default | Descripcion |
|---|---|---|---|
| `client_slug` | string (required) | — | kebab-case del cliente (ej: `chedraui`). Regex `/^[a-z0-9][a-z0-9-]*$/` |
| `period` | string (required) | current month | `YYYY-MM` del periodo del reporte. Regex `/^\d{4}-\d{2}$/` |
| `--no-action-plan` | flag (optional, **DEV-ONLY**) | false | Skip explícito del slice action-plan (skill 8/8). Útil solo para iteración rápida sin esperar al slice. **NO usar en run productivo** — sec-16/19 quedan placeholders en el HTML final entregado al cliente |
| `--pdf` | flag (optional) | false | Placeholder — PDF aun no soportado. Responder que queda queued y continuar con HTML |

**Invocacion esperada del Lead**:
```
/seo-build-report chedraui 2026-04
/seo-build-report chedraui 2026-04 --no-action-plan
/seo-build-report chedraui 2026-04 --pdf   (warning: PDF aún no soportado, fallback a HTML)
```

---

## Prerequisitos

1. **Carpeta del cliente** en `~/Documents/punto-rojo-clients/{client_slug}/` con `cliente-CLAUDE.md` + `intelligence/*.md`.
2. **Slices Phase 8** en `{cliente}/sections/`:
   - **REQUERIDOS (8)** — si falta cualquiera, STOP con `"Run /seo-section-{name} first."`:
     - `foda.json` (1/8), `tech-audit.json` (2/8), `history.json` (3/8), `ai-audit.json` (4/8), `competitive.json` (5/8), `benchmarks.json` (6/8), `context.json` (7/8), `action-plan.json` (8/8).
   - **Bypass DEV-ONLY**: `--no-action-plan` permite skip de action-plan SOLO para iteración rápida (sec-16/19 degradan a placeholders). NO usar en run productivo.
3. **Node 20+** + `report-builder/node_modules` (si falta: `cd report-builder && npm install`).
4. **Repo pr-toolkit** (solo si Lead elige upload) — default `C:\Users\nicko\OneDrive\Escritorio\Proyectos\Punto-Rojo\pr-toolkit\` o `$PR_TOOLKIT_PATH`.

---

## Flujo general

```
Inicio → Inputs + validacion →
  Fase 0: Context load (cliente-CLAUDE.md + actividad.md + intelligence/*)
  Fase 1: Verify slices exist + freshness check (warn si >30 dias)
          + Validate cada slice via su validator (lib/{name}-validator.js)
  Fase 2: Compose assembled JSON (deep-merge slices + meta + intelligence
          fallbacks para campos no cubiertos por slices)
          → persist a {client_repo}/output/assembled-{period}.json (re-render-friendly)
  Fase 3: CHECKPOINT OBLIGATORIO con el Lead (pre-generate — nunca saltarlo)
  Fase 4: Generar HTML via generate-report.js CLI
          → CHECKPOINT pre-upload (local-only vs push)
  Fase 5: (Opcional) Upload a pr-toolkit + git push + Vercel deploy
  Fase 6: Output al Lead + update actividad.md
```

---

## Fase 0: Context load

### 0.1 Validar inputs

```javascript
const SLUG_RE = /^[a-z0-9][a-z0-9-]*$/;
const PERIOD_RE = /^\d{4}-\d{2}$/;

if (!SLUG_RE.test(slug)) → STOP: "slug invalido: {slug}. Debe matchear /^[a-z0-9][a-z0-9-]*$/"
if (!PERIOD_RE.test(period)) → STOP: "period invalido: {period}. Debe ser YYYY-MM"
```

Si el Lead no proveyo `period`, default al mes actual (`YYYY-MM` desde `currentDate`).

### 0.2 Leer contexto del cliente

Usando Read tool (absolute paths):

1. `~/Documents/punto-rojo-clients/{slug}/cliente-CLAUDE.md` — S1 (dominio, lead, etapa), S3 (accesos), S5 (progreso skills).
2. `~/Documents/punto-rojo-clients/{slug}/actividad.md` — ultimas sesiones del equipo.
3. `~/Documents/punto-rojo-clients/{slug}/intelligence/perfil.md` — identidad, audiencia, tono.
4. `~/Documents/punto-rojo-clients/{slug}/intelligence/objetivos.md` — KPIs, targets.
5. `~/Documents/punto-rojo-clients/{slug}/intelligence/productos-foco.md` — productos priorizados.

Si falta alguno de los 3 obligatorios (`perfil`, `objetivos`, `productos-foco`):
warning al Lead, **no abortar** — los slices son la fuente primaria; los
intelligence files solo cubren campos auxiliares (`access_requirements`,
`onboarding_checklist`, `next_steps`).

Intelligence opcionales (leer si existen): `competidores.md`, `estacionalidad.md`,
`contexto-historico.md`.

### 0.3 Operador correcto

Ver `shared/skill-execution-protocol.md` §Regla 6. **Operador = userEmail prefix**
(ej: `nico.m@puntorojo.com` → "Nico"). NUNCA usar `cliente-CLAUDE.md.Lead` como
nombre del operador — ese es el account manager del cliente.

---

## Fase 1: Verify + validate slices

### 1.1 Required slices presentes

```
SECTIONS_DIR = ~/Documents/punto-rojo-clients/{slug}/sections/

REQUIRED = ['foda', 'tech-audit', 'history', 'ai-audit',
            'competitive', 'benchmarks', 'context', 'action-plan']
DEV_BYPASS_FLAG = '--no-action-plan'  // permite skip de action-plan SOLO en dev
```

Para cada nombre en `REQUIRED`:

```bash
test -f "$SECTIONS_DIR/{name}.json"
```

Si NO existe → STOP con mensaje:

```
❌ Slice {name}.json no existe en {SECTIONS_DIR}.

Run /seo-section-{name} first.

(Este orquestador no genera la data — solo compone los 8 slices Phase 8 que ya
debieron correrse antes para este cliente/periodo.)
```

**Excepción dev-only para `action-plan.json`**:

- Si existe → leer y validar (igual que las otras 7).
- Si NO existe Y el Lead pasó `--no-action-plan` → warn explícito + continuar:
  ```
  ⚠️  --no-action-plan flag activo (DEV-ONLY).
  Las secciones sec-16/17/18/19 (Roadmap + Build/Scale/Evolve + KPIs target)
  van a degradar a placeholders en el HTML.
  NO USAR en run productivo — el HTML entregado al cliente quedará incompleto.

  Continuo igual? [S] continuar / [N] STOP
  ```
- Si NO existe Y el Lead NO pasó `--no-action-plan` → STOP (mismo mensaje que las otras REQUIRED).

### 1.2 Freshness check (warn si >30 dias)

Para cada slice (incluido action-plan si existe):

```bash
# Edad del archivo en dias
file_age_days=$(( ( $(date +%s) - $(stat -c %Y "$SECTIONS_DIR/{name}.json") ) / 86400 ))
```

Si `file_age_days > 30`:

```
⚠️  Slice {name}.json tiene {N} dias (>30). La data puede estar desactualizada.

Recomendacion: corre /seo-section-{name} para refresh antes de generar el reporte.

Continuo igual? [S] continuar / [N] STOP / [R] re-correr esa seccion (te lo
indico — esta skill no la corre por vos)
```

NO bloquear si el Lead responde `[S]`. Documentar el warning en el output final
del Lead (Fase 6) — "Generado con slices stale: {list}".

### 1.3 Validate cada slice via su validator

Por cada slice presente, leer + parsear + validar contra
`report-builder/lib/{name}-validator.js`:

| Slice | Validator | Funcion exportada |
|---|---|---|
| foda | `report-builder/lib/foda-validator.js` | `validateFodaSlice` |
| tech-audit | `report-builder/lib/tech-audit-validator.js` | `validateTechAuditSlice` |
| history | `report-builder/lib/history-validator.js` | `validateHistorySlice` |
| ai-audit | `report-builder/lib/ai-audit-validator.js` | `validateAiAuditSlice` |
| competitive | `report-builder/lib/competitive-validator.js` | `validateCompetitiveSlice` |
| benchmarks | `report-builder/lib/benchmarks-validator.js` | `validateBenchmarksSlice` |
| context | `report-builder/lib/context-validator.js` | `validateContextSlice` |
| action-plan | `report-builder/lib/action-plan-validator.js` | `validateActionPlanSlice` |

Estrategia: invocar todos los validators en una sola pasada Bash:

```bash
cd "${CLAUDE_PLUGIN_ROOT}/report-builder" && node -e '
const fs = require("fs");
const path = require("path");
// 8 slices REQUIRED. Si --no-action-plan flag activo (DEV-ONLY), filtrar action-plan del array.
const slices = ["foda", "tech-audit", "history", "ai-audit", "competitive", "benchmarks", "context", "action-plan"];
const SECTIONS = "/path/to/sections/";
const results = {};
for (const name of slices) {
  const validator = require(`./lib/${name}-validator.js`);
  const fnName = `validate${name.replace(/-./g, m => m[1].toUpperCase()).replace(/^./, m => m.toUpperCase())}Slice`;
  const validate = validator[fnName];
  const slice = JSON.parse(fs.readFileSync(path.join(SECTIONS, `${name}.json`), "utf8"));
  results[name] = validate(slice);
}
process.stdout.write(JSON.stringify(results, null, 2));
'
```

Si **cualquier slice falla validacion** (`valid === false`) → STOP con el
contenido de `errors[]` para que el Lead pueda corregirlo (re-correr la skill
afectada).

NO intentar fixear el slice inline — el extractor de cada skill es el unico
responsable de su shape.

### 1.4 Process-and-discard temprano

Despues de leer + validar cada slice, retener en contexto **solo el slice
parseado** (no el raw text). Patron 5 de `shared/context-engineering.md`. El
assembled JSON final se persiste al client repo (Fase 2.5) — no se retiene en
context.

---

## Fase 2: Compose assembled JSON

### 2.1 Construir `meta` (no viene de ningun slice)

```javascript
const meta = {
  client_name,         // de intelligence/perfil.md o cliente-CLAUDE.md
  client_slug: slug,
  site_url,            // de cliente-CLAUDE.md S1 (dominio)
  industry,            // de intelligence/perfil.md (snake_case)
  country,             // de cliente-CLAUDE.md S1 (ISO 3166-1 alpha-2 lowercase, ej "mx")
  segment,             // de intelligence/perfil.md o derivado (industry_country, ej "retail_mx")
  date: period + "-01",
  lead,                // operador (userEmail prefix — Fase 0.3)
  period,              // "YYYY-MM"
  generator: {
    toolkit_version: /* leer de package.json root del toolkit. NUNCA hardcodear. */
  }
};
```

**Toolkit version**:

```bash
node -e 'console.log("v" + require("'"${CLAUDE_PLUGIN_ROOT}"'/package.json").version)'
```

### 2.2 Deep-merge slices

El assembled JSON es la union de todos los slices + meta + fallbacks de
intelligence files. Mapping slice → top-level keys:

| Slice | Emite top-level keys |
|---|---|
| `foda.json` | `scoring` (overall, label, maturity_level, pillars, weights, foda, priorities, roadmap) |
| `tech-audit.json` | `diagnostic.{tech_seo, content_coverage, authority, audit_date, degradation}` |
| `history.json` | `history` (audit_date, ga4_traffic, ahrefs_visibility, market_trends, degradation) |
| `ai-audit.json` | `ai_visibility` (audit_date, platforms, citability, queries_with_ai, geo_roadmap, kpis) |
| `competitive.json` | `competitive_enrichment` + `top_content_by_competitor` + `top_content_by_competitor_findings` |
| `benchmarks.json` | `scoring.pillar_breakdowns` (merge dentro de scoring) + `audit_meta` + `degradation` |
| `context.json` | `executive` + `project_data` + `context` (objectives_table, scope_table, journey_stages, personas_table...) + `audit_meta` (merge con benchmarks audit_meta) |
| `action-plan.json` (si existe) | `roadmap`, `access_requirements`, `onboarding_checklist`, `next_steps`, `next_steps_summary` y `scoring.roadmap` (merge dentro de scoring) |

**Merge logic** (NO usar lodash — hacerlo a mano):

```javascript
const assembled = {
  meta,
  ...techAuditSlice,         // emite { diagnostic }
  ...historySlice,           // emite { history }
  ...aiAuditSlice,           // emite { ai_visibility }
  executive: contextSlice.executive,
  project_data: contextSlice.project_data,
  context: contextSlice.context,
  competitive_enrichment: competitiveSlice.competitive_enrichment,
  top_content_by_competitor: competitiveSlice.top_content_by_competitor,
  top_content_by_competitor_findings: competitiveSlice.top_content_by_competitor_findings,
  // foda + benchmarks ambos emiten `scoring` — merge: foda da overall/foda/priorities/roadmap/pillars/weights,
  // benchmarks aporta pillar_breakdowns (sec-13)
  scoring: { ...fodaSlice.scoring, pillar_breakdowns: benchmarksSlice.scoring.pillar_breakdowns },
  // benchmarks + context ambos emiten `audit_meta` — context gana (mas campos), pero preservar
  // industry_p50_pillars + coherence_check de benchmarks
  audit_meta: {
    ...benchmarksSlice.audit_meta,
    ...contextSlice.audit_meta,
    industry_p50_pillars: benchmarksSlice.audit_meta?.industry_p50_pillars,
    coherence_check: benchmarksSlice.audit_meta?.coherence_check,
  },
  ...(benchmarksSlice.degradation ? { degradation: benchmarksSlice.degradation } : {}),
};
```

### 2.3 Action-plan slice (opcional)

Si `action-plan.json` existe + parsea OK:

```javascript
assembled.roadmap = actionPlanSlice.roadmap;                 // sec-16
assembled.access_requirements = actionPlanSlice.access_requirements;  // sec-17
assembled.onboarding_checklist = actionPlanSlice.onboarding_checklist; // sec-18
assembled.next_steps = actionPlanSlice.next_steps;           // sec-19
assembled.next_steps_summary = actionPlanSlice.next_steps_summary;
// Merge scoring.roadmap si el slice lo emite (skill 8/8 puede pisarlo o complementarlo)
if (actionPlanSlice.scoring?.roadmap) {
  assembled.scoring.roadmap = actionPlanSlice.scoring.roadmap;
}
```

Si NO existe Y el Lead pasó `--no-action-plan` (DEV-ONLY bypass):

```javascript
assembled.roadmap = { available: false };
assembled.access_requirements = { available: false };
assembled.onboarding_checklist = { available: false };
assembled.next_steps = [];
assembled.next_steps_summary = null;
// scoring.roadmap puede venir de fodaSlice.scoring.roadmap (legacy) — preservar.
```

(Si NO existe Y el Lead NO pasó `--no-action-plan` → ya STOP'd en Fase 1.1, no se llega acá.)

### 2.4 Intelligence fallbacks (campos NO cubiertos por slices)

Si despues del merge algun campo critico esta vacio + viene de intelligence:

| Campo | Fuente fallback (si slice falta) |
|---|---|
| `meta.industry` | `intelligence/perfil.md` line `industry: ...` |
| `meta.country` | `cliente-CLAUDE.md` S1 |
| `meta.segment` | `intelligence/perfil.md` o `industry + "_" + country` |
| `meta.client_name` | `intelligence/perfil.md` o `cliente-CLAUDE.md` S1 |
| `meta.site_url` | `cliente-CLAUDE.md` S1 |

NUNCA inventar metricas o data SEO. Solo metadata (nombres, URLs, country code)
puede venir de intelligence cuando los slices no la cubren.

**Si ningun fallback resuelve** un campo requerido por `generate-report.js`
(`meta.client_name` es el unico hard requirement), STOP con mensaje claro.

### 2.5 Escribir JSON al client repo (B11 fix v3.37.2)

El assembled JSON se persiste al client repo (no a tmp) para que el Lead pueda
re-render con patches data-side sin re-correr el pipeline completo. Ejemplo de
uso: inyectar SimilarWeb post-fetch, fixear insights manuales, agregar slices
nuevos sin regenerar todo.

```bash
ASSEMBLED_JSON="$HOME/Documents/punto-rojo-clients/{slug}/output/assembled-{period}.json"
mkdir -p "$(dirname "$ASSEMBLED_JSON")"
```

Escribir el assembled JSON con Write tool a `$ASSEMBLED_JSON`.

**Pre-v3.37.2 (legacy)**: el JSON se escribía a `os.tmpdir()` y se borraba en
Fase 6.3 — imposible re-render con patches sin re-correr `/seo-build-report`
completo. Bug B11 (post-prosegur-ar empirical 2026-05-05).

---

## Fase 3: Checkpoint pre-generate

Presentar al Lead:

```
Voy a generar el reporte HTML para {client_name} del periodo {period}.

Slices Phase 8 cargados:
  ✓ foda.json           ({age} dias, {N} priorities)
  ✓ tech-audit.json     ({age} dias, audit_date {ISO})
  ✓ history.json        ({age} dias, {N} meses serie)
  ✓ ai-audit.json       ({age} dias, score citability {X}/10)
  ✓ competitive.json    ({age} dias, {N} competidores)
  ✓ benchmarks.json     ({age} dias, 3 pillars × {scores})
  ✓ context.json        ({age} dias, {N} personas, {N} stages journey)
  {✓|✗} action-plan.json  ({age} dias o "missing — DEV-ONLY bypass via --no-action-plan")

Stale slices (>30 dias): {list o "ninguno"}

Data assembled:
  overall_score: {X}/100
  maturity_level: {Y}
  pillar_breakdowns: 3/3
  intelligence loaded: {Z/3 obligatorios + opcionales}

Salida HTML:    ~/Documents/punto-rojo-clients/{slug}/output/{slug}-diagnostico-{period}.html
Salida JSON:    ~/Documents/punto-rojo-clients/{slug}/output/assembled-{period}.json (persistente — re-render-friendly)

¿Arrancamos la generacion?
[S] Si, generar HTML
[N] No, ajustar algo
[R] Revisar el JSON assembled primero
```

Esperar respuesta explicita. Si `[R]`, hacer `Read` del `$ASSEMBLED_JSON` y
mostrar al Lead antes de repetir el checkpoint.

---

## Fase 4: Generar HTML

### 4.1 Invocar el CLI

Via Bash tool:

```bash
cd "${CLAUDE_PLUGIN_ROOT:-C:/Users/nicko/OneDrive/Escritorio/Proyectos/Punto-Rojo/punto-rojo-claude-toolkit}/report-builder" && \
node generate-report.js \
  --diagnostic-json "$ASSEMBLED_JSON" \
  --client "{slug}" \
  --period "{period}" \
  --json-summary
```

El CLI (B6 fix v3.37.2):
- Escribe el HTML a `~/Documents/punto-rojo-clients/{slug}/output/{slug}-diagnostico-{period}.html`
  (resolve automático con `--client` + `--period`, default `--client-repo-base`
  apunta al repo cliente persistente — ya NO escribe al install path del plugin).
- Override con `--output <path>` para destinos custom (debe vivir dentro de
  `report-builder/` o del client repo base — path traversal rejected).
- Emite mensaje humano a **stderr** (`✅ Report generated: ...`).
- Con `--json-summary`, emite un single-line JSON a **stdout** con
  `{ok, output, size_kb, sections, duration_ms, ...}`.

### 4.2 Parsear resultado

- **Exit code 0 + stdout JSON con `ok: true`** → extraer `output`, `size_kb`,
  `sections`, `duration_ms` y continuar a Fase 5.
- **Exit code != 0 o `ok: false`** → reportar al Lead:
  ```
  ❌ Generacion fallo: {error del stderr}

  El JSON assembled quedo en $ASSEMBLED_JSON para inspeccion + re-render
  con patches data-side.

  ¿Queres que inspeccione el JSON y re-intente? (S/N)
  ```
  Si acepta: Read del `$ASSEMBLED_JSON` + diagnosticar (puede ser un slice con
  shape mal validado por el orquestador). Si no: STOP con el JSON path
  documentado en `actividad.md`.

### 4.3 Validar output

Antes de Fase 5, verificar:

- El archivo existe en la ruta reportada (Bash `test -f`).
- `size_kb > 50` (si el HTML es <50KB algo fallo — un reporte completo supera
  los 300-500 KB por CSS + JS inlined).
- `sections >= 14` (14 secciones IN minimo + algunas placeholder).

Si alguna validacion falla, reportar al Lead y ofrecer re-intentar.

---

## Fase 5: Upload a pr-toolkit (opcional)

### 5.1 Checkpoint al Lead

```
✅ HTML generado: {output_path} ({size_kb} KB, {sections} sections, {duration_ms}ms)

Opciones de distribucion:
  [L] Local only — lo dejas local, lo mandas por email/drive al cliente manualmente
  [U] Upload a pr-toolkit — commit + push, Vercel auto-deploya en ~60s a
      https://pr-toolkit.puntorojo.com/reports/{slug}/{period}
      (auth-gated @puntorojo.com, para equipo interno)

¿Que elegis? (L / U)
```

Si `[L]` local-only → saltar a Fase 6 directamente con el local path.

### 5.2 Preflight checks (si [U])

```bash
PR_TOOLKIT_PATH="${PR_TOOLKIT_PATH:-C:/Users/nicko/OneDrive/Escritorio/Proyectos/Punto-Rojo/pr-toolkit}"

# a. Path existe
[ -d "$PR_TOOLKIT_PATH" ] || { echo "❌ No encuentro pr-toolkit en $PR_TOOLKIT_PATH"; exit 1; }
# b. Es git repo
cd "$PR_TOOLKIT_PATH" && git rev-parse --git-dir
# c. Working tree limpio
DIRTY="$(git status --porcelain)"
# d. Branch activo
PR_TOOLKIT_BRANCH="$(git branch --show-current)"
```

STOP messages:
- **(a) path no existe** → indicar al Lead que setee `$env:PR_TOOLKIT_PATH = "C:\ruta\correcta"` o clone el repo. El HTML local ya esta generado, no se pierde.
- **(b) no es git repo** → "Verificá la ruta — `{PR_TOOLKIT_PATH}` no es un repo git."
- **(c) dirty** (output no vacio) → mostrar `git status --porcelain` y pedir al Lead commit/stash primero. El HTML local ya esta listo mientras tanto.

### 5.3 Copiar HTML al repo

```bash
DEST_DIR="$PR_TOOLKIT_PATH/src/reports/{slug}/{period}"
mkdir -p "$DEST_DIR"
cp "{output_path}" "$DEST_DIR/diagnostico.html"
```

### 5.4 Commit local

```bash
cd "$PR_TOOLKIT_PATH" && \
git add "src/reports/{slug}/{period}/diagnostico.html" && \
git commit -m "feat(reports): add {slug} diagnostic report {period}"
```

Si el commit falla (hook, sign, etc) → reportar el error al Lead sin hacer
`--amend`. Ofrecer diagnosticar manualmente.

### 5.5 CHECKPOINT pre-push (OBLIGATORIO)

**NUNCA pushear sin aprobacion explicita**. Presentar:

```
✅ Commit local creado en pr-toolkit ({PR_TOOLKIT_BRANCH}):
  feat(reports): add {slug} diagnostic report {period}

Siguiente paso: `git push origin {PR_TOOLKIT_BRANCH}` → Vercel detecta + auto-deploya (~60s)
→ URL: https://pr-toolkit.puntorojo.com/reports/{slug}/{period}

¿Hago el push?
[S] Si, pushear ahora
[N] No, lo push-eo yo manualmente mas tarde
```

Esperar respuesta.

### 5.6 Push + Vercel deploy handoff

Si `[S]`:

```bash
cd "$PR_TOOLKIT_PATH" && git push origin "$PR_TOOLKIT_BRANCH"
```

Error handling:
- **Auth failure** (`Permission denied`, `authentication failed`) → reportar:
  ```
  ❌ Push fallo por auth. Opciones:
    1. Verificá `gh auth status` (GitHub CLI)
    2. Verificá tu SSH key (`ssh -T git@github.com`)
    3. Si son creds de Windows Credential Manager, re-logueate

  El commit local esta hecho — cuando resolvás, corré manualmente:
    cd {PR_TOOLKIT_PATH} && git push origin {PR_TOOLKIT_BRANCH}
  ```
- **Non-fast-forward** → reportar que el remote cambio, sugerir
  `git pull --rebase` antes de reintentar.

Si el push exitoso → **NO hacer `sleep`**. Vercel desploya async en ~60-90s; en
vez de bloquear, handoff explícito al Lead con prompt interactivo:

```
✅ Push exitoso — Vercel auto-deploy en curso (~60-90s)

🔗 URL final:  https://pr-toolkit.puntorojo.com/reports/{slug}/{period}
📊 Dashboard:  https://vercel.com/puntorojo/pr-toolkit/deployments

Opciones:
  [S] Ya validé la URL / seguí aunque no la haya abierto — Fase 6
  [W] Esperá vos — reintento el check en ~60s (instrucción: me escribís "listo" cuando quieras avanzar)
  [E] La URL no carga / devuelve error — pasame el síntoma y lo triageamos antes de Fase 6
```

**Reglas de respuesta**:
- `S` → avanzar a Fase 6 inmediatamente.
- `W` o "listo" → avanzar a Fase 6 (el Lead ya esperó).
- `E` + síntoma → NO avanzar a Fase 6. Triage: 404 por deploy todavía en progreso
  (esperar 60s más), 500 por file tracing fallido (revisar
  `next.config.ts > outputFileTracingIncludes`), redirect loop por middleware
  (revisar matcher).

---

## Fase 6: Output al Lead + update actividad.md

### 6.1 Reportar al Lead

```
✅ Reporte generado para {client_name}

🗂  Archivo local: {output_path} ({size_kb} KB, {sections} sections)
🔗 URL (auth-gated): https://pr-toolkit.puntorojo.com/reports/{slug}/{period}     (si hizo upload)
📦 Slices Phase 8 usados:
   • foda ({age}d) · tech-audit ({age}d) · history ({age}d)
   • ai-audit ({age}d) · competitive ({age}d) · benchmarks ({age}d)
   • context ({age}d) · action-plan ({age}d, REQUIRED salvo --no-action-plan dev bypass)

⏱  Render: {duration_ms}ms

Stale slices (>30d): {list o "ninguno"}

**Share-ready**:
- Para clientes externos sin cuenta @puntorojo.com → mandá el archivo local por email/drive
- Para el equipo interno → pasá el URL hosted

**Tips antes de distribuir**:
1. Abrí el HTML local en Chrome y revisá el paginado
2. Validá que los nombres de Lead + equipo coincidan con el cliente actual
3. Si --no-action-plan dev bypass activo — sec-16 a sec-19 muestran placeholders;
   correr /seo-section-action-plan + re-disparar este skill SIN el flag para producción
4. PDF queda queued para un patch futuro

Skill completada. Escribi /context para ver cuanto espacio queda antes de continuar.
```

### 6.2 Update actividad.md

Usar Edit tool sobre `~/Documents/punto-rojo-clients/{slug}/actividad.md`.
Agregar arriba del contenido existente (lo mas reciente primero):

```markdown
## {YYYY-MM-DD} — {operador}

**Qué se hizo:**
- Generé reporte HTML del diagnóstico para período {period} usando 8 slices Phase 8
- {si upload:} Subí a pr-toolkit, URL: https://pr-toolkit.puntorojo.com/reports/{slug}/{period}
- {si local-only:} Dejé local en {output_path} — queda para compartir manual

**Decisiones tomadas:**
- Slices usados: foda, tech-audit, history, ai-audit, competitive, benchmarks, context, action-plan
- {si stale slices:} Slices stale (>30d): {list} — Lead aprobó continuar igual
- {si --no-action-plan dev bypass:} action-plan SKIPPEADO via dev flag — sec-16/19 placeholders

**Pendiente:**
- Validar con cliente los hallazgos del reporte
- {si --no-action-plan dev bypass:} Correr /seo-section-action-plan + re-disparar este skill SIN flag para producción
- {si onboarding pending:} Cerrar items pendientes de onboarding

---
```

Mantener las ultimas 10 entradas — si hay mas, eliminar las mas antiguas.

### 6.3 Persistencia del assembled JSON (B11 fix v3.37.2)

El JSON assembled NO se borra al final del run. Vive persistente en
`~/Documents/punto-rojo-clients/{slug}/output/assembled-{period}.json` para
permitir re-render con patches data-side sin re-correr el pipeline completo.

Casos de uso típicos:
- Inyectar SimilarWeb post-fetch (handoff Prosegur AR pattern).
- Reescribir insights manuales (top channel detection, narrativa per-cliente).
- Agregar slices nuevos / cross-slice patches (ej. strip `<strong>` literal).
- Re-render rápido tras editar 1 sub-campo (vs ~85min de re-pipeline).

Para re-render con patches:
```bash
cd report-builder && \
node generate-report.js \
  --diagnostic-json "$HOME/Documents/punto-rojo-clients/{slug}/output/assembled-{period}.json" \
  --client {slug} \
  --period {period}
```

**No hay limpieza tmp** — pre-v3.37.2 borraba `os.tmpdir()` JSON, comportamiento
deprecado por Bug B11 (post-prosegur-ar empirical 2026-05-05).

---

## Manejo de flags

### `--no-action-plan` (DEV-ONLY — NO USAR EN PRODUCCION)

Skip explicito del slice action-plan. action-plan ya está shipped (v3.35.0) como
slice REQUIRED. Este flag existe SOLO para iteración rápida en desarrollo cuando
el slice todavía no se generó pero querés ver el resto del HTML.

**Comportamiento**:
- Sin la flag + slice existe → flow normal (validate + merge action-plan).
- Sin la flag + slice missing → STOP `"Run /seo-section-action-plan first."` (Fase 1.1).
- Con la flag + slice existe → IGNORA el slice + degrada sec-16/19 a placeholders + warn.
- Con la flag + slice missing → degrada sec-16/19 a placeholders + warn explícito.

**NO USAR en runs productivos**. El HTML entregado al cliente quedará incompleto.

### `--pdf`

Si el Lead invoca con `--pdf`:

```
PDF export aún no está disponible en este release. El HTML está listo ahora y
te lo genero de todas formas. PDF queda queued para un patch futuro —
va a usar Playwright headless contra el HTML generado.

Mientras tanto, dos workarounds rápidos:
  1. Abrir el HTML en Chrome → Ctrl+P → "Save as PDF"
  2. Esperar el patch (sin ETA comprometido todavía)

¿Arranco con HTML ahora? (S/N)
```

Si `[S]` → continuar normalmente (Fase 0). Si `[N]` → STOP.

---

## Error handling (resumen)

| Error | Fase | Accion |
|---|---|---|
| slug/period invalido | 0 | STOP con regex explicit |
| cliente-CLAUDE.md ausente | 0 | STOP — pedir setup del cliente |
| intelligence obligatorio faltante | 0 | Warning + continuar (los slices son la fuente primaria) |
| Required slice missing (incluye action-plan) | 1.1 | STOP — pedir correr `/seo-section-{name}` primero |
| action-plan missing + `--no-action-plan` flag | 1.1 | Warn + continuar (sec-16/19 degradan; DEV-ONLY bypass) |
| Stale slice (>30 dias) | 1.2 | Warn + ask Lead [S]/[N]/[R] |
| Slice falla validator | 1.3 | STOP con `errors[]` — no fixear inline, pedir re-run de la skill afectada |
| meta.client_name no resoluble | 2.4 | STOP — el CLI requiere ese campo (exit code 2) |
| generate-report.js exit != 0 | 4 | Surface stderr + ofrecer inspeccionar `$ASSEMBLED_JSON` (persistente) |
| output <50KB o sections <14 | 4 | Warning + ofrecer re-intento |
| pr-toolkit path no existe | 5 | STOP con instrucciones (env var o clonar) |
| pr-toolkit no es git repo | 5 | STOP |
| working tree dirty | 5 | STOP — pedir commit/stash |
| git commit falla (hook) | 5 | Surface error, NO hacer --amend |
| git push auth failure | 5 | Instrucciones para resolver + commit queda local |
| Lead reporta URL 404 post-push | 5.6 | Esperar 60s mas (deploy en curso) o link a `vercel.com/puntorojo/pr-toolkit/deployments` |
| Lead reporta URL 500 post-push | 5.6 | Probable file tracing fallido — revisar `next.config.ts > outputFileTracingIncludes` |
| Lead reporta redirect loop post-push | 5.6 | Middleware matcher problema — revisar `middleware.ts` |

---

## Reglas generales

- **NUNCA inventes datos**: si un slice no tiene un campo, propagar `{ available: false }` o array vacio. Solo metadata (nombre, country, URL) puede venir de intelligence files cuando los slices no la cubren.
- **Checkpoints obligatorios** (no auto-aprobables): Fase 3 (pre-generate) + Fase 5 (pre-push).
- **Stateless**: cada corrida lee los slices fresh desde disco, no cachea.
- **Single-file output**: el CLI inlinea CSS + JS — share-able por email sin romperse.
- **Auth GSC/GA4**: este skill **no llama** GSC/GA4. Si un slice trae `degradation.{gsc|ga4}` con `oauth_reauth_required`, el reporte degrada esa seccion — el orquestador no redispara reauth.
- **PDF**: queued para patch futuro. No prometer timelines.

---

## MCPs utilizados + costos

Este orquestador es **file system + 1 CLI call**. Solo built-in tools:

- **Read** — cliente-CLAUDE, actividad, intelligence files, slices JSON.
- **Bash** — `test -f`, `stat`, validator inline, mkdir, node CLI, git.
- **Write** — assembled JSON persistente al client repo.
- **Edit** — actividad.md (prepend entry en Fase 6).

**NO usar** (toda esa data ya vive en los slices upstream): `diagnostic-mcp`,
`memory-mcp`, Ahrefs / GSC / GA4 / DataForSEO MCPs, Sheets, ClickUp.

**Costos**: **$0** (0 Ahrefs units, 0 GSC/GA4 calls, 0 DataForSEO units). El
costo real se pago al correr las 7-8 skills `/seo-section-*` previas. Re-ejecutar
este skill cuesta segundos + $0.

---

## Diferencia vs otros skills

Las 8 skills `/seo-section-*` (Phase 8) **producen los slices**. Este skill
**los compone**. `/seo-reporte` hace queries ad-hoc y resuelve findings — son
complementarios, no overlapping.

Flujo tipico:

```
/seo-section-foda → tech-audit → history → ai-audit → competitive → benchmarks
→ context [→ action-plan]
→ /seo-build-report → entregar al cliente
```

**Contexto historico (Phase 8 split)**: pre-Phase 8 este skill consumia
`consolidated_json` del backend (`diagnostic-mcp`) + hacia enrichment Ahrefs
inline + reproducia logica de `/seo-scoring`. Ese diseño quedo deprecado: las
skills `/seo-section-*` pre-computan + persisten cada slice, y este orquestador
solo compone. La ventaja: re-ejecutar el reporte es $0 + segundos, y cada slice
se puede regenerar/iterar independientemente.

---

## Context window management

Patrones aplicados (`shared/context-engineering.md`): Patron 5 (process-and-discard
slices despues de leer cada uno) + Patron 6 (backend pre-computation: toda la
data pesada ya vive en los slices). Budget total: ~20-25 tool responses, sin
riesgo de compactacion.

---

## References

- **CLI**: `report-builder/generate-report.js` (entry point — input/output contract)
- **Sample shape**: `report-builder/samples/chedraui-sample.json` (estructura target del assembled JSON)
- **Slice samples**: `report-builder/samples/sections/{foda,tech-audit,history,ai-audit,competitive,benchmarks,context}.json`
- **Validators (cero deps, validan W3.4 contract)**:
  - `report-builder/lib/foda-validator.js` — `validateFodaSlice`
  - `report-builder/lib/tech-audit-validator.js` — `validateTechAuditSlice`
  - `report-builder/lib/history-validator.js` — `validateHistorySlice`
  - `report-builder/lib/ai-audit-validator.js` — `validateAiAuditSlice`
  - `report-builder/lib/competitive-validator.js` — `validateCompetitiveSlice`
  - `report-builder/lib/benchmarks-validator.js` — `validateBenchmarksSlice`
  - `report-builder/lib/context-validator.js` — `validateContextSlice`
- **Schema W3.4**: `docs/superpowers/specs/schemas/w3.4-diagnostic-data.schema.json`
- **pr-toolkit repo**: `C:\Users\nicko\OneDrive\Escritorio\Proyectos\Punto-Rojo\pr-toolkit\` (Next.js app, Vercel auto-deploy)
- **Skills upstream (Phase 8)**: `skills/seo-section-{foda,tech-audit,history,ai-audit,competitive,benchmarks,context,action-plan}/`
