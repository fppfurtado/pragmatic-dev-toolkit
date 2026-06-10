---
name: curate-backlog
description: Manutenção editorial periódica do BACKLOG.md (4 heurísticas detectivas + salvaguarda worktree-probe), preview-first, non-destructive. Use quando o mantenedor quer varrer o backlog inteiro fora do fluxo de sessão (/next).
disable-model-invocation: false
roles:
  required: [backlog]
  informational: [plans_dir]
---

# curate-backlog

Manutenção editorial periódica do papel `backlog` (default `BACKLOG.md`). Aplica 4 heurísticas cumulativas, oferece preview com mutações propostas, e aplica via commit unificado ou defere via NOTES.md signal queue conforme estado de concorrência. **Não-destrutivo, preview-first, sob demanda.**

Mecânica per [ADR-057](../../docs/decisions/ADR-057-curate-backlog-manutencao-editorial-periodica.md). Skill irmã de `/archive-plans` (ADR-022) — mesma natureza editorial, escopo `BACKLOG.md` em vez de `docs/plans/`.

## Argumentos

Sem argumentos. Skill é low-frequency operator-initiated; toda invocação é preview-first.

## Pré-condições

1. **Working tree limpo** (`git status --porcelain` vazio). Curagem mistura mal com mudança não-revisada; bloquear preserva isolamento (mesmo pattern de `/archive-plans`).
2. **Não bloqueia por branch** — operador pode legitimamente rodar `/curate-backlog` em qualquer branch; a salvaguarda worktree-probe (passo 2) cobre concorrência mecanicamente.

## Passos

### 1. Coletar contexto

Ler na íntegra:

- `BACKLOG.md` (papel `backlog`; em modo `local`, `.claude/local/BACKLOG.md`).
- `.claude/local/NOTES.md` se existir.

NOTES.md ausente → H4 vira no-op silente (sem fonte de sinais).

### 2. Salvaguarda de concorrência (worktree-probe)

`git worktree list --porcelain` → classificar:

- **Só worktree main** (`main-só`): mutações cross-seção em `BACKLOG.md` autorizadas. ADR-049 § Decisão (a) preservado (sem concorrência multi-PR).
- **≥1 worktree adicional ativa** (`worktree-adicional`): mutações cross-seção **deferidas** via NOTES.md signal queue (formato no passo 6).

Estado classificado vira metadata do preview (passo 4) e do gate (passo 5).

### 3. Executar 4 heurísticas cumulativas

Acumular findings com (categoria, linha-do-BACKLOG, ação proposta). Sem findings em todas as heurísticas → skip silente para passo 7 (cutucada de descoberta + done).

#### 3.1. Gatilhos temporais vencidos (predicado mecânico)

Para cada linha em `## Próximos`, casar regex de marca temporal:

- `até YYYY-MM-DD` ou `deadline YYYY-MM-DD` — extrair data literal.
- `T+Nd` (N inteiro) — calcular data: data do commit de adição (via pickaxe `git log -S "<linha>" --diff-filter=A --reverse | head -1`) + N dias.

Comparar contra `date +%Y-%m-%d`. Data passou → finding `Gatilho temporal vencido`, ação `revisar prioridade ou mover para ## Concluídos`.

Sem marca temporal → linha não gera finding desta heurística.

#### 3.2. Redação stale (heurística semântica)

Para cada linha em `## Próximos`, julgamento do agente runtime via Read + cross-ref `git log -S "<termo>"` quando aplicável. Sinais alvo:

- Paths/skills/agents que não existem mais em main (probe via `test -e <path>` ou `grep -F "<nome>" skills/ agents/`).
- ADRs marcados `Substituído` em § Status (cross-ref via `grep -E "^\*\*Status:\*\* Substituído" docs/decisions/ADR-NNN-*.md`).
- Números desatualizados (saldos, contagens, percentuais) — comparar com estado git corrente quando linha cita métrica.

Finding `Redação stale`, ação `refinar texto OR remover linha`. **Limitação reconhecida no ADR-057:** julgamento semântico do agente; spec leve por design (regex mecânica produziria falsos positivos massivos).

#### 3.3. Mergeable items (heurística semântica com anti-spam)

1. Tokenizar cada linha de `## Próximos` em substantivos (heurística por capitalização + ignore stop-words PT-BR).
2. Calcular frequência de cada termo no BACKLOG inteiro.
3. **Anti-spam:** identificar top-20 termos mais frequentes (ex.: "plugin", "skill", "ADR", "BACKLOG", "toolkit"). Excluí-los do cálculo de overlap.
4. Para cada par de linhas, contar termos compartilhados pós-anti-spam. ≥3 → finding `Mergeable`, ação `consolidar em linha única`.

Apresentar pares no preview com termos compartilhados destacados; operador decide redação do merge se aceitar.

#### 3.4. NOTES.md sinais editoriais (informacional refinado)

Varredura textual de `.claude/local/NOTES.md` (scan completo na 1ª iteração). Sinais alvo:

- Menções de linha do BACKLOG como obsoleta/concluída ("já feito", "linha X cumprida", "cobrimos via Y").
- Deadlines vencidos capturados via `/note`.
- Work cross-projeto sinalizando convergência ou contradição com items registrados.

Findings desta heurística são **informacionais** — não geram ação direta no gate `Aplicar tudo`. Listados como **contexto** para operador inspecionar antes de decidir sobre H1-H3 (alinhado a ADR-054 § Decisão (a); NOTES.md mantém status non-role).

### 4. Apresentar preview estruturado

Reportar ao operador em formato compacto:

- **Estado da salvaguarda:** `main-só: mutações diretas` ou `worktree-adicional: mutações deferidas via NOTES.md` (literal).
- **H1 — Gatilhos temporais vencidos** (N findings): cada um como `BACKLOG.md:<linha>: <texto> [marca <data>] → <ação>`.
- **H2 — Redação stale** (M findings): cada um como `BACKLOG.md:<linha>: <texto curto> → <ação>; cross-ref: <evidência>`.
- **H3 — Mergeable items** (K pares): cada par como `BACKLOG.md:<linha-A> + <linha-B>: termos compartilhados <termo1, termo2, termo3> → consolidar`.
- **H4 — NOTES.md sinais (contexto informacional)** (J sinais): cada um como `NOTES.md:<linha>: <trecho> ← relaciona BACKLOG.md:<linha>`.
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

Operador invocando `/curate-backlog` em estado `main-só` com entries `## curate-backlog deferred YYYY-MM-DD` existentes em NOTES.md:

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
- **Não interpretar findings de H4 como acionáveis** — H4 é contexto informacional, não decisional; tratá-los como ação direta viola ADR-054 § Decisão (a) (NOTES.md non-role).
