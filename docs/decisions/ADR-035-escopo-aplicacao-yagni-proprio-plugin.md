# ADR-035: Escopo de aplicação de YAGNI ao próprio plugin

**Data:** 2026-05-18
**Status:** Proposto

## Origem

- **Investigação:** Padrão recorrente em planos históricos do plugin usando YAGNI como veto reflexo a estrutura interna — `docs/plans/v1.8-cenarios-validacao-manual.md` ("Não criar agente prompt-reviewer — uma sessão não justifica papel novo (YAGNI)"), `docs/plans/v1.11-skill-release-tagueamento.md` ("promover pra philosophy só se um segundo consumidor aparecer (YAGNI)"), `docs/plans/cleanup-pos-merge-worktree.md` ("Reavaliar se YAGNI: cleanup é trivial"), múltiplas linhas em `BACKLOG.md ## Próximos` ("YAGNI até backlog crescer ≥20 itens", "YAGNI até o pain ser reportado em uso real"). Aplicação reflexa que vetava estrutura sem examinar o filtro real.
- **Decisão base:** Memory editorial `feedback_yagni_plugin_vs_consumer` (2026-05-17) — operador identificou que a intenção original ao codificar YAGNI no coração do plugin era orientar projetos consumidores, não a si mesmo; "não era para ser uma restrição" autoaplicada. Default ADR para refinamento doutrinal per memory `feedback_adr_threshold_doctrine`.
- **Classificação editorial:** Pelo [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md), condição 1 (decisão estrutural sem ancestral — YAGNI nunca codificado em ADR) aplica → novo ADR. Condição 4 (categoria nova) **não** aplica — ADR-035 é critério editorial paralelo a outras meta-doutrinas (ADR-010, ADR-011, ADR-023, ADR-026, ADR-034), não categoria conceitual de artefato (cf. ADR-034 § Auto-aplicação que estreita "categoria nova" a categoria de artefato).

## Contexto

`docs/philosophy.md` linha 7 abre o documento com **"YAGNI por padrão"** como princípio universal, sem qualificar target. O princípio permeia o coração do toolkit: skills (checklist de gaps em `/triage`, heurísticas em `/run-plan`), reviewers (`code-reviewer` aplica rubrica YAGNI em diffs), e o próprio framing editorial. A intenção original quando isso foi codificado: oferecer aos projetos consumidores um workflow que rejeita cerimônia tática prematura e abstrações sem dor real.

Em paralelo, durante o desenvolvimento do próprio plugin, o agente (e por extensão o operador-via-agente) acabou aplicando YAGNI como **filtro reflexo** a decisões internas: criar ADR, adicionar role, refinar mecanismo de skill, formalizar doutrina. Os planos citados na § Origem ilustram o padrão. O deslize é sutil porque YAGNI é princípio do toolkit — invocá-lo dá ar de coerência editorial. Mas o plugin tem natureza distinta de um app/lib de domínio:

- App de domínio: valor cresce com **menos código** (YAGNI evita peso morto que retarda mudança futura).
- Plugin de metodologia: valor cresce com **coerência doutrinal articulada** (skills/ADRs/philosophy precisos reduzem ambiguidade que o agente reproduz em consumidores).

Aplicar YAGNI reflexamente a decisões internas do plugin suprime exatamente o tipo de estrutura que o plugin precisa para funcionar (doutrina explícita, fronteiras nítidas, incidentes codificados) — a mesma estrutura que skills/reviewers ensinam consumidores a adicionar quando há dor real.

Sem critério escrito, ad hoc continua: próxima decisão interna pode novamente ser vetada por "YAGNI" sem que o filtro real seja examinado.

## Decisão

YAGNI no `pragmatic-dev-toolkit` é princípio **transmitido a projetos consumidores**, codificado em skills, reviewers, agents e `docs/philosophy.md`. **Não é filtro autoaplicado mecanicamente a decisões internas do plugin** (ADRs, roles, mecanismos de skill, formalização doutrinal em `CLAUDE.md`/`philosophy.md`).

### Filtro para decisões internas do plugin

Em decisões sobre o design interno do plugin, o filtro **não é** "precisamos disso agora?" e sim:

> Isso paga seu custo de manutenção pela clareza/coerência que adiciona?

Critérios legítimos para adicionar estrutura no plugin (≥1 basta):

1. **Incidente recorrente ou padrão observado** em uso real (não hipótese).
2. **Fronteira doutrinal borrada** — categoria nova com fronteira nítida supera churn de refactor (per memory `feedback_semantic_purity_preference`).
3. **Contradição/refinamento de doutrina** existente em ADR/`philosophy.md`/`CLAUDE.md` — empurra ADR per memory `feedback_adr_threshold_doctrine` e [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md).
4. **Codificação de pattern emergente** já aplicado ≥3 vezes ad hoc em decisões anteriores do plugin (auditável retroativamente).

### Escopo do princípio para consumidores preservado

YAGNI continua valendo plenamente para artefatos **dirigidos a consumidores**:

- Skills/reviewers/agents avaliam ou geram código consumidor → "YAGNI por padrão" continua o critério promovido.
- `design-reviewer` aplica os 4 critérios em planos/ADRs do plugin pré-commit (wiring de [ADR-011](ADR-011-wiring-design-reviewer-automatico.md), free-read de `docs/decisions/` e `philosophy.md`). É o auditor designado para decisões internas do plugin.
- `code-reviewer` mantém rubrica YAGNI universal no diff (independente de o diff ser do plugin ou de consumidor) — não tem context-aware switch nem free-read de ADRs. Quando flagar estrutura doutrinal legítima do plugin no dogfood, override por inação do operador citando este ADR (pattern já estabelecido para reviewers).

## Consequências

### Benefícios

