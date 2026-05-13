# Plano — Critério mecânico de absorção de findings do `design-reviewer`

## Contexto

Implementação de [ADR-026](../decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md), sucessor parcial de [ADR-011](../decisions/ADR-011-wiring-design-reviewer-automatico.md) § Decisão #1. ADR-011 atribuiu aplicação de findings exclusivamente ao operador; ADR-026 inverte o default (absorver pré-commit) + cutucar somente quando finding satisfaz ≥1 das 3 condições (alternativas competindo / contradiz doutrina / contexto externo). Operador escolheu forma estruturada para o commit message: seção dedicada `## design-reviewer findings absorvidos`.

**ADRs candidatos:** ADR-026 (este ADR), ADR-011 (decisão base que será refinada por cross-ref), ADR-009 (fundação do `design-reviewer`), ADR-002 (eliminar gates de cutucada quando trilho automático cobre — princípio subjacente), ADR-007 (idioma de artefatos informativos — convenção de commits do consumer).

**Linha do backlog:** plugin: critério mecânico para absorção de findings do design-reviewer pré-commit — sucessor parcial de ADR-011 § Decisão #1; default invertido (absorver) + 3 condições de cutucada; commit message ganha seção estruturada `## design-reviewer findings absorvidos` para auditoria pós-fato.

## Resumo da mudança

3 blocos doc-only consolidando ADR-026 em mecânica concreta:

1. **Bloco 1** — `/triage` step 5 (Revisão pré-commit caminho-com-plano) reescrito para refletir critério mecânico (default absorver; 3 condições de cutucada) + prescrição da seção estruturada `## design-reviewer findings absorvidos` no commit message.
2. **Bloco 2** — `/new-adr` step 5 (Revisão pré-retorno) reescrito com mesma mecânica. Caso especial: `/new-adr` não compõe commit message diretamente (responsabilidade externa per spec), mas instrui o caller (`/triage` ou operador manual) sobre quais findings foram absorvidos vs cutucados.
3. **Bloco 3** — ADR-011 § Decisão #1 ganha parágrafo de cross-ref textual ao ADR-026 (paralelo a ADR-005 ↔ ADR-025).

Bundle homogêneo doc-only — `doc-reviewer` em todos.

## Arquivos a alterar

### Bloco 1 — `/triage` step 5 Revisão pré-commit + commit form {reviewer: doc}

- `skills/triage/SKILL.md` step 5 "Revisão pré-commit (caminho-com-plano)": substituir parágrafo atual. Texto-alvo aproximado:

  > **Revisão pré-commit (caminho-com-plano).** Quando o passo 4 produziu plano (caminho-com-plano, com ou sem ADR delegada via `/new-adr`), invocar `@design-reviewer` apontando para o plano. Sem cutucada de pré-execução — o reviewer dispara automaticamente conforme [ADR-011](../../docs/decisions/ADR-011-wiring-design-reviewer-automatico.md). Para cada finding, aplicar critério de [ADR-026](../../docs/decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md):
  >
  > - **Cutucar operador** via `AskUserQuestion` se finding satisfaz ≥1 das 3 condições: (i) ≥2 alternativas legítimas competindo (alternativa rebatida descritivamente pelo reviewer conta como 1 caminho); (ii) contradiz decisão documentada em ADR/philosophy/CLAUDE; (iii) exige contexto fora do diff/plano/ADR. Cláusula default-conservadora: dúvida na classificação → cutucar.
  > - **Absorver pré-commit** quando nenhuma condição dispara (caminho-único). Aplicar correção; registrar no commit message conforme abaixo.
  >
  > **Não dispara** quando o caminho fechou em linha de backlog pura, atualização cirúrgica de `docs/domain.md`/`docs/design.md`, ou ADR-only delegada sem plano — ADR-only é coberta pelo wiring de `/new-adr` (evita dispatch duplo).

  Em seguida (mais abaixo no mesmo step 5, sub-fluxo de commit), adicionar regra de forma:

  > **Forma do commit message com findings absorvidos.** Quando ≥1 finding foi absorvido pré-commit (ADR-026), commit message inclui seção `## design-reviewer findings absorvidos` (idioma da convenção de commits per ADR-007) com bullets curtos no formato `- <localização breve>: <correção aplicada> (caminho-único).`. Seção omitida quando não há findings absorvidos. Findings cutucados via `AskUserQuestion` não entram nesta seção — viram parte do trace narrativo normal (decisão do operador descrita em prosa).

### Bloco 2 — `/new-adr` step 5 Revisão pré-retorno {reviewer: doc}

- `skills/new-adr/SKILL.md` step 5 "Revisão pré-retorno": substituir parágrafo atual. Texto-alvo aproximado:

  > **Revisão pré-retorno.** Invocar `@design-reviewer` apontando para o ADR draft recém-criado. Sem cutucada de pré-execução — o reviewer dispara automaticamente conforme [ADR-011](../../docs/decisions/ADR-011-wiring-design-reviewer-automatico.md). Para cada finding, aplicar critério de [ADR-026](../../docs/decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md):
  >
  > - **Cutucar operador** via `AskUserQuestion` se finding satisfaz ≥1 das 3 condições: (i) ≥2 alternativas legítimas competindo (alternativa rebatida descritivamente pelo reviewer conta como 1 caminho; só conta como ≥2 quando o reviewer apresenta caminhos competindo sem rebater); (ii) contradiz decisão documentada em ADR/philosophy/CLAUDE; (iii) exige contexto fora do diff/plano/ADR. Cláusula default-conservadora: dúvida na classificação → cutucar.
  > - **Absorver pré-commit** quando nenhuma condição dispara (caminho-único). Aplicar correção no ADR draft antes de devolver controle.
  >
  > Cobre tanto invocação standalone quanto delegada por `/triage` no caminho ADR-only — `/triage` passo 5 reconhece que `/new-adr` já cobriu e não redispara o reviewer.
  >
  > **Reportar absorções no relatório de retorno em forma pronta para colar.** Quando ≥1 finding foi absorvido, relatório final inclui o **bloco formatado** `## design-reviewer findings absorvidos` (idioma da convenção de commits per ADR-007) com bullets curtos no formato `- <localização breve>: <correção aplicada> (caminho-único).` — idêntico à forma prescrita no `/triage` step 5. Caller cola integralmente no commit message: (i) no caminho delegado, `/triage` step 5 cola no commit unificado; (ii) no caminho standalone, operador cola no commit do ADR. `/new-adr` não faz commit diretamente (responsabilidade externa per spec).

