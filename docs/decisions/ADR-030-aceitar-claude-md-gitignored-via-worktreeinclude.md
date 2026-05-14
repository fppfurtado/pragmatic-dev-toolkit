# ADR-030: `/init-config` aceita `CLAUDE.md` gitignored com replicação via `.worktreeinclude`

**Data:** 2026-05-14
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-016](ADR-016-manter-block-gitignored-scripts-no-consumer.md) (escopo literal: hooks/scripts) — postura "consumer sinaliza via `.gitignore`, plugin não subverte". `/init-config` step 3 estendeu informalmente essa postura para `CLAUDE.md` gitignored ("artefato compartilhável por design"); ADR-030 reverte parcialmente essa extrapolação, mantendo ADR-016 íntegro no escopo de hooks.
- **Investigação:** Sessão de `/triage` 2026-05-14. Operador relatou: "em alguns projetos em que trabalho, não cabe commit CLAUDE.md". Status quo: `/init-config` step 3 detecta gitignored `CLAUDE.md` e **para** — deixa operador sem caminho institucional. Resolution protocol passos 2 e 4 já operam textualmente (sem checagem de git), mas memoização grava em arquivo que não propaga + worktrees do `/run-plan` não enxergam `CLAUDE.md`.

## Contexto

`/init-config` cobre setup do bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md` do consumidor. Step 3 atual (`skills/init-config/SKILL.md:27-31`) detecta `CLAUDE.md` gitignored via `git check-ignore -q CLAUDE.md` e para com mensagem alinhada a uma **extrapolação** da doutrina de ADR-016: "CLAUDE.md é artefato compartilhável por design; plugin não prescreve workaround". Essa extrapolação fecha o ciclo institucional do plugin para projetos onde política organizacional não permite commit de `CLAUDE.md`.

Casos reais onde política impede commit de `CLAUDE.md`:

- Projeto cujo `.gitignore` corporativo cobre `CLAUDE.md` por padrão (template org-wide).
- Equipe que considera `CLAUDE.md` instrução individual ao agent (cada dev mantém o seu), análogo a `.vscode/settings.json` pessoal.

Doutrina relevante:

- **ADR-016 leitura literal** (hooks): "sinal vem do consumer via `.gitignore`, plugin não subverte". Aplicada a `CLAUDE.md`, a doutrina **valida** o gitignore do consumer — i.e., `/init-config` deveria operar **dentro** da decisão do consumer, não recusar.
- **ADR-016 extrapolação atual** (em `/init-config` step 3): "CLAUDE.md é compartilhável por design; reconsidere o gitignore". Vai além do escopo original de ADR-016 (sobre hooks bloqueando edits em paths gitignored). Pressiona o consumer contra sua própria política.
- **[ADR-018](ADR-018-replicacao-claude-em-modo-local-init-config.md) critério distintivo**: `/init-config` modifica arquivos cujo único propósito é mecânica do plugin (`.worktreeinclude`); não modifica arquivos com propósito mais amplo que preexiste ao plugin. Preservado por ADR-030: replicação via `.worktreeinclude` (plugin-internal) não viola; modificar `CLAUDE.md` já é caso preexistente do `/init-config` (passo 4 grava o bloco config), tolerado por ADR-018 como "modifica existente, não cria".
- **[ADR-005](ADR-005-modo-local-gitignored-roles.md) modo local**: precedente de "skill cuida do setup ao primeiro contato com sinal declarado pelo operador". ADR-030 segue o mesmo padrão para gitignore de `CLAUDE.md` (sinal declarado → plugin opera dentro).

Lacuna identificada: o gap entre "Resolution protocol passos 2/4 já leem/gravam textualmente em `CLAUDE.md` gitignored" e "`/init-config` step 3 recusa antes de chegar a esses passos" é cosmético do ponto de vista mecânico (skills downstream funcionam se o operador conseguir bootstrap manual); doutrinário do ponto de vista da experiência (operador esbarra na recusa sem caminho institucional para seguir).

Alternativas avaliadas no `/triage` (detalhes em § Alternativas consideradas):

- **(c) Aceitar+replicar** — escolhida.
- **(a) Ler `CLAUDE.local.md`** — descartada por escopo + complexidade adicional sem ganho proporcional ao caso primário.
- **(b) Modo `local` para o bloco config** — descartada por paradoxo de bootstrap.

## Decisão

**`/init-config` passa a aceitar `CLAUDE.md` gitignored e a garantir replicação via `.worktreeinclude`. Step 3 deixa de parar; prossegue para steps 4-5, sinalizando para o step 4.5 incluir `CLAUDE.md` na lista de paths a replicar quando `.worktreeinclude` é tocado.**

Mecânica:

1. **Step 3 reformulado:** `git check-ignore -q CLAUDE.md` retorna zero (gitignored) → **registrar flag interna** `claude_md_gitignored = true` para o step 4.5; prosseguir normalmente. Sem mensagem de parada; comportamento canonical preservado para `CLAUDE.md` tracked.

2. **Step 4.5 estendido:** critério de disparo (hoje "≥1 role configurada como `local`") ganha cláusula OR: "OR `claude_md_gitignored = true`". Lista de paths a garantir em `.worktreeinclude` passa a ser composta:
   - `.claude/` quando ≥1 role local.
   - `CLAUDE.md` quando `claude_md_gitignored = true`.
   - Cada adição é independente e idempotente — testa sua condição de disparo isoladamente; presença prévia da linha (de run anterior) é skip silente. Step 4.5 nunca remove linhas — limpeza é manual (paralelo com `.claude/` per [ADR-018](ADR-018-replicacao-claude-em-modo-local-init-config.md) § Limitações).
   - Probe concreto: `grep -qE '^CLAUDE\.md$' .worktreeinclude` retorna não-zero → adicionar `CLAUDE.md` ao fim do arquivo. Simetria editorial com ADR-018 (que usa `grep -qE "^\.claude(/|$)"` no probe análogo). Falso-negativo benigno aceito por paralelo direto: regex simples + linha redundante = sem dano funcional (replicação de path já replicado por entrada anterior é no-op real).

3. **Resolution protocol inalterado:** passos 2 (consultar marker em `CLAUDE.md`) e 4 (memoização one-shot) já operam textualmente. `/run-plan` em worktree fresca agora enxerga `CLAUDE.md` replicado, mantendo coerência com o estado tracked.

4. **Step 5 emite linha adicional quando `claude_md_gitignored = true`:** `CLAUDE.md gitignored detectado — replicação garantida via .worktreeinclude por ADR-030.` Operador entende a aceitação como ato deliberado da skill, não como falha silente. Substitui a mensagem doutrinária revogada do step 3 atual.

Razões:

- **Alinhamento literal com ADR-016:** "sinal vem do consumer via `.gitignore`". `/init-config` honra o sinal em vez de pressionar o consumer.
- **Mesma estratégia de ADR-018:** "skill cuida do setup ao primeiro contato com sinal declarado pelo operador". `.worktreeinclude` é mecanismo plugin-internal (preserva critério distintivo de ADR-018); `CLAUDE.md` já é modificado pelo `/init-config` no fluxo canonical (escrita do bloco), critério "modifica existente, não cria" inalterado.
- **Postura editorial não-reparativa preservada:** plugin segue sem criar `CLAUDE.md` ausente (step 1 inalterado), sem modificar `.gitignore` automaticamente (gate `Gitignore` do [ADR-005](ADR-005-modo-local-gitignored-roles.md) continua sendo o único toque), sem reescrever bloco config malformado.
- **Resolve limitação documentada de [ADR-029](ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md) § Limitações:** cutucada de descoberta em projeto com `CLAUDE.md` gitignored sem bloco passa a ter destino útil (operador roda `/init-config`, que agora opera; antes recusava).

## Consequências

### Benefícios

- Operador em projeto com `CLAUDE.md` gitignored ganha caminho institucional — `/init-config` opera, Resolution protocol passos 2/4 funcionais, worktrees do `/run-plan` enxergam o config block via replicação.
- Doutrina coerente com ADR-016 leitura literal + padrão de ADR-018 (skill de setup garante invariante).
- Limitação de ADR-029 § Limitações dissolve (cutucada → `/init-config` → setup completo, sem recusa intermediária).
- Zero impacto em consumers com `CLAUDE.md` tracked — step 3 segue silente quando gitignored não detectado; step 4.5 segue só disparando quando há sinal (role local OR `CLAUDE.md` gitignored).

### Trade-offs

- **Extrapolação atual de ADR-016 em `/init-config` step 3 é parcialmente revertida.** Mensagem doutrinária ("reconsidere o gitignore") desaparece; consumer não é mais pressionado a justificar a política. Aceito — pressão doutrinária via mensagem da skill era atrito sem caminho construtivo. ADR-016 literal permanece íntegro no escopo de hooks/scripts.
- **`/init-config` agora replica `CLAUDE.md` via `.worktreeinclude`** quando gitignored — invariante extra para manter. Aceito sob mesmo critério de ADR-018 (sinal declarado pelo operador → invariante derivada matematicamente).
- **Operador que muda política mid-stream** (ex.: começa gitignored, depois decide tracked) precisa rodar `/init-config` novamente para a invariante refletir o novo estado — passo 4.5 é idempotente mas não detecta remoção de `CLAUDE.md` do `.gitignore` (regra inversa não disparada). Aceito como caso edge; operador remove manualmente a linha `CLAUDE.md` do `.worktreeinclude` se desejar limpar.

### Limitações

- **Sem safety net no `/run-plan` para o caso "operador remove `CLAUDE.md` do `.worktreeinclude` manualmente"** (ao contrário de `.claude/local/` que tem o detect-e-bloqueia em `skills/run-plan/SKILL.md:36`). Resolution protocol passo 2 falha silente — worktree não enxerga `CLAUDE.md` → marker ausente → memoização passada não vista → ask-on-demand per role. Aceito — operador roda `/init-config` novamente se desejar restaurar (`Editar` no fluxo do step 2). Reabrir se sinal real surgir (gatilho de revisão registrado).
- **`.worktreeinclude` listando `CLAUDE.md` é ruído moderado em modo canonical posterior.** Se consumer remover `CLAUDE.md` do `.gitignore` futuramente (decisão organizacional muda), o listing permanece. Sem dano funcional (replicação de arquivo já tracked é no-op real); operador limpa manualmente. Aceito.
- **Não aplica retroativamente em consumers em upgrade.** Consumers com `CLAUDE.md` gitignored e `/init-config` em versão prévia (que recusava) precisam re-rodar `/init-config` para que step 4.5 estendido aplique. Sem migration automática — escopo de SKILL.md per release. Paralelo direto com [ADR-018](ADR-018-replicacao-claude-em-modo-local-init-config.md) § Limitações (mesma redação literal): primeiro `/run-plan` pós-upgrade em consumer com gap não-aplicado cai em Resolution protocol passo 3 (ask-on-demand per role); operador roda `/init-config` para restaurar invariante ou aceita o ask-on-demand. Safety net no `/run-plan` análogo ao de `.claude/local/` (`skills/run-plan/SKILL.md:36`) descartado como YAGNI — caso de upgrade é único por consumer, sem dano funcional além de fricção transitória; sinal real de recorrência reabre alternativa.

## Alternativas consideradas

### (a) Ler `CLAUDE.local.md` via Resolution protocol passo 2

Resolution protocol passo 2 passa a também ler `CLAUDE.local.md` (convenção nativa do Claude Code para complemento local-gitignored). `CLAUDE.md` tracked permanece prioritário; `CLAUDE.local.md` adiciona/sobrescreve por dev.

Descartada:

- **Nova superfície de leitura.** Plugin ganha segundo arquivo de config com semântica de precedência/merge a decidir (merge by key vs override total). Escopo significativamente maior.
- **Caso primário do operador é "CLAUDE.md inteiramente per-dev"**, não "tracked + override pessoal". Cobertura de (c) é direta no caso primário; (a) cobre caso secundário com mais complexidade.
- **Critério distintivo de ADR-018** ficaria pressionado: plugin lendo de arquivo Claude Code-native amplia escopo do que o plugin entende como "input". (c) preserva: plugin só lê de `CLAUDE.md` (status quo) + modifica plugin-internal `.worktreeinclude`.
- Reabertura plausível se aparecer caso real de "CLAUDE.md compartilhado + override pessoal por dev em bloco config" — gatilho de revisão registrado.

### (b) Modo `local` para o próprio bloco config

Estender `paths.config: local` (ou similar) para declarar que o bloco config vive em arquivo gitignored.

Descartada:

- **Paradoxo de bootstrap.** Config local declarada em arquivo que o plugin não sabe onde encontrar — o sinal de "configuração está em outro lugar" precisa estar em algum lugar conhecido a priori.
- Levantada e rebatida pelo próprio operador na sessão `/triage`.

### Status quo (recusar e parar)

Comportamento atual. Operador resolve no consumer (descomenta `CLAUDE.md` do `.gitignore`).

Descartada:

- **Sinal real do operador.** Política organizacional do consumer não é negociável pelo plugin — pressão doutrinária via mensagem não tem efeito construtivo.
- **Extrapolação de ADR-016** que sustenta a recusa é frágil — escopo literal de ADR-016 é hooks/scripts, não `CLAUDE.md`.

## Gatilhos de revisão

- **Sinal real de "CLAUDE.md compartilhável + override pessoal por dev em bloco config"** (caso primário de alternativa (a)) → reabrir para considerar leitura de `CLAUDE.local.md` como caminho aditivo a este ADR.
- **Operador remove `CLAUDE.md` do `.worktreeinclude` manualmente** e bate em falha silente no `/run-plan` ≥2 vezes → considerar safety net no `/run-plan` análogo a `skills/run-plan/SKILL.md:36`.
- **Convenção do `.worktreeinclude` mudar** (alias, formato novo) → re-confirmar probe.
- **Operador reporta atrito com a inversão** (espera mensagem doutrinária e fica confuso com aceitação silenciosa) → revisar redação do relatório do `/init-config` step 5 para deixar a aceitação explícita.
