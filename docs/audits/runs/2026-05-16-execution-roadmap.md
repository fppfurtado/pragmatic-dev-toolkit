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
- [ ] **F_arch** — antecipar primeira execução de `/archive-plans` em modo preview (gate `Cancelar`), sem aplicar archival. Valida coleta dos 78 planos + 6 critérios cumulativos + preview estruturado antes do gatilho ADR-014 (≥100 planos) forçar uso reativo. **Destranca A_arch item ADR-022**: critério Strong-stable do plano de promoção exige dogfood empírico; dogfood seco fornece a evidência sem aplicar archival. Custo: 1 invocação + leitura de preview.
- [~] **A_arch** — promover ADRs Proposto→Aceito quando critério Strong-stable bater. **Parcialmente shippado:** [PR #67](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/67) (2026-05-15) promoveu 7 ADRs (005, 011, 015, 020, 021, 023, 026) + rebaixou ADR-024 a Medium pelo finding F2 do design-reviewer ("§Limitações reconhece categoria com 1 item como YAGNI suspeito"). **Restam 9 ADRs em Proposto** (022, 024-032) com mecânica em vigor; promoção de cada um aguarda evidência específica per plano `fechar-pendencias-e-promover-adrs` (dogfood ou múltiplas invocações sem regressão). Sub-tarefas-destrancadoras: F_arch (destranca 022); criar nova procedure via Onda 3 (destranca 024 — promove categoria com 1 item suspeito para categoria com 3 itens); demais aguardam uso real. Cross-refs stale (ADR-025:52 e ADR-026:66) já corrigidos no PR #67.

**Encaminhamento sugerido:** F_arch via linha de backlog (1 invocação seca + reporte). A_arch deixa de ser onda massa — cada ADR restante promove-se quando seu critério individual bater; meta-acompanhamento pode rodar como leitura periódica do índice de decisões, não como plano único.

## Onda 2 — auto-loaded (impacto a cada turn)

Único item de eixo auto-loaded. Independente de todas as demais ondas; pode rodar em paralelo. Maior ROI de palavras-por-edit no corpus runtime.

- [ ] **A_prose** — encurtar 4 descriptions auto-loaded longas: `security-reviewer` (42→~28 w; remover frase final que duplica categorias da primeira), `init-config` (29→~22 w; remover cauda "em projeto novo ou reconfigurar bloco existente"), `triage` (29→~22 w; condensar "feature, fix ou refactor sem plano nem linha de backlog" → "mudança não-trivial sem plano ou linha de backlog"), `release` (24→~18 w; remover "Use quando o operador autorizou publicar release" — `release` no name já é o gatilho). Redução: ~50 w (~65 tokens) auto-loaded por turn.

**Encaminhamento sugerido:** linha de backlog (4 edits cirúrgicos em frontmatter, sem plano). Pode entrar como commit cirúrgico direto no main paralelo a qualquer onda.

## Onda 3 — extração para `docs/procedures/` (bundle cross-skill)

Padrão "extração para procedure" inaugurado por `cleanup-pos-merge.md` ganha 2 novos artefatos no mesmo PR. Coerência com ADR-024 (que formaliza a categoria) — onda 3 valida `docs/procedures/` como padrão editorial estável.

Bundle único: um `/triage` produz plano "novas procedures cross-skill" cobrindo B_prose + G_arch≡C_prose.

- [ ] **G_arch ≡ C_prose** — criar `docs/procedures/cutucada-descoberta.md` consolidando tabela tri-state (CLAUDE.md ausente / marker ausente / dedup) + 2 strings canonical. Sites afetados: `skills/triage`, `skills/run-plan`, `skills/new-adr`, `skills/next`, `skills/draft-idea` — cada um substitui ~30 w por 1 linha de referência. **Urgência rebaixada pós-pull 2026-05-16:** skill `/note` (PR #69) é a 11ª skill mas **não consome** cutucada (sem `roles.required` + frontmatter explicita "cutucada não aplica"). Gatilho ADR-029 segue em 5/6 — proposta válida pelo eixo redução-de-prosa (~120 w líquidos cross-skill), não pela iminência do gatilho. **Bônus pós-pull:** criar a procedure também destranca promoção de **ADR-024** (item A_arch — hoje rebaixado a Medium por "categoria com 1 item como YAGNI suspeito"; bundle B_prose + G_arch≡C_prose move categoria para 3 itens, fortalecendo critério Strong). **Test de regressão:** confirmar que cutucada continua disparando nos 5 sites após o refactor.
- [ ] **B_prose** — criar `docs/procedures/forge-auto-detect.md` consolidando mecânica auto-detect forge (parse `git remote get-url origin` → `github.com`/`gh` / regex `^gitlab\.`/`glab` / fallback textual com link CLI). Sites afetados: `skills/release §5`, `skills/next §4.5`, `skills/run-plan §3.7`, `skills/archive-plans §1` critério 6, `docs/procedures/cleanup-pos-merge.md` (substituir versão embutida por referência também). Redução: ~100 w líquidos cross-skill. **Validação:** cada SKILL preserva contexto local (gate `AskUserQuestion` específico de cada caminho fica na SKILL — só a parte de detecção forge migra).

**Encaminhamento sugerido:** plano único cobrindo as 2 extrações; sequenciar 1 PR por extração para revisão mais fácil (Bloco 1 = cutucada; Bloco 2 = forge). G_arch≡C_prose primeiro porque tem mais sites (5 vs 4) e gatilho ADR-029 mais próximo.

**Atenção cross-onda:** se `B_arch` (Onda 1) decidir por (b1) completar ADR-032 e implementar `/note`, a nova skill emerge como 6º site da cutucada de descoberta. Sequenciar Onda 3 **antes** de Onda 1 b1 evita re-trabalho (skill nasceria já consumindo o procedure); sequenciar Onda 3 **depois** de Onda 1 b1 garante que o procedure já contempla o 6º consumidor desde o nascimento. Decisão depende de cadência preferida do operador.

## Onda 4 — coerência editorial baixo-risco (bundles por arquivo)

Edições cirúrgicas em 3 SKILLs. Bundle por arquivo evita conflito de merge entre edits sequenciais no mesmo SKILL.md.

### 4a — `/triage` (frontmatter + sub-fluxo)

- [ ] **C_arch** — reclassificar `/triage roles.required = [plans_dir]` para `informational`. A skill decide entre 4 saídas (linha de backlog, plano, ADR delegado, atualização domain/design); `plans_dir` só é necessário no caminho-com-plano. Tornar informational alinha frontmatter à dependência real (paralelo a `/debug` que declara só informational apesar de ler `decisions_dir`). Adicionar sub-fluxo: quando passo 3 escolhe "plano" e `plans_dir` resolveu "não temos", aplicar oferta canonical via enum (paralelo ao sub-fluxo de `backlog` no passo 4 — pattern já existe). ADR-003 frontmatter declarativo prevê required vs informational como propriedades-por-papel-por-skill.

### 4b — `/run-plan` (refactor + bullet)

- [ ] **D_prose** — estruturar `/run-plan §1.1` (4 sub-casos stderr de `git worktree add`) em tabela `| Detecção (stderr regex) | Linha do backlog | Ação |`. Prosa contínua atual: ~300 palavras com regex inline. Padrão paralelo a `## Detecção de warnings pré-loop` (mesma skill) e `/run-plan §3.3` (sanity check de docs — E_prose 2026-05-12). Redução: ~50 w + maior ganho em legibilidade.
- [ ] **E_prose (parte /run-plan)** — compactar bullet de "O que NÃO fazer" sobre comandos destrutivos. Condensar enumeração exaustiva "incluindo mas não limitado a `git checkout`/`git switch` no principal, `git branch -D`, `git worktree remove`, `git reset --hard`" → "comandos destrutivos no working tree principal (ex.: `git reset --hard`, `git worktree remove`)" + manter cross-ref "CLAUDE.md global exige confirmação explícita para ações de blast-radius compartilhado". **Risco baixo-médio:** bullet é pós-incidente; manter pelo menos 1 exemplo + cross-ref doutrinária preserva a regra.

### 4c — `/draft-idea` (bullet + Read condicional)

- [ ] **E_prose (parte /draft-idea) + F_prose** — bundle por arquivo. (i) **E_prose parte /draft-idea**: remover "(decisão F2 do design-reviewer no plano)" do bullet 6 — cicatriz interna datada; regra preservada. (ii) **F_prose bullet 5**: cortar "(passo 5)" da prosa "Não invocar `/triage` automaticamente — só **sugere** no relatório (passo 5)" — recapitulação do body. (iii) **F_prose Read condicional**: condicionar `Read` do `templates/IDEA.md` em `/draft-idea` passo 4 a "modo update com ≥1 seção escolhida OR modo one-shot" (skip silente upstream torna o Read órfão). Redução: ~50 w + Read condicional em caminho ocioso.

**Encaminhamento sugerido:** 3 linhas de backlog (4a, 4b, 4c), uma por arquivo. Sem dependência cruzada; podem rodar em qualquer ordem dentro da onda. Bundle por SKILL evita ping-pong de revisão.

**Dependência com Onda 3:** se G_arch≡C_prose for executada **antes** de 4b/4c, os SKILLs `/run-plan` e `/draft-idea` já estarão sem a duplicação da cutucada; edição posterior é cirúrgica sobre prosa restante. Sequência preferível: Onda 3 → Onda 4.

## Onda 5 — decisões doutrinárias / meta

Edições que mexem em doutrina. Memória "Limiar de ADR para mudanças em doutrina" sugere default ADR para refinamentos doutrinários — esta onda potencialmente gera 1-2 ADRs novos.

- [ ] **D_arch** — decidir critério editorial de `templates/` em face do single-consumer (`IDEA.md` adicionado via ADR-027 com 1 consumidor; ADR-001 estabelecia 3+ consumidores). Duas saídas: (d1) adendo a `ADR-001 § Implementação` registrando que single-consumer também justifica `templates/` quando o artefato é declarativo (esqueleto preenchível) — critério "skill geradora com template" relaxa exigência; (d2) mover `templates/IDEA.md` para `skills/draft-idea/template.md` (collocated) preservando ADR-001 escopo original. `/triage` + `design-reviewer` decide entre d1 e d2. Vale resolver **antes do 3º template emergir**.
- [ ] **E_arch** — critério editorial "refinamento de mecânica → adendo em ADR existente, não novo ADR". Registrar em `CLAUDE.md` (ou ADR meta-doutrina) distinguindo: (e1) **novo ADR** quando muda decisão estrutural, contradiz ADR anterior, codifica restrição externa, ou introduz categoria nova; (e2) **adendo em ADR existente** (§ Implementação ou § Limitações) quando refina mecânica sem alterar decisão central, ajusta threshold, formaliza pattern emergente. Sustenta cadeias temáticas (design-reviewer 4 ADRs, modo local 4 ADRs, cutucada 2 ADRs). **Risco médio:** memória "Limiar de ADR para mudanças em doutrina" estabelece default ADR para refinos doutrinários — diferenciação delicada; pode requerer próprio ADR meta (auto-aplicação coerente).

**Encaminhamento sugerido:** D_arch via `/triage` → ADR sucessor de ADR-001 (decisão sobre critério editorial). E_arch via `/triage` → muito provavelmente ADR meta (alinhado à regra-mãe). Não bundle entre si — eixos doutrinários distintos.

## Onda 6 — débito conhecido / cosmético

- [ ] **H_arch** — documentar dependência implícita `block_gitignored.py` ↔ convenção Claude Code (allowlist `.claude/` hardcoded na linha 64-66). L2 da auditoria 2026-05-12 persiste; risco baixo (convenção CC estável). Comentário no script + opcional ADR cirúrgico explicitando gatilho de revisão (mudança da convenção CC). Linha de backlog.

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

(Atualizar conforme cada item shippa — link a commit/PR/ADR + data curta.)
