# Backlog

## Próximos

- /triage: push automático pós-commit não é executado de forma confiável — verificar condições de disparo

## Em andamento

- /run-plan: captura automática de bloqueios em pré-condição de worktree (fase anterior ao loop de arquivos)

## Concluídos

- /run-plan: sugerir push e abertura de PR ao final, além do commit (quando aplicável)
- /run-plan + philosophy.md: distinguir capturas de validação (plano) de capturas de feature/correção (backlog) na regra de captura automática

- /triage + /run-plan: merge artifact eliminado — triage empurra main ao remote após commit; run-plan bloqueia se main estiver à frente do remote com Em andamento no backlog
- /triage: guarda explícita contra inclusão de BACKLOG.md em ## Arquivos a alterar — transições gerenciadas pelo campo Linha do backlog
- /run-plan: condição de skip do sanity check de docs (4.3) restrita a padrões user-facing (positive list: README*, CHANGELOG*, install.md, docs/guides/**)
- skill /next: orientação de sessão — analisa backlog, verifica implementados e sugere top 3 por impacto; /triage delega a /next quando invocada sem argumento
- /run-plan: refinar sanity check de documentação no passo 4.3
- release: colapsar gates de version_files, changelog e commit/tag num único review final consolidado
- captura automática de imprevistos durante /run-plan e validação manual
- backlog: transições de estado automáticas sem cutucada ao operador
