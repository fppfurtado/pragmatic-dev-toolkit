# Plano — /next varrer pendências de validação em planos

## Contexto

`/next` hoje lê apenas o BACKLOG (`## Próximos`) para sugerir top 3 candidatos. Pendências de validação capturadas pelo `/run-plan §3.5` ficam em `## Pendências de validação` no próprio plano (memory `feedback_backlog_scope` registra essa separação como doutrina: pendência de validação fica no plano, não no backlog) — fonte paralela de pendentes que não aparece em nenhuma cutucada de "o que fazer agora?". Operador depende de memória para revisitá-las.

Caso real flagado nesta sessão (2026-05-08): pendências (a) e (b) do plano `instrumentar-skills-multi-passo.md` (PR #44) e a pendência do plano `run-plan-3-3-skip-empirico.md` (PR #46) só apareceram no radar quando o operador trouxe manualmente a pergunta "vê se há pendência de validação em planos também?". O `/next` não tem mecanismo para descobri-las automaticamente.

**Doutrina aplicada:**

- `feedback_backlog_scope` (memory): pendência de validação **não vai pro BACKLOG** — fica no plano de origem. Confirma a separação atual; não inverte.
- ADR-004 (state-tracking em git): planos commitados são state em git/forge — fonte canônica que `/next` deveria varrer naturalmente, sem persistir em estrutura paralela.
- O ranking principal do `/next` (top 3 por alinhamento estratégico × amplitude) continua sendo sobre `## Próximos` do BACKLOG. Pendências de validação têm rationale diferente (fechamento de plano específico) e merecem **listagem separada** — não competir no top 3.

**Linha do backlog:** plugin: `/next` varrer também `## Pendências de validação` em planos `<plans_dir>/*.md` — hoje só lê BACKLOG, mas pendências de validação são fonte paralela de pendentes (memory `feedback_backlog_scope`: pendência fica no plano, não no backlog) sem mecanismo de descoberta. Direção: listagem separada (rationale é fechamento de plano específico, não estratégia × amplitude do top 3); filtrar planos em curso (worktree ativa / PR aberto). Caso real: pendências (a) e (b) do plano `instrumentar-skills-multi-passo.md` invisíveis ao `/next` até operador trazer manualmente.

## Resumo da mudança

Adicionar passo de varredura ao `/next` que lista `## Pendências de validação` de planos mergeados, em **seção separada** do top 3:

1. **Varrer** `<plans_dir>/*.md` (papel `plans_dir`; modo local lido de `.claude/local/plans/*.md`).
2. **Filtrar planos em curso:** plano cujo slug bate com worktree em `.worktrees/<slug>` ou com branch de PR/MR aberto (auto-detect de forge análogo ao `/run-plan §3.7`: `github.com` → `gh pr list --state open --json headRefName --jq '.[].headRefName'`; host casando `^gitlab\.` → `glab mr list --opened`; outros hosts ou CLI ausente → fallback só por worktree) é considerado **em execução** — pendência ainda em escopo do `/run-plan` corrente, não cabe na listagem de "afazer pendente". Pular.
3. **Extrair** `## Pendências de validação` dos planos restantes (mergeados ou nunca executados): cada bullet vira uma entrada.
4. **Apresentar separadamente** após o top 3 do BACKLOG e antes do enum de escolha. Bloco editorial: cabeçalho `Pendências de validação em planos:` com lista `<slug>: <texto da linha>`. Plano sem pendências → omitir do bloco. Bloco vazio inteiro → omitir.
5. **Não competir no enum de escolha do `/next`** — top 3 continua sendo do BACKLOG. Pendências aparecem para visibilidade; operador escolhe via `Other` se quiser endereçar uma pendência específica (digita o texto), ou ignora.

Critério de "filtrar planos em curso" combina duas fontes:
- **Worktree ativa:** `git worktree list --porcelain` → listar paths sob `.worktrees/`; extrair slug do basename.
- **PR/MR aberto via forge auto-detect** (mesmo padrão do `/run-plan §3.7`): parse `git remote get-url origin`. `github.com` → `gh pr list --state open --json headRefName --jq '.[].headRefName'`; host casando `^gitlab\.` (gitlab.com ou GitLab corporativo `gitlab.<domínio>`) → `glab mr list --opened`; outros hosts → fallback (só worktree). CLI ausente em host mapeado → fallback (só worktree). Sem flag, sem cutucada — degradação silenciosa porque a filtragem é heurística informativa, não invariante crítica.

Plano cujo slug bate em qualquer das fontes ativas é "em curso".

Fica de fora:
- Cutucada para "atacar pendência X" via enum dedicado — operador escolhe via `Other` no enum existente. YAGNI até pain de digitar emergir.
- Ordenação/ranking das pendências — listadas em ordem do filesystem (alfabético do slug); priorização vira pain real só com volume.
- Sincronização com PR já mergeado mas plano editado pós-merge — borda rara; documentar em Notas operacionais.
- ADR — refinamento de skill, não mexe em doutrina central nem toca regra cross-skill (apenas `/next`); ambos os trilhos de `feedback_adr_threshold_doctrine` não disparam.
- Detecção de pendência **resolvida** (operador editou plano e removeu linha) — operador resolve manualmente movendo bullet do `## Pendências de validação`; `/next` próximo varre o estado atualizado. Auto-detect resolvido seria abstração prematura.
- Generalização para outras seções de plano (`## Notas operacionais` não-aplicadas, gaps de teste documentados em outras seções, etc.) — só `## Pendências de validação` tem rationale claro de "afazer pendente que precisa fechar fora do `/run-plan`". Outras seções são informativas/notas, não pendências acionáveis. Reabrir se surgir 2ª categoria com mesma natureza (pendência cross-plano que escapa do gate de execução).

## Arquivos a alterar

### Bloco 1 — passo de varredura de pendências em /next {reviewer: code}

- `skills/next/SKILL.md`: adicionar passo entre o atual passo 4 (Avaliar e classificar) e passo 5 (Apresentar resultado), ou subseção dentro do passo 5 antes da apresentação. Escolha do ponto de inserção:
  - **Inserir antes do passo 5** como passo 4.5 (ou subseção `**Pendências de validação em planos.**` após "## Avaliar"): a varredura é independente do ranking do top 3, então roda em paralelo conceitual mas é apresentada junto.
  - Mecânica:
    1. Listar planos: papel `plans_dir` resolvido (default `docs/plans/`); modo local lê de `.claude/local/plans/`.
    2. Filtrar em curso: cruzar com `git worktree list --porcelain` e auto-detect de forge (mesmo padrão do `/run-plan §3.7`) — parse `git remote get-url origin`, `github.com` → `gh pr list --state open`, `^gitlab\.` → `glab mr list --opened`, outros hosts ou CLI ausente → fallback só por worktree.
    3. Para cada plano não-em-curso, extrair `## Pendências de validação` (entre o header e o próximo `##` ou EOF). Sem seção → pular.
    4. Acumular lista; vazio → omitir do relatório do passo 5.
  - Apresentação no passo 5: após o top 3, adicionar bloco `**Pendências de validação em planos:**` listando `- <slug>: <texto da linha>` por entrada. Operador escolhe via `Other` no enum existente caso queira endereçar uma pendência específica.

## Verificação end-to-end

- `grep -n "Pendências de validação\|plans_dir.*\*\.md\|gh pr list\|glab mr list" skills/next/SKILL.md` retorna as linhas novas (varredura, filtragem por forge auto-detect, apresentação).
- Releitura textual confirma: (a) varredura roda após avaliar (passo 4) e antes de apresentar (passo 5); (b) filtragem de "em curso" usa worktree + auto-detect de forge (`gh` para GitHub, `glab` para GitLab, fallback só worktree para outros); (c) apresentação é seção separada do top 3, não compete no ranking; (d) bloco vazio é omitido (sem ruído).
- Top 3 atual continua sendo o ranking principal — varredura não substitui nem altera o `## Próximos` do BACKLOG.

## Verificação manual

Surface não-determinística (matching textual de slug contra worktree/PR; extração de seção markdown). Forma do dado real:

- `git worktree list --porcelain` → `worktree /storage/.../.worktrees/<slug>\nbranch refs/heads/<slug>`.
- `gh pr list --state open --json headRefName` → `[{"headRefName":"feature-x"}]`.
- Plano com pendência: arquivo `<plans_dir>/<slug>.md` contendo seção `## Pendências de validação` com bullets.

Cenários enumerados:

1. **Plano mergeado com pendência aberta.** Setup atual da repo: `docs/plans/instrumentar-skills-multi-passo.md` tem 2 itens em `## Pendências de validação` (PR #44 mergeado); `docs/plans/run-plan-3-3-skip-empirico.md` tem 1 item (PR #46 mergeado). Esperado: invocar `/next` lista esses 3 itens em `**Pendências de validação em planos:**` após o top 3.

2. **Plano em curso (worktree ativa) → filtrado.** Criar plano fictício em `docs/plans/teste-em-curso.md` com `## Pendências de validação` + criar worktree `.worktrees/teste-em-curso`. Esperado: `/next` **não** lista esse plano (filtrado pela worktree). Limpar setup ao fim.

3. **Plano em curso (PR aberto) → filtrado.** Branch com PR aberto cujo nome bate com slug de plano existente. Fixture difícil de reproduzir sem PR real — verificar por inspeção textual da regra implementada: reler as linhas que invocam `gh pr list --state open --json headRefName --jq '.[].headRefName'`, extrair os branch names, cruzar com slug; confirmar que plano correspondente é pulado antes da extração de `## Pendências de validação`. Sem inspeção dirigida, o "verifiquei e parece ok" vira anti-padrão.

4. **Plano sem pendências → omitido.** Plano sem a seção `## Pendências de validação`. Esperado: não aparece na listagem.

5. **Lista vazia → bloco omitido.** Todos os planos são em curso ou sem pendências. Esperado: nenhum bloco `Pendências de validação em planos:` no relatório do passo 5 — só top 3.

6. **CLI do forge ausente ou host não-mapeado → fallback só por worktree.** Subcasos: (a) host `github.com` mas `gh` não-instalado; (b) host casa `^gitlab\.` mas `glab` não-instalado; (c) host fora do mapeamento (Bitbucket, Forgejo, Gitea, etc.) — sem CLI tentado. Esperado em todos: filtragem usa só `git worktree list`; planos com PR/MR aberto mas sem worktree local podem aparecer (degradação aceita; operador descarta via `Other` se necessário). Cenário 6 da `## Verificação manual` análogo ao tratamento do `/run-plan §3.7`.

7. **Plano editado pós-merge (bullets removidos) → omitido.** Plano que tinha pendência foi mergeado, operador editou em commit posterior removendo todos os bullets de `## Pendências de validação` (seção fica vazia ou só com header). Esperado: extração não retorna entradas; plano não aparece na listagem (mesmo comportamento de "plano sem pendências"). Verifica que a extração lê o estado atual do arquivo, não memória do estado pré-edição.

## Notas operacionais

- **Plano editado pós-merge** (operador remove bullet de `## Pendências de validação` manualmente após resolver fora do `/run-plan`) é detectado naturalmente — varredura lê o arquivo atual; bullet removido não aparece. Sem mecanismo extra. Cenário 7 da `## Verificação manual` exercita.
- **Performance:** ler N planos por invocação do `/next` é O(N) em IO local. N atual no repo ≈ 50 planos; cada arquivo é < 5KB. Custo trivial. Reabrir se N ultrapassar ~500 ou se latência aparente.
- **Sem cache cross-invocação:** cada `/next` relê todos os planos. Decisão consciente — cache invalidaria com edição de plano (caso comum entre invocações), e custo trivial em N≈50 não justifica overhead. Reavaliar se sessões com `/next` repetido virarem comuns e N crescer.
- **Plano sem `## Pendências de validação`** continua sendo o caso comum (maioria dos planos não acumula pendência). Skip silente do plano nessa varredura.
- **Apresentação ao operador é interna** (relatório do passo 5, não vai a commit/PR/branch). A regra de não-referenciar de [ADR-005](../decisions/ADR-005-modo-local-gitignored-roles.md) **não se aplica** — slug de plano e texto da pendência podem aparecer no relatório inclusive em modo local (`paths.plans_dir: local`); ADR-005 rege só metadata externa (commit msg, PR descrição, branch name).
- **Plano `desacoplar-gh-em-skills.md` em `docs/plans/`:** se ativo (não sei o status sem inspecionar), este plano introduz mais um ponto de uso de `gh` (`gh pr list`); ambos podem precisar harmonizar fallback textual genérico no futuro. Hoje aceito porque `gh` já é dependência implícita do toolkit (cleanup pós-merge no `/triage` step 0 e auto-detect de forge no `/run-plan §3.7` já assumem).
- **Bloco único `{reviewer: code}`** — refinamento editorial em SKILL de implementação; sem teste novo (plugin sem suite); sem doc user-facing tocada. O sanity check 3.3 do `/run-plan` (regra mergeada no PR #46) cobrirá README/install no done — provavelmente vai cutucar com referrers espúrios `/next` (descrição genérica), absorvidos por `Consistente`.

## Pendências de validação

- ~~1ª invocação real do `design-reviewer` pós-wiring (ADR-011) não detectou que a versão original do plano hardcoded `gh pr list` contradizia o padrão de auto-detect de forge estabelecido no `/run-plan §3.7` e `/release` (item Concluído no BACKLOG `desacoplar-gh-em-skills` + auto-detect implementado). Operador trouxe o ponto manualmente pós-commit (commit `d463bb6`); plano corrigido em commit subsequente. Captura empírica: 1 ocorrência ainda não justifica reabrir critério do agent (`agents/design-reviewer.md`) — YAGNI. Se 2ª ocorrência aparecer (reviewer perde acoplamento a padrão estabelecido do toolkit), reabrir para acrescentar heurística "ao detectar uso de CLI/biblioteca/dependência específica, verificar se há padrão estabelecido no toolkit antes de aprovar". Por enquanto: nota empírica no plano corrente.~~ **Encerrada 2026-05-15:** 2ª ocorrência do gap não emergiu desde shipping; critério do reviewer permanece sem refinamento (YAGNI ativo).
