# ADR-052: Codificação dos 3 modos editoriais de refinamento da consolidação

**Data:** 2026-05-31
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão linha 56 — fronteira "ajuste editorial do charter vs revisão de ADR-045" lista "absorção em consolidado diferente do sketch original" como ajuste editorial livre. ADR-052 é sucessor parcial primário per cond 5 de ADR-034 **promovendo** 3 categorias editoriais emergentes — operadas implicitamente nas Ondas F+G+H sob a fronteira de ADR-045 como ajustes editoriais individuais — **para meta-pattern canonical com critério mecânico verificável e exemplos canonical**. Decisão central de ADR-045 preservada (consolidação 45 → ~13-15 ADRs sob hierarquia invertida + filtro de admissão); ADR-052 refina o escopo do terceiro item da fronteira ("absorção em consolidado diferente do sketch") promovendo-o de "categoria não-codificada" para "categoria com sub-modos canonical".
- **Critério editorial:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 5 (sucessor parcial primário estendendo ADR Aceito sem revogar); cond 4 **NÃO aplica** (refinamento editorial dentro de categoria existente "consolidação da redesign", não categoria conceitual nova de artefato); cond 1 **NÃO aplica** (ADR-045 ancestral codificado direto); cond 2 **NÃO aplica** — regra central de ADR-045 (consolidação 45 → ~13-15 ADRs sob hierarquia invertida + filtro de admissão) preservada integralmente; cond 3 **NÃO aplica** (sem restrição externa).
- **Gatilho disparado pós-Onda H:** [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) critério 4 ("codificação de pattern emergente ≥3x") atingido. 3 instâncias empíricas das Ondas F+G+H da redesign convergiram em pattern editorial reconhecível. Charter `docs/plans/redesign-camada-doutrinal-charter.md` § "Refinamento editorial documentado" registrou sinal a observar pré-Onda H; sinal materializado pós-Onda H com gatilho de revisão de ADR-045 explicitamente disparado.
- **Decisão de operador registrada:** Opção B (ADR sucessor codificando 3 modos editoriais antes da Onda I) escolhida sobre Opção A (status quo continuar absorvendo via fronteira atual de ADR-045) e Opção C (aguardar 4ª instância). Justificativa: ADR-035 critério 4 já atingido em rigor + escala mecanismo sem reabrir doutrina por cada onda futura.
- **Pattern paralelo:** ADR-020 (warnings pré-loop) + ADR-022 (archival docs/plans) + ADR-023 (disable-model-invocation) reusaram "critério mecânico cumulativo" estabelecido por ADR-013 (CI lint mínimo) via ADRs sucessores. ADR-052 segue precedente editorial — pattern emergente em ADRs ancestrais codificado formalmente via ADR sucessor quando ≥3 reusos justificam.
- **Templates empíricos:** ADR-049 (Onda F — 1ª instância exclusão) + ADR-050 (Onda G — 2ª instância inclusão) + ADR-051 (Onda H — 3ª instância preservação por constraint) carregam exemplos canonical de cada modo em § Origem respectiva.
- **Hierarquia doutrinal:** [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) endossa codificação por triangulação dos 3 fundamentais aplicados a este meta-pattern: **Verdade** nomeia o pattern observável (3 instâncias empíricas distintas); **Excelência** sem over-engineering — codificação preventiva evita reabertura caso-a-caso em ondas futuras; **Ockham** — 1 ADR codifica 3 modos compartilhando mesmo escopo aplicacional vs 3 ADRs separados.

## Contexto

ADR-045 (apex da redesign da camada doutrinal) § Decisão parte 1 estabelece sketch da estrutura-alvo (~13-15 ADRs consolidados) como **artefato para criticar, não decisão imutável** — sequence de cluster absorption refinada por ondas anteriores. Decisão imutável é a regra de consolidação (hierarquia invertida + filtro de admissão); forma exata é descobrível durante execução.

§ Decisão linha 56 codifica fronteira:

> Ajuste de cluster sequence (ordem de migração), subdivisão de consolidado em 2, **absorção de ADR em consolidado diferente do sketch original** → ajuste editorial livre do charter durante execução. Mudança estrutural na regra de consolidação → revisão de ADR-045 via § Gatilhos.

Pós-Ondas F+G+H, 3 instâncias empíricas de "absorção em consolidado diferente do sketch" emergiram com características distintas:

| Onda | Modo emergente | Cluster | ADR(s) tocado(s) | Justificativa |
|---|---|---|---|---|
| **F** | EXCLUSÃO | execução/run-plan | ADR-037 + ADR-010 (excluídos do cluster) | ADR-037 pertence semanticamente a discoverability/branding; ADR-010 categoria distinta progress display com potencial consumers futuros além de `/run-plan` |
| **G** | INCLUSÃO | componentes plugin | ADR-015 (incluído ao cluster apesar de omitido no sketch) | Sketch omitiu por descuido editorial; ADR-015 pertence à família PreToolUse block hooks (ADR-040 § Origem cita ADR-015 como "ancestral direto"); excluir deixaria órfão membro coeso |
| **H** | PRESERVAÇÃO POR CONSTRAINT | convenções editoriais | ADR-034 (preservado vigente fora do cluster) | ADR-034 hardcoded na always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]` + categoria semântica distinta (meta-doutrina apex vs convenções editoriais estruturais) |

Sem codificação formal, cada onda futura aplica refinamento ad hoc, reabrindo justificativa do zero. Reader independente não consegue prever qual modo se aplica sem ler § Origem do ADR consolidado da onda + charter § Atualização pós-execução.

ADR-035 critério 4 ("≥3 pattern emergente") atingido em rigor — pattern editorial reconhecível com 3 instâncias distintas justificando codificação. ADR-052 codifica preventivamente antes da Onda I (alinhamento/triage com constraint análogo always-include sobre ADR-009) para que Onda I aplique modo (c) preservação por constraint **com referência formal estabelecida** em vez de descobrir o pattern reativamente.

## Decisão

ADR-052 codifica **3 modos editoriais de refinamento da composição do cluster vs sketch original** que cabem dentro da fronteira de ADR-045 § Decisão linha 56 ("absorção em consolidado diferente do sketch original"). Decisão central de ADR-045 preservada; ADR-052 explicita o escopo da fronteira existente, não revisão estrutural.

### (a) EXCLUSÃO de ADRs semanticamente desalinhados do sketch

**Caso de uso:** cluster sketch agrupou por proximidade numérica ou heurística similar em vez de coesão semântica; ADR semanticamente pertence a categoria diferente (cluster atual ou futuro).

**Critério mecânico:**

- ADR listado no sketch pertence semanticamente a categoria diferente da do cluster sendo migrado, verificável por leitor independente do sketch (ex.: ADR sobre README framing listado em cluster execução/run-plan claramente pertence a discoverability/branding).
- OU: ADR é ancestral codificado direto de outro absorvido mas representa categoria conceitual distinta com potencial consumers futuros independentes (ex.: ADR-010 progress display vs ADR-039 state-keeping — categorias paralelas de Task tool com escopos não-sobrepostos).

**Exemplo canonical** (Onda F):
- ADR-037 (README framing Product Engineer) excluído do cluster execução/run-plan por pertencer a discoverability/branding. Sketch agrupou por proximidade numérica.
- ADR-010 (progress display Task tool) NÃO absorvido apesar de ser decisão base de ADR-039 (state-keeping). Categoria distinta com potencial consumers futuros além de `/run-plan`. Charter sketch tinha contradição interna (ADR-039 listado em 2 clusters); resolução favorece preservar categoria distinta.

**Aplicação operacional:** ADR(s) excluído(s) ficam vigentes como ADRs clássicos standalone OU são realocados para futuro cluster apropriado (decisão editorial caso-a-caso). Cluster da onda atual absorve subset reduzido vs sketch.

### (b) INCLUSÃO de ADRs omitidos do sketch quando coesão semântica de família justifica

**Caso de uso:** sketch omitiu ADR aparentemente por descuido editorial; ADR pertence a família semântica já presente no cluster e excluir deixaria órfão membro coeso.

**Critério mecânico:**

- ADR omitido do sketch pertence a família semântica já presente no cluster, verificável por cross-ref doutrinal entre ADR omitido e ADRs incluídos no sketch.
- E: omissão é descuido editorial (não decisão deliberada), verificável por ausência de justificativa explícita no sketch ou em ADR-045 § Decisão para a omissão.

**Exemplo canonical** (Onda G):
- ADR-015 (hook block_env por sufixo `.env`) **incluído** ao cluster componentes plugin apesar de omitido no sketch (5 ADRs originalmente listados: 008+013+016+023+040; ADR-015 omisso).
- Pertence à família PreToolUse block hooks: ADR-040 § Origem cita ADR-015 como "ancestral direto — primeiro PreToolUse block hook do plugin, estabelece pattern de gate por filename match com escape hatch documentado".
- Excluir deixaria órfão um membro da família coesa de 3 hooks defensivos (block_env + block_gitignored + block_settings_drift).

**Aplicação operacional:** ADR incluído é absorvido no consolidado da onda como qualquer outro membro do cluster. Cluster da onda atual absorve subset expandido vs sketch.

### (c) PRESERVAÇÃO de ADRs ancestrais fora do cluster por constraint mecânico

**Caso de uso:** ADR está hardcoded em decisão Aceito de outro ADR (e.g., always-include curated list, schema enforcement, gate concreto). Absorvê-lo exigiria editar ADR-classical (antipattern: ADRs Aceito imutáveis) + quebraria caminho mecânico de leitura por sistemas que consultam o hardcode.

**Critério mecânico:**

- ADR está hardcoded em decisão Aceito de outro ADR, verificável por grep do ID do ADR em § Decisão de ADRs Aceito vigentes (não em § Origem, § Trade-offs, ou § Alternativas — apenas em § Decisão onde a regra central vive).

**Exemplo canonical** (Onda H):
- ADR-034 (critério adendo vs novo ADR) **preservado vigente** fora do cluster convenções editoriais apesar de pertencer ao sketch original (4 ADRs listados: 007+012+024+034).
- Constraint mecânico: ADR-034 está hardcoded na always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]`.
- Categoria semântica distinta (meta-doutrina apex vs convenções editoriais estruturais) **reforça** a decisão de preservação mas NÃO é critério independente — categoria semântica distinta sem constraint mecânico cai em modo (a) EXCLUSÃO bullet 2 (ancestralidade codificada com categoria distinta), não em modo (c).
- ADR-034 fica vigente como ADR clássico standalone; substância NÃO absorvida no consolidado da onda.

