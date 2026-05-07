# Plano — Cleanup pós-merge cutucada

## Contexto

`/run-plan` termina na worktree (branch da feature) após oferecer Push/Push+PR; não há retorno após o merge no remote. Hoje o cleanup (`git worktree remove`, `git branch -d`, `git push origin --delete`, `git fetch --prune`) é manual e gera atrito recorrente — manifestou-se literalmente na sessão de hoje após PR #42 (precisei de `AskUserQuestion` enum manual para limpar).

Mecanismo: **passo anexado em `/triage` e `/release`** (não skill nova). A cutucada surge naturalmente quando o operador inicia o próximo workflow — momento em que worktrees mergeadas já são restos do trabalho anterior. Skill dedicada (`/post-merge-cleanup`) descartada: exigiria invocação explícita e perderia a janela natural; passo anexado fica oportunista mas previsível.

Forma da cutucada: `AskUserQuestion` multi-select por candidato detectado, header `Cleanup`, opções `Worktree` / `Branch local` / `Branch remota` (cada uma carregando comando equivalente em `description`). Operador escolhe qualquer combinação ou pula deixando todas desmarcadas. Sem candidatos detectados → skip silente; passo nunca incomoda quando nada precisa ser limpo.

Detecção squash-merge-aware: `gh pr list --state merged --head <branch>` é o caminho confiável (squash não preserva ancestry, então `git branch --merged` perde esses casos). Fallback `git branch -r --merged origin/<main>` quando `gh` ausente ou remote não-GitHub — captura merges normais mas perde squash; documentar limitação.

**ADRs tocadas:** ADR-002 (eliminar gates pré-loop) — tangente: cutucada nova é gate adicional, mas é cutucada de **estado de repo** (worktree órfã), não de qualidade-de-mudança; ADR-002 não aplica diretamente. ADR-004 (state em git/forge) — alinha: cleanup pós-merge é higiene da decisão de tratar git/forge como fonte de estado.

**Linha do backlog:** plugin: cutucada pós-merge para cleanup de worktree/branch local — `/run-plan` termina na worktree na branch da feature após oferecer Push/Push+PR (skill, linha final do passo 7) e não há retorno após o merge; `git worktree remove .worktrees/<slug>`, `git branch -d <slug>` e `git fetch --prune` ficam manuais. Direção possível: skill nova (`/post-merge-cleanup`) ou passo opcional anexado à próxima invocação de `/triage`/`/release` quando detectar worktrees em `.worktrees/` cuja branch já mergeou em `origin/<main>` (`git branch -r --merged origin/<main>` cruzado com `git worktree list`). Reavaliar se YAGNI: cleanup é trivial e o operador pode preferir manter a worktree para inspeção pós-merge — registrar para reavaliar se atrito recorrer.

## Resumo da mudança

1. Adicionar `### 0. Cleanup pós-merge` em `skills/triage/SKILL.md` (antes do passo 1 atual).
2. Adicionar passo equivalente em `skills/release/SKILL.md` (antes da pré-condição 1) — referência cruzada à descrição em `/triage` para evitar duplicação que driftaria.
3. Skip silente quando `.worktrees/` ausente ou sem candidatos mergeados.
4. Multi-select `AskUserQuestion` com 3 opções por candidato; cada uma mapeia comando concreto. Sem seleção → skip esse candidato.

Fora de escopo (deferido):
- Cleanup automatizado sem cutucada (ADR-002 priorizou captura sobre auto-execução em todo o plugin).
- Detecção em hook `SessionStart` (auto-gating triplo entre projetos torna heurística complexa para ganho marginal).
- Cleanup do worktree principal ou da branch `main`/principal — sempre excluídos do scan.
- Anexar a `/run-plan`: `/triage` precede `/run-plan` no fluxo natural; cleanup em `/triage` deixa `/run-plan` partir de estado limpo.
- Suporte a forges não-GitHub para detecção de squash (depende do item `auto-detect-forge` em `## Próximos`).

## Arquivos a alterar

### Bloco 1 — `/triage` ganha passo 0 de cleanup pós-merge {reviewer: code}

- `skills/triage/SKILL.md`: novo `### 0. Cleanup pós-merge` antes do `### 1. Carregar contexto mínimo`. Conteúdo:
  - **Detecção de candidatos**:
    1. `git worktree list --porcelain` → filtrar entradas cujo `worktree` está sob `.worktrees/` (excluir worktree principal).
    2. Para cada candidato, extrair branch (`branch refs/heads/<slug>` da saída porcelain).
    3. Verificar merge status: `gh pr list --state merged --head <branch> --json number --jq '.[0].number'` (squash-aware). Saída numérica → mergeado, capturar PR number. Saída vazia / `gh` ausente → fallback `git branch -r --merged origin/<main>` checando se `<branch>` está listada (perde squash; documentar como limitação textual no `description` do bloco doc-only futuro). Sem detecção em nenhum dos dois → não é candidato; pular.
    4. Lista de candidatos mergeados vazia → **skip silente** (skill prossegue para passo 1 sem mensagem).
  - **Cutucada por candidato**: para cada candidato, `AskUserQuestion`:
    - `header`: `Cleanup`
    - `question`: `"Worktree '<slug>' (PR #<num> mergeado): limpar o quê?"` (omitir `PR #<num>` no fallback git-only)
    - `multiSelect`: `true`
    - Opções:
      - `Worktree` — `description`: `"git worktree remove .worktrees/<slug>"`
      - `Branch local` — `description`: `"git branch -d <slug>; squash detectado força -D com nota"`
      - `Branch remota` — `description`: `"git push origin --delete <slug>"`
    - Sem seleção (todas desmarcadas + confirmar) → skip esse candidato; segue para o próximo.
  - **Execução das seleções**: ordem importa para isolamento — `worktree remove` antes de `branch -d` (worktree em uso bloqueia delete). Ordem padrão: Worktree → Branch local → Branch remota.
    - `Branch local`: tentar `git branch -d <slug>` primeiro. Falha com "not fully merged" → executar `git branch -D <slug>` e reportar `"branch <slug> não mergeada via fast-forward — squash detectado via gh; usando -D"` (caso real para PRs squash-merged onde ancestry local não bate).
    - Falha em qualquer comando após o primeiro → reportar erro literal e parar (sem `--force` adicional, sem retry). Comandos já executados permanecem aplicados; operador resolve o resto manual.
  - **Após todos os candidatos**: `git fetch origin --prune` para limpar refs remotos órfãos.
  - **Skill prossegue para passo 1** normalmente.

