# ADR-058: Role backlog aceita forge como fonte (sucessor parcial de ADR-049 § Decisão (a))

**Data:** 2026-06-10
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-049](ADR-049-execucao-run-plan-consolidado.md) § Decisão (a) — codificou state vivo em git/forge mas restringiu o role `backlog` ao arquivo `BACKLOG.md` (`## Próximos` curatorial + `## Concluídos` editorial append-only). Este ADR estende o role para aceitar forge como **fonte**, não apenas como destino de state in-flight.
- **Decisão base:** [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) § Decisão (a) — codificou pattern `paths.<role>: <modo>` com 3 modos (canonical/local/null). Este ADR introduz `forge` como **quarta variante** paralela da família.
- **Decisão base:** [ADR-057](ADR-057-curate-backlog-manutencao-editorial-periodica.md) — codifica `/curate-backlog` com 4 heurísticas (H1 temporais predicado mecânico, H2 redação stale, H3 mergeable items, H4 NOTES sinais). Este ADR exige reinterpretação dessas heurísticas para issues como fonte.
- **Decisão base:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 5 (sucessor parcial) — aplica primária. Cond 1/2/3/4 não aplicam (justificativa em § Auto-aplicação).
- **Investigação:** sessão 2026-06-10 — operador trouxe demanda concreta de projetos guarda-chuva TJPA (times de devs operam backlog no GitLab, não em arquivo). Memory `project_tjpa_backlog_forge.md` salvo na mesma sessão. Predecessor BACKLOG.md linha 100 ("desacoplar de GitHub-específico") cobria PR/issue creation em `/run-plan` e `/release` — este ADR cobre o gap distinto de **backlog como fonte**.

## Contexto

ADR-049 § Decisão (a) estabeleceu: `BACKLOG.md` cumpre 2 papéis (`## Próximos` curatorial + `## Concluídos` editorial append-only); state vivo de in-flight work = branches/PRs descobríveis via `git branch` / `gh pr list`. A divisão é funcional, não substitui o role — o role `backlog` permanece atrelado ao arquivo markdown como destino canonical único.

Projetos guarda-chuva TJPA operam diferente: times de devs já mantêm o backlog no GitLab (issues abertas), não em arquivo. Hoje o operador tem dois caminhos: (i) `paths.backlog: null` — role desativado, skills consumidoras (`/next`, `/triage` step 4, `/run-plan §3.4`, `/curate-backlog`) não aplicam, perde valor das skills mais usadas do toolkit; (ii) duplicar issues em `BACKLOG.md` — state drift entre forge e arquivo, manutenção dupla.

Lacuna: o role `backlog` aceita 3 modos (path canonical, `local`, `null`/`false`) mas não aceita "forge como fonte". ADR-047 § Decisão (a) já estabeleceu pattern `paths.<role>: <modo>` com modos como valores literais — adicionar `forge` é extensão natural da família.

`docs/procedures/forge-auto-detect.md` já dogfooda mecânica de detecção `gh`/`glab` em 4 SKILLs (`/next` passo 4.5, `/release`, `/run-plan §3.7`, `cleanup-pos-merge.md`). Estender de `pr list`/`mr list` para `issue list`/`issue close`/`issue create` é incremento de ~3 operações sobre infra existente, não invenção.

## Decisão

**Estender role `backlog` para aceitar `paths.backlog: forge` como quarta variante paralela a `local`/`null`/path-canonical. Forge como fonte = issues abertas + sem assignee do repo corrente, auto-detect via `gh`/`glab` per `forge-auto-detect.md` estendido. Mutações remotas (criar issue, fechar issue) sempre precedidas de cutucada `AskUserQuestion` — blast radius muda (mutação imediata visível a todos). Sem cache na v1 (alternativa A — fetch sempre fresh); gatilho de revisão concreto para promover diretamente para revalidação seletiva se latência virar dor.**

### Escopo e mecanismo unificado

#### (a) Schema: `paths.backlog: forge` (string literal)