**Aplicação operacional:** ADR preservado fica vigente como ADR clássico standalone; substância NÃO é absorvida em § Decisão do consolidado da onda; cluster absorve subset reduzido vs sketch. ADR preservado mantém-se como referência de autoridade vigente para sub-decisões dependentes; redirect canonical de archive não aplica (ADR não foi archived).

**Fronteira com modo (a) EXCLUSÃO bullet 2:** modo (a) cobre ADRs preservados fora do cluster por **ancestralidade codificada com categoria distinta** quando NÃO há constraint mecânico (caso canonical: ADR-010 Onda F — categoria distinta progress display vs state-keeping, sem hardcode). Modo (c) é restrito ao caso com hardcode em § Decisão de ADR Aceito (caso canonical: ADR-034 Onda H). Operacionalmente os 2 caminhos produzem o mesmo outcome (ADR fica fora do consolidado, vigente standalone), mas o critério mecânico discrimina genuinamente: grep do ID em § Decisão = modo (c); sem grep + categoria distinta = modo (a) bullet 2.

### Aplicação à fronteira ADR-045 § Decisão linha 56

ADR-045 § Decisão linha 56 lista 3 categorias de ajuste editorial livre:

1. Ajuste de cluster sequence (ordem de migração);
2. Subdivisão de consolidado em 2 (ex.: alinhamento + reviewer dispatch);
3. **Absorção de ADR em consolidado diferente do sketch original**.

ADR-052 refina **o terceiro item** explicitando que as 3 modalidades (a)+(b)+(c) cabem dentro dele:

- **(a) Exclusão** = "absorção em consolidado diferente do sketch" via remoção do cluster atual (ADR fica fora; absorção zero).
- **(b) Inclusão** = "absorção em consolidado diferente do sketch" via adição ao cluster atual apesar de omitido (ADR absorvido contra omissão do sketch).
- **(c) Preservação por constraint mecânico** = "absorção em consolidado diferente do sketch" via não-absorção quando ADR está hardcoded em § Decisão de outro ADR Aceito (ADR não absorvido apesar de listado no sketch; fica vigente standalone). Caso de preservação por categoria distinta SEM constraint mecânico cai em modo (a) EXCLUSÃO bullet 2.

