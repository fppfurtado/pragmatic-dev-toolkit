# ADR-051: Convenções editoriais consolidado

**Data:** 2026-05-31
**Status:** Aceito

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 1 § Implementação — esta Onda H materializa migração do cluster convenções editoriais (6º cluster temático per sketch + refinamento editorial 3ª instância). Sucessor parcial de 3 ADRs sob política de consolidação.
- **Templates de migração:** [ADR-046](ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) (template Onda C — pattern de migração + F1 link rot 2 categorias + F4 cond 5 isolada + F9 fronteira ADR-024) + [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) (template Onda D — primeira sem procedure file + F2 absorção assimétrica) + [ADR-048](ADR-048-free-read-design-reviewer-consolidado.md) (template Onda E — calibração descendente + auto-consistência da always-include) + [ADR-049](ADR-049-execucao-run-plan-consolidado.md) (template Onda F — refinamento editorial por EXCLUSÃO documentado) + [ADR-050](ADR-050-componentes-plugin-consolidado.md) (template Onda G — refinamento editorial por INCLUSÃO + scope máximo).
- **Decisões absorvidas (sucessores parciais primários per ADR-034 cond 5):**
  - ADR-007 (idioma de artefatos informativos — `CHANGELOG`/tag annotation/PR descriptions seguem convenção de commits do projeto; default canonical EN para este repo);
  - ADR-012 (idioma de artefatos discoverability/landing — `README`/manifest descriptions/keywords seguem público alvo do canal de descoberta; sucessor parcial de ADR-007; default canonical EN para Claude Code marketplace);
  - ADR-024 (categoria `docs/procedures/` para procedimentos operacionais compartilhados — sucessor parcial de ADR-055 (originalmente ADR-001 archived na Onda M); paralela a `templates/`; 3 critérios cumulativos para criação de novo procedure).
- **Critério editorial:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 5 (sucessor parcial primário absorvendo 3 ADRs em 1 consolidado); cond 4 **NÃO aplica** (ADR-045 carrega categoria meta da redesign; ADR-051 é sexta instância de migração cluster — F4 lesson Onda C reaplicada literal); cond 1 **NÃO aplica** (ADR-045/-046/-047/-048/-049/-050 são ancestrais codificados em sequência direta); cond 2 **NÃO aplica** — regra central de cada ADR absorvido preservada integralmente em § Decisão (a)-(d); nenhum marcado como `Substituído`; nenhuma inversão de decisão central.
- **Preservação explícita de ADR-034 fora do cluster por constraint mecânico:** ADR-034 (critério adendo vs novo ADR) está hardcoded na always-include curated list de ADR-048 (`always-include hardcoded ADR-009/-034/-043`). Absorvê-lo causaria 2 problemas: (1) editar ADR-048 Aceito para substituir o ID na always-include (mexer ADR-classical é antipattern); (2) ADR-034 é meta-doutrina apex (critério editorial), categoria semântica distinta das convenções editoriais estruturais (idiomas + categoria docs/procedures/). Solução análoga a ADR-010 em Onda F (preservação de ancestral codificado por categoria distinta) com **constraint mecânico explícito adicional**. ADR-034 mantém-se vigente como ADR clássico standalone codificando meta-doutrina apex; substância NÃO precisa estar em ADR-051. Sketch original do charter previa cluster de 4 ADRs (007+012+024+034); Onda H absorve 3 (sem 034) — categoria editorial per ADR-045 § Decisão linha 56 fronteira "absorção em consolidado diferente do sketch original".
- **Refinamento editorial 3ª instância — gatilho de revisão de ADR-045 disparado:** Onda F estabeleceu refinamento por EXCLUSÃO (ADR-037+ADR-010 fora do cluster execução). Onda G por INCLUSÃO (ADR-015 dentro do cluster componentes). Onda H por **PRESERVAÇÃO por constraint mecânico** (ADR-034 fora do cluster por hardcode na always-include). 3 aplicações editoriais sugerem que merece consideração de codificação explícita via ADR sucessor de ADR-045 antes da Onda I. Charter § "Refinamento editorial documentado" registra sinal explícito para decisão de operador em sessão futura. NÃO escopo deste ADR — apenas reconhecimento do gatilho.
- **Link rot doutrinal ativa identificada pré-execução (categoria-b de F1 lesson Onda C):** 4 procedures (cleanup-pos-merge, cutucada-descoberta, forge-auto-detect, reviewer-invocation-read) + README.md citam ADR-024 como autoridade vigente ("categoria `docs/procedures/` estabelecida em ADR-024"); `docs/philosophy.md` linhas 75+77 citam ADR-007 + ADR-012 como decisões canonical de idioma; `skills/release/SKILL.md` linha 72 cita ADR-007 como autoridade do idioma das bullets do changelog. Substância dessas referências absorvida em ADR-051 § Decisão (a)+(b)+(c) fecha gap; ADRs vigentes (ADR-055 (originalmente ADR-001 archived na Onda M consolidado), ADR-014, ADR-026, ADR-034, ADR-040, ADR-041, ADR-043, ADR-046, ADR-047, ADR-048, ADR-049, ADR-050) mantêm-se imutáveis citando autoridade histórica via redirect canonical (categoria-a).