Pattern paralelo a `paths.backlog: local` (ADR-047 § Decisão (a)). String literal — sem objeto (`{type: forge, filter: {...}}`) — porque o recorte canonical é fixo e único na v1 (issues abertas + sem assignee, sem labels). Forward-compat para objeto fica disponível se labels/recorte virarem demanda concreta (gatilho de revisão abaixo).

Outros roles continuam rejeitando modo forge — paralelo a ADR-047 § Decisão (a) que rejeita modo local para `version_files`/`changelog`. `decisions_dir`, `plans_dir`, `version_files`, `changelog` rejeitam `forge` (não há "forge como diretório de decisões" ou "forge como fonte de version_files" no contrato). Skill que detecta valor `forge` em role não suportado para com mensagem clara.

#### (b) Recorte canonical: issues abertas + sem assignee

V1 confia em assignee como proxy para "sem PR/MR aberto". Convenção parcial: GitLab tem configuração explícita de auto-assign on MR (depende de setting da instância/projeto); GitHub requer Actions/app custom para auto-assign (não default — `Closes #N` fecha issue ao mergear mas não atribui). Simplifica em troca de precisão — projetos que não exercem a convenção verão issues com PR/MR já aberto sendo propostas como candidatas. Gatilho de revisão registrado se incidência empírica relatar.

Sem labels v1 — cada projeto tem conjunto distinto de labels, configurar no schema adicionaria configuração paralela sem ganho universal. Forward-compat via schema objeto se demanda emergir.

#### (c) Identificador canonical: `#<número>: <título>`

Em modo forge, identificador de item = `#<número>: <título>` (ex.: `#123: Exportar movimentos em CSV`). Paralelo ao texto literal de linha em modo arquivo. Estabilidade do identificador no forge é mais alta que texto literal (texto pode ser editado depois; número é imutável); permite link bidirecional automático em commits/PRs (GitHub/GitLab auto-linkify `#N`).

Em mensagens internas (commits, planos, NOTES, etc.), identificador segue forma `#<número>: <título>`. Em modo `local` + `forge` (combinação válida, § (i) abaixo), identificador forge é **público** (issue existe no remote por construção), então a regra de não-referenciar de ADR-047 não se aplica — não há leak de texto privado para metadata pública.

#### (d) Auto-detect via `forge-auto-detect.md` estendido (procedure neutro + policy no caller)

`forge-auto-detect.md` (procedure existente para PR/MR listing) ganha 3 operações novas: `issue list`, `issue close`, `issue create`. Output discrimination **idêntica** à mecânica existente — procedure **permanece neutro** (`gh`/`glab`/`no-detection`/`unsupported-host`); policy local em cada caller, paralelo aos 4 consumers existentes do procedure (`cleanup-pos-merge.md`, `/archive-plans`, `/release`, `/next §4.5`).

Comandos canonical (compostos pelo caller após detection):

- `gh` → `gh issue list --state open --search "no:assignee" --json number,title,createdAt --jq '.[]'`; `gh issue close N --reason completed --comment "<justificativa>"`; `gh issue create -t "<linha>" -b "<contexto>" --json number,url`.
- `glab` → `glab issue list --opened --not-assignee --output json | jq ...`; `glab issue close N`; `glab issue create -t "<linha>" -d "<contexto>"`.

**Policy do caller para role `backlog: forge`** — implementada em cada uma das 4 skills consumidoras (`/next`, `/triage`, `/run-plan`, `/curate-backlog`):

- `no-detection` (CLI ausente em host mapeado, ou `jq` ausente em GitLab path) → **caller para com erro explícito** orientando setup (`gh auth login` / `glab auth login` / `dnf install jq`). Sem degradação silente — role declarado depende inteiramente do CLI.
- `unsupported-host` (Bitbucket, Codeberg, host customizado, sem remote) → **caller para com erro explícito** orientando declarar `paths.backlog: null` ou path canonical. Sem fallback git-only (issues não vivem em git).

