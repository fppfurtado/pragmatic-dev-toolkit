# Plano — Wiring de ADR-064: gate-com-executor-validacao em /run-plan §3.2 e /session-audit

## Contexto

Materialização do ciclo runtime de [ADR-064](../decisions/ADR-064-gate-com-executor-validacao-2-sites.md) — categoria nova `gate-com-executor-validacao` wired em 2 sites paralelos (`/run-plan §3.2` gate manual + `/session-audit` passo 6). Pattern emergeu empiricamente em 2 instâncias da sessão CC `next-2026-06-14` (Lotes 2/3/4 do `/session-audit` + pivôt do `/next`) + auto-relato do operador como hábito frequente.

**Linha do backlog:** plugin: codificar `gate-com-executor-validacao` em `/run-plan §3.2` e `/session-audit` — categoria nova wired em 2 sites paralelos via procedure shared `docs/procedures/gate-com-executor-validacao.md` per [ADR-064](../decisions/ADR-064-gate-com-executor-validacao-2-sites.md).

**ADRs candidatos:** ADR-049 § Decisão (b) (gate manual mecânica de `/run-plan` estendido de 2 para 3 opções condicional sobre baseline binário `Validei` / `Falhou — descrever`), ADR-061 § Decisão (scope `/session-audit` estendido com tipo derivado `executar_validacao_pendente`; ADR-061 § Limitações tem tensão reconhecida em ADR-064 § Contexto), ADR-064 (apex desta wave), ADR-002 § Decisão (anti-gate-cerimônia honrado via 3ª opção condicional).

## Arquivos a alterar

### Bloco 1 — Criar procedure shared docs/procedures/gate-com-executor-validacao.md {reviewer: doc}

- `docs/procedures/gate-com-executor-validacao.md` (criar)

Conteúdo canonical (fonte de verdade referenciada por Blocos 2 e 3):

1. **Heurística de classificação** [executável-pra-mim] vs [exige-operador]:
   - **[executável-pra-mim]** — cenário cobre por Bash/Read/grep/AST parse/reviewer subagent retroativo/fixture mecânico controlado. Substância concreta: comando shell, padrão grep, invocação de reviewer, comparação textual.
   - **[exige-operador]** — UI interaction (clicar, navegar), dado real de produção (volume, latência, integração externa), business judgment (avaliação subjetiva de UX), sistema externo controlado pelo operador (TJPA real, Bitbucket, etc.).
   - **[ambíguo]** → cláusula default-conservadora → classificar como **[exige-operador]** (preserva consent + visibilidade da fronteira).

2. **Cláusula blast-radius compartilhado**: mutação remota (push, `gh release create`, `glab issue create`, `glab issue close`, e quaisquer comandos com efeito imediato fora da worktree corrente) **nunca** entra no escopo [executável-pra-mim] — classificar como [exige-operador] independente de "executável tecnicamente". Preserva ADR-049 § Decisão (a) + bullet "blast-radius compartilhado" em CLAUDE.md.

3. **Formato canonical do reporte de classificação** (1 bullet por cenário, antes do enum/cutucada):
   ```
   - [executável] Cenário N: <texto curto>. Razão: <heurística aplicada — ex.: "smoke programático via Bash grep">.
   - [exige-operador] Cenário M: <texto curto>. Razão: <heurística aplicada — ex.: "UI interaction explícito">.
   ```

4. **Cláusula de execução** (quando opção `Executar [executável]` escolhida):
   - Rodar cenários [executável] em sequência (paralelo onde tool calls permitem; serial onde há dependência ordenada).
   - Reportar verdict per cenário (PASS / FAIL / CLEAN / N findings / erro literal).
   - Deferir cenários [exige-operador] explicitamente: "Defere para sua validação manual: cenário N, M".

5. **Consumidores**: `skills/run-plan/SKILL.md §3.2` (gate manual), `skills/session-audit/SKILL.md` (passo 6 tipo derivado `executar_validacao_pendente`). Mudança da heurística vive aqui — SKILL.mds referenciam o procedure como fonte canonical (pattern paralelo a `docs/procedures/cutucada-descoberta.md` e `docs/procedures/forge-auto-detect.md`).

### Bloco 2 — Wire /run-plan §3.2 gate manual condicional {reviewer: prompt}

- `skills/run-plan/SKILL.md`

Localizar `§3.2` (gate manual de validação) e estender:

1. **Antes do enum:** ler `## Verificação manual` do plano (se presente). Para cada bullet, classificar via heurística do `docs/procedures/gate-com-executor-validacao.md`. Reportar classificação no formato canonical do procedure (1 bullet por cenário com tag explícita).
2. **Cláusula condicional do enum:** baseline atual é binário (`Validei (Recommended)` / `Falhou — descrever`). Se classificação detecta ≥1 cenário [executável], enum apresenta 3 opções com `Executar o que for executável pra mim (Recommended)` como 3ª. Se 0 [executável], enum mantém binário original (sem 3ª opção — preserva ADR-002 § Decisão anti-gate-cerimônia).
3. **Quando 3ª opção escolhida:** executar cenários [executável] em sequência conforme cláusula de execução do procedure; reportar verdict per cenário; deferir [exige-operador] explicitamente; re-dispatch do enum binário original (`Validei` / `Falhou — descrever`) para o operador decidir após validação do subset deferido.
4. **Sem `## Verificação manual` no plano:** classificação skip silente; enum binário inalterado (pattern atual preservado).

Adicionar bullet em `## O que NÃO fazer` da SKILL: "Não classificar cenários como [executável-pra-mim] que mutam state remoto (push, gh release, glab issue) — cláusula blast-radius do procedure preserva fronteira."

### Bloco 3 — Wire /session-audit tipo derivado executar_validacao_pendente {reviewer: prompt}

- `skills/session-audit/SKILL.md`

Estender passo 6 "Aplicar capturas" + passo 2 análise transcript:

1. **Heurística de detecção em passo 2 análise:** adicionar item ao checklist — "Planos com `## Pendências de validação` cuja sessão tocou direta ou indiretamente (via `/run-plan`, refs explícitas em prosa, ou trace de file edits em paths do plano)". Detecção independente do enum formal 4-tipos.
2. **Tipo derivado `executar_validacao_pendente`** (extensão informal — não entra no enum formal 4-tipos do passo 5): para cada pendência detectada, classificar bullets via heurística do `docs/procedures/gate-com-executor-validacao.md`.
3. **Passo 5 relatório:** addendum "**Pendências de validação executáveis**" listando bullets classificados [executável] / [exige-operador] no formato canonical do procedure. Bloco omitido se 0 pendências detectadas ou 0 [executável].
4. **Cutucada batched do passo 5** ganha 4ª opção: `Executar [executável] também` (além de `Aplicar tudo` / `Aplicar parcial (Other)` / `Cancelar`). Opção presente APENAS quando addendum tem ≥1 [executável] (cláusula condicional paralela ao Bloco 2 anti-gate-cerimônia).
5. **Passo 6 aplicar** para tipo derivado: rodar cenários [executável] conforme cláusula de execução do procedure; reportar verdict; marcar pendência como `Encerrada YYYY-MM-DD` no plan body (mesma mecânica usada manualmente em commits `e2e135f` + `10c256c` desta sessão CC). Cenários [exige-operador] deferidos explicitamente para revisão humana subsequente.

Adicionar bullet em `## O que NÃO fazer` da SKILL: "Não classificar cenários como [executável-pra-mim] que mutam state remoto (push, gh release, glab issue) — cláusula blast-radius do procedure preserva fronteira." (Paralelo ao Bloco 2.)

Adicionar parágrafo em SKILL § Contexto reconhecendo ADR-064 abre exceção controlada para ADR-061 § Limitações ("side-effects executados fora de escopo") via tipo derivado `executar_validacao_pendente`; mutação restrita a `Encerrada YYYY-MM-DD` no plan body, não cobre commits/mutações remotas.

### Bloco 4 — Cross-refs em CLAUDE.md + README.md inventário {reviewer: doc}

- `CLAUDE.md`
- `README.md`

`CLAUDE.md § Editing conventions`: adicionar bullet cross-ref ADR-064 no estilo dos bullets existentes para ADR-063/ADR-062/ADR-061 — formato canonical do toolkit (1 frase descritiva + link ADR + 1 frase rationale).

`README.md`: estender 2 entries do inventário (linha do `/run-plan` + linha do `/session-audit`) com **gabarito explícito target-audience pré-adoção** per ADR-051 § Decisão (b) (framing descritivo de benefício/uso, vocabulário do consumer pré-adoção decidindo se instala, NÃO mecânica interna). Gabaritos canonical (texto exato a inserir após a descrição existente da skill respectiva):

- Para entry de `/run-plan`: "Quando o plano enumera cenários de validação manual que são programaticamente verificáveis (smoke, fixture, comparação textual), `/run-plan` oferece executá-los pelo agente e defere os demais para validação humana — reduzindo fricção quando o subset mecânico é cobrível sem interação."
- Para entry de `/session-audit`: "Quando detecta planos com pendências de validação contendo cenários executáveis programaticamente, `/session-audit` oferece executá-los e marcar como concluído no plano — fechando o ciclo de validação pós-execução sem requerer captura manual pelo operador."

