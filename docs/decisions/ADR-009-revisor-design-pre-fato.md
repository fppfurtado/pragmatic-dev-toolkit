# ADR-009: Revisor design pré-fato e free-read de doctrine sources

**Data:** 2026-05-07
**Status:** Aceito

## Origem

- **Investigação:** /triage do agent `design-reviewer` (sessão pós-v1.24.0) levantou que todos os reviewers atuais (`code/qa/security/doc-reviewer`) operam em diff pós-fato e consomem insumo curado pelo autor do plano (e.g., `**Termos ubíquos tocados:**` repassado pelo /run-plan ao invocar `code-reviewer`). Adicionar revisor que critique decisões estruturais antes de virarem código exige formalizar a divergência do padrão atual.
- **Decisão base:** padrão de reviewers até v1.24.0 (`agents/code-reviewer.md` → "Insumo: Termos ubíquos tocados no ## Contexto do plano") fixa o modelo curado-no-plano. Este ADR formaliza o caso explícito em que o modelo se inverte.

## Contexto

Estado anterior:

- Reviewer roda em `/run-plan` → recebe diff de um bloco como input principal.
- Contexto auxiliar (e.g., termos ubíquos) é curado pelo autor do plano, repassado pelo `/run-plan` no momento da invocação.
- Desenho minimiza tokens (lista curada vence varredura) e responsabiliza o autor por delimitar o eixo de revisão.

Pressões para o caso document-level:

1. **Decisões estruturais cravam no plano antes do diff existir.** Quando o plano introduz abstração prematura, esquece alternativa óbvia, ou contradiz ADR registrada, o `code-reviewer` só toma conhecimento via diff — a essa altura desfazer custa muito mais do que rebater no plano.
2. **Insumo curado é incompatível com o eixo "contradição com doutrina".** Pedir ao autor "liste os ADRs que seu plano contradiz" é circular: o autor não sabe o que está contradizendo (esse é exatamente o ponto cego). Curar a lista transferiria ao autor o trabalho que o reviewer deveria fazer.

## Decisão

**Reviewers podem operar em documento pré-fato ao lado do padrão diff pós-fato.** Insumo do reviewer document-level é o próprio plano ou ADR draft; output usa o mesmo formato dos demais reviewers (`Localização` / `Problema` / `Filosofia violada` / `Sugestão`).

**Reviewer document-level cuja função inclui detectar contradição doutrinária faz free-read em runtime de doctrine sources** — no toolkit: `docs/decisions/*.md` e `docs/philosophy.md`. O autor do plano não cura essa lista. Free-read é uma passagem por invocação, não loop.

### Escopo da inversão

- **Aplica-se:** reviewer document-level cuja função inclui detecção de contradição com decisão registrada ou doutrina escrita. Hoje: `design-reviewer`.
- **Não aplica-se:** reviewers diff-level (`code/qa/security/doc-reviewer`) — mantêm insumo curado.
- **Não-obrigatório:** reviewer document-level cujo eixo é independente de doutrina escrita pode operar sem free-read (caso futuro hipotético).

## Consequências

### Benefícios

- **Cobertura sem ônus para o autor**: contradição com ADR não registrada exige zero curadoria — reviewer descobre ao varrer.
- **Precedente formalizado**: futuros reviewers document-level caem na mesma doutrina sem reabrir convenção.
- **Não invalida o padrão atual**: insumo curado continua sendo default para reviewers diff-level; ADR só formaliza a exceção.

### Trade-offs

- **Custo de tokens**: free-read de `docs/decisions/*.md` + `docs/philosophy.md` em cada invocação. Aceitável para invocação manual de baixa frequência.
- **Eixos misturados na invocação manual**: operador precisa lembrar quando `@design-reviewer` aplica vs quando `@code-reviewer` aplica.
- **Doutrina não-escrita escapa**: free-read só pega o que está em `docs/decisions/` ou `docs/philosophy.md`. Convenção que ainda não virou doctrine source não é flagrada — sinal de que vale escrever.

### Limitações

- **Dependência da granularidade dos ADRs**: contradição depende do ADR cobrir o caso. ADR vago ("usamos approach X") deixa espaço para falsos negativos.

## Alternativas consideradas

- **Manter padrão único (todos reviewers em diff pós-fato + insumo curado)** — descartado: deixa decisões estruturais sem revisão dedicada até virarem código; ponto cego do autor não é resolvido transferindo curadoria a ele.
- **Reviewer document-level com insumo curado (lista `**ADRs tocadas:**` no plano)** — descartado: circular para o eixo "contradição doutrinária"; o autor não sabe o que está contradizendo.
- **Skill `/review-design <slug>` orquestrando o reviewer com lista pré-coletada** — descartado nesta iteração: adiciona skill experimental antes de validar uso real do reviewer; pode reabrir se ergonomia da invocação `@-mention` provar atrito.
- **Delegação via Task/Agent tool dentro do reviewer** — descartado nesta iteração: subagent frio + briefing duplicado anula economia de contexto para volume pequeno (~10 docs); reabrir se wiring automático em alta frequência materializar.

## Gatilhos de revisão

- **Wiring automático em `/run-plan` pré-loop ou `/new-adr` pré-commit materializa** → reabrir trade-off de tokens (alta frequência muda o cálculo) e considerar Task delegation.
- **Volume de ADRs ultrapassa ~30** → free-read passa a ser custoso mesmo em uso manual; reabrir para considerar curadoria semi-automática (e.g., reviewer pré-filtra ADRs por keyword no plano antes de ler).
- **Aparece reviewer document-level cujo eixo é independente de doutrina escrita** (e.g., revisor de completude factual) → reabrir para confirmar se free-read é só para o eixo doutrinário ou se vale generalizar.
- **Falsos negativos recorrentes** (reviewer não detecta contradição que humano vê) → sinal de que ADRs estão vagos ou doctrine sources estão incompletos; reabrir critério editorial dos ADRs.
