# Plano — Role backlog aceitar forge

## Contexto

ADR-058 codifica a decisão estrutural de aceitar `paths.backlog: forge` como quarta variante do role contract — issues abertas + sem assignee do repo corrente como fonte do role `backlog`. Este plano executa a implementação: estende `forge-auto-detect.md` com 3 operações novas (issue list/close/create), atualiza 4 skills consumidoras (`/next`, `/triage` step 4, `/run-plan §3.4`, `/curate-backlog`), e atualiza CLAUDE.md (role contract + Pragmatic Toolkit schema).

**Linha do backlog:** plugin: estender role `backlog` para aceitar forge (paths.backlog: forge) — sucessor parcial de ADR-049 § Decisão (a) per ADR-058

**ADRs candidatos:** ADR-058 (decisão central deste plano), ADR-049 § Decisão (a) (ancestral direto — preservação estrutural confirmada em ADR-058 § (g)), ADR-047 § Decisão (a) (família paths.<role>: <modo>), ADR-057 (curate-backlog impactada — 4 heurísticas reinterpretadas), ADR-053 (reviewer wiring), ADR-046 (cutucada de descoberta — todas as 6 skills atuais permanecem emissoras).

## Resumo da mudança

Implementa ADR-058. **Entra:**

- `paths.backlog: forge` aceito no schema do CLAUDE.md (string literal, sem objeto v1).
- `forge-auto-detect.md` estendido com `issue list`, `issue close`, `issue create` — output discrimination idêntica à mecânica existente; bifurcação editorial: `no-detection` em operações de issue para com erro explícito (não degradação silente como PR/MR listing).
- 4 skills consumidoras com branches `if paths.backlog == forge`:
  - `/next` passo 1 (lê issues), passo 3 (fecha issue com cutucada), passo 6 (skip commit).
  - `/triage` step 4 (cria issue com cutucada; `**Linha do backlog:**` carrega `#<número>: <título>`).
  - `/run-plan §3.4` (fecha issue extraída do `**Linha do backlog:**` com cutucada).
  - `/curate-backlog` H1 (createdAt + marcas temporais), H2/H3 (title+body, escopo reduzido), H4 (inalterado).
- CLAUDE.md atualizado: role contract table linha backlog; Pragmatic Toolkit schema bullet de `forge`; nota de coexistência com modo local.
- BACKLOG.md linha 100 ("desacoplar de GitHub-específico") atualizada — predecessor doutrinal parcialmente coberto por ADR-058.

**Fica de fora (v1):**

- Cache (alternativa A — fetch sempre fresh; gatilho de revisão concreto em ADR-058).
- Schema objeto `{type: forge, filter: {...}}` (string literal sufices; promoção via gatilho).
- Labels customizadas (sem suporte).
- Cross-project/cross-group (per repo apenas).
- "Sem PR/MR aberto" cross-reference (simplifica para sem assignee; convenção parcial documentada em ADR-058 § (b)).

## Arquivos a alterar

### Bloco 1 — CLAUDE.md schema e role contract {reviewer: doc}

- `CLAUDE.md`:
  - Tabela "The role contract" linha `backlog`: atualizar para mencionar modo `forge` ("BACKLOG.md (canonical) | local | null | forge — issues abertas sem assignee do repo corrente").
  - Seção "Pragmatic Toolkit" → "Schema and semantics": adicionar bullet para `forge` (paralelo aos existentes para `null`/`local`): *"`forge` (string literal) → role lido de issues abertas sem assignee via gh/glab; mutações remotas com cutucada AskUserQuestion obrigatória. Aplica-se apenas a `backlog` na v1; outros roles rejeitam (ver ADR-058 § (a))."*
  - Seção "Local mode": nota breve que `forge` é eixo paralelo a `local`/`null` (coexiste por-role; recusa cross-mode de ADR-047 § Decisão (c) não aplica em forge porque identificador é público — ver ADR-058 § (i)).

