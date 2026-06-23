# Plano — Gate verificar-estado-antes-de-materializar (NOTES.md-sourced) em session-audit/triage

## Status

Pendente

## Contexto

Captura originada de entry pré-existente do `.claude/local/NOTES.md` (store que persiste e decai, [ADR-054](../decisions/ADR-054-bridge-cross-project-note-consolidado.md)) pode virar issue-fantasma: `/session-audit` (`captura_backlog`) e `/triage` (linha de backlog) materializam o gap sem re-verificar se a pendência ainda é real. Incidente kl-score 2026-06-23: 2 issues forge criadas de entries stale, fechadas no `/next` seguinte sem código. Decisão e doutrina em [ADR-069](../decisions/ADR-069-gate-verificacao-estado-antes-materializar-captura-notes.md).

Este plano materializa o gate: shared procedure novo (`verify-state-before-materialize.md`, paralelo a `gate-com-executor-validacao.md`) + wiring nas 2 skills consumidoras + bullet em CLAUDE.md.

**ADRs candidatos:** ADR-069 (decisão e doutrina — criado neste /triage; design-reviewer prioriza), ADR-064 (gate-com-executor — modelo do shared procedure cross-skill), ADR-054 (NOTES.md store append-only — invariante preservado via append da baixa)
**Linha do backlog:** #150: session-audit/triage: verificar estado real antes de materializar captura_backlog de entry pré-existente do NOTES.md

## Resumo da mudança

- **Shared procedure** `docs/procedures/verify-state-before-materialize.md`: heurística de probe por tipo de artefato citado (commit→`git log --grep`/`git ls-files`; arquivo→`grep`; issue→`gh issue view`) + cláusula de baixa-via-append no NOTES.md + cláusula default-conservadora (indeterminado → filar). Fonte canonical cross-skill; skills referenciam, não duplicam.
- **`/session-audit`**: no passo 6 (aplicar `captura_backlog`), antes de materializar gap cuja `citação_transcript` aponta para entry pré-existente do NOTES.md, consultar o procedure. Já-resolvido → append da baixa + pular filing.
- **`/triage`**: no passo 2/4, antes de filar linha de backlog originada de entry do NOTES.md (lido no step 1), consultar o procedure. Mesma mecânica.
- **`CLAUDE.md § Editing conventions`**: bullet documentando ADR-069 (paralelo aos bullets dos ADRs recentes).

Decisão-chave (bifurcação resolvida): **baixa via append** de nova entry (não mutação inline) — preserva invariante append-only de ADR-054 (per ADR-069 § Alternativas). Escopo: apenas capturas NOTES.md-sourced; substância gerada na sessão corrente fila direto sem probe.

Fora do escopo: probe de capturas não-NOTES-sourced; mutação inline do NOTES.md; cobertura de side-effects já executados (issue já criada).

## Arquivos a alterar

### Bloco 1 — `docs/procedures/verify-state-before-materialize.md` (novo shared procedure) {reviewer: prompt}

`{reviewer: prompt}` é override explícito (F4 do design-reviewer): o path `docs/procedures/*.md` está fora do path-set de auto-trigger (default seria `doc`), mas o procedure é prompt-substance algorithmic-bearing (heurística de probe + cláusulas de ramo), paralelo a `gate-com-executor-validacao.md`.

- Criar o procedure com: (1) § Heurística de probe por tipo de artefato citado na entry; (2) § Cláusula de baixa-via-append (`Resolvido <data>: <evidência> — refere entry de <data>`); (3) § Cláusula default-conservadora (indeterminado → filar; `/next` é a rede a jusante); (4) § Escopo (só entries pré-existentes do NOTES.md); (5) § Consumidores (`session-audit` passo 6, `triage` passo 2/4). Estrutura paralela a `docs/procedures/gate-com-executor-validacao.md`.

### Bloco 2 — `skills/session-audit/SKILL.md` (wiring no passo 6) {reviewer: prompt}

- Passo 6, ramo `captura_backlog` modo arquivo: antes do `Edit` em `## Próximos`, quando a `citação_transcript` do finding aponta para entry pré-existente do NOTES.md, consultar `docs/procedures/verify-state-before-materialize.md`; já-resolvido → append da baixa + pular filing (reportar a baixa no done). Modo forge: o defer pra /triage (passo 1.5) já existe — o gate aplica em /triage. Adicionar bullet em `## O que NÃO fazer` se necessário (não probar capturas geradas na sessão corrente — fresh por construção). **Dependência cross-bloco (F2):** a corretude do caminho forge (defer pra /triage) depende do Bloco 3 cobrir capturas deferidas via `captura_backlog` — não só a feature-em-curso; senão a captura forge NOTES-sourced de session-audit escapa do gate em ambos os pontos.

