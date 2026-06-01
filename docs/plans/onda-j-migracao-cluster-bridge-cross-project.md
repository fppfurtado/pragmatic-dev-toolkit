# Plano — Onda J da redesign da camada doutrinal (migração cluster bridge cross-project)

## Contexto

**ADRs candidatos:** ADR-032 (skill `/note` foundational — append timestampado em `.claude/local/NOTES.md` store doutrinário non-role; cross-project read como fenômeno conversacional), ADR-042 (flag `--to` em `/note` para cross-project write; sucessor parcial de ADR-032 estendendo cross-write via `$PROJECTS_DIR` discovery + pré-condição target inicializado + blast-radius preserved; **já preservado standalone aguardando Onda J desde Onda I per modo (a) bullet 1 de ADR-052**), ADR-045 (apex redesign — esta onda materializa § Decisão parte 1 § Implementação literal), ADR-046+047+048+049+050+051+053 (templates de migração validados em 7 ondas precedentes — C+D+E+F+G+H+I), ADR-052 (meta-pattern editorial canonical — Onda J segue pattern padrão sem aplicação formal de modos a/b/c — todos 2 ADRs absorvidos cleanly), ADR-034 (critério adendo vs novo ADR — cond 5 primária isolada; cond 4 NÃO aplica per 7 ondas precedentes; cond 1 NÃO aplica — ancestrais codificados; cond 2 NÃO aplica — regra central preservada).

Onda J (décima) da redesign da camada doutrinal coordenada por `docs/plans/redesign-camada-doutrinal-charter.md`. **Oitava migração cluster temático** per ADR-045 § Decisão parte 1 § Implementação literal — Ondas C+D+E+F+G+H+I precederam (cutucadas, modo local, reviewers/curadoria, execução/run-plan, componentes plugin, convenções editoriais, alinhamento/triage).

Cluster bridge cross-project é candidato natural pós-Onda I:

1. **ADR-042 preservado standalone aguardando** — Onda I (alinhamento/triage) aplicou modo (a) bullet 1 de ADR-052 sobre ADR-042 (desalinhamento semântico do sketch: `/note` cross-project é categoria bridge, não design-reviewer ecosystem). ADR-042 ficou explicitamente preservado para Onda J (charter linha "candidatos remanescentes naturais: **bridge cluster** (ADR-032 + ADR-042 preservado — natural sucessor de Onda I; ADR-042 standalone aguardando)"). Onda J fecha a pendência editorial.

2. **Cluster coeso pipeline `/note intra-project foundational + cross-project write`** — 2 ADRs sob narrativa única: skill `/note` foundational (append em store doutrinário non-role) + extensão cross-project via flag `--to` (discovery via `$PROJECTS_DIR` + pré-condição target inicializado + blast-radius preserved). Coesão semântica alta — ADR-042 § Origem explicitamente cita ADR-032 como decisão base ("sucessor parcial estendendo § Decisão e § Limitações de ADR-032 para cobrir cross-project write").

3. **Cluster pequeno + sem ADRs preservados fora** — 2 ADRs absorvidos cleanly; nenhuma aplicação formal de ADR-052 modos a/b/c necessária. Calibração mínima vs Ondas precedentes (2 ADRs paralelo a Onda C+E; 3 em H; 4 em D+F+I; 6 em G).

4. **F4 lessons reaplicadas literal** — cond 5 primária isolada (sucessor parcial absorvendo 2 ADRs); cond 4 NÃO aplica (ADR-045 carrega categoria meta; ADR-054 é oitava instância de migração); cond 1 NÃO aplica (ADR-045/-046/-047/-048/-049/-050/-051/-053 ancestrais codificados); cond 2 NÃO aplica — regra central preservada (ADR-032 § Decisão skill /note + ADR-042 § Decisão flag --to absorvidas literal).

5. **F1 lesson reaplicada literal** — link rot em 2 categorias identificado pré-execução: (a) histórica via archive blockquote redirect; (b) **doutrinal ativa hot spot** via absorção no consolidado. Hot spots concentrados em skill alvo (skills/note/SKILL.md com 5 ocorrências combinadas) + foundation (CLAUDE.md table + README.md hot spot user-facing + docs/install.md verificação manual cenário) + skills consumidoras (skills/next/SKILL.md + skills/triage/SKILL.md leem NOTES.md como contexto suplementar).

### Composição do cluster vs sketch original do charter

