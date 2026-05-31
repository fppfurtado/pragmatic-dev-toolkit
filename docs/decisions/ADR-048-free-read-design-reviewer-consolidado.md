# ADR-048: Free-read do design-reviewer consolidado (anotação + scan medium + always-include foundationals)

**Data:** 2026-05-31
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) (apex da redesign — § Decisão parte 1 § Implementação literal: *"Ondas C-X — migração de ADRs por cluster temático. Cada onda absorve 3-6 ADRs antigos em 1 consolidado..."*). Este ADR é a terceira instância concreta dessa migração (Onda E) consolidando o cluster reviewers/curadoria.
- **ADRs absorvidos:** ADR-021 (foundational do cluster — curadoria do free-read do design-reviewer via modo híbrido anotação + scan + threshold N=15 + philosophy.md integral — agora absorvido e arquivado nesta onda em `docs/decisions/archive/`) + ADR-044 (sucessor parcial — refina mecânica do scan para "scan medium" + adiciona categoria "always-include curado" com 3 ADRs hardcoded; cap nominal 5; rebatimento explícito de candidatos não-incluídos — agora absorvido e arquivado). Cluster index Addendum em ADR-021 (Onda 4 da reforma doutrinária, PR #87) reconheceu explicitamente ADR-044 como sucessor parcial — proof-of-concept de consolidação editorial agora preservado no archive como registro histórico que cumpriu sua função.
- **Decisões template:** [ADR-046](ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) (primeira instância de migração cluster — Onda C) + [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) (segunda instância — Onda D, primeira sem procedure file). Pattern validado: header redirect canonical, archive index incremental, propagação de cross-refs em docs vivos, link rot em 2 categorias, cond 5 primária isolada. F4 lesson Onda C reaplicada literal (cond 4 NÃO aplica; cond 1 NÃO aplica). F4 lesson Onda D — cond 2 refinada "absorção consolidatória vs revogação" — aplicada diretamente como pattern editorial.
- **Investigação:** Onda E codificada em `docs/plans/onda-e-migracao-cluster-reviewers-curadoria.md`. Cluster reviewers/curadoria escolhido como terceira migração por: (1) cluster Addendum já existente em ADR-021 (paralelo idêntico a ADR-005/-017 Addenda das ondas anteriores); (2) **calibração descendente** (2 ADRs vs 4 em Onda D vs 2 em Onda C) — sequência C→D→E exerce scope 2→4→2; (3) cluster sem procedure file (reaplica F9 lesson Onda D — fronteira ADR-024 não aplica antecipadamente); (4) **cluster coeso semanticamente máximo** (ambos os ADRs cobrem dimensões da mesma decisão estrutural — ADR-044 só estende ADR-021 sem revogar; ADR-021 Addendum explicitamente reconhece extensão).

## Contexto

A camada doutrinal pós-v2.14.0 inclui 2 ADRs codificando a curadoria do free-read do design-reviewer:

- **ADR-021 (foundational, 2026-05-12)** — estabeleceu mecanismo híbrido para mitigar custo O(#ADRs) do free-read estabelecido em ADR-009 § "Free-read de doctrine sources". Anotação opcional `**ADRs candidatos:**` no `## Contexto` do plano + scan por keyword nos ADRs não-anotados + philosophy.md sempre integral + threshold N=15 desligando o mecanismo abaixo do volume. Pattern conceitualmente paralelo a `**Termos ubíquos tocados:**` (operador anota o que sabe; reviewer scan cobre o que operador não sabe).
- **ADR-044 (sucessor parcial, 2026-05-29)** — Onda 4 (última) da reforma doutrinária. Refina mecânica do scan target de ADR-021 (~60 linhas/ADR de cabeçalho) para **scan medium** (subset doutrinariamente significativo: título + Status + Data + § Decisão até próximo `##` OU 8 linhas, cap 12). Adiciona categoria nova "always-include curado" com 3 ADRs hardcoded sempre lidos integralmente (ADR-009 base do design-reviewer; ADR-034 critério adendo vs novo; ADR-043 hierarquia doutrinal apex). Cap nominal 5; rebatimento explícito de não-incluídos com critério "escopo de aplicação". Threshold N=15 + anotação + philosophy.md integral preservados.

Sob a redesign da camada doutrinal codificada em ADR-045, o cluster reviewers/curadoria é candidato natural para consolidação:

- **Decisão central estável** — mecanismo híbrido (anotação + scan medium + always-include + threshold + philosophy.md integral) sem revisão pendente. Trade-offs absorvidos editorialmente nas Ondas 3+4 da reforma doutrinária.
- **Sucessor parcial reconhecido** — Cluster index Addendum em ADR-021 (Onda 4) demonstrou que leitura única do thread completo é mais ergonômica que navegação cross-ADR; precedente operacional pontual absorvido por esta consolidação. Pattern paralelo direto a ADR-005 (Onda 3 → Onda D) e ADR-017 (Onda 3 → Onda C).
- **Sem procedure file equivalente** — diferente de cutucadas (Onda C tinha `docs/procedures/cutucada-descoberta.md`), cluster reviewers/curadoria tem toda mecânica em `agents/design-reviewer.md` (sub-headers § Curadoria do free-read + 3 trilhos prescritivos + scan medium concreto + reporte invariante) + CLAUDE.md bullet. F9 lesson Onda D reaplicada — fronteira ADR-024 não aplica antecipadamente.
- **Calibração descendente** — Onda E (2 ADRs) é menor que Onda D (4 ADRs); valida pattern em scope pequeno após validar em médio. Sequência C→D→E exerce 2→4→2 ADRs — testa transferibilidade do pattern em scope variado.

Esta consolidação valida o pattern de migração em terceiro caso (calibração para ondas F-X que terão clusters de 3-8 ADRs variados).

## Decisão

**Consolidar a doutrina sobre free-read do design-reviewer em ADR único (este ADR-048), absorvendo substância de ADR-021 (foundational — modo híbrido + threshold + anotação + philosophy.md integral) + ADR-044 (sucessor parcial — scan medium + always-include curado + cap 5 + rebatimento + reporte invariante) sob narrativa única. Sem procedure file complementar — cluster sem split ADR/procedure per ausência de pré-existência (fronteira ADR-024 não aplica antecipadamente; F9 lesson de Onda D reaplicada).**

### Escopo e mecanismo unificado

**7 dimensões integradas em narrativa única:**

#### (a) Modo híbrido: anotação operador + scan reviewer + philosophy.md integral + always-include curado

Free-read do design-reviewer opera em modo híbrido com 4 trilhos:

1. **`philosophy.md`** — sempre lido integralmente (volume pequeno, doutrina-base cross-cutting). Trilho preservado de ADR-009 fundamental.
2. **Always-include curado** (per dimensão (d) abaixo) — 3 ADRs hardcoded sempre lidos integralmente paralelo a `philosophy.md`. Opera APENAS no modo curado (`#ADRs > 15`).
3. **Anotação operador** (`**ADRs candidatos:**`) — opcional no `## Contexto` do plano ou ADR draft. ADRs anotados entram integralmente. Formato: `**ADRs candidatos:** ADR-NNN (motivo curto), ADR-MMM (motivo curto)`. Operador que não sabe quais ADRs aplicam simplesmente omite; scan cobre.
4. **Scan reviewer** — para ADRs não-anotados, faz scan por keyword no scan target (per dimensão (c) abaixo). Match → ADR entra integral; sem match → descartado do contexto.

Pattern paralelo a `**Termos ubíquos tocados:**`: operador cura o que sabe; reviewer scan cobre o que operador não sabe. Convergência conceitual codificada (assimetria necessária porque ponto cego doutrinário de ADR-009 § Contexto — *"autor não sabe o que está contradizendo"* — impede anotação-only).

#### (b) Threshold N=15

`#ADRs total ≤ N` → mecanismo de scan **desliga**; reviewer faz free-read completo como ADR-009 original (modo legacy). Mecanismo só ativa quando volume justifica o trade-off.

**N=15.** Calibração heurística — abaixo de 15 ADRs, free-read completo é barato e curadoria semi-automática é overhead injustificado. Plugin meta-toolkit (≥15) ativa; consumer externo com inventário menor não paga complexidade. Ajustável via gatilho de revisão.

Modo legacy (`#ADRs ≤ 15`) preserva free-read integral sem distinção — quando tudo é lido, não há subset a curar. Always-include opera **apenas no modo curado**.

#### (c) Scan medium (mecânica do scan target)

Scan target prescritivo (substitui scan de cabeçalho ~60 linhas de ADR-021 original):

- Título (linha 1).
- Linhas com `**Status:**` e `**Data:**`.
- A partir da linha imediatamente após `## Decisão`, ler até o **primeiro** dos seguintes delimitadores:
  - Próximo header top-level (`## `).
  - 8 linhas lidas.
  - Cap absoluto **12 linhas/ADR**.
- Sub-headers `### ` dentro de `## Decisão` são **incluídos** no scan target.

Regra unidirecional (3 delimitadores em ordem) evita ambiguidade entre unidades distintas (parágrafos vs linhas).

**Critério de match:** case-insensitive substring; **≥2 keywords matches** no scan target confirma relevância (1 keyword único = match acidental). ADRs com match entram no input integral; ADRs sem match são descartados.

Custo estimado: ~3-5k tokens scan total (vs ~15k atuais do scan de cabeçalho de ADR-021). Redução ~70% sobre o scan target.

#### (d) Always-include curated list

3 ADRs hardcoded, sempre lidos integralmente paralelo a `philosophy.md`:

- **[ADR-009](ADR-009-revisor-design-pre-fato.md)** (Revisor design pré-fato e free-read de doctrine sources) — foundational do próprio design-reviewer; doutrina-base de qualquer review.
- **[ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md)** (Critério editorial — adendo em ADR existente vs novo ADR) — critério mecânico citado em quase todo sucessor parcial recente; auditável retroativamente nas Ondas 1-3 da reforma (citado em cada uma).
- **[ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md)** (Hierarquia doutrinal — fundamentais como raiz, pragmáticos como consequência operacional) — apex doutrinal do toolkit; raiz epistêmica que governa todas as decisões sob a hierarquia invertida.

**Pattern emergente confirmado empiricamente** nas Ondas 1+2+3 da reforma doutrinária — ADR-034 e ADR-043 citados em TODAS as 3 ondas (sinal forte de "doutrina-base sempre lida"). ADR-009 entra por categoria (qualquer review do design-reviewer pressupõe a doutrina que o instituiu).

**Cap nominal de 5 ADRs.** Expansão futura via gatilho de revisão (≥3 anotações sistemáticas de algum ADR em planos distintos pós-merge). Acima do cap, always-include vira overhead em vez de complemento ao scan.

#### (e) Reporte invariante

Format do reporte ao final da review:

```
Subset analisado: <N> ADRs lidos integralmente — <ADR-NNN>, <ADR-MMM>, ... (anotados: <K>, always-include: <A>, scan-matched: <L>). <M> filtrados pelo scan.
```

Modo legacy (`#ADRs ≤ 15`) → `Subset analisado: free-read integral (modo legacy; #ADRs ≤ 15)`.

Transparência permite ao operador detectar false negatives (ADR doutrinariamente relevante que ficou de fora) e calibra os gatilhos de revisão.

#### (f) Rebatimento de candidatos não-incluídos na always-include

Para evitar drift posterior, decisão registra explicitamente os candidatos óbvios NÃO-incluídos:

- **ADR-011** (Wiring automático do design-reviewer): cross-cutting mas opera só em `/triage`+`/new-adr` dispatch, não em toda review. Doutrina conhecida pelo agent via convenção operacional; promoção a always-include não passa custo-clareza.
- **ADR-026** (Critério mecânico de absorção de findings): pós-fato, do operador-pós-reviewer; não governa o que o reviewer flagra, governa como o operador processa.
- **ADR-007** (Idioma artefatos informativos): específico ao registro de mudanças (CHANGELOG, tag, PR); fora do escopo das reviews de plano/ADR.
- **ADR-046** (Cutucada uniforme em skills para descoberta de gaps de configuração): específico a SKILLs com `roles.required`; doutrina periférica para review de plano.
- **ADR-038** (Mirror de Decisões absorvidas runtime): pattern paralelo de "context-aware via messenger upstream" mas governa runtime de outros reviewers (code/qa/doc/security) durante /run-plan, não a curadoria do free-read pré-fato do design-reviewer. Eixos disjuntos; sem ganho de leitura sempre.

**Critério discriminante (carga empírica vs escopo de aplicação).** ADR-011 e ADR-026 têm carga empírica comparável a ADR-034/-043 — ambos citados em sucessores parciais recentes. O critério discriminante é **escopo de aplicação**: ADR-011 governa **quando** o reviewer dispara (`/triage` + `/new-adr` dispatch), não **o que** ele aplica em runtime na review; ADR-026 governa **pós-fato pelo operador** (absorção de findings), não a leitura de doutrina pelo reviewer. Always-include lista doutrina **aplicada em runtime durante a review** — escopo de ADR-009/-034/-043.

**Critério de promoção futura:** ≥3 anotações sistemáticas em planos distintos.

#### (g) Pontos cegos cobertos vs não-cobertos

| Ponto cego | Cobertura sob ADR-048 |
|---|---|
| Operador não sabe o que contradiz | ✓ scan dos não-anotados cobre |
| Scan false negative (ADR doutrinariamente relevante mas lexicalmente distante) | △ reduzido por (i) anotação manual; (ii) always-include garante ADR-009/-034/-043 sempre presentes mesmo lexicalmente distantes |
| Doutrina não-escrita escapa | ✗ herda limitação de ADR-009 — ortogonal a este ADR |
| Operador anota ADR irrelevante | ✓ reviewer lê integralmente mesmo sem match — custo é só de tokens, não de cobertura |
| Operador omite ADR óbvio | ✓ scan cobre se há match de keyword; △ always-include cobre apex; ✗ se ADR for lexicalmente distante e não-apex |

### Razões

- **Doutrina consolidada com clareza editorial.** Reader único navega thread completo (anotação + scan medium + always-include + threshold + reporte + rebatimento + pontos cegos) em ADR único; não precisa saltar ADR-021 → ADR-044 nem inferir relação por leitura cruzada do Addendum.
- **Sem procedure file — toda mecânica vive em docs vivos.** Cluster reviewers/curadoria não tem procedure pré-existente per ADR-024. Mecânica opera distribuída: `agents/design-reviewer.md` § Curadoria do free-read (3 trilhos prescritivos + scan medium concreto + always-include literal + reporte invariante) + CLAUDE.md bullet de cross-ref + templates/plan.md placeholder + `**ADRs candidatos:**` annotation pattern. Substância semântica vive aqui (ADR-048); doutrina aplicada runtime via agent.
- **Pattern de migração validado em cluster pequeno (calibração descendente).** Onda E demonstra que pattern de migração transfere para 2 ADRs (após validar em 2 ADRs com procedure em C e 4 ADRs sem procedure em D). Sequência C→D→E exerce scope variado; calibração para ondas F-X.
- **Trilha empírica preservada.** § Origem histórica deste ADR lista os 2 incidentes empíricos das decisões absorvidas; conteúdo original arquivado em `docs/decisions/archive/` para registro auditável.
- **Pattern auto-consistente da always-include.** ADR-048 codifica a curadoria mas não se inclui na lista — critério é apex doutrinal (Verdade/Excelência/Ockham), não estrutural-de-curadoria. ADR ancestrais (ADR-021/-044) idem se ainda vigentes. Preserva intenção de Ockham (cap 5).
- **F4 cond 2 lesson Onda D aplicada diretamente.** ADR-021 e ADR-044 têm decisões centrais **preservadas** como dimensões da decisão estrutural "free-read curado" codificada aqui — absorção consolidatória, não revogação. Pattern editorial para ondas F-X.

### Header redirect canonical + archive index — format herdado de ADR-046

Arquivos arquivados sob `docs/decisions/archive/` adotam **format de citação + header H1 original preservado** codificado em ADR-046 § Razões:

```markdown
> **ARCHIVED <YYYY-MM-DD>** — content absorbed into [ADR-MMM](../ADR-MMM-<slug>.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-NNN: <título original>

<body original integral...>
```

`docs/decisions/archive/README.md` (criado na Onda C, estendido em D) **estendido** com 2 linhas novas nesta onda (ADR-021, ADR-044 → ADR-048, Onda E). Pattern incremental por onda preservado per ADR-046 § Razões "Archive index incremental".

## Origem histórica

Incidentes empíricos das 2 decisões absorvidas preservados como contexto para reabertura informada:

### Auditoria 2026-05-12 (origem de ADR-021)

Auditoria arquitetural 2026-05-12 (`docs/audits/runs/2026-05-12-architecture-logic.md`, achado E1 + proposta B_arch) identificou que custo do free-read estabelecido em ADR-009 cresce O(#ADRs). Plugin tinha 20 ADRs no momento; ritmo recente (~19 ADRs em 6 dias) sugeriu atingir 30 em ~1-2 semanas. Reabertura **preventiva** evitou o cenário "reviewer caro mesmo em invocação média". ADR-021 estabeleceu mecanismo híbrido.

### Onda 4 da reforma doutrinária 2026-05-29 (origem de ADR-044)

Onda 4 (última) da reforma doutrinária codificada em umbrella commit `4882629`/`6473a55`. Plano em `docs/plans/onda-4-free-read-refinement.md`. Com 43 ADRs no momento, scan de cabeçalho de ADR-021 (~60 linhas/ADR) consumia ~15k tokens por invocação. Token cost projetado para 50-60 ADRs em meses (~22k+/invocação). Alavanca real de redução vs ~10% das Ondas 1-3 sozinhas. **Recursive moment intencional:** /new-adr disparando design-reviewer auto-fire per ADR-011 sobre ADR-044 draft aplicou mecanismo ATUAL de ADR-021 (não refinado) — token cost serviu como **baseline pré-refinamento** (~36k tokens) para validação empírica pós-merge. ADR-044 refinou scan target para "scan medium" (~3-5k tokens) + adicionou always-include curado (ADR-009/-034/-043) executando trigger antecipado em ADR-021 § Alt (e).

## Consequências

### Benefícios

- Reader navega thread completo da curadoria em 1 ADR (era 2 ADRs + Addendum sustentando o thread).
- Pattern de migração validado em scope variado (sequência C→D→E exerce 2→4→2 ADRs; com vs sem procedure file).
- Mecânica preservada distribuída em docs vivos onde executa (`agents/design-reviewer.md` + CLAUDE.md + templates + skills + procedure) — sem duplicação, sem stranding de substância em ADRs imutáveis.
- Trilha empírica preservada via archive + § Origem histórica.
- Token cost cresce sub-linearmente acima do threshold (mecanismo escala para 50, 100+ ADRs); always-include garante doutrina apex sempre presente sem depender de anotação manual.
- Pattern auto-consistente da always-include preserva Ockham (cap 5; lista enxuta; rebatimento explícito).
- Saldo inventário: 41 vigentes pós-Onda D + 1 novo ADR-048 - 2 arquivados = **40 vigentes pós-Onda E** (drop líquido de 1 — vs 3 em Onda D; cluster menor; calibração descendente).

### Trade-offs

- **Link rot em ADRs imutáveis tem 2 categorias distintas (F1 lesson Onda C reaplicada).**
  - **Categoria (a) — referências históricas/precedente** (vasta maioria — ADRs imutáveis citam ADR-021/-044 em § Origem ou cross-refs textuais). **Archive resolve** — `docs/decisions/archive/<slug>.md` carrega corpo histórico completo per format codificado. Archive index incremental facilita descoberta. Cross-refs em ADRs imutáveis ficam como registro histórico, NÃO são editados.
  - **Categoria (b) — referências de substância doutrinal ativa** (subset identificado pré-execução para verificação no design-reviewer): ADR-044 (próprio sucessor sendo absorvido) cita ADR-021 § Alt (e) como ancestral conceitual — substância delegada para ADR-048 § Decisão (d) onde always-include é codificada; ADR-046 cita ADR-021/-017 Addenda como precedentes para archive pattern — substância delegada para ADR-046 § Razões. **Hipótese: zero substância "doutrinal ativa" perdida** — pre-existente Addendum de ADR-021 (Onda 4) explicitamente reconheceu ADR-044 como sucessor parcial estendendo sem revogar; consolidação preserva isso. design-reviewer valida hipótese.
  - Edição de ADRs imutáveis citantes evitada por preservar ADR-classical convention; substância absorvida em ADR-048 (§ Decisão + § Origem histórica) é a mitigação real.
- **Custo do refactor de cross-refs menor que Onda D** — 6 docs vivos atualizados (vs 9 em D, 5 em C); ~11 ocorrências em ~11 linhas distintas (vs ~58/34 em D, ~12/7 em C). Pattern de propagation testado em scope variado. Bloco 2 (design-reviewer.md sozinho com 6 ocorrências + reformulação narrativa) concentra risco editorial; doc-reviewer audita. Threshold "≥10 findings" no Bloco 2 preservado como conservador.
- **Pattern auto-consistente da always-include constrange expansão** — ADR-048 não pode entrar na própria always-include mesmo se gatilho ≥3 anotações disparar. Constraint mecânico que preserva Ockham mas pode requerer revisão se ADR consolidado se tornar referência sistemática em planos distintos pós-Onda Z. Gatilho de revisão registrado.
- **Implementação history das 2 decisões absorvidas permanece em `archive/ADR-021-*.md` + `archive/ADR-044-*.md`** — NÃO duplicada em ADR-048 (paralelo aos precedentes Onda C e Onda D; padrão editorial codificado em ADR-047 § Trade-offs). Reader que precisa de hash → 1 hop via redirect canonical do archive.
- **CHANGELOG.md preservado intacto** — registro histórico imutável paralelo a ADRs imutáveis. Múltiplas linhas referenciando ADR-021/-044 nas versões v2.x.x preservadas como registro de versionamento; NÃO editadas. Link rot histórico aceito.

### Limitações

- **Herda limitação de ADR-009 sobre doutrina não-escrita** — curadoria não conserta o caso onde decisão estrutural existe sem ser registrada em `docs/decisions/`. Mecânica ortogonal.
- **Herda calibração editorial de scan medium e always-include** — heurística de scan target prescritiva mas não imutável; lista always-include editorial com cap 5. Inclusão/remoção exige decisão operadora consciente.
- **Threshold N=15 sem observabilidade direta** — herda limitação de ADR-021 § Trade-offs (depende de operador reportar findings perdidos por scan ou tokens excessivos por free-read prematuramente desativado). Aceito; gatilho de revisão registrado.
- **Valley of meh para inventário 16-29 ADRs** — herdada de ADR-044 § Limitações. Always-include adiciona ~5-10k tokens fixos sempre lidos, mas scan medium dos 13-26 não-anotados custa só ~1.5-3k. **Saldo líquido pior que modo legacy desligado** nessa janela. Ganho real materializa-se ≥30 ADRs.
- **Pattern auto-consistente constrange catch-up retroativo** — se ADR-048 vier a ser citado sistematicamente em ≥3 planos distintos pós-merge (gatilho de promoção), constraint mecânico de "ADR de curadoria não entra na curadoria" requer revisão deliberada.

### Mitigações

- **Anti-regression checklist do charter** § Reviewers lista os ~8 elementos load-bearing (5 reviewers shippados, design-reviewer auto-fire em /triage e /new-adr, critério de absorção de findings, free-read curado completo, read defensivo, reviewer report idioma, mirror de Decisões absorvidas runtime) — design-reviewer audita preservação em ADR-048 § Decisão. Plano § Verificação end-to-end critério 10 prescreve audit explícito.
- **Plano § Verificação end-to-end critérios 4-7** prescrevem grep explícito de ADR-021/-044 em paths concretos como invariante de sucesso da onda; `doc-reviewer` audita o diff conforme insumo curado pelo plano per ADR-009 padrão diff-level. Pattern reaplicado das Ondas C+D: critério de cross-ref propagation vive no plano, não na mecânica de reviewer.
- **Archive index estendido nesta Onda E** (2 linhas novas em `docs/decisions/archive/README.md`) — link rot mitigation **ativa** desde já para o cluster reviewers/curadoria. Reader que cai em archive/ADR-021-*.md ou archive/ADR-044-*.md vê redirect proeminente para ADR-048 + corpo histórico abaixo.
- **F4 lesson de Onda C reaplicada literal** (cond 5 primária isolada; cond 4 NÃO aplica; cond 1 NÃO aplica). F4 cond 2 refinada de Onda D aplicada diretamente ("absorção consolidatória" preservada). Evita inflação de critérios em cada onda F-X.

## Alternativas consideradas

### (a) Manter ADR-021 + ADR-044 com cluster Addendum (status quo Onda 4)

Continuar com estrutura atual: ADR-021 foundational + ADR-044 sucessor parcial + cluster Addendum em ADR-021 (criado na Onda 4 da reforma doutrinária).

Descartada per ADR-045 § Decisão parte 1: cluster Addenda foram **prova de conceito** de consolidação editorial; a redesign generaliza esse movimento para **archive + consolidado único**. Manter status quo perde benefício de leitura única do thread + mantém 2 ADRs onde 1 cabe sob a nova estrutura.

### (b) Edit in-place em ADR-021 absorvendo ADR-044

Reescrever ADR-021 incorporando substância de ADR-044, mantendo ADR-021 como ADR vigente; ADR-044 marcado `Substituído`.

Descartada:

- Viola convenção ADR-classical (ADRs são registros imutáveis; supersedeção via novo ADR).
- Apaga trajetória editorial (ADR-044 documentou Onda 4 com recursive moment do reviewer baseline ~36k tokens — reescrever ADR-021 apaga essa narrativa).
- ADR-045 explicitamente prescreve archive + novo ADR consolidado.
- ADR-046 (Onda C) + ADR-047 (Onda D) já estabeleceram pattern de archive + novo consolidado; mudar pattern em Onda E fere consistência da redesign.

### (c) Criar `docs/procedures/free-read-curado.md` absorvendo a mecânica

Mover mecânica das 2 decisões para procedure file novo; ADR-048 carrega apenas substância doutrinária; procedure carrega scan target prescritivo + critério match + always-include literal + reporte invariante.

Descartada:

- Cria procedure file **sem necessidade pré-existente** — pattern de Ondas C+D explicita que procedure file separation per ADR-024 aplica quando procedure **pré-existe** (cutucadas tinha; modo local não; reviewers/curadoria não). Criar antecipadamente reabre tensão que ADR-024 resolveu.
- Mecânica do free-read curado já está distribuída em `agents/design-reviewer.md` § Curadoria do free-read (onde executa) + CLAUDE.md + templates + skills. Mover para procedure cria 5ª localização sem ganho de coesão.
- Procedure file tem categoria conceitual de **algoritmo prescritivo executor universal cross-skills** (per ADR-024 — ex.: `cutucada-descoberta.md` executado por 5 skills; `forge-auto-detect.md` por múltiplas). Mecânica do free-read é **interna ao agente design-reviewer** — fit pobre com categoria procedure.

### (d) Always-include expandida para incluir ADR-046+ADR-047+ADR-048 (próprios consolidados da redesign)

Adicionar os 3 ADRs consolidados desta redesign à always-include (junto a ADR-009/-034/-043).

Descartada:

- **Pattern auto-consistente violado** — ADR-048 não pode se autorreferenciar como always-include. Constraint mecânico que preserva Ockham.
- **ADR-046/-047 não são apex doutrinal** — são instâncias de migração cluster, não decisões estruturais cross-cutting que governam runtime do reviewer. Critério "escopo de aplicação" (per dimensão (f)) discrimina: doutrina aplicada em runtime durante a review vs templates de migração.
- **Cap nominal 5 ainda permite expansão futura** via gatilho ≥3 anotações sistemáticas. Caso ADR-046/-047/-048 venham a ser citados sistematicamente, gatilho mecânico promove.

### (e) Splits diferentes — separar ADR-021 (mecanismo híbrido) de ADR-044 (scan medium + always-include)

Criar 2 ADRs novos: ADR-048a "Modo híbrido foundational" + ADR-048b "Refinamento scan medium + always-include".

Descartada:

- Splits artificiais — os 2 ADRs cobrem dimensões da **mesma decisão estrutural** (curadoria do free-read). Cluster index Addendum em ADR-021 (Onda 4) já demonstrou que leitura única do thread é mais ergonômica.
- 2 ADRs onde 1 cabe — viola Ockham.
- Charter sketch original previa **1 ADR consolidado** para cluster reviewers/curadoria. Esta onda materializa fielmente.
- Pattern Onda C (1 consolidado por cluster) + Onda D (1 consolidado por cluster) — mudar em Onda E fere consistência.

### (f) ADR-048 como índice apontando para os 2 ADRs originais (sem archive)

ADR-048 minimalista apontando para os 2 ADRs originais; nada movido para archive.

Descartada (paralelo a Alternativa (e) de ADR-046 e (e) de ADR-047):

- Não materializa a redesign — ADR-045 prescreve absorção de conteúdo + archive de antigos, não indexação cosmética.
- Pattern Onda C+D já estabeleceu absorção + archive; mudar em Onda E fere consistência da redesign.

## Gatilhos de revisão

Triggers das 2 decisões absorvidas consolidados + triggers específicos da consolidação:

### Herdados de ADR-021 (curadoria foundational)

- **Scan reporta zero matches** em invocação onde operador percebe que ADR não-anotado deveria ter aparecido — false negative concreto. Refinar heurística de keyword.
- **Operador anota sistematicamente os mesmos ADRs em planos diferentes** — sinal de que esses ADRs viraram doutrina-base; promover para inclusão automática sempre-lida (paralelo a `philosophy.md` integral). **Cap nominal 5 ADRs na always-include** limita expansão; ≥3 anotações sistemáticas em planos distintos triggera promoção.
- **Threshold N=15 mal-calibrado** (mecanismo ativa cedo demais ou tarde demais) — ajustar com base em observação.
- **Reviewer reporta inconsistência entre subset lido e ADR não-lido** (auto-validação rara) — confirma necessidade de safety net.
- **Próximo refactor sweep grande** — observar como o mecanismo se comporta sob carga de adições rápidas; cada novo ADR muda o universo de scan.
- **Consumer externo reporta confusão sobre `**ADRs candidatos:**`** — campo mal documentado ou redundante para projetos pequenos. Refinar critério de quando `/triage` sugere o campo.
- **Volume de `docs/philosophy.md` dobra** — revisitar a exceção que mantém philosophy.md em free-read sempre.

### Herdados de ADR-044 (scan medium + always-include)

- **Always-include list precisa crescer** — ≥3 anotações sistemáticas de algum ADR (ex.: ADR-011, ADR-026) em planos distintos pós-merge, sinalizando promoção a always-include. Cap nominal 5 limita expansão.
- **Scan medium subdimensionado** — false negatives recorrentes em invocações reais (operador percebe ADR doutrinariamente relevante não-aparecido no "Subset analisado"). Ampliar para ~15 linhas/ADR (incluindo § Consequências 1ª frase?) ou recalibrar heurística.
- **Token cost real não cair conforme estimado** (~50-70%) — observação pós-merge via invocações do design-reviewer em ondas/planos subsequentes. Recalibrar scan target ou expandir always-include conforme dado empírico.
- **Cap nominal 5 mal-calibrado** — operador precisa expandir always-include para 6-7 e o cap estorva. Recalibrar.

### Específicos desta consolidação (Onda E)

- **Pattern auto-consistente da always-include estorva** — se ADR-048 vier a ser citado sistematicamente em ≥3 planos distintos pós-merge (gatilho de promoção), constraint mecânico de "ADR de curadoria não entra na curadoria" requer revisão deliberada. Critério "doutrinariamente apex" pode requerer ajuste.
- **Pattern de migração falhar em outra onda F-X** com cluster pequeno (2-3 ADRs) — design-reviewer flagrar gap material no pattern (substância não absorvível limpamente em cluster pequeno; reformulação narrativa do agent gerar inconsistência). Reabrir ADR-046+ADR-047+ADR-048 como template combinado; pode requerer revisão de ADR-045 § Decisão parte 1.
- **Volume de cross-refs (~11 em 6 docs vivos) gerar ≥10 findings de doc-reviewer no Bloco 2 (design-reviewer.md)** — pattern de reformulação narrativa precisa refinamento antes de aplicar a clusters com mais reformulação. Pausar redesign e revisitar charter per § Sinal de saúde.
- **Reformulação narrativa do `agents/design-reviewer.md` introduz inconsistência** entre subseções do agent (§ Curadoria do free-read 3 trilhos + scan medium + always-include + reporte) e ADR-048 § Decisão (a-g) — drift entre autor do mecanismo (ADR-048) e executor do mecanismo (agent). Reabrir para revisar reformulação.

## Auto-aplicação coerente per ADR-034

- **Cond 5 (sucessor parcial):** aplica primária — consolidado absorve substância de ADR-021 (foundational) + ADR-044 (sucessor parcial estendendo cobertura) sob narrativa única. Os 2 ADRs vão para archive com header redirect canonical a este ADR. **Suficiente per ADR-034** *"novo ADR quando ≥1 das 5 condições aplica"*; cond 5 isolada justifica criação deste ADR.
- **Cond 4 (categoria nova):** **NÃO aplica** — ADR-045 § Decisão parte 1 § Implementação **já codificou a categoria** "consolidação editorial cross-ADR de cluster temático como decisão estrutural" no nível meta-pattern; ADR-046 estabeleceu primeira instância concreta (Onda C); ADR-047 segunda instância (Onda D); ADR-048 é **terceira instância concreta** da categoria já estabelecida, não introduz categoria conceitual nova. **F4 lesson de Onda C reaplicada literal** — aplicar cond 4 aqui inflaria o critério em cada onda F-X ("N-ésima instância como categoria nova" auto-justificativa), diluindo a precisão de ADR-034.
- **Cond 1 (decisão estrutural sem ancestral direto):** **NÃO aplica** — ADR-045 § Decisão parte 1 § Implementação **é ancestral codificado direto** do pattern que ADR-048 instancia. ADR-046 + ADR-047 são segundas/terceiras fontes ancestrais codificadas (templates diretos da migração). Onda 4 cluster index Addendum em ADR-021 é precedente operacional pontual, mas ADR-045 elevou o pattern a decisão estrutural codificada — ADR-048 herda essa ancestralidade.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — operação é **absorção consolidatória** (substância das 2 decisões codificada integralmente em ADR-048 § Decisão sob narrativa única; archive preserva trajetória), **não revogação** (paralelo a ADR-043 → ADR-035, onde apex doutrinal foi invertido). Diferença pragmática: leitor de ADR-048 obtém regra vigente identicamente equivalente à composição dos 2 absorvidos; leitor de archive/ADR-021-*.md ou archive/ADR-044-*.md vê redirect canonical apontando para autoridade vigente sem ambiguidade. **F4 cond 2 lesson de Onda D aplicada diretamente** — pattern editorial para ondas F-X (cond 2 reservada para inversões/revogações; absorções consolidatórias seguem cond 5 isolada).
- **Cond 3 (codifica restrição externa):** NÃO aplica — decisão interna ao processo doutrinal do plugin.

Pattern editorial para ondas F-X: cada migração cluster aplica **cond 5 primária + outras condições conforme ancestralidade real**, não cond 4 inflada nem cond 1 espúria. ADR-045 § Decisão parte 1 + ADR-046 + ADR-047 são ancestrais codificados de cada migração; ondas instanciam, não criam categoria. **F4 lessons codificadas como pattern para F-X.**
