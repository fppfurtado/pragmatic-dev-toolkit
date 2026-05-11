# Plano — `/init-config` garante `.claude/` em `.worktreeinclude` quando modo local

## Contexto

**Linha do backlog:** /run-plan + modo local: artefatos sob `.claude/local/<role>/` (plano, ADRs, backlog) só são replicados para worktree fresca se consumer declarou `.claude/local/` (ou `.claude/`) em `.worktreeinclude`. Hoje `/run-plan` SKILL.md:36 detecta e **bloqueia** com instrução de adicionar manualmente — UX ruim quando operador acabou de configurar local mode via `/init-config`. [ADR-005](docs/decisions/ADR-005-modo-local-gitignored-roles.md):48 e :75 afirmam que `.worktreeinclude` "já cobre `.claude/`" como se fosse default — válido só quando consumer declarou explicitamente. Direção: `/init-config` ao gravar `paths.<role>: local` oferece também adicionar `.claude/local/` ao `.worktreeinclude` (proativo, paralelo com gate `Gitignore` do ADR-005); OU `/run-plan` em vez de bloquear oferece auto-recovery (adicionar entry + retry via enum). Adjacente ao plano `init-config-wizard` (v1) mas decisão de design separada (proatividade vs reatividade; escopo `.claude/` vs `.claude/local/`; quem é responsável — `/init-config` ou `/run-plan`). Origem: descoberta em smoke-test no PJe 2026-05-11.

Gatilho atendido pelo smoke-test PJe 2026-05-11: operador configurou modo local via `/init-config`, tentou `/run-plan` e bateu em bloqueio per SKILL.md:36 (worktree não veria o plano local). Item promovido pelo `/next` 2026-05-11 como top 1 — único item do BACKLOG com sinal real recente, não auto-marcado YAGNI.

**Decisão de design tomada no `/triage` 2026-05-11**: `/init-config` proativo é responsável (alternativa (a) de 3 caminhos avaliados). Alternativas descartadas:

- **(b) `/run-plan` reativo com auto-recovery** — atrito repetido em cada `/run-plan` em modo local até operador resolver.
- **(c) Ambos (defesa em camadas)** — over-engineering; problema tem solução única (operador roda `/init-config` antes do primeiro `/run-plan`).
- **(d) Status quo** — descartada pelo sinal real do PJe.

**ADR delegada via `/new-adr`** durante o `/triage` formaliza a política. Este plano implementa.

**ADRs vizinhos:**

- [ADR-005](../decisions/ADR-005-modo-local-gitignored-roles.md) — modo local. Precedente direto: gate `Gitignore` no ADR-005 usa mesma estratégia ("skill cuida do setup ao primeiro contato com modo local"). Item editorial: linhas 48 e 75 afirmam `.worktreeinclude` "já cobre `.claude/`" como se fosse default; precisa ressignificar pelo Bloco 2 abaixo.
- [ADR-016](../decisions/ADR-016-manter-block-gitignored-scripts-no-consumer.md) — vizinho doutrinário. Trata pattern "arquivo gitignored como entrypoint operacional" como responsabilidade do consumer (não do plugin). O caso atual é **diferente**: `.worktreeinclude` é mecanismo interno do plugin para setup de worktree; está dentro do escopo do `/init-config` por design (setup wizard).
- [ADR-017](../decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) — paralelo: precedente de "setup proativo via skill própria" + integração com Resolution protocol.

**Dimensão levantada pelo operador no `/next` — `.worktreeinclude` viável gitignored:** decisão organizacional do consumer. Plugin permanece agnóstico — `/init-config` cria/atualiza o arquivo independente de tracked/gitignored. Útil quando a lista varia por dev (paths de fixtures locais, etc.). Plugin não força tracking. Nota informativa em `docs/install.md` (Bloco 3).

## Resumo da mudança

Estender `/init-config` com novo passo 4.5 (entre o atual passo 4 "Compor e gravar" e o atual passo 5 "Informar interações pendentes") para garantir a invariante:

> Se operador escolheu `local` para ≥1 role, `.worktreeinclude` do consumer contém `.claude/`.

Mecânica determinística (sem cutucada — operação barata, resultado óbvio, sem decisão organizacional cross-team a confirmar):

1. Skip se nenhuma role foi configurada como `local` (passo 3).
2. Probe `.worktreeinclude`:
   - **Ausente** → criar com header de comentário + linha `.claude/`.
   - **Presente, sem `.claude/`** (regex `^\.claude(/|$)`) → adicionar linha `.claude/` ao fim do arquivo.
   - **Presente com `.claude/`** → skip silente (invariante já satisfeita).
3. Reportar no relatório final (passo 6 do skill): `.worktreeinclude criado/atualizado em <path>; .claude/ replicado nas worktrees subsequentes do /run-plan.`

