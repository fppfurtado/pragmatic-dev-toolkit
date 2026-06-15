---
name: session-audit
description: Audita captura pendente da sessão CC corrente — identifica substância gerada (decisões, classificações, drift, findings) não persistida em artefato canonical (BACKLOG, NOTES.md, ADRs, CLAUDE.md/philosophy.md). Reporta gaps agrupados por tipo com cutucada batched single-call. Invocação manual antes de encerrar a sessão.
disable-model-invocation: false
roles:
  required: []
  informational: [backlog, decisions_dir]
---

# session-audit

Audit de **captura pendente sessional**: lê transcript da sessão corrente, identifica substância gerada mas não persistida nos artefatos canonical, e oferece materialização batched antes do encerramento. **Operator-initiated, preview-first, não-destrutivo.**

Skill irmã de `/curate-backlog` (ADR-057) e `/archive-plans` (ADR-022) — mesma natureza editorial não-mutativa por design, escopo diferente. `/curate-backlog` cura periódica do BACKLOG; `/archive-plans` arquiva planos antigos; `/session-audit` fecha o ciclo no fim de sessão antes que substância gerada se perca.

**Tensão com ADR-061 § Limitações reconciliada** (per [ADR-064](../../docs/decisions/ADR-064-gate-com-executor-validacao-2-sites.md) § Contexto). ADR-061 § Limitações declara side-effects executados (commits, mutações remotas, file edits aplicados) fora de escopo. ADR-064 abre exceção controlada para o tipo derivado `executar_validacao_pendente` (passos 2, 4, 5, 6 abaixo): mutação restrita ao marker `Encerrada YYYY-MM-DD` no plan body como signal de validação concluída — não cobre commits novos, mutações remotas, ou edits arbitrários em arquivos do projeto. Escopo declarado de ADR-061 sobre commits e mutações remotas permanece intacto.

## Argumentos

- Sem argumentos (default): audit completo dos 4 destinos.
- `--scope <area>`: foca em subset — valores aceitos `backlog`, `notes`, `adr`, `doutrina`. Reduz ruído quando operador já endereçou parte manualmente.

Argumento inválido → reportar e usar default.

## Passos

### 1. Parse argumento

Capturar `--scope <area>` opcional. Sem flag = `default` (cobre os 4 destinos).

### 1.5. Detecção de modo `forge` no role `backlog`

Resolver `paths.backlog` via Resolution Protocol. Se `forge`, marcar findings de tipo `captura_backlog` como **defer pra `/triage`** com nota informativa apontando ADR-058 § Decisão (policy de cutucada granular por mutação remota). Skill **não** propõe `gh issue create` / `glab issue create` direto — `/triage` step 4 modo forge já tem a mecânica codificada; duplicar quebraria a fronteira editorial.

Modo arquivo (canonical ou `local`) ou `paths.backlog: null` → seguir fluxo normal de captura para BACKLOG.

### 2. Análise do transcript

Ler transcript da sessão CC corrente. Aplicar heurísticas detectivas — sinais que indicam substância gerada potencialmente não-persistida:

- **Palavras-chave indicativas de decisão emitida**: "decidi", "classifico", "concluí", "identifiquei drift", "smoke validado", "validei mecanicamente", "padrão emergente", "pattern observado".
- **Tool calls de classificação/decisão sem Edit/Write subsequente em artefato canonical**: substância sem destino editorial.
- **Findings de cutucadas (design-reviewer/code-reviewer/etc.) resolvidos via prosa sem entry derivada** em ADR ou em BACKLOG (caminho-único absorvido em commit message é OK; caminho-cutucada decidido sem registro = gap).
- **Cross-refs declarados em commit messages mas não materializados** em ADRs ou no índice cross-reference correspondente.
- **Snapshots ou observações de drift mencionados em prosa** sem entry de capturas (ex.: "drift detectado em X" sem follow-up).
- **Planos com `## Pendências de validação` cuja sessão tocou direta ou indiretamente** (via `/run-plan`, refs explícitas em prosa, ou trace de file edits em paths do plano) — detectar para tipo derivado `executar_validacao_pendente` (per [ADR-064](../../docs/decisions/ADR-064-gate-com-executor-validacao-2-sites.md)); classificação ocorre no passo 4.

Heurísticas são detectivas (qualitativas), não predicados mecânicos. Skill aplica julgamento sobre a substância — não conta tool calls.

### 3. Resolução de artefatos

Via Resolution Protocol do CLAUDE.md, resolver paths dos 4 destinos canonical:

