# ADR-061: Skill `/session-audit` — categoria editorial "audit captura pendente sessional"

**Data:** 2026-06-12
**Status:** Proposto

## Origem

- **Plano:** `docs/plans/session-audit-skill.md` (caminho-com-plano gerado via `/triage` upstream em sessão cross-cwd).
- **Decisão base (paralelo periódico):** [ADR-057](ADR-057-curate-backlog-manutencao-editorial-periodica.md) (categoria editorial periódica `/curate-backlog`) — precedente da cristalização de skill editorial via ADR + precedente do Override do critério N=3.
- **Decisão base (precedente categoria editorial):** [ADR-022](ADR-022-politica-archival-docs-plans.md) (`/archive-plans` periódica) — primeira instância editorial não-mutativa do toolkit.
- **Decisão base (filtro de admissão):** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão — filtro com 3 saídas; substância passa em `ADR — decisão estrutural reversível` por padrão emergente operador-recorrente + Override do critério N=3 (precedente em ADR-057 § Override).
- **Decisão correlata (regra dura mutações BACKLOG):** [ADR-049](ADR-049-execucao-run-plan-consolidado.md) § Decisão (a) — state em git/forge; salvaguarda worktree-probe de ADR-057 herdada pelo `skills/session-audit/SKILL.md` (ver § Trade-offs).

## Contexto

Operador articulou múltiplas vezes em sessões CC distintas (meta-system, h3-finance-agent, este plugin) o pedido "verifique se todos os itens de backlog e respectivos contextos necessários foram devidamente registrados nos artefatos adequados" — substância recorrente cross-projeto. Sem skill dedicada, o pattern era executado manualmente turn-by-turn no encerramento de sessão, com risco de captura incompleta quando contexto se aproximava do limite.

Substância da skill resultante (cristalizada em `skills/session-audit/SKILL.md`): leitura do transcript da sessão CC corrente identificando substância gerada (decisões emitidas, classificações, drift declarado, findings de cutucadas resolvidas sem entry derivada, cross-refs declarados sem materialização) **não persistida em artefato canonical** (BACKLOG / NOTES.md / ADR / CLAUDE.md/philosophy.md). Saída: relatório markdown agrupado por tipo + cutucada batched single-call.

Substância de raciocínio dominante (julgamento "vale persistir?", "onde mora?") — Cond 1 ADR-011 do meta-system falha por design → skill markdown per § "Skill = pensamento". Per ADR-008 do meta-system (homing arquitetural por necessidade): necessidade universal stack-agnóstica → toolkit universal.

## Decisão

Cristalizar **categoria editorial "audit captura pendente sessional"** — skill `/session-audit` materializa trigger temporal **sessional** (manual, "antes de encerrar a sessão CC"), distinta de categoria editorial **periódica** de ADR-057 e ADR-022. Diferenças semânticas:

- **ADR-057** (`/curate-backlog`): trigger periódico, escopo single-artefato (`BACKLOG.md`), mutações cross-seção do arquivo, ≥3 heurísticas detectivas (H1 temporal + H2 redação stale + H3 mergeable items).
- **ADR-022** (`/archive-plans`): trigger periódico, escopo single-artefato (`docs/plans/`), mutação `git mv` para `archive/<YYYY-Qx>/`.
- **ADR-061** (esta decisão, `/session-audit`): trigger **sessional** (manual), escopo **multi-artefato** (4 destinos canonical: BACKLOG, NOTES.md, ADRs, CLAUDE.md/philosophy.md), heurísticas detectivas qualitativas sobre transcript da sessão corrente, paralelismo editorial preview-first não-destrutivo.

Razões:

- Pedido recorrente do operador em sessões distintas (≥3 instâncias documentadas) sinaliza padrão emergente estabilizado.
- Captura no fim de sessão fecha gap real: substância gerada turn-by-turn perde acesso ao transcript quando sessão encerra; persistência tardia depende de memória do operador.
- Categoria sessional não cabe em ADR-057 (trigger periódico explícito) nem em ADR-022 (escopo single-artefato `plans_dir`).

### § Override do critério N=3 (ADR-043 § Ockham operacionalizado #4)

Esta decisão cristaliza categoria editorial nova com **<3 instâncias materializadas** desta skill específica (sessional como categoria semântica é nova em `/session-audit`). Override análogo ao precedente de [ADR-057](ADR-057-curate-backlog-manutencao-editorial-periodica.md) § Override: padrão emergente recorrente do operador antecipa cristalização quando custo de não-cristalizar é re-construir doutrina do zero a cada sessão. Gatilho de revisão concreto registrado em § Gatilhos de revisão.

Memory `feedback_editorial_patterns_emergentes` flagrava risco de over-correção em ≥3 contadores em curso à época de ADR-057 § Override; gatilho de revisão #1 deste ADR testa empiricamente se o override aqui foi prematuro (paralelo direto ao precedente).

## Auto-aplicação per ADR-034

Decisão estrutural duradoura — cristaliza categoria editorial nova "sessional" no toolkit:

- **Cond 1 (decisão estrutural sem ancestral):** **NÃO aplica isoladamente** — categoria sessional tem ancestral indireto em ADR-057/-022 (skills editoriais periódicas); não é decisão sem ancestral, é variante semântica nova.
- **Cond 2 (substitui ADR ancestral):** **NÃO aplica** — ADR-057 e ADR-022 permanecem vigentes e cobrem suas categorias periódicas; este ADR adiciona categoria distinta.
- **Cond 3 (codifica restrição externa):** **NÃO aplica** — sem restrição regulatória/contratual.
- **Cond 4 (introduz categoria nova):** **APLICA** — categoria editorial "audit captura pendente sessional" (trigger temporal sessional + escopo multi-artefato) é nova; sem precedente direto no toolkit.
- **Cond 5 (sucessor parcial):** **APLICA** — sucessor parcial **lateral** de ADR-057 (paralelismo sessional ↔ periódico); ancestral declarado em § Origem com diferenças semânticas explícitas em § Decisão.