### Bloco 2 — `/release` ganha mesmo passo via referência {reviewer: code}

- `skills/release/SKILL.md`: nova seção `## Cleanup pós-merge` antes de `## Pré-condições`. Conteúdo curto:
  ```
  Antes das pré-condições, executar passo de cleanup pós-merge conforme `skills/triage/SKILL.md` `### 0. Cleanup pós-merge`. Mesma detecção, mesma cutucada, mesmas execuções. Skip silente se nada a limpar.
  ```
- Justificativa de referência cruzada (não duplicação): comportamento deve ser idêntico entre as duas skills; drift seria bug. Skills do plugin são prosa lida pelo modelo — referência cruzada funciona sem mecânica de import.

## Verificação end-to-end

Repo sem suite (`test_command: null`). Inspeção textual:

1. `skills/triage/SKILL.md` tem `### 0. Cleanup pós-merge` antes de `### 1. Carregar contexto mínimo`.
2. `skills/release/SKILL.md` tem `## Cleanup pós-merge` antes de `## Pré-condições`, com referência cruzada para `/triage`.

## Verificação manual

**Surface não-determinística**: parsing de output de `gh pr list` e `git worktree list --porcelain`; decisão runtime sobre squash via fallback; cutucada via LLM. Cenários enumerados:

**Forma do dado real**:
- `git worktree list --porcelain` saída multi-linha: `worktree <path>` / `HEAD <sha>` / `branch refs/heads/<slug>`.
- `gh pr list --state merged --head <branch> --json number --jq '.[0].number'`: número (mergeado) ou vazio.
- Branch squash-merged: `git branch --merged main` **não** inclui; `gh` retorna PR mergeado.
- Branch fast-forward/merge-commit: ambos detectam.

**Cenários** (executar em worktree do toolkit com `.worktrees/<slug>` artificial):

1. **Squash-merge detectado.** Criar worktree+branch local; mergear PR squash em origin; rodar `/triage` (sem args). Esperado: detecta candidato, mostra cutucada com `PR #<num>`, multi-select de 3 opções; selecionar todas → 4 comandos executam; reporta sucesso; passo 1 prossegue.
2. **Fast-forward merge detectado.** Mesmo cenário com merge fast-forward. `gh` e `git branch --merged` ambos detectam — mesmo fluxo do (1).
3. **Worktree NÃO mergeado.** Worktree existe mas PR não foi mergeado (em curso ou abandonado). Esperado: candidato não dispara cutucada — `gh` retorna vazio E `git branch --merged` não lista.
4. **`.worktrees/` ausente.** `/triage` rodado em repo sem `.worktrees/` (caso comum). Esperado: skip silente, sem mensagem; passo 1 imediato.
5. **Operador deixa todas desmarcadas.** Cutucada apresentada, operador confirma sem selecionar. Esperado: skip esse candidato, segue para próximo (ou passo 1 se for o último).
6. **`push --delete` falha (branch já deletada em origin via auto-delete do GitHub).** Esperado: reportar erro literal de `git`, parar; worktree e branch local (se selecionados antes) permanecem deletados. Operador roda `git fetch --prune` manual depois.
7. **`gh` ausente, fallback git-only.** Worktree fast-forward-merged. Esperado: detecta via `git branch -r --merged`; cutucada não cita `PR #<num>` (fallback). Caso squash-merged: NÃO detecta; cleanup fica manual (limitação documentada).
8. **Worktree principal jamais como candidato.** Path-based filter exclui qualquer entrada fora de `.worktrees/`.
9. **Múltiplos candidatos.** 2+ worktrees mergeadas. Esperado: cutucada por candidato em sequência; cada um independente.

## Notas operacionais

- **Custo de invocação**: `git worktree list` é instantâneo; `gh pr list` por candidato é ~1s. Worktrees ativas tipicamente ≤3, custo aceitável. Skip silente em `.worktrees/` ausente mantém `/triage` rápido no caminho-comum.
- **Reusabilidade do bloco**: prosa única em `/triage` `### 0`; `/release` referencia. Drift é bug — manter o ponto único.
- **Compatibilidade não-GitHub**: detecção squash via `gh` é específica de GitHub. GitLab/outros: fallback git-only só captura merges com ancestry. Item de backlog `auto-detect-forge` (em `## Próximos`) eventualmente fechará essa lacuna; reabrir esta detecção quando `glab` etc. forem suportados.
- **Race com push concorrente**: outro operador (ou GitHub auto-delete) pode ter removido a branch remota. Erro de `push --delete` reporta e segue — não trava.
- **Squash + `-d` vs `-D`**: tentativa de `-d` primeiro para preservar safety; fallback explícito `-D` quando `-d` recusa, com nota informativa. Regra geral do plugin é evitar `--force`; aqui é `-D` (não `--force`), justificado pelo squash-merge ter sido confirmado via `gh`.
