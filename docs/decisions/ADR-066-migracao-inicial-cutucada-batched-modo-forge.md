# ADR-066: Migração inicial em modo forge — batched-com-confirmação como 3ª categoria editorial de cutucada por mutação

**Data:** 2026-06-19
**Status:** Proposto

**Próxima revisão:** 2026-12-19
**Cadência:** trimestral
**Critério de erosão auditável:** Operador reporta fricção real (decisão estrutural não-óbvia que merecia per-item) em ≥2 migrações batched-com-confirmação reais via `/migrate-backlog-to-forge`, OR ≥1 migração batched-com-confirmação real falha mid-execução com state parcial mal-recuperado pela idempotência declarada em § Trade-offs (sinal que mitigação não cobriu na prática).

## Origem

- **Investigação:** `@design-reviewer` Finding 2 do plano `docs/plans/migrate-backlog-to-forge-skill.md` (review 2026-06-19) — identificou contradição entre cutucada batched single-call proposta pelo helper `/migrate-backlog-to-forge` e ADR-058 § (e) literal (*"sem batched para múltiplas mutações na mesma invocação"*). Operador escolheu via `/triage` step 5 enum F2 opção `Batched + ADR sucessor parcial codificando 3ª categoria editorial`.
- **Decisão base:** [ADR-058](ADR-058-role-backlog-aceitar-forge.md) § (e) — sucessor parcial editorial deste. ADR-058 vigente NÃO mutado (invariante "Não alterar ADRs existentes" preservada per CLAUDE.md § Editing conventions).
- **Empírica acumulada:** 3 migrações end-to-end materializadas em 2026-06-19 — meta-system (19 entries → gh issues #18–#36, sessão `backlog-forge-migration`), logseq-notes (1 entry → gh issue #1, sessão setup operacional), pragmatic-dev-toolkit (7 entries → gh issues #127–#133, commit `28c92a9`). 3/3 com batched single-call manual sem fricção observada em vivo.

## Contexto

ADR-058 § (e) estabelece como default editorial do modo forge: **uma cutucada por mutação**, sem batched. Justificativa doutrinal: blast radius cumulativo é o argumento — issues criadas em forge são imediatamente visíveis a todos sem chance de reverter; gate único agruparia decisões irreversíveis num clique.

Existing exception documentada em ADR-058 § (e): **batched-com-seleção** para `/run-plan §3.5` `[capture:backlog]` — justificada pela acumulação cross-passos do `/run-plan` (warnings pré-loop + passo 2 + passo 3.2 até 5+ markers; cutucada granular geraria N cliques fadigosos).

3 migrações end-to-end de `BACKLOG.md` → forge issues materializadas em 2026-06-19 expuseram 3ª categoria distinta: **migração inicial**. Substância:

- N issues criadas com body padronizado idêntico (entry prose + footer `Migrado de BACKLOG.md em <data>`)
- 1 drain marker em `## Próximos`
- 1 config flip `paths.backlog: forge` em `CLAUDE.md`
- 1 commit unificado + push
- 1 comment opcional na issue ancora do gap (#125 caso aplicável)

Operador foi confrontado nas 3 invocações com a mesma decisão estrutural: "autorizar batch completo OR revisar títulos OR cancelar". Decisão real é **title generation + batch authorization** — não decisão por issue independente (cada entry já foi previamente decidida quando registrada em `## Próximos`).

Doutrina ADR-058 § (e) default "uma cutucada por mutação" aplicada literalmente significaria N+3 cutucadas (N por issue + 1 drain + 1 config + 1 commit/push). Para meta-system N=19, seriam 22 cliques irritando o operador power-user com decisões sem substância nova (cada cutucada apresenta a mesma decisão de fato). Critério de "decisão irreversível por clique" do default ADR-058 não bate aqui: a decisão real (autorizar a migração) é única; multiplicar cutucadas é cerimônia ornamental anti-ADR-002.

## Decisão

Codificar **3ª categoria editorial de cutucada por mutação no modo forge**: **batched-com-confirmação** para migração inicial. Sucessor parcial editorial de ADR-058 § (e) — adiciona 3ª linha à taxonomia documentada sem mutar ADR-058 vigente.

Taxonomia completa:

1. **Granular per-mutação** (default ADR-058 § (e)) — 1 cutucada `AskUserQuestion` (header `Forge`) por mutação. Aplica em `/triage` step 4 (criação de issue feature em curso + capturas fora-de-escopo). **Substância:** cada mutação é decisão estrutural independente.
2. **Batched-com-seleção** (sub-caso editorial ADR-058 § (e)) — 1 cutucada agrupada com `AskUserQuestion` 4 opções (`Aplicar todas` Recommended / `Selecionar quais` / `Manter como pendentes` / Other → revisar antes). Aplica em `/run-plan §3.5` `[capture:backlog]`. **Substância:** signal acumula cross-passos do `/run-plan` (até 5+ markers); cutucada granular geraria fadiga.
3. **Batched-com-confirmação** (esta categoria) — 1 cutucada unificada `AskUserQuestion` 3 opções (`Aplicar batch completo` Recommended / `Revisar antes (loop per-item)` / `Cancelar`) antes da 1ª mutação remota; autorização cobre TODAS as N mutações + side-effects relacionados (drain + config + commit + push). Aplica em `/migrate-backlog-to-forge` v0. **Substância:** N mutações com body padronizado idêntico; decisão real é title generation + batch authorization (não decisão por mutação independente).

### Critério de discriminação cross-categoria (predicado mecânico)

**Eixo primário: heterogeneidade decisional** — alinhamento mecânico com ADR-058 § (e) blast-radius critério original (decisões substancialmente distintas merecem granularidade independente de onde acumulam). Eixo secundário: origem do signal (informativo, não-determinante em casos de conflito).

| Categoria | Heterogeneidade decisional (primário) | Origem do signal (secundário) |
|---|---|---|
| 1ª granular | ≥2 decisões estruturais distintas por mutação | Operador raciocínio per-item |
| 2ª batched-com-seleção | Decisões homogêneas mas dispersas cross-passos | Acumulação editorial via skill multi-step |
| 3ª batched-com-confirmação | Decisões homogêneas concentradas em 1 invocação | Migração inicial / bulk import / one-shot |

**Rebate de contraexemplo concreto:** bulk operation futura tipo `/curate-backlog` em modo forge varrendo N issues stale e propondo close em batch — signal concentrado em 1 invocação **mas** cada close exige avaliação contextual única (heterogeneidade decisional alta). Pelo eixo primário, cai em 1ª categoria (granular per-mutação) apesar de pattern operacional batched-like. Hierarquia explícita: heterogeneidade decisional > origem do signal em casos de conflito.

### Mecânica da 3ª categoria

- Cutucada `AskUserQuestion` única antes da 1ª mutação remota (gate antes batched).
- `Aplicar batch completo` autoriza TODAS as mutações + side-effects (drain + config + commit + push em 1 fluxo).
- `Revisar antes (loop per-item)` cai num loop de cutucada granular per-item ainda gateado por confirmação final batched (combinação 1ª + 3ª).
- `Cancelar` aborta sem mutações remotas.
- **Idempotência:** re-invocação detecta state pós-migração (marker drain + config já flippado) e para fail-fast com mensagem clara.

## Consequências

### Benefícios

- UX hostil de N+3 cutucadas eliminada (meta-system 19 entries → 22 cliques sem decisão substantiva nova).
- Operador power-user atendido sem multiplicar cerimônia anti-ADR-002.
- Pattern empírico (3 migrações de hoje) codificado canonicamente em vez de ad-hoc replay.
- Taxonomia documentada em ADR-058 § (e) ganha 3ª linha sem mutar ADR vigente — preserva invariante editorial "Não alterar ADRs existentes".

### Trade-offs

- Poder do operador sobre revisão per-item movida para opção secundária (`Revisar antes` no enum). Default Recommended é trust-batch.
- Helper sub-tool concentra side-effects em 1 ponto — falha mid-execução em N+1ª issue deixa state parcial (N-1 issues criadas + drain ainda não aplicado). Mitigação: sub-tool re-executável é idempotente (detecta state parcial via marker drain).

### Limitações

- v0 cobre apenas migração inicial (file → forge). Bulk import de issues sem `BACKLOG.md` pré-existente (e.g., consolidar issues órfãs cross-repo) **NÃO aplica** esta categoria — cabe avaliação separada.
- Restrita a modo forge — operações analógicas em modo arquivo (e.g., bulk move entries cross-files) **NÃO cobertas** (ADR-058 sub-decision scope-restricted).
- gh-only v0 — quando glab materializar 1ª migração, padrão batched-com-confirmação deve ser revisitado se semantics divergirem significativamente (e.g., MR vs PR semantics afetando issue auto-close trailer).

## Gatilhos de revisão

1. Operador reportar fricção real com batched-com-confirmação em invocação ≥2ª (decisão estrutural não-óbvia que merecia per-item), OR opção `Revisar antes (loop per-item)` materializar fricção de UX em ≥1 invocação real (forward-looking sem cobertura empírica em 2026-06-19; § Override calibração específica reconhece).
2. Helper concentrar falhas mid-execução em ≥1 invocação real (state parcial mal-recuperado por idempotência).
3. glab materializar 1ª migração e revelar que semantics divergem (cutucada model batched precisa adaptar; reabrir critério editorial cross-forge).
4. Pattern emergir em 2ª/3ª skill (bulk operation distinta de migração inicial mas com mesma heterogeneidade decisional concentrada — e.g., bulk archive, bulk close) — revisar se categoria 3ª precisa generalização ("batched-com-confirmação" não-restrito a migração inicial).

## Alternativas consideradas

### Honrar ADR-058 § (e) literal (N+3 cutucadas)

Descartada. UX hostil em migrações grandes (meta-system 19 → 22 cliques). Operador power-user reclamaria empiricamente em 1ª migração não-trivial; ADR-058 § Gatilhos prevê esse próprio gatilho ("Cutucada por mutação irrita power-user → reabrir critério batched"). Honrar literal violaria o próprio gatilho codificado.

### Batched + nota inline sem ADR (decisão tática)

Descartada. Anti-disciplina — divergência silenciosa de ADR-058 § (e) sem rebate documentado. 2ª migração análoga repetiria o padrão sem auditoria. Operador escolheu disciplinadamente via `/triage` F2 enum sucessor parcial em vez de tática localizada.

### Generalizar 2ª categoria (batched-com-seleção) cobrindo migração inicial

Descartada. Substância dispersa cross-passos (2ª) vs concentrada 1-invocação (3ª) é categoria distinta. Generalizar perderia discriminação útil — em migração inicial não há substância adicional cross-passos pra aproveitar a seleção; reduzir-se-ia a "Aplicar todas" sempre, anti-padrão "opção sem trade-off real" do `AskUserQuestion mechanics`.

## Auto-aplicação coerente per ADR-034

Sucessor parcial editorial de ADR-058 § (e). Aplicação das 5 condições:

- **Cond 1 (decisão estrutural sem ancestral):** NÃO aplica — ancestral direto é ADR-058 § (e); taxonomia 1ª/2ª já-existente é ponto de partida.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — ADR-058 vigente preservado intacto; este ADR adiciona 3ª linha à taxonomia sem mutar.
- **Cond 3 (codifica restrição externa):** NÃO aplica — substância é decisão editorial interna do toolkit (modelo de cutucada em modo forge), sem origem em regulação/contrato/plataforma externa.
- **Cond 4 (introduz categoria conceitual nova):** NÃO aplica — taxonomia 1ª/2ª já estava aberta em ADR-058 § (e); 3ª linha estende a taxonomia existente, não cria novo eixo conceitual. Contra-leitura legítima: "categoria editorial 'batched-com-confirmação' é novo nome" — rebatida porque o eixo (cutucada por mutação no modo forge) é o mesmo de ADR-058; nomes de linhas dentro de taxonomia existente não constituem categoria conceitual nova.
- **Cond 5 (sucessor parcial):** APLICA — sucessor parcial editorial de ADR-058 § (e) reconhecendo divergência empírica + 3 instâncias materializadas + UX hostil de literal honor. ADR-058 vigente NÃO mutado.

Cond 5 isolada aplica per critério de admissão de ADR-034 (sucessor parcial editorial é caso central). Bloco mecânico paralelo ao precedent ADR-058 § Auto-aplicação + ADR-065 § Auto-aplicação.

## Override do critério N=3

7ª aplicação consecutiva após ADR-057→-061→-062→-063→-064→-065 (calibração explícita reconhecendo fragilidade epistêmica acumulada).

**Empírica deste ADR:** N=3 migrações end-to-end em 1 dia (meta-system + logseq-notes + pragmatic-dev-toolkit). 3 instâncias same-day same-operator cobertura forge restrita (gh-only). Forte para confirmar pattern operacional; fraca para confirmar generalização cross-forge.

**Caráter da fragilidade desta aplicação:**

- Pattern materializou-se durante `/triage` dispatchado em mesma sessão CC — mesma janela cognitiva.
- Decisão de codificar veio do design-reviewer F2 (não emergindo from grassroots backlog signal), enquadrando como rebate-de-contradição doutrinal.
- Operador confirmação via enum em mesma sessão — sem janela de "sit on it".

**Por que codificar mesmo assim:**

- Contradição doutrinal explícita com ADR-058 § (e) precisa de ADR sucessor parcial (caminho disciplinado per ADR-053 § Decisão (c) cond (ii) "contradiz decisão documentada em ADR").
- Alternativa (silent divergence ou ad-hoc inline) viola disciplina — vamos pagar custo de cristalização agora vs custo de inventário stale acumulando.
- Override codificado com Gatilho de revisão #1 acima (próximas migrações reabrem se semantics não baterem).

**Calibração específica desta aplicação:** sinal empírico cobre apenas a opção `Aplicar batch completo` do enum proposto na § Mecânica (3 migrações materializadas com essa opção); opções `Revisar antes (loop per-item)` e `Cancelar` são forward-looking sem N=1. § Mecânica codifica enum completo por coerência de contrato, mas próxima invocação que escolher `Revisar antes` materializa teste empírico forward — fricção real reabre o critério editorial. Gatilho de revisão #1 ampliado pra cobrir esse vetor explicitamente.
