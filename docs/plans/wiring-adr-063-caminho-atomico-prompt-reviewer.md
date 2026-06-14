# Plano — Wiring ADR-063: caminho atômico em path-set com trigger prompt-reviewer pré-commit

## Contexto

Materializar decisão de [ADR-063](../decisions/ADR-063-caminho-atomico-trigger-prompt-reviewer.md) no ciclo runtime: tabela do `/triage` step 3 ganha 6ª linha + step 5 ganha parágrafo de Revisão pré-commit (caminho-atômico em path-set narrow) invocando `@prompt-reviewer`; `agents/prompt-reviewer.md` description reflete 2ª trajetória de auto-trigger; `CLAUDE.md` ganha bullet cross-ref.

**Linha do backlog:** plugin: wiring de ADR-063 — codificar 6ª linha "Edit atômico em SKILL/agent/plano" na tabela do /triage step 3 com auto-trigger pré-commit de @prompt-reviewer (escopo: path-set narrow agents/*.md, skills/**/SKILL.md, docs/plans/*.md)

**ADRs candidatos:** ADR-063 (decisão central materializada), ADR-053 (ancestral § Decisão (b) sendo estendida — sucessor parcial primário), ADR-062 (ancestral cujo pattern de dispatch é estendido — sucessor parcial lateral), ADR-009 (substrato categórico — foundational document-level reviewer com free-read; substrato doutrinal de auto-trigger pré-commit)

## Resumo da mudança

Tabela do `## 3. Decidir o artefato` do `skills/triage/SKILL.md` ganha 6ª linha **"Edit atômico em SKILL/agent/plano"** com escopo path-set narrow + critério mecânico de discriminação vs. linhas 4-5 (domain/design). Step 5 do mesmo arquivo ganha parágrafo **Revisão pré-commit (caminho-atômico em path-set narrow)** análogo ao de caminho-com-plano: invoca `@prompt-reviewer` apontando para arquivos editados antes do commit; aplica critério de ADR-053 § Decisão (c) com mapeamento por analogia das 3 condições sobre 4 heurísticas seed do `@prompt-reviewer` (per ADR-063 § Decisão #4). Linha 169 ("Não dispara") revisada para coerência semântica — caminho-atômico em path-set é trigger novo, não exclusão.

`agents/prompt-reviewer.md` description estendida reconhecendo 2ª trajetória de auto-trigger (`/triage` step 5 caminho-atômico + `/run-plan` per-bloco).

`CLAUDE.md` § "Editing conventions" ganha bullet cross-ref a ADR-063 paralelo aos bullets de ADR-053/-057/-061/-062 já presentes.

## Arquivos a alterar

### Bloco 1 — skills/triage/SKILL.md (tabela step 3 + step 5 parágrafo + line 169) {reviewer: prompt}

- `skills/triage/SKILL.md`:
  - Adicionar 6ª linha na tabela do `## 3. Decidir o artefato` (após linha 81 "Atualizar docs/design.md"): **Edit atômico em SKILL/agent/plano** com texto "Refinamento de 1-N edits cirúrgicos em path-set narrow (agents/*.md, skills/**/SKILL.md, docs/plans/*.md), sem multi-fase nem decisão estrutural; dispara @prompt-reviewer pré-commit no step 5 (per ADR-063)".
  - Adicionar critério de discriminação como parágrafo logo após a tabela (antes do "Combinações são comuns..."): critério mecânico de 3 condições per ADR-063 § Decisão #2.
  - Adicionar parágrafo "**Revisão pré-commit (caminho-atômico em path-set narrow).**" no step 5 (após parágrafo de caminho-com-plano linha 162-167) — análogo em estrutura, invoca `@prompt-reviewer`, cita mapeamento por analogia das 3 condições de ADR-053 sobre 4 heurísticas seed de ADR-062 (ADR-063 § Decisão #4).
  - Linha 169 ("Não dispara"): adicionar parágrafo separado **imediatamente após** o bullet existente, no formato canonical: `Caminho-atômico em path-set narrow (`agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md`) **dispara** `@prompt-reviewer` per ADR-063 — ver parágrafo "Revisão pré-commit (caminho-atômico em path-set narrow)" acima.` **Não** reescrever a exclusão original — preservar literal (linha BACKLOG pura, domain/design cirúrgico, ADR-only delegada).

### Bloco 2 — agents/prompt-reviewer.md (description com 2ª trajetória) {reviewer: prompt}

- `agents/prompt-reviewer.md`:
  - Linha 3 (frontmatter `description`): estender de "Acionado automaticamente em diff que toca `agents/*.md`/`skills/**/SKILL.md`/`docs/plans/*.md` per ADR-062; manualmente via `@prompt-reviewer`." para "Acionado automaticamente em (i) `/run-plan` per-bloco quando paths caem em `agents/*.md`/`skills/**/SKILL.md`/`docs/plans/*.md` (per ADR-062), e (ii) `/triage` step 5 caminho-atômico em path-set narrow pré-commit (per ADR-063); manualmente via `@prompt-reviewer`."
  - Linha 8 (body texto da frase "Acionável via..."): estender análogo para refletir 2 trajetórias.

### Bloco 3 — CLAUDE.md (bullet cross-ref) {reviewer: doc}

- `CLAUDE.md`:
  - Adicionar bullet em § "Editing conventions" cross-ref a ADR-063 paralelo aos bullets de ADR-053/-057/-061/-062 já presentes. Posicionar logo após o bullet de ADR-062 (proximidade temática: estende pattern de dispatch).

## Verificação end-to-end

- `grep -c "Edit atômico em SKILL/agent/plano" skills/triage/SKILL.md` retorna 1 (linha 6 da tabela única).
- `grep -c "Revisão pré-commit (caminho-atômico em path-set narrow)" skills/triage/SKILL.md` retorna 1.
- `grep -c "ADR-063" agents/prompt-reviewer.md` retorna ≥1.
- `grep -c "ADR-063" CLAUDE.md` retorna ≥1.
- `grep -E "^\*\*Status:\*\* (Proposto|Aceito)" docs/decisions/ADR-063-caminho-atomico-trigger-prompt-reviewer.md` retorna 1 (Status field canonical preservado).
- `git status --porcelain` clean pós-commit-final.

## Verificação manual

Smoke comportamental pós-`/reload-plugins` em consumer:

1. **Golden path:** invocar `/triage` em consumer com input que motivaria edit atômico em SKILL.md hipotético (operador descreve refinamento pequeno em skill markdown) — verificar que step 3 mostra a tabela com 6 linhas e oferece "Edit atômico em SKILL/agent/plano" como caminho.
2. **Trigger dispara:** step 4 produz edit cirúrgico em SKILL.md; step 5 dispara `@prompt-reviewer` antes do commit; pelo menos 1 finding produzido. Validar: para cada finding, assistente classifica como caminho-único (absorvido pré-commit, registrado em `## design-reviewer findings absorvidos` no commit message) ou ≥1 das 3 condições de ADR-053 § Decisão (c) (cutucado via `AskUserQuestion`). Se reviewer reportar "Prompt alinhado" sem findings → validar que commit prossegue sem dispatcher de absorção/cutucada. Critério: zero outputs intermediários ambíguos (toda finding tem dispatch verificável).
3. **Não-disparo espúrio:** invocar `/triage` produzindo linha BACKLOG pura que tangencialmente toca SKILL.md (ex.: registro de feature futura sem edit em SKILL.md) — trigger NÃO dispara.
4. **Preservação domain/design:** edit atômico em `docs/domain.md` ou `docs/design.md` literalmente — trigger NÃO dispara (preserva linhas 4-5 da tabela; regime ADR-053 mantido).
5. **Path misto (critério ⊆-strict):** edit cross-fronteira em paths misto (`skills/triage/SKILL.md` + `docs/domain.md` no mesmo `/triage`) — verificar que linha 6 da tabela NÃO dispara (predicado ⊆-strict per ADR-063 § Decisão #2 atualizado); substância cai em linhas 4-5; `@prompt-reviewer` NÃO roda automaticamente. Operador pode invocar `@prompt-reviewer` manualmente sobre o arquivo do path-set se quiser scrutiny — verificar que invocação manual funciona normalmente.

## Notas operacionais

- N=1 sessão dogfood-recursive (esta sessão CC) materializou a substância de ADR-063 + este plano. Smoke comportamental em consumer real fica como pendência de validação pós-shipping (cenários 1-5).
- Override do critério N=3 (ADR-043 § Ockham operacionalizado #4) registrado em ADR-063 § Override do critério N=3 — 4ª aplicação consecutiva (precedentes: ADR-057, -061, -062).
- Gatilho de revisão #1 de ADR-063 (≥2 sessões reais com flag trivial) é o teste empírico forward — observar nas próximas invocações pós-shipping.
- Linha 169 do `skills/triage/SKILL.md` é a parte mais delicada — verificar que o parágrafo adicional de "caminho-atômico DISPARA" não cria ambiguidade com a lista de exclusões. Reviewer do Bloco 1 (`@prompt-reviewer`) é o detector natural desse risco.
- **Bloco 1 unificado é deliberado:** acumula 4 edits semanticamente distintos no mesmo arquivo (tabela step 3 + parágrafo de critério mecânico + parágrafo de Revisão pré-commit no step 5 + edit cirúrgico linha 169). Decisão preserva invariante "1 reviewer = visão sistêmica do prompt" (per `agents/prompt-reviewer.md` linha 21 "Analise o arquivo alvo na íntegra"). Reviewer deve tratar como sistema integrado — passos conflitantes potenciais entre linha 6 da tabela, parágrafo de critério, parágrafo do step 5, e exclusão da linha 169 são o ponto mais crítico de coerência.
- **Meta-pattern Override N=3 — decisão deliberada de não-ação:** 4ª aplicação consecutiva do Override em <4 dias (ADR-057 → ADR-061 → ADR-062 → ADR-063). Gatilho #7 de ADR-062 prescreve reabertura na 5ª aplicação. Esta 4ª aplicação **reconhece a pressão e abdica conscientemente** de disparar o gatilho agora — substância de meta-pattern (Override N=3 como categoria editorial) fica para gatilho na 5ª. Honestidade epistêmica sem pré-comprometer ADR sucessor.

## Decisões absorvidas

- ADR-063 § Decisão: parágrafo "estado anterior → estado novo" adicionado ao início (caminho-único).
- ADR-063 § Override do critério N=3: seção nova análoga a ADR-062 reconhecendo 4ª aplicação consecutiva (caminho-único).
- ADR-063 § Auto-aplicação: seção nova com critérios ADR-034 + ADR-043 + ADR-045 + reconhecimento de fragilidade epistêmica (caminho-único).
- ADR-063 § Decisão #2: critério mecânico de discriminação 3-condições da 6ª linha codificado (caminho-único).
- Plano Bloco 1: 4º bullet com prescrição mecânica da edição da linha 169 (preservar literal + parágrafo separado dispatcher); remoção da hesitação "possivelmente" (caminho-único).
- Plano § Notas operacionais: nota explicitando decisão de Bloco 1 unificado + risco de coerência sistêmica (caminho-único).
- Plano § ADRs candidatos + ADR-063 § Origem: ADR-009 adicionado como substrato categórico foundational document-level reviewer (caminho-único).
- Plano § Verificação manual cenário (2): critério verificável substituindo "funciona" vago (commit message section, AskUserQuestion dispatcher, comportamento "Prompt alinhado") (caminho-único).
