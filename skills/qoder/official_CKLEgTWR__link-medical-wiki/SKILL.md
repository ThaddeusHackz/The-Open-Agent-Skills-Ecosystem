---
name: link-medical-wiki
description: Roda o linker semântico da Wiki_Medicina com dry-run auditável, catálogo CATALOGO_WIKI.json e aplicação controlada. Use com /mednotes:link.
---

# Skill: link-medical-wiki

Resumo canônico do workflow: `docs/workflows/link.md`.
Resposta ao usuário: `knowledge/workflow-output-contract.md`.

## Quando usar

Use quando o usuário pedir para interconectar notas da `Wiki_Medicina`, rodar o
linker semântico, atualizar links internos ou linkar uma nota recém-criada.

## Fontes de verdade

- CLI pública: `${extensionPath}/scripts/mednotes/med_ops.py run-linker`
  (alias fino para `wiki.cli`; wrapper interno em `wiki.linking`).
- Implementação de baixo nível/compat: `${extensionPath}/scripts/mednotes/med_linker.py`.
- Regras semânticas: `${extensionPath}/knowledge/semantic-linker.md`.
- Saída visível: `${extensionPath}/knowledge/workflow-output-contract.md`.

## Fluxo

1. Localize `${extensionPath}` e `${extensionPath}/scripts/mednotes/med_ops.py`.
2. Use o `wiki_dir` do GEMINI.md persistente como destino normal. `--wiki-dir`
   é override explícito; `--catalog-path`/`--config` ajustam catálogo ou
   compatibilidade. O catálogo configurado é a fonte primária de vocabulário.
3. Rode dry-run auditável primeiro pelo wrapper público:

   ```bash
   uv run python "${extensionPath}/scripts/mednotes/med_ops.py" run-linker --dry-run --json
   ```

4. Revise links planejados/reescritos, índice, catálogo, warnings e blockers.
   Trate `phase`, `status`, `blocked_reason`, `next_action`,
   `required_inputs` e `human_decision_required` como contrato do wrapper.
5. Se o dry-run estiver coerente e sem blockers, aplique:

   ```bash
   uv run python "${extensionPath}/scripts/mednotes/med_ops.py" run-linker --json
   ```

6. Responda usando `workflow-output-contract.md`, sem despejar JSON bruto.

## Limites

- Não use regex manual para linkar notas.
- Não atualize `CATALOGO_WIKI.json` com aliases genéricos.
- Não publique chats nem corrija estilo/YAML/taxonomia; este skill só linka
  conteúdo já existente.