## Contexto

A camada doutrinal do plugin pós-Onda G carregava **3 ADRs vigentes** codificando convenções editoriais estruturais do toolkit:

- **Idioma por audiência:** ADR-007 (informativos: CHANGELOG/tag/PR — convenção de commits) + ADR-012 (discoverability: README/manifests — público alvo do canal). Sucessor parcial relationship (ADR-012 retirou README do escopo livre de ADR-007). Convenção de idioma operativa (espelha projeto consumidor) vive em `philosophy.md` § "Convenção de idioma" — não é ADR, é doutrina pragmática base.
- **Categoria de artefato:** ADR-024 (`docs/procedures/` — procedimentos operacionais compartilhados; paralela a `templates/` de ADR-055 (originalmente ADR-001 absorvido na Onda M) com esqueletos canonical preencheveis). Sucessor parcial de ADR-055 (originalmente ADR-001 archived na Onda M) com fronteira semântica nítida (esqueletos vs algoritmos).

Os 3 ADRs foram criados em sequência empírica (Maio 2026) cada um codificando uma decisão pontual em resposta a incidente concreto — sem coordenação editorial inicial. Pós-v2.14.0 reforma doutrinária e ADR-045 (redesign codificando consolidação 45 → ~13-15 ADRs), o cluster ficou identificado como candidato natural de consolidação por 3 critérios:

1. **Coesão temática moderada** — todos os 3 codificam "convenções editoriais estruturais do toolkit" (idioma por audiência + categoria de artefato). Coesão menor que cluster componentes plugin (Onda G), maior que clusters discoverability/branding ou brainstorm isolados.
2. **Pattern editorial das 3 audiências** — meta-doutrina implícita conectando ADR-007 + ADR-012 + Convenção de idioma operativa de philosophy.md. Consolidação tornaria pattern editorial explícito em ADR único.
3. **Hot spot user-facing em README + 4 procedures** — 5 das 8 ocorrências em docs vivos citam ADR-024 como autoridade. Categoria-b link rot doutrinal ativa concentrada — absorção fecha gap em 1 só sweep.

A consolidação preserva substância integralmente (4 dimensões a/b/c/d codificadas literalmente em § Decisão) e fecha link rot doutrinal ativa (substância de ADR-007/-012/-024 que docs vivos citam vivendo em ADR-051). Frase canonical de philosophy.md "Convenção de idioma" permanece intacta — dimensões (a)+(b)+(d) deste ADR estendem a doutrina operativa sem revogá-la.

**ADR-034 preservado fora do cluster** por constraint mecânico (hardcoded na always-include de ADR-048 § Decisão) + categoria semântica distinta (meta-doutrina apex vs convenções editoriais estruturais). Sketch original do charter listava 4 ADRs no cluster; Onda H absorve 3 — 3ª instância de refinamento editorial após Ondas F (exclusão) e G (inclusão), com **constraint mecânico adicional** que reforça a preservação.

## Decisão

ADR-051 absorve substância integral dos 3 ADRs sob narrativa única coerente, organizada em 4 dimensões interconectadas que codificam as convenções editoriais estruturais do toolkit:

### (a) Idioma de artefatos informativos segue convenção de commits do projeto

**Artefatos informativos do registro de mudanças seguem o idioma da convenção de commits do projeto.**

Cobertura explícita:

- **`CHANGELOG.md`** (entradas e nova prepend a cada release).
- **Mensagem de tag anotada** (a frase fixa `Release vX.Y.Z` continua válida; qualquer síntese de mudanças incluída na annotation acompanha o idioma dos commits).
- **Descrição de PR** quando composta pelo toolkit (ex.: `gh pr create --fill` deriva da mensagem de commit, então herda naturalmente; ferramentas que compõem PR body próprio devem alinhar).

