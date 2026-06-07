# ADR-056: Partição editorial dual-audience público-plugin vs pessoal-autor

**Data:** 2026-06-07
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-051](ADR-051-convencoes-editoriais-consolidado.md) § Decisão (a)+(b) — partição editorial por audiência (registro de mudanças vs discoverability vs operativo) é ancestral; este ADR é sucessor parcial estendendo a partição com novo eixo cross-repo (público-plugin vs pessoal-autor) e framing constraint mecanizada.
- **Investigação:** plano `docs/plans/principios-fundamentais-philosophy.md` (2026-05-28, shipped na Onda B/PR #89, merge `f758c8d`) flagrou em decisão (e) a necessidade de codificar partição entre doutrina pública do plugin (descritiva do artefato) e doutrina pessoal do autor (stance personalista em `meta-system/ARCHITECTURE.md`). Deferida via linha em BACKLOG `## Próximos` per ADR-035 critério 4 (aguardava 2º pattern emergente). Item deslockado pós-bump v3.0.0 (PR #106 admission policy enforcement runtime) como primeira aplicação concreta do filtro mecânico em `/new-adr` step 3.5 (ADR-045 § Decisão parte 2).

## Contexto

`docs/philosophy.md` é doutrina pública do plugin — lida por consumers terceiros como descrição da forma do artefato. `meta-system/ARCHITECTURE.md` é doutrina pessoal do autor — registra princípios com framing personalista (stance do autor sobre engenharia em geral). Substância dos 3 princípios fundamentais (Verdade, Excelência, Ockham) emergiu primeiro no meta-system (commit `ac0811d`, 2026-05-28) e foi adaptada para o plugin via plano `principios-fundamentais-philosophy` (Onda B, PR #89).

A partir desse momento concreto, a doutrina vive em duas localizações cross-repo, com framings distintos:

| Localização | Audiência | Framing | Autoridade |
|---|---|---|---|
| `meta-system/ARCHITECTURE.md` | Autor (uso pessoal) | Personalista | Stance do autor |
| `pragmatic-dev-toolkit/docs/philosophy.md` | Consumers terceiros | Descritivo do artefato | Sem prescrição ao usuário |

Sem partição codificada, a tentação editorial natural é: (a) referenciar substância cross-repo (footnote opaca a commit do meta-system); (b) duplicar sem coordenação (drift silencioso entre repos); (c) consolidar substância num lado (perde framing distinto). O plano `principios-fundamentais-philosophy` rejeitou (a) per design-reviewer finding 6 ("dependência cross-repo opaca em doc público") e mecanizou (b) com gabarito anti-prescritivo ("O toolkit assume X" / "Este princípio orientou o design quando Y") + footnote inicial ("Esta seção descreve o que o toolkit assume; não é prescrição ao leitor"). Este ADR codifica retroativamente o pattern aplicado naquela onda como invariante editorial para artefatos futuros.

ADR-051 § Decisão (a)+(b) já partiu artefatos por audiência intra-repo, mas (i) eixos cobertos são **idioma** (PT/EN) e **canal de descoberta** (pré-adoção vs operativo); (ii) escopo é **intra-repo** (artefatos do plugin). O novo eixo (cross-repo + framing constraint) não cabe sob a partição existente — é categoria conceitualmente nova.

## Decisão

Codificar partição editorial em dois eixos paralelos a ADR-051 § Decisão (a)+(b):

### (a) Eixo audiência: público-plugin vs pessoal-autor

Doutrina do toolkit pública (`philosophy.md`, `README.md`, agents/skills, ADRs, planos, `CLAUDE.md`, `BACKLOG.md`) é **descritiva do artefato** — explica o que o toolkit assume e como suas regras pragmáticas materializam o assumido. Doutrina do autor pessoal (`meta-system/ARCHITECTURE.md` e equivalentes futuros) é **personalista** — stance do autor sobre engenharia em geral.

**Critério para placement** (onde uma nova doutrina deve viver) opera em 2 níveis paralelos:

**(i) Critério mecânico** — testável sem julgamento subjetivo, para doutrina específica ao mecanismo do plugin ou à forma observável do artefato:

- Doutrina que governa **mecanismo runtime do toolkit** (skill, agent, hook, schema, lifecycle, gate) → plugin.
- Doutrina que descreve **forma observável do artefato plugin** (convenção editorial do toolkit, instrução operativa) → plugin.
- Doutrina que codifica **stance do autor sobre engenharia geral**, sem amarração ao artefato plugin específico → meta-system.

**(ii) Regra explícita não-mecânica** — para doutrina epistêmica/axiológica cross-cutting que cabe em ambos os repos por audiência:

- Princípio epistêmico ou axiológico cross-cutting (Verdade, Excelência, Ockham, ou futuro análogo) → codificar em **ambos** com framings distintos. Não há canonical único — cada repo carrega a substância pela perspectiva da sua audiência.

Os 2 níveis são paralelos, não hierárquicos. Critério (ii) reconhece honestamente que (i) não cobre o caso epistêmico cross-cutting; autor futuro escrevendo doutrina nova decide por enquadramento antes do placement — substância amarrada a mecanismo/forma do plugin → (i); substância epistêmica/axiológica cross-cutting → (ii). Default conservador (paralelo a ADR-045 § Decisão parte 2 cláusula default-conservadora): em dúvida → assumir cross-cutting e codificar em ambos.

### (b) Eixo cross-repo: framing constraint vs cross-ref opaca

`philosophy.md` (público) **não cita** identificadores cross-repo opacos ao consumer terceiro — commit hashes do meta-system, paths de outros repos sem contexto público, IDs internos pessoais do autor. Razão substantiva: consumer terceiro do plugin não tem acesso ao meta-system; cross-ref público→pessoal vira dead-link semântico para o leitor que mais importa.

`meta-system/ARCHITECTURE.md` (pessoal) **pode citar** o plugin como instância concreta da doutrina pessoal materializada — autor consultando doutrina pessoal tem acesso garantido ao plugin público; referência funciona sintática e semanticamente.

Asymetria portanto é deliberada e segue do acesso assimétrico das audiências, não de categorização editorial (canonical vs informativa).

### (c) Framing constraint mecanizada (load-bearing)

`philosophy.md` e demais artefatos públicos do plugin **não usam**:

- Verbos imperativos diretos ao usuário ("você deve", "você precisa", "siga", "faça").
- Stance personalista ("o autor acredita", "acreditamos", "na nossa visão", "recomendamos que você").
- Cross-ref a artefatos pessoais do autor (commits do meta-system, paths externos opacos ao consumer).

`philosophy.md` e demais artefatos públicos do plugin **usam**:

- Framing descritivo do artefato ("O toolkit assume X", "Este princípio orientou o design quando Y", "Esta convenção materializa Z").
- Footnotes de framing quando a leitura prescritiva é tentadora ("Esta seção descreve o que o toolkit assume; não é prescrição ao leitor").

Gabarito anti-prescritivo + footnote estão materializados em `docs/philosophy.md § Princípios fundamentais` (Onda B). Este ADR promove o pattern de absorção ad hoc para invariante editorial verificável retroativamente.

**Exemplos concretos** (calibração para `design-reviewer` e autor futuro):

- ❌ "Acreditamos que YAGNI é virtude operacional."
- ✅ "O toolkit assume que YAGNI por padrão produz código mais coerente."

O primeiro carrega stance personalista ("acreditamos"); o segundo descreve o que o toolkit assume sem amarrar o leitor a uma crença.

### Razões

- **Audiência distinta** (paralelo a ADR-051 § Razões). Consumer terceiro do plugin tem direito a framing descritivo do artefato; stance personalista é fora-de-escopo para plugin público. Autor tem direito a stance pessoal no próprio repo; framing descritivo do toolkit é fora-de-escopo para doutrina pessoal.
- **Critério em 2 níveis paralelos** (mecânico + regra explícita cross-cutting). § Decisão (a) nível (i) é determinável sem julgamento subjetivo (paralelo a ADR-051 § Decisão (b) critério "lido antes ou depois da adoção"). Nível (ii) reconhece honestamente exceção para epistêmico cross-cutting — operacionalmente claro, ainda que não-mecânico. Autor futuro escrevendo doutrina nova enquadra por nível antes de decidir placement.
- **Drift cross-repo mitigado por independência**. Sem dependência referencial obrigatória, cada lado evolui sem coordenação síncrona forçada; revisão síncrona vira discricionária do autor quando substância nova num lado tem paralelo no outro.
- **Categoria conceitual nova + decisão estrutural sem ancestral direto** (per [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) critérios 4 e 1). Eixo cross-repo + framing constraint não é coberto por ADR-051 (idioma + canal pré/pós-adoção, intra-repo); ADR-056 coexiste paralelamente sem absorver, estender ou revogar ADR-051. Detalhamento em § Auto-aplicação.
- **Materializa filtro de admissão runtime** (per [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 2). 1ª aplicação concreta do step 3.5 de `/new-adr` em uso real pós-v3.0.0. Passa o filtro via reversibilidade (6 cenários concretos nomeados em § Gatilhos) + categoria nova (eixo cross-repo + framing constraint não coberto por ADR-051) — qualquer das 4 heurísticas primárias basta isoladamente; ADR-056 satisfaz 2.

## Auto-aplicação

Aplicação dos critérios de [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) a este ADR:

- **Cond 1 (decisão estrutural sem ancestral direto):** APLICA. Partição público-plugin vs pessoal-autor cross-repo não tinha codificação prévia em ADR vigente.
- **Cond 2 (substitui ADR ancestral identificável):** NÃO APLICA. ADR-051 permanece vigente, não revogado nem marcado Substituído.
- **Cond 3 (codifica restrição externa):** NÃO APLICA. Sem restrição regulatória/contratual/integração externa.
- **Cond 4 (introduz categoria nova):** APLICA. Eixo cross-repo + framing constraint é categoria conceitualmente paralela a ADR-051 (idioma + canal intra-repo).
- **Cond 5 (sucessor parcial):** NÃO APLICA. ADR-056 não absorve, não estende refinando, nem condiciona ADR-051. Cross-ref em § Origem é referência histórica do ancestral conceitual mais próximo, não absorção; coexistência paralela sem amarração canonical.

Cond 1 + Cond 4 isoladamente bastam por ADR-034 § Decisão "Novo ADR quando ≥1 das condições aplica"; aplicação cumulativa reforça a admissão.

## Consequências

### Benefícios

- Framing constraint do `philosophy.md` (e demais artefatos públicos) fica codificada como invariante editorial — autor futuro escrevendo doutrina nova verifica contra checklist concreto (verbos imperativos / stance personalista / cross-ref opaca).
- Doutrina pessoal no meta-system tem espaço próprio para framings que não cabem no plugin (vocabulário pessoal, atalhos privados de pensamento, stance não justificada para terceiros).
- Decisão de placement removida do caso-a-caso: critério mecânico em § Decisão (a) decide sem entrevista.
- Operacionaliza retroativamente o pattern emergente do gabarito anti-prescritivo + footnote já aplicado em Onda B (philosophy.md § Princípios fundamentais), tornando o invariante auditável pelo `design-reviewer`.

### Trade-offs

- Duplicação aceita de substância nos repos (3 princípios fundamentais vivem em ambos com framings distintos). Mitigação: framings distintos justificam — não é replicação cega; cada lado carrega substância pela audiência.
- Sem mecanismo automático de detecção de drift cross-repo. Mitigação: revisão síncrona quando autor toca um dos lados é discricionária; pattern emergente de drift concreto reabre via § Gatilhos.
- Carga editorial do gabarito anti-prescritivo no plugin (autor revisa contra checklist a cada edit em artefato público). Mitigação: `design-reviewer` audita drift via critério novo em `## O que flagrar` "uso de verbo imperativo direto ao usuário / stance personalista / cross-ref opaca em artefato público" — codificado conjuntamente no mesmo commit deste ADR (edit cirúrgico em `agents/design-reviewer.md`), evitando "ADR sem enforcement = decoração" per precedente de ADR-045 § Decisão parte 2 linha 90.

### Limitações

- Não codifica como sincronizar atualizações cross-repo (vira responsabilidade discricionária do autor). Aceito porque mecanismo automático seria over-engineering para 2 repos de mesmo autor.
- Cross-ref pessoal→público é informativa, não canonical — futuro pode requerer canonical dependency se um terceiro consumir doutrina pessoal (improvável; meta-system é repo pessoal por design).
- Decisão de qual nível aplica em § Decisão (a) (mecânico (i) ou regra cross-cutting (ii)) é editorial, não-mecânica. Autor decide se substância nova é amarrada a mecanismo/forma do plugin ou se é epistêmica/axiológica cross-cutting. Para os 3 princípios fundamentais o enquadramento é nível (ii); para doutrina nova futura pode ser ambíguo, com default conservador "em dúvida → assumir cross-cutting e codificar em ambos". Alternativa "canonical em um lado + cross-ref no outro" foi rejeitada por reintroduzir a dependência opaca que § Decisão (b) bane.

## Alternativas consideradas

### Footnote cross-ref opaca em `philosophy.md`

Citar `meta-system/ARCHITECTURE.md` ou commit `ac0811d` via footnote descritivo na seção "Princípios fundamentais". Rejeitada per design-reviewer finding 6 do plano `principios-fundamentais-philosophy` — dependência cross-repo opaca em doc público viola framing descritivo (consumer terceiro não tem acesso ao meta-system; footnote vira dead-link semântico).

### Absorvido em ADR-051 como dimensão (e)

Estender ADR-051 com nova dimensão "framing constraint by cross-repo audience". Rejeitada — ADR-051 já consolidou ADR-007+012+024 sob convenções editoriais intra-repo (idioma + canal + procedures); novo eixo cross-repo é categoria conceitualmente paralela, não refinamento. Per ADR-034 critério 4 (categoria nova) e critério 5 (sucessor parcial), → novo ADR preservando ADR-051 vigente.

### Consolidar substância num lado (plugin OR meta-system)

Eliminar duplicação consolidando em apenas um repo. Rejeitada — perde framing distinto por audiência. Plugin precisa framing descritivo público; meta-system precisa framing personalista. Consolidar = perder uma das audiências.

### git log decision (sem ADR)

Substância como commit message do plano `principios-fundamentais-philosophy` retroativo. Rejeitada — substância governa **invariante editorial** (artefato público vs pessoal) que precisa ser auditável pelo `design-reviewer` e por autor futuro escrevendo doutrina nova. Iteração editorial sem ADR não cria gabarito mecânico testável.

## Gatilhos de revisão

- **2º pattern emergente cross-repo distinto** (outro repo do ecossistema adota framing constraint similar com eixo distinto — ex.: h3-finance-agent codifica framing por audiência operacional vs externa): reabre para revalidar partição vs categoria mais ampla "framing constraint by audience" cross-ecossistema.
- **Autor publica `meta-system/ARCHITECTURE.md`**: framing personalista vira público — partição cross-repo perde objeto; revisão para reformular ou substituir.
- **Plugin transforma framing constraint** (descritivo → prescritivo declarado): cenário improvável per § Decisão; se acontecer, ADR substituído.
- **Drift cross-repo concreto observado** (substância divergente entre `philosophy.md` e `ARCHITECTURE.md` em direção que confunde leitor): reabre para mecanismo automático de detecção ou revisão síncrona obrigatória.
- **Cross-ref pessoal→público vira fricção** (consumers terceiros começam a consumir doutrina pessoal do meta-system de forma sistemática): revisar asymetria § Decisão (b).
- **`design-reviewer` flag de drift do framing constraint em ≥2 artefatos públicos consecutivos**: indica que invariante editorial ficou implícita demais; revisar para incorporar gabarito anti-prescritivo direto em template canonical (`templates/plan.md`, ADR template) ou em `CLAUDE.md` § Editing conventions.