- Decisões internas do plugin (ADRs, roles, doutrina) deixam de ser vetadas reflexamente por "YAGNI" — filtro positivo (custo vs clareza) substitui filtro negativo (YAGNI).
- Coerência: o que skills ensinam consumidores a fazer (resistir a cerimônia tática prematura) não vira impedimento para o plugin articular sua própria doutrina.
- `design-reviewer` ganha critério explícito para auditar decisões internas — ausência dos 4 critérios é sinal de cutucada em ADRs/planos do plugin.

### Trade-offs

- Filtro "paga seu custo pela clareza?" tem zona cinzenta — operador/reviewer pode justificar estrutura excessiva. Mitigação: 4 critérios concretos limitam o "sim" a casos com benchmark (incidente, fronteira nítida, contradição, refinamento).
- 1 ADR adicional no inventário (35 total). Mitigação: codifica critério usado retroativamente em quase todos os ADRs do plugin — formalização tardia de regra emergente, baixo custo de manutenção.

### Limitações

- ADR cobre apenas YAGNI. Outros princípios doutrinais ("flat por padrão", "refatorar depois > abstrair cedo", bounded contexts) podem ter o mesmo padrão de aplicação reflexa interna. Reabrir escopo ou criar ADR análogo se padrão recorrer com outro princípio.

### Auto-aplicação coerente

ADR-035 é ele próprio refinamento doutrinal — codifica regra que vivia implícita e que o próprio agente vinha aplicando reflexamente. Pelo ADR-034, condição 1 (decisão estrutural sem ancestral — YAGNI nunca codificado em ADR) aplica → novo ADR é o caminho correto. Condição 4 (categoria nova) **não** aplica — ADR-035 é critério editorial paralelo a outras meta-doutrinas (ADR-010, ADR-011, ADR-023, ADR-026, ADR-034), não introduz categoria conceitual de artefato. Auto-consistente com a leitura estreita de "categoria nova" estabelecida em ADR-034 § Auto-aplicação.

## Implementação

- `docs/philosophy.md` linha 7 ganha nota curta qualificando "YAGNI por padrão" + cross-ref a este ADR. Texto literal sugerido — adicionar entre a frase "YAGNI por padrão." e a frase seguinte: "**Escopo:** princípio transmitido a projetos consumidores; decisões internas do próprio plugin seguem critério distinto, ver [ADR-035](decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md)."
- `CLAUDE.md` § "Editing conventions" ganha bullet cross-ref a este ADR (paralelo aos bullets de ADR-010, ADR-011, ADR-023, ADR-026, ADR-034): texto literal sugerido — "**Escopo de aplicação de YAGNI**: princípio transmitido a projetos consumidores via skills/reviewers/`philosophy.md`, não filtro autoaplicado a decisões internas do plugin per [ADR-035](docs/decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) — em decisões internas (ADR, role, mecanismo, formalização doutrinal), filtro é 'paga seu custo de manutenção pela clareza/coerência?' com 4 critérios legítimos: incidente recorrente, fronteira doutrinal borrada, contradição/refinamento de doutrina, codificação de pattern emergente ≥3x ad hoc."

## Alternativas consideradas

### (b) Manter `docs/philosophy.md` inalterado, só ADR + bullet CLAUDE.md

Padrão recente (ADR-033, ADR-034) shippou ADR + bullet CLAUDE.md sem tocar `philosophy.md`. Mais conciso, preserva `philosophy.md` como produto consumer-facing limpo.

Descartada por escolha do operador na cutucada do `/triage` (2026-05-18): a frase "YAGNI por padrão" em `philosophy.md` é fonte universal lida por reviewers via free-read (`design-reviewer`, `code-reviewer`); refinamento isolado em ADR/`CLAUDE.md` deixa drift na fonte que mais frequentemente gatilha aplicação reflexa. Per memory `feedback_semantic_purity_preference`, fronteira nítida em fonte universal supera 1-2 linhas de churn editorial.

### (c) Manter apenas como memory editorial

Memory `feedback_yagni_plugin_vs_consumer` (2026-05-17) registra a regra. Descartada porque memory é vivência local-gitignored sem rastreabilidade pública nem auditabilidade por `design-reviewer`; default ADR per memory `feedback_adr_threshold_doctrine` para refinamentos doutrinais.

### (d) Só bullet em `CLAUDE.md` § "Editing conventions", sem ADR

Registrar critério apenas como bullet em `CLAUDE.md` sem novo ADR. Mais conciso, evita 1 ADR no inventário. Descartada pelo pattern simétrico estabelecido por ADR-010, ADR-011, ADR-023, ADR-026, ADR-034 — todas meta-doutrinas em ADRs com bullets cross-ref em `CLAUDE.md`. Bullet sem ADR perde Origem/Contexto/Alternativas/Gatilhos que justificam e auditam a decisão. Descarte paralelo ao de (b) "Só CLAUDE.md prosa, sem ADR" em ADR-034 § Alternativas.

## Gatilhos de revisão

- **Segundo princípio doutrinal** mostrando o mesmo padrão de aplicação reflexa interna (ex.: "flat por padrão" sendo invocado para vetar estrutura no plugin) — reabre escopo: generalizar este ADR para "Escopo de aplicação de princípios doutrinais ao próprio plugin" ou criar ADR análogo dedicado.
- **5º critério legítimo** emergir para adicionar estrutura no plugin além dos 4 codificados — refinar lista em § Filtro para decisões internas do plugin.
- **`design-reviewer` ou code-reviewer aplicar mal** o filtro em ≥2 PRs (justificar over-engineering como "paga seu custo" ou vetar estrutura legítima como "YAGNI" mesmo após este ADR) — refinar critério, adicionar guarda ou tornar mais mecânico.
