---
name: dashboard-auto-onboarder
description: "Auto-detect novos mecanismos autônomos (nova skill, novo agent, novo hook, novo MCP server, nova métrica claude_* exposta pelo exporter) e auto-cria panel no dashboard `autonomous-mechanisms.yaml` em infra-platform via PR. Trigger phrases — \"novo mecanismo no dashboard\", \"auto-onboard\", \"panel pra <metric>\", \"auto-add dashboard panel\". Cravado 2026-04-30 — Lucas: \"todo novo mecanismo tem que ser automaticamente implementado nesse dash\". Roda via cron weekly + on-demand. Detecta gap entre métricas expostas pelo exporter (port 9090) e panels presentes no dashboard. Para cada métrica claude_* sem panel: gera panel JSON via template + abre PR auto-merge em infra-platform. Catalog em `~/.claude/lince/dashboard-onboarding-history.jsonl`."
version: 1.0.1
---

# dashboard-auto-onboarder

Auto-onboard mecanismos autônomos novos no dashboard `autonomous-mechanisms.yaml`. Fecha o loop "criei skill nova → ela aparece no dashboard sem human action".

## Trigger

Auto-fire quando:
- Cron weekly (Sun 03:13 via `com.claude.dashboard-onboarder-weekly.plist`)
- User diz "novo mecanismo no dashboard", "auto-onboard panel"
- Hook detecta nova métrica `claude_*` no exporter scrape OU nova entrada em `~/.claude/skills/_manifest.jsonl` etc.

## Protocolo (script `~/.claude/scripts/dashboard_auto_onboard.sh`)

```bash
1. Curl http://localhost:9090/metrics | grep "^# TYPE claude_" → list de métricas atuais
2. Parse infra-platform/observability/grafana-dashboards/autonomous-mechanisms.yaml → list de exprs em panels
3. Diff: métricas expostas SEM panel correspondente
4. Para cada gap:
   a. Lookup template panel em `~/.claude/lince/templates/panel-by-type.json` (counter→stat+timeseries, gauge→stat, histogram→heatmap)
   b. Gerar panel JSON com expr + title + gridPos auto-incremento
   c. Patch dashboard JSON inserindo panel
5. Se mudanças → branch claude/auto-onboard-<metric>-<date>, commit, push, PR auto-merge em infra-platform
6. Append ~/.claude/lince/dashboard-onboarding-history.jsonl
```

## Catalog template format

`~/.claude/lince/templates/panel-by-type.json`:
```json
{
  "counter": {
    "type": "timeseries",
    "expr_template": "sum(rate({metric}[1h]) * 3600)",
    "title_template": "{metric} per hour"
  },
  "gauge": {
    "type": "stat",
    "expr_template": "{metric}",
    "title_template": "{metric} (current)"
  },
  "histogram": {
    "type": "timeseries",
    "expr_template": "histogram_quantile(0.99, sum(rate({metric}_bucket[5m])) by (le))",
    "title_template": "{metric} p99"
  }
}
```

## T1/T2/T3

- T1: detect novo metric + abrir PR draft auto-merge se simples (counter/gauge sem labels custom)
- T2: histogram + métrica com 3+ labels → PR draft sem auto-merge (humano review template)
- T3: nunca aplicado — esta skill só PROPOE, não merge produção sem CI green

## Anti-patterns

- ❌ Pular kustomization.yaml registration (panel novo não carrega)
- ❌ Auto-onboard métrica deprecated (verificar se tem `# DEPRECATED` no comment do exporter)
- ❌ Loop infinito de re-onboarding (max_attempts=3 per gap_id em `dashboard-onboarding-history.jsonl`)

## Persuasion

Authority: Lucas cravou 2026-04-30 — "todo novo mecanismo tem que ser automaticamente implementado nesse dash com mecanismo automatico". Esta skill fecha o loop sem human review pra cada nova skill/agent/exporter.

Loss aversion: sem auto-onboard, dashboard fica desatualizado entre adições, criando gap entre "mechanism existe" e "mechanism observable".

## Reference paths

- Dashboard target: `infra-platform/observability/grafana-dashboards/autonomous-mechanisms.yaml`
- Cron: `~/Library/LaunchAgents/com.claude.dashboard-onboarder-weekly.plist`
- Script: `~/.claude/scripts/dashboard_auto_onboard.sh`
- Catalog: `~/.claude/lince/dashboard-onboarding-history.jsonl`
- Templates: `~/.claude/lince/templates/panel-by-type.json`