**Fora do escopo desta dimensão:**

- Arquivos `.md` operativos/editoriais — SKILLs, agents, `philosophy.md`, `CLAUDE.md`, ADRs, planos em `docs/plans/`, `BACKLOG.md`, `install.md`. Esses ficam livres — escolha do dev/projeto, audiência diferente, sem benefício de alinhar com idioma de commit. Operativos cobertos por "Convenção de idioma" operativa de `philosophy.md` (espelha projeto consumidor).
- **`README.md` sai desta lista** via dimensão (b) abaixo — categoria de discoverability distinta, audiência pré-adoção.

**Para este repo:** commits EN → `CHANGELOG.md` e tag synthesis em EN; demais `.md` operativos ficam em PT (status quo do repo).

Razões:

- **Coerência narrativa.** Leitor consumindo registro de mudanças (`git log`, `CHANGELOG.md`, `git show <tag>`, PR description) está numa única travessia textual. Mudar idioma entre os artefatos divide a leitura sem benefício.
- **Eliminação de tradução implícita.** Skill que compõe changelog/tag a partir dos commits não precisa traduzir. Tradução automática introduz erro silencioso; tradução manual obriga o operador a redigir o mesmo conteúdo duas vezes.
- **Audiência única do registro de mudanças.** `CHANGELOG`, tag annotation e commits são consumidos pela mesma pessoa (dev examinando release, operador rodando archeology). Operativo tem audiência diferente (dev escrevendo/lendo durante desenvolvimento) e pode legitimamente ficar no idioma natural do dev.

### (b) Idioma de artefatos discoverability/landing segue público alvo do canal de descoberta

**Artefatos cuja função primária é discoverability seguem o idioma do público alvo do canal de descoberta** (sucessor parcial da dimensão (a) — `README.md` sai da categoria "fora do escopo / livre" da (a) via esta dimensão).

**Critério mecânico:** "artefato cuja função primária é ser indexado/lido por audiência externa **antes** de a pessoa decidir adotar o plugin".

Cobertura concreta:

- `README.md` raiz do plugin.
- `.claude-plugin/plugin.json` `description`.
- `.claude-plugin/marketplace.json` descriptions (top-level e por plugin).
- `keywords`/`tags` em manifests (vocabulário de busca).
- GitHub repo About / topics (canal de descoberta, mesmo não versionado).

**Fora do escopo desta dimensão:**

- `docs/install.md` (lido **após** adoção, audiência operativa).
- `docs/philosophy.md` (doutrina operativa).
- `CLAUDE.md` (operating instructions do agente).
- ADRs / planos em `docs/plans/` / `BACKLOG.md` (operativos).
- `CHANGELOG.md` / tag annotations / PR descriptions (cobertos por dimensão (a)).

**Para este repo:** `README.md` em EN com link para `docs/philosophy.md` PT; manifests em EN (status quo ratificado).

Razões:

- **Audiência distinta.** Discoverability serve leitor pré-adoção; operativa serve dev no projeto. Idioma alinhado à audiência reduz fricção em cada caso.
- **Critério mecânico testável.** "Lido antes ou depois da adoção" é determinável sem julgamento subjetivo. Skill author futuro consegue enquadrar artefato novo sem reabrir doutrina.
- **Ratifica status quo dos manifests.** `plugin.json`/`marketplace.json` descriptions já operavam em EN sem ADR antes da consolidação; formalizar reduz dívida doutrinária silenciosa.

### (c) Categoria `docs/procedures/` para procedimentos operacionais compartilhados

**Estabelecida `docs/procedures/` como categoria distinta de `templates/` para procedimentos operacionais compartilhados consumidos por múltiplas skills.**

Distinção semântica nítida (ADR-055 § templates preserved; originalmente ADR-001 absorvido na Onda M):

- **`templates/`** (ADR-055, originalmente ADR-001 absorvido na Onda M; substância preservada vigente): esqueletos canônicos de artefatos. Skills leem via Read em runtime e **preenchem** placeholders ao produzir o artefato. Exemplo: `templates/plan.md` lido por `/triage` ao criar plano novo.
- **`docs/procedures/`** (esta dimensão): procedimentos operacionais. Skills leem via Read em runtime e **executam** o algoritmo descrito ao referenciar o procedimento. Exemplos canonical: `docs/procedures/cleanup-pos-merge.md` referenciado por `/triage` (passo 0) e `/release` (pré-condição); `cutucada-descoberta.md`; `forge-auto-detect.md`; `reviewer-invocation-read.md`.

