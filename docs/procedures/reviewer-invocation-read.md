# Reviewer invocation — `Read` antes de análise

Procedimento compartilhado consumido em runtime pelas skills que invocam reviewers via `Agent` tool: `/run-plan` §2.3 (loop por bloco), `/triage` step 5 (revisão pré-commit), `/new-adr` step 5 (revisão pré-retorno). Skills referenciam este arquivo na composição do prompt do reviewer. Categoria `docs/procedures/` estabelecida em [ADR-051](../decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c).

## Regra

No prompt da invocação do reviewer (qualquer agent shipado via `agents/`), incluir instrução explícita:

> **Antes de analisar, leia o arquivo alvo via `Read`** — não confie só em `git diff`, que pode estar stale entre Edit recente e invocação do Agent.

Substituir "arquivo alvo" pelo path concreto na composição do prompt — ex.: "leia `docs/plans/<slug>.md` via Read antes de analisar"; "leia `docs/decisions/ADR-NNN-*.md` via Read antes de analisar"; "leia os arquivos tocados no diff via Read antes de analisar".

## Origem

Fragilidade observada em sessão de 2026-05-26 (ROADMAP item 7 / item 4 §3.4 da Onda 1): `code-reviewer` invocado no bloco extra de `/run-plan` rodou contra estado pré-Edit; produziu finding moot ("entrada usa texto antigo") porque `git diff` ainda mostrava só o commit anterior, sem o Edit recém-aplicado. Sequência **Edit → Agent rápido** pode disparar antes do harness sincronizar git stage, OR reviewer recebe snapshot estático do diff como input, OR cache de tool result.

Instrução de `Read` força refresh defensivo do reviewer sobre o estado atual do arquivo alvo, cobrindo eficazmente esses cenários sem depender da causa raiz exata.

## Escopo

**Caller-side apenas** — instrução vive no prompt composto pela skill consumidora, não no agent definition. Razão doutrinária: `agents/code-reviewer.md:10` prescreve literalmente *"Analise o diff fornecido **e apenas o diff**"*; adicionar "Read target" agent-side conflitaria com esse escopo (agent expandiria análise além do diff). Caller-side preserva a doutrina diff-only dos reviewers shipados (`code-reviewer`, `qa-reviewer`, `security-reviewer`, `doc-reviewer`) enquanto força refresh defensivo via prompt.

`design-reviewer` é exceção — já tem free-read autônomo per [ADR-048](../decisions/ADR-048-free-read-design-reviewer-consolidado.md) — não precisa da instrução mas recebe sem prejuízo (uniformidade no prompt da skill consumidora).

**Manual `@reviewer`** (operador invocando direto sem skill mediator) **não é coberto** — incidência baixa porque operador tipicamente invoca após Edit completo. Estender para agent-side (e potencial refinamento de ADR-035) se incidência emergir em invocações manuais.
