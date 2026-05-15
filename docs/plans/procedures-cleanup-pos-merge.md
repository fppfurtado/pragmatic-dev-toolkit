# Plano — Extrair Cleanup pós-merge para docs/procedures/ + forge bilateral (Onda 3a)

## Contexto

Bundle pré-curado pela auditoria `docs/audits/runs/2026-05-12-architecture-logic.md` (propostas G + D), sequenciado como **Onda 3a** em `docs/audits/runs/2026-05-12-execution-roadmap.md`. As 2 propostas tocam o mesmo procedimento operacional ("Cleanup pós-merge") referenciado por `/triage §0` e `/release § Cleanup pós-merge` via acoplamento textual hoje — atacar junto resolve L1 (audit § 2.6) e elimina duplicação intermediária entre G (extrair) e D (estender forge bilateral).

**ADRs candidatos:** [ADR-024](../decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md) (criado neste `/triage` para fundamentar G — estabelece `docs/procedures/` como categoria distinta de `templates/` para procedimentos operacionais compartilhados; sucessor parcial de ADR-001), [ADR-001](../decisions/ADR-001-protocolo-de-templates.md) (fronteira semântica original de `templates/`, recebe addendum pós-aceitação apontando para ADR-024 per invariante de implementação da § Decisão de ADR-024).

## Resumo da mudança

**Verificação dos 3 critérios cumulativos do ADR-024 § Decisão** (registrada per invariante "verificação obrigatória registrada no plano/ADR"):

1. **Procedimento operacional executável** ✓ — algoritmo de detecção+cutucada+execução em runtime, não esqueleto preenchível.
2. **≥2 skills consumindo** ✓ — `/triage` passo 0 + `/release` pré-condição.
3. **Acoplamento textual concreto resolvido** ✓ — L1 do audit `docs/audits/runs/2026-05-12-architecture-logic.md` § 2.6 (`/release` referencia "skills/triage/SKILL.md `### 0. Cleanup pós-merge`").

Duas frentes consecutivas no mesmo arquivo novo + 1 addendum em ADR-001:

1. **G_arch — extrair Cleanup pós-merge** de `/triage §0` (~30 linhas) para `docs/procedures/cleanup-pos-merge.md` AS-IS. `/triage` e `/release` passam a referenciar o procedimento via 1-2 linhas cada. Resolve L1 do audit (acoplamento textual entre /release e /triage §0 por path + nome de seção). Estabelece consumer-pattern paralelo a `templates/plan.md`: skills leem o procedimento em runtime via Read, sem duplicar conteúdo.

2. **D_arch — estender auto-detect forge bilateral** dentro do procedimento extraído. Hoje detecta merge status só via `gh pr list`; replicar pattern já validado em `/run-plan §3.7`, `/release §5`, `/next §4.5`: parse `git remote get-url origin` → `github.com` → `gh`; regex `^gitlab\.` → `glab mr list` (squash-aware no GitLab); fallback `git --merged` para hosts não mapeados. Consumer GitLab ganha cleanup squash-aware.

3. **Addendum pós-aceitação em ADR-001** (invariante de implementação de ADR-024 § Decisão) — nova seção `## Addendum (2026-05-12)` em ADR-001 apontando para ADR-024 como categoria paralela. Marcação explícita "addendum informativo posterior à aceitação" preserva imutabilidade da § Decisão original. Sem essa edição, ADR-024 não está implementado.

**Localização decidida em alinhamento prévio:** `docs/procedures/` (categoria nova, pureza semântica) ao invés de `templates/cleanup-pos-merge.md` (esticar semântica de templates/) ou `templates/protocols/` (subdiretório sob templates/). Trade-off: 4ª categoria sob `docs/`, justificada pela fronteira nítida entre `templates/` (esqueletos preenchidos quando o artefato é produzido) e `docs/procedures/` (procedimentos executados quando referenciados). Nome `procedures` (não `protocols`) evita colisão lexical com "Resolution protocol" e "Protocolo de templates" — ver ADR-024 § Contexto "Desambiguação lexical".

**Sequenciamento G→D atômico no mesmo arquivo:** Bloco 1 extrai AS-IS (fidelidade revisável); Bloco 2 estende forge bilateral (mudança nova revisável). Permite diff cirúrgico — reviewer do Bloco 1 valida "extração fiel?"; reviewer do Bloco 2 valida "pattern de auto-detect aplicado corretamente?". Combinar em 1 bloco misturaria literal-copy com mudança comportamental, dificultando review.

