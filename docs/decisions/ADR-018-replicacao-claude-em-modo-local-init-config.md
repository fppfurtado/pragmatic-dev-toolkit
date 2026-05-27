# ADR-018: Replicação `.claude/` em modo local: responsabilidade proativa do `/init-config`

**Data:** 2026-05-11
**Status:** Aceito

## Origem

- **Investigação:** smoke-test do plugin v2.4.0 no projeto Java PJe (TJPA) 2026-05-11. Operador configurou modo local via `/init-config` e tentou rodar `/run-plan` em seguida — bateu em bloqueio surpresa per `skills/run-plan/SKILL.md:36` (worktree não enxerga `.claude/local/<role>/` porque consumer não declarou `.claude/` em `.worktreeinclude`). Item promovido pelo `/next` 2026-05-11 como top 1 — único item do BACKLOG com sinal real recente, não auto-marcado YAGNI. Registro detalhado no BACKLOG (commit `7f65605`).

## Contexto

`/run-plan` cria worktrees isoladas para execução de planos (`.worktrees/<slug>/`). Worktrees herdam conteúdo tracked do branch base, mas **não** carregam paths gitignored automaticamente. O plugin já tem mecanismo para replicar gitignored relevantes: `.worktreeinclude` (papel "plugin-internal" listado em `CLAUDE.md` → "The role contract"), lido por `/run-plan` step 1.2 e copia cada path listado para a worktree.

Quando consumer adota **modo local** (per [ADR-005](ADR-005-modo-local-gitignored-roles.md)), artefatos do plugin vão para `.claude/local/<role>/` (gitignored por design). Para `/run-plan` enxergar plano local, `.claude/local/` (ou `.claude/`) precisa estar em `.worktreeinclude`. Hoje:

- `/run-plan` SKILL.md:36 **detecta e bloqueia** quando modo local está ativo e `.worktreeinclude` não cobre `.claude/local/`. Mensagem orienta adicionar manualmente.
- [ADR-005](ADR-005-modo-local-gitignored-roles.md):48 e :75 afirmam que `.worktreeinclude` "já cobre `.claude/`" como se fosse default — afirmação válida **apenas** quando consumer declarou explicitamente. Consumer recém-configurado em modo local via `/init-config` **não** tem `.worktreeinclude` declarando `.claude/`.

**Sinal real (PJe 2026-05-11):** operador acabou de configurar `/init-config` e tentou primeiro `/run-plan` em seguida — UX foi: "ok, config gravado, próximo passo" → bloqueio surpresa pedindo ação manual em outro arquivo. Atrito é **previsível**: qualquer consumer que adote modo local via `/init-config` vai bater no mesmo gap.

**Doutrina relevante:**

- [ADR-005](ADR-005-modo-local-gitignored-roles.md) precedente: gate `Gitignore` no modo local. Quando skill detecta primeira escrita sob `.claude/local/<role>/` e `.gitignore` não cobre, skill propõe adicionar entrada. "Setup ao primeiro contato com modo local" é estratégia já estabelecida.
- [ADR-016](ADR-016-manter-block-gitignored-scripts-no-consumer.md) doutrina inversa: para padrão "arquivo gitignored como entrypoint operacional" (scripts `*.sh` do consumer), plugin **não** acomoda — consumer refatora workflow. **Não se aplica aqui** por critério mais preciso: ADR-016 rejeita acomodações que **subvertam sinal declarado** do consumer (ex.: liberar paths que o consumer gitignored). ADR-018 não subverte sinal — opera **na direção** da intenção declarada (consumer declarou `paths.<role>: local` → coerência implica `.claude/` replicado para worktree). Categorias distintas.
- [ADR-017](ADR-017-cutucada-uniforme-descoberta-config-ausente.md) paralelo: `/init-config` é a skill de setup proativo já estabelecida; faz sentido carregar a responsabilidade pelo invariante.

Alternativas avaliadas no `/triage` 2026-05-11 (todas descartadas exceto a escolhida — detalhes em § Alternativas consideradas):

- **(a) `/init-config` proativo** — ao gravar `paths.<role>: local`, skill garante que `.worktreeinclude` contém `.claude/`. Escolhida.
- **(b) `/run-plan` reativo com auto-recovery** — em vez de bloquear, oferecer enum para adicionar entrada na hora.
- **(c) Ambos** — defesa em camadas.
- **(d) Status quo** — bloquear, operador resolve manual.