Charter sketch original (NOTES 2026-05-30T06:08:04Z) / ADR-045 § Decisão parte 1 § Implementação:

```
ADR-009-bridge-meta-system.md           # /note + cross-project write +
                                        # informational store
                                        # (absorve atual: 032, 042)
```

**Sketch absorvia 2 ADRs; Onda J inclui exatos 2** (sem refinamento editorial — cluster sketch literal aplicado). Pattern editorial limpo:

- **Sem aplicação formal de modos ADR-052** — todos 2 ADRs do sketch absorvidos; nenhum preservado fora do cluster por constraint mecânico (a) ou categoria distinta (b/c).
- ADR-042 já tinha sido preservado standalone fora da Onda I via modo (a) bullet 1; agora absorvido naturalmente em Onda J (fim da pendência editorial).

**Saldo:** Onda J absorve 2 ADRs (literal sketch). Inventário pós-Onda J: 28 - 2 archivados + 1 ADR-054 = **27 vigentes** (drop líquido de 1 nesta onda; calibração mínima paralelo a Onda E).

**Linha do backlog:** Onda J é sub-scope da umbrella multi-onda em `## Próximos`; não corresponde a linha distinta. Per ADR-049 § Decisão (a) + precedente Ondas A-I, umbrella é atualizada in-place post-merge.

## Resumo da mudança

**Esta Onda J produz:**

1. **ADR-054 consolidado** (criado via `/new-adr` no /triage step 4) — absorve substância de ADR-032 + ADR-042 num único ADR temático "bridge cross-project — skill /note + .claude/local/NOTES.md store". § Decisão integra:

   - (a) **Skill `/note` foundational + store doutrinário non-role** (de ADR-032): skill geradora que faz `append <conteúdo>` timestampado em `.claude/local/NOTES.md` — store doutrinário **fixo non-role**, local-gitignored por design (canonical committed vazaria privacidade). Categoria nova "store doutrinário fixo non-role" ao lado de `.worktreeinclude` na tabela "The role contract" — sem schema declarável, sem alternativa de path. Captura **operador-driven** via skill explícita (sustentável; sem inundação). Skill independente de CLAUDE.md / role contract (frontmatter sem `roles:` per ADR-003). **Cross-project read como fenômeno conversacional** — sem auto-discovery agressivo, sem skill complementar de leitura/busca; operador menciona NOTES.md de outro projeto em prosa, Claude propõe candidato via contexto. **Mecânica de invariante `.worktreeinclude`** preservada: `/note` passo 1 aplica silentemente probe-and-add idempotente (per Addendum 2026-05-27 de ADR-032 absorvido em ADR-047 § Decisão — segundo dispatcher universal, ortogonal ao trigger condicional do `/init-config` step 4.5; cross-ref preserved para ADR-047 § Decisão como autoridade vigente).

   - (b) **Flag `--to` cross-project write com discovery via `$PROJECTS_DIR`** (de ADR-042, sucessor parcial de § Decisão (a)): extensão da skill `/note` com flag opcional `--to <projeto-ou-path>`. Comportamento default intra-projeto preservado (sem `--to` → append no `<repo-corrente>/.claude/local/NOTES.md`). Cross-project write é **opt-in explícito**. **Discovery em 2 níveis**: (i) `--to <nome>` (sem `/`) → resolve via `$PROJECTS_DIR/<nome>/.claude/local/NOTES.md`; `$PROJECTS_DIR` ausente → recusa explícita; target inexistente → recusa listando projetos detectados; (ii) `--to <path-absoluto>` (começa com `/`) → bypass discovery. **Critério mecânico contrato-vs-heurística** (load-bearing): `$PROJECTS_DIR` é contrato declarado (env var explícita) — distinto de heurística filesystem-wide rejeitada (não tentar `~/Projects/`, `find /storage/...`); recusa explícita orientando definir env var quando ausente. **Pré-condição target inicializado**: cross-write exige target com `.claude/local/` existente E `git check-ignore` cobrindo; faltando → recusa orientando inicializar via sessão CC do target (move first-time setup para contexto onde operador aprova mudanças). **Gates Gitignore/Worktree replication NÃO rodam cross-write** (blast-radius preserved per `/run-plan §1.1`); pré-condição substitui gates. **Mesmo formato de append**: timestamp UTC + corpo literal; receptor não distingue origem mecanicamente (operador prefaceia em prosa quando relevante).

   § Origem histórica preserva 2 incidentes empíricos: (1) sessão CC 2026-05-15 cross-session em `pje-2.1` que se estendeu para `connector-pje-mandamus-tjpa` (sessão `pje-issue-1920`) — recopia manual de contexto entre sessões → ADR-032 (skill `/note` foundational; pain real cross-session intra-project com referência cross-project); (2) sessão CC 2026-05-28 varredura empírica de 6 NOTES.md ativos confirmou pattern ad hoc recorrente cross-repo (dotfiles↔loadout com ≥6 entradas; drive-sync←chezmoi; meta-system↔consumers; pragmatic-dev-toolkit/.claude/local/NOTES.md linha 4 *"Sessão CC: meta-system (cross-repo registration)"*) — operador escrevendo manualmente a partir de outra sessão → ADR-042 (flag `--to`; pain real cross-project write resolvido em send-side ergonômico). § Gatilhos consolida triggers das 2 decisões. § Auto-aplicação cond 5 primária isolada per F4 Ondas C-I.

   **Substância preservada para link rot doutrinal ativa categoria-b** — gap fechado quando docs vivos citam membros do cluster archived:
   - `CLAUDE.md` linha 43 (table role contract entry `.claude/local/NOTES.md`) cita ADR-032 + ADR-042 como autoridades do `/note` e cross-project write → ADR-054 § Decisão (a)+(b) preserva substância.
   - `README.md` linha 12 (descrição user-facing `/note [--to <target>] <content>`) cita ADR-042 como autoridade do cross-project write — hot spot user-facing per ADR-051 § Decisão (b) discoverability.
   - `docs/install.md` linha 38 (cenário 3a Verificação manual cross-project write) cita ADR-042 como decisão.
   - `skills/note/SKILL.md` linha 9 (cabeçalho cita ADR-032 + ADR-047 como autoridades); linhas 17, 30, 57, 94 (4 ocorrências ADR-042 como decisão dos 2 modos + resolução do target + caminho cross-write + critério contrato-vs-heurística).
   - `skills/next/SKILL.md` linha 22 (informational read de NOTES.md cita ADR-032 store non-role).
   - `skills/triage/SKILL.md` linha 38 (informational read de NOTES.md cita ADR-032 store non-role).
   - ADRs vigentes preservados citando ADR-032/-042 como precedente (cross-refs históricas, categoria (a) preserved via redirect canonical): ADR-037, ADR-043 Addendum, ADR-045, ADR-047, ADR-050, ADR-053.