- **`paths.backlog`** — destino de feature/fix/regra/doc nova, bug colateral, finding fora-do-escopo.
- **`.claude/local/NOTES.md`** — destino de contexto cross-session, observação operacional, padrão emergente sub-N3, snapshot informativo (per ADR-054 § Decisão (b), store non-role).
- **`paths.decisions_dir`** (default `docs/decisions/`) — destino de decisão estrutural duradoura satisfazendo ≥1 das 5 condições de ADR-034.
- **`CLAUDE.md` / `philosophy.md`** (ou equivalente do projeto consumidor) — destino de entendimento estabilizado redirecionado pelo filtro de admissão de ADR-045 § Decisão.

Role ausente (informational não-declarado) → skip silente naquele destino; relatório limita-se aos disponíveis (Cenário 4 da Verificação manual do plano de origem).

### 4. Classificar substância

Para cada substância detectada no passo 2, produzir um finding com schema:

```
{
  tipo: <enum: captura_backlog | captura_notes | cristalizacao_adr | atualizacao_doutrina>,
  substancia_breve: <prosa curta, ≤1 linha>,
  artefato_sugerido: <citação explícita do artefato resolvido no passo 3>,
  citação_transcript: <citação concreta do transcript que substantia a detecção>,
  ação_sugerida_prosa_curta: <o que escrever, onde, com qual contexto>
}
```

**`citação_transcript` é obrigatória** — substância sem citação concreta não passa para o relatório (salvaguarda contra hallucination paralela à constraint de `/new-adr` "não inventar Contexto/Decisão sem input explícito"). `tipo` é enum fechado nos 4 destinos do passo 5. `artefato_sugerido` cita o destino resolvido no passo 3 explicitamente — não genérico ("BACKLOG.md", "NOTES.md", "ADR-NNN em `docs/decisions/`", "CLAUDE.md § <seção>").

Cross-refs faltantes em ADRs **ficam fora de escopo** desta skill. Side-effects executados (commits, mutações remotas) **também ficam fora de escopo** — categoria distinta, sem dor materializada hoje (YAGNI; reabrir se ≥3 sessões com gaps deste tipo emergirem).

**Tipo derivado `executar_validacao_pendente`** (per [ADR-064](../../docs/decisions/ADR-064-gate-com-executor-validacao-2-sites.md)) — **extensão informal** que não entra no enum formal 4-tipos acima; vai como **addendum** "**Pendências de validação executáveis**" no relatório do passo 5. Para cada plano detectado no passo 2 (heurística "Planos com `## Pendências de validação` tocados pela sessão"), classificar bullets via `${CLAUDE_PLUGIN_ROOT}/docs/procedures/gate-com-executor-validacao.md` em **[executável-pra-mim]** vs **[exige-operador]** (cláusula default-conservadora: ambíguo → [exige-operador]). Citação_transcript obrigatória aqui também: identificar a entrada do transcript (`/run-plan` invocado sobre o plano, ref explícita, edit em path do plano) que liga a sessão à pendência.

### 5. Relatório markdown + cutucada batched

Reportar em formato markdown agrupado por tipo (4 grupos, omitir os vazios):

```
## Captura BACKLOG
- <substancia_breve> → <artefato_sugerido> [citação: <trecho>]

## Captura NOTES
- ...

## Cristalização ADR
- ...

## Atualização doutrina canonical
- ...
```

Cada linha cita `citação_transcript` para auditabilidade. Lista vazia → relatório enxuto "0 gaps detectados; encerramento limpo" (Cenário 2 da Verificação manual).

**Addendum "Pendências de validação executáveis"** (per [ADR-064](../../docs/decisions/ADR-064-gate-com-executor-validacao-2-sites.md)): quando passo 4 produziu findings tipo derivado `executar_validacao_pendente`, adicionar bloco após o relatório dos 4 tipos formais (omitido se 0 planos detectados):

```
## Pendências de validação executáveis
- [executável] <slug do plano> — Cenário N: <texto do bullet>. Razão: <heurística do procedure §3>.
- [exige-operador] <slug do plano> — Cenário M: <texto do bullet>. Razão: <heurística do procedure §3>.
```

Em seguida, **uma única cutucada batched** via `AskUserQuestion` (header `Captura`). Opções condicionais ao addendum:

- **0 cenários [executável]** (addendum ausente OU sem [executável] após classificação): cutucada mantém 3 opções `Aplicar tudo (Recommended)` / `Aplicar parcial (Other)` / `Cancelar` — preserva ADR-002 § Decisão anti-gate-cerimônia (sem oferta cosmética sem decisão genuína; paralelo a `/run-plan §3.2` per ADR-064).
- **≥1 cenário [executável]**: cutucada apresenta 4 opções: `Aplicar tudo (Recommended)` / `Aplicar parcial (Other)` / `Cancelar` / `Executar [executável] também` (4ª opção). `description` da 4ª opção carrega contagem dos cenários [executável] + slug dos planos tocados.

