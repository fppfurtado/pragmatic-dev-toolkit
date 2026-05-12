# Plano — Trim residual editorial Onda 4

## Contexto

Bundle "trim cirúrgico" da **Onda 4** do roadmap `docs/audits/runs/2026-05-12-execution-roadmap.md`. Re-execução da auditoria prose-tokens (`docs/audits/runs/2026-05-12b-prose-tokens.md`) pós-fechamento das Ondas 1-3b confirmou os 3 itens prose originais pendentes (E_prose, F_prose, G_prose) e identificou 4 novos achados (A-NEW, B-NEW, C-NEW, D-NEW). Total estimado: ~210 palavras / ~275 tokens.

Bundle homogêneo — edits cirúrgicos de prosa em 5 arquivos (`CLAUDE.md`, `agents/doc-reviewer.md`, `templates/plan.md`, `skills/run-plan/SKILL.md`, `skills/init-config/SKILL.md`, `skills/release/SKILL.md`). Sem decisão estrutural pendente; sem ADR.

Ordem dos blocos prioriza ganho auto-loaded: Bloco 1 (`doc-reviewer` description) + Bloco 2 (dedup dispatch em CLAUDE.md) são auto-loaded por turn — ganho imediato.

## Resumo da mudança

7 edits prose-tokens consolidados em 6 blocos (F_prose + G_prose unificados — mesmo arquivo, lógica correlacionada):

1. **Bloco 1 (B-NEW)** — `agents/doc-reviewer.md` frontmatter description: 48 → ~25 palavras, remove enumeração de 3 tipos de drift que duplica `## O que flagrar` do body. **Auto-loaded por roteador**.
2. **Bloco 2 (C-NEW)** — `CLAUDE.md` linhas 15-17 (Plugin layout / **Agents**) reduzidas a 1 frase apontando para a tabela em "The role contract" (linha 43). Remove duplicação de dispatch que aparece em ambas. **Auto-loaded por turn**.
3. **Bloco 3 (A-NEW)** — `templates/plan.md` comentário dos 3 campos especiais (Termos ubíquos, ADRs candidatos, Linha do backlog) condensado de 2-3 linhas cada → 1 linha cada. ~40 palavras.
4. **Bloco 4 (E_prose)** — `skills/run-plan/SKILL.md` §3.3 sanity check de docs: 3 skip + cutucada em prosa contínua → tabela `Condição | Skip silente? | Ação`. Ganho de legibilidade.
5. **Bloco 5 (F_prose + G_prose)** — `skills/init-config/SKILL.md`: (a) preâmbulo linhas 12-13 ("Diferente das demais skills do toolkit...") compactado em 1 frase enxuta; (b) bullet em `## O que NÃO fazer` linha 128 encolhido (~30 → ~15 palavras) preservando função-checklist mecânica — design-reviewer flagou que bullet é guarda contra exceção localizada não-óbvia (`/init-config` é única skill fora do universo de ADR-017); preâmbulo é função-justificativa, bullet é função-checklist, não são intercambiáveis.
6. **Bloco 6 (D-NEW)** — `skills/release/SKILL.md` §4.5 item 5 "Aplicar" (linha 126): sentença ~250 palavras descrevendo recovery proativo + sequência (a)-(e) reescrita como tabela de recovery + sequência enumerada. Ganho principal de legibilidade; redução de palavras modesta.

Sem decisão estrutural — nenhum ADR previsto. Critério editorial **Editing conventions** § "Skills end with an explicit `## O que NÃO fazer`" preservado em todos os blocos.

## Arquivos a alterar

### Bloco 1 — `agents/doc-reviewer.md` description (B-NEW) {reviewer: doc}

- `agents/doc-reviewer.md`: substituir o `description:` no frontmatter de 48 palavras para ~25 palavras. Texto-alvo: `"Revisor de drift entre documentação e código no diff. Stack-agnóstico. Acionar quando o diff toca .md/.rst/.txt ou renomeia/remove identificadores referenciados em docs."`. Body do agent (`## O que flagrar`) já cobre os 3 tipos de drift (identificadores, cross-refs, exemplos) — description é tag de invocação, não duplicação do body.

### Bloco 2 — `CLAUDE.md` dedup dispatch (C-NEW) {reviewer: doc}

- `CLAUDE.md` linhas 15-17 (seção "Plugin layout (what loads what)", bullet **Agents**): reduzir a 1 frase listando os 5 reviewers + ponteiro para a tabela em "The role contract". Texto-alvo aproximado: `"Agents — agents/<name>.md with frontmatter. Five reviewers shipped: code-reviewer, qa-reviewer, security-reviewer, doc-reviewer, design-reviewer. Dispatch rules in 'The role contract' table below."`. Linha 43 (última row da tabela, que detalha dispatch + shadow rule) mantida como fonte única.