2. **Archive de ADR-032, ADR-042** — `git mv` para `docs/decisions/archive/` + header redirect canonical (format de ADR-046): blockquote `> **ARCHIVED 2026-05-31** — content absorbed into [ADR-054](../ADR-054-<slug>.md); see that ADR for current authority. Body below preserved verbatim for historical record.` + header H1 original preservado intacto abaixo.

3. **Archive index update** — `docs/decisions/archive/README.md` ganha 2 linhas novas na tabela (Onda J). Cada onda C-X estende a tabela como invariante codificada em ADR-046.

4. **Propagação de cross-refs em docs vivos** (6 arquivos; 10 ocorrências em 10 linhas distintas):
   - `CLAUDE.md` linha 43 → ADR-054 § Decisão (a) (ADR-032 store doutrinário non-role) + ADR-054 § Decisão (b) (ADR-042 cross-project write); ADR-047 cross-ref preservada como vigente.
   - `README.md` linha 12 → ADR-054 § Decisão (a)+(b) (ADR-047 cross-ref + ADR-042 cross-project write; user-facing descoberta).
   - `docs/install.md` linha 38 → ADR-054 § Decisão (b) (cenário 3a Verificação manual cross-project write).
   - `skills/note/SKILL.md` linha 9 → ADR-054 § Decisão (a) (ADR-032 store + ADR-047 cross-ref preserved).
   - `skills/note/SKILL.md` linha 17 → ADR-054 § Decisão (b) (2 modos da skill).
   - `skills/note/SKILL.md` linha 30 → ADR-054 § Decisão (b) (resolução do target).
   - `skills/note/SKILL.md` linha 57 → ADR-054 § Decisão (b) (caminho cross-write blast-radius).
   - `skills/note/SKILL.md` linha 94 → ADR-054 § Decisão (b) Contexto (critério mecânico contrato-vs-heurística).
   - `skills/next/SKILL.md` linha 22 → ADR-054 § Decisão (a) (informational read NOTES.md store non-role).
   - `skills/triage/SKILL.md` linha 38 → ADR-054 § Decisão (a) (informational read NOTES.md store non-role).

