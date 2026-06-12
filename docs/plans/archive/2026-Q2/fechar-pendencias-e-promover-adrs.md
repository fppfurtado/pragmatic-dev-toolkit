# Plano — Fechar pendências de validação e promover ADRs Strong para Aceito

## Contexto

Onda editorial 2026-05-15: pendências de validação ativas em 4 planos seguem sem regressão observada em uso real (gates manuais e dogfood pós-release cobriram o contrato); ADRs em `Proposto` com evidência empírica acumulada merecem promoção a `Aceito` para refletir o estado de fato. Escopo decidido em `/triage` com o operador via enum `Escopo ADRs`: **ampla com critério** — promover apenas ADRs `Strong` (shipped + dogfood/múltiplas invocações registradas + sem regressão), manter `Medium`/`Weak` em `Proposto` (Medium = uso real incipiente; Weak = ADR explicitamente reserva validação pós-release ou recém-shipped sem dogfood).

**Régua editorial vs doutrina.** A régua Strong/Medium/Weak aplicada nesta onda é **mais conservadora** que `skills/new-adr/SKILL.md:105` ("pós-revisão vira Aceito"): aqui a transição Proposto→Aceito exige dogfood acumulado, não apenas revisão. Para os ADRs mantidos em Proposto neste lote, o estado sinaliza "aguarda dogfood", não "aguarda revisão" — distinção semântica preservada por esta onda, sem alterar a doutrina escrita.

**Linha do backlog:** plugin: onda editorial 2026-05-15 — fechar pendências de validação ativas em 4 planos + promover 7 ADRs Strong de Proposto→Aceito.

**ADRs candidatos:** ADR-005, ADR-011, ADR-015, ADR-020, ADR-021, ADR-023, ADR-026.

## Resumo da mudança

**Bloco 1 — Fechar pendências de validação em 3 planos.** Marcar bullets ativos com strikethrough + "Encerrada 2026-05-15: sem regressão observada em uso real subsequente" (convenção já estabelecida nos planos `captura-automatica-imprevistos`, `d2-state-em-git`, `desacoplar-gh-em-skills`, `instrumentar-skills-multi-passo`). Planos tocados:

- `marketplace-prep-batch-2-ci-validate`: cenários 1 e 3 (gh pr checks verde + Python ≥3.10) — Action vermelha/verde observada em todos PRs #54-#66 da Onda 2026-05-12 e subsequentes sem regressão.
- `procedures-cleanup-pos-merge`: cenários 1-6 + 8-10 (smoke detection em consumers GitHub/GitLab/host-não-mapeado/`gh` ausente/`glab` ausente/`/release` squash/mix mergeada-órfã/órfã/`jq` ausente) — fluxo `/triage` step 0 cleanup pós-merge exercitado em sessões reais sem regressão.
- `next-varrer-pendencias-validacao`: nota empírica do design-reviewer (1ª ocorrência de gap "auto-detect de forge"; reabrir critério só se 2ª aparecer) — 2ª ocorrência não emergiu desde então.

**Cenário 1 de `run-plan-3-3-skip-empirico`** NÃO é fechado neste plano — é inconsistência editorial substantiva (fixture descreve grep que produziria matches espúrios), não validação de comportamento. Capturado como item separado em `## Próximos`.

**Bloco 2 — Promover 7 ADRs Strong: `**Status:** Proposto` → `**Status:** Aceito`.** Edit cirúrgico de 1 palavra por ADR. Justificativa por ADR:

- **ADR-005** (modo local-gitignored) — shipped via PR #43 (2026-05-04); em uso ativo no consumer `connector-pje-mandamus-tjpa` per memória de incidente; allowlist do hook `block_gitignored` corrigida em commit posterior por regressão real do contrato.
- **ADR-011** (wiring design-reviewer automático) — wiring ativo em `/triage` e `/new-adr`; commits subsequentes registram findings absorvidos pré-commit em múltiplos planos (ADR-025, ADR-026, ADR-028, ADR-030 e PRs derivados).
- **ADR-015** (bloquear env por sufixo) — hook ativo desde shipping; 20 fixtures de smoke documentadas no plano; sem incidente de bypass desde então.
- **ADR-020** (critério mecânico admissão warnings pré-loop) — em uso por `/run-plan` em todas as execuções pós-shipping (Ondas 2026-05-12 + planos subsequentes).
- **ADR-021** (curadoria free-read design-reviewer) — campo `**ADRs candidatos:**` em uso em planos Onda 4 + posteriores; mecanismo de priorização exercitado pelo reviewer em múltiplas invocações.
- **ADR-023** (critério mecânico `disable-model-invocation`) — tabela retroativa aplicada às 9 skills no próprio ADR; convenção honrada na skill `/draft-idea` (ADR-027) explicitamente.
- **ADR-026** (critério mecânico absorção findings design-reviewer) — em uso explícito (Concluídos do BACKLOG: "X findings do design-reviewer absorvidos no plano" em ADR-025, ADR-028, ADR-030).

**ADRs mantidos em Proposto** (sem alteração neste plano):