### Bloco 3 — ADR-011 § Decisão #1 cross-ref textual {reviewer: doc}

- `docs/decisions/ADR-011-wiring-design-reviewer-automatico.md` § Decisão #1: após bullet existente "Findings reportados ao operador, que decide aplicar antes de commitar ou seguir como está", acrescentar parágrafo literal:

  > Refinado por [ADR-026](ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md): default da aplicação invertido para absorção pré-commit + commit message estruturado; cutucada do operador via `AskUserQuestion` reservada para findings que satisfazem ≥1 das 3 condições (alternativas competindo / contradiz doutrina / contexto externo). Mecânica do wiring (quando dispara, override por inação) preservada.

  Status de ADR-011 mantido em `Proposto` per ADR-026 § Decisão (paralelo a ADR-005 ↔ ADR-025: extensão semântica não obriga revisão de status).

## Verificação end-to-end

Pós-execução, confirmar via comandos concretos:

- **Bloco 1:** `grep -c "ADR-026" skills/triage/SKILL.md` retorna ≥2 (referência no parágrafo Revisão pré-commit + na forma do commit message). `grep -c "design-reviewer findings absorvidos" skills/triage/SKILL.md` retorna ≥1.
- **Bloco 2:** `grep -c "ADR-026" skills/new-adr/SKILL.md` retorna ≥1. `grep -c "design-reviewer findings absorvidos" skills/new-adr/SKILL.md` retorna ≥1.
- **Bloco 3:** `grep -c "Refinado por.*ADR-026" docs/decisions/ADR-011-wiring-design-reviewer-automatico.md` retorna 1. `grep -cF "**Status:** Proposto" docs/decisions/ADR-011-wiring-design-reviewer-automatico.md` retorna 1 (status preservado — `-F` força fixed-string match para escapar os asteriscos do markdown bold).
- **Holístico:** `grep -rln "ADR-026" docs/ skills/` retorna ≥4 sites (ADR-026 próprio + 3 blocos).

Sem `test_command` aplicável (toolkit sem suite per `<!-- pragmatic-toolkit:config -->`); verificação end-to-end é textual.

## Verificação manual

Smoke-test em consumer fresh pós-merge:

1. **Cenário Absorção (caminho-único).** Rodar `/triage` com pedido produzindo plano simples; observar `design-reviewer` invocado automaticamente; verificar que findings caminho-único (drift textual, cross-ref) são absorvidos sem prompt; commit message gerado pelo step 5 inclui seção `## design-reviewer findings absorvidos`. **Inspecionar forma dos bullets:** cada um segue `- <localização>: <correção> (caminho-único).` (forma estruturada habilita auditoria via grep).
2. **Cenário Cutucada (Condição 1).** Forçar plano com decisão estrutural ambígua (ex.: 2 caminhos de implementação possíveis); reviewer flaga alternativas competindo; confirmar que assistente cutuca via `AskUserQuestion` em vez de absorver. **Após operador decidir**, inspecionar commit message — finding cutucado aparece no trace narrativo normal em prosa, **não** dentro da seção `## design-reviewer findings absorvidos` (invariante de separação trace vs lista estruturada).
3. **Cenário ADR-only via `/new-adr`.** Rodar `/new-adr "<título>"` standalone; verificar absorção/cutucada per critério no draft; relatório final inclui seção de absorções quando aplicável.

Cenários adicionais (Condições 2 e 3) ficam como pendência se materializarem em uso real — ADR-026 estável sob recursão, doutrina já validada retroativamente.

## Notas operacionais

- **Ordem dos blocos:** 1 (`/triage`) → 2 (`/new-adr`) → 3 (ADR-011 cross-ref). Ordem reflete fluxo de uso (skills primeiro, ADR-011 fechando com cross-ref ao trilho refinado).
- **Sem ADR no caminho de implementação:** ADR-026 já criado e revisado pré-plano (via `/new-adr` delegado por `/triage`). Plano executa apenas a mecânica concreta.
- **Pós-merge:** atualizar `BACKLOG.md ## Concluídos` registrando ADR-026 + plano + link a PR. Considerar `/release` patch (v2.6.1) ou minor (v2.7.0) — feat em mecânica de skills (ADR-026 muda comportamento perceptível de `/triage` e `/new-adr`) sugere **minor**.
- **Recursão:** primeira invocação real do critério após o merge será o próprio `design-reviewer` revisando algum plano/ADR futuro. Critério é estável sob recursão (validado durante revisão de ADR-026 — ver tabela retroativa em ADR-026 § Contexto).
- **Sem alteração de comportamento do `design-reviewer` (agents/design-reviewer.md).** O critério opera no caller (`/triage`, `/new-adr`), não no agent. Reviewer continua reportando findings da mesma forma — caller decide absorção vs cutucada.
