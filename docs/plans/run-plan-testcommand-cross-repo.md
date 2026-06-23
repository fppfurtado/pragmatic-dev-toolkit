# Plano — Campo `**TestCommand:**` declarativo no plano para override cross-repo

## Contexto

`/run-plan` resolve `test_command` do `CLAUDE.md` do repo onde o plano vive — comportamento documentado como "canonical = single-repo" em ADR-049 § Fronteira inversa. O gap: planos no toolkit que alteram arquivos em consumer projects (ex.: `h3-finance-agent`, `scaffold-kit`) rodam o `test_command: null` do toolkit em vez do suite do consumer. A instrução atual é que tais planos usem `**Modo:** runbook`, mas o fluxo canonical (worktree isolada + reviewer por bloco) é desejável quando o plano é pequeno e cirúrgico.

Solução declarativa: campo opcional `**TestCommand:**` no `## Contexto` do plano, paralelo ao `**Branch:**` e `**Modo:**`. Quando presente, `/run-plan` usa esse valor em todos os 3 sites de gate automático (pré-condição 3 baseline + §2 item 2 per-bloco + §3 item 1 gate final), substituindo o `test_command` resolvido do `CLAUDE.md` local. Abordagem manual mas consistente com a filosofia declarativa do toolkit e sem complexidade de resolução dinâmica de paths cross-repo.

**ADRs candidatos:** ADR-049 (mudança é successor partial da fronteira canonical = single-repo para o eixo test_command)
**Linha do backlog:** #132: `/run-plan` — adotar `test_command` do repo afetado em planos canonical cross-repo

## Resumo da mudança

- Adicionar `**TestCommand:**` como campo opcional em `## Contexto` do plano (documentado no template e nas Pré-condições do SKILL.md).
- `/run-plan` lê o campo antes de resolver `test_command` do CLAUDE.md; se presente, usa o valor declarado em todos os 3 sites de gate.
- Comportamento com `**TestCommand:** null` (ou valor explícito `null`) idêntico a `test_command: null`: skip do gate automático, fallback textual se `## Verificação end-to-end` presente.
- ADR novo (successor partial de ADR-049) documenta a dor empírica concreta e a decisão de reabrir a fronteira via campo declarativo.

Fora do escopo: detecção automática de paths cross-repo, per-bloco `TestCommand`, mudanças no modo runbook.

## Arquivos a alterar

### Bloco 1 — `skills/run-plan/SKILL.md` {reviewer: prompt}

- `skills/run-plan/SKILL.md`: 3 sites de gate + 1 atualização doutrinária:
  - **Sites de gate** (onde `test_command` é resolvido e usado):
    1. **Pré-condição 3** — após resolver `test_command` do CLAUDE.md, verificar campo `**TestCommand:**` no `## Contexto` do plano (via grep/read); se presente e não-nulo, substituir. Comportamento `null` explícito: trata como `test_command: null` (skip de gate, fallback textual).
    2. **§2 item 2** — campo já lido na pré-condição; reusar o valor resolvido sem re-leitura.
    3. **§3 item 1** — idem (gate final usa o valor resolvido na pré-condição).
  - **Atualização doutrinária** (texto, não gate):
    4. **Fronteira inversa** — adicionar parágrafo explicando que `**TestCommand:**` é a exceção declarativa para override cross-repo sem detecção automática; manter o aviso de reabertura via dor empírica.

### Bloco 2 — `templates/plan.md` + `docs/decisions/ADR-049-execucao-run-plan-consolidado.md` {reviewer: doc}

- `templates/plan.md`: adicionar `**TestCommand:**` no bloco de comment dos campos especiais do `## Contexto`, imediatamente após `**Modo:**`. Texto: `**TestCommand:** <comando> — incluir quando o plano altera arquivos em outro repo e o test_command do CLAUDE.md local não é o correto; ausência = resolve do CLAUDE.md local normalmente (ADR-049 § Decisão / ADR-068).`
- `docs/decisions/ADR-049-execucao-run-plan-consolidado.md`: adendo em § Decisão (e) — estender lista da família de campos com `**TestCommand:**` + cross-ref a ADR-068 (per ADR-068 § Consequências § Adendos planejados).

## Verificação end-to-end

Inspeção textual (sem suite automática — `test_command: null`):

1. `grep -n "TestCommand" skills/run-plan/SKILL.md` → ≥4 matches (pré-condição 3 + §2 item 2 + §3 item 1 + fronteira inversa).
2. `grep -n "TestCommand" templates/plan.md` → ≥1 match no bloco de comment dos campos especiais.
3. `ls docs/decisions/ | grep ADR-068` → arquivo presente com slug descritivo do campo.
4. `grep -n "ADR-068" docs/decisions/ADR-049-*.md` → ≥1 match (cross-ref adicionado via adendo).

## Verificação manual

Smoke comportamental após `/reload-plugins` em sessão CC nova com plano fixture:

- **C1 — TestCommand presente (string)**: criar `docs/plans/testcommand-fixture.md` com `**TestCommand:** echo "consumer-test"` em `## Contexto` + bloco mínimo em `## Arquivos a alterar`. Rodar `/run-plan testcommand-fixture`. Observar que pré-condição 3 executa `echo "consumer-test"` (não o `test_command: null` do CLAUDE.md local). Gate per-bloco e gate final idem. Deletar o fixture após o smoke test.
- **C2 — TestCommand ausente**: plano sem o campo. Comportamento atual preservado — resolve do CLAUDE.md normalmente. Confirmar ausência de regressão.
- **C3 — TestCommand: null**: plano com `**TestCommand:** null`. Gate automático skipado; se plano tem `## Verificação end-to-end`, usa inspeção textual.

## Decisões absorvidas

- ADR-068 § Decisão: parágrafo verificando 4 critérios ADR-049 § Decisão (e) + família de campos estendida (caminho-único).
- ADR-068 § Decisão regra null: reformulado para deixar explícito override local por plano vs. `test_command: null` global no CLAUDE.md (caminho-único).
- ADR-068 § Consequências: subseção "Adendos planejados" documentando cross-ref ADR-049 via adendo na implementação (caminho-único).
- ADR-068 § Alternativas: alternativa (c) aviso-informativo-runbook+TC registrada como descartada — operador escolheu silêncio, fundamento documentado (caminho-único).
- Plano § Bloco 1: separados subitems de gate (1-3) de atualização doutrinária (4) — contagem inconsistente resolvida (caminho-único).
- Plano § Verificação end-to-end: critério 4 substituído por grep ADR-068 em ADR-049 (evidência real vs status trivialmente satisfeito); critério 1 ajustado para ≥4 matches (caminho-único).
- Plano § Verificação manual C1: path do fixture especificado (`docs/plans/testcommand-fixture.md`, delete após smoke) (caminho-único).

## Pendências de validação

- [capture:validacao] Smoke comportamental dos cenários C1/C2/C3 pós-`/reload-plugins` em sessão CC nova com plano fixture — verificação comportamental do campo declarativo (não exercitável nesta execução). **Encerrada 2026-06-23:** 3/3 PASS contra a prosa shipada v3.14.0 (resolução determinística da pré-condição 3 + 3 sites de gate via 3 fixtures) — C1 `**TestCommand:** echo "consumer-test"` usa o override (não o `null` global) ✓ / C2 ausente herda do CLAUDE.md ✓ / C3 `null` literal faz override local skip. Discriminação null-local vs global confirmada via cenário simulado com global não-nulo (`make test`): C2 herda, C3 ignora e skipa. Não exercitado `/run-plan` ao vivo end-to-end com worktree (resolução determinística cobre o coração da feature).