### Bloco 2 — forge-auto-detect.md estendido com operações de issue (extensão neutra) {reviewer: doc}

- `docs/procedures/forge-auto-detect.md`: adicionar seção "Operações de issue (extensão neutra paralela ao PR/MR listing existente)" com 3 operações:
  - `issue list`: `gh issue list --state open --search "no:assignee" --json number,title,createdAt --jq '.[]'` / `glab issue list --opened --not-assignee --output json | jq -r '.[] | {number: .iid, title, createdAt: .created_at}'`.
  - `issue close`: `gh issue close N --reason completed --comment "<glosa>"` (gh: close + comentário num único comando) / `glab issue note N --message "<glosa>"` então `glab issue close N` (glab: dois comandos sequenciais — CLI assimétrica vs gh, verificado em glab 1.89.0).
  - `issue create`: `gh issue create -t "<title>" -b "<body>"` / `glab issue create -t "<title>" -d "<body>"`.
  - **Output discrimination idêntica** ao PR/MR listing (`gh`/`glab`/`no-detection`/`unsupported-host`) — procedure **permanece neutro**; policy local no caller per ADR-058 § (d). Pattern editorial dos 4 consumers existentes (cleanup-pos-merge, /archive-plans, /release, /next §4.5) preservado.
  - Nota explicativa breve no procedure que callers podem aplicar policies distintas (heurística opcional pode degradar silente; role-declared dependency exige erro explícito) — cross-ref a ADR-058 § (d) para a regra do role backlog: forge.

### Bloco 3 — `/next` adapter forge {reviewer: code}

- `skills/next/SKILL.md`:
  - Passo 1 "Ler o backlog": adicionar branch para modo forge — em vez de Read do arquivo, chamar via forge-auto-detect operações `issue list`; itens formatados como `#<número>: <título>` na lista de candidatos; top 10 por `createdAt` ascendente.
  - Passo 3 "Verificar implementação no código": branch para modo forge — em vez de "Preparar movimentação da linha para `## Concluídos` (escrever no arquivo)", disparar cutucada `AskUserQuestion` (header `Forge`, opções `Aplicar no forge` / `Cancelar`) antes de `gh/glab issue close N --reason completed --comment "<justificativa>"`. Uma cutucada por issue movida.
  - Passo 6 "Commit das movimentações": skip silente em modo forge (mutações já aplicadas remotamente; sem commit local — paralelo ao skip em modo `local`).
  - **Passo 4.5 (varrer pendências de validação em planos) inalterado em modo forge** — opera sobre `pr list`/`mr list` para detectar worktree/PR ativo (ortogonal ao role backlog); segue policy local pré-existente (`no-detection` skipa silente, é heurística informativa opcional). Anti-regression explícito.
  - **Policy de erro do caller (per ADR-058 § (d)):** em passo 1 (lista de issues), branch para `no-detection` → parar com mensagem orientando `gh auth login` / `glab auth login` / `dnf install jq`; branch para `unsupported-host` → parar com mensagem orientando declarar `paths.backlog: null` ou path canonical. Implementação local na skill (procedure forge-auto-detect.md permanece neutro).
  - Atualizar frontmatter ou prose se necessário para refletir modos suportados.

### Bloco 4 — `/triage` step 4 adapter forge {reviewer: code}

- `skills/triage/SKILL.md`:
  - Step 4 "BACKLOG" sub-fluxo: adicionar branch para modo forge. Em vez de gravar linha em `## Próximos`, disparar cutucada `AskUserQuestion` antes de `gh/glab issue create -t "<linha>" -b "<contexto>"`. Identificador `#<número>: <título>` registrado para uso downstream.
  - Step 4 caminho-com-plano: campo `**Linha do backlog:**` no `## Contexto` do plano carrega `#<número>: <título>` (não texto livre) em modo forge.
  - Sub-fluxo "criação canonical via enum" para papel `backlog` "não temos": em modo forge não dispara (forge não tem "criar canonical" — operador tem que estar em repo com `gh`/`glab` configurado).
  - "Consolidação (quando há edit em backlog)" — em modo forge: relê via `gh/glab issue list` para detectar duplicatas com issues pré-existentes (mesmo critério editorial, fonte diferente).
  - **Policy de erro do caller (per ADR-058 § (d)):** ao consumir `issue list`/`issue create` para o role backlog: forge, branch para `no-detection` → parar com mensagem orientando setup; branch para `unsupported-host` → parar com mensagem orientando declarar `paths.backlog: null` ou path canonical.