`description` carrega contagem total de gaps + breakdown por tipo. Operador via `Other` descreve subset em prosa ("aplicar gaps 1 e 3, cancelar 2"). Pattern paralelo a `/curate-backlog` (preview-first batched) e `/archive-plans` (write-local não-destrutivo) — sem mutação remota, sem cutucada granular.

### 6. Aplicar capturas

Para cada finding aceito pela cutucada do passo 5, executar a `ação_sugerida_prosa_curta` aplicando edit no artefato resolvido:

- **`captura_backlog` em modo arquivo:** `Edit` em `## Próximos` do papel `backlog` adicionando bullet com `substancia_breve`. **Salvaguarda worktree-probe** (herdada de [ADR-057](../../docs/decisions/ADR-057-curate-backlog-manutencao-editorial-periodica.md) § Decisão § Salvaguarda de concorrência, per ADR-061 § Trade-offs): antes de aplicar, probe `git worktree list --porcelain`. Main-só (sem worktree adicional) → mutação direta. ≥1 worktree adicional → defer via append em `.claude/local/NOTES.md` como signal queue (mesma mecânica do ADR-057), sem mutação direta em `BACKLOG.md`; operador re-aplica via `/curate-backlog` ou manual.
- **`captura_backlog` em modo `forge`:** **defer pra `/triage` subsequente** (per passo 1.5). Reportar no done explicitamente sem mutação remota.
- **`captura_notes`:** `Edit` (append) em `.claude/local/NOTES.md` com timestamp (paralelo a `/note`).
- **`cristalizacao_adr`:** sugestão textual de invocar `/new-adr <título>` no encerramento — skill **não** chama `/new-adr` aninhado (operador decide; ADR-009 design-reviewer entra no fluxo via /new-adr standalone).
- **`atualizacao_doutrina`:** sugestão textual de edit em `CLAUDE.md` / `philosophy.md` no encerramento — operador aplica manualmente; salvaguarda contra automação de mudança apex.
- **Tipo derivado `executar_validacao_pendente`** (per [ADR-064](../../docs/decisions/ADR-064-gate-com-executor-validacao-2-sites.md)): quando operador escolhe 4ª opção `Executar [executável] também` no passo 5, rodar cenários [executável] de cada plano detectado conforme cláusula de execução de `${CLAUDE_PLUGIN_ROOT}/docs/procedures/gate-com-executor-validacao.md` §4. Reportar verdict per cenário; **marcar cada bullet [executável] exercitado** como `Encerrada YYYY-MM-DD: <síntese do verdict>` no plan body (granularidade per-bullet, não per-seção; paralelo ao pattern manual aplicado em commits `e2e135f` + `10c256c` da sessão CC `next-2026-06-14`). Cenários [exige-operador] tratados conforme procedure §4 item 3 (deferência explícita em prosa).

Capturas canceladas (Other com subset) ficam no relatório como referência informativa da sessão, sem persistência editorial.

Sem capturas aceitas (operador escolhe `Cancelar` no passo 5) → reportar relatório como leitura informativa e encerrar sem mutação.

## O que NÃO fazer

- **Não inventar substância sem base concreta no transcript** — `citação_transcript` obrigatória per passo 4 (paralelo à constraint do `/new-adr` "não inventar Contexto/Decisão sem input explícito do operador"). Hallucination de gap inexistente erode confiança operacional na skill.
- **Não executar capturas sem cutucada afirmativa** do operador no passo 5. Skill é preview-first não-destrutiva por construção.
- **Não interpretar side-effects executados como captura pendente** (commits, mutações remotas, file edits aplicados ficam fora de escopo). Categoria distinta sem dor materializada.
- **Não tratar Read defensivo como gap de captura** — `Read` sem `Edit` subsequente é validação per `philosophy.md` § Busca pela verdade, não decisão pendente. Gap requer **decisão emitida** (classificação, drift declarado, finding cristalizado em prosa).
- **Não chamar `/new-adr` aninhado** no passo 6 — `cristalizacao_adr` vira sugestão textual; operador decide invocação separada. Wiring automático do design-reviewer via ADR-053 § Decisão (b) entra naturalmente quando operador roda `/new-adr` standalone.
- **Não aplicar capturas em projetos sem `paths.*` declarados** sem oferta de criação canonical paralela ao sub-fluxo do `/triage` step 4 — papel "não temos" em todos os destinos = relatório informativo, skip silente da aplicação.
- **Não classificar cenários como [executável-pra-mim]** no addendum "Pendências de validação executáveis" do passo 5 que mutam state remoto (push, gh release, glab issue) — mesmo se classificação automática errar, o bullet é cinto de segurança independente da cláusula blast-radius do `${CLAUDE_PLUGIN_ROOT}/docs/procedures/gate-com-executor-validacao.md`; remover este guarda risca regressão silenciosa em refactor futuro da heurística (per [ADR-064](../../docs/decisions/ADR-064-gate-com-executor-validacao-2-sites.md) § Limitações).