Razões objetivas:

- **Pureza semântica por localização.** Reader sabe o tipo só pela pasta; não precisa abrir conteúdo nem consultar ADR para entender se é skeleton ou procedimento. Reduz sobrecarga cognitiva sustentada (a cada leitura, qualquer mantenedor futuro).
- **Fronteira intacta de ADR-055 (originalmente ADR-001 absorvido na Onda M).** Definição original de `templates/` como esqueleto preenchível permanece honesta. Sem reescrita semântica, sem exceção silenciosa.
- **Forward-compat.** Próximas extrações de procedimentos compartilhados caem naturalmente em `docs/procedures/<nome>.md` sem reabrir doutrina.
- **Consumer-pattern reutilizado.** Skills consomem `docs/procedures/<nome>.md` via Read runtime, idêntico ao pattern de `templates/plan.md` — mecânica conhecida, sem categoria nova de invocação.

**Mecânica de consumo:** Read em runtime via path do plugin. Embed/copy reintroduz duplicação que esta dimensão resolve — descartado (mesmo critério de ADR-055, originalmente ADR-001 absorvido na Onda M).

**Critério para criação de novo procedimento em `docs/procedures/`** (cumulativo — todos os 3 devem se verificar):

1. Conteúdo é **procedimento operacional** (algoritmo executável), não esqueleto preenchível;
2. **≥2 skills referenciam** ou consumiriam o procedimento (1 consumer = manter inline na skill — extrair sem necessidade vira indireção pura);
3. Extração **resolve acoplamento textual concreto** entre skills (análogo a L1 do audit 2026-05-12). Skill nova hipotética não conta — quando a skill nova de fato aparecer (com plano aprovado em `docs/plans/` ou PR aberto), a extração acompanha.

**Verificação dos 3 critérios é obrigatória** no `/triage` ou ADR que propõe novo procedimento. Revisor (humano ou `design-reviewer`) registra a verificação explicitamente no plano/ADR. Sem essa verificação, a categoria fica sujeita a extração especulativa e perde o gating.

**Invariante de cross-ref bilateral:** ADR/plano que estende `templates/` ou `docs/procedures/` deve manter cross-ref bilateral entre os 2 ADRs governando as categorias (ADR-055 para `templates/` ↔ ADR-051 § Decisão (c) para `docs/procedures/`; originalmente ADR-001 antes da Onda M). Herda invariante de implementação de ADR-024 original (§ Decisão "plano que implementa este ADR deve adicionar bullet em ADR-001 § Status... mitigação não é deferida ao plano — é invariante mecânica"; ADR-001 substância preservada em ADR-055 § Decisão (a) pós-Onda M). ADR-001 § Addendum 2026-05-12 (preservado como § Origem histórica em ADR-055) já satisfaz o cross-ref para ADR-024 archived (redirect canonical resolve para ADR-051 § Decisão (c) automaticamente). Reader futuro propondo extensão de qualquer das 2 categorias deve verificar e manter cross-ref vigente.

**Categorias dentro de `docs/`** (5 totais): `decisions/`, `plans/`, `audits/`, `procedures/` (+ `templates/` separado em raiz do plugin).

### (d) Pattern editorial "3 audiências distintas"

**Meta-doutrina canonical das convenções editoriais — 3 audiências distintas com critério de idioma próprio:**

| Audiência | Artefatos canonical | Critério de idioma | Origem doutrinária |
|---|---|---|---|
| **Operativa** | SKILLs/agents/`philosophy.md`/`CLAUDE.md`/ADRs/planos/`BACKLOG.md`/`install.md` | Espelha o idioma do projeto consumidor (default canonical PT-BR) | "Convenção de idioma" em `philosophy.md` — doutrina pragmática base, não é ADR |
| **Informativa** | `CHANGELOG.md` + tag annotations + PR descriptions | Segue convenção de commits do projeto (default canonical EN) | Esta dimensão § (a) |
| **Discoverability** | `README.md` + manifest descriptions + keywords + GitHub About | Segue público alvo do canal de descoberta (default canonical EN para Claude Code marketplace) | Esta dimensão § (b) |