### Bloco 3 — `templates/plan.md` comentário compactado (A-NEW) {reviewer: doc}

- `templates/plan.md` linhas 14-28 (comentário HTML com 3 campos especiais): condensar cada campo a 1 linha. Texto-alvo:
  ```
  **Termos ubíquos tocados:** <Termo> (<categoria>) — bounded context|agregado|entidade|RN|conceito; omitir em refactor/doc-only.
  **ADRs candidatos:** ADR-NNN (motivo) — opcional; reviewer prioriza esses, scan cobre os demais (ADR-021).
  **Linha do backlog:** <texto exato> — incluir quando há linha no BACKLOG; mensageiro pra /run-plan operar transições.
  ```
  Preservar header `Campos especiais (incluir só quando aplicáveis):` e indentação canonical.

### Bloco 4 — `skills/run-plan/SKILL.md` §3.3 prosa → tabela (E_prose) {reviewer: doc}

- `skills/run-plan/SKILL.md` linhas 99-103 (§3.3 "Sanity check de docs user-facing"): trocar os 3 bullets de skip + 1 bullet de cutucada por tabela `Condição | Skip silente? | Ação`. Manter intro "Antes do done:" + preservar prosa pós-tabela sobre listar referrers concretos (`<path>:<linha>: <trecho>` — não candidatos genéricos). Tabela proposta:

  | Condição | Skip silente? | Ação |
  |---|---|---|
  | Plano lista `.md` user-facing + diff toca | sim | — |
  | `## Resumo da mudança` sem superfície user-facing | sim | — |
  | Grep de identificadores tocados retorna vazio | sim (empírico) | — |
  | Caso contrário | não | Cutucar enum `Docs` (Consistente / Listar arquivos a atualizar) listando referrers concretos antes |

  Definições de "user-facing" (positive list: `README*`, `CHANGELOG*`, `install.md`, `docs/install.md`, `docs/guides/**`) e "identificadores tocados" (filenames base sem extensão de `## Arquivos a alterar` + nomes de skill/agent/comando textualmente presentes em `## Resumo da mudança`) preservadas em prosa pós-tabela.

### Bloco 5 — `skills/init-config/SKILL.md` preâmbulo + bullet (F_prose + G_prose) {reviewer: doc}

- `skills/init-config/SKILL.md` linha 13 (preâmbulo "Diferente das demais skills do toolkit..."): compactar parágrafo de ~50 palavras em 1 frase. Texto-alvo: `"Frontmatter sem `roles:` por design (ADR-003 § Schema, listas vazias podem ser omitidas) — /init-config define o bloco que o Resolution protocol lê em vez de consumi-lo; cutucada de descoberta (ADR-017) não se aplica dentro desta skill."`. Preserva referências aos 2 ADRs e a justificativa, elimina narrativa contrastiva ("Diferente das demais skills...").
- `skills/init-config/SKILL.md` linha 128 (`## O que NÃO fazer`): encolher bullet de ~30 → ~15 palavras. Texto-alvo: `"- **Não emitir cutucada de descoberta (ADR-017):** /init-config define o bloco em vez de consumir."`. Bullet preservado como guarda-checklist contra exceção localizada (autor de skill nova com `roles.required` clonando pattern das outras 4 skills pode replicar cutucada inadvertidamente em `/init-config`-clone) per critério editorial em CLAUDE.md → "Editing conventions" e ADR-017 § "Editorial inheritance". Manter os outros 4 bullets do `## O que NÃO fazer` intactos.

### Bloco 6 — `skills/release/SKILL.md` §4.5 item 5 "Aplicar" estrutura (D-NEW) {reviewer: doc}

- `skills/release/SKILL.md` linha 126 (item 5 "Aplicar" do gate `AskUserQuestion`): reescrever a sentença única (~250 palavras) como sub-fluxo enumerado com tabela de recovery. Estrutura-alvo:

  ```markdown
  - **`Aplicar`** — executar em sequência:

    1. **Verificar HEAD.** `git symbolic-ref --short HEAD`. Em três estados:

       | Estado | Ação | Sub-ações |
       |---|---|---|
       | Detached ou branch ≠ pré-condição 2 | Recovery proativo | `git status --porcelain`; se sujo, `git stash push -m "release v<X.Y.Z> auto-stash"`; depois `git checkout <branch-da-pré-condição-2>` |
       | Branch OK, behind upstream | Sync | `git fetch origin <branch>`; `behind=$(git rev-list --count HEAD..@{u})`; `behind > 0` → `git pull --ff-only` (falha → abortar release com erro literal, instruir pull manual) |
       | Branch OK, sync OK | (nenhuma) | — |

    2. **Reportar ao operador** ref-atual encontrada no início, branch esperado, nome da stash se criada, e número de commits trazidos pelo pull se aplicável (operador roda `git stash pop` manual após release).

    3. **Aplicar sequência:** (a) escrever cada `version_file`; (b) inserir entrada no changelog; (c) `git add <paths-específicos>` (**não** `git add -A`); (d) `git commit -m "<msg>"`; (e) `git tag -a <tag>` com **um `-m` por linha** da mensagem composta no item 3.5 (`-m "Release <tag>" -m "Added: ..." -m "Changed: ..." ...`); fallback (sem síntese) usa `-m "Release <tag>"` único.
  ```

  Preservar literalmente: invariantes do `git add -A` (warning de risco), formato `-m` por linha da tag (item 3.5), e o fallback. Não introduzir comportamento novo — só re-estruturar prosa.