- **ADR-022** (archival `docs/plans/`) — `Medium`: skill `/archive-plans` shipped, mas archival é editorial periódico (não cobre janela ainda); reavaliar após 1ª archival real.
- **ADR-024** (categoria `docs/procedures/`) — `Medium`: `cleanup-pos-merge.md` é consumido em runtime sem regressão, mas o ADR §Limitações reconhece "categoria nova com 1 item é YAGNI suspeito" e §Gatilhos exige "próximo procedimento proposto exercita os 3 critérios em fluxo real" — runtime consumption valida leitura, não admissão. Gatilho de promoção: 2º procedimento extraído passando pelos 3 critérios cumulativos.
- **ADR-025** (recusar cross-mode `backlog: local + plans_dir: canonical`) — `Weak`: ADR explicitamente registra "Status preservado em Proposto" pendente de smoke em consumer real.
- **ADR-027** (skill `/draft-idea`) — `Weak`: "Validação manual (5 cenários: one-shot, update, Other em one-shot, cutucada descoberta, update + Other) fica como spec para smoke pós-release".
- **ADR-028** (campo `**Branch:**` opcional) — `Medium`: shipped via PR #66 (2026-05-13); poucos usos issue-first reais ainda.
- **ADR-029** (cutucada `CLAUDE.md` ausente) — `Medium`: shipped recente, cutucada string-B ainda não exercitada em consumer com `CLAUDE.md` ausente.
- **ADR-030** (aceitar `CLAUDE.md` gitignored) — `Weak`: shipped via PR #65 (2026-05-14); sem dogfood acumulado ainda.

Reavaliação destes 7 fica para próxima onda editorial (gatilho: cada ADR carrega critério próprio — uso real exercitando o contrato).

## Arquivos a alterar

### Bloco 1 — Fechar pendências de validação em planos

- `docs/plans/marketplace-prep-batch-2-ci-validate.md`: na seção `## Pendências de validação`, envolver cada bullet ativo (cenários 1 e 3) com `~~...~~` e acrescentar `**Encerrada 2026-05-15:** sem regressão observada — Action verde exercitada em todos PRs #54-#66 da Onda 2026-05-12 e subsequentes.`
- `docs/plans/procedures-cleanup-pos-merge.md`: na seção `## Pendências de validação`, dividir cenários em dois grupos por acessibilidade ao dogfood do próprio repo (GitHub-only):
  - Cenários (1) GitHub squash-merge, (6) `/release` squash, (8) mix mergeada/órfã, (9) órfã pura — envolver com `~~...~~` e acrescentar `**Encerrada 2026-05-15:** sem regressão observada em uso real do toolkit no próprio repo.`
  - Cenários (2) GitLab squash, (3) host não-mapeado, (4) `gh` ausente, (5) `glab` ausente, (10) `jq` ausente — envolver com `~~...~~` e acrescentar `**Encerrada 2026-05-15 (validação herdada por simetria mecânica do auto-detect bilateral; smoke real em consumer correspondente não exercitado):** reabrir gatilho do plano se operador adotar consumer GitLab/Bitbucket no futuro.` Honestidade arqueológica preservada — leitor futuro vê a distinção entre dogfood direto e simetria mecânica.
- `docs/plans/next-varrer-pendencias-validacao.md`: na seção `## Pendências de validação`, envolver a nota empírica do design-reviewer com `~~...~~` e acrescentar `**Encerrada 2026-05-15:** 2ª ocorrência do gap não emergiu desde shipping; critério do reviewer permanece sem refinamento (YAGNI ativo).`

### Bloco 2 — Promover 7 ADRs Strong de Proposto para Aceito

- `docs/decisions/ADR-005-modo-local-gitignored-roles.md`: `**Status:** Proposto` → `**Status:** Aceito`.
- `docs/decisions/ADR-011-wiring-design-reviewer-automatico.md`: `**Status:** Proposto` → `**Status:** Aceito`.
- `docs/decisions/ADR-015-bloquear-env-files-por-sufixo.md`: `**Status:** Proposto` → `**Status:** Aceito`.
- `docs/decisions/ADR-020-criterio-mecanico-admissao-warnings-pre-loop.md`: `**Status:** Proposto` → `**Status:** Aceito`.
- `docs/decisions/ADR-021-curadoria-free-read-design-reviewer.md`: `**Status:** Proposto` → `**Status:** Aceito`.
- `docs/decisions/ADR-023-criterio-mecanico-disable-model-invocation-skills.md`: `**Status:** Proposto` → `**Status:** Aceito`.
- `docs/decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md`: `**Status:** Proposto` → `**Status:** Aceito`.

## Verificação end-to-end

- `grep -c '^\*\*Status:\*\* Aceito$' docs/decisions/*.md` aumenta em 7 (de 16 para 23).
- `grep -c '^\*\*Status:\*\* Proposto$' docs/decisions/*.md` cai em 7 (de 14 para 7 — ADR-022, 024, 025, 027, 028, 029, 030).
- `grep -n '^- ' docs/plans/marketplace-prep-batch-2-ci-validate.md docs/plans/procedures-cleanup-pos-merge.md docs/plans/next-varrer-pendencias-validacao.md` mostra que toda linha não-strikethrough na seção `## Pendências de validação` foi marcada com `~~...~~` + `**Encerrada 2026-05-15:**` (com cláusula de simetria mecânica nos 5 cenários inacessíveis ao dogfood do `procedures-cleanup-pos-merge`).
- `run-plan-3-3-skip-empirico` permanece intocado (escopo separado capturado como item fora-do-escopo em `## Próximos` no commit `/triage`).

## Notas operacionais

- Refactor editorial puro — doc-only, zero impacto em runtime. `## Verificação manual` omitida (sem comportamento perceptível alterado).
- Ordem dos blocos é indiferente (independentes). Bloco 1 e Bloco 2 podem ser commitados juntos ou separados conforme decisão do `/run-plan`.
- Cada bloco recebe `doc-reviewer` por default (paths todos `.md`). Anotação `{reviewer: doc}` omitida por economia, conforme convenção do template.