5. **Link rot consciente em docs imutáveis** — ADRs imutáveis e planos históricos citam ADR-032/-042 em § Origem como precedente ou cross-ref doutrinal (categoria (a) histórica de F1 lesson Onda C). Subset suspeito de categoria (b) doutrinal ativa já identificado pré-execução (todos com substância absorvida em ADR-054):
   - ADRs vigentes (-037, -043, -045, -047, -050, -053) citam ADR-032/-042 como precedente — categoria histórica preserved via redirect canonical.
   - ADR-018 (archived em Onda D) tem Addendum 2026-05-27 citando ADR-032 — categoria histórica preserved (archived com redirect para ADR-047 cobre).
   Hipótese de zero substância "doutrinal ativa" perdida — design-reviewer valida.

6. **Charter atualização** (post-merge, manual) — `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução" tabela adiciona linha "Onda J — Migração cluster bridge cross-project" + saldo inventário atualizado (27 vigentes). NÃO escopo desta Onda J; commit separado post-merge per precedente Ondas A-I.

**Pattern de migração validado nesta onda** (oitava aplicação; calibração mínima sem aplicação formal de modos ADR-052):
- Cluster de 2 ADRs absorvidos cleanly (paralelo a Onda C+E; calibração mínima). Sem refinamento editorial — sketch literal aplicado.
- Hot spot em **skills/note/SKILL.md** (5 das 10 ocorrências). Spread em 6 docs vivos.
- F4 lessons reaplicadas literal (cond 5 isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica — regra central preservada).
- F1 lesson reaplicada literal (link rot 2 categorias; categoria-b doutrinal ativa identificada pré-execução; substância absorvida em ADR-054).
- **Invariante operacional 10 instâncias consecutivas** com reviewer-per-bloco estrito (C+D+E+F+G+H + plano ADR-052 + Onda I + Onda Promoção + esta Onda J): 3 blocos planejados, todos com `{reviewer: doc}`.

## Arquivos a alterar

### Bloco 1 — Archive 2 ADRs + archive index extension {reviewer: doc}

**Instrução para data dinâmica:** substituir `2026-05-31` no template do blockquote pela data de execução (formato `YYYY-MM-DD` do dia de aplicação) ao replicar em cada um dos 2 arquivos arquivados — pattern Ondas C+D+E+F+G+H+I.

- `git mv docs/decisions/ADR-032-skill-note-contexto-compartilhado.md docs/decisions/archive/`
- Editar topo do arquivo movido inserindo blockquote redirect **antes** do `# ADR-032: <título original>`:

  ```markdown
  > **ARCHIVED 2026-05-31** — content absorbed into [ADR-054](../ADR-054-bridge-cross-project-note-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

  # ADR-032: Skill /note e store de contexto compartilhado em .claude/local/NOTES.md
  ```

- `git mv docs/decisions/ADR-042-note-flag-to-cross-project-write.md docs/decisions/archive/` + análogo.
- Estender tabela em `docs/decisions/archive/README.md` adicionando 2 linhas (Onda J):

  ```markdown
  | ADR-032 — Skill /note e store de contexto compartilhado em .claude/local/NOTES.md | [ADR-054](../ADR-054-bridge-cross-project-note-consolidado.md) | J |
  | ADR-042 — Flag --to em /note para cross-project write com discovery via $PROJECTS_DIR | [ADR-054](../ADR-054-bridge-cross-project-note-consolidado.md) | J |
  ```

**Nota:** slug efetivo `ADR-054-bridge-cross-project-note-consolidado.md` já criado pelo `/new-adr` delegado nesta sessão de /triage; templates desta seção e Blocos 2-3 usam-no literal.

### Bloco 2 — Hot spot mecanismo: skills cross-refs (7 ocorrências em 3 docs) {reviewer: doc}