## Arquivos a alterar

### Bloco 1 — Criar docs/procedures/cleanup-pos-merge.md (extração AS-IS de /triage §0)

- `docs/procedures/cleanup-pos-merge.md` (novo): copiar AS-IS o conteúdo de `skills/triage/SKILL.md` `### 0. Cleanup pós-merge` (linhas ~15-55 atuais — sub-seções Detecção de candidatos, Cutucada por candidato, Execução das seleções, Após todos os candidatos). Substituir título `### 0. Cleanup pós-merge` por `# Cleanup pós-merge` (top-level no arquivo novo). Renumeração de sub-headers (H4 → H2/H3) conforme estrutura standalone. Adicionar parágrafo de abertura curto explicando que o procedimento é referenciado por `/triage` (passo 0) e `/release` (pré-condição), Read em runtime, per ADR-024.

**Reviewer orientação (critério atípico):** Bloco 1 é literal-extraction puro. Reviewer code valida que extração é textualmente fiel — diff entre original (`### 0. Cleanup pós-merge` em `skills/triage/SKILL.md`) e novo arquivo (`# Cleanup pós-merge` em `docs/procedures/`) deve mostrar apenas: (a) renumeração de headers, (b) parágrafo de abertura adicionado. Nenhuma reescrita semântica neste bloco — alterações de mecânica entram no Bloco 2.

### Bloco 2 — Estender auto-detect forge bilateral em docs/procedures/cleanup-pos-merge.md

- `docs/procedures/cleanup-pos-merge.md`: ajustar passo 3 da "Detecção de candidatos" (atual: só `gh pr list`). Wording aplicado (sintaxe `glab` confirmada via docs oficiais durante o gate abaixo): detectar host via `git remote get-url origin`; `github.com` → `gh pr list --state merged --head <branch> --json number --jq '.[0].number'`; regex `^gitlab\.` → `glab mr list --merged --source-branch <branch> --output json | jq -r '.[0].iid // empty'`; host não-mapeado ou CLI ausente → fallback `git branch -r --merged origin/<main>` (perde squash). Cutucada (texto da pergunta) e mensagens de execução omitem "PR #" / "MR !" no fallback git-only (preservar comportamento atual). Quando forge for GitLab, identificador é "MR !<num>" em vez de "PR #<num>".

