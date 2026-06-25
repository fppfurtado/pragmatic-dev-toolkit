# Plano — Separar signal-queue worktree-defer num arquivo dedicado

## Status

Pendente

## Contexto

Materializa o escopo (c) de [ADR-072](../decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md) (rastreado como #157): migrar a **signal-queue worktree-defer** de `.claude/local/NOTES.md` para um arquivo de coordenação dedicado (`.claude/local/defer-queue.md`), separando **fisicamente** o mecanismo de concorrência (ADR-057) do conteúdo de anotação (role `annotations`). A decisão estrutural "separar" já foi tomada em ADR-072 escopo (a); este plano é a implementação.

**Decisão de design (Q1, operador):** a **baixa-append do gate ADR-069 FICA no annotation store** — só o worktree-defer signal-queue migra. Razão: `docs/procedures/verify-state-before-materialize.md` §4 já enquadra a baixa como append no annotation store (semântica ADR-054 append-only, paralela a `captura_notes`); a baixa marca uma *annotation entry* como resolvida e é moot sob backend `null`/`logseq` (sem entries) — logo segue o backend do role, não a fila de coordenação. Isto **refina a fronteira** que a prose de ADR-072/skills descrevia ("signal-queue + baixa = coordenação"): apenas o worktree-defer é coordenação pura.

`verify-state-before-materialize.md` **não muda** (baixa permanece em NOTES.md). 0 entries `## curate-backlog deferred` ativas → cutover limpo (sem migração de dados).

**ADRs candidatos:** ADR-072 (escopo (c) materializado; fronteira refinada), ADR-057 (origem da signal-queue em NOTES.md — substrato muda), ADR-069 (baixa — fica, não migra).

**Linha do backlog:** #157: Separar signal-queue worktree-defer de NOTES.md num arquivo de coordenação próprio (escopo (c) do role annotations)

## Resumo da mudança

**Entra:** a signal-queue worktree-defer (entries `## curate-backlog deferred YYYY-MM-DD` de `/curate-backlog` write+drain + o defer de `captura_backlog` do `/session-audit`) passa a gravar/ler em `.claude/local/defer-queue.md` em vez de `.claude/local/NOTES.md`. Notas de fronteira nas skills + role contract refinadas para "worktree-defer signal-queue → `defer-queue.md`; baixa ADR-069 fica no annotation store".

**Fica de fora / inalterado:** a **baixa-append do gate ADR-069** (permanece em NOTES.md / backend do role, per Q1) — `verify-state-before-materialize.md` intacto. O conteúdo de anotação (`/note`, `captura_notes`, H4 read) inalterado.

**Decisões-chave:**
- **Baixa fica no annotation store** (Q1) — refina ADR-072: baixa é annotation-adjacent, não coordenação. Só o worktree-defer migra.
- **Nome do arquivo:** `.claude/local/defer-queue.md` (não `curate-queue.md` — `/session-audit` também defere; nome genérico reflete os 2 consumidores). Coberto por `.worktreeinclude` (`.claude/`) já existente.
- **Cutover limpo** — 0 entries ativas; sem lógica de migração nem leitura dual (old NOTES + new file).

## Arquivos a alterar

### Bloco 1 — `/curate-backlog`: signal-queue write+drain → `defer-queue.md` {reviewer: prompt}

- `skills/curate-backlog/SKILL.md`:
  - Linha 12 (sumário): "defere via signal queue (`.claude/local/NOTES.md`, local-fixed)" → "(`.claude/local/defer-queue.md`)".
  - Linha 42 (estado salvaguarda) + linha 98 (preview label): a signal-queue grava em `.claude/local/defer-queue.md` (não NOTES.md); refinar a nota de fronteira (escopo (c) **materializado**, não mais "deferido a #157").
  - Passo 6 caminho `worktree-adicional` (write, ~linha 151): escrever entry `## curate-backlog deferred` em `.claude/local/defer-queue.md`.
  - Sub-fluxo "aplicar mutações deferidas" (drain, ~linha 174-180): ler/remover entries de `.claude/local/defer-queue.md`.
  - H4 (read de sinais editoriais) **permanece** lendo o annotation store via role (inalterado — H4 é conteúdo de anotação, ortogonal à signal-queue).

### Bloco 2 — `/session-audit`: worktree-defer → `defer-queue.md`, baixa fica {reviewer: prompt}

- `skills/session-audit/SKILL.md`:
  - Passo 6 `captura_backlog` modo-arquivo (~linha 127): o defer worktree-adicional escreve em `.claude/local/defer-queue.md` (não NOTES.md). A **baixa-append do gate ADR-069 permanece em NOTES.md** (annotation store, per Q1) — não tocar.
  - Linha 136 (nota de fronteira consolidada): refinar para "worktree-defer signal-queue → `defer-queue.md` (coordenação, fora do role); baixa ADR-069 fica no annotation store (annotation-adjacent, segue o backend)". Escopo (c) materializado.

### Bloco 3 — `/triage`: reformular a fronteira baixa-vs-signal-queue no gate verify-state {reviewer: prompt}

- `skills/triage/SKILL.md` linha 95: o texto atual **agrupa baixa + signal-queue** na mesma categoria via `**também**` ("A baixa-append... escreve em `.claude/local/NOTES.md` — destino físico local-fixed **fora do role**... independente do backend. (A signal-queue... **também** permanece local-fixed, fora do role — #157)"). Isto é exatamente o bundling que Q1 desfaz. **Reformular** (não "confirmar"):
  - **Baixa:** reclassificar para o framing Q1 — "annotation store (annotation-adjacent), **segue o backend do role**" (remover "fora do role / independente do backend"). Coerente com Blocos 2/4 e com `verify-state §4` (append-only de ADR-054).
  - **Signal-queue:** dissolver o `**também**`; passa a "worktree-defer → `.claude/local/defer-queue.md` (coordenação, fora do role; escopo (c) materializado)".

### Bloco 4 — role contract + doutrina + README {reviewer: doc}

- `CLAUDE.md` linha 44 (role `annotations`): "The worktree-defer signal-queue use of `.claude/local/NOTES.md` ... physical split tracked as #157" → "...now lives in `.claude/local/defer-queue.md` (#157); the ADR-069 baixa-append stays in the annotation store (annotation-adjacent)".
- `CLAUDE.md` linha 102 (bullet ADR-057): "defer via NOTES.md como signal queue" → "defer via `.claude/local/defer-queue.md`".
- `README.md` linha 24 (`/curate-backlog`): "defer via a local-fixed signal queue in `.claude/local/NOTES.md`, outside the `annotations` role" → "...in `.claude/local/defer-queue.md`".

## Verificação end-to-end

- `grep -rn "deferred\|signal queue\|signal-queue" skills/curate-backlog/SKILL.md skills/session-audit/SKILL.md` aponta para `defer-queue.md`, não `NOTES.md`, nos sites de write/drain/defer.
- `grep -c "defer-queue" skills/curate-backlog/SKILL.md skills/session-audit/SKILL.md skills/triage/SKILL.md CLAUDE.md README.md` ≥ 1 em cada.
- **Baixa intacta (destino):** `grep -n "baixa.*NOTES.md\|append.*NOTES.md" skills/session-audit/SKILL.md skills/triage/SKILL.md docs/procedures/verify-state-before-materialize.md` ainda aponta NOTES.md (baixa não migrou); `git diff` não toca `verify-state-before-materialize.md`.
- **Baixa intacta (framing, pega o Finding 1):** nenhum arquivo varrido associa a baixa a "fora do role"/"independente do backend" — `grep -rn "independente do backend\|fora do role" skills/triage/SKILL.md skills/session-audit/SKILL.md` não co-ocorre com `baixa` na mesma cláusula (a baixa é "annotation-adjacent, segue o backend"; só a signal-queue é "fora do role").
- Nenhuma referência residual a escopo (c) como **deferido** (já materializado), cobrindo a frase real de cada site: `grep -rn "deferido a #157\|deferida a #157\|deferida a issue #157\|tracked as #157\|fora do role — #157" skills/ CLAUDE.md README.md` retorna 0. (Nota: `#157` **é retido intencionalmente** como cross-ref "materializado" em `CLAUDE.md` — ex.: `(#157)` — então `grep #157 == 0` global seria errado; verificar por frase-deferida, não por número.)

## Verificação manual

Surface comportamental (mecanismo de concorrência) → smoke pós-`/reload-plugins`:

- **D0 — pré-cutover (segurança, antes de aplicar o `/run-plan`):** confirmar `grep -c '## curate-backlog deferred' .claude/local/NOTES.md` == 0. Se houver entry pendente, **drená-la via `/curate-backlog` em estado main-só ANTES** do cutover — o drain pós-migração lê só `defer-queue.md`, então uma entry pendente em NOTES.md ficaria órfã (silenciosamente perdida). Baixo risco (store local, autor é o único consumidor), mas fecha o gap.
- **D1 — defer:** em estado `worktree-adicional` (≥1 worktree além da main), acionar `/curate-backlog` com finding H1/H2/H3 → entry `## curate-backlog deferred` é escrita em `.claude/local/defer-queue.md` (NÃO em NOTES.md); commit `chore(backlog): defer ...`.
- **D2 — drain:** em estado `main-só` com entry pendente em `defer-queue.md` → `/curate-backlog` lê do `defer-queue.md`, aplica, remove a entry de lá.
- **D3 — baixa intacta:** acionar gate ADR-069 (captura cuja origem é entry NOTES.md já-resolvida) → baixa segue escrita em `.claude/local/NOTES.md` (annotation store), não em `defer-queue.md`.
- **D4 — annotation inalterado:** `/note`, H4 read de `/curate-backlog`, `captura_notes` de `/session-audit` continuam em NOTES.md (backend local) — sem regressão da fatia ADR-072.

## Pendências de validação

- `[capture:validacao]` Smoke D0–D4 do `## Verificação manual` pós-`/reload-plugins` em sessão CC real com estado de worktree controlado — exige plugin recarregado + ≥1 worktree adicional para exercitar o defer; não exercitável na execução do `/run-plan`. Operador roda manual.

## Notas operacionais

- **`verify-state-before-materialize.md` fica intacto (Finding 4 do design-reviewer):** o procedure hardcoda `.claude/local/NOTES.md` para o read da entry-fonte e a baixa-append. Sob Q1 ("baixa = annotation store, segue o backend"), o path-literal é o annotation-store target — coerente, porque o gate só dispara sob backend `local` (moot sob null/logseq) e §4 já ancora a baixa em "append-only de ADR-054" (invariante do annotation store). Gap conceitual path-literal-vs-framing é pré-existente e aceitável, **não introduzido** por este plano. Não tocar o procedure.
- **`defer-queue.md` é append-created** (como NOTES.md) — sem bloco de criação dedicado; o primeiro write da signal-queue cria o arquivo. Coberto por `.worktreeinclude` (`.claude/`) já existente.
- **Ordem dos blocos:** os 4 são independentes (sites distintos). Atenção do reviewer: o fio condutor é "worktree-defer signal-queue → `defer-queue.md` (fora do role) / baixa ADR-069 → fica no annotation store (segue o backend)" — confundir os dois é o erro a vigiar (Finding 1 foi exatamente isso).

## Decisões absorvidas

- Bloco 3 (triage:95): reformular — reclassificar a baixa para "annotation-adjacent, segue o backend" + dissolver o `**também**` que agrupava baixa+signal-queue como "fora do role"; era "já correto, confirmar" no draft (caminho-único; resolvia contradição doc↔doc que o plano shiparia).
- Verificação end-to-end: adicionado check de **framing** da baixa (não só destino físico) + `triage` nos targets do grep + residual-#157 corrigido para frase-deferida (#157 é retido intencionalmente como cross-ref materializado em CLAUDE.md) (caminho-único).
- Verificação manual: adicionado **D0 pré-cutover** (drenar entry pendente em NOTES.md antes do cutover — senão fica órfã pós-migração) (caminho-único).
