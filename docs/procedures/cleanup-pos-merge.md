# Cleanup pós-merge

Procedimento compartilhado executado em runtime por `/triage` (passo 0) e `/release` (antes das pré-condições). Skills consumidoras leem este arquivo via Read e executam o algoritmo abaixo. Categoria `docs/procedures/` estabelecida em [ADR-024](../decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md).

Antes de carregar contexto, varrer worktrees mergeadas em `.worktrees/` e oferecer cleanup. Skip silente quando nada a limpar; nunca incomoda no caminho-comum.

## Detecção de candidatos

1. `git worktree list --porcelain` → filtrar entradas cujo `worktree` está sob `.worktrees/` (excluir worktree principal).
2. Para cada candidato, extrair branch (`branch refs/heads/<slug>` da saída porcelain).
3. Verificar merge status: `gh pr list --state merged --head <branch> --json number --jq '.[0].number'` (squash-aware). Saída numérica → mergeado, capturar PR number. Saída vazia / `gh` ausente → fallback `git branch -r --merged origin/<main>` checando se `<branch>` está listada (perde squash). Sem detecção em nenhum dos dois → não é candidato; pular.
4. Lista de candidatos mergeados vazia → **skip silente**; segue para o passo 1.

## Cutucada por candidato

Para cada candidato, `AskUserQuestion`:

- `header`: `Cleanup`
- `question`: `"Worktree '<slug>' (PR #<num> mergeado): limpar o quê?"` (omitir `PR #<num>` no fallback git-only)
- `multiSelect`: `true`
- Opções:
  - `Worktree` — `description`: `"git worktree remove .worktrees/<slug>"`
  - `Branch local` — `description`: `"git branch -d <slug>; squash detectado força -D com nota"`
  - `Branch remota` — `description`: `"git push origin --delete <slug>"`

Sem seleção (todas desmarcadas + confirmar) → skip esse candidato; segue para o próximo.

## Execução das seleções

Ordem importa para isolamento — `worktree remove` antes de `branch -d` (worktree em uso bloqueia delete). Ordem padrão: Worktree → Branch local → Branch remota.

- `Branch local`: tentar `git branch -d <slug>` primeiro. Falha com "not fully merged" → executar `git branch -D <slug>` e reportar `"branch <slug> não mergeada via fast-forward — squash detectado via gh; usando -D"` (caso real para PRs squash-merged onde ancestry local não bate).
- `Branch remota`: tentar `git push origin --delete <slug>`. Falha com `remote ref does not exist` no stderr → branch já estava apagada no remoto (auto-delete pós-merge do GitHub, etc.); reportar `"branch <slug> já estava apagada no remoto"` e seguir.
- Falha em qualquer comando após o primeiro → reportar erro literal e parar (sem `--force` adicional, sem retry). Comandos já executados permanecem aplicados; operador resolve o resto manual.

## Após todos os candidatos

`git fetch origin --prune` para limpar refs remotos órfãos.
