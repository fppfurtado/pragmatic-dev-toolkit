# ADR-064: gate-com-executor-validacao em /run-plan §3.2 e /session-audit

**Data:** 2026-06-15
**Status:** Proposto

## Origem

- **Pattern empírico**: 2 instâncias na sessão CC `next-2026-06-14` (2026-06-15) — (i) durante pivôt do `/next`, operador disse "execute as validações pendentes que for possível você rodar sozinho" → Claude mapeou 4 lotes self-contained (Lote 1 `/session-audit` própria; Lote 2 `@doc-reviewer` retroativo Bloco 1 Onda F = 0 findings; Lote 3 AST parse 3 hooks = OK; Lote 4 fixture-based mechanical simulation `/next §4.6+§5` = 6 cenários match spec); (ii) operador auto-relatou como pattern recorrente do uso ("hábito frequente quando endereçando itens de backlog usando o plugin"). NOTES.md entry 2026-06-15T01:08:07Z captura instância (i).
- **Decisão base**: sucessor parcial primário de [ADR-049](ADR-049-execucao-run-plan-consolidado.md) § Decisão (b) (gate manual mecânica de `/run-plan`) — estende o gate de 3 para 4 opções. Sucessor parcial lateral de [ADR-061](ADR-061-skill-session-audit-categorias-editoriais.md) § Decisão (scope `/session-audit`) — adiciona tipo derivado `executar_validacao_pendente` como extensão informal do enum 4-tipos.
- **Triagem**: bifurcação (a) restritivo só `/session-audit` pós-done vs. (b) ambos `/run-plan §3.2` + `/session-audit` resolvida em (b) pelo operador no `/triage` desta sessão — cobrir o "frequentemente" do operador em ambos os pontos onde aparece gate de validação manual.
- **Override do critério N=3**: 5ª aplicação consecutiva (após ADR-057 → -061 → -062 → -063) — ver § Override do critério N=3 abaixo.

## Contexto

`/run-plan §3.2` (gate manual de validação) hoje oferece enum binário: `Validei (Recommended)` / `Falhou — descrever` (`skills/run-plan/SKILL.md:144`). Pattern implícito: operador valida cenários do `## Verificação manual` manualmente, depois reporta verdict via `Validei` (testou OK) ou `Falhou — descrever` (encontrou issue). Quando o plano carrega `## Verificação manual` com cenários enumerados, alguns cenários são executáveis pelo agente sem interação humana (smoke programático, fixture mecânico, comando bash de teste, AST parse, grep/sed em arquivos do repo, invocação de reviewer retroativo sobre commit), outros exigem operador (UI interaction, dado real de produção, business judgment, sistema externo).

Hoje o operador pede manualmente: "execute as que conseguir, defere o resto". Skill não tem rota mecânica — operator escreve em prosa, Claude classifica ad-hoc, executa, reporta. Pattern recorrente e empiricamente validado na sessão CC `next-2026-06-14` (2 instâncias) + auto-reportado pelo operador como hábito frequente do uso.

`/session-audit` (per ADR-061) detecta pendências de validação em planos via heurística "Tool calls de classificação/decisão sem Edit/Write subsequente em artefato canonical" — mas o enum formal de 4 tipos (`captura_backlog` / `captura_notes` / `cristalizacao_adr` / `atualizacao_doutrina`) não cobre "executar uma pendência de validação". Hoje vai como addendum "Follow-up edits identificados (fora do escopo formal de /session-audit)" — workaround manual, não codificado.

**Tensão com ADR-061 § Limitações reconhecida:** ADR-061 § Limitações declara *"side-effects executados (commits, mutações remotas, file edits aplicados) fora de escopo desta skill — categoria distinta sem dor materializada"*. ADR-064 abre exceção controlada para o tipo derivado `executar_validacao_pendente` (definido em § Decisão item 2): execução do subset [executável] muta plano (marca pendência como Encerrada). A "categoria distinta sem dor materializada" passa a ter dor materializada via 2 instâncias da sessão CC `next-2026-06-14` (Lotes 2/3/4 + auto-relato do operador). Expansão registrada como sucessor parcial lateral cond 5 em § Auto-aplicação abaixo.