### Bloco 5 — `/run-plan §3.4` adapter forge {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - §3.4 "Concluídos": branch para modo forge — extrair `#<número>` do campo `**Linha do backlog:**` do plano via regex `#(\d+):`; disparar cutucada `AskUserQuestion` antes de `gh/glab issue close N --reason completed --comment "<glosa derivada do plano done>"`. Glosa pode citar PR # ou commit hash do done.
  - Atualizar prose para refletir que ADR-049 § Decisão (a) regra dura é estruturalmente preservada em modo forge (cross-ref a ADR-058 § (g)).
  - **Policy de erro do caller (per ADR-058 § (d)):** ao consumir `issue close` para o role backlog: forge, branch para `no-detection` → parar com mensagem orientando setup; branch para `unsupported-host` → parar com mensagem orientando declarar `paths.backlog: null` ou path canonical.

### Bloco 6 — `/curate-backlog` adapter forge {reviewer: code}

- `skills/curate-backlog/SKILL.md`:
  - Passo 1 (Ler backlog): branch para modo forge — `gh issue list --state open --search "no:assignee"` / `glab issue list --opened --not-assignee` em vez de Read de BACKLOG.md.
  - Heurística H1 (gatilhos temporais): adaptar predicado mecânico para usar `createdAt` da issue como data de adição + match de marcas `até YYYY-MM-DD` / `deadline YYYY-MM-DD` / `T+Nd` em title+body.
  - Heurística H2 (redação stale): mantida; escopo title+body de issue (limitação reconhecida em ADR-058 § Limitações — menos potente em forge).
  - Heurística H3 (mergeable items): mantida; anti-spam top-20 termos aplicado idêntico sobre title+body.
  - Heurística H4 (NOTES sinais): inalterada.
  - Salvaguarda worktree-probe: inalterada (continua ortogonal ao modo; cross-ref a ADR-058 § (g) explica por que merge artifact não materializa em forge).
  - Aplicação de H1 → fechar issue: cutucada `AskUserQuestion` por issue antes de `gh/glab issue close N`.
  - Commit unificado: em modo forge, "chore(backlog): fechar N issue(s) por curagem editorial — <data>" (sem path BACKLOG.md no message). Em modo arquivo: mensagem atual preservada.
  - **Policy de erro do caller (per ADR-058 § (d)):** ao consumir `issue list`/`issue close` para o role backlog: forge, branch para `no-detection` → parar com mensagem orientando setup; branch para `unsupported-host` → parar com mensagem orientando declarar `paths.backlog: null` ou path canonical.

### Bloco 7 — BACKLOG.md predecessor doutrinal {reviewer: doc}

- `BACKLOG.md`:
  - Linha 100 ("desacoplar de GitHub-específico") tem substância **parcialmente coberta** por ADR-058: auto-detect já existe via `forge-auto-detect.md`; role `forge` agora existe (ADR-058). **Residual:** `/release` ainda sugere `gh release create` no texto final — não tocado por ADR-058. **Ação predeterminada:** editar texto da linha 100 em `## Próximos` restringindo escopo ao residual (substituir referências a "auto-detect" e "role `forge`" por menção que ambos já existem; manter substância sobre `/release` sugerir comando neutro). **Não mover para `## Concluídos`** — cobertura parcial.

## Verificação end-to-end

Critérios objetivos para considerar a mudança válida — combinação de inspeção textual + comandos concretos. Repo não tem `make test` (`test_command: null` em CLAUDE.md), gates são inspeção.

