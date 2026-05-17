# Roadmap de execução — auditorias 2026-05-15/16

Sequência recomendada para implementar as propostas das duas auditorias do ciclo 05-15/16:

- `docs/audits/runs/2026-05-15-architecture-logic.md` — propostas com sufixo `_arch` (A_arch a H_arch).
- `docs/audits/runs/2026-05-16-prose-tokens.md` — propostas com sufixo `_prose` (A_prose a F_prose).

**Nota para sessão futura:** leia os 2 audits antes de pegar um item daqui — cada proposta refere-se a achados específicos com contexto que não cabe nesta lista.

**Convenção de status:** `[ ]` pendente · `[~]` em andamento · `[x]` concluído (atualizar com link a commit/PR/ADR shippado + data curta).

**Convenção de encaminhamento:** cada item entra pelo fluxo padrão `/triage <proposta>` que decide artefato (linha de backlog, plano, ADR, atualização cirúrgica). Bundles indicados explicitamente abaixo passam por **um único** `/triage` produzindo plano cobrindo os itens agrupados.

**Sobreposição declarada (item unificado):** `G_arch` (helper cutucada de descoberta, eixo arquitetural) ≡ `C_prose` (extração `docs/procedures/cutucada-descoberta.md`, eixo prosa). Mesma intervenção, descrita por dois eixos distintos. Tratada como **um único item** no roadmap, referida como `G_arch ≡ C_prose`. Auditoria arquitetural identifica como "antecipar gatilho ADR-029"; auditoria prosa quantifica em ~120 w líquidos cross-skill.

---

## Onda 1 — fechamento editorial em curso (drift ADR Proposed/implementação)