Reviewer `doc-reviewer` avalia consistência de framing (descritivo, target-audience pré-adoção, sem vocabulário mecânico interno). Sem mudança de fluxo de invocação.

## Verificação end-to-end

1. `test -f docs/procedures/gate-com-executor-validacao.md && echo OK` retorna `OK` (Bloco 1).
2. `grep -c "gate-com-executor-validacao\.md\|Executar o que for executável" skills/run-plan/SKILL.md` retorna ≥2 (referência ao procedure + texto da opção; Bloco 2).
3. `grep -c "gate-com-executor-validacao\.md\|executar_validacao_pendente\|Pendências de validação executáveis" skills/session-audit/SKILL.md` retorna ≥3 (Bloco 3).
4. `grep -c "ADR-064" CLAUDE.md` retorna ≥1 (Bloco 4 — CLAUDE.md cross-ref).
5. `grep -c "Executar o que for executável\|executar_validacao_pendente" README.md` retorna ≥1 (Bloco 4 — README inventário refletindo nova opção).
6. `grep -c "^## Status$" docs/plans/wiring-adr-064-gate-com-executor-validacao.md` retorna `0` pós-`/run-plan §3.4` done (header `## Status` removido literalmente — não apenas conteúdo esvaziado; alinhado a ADR-060 § Wiring nas skills).

## Verificação manual

Smoke comportamental em consumer após `/reload-plugins`:

- **C1: Plano com `## Verificação manual` carregando 3 cenários (1 smoke programático + 1 fixture mecânico + 1 UI test).** Esperado em `/run-plan §3.2` gate manual:
  - Antes do enum: relatório de classificação reportado no formato canonical do procedure — cenário 1 [executável], cenário 2 [executável], cenário 3 [exige-operador].
  - Enum apresenta 3 opções (`Validei (Recommended)` / `Falhou — descrever` / `Executar o que for executável pra mim (Recommended)`). Cláusula condicional kicks in — terceira opção presente porque ≥1 [executável] detectado; Recommended pela presença de subset executável.
  - Operador escolhe `Executar o que for executável` → executor roda smoke + fixture, reporta verdict, defere UI test explicitamente.
  - Re-dispatch do enum binário original (`Validei` / `Falhou — descrever`) para operador decidir após validar o cenário 3 deferido.

- **C2: Plano com `## Verificação manual` carregando 1 cenário (UI test puro).** Esperado:
  - Antes do enum: classificação reporta 0 [executável] + 1 [exige-operador].
  - Enum apresenta APENAS o binário original (`Validei (Recommended)` / `Falhou — descrever`) — sem 3ª opção condicional, preserve pattern atual da skill.
  - Anti-gate-cerimônia per ADR-002 demonstrado mecanicamente.

- **C3: `/session-audit` detectando plano com `## Pendências de validação`.** Esperado:
  - Heurística do passo 2 análise detecta plano tocado pela sessão.
  - Relatório inclui addendum "**Pendências de validação executáveis**" com classificação [executável] / [exige-operador] discriminados.
  - Cutucada batched ganha 4ª opção `Executar [executável] também` (presente porque ≥1 [executável] detectado).
  - Operador escolhe → executa, reporta verdict, marca pendência como `Encerrada YYYY-MM-DD` no plan body.

- **C4: Cenário ambíguo na classificação (smoke OR UI test depending on interpretation).** Esperado:
  - Cláusula default-conservadora do procedure → classificar como [exige-operador].
  - Reporte explicita o motivo da classificação (frase canonical do procedure).

- **C5: Plano com cenário que muta state remoto (`gh release create` / `glab issue close`).** Esperado:
  - Cláusula blast-radius do procedure → classificar como [exige-operador] independente de "executável tecnicamente".
  - Operador valida manual (preserva blast-radius compartilhado).
  - Mesmo bullet em `## O que NÃO fazer` de ambos SKILL.mds reforça enforcement.

- **C6: `/session-audit` sem pendências de validação detectáveis.** Esperado:
  - Addendum "**Pendências de validação executáveis**" omitido do relatório.
  - Cutucada batched mantém 3 opções (sem 4ª opção condicional).