Pattern editorial do procedure preservado — "detection neutro + policy no caller" continua load-bearing. Bifurcação semântica ("role-declared dependency exige CLI" vs "heurística opcional pode degradar") vive nas skills, não no procedure. Forward-compat preservada — operações de issue podem ganhar consumer futuro com semântica diferente (heurística informativa) sem mudar policy embutida no procedure.

#### (e) Mutações remotas com cutucada `AskUserQuestion` obrigatória

Blast radius muda: em modo arquivo, mutações ficam locais até push (3 chances de reverter — descartar edit antes de commit, descartar commit antes de push, descartar push). Em modo forge, mutações remotas (`issue close`, `issue create`) são imediatas e visíveis a todos no segundo em que acontecem.

Toda mutação remota é precedida de `AskUserQuestion`:

- Header: `Forge`
- Opções: `Aplicar no forge` (Recommended) / `Cancelar (não aplicar)`
- `description` da opção `Aplicar` carrega a operação concreta (ex.: `"gh issue close #123 --reason completed --comment '<glosa>'"`).
- **Uma cutucada por mutação** — sem batched para múltiplas mutações na mesma invocação. Trade-off: mais cliques, mas blast radius cumulativo é o argumento.

**Pattern competidor documentado e rebatido:** `/archive-plans` (ADR-022) e `/curate-backlog` (ADR-057) usam gate único batched (`Aplicar tudo` / `Aplicar parcial` / `Cancelar`) sobre múltiplas mutações da mesma invocação. Pattern recusado aqui porque essas skills operam sobre arquivo-local com 3 chances de reverter (descartar edit antes de commit, descartar commit antes de push, descartar push antes de merge); mutações em forge são imediatamente visíveis a todos sem chance de reverter. Gate único "aplicar 5 issues remotas batched" agruparia decisões irreversíveis num clique. Gatilho de revisão registrado se power-user reportar fricção cumulativa.

Aplica a 4 superfícies: `/triage` step 4 (criar issue), `/next` passo 3 (fechar issue de feature implementada via evidência forte), `/run-plan §3.4` (fechar issue da feature em done), `/curate-backlog` H1 (fechar issue com gatilho temporal vencido).

#### (f) Sem cache na v1 (alternativa A)

Cada invocação faz fetch fresh via `gh issue list` / `glab issue list`. Tipicamente 1-3 segundos por invocação (1-5s em repo grande). `/next` rodado ~3× por sessão = ~6s acumulados — incômodo gerenciável vs zero stale risk.

Gatilho de revisão concreto: latência reportada ≥3 vezes pelo operador OU >5s consistente em projeto TJPA típico → promover diretamente para revalidação seletiva no ponto crítico (alternativa (d) em § Alternativas, reservada como destino de promoção). Pular cache TTL curto (alternativa (c) descartada — estado intermediário com pior tradeoff entre A e (d)).

#### (g) Skills consumidoras impactadas (4)

| Skill | Operação | Comportamento em modo forge |
|---|---|---|
| `/next` passo 1 | Ler `## Próximos` | `gh/glab issue list --state open --no-assignee` (top 10 por `createdAt` ascendente); itens formatados `#<número>: <título>`. |
| `/next` passo 3 | Mover impl. forte → Concluídos | Cutucada por issue antes de `gh/glab issue close N --reason completed --comment "<justificativa>"`. |
| `/next` passo 6 | Commit movimentações | **Skip** — mutações já foram aplicadas remotamente via fechar issue; sem commit local. Paralelo a modo `local` onde commit é skipado por arquivo gitignored. |
| `/triage` step 4 | Criar entrada de backlog (caminho sem plano OU itens fora-de-escopo) | Cutucada antes de `gh/glab issue create -t "<linha>" -b "<contexto>"`. URL/number retornado registrado para uso downstream. |
| `/triage` step 4 | `**Linha do backlog:**` no plano (caminho com plano) | Após criar issue, campo `**Linha do backlog:**` no `## Contexto` do plano carrega `#<número>: <título>` (não texto livre). `/run-plan §3.4` usa esse identificador para fechar issue no done. |
| `/run-plan §3.4` | Append em `## Concluídos` | Cutucada antes de fechar issue da feature, identificada via `#<número>` extraído do campo `**Linha do backlog:**` do plano. |
| `/curate-backlog` H1 | Gatilhos temporais → Concluídos | Cutucada antes de fechar issue. Filtro temporal aplicado via `createdAt` da issue + match de marcas `até YYYY-MM-DD` / `deadline YYYY-MM-DD` em title/body. |
| `/curate-backlog` H2 | Redação stale | Mantém — sobre title+body de issue. Refs a paths renomeados / ADRs Substituídos / skills extintas. Limitação: menos potente que markdown (issues raramente carregam refs estruturais como BACKLOG.md). |
| `/curate-backlog` H3 | Mergeable items | Mantém — sobre title+body. Anti-spam top-20 termos aplicado idêntico. Limitação: similaridade por title funciona; por body é mais frágil que markdown. |
| `/curate-backlog` H4 | NOTES.md sinais | **Inalterado** — NOTES.md é local e ortogonal ao modo do backlog. |
| `/curate-backlog` worktree-probe | Salvaguarda concorrência ADR-049 | Mantém — `/run-plan §3.4` em outra worktree continua sendo o risco; salvaguarda ortogonal ao modo do backlog. |

