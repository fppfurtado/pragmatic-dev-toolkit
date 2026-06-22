# ADR-068: Campo `**TestCommand:**` declarativo no plano para override cross-repo do `test_command`

**Data:** 2026-06-22
**Status:** Proposto

**Próxima revisão:** 2026-12-22
**Cadência:** trimestral
**Critério de erosão auditável:** ≥1 incidente de plano cross-repo onde `**TestCommand:**` foi omitido e o gate executou o suite incorreto sem aviso (falso negativo silencioso da abordagem declarativa), OR ≥2 planos reais com demanda por per-bloco test_command (alternativa (b) descartada em ADR-068 § Alternativas consideradas).

## Origem

- **Decisão base:** [ADR-049](ADR-049-execucao-run-plan-consolidado.md) (fronteira canonical = single-repo; mudança é successor partial da § Fronteira inversa).
- **Dor empírica:** plano no toolkit que altera arquivos de consumer project executou `test_command: null` do toolkit em vez do suite do consumer — motivação concreta para reabrir a fronteira via mecanismo declarativo.

## Contexto

ADR-049 § Modo runbook documenta a "Fronteira inversa (canonical = single-repo)": `test_command` resolve do `CLAUDE.md` do repo onde o plano vive; planos com edits coordenados em múltiplos repos devem usar `**Modo:** runbook`. A reabertura desta fronteira foi explicitamente gated por "dor empírica concreta (skip de teste relevante levando a regressão)".

A dor foi observada: plano cirúrgico no toolkit (onde `test_command: null`) que altera skill/template em consumer project não executa o suite do consumer — o operador quer o fluxo canonical (worktree isolada + reviewer por bloco) mas o `test_command` resolvido é incorreto para o contexto cross-repo.

O pattern de campos opcionais no `## Contexto` do plano (`**Branch:**` per ADR-028/ADR-049 § (b), `**Modo:**` per ADR-041/ADR-049 § (d), `**Linha do backlog:**` per ADR-049 § (a)) é o idioma declarativo do toolkit para customizar comportamento por plano. Extendê-lo com `**TestCommand:**` é a solução mais consistente com o estilo existente.

## Decisão

**Adicionar campo opcional `**TestCommand:**` no `## Contexto` do plano (documentado no template + SKILL.md). Quando presente, `/run-plan` usa o valor em todos os 3 sites de gate automático, substituindo o `test_command` resolvido do CLAUDE.md local.**

Regras de uso:

- **Ausência** → comportamento atual preservado (resolve do CLAUDE.md local normalmente).
- **Valor string** (ex.: `cd /path/to-consumer && make test`) → usado literalmente nos 3 sites: pré-condição 3 baseline, §2 item 2 per-bloco, §3 item 1 gate final.
- **Valor `null`** (literal `null`) → skip de gate automático para este plano, mesmo que `test_command` esteja configurado no CLAUDE.md do repo. Útil em plano cross-repo onde o suite local (do repo do plano) é irrelevante para a mudança; fallback textual se `## Verificação end-to-end` presente. Distinto de `test_command: null` global no CLAUDE.md — este campo é override local por plano.
- **Interação com `**Modo:** runbook`**: campo `**TestCommand:**` é no-op em runbook (pré-condição 3 e gates de bloco não aplicam em runbook per ADR-049 § (d)). Sem incompatibilidade dura — silêncio é a política conservadora.

Implementação: ler `**TestCommand:**` do `## Contexto` do plano na pré-condição 3 (antes de resolver do CLAUDE.md); valor resolvido propagado para §2 item 2 e §3 item 1 sem re-leitura.

Campo `**TestCommand:**` satisfaz os 4 critérios de promoção de ADR-049 § Decisão (e) para a família de campos opcionais do `## Contexto`: (i) afeta `/run-plan`; (ii) ausência = comportamento atual preservado (default natural); (iii) opt-in por plano, revertível com 1 linha de edit; (iv) cabe em 1 linha de `## Contexto`. Campo entra na família: `**Branch:** + **Modo:** + **Linha do backlog:** + **Termos ubíquos tocados:** + **ADRs candidatos:** + **TestCommand:**`. ADR-049 § Decisão (e) recebe cross-ref a este ADR via adendo (ver `## Consequências`).

## Consequências

### Benefícios

- Planos canonical cross-repo podem rodar o suite do repo afetado sem recorrer ao modo runbook.
- Consistente com o pattern de campos declarativos do toolkit — sem lógica de detecção automática nem path resolution de repos externos.
- Implementação simples: ~10 linhas de mudança em `skills/run-plan/SKILL.md` + 1 linha em `templates/plan.md`.

### Trade-offs

- Campo manual: author do plano precisa declarar explicitamente (vs. detecção automática). Preferível per filosofia YAGNI + estilo declarativo do toolkit.
- Reabre parcialmente a fronteira canonical = single-repo — restrita ao eixo `test_command`; worktree, commits e reviewers continuam single-repo.

### Limitações

- `**TestCommand:**` é string literal: sem variáveis de ambiente, sem resolução de path relativo via toolkit. Responsabilidade do author do plano garantir que o comando funcione no contexto de execução.
- Modo runbook: campo no-op (silêncio intencional — runbook não tem gates automáticos).

### Adendos planejados

- **ADR-049 § Decisão (e)**: estender lista da família de campos com `**TestCommand:**` + cross-ref a ADR-068. Mantém ADR-049 como source-of-truth da família. Adendo aplicado na implementação do plano `run-plan-testcommand-cross-repo`.

## Alternativas consideradas

### (a) Detecção automática de paths cross-repo

`/run-plan` inspecionaria `## Arquivos a alterar`, detectaria paths fora do git root atual, resolveria o `CLAUDE.md` do repo afetado, leria `test_command` de lá.

**Descartada**: complexidade de path resolution + CLAUDE.md parsing de repo externo + detecção de git root externo — viola YAGNI. Campo declarativo entrega o mesmo resultado com zero lógica de resolução.

### (b) Campo per-bloco `{test_command: ...}` no header do bloco

Anotação `{test_command: cd /path && make test}` em cada bloco de `## Arquivos a alterar`, paralela ao `{reviewer: ...}`.

**Descartada**: fragmentação sem ganho prático — plano cross-repo tipicamente tem um único `test_command` para o repo afetado; per-bloco aumenta verbosidade do plano sem cenário de uso distinto identificado.

### (c) Aviso informativo quando `**TestCommand:**` presente em plano runbook

Quando `/run-plan` detecta `**TestCommand:**` declarado + `**Modo:** runbook` no mesmo plano, emitir 1 linha de aviso não-bloqueante (paralelo ao aviso de "alinhamento dirty").

**Descartada**: campo ignorado silenciosamente tem precedente em campos de contexto sem efeito em modos alternativos — cerimônia de aviso desproporcional ao risco. O caso é raro por construção (planos runbook tipicamente cobrem system-surgery, não casos cross-repo com suite do consumer). Reabrir se incidência documentada em ≥2 planos reais mostrar que o silêncio causou confusão.

## Gatilhos de revisão

- Plano cross-repo com `**TestCommand:**` declarado que executou o comando errado (evidence de falso conforto).
- Demanda de per-bloco `test_command` em ≥2 planos reais (sinal de que (b) descartada deveria ser revisitada).
- Proposta de detecção automática com ≥1 caso concreto onde declaração manual foi esquecida causando regressão (evidence de que YAGNI foi conservador demais).
