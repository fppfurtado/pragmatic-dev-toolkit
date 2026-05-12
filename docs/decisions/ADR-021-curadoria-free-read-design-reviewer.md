# ADR-021: Curadoria do free-read do design-reviewer (anotação + scan)

**Data:** 2026-05-12
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-009](ADR-009-revisor-design-pre-fato.md) — estabeleceu free-read de doctrine sources (`docs/decisions/*.md` + `docs/philosophy.md`) no design-reviewer. Gatilho § "Gatilhos de revisão" #2: *"Volume de ADRs ultrapassa ~30 → free-read passa a ser custoso mesmo em uso manual; reabrir para considerar curadoria semi-automática (e.g., reviewer pré-filtra ADRs por keyword no plano antes de ler)."*
- **Decisão base:** [ADR-011](ADR-011-wiring-design-reviewer-automatico.md) — wiring automático em `/triage` (plano-producing) e `/new-adr`. Gatilho § "Gatilhos de revisão" #2 cita o mesmo limiar de ~30 ADRs.
- **Investigação:** Auditoria arquitetural 2026-05-12 (`docs/audits/runs/2026-05-12-architecture-logic.md`, achado E1 + proposta B_arch). Hoje 20 ADRs (após ADR-020); ritmo recente (~19 ADRs em 6 dias) sugere atingir 30 em ~1-2 semanas. Reabertura **preventiva** evita o cenário "reviewer caro mesmo em invocação média".

## Contexto

ADR-009 estabeleceu free-read de `docs/decisions/*.md` + `docs/philosophy.md` no design-reviewer como mecanismo para detectar contradição doutrinária sem ônus de curadoria pelo autor do plano. ADR-011 fixou wiring automático em 2 pontos (`/triage` plano-producing + `/new-adr`).

