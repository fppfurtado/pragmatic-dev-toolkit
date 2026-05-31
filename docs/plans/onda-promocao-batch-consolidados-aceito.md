# Plano — Onda Promoção (7 consolidados Proposto → Aceito em batch)

## Contexto

**ADRs candidatos:** ADR-046+047+048+049+050+051+052 (todos 7 consolidados da redesign — alvos da promoção em batch), ADR-034 (critério adendo vs novo ADR — não tocado; promoção de Status não é refinamento de doutrina, é lifecycle), ADR-052 (meta-pattern editorial — § Decisão (c) literal exige "Aceito" para critério mecânico de modo (c) sobre ADR-009; gating descoberto via F10 cutucada).

**Linha do backlog:** Onda Promoção é sub-scope da umbrella multi-onda em `## Próximos` (redesign camada doutrinal); não corresponde a linha distinta. Per ADR-049 § Decisão (a) + precedente Ondas A-H, umbrella é atualizada in-place post-merge.

**Origem da onda:** F10 cutucada absorvida durante sessão de `/triage` Onda I (commit `9540a8f` em branch `onda-i-draft-pending-promotion`, draft work-in-progress preservado). F10 revelou que ADR-052 § Decisão (c) literal exige "grep ID em § Decisão de ADRs **Aceito** vigentes" para critério mecânico de modo (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO. Onda I aplica modo (c) sobre ADR-009 com base em hardcode em ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]` — mas ADR-048 está formalmente Proposto, não Aceito. TODOS os 7 consolidados (ADR-046+047+048+049+050+051+052) estão Proposto-shipped — effective em produção, referenciados por CLAUDE.md/skills/agents como autoridade, mas formalmente Proposto.

Operador escolheu via F10 Opção (b) "Promover consolidados a Aceito em batch" — onda dedicada PRÉ-Onda I com cascata múltipla. Trade-off explícito vs outras opções:
- (a) "Aceito de fato + documentar trade-off" — rejeitada (precedente flexibiliza critério mecânico de ADR-052 para ondas futuras).
- (c) "Refinar ADR-052 § (c) para 'vigente sem Substituído'" — rejeitada (scope creep dentro da Onda I; ADR sucessor parcial de ADR-052 fora de escopo).

Onda Promoção é tactical-only — promove Status sem codificar critério via ADR. Critério de promoção aplicado documentado em § Resumo da mudança (substância pragmática), preservado em commit message + plan body como invariante editorial (mecanismo análogo ao mirror runtime de design-reviewer findings entre commit message e plan body, pattern aplicado em ondas precedentes — independente de ADR-053 que vive em branch separado pré-merge desta onda). Se pattern recorrer (futuros consolidados Proposto-shipped sem promotion), onda futura pode codificar via ADR sucessor parcial de ADR-034.

## Resumo da mudança

**Critério de promoção aplicado uniformemente aos 7 ADRs** (substância pragmática absorvida da F10 cutucada da Onda I):

1. **Shipped** — merged em main via PR aceito (verificável via `git log --merges` por commit hash do ADR).
2. **Effective em produção** — comportamento prescrito está vigente no plugin (skills/agents/hooks invocam mecanismo conforme ADR).
3. **Referenciado como autoridade** — citado por ≥1 doc vivo (CLAUDE.md OR skills/*.md OR agents/*.md) como fonte de verdade vigente, não apenas como precedente histórico.
4. **Sem `Substituído` marker** — ADR não foi superseded por sucessor parcial que revoga doutrina central (cond 2 de ADR-034 NÃO disparou).

Aplicação dos 4 critérios aos 7 candidatos:

| ADR | Shipped (PR + commit) | Effective | Referenciado | Sem Substituído | Promotion OK? |
|---|---|---|---|---|---|
| ADR-046 (cutucada uniforme descoberta) | PR #90 `dbac4d6` | sim (5 skills aplicam) | CLAUDE.md `## Cutucada de descoberta` § + skills | sim | ✓ |
| ADR-047 (modo local paths) | PR #91 `cd0b533` | sim (paths.local mode) | CLAUDE.md `## Pragmatic Toolkit` + role contract | sim | ✓ |
| ADR-048 (free-read design-reviewer) | PR #92 `2858005` | sim (design-reviewer carrega curadoria) | CLAUDE.md bullet + agents/design-reviewer.md | sim | ✓ |
| ADR-049 (execução run-plan) | PR #93 `f55e2a4` | sim (run-plan opera 4-dimensões) | CLAUDE.md bullet + skills/run-plan + skills/triage | sim | ✓ |
| ADR-050 (componentes plugin) | PR #94 `376a755` | sim (naming + auto-gating triplo) | CLAUDE.md `## Plugin component naming` + hooks docstrings | sim | ✓ |
| ADR-051 (convenções editoriais) | PR #95 `7991fdb` | sim (3 audiências + categoria procedures/) | CLAUDE.md + philosophy + skills/release + procedures | sim | ✓ |
| ADR-052 (3 modos editoriais) | PR #96 `fdba1aa` | sim (meta-pattern aplicado em Onda I draft) | CLAUDE.md bullet | sim | ✓ |

