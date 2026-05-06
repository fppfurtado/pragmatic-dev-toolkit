# `/release` HEAD-branch check + Action `validate-backlog` issue dedup

## Contexto

Duas defesas operacionais pequenas capturadas em `## Próximos` do BACKLOG.md durante a sessão atual, com arquivos disjuntos:

1. **`/release` HEAD-branch check.** Operador rodou `git checkout v1.17.0` em terminal concorrente durante release v1.18.0; HEAD detachou; commit de release nasceu em linha paralela (tree de v1.17.0 + version bumps + entrada de changelog), fora do `main`. Pré-condição 2 do `/release` valida branch no início, mas não revalida imediatamente antes do `git commit` do passo 4.5.Aplicar. Janela aberta entre prep (passos 1–3) e apply (passo 4.5).

2. **Action `validate-backlog` issue dedup.** Workflow cria nova issue a cada push para `main` que detecta artefato. Pushes sucessivos com mesmo artefato geram N issues duplicadas. `security-reviewer` flagou como editorial (fora-de-escopo de segurança) durante o PR #23. Solução: `gh issue list --label backlog-merge-artifact --state open` antes do `gh issue create`; se ≥1, skip + log explícito.

Sem `**Linha do backlog:**` (plano cobre 2 linhas em Próximos; auto-transição inicial e gate final 4.4 ficam em skip silente). `## Notas operacionais` registra a transição manual de ambas as linhas após merge.

## Resumo da mudança

**Bloco 1 — `/release` SKILL.md:** inserir verificação + recovery de HEAD branch como primeiro item da sequência `Aplicar` no passo 4.5. `git symbolic-ref --short HEAD`; detached ou diferente do branch da pré-condição 2 → recovery proativo: se houver alterações uncommitted (`git status --porcelain` não-vazio), `git stash push -m "<mensagem descritiva>"`; depois `git checkout <branch-da-pré-condição-2>`; só então prosseguir com a sequência (a)-(e). Release continua em vez de abortar; operador recupera stash manualmente após release se necessário.

**Bloco 2 — Action workflow:** modificar step `Open issue on artifact detected` para checar `gh issue list --label backlog-merge-artifact --state open --json number --jq 'length'` antes do `gh issue create`. Count ≥1 → log + early-exit do step. Permissions inalteradas (`contents: read, issues: write`).

Arquivos disjuntos (`skills/release/SKILL.md` vs `.github/workflows/validate-backlog.yml`); zero conflito entre blocos.

## Arquivos a alterar

### Bloco 1 — skills/release/SKILL.md

Inserir verificação + recovery de HEAD branch como **primeiro item** da sequência `Aplicar` no passo 4.5 (antes do atual `(a) escrever cada version_file`):

```
- **Aplicar** — verificar HEAD e recuperar se necessário:
  1. Rodar `git symbolic-ref --short HEAD`. Output → branch atual; falha (exit ≠ 0) → HEAD detached.
  2. Se detached OU se branch atual difere do branch da pré-condição 2:
     - `git status --porcelain`; se não-vazio, `git stash push -m "release v<X.Y.Z> auto-stash: HEAD inesperado em <ref-atual> ao iniciar Aplicar (esperado <branch-pré-condição-2>)"` para preservar trabalho local.
     - `git checkout <branch-da-pré-condição-2>`.
     - Reportar ao operador o que aconteceu (incluindo nome da stash se criada) — operador recupera manualmente após release com `git stash pop` se desejar.
  3. Caso ok desde o início (HEAD igual ao branch da pré-condição 2 e working tree clean), prosseguir direto.
  4. Executar em sequência: (a) escrever cada `version_file` preparado; (b) inserir entrada do changelog; (c) `git add <paths-específicos>` (...).
```

Recovery cobre janela entre prep (passos 1–3, em memória) e apply (passo 4.5, escrita + commit) — HEAD pode mudar por sessão concorrente. Stash preserva trabalho do operador se houver; checkout volta para o branch correto; release continua. Operador retoma stash manualmente após release.