**Preservação estrutural de ADR-049 § Decisão (a) em modo forge.** A regra dura de ADR-049 § Decisão (a) (`/run-plan §3.4` apenas adiciona em `## Concluídos`, sem mover de outra seção) é **estruturalmente preservada** em modo forge — operação "fechar issue" opera sobre state-tracker remoto idempotente (`gh/glab issue close N` em issue já fechada é noop ou erro explícito, não merge artifact). A razão original de ADR-049 (concorrência multi-PR sobre o mesmo arquivo markdown gerando merge artifact em `## Concluídos`) **não se materializa** quando o state vive no forge — não há arquivo concorrente para mesclar. Salvaguarda worktree-probe de ADR-057 também não aplica aqui pelo mesmo motivo (sua razão é concorrência local entre `/curate-backlog` e `/run-plan §3.4` sobre BACKLOG.md). Em modo forge, race condition possível é "operador propõe candidato já tomado por outro dev entre fetch e mutação" — categoria conceitual distinta de merge artifact; gatilho de revisão registrado se incidência empírica relatar.

#### (h) Valor editorial via comentários em issues fechadas

Em modo arquivo, `## Concluídos` é stream agregado cronológico de glosa editorial ("Flagado pelo X durante Y", "Movido após PR #N com falha em Z"). Em modo forge, glosa editorial = comentário em issue fechada via `--comment "..."` no `issue close` + `state_reason: completed`.

Trade-off aceito: **perde stream agregado**. Para inspecionar histórico de itens concluídos em modo forge, operador filtra `gh/glab issue list --state closed` ordenando por `closedAt`. Para times, ergonomia é equivalente (notification, search nativo do forge). Para solo, pode incomodar — mas modo forge é caso de time por construção (motivação para `paths.backlog: forge` = colaboração de equipe; solo provavelmente fica em modo arquivo ou local).

#### (i) Coexistência com modo local (ortogonal por role)

`paths.backlog: forge` + `paths.decisions_dir: local` é caso válido — backlog do time + decisões locais do dev específico, ortogonais. Paralelo a ADR-047 § Decisão (a): modo local aplica per-role independentemente.

`paths.backlog: forge` + `paths.plans_dir: local` é caso válido — backlog do time, planos privados do dev. Identificador `**Linha do backlog:**` no plano local pode citar `#<número>: <título>` do forge sem leak (issue é pública por construção).

Combinação **recusada** análoga a ADR-047 § Decisão (c) (`backlog: local + plans_dir: canonical`): **não aplica em modo forge**. O critério de ADR-047 opera sobre o mensageiro `**Linha do backlog:**` no `## Contexto` do plano (que viraria leak privado→público quando backlog é local e plano é canonical). Em modo forge, esse mensageiro carrega `#<número>: <título>` (per § (c)) — identificador público por construção (issue existe no remote). Não há leak privado→público a evitar; combinação `paths.backlog: forge + paths.plans_dir: canonical` é **válida**.

