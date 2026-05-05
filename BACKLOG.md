# Backlog

## Próximos

- /run-plan: sugerir push e abertura de PR ao final, além do commit (quando aplicável)
- /run-plan + philosophy.md: distinguir capturas de validação (plano) de capturas de feature/correção (backlog) na regra de captura automática

## Em andamento

## Concluídos

- /triage + /run-plan: merge artifact eliminado — /triage grava sempre em Próximos; Próximos→Em andamento passa a ser responsabilidade exclusiva do /run-plan no branch da feature
- /triage: guarda explícita contra inclusão de BACKLOG.md em ## Arquivos a alterar — transições gerenciadas pelo campo Linha do backlog
- /run-plan: condição de skip do sanity check de docs (4.3) restrita a padrões user-facing (positive list: README*, CHANGELOG*, install.md, docs/guides/**)
- skill /next: orientação de sessão — analisa backlog, verifica implementados e sugere top 3 por impacto; /triage delega a /next quando invocada sem argumento
- /run-plan: refinar sanity check de documentação no passo 4.3
- release: colapsar gates de version_files, changelog e commit/tag num único review final consolidado
- captura automática de imprevistos durante /run-plan e validação manual
- backlog: transições de estado automáticas sem cutucada ao operador