## Decisão

Codificar categoria nova **`gate-com-executor-validacao`** em 2 sites paralelos:

1. **`/run-plan §3.2` gate manual**: estender enum **condicionalmente** de 2 para 3 opções. Nova opção `Executar o que for executável pra mim (Recommended)` **aparece no enum somente quando classificação prévia detecta ≥1 cenário [executável-pra-mim]**; ausente quando 0 [executável] (enum mantém binário original — `Validei (Recommended)` / `Falhou — descrever`). Cláusula condicional evita gate-cerimônia per ADR-002 § Decisão (oferta sem decisão genuína quando default é determinístico). Skill classifica cada bullet do `## Verificação manual` em **[executável-pra-mim]** vs **[exige-operador]**, reporta a classificação antes do enum (1 bullet por cenário com tag explícita), executa os [executável] em sequência (paralelo onde possível) quando opção escolhida, reporta verdict (PASS/FAIL/CLEAN/N findings/etc.), defere os [exige-operador] explicitamente para revisão humana subsequente, e re-dispatch do enum binário original (`Validei` / `Falhou — descrever`) para o operador decidir após validação do subset deferido.

2. **`/session-audit`**: estender passo 6 com tipo derivado `executar_validacao_pendente` (extensão informal — não entra no enum formal 4-tipos; vai como addendum "**Pendências de validação executáveis**" no relatório). Detectar pendências em planos via heurística adicional ("planos com `## Pendências de validação` cuja sessão tocou direta ou indiretamente"). Cutucada batched ganha 4ª opção: `Executar [executável] também`. Aplicação executa [executável], reporta verdict, marca pendência como Encerrada no plan body.

Cláusula default-conservadora: ambíguo na classificação → [exige-operador] (preserva consent + visibilidade da fronteira).

**Mecânica compartilhada cross-site**: a heurística [executável-pra-mim] vs [exige-operador], critério default-conservadora, e formato canonical do reporte da classificação ficam codificados em `docs/procedures/gate-com-executor-validacao.md` (procedure shared, paralelo a `docs/procedures/cutucada-descoberta.md` consumido por 6 skills e `docs/procedures/forge-auto-detect.md` consumido por 3). Ambos `/run-plan §3.2` e `/session-audit` (itens 1 e 2 acima) referenciam o procedure como fonte canonical. Previne drift cross-site por construção; refactor para procedure shared não aguarda gatilho #3 (3º site emerge) — codificado desde já no plano de implementação. **Alternativa rebatida explicitamente**: (b) inline duplicado nos 2 SKILL.mds, refactor para procedure quando 3º site emerge per gatilho próprio. Rejeitada porque drift entre 2 sites já é caro mecanicamente (mesma classificação + execução + reporte; substância de ~100 linhas de prescrição prompt); custo de refactor pós-fato sobre código já-divergido (re-conciliar prosa de 2 SKILL.mds + ajustar referências cruzadas) superaria custo do procedure agora. Trade-off aceito explicitamente em vez de tácito.

**Razões objetivas:**

- **Preserva consent**: opção explícita no enum (não default automático). Operador escolhe per-invocação se quer delegar execução.
- **Visibilidade da fronteira**: reporte da classificação ANTES da execução permite operador discordar (escolher `Validei` direto sem delegar, ou `Falhou — descrever` se discorda da classificação) se classification model errar.
- **Cobertura ampla** (cf. escolha (b) do `/triage`): o "frequentemente" do operador é coberto em ambos os pontos onde aparece gate manual no fluxo do plugin.
- **Categoria mecânica clara**: heurística [executável-pra-mim] = "cobre por Bash/Read/grep/AST parse/reviewer subagent retroativo/fixture mecânico controlado" (substância concreta verificável). [exige-operador] = "UI interaction, dado real, business judgment, sistema externo".
- **Anti-gate-cerimônia per ADR-002**: 3ª opção é condicional (presente só com ≥1 [executável]), não acompanha o enum cosmeticamente — sem cenário executável, sem opção (enum permanece binário).