1. **ADR-058 vigente com Status correto.** `grep -n "^\*\*Status:\*\*" docs/decisions/ADR-058-role-backlog-aceitar-forge.md` retorna `**Status:** Aceito` (mudança Proposto → Aceito pós-review).

2. **Schema documentado em CLAUDE.md em 3 locais.** `grep -nE "forge" CLAUDE.md` retorna ≥3 ocorrências: (i) role contract table linha backlog; (ii) "Schema and semantics" bullet de `forge`; (iii) "Local mode" nota de coexistência.

3. **forge-auto-detect.md cobre 3 operações de issue.** `grep -nE "issue (list|close|create)" docs/procedures/forge-auto-detect.md` retorna ≥3 linhas distintas; ≥1 com sintaxe `gh` e ≥1 com sintaxe `glab` em cada operação.

4. **Cada uma das 4 skills tem branch para modo forge.** Para cada SKILL (`next`, `triage`, `run-plan`, `curate-backlog`): `grep -nE "paths\.backlog.*==.*['\"]forge['\"]|paths\.backlog: forge" skills/<name>/SKILL.md` retorna ≥1 match. Critério verifica sintaxe condicional ou declaração explícita do modo, não menção textual livre.

5. **Cutucada AskUserQuestion específica para forge presente.** Para cada SKILL onde mutação remota aplica (next passo 3, triage step 4, run-plan §3.4, curate-backlog H1): `grep -nE "header.*\bForge\b" skills/<name>/SKILL.md` retorna ≥1 match AND `grep -nE "gh.*issue (close|create)|glab.*issue (close|create)" skills/<name>/SKILL.md` retorna ≥1 match no mesmo arquivo. Garante que cutucada nova foi adicionada (não matching `AskUserQuestion` pré-existente para outras decisões).

6. **Identificador `#<número>: <título>` documentado em CLAUDE.md (canonical) + ≥1 SKILL consumer.** `grep -nE "#<n[uú]mero>: <t[ií]tulo>" CLAUDE.md` retorna ≥1 match (definição canonical do schema). `grep -nE "#<n[uú]mero>" skills/triage/SKILL.md skills/run-plan/SKILL.md` retorna ≥1 match em pelo menos 1 (uso downstream documentado).

7. **ADR-049 § Decisão (a) preservação reconhecida em /run-plan.** `grep -n "ADR-049" skills/run-plan/SKILL.md` retorna ≥1 referência mencionando preservação estrutural em modo forge.

8. **BACKLOG.md linha 100 atualizada ou movida.** `grep -n "desacoplar de GitHub-específico" BACKLOG.md` retorna 0 linhas em `## Próximos` (movida para `## Concluídos` ou texto reformulado).

9. **Cutucada de descoberta inheritance.** `grep -c "cutucada-descoberta" skills/next/SKILL.md skills/triage/SKILL.md skills/run-plan/SKILL.md skills/curate-backlog/SKILL.md` retorna ≥4 (uma por skill emissora). Inalterado pelo plano — verificação de não-regressão.

10. **Anti-regression: skills com modo arquivo continuam funcionando.** Branch `if paths.backlog == forge` deve ser **adição** ao fluxo existente, não substituição. Verificar: cada SKILL preserva o fluxo de modo arquivo (Read de `BACKLOG.md`, edit de `## Próximos`/`## Concluídos`, etc.) intacto. Inspeção textual.

## Verificação manual

Cenários para o operador exercitar — toca surface não-determinística (issue API shapes variam entre GitHub/GitLab; mutações remotas irreversíveis). Operador tem ambiente TJPA para exercer GitLab; repos pessoais GitHub para exercer host alternativo.

### Cenário 1 — `/next` em projeto TJPA (GitLab) com modo forge