- `skills/note/SKILL.md` linha 9 (parágrafo cabeçalho): substituir "Per [ADR-032](../../docs/decisions/ADR-032-skill-note-contexto-compartilhado.md) — extensão de [ADR-047](...)" por "Per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a) — extensão de [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)". ADR-047 cross-ref preservada (vigente).
- `skills/note/SKILL.md` linha 17 (parágrafo "Skill aceita 2 modos"): substituir "(per [ADR-042](../../docs/decisions/ADR-042-note-flag-to-cross-project-write.md))" por "(per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b))".
- `skills/note/SKILL.md` linha 30 (parágrafo "Resolução do target"): substituir "(per [ADR-042](...))" por "(per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b))".
- `skills/note/SKILL.md` linha 57 (parágrafo "Caminho cross-write"): substituir "(com `--to`, per [ADR-042](...))" por "(com `--to`, per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b))".
- `skills/note/SKILL.md` linha 94 (bullet sobre critério mecânico contrato-vs-heurística): substituir "Critério mecânico contrato-declarado-vs-heurística (ADR-042 § Contexto) exige" por "Critério mecânico contrato-declarado-vs-heurística (ADR-054 § Decisão (b)) exige"; e "fere a doutrina de ADR-032 § F4 alternativa b" por "fere a doutrina de ADR-054 § Decisão (a) (F4 alternativa b absorvida da ADR-032 § Alternativas)".
- `skills/next/SKILL.md` linha 22 (parágrafo informational read NOTES.md): substituir "Informational (per [ADR-032](../../docs/decisions/ADR-032-skill-note-contexto-compartilhado.md) store non-role)" por "Informational (per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a) store non-role)".
- `skills/triage/SKILL.md` linha 38 (passo 1 sub-item 6 — informational read NOTES.md): substituir "(store non-role per [ADR-032](../../docs/decisions/ADR-032-skill-note-contexto-compartilhado.md); informational, nunca bloqueia)" por "(store non-role per [ADR-054](../../docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a); informational, nunca bloqueia)".

### Bloco 3 — Foundation + docs vivos cross-refs (3 ocorrências em 3 docs; hot spot user-facing README) {reviewer: doc}

**Nota editorial:** Bloco 3 unifica CLAUDE.md table + README.md (apex sensitivity — discoverability per ADR-051 § Decisão (b)) + docs/install.md (cenário Verificação manual). Doc-reviewer audita com mesma lente — justificado pela baixa cardinalidade (3 ocorrências total; splittar adicionaria overhead operacional desproporcional, paralelo à decisão F6 da Onda I).

- `CLAUDE.md` linha 43 (table row `.claude/local/NOTES.md`): substituir "(append-only, local-gitignored per [ADR-047](docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) extended in [ADR-032](docs/decisions/ADR-032-skill-note-contexto-compartilhado.md); non-role). Cross-project write via `/note --to <projeto-ou-path>` per [ADR-042](docs/decisions/ADR-042-note-flag-to-cross-project-write.md)" por "(append-only, local-gitignored per [ADR-047](docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) extended in [ADR-054](docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a)+(b); non-role). Cross-project write via `/note --to <projeto-ou-path>`". **Consolidação de cite** (Ockham operacional — evita 3 citações redundantes a ADR-054 na mesma linha): única referência cobre ambas dimensões (a) store doutrinário non-role + (b) cross-project write. ADR-047 cross-ref preservada (vigente). Substância (store non-role, append-only, local-gitignored, cross-project write via --to, $PROJECTS_DIR discovery, target inicializado pré-condição) preservada literal.
- `README.md` linha 12 (descrição user-facing `/note [--to <target>] <content>` na tabela components): substituir "(local-gitignored store extending ADR-047 to a non-role category)" por "(local-gitignored store extending ADR-047 to a non-role category per ADR-054 § Decisão (a))"; substituir "**Cross-project write** via `/note --to <project-or-path> <content>` (ADR-042)" por "**Cross-project write** via `/note --to <project-or-path> <content>` (ADR-054 § Decisão (b))". Hot spot user-facing per ADR-051 § Decisão (b) discoverability — substituição preserva substância integralmente (descrição do que a skill faz continua coerente para leitor pré-adoção).
- `docs/install.md` linha 38 (cenário 3a Verificação manual cross-project write): substituir "Cross-project write via `/note --to` (per [ADR-042](decisions/ADR-042-note-flag-to-cross-project-write.md))" por "Cross-project write via `/note --to` (per [ADR-054](decisions/ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (b))". Substância (cenário de smoke test cross-project) preservada literal.

## Verificação end-to-end

**Critérios de sucesso da Onda J:**

