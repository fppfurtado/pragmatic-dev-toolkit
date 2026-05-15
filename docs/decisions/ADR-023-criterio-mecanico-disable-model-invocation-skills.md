# ADR-023: Critério mecânico para declaração explícita de `disable-model-invocation` em skills

**Data:** 2026-05-12
**Status:** Aceito

## Origem

- **Decisão base:** `BACKLOG.md` `## Concluídos` — item "trocar `disable-model-invocation: true` para `false` em `/release`, `/run-plan` e `/new-adr`": primeira aplicação parcial com racional "blast radius real é baixo (release é local até push manual; run-plan opera em worktree isolada; new-adr só cria markdown), e inconveniência de não permitir autoinvocação supera o ganho do flag." Critério em embrião, registrado em artefato editorial canônico, sem generalização para skills futuras.
- **Investigação:** Auditoria [`docs/audits/runs/2026-05-12-architecture-logic.md`](../audits/runs/2026-05-12-architecture-logic.md) § 3 (proposta A_arch) diagnosticou drift editorial — 5 skills (`/triage`, `/debug`, `/gen-tests`, `/next`, `/init-config`) omitem o campo enquanto 4 declaram explicitamente `false` (`/release`, `/new-adr`, `/run-plan`, `/archive-plans` — a 4ª shippou na Onda 1 pós-recorte da auditoria).
- **Design review:** plano `docs/plans/tightening-editorial-auto-loaded.md` (Onda 2 do roadmap das auditorias) recebeu 2 findings altos do `design-reviewer` que rejeitaram o caminho doutrinário-sem-ADR: (1) wording em embrião do critério criava 3 ambiguidades quando aplicado retroativamente (`/triage` faz `git push` gateado, `/init-config` muta arquivos do consumer, `/release` é local mas o exemplo inicial classificava push de release como `true`); (2) formalizar critério parcial documentado é ADR-worthy per memory `feedback_adr_threshold_doctrine` + precedente direto ADR-013/ADR-020 da Onda 1.

## Contexto

Cada `SKILL.md` do toolkit pode declarar `disable-model-invocation: <bool>` no frontmatter — campo da harness Claude Code que controla se o modelo pode autoinvocar a skill ao decidir uma ação. Default da harness em ausência de declaração é fora do controle do plugin.

Hoje 9 skills shippadas no toolkit:

- **Declaram `false`:** `/release`, `/new-adr`, `/run-plan`, `/archive-plans`.
- **Omitem:** `/triage`, `/debug`, `/gen-tests`, `/next`, `/init-config`.

A doutrina parcial em embrião está no `BACKLOG.md` `## Concluídos` linha 43 — racional "blast radius real é baixo" aplicado a 3 skills nominalmente, sem generalização. Três tensões precisam ser endereçadas pela formalização:

1. **Drift editorial em skills omissas.** Skill nova herda critério por imitação frágil; doutrina não-escrita escapa do free-read do `design-reviewer` (ADR-009 § Limitações), reviewer não consegue ler como decisão estrutural duradoura.
2. **Wording em prosa única não testável.** Diagnóstico do `design-reviewer` no plano Onda 2 expôs que "blast radius local até ação visível externamente → `false`" cria 3 ambiguidades reais quando aplicado retroativamente — `/triage` faz `git push origin main` no caminho-com-plano (gateado por enum upstream), `/init-config` muta arquivos do consumer (cross-skill, não cross-team), `/release` declara `false` mas wording inicial classificava "release" como exemplo de `true`. Critério precisa distinguir ação **direta** vs ação **gateada por enum** + cross-skill vs cross-team.
3. **Risco de autoinvocação recursiva destrutiva.** ADR-006 § Limitações reconhece "comportamento meu (modelo) ad-hoc fora do roteiro... segue dependendo da minha calibragem". Skill cujo loop interno pode autoinvocar-se em loop (skill que muta artefato que ela mesma re-lê) tem risco ortogonal ao blast radius — `false` autoriza loop autoinvocado mesmo se cada iteração isolada é local.

## Decisão

Toda `SKILL.md` do toolkit declara `disable-model-invocation` **explicitamente** no frontmatter (sem omissão) com valor dado por **critério mecânico cumulativo**:

**Declara `false`** quando **todos** os critérios valem:

1. **Blast radius estritamente local pela ação direta da skill.** Mutação restrita ao working tree do consumer (arquivos, commits locais, criação/edição de worktrees). Push para remote, abertura de PR/MR, ação destrutiva remota, mensagem externa ou efeito imediato em sistema cross-team **não** contam como "local".
2. **Pushes/PRs gateados por enum upstream contam como local.** Quando push (ou outra ação cross-team) só acontece após `AskUserQuestion` cancel-friendly que o operador pode interromper, o gate é a fronteira, não a ação. A skill mantém blast-radius classificado pelo que faz **antes** do gate.
3. **Sem risco de autoinvocação recursiva destrutiva pelo modelo.** A execução da skill não pode disparar autoinvocação cross-turn da própria skill (ou de outra skill `disable-model-invocation: false`) em loop não-terminado por gate operador. **Não conta:** loop interno determinístico dentro do mesmo turn (releitura para consolidação, retry com cap, iteração `read → mutate → read` controlada) — cláusula visa dispatch do modelo entre invocações, não iteração intra-turn.

**Declara `true`** quando **qualquer** critério falha — em particular: ação direta cross-team (push automático sem gate, release publicada, mensagem externa enviada), ou risco de loop autoinvocado cross-turn pelo modelo.

### Aplicação retroativa às 9 skills

| Skill | Valor | Justificativa pelo critério |
|---|---|---|
| `/triage` | `false` | Push pós-commit no caminho-com-plano é gateado pelo enum `Commit` upstream (commit+push como unidade atômica). Push do step 0 cleanup (`git push origin --delete`) é opt-in explícito por candidato no `multiSelect` (default desmarcado → skip). Antes dos gates, mutação é local. Sem loop autoinvocado. |
| `/run-plan` | `false` (mantém) | Opera em worktree isolada, micro-commits locais. Push é gateado pelo enum `Publicar`. Sem loop. |
| `/new-adr` | `false` (mantém) | Cria 1 markdown local. Não commita. Sem push. Sem loop. |
| `/release` | `false` (mantém) | Bump local + commit local + tag local. **Push permanece manual** (operador executa `git push --follow-tags` fora da skill). Blast radius da skill é estritamente local. Sem loop. |
| `/debug` | `false` | Produz diagnóstico em texto na conversa. Não escreve código, não cria commit, não aplica instrumentação. Blast radius zero no working tree. Sem loop. |
| `/gen-tests` | `false` | Gera arquivo de teste local. Não commita. Sem push. Sem loop. |
| `/next` | `false` | Lê backlog, propõe candidatos. Movimentações em backlog são gateadas pelo enum `Movimentações`. Sem loop autoinvocado. |
| `/init-config` | `false` | Muta `CLAUDE.md` (escrita direta após coleta interativa role-a-role via `AskUserQuestion`), `.gitignore` (gate `Gitignore` per [ADR-005](ADR-005-modo-local-gitignored-roles.md) aplicado pelo modo `local` quando primeira escrita sob `.claude/local/` ocorre — fora desta skill), `.worktreeinclude` (escrita determinística sem `AskUserQuestion` per [ADR-018](ADR-018-replicacao-claude-em-modo-local-init-config.md) § Decisão — resultado óbvio, sem trade-off cross-team). Todas mutações no working tree do consumer; sem push, sem loop. Mutação cross-skill de config compartilhada **não** quebra "blast radius local" — fronteira do critério é cross-team, não cross-skill. |
| `/archive-plans` | `false` (mantém) | Preview-first + enum `Aplicar/Cancelar`. `git mv` local + commit local. Sem push. Sem loop. |

Resultado: **9 skills declaram `false`**, zero declaram `true`. Universo válido hoje — não há skill no toolkit cujo blast radius justifique `true`. Skill futura com `true` deve carregar justificativa explícita citando este ADR no próprio `SKILL.md` (paralelo à herança editorial de [ADR-017](ADR-017-cutucada-uniforme-descoberta-config-ausente.md) § Editorial inheritance). Convenção sustentada por `code-reviewer` e revisor humano em PRs introduzindo SKILL.md novo — sem enforcement mecânico.

## Consequências

### Benefícios

- **Drift editorial eliminado.** Cada `SKILL.md` declara explicitamente; reviewer humano ou `code-reviewer` flagra ausência em PR de skill nova.
- **Doutrina lível ao `design-reviewer`.** ADR-009 § Limitações ("doutrina não-escrita escapa") fechada nesse eixo. Reviewer aplica este ADR como referência mecânica.
- **Critério testável.** Aplicação retroativa documentada serve como template — qualquer leitor reproduz a classificação para skill futura.
- **3 casos cinza reconciliados.** `/triage` (push gateado), `/init-config` (mutação cross-skill local), `/release` (local até push manual) ficam sem ambiguidade.