**Gate explícito de sintaxe `glab` (executado durante Bloco 2):** os 3 sites canonical do toolkit (`/run-plan §3.7`, `/release §5`, `/next §4.5`) usam `glab mr create --fill`, `glab release create --notes` e `glab mr list --opened` — **nenhum** cobre `glab mr list --merged --source-branch`. Gate executado contra docs oficiais (https://gitlab.com/gitlab-org/cli/-/raw/main/docs/source/mr/list.md). Sintaxe **divergente** do wording-alvo inicial detectada: `--merged` é flag única (não `--state merged`); `--output json` produz JSON completo (sem `--fields iid`). Wording acima atualizado com sintaxe confirmada; § Verificação manual cenário 2 + "Forma do dado real" GitLab também sincronizados.

### Bloco 3 — Wire /triage e /release para referenciar o procedimento

- `skills/triage/SKILL.md`: substituir corpo de `### 0. Cleanup pós-merge` (linhas ~15-55) por 1-2 linhas referenciando `docs/procedures/cleanup-pos-merge.md`. Wording-alvo: *"Antes de carregar contexto, executar passo de cleanup pós-merge conforme `docs/procedures/cleanup-pos-merge.md`. Skip silente se nada a limpar."* Header `### 0. Cleanup pós-merge` permanece como passo numerado da skill (operador-anchored); só o corpo migra.
- `skills/release/SKILL.md`: atualizar a seção `## Cleanup pós-merge` (linhas ~25-27 atuais). Wording-alvo: *"Antes das pré-condições, executar passo de cleanup pós-merge conforme `docs/procedures/cleanup-pos-merge.md`. Skip silente se nada a limpar."*

### Bloco 4 — Addendum em ADR-001 apontando para ADR-024 {reviewer: doc}

- `docs/decisions/ADR-001-protocolo-de-templates.md`: adicionar nova seção `## Addendum (2026-05-12)` após § Gatilhos de revisão (não inline em § Gatilhos; seção própria preserva imutabilidade de § Decisão original). Wording-alvo: *"Esta nota é adendo informativo posterior à aceitação; não altera a decisão original. [ADR-024](ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md) estabelece categoria paralela `docs/procedures/` para procedimentos operacionais compartilhados; complementa este ADR sem revogá-lo. Fronteira: `templates/` = esqueletos preenchidos quando o artefato é produzido; `docs/procedures/` = procedimentos executados quando referenciados."* Invariante mecânica per ADR-024 § Decisão — sem essa edição, ADR-024 não está implementado.

### Bloco 5 — Atualizar roadmap marcando G_arch e D_arch shipped {reviewer: doc}

- `docs/audits/runs/2026-05-12-execution-roadmap.md`:
  - Marcar item G_arch (linha 38) e D_arch (linha 39) com `[x]` + link a PR/commit + data curta `2026-05-12`. Aplicar mesmo pattern dos itens shippados de Ondas 1 e 2 (linhas 20-22, 28-30).
  - **Atualizar path obsoleto na linha 38**: descrição original menciona `templates/cleanup-pos-merge.md` — caminho descartado após `/triage` ter produzido ADR-024 com `docs/procedures/`. Substituir o path inline e adicionar referência ao ADR-024 para consistência arqueológica.
  - Nota no final do bloco "3a" indicando Onda 3a fechada.
  - **G vs D shipped têm gates diferentes**: G_arch verifica-se nos greps do § Verificação end-to-end (extração + wire-up testáveis pelo `/run-plan`); D_arch (forge bilateral) só se valida via cenário 2 da § Verificação manual em consumer GitLab real pós-release. Marcar ambos `[x]` no Bloco 5 é decisão editorial honesta (mesmo PR, mesma onda) — operador rodando o smoke-test pós-release pode reabrir D_arch se cenário 2 falhar.

## Verificação end-to-end

- `test -f docs/procedures/cleanup-pos-merge.md` retorna 0 (arquivo criado pelo Bloco 1).
- `grep -q "docs/procedures/cleanup-pos-merge.md" skills/triage/SKILL.md` retorna 0 (referência wired pelo Bloco 3).
- `grep -q "docs/procedures/cleanup-pos-merge.md" skills/release/SKILL.md` retorna 0 (referência wired pelo Bloco 3).
- `grep -c "### 0. Cleanup pós-merge" skills/triage/SKILL.md` retorna 1 (header preservado como ponteiro; corpo deslocado para procedimento).
- `grep -q "glab" docs/procedures/cleanup-pos-merge.md` retorna 0 (forge bilateral aplicado pelo Bloco 2).
- `grep -q "gh pr list" docs/procedures/cleanup-pos-merge.md` retorna 0 (gh ainda usado, agora dentro do auto-detect).
- `grep -q "ADR-024" docs/decisions/ADR-001-protocolo-de-templates.md` retorna 0 (cross-reference adicionado pelo Bloco 4).
- `grep -E "^- \\[x\\] \\*\\*(G|D)_arch\\*\\*" docs/audits/runs/2026-05-12-execution-roadmap.md | wc -l` retorna 2 (Bloco 5 marcou ambos).
- Pipeline CI (`.github/workflows/validate.yml`) verde no PR.

## Verificação manual

Procedimento toca **comportamento observável** de `/triage` (passo 0) e `/release` (cleanup pré-pré-condições), incluindo **surface não-determinística** (parsing de saída do `gh`/`glab`, matching de branch, comportamento do agente em consumer GitLab). Validação manual obrigatória.

**Forma do dado real:**

- `gh pr list --state merged --head <branch> --json number --jq '.[0].number'` em PR squash-merged retorna número simples (ex: `54`).
- `glab mr list --merged --source-branch <branch> --output json` em GitLab retorna lista JSON completa de MRs mergeadas com a source-branch indicada; pipe via `jq -r '.[0].iid // empty'` extrai o IID numérico (ex: `12`) ou string vazia se nenhum match. Sintaxe confirmada via docs oficiais durante gate do Bloco 2.
- `git remote get-url origin` em consumer GitHub retorna `git@github.com:user/repo.git` ou `https://github.com/user/repo.git`.
- Em consumer GitLab corporativo retorna `git@gitlab.empresa.com:user/repo.git` ou `https://gitlab.empresa.com/user/repo.git`.
- Slug de branch típico: kebab-case sem prefixo (ex: `curadoria-free-read-design-reviewer`).

**Cenários enumerados (executar em consumer real após release):**

1. **GitHub squash-merge detection (regressão):** PR squash-merged no GitHub; invocar `/triage <intenção>`; passo 0 detecta worktree, identifica PR mergeado, oferece cleanup. Esperado: comportamento idêntico ao atual.
2. **GitLab squash-merge detection (novo via D_arch):** consumer GitLab corporativo; MR squash-mergeada; invocar `/triage`; passo 0 detecta worktree, executa `glab mr list --merged --source-branch <branch> --output json | jq -r '.[0].iid // empty'` (sintaxe confirmada durante gate do Bloco 2), identifica MR mergeada, oferece cleanup com identificador "MR !<num>". Esperado: comportamento novo funcional.
3. **Host não-mapeado (fallback):** consumer com remote `bitbucket.org`; invocar `/triage`; passo 0 cai no fallback `git branch -r --merged`. Esperado: cleanup procede sem squash-awareness, com nota.
4. **`gh` ausente no PATH:** desinstalar/desautenticar gh temporariamente em consumer GitHub; invocar `/triage`; fallback git-only. Esperado: mesmo comportamento de (3).
5. **`glab` ausente no PATH:** consumer GitLab sem glab instalado; invocar `/triage`; fallback git-only. Esperado: mesmo comportamento de (3).
6. **/release squash-detection:** mesmo cenário (1) ou (2) mas via `/release` em vez de `/triage`. Esperado: cleanup idêntico via mesmo procedimento (sem duplicação de path).
7. **Skip silente (nada a limpar):** estado limpo sem worktrees em `.worktrees/`; invocar `/triage`; passo 0 silente. Esperado: nenhuma cutucada.
8. **Mix de worktrees mergeada/não-mergeada:** ≥1 worktree mergeada + ≥1 worktree não-mergeada sob `.worktrees/`; invocar `/triage`. Esperado: cutucada só para worktrees mergeadas; não-mergeadas filtradas silenciosamente no passo 1 condição 3 do procedimento (sem detecção de merge → não é candidato).
9. **Worktree órfã (branch sumiu):** worktree presente sob `.worktrees/<slug>/` mas `git worktree list --porcelain` não retorna `branch refs/heads/<slug>` válida. Esperado: skip silente do candidato (passo 1 extrai branch da saída porcelain — ausente, pula); warning informativo opcional.
10. **GitLab sem `jq` no PATH (gap operacional):** consumer GitLab com `glab` instalado mas `jq` ausente; MR squash-mergeada existente; invocar `/triage`. Esperado: pipe `glab mr list ... | jq` produz saída vazia (jq: command not found no stderr), candidato cai em "sem detecção" e é silenciosamente pulado — NÃO cai no fallback git-only. Confirma o gap operacional documentado no procedure file. Workaround: instalar `jq` ou remover `glab` do PATH para forçar fallback.

## Notas operacionais

- **Ordem dos blocos:** 1 → 2 → 3 → 4 → 5. Bloco 1 cria arquivo AS-IS (sem mudança de comportamento; /triage e /release ainda usam conteúdo inline original). Bloco 2 estende o arquivo (forge bilateral; ainda sem efeito porque skills não referenciam). Bloco 3 switcha as duas skills para referenciar o novo arquivo (ativa novo comportamento; passam a usar procedimento extraído + forge bilateral). Bloco 4 adiciona cross-reference em ADR-001 (invariante de implementação de ADR-024). Bloco 5 atualiza roadmap.
- **Reviewer dispatch:** Blocos 1-3 default code-reviewer — arquivo novo carrega procedimento executado em runtime pelas skills (behavioral content); SKILL.md edits em Bloco 3 são behavior change. Blocos 4-5 `{reviewer: doc}` — edição cirúrgica em ADR + tracking de roadmap. `design-reviewer` **não** redisparado por `/run-plan` (ADR-011 — opera pré-fato; já disparou neste `/triage` no draft de ADR-024 e dispara automaticamente no plano).
- **BACKLOG (sem transição automática nesta onda):** linha umbrella em `## Próximos` (linha 5) cobre as 4 ondas como um todo; **não** transita para `## Concluídos` ao fim desta Onda 3a — só quando a última onda ativada fechar. `/run-plan §3.4` é mecânica determinística (move `**Linha do backlog:**` para Concluídos sem gate de skip), portanto **este plano omite deliberadamente o campo `**Linha do backlog:**` no `## Contexto`**. `/run-plan §3.4` pula silente quando o campo está ausente; o tracking da Onda 3a fica no Bloco 5 (atualização do roadmap) em vez do BACKLOG. Quando a última onda fechar, a linha umbrella transita para `## Concluídos` via plano dedicado dessa onda final (que pode preencher `**Linha do backlog:**` com o texto exato da linha 5 atual para acionar a transição mecânica do `/run-plan §3.4`).
- **Re-rodar prose-tokens depois deste plano:** roadmap linha 63 prevê — G_arch sozinho remove ~200 palavras de `/triage §0` e muda alvos restantes da Onda 4. Auditoria pode ser refeita após esta Onda fechar.
- **glab syntax confirmada durante Bloco 2:** sintaxe final aplicada é `glab mr list --merged --source-branch <branch> --output json | jq -r '.[0].iid // empty'`. Wording-alvo inicial divergiu (`--state merged` em vez de `--merged`; `--fields iid` que não existe). Gate detectou e ajustou pré-commit per docs oficiais. Pattern bilateral (gh+glab) é o segundo caso forge-bilateral no toolkit (paralelo ao `mr create --fill` / `pr create --fill` já em `/run-plan §3.7`).
- **ADR-024 já criado neste /triage:** ADR existe em `docs/decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md` (sucessor parcial de ADR-001); plano referencia, não cria. Design-reviewer findings absorvidos pré-commit (7 findings: 2 altos rename `protocols`→`procedures` e reinterpretação ADR-001; 3 médios endurecendo mitigações; 2 baixos polish).
- **Bloco 4 é load-bearing.** Sem cross-reference em ADR-001, ADR-024 § Decisão fica violado e o plano fica incompleto. Não tratar como bloco editorial opcional.

## Pendências de validação

Capturadas no gate final do `/run-plan` — smoke-test pós-release em consumer real:

- ~~**Cenário 1** — GitHub squash-merge detection (regressão); invocar `/triage` em consumer GitHub com worktree de PR squash-merged.~~ **Encerrada 2026-05-15:** sem regressão observada em uso real do toolkit no próprio repo (GitHub).
- ~~**Cenário 2** — GitLab squash-merge detection (novo via D_arch); invocar `/triage` em consumer GitLab corporativo com MR squash-mergeada.~~ **Encerrada 2026-05-15 (validação herdada por simetria mecânica do auto-detect bilateral; smoke real em consumer correspondente não exercitado):** reabrir gatilho do plano se operador adotar consumer GitLab no futuro.
- ~~**Cenário 3** — Host não-mapeado (fallback); consumer com remote `bitbucket.org`.~~ **Encerrada 2026-05-15 (validação herdada por simetria mecânica do auto-detect bilateral; smoke real em consumer correspondente não exercitado):** reabrir gatilho do plano se operador adotar consumer Bitbucket no futuro.
- ~~**Cenário 4** — `gh` ausente no PATH; consumer GitHub sem `gh`.~~ **Encerrada 2026-05-15 (validação herdada por simetria mecânica do auto-detect bilateral; smoke real em consumer correspondente não exercitado):** reabrir gatilho do plano se operador adotar consumer sem `gh` no futuro.
- ~~**Cenário 5** — `glab` ausente no PATH; consumer GitLab sem `glab` (fallback git-only).~~ **Encerrada 2026-05-15 (validação herdada por simetria mecânica do auto-detect bilateral; smoke real em consumer correspondente não exercitado):** reabrir gatilho do plano se operador adotar consumer GitLab sem `glab` no futuro.
- ~~**Cenário 6** — `/release` squash-detection; mesmo path do cenário 1 ou 2 via `/release`.~~ **Encerrada 2026-05-15:** sem regressão observada em uso real do toolkit no próprio repo — `/release` exercitado em releases consecutivas pós-shipping.
- ~~**Cenário 8** — Mix mergeada/não-mergeada em `.worktrees/`.~~ **Encerrada 2026-05-15:** sem regressão observada em uso real do toolkit no próprio repo.
- ~~**Cenário 9** — Worktree órfã (branch sumiu).~~ **Encerrada 2026-05-15:** sem regressão observada em uso real do toolkit no próprio repo.
- ~~**Cenário 10** — GitLab sem `jq` no PATH (gap operacional); consumer GitLab com `glab` instalado mas `jq` ausente. Esperado: candidato cai em "sem detecção" (não fallback git-only).~~ **Encerrada 2026-05-15 (validação herdada por simetria mecânica do auto-detect bilateral; smoke real em consumer correspondente não exercitado):** reabrir gatilho do plano se operador adotar consumer GitLab sem `jq` no futuro.

Cenário 7 (skip silente) foi auto-validado no worktree do `/run-plan` (sem `.worktrees/` sub-worktrees).
