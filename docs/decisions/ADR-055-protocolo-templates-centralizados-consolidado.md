# ADR-055: Protocolo de templates centralizados (consolidado)

**Data:** 2026-06-01
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-001](archive/ADR-001-protocolo-de-templates.md) (foundational — protocolo de templates centralizados; archived na Onda M consolidado nesta § Decisão) + [ADR-033](archive/ADR-033-templates-admite-single-consumer-declarativo.md) (sucessor parcial primário de ADR-001 estendendo critério single-consumer-declarativo; archived na Onda M consolidado nesta § Decisão). Sucessor consolidando per [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 5 primária isolada.
- **Investigação:** Charter `docs/plans/redesign-camada-doutrinal-charter.md` § Atualização pós-execução tabela linha 192 ("Onda M opcional — Cluster foundational templates") materializada como migração cluster genuína via /triage 2026-06-01. Família semântica clara ADR-001↔ADR-033 codificada via sucessor parcial (ADR-033 § Origem citava ADR-001 § Decisão linha 33; ADR-033 § Invariante implementação cumprida via ADR-001 Addendum 2026-05-16).
- **Plano coordenador:** `docs/plans/onda-m-foundational-templates.md` materializa decomposição operacional desta § Decisão.
- **Pattern de migração:** 8 ondas precedentes (C+D+E+F+G+H+I+J) validaram pattern de absorção cluster sob hierarquia invertida per [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 1 § Implementação literal; ADR-055 é 9ª migração cluster + 11ª ADR consolidado da redesign (incluindo [ADR-052](ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md) meta-pattern editorial não-cluster).

## Contexto

A pasta `templates/` na raiz do plugin é destino canonical para esqueletos de artefatos consumidos por skills. ADR-001 estabeleceu o protocolo com escopo inicial `templates/plan.md` (consumido por /triage + /run-plan); ADR-033 estendeu critério para single-consumer + artefato declarativo (`templates/IDEA.md` consumido apenas por /draft-idea). A relação sucessor-parcial criou família semântica clara entre os 2 ADRs:

- ADR-033 § Origem citava ADR-001 § Decisão linha 33 ("ADR template fica inline em /new-adr por ora — single consumer, sem ganho imediato em extrair") como decisão base.
- ADR-001 Addendum 2026-05-16 citava ADR-033 como sucessor parcial estendendo critério (invariante implementação de ADR-033 § cumprida explicitamente).
- [ADR-051](ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c) (categoria `docs/procedures/` paralela) cita autoridade vigente da categoria `templates/`; invariante de cross-ref bilateral ADR-055↔ADR-051 substituindo ADR-001↔ADR-051 preservada anti-regression checklist (charter linhas 245-247).

Onda M (per charter § Cap de ondas linha 152 + § Atualização pós-execução linha 192) é cluster minúsculo (2 ADRs); consolidação genuína cabe sob ADR-045 hierarquia invertida + filtro de admissão. Sub-3c "standalone por unicidade categórica" NÃO aplica (família plausível existe ENTRE ADR-001 e ADR-033 via sucessor parcial codificada); contador sub-3c permanece 2/3 paralelo a Onda L; gatilho refinamento ADR-052 § Gatilhos linha 187 aguarda 3ª aplicação genuína futura.

## Decisão

Estabelecer pasta `templates/` na raiz do plugin como **single source of truth para esqueletos canônicos** de artefatos consumidos por skills, com critério mecânico cumulativo para admissão.

### (a) Protocolo de templates centralizados (originalmente ADR-001 § Decisão)

Skills leem o template em runtime via `${CLAUDE_PLUGIN_ROOT}/templates/<artifact>.md` quando precisam compor ou validar o artefato. **Mecânica: `Read` em runtime, não embed/copy.** Embed reintroduz duplicação.

Razões objetivas:

- **DRY operacional**: editar a estrutura em um lugar; skills consumidoras refletem automaticamente.
- **Skills enxutas**: prosa de estrutura sai dos SKILL.md; cada skill descreve seu papel sobre o template, não duplica o template.
- **Padrão extensível**: futuros artefatos com estrutura compartilhada (templates de check, release notes, etc.) seguem o mesmo protocolo sem nova decisão.

**Fronteira `templates/` vs `docs/procedures/`** (originalmente ADR-001 Addendum 2026-05-12 + [ADR-024](archive/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md) archived; substância preservada via ADR-051 § Decisão (c) categoria paralela):

- `templates/` = esqueletos preenchidos quando o artefato é produzido. Skills consomem via `Read` e preenchem placeholders ao produzir o artefato. Exemplo: `templates/plan.md` lido por /triage ao criar plano novo.
- `docs/procedures/` = procedimentos executados quando referenciados. Skills consomem via `Read` e executam o algoritmo descrito. Exemplo: `docs/procedures/forge-auto-detect.md` lido por /run-plan ao decidir CLI de forge.

Distinção semântica nítida: **esqueletos vs algoritmos**. Categorias paralelas com fronteira mecânica.

### (b) Critério mecânico cumulativo (originalmente ADR-033 § Decisão)

Template em `templates/` quando **qualquer** das duas condições aplicar:

1. **Consumidor múltiplo (≥2 skills)** — critério foundational de ADR-001 preservado.
2. **Consumidor único + artefato declarativo** (fill-in skeleton processado via `Read`) — critério estendido de ADR-033.

Template inline (em SKILL.md) quando único consumidor **E** template é tutorial entrelaçado com instruções da skill (ex.: ADR template em /new-adr — o SKILL.md ensina + carrega o esqueleto numa só prosa).

**Razões objetivas:**

- **Separação dados vs lógica:** esqueleto preenchível é dado; instruções de como compor são lógica. Mistura cabe quando o template é tutorial (inline); separação cabe quando o template é dado processado.
- **Editabilidade manual:** template declarativo pode ser revisado por humano sem tocar SKILL.md — função importante quando a estrutura evolui editorialmente.
- **Extensibilidade:** próximo template declarativo (de check, release notes preenchível, etc.) cai naturalmente em `templates/` sem reabrir ambiguidade.

### Testes mecânicos para casos de fronteira

Quando a classificação "declarativo vs inline-prose" for ambígua, perguntar:

- **Skill faz `Read` do arquivo em runtime e injeta no fluxo?** Sim → declarativo. Não (skill carrega a estrutura inline em prosa) → inline-prose.
- **Editar o arquivo isoladamente faz sentido sem editar SKILL.md?** Sim → declarativo. Não (instruções referenciam o esqueleto entrelaçado) → inline-prose.

Resposta "sim" para ambos confirma declarativo; "não" para ambos confirma inline-prose; resposta dividida → cutucar `design-reviewer` ou humano para auditar caso a caso (gatilho de revisão #3 abaixo antecipa essa fronteira).

### Exemplos canonical

- **`templates/plan.md`** — multi-consumer (≥2 skills: /triage + /run-plan). Cabe em (b) bullet 1. Esqueleto preenchível.
- **`templates/IDEA.md`** — single-consumer (/draft-idea). Cabe em (b) bullet 2. Esqueleto preenchível processado via `Read`.
- **ADR template em /new-adr SKILL.md** — single-consumer + inline-prose tutorial. Permanece em SKILL.md (não em `templates/`).

## Consequências

### Benefícios

- Skills enxutas com prosa de estrutura externalizada para `templates/`.
- Drift entre /triage e /run-plan sobre estrutura do plano eliminado (`Read` em runtime).
- Critério mecânico cumulativo claro para próximas skills geradoras com template.
- Operador externo abrindo plugin tem `templates/` como referência canônica de "como o artefato se parece" — facilita autoria manual.
- ADR-027 (templates/IDEA.md) justificado retroativamente sem contradição implícita (originalmente resolvido via ADR-033; preservado em ADR-055 § Decisão (b) bullet 2).

### Trade-offs

- Skills dependem de `Read` runtime no path `${CLAUDE_PLUGIN_ROOT}/templates/<artifact>.md`. Se file não existir (cache corrompido, instalação parcial), skill falha ao compor artefato.
- Idioma do template é PT-BR canonical (origem do toolkit). Skills adaptam headers ao idioma do projeto consumidor (per `docs/philosophy.md` → Convenção de idioma) — adaptação na skill, não no template. Template é mecânica do toolkit; idioma fica canonical.
- Critério depende de classificação subjetiva ("declarativo vs inline-prose"). Mitigação: dois exemplos canonical (`plan.md`/`IDEA.md` = declarativo; ADR template em /new-adr = inline) ancoram a categorização; revisor (`design-reviewer` ou humano) audita casos de fronteira.

### Limitações

- ADR template não migra (mantém escopo de single-consumer + inline-prose tutorial em /new-adr SKILL.md). Decisão futura, sob este protocolo, pode estender se ADR template emergir como artefato declarativo separado.
- Critério "`templates/` vs inline" não cobre o caso "múltiplos consumidores + template inline-prose" (não-instanciado hoje). Gatilho de revisão registra para refinamento se emergir.

### Mitigações

- Cross-ref bilateral ADR-055↔ADR-051 substituindo ADR-001↔ADR-051 preserva anti-regression checklist charter linhas 245-247 (invariante de cross-ref bilateral entre categorias `templates/` e `docs/procedures/`).
- ADRs vigentes citando ADR-001/ADR-033 (ADR-003, ADR-034, ADR-051) recebem atualização cross-ref preservando substância via body verbatim — pattern 8+ ondas estabelecido.
- ADR-035 linha 84 (referência histórica "Padrão recente (ADR-033, ADR-034) shippou ADR + bullet CLAUDE.md sem tocar philosophy.md") preservada in-place per ADR-045 § Decisão parte 1 (ADR Substituído imutável referencia state da época) — operador vê redirect canonical via archive/.

## Alternativas consideradas

### (b) Preservar ambos standalone via sub-3c (modo emergente Promoção II + Onda L)

Sub-3c "standalone por unicidade categórica" exige "categoria solo sem família plausível no toolkit". ADR-001 e ADR-033 têm família ENTRE SI codificada via sucessor parcial (ADR-033 § Origem citava ADR-001 § Decisão linha 33; ADR-001 Addendum 2026-05-16 citava ADR-033). Forçar sub-3c contradiria o próprio critério (categoria solo); seria leitura desonesta paralela ao caminho A rejeitado na Onda L. Descartada por construção; contador sub-3c permanece 2/3 paralelo a Onda L.

### (c) Split arbitrário (1 standalone + 1 absorvido)

Move o problema sem resolvê-lo. Relação sucessor-parcial força família coesa por construção; não há justificativa para split.

### (d) Adendo direto em ADR-001 § Decisão estendendo critério single-consumer-declarativo inline

Mais conciso (1 ADR vs 2 → 1). Mas viola convenção de immutability de ADRs Aceitos. Originalmente discutido em ADR-033 § Alternativa (c) (adendo direto em ADR-001 era violação de immutability); ADR-034 cond 5 reconhece sucessor parcial como modalidade explícita do toolkit.

**Distinção categorial vs caminho A escolhido (consolidação):** ADR-001 e ADR-033 ficam **imutáveis** (archived intactos sob `docs/decisions/archive/`); ADR-055 é peça nova absorvendo a substância sem editar o body dos ADRs Aceitos. Caminho (d) editaria o body de ADR-001 in-place (adendo direto extendendo § Decisão), violando immutability. Caminho A respeita immutability via archive + redirect canonical (pattern Ondas C-J 8+ instâncias).

## Auto-aplicação per ADR-034

ADR-055 é refinamento doutrinal consolidatório — absorve substância de ADR-001 (foundational) + ADR-033 (sucessor parcial primário) em 1 consolidado preservando regra central + critério mecânico. Pela classificação editorial de ADR-034:

- **Cond 5 (sucessor parcial primário estendendo ADR Aceito sem revogar)**: aplica primária — estende ADR-001 protocolo templates centralizados absorvendo critério mecânico cumulativo de ADR-033 (extensão deste); regra central de ambos preservada literal (multi-consumer da ADR-001; single-consumer-declarativo da ADR-033 como bullet 2 do critério).
- **Cond 4 (categoria conceitual nova de artefato)**: **NÃO aplica** — categoria `templates/` foundational de ADR-001 absorvida intacta; ADR-055 não introduz categoria conceitual nova de artefato.
- **Cond 1 (decisão estrutural sem ancestral)**: **NÃO aplica** — ADR-001 + ADR-033 são ancestrais codificados diretos.
- **Cond 2 (substitui ADR ancestral invertendo decisão central)**: **NÃO aplica** — regra central de ADR-001 (protocolo templates centralizados) e ADR-033 (critério mecânico cumulativo) preservadas literal.
- **Cond 3 (codifica restrição externa de longa duração)**: **NÃO aplica** — refinamento editorial interno.

**Justificativa para novo ADR vs adendos cross-ref:** cond 5 primária isolada justifica novo ADR. Pattern editorial F4 Ondas C-J estabilizado em 8+ ondas precedentes — auto-aplicação coerente.

## Gatilhos de revisão

- **Pain reportado em manter ADR template inline em /new-adr** (drift detectado, edit fraturado, ou nova skill que precisa do mesmo template) → reabrir para estender o protocolo a `templates/adr.md` (gatilho original de ADR-001 preservado).
- **Caso "múltiplos consumidores + template inline-prose"** emergir (não-instanciado hoje) — abre questão não coberta por critério mecânico cumulativo; possivelmente refinar (gatilho original de ADR-033 preservado).
- **3º template declarativo single-consumer** emergir e revelar que o critério "declarativo" não disambigua suficientemente — pode precisar refinamento ou collocated-as-default (gatilho original de ADR-033 preservado).
- **Plugin ganha 3+ artefatos com estrutura compartilhada além de plano** → reabrir para considerar formato de manifesto (ex.: `templates/index.json` listando artefatos disponíveis) em vez de scan ad-hoc (gatilho original de ADR-001 preservado).
- **Mudança estrutural da regra de consolidação de ADR-045** — ADR-055 herda revisão proporcional se fronteira de ADR-045 § Decisão linha 56 mudar estruturalmente.
