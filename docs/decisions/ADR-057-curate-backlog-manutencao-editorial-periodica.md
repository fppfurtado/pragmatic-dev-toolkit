# ADR-057: Skill `/curate-backlog` — manutenção editorial periódica do BACKLOG com NOTES.md como fonte decisional

**Data:** 2026-06-10
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-022](ADR-022-politica-archival-docs-plans.md) — precedente direto de skill editorial periódica operator-initiated, preview-first, non-destructive. `/curate-backlog` é skill irmã com escopo `BACKLOG.md` em vez de `docs/plans/`; segue mesma natureza e shape de operação.
- **Decisão base:** [ADR-036](ADR-036-brainstorm-intencionalmente-nao-codificado-em-skill.md) — precedente de ADR que registra decisão de (não-)codificação com critério N=3 explícito. Este ADR aplica o critério na direção oposta — codificar **com override registrado** quando operador reconhece instâncias empíricas não-capturadas em registro formal.
- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) — admission policy. Saída `ADR` satisfeita por: (i) reversibilidade positiva (cenário de reversão nomeável — under-use ou findings inúteis); (ii) categoria nova "manutenção editorial periódica do BACKLOG"; (iii) pattern emergente ≥3 aplicações ad hoc satisfeito retroativamente por declaração informada do operador.
- **Decisão base:** [ADR-049](ADR-049-execucao-run-plan-consolidado.md) — § Decisão (a) prescreve que `/run-plan §3.4` apenas **adiciona** em `## Concluídos` (sem mover de outra seção). `/curate-backlog` propõe mutações cross-seção (Próximos→Concluídos) que tensionam essa regra. Tensão resolvida via **salvaguarda worktree-probe** (§ Decisão § Salvaguarda de concorrência) — mutações cross-seção só ocorrem em main-só; ≥1 worktree adicional → defer via NOTES.md como signal queue. Ver § Decisão para detalhe.
- **Decisão base:** [ADR-054](ADR-054-bridge-cross-project-note-consolidado.md) — define NOTES.md como store informational non-role. Este ADR consome NOTES.md em dois eixos sem alterar ADR-054: (i) heurística 5 lê NOTES como **sinais informacionais refinados** (igual ao pattern já existente em `/next`/`/triage`); (ii) salvaguarda worktree-probe **escreve** NOTES.md como signal queue para invocações futuras. Nenhum dos eixos cria role nem extensão decisional global.
- **Investigação:** sessão CC `tjpa-tools-backlog` 2026-06-10 (meta-system) registrou pattern empírico — revisão manual ampla de `BACKLOG.md`: verificação de gatilhos temporais vencidos, detecção de obsoletos parciais, redação stale, redundâncias/merges. `/triage` subsequente no toolkit (2026-06-10) confirmou ≥3 instâncias ad hoc não-registradas em projetos do ecossistema via declaração explícita do operador.

## Contexto

`/next` cobre **orientação de sessão**: lê os 10 primeiros itens de `## Próximos`, verifica evidência de implementação, propõe top 3 candidatos para `/triage`. Não cobre varredura editorial periódica ampla.

Pattern emergente registra natureza diferente da cobertura de `/next`:

| Eixo | `/next` | Pattern observado |
|---|---|---|
| Cadência | Por sessão | Periódica (operator-initiated) |
| Escopo | 10 primeiros itens | Arquivo inteiro |
| Saída | Recomendação (enum top 3) | Mutações pequenas em múltiplas linhas + commit unificado |
| Mutação | Mover implementados (1 caso) | Refinos, merges, moves cross-seção |

`/archive-plans` ([ADR-022](ADR-022-politica-archival-docs-plans.md)) é o precedente direto de skill editorial periódica: operator-initiated, preview-first, non-destructive, escopo `docs/plans/`. ADR-022 § Alternativas considerou os mesmos trade-offs (`/next` sub-passo, sub-passo de `/triage`, comando manual, gesto de `/release`) e escolheu skill standalone — este ADR aplica o mesmo raciocínio ao domínio `BACKLOG.md`.