## Consequências

### Benefícios

- Fecha pendências de validação executáveis mais cedo (no /run-plan done OU no /session-audit pós-done), reduzindo fricção do "operador esquece de pedir".
- Pattern consistente cross-skill — mesma classificação heurística + mesma opção textual + mesmo critério default-conservador em ambos os sites.
- Auditabilidade: classificação reportada permite operador validar before-and-after a execução.

### Trade-offs

- **Superfície maior**: feature wired duas vezes (`/run-plan` + `/session-audit`). Risco de divergência editorial mitigado **por construção** via procedure shared `docs/procedures/gate-com-executor-validacao.md` (codificada desde já — ver § Decisão "Mecânica compartilhada cross-site"). Ambos os SKILL.mds referenciam o procedure; mudança da heurística vive em 1 arquivo só.
- **Custo de classificação**: Claude paga tokens classificando cada cenário per gate (mesmo quando opção não é escolhida). Mitigação: classificação simples (heurística mecânica de keywords + sub-bullets do cenário), não recursiva.
- **Risco de classificação errada**: agente pode classificar como [executável] cenário que na verdade exige operador (ex: smoke que muta state remoto). Mitigação: cláusula default-conservadora ([exige-operador] em dúvida); operador pode override no enum (escolher `Eu valido manual` mesmo após classificação reportar [executável]).
- **Calibração esperada da heurística [executável-pra-mim]**: empírico dos Lotes 2/3/4 da sessão CC `next-2026-06-14` mostrou 100% dos cenários classificáveis como [executável] sem ambiguidade (smoke programático, fixture mecânico, AST parse, reviewer retroativo). Calibração otimista — over-correção possível se cenários reais forem mais ambíguos. Próximo design-reviewer audita drift comparando com esta baseline empírica.
- **Tensão alinhamento empírico vs. cobertura ampla**: alternativa (a) restritiva alinharia melhor com a evidência (Lotes 2/3/4 todos dentro de `/session-audit`); escolha (b) ampla justificada via auto-relato do operador como pattern recorrente. Trade-off visível: aceito risco de superfície subutilizada em `/run-plan §3.2` se uso real cair na minoria.

### Limitações

- Não cobre validações que emergem dinamicamente em runtime do `/run-plan` (só as listadas em `## Verificação manual` no plano + as detectadas pela heurística de `/session-audit`).
- Cláusula de blast-radius: opção `Executar [executável]` NUNCA inclui mutação remota (push, gh release, issue create) — esses ficam fora do escopo [executável-pra-mim] por construção. Codificado na heurística do plano de implementação.

## Auto-aplicação per ADR-034

- **Cond 1** (incidente recorrente, ≥3 instâncias práticas): **NÃO APLICA** — 2 instâncias na sessão CC `next-2026-06-14` + auto-relato operador (sub-N3 cross-sessão; ver § Override do critério N=3 abaixo para calibração frágil).
- **Cond 2** (substitui ADR ancestral): **NÃO APLICA** — estende ADR-049 § Decisão (b) e ADR-061 § Decisão sem substituir.
- **Cond 3** (codifica restrição externa de longa duração): **NÃO APLICA** — pattern interno operacional, sem componente regulatório/contratual.
- **Cond 4** (introduz categoria nova de decisão): **APLICA** — "gate-com-executor-validacao" é categoria nova de pattern wired cross-skill (gate manual com executor automático classificado + deferido).
- **Cond 5** (sucessor parcial): **APLICA** — sucessor parcial primário de ADR-049 § Decisão (b) (gate manual de `/run-plan` estendido de 3 para 4 opções) + sucessor parcial lateral de ADR-061 § Decisão (scope `/session-audit` estendido com tipo derivado).

Peso primário em cond 4 (categoria nova); cond 5 reforça via dupla ancestralidade.

## Override do critério N=3

5ª aplicação consecutiva da Override do critério N=3 (após ADR-057 → -061 → -062 → -063) — gatilho #1 de [ADR-063](ADR-063-caminho-atomico-trigger-prompt-reviewer.md) § Gatilhos atingido.

