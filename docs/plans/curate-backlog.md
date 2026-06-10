# Plano — skill `/curate-backlog` (manutenção editorial periódica do BACKLOG)

## Contexto

`/next` cobre **orientação de sessão** (top 3 candidatos para `/triage` a seguir). Não cobre manutenção editorial periódica do `BACKLOG.md` como um todo — varredura ampla que verifica gatilhos temporais vencidos (`T+Nd`, deadlines), refresh de redação stale (refs a estado superado), detecção de mergeable items (similaridade textual entre linhas), execução inline de items triviais (~5 min sem `/triage`). Pattern emergiu empiricamente em uso real (≥3 instâncias ad hoc não-registradas em projetos do ecossistema — operador confirmou override do critério N=3 explicitamente neste `/triage`).

`/archive-plans` é o precedente direto: editorial periódico, operator-initiated, preview-first, non-destructive (ADR-022). `/curate-backlog` é a skill irmã, mesma natureza, escopo `BACKLOG.md` em vez de `docs/plans/`.

Adicionalmente: NOTES.md (store informacional cross-session per ADR-054) é **fonte de dados curatorial ativa** — notas marcando linha como obsoleta, refs a items adjacentes em outros projetos, deadlines vencidos capturados via `/note` influenciam decisões editoriais. Estende uso informational de NOTES.md em `/next`/`/triage` para uso decisional explícito nesta skill.

**Termos ubíquos tocados:** n/a (`docs/domain.md` não materializado neste repo).

**ADRs candidatos:** ADR-022 (precedente direto de skill editorial periódica), ADR-036 (precedente de override de critério de codificação registrado em ADR novo), ADR-045 (filtro de admissão — categoria nova "manutenção editorial do BACKLOG"), ADR-049 (tensão com § Decisão (a) resolvida via salvaguarda worktree-probe), ADR-054 (NOTES.md informational store consumido sem alteração), ADR-046 (gatilho linha 219 — 6ª skill emissora).

**Linha do backlog:** plugin: skill de manutenção editorial do BACKLOG (full-scan, distinta de `/next`)

## Resumo da mudança

Cria **skill standalone `/curate-backlog`** (paralela a `/archive-plans`, não substitui `/next` nem mistura escopo). Preview-first, operator-initiated, sob demanda. ADR-057 codifica decisão estrutural.

**4 heurísticas cumulativas** (cada uma gera categoria de finding no preview; operador decide via gate `Aplicar tudo` / `Aplicar parcial` / `Cancelar`):

1. **Gatilhos temporais vencidos** (predicado mecânico). Marcas `até YYYY-MM-DD`, `deadline YYYY-MM-DD`, `T+Nd` (N dias relativos à data do commit de adição via pickaxe). Sinal: revisar prioridade ou mover para Concluídos.
2. **Redação stale** (heurística semântica). Refs a estado superado — paths renomeados, ADRs Substituídos, skills extintas, números desatualizados. Detecção via judgment do agente + cross-ref `git log -S` quando aplicável.
3. **Mergeable items** (heurística semântica com anti-spam). Pares de linhas com ≥3 substantivos compartilhados **excluindo top-20 termos mais frequentes do BACKLOG** (anti-spam para "plugin", "skill", "ADR").
4. **NOTES.md sinais editoriais** (informacional refinado). Varredura textual de `.claude/local/NOTES.md` listando sinais como contexto para operador decidir manualmente sobre H1-H3 — **não geram ação direta no gate** (não-decisional, igual ao consumo de NOTES.md em `/next`/`/triage`, escopo de inspeção mais largo).

**Salvaguarda de concorrência:** antes de aplicar mutações cross-seção (H1 move Próximos→Concluídos), skill executa `git worktree list --porcelain`. Main-só → aplica direto. ≥1 worktree adicional → **defer**: registra finding como entry estruturada em `.claude/local/NOTES.md` (signal queue) para próxima invocação picar. Preserva ADR-049 § Decisão (a) substância (sem merge artifact em concorrência multi-PR).

**Não cobre:**
- Decisão de prioridade entre items (escopo de `/next`).
- Archival de planos (`/archive-plans`).
- Adicionar items novos (`/triage`).
- Execução inline de items triviais (considerada e removida na 1ª iteração — YAGNI, zero evidência empírica; gatilho de reabertura em ADR-057 § Gatilhos).