### Bloco 3 — `skills/triage/SKILL.md` (wiring nos 2 sites de filing) {reviewer: prompt}

- Passo 4, **ambos os ramos que filam em `## Próximos`/forge** (F1 do design-reviewer): (a) linha da feature-em-curso originada de entry do NOTES.md (caminho sem plano); (b) **cada item fora-de-escopo emergido no passo 2** (SKILL.md §67/§97/§106) cuja origem é entry do NOTES.md lida no step 1 — **vetor mais provável** de captura NOTES-sourced em `/triage` (é o caminho do incidente kl-score #4/#5). Antes de gravar/criar issue em qualquer dos dois, consultar `docs/procedures/verify-state-before-materialize.md`; já-resolvido → append da baixa + pular o filing daquele item. Aplica em todos os modos do backlog (arquivo/forge/local) — o gate precede o canal (per ADR-069 § Limitações ordem com #145).

### Bloco 4 — `CLAUDE.md § Editing conventions` (bullet ADR-069) {reviewer: doc}

- Adicionar bullet curto documentando ADR-069 (gate verificar-estado-antes-de-materializar, shared procedure, escopo NOTES.md-sourced, baixa via append), paralelo aos bullets dos ADRs recentes na seção.

## Verificação end-to-end

Inspeção textual (`test_command: null`):

1. `ls docs/procedures/verify-state-before-materialize.md` → arquivo presente.
2. `grep -n "verify-state-before-materialize" skills/session-audit/SKILL.md` → ≥1 match (wiring passo 6).
3. `grep -n "verify-state-before-materialize" skills/triage/SKILL.md` → ≥1 match (wiring passo 2/4).
4. `grep -n "ADR-069" CLAUDE.md` → ≥1 match (bullet § Editing conventions com link correto).
5. `grep -c "append" docs/procedures/verify-state-before-materialize.md` → ≥1 (cláusula de baixa-via-append presente, não mutação inline).

## Verificação manual

Comportamental — exige sessão CC com NOTES.md contendo entry stale citável:

- **C1 — gate dispara, entry já resolvida:** NOTES.md com entry citando artefato já concluído (ex.: "commitar reports X" com `git ls-files` confirmando tracked). Rodar `/session-audit` ou `/triage` que materializaria a captura. Observar: probe roda, confirma resolvido, append da baixa no NOTES.md, filing pulado (sem issue/linha). 
- **C2 — gate dispara, entry ainda pendente:** entry citando artefato ausente. Observar: probe não confirma, filing segue normal.
- **C3 — entry indeterminada (sem artefato citável):** entry vaga. Observar: default-conservador, filing segue (sem probe inconclusivo barrar).
- **C4 — captura gerada na sessão (não NOTES-sourced):** observar que o gate NÃO dispara (fresh por construção, fila direto).
- **C5 — item fora-de-escopo NOTES-sourced em `/triage`** (F3): entry stale citável no NOTES.md → `/triage` que captura um item fora-de-escopo derivado dela (passo 2) → observar probe + baixa via append + filing do item pulado (exercita o vetor do incidente kl-score #4/#5, o site de filing mais provável de regressão).

## Pendências de validação

- [capture:validacao] Smoke comportamental C1-C5 pós-`/reload-plugins` em sessão CC com NOTES.md preparado (entry stale citável + entry pendente + entry vaga + item fora-de-escopo NOTES-sourced). Não exercitável na execução do `/run-plan` (depende do plugin recarregado + estado de NOTES.md controlado).

## Decisões absorvidas

- Bloco 3: expandido para cobrir os 2 sites de filing de `/triage` step 4 — linha-feature E itens fora-de-escopo do passo 2 (vetor do incidente kl-score), não só a feature (F1, caminho-único).
- Bloco 2: nota de dependência cross-bloco — corretude do caminho forge depende do Bloco 3 cobrir capturas deferidas via `captura_backlog` (F2, caminho-único).
- Bloco 1: registrado o motivo do override `{reviewer: prompt}` no procedure (prompt-substance algorithmic-bearing fora do path-set; F4, caminho-único).
- § Verificação manual: adicionado C5 (item fora-de-escopo NOTES-sourced em `/triage`) cobrindo o site de filing mais provável de regressão (F3, caminho-único).
