# Plano — Prazo canonical de revisão temporal em ADRs futuros

## Contexto

Operacionaliza a 3ª/última follow-up deferida em [meta-system ADR-021 § Limitações](https://github.com/fppfurtado/meta-system/blob/main/docs/decisions/ADR-021-auto-critica-permanente-4o-principio-fundamental.md) — 4º princípio fundamental "Auto-crítica permanente". Predecessoras shipped 2026-06-15:

- 1ª: `/doctrine-audit` skill local meta-reflexiva.
- 2ª: retrofit prazo nos 8 ADRs apex do meta-system via PR #15 squash `92c1892` — ADRs apex ganharam bloco metadata 3-linhas com substância per-ADR via cutucada inline + Goodhart guard real.

Esta 3ª codifica o mecanismo proativo para que ADRs **futuros** já carreguem prazo canonical de revisão por construção (template-driven), sem depender de retrofit reativo.

**Linha do backlog:** plugin: prazo canonical de revisão temporal em ADRs futuros — `/new-adr` template (`templates/adr.md`) + skill `/new-adr` SKILL.md ganham bloco metadata canonical com 3 campos bold-paragraph: `**Próxima revisão:**` + `**Cadência:**` + `**Critério de erosão auditável:**`. Operacionalização da **3ª/última das 3 follow-ups deferidas** em meta-system [ADR-021](https://github.com/fppfurtado/meta-system/blob/main/docs/decisions/ADR-021-auto-critica-permanente-4o-principio-fundamental.md) § Limitações (4º princípio fundamental "Auto-crítica permanente").

**ADRs candidatos:** ADR-053 (sucessor parcial editorial — § Decisão (b) ganha cláusula proativa paralela à reativa existente, **não edit no ADR vigente** per cond 5 ADR-034 + invariante "Não alterar ADRs existentes"); ADR-034 (cond 5 — sucessor parcial via novo ADR é a forma correta); ADR-043 (§ Ockham operacionalizado #4 — override do critério N=3 documentado no novo ADR, 1ª instância sub-N3).

## Resumo da mudança

Decisões pré-fato (resolvidas no `/triage`):
- **Template inline preservado** em `skills/new-adr/SKILL.md` (não externalizar para `templates/adr.md` — YAGNI; nenhum 2º consumidor justifica externalização).
- **Cutucada per-novo-ADR só para `**Critério de erosão auditável:**`** (paralelo à mecânica `/run-plan` do plano `retrofit-prazo-revisao-temporal-adrs.md` do meta-system); `**Próxima revisão:**` + `**Cadência:**` ganham defaults editoriais auto-preenchidos.
- **(c) incluído agora** como novo ADR (cond 5 ADR-034 sucessor parcial editorial de ADR-053).

3 blocos coordenados, ordem importa (Bloco 1 cria ADR → Blocos 2+3 referenciam o número):

1. **Bloco 1 — ADR sucessor parcial de ADR-053 § Decisão (b)** via `/new-adr` delegada. Cláusula doutrinal de "prazo temporal proativo" paralela ao wiring reativo existente. Mecânica de execução reconhecidamente especulativa (quem dispara revisão periódica? `/curate-backlog` estendido? skill nova?) — substância doutrinal registrada agora; mecânica cristaliza em onda futura quando erosão acumulada justificar. § Override do critério N=3 dedicada com sub-N3 explícito (1ª instância no toolkit; precedente análogo aos ADR-057/-061/-062/-063/-064). § Auto-aplicação examina **as 5 cond ADR-034 explicitamente** (pattern editorial de ADR-053 § Auto-aplicação): cond 5 APLICA isoladamente (sucessor parcial de ADR-053); cond 4 NÃO APLICA (substância importada do meta-system como mecanismo cross-projeto, não categoria emergente N≥3 do plugin); cond 1/2/3 NÃO APLICAM com argumento. § Decisão registra rebate explícito da alternativa "cutucada para os 3 campos" (Cadência + Próxima revisão herdam defaults canonical como safety-net editorial — `currentDate + 6 meses` e `trimestral`; defaults são reversíveis por revisão pós-fato; Critério é o único campo cuja substância semântica per-ADR não pode ser inferida).

2. **Bloco 2 — `skills/new-adr/SKILL.md`** (edit cirúrgico em path-set narrow per ADR-063 → `@prompt-reviewer` pré-commit). 2 sub-edits:
   - **2.1** Template inline (linhas 77-98) ganha bloco metadata HTML-comentado entre `**Status:** Proposto` e `## Origem`:

     ```markdown
     **Próxima revisão:** <currentDate + 6 meses>
     **Cadência:** <trimestral|semestral|anual>
     **Critério de erosão auditável:** <condição substantiva per-ADR; Goodhart guard explícito — não placeholder cosmético tipo "reavaliar em 6 meses">
     ```

     Bloco **visível** (placeholders explícitos, paralelo aos demais placeholders do template inline em linhas 80-93 — `<Título>`, `<YYYY-MM-DD>`, `<Frase direta...>`). Consistência editorial preservada per ADR-055 § Decisão (a) classificação inline-prose tutorial. `/new-adr` step 4 substitui placeholders durante preenchimento (mesmo pattern dos demais).

   - **2.2** § Passos passo 4 ganha cutucada per-novo-ADR para `**Critério de erosão auditável:**` (modo prosa-livre via `AskUserQuestion` Other ou prompt direto — Goodhart guard explícito na pergunta: "Que condição auditável reabriria este ADR? Substância semântica per-ADR, não placeholder genérico tipo 'reavaliar em 6 meses'."). Defaults editoriais auto-preenchidos pela skill: `**Próxima revisão:** <currentDate + 6 meses canonical>`, `**Cadência:** trimestral`.

3. **Bloco 3 — `CLAUDE.md` § Editing conventions** (1 edit). Adicionar bullet referenciando o novo ADR + 1-2 linhas resumindo a doutrina (paralelo aos bullets existentes que referenciam ADRs-049/-053/-057/-061/-062/-063/-064).

## Arquivos a alterar

### Bloco 1 — ADR sucessor parcial via `/new-adr` delegada

- `docs/decisions/ADR-NNN-prazo-canonical-revisao-temporal-adrs-futuros.md`: criado via `/new-adr` skill. Título: "Prazo canonical de revisão temporal em ADRs futuros". Substância:
  - § Origem: link à 3ª follow-up de meta-system ADR-021 + predecessoras 1ª/2ª shipped 2026-06-15; ADR-053 § Decisão (b) como decisão base extendida.
  - § Decisão: cláusula proativa paralela à reativa de ADR-053 § Decisão (b); bloco metadata 3-campos canonical no template; cutucada per-novo-ADR só para `**Critério de erosão auditável:**`; defaults editoriais (currentDate + 6 meses, trimestral) para os outros 2 campos; Goodhart guard documentado na semântica da cutucada.
  - § Override do critério N=3 (ADR-043 § Ockham operacionalizado #4): sub-N3 explícito (1ª instância). Calibração com precedentes -057/-061/-062/-063/-064.
  - § Auto-aplicação: cond 5 ADR-034 sucessor parcial isolada.
  - § Gatilhos de revisão: mecânica de execução proativa cristaliza quando ≥1 ADR vigente erodir sem detecção pela onda reativa atual (sinal empírico); ou quando defaults editoriais (`6 meses`/`trimestral`) mostrarem-se off-mark em 2-3 ADRs criados.

Reviewer: omitido (anotação não usada para bloco delegada a `/new-adr`; `/new-adr` step 5 já invoca `@design-reviewer` per ADR-053 § Decisão (b)).

### Bloco 2 — skills/new-adr/SKILL.md (template + cutucada) {reviewer: prompt}

- `skills/new-adr/SKILL.md`:
  - **Template inline** (linhas 77-98 do estado pré-edit): inserir bloco metadata **visível** (placeholders explícitos, paralelo aos demais placeholders do template inline) entre linha `**Status:** Proposto` e header `## Origem`.
  - **§ Passos passo 4** (após "Preencher conteúdo derivado..." e antes do step 5): adicionar sub-passo prescrevendo cutucada per-novo-ADR para `**Critério de erosão auditável:**` com Goodhart guard explícito + defaults canonical para os outros 2 campos. Referenciar ADR-NNN (substituído pelo número real do ADR criado no Bloco 1) como decisão base.
  - **§ O que NÃO fazer**: adicionar bullet "Não aceitar placeholder cosmético em `**Critério de erosão auditável:**` (Goodhart guard — cutucada rejeita 'reavaliar em 6 meses'/'revisar quando relevante' e exige condição substantiva per-ADR)".

**Substituição de placeholder cross-ref.** Bloco 2 substitui `ADR-NNN` (placeholder neste plano) pelo número real do ADR criado no Bloco 1, em todos os locais onde aparece nos edits do SKILL.md (template inline + § Passos passo 4). Sem substituição, placeholder vira ADR-rot. Verificação mecânica em § Verificação end-to-end abaixo.

### Bloco 3 — CLAUDE.md § Editing conventions {reviewer: doc}

- `CLAUDE.md`: adicionar bullet em § Editing conventions referenciando o novo ADR (`**Prazo canonical de revisão temporal em ADRs futuros**: ...`) + 1-2 linhas resumindo a doutrina + cross-refs para ADR-053 (extendido) + ADR-034 cond 5 (forma do sucessor) + ADR-043 § Ockham operacionalizado #4 (override N=3).

## Verificação end-to-end

- ADR vigente criado: `^\*\*Status:\*\* Proposto` ou `^\*\*Status:\*\* Aceito` em `docs/decisions/ADR-<saldo>-prazo-canonical-revisao-temporal-adrs-futuros.md`.
- Template inline editado: `grep "Próxima revisão" skills/new-adr/SKILL.md` retorna ≥1 match (bloco metadata + cutucada).
- Cutucada wireada: `grep "Critério de erosão auditável" skills/new-adr/SKILL.md` retorna ≥2 matches (1 template + 1 passo).
- Goodhart guard documentado: `grep -i "Goodhart" skills/new-adr/SKILL.md` retorna ≥1 match.
- Defaults canonical wireados: `grep "currentDate" skills/new-adr/SKILL.md` retorna match novo no passo da cutucada (paralelo ao uso pré-existente em passo 3).
- CLAUDE.md atualizado: `grep "prazo-canonical-revisao-temporal" CLAUDE.md` retorna ≥1 match.
- Cross-ref bidirecional: novo ADR referencia ADR-053 § Decisão (b); CLAUDE.md referencia novo ADR.
- **Placeholder `ADR-NNN` resolvido**: `grep -c "ADR-NNN" skills/new-adr/SKILL.md CLAUDE.md` retorna `0` em ambos (placeholder substituído pelo número real do ADR criado no Bloco 1).

## Verificação manual

Skill `/new-adr` é wiring → impacto comportamental só ativa pós-`/reload-plugins` em sessão CC nova (per pattern NOTES.md 2026-06-15T14:32:03Z — dogfood-recursive limit, 1ª instância empírica). Cenários comportamentais deferem para `## Pendências de validação`.

Cenários textuais validados in-flight (via `/run-plan §3.2` gate):
- Bloco metadata HTML-comentado presente no template inline com 3 campos canonical na ordem prescrita.
- Cutucada per-novo-ADR específica para `**Critério de erosão auditável:**` registrada em § Passos (não confunde com a cutucada step 3.5 do filtro de admissão ou step 5 do design-reviewer).
- Goodhart guard explícito no texto da cutucada + reforçado em § O que NÃO fazer.
- Defaults canonical para `**Próxima revisão:**` (currentDate + 6 meses) e `**Cadência:**` (trimestral) declarados no passo.
- Novo ADR carrega § Decisão estendendo ADR-053 § Decisão (b) sem revogar (cond 5 ADR-034).

## Pendências de validação

- **[capture:backlog]** Smoke comportamental `/new-adr` prazo-canonical pós-`/reload-plugins` em sessão CC nova com check-list mecânico: (1) cutucada `AskUserQuestion` dispara para `**Critério de erosão auditável:**` no §Passos passo 4; (2) Goodhart guard rejeita placeholder vago (resposta tipo "reavaliar em 6 meses" recusada com prompt de refinamento) e aceita condição substantiva per-ADR; (3) defaults canonical (`currentDate + 6 meses`, `trimestral`) auto-preenchidos sem prompt; (4) bloco metadata visível no ADR final com 3 campos preenchidos — `grep "^\*\*Próxima revisão:" docs/decisions/ADR-<saldo+1>-*.md` retorna ≥1 match; `grep -i "reavaliar em 6 meses" docs/decisions/ADR-<saldo+1>-*.md` retorna 0 (Goodhart guard funcionou).
- **[capture:backlog]** Calibração empírica dos defaults canonical: após N=3 ADRs criados com defaults, sample dos campos `**Próxima revisão:**` + `**Cadência:**`; se ≥1 mostrar-se off-mark (operador edita pós-criação ≥2 vezes), refinar via novo `/triage`.
- **[capture:backlog]** Auditoria post-mortem trimestral do Goodhart guard: sample dos `**Critério de erosão auditável:**` preenchidos em ADRs criados pós-shipping; ≥1 placeholder cosmético detectado retroativamente → reabrir mecanismo (refinar prompt da cutucada, escalar para `@design-reviewer` validar Critério como finding pré-commit, ou adicionar 2ª pergunta de checagem). Gatilho de revisão concreto.
- Quando shipped: meta-system ADR-021 § Limitações 4ª linha ganha Adendo final "Restam **0 follow-ups deferidas** — princípio 4 plenamente operacionalizado"; entry em meta-system BACKLOG migra de Próximos para Concluídos. Pattern dual-entry (entry mensageira aqui + entry recíproca em meta-system BACKLOG) honrado.

## Notas operacionais

- **Ordem dos blocos importa.** Bloco 1 (ADR criado via `/new-adr`) primeiro porque Blocos 2+3 referenciam o número do ADR.
- **Memory `feedback_dogfood_doctrinal_reform` aplicada.** Bloco 1 usa `/new-adr` skill — não escrever ADR manualmente.
- **Memory `feedback_clarify_before_enum` aplicada.** Substância doutrinal não-trivial explicada em prosa antes do enum no `/triage` step 2 (3 gaps explicados, 3 enums).
- **Memory `feedback_editorial_patterns_emergentes` consultada.** Esta é onda de codificação proativa, não retrofit. Sub-N3 (1ª instância no toolkit). Override de N=3 codificado dedicado no novo ADR § Override.
- **Pattern dogfood-recursive limit** (NOTES.md 2026-06-15T14:32:03Z): cenários comportamentais que exercitam o próprio wiring sendo aplicado deferem para `## Pendências de validação` post-`/reload-plugins`. Aplicado: cenários textuais validados in-flight, comportamentais deferidos.
- **ADR-053 vigente NÃO mutado.** Cond 5 ADR-034 prescreve sucessor parcial via novo ADR + invariante "Não alterar ADRs existentes" em `CLAUDE.md`/`skills/new-adr/SKILL.md`.

## Decisões absorvidas

- Bloco 2 template: bloco metadata trocou de HTML-comentado para placeholders visíveis (consistência editorial ADR-055 inline-prose tutorial) (caminho-único).
- Bloco 1 § Auto-aplicação: examinar todas 5 cond ADR-034 explicitamente (pattern ADR-053 § Auto-aplicação); cond 5 isolada APLICA; cond 4 NÃO APLICA com argumento "substância importada do meta-system, não categoria emergente N≥3 do plugin" (caminho-único).
- Bloco 1 § Decisão: rebate explícito da alternativa "cutucada para os 3 campos" — Cadência/Próxima revisão herdam defaults safety-net; Critério é o único campo cuja substância semântica per-ADR não pode ser inferida (caminho-único).
- § Pendências de validação: check-list mecânico com greps + 3 marker `[capture:backlog]` para smoke pós-`/reload-plugins`, calibração de defaults e auditoria post-mortem trimestral Goodhart (caminho-único).
- Bloco 2 + § Verificação end-to-end: cláusula de substituição placeholder `ADR-NNN` → número real + grep mecânico verificando resolução (caminho-único).