**Calibração:** ADR-064 opera em zona mais frágil que ADR-063 (N=1 sessão dogfood). Comparação:

- ADR-057: ≥1 incidente real cross-sessão + ≥2 instâncias acumuladas.
- ADR-061: ≥1 incidente real cross-sessão + dor materializada.
- ADR-062/063: N=1 sessão dogfood + dor reconhecida.
- ADR-064: 2 instâncias same-sessão (Lotes 2/3/4 do `/session-audit` + pivôt do `/next`) + auto-relato do operador como pattern recorrente do uso — mais frágil que -062/-063 (não cross-sessão).

**Peso primário do override:** escolha (b) cobertura ampla via auto-relato do operador no `/triage` desta sessão. Operador endossou explicitamente que pattern é recorrente no uso diário, não validado cross-sessão por evidência terceira.

**Fragilidade epistêmica reconhecida:** ADR-064 aceita o débito empírico explicitamente — gatilho #1 de § Gatilhos de revisão é o teste empírico forward (override do enum detectado em transcript ≥2 sessões pós-shipping → refinar heurística). Substância opera no limite do critério N=3.

**Avaliação meta-editorial separada** sobre se Override está virando hábito vs. exceção rara recomendada em sessão subsequente via `/triage "avaliar meta-pattern Override critério N=3 após 5ª aplicação consecutiva"`; esta ADR-064 não bloqueia aquela avaliação — substância concreta (pattern empírico operacional + cobertura ampla escolhida no /triage) justifica per-se.

## Alternativas consideradas

### (a) Restritivo — só `/session-audit` pós-done

Refinar somente `/session-audit` passo 6 com tipo derivado `executar_validacao_pendente`. Não tocar `/run-plan §3.2`.

**Por que rejeitada:** alinha com instância empírica (Lotes 2/3/4 desta sessão foram dentro de `/session-audit`), mas o operador relata que faz o pedido também ANTES do done do `/run-plan` — pattern recorrente sub-escopo. Cobertura parcial vs. ampla foi resolvida em favor de ampla no `/triage` bifurcação.

### (b) Amplo — ambos `/run-plan §3.2` + `/session-audit` (escolhido)

Wire-up em 2 sites paralelos. Implementação coordenada via plano executável.

**Por que aceita:** cobre o "frequentemente" do operador onde quer que apareça o gate. Trade-off da superfície aceitável dado pattern recorrente auto-relatado.

### (c) Default automático sem opção

Skill sempre executa o [executável] sem perguntar.

**Por que rejeitada:** paga tokens em todo `/run-plan` mesmo quando não há cenários executáveis. Sem consent visível. Sem fronteira clara entre [executável] e [exige-operador] visível ao operador. Risco de over-correção (agent decide implicitamente, não-auditável).

## Gatilhos de revisão

- **Classificação errada empírica**: **Auto-relato do operador em NOTES.md ≥2 instâncias** (operador captura via `/note` quando classificação reportou [executável] mas cenário realmente exigia operador) **OR override do enum detectado no transcript ≥2 sessões pós-shipping** (operador escolheu `Executar [executável]`, classificação reportou cenário X como [executável], executor reportou PASS, mas operador depois escolheu `Falhou — descrever` listando X como falhando — visível em audit retrospectivo). Qualquer um dos 2 sinais acumula → refinar heurística [executável-pra-mim] vs [exige-operador] no procedure shared.
- **Drift no procedure shared**: code-review futuro flagar que ou `/run-plan §3.2` ou `/session-audit` divergiu da spec literal do `docs/procedures/gate-com-executor-validacao.md` (texto da opção, critério de classificação, default-conservadora) → corrigir o SKILL divergente para realinhar à fonte canonical.
- **Padrão emergente em mais sites**: se 3º site emerge (ex: `/curate-backlog` com pendências executáveis), considerar codificação como procedure shared em `docs/procedures/` (paralelo a `cutucada-descoberta.md` e `forge-auto-detect.md`).
- **Disuso ≥3 meses**: operador nunca seleciona a opção em ≥3 meses de uso recorrente → considerar reversão (manter só /session-audit per alternativa (a)).