1. Em repo TJPA com `paths.backlog: forge` declarado no CLAUDE.md, invocar `/next`.
2. Skill deve fazer `glab issue list --opened --not-assignee --output json | jq ...` e listar top 10 issues por `createdAt` ascendente.
3. Verificar itens formatados como `#<número>: <título>` (separador `: `, sem ID interno do GitLab vazando).
4. Para uma issue com evidência forte no código (escolher manualmente uma issue cuja feature está claramente implementada), cutucada `AskUserQuestion` (header `Forge`) aparece antes de `glab issue close N`.
5. Confirmar `Aplicar no forge` → verificar no GitLab UI que issue foi fechada com `state_reason: completed` e comment foi adicionado.
6. Confirmar `Cancelar` → noop; verificar no GitLab que issue permanece aberta sem comment novo.
7. Variação: candidato em evidência fraca → skill reporta sem mutar; sem cutucada.

### Cenário 2 — `/triage` step 4 em repo TJPA — caminho linha-pura

1. Em repo TJPA com `paths.backlog: forge`, invocar `/triage "exportar movimentos em CSV"`.
2. Step 3 decide "Só linha no BACKLOG" (caminho linha-pura).
3. Step 4 deve disparar cutucada `AskUserQuestion` antes de `glab issue create -t "exportar movimentos em CSV" -d "<contexto>"`.
4. Confirmar `Aplicar` → issue criada; verificar URL retornada e identificador `#<número>` no relato final.
5. Confirmar `Cancelar` → noop; sem issue criada.

### Cenário 3 — `/triage` step 4 caminho-com-plano em modo forge

1. Invocar `/triage` com intenção que produz plano (multi-fase).
2. Step 4 cria plano em `docs/plans/<slug>.md` + (após cutucada) issue no GitLab para a feature.
3. Campo `**Linha do backlog:**` no `## Contexto` do plano carrega `#<número>: <título>` retornado pela create — não texto livre.
4. Plano commit + push como sempre.
5. Variação: `paths.backlog: forge + paths.plans_dir: local` (caso válido per ADR-058 § (i)) — plano vai para `.claude/local/plans/<slug>.md`; linha do backlog continua sendo `#<número>: <título>` do forge.

### Cenário 4 — `/run-plan §3.4` fecha issue no done

1. Plano produzido no Cenário 3 com `**Linha do backlog:** #N: <título>` no `## Contexto`.
2. `/run-plan <slug>` executa até gate final; §3.4 dispara cutucada antes de `glab issue close N --comment "<glosa derivada do plano done>"`.
3. Confirmar `Aplicar` → issue fechada no GitLab; verificar `state_reason: completed` + comment.

### Cenário 5 — `/curate-backlog` em modo forge

1. Em repo TJPA com `paths.backlog: forge` e ≥10 issues abertas sem assignee, invocar `/curate-backlog`.
2. Heurística H1 (gatilhos temporais): verificar que `createdAt` antigo (>6 meses) + marcas `até YYYY-MM-DD` vencidas em title/body geram findings.
3. Heurística H2 (redação stale): verificar judgment do agente sobre title+body — refs a paths renomeados / ADRs obsoletos.
4. Heurística H3 (mergeable items): verificar similaridade entre titles de 2+ issues distintas.
5. Heurística H4 (NOTES sinais): inalterada — leitura de `.claude/local/NOTES.md` continua identificando sinais cruzados.
6. Salvaguarda worktree-probe: em worktree main-só, mutações aplicadas direto; em ≥1 worktree adicional, defer via NOTES.md (inalterado).
7. Aplicar tudo → para cada finding H1, cutucada `AskUserQuestion` por issue antes de fechar.

### Cenário 6 — CLI ausente / auth ausente / host não suportado (erro explícito)