1. **ADR-054 criado** com Status `Proposto` em `docs/decisions/ADR-054-bridge-cross-project-note-consolidado.md` (ou slug equivalente decidido por `/new-adr`). § Origem cita ADR-032+ADR-042 como decisões absorvidas + ADR-045/-046/-047/-048/-049/-050/-051/-053 como templates + ADR-052 como meta-pattern editorial (sem aplicação formal — sketch literal absorvido); ADRs vigentes preservados citando substância (ADR-037, ADR-043 Addendum, ADR-045, ADR-047, ADR-050, ADR-053). § Decisão integra as 2 dimensões (a)+(b) sob narrativa única coerente. § Origem histórica preserva os 2 incidentes empíricos. § Gatilhos consolida triggers das 2 decisões. § Auto-aplicação cond 5 primária isolada; cond 4 NÃO aplica; cond 1 NÃO aplica; cond 2 NÃO aplica (regra central preservada).

2. **ADR-032, ADR-042 arquivados:** `ls docs/decisions/ADR-032-*.md docs/decisions/ADR-042-*.md` → vazio (movidos). `ls docs/decisions/archive/ADR-032-*.md docs/decisions/archive/ADR-042-*.md` → 2 arquivos presentes. Header redirect canonical no topo, H1 original intacto abaixo.

3. **Archive index estendido:** `wc -l docs/decisions/archive/README.md` aumenta em 2 linhas vs baseline; tabela carrega 27 linhas de mapping (incremento de 25 → 27 com adição das 2 da Onda J; decomposição cumulativa por onda: 2C + 4D + 2E + 4F + 6G + 3H + 4I + 2J), ordem cronológica preservada.

4. **`grep -l "^\*\*Status:\*\* Substituído" docs/decisions/ADR-032-*.md docs/decisions/ADR-042-*.md`** → vazio (ADRs absorvidos sem marker Substituído — pattern absorção consolidatória per F4 lesson Onda D).

5. **`grep "ADR-032\|ADR-042" CLAUDE.md README.md docs/install.md skills/note/SKILL.md skills/next/SKILL.md skills/triage/SKILL.md`** → vazio (10 ocorrências substituídas em 6 docs vivos).

6. **Substância preservada para link rot doutrinal ativa categoria-b:**
   - `grep -c "store doutrinário\|non-role\|local-gitignored\|.worktreeinclude" docs/decisions/ADR-054-*.md` → ≥3 matches (substância ADR-032 store + invariante absorvidas).
   - `grep -c "\$PROJECTS_DIR\|pré-condição target\|blast-radius\|--to" docs/decisions/ADR-054-*.md` → ≥4 matches (substância ADR-042 cross-write absorvida).
   - `grep -c "fenômeno conversacional\|cross-project read" docs/decisions/ADR-054-*.md` → ≥1 match (substância ADR-032 cross-project read absorvida).
   - `grep -c "contrato-declarado\|heurística filesystem" docs/decisions/ADR-054-*.md` → ≥1 match (critério mecânico contrato-vs-heurística absorvido).

7. **ADRs vigentes preservados (não arquivados; cross-refs históricas):** `grep -l "ADR-032\|ADR-042" docs/decisions/ADR-0*.md | wc -l` → ~6 ADRs vigentes com cross-ref histórica preservada via redirect canonical (mantêm como autoridade histórica imutável; ADRs vigentes NÃO editados per ADR-classical).

8. **ADR-047 (vigente) cross-refs preservadas:** `grep -c "ADR-047" CLAUDE.md skills/note/SKILL.md` → ≥2 matches (ADR-047 continua vigente; substituições preservaram referência ao consolidado modo local).

9. **Link rot em immutable ADRs aceito explicitamente:** `grep -l "ADR-032\|ADR-042" docs/decisions/ADR-0*.md docs/plans/*.md` ainda retornará vários arquivos antigos — esses são imutáveis (immutable ADRs + historical plans); cross-refs em immutable docs ficam como registro histórico, NÃO são editados.

10. **CHANGELOG.md intacto** (registro histórico imutável) — `grep "ADR-032\|ADR-042" CHANGELOG.md` retorna matches preservados como registro de versionamento; NÃO editar.

