# ADR-033: templates/ admite single-consumer quando artefato é declarativo (esqueleto preenchível)

**Data:** 2026-05-16
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-001](ADR-001-protocolo-de-templates.md) § Decisão linha 33 deixou explícito "por ora" que o ADR template ficaria inline em `/new-adr` (single-consumer + "sem ganho imediato em extrair"). Esse "por ora" nunca foi convertido em critério escrito; na prática, virou regra implícita "single-consumer → inline" para a próxima extração.
- **Decisão precedente:** [ADR-027](ADR-027-skill-draft-idea-elicitacao-product-direction.md) adicionou `templates/IDEA.md` consumido apenas por `/draft-idea` — primeira ocorrência de template centralizado com 1 único consumidor.
- **Investigação:** Auditoria 2026-05-15 (D_arch) sinalizou tensão: ADR-027 atualizou esse "por ora" de ADR-001 sem reabrir o critério. Bifurcação editorial: (a) novo ADR sucessor codificando o critério relaxado; (b) mover `templates/IDEA.md` collocated preservando ADR-001 original; (c) adendo direto em ADR-001 Aceito (taboo). Operador escolheu (a) via cutucada do `/triage` 2026-05-16. § Alternativas detalha por que (b) e (c) foram descartadas; (a) é materializada por este ADR.

## Contexto

A pasta `templates/` na raiz do plugin foi estabelecida em ADR-001 como single source of truth para esqueletos canônicos de artefatos consumidos por múltiplas skills. ADR-001 § Decisão linha 33 deixou o caso ADR template "por ora" inline (single-consumer + "sem ganho imediato em extrair"); sem promoção para critério escrito, virou regra implícita.

`/draft-idea` (ADR-027) adicionou `templates/IDEA.md` com 1 único consumidor, materializando uma classe de templates que **não cabe** na regra single-consumer-inline: o template IDEA.md é um **esqueleto preenchível** (fill-in skeleton com seções placeholder + comentários HTML descritivos), distinto do template ADR de `/new-adr` que é um **manual de instruções entrelaçado com prosa da skill**.

A distinção é qualitativamente real:

- **Template inline-prose (ADR em `/new-adr`):** SKILL.md ensina como compor o ADR e carrega o esqueleto entrelaçado com a prosa de instruções. Separar do SKILL.md fragmenta a leitura sem ganho — o template é tutorial.
- **Template declarativo (IDEA.md, plan.md):** é dado que a skill processa via `Read`; benefício direto de centralização — operador edita o template para revisar estrutura sem mexer no SKILL.md; revisões podem propagar para múltiplas invocações sem patches de prosa.

Sem critério explícito, o próximo template declarativo single-consumer recairia na mesma ambiguidade.

## Decisão

**Estender o critério de ADR-001 § Decisão para incluir o caso single-consumer + artefato declarativo:** `templates/` é o destino canonical quando o artefato é um esqueleto preenchível (fill-in skeleton) processado via `Read` pela skill, **mesmo com apenas 1 consumidor**. Single-consumer + template inline-prose (tutorial entrelaçado) permanece em SKILL.md.

Razões objetivas:

- **Separação dados vs lógica:** esqueleto preenchível é dado; instruções de como compor são lógica. Mistura cabe quando o template é tutorial (inline); separação cabe quando o template é dado processado.
- **Editabilidade manual:** template declarativo pode ser revisado por humano sem tocar SKILL.md — função importante quando a estrutura evolui editorialmente (ADR-001 já antecipa o benefício para multi-consumer; ADR-033 reconhece que vale também single-consumer).
- **Extensibilidade:** próximo template declarativo (de check, release notes preenchível, etc.) cai naturalmente em `templates/` sem reabrir ambiguidade.

### Critério mecânico

Template em `templates/` quando **qualquer** das duas condições aplicar:

1. **Consumidor múltiplo (≥2 skills)** — critério original de ADR-001 preservado.
2. **Consumidor único + artefato declarativo** (fill-in skeleton processado via `Read`) — critério novo deste ADR.

Template inline (em SKILL.md) quando único consumidor **E** template é tutorial entrelaçado com instruções da skill (ex.: ADR em `/new-adr` — o SKILL.md ensina + carrega o esqueleto numa só prosa).

**Testes mecânicos para casos de fronteira** (quando a classificação "declarativo vs inline-prose" for ambígua, perguntar):

- **Skill faz `Read` do arquivo em runtime e injeta no fluxo?** Sim → declarativo. Não (skill carrega a estrutura inline em prosa) → inline-prose.
- **Editar o arquivo isoladamente faz sentido sem editar SKILL.md?** Sim → declarativo. Não (instruções referenciam o esqueleto entrelaçado) → inline-prose.

Resposta "sim" para ambos confirma declarativo; "não" para ambos confirma inline-prose; resposta dividida → cutucar `design-reviewer` ou humano para auditar caso a caso (gatilho de revisão #1 do próprio ADR antecipa essa fronteira).

### Invariante de implementação

Implementação deste ADR deve adicionar adendo informativo em ADR-001 (após o Addendum 2026-05-12 que aponta para ADR-024) apontando para ADR-033 como sucessor parcial que estende o critério para single-consumer declarativo. Pattern paralelo ao de ADR-024 — preserva discoverability quando leitor entra por ADR-001.

## Consequências

### Benefícios

- ADR-001 ganha sucessor parcial sem mutação do ADR Aceito (preserva convenção de immutability).
- Critério mecânico explícito para próximas skills geradoras com template.
- ADR-027 (templates/IDEA.md) fica justificado retroativamente — não mais contradição implícita.

### Trade-offs

- Mais 1 ADR no inventário. Mitigação: ADR-033 é sucessor parcial específico, não duplica conteúdo de ADR-001.
- Critério depende de classificação subjetiva ("declarativo vs inline-prose"). Mitigação: dois exemplos canonical (plan.md/IDEA.md = declarativo; ADR em /new-adr = inline) ancoram a categorização; revisor (`design-reviewer` ou humano) audita casos de fronteira.

## Alternativas consideradas

### (b) Mover `templates/IDEA.md` para `skills/draft-idea/template.md`

Preserva ADR-001 escopo original; `templates/` retém apenas plan.md (multi-consumer). Pattern implícito emergente: "`templates/` para multi-consumer, collocated para single-consumer".

Descartada porque cria policy implícita split entre dois locais para templates similares, dependendo apenas do count de consumidores — quando o consumidor crescer para 2+ (e.g., outra skill começar a ler IDEA.md), o template precisaria voltar para `templates/`. Move-volta-move é churn editorial sem ganho semântico.

### (c) Adendo direto em ADR-001 § Decisão

Mais conciso (1 ADR vs 2). Mas viola convenção de immutability de ADRs Aceitos. E_arch (item gêmeo na Onda 5) discutirá em sucessor próprio quando adendo é aceitável; D_arch resolveu por default ADR per memory "Limiar de ADR para mudanças em doutrina".

## Gatilhos de revisão

- **3º template declarativo single-consumer** emergir e revelar que o critério "declarativo" não disambigua suficientemente — pode precisar refinamento ou collocated-as-default.
- **Próxima skill geradora** que produza template **inline-prose** single-consumer — confirma a outra fronteira do critério.
- **Caso "múltiplos consumidores + template inline-prose"** emergir (não-instanciado hoje) — abre questão não coberta por ADR-033; possivelmente refinar critério mecânico.
- **E_arch shipped pós-Aceito de ADR-033** redefinindo quando adendo é aceitável → reabre D_arch para considerar consolidação em ADR-001 em vez de manter 2 ADRs. Decisão de ordem de shipping é independente (per encaminhamento do roadmap "não bundle entre si — eixos doutrinários distintos").