**Tensão com ADR-049 § Decisão (a)** (codifica regra dura de que `/run-plan §3.4` apenas adiciona em `## Concluídos` para evitar merge artifact com PRs concorrentes mutando seções): mutações cross-seção propostas aqui (Próximos→Concluídos) tensionam essa regra. Resolvida via **salvaguarda worktree-probe** descrita em § Decisão § Salvaguarda de concorrência — em main-só (sem concorrência multi-PR), mutações cross-seção são seguras; ≥1 worktree adicional ativa → defer via NOTES.md como signal queue. ADR-049 substância preservada (regra dura aplica quando há concorrência real); salvaguarda mecânica garante que `/curate-backlog` nunca opera em estado análogo ao que ADR-049 desenhou para evitar.

Adicionalmente, NOTES.md (ADR-054) é store informacional cross-session. `/next` e `/triage` consomem como suplemento informational de ranking/contexto. `/curate-backlog` consome em dois eixos: (i) heurística 5 lê NOTES.md como sinais informacionais refinados (mesmo pattern, escopo de inspeção mais largo); (ii) salvaguarda worktree-probe escreve NOTES.md como signal queue de mutações deferidas. Nenhum dos eixos cria role nem altera ADR-054 § Decisão (a).

## Decisão

**Cria-se skill standalone `/curate-backlog` para manutenção editorial periódica do `BACKLOG.md`. Operação preview-first, sob demanda, non-destructive até o gate de aplicação. Mecanismo determinístico baseado em 4 heurísticas cumulativas + salvaguarda de concorrência via worktree-probe. NOTES.md consumida como sinais informacionais refinados (sem alterar status non-role de ADR-054).**

### Fronteira `/next` vs `/curate-backlog`

| Eixo | `/next` | `/curate-backlog` |
|---|---|---|
| Cadência | Por sessão | Periódica (operator-initiated) |
| Escopo | 10 primeiros itens de `## Próximos` | Arquivo inteiro |
| Saída | Recomendação top 3 | Preview de mutações + commit unificado |
| Mutações | Mover impl. forte → Concluídos (1 caso) | Refinos, merges, moves cross-seção (gated por worktree-probe) |
| NOTES.md | Informational (ranking suplementar) | Informational refinado (heurística 5) + signal queue (deferred mutations) |

### 4 heurísticas cumulativas

1. **Gatilhos temporais vencidos** (predicado mecânico). Linhas em `## Próximos` com marca `até YYYY-MM-DD`, `deadline YYYY-MM-DD`, ou `T+Nd` (N dias relativos à data do commit de adição via pickaxe `git log -S "<linha>" --diff-filter=A --reverse | head -1`). Comparação contra `date +%Y-%m-%d`. Sinal: revisar prioridade ou mover para Concluídos.
2. **Redação stale** (heurística semântica). Refs a estado superado — paths renomeados, ADRs marcados Substituído, skills extintas, números desatualizados. Detecção via judgment do agente runtime + cross-ref via `git log -S "<termo>"` quando aplicável. **Limitação reconhecida:** julgamento do agente; spec leve por design (codificar regex de "stale" produziria falsos positivos massivos).
3. **Mergeable items** (heurística semântica com anti-spam). Pares de linhas com ≥3 substantivos compartilhados, **excluindo top-20 termos mais frequentes do próprio BACKLOG** (anti-spam: termos como "plugin", "skill", "ADR" não contam). Candidatos a consolidar.
4. **NOTES.md sinais editoriais** (heurística semântica, informacional refinado). Varredura textual de `.claude/local/NOTES.md` procurando (a) menções de linha do BACKLOG como obsoleta/concluída; (b) deadlines vencidos capturados via `/note`; (c) work cross-projeto sinalizando convergência ou contradição. **Status:** sinais listados como contexto para operador inspecionar antes de decidir sobre H1-H3 — não geram ação direta no gate `Aplicar tudo`. Scan completo na 1ª iteração (NOTES.md ≤ 1000 linhas é trivial); calibrar window se NOTES.md crescer ≥10× per gatilho de revisão.

Cada heurística produz findings com categoria + linha + ação proposta (H1-H3) ou linha + contexto (H4). Operador decide via gate `AskUserQuestion` (header `Curate`, opções `Aplicar tudo` / `Aplicar parcial` / `Cancelar`).