**Decisão central de ADR-045 preservada:** consolidação 45 → ~13-15 ADRs sob hierarquia invertida + filtro de admissão going forward continua intacta. ADR-052 **promove** o terceiro item da fronteira § Decisão linha 56 de "categoria não-codificada de ajuste editorial livre" para "categoria com sub-modos canonical (a/b/c) com critério mecânico verificável" — refinamento de escopo com força normativa: ondas I-X passam a **dever** classificar refinamento da composição do cluster por modo (a/b/c) com critério aplicado, não a apenas **poder** ajustar editorialmente. Promoção é honesta (vs documentação passiva); fortalece referência formal para ondas futuras sem revisar regra de consolidação.

### Mecanismo de aplicação canonical para ondas I-X

1. Cada onda de migração identifica composição do cluster vs sketch original.
2. Se a composição difere do sketch, classificar refinamento por modo (a/b/c) com critério mecânico aplicado.
3. Documentar em § Origem do ADR consolidado da onda + charter § "Atualização pós-execução" sub-seção dedicada (pattern Ondas F+G+H reaplicado).
4. Operador pode aplicar combinação de modos numa mesma onda — modos não são mutuamente exclusivos (ex.: exclusão + inclusão simultâneas; preservação + exclusão simultâneas).

### Quando NÃO aplica ADR-052

ADR-052 cobre 99% dos refinamentos editoriais da composição do cluster, mas não 100%:

- **Cluster sequence reordering** (ordem de execução das ondas) — coberto pelo primeiro item de ADR-045 § Decisão linha 56; fora do escopo de ADR-052.
- **Subdivisão de consolidado planejado em 2 ADRs** (ex.: alinhamento dividido em alinhamento + reviewer dispatch) — coberto pelo segundo item de ADR-045 § Decisão linha 56; fora do escopo de ADR-052.
- **Mudança estrutural da regra de consolidação** (abandonar hierarquia invertida, reverter para 45 fragmentados, abandonar filtro de admissão) — fora da fronteira inteira; revisão formal de ADR-045 via § Gatilhos próprios (não disparado por ADR-052).

## Consequências

### Benefícios

- **Meta-pattern editorial canonical estabelecido** — 3 modos (a/b/c) com critério mecânico próprio + exemplo empírico canonical. Reader independente classifica refinamento de qualquer onda futura sem reabrir doutrina.
- **Escala mecanismo sem reabrir doutrina por onda** — Onda I aplica modo (c) preservação por constraint análoga ADR-009 com referência formal estabelecida; Ondas J-X seguem mesmo pattern.
- **Charter § "Refinamento editorial documentado" promove de "sinal a observar" para "meta-pattern canonical codificado"** — substância migra de doc operacional editorial para ADR estrutural duradouro.
- **Decisão central de ADR-045 preservada** — apenas o escopo da fronteira § Decisão linha 56 explicitado; sem revisão estrutural.
- **Pattern editorial paralelo a ADR-020/-022/-023 reusos** — "critério mecânico cumulativo" de ADR-013 codificado via ADR sucessor; mesmo padrão aplicado aqui.

### Trade-offs

- **+1 ADR no inventário** (51 → 52, primeiro acréscimo líquido desde Onda A) — natural para ADR meta-doutrinal apex pontual. Inventário continua trajetória para target charter 13-15 (saldo pós-Onda H = 30; ADR-052 + futuras ondas I-X aplicarão consolidação proporcional).
- **§ Decisão extensa (3 modos com 2 critérios cada + exemplos canonical + aplicação à fronteira ADR-045)** — leitor que busca regra pontual precisa scrollar por mais dimensões. Mitigação: sub-headers `### (a) EXCLUSÃO`, `### (b) INCLUSÃO`, `### (c) PRESERVAÇÃO` permitem cross-ref preciso (pattern Ondas E-H reaplicado).
- **Codificação preventiva (antes de 4ª instância empírica)** — ADR-035 critério 4 atingido em rigor com 3 instâncias mas operador escolheu codificar antes em vez de aguardar 4ª. Trade-off aceito: escala mecanismo + estabelece referência formal para Onda I; risco de over-codification mitigado pela § Gatilhos de revisão (4º modo emergente reabre ADR).

### Limitações

