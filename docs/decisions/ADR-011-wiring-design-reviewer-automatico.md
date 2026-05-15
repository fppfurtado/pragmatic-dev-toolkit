# ADR-011: Wiring automático do design-reviewer no /triage e /new-adr

**Data:** 2026-05-08
**Status:** Aceito

## Origem

- **Decisão base:** [ADR-009](ADR-009-revisor-design-pre-fato.md) → "Gatilhos de revisão" #1: *"Wiring automático em /run-plan pré-loop ou /new-adr pré-commit materializa → reabrir trade-off de tokens"*. Este ADR exerce o gatilho com evidência cumulativa do dogfood.

## Contexto

ADR-009 estabeleceu o `design-reviewer` como revisor document-level pré-fato com free-read de doctrine sources (`docs/decisions/*.md` + `docs/philosophy.md`), mas deferiu o wiring automático até dogfood acumular evidência. A janela de dogfood deliberada (registrada em memory `project_design_reviewer_dogfood`) fechou em 2026-05-08 com **3 invocações reais** e **7 findings cumulativos**:

| # | Data | Plano/ADR | Findings |
|---|---|---|---|
| 1 | 2026-05-07 | `instrumentar-skills-multi-passo.md` (PR #44) | 4 — ADR-worthiness do critério "≥3 passos" → ADR-010 (estrutural); alternativa Monitor; acoplamento harness; cerimônia gate sub-steps |
| 2 | 2026-05-08 | `triage-step0-already-deleted-remote.md` (PR #45) | 1 — alternativa "abrandar regra inteira" |
| 3 | 2026-05-08 | `run-plan-3-3-skip-empirico.md` (PR #46) | 2 — alternativa "memory paliativa"; nota lexical vs semântico |

**Padrão observado:** todas as 3 invocações ocorreram em `/triage` que produziu plano (caminho-com-plano), antes do commit do plano. Findings rebatem decisões enquanto o plano ainda está editável; rebater no diff (via `code-reviewer` em `/run-plan`) seria custo desproporcional. 5/7 findings foram editoriais; 1 foi estrutural (ADR-010 emergiu). Nenhum gerou retrabalho — todos couberam em ajustes pré-commit.

**Implicação para wiring:** `/run-plan` pré-loop seria gate **tarde** — plano já commitado e pushed. `/triage` pós-plano/pré-commit é o ponto natural; `/new-adr` standalone cobre ADRs criados fora do `/triage` (caso raro mas possível).

## Decisão

`design-reviewer` dispara automaticamente em:

1. **`/triage` que produz plano** (com ou sem ADR delegada), no passo 5 (antes do commit unificado). Findings reportados ao operador, que decide aplicar antes de commitar ou seguir como está. Sem cutucada de pré-execução — o gate é a presença dos findings, não uma pergunta binária. **Não dispara** em `/triage` que fecha em linha de backlog pura, atualização cirúrgica de `docs/domain.md`/`docs/design.md`, ou ADR-only delegada sem plano (esse último é coberto via #2 abaixo).

   Refinado por [ADR-026](ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md): default da aplicação invertido para absorção pré-commit + commit message estruturado; cutucada do operador via `AskUserQuestion` reservada para findings que satisfazem ≥1 das 3 condições (alternativas competindo / contradiz doutrina / contexto externo). Mecânica do wiring (quando dispara, override por inação) preservada.

2. **`/new-adr`** (standalone OU delegada por `/triage`), antes de retornar controle. Cobre tanto ADR criada diretamente pelo operador quanto ADR criada pelo `/triage` no caminho ADR-only — evita dispatch duplo no caminho `/triage` → `/new-adr` → reviewer (o passo 5 do `/triage` reconhece que `/new-adr` já cobriu).

`/run-plan` permanece sem wiring de `design-reviewer` — gate seria tarde (plano já no remote) e a frequência alta multiplicaria o custo de tokens sem ganho proporcional.

Razões objetivas:

- **Empíricas:** 7 findings cumulativos em 3 invocações no `/triage` pré-commit confirmam o ponto natural; zero findings exercitados em `/run-plan` (não houve invocação ali no dogfood).
- **Custo aceitável:** `/triage` que produz plano/ADR é frequência **média** (não toda invocação produz artefato — muitas fecham em linha de backlog). `/new-adr` standalone é frequência **rara** (estimativa de calibração: até ~5/sprint; acima disso revisitar — ver Gatilhos de revisão). Free-read de ~10 ADRs + `philosophy.md` (~12k tokens/invocação) cabe nesse perfil.
- **Sem cutucada inicial:** ADR-002 ("eliminar gates de cutucada quando trilho automático cobre") aplicado — perguntar `Rodar reviewer?` antes de toda invocação é cerimônia (resposta majoritária seria "Sim" durante dogfood). Findings reportados são o trilho automático equivalente a Aviso/Validação/Backlog do `/run-plan` §3.5; operador decide a ação antes de commitar.
- **Override por inação:** operador pode ignorar findings (commitar mesmo assim). `design-reviewer` reporta, não bloqueia.

## Consequências

### Benefícios

- **Cobertura sem ônus de memória:** decisões estruturais em planos/ADRs revisadas sem operador precisar lembrar de `@-mention`.
- **Ponto temporal correto:** findings chegam quando o plano/ADR ainda está editável (pré-commit), maximizando o ROI de cada finding.
- **Memory `project_design_reviewer_dogfood` encerra:** o estado provisório opt-in vira default formalizado; memory é arquivada.

### Trade-offs

- **`/triage` que produz plano/ADR fica ~12k tokens mais caro por invocação.** Aceitável dado o ROI empírico (5+ findings editoriais por release de plano/ADR — cada um corrigiria depois 5x mais caro).
- **Operador acostumado ao opt-in pode estranhar findings sem ter pedido:** mitigação editorial — `/triage` passo 5 cita explicitamente que findings são reportados antes do commit (não surpresa).
- **`/run-plan` continua sem gate document-level:** se uma decisão estrutural escapou do `/triage` e só apareceu durante a implementação no `/run-plan`, o ciclo só pega no merge ou em revisão pós-fato. Aceitável — caso raro; `code-reviewer` por bloco já cobre eixo de design no diff.
- **Findings em prosa volátil (assimetria com ADR-002):** o trilho automático de findings descrito acima reporta em prosa ao operador antes da cutucada de commit, sem persistir em artefato como o `## Pendências de validação` de ADR-002 faz para warnings de `/run-plan`. Se o operador rola o terminal e commita, o finding desaparece sem trace. Aceitável porque o artefato (plano/ADR) está editável e o operador acabou de ver — janela curta, baixa probabilidade de perda. Reabrir se operador reportar findings importantes perdidos sistematicamente (gatilho registrado abaixo).

### Limitações

- **Free-read continua dependendo de ADRs granulares:** ADR vago não captura contradição (limitação herdada de ADR-009).
- **Paths não-canonicais:** se o consumidor declara `decisions_dir` em modo local, o free-read precisa enxergar `.claude/local/decisions/`. Tratado pelo Resolution protocol — `design-reviewer` lê `<decisions_dir>` resolvido, não path literal.

## Alternativas consideradas

### (a) `/run-plan` pré-loop + `/new-adr` pré-commit

Gate em ambos os pontos. Cobertura total, mas `/run-plan` pré-loop é gate **tarde** (plano já commitado e pushed); custo de tokens em alta frequência (toda invocação de `/run-plan`, não só as que produzem plano novo). 5/7 findings do dogfood vieram do `/triage` pré-commit, não do `/run-plan`. Descartado.

### (b) Só `/new-adr` pré-commit

Cobertura mínima (só ADR explícita). Planos com decisões estruturais embutidas (ADR-010 emergiu de plano, não de ADR pré-existente) escapariam — exatamente o tipo de finding mais valioso (1/7 do dogfood). Descartado.

### (c) Opt-in permanente (status quo dogfood)

Manter `@-mention` manual. Zero overhead de tokens default, mas depende de disciplina do operador/agente em invocar — falhar uma vez tem custo desproporcional (decisão estrutural não-rebatida vira código). Memory `project_design_reviewer_dogfood` operacionalizou isso durante dogfood; encerrar memory sem wiring oficial seria perda do ganho do dogfood. Descartado.

### (d) Wiring via Task tool (subagent delegation)

Wiring nos mesmos pontos da decisão escolhida, mas via `Task` tool (subagent frio) em vez de `@-mention` inline. Reabertura prevista por ADR-009 → `## Alternativas consideradas` ("Delegação via Task/Agent tool dentro do reviewer — descartado nesta iteração; reabrir se wiring automático em alta frequência materializar"). ADR-011 exerce a reabertura e mantém a escolha original — `@-mention` inline — pelas razões: (i) volume de docs ainda pequeno (~10 ADRs + `philosophy.md`); subagent frio + briefing duplicado anularia a economia; (ii) frequência prevista é média/baixa (não "alta frequência" no sentido de ADR-009 — esse foi gatilho hipotético para `/run-plan` pré-loop em todo invocação, descartado em (a)); (iii) Task delegation adicionaria complexidade (cold start, paralelização opcional, custo de orquestração) sem ganho proporcional para o volume atual. Reabrir se volume de ADRs ultrapassar ~30 ou se frequência efetiva de `/triage` que produz plano/ADR superar uma chamada por dia em uso real.

## Gatilhos de revisão

- **Operador frequentemente ignora findings sem aplicar (ou reporta findings importantes perdidos):** sinal de que `design-reviewer` está sensível demais, tokens não compensam, ou a prosa volátil falha em capturar findings sérios. Reabrir critério editorial do reviewer, voltar para opt-in, ou introduzir trilho persistente análogo a `## Pendências de validação` de ADR-002.
- **Tokens de `/triage` superam ROI mensurável:** se ADRs crescerem além de ~30 ou `philosophy.md` dobrar de tamanho, free-read fica caro mesmo em frequência média — reabrir para considerar curadoria semi-automática (ADR-009 limitação já registra esse gatilho).
- **Falsos positivos crescem:** reviewer flaga findings que operador descarta sistematicamente — sinal de que ADRs estão vagos (ADR-009 limitação) ou critério do reviewer precisa refinamento.
- **Aparece skill nova produzindo decisão estrutural pré-commit:** wiring deve estender por simetria (não relistar ad hoc).
