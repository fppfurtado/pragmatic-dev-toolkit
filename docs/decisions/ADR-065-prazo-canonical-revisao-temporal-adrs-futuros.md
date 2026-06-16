# ADR-065: Prazo canonical de revisão temporal em ADRs futuros

**Data:** 2026-06-15
**Status:** Proposto

**Próxima revisão:** 2026-12-15
**Cadência:** semestral
**Critério de erosão auditável:** Mecânica de execução proativa do prazo temporal (quem dispara revisão periódica) **não** ter cristalizado em onda futura mesmo após ≥1 ADR vigente erodir empiricamente sem detecção pelo wiring reativo de ADR-053 § Decisão (b); OR auditoria post-mortem trimestral do Goodhart guard detectar ≥1 placeholder cosmético em ADR criado pós-shipping (mecanismo declarativo insuficiente, escalar para predicado mecânico via design-reviewer step 5).

## Origem

- **Decisão base:** [ADR-053](ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b) — wiring automático **reativo** do `design-reviewer` pré-fato (dispara em `/triage` plan-producing + `/new-adr`). Este ADR estende com cláusula doutrinal de prazo temporal **proativo** paralela, sem revogar a reativa.
- **Decisão base:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 5 (sucessor parcial — estende ADR Aceito vigente sem revogar). Forma do sucessor: novo ADR; ADR-053 vigente preservado intacto per invariante "Não alterar ADRs existentes" (CLAUDE.md + `skills/new-adr/SKILL.md`).
- **Decisão base:** [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado em decisões internas do plugin item 4 (codificação ≥3 instâncias). Este ADR aplica § Override do critério N=3 com sub-N3 explícito (1ª instância no toolkit) — onda análoga aos precedentes ADR-057/-061/-062/-063/-064.
- **Investigação:** 3ª/última follow-up deferida em [meta-system ADR-021](https://github.com/fppfurtado/meta-system/blob/main/docs/decisions/ADR-021-auto-critica-permanente-4o-principio-fundamental.md) § Limitações (4º princípio fundamental "Auto-crítica permanente"). Predecessoras shipped 2026-06-15: (1ª) `/doctrine-audit` skill local meta-reflexiva; (2ª) retrofit prazo nos 8 ADRs apex do meta-system via PR #15 squash `92c1892` — ADRs apex ganharam bloco metadata 3-linhas com substância per-ADR via cutucada inline + Goodhart guard real.
- **Plano:** `docs/plans/prazo-revisao-temporal-adrs-futuros.md`.

## Contexto

`design-reviewer` pré-fato (ADR-053 § Decisão (b)) opera **reativamente** — dispara quando `/triage` produz plano ou quando `/new-adr` é invocado. Cobertura é boa para decisões novas entrando no sistema, mas **invisível** para erosão temporal acumulada em ADRs Aceito vigentes: doutrina decidida 6 meses atrás pode ter sido superada por mudança contextual sem que nenhum gate atual capture o desalinhamento. O 4º princípio fundamental "Auto-crítica permanente" do meta-system pede mecanismo de revisão temporal proativa — ADR deve carregar por construção a condição que reabriria sua doutrina.

Meta-system materializou em 2 movimentos (1ª e 2ª follow-ups shipped 2026-06-15): skill local `/doctrine-audit` para auditoria meta-reflexiva sob demanda; retrofit dos 8 ADRs apex do meta-system com bloco metadata 3-campos (`**Próxima revisão:**` + `**Cadência:**` + `**Critério de erosão auditável:**`). A 3ª follow-up — esta — opera no **toolkit consumidor**: ADRs **futuros** criados via `/new-adr` em qualquer projeto que use o `pragmatic-dev-toolkit` já carregam o bloco metadata por construção, sem necessidade de retrofit reativo no próprio projeto.

A substância do mecanismo (3 campos canonical + cutucada per-novo-ADR para o Critério + Goodhart guard) é **importada** do meta-system como mecanismo cross-projeto, não emergente de pattern interno do plugin. Isso caracteriza onda de codificação proativa pré-N=3 — categoria editorial nova para o plugin, registrada explicitamente em § Override do critério N=3 abaixo.

## Decisão

**Cláusula doutrinal proativa paralela à reativa de ADR-053 § Decisão (b).** ADRs criados via `/new-adr` no toolkit ganham por construção bloco metadata canonical com 3 campos bold-paragraph:

```markdown
**Próxima revisão:** <currentDate + 6 meses>
**Cadência:** <trimestral|semestral|anual>
**Critério de erosão auditável:** <condição substantiva per-ADR; Goodhart guard explícito>
```

Localizado entre `**Status:** Proposto` e `## Origem` no template do `/new-adr`. Campos bold-paragraph (não headers) — preservam fluxo de leitura do ADR + greppáveis via `grep "^\*\*Próxima revisão:"`.

### Mecânica de preenchimento

- **`**Próxima revisão:**`** — default canonical `<currentDate + 6 meses>` auto-preenchido pela skill (paralelo ao uso pré-existente de `currentDate` em step 3 do `/new-adr`). Operador pode editar pós-criação. Safety-net editorial.
- **`**Cadência:**`** — default canonical `trimestral` auto-preenchido. Operador pode editar pós-criação. Safety-net editorial.
- **`**Critério de erosão auditável:**`** — preenchido via **cutucada per-novo-ADR** no `/new-adr` § Passos passo 4: `AskUserQuestion` prosa-livre perguntando "Que condição auditável reabriria este ADR?". Goodhart guard explícito no texto da cutucada + bullet em § O que NÃO fazer rejeitando placeholder cosmético tipo `"reavaliar em 6 meses"`/`"revisar quando relevante"`.

### Rebate da alternativa "cutucada para os 3 campos"

Alternativa não-escolhida: cutucada per-novo-ADR para os 3 campos (cutucada batched ou sequencial). Rebatida com critério:

- **Próxima revisão** depende exclusivamente de data — substância semântica per-ADR é nula (`currentDate + 6 meses` é safety-net automática reversível por revisão pós-fato).
- **Cadência** varia per substância (apex foundational pode ser anual; ADR tático trimestral), mas a variação típica é absorvida pelo default `trimestral` (conservador — agenda revisão mais cedo do que tarde). Reversível por revisão pós-fato.
- **Critério de erosão auditável** é o único campo cuja substância semântica per-ADR **não pode ser inferida** — qual condição concreta auditável reabriria este ADR específico depende do conteúdo da Decisão. Goodhart guard é load-bearing aqui (placeholder cosmético derrota o propósito do campo).

Aplicar cutucada nos 3 campos infla cerimônia (3 prompts em todo `/new-adr`) sem ganho semântico nos 2 primeiros — dilui o sinal load-bearing do Critério no ruído dos defaults.

### Mecânica de execução proativa

Reconhecidamente **especulativa neste ADR** — substância doutrinal é o gate temporal canonical em ADRs futuros (preenchido por construção via template). Quem dispara a revisão periódica (ex.: `/curate-backlog` estendido com varredura temporal, skill nova, cron) **não é decidido aqui** — cristaliza em onda futura quando sinal empírico de erosão acumulada justificar (≥1 ADR vigente claramente erodido sem detecção pelo wiring reativo atual). § Gatilhos de revisão abaixo nomeia o gatilho concreto.

Forma do gate reativo de ADR-053 § Decisão (b) **preservada intacta** — este ADR é cláusula proativa **paralela**, não substitutiva.

### Rebate da alternativa "wiring reativo consome `**Próxima revisão:**`"

Alternativa óbvia descartada pré-fato: `design-reviewer` free-read (per [ADR-048](ADR-048-free-read-design-reviewer-consolidado.md) § Decisão (c)) consumir `**Próxima revisão:**` em runtime, flagando ADRs vencidos como finding adicional do scan medium. **Não escolhida pré-fato** porque:

- (a) Wiring reativo de ADR-053 § Decisão (b) dispara em `/triage` plan-producing + `/new-adr` — janela de oportunidade narrow (apenas planos novos ou criação de ADR); erosão temporal opera **fora** desse gate (ADR Aceito vigente sem trigger natural de re-avaliação).
- (b) Free-read scan medium (ADR-048 § Decisão (c)) lê § Decisão até 8 linhas / cap 12 — bloco metadata fica no topo do ADR (entre `**Status:**` e `## Origem`), **antes** de § Decisão; precisaria estender scan target só para esse caso (custo editorial em ADR-048).
- (c) Sinal empírico de erosão real ainda não materializou (zero incidentes documentados no toolkit); decidir orquestrador agora é abstração prematura per ADR-043 § Ockham operacionalizado item 4.

Reabertura possível: gatilho #4 de § Gatilhos de revisão (drift cross-cláusulas reactive/proativa) é o teste forward concreto da alternativa rebatida.

## Consequências

### Benefícios

- **ADRs futuros carregam por construção o gate temporal** — sem retrofit reativo necessário no próprio projeto consumidor.
- **Goodhart guard explícito** elimina placeholder cosmético (`"reavaliar em 6 meses"`) que derrotaria o propósito do campo.
- **Defaults canonical** absorvem variação típica nos campos não-load-bearing (`Próxima revisão`, `Cadência`) sem inflar cerimônia.
- **Cross-projeto** — mecânica idêntica entre meta-system (ADRs apex retrofitted) e toolkit (ADRs futuros via construção), facilitando uso cruzado.
- **Greppabilidade** — `grep "^\*\*Próxima revisão:" docs/decisions/*.md` lista todos os ADRs do projeto com prazos; auditoria mecânica trivial.
- **Auto-aplicação** — este próprio ADR carrega o bloco metadata, alinhando dogfood (1ª aplicação imediata).

### Trade-offs

- **Cerimônia +1 cutucada `AskUserQuestion`** em todo `/new-adr` (Critério). Aceitável: substância semântica per-ADR é o ponto load-bearing — sem o gate, campo vira placeholder cosmético.
- **Defaults canonical podem mostrar-se off-mark** (6 meses muito longo/curto; trimestral demais/pouco). Mitigação: § Gatilhos de revisão nomeia gatilho de calibração concreto.
- **Mecânica de execução proativa especulativa** — substância doutrinal sem implementação de runtime. Reconhecido em § Decisão; § Gatilhos de revisão nomeia gatilho de cristalização concreto.

### Limitações

- **ADRs Aceito vigentes não retrofitados** — esta decisão é proativa por design (ADRs futuros via `/new-adr`). Retrofit em ADRs vigentes do toolkit é onda separada, não escopo deste ADR.
- **Goodhart guard depende de instrução prescritiva**, não de predicado mecânico verificável (paralelo a ADR-009 § "reviewer document-level" — análise semântica humano-suportada). Auditoria post-mortem trimestral é gatilho de detecção retroativa.
- **Paralelo direto a [ADR-009](ADR-009-revisor-design-pre-fato.md) § Limitações** — granularidade do Goodhart guard depende da capacidade do operador de articular condição auditável em runtime do `/new-adr`. Critério vago = falso negativo silencioso (equivalente proativo do "ADR vago" que ADR-009 reconhece). Gatilho de revisão #3 cobre só via amostragem; falsos negativos sistemáticos podem passar despercebidos até auditoria explícita.
- **Defaults editoriais herdados** podem reduzir esforço de avaliação per-ADR — operador pode aceitar `trimestral` automaticamente sem refletir se cabe ao ADR específico. Reversível por revisão pós-fato.
- **Auto-aplicação dogfood parcial.** ADR-065 carrega os 3 campos canonical (após `**Status:** Proposto` por construção honra de § Decisão § "Localizado entre `**Status:** Proposto` e `## Origem`") mas **não foi criado via a mecânica wiring que prescreve** — wiring `/new-adr` materializa em Bloco 2 do plano `docs/plans/prazo-revisao-temporal-adrs-futuros.md`; até `/reload-plugins` em sessão CC nova, Critério de erosão auditável aqui é articulado pelo agente coordenador, não pela cutucada `AskUserQuestion` que este ADR está propondo. Smoke pós-reload (registrado em `## Pendências de validação` do plano) valida que Goodhart guard real funciona em runtime. Honestidade epistêmica sobre lacuna do dogfood pré-`/reload-plugins`.

## Gatilhos de revisão

- **Cristalização da mecânica proativa de execução:** ≥1 ADR vigente do toolkit erodir empiricamente sem detecção pelo wiring reativo de ADR-053 § Decisão (b) — sinal que justifica codificar quem dispara revisão temporal (`/curate-backlog` estendido? skill nova? cron?). Reabrir § Decisão § "Mecânica de execução proativa" para cristalizar.
- **Calibração dos defaults canonical:** após N=3 ADRs criados com defaults, sample dos campos `**Próxima revisão:**` + `**Cadência:**`; se ≥1 mostrar-se off-mark (operador edita pós-criação ≥2 vezes), refinar defaults via novo `/triage`.
- **Auditoria post-mortem trimestral do Goodhart guard com critério tri-state mecânico:** classificar cada `**Critério de erosão auditável:**` em ADRs criados pós-shipping em **3 categorias**: (i) **substantivo per-ADR** (cita ADR/feature/restrição específica do conteúdo do ADR); (ii) **genérico mas auditável** (e.g. "inversão de doutrina X em § Decisão de outro ADR", "≥N incidentes em pattern Y registrado"); (iii) **cosmético** (paráfrase de "reavaliar quando relevante"/"revisar em 6 meses"/"verificar se faz sentido"). Pode ser executada via skill `/doctrine-audit` (do meta-system, paralela 1ª follow-up já shipped) OU via `@design-reviewer` step 5 quando ADR é editado. ≥1 classificado em (iii) → gatilho dispara: reabrir mecanismo (refinar prompt da cutucada, escalar para `@design-reviewer` validar Critério como finding pré-commit, ou adicionar 2ª pergunta de checagem). Critério tri-state transforma Goodhart guard de declarativo puro em semi-mecânico com classificação verificável.
- **Drift entre cláusula reativa (ADR-053 § Decisão (b)) e proativa (este ADR):** se ≥2 incidentes mostrarem que ADRs vigentes deveriam ter sido revistos mas o wiring reativo não disparou e o gate temporal proativo também não foi acionado, reabrir composição (talvez wiring reativo precise consumir `**Próxima revisão:**`).

## Auto-aplicação

**ADR-034 critério mecânico (adendo vs novo ADR — 5 condições para novo; 4 para adendo):**

- **Cond 5 (sucessor parcial — estende, refina ou condiciona ADR Aceito sem revogar):** **APLICA isoladamente**. Este ADR estende ADR-053 § Decisão (b) com cláusula proativa paralela, sem revogar a reativa. Regra central de ADR-053 preservada integralmente; nenhum marcado como `Substituído`. Forma do sucessor: novo ADR.
- **Cond 4 (codificação de pattern emergente — N≥3 incidentes recorrentes):** **NÃO APLICA**. Substância (3 campos canonical + cutucada + Goodhart guard) é **importada do meta-system** como mecanismo cross-projeto, não emergente de pattern interno do plugin (N=0 no toolkit pré-este ADR; 1ª instância é o próprio ADR-065). Categoria conceitual nova "prazo canonical de revisão temporal em ADR" é importada, não originada. § Override do critério N=3 abaixo cobre a tensão epistêmica. **Nota sobre expansão do argumento:** "importação cross-projeto ≠ categoria nova" foi herdado de ADR-052/ADR-053 § Auto-aplicação (consolidações editoriais sob redesign). Aplicação **estendida em ADR-065** para substância **operacional** importada (sem ancestral editorial direto). Reabrir se ≥2 incidentes futuros aplicarem mesmo argumento em substância operacional — pode sinalizar erosão do critério cond 4 (gatilho de revisão emergente).
- **Modos editoriais canonical de [ADR-052](ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md) (a/b/c):** **NÃO APLICAM**. ADR-065 não é onda de migração editorial sob ADR-045 § Decisão parte 1 § Implementação literal; é refinamento doutrinal proativo sucessor parcial de ADR-053 § Decisão (b). Modos editoriais cobrem composição de cluster temático (exclusão/inclusão/preservação por constraint) — categoria distinta. Examinado por simetria com o pattern de § Auto-aplicação de ADR-053 (que aplica ambos os critérios mecânicos por ser apex de migração).
- **Cond 1 (decisão estrutural sem ancestral codificado):** **NÃO APLICA**. ADR-053 § Decisão (b) é ancestral codificado direto; meta-system ADR-021 (importação) é ancestral cross-projeto.
- **Cond 2 (substitui ADR ancestral revogando doutrina central):** **NÃO APLICA**. Regra central de ADR-053 § Decisão (b) preservada intacta; nenhum ADR marcado como Substituído.
- **Cond 3 (codificação de restrição externa de longa duração):** **NÃO APLICA**. Decisão interna do plugin sobre wiring de revisão temporal.

## Override do critério N=3 (ADR-043 § Ockham operacionalizado item 4)

**Aplicação:** sub-N3 explícito. 1ª instância da categoria "prazo canonical de revisão temporal em ADR" no toolkit (N=0 pré-este ADR). Override consciente sob o critério editorial estabelecido — codificação proativa de mecanismo importado do meta-system.

**Calibração:**

- **Fragilidade epistêmica:** alta. Substância é importada, não emergente de incidentes empíricos do plugin. Mecânica de execução proativa permanece especulativa.
- **Mitigação:** mecânica de execução **não codificada neste ADR** — substância doutrinal é o gate temporal canonical (preenchido por construção); execução cristaliza em onda futura quando sinal empírico justificar (gatilho #1 de § Gatilhos de revisão).
- **Precedentes da onda Override:** ADR-057 (1ª, `/curate-backlog`), ADR-061 (2ª, `/session-audit`), ADR-062 (3ª, `prompt-reviewer`), ADR-063 (4ª, caminho-atômico), ADR-064 (5ª, gate-com-executor-validacao 2 sites). Este ADR-065 é a 6ª aplicação consecutiva — fragilidade epistêmica explicitamente reconhecida, distinta dos precedentes em que substância emergiu do próprio plugin.
- **Reabertura:** gatilho #1 de § Gatilhos de revisão (cristalização da mecânica proativa) é teste forward concreto. Se 6 meses pós-shipping nenhum ADR vigente erodir sem detecção pelo wiring reativo + Goodhart guard for honrado nos ADRs criados, override é validado empiricamente.