- **C7: Tensão ADR-061 § Limitações reconhecida.** Esperado:
  - SKILL `/session-audit` § Contexto carrega parágrafo reconciliando expansão (mutação restrita a `Encerrada YYYY-MM-DD`, não cobre commits/mutações remotas).
  - Edits dos planos via tipo derivado limitam-se a esse marker — gate ainda preserva escopo declarado de ADR-061 sobre commits e mutações remotas.

## Pendências de validação

- Smoke comportamental real dos cenários C1-C6 do `## Verificação manual` pós-`/reload-plugins` em sessão CC nova com fixtures controladas: plano dummy com 3 cenários mistos (smoke + fixture + UI test) para C1 + C4 + C5; plano dummy com 1 UI test puro para C2; transcript real com /session-audit detectando pendências para C3 + C6. C7 (tensão ADR-061 reconhecida em SKILL § Contexto + marker restrito a `Encerrada YYYY-MM-DD`) já validado mecanicamente nesta execução do `/run-plan §3.2` via grep — 3 invariantes textuais confirmados em `skills/session-audit/SKILL.md:16` + linha 125 + ref linha 135.
- Critério end-to-end #5 do plano misaligned com F5→(b) absorvida: grep `"Executar o que for executável\|executar_validacao_pendente" README.md` retorna 0 porque F5→(b) escolhida no /triage redirecionou para gabarito target-audience pré-adoção per ADR-051 § Decisão (b) (sem vocabulário mecânico interno). Refinar critério: ou substituir por grep de strings target-audience efetivamente inseridas ("programmatically executable scenarios", "fixture-based checks"), ou eliminar (não há check mecânico que valide framing constraint subjetivo — pertence ao doc-reviewer, não ao gate automático).
- §3.2 wiring de Bloco 2 carrega dois `(Recommended)` na 3ª opção em leitura literal: SKILL §3.2 wired diz "baseline binário é `Validei (Recommended)` / `Falhou — descrever`; ≥1 cenário [executável] detectado → enum apresenta 3 opções adicionando `Executar o que for executável pra mim (Recommended)` como 3ª". Refinamento esperado per CLAUDE.md AskUserQuestion mechanics (Recommended dinâmico per contexto): quando ≥1 [executável], `(Recommended)` transfere para "Executar..." e drop de Validei; quando 0 [executável], "Validei (Recommended)" preservado no binário. Refinar SKILL §3.2 prose para explicitar a transferência dinâmica.
- §3.4 do SKILL run-plan prescreve "revisor `code` cobre os 2 edits" no bloco extra unificado (BACKLOG mark + remover `## Status`). Mas ambos são editorial puro (1 bullet + 3 linhas removidas), sem código para code-reviewer (YAGNI rubric) operar. Reavaliar: (a) refinar §3.4 para usar `doc-reviewer` (faz sentido editorial); (b) explicitar skip silente quando edits são puramente editorial; ou (c) manter como cinto de segurança (análogo ao bullet anti-blast-radius absorvido em Bloco 2 com mesma justificativa de defesa em profundidade).

## Decisões absorvidas

ADR-064 (pass 1, `/new-adr` design-reviewer):

- § Origem (Override bullet): promoted to dedicated § Override do critério N=3 section parallel to ADR-057/-061/-062/-063 (caminho-único).
- § Trade-offs: added empirical calibration line based on Lotes 2/3/4 of sessão CC `next-2026-06-14` (100% scenarios classified as [executável] without ambiguity) and tensão "alinhamento empírico vs cobertura ampla" (caminho-único).
- Added § Auto-aplicação per ADR-034 with cond 1-5 mapping (NÃO APLICA: 1+2+3; APLICA: 4 categoria nova + 5 sucessor parcial dupla) parallel to ancestor ADRs (caminho-único).

Plano (pass 2, `/triage` design-reviewer):

- F1 baseline correction: ADR-064 + plan baseline corrected from imagined 3-options enum (`Tudo OK` / `Encerrar` / `Eu valido manual`) to actual binary (`Validei` / `Falhou — descrever`) per skills/run-plan/SKILL.md:144; extension recalculated as 2→3 conditional (caminho-único).
- § Verificação end-to-end critério 6 refined from awk-could-false-positive-on-empty-body to `grep -c "^## Status$" returns 0` (literal header absence per ADR-060 § Wiring) (caminho-único).
- § Verificação end-to-end critério 7 ("Status Aceito post-merge") eliminated — workflow ADR padrão implícito; não pertence ao gate executable de /run-plan §3.1 (caminho-único).
- ADR-064 § Decisão "Mecânica compartilhada cross-site": added explicit rebate-of-alternative paragraph (alternative (b) inline duplicado + refactor pós-3º site rejected; drift cost > procedure cost now) (caminho-único).