#### (j) Cross-project/cross-group não é escopo v1

Backlogs TJPA são **por repo** (`gh issue list` / `glab issue list` opera no repo corrente via auto-detect de remote). Cross-group queries (`gh search issues --owner TJPA assignee:none` ou `glab issue list --group=TJPA`) é caso fora de escopo da v1 — adiciona configuração paralela sem demanda concreta documentada. Forward-compat via schema objeto se demanda emergir (gatilho de revisão).

### Razões

- **Demanda concreta documentada.** TJPA é caso motivador empírico — operador declarou ≥3 instâncias em projetos guarda-chuva (memory `project_tjpa_backlog_forge.md` salvo 2026-06-10). Não é YAGNI especulativo.
- **Pattern `paths.<role>: <modo>` já estabelecido.** ADR-047 § Decisão (a) abriu a família com 3 modos; este ADR adiciona quarto membro paralelo sem inverter ou contradizer ADR-047.
- **Infraestrutura existe.** `forge-auto-detect.md` é dogfoodado em 4 SKILLs; estender de PR/MR para issue é incremento de ~3 operações, não invenção. Output discrimination + erro explícito vs degradação são patterns já reconhecidos.
- **Cutucada como contenção do blast radius.** Mutação remota é imediata e visível; enum `AskUserQuestion` materializa a diferença para operador sem permitir que skill opere em background. Pattern paralelo a `AskUserQuestion` em `/release` antes de tag/push.
- **Recorte mínimo + identificador estável.** Issues abertas sem assignee (recorte único v1, sem labels) + `#<número>: <título>` (identificador canonical) → contrato simples; decisões deferidas via gatilhos de revisão concretos, não YAGNI especulativo.

### Trade-offs

- **4 skills viram adapter-aware.** `/next`, `/triage` step 4, `/run-plan §3.4`, `/curate-backlog` ganham branch `if paths.backlog == forge`. Custo de manutenção real — paralelo a modo `local` que adicionou branches em N skills.
- **Valor editorial muda forma.** Stream agregado cronológico de `## Concluídos` vira filtragem `gh issue list --state closed`. Para times, ergonomia equivalente; para solo, pode incomodar — mas modo forge é caso de time por construção.
- **Performance: rede em vez de FS.** Cada invocação `/next` paga 1-3s (até 5s em repo grande). Acumulado por sessão típica: ~6s. Gatilho de revisão registra threshold para promover cache.
- **Mutação remota é mais cara de reverter.** Fechar issue por engano = reabrir manualmente; criar issue por engano = fechar + opcionalmente deletar. Cutucada `AskUserQuestion` por mutação é a mitigação primária; pode irritar operador power-user que faz 5 mutações em sequência.
- **`forge-auto-detect.md` cresce.** Procedure ganha 3 operações novas (`issue list`/`close`/`create`); ~50 linhas adicionais. Não estatutariamente problemático, mas materializa categoria "issue operations" paralela a "PR/MR operations" dentro do mesmo procedure file.

### Limitações