**Dimensão organizacional levantada pelo operador:** `.worktreeinclude` pode ser tracked (default; equipe compartilha lista) ou gitignored (cada dev tem o seu — lista varia por dev em alguns projetos). Plugin permanece agnóstico — qualquer dos caminhos avaliados precisa funcionar independente do tracking.

## Decisão

**`/init-config` é responsável proativamente pela invariante** "se ≥1 role do consumer está em modo local, `.worktreeinclude` contém `.claude/`". Mecânica:

1. Skip se nenhuma role foi configurada como `local` no passo 3 da skill.
2. Probe `.worktreeinclude`:
   - **Ausente** → criar com header de comentário + linha `.claude/`.
   - **Presente sem `.claude/`** (regex `^\.claude(/|$)` nas linhas, falsos positivos aceitos pelo critério da [ADR-017](ADR-017-cutucada-uniforme-descoberta-config-ausente.md) "falso-positivo é mais barato que falso-negativo" em probes do plugin) → adicionar linha `.claude/` ao fim.
   - **Presente com `.claude/`** → skip silente (invariante já satisfeita).
3. Reportar no relatório final da skill.

`/run-plan` SKILL.md:36 permanece como **safety net** — bloqueia quando invariante violada (operador removeu manualmente, modo local declarado fora do `/init-config`, etc.).

Razões:

- **Alinhamento doutrinário com [ADR-005](ADR-005-modo-local-gitignored-roles.md):** mesma estratégia "skill cuida do setup ao primeiro contato com modo local" — paralelo direto com o gate `Gitignore`. `/init-config` já é a skill de setup; ampliar escopo é natural.
- **Sinal vem do consumer:** invariante só é aplicada quando consumer declarou `paths.<role>: local` — sem ativação espúria em consumers em modo canonical.
- **Mecânica determinística sem confirmação extra:** diferente do gate `Gitignore` (que confirma porque `.gitignore` codifica **política deliberada** do consumer sobre o que o repo ignora — adicionar entrada pode contradizer convenção da equipe), `.worktreeinclude` tem **semântica instrumental** ("replique isso na worktree") sem peso de política cross-team, mesmo quando tracked. Operação tem resultado óbvio (adicionar 1 linha com path que o consumer mesmo declarou indiretamente ao escolher modo local); cutucada `AskUserQuestion` seria fricção desnecessária.
- **`.worktreeinclude` tracked/gitignored é decisão do consumer** — plugin agnóstico. `/init-config` cria/atualiza independente do estado de tracking.
- **Não dispara em consumer em modo canonical** — passo 4.5 skip silente quando nenhuma role local. Plugin permanece zero-config para defaults.

## Consequências

### Benefícios

- Onboarding fluido: `/init-config` em modo local → `/run-plan` funciona sem ação manual entre as duas skills.
- Doutrina coerente com gate `Gitignore` do ADR-005 (mesma estratégia, escala 1:1 para outro arquivo de setup).
- Safety net preservado: `/run-plan` SKILL.md:36 continua cobrindo edge cases (operador removeu manualmente, modo local declarado fora do `/init-config`).
- Zero impacto em consumers em modo canonical (passo skip silente).

### Trade-offs

- **`/init-config` ganha escopo:** skill agora modifica 2 arquivos do consumer (`CLAUDE.md` para o bloco config + `.worktreeinclude` para invariante de worktree). Aceito — ambos são setup direto do plugin, dentro do espírito da skill.
- **Postura editorial não-reparativa do passo 1 ganha exceção controlada por critério positivo.** Skill não cria `CLAUDE.md`, não modifica `.gitignore` automaticamente, mas **cria/modifica `.worktreeinclude`**. Critério distintivo que rege a exceção (formalizado aqui para guiar decisões futuras): **`/init-config` modifica arquivos cujo único propósito é configurar mecânica do plugin** (`.worktreeinclude` é mecanismo interno per `CLAUDE.md` → "The role contract" tabela linha "plugin-internal"); **não modifica arquivos com propósito mais amplo que preexiste ao plugin** (`CLAUDE.md` é instrução geral ao Claude Code; `.gitignore` é política git do consumer). Esse critério rebate de antemão tentações análogas — ex.: declarar `test_command: make test` não implica criar `Makefile` (propósito mais amplo). Sub-critério complementar: a modificação só dispara quando é **invariante derivada matematicamente** de configuração que o operador acabou de declarar (declarar modo local → `.claude/` precisa estar replicado para worktree). Explicitar na seção `## O que NÃO fazer` da SKILL.md (exceção localizada, com critério explícito).

### Limitações

