---
name: curate-backlog
description: Manutenção editorial periódica do BACKLOG.md (4 heurísticas detectivas + salvaguarda worktree-probe), preview-first, non-destructive. Use quando o mantenedor quer varrer o backlog inteiro fora do fluxo de sessão (/next).
disable-model-invocation: false
roles:
  required: [backlog]
  informational: [plans_dir]
---

# curate-backlog

Manutenção editorial periódica do papel `backlog` (default `BACKLOG.md`). Aplica 4 heurísticas cumulativas, oferece preview com mutações propostas, e aplica via commit unificado ou defere via signal queue (`.claude/local/NOTES.md`, local-fixed) conforme estado de concorrência. **Não-destrutivo, preview-first, sob demanda.**

Mecânica per [ADR-057](../../docs/decisions/ADR-057-curate-backlog-manutencao-editorial-periodica.md). Skill irmã de `/archive-plans` (ADR-022) — mesma natureza editorial, escopo `BACKLOG.md` em vez de `docs/plans/`.

## Argumentos

Sem argumentos. Skill é low-frequency operator-initiated; toda invocação é preview-first.

## Pré-condições

1. **Working tree limpo** (`git status --porcelain` vazio). Curagem mistura mal com mudança não-revisada; bloquear preserva isolamento (mesmo pattern de `/archive-plans`).
2. **Não bloqueia por branch** — operador pode legitimamente rodar `/curate-backlog` em qualquer branch; a salvaguarda worktree-probe (passo 2) cobre concorrência mecanicamente.

## Passos

### 1. Coletar contexto

**Em modo arquivo** (canonical ou `local`): ler na íntegra `BACKLOG.md` (papel `backlog`; em modo `local`, `.claude/local/BACKLOG.md`).

**Em modo `forge`** (`paths.backlog: forge`, per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md)): seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`. Output `gh` → `gh issue list --state open --search "no:assignee" --json number,title,body,createdAt --jq '.[]'`; output `glab` → `glab issue list --opened --not-assignee --output json | jq -r '.[] | {number: .iid, title, body: .description, createdAt: .created_at}'`. Output `no-detection` ou `unsupported-host` → **parar com erro explícito** orientando setup (`gh auth login` / `glab auth login` / `dnf install jq`) ou declarar `paths.backlog: null` ou path canonical (policy do caller per ADR-058 § (d)). Lista de issues retornada substitui o conteúdo de `## Próximos` no fluxo subsequente; cada item carrega identificador `#<número>: <título>` + body (consumido por H2/H3).