- **v1 confia em assignee como proxy para "sem PR/MR aberto".** Cruzar com `gh pr list --search "linked:#N"` é factível mas adiciona segunda query por issue (latência multiplicativa). Aceitar imprecisão em troca de simplicidade. Gatilho de revisão registrado se operador relatar candidatos mostrados com MR já aberto.
- **Sem cache.** Cada invocação paga rede. Aceitável para `/next` (uso por sessão) — incômodo crescente para `/curate-backlog` (varredura periódica) se issues forem volumosas (>100). Gatilho de revisão concreto registrado.
- **Sem suporte a labels customizadas.** Cada projeto tem conjunto distinto; configurar label requer schema objeto. Forward-compat preservada via gatilho.
- **Cross-project não suportado.** Backlog por repo apenas. Cross-group/cross-org via search query custom não cabe na v1.
- **`/curate-backlog` H2/H3 menos potentes em modo forge.** Issues têm title (curto) + body (livre); refs a paths renomeados / ADRs raramente aparecem em comparison com markdown agrupado. Mergeable items via similaridade de title funciona; via body é mais frágil. Aceitar limitação — `/curate-backlog` em modo forge agrega menos valor que em modo arquivo, mas continua aplicável (H1, H4 inalterados; H2/H3 com escopo reduzido).
- **Identificador `#<número>: <título>` vincula ao remote vivo.** Se issue for renomeada no forge, identificador em planos/commits passa a divergir do title atual. Number permanece estável; title fica histórico. Trade-off aceito — equivalente a texto literal de linha que também pode envelhecer.
- **`/next` em modo forge faz 2 fetches do forge por invocação.** Passo 1 (issues abertas sem assignee) + passo 4.5 (PR/MR list para cleanup pós-merge). Operações ortogonais (issues vs PRs) — sem dedupe natural. Latência cumulativa per § (f) considera ambos; em projetos com muitas PRs abertas, custo do passo 4.5 pode dominar.

### Mitigações

- **Cutucada por mutação remota é gate hard.** Sem flag para suprimir; default conservador. Operador power-user que reclama → gatilho de revisão reabre critério.
- **Erro explícito em CLI ausente.** Skill para com mensagem orientando setup (`gh auth login`, `glab auth login`, `dnf install jq`) em vez de degradar silente. Operador sabe imediatamente onde está o problema.
- **Identificador `#<número>: <título>` materializa link bidirecional grátis.** Commit referenciando `#123` ganha link automático no forge (GitHub/GitLab auto-linkify). Permite navegação rápida sem operador manter mapa mental.
- **Gatilhos de revisão concretos.** 6 gatilhos abaixo cobrem casos de over-correção, latência, demanda por labels, race conditions, falsos positivos, frustração de power-user — não é YAGNI especulativo, é compromisso de revisar com critério mensurável.

## Alternativas consideradas

### (a) Manter status quo — operador usa `paths.backlog: null` e opera fora do toolkit

Operador que quer backlog em forge desativa o role; skills consumidoras (`/next`, `/triage` step 4, `/run-plan §3.4`, `/curate-backlog`) pulam a etapa ou caem no track "inform and stop".

Descartada:

- **Perde valor.** Skills úteis do toolkit (`/next` para orientação top 3, `/triage` step 4 para captura, `/curate-backlog` para manutenção editorial) ficam inaplicáveis em projetos TJPA — exatamente o ecossistema mais ativo do operador.
- **Demanda concreta documentada.** Operador trouxe caso motivador empírico; ignorar via `null` é capitular ao gap real.
- **Pattern `paths.<role>: <modo>` já comporta extensão.** ADR-047 § Decisão (a) abriu a família — `null` é só uma das opções, adicionar `forge` segue o pattern sem inverter.

### (b) Schema objeto `{type: forge, filter: {label: backlog, ...}}` em vez de string literal

Schema rico permite recorte custom (label, milestone, assignee=self, project board específico).

Descartada para v1:

- **YAGNI.** Recorte canonical (issues abertas + sem assignee) cobre o caso TJPA documentado.
- **Cada projeto teria conjunto de labels distinto.** Codificar configuração de labels no schema desloca complexidade para o operador sem reduzir variabilidade real.
- **Forward-compat preservada.** String literal `forge` pode ser promovido para objeto se demanda emergir — schema atual é subset do objeto futuro (`forge` literal ≡ `{type: forge}` implícito).
- **Gatilho de revisão concreto registrado** abaixo.

### (c) Cache TTL curto (5-10 min) em vez de fetch sempre fresh

Cache local em `.claude/local/cache/backlog-forge.json` com TTL curto. Latência baixa em invocações próximas; stale risk dentro do TTL.

Descartada:

- **Stale risk em time concorrente.** Outro dev pode pegar issue dentro do TTL — operador propõe candidato já tomado, mutação remota falha ou pior, fecha issue de outro.
- **Pior tradeoff entre (a-este-ADR) e (d) abaixo.** Cache TTL curto paga complexidade (schema, invalidação, purga) com ganho marginal (~6s economizados por sessão). Cache com revalidação seletiva ((d)) oferece zero stale crítico — TTL curto é estado intermediário com pior dos dois mundos.
- **Gatilho de revisão pula direto para (d).** Se latência virar dor, promover para revalidação seletiva — não passar por TTL curto.

### (d) Cache TTL longo + revalidação seletiva no ponto de mutação

Cache TTL longo (1h+) para a lista; revalidação pontual no momento da mutação (`gh issue view #N --json state,assignee`) antes de fechar/atribuir. Se status mudou (issue assignada/fechada entre fetch e escolha), abortar com mensagem.

**Descartada para v1, reservada como destino de promoção.**

- **Complexidade desnecessária na v1.** Mais simples começar sem cache e promover via gatilho concreto que codificar I/O de 2 caminhos antes da demanda materializar.
- **Reservada para gatilho.** Se latência reportada ≥3 vezes OU race conditions empíricas relatadas, promover diretamente para esta alternativa (não passar por (c)).

### (e) Buffer local intermediário em `.claude/local/BACKLOG.md` + promoção para forge

Captura rápida em buffer markdown local; promoção manual ou automática para issue do forge quando o item amadurece.

Descartada:

- **Complica contrato.** "Backlog mora em 2 lugares" exige decisão de leitura/escrita em cada skill consumidora — viola simplicidade do contrato `paths.<role>`.
- **Modo `local` já cobre captura sem forge.** Operador que quer buffer local pode usar `paths.backlog: local` em projeto diferente; misturar = redundância.
- **"Fricção de criar issue" pode ser feature.** Gate editorial mínimo (título + body) filtra capturas vagas — buffer markdown reintroduz o que se quis evitar.
- **Promoção buffer→forge seria mais uma engrenagem.** Manual = workflow do operador (não precisa de plugin); automática = decisão de critério (quando promover?) + side effects.

### (f) Cross-project/cross-group support na v1

Schema permite query custom multi-repo (ex.: `gh search issues --owner TJPA assignee:none state:open`).

Descartada para v1:

- **TJPA documentado opera per-repo.** Backlog é por repo no caso motivador.
- **Adiciona complexidade de configuração sem demanda concreta.**
- **Forward-compat via schema objeto se demanda emergir** (gatilho de revisão).

## Gatilhos de revisão

- **Latência reportada como dor.** Operador reporta `/next` lento ≥3 vezes OU latência típica em projeto TJPA passa consistentemente de 5s → promover para revalidação seletiva (alternativa (d), reservada como destino). Pular cache TTL curto (alternativa (c) descartada).
- **Demanda concreta por labels customizadas.** Operador pede recorte por label (ex.: `--label "ready"` em vez de "todas issues sem assignee") → promover schema string literal → schema objeto `{type: forge, filter: {label: ...}}`.
- **Race condition empírica.** Operador relata candidato proposto que já estava tomado (issue assignada entre fetch e escolha) ≥3 vezes → promover para revalidação seletiva ANTES da mutação (alternativa (d)) mesmo sem latência ser dor.
- **Cross-project/cross-group demanda emergir.** TJPA outras configurações (org-wide backlog) ou outro consumer com setup multi-repo → reabrir schema para suportar query custom.
- **"Sem PR/MR aberto" simplificação gera falsos positivos.** Operador relata issues sem assignee mas com MR aberto sendo propostas como candidatas → reabrir filtro para incluir cross-reference com PR list (paga query extra mas remove falso positivo).
- **`/curate-backlog` H2/H3 inúteis em modo forge.** ≥5 invocações em projetos forge com zero findings de H2/H3 → reabrir aplicabilidade das heurísticas no modo (talvez restringir a H1 + H4 em modo forge).
- **Cutucada por mutação irrita power-user.** Operador desativa via flag local ou expressa frustração ≥3 vezes → reabrir critério "cutucada por mutação" — talvez batched ou flag `--no-confirm` opt-in.
- **`gh`/`glab` API/CLI mudar.** Breaking change em CLI ou REST → reabrir `forge-auto-detect.md` operations.
- **Over-correção do recorte v1.** 6 meses pós-shipping, modo forge invocado ≤2× OR ≥50% das invocações com findings inúteis → reabrir decisão de codificação (paralelo a gatilho de over-correção de ADR-057).
- **Categoria "role com fonte remota" acumula instâncias.** Se ≥2 outros roles do path contract (`decisions_dir`, `version_files`, etc.) ganharem demanda concreta por fonte remota (notion para decisões, pypi para version, etc.), reabrir a contra-leitura cond 4 ("forge é fonte ontológica nova") rebatida em § Auto-aplicação. Pode justificar promoção de modo individual → categoria conceitual codificada com schema unificado de adapters, política de cache cross-role, mecânica de auth comum. **Único gatilho que reabre classificação ADR-034 cond 4 deste ADR.**