## Arquivos a alterar

<!--
ADR-057 já foi criado upstream via /new-adr no /triage; não vira bloco do plano. /run-plan parte direto da criação da skill.
-->

### Bloco 1 — skill `/curate-backlog` {reviewer: doc}

- `skills/curate-backlog/SKILL.md` (novo): frontmatter (`name: curate-backlog`, description editorial, `disable-model-invocation: false` per ADR-050 § Decisão (e) cumulativo, `roles: required: [backlog]; informational: [plans_dir]`). Passos:
  1. **Ler BACKLOG.md** na íntegra + `.claude/local/NOTES.md` se existir.
  2. **Executar `git worktree list --porcelain`** (salvaguarda): classificar como `main-só` ou `worktree-adicional`.
  3. **Executar 4 heurísticas cumulativas** (sub-passos 3.1–3.4); acumular findings por categoria + linha + ação proposta (H1-H3) ou contexto (H4).
  4. **Apresentar preview estruturado** (paralelo a `/archive-plans` step 3): elegíveis por categoria + estado da salvaguarda (`main-só: mutações diretas` vs `worktree-adicional: mutações deferidas`).
  5. **Gate `AskUserQuestion`** (header `Curate`, opções `Aplicar tudo` / `Aplicar parcial` / `Cancelar`; `Aplicar parcial` desce em sub-gate por categoria).
  6. **Aplicar:**
     - `main-só`: mutar `BACKLOG.md` (refinos, merges, moves Próximos→Concluídos), commit unificado `chore(backlog): editorial curation — <N> refinements`.
     - `worktree-adicional`: escrever entry estruturada em `.claude/local/NOTES.md` sob `## curate-backlog deferred YYYY-MM-DD` (signal queue para próxima invocação picar), commit `chore(backlog): defer <N> editorial signals (worktree active)`.
  7. **Cutucada de descoberta** (per `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md` — skill nova traversa Resolution protocol step 3 para `backlog`).

### Bloco 2 — CLAUDE.md (bullet em Editing conventions + Cutucada de descoberta) {reviewer: doc}

- `CLAUDE.md`:
  - Acrescentar bullet em § "Editing conventions" referenciando ADR-057 (fronteira `/next` vs `/curate-backlog` + salvaguarda worktree-probe + H4 NOTES informacional refinado).
  - Atualizar § "Cutucada de descoberta" linha 137 para incluir `/curate-backlog` na lista de 5 skills que emitem a cutucada (vira 6) — gatilho ADR-046 linha 219 reconhecido (12 sites = limiar de avaliar helper; reapply editorial inheritance per ADR-057 § Decisão).

### Bloco 3 — `docs/procedures/cutucada-descoberta.md` ref {reviewer: doc}

- `docs/procedures/cutucada-descoberta.md`: adicionar `/curate-backlog` à lista de skills que emitem a cutucada (linha-ref editorial per § "Editorial inheritance" em CLAUDE.md).

## Verificação end-to-end

1. **ADR-057 existe** com Status `Aceito` (promoção pós-merge): `grep -F "Skill .curate-backlog." docs/decisions/ADR-057-curate-backlog-manutencao-editorial-periodica.md` retorna ≥1 match.
2. **Skill descobrível**: `ls skills/curate-backlog/SKILL.md` retorna o arquivo; frontmatter parseable: `python3 -c "import yaml; print(yaml.safe_load(open('skills/curate-backlog/SKILL.md').read().split('---')[1]))"` não levanta exceção.
3. **CLAUDE.md atualizado**: `grep -F "/curate-backlog" CLAUDE.md` retorna ≥2 matches (bullet em Editing conventions + linha em § Cutucada de descoberta).
4. **Procedure atualizado**: `grep -F "/curate-backlog" docs/procedures/cutucada-descoberta.md` retorna ≥1 match.
5. **Plan reference rot guard**: `grep -F "skill de manutenção editorial do BACKLOG (full-scan" BACKLOG.md` retorna 1 match (substring discriminante sem backtick — quoting-safe).

## Verificação manual