**Por que sem `AskUserQuestion` no passo 4.5** (diferente do gate `Gitignore` do ADR-005): `.worktreeinclude` é mecanismo interno do plugin (sem semântica organizacional cross-team como `.gitignore`); decisão de tracking permanece do operador (que pode gitignorar o arquivo depois se quiser). Não há trade-off cross-team a confirmar.

**Implicação no atual passo 5 da skill:** o aviso "Atenção: `/run-plan` em modo local exige `.claude/local/` replicado..." (introduzido no plano `init-config-wizard`) deixa de ser válido — a invariante agora é garantida pelo passo 4.5. Passo 5 reformulado para reportar a mudança feita ao `.worktreeinclude`.

**Implicação no `## O que NÃO fazer` da skill:** linha "Não modificar `.worktreeinclude` automaticamente" deixa de valer — diretriz invertida por esta política.

**Implicação no `/run-plan`:** SKILL.md:36 (bloqueio quando consumer está em modo local e `.worktreeinclude` não cobre `.claude/local/`) **permanece** como safety net — invariante deveria estar satisfeita pelo `/init-config`, mas o bloqueio cobre o caso "operador removeu manualmente entre `/init-config` e `/run-plan`" ou "modo local declarado manualmente sem `/init-config`".

## Arquivos a alterar

### Bloco 1 — estender `/init-config` {reviewer: code}

- `skills/init-config/SKILL.md`:
  - Adicionar passo 4.5 "Garantir `.claude/` em `.worktreeinclude`" entre os atuais passos 4 e 5, com a mecânica determinística descrita acima.
  - **Critério de disparo do passo 4.5:** ≥1 role configurada como `local` no passo 3, **independente do caminho de entrada do passo 2** (bloco ausente → gravar novo; bloco presente + `Editar` → gravar atualizado). Ou seja, re-execução em modo `Editar` que mantenha local também dispara o passo 4.5; passo 4.5 com `.claude/` já presente faz skip silente (idempotente).
  - Reformular passo 5 — substituir aviso "Atenção: `/run-plan` em modo local exige..." por "Confirmado: `.worktreeinclude` garante replicação de `.claude/` nas worktrees do `/run-plan`. Operação feita no passo 4.5."
  - Atualizar `## O que NÃO fazer`: remover "Não modificar `.worktreeinclude` automaticamente"; substituir por explicação curta de que o passo 4.5 é exceção localizada à postura editorial não-reparativa do passo 1, **governada pelo critério positivo de ADR-018** (modificar arquivos cujo único propósito é configurar mecânica do plugin; preservar arquivos com propósito mais amplo como `CLAUDE.md` e `.gitignore`).

### Bloco 2 — atualização editorial ADR-005 {reviewer: doc}

- `docs/decisions/ADR-005-modo-local-gitignored-roles.md` linha 48 (parte da § Decisão): reformular "Worktree replication via `.worktreeinclude` já cobre `.claude/`" para "Worktree replication via `.worktreeinclude` é garantida proativamente por `/init-config` em modo local (per [ADR-018](ADR-018-replicacao-claude-em-modo-local-init-config.md)); consumer-only `.worktreeinclude` permanece válido (skill detecta cobertura existente e faz skip silente)".
- `docs/decisions/ADR-005-modo-local-gitignored-roles.md` linha 75 (parte de § Benefícios — bullet "sem nova mecânica"): **reformular o bullet inteiro** (não substituição cirúrgica) — a afirmação original "sem nova mecânica" deixa de valer com ADR-018 (que **introduz** mecânica explícita no passo 4.5 do `/init-config`). Texto novo: "Worktree replication coberta por `.worktreeinclude` — mecânica de garantia formalizada em [ADR-018](ADR-018-replicacao-claude-em-modo-local-init-config.md), com fallback de safety net no `/run-plan` SKILL.md:36."
- ADR-005 está em Status `Proposto` (não-Aceito) — modificação editorial menos invasiva doutrinariamente do que se fosse Aceito; ainda assim, edits são **adições/substituições controladas referenciando ADR-018**, preservando a estrutura do ADR-005.

### Bloco 3 — nota em docs/install.md {reviewer: doc}

- `docs/install.md`: adicionar 1 parágrafo na seção "Pré-requisitos no projeto consumidor" sobre `.worktreeinclude` viável como gitignored. Texto:

  > `.worktreeinclude` pode ser tracked (default; equipe compartilha lista) ou gitignored (cada dev tem o seu, útil quando lista varia por dev — paths de fixtures locais, credenciais por máquina, etc.). Plugin permanece agnóstico — em modo local, `/init-config` cria/atualiza o arquivo independente do estado de tracking. **Em modo canonical (nenhum role declarado `local`), `/init-config` não toca `.worktreeinclude`.** `/run-plan` lê e replica o conteúdo na worktree fresca.

