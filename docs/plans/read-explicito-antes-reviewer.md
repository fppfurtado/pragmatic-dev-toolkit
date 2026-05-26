# Plano — Read explícito antes de análise nos prompts dos reviewers

## Contexto

ROADMAP item 7 (commit `163aea7`). Resolve fragilidade observada em item 4 §3.4 da Onda 1 (sessão 2026-05-26): `code-reviewer` invocado no bloco extra (§3.4) rodou contra estado pré-Edit; produziu finding moot ("entrada usa texto antigo") porque `git diff` ainda mostrava só o commit anterior, sem o Edit recém-aplicado. Eu dismissei como stale e segui — mas se o finding fosse legítimo mascarado por timing, teria absorvido um falso "tudo OK". Regressão silenciosa de correctness.

**Hipótese da causa raiz (não validada via `/debug` cirúrgico — registrada como precaução defensiva per absorbed finding F4):** sequência **Edit → Agent rápido** pode disparar antes do harness sincronizar git stage, OR o reviewer recebe snapshot estático do diff como input sem chamar `git diff` em runtime, OR cache de tool result. Mitigação ("instruir `Read`") cobre eficazmente cenários (a)+(b) e provavelmente (c). Validação rigorosa da causa raiz é trabalho separado (potencial `/debug`); este plano ship defensivamente sem bloquear no diagnóstico exaustivo.

**Mecanismo (caller-side per ROADMAP, com docs/procedures/ helper escolhido em gap-clarification — F2 absorbed):** criar `docs/procedures/reviewer-invocation-read.md` com a regra canonical; 3 SKILLs (`/run-plan` §2.3, `/triage` step 5, `/new-adr` step 5) referenciam o procedure. Pattern paralelo a `cutucada-descoberta.md` / `cleanup-pos-merge.md` / `forge-auto-detect.md` (categoria ADR-024). Zero drift entre múltiplos consumidores; extração preventiva antes do pattern emergir 3x ad hoc.

**Por que caller-side e NÃO agent-side (F1 absorbed — rebuttal de alternativa):** `agents/code-reviewer.md:10` prescreve literalmente *"Analise o diff fornecido **e apenas o diff**"*. Agent-side instruction "Read target before analysis" conflitaria com esse escopo doutrinário — agent expandiria análise além do diff. Caller-side preserva a doutrina do `code-reviewer` (escopo diff-only) enquanto força refresh defensivo via prompt composto pela skill. Mesma lógica aplica aos demais reviewers shipados (qa, security, doc) que também são diff-scoped por design. `design-reviewer` é exceção (já tem free-read autônomo per ADR-021) — não precisa da instrução mas recebe sem prejuízo.

**Por que NÃO ADR (F3 absorbed — rebuttal de critérios ADR-035):** (1) incidente recorrente ✓ (1 caso registrado), mas critério "≥3 ad hoc" não atingido; (2) fronteira doutrinal NÃO borrada (mecanismo cirúrgico, sem categoria nova); (3) refinamento doutrinal? — apenas se fosse agent-side (que toca subseção code-reviewer de ADR-035) — caller-side é implementation detail, não doutrina; (4) pattern emergente ≥3x — 3 copies em 1 wave coordenada ≠ emergência ad hoc orgânica. Conclusão: plano é refinamento operacional sob ADR-024 (categoria procedures), não estrutural. Sem ADR.

**Cobertura aceita.** Manual `@reviewer` (operador invocando direto sem skill mediator) não é coberto — incidência baixa porque operador tipicamente invoca após Edit completo. Documentado como gap intencional no procedure file; estender para agent-side (e potencial ADR refinando ADR-035) se incidência emergir.

**ADRs candidatos:** [ADR-011](../decisions/ADR-011-wiring-design-reviewer-automatico.md) (wiring de design-reviewer — toca quando reviewer fires), [ADR-024](../decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md) (categoria procedures que este plano usa), [ADR-026](../decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md) (absorção de findings — mecânica de invocação adjacente), [ADR-029](../decisions/ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md) (precedente § Gatilhos de extração para procedures), [ADR-035](../decisions/ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) (critérios mecânicos — rebatidos para justificar não-ADR), [ADR-038](../decisions/ADR-038-mirror-decisoes-absorvidas-runtime.md) (mensageiro upstream paralelo — context vs operational instruction).

**Linha do backlog:** plugin: Read explícito antes de análise nos prompts dos reviewers

## Resumo da mudança

4 edits coordenados — 1 procedure novo + 3 referências:

1. **`docs/procedures/reviewer-invocation-read.md`** — novo arquivo na categoria ADR-024. Conteúdo: regra canonical da instrução, origem (link ao incidente), escopo (caller-side; razão doutrinária; gap @reviewer manual aceito). ~25 linhas.

2. **`skills/run-plan/SKILL.md` §2.3** — no paragrafo que descreve invocação do reviewer por bloco (passo 3 do loop), adicionar nota: "ao compor o prompt do reviewer, seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/reviewer-invocation-read.md`."

3. **`skills/triage/SKILL.md` step 5** — no bloco "Revisão pré-commit (caminho-com-plano)" que invoca `@design-reviewer`, adicionar nota análoga referenciando o procedure.

4. **`skills/new-adr/SKILL.md` step 5** — no bloco "Revisão pré-retorno" que invoca `@design-reviewer` no ADR draft, adicionar nota análoga referenciando o procedure.

Não toca agent definitions. Doutrina de `code-reviewer` (escopo diff-only) preservada.

## Arquivos a alterar

### Bloco 1 — docs/procedures/reviewer-invocation-read.md novo procedure {reviewer: doc}

- `docs/procedures/reviewer-invocation-read.md`: criar arquivo novo na categoria ADR-024. Estrutura: título + § Regra (instrução canonical com substituição contextual do path do arquivo alvo) + § Origem (link ao incidente + ROADMAP item 7) + § Escopo (caller-side; razão doutrinária citando `code-reviewer.md:10` "apenas o diff"; gap @reviewer manual aceito como cobertura editorial futura).

### Bloco 2 — skills/run-plan/SKILL.md §2.3 referência ao procedure {reviewer: code}

- `skills/run-plan/SKILL.md`: no passo 3 do loop por bloco ("Escolher revisor"), antes ou após o parágrafo que descreve a invocação do reviewer, adicionar 1 frase: "ao compor o prompt do reviewer, seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/reviewer-invocation-read.md`."

### Bloco 3 — skills/triage/SKILL.md step 5 referência ao procedure {reviewer: code}

- `skills/triage/SKILL.md`: no step 5 seção "Revisão pré-commit (caminho-com-plano)", antes ou após a invocação de `@design-reviewer`, adicionar 1 frase análoga referenciando o procedure.

### Bloco 4 — skills/new-adr/SKILL.md step 5 referência ao procedure {reviewer: code}

- `skills/new-adr/SKILL.md`: no step 5 "Revisão pré-retorno", antes ou após a invocação de `@design-reviewer` no ADR draft, adicionar 1 frase análoga referenciando o procedure.

## Verificação end-to-end

- `ls docs/procedures/reviewer-invocation-read.md` retorna o arquivo.
- `grep -n "reviewer-invocation-read" skills/run-plan/SKILL.md skills/triage/SKILL.md skills/new-adr/SKILL.md` retorna match em cada um dos 3 arquivos.
- `grep -nE "apenas o diff" agents/code-reviewer.md` permanece (doutrina diff-only não tocada — agent-side rejeitado per F1 rebuttal).
- Inspeção textual: procedure file tem 3 seções (Regra / Origem / Escopo); razão doutrinária para caller-side citada; gap @reviewer manual reconhecido.

## Notas operacionais

- Plano 4 blocos — procedure primeiro (canonical), depois 3 referências (consumers). Ordem importa: Bloco 1 cria o arquivo referenciado pelos demais; se Bloco 2-4 rodassem antes, referências apontariam para arquivo inexistente.
- design-reviewer dispatcha automaticamente pré-commit (ADR-011); free-read prioriza ADRs candidatos em `## Contexto`.
- Sem `## Verificação manual` — verificação runtime ("observar via trace que prompt inclui instrução") foi avaliada como subjetiva no design-reviewer F5 e absorvida via drop da seção. Grep-based end-to-end cobre. Próxima execução real de `/run-plan`/`/triage`/`/new-adr` valida em uso natural.

## Decisões absorvidas

- `## Contexto`: rebatido agent-side alternative (F1) citando `code-reviewer.md:10` "apenas o diff" como conflito doutrinário (single-path, doutrina diff-only preservada).
- `## Contexto`: rebatidos 4 critérios ADR-035 (F3) justificando não-ADR — 3 copies em 1 wave coordenada não dispara critério "emergente ≥3x ad hoc" (single-path).
- `## Contexto`: adicionada caveat de hipótese sobre causa raiz (F4) — `/debug` cirúrgico deferido; `Read` é precaução defensiva eficaz para múltiplos cenários (single-path).
- `## Verificação manual` removida (F5) — verificação "observar via trace" era subjetiva; grep-based end-to-end basta (single-path).