Ler também o store do role `annotations` (per [ADR-072](../../docs/decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md), ortogonal ao modo do backlog) para H4: backend `local`/ausente → ler `.claude/local/NOTES.md` se existir; `null` → H4 no-op silente; `logseq` → graceful-degrade (deferido a meta-bridge#41).

Store ausente (backend `local` sem arquivo, ou `null`/`logseq`) → H4 vira no-op silente (sem fonte de sinais).

### 2. Salvaguarda de concorrência (worktree-probe)

**Em modo arquivo** (canonical ou `local`): `git worktree list --porcelain` → classificar:

- **Só worktree main** (`main-só`): mutações cross-seção em `BACKLOG.md` autorizadas. ADR-049 § Decisão (a) preservado (sem concorrência multi-PR).
- **≥1 worktree adicional ativa** (`worktree-adicional`): mutações cross-seção **deferidas** via signal queue (formato no passo 6). A signal-queue grava sempre em `.claude/local/NOTES.md` (destino local-fixed, **fora do role** `annotations` — é mecanismo de coordenação de concorrência, não conteúdo de anotação; escopo (a) per [ADR-072](../../docs/decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md), separação física deferida a #157). Independe do backend declarado.

**Em modo `forge`**: salvaguarda **não aplica** — state vive em forge remoto idempotente, sem arquivo local concorrente para merge artifact (per ADR-058 § (g)). Classificação sempre vira `main-só` em modo forge (mutações remotas aplicáveis diretamente).

Estado classificado vira metadata do preview (passo 4) e do gate (passo 5).

### 3. Executar 4 heurísticas cumulativas

Acumular findings com (categoria, linha-do-BACKLOG, ação proposta). Sem findings em todas as heurísticas → skip silente para passo 7 (cutucada de descoberta + done).

#### 3.1. Gatilhos temporais vencidos (predicado mecânico)

**Em modo arquivo:** para cada linha em `## Próximos`, casar regex de marca temporal:

- `até YYYY-MM-DD` ou `deadline YYYY-MM-DD` — extrair data literal.
- `T+Nd` (N inteiro) — calcular data: data do commit de adição (via pickaxe `git log -S "<linha>" --diff-filter=A --reverse | head -1`) + N dias.

Comparar contra `date +%Y-%m-%d`. Data passou → finding `Gatilho temporal vencido`, ação `revisar prioridade ou mover para ## Concluídos`.

**Em modo `forge`:** para cada issue, casar regex de marca temporal em title+body (mesmas marcas `até YYYY-MM-DD` / `deadline YYYY-MM-DD` / `T+Nd`). Data de referência para `T+Nd` = `createdAt` da issue (já disponível no item; sem pickaxe). Data passou → finding `Gatilho temporal vencido` no `#<número>: <título>`, ação `revisar prioridade ou fechar issue`.

Sem marca temporal → linha/issue não gera finding desta heurística.

#### 3.2. Redação stale (heurística semântica)

Para cada linha em `## Próximos` (modo arquivo) ou para cada title+body de issue (modo `forge`), julgamento do agente runtime via Read + cross-ref `git log -S "<termo>"` quando aplicável. Sinais alvo:

- Paths/skills/agents que não existem mais em main (probe via `test -e <path>` ou `grep -F "<nome>" skills/ agents/`).
- ADRs marcados `Substituído` em § Status (cross-ref via `grep -E "^\*\*Status:\*\* Substituído" docs/decisions/ADR-NNN-*.md`).
- Números desatualizados (saldos, contagens, percentuais) — comparar com estado git corrente quando linha cita métrica.

Finding `Redação stale`, ação `refinar texto OR remover linha/issue`. **Limitação reconhecida no ADR-057:** julgamento semântico do agente; spec leve por design (regex mecânica produziria falsos positivos massivos). **Adicional em modo `forge`:** issues raramente carregam refs estruturais (paths/ADRs) — heurística é menos potente que markdown agrupado (limitação documentada em ADR-058 § Limitações).

#### 3.3. Mergeable items (heurística semântica com anti-spam)

1. Tokenizar cada linha de `## Próximos` (modo arquivo) ou cada title+body de issue (modo `forge`) em substantivos (heurística por capitalização + ignore stop-words PT-BR).
2. Calcular frequência de cada termo no escopo inteiro (BACKLOG.md ou lista de issues).
3. **Anti-spam:** identificar top-20 termos mais frequentes (ex.: "plugin", "skill", "ADR", "BACKLOG", "toolkit"). Excluí-los do cálculo de overlap.
4. Para cada par de linhas/issues, contar termos compartilhados pós-anti-spam. ≥3 → finding `Mergeable`, ação `consolidar em linha única OR fechar issue duplicada`.

Apresentar pares no preview com termos compartilhados destacados; operador decide redação do merge se aceitar. **Em modo `forge`:** similaridade por title funciona bem; por body é mais frágil (issues frequentemente têm body livre/conversacional). Limitação documentada em ADR-058 § Limitações.

#### 3.4. Sinais editoriais do store `annotations` (informacional refinado)

Varredura textual do store do role `annotations` resolvido no passo 1 (backend `local` → `.claude/local/NOTES.md`; `null`/`logseq` → H4 já é no-op por aquele passo, pular esta varredura). Scan completo na 1ª iteração. Sinais alvo:

- Menções de linha do BACKLOG como obsoleta/concluída ("já feito", "linha X cumprida", "cobrimos via Y").
- Deadlines vencidos capturados via `/note`.
- Work cross-projeto sinalizando convergência ou contradição com items registrados.

Findings desta heurística são **informacionais** — não geram ação direta no gate `Aplicar tudo`. Listados como **contexto** para operador inspecionar antes de decidir sobre H1-H3 (o store do role `annotations` é consumido aqui read-only — informacional neste consumidor; a classificação non-role de ADR-054 § Decisão (a) foi revisada para role por [ADR-072](../../docs/decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md), mas o caráter informacional de H4 permanece).

### 4. Apresentar preview estruturado

Reportar ao operador em formato compacto:

- **Estado da salvaguarda:** `main-só: mutações diretas` ou `worktree-adicional: mutações deferidas via signal queue (.claude/local/NOTES.md, local-fixed)` (literal).
- **H1 — Gatilhos temporais vencidos** (N findings): cada um como `BACKLOG.md:<linha>: <texto> [marca <data>] → <ação>`.
- **H2 — Redação stale** (M findings): cada um como `BACKLOG.md:<linha>: <texto curto> → <ação>; cross-ref: <evidência>`.
- **H3 — Mergeable items** (K pares): cada par como `BACKLOG.md:<linha-A> + <linha-B>: termos compartilhados <termo1, termo2, termo3> → consolidar`.
- **H4 — sinais de anotações (contexto informacional)** (J sinais; só emitido sob backend `local`): cada um como `<store>:<linha>: <trecho> ← relaciona BACKLOG.md:<linha>` (`<store>` = backend resolvido, ex.: `.claude/local/NOTES.md`).
- **Resumo final:** `H1: N | H2: M | H3: K (pares) | H4: J (info)`.

H4 listado separado dos demais — operador entende que é contexto, não ação aplicável diretamente.

### 5. Gate `AskUserQuestion`

Header `Curate`, opções:

- **`Aplicar tudo`** — `description`: `aplica N+M+K mutações de H1+H2+H3 (H4 não tem ação direta); commit unificado.`
- **`Aplicar parcial`** — `description`: `desce em sub-gate por categoria (H1/H2/H3) com Aplicar/Pular cada uma.`
- **`Cancelar`** — `description`: `zero mutações, zero commit.`

Sem `Recommended` — operador decide após ver preview; ambos `Aplicar tudo` e `Aplicar parcial` são legítimos. H4 nunca aparece no gate (informacional).

### 6. Aplicar

**Caminho `main-só` (mutações diretas):**

**Em modo arquivo:**

1. Para cada finding aceito, mutar `BACKLOG.md`:
   - H1 (move): remover linha de `## Próximos`, adicionar topo de `## Concluídos`.
   - H2 (refinar): edit cirúrgico in-place; H2 (remover): deletar linha.
   - H3 (merge): substituir o par por uma única linha consolidada (operador redige; skill propõe esqueleto via combinação dos termos compartilhados).
2. Commit unificado:

   ```
   chore(backlog): editorial curation — <N> refinements

   H1: <N1> moves Próximos→Concluídos
   H2: <N2> refinos/removes (stale)
   H3: <N3> merges
   ```

3. **Não pusha** — operador decide quando publicar (paralelo a `/archive-plans`).

**Em modo `forge`:**

1. Para cada finding aceito, mutação remota com **cutucada `AskUserQuestion` por issue** (header `Forge`, opções `Aplicar no forge` (Recommended) / `Cancelar (não aplicar)`) per ADR-058 § (e). `description` da opção `Aplicar no forge` carrega o(s) comando(s) concreto(s). Uma cutucada por issue:
   - H1 (gatilho vencido): em `gh`, `gh issue close <número> --reason completed --comment "<glosa>"` (close + comentário num único comando); em `glab`, dois comandos sequenciais — `glab issue note <número> --message "<glosa>"` então `glab issue close <número>` (CLI assimétrica: `glab issue close` não aceita `--comment`). Glosa cita marca temporal vencida.
   - H2 (refinar): `gh issue edit <número> --title "<novo>" --body "<novo>"` ou `glab issue update <número> --title "<novo>" --description "<novo>"`. Operador edita texto antes de confirmar; cutucada carrega proposta.
   - H2 (remover): fechar issue com semântica de "não vai ser feita". Em `gh`, `gh issue close <número> --reason "not planned" --comment "<glosa>"` (state_reason distinto de H1 completed). Em `glab`, issues fechadas não têm subclassificação (sem state_reason) — `glab issue note <número> --message "<glosa>"` então `glab issue close <número>`, glosa documenta motivo.
   - H3 (merge): fechar uma das issues do par com glosa "consolidado em #<número-mantida>" (gh: `--reason completed --comment "..."`; glab: `note + close` sequencial); opcionalmente editar a issue mantida via H2 mecânica para refletir merge.
2. Sem commit local (mutações já remotas). Skill apenas relata as N+M+K mutações aplicadas + N rejeições (cancelamentos da cutucada).
3. **Não pusha** — N/A em modo forge (sem commits locais).

**Caminho `worktree-adicional` (mutações deferidas):**

1. Escrever entry estruturada em `.claude/local/NOTES.md`. Formato:

   ```
   ## curate-backlog deferred YYYY-MM-DD
   - BACKLOG.md:<linha>: H1 move para ## Concluídos — texto: "<linha exata>"
   - BACKLOG.md:<linha>: H2 refinar — proposta: "<novo texto>"
   - BACKLOG.md:<linha>: H3 merge com BACKLOG.md:<linha-B> — proposta: "<linha consolidada>"
   ```

2. Commit unificado:

   ```
   chore(backlog): defer <N> editorial signals (worktree active)

   <N1> moves + <N2> refinos + <N3> merges deferidos
   ```

3. Próxima invocação de `/curate-backlog` em estado `main-só` lê essa entry, propõe aplicar as mutações deferidas (preview-first com cross-ref à data da deferral), commit unificado limpa a entry após aplicação.

### 7. Cutucada de descoberta

Executar conforme `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md` (emitir como última linha informacional antes de devolver controle). Skill nova traversa Resolution protocol step 3 para `backlog`; a cutucada cobre gap de configuração se `CLAUDE.md` ou o marker estiverem ausentes.

## Sub-fluxo: aplicar mutações deferidas

Operador invocando `/curate-backlog` em estado `main-só` com entries `## curate-backlog deferred YYYY-MM-DD` existentes na signal-queue. A signal-queue write/drain opera sempre em `.claude/local/NOTES.md` (local-fixed, **fora do role** `annotations` — independe do backend declarado; sob `null` não há no-op da queue, só do H4 read):

1. Skill lê entries pendentes; apresenta preview de cada entry (linhas propostas + data da deferral original).
2. Gate `AskUserQuestion` (header `Deferred`, opções `Aplicar pendentes` / `Aplicar pendentes + nova curagem` / `Cancelar`).
3. `Aplicar pendentes` → aplica mutações exatamente como descritas na entry; remove entry de NOTES.md; commit unificado `chore(backlog): apply <N> deferred editorial signals`.
4. `Aplicar pendentes + nova curagem` → aplica deferidas, executa novamente passos 3-5 sobre o estado pós-aplicação, gate consolidado.

## O que NÃO fazer

- **Não modificar `BACKLOG.md` quando `worktree-adicional` detectado.** A salvaguarda existe para preservar ADR-049 § Decisão (a) mecanicamente; bypass via flag é anti-padrão.
- **Não decidir prioridade entre items** — escopo de `/next`. Skill só registra/move/refina/merge baseado em sinais empíricos.
- **Não executar trabalho trivial inline** — heurística considerada e removida na 1ª iteração (per ADR-057 § Consequências › Limitações). Reabertura via gatilho concreto (≥3 instâncias auditadas).
- **Não pushar** — operador decide publicação. Skill não invoca `git push`.
- **Não adicionar items novos** — escopo de `/triage`.
- **Não interpretar findings de H4 como acionáveis** — H4 é contexto informacional, não decisional; tratá-los como ação direta fere o caráter read-only do consumo do role `annotations` aqui (per [ADR-072](../../docs/decisions/ADR-072-role-annotations-plugavel-backend-por-projeto.md), sucessor de ADR-054 § Decisão (a)).
