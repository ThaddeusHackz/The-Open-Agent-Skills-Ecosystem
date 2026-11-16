---
name: fix-medical-wiki
description: Audita e corrige a saude da Wiki_Medicina com fix-wiki, taxonomia, reescritas controladas, graph-audit e linker. Use com /mednotes:fix-wiki.
---

# Skill: fix-medical-wiki

Workflow: `docs/workflows/fix-wiki.md`.
Contratos JSON: `docs/reference/json-contracts.md`.
Resposta: `knowledge/workflow-output-contract.md`.

Use para auditoria/preview/reparo em lote da `Wiki_Medicina`: hierarquia,
taxonomia, estilo, YAML, reescritas necessárias e grafo.

## Fontes

- Estilo: `${extensionPath}/knowledge/knowledge-architect.md`.
- CLI pública: `${extensionPath}/scripts/mednotes/med_ops.py` (alias fino para
  `wiki.cli`; lógica em `wiki.api` e módulos `wiki.*`).
- Taxonomia/grafo/linker: orquestrados por `med_ops.py fix-wiki`; a lógica
  real fica em `wiki.health`, `wiki.graph_fixes`, `wiki.taxonomy.migration` e
  `wiki.linking`.
- Reescrita/merge LLM: `med-knowledge-architect` só quando CLI pedir
  `requires_llm_rewrite` ou `duplicate_merge_required`.

## Fluxo

1. Ache `${extensionPath}` e `<med_ops.py>`.
2. Modo padrão do slash command: repare com backup:

   ```bash
   uv run python "<med_ops.py>" fix-wiki --apply --backup --json
   ```

   Com `/mednotes:fix-wiki --dry-run` ou pedido de preview:

   ```bash
   uv run python "<med_ops.py>" fix-wiki --dry-run --json
   ```

   Respeite o `wiki_dir` resolvido pelo GEMINI.md persistente; `--wiki-dir`,
   `MED_WIKI_DIR` e config legado só devem ser usados quando explícitos.
3. Interprete `status`, `next_command`, `rollback_command`,
   `human_decision_required`, blockers, rewrites, backups, higiene e
   grafo/linker. Campos completos ficam em `docs/reference/json-contracts.md`.
4. Com `write_error_count > 0`, trate como IO bloqueado: diga que o linker real
   foi pulado por `linker_skipped_reason: write_errors`, mostre exemplos e peça
   liberar iCloud/Obsidian/antivírus/processo antes de retentar.
5. Repita só se `next_command` vier preenchido. Se
   `human_decision_required=true`, pare e mostre `human_decisions`; não improvise
   renome semântico ou deleção.
6. Se houver reescrita LLM:

   ```bash
   uv run python "<med_ops.py>" plan-subagents --phase style-rewrite --max-concurrency 3 --temp-root <tmp-rewrites>
   ```

   Use um `med-knowledge-architect` por `work_item.target_path`; o subagent
   escreve só em `temp_output`.
7. Dry-run de cada rewrite:

   ```bash
   uv run python "<med_ops.py>" apply-style-rewrite --target <nota.md> --content <temp.md> --dry-run --json
   ```

   Aplique só se `validation.errors` vazio.
8. Aplicação real:

   ```bash
   uv run python "<med_ops.py>" apply-style-rewrite --target <nota.md> --content <temp.md> --backup --json
   ```

   Use `--backup`; limite 2 tentativas por nota; nunca rode duas reescritas da
   mesma nota em paralelo.
9. Se `blocker_resolution.groups` trouxer `duplicate_merge_required`, não pare
   no primeiro `fix-wiki`. Planeje merges:

   ```bash
   uv run python "<med_ops.py>" plan-subagents --phase duplicate-merge --max-concurrency 3 --temp-root <tmp-merges>
   ```

   Use um `med-knowledge-architect` por `work_item.group_id`. Payload completo
   vem só de `work_items`; `batches[].work_ids` apenas escolhe a rodada.
10. Valide cada merge:

    ```bash
    uv run python "<med_ops.py>" apply-duplicate-merge --plan <plan.json> --group-id <id> --content <merged.md> --dry-run --json
    ```

    Aplique automaticamente só se não houver `validation_errors`,
    `human_decision_required=false` e nenhum conflito `images_*`:

    ```bash
    uv run python "<med_ops.py>" apply-duplicate-merge --plan <plan.json> --group-id <id> --content <merged.md> --backup --json
    ```

    O apply valida hashes, título, contrato Wiki, provenance e faz rollback se
    falhar depois de começar a mutar.
11. Após rewrites/merges aceitos, revalide:

    ```bash
    uv run python "<med_ops.py>" fix-wiki --apply --backup --json
    ```

12. Se `taxonomy_action_required` persistir, movimentos seguros já foram feitos;
    falta decisão humana/semântica. Use `human_decisions`,
    `blocker_resolution.groups` e `rollback_command`.
13. Backups `.bak`/`.rewrite` devem ser arquivados fora do vault em
    `~/.gemini/backup_archive/fix-wiki/<data>/<run_id>/...`; confira higiene e
    cleanup antes de concluir. A política central mantém até 5 backups por
    arquivo e exclui qualquer backup com mais de 30 dias.
14. Responda por `workflow-output-contract.md`: status, contagens, arquivos,
    rewrites, links, backups, blockers, hierarquia e próxima ação. Em revisão,
    confira: há bloqueio antes de mutar?

## Limites

- Não edite YAML/status de raw chats.
- Não publique notas.
- Não use regex manual para links; use `fix-wiki`, grafo/linker ou
  `/mednotes:link`.
- Não escreva manualmente sobre a Wiki; use `fix-wiki` ou
  `apply-style-rewrite`/`apply-duplicate-merge`.
- Não mova pastas manualmente; hierarquia é `taxonomy-migrate` com plano,
  recibo e rollback, orquestrado pelo `fix-wiki` quando determinístico.