Pattern editorial estabelecido em ADR-007 (2 audiências: operativa + informativa) + estendido em ADR-012 (3ª audiência: discoverability). Preservado em ADR-051 § Decisão (d) como meta-doutrina canonical das convenções editoriais.

**Para este repo:** operativa PT-BR + informativa EN (commits EN) + discoverability EN (marketplace anglófono).

**Aplicação canonical:** dev consumidor encara matriz audiência-vs-artefato; cada artefato cai em 1 das 3 categorias com critério mecânico próprio. Sem julgamento subjetivo — qualquer skill author futuro enquadra artefato novo sem reabrir doutrina.

**Hooks são exceção universal** — mecânica universal, mensagens de erro/bloqueio sempre em inglês, independentemente do idioma do projeto (per `philosophy.md` § Convenção de idioma; preservado vigente sem necessidade de cobertura em ADR-051).

## Origem histórica

Cada dimensão consolida 1 incidente empírico, preservado integralmente na trilha histórica:

- **Dimensão (a)** — Drift entre commits (EN) e `CHANGELOG.md` (PT) descoberto durante `/triage` da demanda de síntese de tag em `/release` (sessão de 2026-05-07). v1.23.0 commitada localmente seguiria o mesmo padrão; tag synthesis herdaria o drift e tornaria o problema visível em mais artefatos. Gap subjacente: nem `philosophy.md` → "Convenção de idioma" (escopo: prosa de skills/agents/templates/reports) nem "Convenção de commits" (escopo: mensagens de micro-commit) cobriam artefatos informativos do registro de mudanças. Cobertura ratificou status quo de manifests-EN sem ADR. **Trade-off de migração retroativa documentado em ADR-007 original:** entradas PT pré-2026-05-07 do `CHANGELOG.md` migraram para EN como trabalho one-time aceito consequência editorial da decisão; drift acumulado apenas no CHANGELOG, com commits EN consistentes desde o início — migração restaurou coerência histórica entre commits e changelog. Decisão consciente, não negligência; reader que cai em CHANGELOG bilíngue em git history pré-migração tem o contexto preserved.

- **Dimensão (b)** — Análise pré-publicação no Claude Code marketplace (sessão `/triage` de 2026-05-10) detectou que o `README.md` em PT-BR limitava discoverability para o público anglófono majoritário do canal, enquanto `plugin.json` e `marketplace.json` descriptions já operavam em EN sem registro doutrinário. ADR-007 (`## Decisão` → "Fora do escopo") explicitamente listava `README.md` como livre — categoria operativa misturando audiências distintas (dev no projeto vs leitor pré-adoção). Refinamento extraiu README para categoria de discoverability própria; ratificou status quo dos manifests-EN.

- **Dimensão (c)** — Auditoria `docs/audits/runs/2026-05-12-architecture-logic.md` § 2.6 (finding L1) identificou acoplamento textual entre `/release § Cleanup pós-merge` e `/triage §0` — `/release` referenciava textualmente "skills/triage/SKILL.md `### 0. Cleanup pós-merge`"; renomear ou mover o passo 0 em `/triage` quebrava `/release` silenciosamente. Proposta G_arch sugeriu extrair algoritmo (~30 linhas) para procedimento compartilhado. Categoria nova `docs/procedures/` ratificada pós-fato com 3 itens em 4 dias (cleanup-pos-merge + cutucada-descoberta + forge-auto-detect), confirmando YAGNI suspeito da criação com 1 arquivo (ADR-024 § Limitações Strong-stable atingido; Status promovido Proposto→Aceito 2026-05-16).

§ Gatilhos abaixo consolida triggers das 3 decisões em formato unificado.

## Consequências

### Benefícios

- **Cluster convenções editoriais migrado em 1 ADR** (vs 3 fragmentados) — leitura linear das 4 dimensões interconectadas em vez de cross-refs entre 3 arquivos. Pattern editorial das 3 audiências fica explícito em ADR único.
- **Link rot doutrinal ativa categoria-b fechado** — substância citada por 4 procedures + README + philosophy.md + skills/release absorvida em § Decisão; ADRs vigentes preservados sem edição (imutáveis); cross-refs resolvem via redirect canonical.
- **Pattern editorial "3 audiências distintas"** centralizado como meta-doutrina explícita — skill author futuro enquadra artefato novo sem reabrir doutrina.
- **Categoria `docs/procedures/` consolidada como decisão estável** — Strong-stable atingido pós-Onda 3 com 3 procedures; ADR-051 § Decisão (c) preserva 3 critérios cumulativos para criação de novos procedures.
- **ADR-034 preservado vigente** como meta-doutrina apex standalone — constraint mecânico de always-include ADR-048 respeitado; categoria semântica meta-doutrinal preservada distinta da estrutural editorial.

