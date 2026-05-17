# ADR-034: Critério editorial — adendo em ADR existente vs novo ADR para refinamento doutrinal

**Data:** 2026-05-17
**Status:** Proposto

## Origem

- **Investigação:** Auditoria 2026-05-15 (E_arch) flagou ambiguidade quando refinamento doutrinal pode (a) ficar como adendo em ADR existente ou (b) criar novo ADR. Cadeias temáticas do toolkit mostram padrões mistos: design-reviewer cobre 4 ADRs (ADR-009, ADR-011, ADR-021, ADR-026), modo local cobre 4 ADRs (ADR-005, ADR-018, ADR-025, ADR-030), cutucada cobre 2 ADRs (ADR-017, ADR-029). Refinamentos foram absorvidos via 2 caminhos sem critério escrito: novos ADRs sucessores parciais (ADR-024/-029/-030/-033) ou adendos em ADRs Aceitos (ADR-001 ganhou Addendum 2026-05-12 → ADR-024 e Addendum 2026-05-16 → ADR-033; ADR-005 ganhou parágrafo cross-ref em § Limitações para ADR-025; ADR-011 ganhou parágrafo cross-ref em § Decisão para ADR-026).
- **Decisão base:** Memory editorial "Limiar de ADR para mudanças em doutrina" — refinar/inverter critério documentado em `philosophy.md`/`CLAUDE.md` (mesmo parcial) → default ADR. ADR-034 codifica esse limiar de forma mecânica.
- **Caso de uso recente:** D_arch (Onda 5 gêmeo, [ADR-033](ADR-033-templates-admite-single-consumer-declarativo.md), commit `ea602bf`, 2026-05-16) escolheu "novo ADR sucessor" sobre "adendo em ADR-001 Aceito" via cutucada do `/triage` — primeiro exemplo concreto da regra que E_arch codifica retroativamente.

## Contexto

O toolkit acumulou 34 ADRs (incluindo este) por meio de duas formas distintas para refinar doutrina:

1. **ADRs novos** (incluindo sucessores parciais explícitos como ADR-024 → sucessor parcial de ADR-001; ADR-029 → sucessor parcial de ADR-017; ADR-030 → sucessor parcial de ADR-005; ADR-033 → sucessor parcial de ADR-001).
2. **Adendos** em ADRs Aceitos (ADR-001 ganhou dois Addenda; ADR-005 ganhou parágrafo cross-ref em § Limitações para ADR-025; ADR-011 ganhou parágrafo cross-ref em § Decisão para ADR-026).

Sem critério escrito, autor de mudança doutrinal decide ad hoc — produz inconsistência (mesmo tipo de refinamento às vezes vira ADR, às vezes adendo). `design-reviewer` audita caso por caso sem benchmark mecânico.

## Decisão

Critério mecânico para escolher entre adendo em ADR existente vs novo ADR:

### Novo ADR quando ≥1 das condições aplica

1. **Decisão estrutural sem ancestral direto** — regra central nova em vértice doutrinário ainda não coberto por ADR existente.
2. **Substitui ADR ancestral identificável** — operação que requer marcar ADR específico como `Substituído` ou cuja regra central inverte a de ancestral identificável.
3. **Codifica restrição externa** de longa duração (regulatória, contratual, integração estável).
4. **Introduz categoria nova** (novo eixo conceitual paralelo ao existente — ex.: ADR-024 criou categoria `docs/procedures/` paralela a `templates/`).
5. **Sucessor parcial** — estende, refina ou condiciona ADR Aceito sem revogar. Modalidade explícita do toolkit; exemplos canonical: ADR-024, ADR-029, ADR-030, ADR-033.

### Adendo em ADR existente quando **todas** abaixo aplicam

1. **Decisão central intacta** — só refina mecânica, ajusta threshold, formaliza pattern emergente que o ADR antecipou.
2. **Sem nova categoria** — ainda dentro do escopo conceitual original.
3. **Sem restrição externa nova** — refinamento interno editorial.
4. **Caráter explicativo, não decisório** — adendo só "anota" o que mudou desde o ADR; decisão de mudar mora em outro lugar (geralmente em sucessor parcial mais recente — ADR-001 Addendum 2026-05-12 cita ADR-024 como decisão; o adendo só faz a cross-ref).

### Localização do adendo

Adendo em ADR Aceito aparece em uma de quatro formas observadas no toolkit:

- **Seção `## Addendum (YYYY-MM-DD)`** ao final do ADR — pattern usado em ADR-001 (cross-refs a ADR-024 e ADR-033). Forma preferida quando o adendo é cross-ref para sucessor parcial mais recente sem amarração sintática a seção específica.
- **Parágrafo cross-ref inline em `## Decisão` ou `### Limitações`** (ex.: `Refinado por ADR-NNN: ...`, `Estendido por ADR-NNN: ...`) — pattern usado em ADR-005 § Limitações (cross-ref a ADR-025) e ADR-011 § Decisão (cross-ref a ADR-026). Forma preferida quando o adendo é continuação semântica daquela seção específica (item de decisão ou limitação) e precisa amarrar-se sintaticamente ao texto original.
- **Bullet em `### Implementação`** quando o adendo lista commits implementadores (útil em modo `local` ou tracking explícito).
- **Bullet em `### Limitações`** (sem prefixo `Refinado por`/`Estendido por`) quando o adendo registra escopo descoberto pós-fato como limitação nova, não como cross-ref a sucessor.

## Consequências

### Benefícios

- Critério mecânico explícito reduz decisão ad hoc; `design-reviewer` audita uniforme.
- Pattern "sucessor parcial + Addendum cross-ref no ancestral" — emergente em uso desde ADR-024 — fica explicitamente formalizado.
- Cadeias temáticas (design-reviewer, modo local, cutucada) recebem rationale posterior: não foram acidente, foram aplicação consistente do critério (cada refinamento mudava estrutura, contradizia ou estendia).

### Trade-offs

- Mais 1 ADR no inventário (34 total). Mitigação: meta-doutrina escopo restrito a 1 critério; baixo custo de manutenção.
- Critério tem zona cinzenta em "muda decisão estrutural" vs "refina mecânica" — borderline cases ficam para `design-reviewer` julgar. Mitigação: 4 ADRs canonical (ADR-024/-029/-030/-033) ancoram o lado "novo ADR sucessor"; 2 Addenda em ADR-001 ancoram o lado "adendo cross-ref". Próximo borderline tem benchmark dual.

### Auto-aplicação coerente

ADR-034 é ele próprio refinamento doutrinal — codifica regra que vivia implícita. Pelo critério (5) "sucessor parcial" da convenção emergente (refinamento de regra implícita não-escrita), novo ADR é o caminho correto. Critério (4) **não** aplica — ADR-034 não estabelece categoria conceitual nova de artefato, apenas formaliza critério editorial paralelo a outras meta-doutrinas (ADR-010, ADR-011, ADR-023, ADR-026). Auto-consistente.

## Implementação

- `CLAUDE.md` § "Editing conventions" ganha bullet cross-ref a este ADR (paralelo aos bullets de ADR-010, ADR-011, ADR-023, ADR-026): texto literal sugerido — "**Adendo vs novo ADR para refinamento doutrinal**: critério mecânico em [ADR-034](docs/decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) — novo ADR quando muda decisão estrutural, contradiz ADR anterior, codifica restrição externa, introduz categoria nova, ou é sucessor parcial; adendo quando todas: decisão central intacta + sem nova categoria + sem restrição externa + caráter explicativo."

## Alternativas consideradas

### (b) Só CLAUDE.md prosa, sem ADR

Registrar o critério apenas como bullet em CLAUDE.md § "Editing conventions" sem novo ADR. Mais conciso, evita 1 ADR.

Descartada porque memory "Limiar de ADR para mudanças em doutrina" estabelece default ADR para refinamentos doutrinais. CLAUDE.md prose sem ADR perde a estrutura de Origem/Contexto/Alternativas/Gatilhos que justifica e audita a decisão. Pattern paralelo a ADR-010 (instrumentação Tasks), ADR-011 (wiring design-reviewer), ADR-023 (disable-model-invocation), ADR-026 (absorpção findings) — todos meta-doutrinas em ADRs com CLAUDE.md bullets cross-ref. Manter consistência.

## Gatilhos de revisão

- **5º caso borderline** que `design-reviewer` julgou ad hoc sem critério mecânico bater claramente — sinal de que o critério precisa refinar (categoria adicional ou threshold a alterar).
- **Convenção do "sucessor parcial"** mudar (ex.: passar a usar `Substituído` para todo sucessor parcial em vez de só revogar) — reabre § Localização do adendo.
- **Novo tipo de adendo** emergir (ex.: tabela retroativa de aplicação cross-ADR; ledger de gatilhos de revisão acionados) — pode adicionar 5ª forma em § Localização do adendo.
- **5ª meta-doutrina** propondo bullet em CLAUDE.md § "Editing conventions" — empurra cap nominal de 200 linhas (ADR-024 § Alternativas estabeleceu o cap). Reabre critério "meta-doutrina ganha bullet em CLAUDE.md vs índice consolidado em `docs/decisions/README.md`".