## Verificação end-to-end

Toolkit sem suite (`test_command: null` per config próprio). Inspeção textual:

1. `grep -n "Garantir .claude" skills/init-config/SKILL.md` — header do passo 4.5 presente.
2. `grep -c "Não modificar .worktreeinclude" skills/init-config/SKILL.md` — diretriz invertida (0 ocorrências do bullet antigo).
3. `grep -c "ADR-018" docs/decisions/ADR-005-modo-local-gitignored-roles.md` — referência cruzada (≥1).
4. `grep -n "tracked (default) ou gitignored" docs/install.md` — nota presente.

## Verificação manual

Skill nova extensão com efeito determinístico — cenários enumerados:

1. **Operador escolhe `local` para 1 role; `.worktreeinclude` ausente** — esperado: `/init-config` cria `.worktreeinclude` com header de comentário + linha `.claude/`. Reporta caminho.
2. **Operador escolhe `local` para 1 role; `.worktreeinclude` presente listando outros paths sem `.claude/`** — esperado: `/init-config` adiciona linha `.claude/` ao fim. Reporta path:linha.
3. **Operador escolhe `local` para 1 role; `.worktreeinclude` presente já listando `.claude/`** — esperado: skip silente. Invariante satisfeita; relatório final menciona "já satisfeita".
4. **Operador escolhe `local` para 1 role; `.worktreeinclude` listando `.claude/local/` (sub-path)** — esperado: skip silente. Regex `^\.claude(/|$)` cobre.
5. **Operador escolhe `canonical` para todas as roles (nenhum `local`)** — esperado: passo 4.5 skip silente (sem invariante a garantir). `.worktreeinclude` não tocado.
6. **`.worktreeinclude` gitignored E operador escolheu `local`** — esperado: `/init-config` cria/atualiza o arquivo normalmente (probe não checa tracked status). `git status` subsequente não mostra `.worktreeinclude` modificado (gitignored).
7. **`/run-plan` subsequente em consumer pós-`/init-config` com local mode** — esperado: SKILL.md:36 não mais bloqueia (invariante satisfeita); worktree fresca replica `.claude/`; plano local visível na worktree.
8. **Re-invocação de `/init-config` (cenário 3 do plano init-config-wizard) com local mode preservado** — esperado: passo 4.5 detecta `.claude/` presente, skip silente.
9. **Operador removeu `.claude/` do `.worktreeinclude` entre `/init-config` e `/run-plan`** — esperado: `/run-plan` cai no bloqueio de SKILL.md:36 (safety net preservado). Operador roda `/init-config` novamente para restaurar invariante.
10. **Modo local declarado manualmente sem `/init-config`** (operador editou `CLAUDE.md` à mão) — esperado: `/run-plan` cai no bloqueio de SKILL.md:36 (safety net cobre este caminho também, per ADR-018 § Limitações). Operador roda `/init-config` em modo `Editar` (passo 2) ou adiciona `.claude/` manualmente ao `.worktreeinclude`.
11. **Falso-negativo benigno do regex** — consumer com `.worktreeinclude` listando apenas `.claude/local/` (subpath) — esperado: passo 4.5 adiciona linha `.claude/` raso (regex não detecta subpath). Resultado: linha redundante sem dano funcional (per ADR-018 § Limitações). Relatório do passo 4.5 menciona condicionalmente a possibilidade ("Adicionei `.claude/`; caso `.claude/local/<sub>` já estivesse listado, a adição é redundante per ADR-018").

## Notas operacionais

- **Ordem dos blocos importa.** Bloco 1 (extensão da skill) é a mudança central. Bloco 2 (ADR-005) referencia ADR-018 — depende do ADR existir tracked em HEAD. Bloco 3 (install.md) é editorial-independente.
- **Pré-condição editorial:** ADR-018 (`docs/decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md`) deve estar tracked em HEAD **antes** do `/run-plan` deste plano iniciar. ADR foi criado durante o `/triage` que produziu este plano; o commit unificado de `/triage` step 6 garante isso (plano + ADR-018 + qualquer edit de BACKLOG entram juntos no commit que precede o `/run-plan`).
- **Idioma:** prosa em PT-BR (canonical do toolkit). Frontmatter keys + paths em inglês.
- **Sem `AskUserQuestion` no passo 4.5.** Operação determinística sem trade-off cross-team a confirmar — `.worktreeinclude` é mecanismo do plugin, não artefato organizacional como `.gitignore`. Diferente do gate `Gitignore` do ADR-005 (que confirma porque `.gitignore` é compartilhado entre devs por design).
- **Safety net do `/run-plan` preservado.** SKILL.md:36 continua bloqueando se invariante violada — cobre o caso edge "operador removeu `.claude/` do `.worktreeinclude` manualmente" ou "modo local declarado fora do `/init-config`".