### Trade-offs

- **+1 linha no frontmatter de cada SKILL.md** (5 skills hoje omissas ganham a linha). Custo trivial; alinha com ADR-003 § Trade-offs ("frontmatter mais carregado ... custo trivial; ganho em DRY compensa").
- **Sem enforcement mecânico.** Skill nova esquecendo a declaração cai no default da harness — herança é editorial (paralelo a [ADR-017](ADR-017-cutucada-uniforme-descoberta-config-ausente.md) § Editorial inheritance). Mitigação: convenção sustentada por `code-reviewer` em PRs introduzindo SKILL.md novo. Validação automática no CI lint (ADR-013) está fora-de-escopo desta iteração.
- **Cláusula "risco de autoinvocação" é hipotética hoje.** Nenhuma skill atual tem essa propriedade; cláusula custa 1 linha do critério mas fecha gap real (per finding do `design-reviewer`).

### Limitações

- **Default da harness sobre autoinvocação muda → reabrir.** Hoje a omissão cai num default fora do controle do plugin; declaração explícita evita ambiguidade enquanto o default for o que é.
- **Critério não cobre skill com sub-fluxo que muda blast radius dinamicamente** (skill que ora roda local, ora deploya). Não existe hoje; gatilho de revisão registrado.

## Alternativas consideradas

### (a) Cirúrgico — só declarar `false` nas 5 skills omissas, sem doutrina

Aplicar `disable-model-invocation: false` nas 5 skills omissas mantendo a doutrina informal no BACKLOG ## Concluídos linha 43. **Rejeitada por finding 2 do `design-reviewer`:**

- Doutrina-não-escrita escapa do free-read (ADR-009 § Limitações).
- Skill nova herda por imitação frágil — sem precedente claro, reviewer não tem âncora.
- Memory `feedback_adr_threshold_doctrine` aplica: "refinar/inverter critério documentado em philosophy.md/CLAUDE.md (mesmo parcial) → default ADR". O BACKLOG ## Concluídos é o critério parcial; generalizar pede ADR.

### (b) Doutrinário em CLAUDE.md sem ADR

Adicionar seção em CLAUDE.md com critério mecânico + aplicar nas 5 sem criar ADR. **Rejeitada por findings 1 e 2 do `design-reviewer`:**

- Wording em prosa única (sem § Alternativas, sem § Gatilhos) criou as 3 ambiguidades flagradas pelo finding 1 (casos `/triage`, `/init-config`, `/release`).
- Refinamento de critério parcial documentado é ADR-worthy per memory + precedente direto [ADR-013](ADR-013-ci-lint-minimo-no-build-runner.md) (formalização preventiva de CI lint mínimo) e [ADR-020](ADR-020-criterio-mecanico-admissao-warnings-pre-loop.md) (formalização preventiva de critério de admissão de warnings em `/run-plan`).
- Argumento "ADR contamina leveza da Onda 2" é frágil — Onda 1 fechou 3 ADRs em sequência sem comprometer cadência.

## Gatilhos de revisão

- **Skill nova violando o critério.** PR introduzindo `SKILL.md` que declara o valor "errado" pela leitura mecânica deste ADR → revisitar wording (ambiguidade real revelada pelo caso) ou tabela de aplicação (caso novo emerge).
- **Sub-fluxo onde blast radius muda dinamicamente.** Skill que ora roda local ora roda em deploy (hipotético `/deploy-preview` que pode rodar local-only-dry-run ou push-to-staging conforme arg). Critério atual classifica por máximo blast radius; revisitar se sub-fluxo seguro merecesse `false`.
- **Mudança na semântica default da harness sobre autoinvocação.** Hoje fora do controle do plugin; se default mudar para "sempre permite" ou para "campo é mandatório", semântica de "omissão = default" muda e a regra precisa ser reescrita.
- **Cláusula "risco de autoinvocação cross-turn" exercida concretamente.** Hoje hipotética; primeira skill nova que justificar `true` citando o critério 3 (não por blast radius cross-team) valida ou pede refinamento do wording. Sinal específico: classificador (autor da skill ou reviewer) precisa decidir se o loop é "cross-turn pelo modelo" (cobrindo) ou "intra-turn determinístico" (não cobrindo, per Decisão) — se a distinção exigir interpretação caso-a-caso, wording precisa reforço.

Não invertem a regra geral — refinam o critério se a aplicação revelar caso real não previsto.
