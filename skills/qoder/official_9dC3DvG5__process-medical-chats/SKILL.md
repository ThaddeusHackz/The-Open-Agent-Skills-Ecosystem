---
name: process-medical-chats
description: Processa Chats_Raw médicos em notas Wiki_Medicina usando med_ops.py, subagents, validação formal, publish dry-run e linker semântico. Use com /mednotes:process-chats.
---

# Skill: process-medical-chats

Workflow: `docs/workflows/process-chats.md`.
Contratos: `docs/reference/json-contracts.md`.
Resposta: `knowledge/workflow-output-contract.md`.

Use para processar `Chats_Raw` em notas `Wiki_Medicina` ou continuar
`/mednotes:process-chats`.

## Fontes

- CLI pública: `${extensionPath}/scripts/mednotes/med_ops.py`.
- Taxonomia: `${extensionPath}/scripts/mednotes/wiki_tree.py`,
  `taxonomy-canonical`, `taxonomy-tree`, `taxonomy-audit`.
- Estilo: `${extensionPath}/knowledge/knowledge-architect.md`.
- Linker: `${extensionPath}/knowledge/semantic-linker.md`,
  `med_ops.py run-linker`.
- Ownership: `docs/reference/context-ownership.md`.

## Invariantes

- Nunca edite YAML/status de raw chat manualmente; use `med_ops.py`.
- Mutação compartilhada é serial no agente principal: `triage`, `discard`,
  `stage-note`, catálogo, dry-run, publish, linker.
- Paralelize só `work_items`; `batches` apenas agrupam `work_ids`.
- Próxima ação limitada autoriza só aquela fase.
- Bloqueio recuperável preserva `error_context`; subagent de reparo recebe
  causa, artefato, correção, `retry_scope` e `next_action`.
- Run de agente registra `agent_events` redigidos para retry/loop, fase errada,
  `next_action` ignorado, drift, mutação inesperada, bloqueio ou comando falho.
- Python/uv/venv/PowerShell/path Windows quebrado é
  `environment_blocker.windows_path_or_venv`: rode `/mednotes:setup` ou
  bootstrap/reset oficial; não edite scripts/runbooks para contornar ambiente.
- Decisão humana usa `human_decision_packet`; resolva e retome por
  `resume_action` antes de publish.
- `note_plan` é da triagem. O architect escreve
  todas as notas `create_note` planejadas pela triagem, somente elas, e gera
  `raw-coverage.v1`.
- `publish-batch` bloqueia sem `coverage_path`, raw sem `note_plan`, coverage
  divergente, staged fora do plano ou alvo duplicado por normalização.
- Merge multi-fonte usa `raw_files[]`/`sources[]`; `covered` exige
  delta/seção/referência. Falta vira `provenance_gap`.
- HTML salvo por `gemini-md-export` é obrigatório, iframe/linkado; nunca inline
  HTML.
- Sempre rode `publish-batch --dry-run`; publish real exige recibo compatível e
  rollback automático em falha pós-mutação.
- Rode linker/grafo uma vez ao final.
- Dry-run limpo é `ready_to_publish`, publish real é `published`, linker com
  blockers é `completed_with_link_blockers`; não chame de `completed`.
- Taxonomia é pasta de categoria; `title` vira o arquivo `.md`.

## Fluxo

1. Ache `${extensionPath}`; fallback:
   `~/.gemini/extensions/medical-notes-workbench`.
2. Valide e carregue taxonomia:

   ```bash
   uv run python "${extensionPath}/scripts/mednotes/med_ops.py" validate
   uv run python "${extensionPath}/scripts/mednotes/wiki_tree.py" --max-depth 4 --audit --format text
   ```

   Se `environment_preflight.status=blocked`, pare com setup/reset oficial
   antes de ler/mutar Wiki. Se o usuário pedir organização prévia, use
   `taxonomy-migrate --dry-run`; aplique só com confirmação e
   `--rollback --receipt <recibo.json>`.
3. Oriente backlog com `list-pending --summary` e `list-triados --summary`.
4. Pendentes: `plan-subagents --phase triage --limit <N>`. Default 5; use 2/3
   em modo econômico. Lance no máximo um triager por `work_item.raw_file`;
   aplique em série `triage --note-plan <note-plan.json>` ou `discard`.
5. Triados: `plan-subagents --phase architect --temp-root <tmp> --limit <N>`.
   Um architect por `work_item` com raw(s), `temp_dir`, plano, taxonomia, árvore
   e catálogo; escreve só no `temp_dir`. `canonical_merge` usa um architect por
   `target_key`; `canonical_merge_required`/ambiguidade bloqueiam para revisão
   ou decisão humana, sem nota paralela.
6. Valide temporárias com `validate-note`; se `requires_llm_rewrite`, passe
   `rewrite_prompt` e `error_context` ao architect, máximo 2 tentativas. Use
   `fix-note` só para YAML/erros determinísticos. Confira cobertura
   informacional.
7. Manifest único: `stage-note --coverage <coverage.json>`. Não edite manifest.
   Sem proveniência multi-fonte, bloqueie como `provenance_gap`.
8. Rode `med-catalog-curator`, depois `publish-batch --manifest <manifest> --dry-run`.
   Chame `med-publish-guard`; publique só com `approve`.
9. Rode `publish-batch` real uma vez e, ao final do lote, `run-linker`. Com
   blockers de grafo/linker, próxima ação: `/mednotes:fix-wiki --dry-run`.
10. Registre feedback local quando possível, incluindo `agent_events` e
    bloqueios de ambiente. Responda por `workflow-output-contract.md` com
    status real e sem JSON bruto.

## Paralelização

- Unidade indivisível: raw chat, nota temporária ou nota final.
- Fonte única de spawn: `work_items`; não processe `batches` como segunda fila.
- Um raw com várias notas continua com um architect; merge canônico usa
  ownership por `target_key`.
- Todo `create_note` aparece em coverage/manifest; toda staged note aparece no
  `note_plan`.
- `plan-subagents --phase architect` agrupa duplicata simples em
  `canonical_merge`; o resto bloqueia antes de gastar tokens.
- Com 0/1 item, não crie paralelismo artificial.
- Se `truncated: true`, termine a fase atual antes de novo lote.