1. **Cenário 1 (gatilho temporal vencido).** Inserir linha temporária em `BACKLOG.md` `## Próximos`: `- plugin: teste cenário 1 — revisitar até 2026-01-01`. Invocar `/curate-backlog`. Esperado: preview lista a linha sob "Gatilhos temporais vencidos"; sem aplicar, cancelar; remover a linha manualmente.
2. **Cenário 2 (redação stale).** Inserir linha `- plugin: refinar skill /heal-backlog (renomeada)` (path inexistente em main). Invocar `/curate-backlog`. Esperado: preview lista sob "Redação stale" com cross-ref `git log -S "/heal-backlog"`.
3. **Cenário 3 (mergeable items + anti-spam).** Inserir duas linhas com ≥3 substantivos compartilhados não-meta (ex.: "skill exportar movimentos CSV streaming" + "ferramenta exportar movimentos CSV batch"). Invocar `/curate-backlog`. Esperado: preview oferece merge — "plugin"/"skill"/"ADR" ignorados pelo anti-spam.
4. **Cenário 4 (NOTES.md sinal informacional).** Adicionar entrada em `.claude/local/NOTES.md` com data atual: `## 2026-06-10\nlinha "plugin: teste cenário 4" do BACKLOG já está cumprida`. Inserir linha correspondente em `BACKLOG.md`. Invocar `/curate-backlog`. Esperado: preview lista sinal sob "NOTES.md" como **contexto** (não como ação direta); operador decide manualmente.
5. **Cenário 5 (salvaguarda worktree-probe).** Em estado main-só, invocar `/curate-backlog` com ≥1 finding H1 ativo. Esperado: preview indica `main-só: mutações diretas`. Depois, criar worktree fake (`git worktree add /tmp/test-curate test-branch`), repetir. Esperado: preview indica `worktree-adicional: mutações deferidas` e preview do conteúdo a escrever em NOTES.md. Remover worktree fake após teste (`git worktree remove /tmp/test-curate`).
6. **Cenário 6 (gate Cancelar).** Invocar `/curate-backlog` em estado real e responder `Cancelar`. Esperado: zero mutações, zero commits, zero writes em NOTES.md.

## Notas operacionais

- Skill é nova; primeira invocação real é o gate de validação. Heurística 4 (NOTES.md scan) faz scan completo na 1ª iteração — NOTES.md neste repo já tem 968 linhas; cap só entra como gatilho de revisão se skill demorar >10s.
- Salvaguarda worktree-probe é mecanismo defensivo determinístico, não heurística — não precisa de calibração empírica; é binary state.
- ADR-057 § Gatilhos de revisão consolida: over-correção do override N=3 (6 meses / ≤2 invocações OR ≥50% findings inúteis); ressurreição de H4 (≥3 instâncias auditadas); 7ª skill emissora.

## Pendências de validação

- Smoke real dos 6 cenários acima em invocação subsequente pós-merge+reload do plugin no consumer.
- Validar que cutucada de descoberta dispara conforme convenção (`/curate-backlog` traversa Resolution protocol step 3).
- Promover ADR-057 de `Proposto` → `Aceito (YYYY-MM-DD)` após smoke real bem-sucedido + 1 invocação real útil.

## Decisões absorvidas

- ADR-057 § Origem + § Contexto: ADR-049 § Decisão (a) reconhecido como decisão base com tensão resolvida via salvaguarda worktree-probe (caminho-único).
- ADR-057 § Gatilhos de revisão: gatilho de under-use consolidado em "6 meses pós-shipping / ≤2 invocações OR ≥50% findings inúteis" (caminho-único).
- ADR-057 § Alternativas (c): descarte reformulado reconhecendo override explícito + cross-ref para § Override do critério N=3 (caminho-único).
- ADR-057 § Cutucada e gatilho ADR-046: gatilho linha 219 (6ª skill emissora, 12 sites) reconhecido + decisão de reapply editorial inheritance até 12+ sites (caminho-único).
- Plano § Arquivos a alterar Bloco 1 original (ADR via /new-adr): removido — ADR-057 já em disco pós-/triage, /run-plan parte direto da skill; renumeração 4→3 blocos (caminho-único).
- Plano § Bloco 1 (skill) reviewer annotation: `{reviewer: code}` → `{reviewer: doc}` — SKILL.md é prosa markdown, não código (caminho-único).
- Plano § Verificação end-to-end critério 5: simplificado para substring discriminante sem backtick (quoting-safe) (caminho-único).