**Os 7 satisfazem cumulativamente** — promoção em batch é coerente. Saldo pós-Onda Promoção: 7 ADRs Proposto → Aceito (zero archived, zero novos); inventário vigente permanece 31; apenas Status formal alinha com state real.

**Nota sobre limiar de critério (3) — caso ADR-052:** ADR-052 satisfaz critério (3) com 1 referência apenas (CLAUDE.md bullet), enquanto os outros 6 ADRs aparecem em ≥2 docs vivos. É tecnicamente OK pelo critério literal ("≥1 doc vivo") pois o bullet codifica meta-pattern aplicado em Onda I draft. Se promoção batch futura encontrar ADR com referência apenas em bullet meta-citação sem aplicação concreta derivada, reavaliar critério (3) para "≥1 doc vivo + ≥1 aplicação concreta evidente em código/skill/agent vivo".

**Pós-Onda Promoção, Onda I retoma** com critério mecânico de ADR-052 § Decisão (c) estritamente satisfeito (`grep "ADR-009" docs/decisions/ADR-048-*.md` → match em § Decisão de ADR Aceito vigente). Branch `onda-i-draft-pending-promotion` re-validado e merged para main.

## Arquivos a alterar

### Bloco 1 — Promoção Status: Proposto → Aceito em 7 ADRs consolidados {reviewer: doc}

7 edits cirúrgicos uniformes (1 linha cada) — frontmatter Status field.

- `docs/decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md`: substituir `**Status:** Proposto` por `**Status:** Aceito`.
- `docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md`: análogo.
- `docs/decisions/ADR-048-free-read-design-reviewer-consolidado.md`: análogo.
- `docs/decisions/ADR-049-execucao-run-plan-consolidado.md`: análogo.
- `docs/decisions/ADR-050-componentes-plugin-consolidado.md`: análogo.
- `docs/decisions/ADR-051-convencoes-editoriais-consolidado.md`: análogo.
- `docs/decisions/ADR-052-codificacao-3-modos-editoriais-refinamento-consolidacao.md`: análogo.

**Nota editorial:** edits ficam restritos ao campo Status do frontmatter — corpo dos ADRs (§ Origem, § Contexto, § Decisão, etc.) permanece intacto per ADR-classical "ADR aceito é imutável exceto Status lifecycle". Promoção é parte do lifecycle (Proposto → Aceito → Substituído → Revogado), não edição de substância.

## Verificação end-to-end

**Critérios de sucesso da Onda Promoção:**

1. **7 ADRs com Status: Aceito:** `grep -l "^\*\*Status:\*\* Aceito" docs/decisions/ADR-046-*.md docs/decisions/ADR-047-*.md docs/decisions/ADR-048-*.md docs/decisions/ADR-049-*.md docs/decisions/ADR-050-*.md docs/decisions/ADR-051-*.md docs/decisions/ADR-052-*.md | wc -l` → 7.

2. **Nenhum ADR consolidado permanece Proposto:** `grep -l "^\*\*Status:\*\* Proposto" docs/decisions/ADR-046-*.md docs/decisions/ADR-047-*.md docs/decisions/ADR-048-*.md docs/decisions/ADR-049-*.md docs/decisions/ADR-050-*.md docs/decisions/ADR-051-*.md docs/decisions/ADR-052-*.md` → vazio (zero matches).