11. **doc-reviewer audita drift cross-doc:** cross-refs corretos cross-doc; ADR-054 substância fiel a ADR-032+ADR-042 combinados; nenhuma carga doutrinal da § Discoverability e bridge do anti-regression checklist perdida (`/note --to` cross-project write + `$PROJECTS_DIR` discovery + path absoluto fallback + cross-project read fenômeno conversacional + store doutrinário non-role — todas preservadas em ADR-054).

12. **design-reviewer auto-fire em /new-adr step 5 e /triage step 5** valida: padrão de migração coerente com ADR-045 § Decisão parte 1; sketch literal aplicado sem refinamento editorial (sem aplicação formal de modos ADR-052); auto-aplicação per ADR-034 (cond 5 primária; cond 4/1/2 NÃO aplicam) coerente.

## Notas operacionais

**Ordem dos blocos:** Bloco 1 (archive) executado antes dos demais — outros blocos referenciam ADR-054 que substitui os 2 arquivos arquivados. Blocos 2-3 podem rodar em qualquer ordem (independentes entre si após archive); Bloco 2 (skills) tem hot spot mecanismo (skills/note/SKILL.md 5 ocorrências) — concentração maior justifica revisão antes do Bloco 3 (foundation + user-facing).

**Aderir reviewer-per-bloco estrito (invariante mantida da Onda C em diante — esta é a 10ª aplicação):** Bloco 1 (archive) DEVE invocar `doc-reviewer` obrigatório — invariante de 10 instâncias consecutivas (C+D+E+F+G+H + plano ADR-052 + I + Promoção + esta Onda J) sem exceção à doutrina explícita "Não pular revisor, mesmo em bloco trivial". Onda J mantém pattern.

**Validação da absorção da invariante `.worktreeinclude`** (ADR-032 § Decisão Addendum 2026-05-27): mecanismo "probe-and-add idempotente do `.claude/` em `.worktreeinclude`" foi absorvido em ADR-047 § Decisão durante Onda D (ADR-018 archived). Em ADR-054 § Decisão (a), cross-ref para ADR-047 § Decisão preservada como autoridade vigente da invariante (não duplica substância — ADR-054 cita ADR-047 como autoridade do mecanismo). Design-reviewer valida cross-ref preciso.

**Charter atualização post-merge:** após merge da Onda J, atualizar `docs/plans/redesign-camada-doutrinal-charter.md` § "Atualização pós-execução":
- Estender tabela de ondas com linha "Onda J — Migração cluster bridge cross-project" (commit hash + PR + substância).
- Anti-regression checklist § Discoverability e bridge — atualizar referências a "ADR-032/-042" para "ADR-054 § Decisão (a/b)".
- Saldo inventário pós-Onda J: estimado **27 vigentes** (28 pós-Onda I + 1 ADR-054 - 2 arquivados); drop líquido de 1 (paralelo a Onda E; calibração mínima).
- Anotação progressiva: "Onda J shipped — commit <hash>; cluster bridge cross-project migrado encerrando pendência editorial de ADR-042 preservado standalone de Onda I".

Update do charter é commit separado post-merge (paralelo às atualizações de umbrella in BACKLOG das Ondas A-I); NÃO escopo desta Onda J.

**Calibração mínima — sem aplicação formal de modos ADR-052:** Onda J é a primeira onda pós-codificação de ADR-052 (Onda I aplicou formal pela primeira vez) onde sketch literal foi aplicado sem refinamento editorial (sem exclusão/inclusão/preservação). Pattern editorial mais limpo possível — 2 ADRs absorvidos cleanly. Sinal de saúde: se Ondas J-X subsequentes seguirem este pattern (sketch literal sem refinamento), ADR-052 modos a/b/c continuam como contingência editorial vs invariante operacional.

**Cap de ondas estimado:** charter previa 6-10 ondas. Pós-Onda J (décima), trajetória esperada: ≥1 onda adicional; target 13-15 vigentes sujeito a re-auditoria do inventário remanescente (27 vigentes pós-Onda J vs ~14 ADRs ainda não absorvidos nem listados explicitamente). Cluster sequence revisitada — candidatos remanescentes pós-Onda J (amostra top-of-mind, não inventário exaustivo):
- **discoverability/branding** (ADR-037 + ?) — coleta de órfãos editoriais; sub-cluster pequeno (1-2 ADRs).
- **brainstorm** (ADR-036 standalone) — micro-cluster ou preservação como ADR clássico vigente.
- **apex meta-cluster** (ADR-009+034+035+043+045+046+047+048+049+050+051+052+053+054 — pode ou não consolidar; risco alto auto-referência).