H1 é predicado mecânico (data comparativa); H2/H3/H4 são heurísticas semânticas exercidas pelo agente runtime via Read+julgamento. Diferença reconhecida explicitamente como Limitação — spec mais leve que ADR-022 (cujos 6 critérios são mecânicos via `git`) porque domínio é textual+semântico, não git-state.

### Salvaguarda de concorrência via worktree-probe

Antes de aplicar mutações cross-seção (H1 move Próximos→Concluídos), skill executa `git worktree list --porcelain` e classifica:

- **Só worktree main** → aplica mutações direto. ADR-049 § Decisão (a) preservado (sem concorrência multi-PR; merge artifact impossível).
- **≥1 worktree adicional ativa** → **defer**: registra finding como entry estruturada em `.claude/local/NOTES.md` sob header `## curate-backlog deferred YYYY-MM-DD`, formato:

  ```
  ## curate-backlog deferred 2026-06-10
  - BACKLOG.md:<linha>: move para Concluídos — razão: <heurística>
  - BACKLOG.md:<linha>: refinar — razão: <heurística>
  ```

  Próxima invocação de `/curate-backlog` em estado main-só lê essa entry, propõe aplicar as mutações deferidas (preview-first com cross-ref à data da deferral), commit unificado limpa a entry após aplicação.

Salvaguarda mecânica garante que `/curate-backlog` nunca opera concorrente com `/run-plan` sobre o mesmo arquivo — ADR-049 substância (regra dura) preservada empiricamente.

### Operação preview-first (mesma forma de `/archive-plans`)

1. Ler `BACKLOG.md` + `.claude/local/NOTES.md` (se existir).
2. Executar `git worktree list --porcelain` (salvaguarda).
3. Executar 4 heurísticas; acumular findings.
4. Apresentar preview estruturado por categoria + estado da salvaguarda (main-só vs deferred).
5. Gate `AskUserQuestion` (Aplicar tudo / parcial / Cancelar).
6. Aplicar: mutar arquivo (main-só) OR escrever NOTES.md signal queue (worktree adicional). Commit unificado `chore(backlog): editorial curation — <N> refinements` ou `chore(backlog): defer <N> editorial signals (worktree active)`.
7. Não pusha (paralelo a `/archive-plans` ADR-022).

### Override do critério N=3 — registrado explicitamente

[ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado critério 4 prescreve ≥3 aplicações ad hoc auditáveis retroativamente antes de codificar pattern como abstração. Backlog line registrava UMA instância documentada (sessão `tjpa-tools-backlog` 2026-06-10 do meta-system). Operador em `/triage` (toolkit, 2026-06-10) sobrescreveu o critério: *"essa demanda já ocorreu outras vezes, em outros repos, porém não houve registro da ocorrência, portanto, a demanda já possui justificativa concreta."*

ADR-045 admission policy aplica via "pattern emergente" satisfeito retroativamente por declaração informada. Este ADR registra a declaração para auditoria futura. Memory `feedback_editorial_patterns_emergentes` flagara explicitamente risco de over-correção em ≥3 contadores em curso (sub-3c 2/3, decimal-retroativa 1/3, preservação seletiva 1/3, variação blockquote 1/3) — gatilho de revisão correspondente abaixo testa empiricamente se o override aqui foi premature.

### Cutucada de descoberta e gatilho ADR-046

`/curate-backlog` é a **6ª skill** com `roles.required` que emite cutucada de descoberta (per ADR-046 § Decisão tabela tri-state). Isso dispara o gatilho ADR-046 linha 219: *"6ª skill com `roles.required` aparecer — herdar gatilho de ADR-029 § Gatilhos linha 110; reabrir alternativa (g) de ADR-017 (helper compartilhado) ou herança mecânica quando universo dobrar para 12+ sites."*

**Decisão:** reapply editorial inheritance (linha-ref adicionada ao procedure `docs/procedures/cutucada-descoberta.md`); defer helper compartilhado até 12+ sites per o próprio threshold de ADR-046. Justificativa: 6 skills × 2 strings = 12 sites é exatamente o limiar onde ADR-046 prescreve avaliar. Estamos no limiar, ainda cabe inheritance editorial; ultrapassar via 7ª skill emissora dispara avaliação de helper.

## Consequências

### Benefícios

- **Pattern editorial periódico capturado como mecanismo determinístico.** Preview-first beats ad hoc raw-chat para operação mutativa repetível.
- **Fronteira nítida `/next` vs `/curate-backlog`.** Tabela explícita evita scope creep; cada skill faz menos e melhor.
- **NOTES.md ganha uso decisional sem virar role.** Restrição ao escopo desta skill preserva ADR-054 § Decisão (a) — não cria contrato global; outras skills mantêm uso informational.
- **Override registrado para auditoria.** Future-self e design-reviewer free-read têm trilha empírica do override; gatilho de revisão concreto detecta over-correção.

### Trade-offs

- **+1 skill no plugin** (10 → 11). Custo de manutenção marginal; superfície semelhante a `/archive-plans` (operação periódica do mantenedor, baixa frequência).
- **Override do critério N=3 cria precedent.** Operadores futuros podem invocar o pattern ("já vi N vezes, registrar e codificar") sem registrar instâncias. Mitigação: gatilho de revisão concreto (6 meses / ≤2 invocações OR findings inúteis ≥50%) + memory `feedback_editorial_patterns_emergentes` segue sinalizando.
- **Heurísticas H2-H4 dependem de julgamento do agente runtime.** H1 é mecânico (data); H2/H3/H4 são semânticas. Spec leve por design — codificar regex de "stale" ou "mergeable" produziria falsos positivos massivos. Limitação reconhecida explicitamente.
- **Heurística 4 (NOTES.md scan) tem custo proporcional ao tamanho do store.** Scan completo na 1ª iteração (NOTES.md ≤ 1000 linhas é trivial). NOTES.md cresce monotonicamente; window cap entra apenas se scan demorar >10s (gatilho de revisão).
- **Salvaguarda worktree-probe adiciona latência mínima** (1 chamada `git worktree list --porcelain` por invocação). Aceito — overhead irrelevante vs valor do isolamento mecânico contra ADR-049 § Decisão (a).

### Limitações

- **Não cobre prioridade entre items** (escopo de `/next`).
- **Não cobre archival de planos** (`/archive-plans`).
- **Não cobre adição de items novos** (`/triage`).
- **Não cobre execução de items triviais inline** — heurística considerada e removida na 1ª iteração (YAGNI; zero evidência empírica registrada). Gatilho de reabertura abaixo se pattern emergir.

### Mitigações

- **Preview obrigatório.** Gate `AskUserQuestion` com `Cancelar` sempre disponível elimina classe de erro irreversível (mesmo pattern de `/archive-plans` e `/release`).
- **Commit unificado, no-push.** Operador decide quando publicar mutações.
- **Cutucada de descoberta + bullet em CLAUDE.md.** Skill discoverable via convenções já estabelecidas.

## Alternativas consideradas

### (a) Extensão de `/next` com modo `--full-scan`

`/next` ganha sub-modo que faz varredura editorial periódica em vez de top 3.

Descartada:

- `/next` é orientação de sessão. Mistura "candidatos a triar" com "mutações editoriais" borra fronteira UX.
- Modo `--full-scan` cria multi-shape skill (anti-padrão paralelo a ADR-036 alt (c)).
- Mesmo raciocínio de ADR-022 alt (e) que descartou `/next §6 cleanup` como entry point para archival: *"`/next` é orientação de sessão (top 3 candidatos). Archival mid-flow distrai."*

### (b) Skill unificada `/curate-repo` (BACKLOG + plans)

`/curate-repo` agrupa `/archive-plans` + `/curate-backlog` numa cadência editorial única.

Descartada:

- Multi-shape — 2 domínios (`docs/plans/` vs `BACKLOG.md`) com critérios e fontes distintas (forge auto-detect para PR detection em `/archive-plans`; NOTES.md scan em `/curate-backlog`).
- Refatora `/archive-plans` (estabilizado via ADR-022) sem dor real. Viola Ockham operacionalizado.
- Cadências editoriais possivelmente distintas; forçar unificação cria gate "aplicar plans mas não BACKLOG?" que confunde.

### (c) Não codificar; manter como pattern ad hoc (pattern ADR-036 invertido)

Aplicar ADR-036 status quo refinado — manutenção editorial periódica fica como raw-chat com Claude quando operador sente necessidade.

Descartada:

- Operador declarou ≥3 instâncias empíricas em outros repos (texto preservado em § Decisão § Override do critério N=3). ADR-036 critério 1 prescreve documentação verificável; aceitar declaração não-documentada é o **override registrado** neste ADR.
- Alt (c) seria a saída por inação que ADR-036 favorece quando evidência é fraca; ADR-057 inverte porque (i) operador aceita débito empírico explícito; (ii) gatilho de revisão concreto (6 meses) testa over-correção empiricamente; (iii) pattern repetível e mutativo (não exploratório) — preview-first mecânico beats raw-chat variável; (iv) salvaguarda worktree-probe + estrutura de signal queue não materializam consistentemente via raw-chat.

### (d) Sub-passo de `/release`

`/release` dispara curation editorial no início do fluxo (antes de bump + changelog).

Descartada:

- `/release` ganha responsabilidade nova além de version+changelog+tag.
- Cadência de release ≠ cadência de curation editorial.
- Acoplamento spurious — paralelo ao alt (d) descartado em ADR-022 pela mesma razão.

## Gatilhos de revisão

- **Over-correção do override N=3** (gatilho primário) — em **6 meses pós-shipping**, `/curate-backlog` invocado ≤2× OR findings inúteis em ≥50% das invocações reais. Sinal de codificação precoce. Ação: ADR sucessor deprecia skill e reverte para pattern ADR-036 status quo refinado (raw-chat para manutenção editorial ad hoc).
- **Findings inúteis recorrentes em heurística específica** — operador rejeita 5+ findings consecutivos da mesma categoria. Heurística calibrada errado; ajustar threshold ou remover categoria.
- **NOTES.md scan custoso** — skill demora >10s para processar. NOTES.md cresceu além do esperado; introduzir window cap (30/60/90 dias) ou indexação.
- **Heurística 4 (execução inline) ressuscita** — ≥3 instâncias auditadas de operador querendo executar item trivial durante curagem. Reabrir H4 via ADR sucessor com critério mecânico (marca `quick:`, whitelist de arquivos).
- **Salvaguarda worktree-probe rejeitada** — operador desabilita gate ≥2× expressando frustração. Reabrir desenho do worktree-probe (talvez condição mais frouxa, ex.: só worktrees com PR aberto contam).
- **7ª skill emissora de cutucada** — gatilho ADR-046 linha 219 reativado; sites = 14, ultrapassa threshold de 12. Reabrir helper compartilhado per alt (g) ADR-017.
- **Mergeable items pega falsos positivos** — operador rejeita 5+ merges consecutivamente. Anti-spam top-20 termos é insuficiente; refinar.
- **`/curate-backlog` e `/archive-plans` precisariam executar juntos** (mesma invocação) por dor real do operador — reabrir alt (b) `/curate-repo` com evidência empírica.

## Auto-aplicação coerente per ADR-034

- **Cond 1 (decisão estrutural sem ancestral direto):** aplica — nenhum ADR codifica "manutenção editorial periódica do BACKLOG" como decisão. ADR-022 codifica análoga para planos; este ADR é skill irmã, não sucessor.
- **Cond 4 (categoria nova):** aplica — "manutenção editorial periódica do BACKLOG com salvaguarda worktree-probe" é categoria conceitual nova, paralela mas distinta de "archival de planos" (ADR-022). NOTES.md como signal queue para deferred mutations é mecanismo derivado da categoria, não categoria conceitual separada (consome ADR-054 sem alterá-lo).
- **Cond 5 (sucessor parcial):** NÃO aplica primário — não substitui nem refina ADR-054 (apenas consume); não substitui ADR-022 (paralela, não sucessora); reconhece tensão com ADR-049 mas preserva substância via salvaguarda mecânica.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica.
- **Cond 3 (codifica restrição externa):** NÃO aplica.