Reviewer default `code`. Sem `## O que NÃO fazer` novo (o guard fica embutido no Aplicar).

### Bloco 2 — .github/workflows/validate-backlog.yml {reviewer: code,security}

Modificar o step `Open issue on artifact detected`. Antes de `gh label create` e `gh issue create`, checar:

```bash
open_count=$(gh issue list --label backlog-merge-artifact --state open --json number --jq 'length')
if [ "$open_count" -gt 0 ]; then
  echo "skipping issue creation: $open_count open issue(s) already track this artifact"
  exit 0
fi
```

Resto do step (label create + issue create + body composition) inalterado.

Reviewer combinado: `code` revisa o shell + condicional. `security` revisa: (a) `gh issue list --state open` lê apenas issues abertas (não vaza estado de issues fechadas/privadas além do necessário); (b) permissions explícitas inalteradas (`contents: read, issues: write`); (c) sem novos secrets ou tokens; (d) `exit 0` do step não fecha o workflow inteiro — outros steps continuam (no caso, "Fail on script error" condicionalmente).

## Verificação end-to-end

`test_command: null`. Substituto textual:

1. **Bloco 1 (release):** inspeção de `skills/release/SKILL.md` — sequência `Aplicar` no passo 4.5 inicia com verificação de HEAD via `git symbolic-ref --short HEAD`; abort em caso de detached/branch errada é descrito; sub-itens `(a)`–`(e)` preservados em ordem.

2. **Bloco 2 (workflow):** YAML parseable via `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/validate-backlog.yml'))"`; condicional `open_count > 0` precede `gh label create`/`gh issue create`; permissions inalteradas (top-level `contents: read, issues: write`).

3. **Skill estrutura preservada:** `skills/release/SKILL.md` ainda tem Argumentos / Pré-condições / Passos / O que NÃO fazer; `## O que NÃO fazer` ≤7 itens; mudança é cirúrgica no passo 4.5.

4. **Smoke real (post-merge, opcional):**
   - Bloco 2: push para main com artefato + 0 issues abertas → cria issue. Push subsequente com artefato ainda não resolvido → skip silente, log "skipping issue creation: 1 open issue(s) already track this artifact".
   - Bloco 1: próxima invocação de `/release` (esta sessão ou futura) deve passar pela verificação inteira; se operador rodar `git checkout <outro-ref>` em paralelo, release aborta com erro literal antes de tocar disco.

## Notas operacionais

**Transição manual do backlog após merge.** Plano cobre 2 linhas em `## Próximos`; sem `**Linha do backlog:**` (singular pelo design da convenção), `/run-plan` skipa auto-transição inicial (passo 3) e final (passo 4.4) silenciosamente — comportamento prescrito pela própria regra.

Após merge desta PR, operador transiciona **ambas** as linhas de `## Próximos` para `## Concluídos` em commit único (chore commit direto em main):

- `/release: verificar HEAD branch (não detached, mesma branch da pré-condição 2) imediatamente antes do `git commit` no passo 4.Aplicar — guarda contra mudança de HEAD por sessão concorrente em outro terminal. Sintoma observado na release v1.18.0: `git checkout v1.17.0` rodado em paralelo detachou HEAD; commit nasceu em linha paralela com tree de v1.17.0 + version bumps, fora do main.`
- `Action `validate-backlog`: deduplicar issues abertas com mesma label antes de criar nova (`gh issue list --label backlog-merge-artifact --state open`) — evita N issues duplicadas em pushes sucessivos com artefato. Flagado pelo `security-reviewer` como editorial (fora-de-escopo de segurança) durante execução do plano `backlog-validate-and-heal`.`

Mensagem do chore commit sugerida: `chore(backlog): move /release HEAD-check and Action issue-dedup lines to Concluidos`.