3. **Corpo dos 7 ADRs intacto exceto Status:** `git diff main --stat docs/decisions/ADR-046-*.md docs/decisions/ADR-047-*.md docs/decisions/ADR-048-*.md docs/decisions/ADR-049-*.md docs/decisions/ADR-050-*.md docs/decisions/ADR-051-*.md docs/decisions/ADR-052-*.md` → 7 arquivos, +7/-7 (uma linha alterada por arquivo).

4. **Critério mecânico de ADR-052 § Decisão (c) agora estritamente satisfeito sobre ADR-009 via ADR-048:** `awk '/^## Decisão/,/^## (Consequências|Alternativas)/' docs/decisions/ADR-048-*.md | grep "ADR-009"` → match não-vazio (always-include curated list `[ADR-009, ADR-034, ADR-043]` em § Decisão de ADR-048 que agora está Aceito); pré-condição para Onda I retomar. Awk extrai seção semantica (não grep linha-a-linha) — verifica que match está dentro de § Decisão, não em § Origem/§ Contexto.

5. **Inventário vigente preservado:** `ls docs/decisions/ADR-0*.md | grep -v archive | wc -l` → 31 (zero archived nesta onda; zero novos).

6. **Nenhum dos 7 ADRs ganhou marker `Substituído`:** `grep -l "Substituído" docs/decisions/ADR-046-*.md docs/decisions/ADR-047-*.md docs/decisions/ADR-048-*.md docs/decisions/ADR-049-*.md docs/decisions/ADR-050-*.md docs/decisions/ADR-051-*.md docs/decisions/ADR-052-*.md` → vazio.

7. **Nenhum ADR fora dos 7 alvos teve Status modificado por engano:** `git diff main --name-only docs/decisions/` → apenas 7 paths listados (ADR-046+047+048+049+050+051+052); zero drift transversal. Charter atualização (`docs/plans/redesign-camada-doutrinal-charter.md`) fica como separate commit post-merge per Notas operacionais (NÃO escopo desta onda).

8. **doc-reviewer audita drift:** edits cirúrgicos restritos ao campo Status; corpo dos ADRs (§ Origem, § Contexto, § Decisão, etc.) preservado verbatim; nenhuma substância tocada.

## Notas operacionais

**Single bloco unitário:** 7 edits uniformes em 7 arquivos. Doc-reviewer audita uniformidade do critério aplicado (todos 4 critérios verificados na tabela do § Resumo). Sem partição em sub-blocos — operação mecânica.

