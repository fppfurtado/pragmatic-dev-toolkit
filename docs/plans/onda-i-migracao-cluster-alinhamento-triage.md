# Plano — Onda I da redesign da camada doutrinal (migração cluster alinhamento/triage)

## Contexto

**ADRs candidatos:** ADR-011 (wiring automático do design-reviewer em `/triage` plan-producing + `/new-adr`; sucessor parcial de ADR-009), ADR-026 (critério mecânico de absorção de findings do design-reviewer pré-commit — 3 condições + default absorvedor; sucessor parcial de ADR-011), ADR-027 (skill `/draft-idea` para elicitação estruturada de `product_direction`/IDEA.md; alinhamento upstream de `/triage`), ADR-038 (mirror das Decisões absorvidas no plan body + consumo runtime por reviewers via `/run-plan` §2.3; sucessor parcial de ADR-026), ADR-045 (apex redesign — esta onda materializa § Decisão parte 1 § Implementação literal), ADR-046+ADR-047+ADR-048+ADR-049+ADR-050+ADR-051 (templates do pattern de migração validado em Ondas C+D+E+F+G+H), ADR-052 (meta-pattern editorial canonical — primeira aplicação formal com modo (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO sobre ADR-009 e modo (a) EXCLUSÃO sobre ADR-042), **ADR-009 PRESERVADO vigente fora do cluster** por constraint mecânico (hardcoded na always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]`) — análogo a ADR-034 em Onda H, **primeira aplicação formal de ADR-052 § Decisão (c)**, ADR-042 EXCLUÍDO por desalinhamento semântico do sketch — modo (a) ADR-052 § Decisão (a) bullet 2 (`/note` cross-project write pertence ao cluster bridge/discoverability junto com ADR-032; sketch original do charter listou ADR-042 em 2 clusters distintos — contradição interna análoga a ADR-039 em F), ADR-034 (critério adendo vs novo ADR — cond 5 primária absorvendo 4 ADRs; cond 4 NÃO aplica per F4 Ondas C-H; cond 1 NÃO aplica — ADR-045/-046/-047/-048/-049/-050/-051/-052 ancestrais codificados; cond 2 NÃO aplica — regra central de cada ADR absorvido preservada integralmente).

Onda I (nona) da redesign da camada doutrinal coordenada por `docs/plans/redesign-camada-doutrinal-charter.md`. **Sétima migração cluster temático** per ADR-045 § Decisão parte 1 § Implementação literal — Ondas C+D+E+F+G+H precederam (cutucadas, modo local, reviewers/curadoria, execução/run-plan, componentes plugin, convenções editoriais). **Primeira onda pós-ADR-052** — referência formal a meta-pattern editorial canonical aplicada nas decisões de composição do cluster.

Cluster alinhamento/triage é candidato natural pós-Onda H:

1. **Cluster coeso pipeline `alinhamento → wiring reviewer → absorção → propagação runtime`** — 4 ADRs sob narrativa única: skill `/draft-idea` upstream produzindo IDEA.md → `design-reviewer` wired automaticamente em `/triage` plan-producing + `/new-adr` → critério mecânico de absorção de findings com 3 condições → mirror runtime das decisões absorvidas consumido por reviewers em `/run-plan`. Coesão semântica alta — todo o ecosistema do design-reviewer pré-fato + skill upstream que alimenta o pipeline.

2. **Constraint mecânico estrutural — ADR-009 preservado fora do cluster (modo (c) ADR-052)** — ADR-009 (revisor design pré-fato + free-read de doctrine sources) está hardcoded na always-include curated list de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]`. Mesmo padrão de Onda H (ADR-034 preservado por constraint análogo). **Critério mecânico verificável** per ADR-052 § Decisão (c): `grep "ADR-009" docs/decisions/ADR-048-*.md` retorna match em § Decisão de ADR Aceito vigente → modo (c) aplica diretamente. Absorvê-lo exigiria editar ADR-048 Aceito (mexer ADR-classical é antipattern) + leitura mecânica do design-reviewer cairia em ADR-009 archived com redirect em vez do consolidado. ADR-009 mantém-se como ADR clássico standalone codificando categoria foundational (revisor document-level pré-fato + free-read de doctrine).

3. **Refinamento editorial — ADR-042 excluído (modo (a) ADR-052)** — ADR-042 (`/note --to` cross-project write) pertencia ao sketch original do cluster mas tem categoria semântica distinta (skill `/note` bridge/cross-project, não design-reviewer ecosystem). **Sketch original tinha contradição interna** — charter linha 264 listava ADR-042 também em cluster "ADR-009-bridge-meta-system" (com ADR-032). Análogo a ADR-039 em Onda F (listado em 2 clusters; refinamento editorial corrigiu via exclusão). **Critério mecânico verificável** per ADR-052 § Decisão (a) bullet 1 (desalinhamento semântico): ADR-042 cita `/note`/`$PROJECTS_DIR`/`.claude/local/NOTES.md` cross-project como decisão central — zero overlap semântico com design-reviewer wiring/absorção. ADR-042 fica preservado vigente para futura Onda bridge cluster (com ADR-032).

4. **Cluster com 4 ADRs absorvidos + 2 preservados** — primeira onda com aplicação formal explícita de **2 modos editoriais canonical de ADR-052 simultaneamente** (modo (c) sobre ADR-009 + modo (a) sobre ADR-042). Calibração escopo intermediário (4 absorvidos vs 6 em G; 3 em H; 4 em D+F; 2 em C+E).

5. **F4 lessons reaplicadas literal** — cond 5 primária isolada (sucessor parcial absorvendo 4 ADRs); cond 4 NÃO aplica (ADR-045 carrega categoria meta; ADR-053 é sétima instância de migração); cond 1 NÃO aplica (ADR-045/-046/-047/-048/-049/-050/-051/-052 ancestrais codificados); cond 2 NÃO aplica — regra central de cada ADR absorvido preservada integralmente; nenhum marcado como `Substituído`.

6. **F1 lesson reaplicada literal** — link rot em 2 categorias identificado pré-execução: (a) histórica via archive blockquote redirect; (b) **doutrinal ativa hot spot** via absorção no consolidado. Hot spots concentrados em mecanismo (skills/triage + skills/new-adr + skills/run-plan + agents/code-reviewer + agents/design-reviewer + templates/plan.md) — substância absorvida em ADR-053 fecha gap; ADRs vigentes mantêm-se imutáveis (categoria histórica via redirect).

### Composição do cluster vs sketch original do charter

Charter sketch original (NOTES 2026-05-30T06:08:04Z) / ADR-045 § Decisão parte 1 § Implementação:

```
ADR-004-skill-alinhamento-triage.md   # /triage decision tree + design-reviewer
                                      # pré-fato + cutucada de descoberta +
                                      # absorção de findings + read defensivo
                                      # (absorve atual: 009, 011, 017, 026, 027, 029, 038, 042)
```

**Sketch absorvia 8 ADRs; Onda I inclui 4** (ADR-017 + ADR-029 já archived em Onda C — cutucadas standalone; ADR-009 preservado modo (c); ADR-042 excluído modo (a)):

- **(c) ADR-009 PRESERVADO fora do cluster** — análogo a ADR-034 em H. Constraint mecânico hardcoded em ADR-048 always-include. Primeira aplicação formal de ADR-052 § Decisão (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO. Critério mecânico verificável: `grep "ADR-009" docs/decisions/ADR-048-*.md` → match em § Decisão vigente.
- **(a) ADR-042 EXCLUÍDO** — desalinhamento semântico do sketch (categoria `/note` bridge, não design-reviewer ecosystem). Primeira aplicação formal de ADR-052 § Decisão (a) bullet 1 EXCLUSÃO desde codificação. ADR-042 fica preservado vigente para futura Onda bridge cluster com ADR-032.
- **(a) bullet 2 ADR-031 PRESERVADO standalone** — ADR-031 (cutucada condicional `/draft-idea` projeto maduro) é sucessor parcial direto de ADR-027 (verificável: `ADR-031 § Origem linha 8`); emergiu pós-sketch do charter (2026-05-15). Preservação por categoria semântica distinta sem constraint mecânico (modo (a) bullet 2 ADR-052 — análogo a ADR-010 em F): `/draft-idea` cutucada condicional mature-project é refinamento operacional ergonômico, não pertence à narrativa central do consolidado (alinhamento upstream + design-reviewer wiring/absorção/mirror). Sub-fluxo "presente → update seção-a-seção" de ADR-027 (preservado em ADR-053 § Decisão (a)) cobre o caso comum; cutucada condicional projeto maduro fica como refinamento ergonômico vivente standalone. Pertenceria a futuro cluster `/draft-idea` ergonomia ou permanece standalone como decisão ergonômica reversível.

**Cluster ADR-053 absorve 4 do sketch:** 011 + 026 + 027 + 038. Substância completa preservada em § Decisão (a-d).

**Saldo:** Onda I absorve 4 ADRs (vs 8 do sketch). Inventário pós-Onda I: 31 - 4 archivados + 1 ADR-053 = **28 vigentes** (drop líquido de 3 nesta onda; alinha com calibração escopo intermediário do cluster). Documentação editorial post-merge consolida em charter § "Atualização pós-execução".

**Linha do backlog:** Onda I é sub-scope da umbrella multi-onda em `## Próximos`; não corresponde a linha distinta. Per ADR-049 § Decisão (a) + precedente Ondas A-H, umbrella é atualizada in-place post-merge.

## Resumo da mudança

**Esta Onda I produz:**

1. **ADR-053 consolidado** (criado via `/new-adr` no /triage step 4) — absorve substância de ADR-011 + ADR-026 + ADR-027 + ADR-038 num único ADR temático "alinhamento upstream e ecosistema do design-reviewer". § Decisão integra:

   - (a) **Skill `/draft-idea` upstream — elicitação estruturada de `product_direction`/IDEA.md** (de ADR-027): naming `<verb>-<artifact>` alinhado a filename canonical (`IDEA.md`); escopo elicitação multi-turn (problema, persona, restrições, critérios, alternativas) — skeleton-only rejeitado; modo de operação probe canonical + dual (IDEA.md ausente → one-shot full; presente → update seção-a-seção via enum); fronteira upstream de `/triage` (skill sugere `/triage` como próximo passo); stack-agnóstica per ADR-050 § Decisão (a) caminho artefatos não-código; `disable-model-invocation: false` esperado per ADR-050 § Decisão (e). Substância de ADR-027 § Decisão preservada literal.

   - (b) **Wiring automático do design-reviewer pré-fato em `/triage` plan-producing + `/new-adr`** (de ADR-011, sucessor parcial de ADR-009): design-reviewer dispara automaticamente em (1) `/triage` que produz plano (caminho-com-plano, com ou sem ADR delegada), no passo 5 antes do commit unificado — não dispara em backlog-puro/domain-update/ADR-only-delegada; (2) `/new-adr` standalone OU delegada por `/triage`, antes de retornar controle — cobre dispatch duplo no caminho `/triage` → `/new-adr` → reviewer (passo 5 do `/triage` reconhece que `/new-adr` já cobriu o ADR; dispatch sobre o plano permanece). `/run-plan` permanece sem wiring (gate seria tarde — plano já no remote — e frequência alta multiplicaria custo de tokens). Override por inação. Dogfood empírico que produziu o gatilho (3 invocações + 7 findings cumulativos pré-ADR-011) preservado em § Origem histórica como evidência cumulativa. ADR-009 preservado vigente (modo (c) ADR-052) — citado como ancestral foundational; substância "revisor document-level pré-fato + free-read de doctrine sources" NÃO duplicada em ADR-053 (apex preserved standalone).

   - (c) **Critério mecânico de absorção de findings do design-reviewer pré-commit** (de ADR-026, sucessor parcial de ADR-011 § Decisão #1): default **invertido** — assistente absorve findings pré-commit + reporta absorção em seção dedicada `## design-reviewer findings absorvidos` do commit message. Cutucar operador via `AskUserQuestion` **somente quando** finding satisfaz ≥1 das 3 condições: (1) ≥2 alternativas legítimas competindo (alternativa rebatida descritivamente conta como 1 caminho; só ≥2 quando reviewer apresenta sem rebater); (2) contradiz decisão documentada em ADR/`philosophy.md`/`CLAUDE.md`; (3) exige contexto fora do diff/plano/ADR. Cláusula default-conservadora: dúvida → cutucada. Forma do reporte (seção dedicada com bullet `- <localização breve>: <correção aplicada> (caminho-único).`) preservada literal. Posição vs ADR-011: mecânica do wiring (quando dispara, override por inação) preservada vigente; atribuição literal "operador decide aplicar" refinada pela cláusula de absorção pré-commit. Critério é **stack-agnóstico** — opera sobre shape do finding, não conteúdo ou stack.

   - (d) **Mirror runtime das Decisões absorvidas: plan body + consumo por reviewers via `/run-plan` §2.3** (de ADR-038, sucessor parcial de ADR-026): seção `## design-reviewer findings absorvidos` do commit message (preservada por (c) acima) tem espelho idêntico no body do plano sob `## Decisões absorvidas` (após `## Notas operacionais` quando existe; último bloco antes do EOF caso contrário); mesmo formato de bullets. `/triage` step 5 escreve em ambos os locais (mesma sequência atômica antes do commit). Consumo runtime por `/run-plan` §2.3 (reader): antes de cada reviewer invocado por bloco, conteúdo passado como contexto adicional na prompt — uniform protocol cross-reviewer (code/doc/qa/security). `code-reviewer` cláusula consumer: trata estruturas listadas como out-of-scope da rubrica YAGNI; categoria nova "context-aware via messenger upstream" (distinta da rejeitada "free-read autônomo de ADRs" per ADR-043 § Ockham operacionalizado em decisões internas do plugin — ex-ADR-035 Substituído). Backward-compat: planos antigos sem a seção continuam executáveis (reader skip silente).

   § Origem histórica preserva 4 incidentes empíricos: (1) `/triage` do `design-reviewer` (sessão pós-v1.24.0) levantou divergência do padrão diff pós-fato + insumo curado → ADR-009 (preservado standalone, vigente); (2) dogfood deliberado de design-reviewer pós-ADR-009 acumulando 3 invocações + 7 findings → ADR-011; (3) prática empírica em 11 sessões pós-ADR-011 divergindo do default literal "sempre cutucar" + feedback explícito do operador → ADR-026 (~17 findings absorvidos retroativamente, zero retrabalho); (4) ROADMAP item 1 sessão 2026-05-26 evidenciou regressão silenciosa do `code-reviewer` flaggando estrutura aprovada pelo `design-reviewer` pré-commit → ADR-038 (causa raiz: code-reviewer sem acesso ao registro das decisões absorvidas; mecanismo runtime via mensageiro upstream fecha gap). § Gatilhos consolida triggers das 4 decisões. § Auto-aplicação cond 5 primária isolada per F4 Ondas C-H.

   **Substância preservada para link rot doutrinal ativa categoria-b** — gap fechado quando docs vivos citam membros do cluster archived:
   - `CLAUDE.md` linha 44 (table row agents) + linha 88 (bullet meta-doutrinal) citam ADR-011 como autoridade do wiring → ADR-053 § Decisão (b) preserva mecanismo wiring literal.
   - `README.md` linha 26 (descrição do `design-reviewer`) cita "Auto-dispatched in `/triage` ... per ADR-011" → ADR-053 § Decisão (b) preserva.
   - `agents/design-reviewer.md` linha 3 (description frontmatter) cita "per ADR-011" → ADR-053 § Decisão (b) preserva.
   - `agents/code-reviewer.md` linha 62 cita ADR-038 (mecanismo prescrito) + linha 64 cita ADR-026 (operador absorveu via) → ADR-053 § Decisão (c)+(d) preservam.
   - `skills/triage/SKILL.md` linha 160 cita ADR-011 (conforme) + ADR-026 (critério); linha 169 cita ADR-026 (absorvido pré-commit); linha 171 cita ADR-038 (mirror) → ADR-053 § Decisão (b)+(c)+(d) preservam.
   - `skills/new-adr/SKILL.md` linha 48 cita ADR-011 (conforme) + ADR-026 (critério); linha 103 cita ADR-011 (audita drift) → ADR-053 § Decisão (b)+(c) preservam.
   - `skills/run-plan/SKILL.md` linha 118 cita ADR-038 (uniform protocol context-passing) → ADR-053 § Decisão (d) preserva.
   - `skills/draft-idea/SKILL.md` linha 131 cita ADR-027 § Consequências (limitação cross-seção) → ADR-053 § Decisão (a) preserva.
   - `templates/plan.md` linha 61 cita "per ADR-026 § Forma estendida por ADR-038" → ADR-053 § Decisão (c)+(d) preservam.
   - `templates/IDEA.md` linha 4 cita "consumido por /draft-idea (ADR-027)" → ADR-053 § Decisão (a) preserva.
   - ADR-009 vigente preserved standalone (apex foundational) — categoria-b NÃO aplica (revogação foundational seria modo (a) ADR-052 errado para constraint mecânico explícito).
   - ADR-042 vigente preserved standalone (cluster bridge futuro) — categoria-b NÃO aplica (excluído do cluster modo (a) ADR-052).
   - Múltiplos ADRs vigentes (-020, -034, -035, -036, -043, -045, -048, -049, -051) citam ADR-011/-026 como precedente — categoria histórica preserved via redirect canonical.
   - Múltiplos ADRs vigentes (-031, -033, -037, -046, -050) citam ADR-027 como precedente — categoria histórica preserved via redirect canonical.
   - ADR-047 + ADR-048 citam ADR-038 como precedente — categoria histórica preserved via redirect canonical.

2. **Archive de ADR-011, ADR-026, ADR-027, ADR-038** — `git mv` para `docs/decisions/archive/` + header redirect canonical (format de ADR-046): blockquote `> **ARCHIVED 2026-05-31** — content absorbed into [ADR-053](../ADR-053-<slug>.md); see that ADR for current authority. Body below preserved verbatim for historical record.` + header H1 original preservado intacto abaixo.

3. **Archive index update** — `docs/decisions/archive/README.md` ganha 4 linhas novas na tabela (Onda I). Cada onda C-X estende a tabela como invariante codificada em ADR-046.

4. **Propagação de cross-refs em docs vivos** (10 arquivos; 14 ocorrências em 14 linhas distintas):
   - `CLAUDE.md` linha 44 → ADR-053 § Decisão (b).
   - `CLAUDE.md` linha 88 → ADR-053 § Decisão (b) (bullet meta-doutrinal).
   - `README.md` linha 26 → ADR-053 § Decisão (b) (descrição do `design-reviewer`).
   - `agents/design-reviewer.md` linha 3 → ADR-053 § Decisão (b) (description frontmatter).
   - `agents/code-reviewer.md` linha 62 → ADR-053 § Decisão (d) (mecanismo prescrito).
   - `agents/code-reviewer.md` linha 64 → ADR-053 § Decisão (c) (operador absorveu via).
   - `skills/triage/SKILL.md` linha 160 → ADR-053 § Decisão (b)+(c) (conforme + critério).
   - `skills/triage/SKILL.md` linha 169 → ADR-053 § Decisão (c) (absorvido pré-commit).
   - `skills/triage/SKILL.md` linha 171 → ADR-053 § Decisão (d) (mirror per).
   - `skills/new-adr/SKILL.md` linha 48 → ADR-053 § Decisão (b)+(c) (conforme + critério).
   - `skills/new-adr/SKILL.md` linha 103 → ADR-053 § Decisão (b) (audita drift).
   - `skills/run-plan/SKILL.md` linha 118 → ADR-053 § Decisão (d) (uniform protocol).
   - `skills/draft-idea/SKILL.md` linha 131 → ADR-053 § Decisão (a) (limitação cross-seção).
   - `templates/plan.md` linha 61 → ADR-053 § Decisão (c)+(d) (per ADR-026 estendida por ADR-038).
   - `templates/IDEA.md` linha 4 → ADR-053 § Decisão (a) (consumido por /draft-idea).

5. **Link rot consciente em docs imutáveis** — outros ADRs imutáveis e planos históricos citam ADR-011/-026/-027/-038 em § Origem como precedente ou cross-ref doutrinal (categoria (a) histórica de F1 lesson Onda C). Subset suspeito de categoria (b) doutrinal ativa já identificado pré-execução (todos com substância absorvida em ADR-053; link via archive resolve):
   - ADRs vigentes (-020, -034, -035, -036, -043, -045, -048, -049, -051) citam ADR-011 como precedente — categoria histórica preserved.
   - ADRs vigentes (-034, -035, -043, -045, -048, -051) citam ADR-026 como precedente — categoria histórica preserved.
   - ADRs vigentes (-031, -033, -037, -046, -050) citam ADR-027 como precedente — categoria histórica preserved.
   - ADRs vigentes (-047, -048) citam ADR-038 como precedente — categoria histórica preserved.
   Hipótese de zero substância "doutrinal ativa" perdida — design-reviewer valida.

6. **Charter atualização** (post-merge, manual) — `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução" tabela adiciona linha "Onda I — Migração cluster alinhamento/triage" + **primeira aplicação formal de ADR-052 § Decisão (c) [modo c sobre ADR-009] e § Decisão (a) [modo a sobre ADR-042]** documentadas; anti-regression checklist § Skills e fluxo + § Reviewers atualizadas refletindo ADR-053 como nova autoridade do wiring/absorção/mirror + ADR-027 como autoridade do `/draft-idea`. NÃO escopo desta Onda I; commit separado post-merge per precedente Ondas A-H.

**Pattern de migração validado nesta onda** (sétima aplicação; **primeira aplicação formal de ADR-052 com 2 modos simultâneos**):
- Cluster de 4 ADRs absorvidos + 2 preservados — calibração escopo intermediário entre Ondas G (6) e D+F (4); H (3) e C+E (2).
- **Primeira aplicação formal explícita de ADR-052 § Decisão (a) e (c) simultaneamente** — modo (c) sobre ADR-009 (constraint mecânico hardcoded ADR-048 always-include; análogo a ADR-034 em H) + modo (a) sobre ADR-042 (desalinhamento semântico do sketch; análogo a ADR-039 em F). Referência formal ao meta-pattern editorial canonical preservada em § Origem do consolidado e charter pós-merge.
- Hot spot em **6 docs vivos de mecanismo** (CLAUDE.md + skills/triage + skills/new-adr + skills/run-plan + agents/design-reviewer + agents/code-reviewer = 11 das 14 ocorrências). Spread em 10 docs vivos (vs 9 em H; 7 em G; 5 em F; 6 em E).
- F4 lessons reaplicadas literal (cond 5 isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica — regra central preservada).
- F1 lesson reaplicada literal (link rot 2 categorias; categoria-b doutrinal ativa identificada pré-execução; substância absorvida em ADR-053).
- **Invariante operacional 8 ondas consecutivas** com reviewer-per-bloco estrito (C+D+E+F+G+H + ADR-052 plano + Onda I): 3 blocos planejados, todos com `{reviewer: doc}`.

## Arquivos a alterar

### Bloco 1 — Archive 4 ADRs + archive index extension {reviewer: doc}

**Instrução para data dinâmica:** substituir `2026-05-31` no template do blockquote pela data de execução (formato `YYYY-MM-DD` do dia de aplicação) ao replicar em cada um dos 4 arquivos arquivados — pattern Ondas C+D+E+F+G+H.

- `git mv docs/decisions/ADR-011-wiring-design-reviewer-automatico.md docs/decisions/archive/`
- Editar topo do arquivo movido inserindo blockquote redirect **antes** do `# ADR-011: <título original>`:

  ```markdown
  > **ARCHIVED 2026-05-31** — content absorbed into [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

  # ADR-011: Wiring automático do design-reviewer no /triage e /new-adr
  ```

- `git mv docs/decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-027-skill-draft-idea-elicitacao-product-direction.md docs/decisions/archive/` + análogo.
- `git mv docs/decisions/ADR-038-mirror-decisoes-absorvidas-runtime.md docs/decisions/archive/` + análogo.
- Estender tabela em `docs/decisions/archive/README.md` adicionando 4 linhas (Onda I):

  ```markdown
  | ADR-011 — Wiring automático do design-reviewer no /triage e /new-adr | [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) | I |
  | ADR-026 — Critério mecânico de absorção de findings do design-reviewer pré-commit | [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) | I |
  | ADR-027 — Skill /draft-idea para elicitação estruturada de product_direction | [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) | I |
  | ADR-038 — Mirror de Decisões absorvidas no plan body + consumo runtime por reviewers | [ADR-053](../ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) | I |
  ```

**Nota:** slug exato do ADR-053 é determinado por `/new-adr` no /triage step 4; substituir `alinhamento-triage-ecosistema-design-reviewer-consolidado` pelo slug efetivo após criação do ADR.

### Bloco 2 — Hot spot mecanismo: skills + agents cross-refs (10 ocorrências em 6 docs) {reviewer: doc}

- `skills/triage/SKILL.md` linha 160 (parágrafo "Revisão pré-commit caminho-com-plano"): substituir 2 cross-refs na mesma linha — "conforme [ADR-011](...)" → "conforme [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b)"; "critério de [ADR-026](...)" → "critério de [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c)".
- `skills/triage/SKILL.md` linha 169 (parágrafo "Forma do commit message"): substituir "absorvido pré-commit (ADR-026)" por "absorvido pré-commit ([ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c))".
- `skills/triage/SKILL.md` linha 171 (parágrafo "Mirror no plan body"): substituir "per [ADR-038](...)" por "per [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (d)".
- `skills/new-adr/SKILL.md` linha 48 (passo 5 "Revisão pré-retorno"): substituir 2 cross-refs na mesma linha — "conforme [ADR-011](...)" → "conforme [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b)"; "critério de [ADR-026](...)" → "critério de [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c)".
- `skills/new-adr/SKILL.md` linha 103 (bullet "Não inventar conteúdo"): substituir "`design-reviewer` (per [ADR-011](...))" por "`design-reviewer` (per [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b))".
- `skills/run-plan/SKILL.md` linha 118 (parágrafo "Decisões absorvidas repassadas ao reviewer"): substituir "([ADR-038](...))" por "([ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (d))".
- `skills/draft-idea/SKILL.md` linha 131 (bullet limitação cross-seção): substituir "registrada em [ADR-027](...) § Consequências" por "registrada em [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (a) Limitações".
- `agents/design-reviewer.md` linha 3 (description frontmatter): substituir "per ADR-011" por "per ADR-053 § Decisão (b)".
- `agents/code-reviewer.md` linha 62 (parágrafo "Aplicabilidade"): substituir "mecanismo prescrito em [ADR-038](../docs/decisions/ADR-038-...)" por "mecanismo prescrito em [ADR-053](../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (d)".
- `agents/code-reviewer.md` linha 64 (parágrafo subsequente): substituir 3 cross-refs na mesma linha — "operador absorveu via [ADR-026](...)" por "operador absorveu via [ADR-053](../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c)"; "viola 'override por inação' de [ADR-035](...)" por "viola 'override por inação' de [ADR-043](../docs/decisions/ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § Ockham operacionalizado em decisões internas do plugin (ex-ADR-035 Substituído por ADR-043 em 2026-05-29)" — alinha com correção F1 já aplicada em ADR-053 (evita drift Frankenstein por omissão); "refinado por ADR-038 (categoria nova ..." por "refinado por ADR-053 § Decisão (d) (categoria nova ...".

### Bloco 3 — Foundation + templates cross-refs (4 ocorrências em 4 docs; mistura categorial intencional) {reviewer: doc}

**Nota editorial:** Bloco 3 unifica README.md (apex sensitivity — discoverability per ADR-051 § Decisão (b)) + CLAUDE.md + templates internal (low sensitivity). Doc-reviewer audita ambas com mesma lente — justificado pela baixa cardinalidade (4 ocorrências total; splittar em 3a/3b adicionaria overhead operacional desproporcional). README user-facing recebe substituição preserve substância integralmente.


- `CLAUDE.md` linha 44 (table row agents shipped by the plugin): substituir "per [ADR-011](docs/decisions/ADR-011-wiring-design-reviewer-automatico.md)" por "per [ADR-053](docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b)". Substância (auto-dispatched in `/triage` plan-producing + `/new-adr`) preservada literal.
- `CLAUDE.md` linha 88 (bullet meta-doutrinal "Wiring automático do design-reviewer"): substituir "ver [ADR-011](...)" por "ver [ADR-053](docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b)". Substância (quando dispara em /triage e /new-adr, override por inação, custo de tokens) preservada literal.
- `README.md` linha 26 (descrição do `design-reviewer` na tabela components): substituir "per ADR-011" por "per [ADR-053](docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b)". Substância (Auto-dispatched in `/triage` plan-producing + `/new-adr`) preservada literal. Hot spot user-facing per ADR-051 § Decisão (b) discoverability — substituição preserva substância integralmente.
- `templates/plan.md` linha 61 (comentário HTML da seção Decisões absorvidas): substituir "per ADR-026 § Forma estendida por ADR-038" por "per ADR-053 § Decisão (c) + (d)". Substância (mirror do bloco do commit message; bullet format idêntico; consumido por /run-plan §2.3) preservada literal.
- `templates/IDEA.md` linha 4 (comentário HTML do esqueleto): substituir "consumido por /draft-idea (ADR-027)" por "consumido por /draft-idea (ADR-053 § Decisão (a))".

## Verificação end-to-end

**Critérios de sucesso da Onda I:**

1. **ADR-053 criado** com Status `Proposto` em `docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md` (ou slug equivalente decidido por `/new-adr`). § Origem cita ADR-011+ADR-026+ADR-027+ADR-038 como decisões absorvidas + ADR-045/-046/-047/-048/-049/-050/-051 como templates + **ADR-052 como meta-pattern editorial canonical com primeira aplicação formal** (modo (c) sobre ADR-009 + modo (a) sobre ADR-042) + ADR-009 explicitamente preservado fora do cluster por constraint always-include de ADR-048 + ADR-042 explicitamente excluído por desalinhamento semântico do sketch + ADRs vigentes preservados citando substância (ADRs -020, -031, -033, -034, -035, -036, -037, -043, -045, -046, -047, -048, -049, -050, -051). § Decisão integra as 4 dimensões (a-d) sob narrativa única coerente. § Origem histórica preserva os 4 incidentes empíricos. § Gatilhos consolida triggers das 4 decisões. § Auto-aplicação cond 5 primária isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica (regra central preservada).

2. **ADR-011, ADR-026, ADR-027, ADR-038 arquivados:** `ls docs/decisions/ADR-011-*.md docs/decisions/ADR-026-*.md docs/decisions/ADR-027-*.md docs/decisions/ADR-038-*.md` → vazio (movidos). `ls docs/decisions/archive/ADR-011-*.md docs/decisions/archive/ADR-026-*.md docs/decisions/archive/ADR-027-*.md docs/decisions/archive/ADR-038-*.md` → 4 arquivos presentes. Header redirect canonical no topo, H1 original intacto abaixo.

3. **ADR-009 preservado vigente (modo (c) ADR-052):** `ls docs/decisions/ADR-009-*.md` → 1 arquivo presente (NÃO arquivado). ADR-009 mantém-se como ADR clássico standalone codificando categoria foundational (revisor document-level pré-fato + free-read de doctrine sources). Always-include de ADR-048 § Decisão `[ADR-009, ADR-034, ADR-043]` permanece intacta (constraint mecânico preserved). `grep "ADR-009" docs/decisions/ADR-048-*.md` → match em § Decisão (always-include curated list).

4. **ADR-042 preservado vigente (modo (a) ADR-052):** `ls docs/decisions/ADR-042-*.md` → 1 arquivo presente (NÃO arquivado). ADR-042 mantém-se como ADR clássico standalone codificando `/note --to` cross-project write — fica disponível para futura Onda bridge cluster com ADR-032 (categoria semântica distinta de design-reviewer ecosystem).

5. **Archive index estendido:** `docs/decisions/archive/README.md` carrega tabela com 25 linhas (2C + 4D + 2E + 4F + 6G + 3H + 4I), ordem cronológica por onda preservada.

6. **`grep "ADR-011\|ADR-026\|ADR-027\|ADR-038" CLAUDE.md README.md` → 0 matches** (3 ocorrências substituídas; 2 em CLAUDE.md + 1 em README.md).

7. **`grep "ADR-011\|ADR-026\|ADR-027\|ADR-038" skills/*/SKILL.md` → 0 matches** (8 ocorrências substituídas; 4 em skills/triage + 2 em skills/new-adr + 1 em skills/run-plan + 1 em skills/draft-idea).

8. **`grep "ADR-011\|ADR-026\|ADR-038" agents/*.md` → 0 matches** (3 ocorrências substituídas; 1 em design-reviewer + 2 em code-reviewer; ADR-027 não aparece em agents).

9. **`grep "ADR-026\|ADR-027\|ADR-038" templates/*.md` → 0 matches** (2 ocorrências substituídas; 1 em plan.md cobrindo ADR-026+ADR-038 + 1 em IDEA.md cobrindo ADR-027; ADR-011 não aparece em templates).

10. **Substância preservada para link rot doutrinal ativa categoria-b:**
   - `grep -c "design-reviewer.*dispara\|automaticamente.*design-reviewer\|wiring.*design-reviewer" docs/decisions/ADR-053-*.md` → ≥1 match (substância ADR-011 wiring absorvida).
   - `grep -c "3 condições\|alternativas legítimas competindo\|caminho-único" docs/decisions/ADR-053-*.md` → ≥2 matches (substância ADR-026 critério absorvida).
   - `grep -c "skeleton-only\|probe canonical + dual\|one-shot full\|update seção-a-seção" docs/decisions/ADR-053-*.md` → ≥3 matches (substância ADR-027 § Decisão central absorvida — modo dual + skeleton-only rejection + sub-modos).
   - `grep -c "mirror\|Decisões absorvidas\|context-aware via messenger" docs/decisions/ADR-053-*.md` → ≥2 matches (substância ADR-038 mirror runtime absorvida).

11. **ADRs vigentes preservados (não arquivados; cross-refs históricas):** `grep -l "ADR-011\|ADR-026\|ADR-027\|ADR-038" docs/decisions/ADR-0*.md | wc -l` → ~20 ADRs vigentes com cross-ref histórica a algum dos 4 ADRs absorvidos (mantêm cross-refs como autoridade histórica via redirect canonical; immutável, NÃO editados). Comando é single source of truth — listas hardcoded em § Resumo § Pattern + § Substância preservada são informativas, podem estar incompletas.

12. **Tabela "Components" do README intacta exceto cross-ref ADR-011:** `grep -c 'design-reviewer.*Agent.*Pre-fact' README.md` → 1 match (linha preservada; apenas link atualizado para ADR-053).

13. **CLAUDE.md bullet "Wiring automático do design-reviewer" preserva substância + ganha link novo:** `grep -c "Wiring automático do design-reviewer.*ADR-053" CLAUDE.md` → 1 (substância preservada + cross-ref atualizado para consolidado).

14. **Link rot em immutable ADRs aceito explicitamente:** `grep -l "ADR-011\|ADR-026\|ADR-027\|ADR-038" docs/decisions/ADR-0*.md docs/plans/*.md` ainda retornará vários arquivos antigos — esses são imutáveis (immutable ADRs + historical plans); cross-refs em immutable docs ficam como registro histórico, NÃO são editados.

15. **CHANGELOG.md intacto** (registro histórico imutável) — `grep "ADR-011\|ADR-026\|ADR-027\|ADR-038" CHANGELOG.md` retorna matches preservados como registro de versionamento; NÃO editar.

16. **doc-reviewer audita drift cross-doc:** cross-refs corretos cross-doc; ADR-053 substância fiel a ADR-011+ADR-026+ADR-027+ADR-038 combinados; nenhuma carga doutrinal da § Skills e fluxo + § Reviewers do anti-regression checklist perdida (wiring automático + critério de absorção 3 condições + mirror runtime + skill `/draft-idea` upstream — todas preservadas em ADR-053). Verificar especialmente fidelidade das 3 condições disjuntivas + cláusula default-conservadora + uniform protocol cross-reviewer — substância load-bearing per ADR-026 § Decisão + ADR-038 § Decisão.

17. **design-reviewer auto-fire em /new-adr step 5 e /triage step 5** valida: padrão de migração coerente com ADR-045 § Decisão parte 1; **primeira aplicação formal de ADR-052 § Decisão (c) e (a) simultaneamente** com critério mecânico verificável (modo (c) ADR-009 hardcoded em ADR-048 § Decisão; modo (a) ADR-042 desalinhamento semântico do sketch); pattern reusable em cluster com hot spot mecânico em skills+agents; auto-aplicação per ADR-034 (cond 5 primária; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica — regra central preservada) coerente.

## Notas operacionais

**DEPENDÊNCIA CRÍTICA — Onda Promoção PRÉ-Onda I (F10 cutucado, escolha (b) do operador):** Esta Onda I aplica modo (c) ADR-052 sobre ADR-009 com base em hardcode em ADR-048 § Decisão (always-include `[ADR-009, ADR-034, ADR-043]`). ADR-052 § Decisão (c) literal exige "grep ID em § Decisão de ADRs **Aceito** vigentes". TODOS os 7 consolidados (ADR-046+047+048+049+050+051+052) estão Proposto-shipped — effective em produção, referenciados por CLAUDE.md/skills/agents como autoridade, mas formalmente Proposto. Critério literal não estritamente satisfeito.

**Onda Promoção dedicada (não-Onda-I, plano separado) precede Onda I:** operador escolheu via F10 cutucada Opção (b) "Promover consolidados a Aceito em batch". Onda Promoção toca os 7 ADRs vigentes (Proposto → Aceito), com critério de promoção uniforme (shipped + effective + referenciado como autoridade + sem `Substituído` marker + tempo mínimo desde Proposto). Após Onda Promoção merging, esta Onda I retoma com critério mecânico de ADR-052 § Decisão (c) **estritamente satisfeito**.

**Trabalho de Onda I preservado como draft em branch dedicado** (`onda-i-draft-pending-promotion`) sem push até Onda Promoção concluir. Re-validação pós-merge: F4/F6/F9 já decididas; F10 resolve automaticamente (ADR-048 vira Aceito); plano + ADR-053 prontos para promoção a main.

**Ordem dos blocos:** Bloco 1 (archive) executado antes dos demais — outros blocos referenciam ADR-053 que substitui os 4 arquivos arquivados. Blocos 2-3 podem rodar em qualquer ordem (independentes entre si após archive); Bloco 2 (skills/agents) tem hot spot mecânico (skills/triage 3 ocorrências; skills/new-adr 2 ocorrências) — concentração maior justifica revisão antes do Bloco 3 (foundation + templates).

**Aderir reviewer-per-bloco estrito (lição operacional Onda F endereçada em Ondas G+H+ADR-052 plano):** Bloco 1 (archive) DEVE invocar `doc-reviewer` obrigatório — invariante de 8 instâncias consecutivas (C+D+E+F+G+H + ADR-052 plano + Onda I) sem exceção à doutrina explícita "Não pular revisor, mesmo em bloco trivial". Onda I mantém pattern.

**Validação da preservação de ADR-009 + exclusão de ADR-042:** se design-reviewer flagrar gap na preservação de ADR-009 (ex.: substância "revisor document-level pré-fato + free-read de doctrine sources" não-canonical preserved separadamente; constraint always-include não-justificado) OU na exclusão de ADR-042 (ex.: critério modo (a) ADR-052 não aplicável; cluster bridge não existir como categoria futura), preservação/exclusão é editorial do plano antes de prosseguir. **Esta é a primeira aplicação formal de ADR-052 com 2 modos simultâneos** — design-reviewer deve validar coerência metalinguística (modo c se aplica apenas quando hardcode em § Decisão de ADR Aceito vigente; modo a se aplica quando desalinhamento semântico do sketch ou ancestralidade codificada com categoria distinta sem constraint mecânico).

**Charter atualização post-merge:** após merge da Onda I, atualizar `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução":
- Estender tabela de ondas com linha "Onda I — Migração cluster alinhamento/triage" (commit hash + PR + substância + **primeira aplicação formal de ADR-052 § Decisão (c) e (a) simultaneamente documentada**).
- Anti-regression checklist § Skills e fluxo + § Reviewers — atualizar referências a "ADR-011/-026/-027/-038" para "ADR-053 § Decisão (a/b/c/d)" + nota explícita sobre ADR-009 preservado vigente como ADR clássico standalone codificando categoria foundational + ADR-042 preservado vigente para futura Onda bridge cluster.
- § Refinamento editorial documentado: estender com **primeira aplicação formal de ADR-052** (modo (c) sobre ADR-009 + modo (a) sobre ADR-042 simultaneamente). Sinal explícito de que meta-pattern editorial canonical funciona em escala — não mais apenas categorias editoriais ad hoc das Ondas F+G+H.
- Saldo inventário pós-Onda I: estimado **28 vigentes** (31 pós-ADR-052 + 1 ADR-053 - 4 arquivados); drop líquido de 3 (paralelo a Onda D+F; alinha com calibração escopo intermediário).
- Anotação progressiva: "Onda I shipped — commit <hash>; cluster alinhamento/triage migrado com primeira aplicação formal de ADR-052 (modo (c) ADR-009 + modo (a) ADR-042 simultâneo)".

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A-H); NÃO escopo desta Onda I.

**Decisão excluída — ADR-009 NÃO absorvido apesar de pertencer ao sketch original do cluster:** constraint mecânico (hardcoded na always-include de ADR-048 § Decisão) + categoria semântica distinta (foundational do design-reviewer document-level vs ecosistema operacional wired sobre ADR-009) justificam preservação fora do cluster. **Primeira aplicação formal de ADR-052 § Decisão (c) PRESERVAÇÃO POR CONSTRAINT MECÂNICO PURO** — critério mecânico verificável via `grep "ADR-009" docs/decisions/ADR-048-*.md`. ADR-009 pertenceria a futuro cluster apex meta-doutrinal hipotético (charter linha 182), não a ecosistema do design-reviewer. ADR-053 § Origem reconhece ADR-009 como ancestral foundational vigente preservado (cross-ref preservada como autoridade).

**Decisão excluída — ADR-042 NÃO absorvido apesar de pertencer ao sketch original do cluster:** desalinhamento semântico do sketch (`/note --to` cross-project write é categoria `/note` bridge, não design-reviewer ecosystem) + sketch original tinha contradição interna (ADR-042 listado em 2 clusters distintos — alinhamento + bridge-meta-system) justificam exclusão. **Primeira aplicação formal de ADR-052 § Decisão (a) EXCLUSÃO bullet 1** (desalinhamento semântico do sketch). ADR-042 pertence ao futuro cluster bridge/discoverability junto com ADR-032 (foundational `/note`). ADR-053 § Origem reconhece ADR-042 como decisão preservada vigente para futura onda (cross-ref preservada como categoria distinta).

**Sinal a observar para ondas J-X — primeira aplicação formal de ADR-052 calibração:** Onda I aplica 2 modos simultaneamente (c + a). Sinal a observar pós-merge:
- Se design-reviewer absorve referências ADR-052 sem cutucada (caminho-único), pattern é estável — Ondas J-X aplicam modos diretamente.
- Se cutucada emergir (ex.: critério mecânico não-óbvio, sub-modos colidindo, novo modo emergente), registrar no charter pós-merge e considerar refinamento de ADR-052.
- Operador decide em sessão futura — não bloqueia Ondas J-X enquanto pattern editorial cabe nos 3 modos canonical atuais.

**Cap de ondas estimado:** charter previa 6-10 ondas. Pós-Onda I (nona), trajetória esperada: I + 2-3 ondas J-X adicionais. Cluster sequence revisitada — candidatos remanescentes após Onda I:
- **bridge cluster** (ADR-032 + ADR-042 preservado) — natural sucessor de Onda I (ADR-042 já preservado standalone aguardando).
- **discoverability/branding** (ADR-037 + ?) — coleta órfãos editoriais.
- **brainstorm** (ADR-036 standalone) — micro-cluster ou preservação clássico.
- **apex meta-cluster** (ADR-009 + ADR-034 + ADR-035 + ADR-043 + ADR-045 + ADR-046 + ADR-047 + ADR-048 + ADR-049 + ADR-050 + ADR-051 + ADR-052 + ADR-053) — meta-consolidação dos próprios apex. Risco alto de auto-referência. Provavelmente skip — apex vive como camada vigente sem necessidade de consolidação adicional.

**Sinal de saúde:** se Bloco 2 (skills+agents) gerar ≥10 findings de doc-reviewer, sinal de que cross-refs em skills/agents precisam refinamento antes de aplicar a clusters com hot spot mecânico maior em ondas futuras. Pausar e iterar conforme charter linha 154.

## Decisões absorvidas

Findings absorvidos pré-commit pelos 2 design-reviewers (sobre ADR-053 + sobre este plano) per ADR-053 § Decisão (c) critério mecânico (caminho-único). Findings cutucados via `AskUserQuestion` (F4 extender Bloco 2 / F6 manter unificado nomeando / F9 modo (a) bullet 2 / F10 Onda Promoção precede) ficam em trace narrativo do commit message, NÃO nesta seção, per ADR-053 § Decisão (c) cláusula.

- ADR-053 § Decisão (d) #4+#5, § Origem histórica item 5, § Trade-offs: 4 ocorrências de "ADR-035" substituídas por "ADR-043 § Ockham operacionalizado em decisões internas do plugin" com anotação histórica "ex-ADR-035 Substituído em 2026-05-29" preservando narrativa do incidente (caminho-único).
- ADR-053 § Auto-aplicação Cond 4: adicionado paralelo borderline com ADR-052 § Auto-aplicação reconhecendo estreia editorial (combinação inédita modos a+c simultâneos) NÃO equivale a categoria conceitual nova de artefato (caminho-único).
- ADR-053 § Limitações global: adicionado bullet "Critério (c) não substitui revisão editorial humana de qualidade do reviewer" preservando substância de ADR-026 § Limitações ii (caminho-único).
- ADR-053 § Decisão (a): removida sub-section `#### Limitações` local (duplicação com § Limitações global); 2 limitações consolidadas em § Limitações global paralelo a (b)/(c)/(d) e às 6 consolidações precedentes (caminho-único).
- ADR-053 § Alternativas (c): adicionado parágrafo de trade-off honesto sobre carga doutrinária autônoma de ADR-042 (/note --to semantics + $PROJECTS_DIR discovery + target inicializado pré-condição) (caminho-único).
- Plano § Resumo da mudança bloco (d): substituída referência incorreta a "ADR-050 § Decisão (a) caminho stack-agnóstico + ADR-035 escopo" por "ADR-043 § Ockham operacionalizado em decisões internas do plugin (ex-ADR-035 Substituído)" alinhando com correção F1 (caminho-único).
- Plano § Verificação end-to-end critério 12: substituída sintaxe shell quebrada (`grep -cE "^\| \`design-reviewer\` \|"` com backticks dentro de duplo-quote disparando command substitution) por grep válido (`grep -c 'design-reviewer.*Agent.*Pre-fact' README.md`) — critério agora executável (caminho-único).
- Plano § Verificação end-to-end critério 11: substituída lista hardcoded de 18 ADRs vigentes por grep auditável (`grep -l "ADR-011\|ADR-026\|ADR-027\|ADR-038" docs/decisions/ADR-0*.md | wc -l` → ~20) — single source of truth; listas em § Resumo viraram informativas (caminho-único).
- Plano § Verificação end-to-end critério 13: substituída verificação trivial (`grep -c "^- \*\*" CLAUDE.md` retornando contagem que a operação não pode mudar) por grep substantivo (`grep -c "Wiring automático do design-reviewer.*ADR-053"`) verificando substância + link novo (caminho-único).
- Plano § Verificação end-to-end critério 10 substância ADR-027: substituído grep fraco (`grep "draft-idea\|elicitação\|IDEA.md"` com alta probabilidade de falso positivo) por grep discriminante de § Decisão central (skeleton-only + probe canonical + dual + one-shot full + update seção-a-seção) — verifica substância presente, não keyword genérico (caminho-único).