1. Em ambiente sem `gh`/`glab` no PATH (ou com `glab` autenticado mas `paths.backlog: forge` declarado em repo GitHub), invocar `/next`.
2. Skill deve **parar com erro explícito** orientando setup — não degradar silente.
3. Mensagem deve nomear comando de setup específico (`gh auth login` / `glab auth login` / `dnf install jq` conforme o gap).
4. Variação A: `jq` ausente em fluxo GitLab → erro orientando install do `jq`.
5. Variação B: `unsupported-host` — `paths.backlog: forge` declarado em repo Bitbucket / repo sem remote / host customizado. Skill deve parar com erro explícito orientando declarar `paths.backlog: null` ou path canonical (não há fallback git-only — issues não vivem em git, paralelo a `cleanup-pos-merge.md` policy local).

### Cenário 7 — paths.backlog: forge em repo GitHub (variação de host)

1. Em repo GitHub pessoal com `paths.backlog: forge`, invocar `/next`.
2. Skill auto-detecta `gh` via forge-auto-detect.
3. Comportamento equivalente ao Cenário 1 com sintaxe `gh issue list --state open --search "no:assignee" --json number,title,createdAt`.
4. Verificar que parse JSON funciona (forma do dado real do `gh issue list --json` pode diferir de `glab`).

### Cenário 8 — Race condition latente (informacional)

1. Operador A invoca `/next` em repo TJPA; vê issue #123 como candidata.
2. Operador B atribui #123 a si mesmo no GitLab UI antes do A escolher.
3. Operador A escolhe #123 → cutucada → confirma → `glab issue close 123` aplica mesmo assim (issue não re-fetched antes da mutação).
4. Comportamento esperado v1: aceito (assignee não bloqueia close API). Race latente documentada em ADR-058 § Limitações + gatilho de revisão registrado. Sem fix v1.

### Cenário 9 — Coexistência local + forge ortogonais

1. Repo com config: `paths.backlog: forge`, `paths.decisions_dir: local`, `paths.plans_dir: local`.
2. Invocar `/triage` com intenção que produz ADR + plano.
3. ADR vai para `.claude/local/decisions/ADR-NNN-*.md` (modo local — gitignored).
4. Plano vai para `.claude/local/plans/<slug>.md` (modo local — gitignored).
5. Linha do backlog → cutucada → `glab issue create` (modo forge — público).
6. Commit do `/triage` não referencia ADR ID nem slug do plano (regra de não-referenciar de ADR-047), mas pode referenciar `#<número>` da issue (forge é público — ADR-058 § (i)).

## Pendências de validação

Capturadas pelo `/run-plan §3.5` durante execução do plano. Validação real exige `paths.backlog: forge` declarado em consumer real — plugin (este repo) não tem o modo. Validação textual + revisão por blocos aceitos no done (operador escolheu `Validei` no §3.2 com cenários diferidos como pendências).

- Cenários 1-9 do `## Verificação manual` deste plano — executar em ambiente TJPA real (`paths.backlog: forge` em repo GitLab) + repo GitHub pessoal (variação de host) + ambiente sem `gh`/`glab` instalado (cenário 6 erro explícito) + repo Bitbucket/sem remote (cenário 6 sub-cenário `unsupported-host`). Capturar findings empíricos por cenário; alimenta gatilhos de revisão de ADR-058 (latência reportada, race conditions, falsos positivos do "sem PR/MR aberto" simplificado v1, cutucada por mutação irritando power-user).

## Notas operacionais

