# Cleanup pós-merge

Procedimento compartilhado executado em runtime por `/triage` (passo 0) e `/release` (antes das pré-condições). Skills consumidoras leem este arquivo via Read e executam o algoritmo abaixo. Categoria `docs/procedures/` estabelecida em [ADR-051](../decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c).

Antes de carregar contexto, executar 2 algoritmos de cleanup pós-merge complementares: (1) varrer worktrees mergeadas em `.worktrees/` e oferecer cleanup (seções "Detecção de candidatos" → "Após todos os candidatos" abaixo); (2) detectar ADRs órfãos no `decisions_dir` resolvido — drive-sync (rclone bisync ou equivalente) em máquina secundária pode ressuscitar arquivos arquivados pós-merge (seção "Detecção de ADRs órfãos no decisions_dir" no fim). Skip silente quando nada a limpar em qualquer dos dois; nunca incomoda no caminho-comum.

## Detecção de candidatos

1. `git worktree list --porcelain` → filtrar entradas cujo `worktree` está sob `.worktrees/` (excluir worktree principal).
2. Para cada candidato, extrair branch (`branch refs/heads/<slug>` da saída porcelain).
3. Verificar merge status. Detectar forge seguindo `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`; output discrimina policy local:
   - Output `gh` → `gh pr list --state merged --head <branch> --json number --jq '.[0].number'` (squash-aware). Saída numérica → mergeado, capturar PR number (identificador `PR #<num>`).
   - Output `glab` → `glab mr list --merged --source-branch <branch> --output json | jq -r '.[0].iid // empty'` (squash-aware). Saída numérica → mergeado, capturar MR IID (identificador `MR !<num>`).
   - Output `no-detection` (CLI ausente em host mapeado, ou jq ausente em GitLab path) → candidato **silenciosamente pulado** (não cai em fallback git-only — operador instala dependência ou remove CLI do PATH para forçar caminho desejado).
   - Output `unsupported-host` (Bitbucket, Codeberg, host customizado, ou sem remote) → fallback `git branch -r --merged origin/<main>` checando se `<branch>` está listada (perde squash; identificador omitido — sem `PR #` / `MR !`).
   - Sem detecção em nenhum dos modos → não é candidato; pular.
4. Lista de candidatos mergeados vazia → **skip silente**; retorna controle à skill consumidora.

## Cutucada por candidato

Para cada candidato, `AskUserQuestion`:

- `header`: `Cleanup`
- `question`: `"Worktree '<slug>' (<identificador> mergeado): limpar o quê?"` — `<identificador>` é `PR #<num>` (GitHub via `gh`) ou `MR !<num>` (GitLab via `glab`); omitir parêntese inteiro no fallback git-only.
- `multiSelect`: `true`
- Opções:
  - `Worktree` — `description`: `"git worktree remove .worktrees/<slug>"`
  - `Branch local` — `description`: `"git branch -d <slug>; squash detectado força -D com nota"`
  - `Branch remota` — `description`: `"git push origin --delete <slug>"`

Sem seleção (todas desmarcadas + confirmar) → skip esse candidato; segue para o próximo.

## Execução das seleções

Ordem importa para isolamento — `worktree remove` antes de `branch -d` (worktree em uso bloqueia delete). Ordem padrão: Worktree → Branch local → Branch remota.

- `Branch local`: tentar `git branch -d <slug>` primeiro. Falha com "not fully merged" → executar `git branch -D <slug>` e reportar `"branch <slug> não mergeada via fast-forward — squash detectado via gh/glab; usando -D"` (caso real para PRs/MRs squash-merged onde ancestry local não bate).
- `Branch remota`: tentar `git push origin --delete <slug>`. Falha com `remote ref does not exist` no stderr → branch já estava apagada no remoto (auto-delete pós-merge do GitHub/GitLab, etc.); reportar `"branch <slug> já estava apagada no remoto"` e seguir.
- Falha em qualquer comando após o primeiro → reportar erro literal e parar (sem `--force` adicional, sem retry). Comandos já executados permanecem aplicados; operador resolve o resto manual.

## Após todos os candidatos

`git fetch origin --prune` para limpar refs remotos órfãos.

## Detecção de ADRs órfãos no decisions_dir

Pós-merge de uma onda que arquiva ADRs via `git mv` para `<decisions_dir>/archive/`, drive-sync (rclone bisync ou equivalente) em máquina secundária pode re-introduzir a versão pré-archive no path canonical como untracked. Próxima invocação que dependa do `decisions_dir` (`/run-plan` setup, `/new-adr` numbering, auditoria de inventário) pode bloquear ou produzir saldo inconsistente. Algoritmo de detecção complementa o cleanup de worktrees acima — investigação primária da causa-raiz (filters/excludes de drive-sync) vive fora do toolkit.

1. **Resolver papel `decisions_dir`** via Resolution protocol (canonical `docs/decisions/`, modo `local` `.claude/local/decisions/`, ou custom declarado em `paths.decisions_dir`).

2. **Detectar órfãos:** `git status --porcelain` e filtrar por pattern `^\?\? <decisions_dir-resolvido>/ADR-` (ADRs untracked no path resolvido). Em modo `local` (`paths.decisions_dir: local`), `.claude/local/decisions/` é gitignored — `git status --porcelain` não emite entries para paths gitignored, então grep retorna vazio sempre; skip silente automático sem branch especial.

3. **Sem matches → skip silente.** Retorna controle à skill consumidora.

4. **Com matches → aviso informativo listando filenames concretos** (não apenas count). Operador vê os paths reais e reconhece se algum é ADR válido recém-criado via `/new-adr` em sessão prévia (mitigação edge case `/new-adr` cross-turn — paralelo ao pattern cutucada-com-referrer concreto do `/run-plan` §3.3). Formato do aviso: `"<N> ADR(s) órfão(s) detectado(s) — drive-sync ressuscitou pós-archive? Filenames: <path1>, <path2>, ..."`.

5. **Cutucada batched** via `AskUserQuestion`:
   - `header`: `ADR órfão`
   - `question`: `"<N> ADR(s) órfão(s) detectado(s) — como resolver?"`
   - Opções (sem `(Recommended)` — default estatisticamente instável com 1 incidente fundador apenas; mitiga risco operador-por-reflexo):
     - `Remover todos os <N>` — executa `rm <path>` em cada órfão.
     - `Cutucar individualmente` — loop com cutucada por órfão (`Remover` / `Manter`).
     - `Manter todos (investigar)` — preserva todos; operador investiga depois.
   - `Other` (automático) cobre subset ad-hoc ou direção de investigação livre.

6. **Aplicar seleção** e retornar controle à skill consumidora.