- **Falso-negativo benigno do probe regex `^\.claude(/|$)`:** consumer com `.worktreeinclude` listando apenas `.claude/local/` ou `.claude/local/plans/` (subpath) — invariante "consumer enxerga plano local" **já satisfeita** na prática, mas o regex (ancorado em `(/|$)` logo após `claude`) **não detecta**. Skill adicionaria linha `.claude/` redundante. Resultado: sem dano funcional (worktree replica `.claude/` que cobre `.claude/local/*`), apenas inelegância de uma linha extra. Aceito — falso-negativo conservativo (adicionar quando duvidoso) é mais barato do que regex mais complexo cobrindo subpaths. Falso-positivo real do regex é improvável (`.claudefoo/` **não** casa — `(/|$)` impede; cenário realístico de falso-positivo exigiria literal `.claude` sem subpath querendo significar outra coisa, irrealístico).
- **Não cobre consumer que declara modo local **manualmente** sem `/init-config`** (operador edita CLAUDE.md à mão). `/run-plan` SKILL.md:36 cobre via safety net (bloqueia + orienta). Aceito.
- **Não cobre operador que remove `.claude/` do `.worktreeinclude` entre `/init-config` e `/run-plan`** — caso edge; `/run-plan` SKILL.md:36 cobre. Operador roda `/init-config` novamente se desejar restaurar invariante; ou aceita o bloqueio do `/run-plan`.
- **Não aplica retroativamente em consumers em upgrade.** Consumers que adotaram modo local em versões do plugin anteriores a este ADR (bloco config gravado por `/init-config` antigo, sem o passo 4.5) não têm a invariante aplicada automaticamente — primeiro `/run-plan` pós-upgrade bate no safety net. Operador roda `/init-config` novamente (fluxo "Editar" do passo 2 da skill aceita re-run) **ou** adiciona `.claude/` manualmente ao `.worktreeinclude`. Sem migration step automática — escopo da SKILL não inclui detectar versões anteriores.

## Alternativas consideradas

### (b) `/run-plan` reativo com auto-recovery

Em vez de bloquear quando modo local + `.worktreeinclude` faltando, `/run-plan` oferece `AskUserQuestion` (header `Worktreeinclude`) com opções `Adicionar entry e prosseguir` / `Cancelar`. Mesma cobertura do (a) em termos de eliminar bloqueio surpresa, mas tratamento reativo (no momento da dor).

Descartada:

- **Atrito repetido em cada `/run-plan`** em modo local até operador resolver. Operador pode esquecer ou postergar; bloqueio aparece em cada invocação subsequente do `/run-plan` até virar reflexo.
- **`/run-plan` ganha responsabilidade de setup**, mas é skill executora (worktree → loop → gate); responsabilidade de setup pertence ao `/init-config`. Separação de responsabilidades fica melhor com (a).
- **Inverte ordem natural:** setup deveria preceder execução; (b) faz execução cobrir gap do setup.

### (c) Ambos (defesa em camadas)

(a) + (b). `/init-config` garante invariante proativamente; `/run-plan` oferece auto-recovery como fallback (em vez do bloqueio atual).

Descartada:

- **Over-engineering** para um problema com solução única (operador rodar `/init-config` antes do primeiro `/run-plan` em projeto novo). Caso edge de "invariante violada entre `/init-config` e `/run-plan`" é coberto pelo safety net atual (bloqueio) — operador roda `/init-config` novamente se desejar.
- **Mais código em 2 skills** sem proporcional ganho de UX. (a) cobre 99% dos casos; (b) seria belt-and-suspenders.
- Pode ser reabertura futura se sinal real surgir (caso edge virar recorrente).

### (d) Status quo (bloquear; operador resolve manual)

Comportamento atual. `/run-plan` SKILL.md:36 detecta e bloqueia.

Descartada:

- **Sinal real do PJe** demonstra atrito previsível. Manter status quo perpetua a fricção em todo consumer que adote modo local via `/init-config`.
- **ADR-005:48 e :75 ficam editorialmente errados** — afirmam `.worktreeinclude` "já cobre `.claude/`" como default, o que é falso em consumer recém-configurado.

## Gatilhos de revisão