Custo de tokens cresce O(#ADRs). Estimativa ADR-011: ~12k tokens por invocação com inventário atual (~10 ADRs no momento da estimativa). Com 20 ADRs hoje o número escalou; com 30, ~18k+; com 50, ~30k+ — ainda viável tecnicamente, mas erode margem em invocações frequentes.

**Pontos cegos a respeitar** quando se introduz curadoria:

- **Operador não sabe o que está contradizendo** (ADR-009 § Contexto, motivação central do free-read). Curadoria 100% dependente do autor reabriria esse ponto cego.
- **Scan automatizado tem false negative.** Filtrar por keyword pode pular ADR doutrinariamente crítico mas lexicalmente distante do plano.
- **Doutrina não-escrita escapa** (ADR-009 § Limitações). Curadoria não conserta isso; só reduz ônus do free-read.

**Convergência conceitual parcial:** o plugin já tem pipeline análogo de **anotação manual** para vocabulário ubíquo — operador anota `**Termos ubíquos tocados:**` no plano via `/triage`, `/run-plan` repassa ao reviewer, `code-reviewer` valida no diff (`docs/philosophy.md` → "Linguagem ubíqua na implementação"; pipeline canonical). ADR-021 replica a forma da anotação manual mas **acrescenta** scan automático sobre os ADRs não-anotados — assimetria necessária porque o ponto cego doutrinário (ADR-009 § Contexto: *"autor não sabe o que está contradizendo"*) impede anotação-only. O paralelo cobre só a primeira metade da decisão.

## Decisão

**Free-read do design-reviewer passa a operar em modo híbrido: operador anota `**ADRs candidatos:**` no `## Contexto` do plano (opcional) + reviewer faz scan por keyword dos demais ADRs. Threshold abaixo de N preserva free-read completo (mecanismo dorme quando volume não justifica overhead).**

### Mecânica

#### 1. Anotação opcional no `## Contexto` do plano

`/triage` step 4 sugere ao operador listar `**ADRs candidatos:**` no `## Contexto` se identificar ADRs concretos tocados/contradictados pela mudança. Formato:

```markdown
**ADRs candidatos:** ADR-NNN (motivo curto), ADR-MMM (motivo curto)
```

Campo opcional. Operador que não sabe quais ADRs aplicam **simplesmente omite**; scan cobre.

Pattern paralelo a `**Termos ubíquos tocados:**`: operador cura o que sabe; reviewer scan cobre o que operador não sabe. Convergência conceitual codificada.

#### 2. Scan por keyword nos ADRs não-anotados

design-reviewer, ao receber plano ou ADR draft, executa:

1. **Lê anotação** `**ADRs candidatos:**` se presente — esses ADRs entram no input integral (free-read completo).
2. **Extrai keywords** do plano/draft:
   - Plano: tokens significativos do `## Contexto` + `## Resumo da mudança` (não stop-words).
   - ADR draft: tokens significativos da `## Origem` + `## Decisão`.
3. **Para cada ADR não-anotado** em `docs/decisions/*.md`:
   - Lê **apenas o cabeçalho** (título + frontmatter + `## Origem` + `## Decisão`; ~10-20 linhas).
   - Verifica match de keyword no cabeçalho.
   - **Match** → ADR entra no input integral (free-read completo).
   - **Sem match** → ADR é descartado do contexto do reviewer.
4. **`docs/philosophy.md`** continua sendo free-read integral (volume pequeno, doutrina-base cross-cutting).

#### 3. Threshold de ativação

`#ADRs total ≤ N` → mecanismo de scan **desliga**; reviewer faz free-read completo como ADR-009 original. Mecanismo só ativa quando volume justifica o trade-off.

**N candidato: 15.** Calibração heurística — abaixo de 15 ADRs, free-read completo é barato e curadoria semi-automática é overhead injustificado. Plugin meta-toolkit (20 ADRs hoje) ativa; consumer externo com inventário menor não paga complexidade. Ajustável via gatilho de revisão.

### Pontos cegos cobertos vs não-cobertos

| Ponto cego | Cobertura sob ADR-021 |
|---|---|
| Operador não sabe o que contradiz | ✓ scan dos não-anotados cobre |
| Scan false negative (ADR doutrinariamente relevante mas lexicalmente distante) | △ reduzido por (i) anotação manual quando operador sabe; (ii) keywords extraídas de `## Origem` + `## Decisão` — ricos em vocabulário doutrinário, não só do título |
| Doutrina não-escrita escapa | ✗ herda limitação de ADR-009 — ortogonal a este ADR |
| Operador anota ADR irrelevante | ✓ reviewer lê integralmente mesmo sem match de keyword no plano — custo é só de tokens, não de cobertura |
| Operador omite ADR óbvio | ✓ scan cobre se há match de keyword; ✗ se ADR for lexicalmente distante |

## Consequências

### Benefícios

- **Custo de tokens cresce sub-linearmente** com #ADRs além do threshold. Mecanismo escala.
- **Pattern reutilizável.** `**ADRs candidatos:**` paralelo a `**Termos ubíquos tocados:**` consolida convenção "operador anota o que sabe; reviewer scan cobre o resto" em segundo eixo.
- **Threshold preserva comportamento original** em projetos com poucos ADRs; consumer externo provavelmente cai aí. Plugin meta-toolkit (≥15) ativa o mecanismo.
- **Anotação manual valida implicitamente o trabalho do operador.** Refletir sobre quais ADRs aplicam é exercício útil de alinhamento.

### Trade-offs

- **Regresso parcial do ponto cego que ADR-009 evitava.** Free-read integral garantia cobertura mesmo para ADR doutrinariamente relevante mas lexicalmente distante do plano. ADR-021 reduz essa cobertura quando #ADRs > N: scan pode pular ADR que operador esqueceu de anotar (porque não sabia que aplicava — exatamente o ponto cego de ADR-009 § Contexto). **Trade-off principal aceito:** regresso parcial em troca de sub-linearidade de custo. Mitigações: (i) anotação manual cobre o caso onde operador sabe; (ii) `philosophy.md` (free-read sempre) carrega doutrina cross-cutting; (iii) gatilho de revisão #1 (scan reporta zero matches em invocação onde operador percebe omissão) detecta incidentes pós-fato.
- **Calibração de N=15 não tem observabilidade direta.** Depende de operador reportar findings perdidos por scan ou tokens excessivos por free-read prematuramente desativado — trilho frágil. Alternativa (medir tokens por invocação ou contar findings com auto-validação) introduz instrumentação não-existente hoje. Aceito; gatilho de revisão sobre N=15 mal-calibrado registra o sinal sem automatizar.
- **Complexidade nova no agent.** Reviewer ganha lógica de extração de keyword + scan de cabeçalho + decisão de threshold. **Mecânica do scan é editorial** — stop-word list, regra de match (substring vs stemming vs token), threshold mínimo de keywords matching, tamanho efetivo do "cabeçalho lido" não estão cristalizados nesta prosa. Primeira iteração de implementação no `design-reviewer` registra a escolha; refinamento iterativo previsto. Aceito como gap intencional — calibrar antes do uso real é overfitting.
- **Operador novo (consumer externo)** pode não saber do campo `**ADRs candidatos:**`. Mitigação: `/triage` step 4 sugere quando aplicável; template `plan.md` carrega placeholder + comentário explicativo análogo ao de `**Termos ubíquos tocados:**`.
- **Tokens economizados são marginais para plano único** (ADR cabeçalho lido mesmo em sem-match custa alguns tokens). Ganho concreto vem do conjunto: 20+ ADRs com filtragem reduz pesadamente vs free-read integral.

### Limitações

- ADR cobre apenas o `design-reviewer` lendo `docs/decisions/`. `docs/philosophy.md` continua sempre lido integralmente — volume pequeno (77 linhas hoje); revisitar se dobrar.
- Curadoria não conserta "doutrina não-escrita escapa" (ADR-009 § Limitações). Mecanismo ortogonal.
- Não cobre outras superfícies de free-read (hipotéticas: reviewers que lessem `docs/plans/` históricos). Single data point hoje.
- Heurística de extração de keyword não está cristalizada na prosa do agent — depende de calibração editorial. Refinamento iterativo previsto.

## Alternativas consideradas

### (b1) Scan only

Reviewer faz scan por keyword sem anotação manual.

Descartada:
- Reabre o ponto cego "operador não sabe" só parcialmente (scan cobre lexicalmente; doutrinariamente cego se ADR não compartilha keyword com plano).
- Sem fallback para operador que **sabe** que um ADR aplica mas scan não acha (false negative sem escape hatch).

### (b2) Anotação only

Operador anota `**ADRs candidatos:**`; reviewer lê só os anotados (mais `philosophy.md`).

Descartada:
- Reabre exatamente o ponto cego que ADR-009 evitava: *"Pedir ao autor 'liste os ADRs que seu plano contradiz' é circular: o autor não sabe o que está contradizendo (esse é exatamente o ponto cego)."*

### (b3) Subdiretórios por eixo em `docs/decisions/`

Reorganizar fisicamente os ADRs em subdiretórios (workflow/, idioma/, hooks/, ...); reviewer lê só o subdiretório relevante ao plano.

Descartada:
- **Migração custosa.** 20 ADRs com cross-refs em prosa precisariam ser atualizados (links relativos quebram).
- **Eixo errado é ADR órfão.** ADRs frequentemente tocam múltiplos eixos (ADR-011 = workflow + reviewer + token-budget; ADR-019 = reviewer + skill geradora). Categorização forçada perde decisão estrutural.
- **Skill `/new-adr` ganha decisão extra** (escolher eixo) a cada invocação. Acoplamento ao layout.
- **Path contract não cobre subdiretórios.** Convenção `decisions_dir` é diretório plano hoje; mudar quebra documentação + skills.

### (c) Manter status quo até o gatilho disparar

Free-read integral até atingir o gatilho ≥30 e reabrir reativamente.

Descartada:
- Ritmo recente (~19 ADRs/6 dias) sugere atingir 30 em ~1-2 semanas. Decidir sob pressão de gatilho disparado tende a soluções frágeis. Preempção é o ponto da proposta B_arch.

### (d) Threshold puro sem scan/anotação

Free-read completo até N; pausar wiring acima de N.

Descartada:
- Volta o ônus à manual (operador `@-mention` para invocar). Inverte ADR-011 (wiring automático) sem decidir o mecanismo de curadoria que justificou esta reabertura.

### (e) Lista always-include de ADRs doutrina-base

Marcação editorial de subconjunto de ADRs como "doutrina-base sempre-lida" (paralelo a `philosophy.md` integral). Reviewer leria sempre esse conjunto + scan opcional sobre os demais.

Descartada **nesta iteração**:
- **Curadoria editorial não-trivial.** Identificar o subconjunto exige decisão estrutural separada (qual ADR é "doutrina-base"? ADR-002, ADR-004, ADR-008, ADR-009 são candidatos óbvios; mas ADR-006, ADR-011, ADR-019 também tocam cross-cutting). ADR-021 não quer carregar essa decisão; preferiu mecanismo orgânico (operador anota o que reconhece como aplicável).
- **Mecanismo pode emergir via gatilho de revisão.** O gatilho *"Operador anota sistematicamente os mesmos ADRs em planos diferentes — sinal de que esses ADRs viraram doutrina-base; promover para inclusão automática sempre-lida"* antecipa essa promoção. Esperar o sinal empírico é mais conservativo que decidir o subconjunto agora.
- **Não anula necessidade de scan.** Mesmo com lista always-include, o scan dos demais continuaria necessário para cobrir o ponto cego ADR-009 § Contexto. (e) é **complemento futuro**, não alternativa concorrente — pode coexistir com ADR-021 se vier.

## Gatilhos de revisão

- **Scan reporta zero matches** em invocação onde operador percebe que ADR não-anotado deveria ter aparecido — false negative concreto. Refinar heurística de keyword (e.g., incluir § Decisão + § Consequências no scan target em vez de só § Origem).
- **Operador anota sistematicamente os mesmos ADRs em planos diferentes** — sinal de que esses ADRs viraram doutrina-base; promover para inclusão automática sempre-lida (paralelo a `philosophy.md` integral).
- **Threshold N=15 mal-calibrado** (mecanismo ativa cedo demais ou tarde demais) — ajustar com base em observação.
- **Reviewer reporta inconsistência entre subset lido e ADR não-lido** (auto-validação rara mas possível) — confirma necessidade de safety net (talvez sempre incluir ADRs cujo título contém termos genéricos como "doutrina", "pipeline", "convenção").
- **Próximo refactor sweep grande** (similar ao de 2026-05-06 → 12) — observar como o mecanismo se comporta sob carga de adições rápidas; cada novo ADR muda o universo de scan.
- **Consumer externo reporta confusão sobre `**ADRs candidatos:**`** — campo mal documentado ou redundante para projetos pequenos. Refinar critério de quando `/triage` sugere o campo.
- **Volume de `docs/philosophy.md` dobra** (de ~77 para ~150 linhas) — revisitar a exceção que mantém philosophy.md em free-read sempre.

## Implementação prevista

Materialização editorial deste ADR exige 3 arquivos:

- `agents/design-reviewer.md` — adicionar seção "Curadoria do free-read" descrevendo (i) leitura de `**ADRs candidatos:**` integral; (ii) scan por keyword nos demais (mecânica concreta cristalizada na primeira iteração); (iii) threshold N=15; (iv) `philosophy.md` sempre integral.
- `skills/triage/SKILL.md` step 4 — sugerir `**ADRs candidatos:**` no `## Contexto` do plano quando aplicável (paralelo à sugestão atual de `**Termos ubíquos tocados:**`).
- `templates/plan.md` — placeholder + comentário explicativo análogo ao de `**Termos ubíquos tocados:**`.

Plano de implementação produzido no fluxo `/triage` que originou este ADR; ver `docs/plans/curadoria-free-read-design-reviewer.md`.