**Sinal de saúde:** se Bloco 2 (skills/note hot spot 5 ocorrências) gerar ≥10 findings de doc-reviewer, sinal de que skills/note/SKILL.md cross-refs precisam refinamento antes de aplicar a clusters com hot spot mecânico maior. Pausar e iterar conforme charter linha 154.

## Decisões absorvidas

Findings absorvidos pré-commit pelos 2 design-reviewers (sobre ADR-054 + sobre este plano) per ADR-053 § Decisão (c) critério mecânico (caminho-único). Finding cutucado via `AskUserQuestion` (F3 § Cap de ondas — operador escolheu opção (a) reduzir escopo da projeção) fica em trace narrativo do commit message, NÃO nesta seção, per ADR-053 § Decisão (c) cláusula.

- ADR-054 § Decisão (b) bullet "gates cross-write": restaurada distinção textual original entre gate Gitignore (read-only probe via pré-condição) e gate Worktree replication (não roda em modo algum) — fidelidade textual ao ADR-042 § Decisão preservada (caminho-único).
- ADR-054 § Origem histórica item 2: expandida nota inline sobre ADR-035 (Substituído por ADR-043) mapeando critérios homólogos (critério 1 "incidente recorrente ou padrão observado" + critério 4 "codificação de pattern emergente ad hoc ≥3 vezes") — reduz a 1 hop a navegação do reader contemporâneo (caminho-único).
- Plano § Arquivos a alterar Bloco 2 cabeçalho: corrigida contagem aritmética "8 ocorrências" → "7 ocorrências" (5 skills/note + 1 skills/next + 1 skills/triage); 7+3=10 alinhado com § Resumo da mudança item 4 (caminho-único).
- Plano § Resumo da mudança + § Notas operacionais: corrigida invariante reviewer-per-bloco "9 ondas consecutivas" → "10 instâncias consecutivas" (C+D+E+F+G+H + plano ADR-052 + I + Promoção + esta Onda J = 10); enumeração explícita evita ambiguidade aritmética (caminho-único).
- Plano § Verificação end-to-end critério 3: refinado para incluir incremento explícito (`wc -l aumenta em 2 linhas vs baseline`) + estado-alvo unambiguous (25 → 27); remove ambiguidade temporal sobre quando a soma 2C+...+2J se aplica (caminho-único).
- Plano § Arquivos a alterar Bloco 3 CLAUDE.md:43: consolidada citação de 3 ADR-054 redundantes na mesma linha para única cite cobrindo § Decisão (a)+(b); Ockham operacional + reduz overhead editorial do doc-reviewer em runtime (caminho-único).
- Plano § Arquivos a alterar Bloco 1 Nota: removida instrução obsoleta "slug exato é determinado por /new-adr"; substituída por confirmação de slug efetivo já criado (ADR-054 já existe nesta sessão de /triage); elimina defensividade ornamental (caminho-único).

## Pendências de validação

- ~~**Critério 6.4 da § Verificação end-to-end (specification bug — typo lexical, paralelo à captura de Onda Promoção):** grep `"contrato-declarado\|heurística filesystem"` (com hífen + termo "filesystem") não casa o texto real do ADR-054. Substância está presente — linha 51 usa "*contrato declarado*" (com espaço, sem hífen); termo "heurística filesystem-wide" aparece em ADR-032 § Contexto absorvido como referência mais abstrata. Substância preservada confirmada via grep alternativo `"contrato declarado\|critério mecânico contrato\|heurística"` retornando 4 matches (linhas 13, 51 da § Decisão (b)). Sem impacto material — substância absorvida corretamente em ADR-054; apenas critério end-to-end como escrito gerou falso-negativo absorvível inline via re-grep. Refinamento do critério: prefixar com termo canonical "contrato declarado" (com espaço) ou aceitar match em qualquer formulação. Captura editorial paralela à de Onda Promoção (critério 6 lexical bug `Substituído` sem prefixo Status field).~~ **Encerrada 2026-06-01:** resolvida sistemicamente via Onda K' (PR #102, commit `c713238`) — diretriz canonical #3 (fidelidade ao texto-alvo via `Read` antes de hardcodar grep) codificada em `templates/plan.md` § Verificação end-to-end comentário HTML inline. Aplicação forward (planos posteriores aplicam diretriz; plano histórico imutável).