- **≥2 operadores reportarem caso edge "invariante violada entre `/init-config` e `/run-plan`"** (ex.: operador removeu `.claude/` do `.worktreeinclude` manualmente e bateu no bloqueio do `/run-plan`) — reabrir alternativa (c) (defesa em camadas).
- **Falso-positivo do probe regex `^\.claude(/|$)`** atrapalhando um consumer real (`.claudefoo/` em uso legítimo) — reabrir critério de match.
- **Convenção de naming de `.worktreeinclude` mudar** (alias, formato novo) — re-confirmar que o probe continua válido.
- **Plugin ganhar segundo path canonical que precise replicação** (além de `.claude/local/`) — re-avaliar se `/init-config` é o lugar certo para gerenciar ou se vale extrair para skill própria de setup de worktree.
- **Operador reporta atrito com a exceção editorial** ("por que `/init-config` modifica `.worktreeinclude` mas não cria `CLAUDE.md` nem mexe em `.gitignore`?") — reavaliar consistência da postura editorial não-reparativa.

## Addendum (2026-05-27)

**Origem.** [ADR-032](ADR-032-skill-note-contexto-compartilhado.md) (2026-05-15) introduziu `.claude/local/NOTES.md` como store doutrinário fixo **non-role** — gravado pela skill `/note` em qualquer git repo, independente de role contract. Pressuposto original deste ADR de que `.claude/local/` só hospeda artefatos de role (`decisions/`, `BACKLOG.md`, `plans/`) deixou de valer: operador pode ter `NOTES.md` ativo **sem nenhuma role declarada como `local`**, e a invariante "`.claude/` em `.worktreeinclude`" passou a depender de skill fora do escopo do `/init-config`. Gap exposto em raw-chat 2026-05-27.

**Extensão.** `/note` se torna **segundo dispatcher** para a mesma invariante. Mecânica idêntica à linha `.claude/` da tabela composta do step 4.5 do `/init-config` SKILL.md (probe regex `^\.claude(/|$)`, 3 ramos exaustivos: criar arquivo com header + `.claude/` / adicionar linha / skip silente), operação silente e determinística, idempotente cross-skill. Concreto em `skills/note/SKILL.md` passo 1 ("Garantir store").

**Assimetria de trigger é deliberada.** `/init-config` step 4.5 dispara condicionalmente (≥1 role local declarada). `/note` passo 1 dispara **universalmente** (toda invocação) — porque o sinal de "preciso replicar `.claude/`" no `/note` é a própria invocação (existe NOTES.md a gravar). Não há perda de simetria: invariante é a mesma; `.claude/` cobre `.claude/local/<role>/` e `.claude/local/NOTES.md` simultaneamente.

**`/init-config` permanece dono no caminho setup-driven.** Step 4.5 inalterado; safety net do `/run-plan` SKILL.md:36 preservado para casos edge (`.claude/` removido manualmente do `.worktreeinclude` entre invocações).

**Gatilho de revisão acionado em duas ondas.** O gatilho original *"Plugin ganhar segundo path canonical que precise replicação (além de `.claude/local/`)"* foi acionado em duas ondas:

1. [ADR-030](ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md) (2026-05-14) adicionou `CLAUDE.md` como **path novo** ao `.worktreeinclude`, mesma skill dispatcher (`/init-config` step 4.5 tabela linha nova).
2. Este adendo adiciona `/note` como **dispatcher novo** para o path `.claude/` pré-existente.

Extração para skill própria de setup de worktree (`docs/procedures/worktree-replication-dispatch.md`) **avaliada e descartada** — dispatchers permanecem distribuídos por skill que tem o sinal de configuração na mão (init-config = role declaration; note = ad-hoc capture); idempotência cross-skill cobre conflito mecânico runtime; cross-ref textual no `/note` SKILL.md cobre drift editorial.

**Gatilho de revisão novo:** **4º dispatcher emergir** (além de `/init-config` × 2 paths + `/note`) → extrair pattern probe-and-add para `docs/procedures/worktree-replication-dispatch.md`. Paralelo direto com [ADR-029](ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md) § Gatilhos sobre cutucada-emitting skills.

**Justificativa de adendo (vs novo ADR sucessor parcial).** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) critério 5 (sucessor parcial) é defensável aqui, mas o **eixo de extensão é diferente** do precedente ADR-030. ADR-030 introduziu **novo path** (`CLAUDE.md`) coberto pelo **mesmo dispatcher** (`/init-config` step 4.5 tabela linha nova) → mecânica composta, novo ADR sucessor justificado. Este adendo introduz **novo dispatcher** (`/note` passo 1) para o **mesmo path** (`.claude/`) → mecânica replicada com decisão central do ADR-018 (probe regex + 3 ramos + idempotência) preservada intacta. ADR-034 critérios de adendo (4/4): decisão central intacta + sem nova categoria conceitual de artefato + sem restrição externa + caráter explicativo da extensão. Assimetria com ADR-030 é deliberada e amarrada ao critério ADR-034.