- **3 modos cobrem 99%, não 100%** — categorias editoriais nicho podem emergir em Ondas I-X (ex.: substituição inline sem absorção, fragmentação de ADR em sub-categorias). Gatilho de revisão registrado para 4º modo emergente.
- **Fronteira modo (a) bullet 2 vs modo (c)** — ambos cobrem ADRs vigentes standalone (não-absorvidos do cluster); discriminação operada via constraint mecânico (grep ID em § Decisão de ADR Aceito vigente = modo (c); sem grep + ancestralidade codificada com categoria distinta = modo (a) bullet 2). Caso canonical de cada (ADR-034 → modo (c); ADR-010 → modo (a) bullet 2) ancora a fronteira; design-reviewer cutuca se hardcode menos formal aparecer.
- **Combinação de modos numa onda** (ex.: exclusão + inclusão simultâneas) suportada como aplicação operacional mas sem critério explícito de quando combinar vs aplicar individualmente. Mitigação: charter § "Refinamento editorial documentado" registra precedente; padrão emerge empíricamente em Ondas I-X.
- **Sem enforcement mecânico** — convenção sustentada por design-reviewer em /new-adr + doc-reviewer em planos de migração. Validação automática no CI lint (ADR-050 § Decisão (b)) está fora-de-escopo (categoria nova de invariante editorial não-coberta).

### Mitigações

- **§ Anti-regression checklist do charter** atualizado em commit separado post-merge documentando ADR-052 preservações: 3 modos editoriais + aplicação à fronteira ADR-045 linha 56 + escalação se 4º modo emergir.
- **Exemplos canonical literais** preservados em § Decisão de cada modo (a/b/c) — design-reviewer e doc-reviewer auditam fidelidade vs ADR-049/-050/-051 § Origem originais.
- **Gatilho de revisão de ADR-052** registrado para 4º modo emergente — pattern paralelo a ADR-020 que refinou "critério mecânico cumulativo" para 3 cumulativos + 1 pré-requisito quando refinamento empírico justificou.
- **Decisão central de ADR-045 explícitamente preservada** — ADR-052 § Aplicação à fronteira ADR-045 documenta que apenas o escopo do terceiro item de § Decisão linha 56 é explicitado; revisões estruturais continuam via § Gatilhos próprios de ADR-045.

## Alternativas consideradas

### (a) Status quo — continuar absorvendo refinamentos via fronteira atual de ADR-045

Onda I aplicaria preservação análoga de ADR-009 sem meta-pattern codificado; charter § "Refinamento editorial documentado" fica como único registro. Descartada por operador em favor de (B) codificação preventiva. Razões do descarte:

- 3 instâncias empíricas atingem critério ADR-035 4 — codificação preventiva justificada em rigor.
- Risco: cada onda futura aplica refinamento sem perceber pattern estabelecido; 4ª/5ª instâncias escalam urgência sem benefício de codificação anterior.
- Pattern paralelo a ADR-020/-022/-023 reusos: editorial precedente do plugin é codificar pattern emergente via ADR sucessor quando ≥3 reusos justificam.

### (c) Aguardar 4ª instância antes de codificar

ADR-035 critério 4 puro: "≥3 pattern emergente" já atingido em rigor com 3 instâncias; aguardar 4ª daria validação empírica extra antes de codificar. Descartada por operador:

- Critério ADR-035 satisfeito em rigor com 3 instâncias; esperar 4ª não muda satisfação do critério.
- Adia meta-pattern formal sem evidência adicional necessária.
- Onda I (alinhamento/triage com constraint análogo always-include sobre ADR-009) aplicaria modo (c) sem referência formal — perde benefício de codificação anterior.
- Validação extra é coberta pela § Gatilhos de revisão de ADR-052 (4º modo emergente reabre ADR; permite refinamento empírico subsequente).

### (d) Codificar bidirecional + preservação como 2 ADRs separados

Onda G F4 cutucada original (bidirecionalidade) propunha codificar exclusão + inclusão como pattern bidirecional. Onda H adicionou preservação por constraint como 3ª categoria. Alternativa (d) seria codificar bidirecional via ADR-052a + preservação via ADR-052b. Descartada:

- 3 modos compartilham mesmo escopo aplicacional (refinamento da composição do cluster vs sketch); apenas direção da operação difere.
- Codificar como pattern unitário com 3 modalidades é mais **Ockham** (per ADR-043 § Ockham operacionalizado) que 2 ADRs separados sem ganho semântico proporcional.
- Reduz inventário em 1 ADR sem perda de clareza editorial.

### (e) Refinar ADR-045 § Decisão linha 56 inline em vez de ADR sucessor

Editar ADR-045 § Decisão linha 56 expandindo o terceiro item para listar as 3 modalidades. Descartada:

- ADR-045 está Aceito; editar § Decisão é antipattern (ADR-classical principle: imutável).
- Refinamento via ADR sucessor é convenção do toolkit per ADR-034 cond 5 ("sucessor parcial estende sem revogar").
- Pattern paralelo: ADR-020/-022/-023 não editaram ADR-013 § Decisão para reusar "critério mecânico cumulativo" — criaram ADR sucessores próprios.

## Gatilhos de revisão

- **4º modo editorial emerge** em Ondas I-X — categoria editorial nova não-coberta por (a)+(b)+(c). Refinar ADR-052 (pattern paralelo a ADR-020 refinamento "critério mecânico cumulativo" para 3 cumulativos + 1 pré-requisito).
- **Combinação de modos numa onda** torna-se padrão empírico (≥3 ondas combinam modos) sem critério explícito — codificar critério de combinação como sub-pattern.
- **Fronteira modo (a) bullet 2 vs modo (c) gera zona cinzenta recorrente** (≥3 ondas com cutucada do design-reviewer sobre se preservação aplica como EXCLUSÃO por ancestralidade ou PRESERVAÇÃO por constraint) — refinar critério mecânico de discriminação (constraint mecânico via grep em § Decisão é a fronteira atual; ambiguidade pode emergir se hardcode menos formal aparecer).
- **Mudança estrutural na regra de consolidação de ADR-045** (gatilho próprio de ADR-045) — ADR-052 herda revisão proporcional se fronteira de ADR-045 § Decisão linha 56 mudar estruturalmente.
- **Pattern de "sucessor parcial codificando meta-pattern editorial" reusado em outro contexto** (3ª aplicação editorial em outro escopo doutrinal, fora da redesign) — sinal de meta-pattern editorial cross-escopo que merece codificação em camada superior.

## Auto-aplicação per ADR-034

ADR-052 é refinamento doutrinal — codifica meta-pattern editorial emergente em 3 instâncias empíricas. Pela classificação editorial de ADR-034:

- **Cond 5 (sucessor parcial primário estendendo ADR Aceito sem revogar)**: aplica primária — estende fronteira de ADR-045 § Decisão linha 56 explicitando as 3 modalidades editoriais; regra central de ADR-045 (consolidação 45 → ~13-15 ADRs sob hierarquia invertida + filtro de admissão) preservada integralmente.
- **Cond 4 (categoria conceitual nova de artefato)**: **NÃO aplica** sob leitura estreita de "categoria conceitual de artefato" per ADR-034 § Auto-aplicação — ADR-045 introduziu eixo conceitual novo "consolidação editorial cross-cluster sob hierarquia invertida + política de admissão" (cond 4 aplicada em ADR-045 § Auto-aplicação); ADR-052 refina sub-estrutura desse eixo (modos editoriais de operar a fronteira) sem criar 4º eixo conceitual paralelo. Distinto do paralelo ADR-020/ADR-013 (que reusaram pattern operacional já maduro em escopo aplicacional novo); ADR-052 promove sub-pattern dentro de categoria já codificada. Reconhecido na fronteira de cond 4; resolução "cond 5 isolada" é caminho mais conservador (sucessor parcial estende sem criar eixo novo).
- **Cond 1 (decisão estrutural sem ancestral)**: **NÃO aplica** — ADR-045 é ancestral codificado direto (§ Decisão linha 56 fronteira é o ponto de partida).
- **Cond 2 (substitui ADR ancestral invertendo decisão central)**: **NÃO aplica** — regra central de ADR-045 preservada; ADR-052 explicita escopo da fronteira existente.
- **Cond 3 (codifica restrição externa de longa duração)**: **NÃO aplica** — refinamento editorial interno.

**Justificativa para novo ADR vs adendos cross-ref:** cond 5 primária isolada justifica novo ADR. Pattern editorial F4 Ondas C-H estabilizado — auto-aplicação coerente.