Cond 4 + cond 5 simultâneas aplicam — pattern editorial estabelecido por ADRs precedentes ≥ADR-045 (e.g. ADR-053, ADR-054 sucessores parciais introduzindo categoria nova).

## Consequências

### Benefícios

- Fecha gap real de captura no encerramento de sessão (substância turn-by-turn não-persistida).
- Pattern editorial preview-first não-destrutivo paralelo a `/curate-backlog` e `/archive-plans` — operador tem familiaridade.

### Trade-offs

- Cross-plugin coupling rejeitado (skill autônoma vs hook CC `Stop` event sugerindo `/session-audit`; integração tight com `meta-bridge` `/journal-close` rejeitada por design).
- Operator invoca manual; valor depende de adoção (gatilho de revisão #1 cobre).
- **Salvaguarda contra concorrência herdada de ADR-057.** Mutações em BACKLOG.md por `/session-audit` herdam pattern de salvaguarda worktree-probe de [ADR-057](ADR-057-curate-backlog-manutencao-editorial-periodica.md) § Decisão § Salvaguarda de concorrência. Mecânica runtime vive em `skills/session-audit/SKILL.md`; ADR-061 cristaliza categoria editorial, não duplica mecânica. Tensão com [ADR-049](ADR-049-execucao-run-plan-consolidado.md) § Decisão (a) (mutações BACKLOG cross-seção) resolvida via mesmo precedente. Em modo `paths.backlog: forge` ([ADR-058](ADR-058-role-backlog-aceitar-forge.md) § Decisão — policy de cutucada granular por mutação remota), findings `captura_backlog` viram defer pra `/triage` step 4 — política herdada sem co-localização.

### Limitações

- Substância "side-effects executados" (commits, mutações remotas, file edits aplicados) **fora de escopo** desta skill — categoria distinta sem dor materializada.
- Substância "cross-refs faltantes em ADRs" **fora de escopo** — categoria distinta.

## Alternativas consideradas

### Hook CC `Stop` event sugerindo `/session-audit`

Rejeitado: cross-plugin coupling com lifecycle CC; pattern análogo a `suggest_journal_close` do `meta-bridge` ficou em `meta-bridge` por design (categoria pertence à fronteira do operador, não da skill que reage). Operador invoca manual; extension hint não-bloqueante no `/run-plan` §3.6 cumpre o gatilho semântico mínimo sem acoplamento mecânico cross-plugin (decisão tática, **não-categoria** — cabe em `CLAUDE.md` § Editing conventions como pavimentação de pattern futuro, não em ADR).

### Integração tight com `meta-bridge` `/journal-close`

Rejeitado: cross-plugin coupling. Operador invoca skills sequencialmente livre — `/session-audit` antes, `/journal-close` depois é o pattern intencional.

### Auto-classify enums no batched output (passo 5)

Rejeitado: `Aplicar tudo (Recommended)` / `Aplicar parcial (Other)` / `Cancelar` é mais simples e cobre os casos comuns; operador descreve subset via Other quando quer granularidade. Auto-classify ad-hoc inflaria interface sem dor materializada.

### Escopo expandido (side-effects + cross-refs + ADRs sem cross-ref)

Rejeitado para v1: YAGNI explícito no plano. Reabrir quando ≥3 sessões com gaps deste tipo emergirem (gatilho de revisão #3).

### Cristalizar categoria "extension hint cross-skill no done" junto

Rejeitado neste ADR: design-reviewer (review pré-shipping) flagrou codificação prematura — categoria com 1 só instância (o hint em `/run-plan` §3.6) viola ADR-043 § Ockham operacionalizado #4 (pattern emergente ≥3 aplicações ad hoc) e ADR-036 (não codifique pattern com evidência empírica fraca). Substância tática preservada como decisão registrada em commit + bullet `CLAUDE.md` § Editing conventions ("pavimenta categoria futura quando ≥2 análogos emergirem"). ADR sucessor codifica categoria quando ≥2 data points concretos existirem.

## Gatilhos de revisão

1. **≤2 invocações de `/session-audit` em 6 meses pós-shipping OR findings inúteis em ≥50% das invocações reais** — operador pediu múltiplas sessões mas adoção ou utilidade não confirma; reabrir Override do critério N=3 e re-avaliar valor da skill. Pattern de gatilho composto idêntico ao precedente [ADR-057](ADR-057-curate-backlog-manutencao-editorial-periodica.md) § Gatilhos.
2. **Ruído sustained no hint do `/run-plan` §3.6** (operador silencia frequentemente) — reabrir opt-out via `paths.session_audit_hint: false` no `<!-- pragmatic-toolkit:config -->`. Este gatilho aplica-se também à decisão tática de extension hint registrada em `CLAUDE.md` § Editing conventions (fronteira entre decisão tática e categoria doutrinal preservada).
3. **≥3 sessões reportadas com gaps de side-effects / cross-refs faltantes** — categoria expandida reabre escopo § Limitações.
4. **≥2 extension hints cross-skill análogos emergirem em outras skills do toolkit** — categoria editorial nova consolidada (decisão tática preservada em `CLAUDE.md` vira candidata a ADR sucessor cristalizando categoria com 2 data points concretos).