**Charter atualização post-merge:** após merge desta Onda Promoção, atualizar `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução":
- Adicionar linha "Onda Promoção — Batch promotion 7 consolidados Proposto → Aceito" entre ADR-052 e Onda I.
- Anti-regression checklist: § Skills e fluxo + § Convenções editoriais + § Reviewers preserved (promoção não toca substância; apenas Status formal alinha com state real).
- Sinal explícito de que critério mecânico de ADR-052 § Decisão (c) agora estritamente satisfeito sobre ADR-009 via ADR-048.

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A-H); NÃO escopo desta Onda Promoção.

**Auto-bootstrap mecânico:** ADR-052 (definidor do critério modo (c)) e ADR-048 (alvo da verificação mecânica via grep da always-include list) são promovidos na mesma onda. Critério mecânico de ADR-052 § Decisão (c) (grep ID em § Decisão de ADR Aceito vigente) passa a ser estritamente satisfeito a partir do merge desta onda — Onda I retoma com o critério vigente. Sem circularidade lógica: critério opera sobre o alvo do grep (ADR-048), não sobre o definidor (ADR-052); ambos ficarem Aceito simultaneamente apenas habilita a aplicação retroativa do critério.

**Pós-merge desta Onda Promoção — Onda I retoma:**
1. `git checkout onda-i-draft-pending-promotion` (branch dedicado preservado em `9540a8f`).
2. `git rebase main` (incorpora Status promotions).
3. Re-validação: F10 resolve automaticamente (ADR-048 agora Aceito); F4/F6/F9 cutucadas já decididas.
4. `git checkout main && git merge onda-i-draft-pending-promotion --no-ff` OR push branch + PR + merge.
5. Onda I execução via `/run-plan onda-i-migracao-cluster-alinhamento-triage`.

**Critério de promoção (4-cumulativos) documentado em prosa, não codificado via ADR.** Esta onda **é** a primeira aplicação do critério a 7 ADRs simultaneamente — ADR-034 cond 4 (categoria editorial nova "promoção retroativa Proposto→Aceito de consolidado-shipped") e cond 5 (sucessor parcial estendendo lifecycle clássico) são genuinamente disparáveis. Operador rejeitou via F10 Opção (c) "refinar ADR-052"; tactical-only nesta onda é decisão consciente do operador, NÃO invariante doutrinal. Se pattern recorrer em onda futura (≥1 nova batch de consolidados Proposto-shipped após Onda Promoção), gatilho ADR-034 cond 4 + cond 5 dispara — pode codificar via ADR sucessor parcial de ADR-034 ou sub-modo de ADR-052 (recodificar após próxima instância empírica sem espera adicional).

**Risco a vigiar:** se design-reviewer flagrar gap doutrinário grave (ex.: promoção sem ADR codificando critério é antipattern), absorção/cutucada pré-commit conforme ADR-053 § Decisão (c).

**Sinal de saúde:** doc-reviewer deve absorver edits caminho-único — operação mecânica uniforme sem trade-off editorial. Se findings ≥3, sinal de que critério precisa codificação imediata via ADR (não diferida).

## Decisões absorvidas

- Plano § Verificação end-to-end item 4: substituído pipe `grep | grep` (que verifica linha-a-linha sem garantir presença em § Decisão) por `awk` extraindo seção semantica (`awk '/^## Decisão/,/^## (Consequências|Alternativas)/'`) — verifica que match ADR-009 está dentro de § Decisão de ADR-048, não em § Origem/§ Contexto (caminho-único).
- Plano § Verificação end-to-end item 7: substituída verificação trivial ("Charter inalterado" testa coisa que o próprio plano garante por construção) por verificação inversa de drift transversal (`git diff main --name-only docs/decisions/` → apenas 7 paths listados); slot usado para invariante estrutural mais valioso (caminho-único).
- Plano § Resumo da mudança (após tabela): adicionada nota sobre limiar de critério (3) — ADR-052 satisfaz com 1 referência (CLAUDE.md bullet) enquanto outros 6 ADRs aparecem em ≥2 docs vivos; caso registrado para evitar precedente em ondas futuras (caminho-único).
- Plano § Contexto último parágrafo: substituída referência específica a "ADR-053 § Decisão (d) mirror runtime" (ADR vive em branch separado pré-merge desta onda — link rot em main entre Onda Promoção e Onda I) por enunciado independente ("invariante editorial análogo ao mirror runtime aplicado em ondas precedentes") — plano fica auto-suficiente (caminho-único).
- Plano § Notas operacionais penúltimo parágrafo: refinado tactical-only — caracterização "≥3 futuros consolidados Proposto-shipped" corrigida ("esta onda É 7 instâncias"); adicionado reconhecimento explícito de gatilho ADR-034 cond 4+5 disparável + decisão consciente do operador via F10 (tactical-only NÃO é invariante doutrinal); recodificação após próxima instância empírica sem espera adicional (caminho-único).
- Plano § Notas operacionais: adicionada nota "Auto-bootstrap mecânico" explicitando que ADR-052 (definidor do critério modo (c)) e ADR-048 (alvo da verificação mecânica) são promovidos na mesma onda; critério mecânico passa a ser estritamente satisfeito a partir do merge; sem circularidade lógica (caminho-único).

## Pendências de validação

- **Critério 6 da § Verificação end-to-end (specification bug — falso-positivo lexical):** grep `"Substituído"` casa referências em § Origem dos consolidados (narrativa histórica "ADR-XXX marcado `Substituído`" sobre ADRs absorvidos — ex.: ADR-046:161 cita ADR-029 marcado Substituído; ADR-047:194 cita ADR-018/-025/-030; ADR-048:205 cita ADR-044; ADR-049:297 cita ADR-028/-039/-041; ADR-050:266 + ADR-051:229 reforçam que nenhum dos absorvidos é Substituído). Verificação corrigida durante gate final via `grep "^\*\*Status:\*\* Substituído"` (vazio confirmado — Status field puro). Refinar plano canônico: prefixar critério com `^\*\*Status:\*\*` para discriminar Status field vs body text. Sem impacto material — promoção em batch executou corretamente; apenas critério end-to-end como escrito gerou falso-positivo absorvível inline.