## Auto-aplicação coerente per ADR-034

- **Cond 5 (sucessor parcial):** **aplica primária** — sucessor parcial de ADR-049 § Decisão (a) (que codificou state em git/forge mas restringiu role `backlog` ao arquivo curatorial). Este ADR adiciona forge como **fonte do role** sem revogar ADR-049 substância (modo arquivo continua canonical default; estado in-flight continua em git/forge para mudança de código). Suficiente per ADR-034 *"novo ADR quando ≥1 das 5 condições aplica"*.
- **Cond 4 (categoria nova):** **NÃO aplica** — `paths.<role>: <modo>` é família já estabelecida por ADR-047 § Decisão (a) com 3 modos (canonical/local/null). Adicionar `forge` é **quarta variante** dentro da família, não categoria conceitual nova. Aplicar cond 4 aqui inflaria o critério (paralelo a ADR-047/-049 que não aplicaram cond 4 sob lógica idêntica). **Contra-leitura legítima rebatida:** existe leitura competidora "`forge` é mudança de **fonte ontológica** (API remota), não só de localização (path local) — categoria conceitual nova". Rebatida porque pattern `paths.<role>: <modo>` já comporta naturezas fundamentalmente variáveis: `null` opera com zero I/O (role desativado), `local` opera com filesystem gitignored, `canonical` opera com filesystem tracked. Variação de natureza já é parte do contrato da família; `forge` é quarto modo do mesmo eixo "onde declarar a fonte do role", não eixo conceitual novo. Pattern Ockham operacionalizado (ADR-043 § #4) prefere extensão dentro de família existente. **Alternativa registrada para maturação futura** via gatilho específico abaixo — se ≥2 outros roles ganharem demanda concreta por fonte remota (notion para decisions_dir, pypi para version_files, etc.), reabrir a classificação para considerar categoria conceitual codificada.
- **Cond 1 (decisão estrutural sem ancestral direto):** **NÃO aplica** — ADR-049 § Decisão (a) é ancestral direto codificado. ADR-047 § Decisão (a) é segunda fonte ancestral (família `paths.<role>`).
- **Cond 2 (substitui ADR ancestral):** **NÃO aplica** — operação é **extensão paralela**, não revogação. ADR-049 § Decisão (a) substância preservada (BACKLOG.md arquivo continua canonical default + state vivo em git/forge); este ADR ADICIONA opção paralela `paths.backlog: forge`. Leitor de ADR-049 continua obtendo regra vigente para modo arquivo identicamente; leitor de ADR-058 obtém regra vigente para modo forge. Pattern editorial paralelo a ADR-047 que estendeu role contract com modo `local` sem revogar modo canonical.
- **Cond 3 (codifica restrição externa):** **NÃO aplica** — decisão interna à arquitetura de path contract do plugin.

Cond 5 primária isolada justifica criação. Pattern editorial paralelo a ADRs anteriores que estenderam família `paths.<role>` (ADR-047 estabeleceu canonical/local/null; ADR-058 adiciona forge como quarto membro paralelo). F4 lesson das Ondas C-F reaplicada: cond 5 isolada, cond 4 NÃO inflada.