### Trade-offs

- **3 ADRs arquivados** — drop líquido de 2 no inventário (menor que Onda G por scope reduzido). Cross-refs em immutable docs (ADRs antigos + planos históricos + manifests/CHANGELOG) ficam como link rot consciente categoria (a) — redirect canonical em archive fecha o gap.
- **§ Decisão extensa (4 dimensões + tabela meta-doutrinal das 3 audiências)** — leitor que busca regra pontual precisa scrollar por mais dimensões. Mitigação: sub-headers `§ Decisão (a/b/c/d)` permitem cross-ref preciso; pattern editorial Ondas E-G (sub-headers em ADR-048/-049/-050) reaplicado.
- **3ª instância de refinamento editorial** (preservação por constraint mecânico) dispara gatilho de revisão de ADR-045 — sinal explícito a registrar no charter pós-merge para decisão de operador em sessão futura. NÃO bloqueia esta onda; pode resultar em ADR sucessor de ADR-045 antes da Onda I codificando 3 modos editoriais (exclusão + inclusão + preservação por constraint).

### Limitações

- **ADR-034 preservado fora do cluster** — substância (critério adendo vs novo ADR; 5 condições para novo + 4 para adendo; 4 formas de localização do adendo) NÃO está em ADR-051. Reader que busca meta-critério editorial deve consultar ADR-034 vigente diretamente. Justificativa: constraint mecânico (always-include ADR-048) + categoria semântica distinta (meta-doutrina apex vs convenções editoriais estruturais). Ver § Origem para reasoning detalhado.
- **Hooks exceção universal** mantida em `philosophy.md` § Convenção de idioma — não absorvida nesta dimensão (decisão pragmática de mecanismo universal, não convenção editorial doutrinária). ADR-051 § Decisão (d) tabela das 3 audiências menciona exceção mas não a codifica.
- **Sem cobertura de bilingue real** — projeto consumidor adotando fluxo bilíngue real (releases internas PT + externas EN) ficaria sem suporte explícito. ADR-051 herda esta limitação de ADR-007 + ADR-012 originais. Reabrir caso emerja.
- **Não cobre marketplaces dual-language nativos** (cenário futuro) — herdado de ADR-012.
- **Mecanismo de enforcement editorial** ausente para a verificação dos 3 critérios cumulativos para novo procedure (§ Decisão (c)) — convenção sustentada por `design-reviewer` em PRs introduzindo novo `docs/procedures/<nome>.md`. Validação automática no CI lint (ADR-050 § Decisão (b)) está fora-de-escopo desta iteração.

### Mitigações

- **Anti-regression checklist § Convenções editoriais** atualizado em charter post-merge garante substância das 4 dimensões + meta-doutrina das 3 audiências preservada em validação operacional de ondas I-X (design-reviewer aplica checklist como rubric extra).
- **Substância para link rot categoria-b** preservada literal em § Decisão (a) + (b) + (c) + (d) — design-reviewer e doc-reviewer auditam fidelidade vs ADR-007/-012/-024 originais.
- **ADR-034 vigente standalone** com cross-ref preserva em § Origem deste ADR — reader que cai em ADR-007/-012/-024 archived e segue redirect chega em ADR-051; ADR-034 mantém-se discoverable via always-include do design-reviewer (mecânica de leitura preserved).
- **Gatilho de revisão de ADR-045 registrado no charter** como sinal explícito — não dispara ADR sucessor automaticamente; operador decide em sessão futura se merece codificação explícita do meta-pattern editorial das 3 categorias (exclusão + inclusão + preservação por constraint).
- **Hooks exceção universal** continua codificada em `philosophy.md` § Convenção de idioma — cobertura preserved no doc canonical operativo, não duplicada aqui.

## Alternativas consideradas

### (a) Absorver os 4 ADRs do sketch original (incluindo ADR-034)

Sketch original do charter previa cluster de 4 ADRs (007+012+024+034). Absorver os 4 sem refinamento editorial. Descartado:

- **Constraint mecânico**: ADR-034 está hardcoded na always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]`. Absorvê-lo exigiria editar ADR-048 Aceito para substituir o ID (mexer ADR-classical é antipattern); leitura mecânica do design-reviewer cairia em ADR-034 archived (com redirect) em vez do consolidado, perdendo 1 hop e quebrando o caminho mecânico.
- **Categoria semântica distinta**: ADR-034 é meta-doutrina apex (critério meta-editorial sobre quando criar adendo vs novo ADR), não convenção editorial estrutural (idiomas + categoria de artefato). Absorver mistura escopos editoriais.
- ADR-034 pertenceria a futuro cluster apex meta-doutrinal hipotético (charter linha 182), não a convenções editoriais.

### (b) Consolidar em sub-clusters menores (idiomas + categoria procedures separados)

Criar 2 ADRs consolidados (ADR-051a idiomas [007+012]; ADR-051b categoria [024]) em vez de 1. Descartado:

- **Spírito ADR-045**: target 13-15 ADRs vigentes; sub-clusters multiplicariam ADRs sem ganho proporcional. Onda H seria 3 ondas em 1 (idiomas + categoria + nada) com complexidade administrativa amplificada.
- **Coesão temática das convenções editoriais**: idiomas + categoria de artefato coexistem como "convenções editoriais do toolkit" — separação artificial perderia narrativa do pattern das 3 audiências.
- **Pattern editorial das 3 audiências** (dimensão d) transcende sub-clusters — codificar em ADR único alinha pattern central.

### (c) Manter os 3 ADRs vigentes (status quo)

Status quo pré-Onda H. Descartado: cluster identificado em ADR-045 § Decisão parte 1 § Implementação como candidato natural de consolidação; link rot doutrinal ativa categoria-b em 4 procedures + README + philosophy.md + skills/release reabre cada vez que reader busca substância citada; redesign declarou consolidação como invariante doutrinal pós-v2.14.0.

### (d) Disparar ADR sucessor de ADR-045 codificando 3 modos editoriais antes da Onda H

3ª instância de refinamento editorial disparou gatilho de revisão de ADR-045 conforme charter § "Refinamento editorial documentado" sinal. Antes da Onda H, criar ADR sucessor parcial de ADR-045 codificando 3 modos editoriais (exclusão + inclusão + preservação por constraint) explicitamente. Descartado:

- **Bloqueio de Onda H** sem ganho proporcional — refinamento editorial cabe na fronteira atual de ADR-045 § Decisão linha 56; 3 instâncias ainda cabem como ajustes editoriais individuais.
- **Operador decide em sessão futura** — sinal registrado no charter pós-merge é caminho mais conservador. Onda H prossegue documentando explicitamente o gatilho disparado para revisão posterior.
- Defere decisão estrutural editorial sem absorvê-la na temática (paralelo ao caminho Onda G F4 opção (a)).

### (e) Editar ADR-048 para atualizar always-include para `[ADR-009, ADR-051, ADR-043]`

Caminho que viabilizaria absorção de ADR-034 sem perder mecânica da always-include. Descartado:

- **Edit em ADR Aceito é antipattern** — ADR-classical principle: imutável; supersedeção via novo ADR. Editar always-include hardcoded mid-stream durante consolidação editorial mistura escopos (consolidação editorial vs revisão de ADR-048 estrutural).
- **ADR-051 não é meta-doutrina apex equivalente a ADR-034** — substituir ADR-034 por ADR-051 na always-include faria reader cair em consolidado editorial (idiomas + categoria) onde estava buscando meta-critério editorial apex. Categoria semântica errada.

## Auto-aplicação per ADR-034

ADR-051 é ele próprio refinamento doutrinal — codifica regra que vivia distribuída em 3 ADRs vigentes. Pela classificação editorial de ADR-034:

- **Cond 5 (sucessor parcial primário absorvendo ADR Aceito sem revogar)**: aplica primária — absorve ADR-007+ADR-012+ADR-024 em 1 consolidado preservando regra central de cada um integralmente em § Decisão (a)-(d).
- **Cond 4 (categoria conceitual nova de artefato)**: **NÃO aplica** — ADR-045 já carrega categoria meta da redesign ("consolidação 45 → ~13-15 ADRs"); ADR-051 é sexta instância de migração cluster (C+D+E+F+G+H), não primeira instância de categoria nova. F4 lesson Onda C reaplicada literal.
- **Cond 1 (decisão estrutural sem ancestral)**: **NÃO aplica** — ADR-045 (charter da redesign) + ADR-046+ADR-047+ADR-048+ADR-049+ADR-050 (templates de migração) são ancestrais codificados em sequência direta. ADR-051 é instância do pattern, não decisão sem ancestral.
- **Cond 2 (substitui ADR ancestral invertendo decisão central)**: **NÃO aplica** — regra central de cada um dos 3 ADRs absorvidos está preservada integralmente em § Decisão (a) até (d); nenhum ADR é marcado como `Substituído` (ficam `Aceito` com redirect canonical no topo per pattern de archive); nenhuma inversão de decisão central. Há consolidação de cross-refs em narrativa única, não substituição doutrinal.
- **Cond 3 (codifica restrição externa de longa duração)**: **NÃO aplica** — sem restrição externa nova (regulatória, contratual, integração estável); decisão é editorial interna.

**Justificativa para novo ADR vs adendos cross-ref:** cond 5 primária isolada justifica novo ADR. Pattern editorial F4 Ondas C/D/E/F/G/H estabilizado — auto-aplicação coerente.

## Gatilhos de revisão

Consolida triggers das 3 decisões absorvidas:

### Para dimensão (a) idioma artefatos informativos

- Projeto consumidor com fluxo bilíngue real (releases internos em PT, externos em EN) precisar suporte → reabrir para considerar dual-lang artifacts ou idioma override por artefato.
- Surgir novo artefato informativo no toolkit (release notes em formato distinto, summary boards, etc.) que não caiba na regra → re-avaliar definição de "informativo".
- Commits do projeto consumidor mudarem de idioma (raro, mas possível em refactor de processo) — Convenção de commits já cobre detecção; CHANGELOG/tag acompanham automaticamente a partir desse ponto, mas migração retroativa do CHANGELOG fica como decisão separada.

### Para dimensão (b) idioma discoverability

- Marketplace passa a suportar dual-language listing nativo → reabrir para considerar i18n por canal.
- Público alvo do canal muda predominância (ex.: PT vira majoritário no Claude Code marketplace) → critério "público alvo do canal" adapta automaticamente; revisar exemplos congelados em § Decisão (b).
- Surge novo artefato no toolkit cuja audiência está na fronteira (operativa-vs-discoverability) → revisar critério mecânico para incluir explicitamente.

### Para dimensão (c) categoria docs/procedures/

- **Próximo `docs/procedures/<nome>.md` proposto** em `/triage` ou em ADR → revisor (humano ou `design-reviewer`) verifica explicitamente os 3 critérios cumulativos (procedimento operacional, ≥2 skills, acoplamento concreto) e registra a verificação no plano/ADR. Verificação ausente bloqueia merge. Checkpoint observável, não promessa de revisão.
- **`docs/procedures/` cresce para ≥5 arquivos** → reabrir para sub-organização (por skill consumidora ou por tipo de procedimento). Análogo ao gatilho de ADR-014 para `docs/plans/` ≥100.
- **Incidente concreto de mistura** (PR coloca procedimento em `templates/` ou esqueleto em `docs/procedures/`) → reabrir nomenclatura ou consolidar em umbrella único (volta à opção `shared/`).

### Para dimensão (d) pattern editorial 3 audiências

- **Quarta audiência emergir** (ex.: artefato cujo critério não cabe em operativa/informativa/discoverability) — sinal de que pattern precisa estender. Por enquanto 3 audiências cobrem todos os artefatos do toolkit observados.
- **Critério de uma audiência mudar** (ex.: convenção de commits do projeto adotar idioma fixo cross-projeto) — pattern editorial mantém-se; só o critério de uma dimensão atualiza.

### Para meta-decisão de consolidação (Onda H)

- **Operador decide codificar 3 modos editoriais via ADR sucessor de ADR-045** (gatilho de revisão de ADR-045 disparado por 3ª instância de refinamento editorial) — refinamento estrutural de ADR-045 § Decisão linha 56 fronteira. NÃO escopo desta onda; charter pós-merge registra sinal explícito.
- **ADR-034 ganhar consumers vigentes adicionais** (ex.: nova skill ou agent passa a citar ADR-034 como autoridade vigente) — reforça preservação fora do cluster.
- **4ª instância de refinamento editorial** em Ondas I-X (categoria editorial nova não-coberta por exclusão/inclusão/preservação por constraint) — gatilho de revisão de ADR-045 escalado; codificação explícita via ADR sucessor torna-se mais urgente.