Ponto-mãe da auditoria 2026-05-15: ADRs em Proposto com mecânica já em vigor. **Atualização pós-pull 2026-05-16:** inventário corrigido — universo real eram ~14-15 ADRs em Proposto no snapshot da auditoria (não 7 como o inventário disse; agente inventariante errou status dos 7 que viriam a ser promovidos pelo PR #67). PR #67 promoveu 7 (ADRs 005, 011, 015, 020, 021, 023, 026); PR #69 completou ADR-032 stub + implementou skill `/note`. Restam **9 ADRs em Proposto** (022, 024-032) deliberadamente por critério editorial Strong-stable do plano `fechar-pendencias-e-promover-adrs` (= shipped + dogfood/multiple invocations + no regression observed). Ordem: pré-requisitos primeiro (decidir 032, dogfood validador), promoção massa depois.

- [x] **B_arch** — decidir destino de ADR-032 (`/note` + store de contexto compartilhado). [PR #69](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/69) (2026-05-15): caminho (b1) — ADR completado (placeholders preenchidos) + skill `/note` criada como 11ª skill do plugin. Status frontmatter do ADR segue `Proposto` por critério Strong-stable não atingido (aguarda dogfood/multiple invocations). Skill `/note` **não declara `roles.required`** e explicita que cutucada de descoberta não aplica — não conta como 6º consumidor de cutucada (impacto em G_arch ≡ C_prose: ver Onda 3).
- [x] **F_arch** (2026-05-16) — dogfood seco executado em sessão; preview reportou `0 elegíveis · 0 cross-refs · 33 não-elegíveis (24 sem campo `**Linha do backlog:**` + 9 com drift de matching) · 45 silentes (< 2 semanas)`. Mecânica estrutural (coleta, 6 critérios cumulativos, categorização editorial/aviso/degraded/silente, gate) validada. **Achado empírico para refinamento de ADR-022 antes da promoção:** critério 4 usa `git log -S "<texto>"` sensível a reedições in-place — todas as 45 linhas matcháveis aparecem como "< 2 semanas" mesmo quando estão em `## Concluídos` há ~10 dias visíveis, pois cleanup editorial textual avança o timestamp do pickaxe. Três saídas possíveis registradas no log da sessão: (i) `git log --follow --diff-filter=A` na primeira linha do bloco; (ii) ancorar idade no commit que moveu para `## Concluídos` (exige marcador novo); (iii) relaxar threshold para "≥ 4 semanas após primeira aparição em qualquer forma". Decisão fica para A_arch item ADR-022.
- [~] **A_arch** — promover ADRs Proposto→Aceito quando critério Strong-stable bater. **Progresso:** [PR #67](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/67) (2026-05-15) promoveu 7 ADRs (005, 011, 015, 020, 021, 023, 026) + rebaixou ADR-024 a Medium pelo finding F2 do design-reviewer; commit `ae0146b` (2026-05-16) promoveu **ADR-024** (destrancado pela Onda 3 — categoria `docs/procedures/` atinge 3 itens). **Restam 8 ADRs em Proposto** (022, 025-032) com mecânica em vigor; promoção de cada um aguarda evidência específica per plano `fechar-pendencias-e-promover-adrs` (dogfood ou múltiplas invocações sem regressão). Sub-tarefas-destrancadoras: F_arch (destranca 022 — refinamento pré-promoção registrado em F_arch); demais aguardam uso real. Cross-refs stale (ADR-025:52 e ADR-026:66) já corrigidos no PR #67.

**Encaminhamento sugerido:** F_arch via linha de backlog (1 invocação seca + reporte). A_arch deixa de ser onda massa — cada ADR restante promove-se quando seu critério individual bater; meta-acompanhamento pode rodar como leitura periódica do índice de decisões, não como plano único.

## Onda 2 — auto-loaded (impacto a cada turn)

Único item de eixo auto-loaded. Independente de todas as demais ondas; pode rodar em paralelo. Maior ROI de palavras-por-edit no corpus runtime.

- [x] **A_prose** (2026-05-16) — 4 descriptions encurtadas conforme proposta: `security-reviewer` (frase final removida), `init-config` (cauda "em projeto novo..." removida), `triage` (condensada para "mudança não-trivial sem plano ou linha de backlog"), `release` (frase final "Use quando..." removida). Commit cirúrgico direto no main per encaminhamento.

**Encaminhamento sugerido:** linha de backlog (4 edits cirúrgicos em frontmatter, sem plano). Pode entrar como commit cirúrgico direto no main paralelo a qualquer onda.

## Onda 3 — extração para `docs/procedures/` (bundle cross-skill)

Padrão "extração para procedure" inaugurado por `cleanup-pos-merge.md` ganha 2 novos artefatos no mesmo PR. Coerência com ADR-024 (que formaliza a categoria) — onda 3 valida `docs/procedures/` como padrão editorial estável.

Bundle único: um `/triage` produz plano "novas procedures cross-skill" cobrindo B_prose + G_arch≡C_prose.

- [x] **G_arch ≡ C_prose** (2026-05-16) — `docs/procedures/cutucada-descoberta.md` criado (31 linhas: tri-state + 2 strings literais + algoritmo + posicionamento). 5 SKILLs (`/triage`, `/run-plan`, `/new-adr`, `/next`, `/draft-idea`) wired via line-ref `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md` (paridade exata com `cleanup-pos-merge.md`). CLAUDE.md `## Cutucada de descoberta` trimada de ~25 linhas para ~6 (preserva scope das 5 skills, gatilho 6ª skill de ADR-029, regra de herança editorial + checklist code-reviewer, cross-refs ADR-017/029 + `/init-config`). Net: ~17 linhas removidas auto-loaded por turn + ~30 w cross-skill nos 5 sites. [PR #71](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/71). Categoria `docs/procedures/` passa a 2 itens (cleanup-pos-merge + cutucada-descoberta); 3º item virá no plano gêmeo `procedures-forge-auto-detect`.
- [x] **B_prose** (2026-05-16) — `docs/procedures/forge-auto-detect.md` criado (36 linhas: algoritmo parse remote + host detection + CLI probe + 4 outputs distintos `gh`/`glab`/`no-detection`/`unsupported-host` + notas com policy local por consumer). 4 SKILLs (`/release §5`, `/next §4.5`, `/run-plan §3.7`, `/archive-plans §1` critério 6) + 1 procedure (`docs/procedures/cleanup-pos-merge.md`) wired via line-ref `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md` (5 sites). ADR-022 critério 6 não tocado — procedure cross-refs ADR como decisão de origem do uso `search <slug>`. Net: ~100 w cross-skill removidos. [PR #72](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/72). Este PR sozinho move categoria `docs/procedures/` para 2 itens (cleanup-pos-merge + forge-auto-detect); merge conjunto com PR #71 (G_arch ≡ C_prose, plano gêmeo) atinge 3 itens (cleanup-pos-merge + cutucada-descoberta + forge-auto-detect) fortalecendo critério Strong para promoção de ADR-024 via A_arch.

**Encaminhamento sugerido:** plano único cobrindo as 2 extrações; sequenciar 1 PR por extração para revisão mais fácil (Bloco 1 = cutucada; Bloco 2 = forge). G_arch≡C_prose primeiro porque tem mais sites (5 vs 4) e gatilho ADR-029 mais próximo.

**Atenção cross-onda:** se `B_arch` (Onda 1) decidir por (b1) completar ADR-032 e implementar `/note`, a nova skill emerge como 6º site da cutucada de descoberta. Sequenciar Onda 3 **antes** de Onda 1 b1 evita re-trabalho (skill nasceria já consumindo o procedure); sequenciar Onda 3 **depois** de Onda 1 b1 garante que o procedure já contempla o 6º consumidor desde o nascimento. Decisão depende de cadência preferida do operador.

## Onda 4 — coerência editorial baixo-risco (bundles por arquivo)

Edições cirúrgicas em 3 SKILLs. Bundle por arquivo evita conflito de merge entre edits sequenciais no mesmo SKILL.md.

### 4a — `/triage` (frontmatter + sub-fluxo)

- [x] **C_arch** (2026-05-16, commit `75d0f25`) — `/triage` frontmatter: `plans_dir` movido de `roles.required` para `roles.informational`. Sub-fluxo de criação canonical estendido para cobrir `plans_dir` (modelo do `backlog` aplicado: `Criar em docs/plans/` / `Não usamos esse papel`). Cutucada de descoberta scope em CLAUDE.md + procedure atualizado por coerência: "5 skills que reativamente consomem Resolution protocol step 3" + nota explícita de que `/triage` emite por designação editorial mesmo com `plans_dir` informational. Behavior unchanged; doctrine description ajustada à realidade pós-C_arch.

### 4b — `/run-plan` (refactor + bullet)

- [x] **D_prose** (2026-05-16, commit `e34b5d8`) — `/run-plan §1.1` 4 sub-casos stderr de `git worktree add` migrados para tabela `| Detecção (stderr regex) | Linha do backlog |`. Paralelo a `## Detecção de warnings pré-loop` da mesma skill. Ganho de legibilidade + ~50 w reduzidos.
- [x] **E_prose (parte /run-plan)** (2026-05-16, commit `e34b5d8`) — bullet "## O que NÃO fazer" sobre comandos destrutivos compactado: enumeração exaustiva → "ex.: `git reset --hard`, `git worktree remove`" + cross-ref doutrinária preservada (CLAUDE.md global, blast-radius compartilhado). Mantém ≥1 exemplo + cross-ref — risco de regressão do incidente pré-existente preservado.

### 4c — `/draft-idea` (bullet + Read condicional)

- [x] **E_prose (parte /draft-idea) + F_prose** (2026-05-16, commit `785f853`) — 3 trims cirúrgicos: (i) bullet 6 em `## O que NÃO fazer` perde "(decisão F2 do design-reviewer no plano)" — cicatriz datada removida; (ii) bullet 5 perde "(passo 5)" — recapitulação do body; (iii) passo 4 ganha guard explícito "Executar apenas em modo one-shot OR em modo update com ≥1 seção escolhida" — Read de `templates/IDEA.md` agora self-documenting como condicional.

**Encaminhamento sugerido:** 3 linhas de backlog (4a, 4b, 4c), uma por arquivo. Sem dependência cruzada; podem rodar em qualquer ordem dentro da onda. Bundle por SKILL evita ping-pong de revisão.

**Dependência com Onda 3:** se G_arch≡C_prose for executada **antes** de 4b/4c, os SKILLs `/run-plan` e `/draft-idea` já estarão sem a duplicação da cutucada; edição posterior é cirúrgica sobre prosa restante. Sequência preferível: Onda 3 → Onda 4.

## Onda 5 — decisões doutrinárias / meta

Edições que mexem em doutrina. Memória "Limiar de ADR para mudanças em doutrina" sugere default ADR para refinamentos doutrinários — esta onda potencialmente gera 1-2 ADRs novos.

- [x] **D_arch** (2026-05-16, commit `ea602bf`) — [ADR-033](../../decisions/ADR-033-templates-admite-single-consumer-declarativo.md) sucessor parcial de ADR-001 codifica critério relaxado: templates/ aceitável para single-consumer **quando declarativo** (esqueleto preenchível processado via Read). 2 testes mecânicos para fronteira (skill faz Read em runtime? + editar isoladamente faz sentido?). ADR-001 ganha Addendum 2026-05-16 (paralelo a Addendum 2026-05-12 → ADR-024).
- [x] **E_arch** (2026-05-17, commit `b8ffb6d`) — [ADR-034](../../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) meta-doutrina codifica critério mecânico: novo ADR quando ≥1 das 5 condições aplica; adendo em ADR existente quando todas as 4 aplicam. § Localização do adendo documenta 4 formas observadas (Addendum, parágrafo cross-ref inline em § Decisão/§ Limitações, bullet em § Implementação, bullet em § Limitações). CLAUDE.md § Editing conventions ganha bullet cross-ref (paralelo a ADR-010/011/023/026 pattern).

**Encaminhamento sugerido:** D_arch via `/triage` → ADR sucessor de ADR-001 (decisão sobre critério editorial). E_arch via `/triage` → muito provavelmente ADR meta (alinhado à regra-mãe). Não bundle entre si — eixos doutrinários distintos.

## Onda 6 — débito conhecido / cosmético

- [x] **H_arch** (2026-05-16) — comentário no `hooks/block_gitignored.py` registra a dependência implícita do allowlist `.claude/` na convenção Claude Code: trigger de revisão (CC muda convenção) + cross-ref para audit L2. ADR cirúrgico não criado (gatilho concreto ausente; comentário inline + cross-ref bastam).

---

## Pontos de atenção cross-onda

- **B_arch destranca A_arch.** ADR-032 (stub vazio) precisa ter status decidido antes da varredura de promoção massa — incluí-lo no escopo de A_arch sem decisão prévia produz inventário inconsistente.
- **F_arch informa A_arch (item ADR-022).** Dogfood seco de `/archive-plans` em modo preview valida a mecânica que ADR-022 (em Proposto) decide. Sucesso da execução reforça promoção; falha pivota para refinamento antes do Aceito.
- **Onda 3 antes da Onda 4.** Se G_arch≡C_prose extrai cutucada para procedure, os SKILLs `/run-plan` e `/draft-idea` ficam mais enxutos antes das edições cirúrgicas das 4b/4c. Inverter a ordem força edição sobre prosa que vai mudar logo depois.
- **Onda 3 e Onda 1 b1 — resolvido pós-pull 2026-05-16.** Caminho (b1) materializado via PR #69; skill `/note` criada explicitamente **fora do contrato de cutucada de descoberta** (sem `roles.required`, frontmatter declara "cutucada não aplica"). Sequência preocupada (Onda 3 antes vs depois de Onda 1 b1) deixou de ser dependência cruzada — `/note` não consome o procedure mesmo quando criado.
- **Bundle Onda 2 com qualquer outra é inválido** — A_prose é único item auto-loaded; demais ondas são por invocação respectiva. Pode rodar em paralelo a tudo, mas não bundle.
- **Bundle G_arch≡C_prose com qualquer item de outra auditoria é inválido** — mesma proposta vista por dois eixos; entra **uma vez** no roadmap.
- **`design-reviewer` em A_arch.** Promoção massa cruza com vários ADRs sucessores (ADR-029 sucede ADR-017; ADR-030 sucede ADR-005; ADR-031 sucede ADR-027). `design-reviewer` lerá inventário grande — invocação na Onda 1 paga custo de ADR-021 curadoria + scan. Operador anota `**ADRs candidatos:**` no plano de promoção com os 7 IDs explicitamente para priorizar leitura integral.
- **Onda 5 toca doutrina ativa.** Memória "Limiar de ADR para mudanças em doutrina" estabelece default ADR para refinos doutrinários — Onda 5 itens são exatamente isso. Não tentar atalho via linha de backlog; rebatimento em `/triage` deve gerar ADR(s) sucessor(es) per regra-mãe.
- **Release cadence.** Onda 1 sozinha é coherent set (promoção massa + dogfood) → considerar `/release patch` ao fim (promoção é metadata, sem bump funcional óbvio — operador decide). Ondas 2/3/4 podem acumular em `main` ou bumpar entre, conforme energia. Onda 5 deve fechar com `/release minor` se gerar ADR(s) novo(s).

---

## Redução total estimada (eixo prosa)

| Onda | Auto-loaded | Por invocação | Tokens estimados |
|---|---|---|---|
| 1 (B+F+A_arch) | — | — | promoção editorial; sem redução direta |
| 2 (A_prose) | ~50 w | — | ~65/turn |
| 3 (G_arch≡C_prose + B_prose) | — | ~220 w | ~285/invocação afetada |
| 4a (C_arch) | — | trivial (frontmatter + sub-fluxo) | trivial |
| 4b (D_prose + E_prose run-plan) | — | ~90 w | ~115/invocação `/run-plan` |
| 4c (E_prose draft-idea + F_prose) | — | ~10 w + Read condicional | trivial |
| 5 (D+E_arch) | — | ADRs novos possíveis | +volume líquido |
| 6 (H_arch) | — | comentário + opcional ADR | trivial |
| **Total prosa** | **~50 w auto** | **~320 w por invocação** | **~465 tokens** |

Comparado com roadmap 2026-05-12 (~580 w / ~755 tokens), esta onda é menor — esperado, pois a anterior limpou os maiores focos. Esta é refinamento incremental + fechamento editorial do ciclo Proposto.

---

## Histórico de execução

- **B_arch** — [PR #69](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/69) (2026-05-15): caminho (b1) — ADR-032 completado (placeholders preenchidos) + skill `/note` criada (11ª skill, store doutrinário fixo non-role em `.claude/local/NOTES.md`, sem `roles.required`, fora do contrato de cutucada de descoberta). Pré-existente ao snapshot deste roadmap; revisão pós-pull 2026-05-16 reconciliou.
- **A_arch (parcial)** — [PR #67](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/67) (2026-05-15): 7 ADRs promovidos Proposto→Aceito (005, 011, 015, 020, 021, 023, 026) per critério Strong-stable do plano `fechar-pendencias-e-promover-adrs`; ADR-024 rebaixado a Medium pelo finding F2 do design-reviewer; cross-refs stale (ADR-025:52, ADR-026:66) historicized in-place. Itens deste roadmap apontavam ADRs já-Aceito como Proposto por erro de inventário do agente original — corrigido pós-pull.
- **F_arch + A_prose** — commit cirúrgico direto no main (2026-05-16): F_arch dogfood seco de `/archive-plans` reportou 0 elegíveis + finding empírico para refinamento de ADR-022 (sensibilidade do pickaxe a reedições in-place — 3 saídas propostas no checklist do item); A_prose encurtou 4 descriptions auto-loaded (`security-reviewer`, `init-config`, `triage`, `release`) por ~50 w líquidos por turn. Ondas 1 (parcial — resta refinamento de ADR-022 antes de promoção) e 2 fechadas em uma única passada.
- **G_arch ≡ C_prose** — plano `procedures-cutucada-descoberta` executado via `/run-plan` (2026-05-16): 4 blocos (procedure criado · 5 SKILLs wired · CLAUDE.md trimada · roadmap atualizado). 3 design-reviewer findings de Plan 1 absorvidos pré-fato no `/triage` + 1 finding absorvido pré-commit no Bloco 3 (gap clarity em CLAUDE.md). Onda 3 parte 1 fechada. Plan 2 (`procedures-forge-auto-detect`, Onda 3 parte 2) próximo via `/run-plan`. [PR #71](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/71).
- **B_prose** — plano `procedures-forge-auto-detect` executado via `/run-plan` (2026-05-16): 4 blocos (procedure criado com 4 outputs distintos · 4 SKILLs wired · cleanup-pos-merge.md cross-refed · roadmap atualizado). 3 design-reviewer findings de Plan 2 absorvidos pré-fato no `/triage` (ADR-024 critério 3 itens, ADR-022 cross-ref vs edit, cross-procedure dependency nomeada) + 2 findings absorvidos pré-commit (gap clarity em outputs section + wording archive-plans). Onda 3 parte 2 fechada — bundle conjunto com PR #71 (Plan 1 G_arch ≡ C_prose) atinge 3 itens na categoria `docs/procedures/` (cleanup-pos-merge + cutucada-descoberta + forge-auto-detect), fortalecendo critério Strong para promoção de ADR-024 via A_arch. [PR #72](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/72).
- **A_arch (ADR-024) + Onda 4 (C_arch + D/E/F_prose)** — commits cirúrgicos diretos no main (2026-05-16): ADR-024 promovido Proposto→Aceito (commit `ae0146b`) destrancado pela Onda 3 (categoria a 3 itens, fator YAGNI suspeito resolvido). C_arch (commit `75d0f25`) reclassifica `/triage` `plans_dir` como informational + estende sub-fluxo + atualiza scope da cutucada em CLAUDE.md/procedure por coerência. D_prose + E_prose run-plan (commit `e34b5d8`) tableizam §1.1 stderr cases + compactam bullet destrutivo. E_prose draft-idea + F_prose (commit `785f853`) trimam 2 cicatrizes datadas + adicionam guard explícito de modo no passo 4. Ondas 4a/b/c fechadas; A_arch restante = 8 ADRs em Proposto (022 awaits refinement; 025-032 aguardam uso real).
- **Onda 6 H_arch** — commit cirúrgico direto no main (2026-05-16, commits `9202d62` + `8b224a0`): comentário de 5 linhas em `hooks/block_gitignored.py` na branch de allowlist registra dependência implícita do `.claude/` literal na convenção Claude Code; trigger de revisão (CC muda convenção) + cross-ref ao audit L2 (2026-05-12). Sem ADR cirúrgico (gatilho concreto ausente).
- **Onda 5 D_arch + E_arch** — commits cirúrgicos diretos no main (2026-05-16/17): ADR-033 sucessor parcial de ADR-001 codifica critério `templates/` aceita single-consumer **quando declarativo** + 2 testes mecânicos de fronteira; ADR-001 ganha Addendum 2026-05-16 (commit `ea602bf`). ADR-034 meta-doutrina codifica critério mecânico adendo vs novo ADR (5 condições disjuntivas para novo ADR; 4 conjuntivas para adendo) + 4 formas observadas de adendo; CLAUDE.md § Editing conventions ganha bullet cross-ref (commit `b8ffb6d`). 6 design-reviewer findings absorvidos em ADR-033 + 4 absorvidos em ADR-034 + 2 cutucadas operador em cada ADR. Auto-aplicação coerente confirmada em ADR-034 § Auto-aplicação (sucessor parcial).

(Atualizar conforme cada item shippa — link a commit/PR/ADR + data curta.)