- **Ordem dos blocos:** Bloco 1 (CLAUDE.md schema) e Bloco 2 (forge-auto-detect.md) primeiro porque outros blocos dependem do schema definido e das operações disponíveis. Blocos 3-6 (skills) em paralelo possível, mas cada um carrega risco de regressão no modo arquivo — single-reviewer code por bloco. Bloco 7 (BACKLOG.md) por último — depende da decisão tomada em si para refletir corretamente.
- **Salvaguarda durante implementação:** evitar mutações remotas acidentais durante dogfood do plano. Preferir repo de teste pessoal ou repo TJPA sandbox; **não dogfoodar `/curate-backlog` modo forge no próprio plugin** (pragmatic-dev-toolkit não tem `paths.backlog: forge`; mantém modo arquivo).
- **Cutucada por mutação:** durante review do código por bloco, garantir que NENHUMA mutação remota dispare sem `AskUserQuestion` precedente. Critério mecânico para o reviewer: `grep` no diff por chamadas a `gh/glab issue (close|create|edit)` e verificar que cada uma é precedida de cutucada.
- **CLI dependencies:** assumir `gh` 2.40+ e `glab` 1.40+ por features de JSON output (`--json`). `gh` filtra "sem assignee" via qualifier de busca `--search "no:assignee"` (não tem flag dedicada — verificado empiricamente em gh 2.91.0); `glab` tem flag dedicada `--not-assignee`. Documentar como pré-requisito em forge-auto-detect.md.
- **Status do ADR-058:** muda de Proposto → Aceito ao fim deste plano (no done de `/run-plan §3.6`). Edit cirúrgico em ADR-058 linha 3 como parte do gate final.
- **Predecessor BACKLOG linha 100:** decisão "mover vs editar texto" deve considerar que a substância original era sobre push/PR creation em /release e /run-plan; ADR-058 cobre **role backlog** mas não tocou push/PR creation explicitamente (forge-auto-detect.md já cobre essa parte via PR/MR list para cleanup). Ver se substância ainda tem componente residual antes de mover totalmente.
- **NÃO criar `.claude/local/cache/`** — alternativa A (sem cache) é decisão v1 do ADR-058. Tentação de "vou adicionar cache rapidinho enquanto estou aqui" é regressão à alternativa (c) descartada.

## Decisões absorvidas

### Do review do ADR-058

- ADR-058 § (b): hedge premissa fática sobre auto-assign convention — nomear que GitLab é configurável e GitHub não-default (caminho-único).
- ADR-058 § (e): nomeado pattern competidor batched (/archive-plans + /curate-backlog usam gate único) e por que forge merece shape diferente (3 chances de reverter ausentes em forge) (caminho-único).
- ADR-058 § (g): adicionado parágrafo nomeando preservação estrutural de ADR-049 § Decisão (a) em modo forge — state-tracker remoto idempotente; salvaguarda worktree-probe de ADR-057 também não aplica (caminho-único).
- ADR-058 § (i): clarificada direção-do-leak nomeando o mensageiro `**Linha do backlog:**` que ADR-047 § Decisão (c) identifica; combinação `forge + plans_dir: canonical` é válida (caminho-único).
- ADR-058 § Limitações: adicionado bullet sobre 2 fetches em /next modo forge (passo 1 + passo 4.5) — operações ortogonais sem dedupe natural (caminho-único).
- ADR-058 § Decisão (k): removido — duplicava § Alternativas (e); buffer local intermediário fica só em alternativas (caminho-único editorial).
- ADR-058 § Auto-aplicação cond 4: rebatida explícita à contra-leitura "forge como fonte ontológica nova" + gatilho de revisão concreto registrando a alternativa para maturação futura (caminho-único; alternativa mantida para reabertura informada se ≥2 outros roles ganharem demanda por fonte remota).

### Do review do plano

- Plano Bloco 7: pré-decidido — editar texto da linha 100 do BACKLOG (cobertura parcial; residual sobre `/release`), não mover para Concluídos. Justificativa em prosa do bloco (caminho-único).
- Plano § Verificação end-to-end critérios 4, 5, 6: refinados para sinais específicos — critério 4 exige `paths.backlog.*==.*forge` (sintaxe condicional); critério 5 exige `header.*\bForge\b` AND match de `gh/glab issue (close|create)` no mesmo arquivo; critério 6 exige match em CLAUDE.md (canonical) AND ≥1 SKILL consumer (caminho-único).
- Plano § Verificação manual Cenário 6: adicionado sub-cenário `unsupported-host` (Bitbucket/sem remote) — cobre 3 gaps de erro explícito (CLI, jq, host) que ADR-058 § (d) prevê (caminho-único).
- Plano Bloco 3 (/next): bullet declarando passo 4.5 inalterado em modo forge — anti-regression explícito (caminho-único).
