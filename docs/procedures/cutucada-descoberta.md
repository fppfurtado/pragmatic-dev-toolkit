# Cutucada de descoberta

Procedimento compartilhado executado em runtime pelas 5 skills com `roles.required` (`/triage`, `/run-plan`, `/new-adr`, `/next`, `/draft-idea`) antes de devolver controle. Skills consumidoras leem este arquivo via Read e executam o algoritmo abaixo. Categoria `docs/procedures/` estabelecida em [ADR-024](../decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md). Decisões canonical: [ADR-017](../decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) (mecânica original — string-A) e [ADR-029](../decisions/ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md) (extensão para `CLAUDE.md` ausente — string-B).

A cutucada surfa proativamente o caminho `/init-config` em projetos onde o bloco `<!-- pragmatic-toolkit:config -->` está fora de uso (CLAUDE.md ausente ou presente sem o marker).

## Gating tri-state

| Estado | Ação |
|---|---|
| `CLAUDE.md` ausente + string-B não aparece no contexto visível desta conversa CC | Emitir **string-B** como última linha do relatório |
| `CLAUDE.md` presente + `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna não-zero (marker ausente) + string-A não aparece no contexto visível | Emitir **string-A** como última linha do relatório |
| `CLAUDE.md` presente com marker **OR** dedup hit na string aplicável | Suprimir silenciosamente |

Dedup é **por string** (conversation-scoped, alinhado com [ADR-010](../decisions/ADR-010-instrumentacao-progresso-skills-multi-passo.md)). String-A e string-B observam o contexto visível independentemente — transição `ausente → presente-sem-marker` mid-session pode emitir string-A mesmo após string-B já ter aparecido na mesma sessão, porque o gating de dedup é por string distinta (não por presença genérica de cutucada).

## Strings canonical

(em PT-BR per toolkit canonical; literal text reproduzido idêntico aqui — sites consumidores referenciam este procedure em vez de inlinar as strings)

- **string-A** — `CLAUDE.md` presente sem marker:

  > Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.

- **string-B** — `CLAUDE.md` ausente:

  > Dica: este projeto não tem `CLAUDE.md`. Crie o arquivo e rode `/init-config` para configurar os papéis do plugin.

## Posicionamento da emissão

Última linha do relatório final da skill, após qualquer outra saída (commit, push, sugestão de próximo passo). Skills com `roles.informational` apenas (sem `roles.required`) **não** emitem a cutucada — escopo restrito às 5 listadas acima (escopo + regra de herança editorial em `CLAUDE.md` → `## Cutucada de descoberta`).