## Verificação end-to-end

Pós-execução, confirmar via comandos concretos:

- **Bloco 1:** `wc -w` no `description:` extraído de `agents/doc-reviewer.md` retorna ≤30 (vs 48 atual).
- **Bloco 2:** `sed -n '15,20p' CLAUDE.md` mostra ≤6 linhas para o bullet **Agents** (vs ~7 atual com 3 sentenças). `grep -c "invoked by /run-plan per" CLAUDE.md` retorna 1 (não 2 — single source no linha 43).
- **Bloco 3:** `wc -w templates/plan.md` retorna ≤370 palavras (vs 408 atual). `grep -c "ADRs candidatos:" templates/plan.md` retorna 1 (preservado).
- **Bloco 4:** `grep -c "| Condição | Skip silente? | Ação |" skills/run-plan/SKILL.md` retorna 1. Prosa pós-tabela menciona "identificadores tocados" + "referrers concretos".
- **Bloco 5:** `grep -c "Diferente das demais skills" skills/init-config/SKILL.md` retorna 0 (cicatriz removida). `grep -c "Não emitir cutucada de descoberta (ADR-017)" skills/init-config/SKILL.md` retorna 1 (bullet encolhido preservado). `grep -c "ADR-017" skills/init-config/SKILL.md` retorna ≥2 (preâmbulo compactado + bullet encolhido).
- **Bloco 6:** `grep -c "| Estado | Ação | Sub-ações |" skills/release/SKILL.md` retorna 1. `grep -c "um \`-m\` por linha" skills/release/SKILL.md` retorna 1 (invariante preservada).
- **Total:** `wc -w CLAUDE.md agents/doc-reviewer.md templates/plan.md skills/run-plan/SKILL.md skills/init-config/SKILL.md skills/release/SKILL.md` mostra redução agregada de ~150-210 palavras vs baseline pré-plano.

Sem `test_command` aplicável (toolkit sem suite per `<!-- pragmatic-toolkit:config -->`); verificação end-to-end é textual.

## Notas operacionais

- **Bundle homogêneo** — todos os blocos são prose-refactor. `doc-reviewer` cobre os 6.
- **Sem `## Verificação manual`** — refactor de prosa sem comportamento perceptível novo. Doc-only.
- **Auto-loaded payload** — Blocos 1 e 2 atuam em superfície carregada a cada turn (description de agent + CLAUDE.md). Outros blocos são por-invocação. Ordem deliberada: 1 e 2 primeiro para realizar o ganho imediatamente.
- **Onda 4 fecha** — após este plano shippar, atualizar `docs/audits/runs/2026-05-12-execution-roadmap.md` marcando E_prose, F_prose como `[x]`; G_prose como `[x]` com nota "absorvido em forma encolhida pós-finding do design-reviewer (bullet preservado como guarda-checklist conforme critério editorial em CLAUDE.md)" + acrescentar nota cruzada com `2026-05-12b-prose-tokens.md` cobrindo A/B/C/D-NEW. Após isso, único item residual do roadmap é H_arch (diferido — só com evidência empírica).
- **Trade-off documentado em Bloco 5 (G_prose).** Auditoria propôs remover bullet linha 128 como redundante (recapitula preâmbulo). Design-reviewer flagou bullet como guarda-checklist contra exceção localizada não-óbvia (`/init-config` é única skill `roles.required`-vizinha que não emite cutucada ADR-017; autor de skill nova clonando pattern pode replicar inadvertidamente). Bullet ocupa overlap entre as duas regras do critério editorial em CLAUDE.md → "Editing conventions": (1) "recapitula prosa anterior é ruído"; (2) "exceção localizada deve permanecer". Resolução: encolher (~30 → ~15 palavras) preserva função-checklist sem duplicar a ratio do preâmbulo. Captura ~15 palavras do trim original em vez de ~30.
- **Sem ADR no caminho** — bundle puramente editorial; nenhum dos 6 blocos toca decisão estrutural duradoura. `design-reviewer` invocado pelo `/triage` (ADR-011) sinalizará se ele discordar.
