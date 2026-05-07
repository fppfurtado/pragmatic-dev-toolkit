# Plano — Modo local-gitignored para roles do path contract

## Contexto

Implementação de [ADR-005](../decisions/ADR-005-modo-local-gitignored-roles.md) — adicionar modo `local` ao path contract para `decisions_dir`, `backlog`, `plans_dir`. ADR estabelece a decisão; este plano implementa as mudanças mecânicas distribuídas em CLAUDE.md, ADR-003 (cross-ref), e prosa das skills afetadas.

**Linha do backlog:** plugin: reavaliar contrato `required` por role individualmente — `decisions_dir` e `backlog` têm semântica de artefato compartilhado (gitignore mata o ponto do ADR e do registro editorial), mas `plans_dir` faz sentido como artefato local-gitignored opcional. Não tratar como bloco único; cada role demanda análise distinta de fallback.

`.claude/` já consta no `.gitignore` raiz; sub-paths `.claude/local/<role>/` herdam o ignore automaticamente. Sem alteração no `.gitignore`.

## Resumo da mudança

Estender o path contract com sintaxe `paths.<role>: local` para `decisions_dir`, `backlog`, `plans_dir`. Quando declarado:

1. **Path resolution:** skill usa path em `.claude/local/<role>/` (ex.: `.claude/local/decisions/`, `.claude/local/BACKLOG.md`, `.claude/local/plans/<slug>.md`).
2. **Resolution protocol:** trilho paralelo aos 3 atuais — modo `local` é resolução final, sem ofertar canonical, sem informar+parar.
3. **Regra de não-referenciar:** quando role está em modo `local`, skills geradoras de commit/PR/branch metadata (`/triage`, `/run-plan`) não citam o artefato em modo local (ID do ADR, slug do plano, texto da linha do backlog) nas mensagens externas.

`test_command` permanece como condicional (ADR-003) — fora do escopo. `version_files`/`changelog` não aceitam modo `local` (release pessoal sem publicar é fora-de-escopo).

## Arquivos a alterar

### Bloco 1 — CLAUDE.md: schema do path contract e Resolution protocol {reviewer: code}

- `CLAUDE.md` (seção "Pragmatic Toolkit"): estender o exemplo YAML mostrando o novo modo:
  ```yaml
  paths:
    decisions_dir: local   # cria/lê em .claude/local/decisions/
    backlog: local         # cria/lê em .claude/local/BACKLOG.md
    plans_dir: local       # cria/lê em .claude/local/plans/
  ```
  Adicionar item ao "Schema and semantics" enumerando: `local` → "modo local-gitignored, skill cria/lê em `.claude/local/<role>/`, artefato não é commitado, commit/PR não referenciam (ADR-005)".
- `CLAUDE.md` (seção "Resolution protocol"): adicionar trilho paralelo aos 3 atuais — "Modo `local` declarado: skill usa path local-gitignored sem aplicar os 3 trilhos default (sem probe canonical, sem ofertar criação, sem informar+parar). Path concreto é `.claude/local/<role>/`. Skills geradoras de commit/PR não referenciam o artefato em mensagens — regra de não-referenciar (ADR-005)."

### Bloco 2 — ADR-003: cross-reference para ADR-005 {reviewer: doc}

- `docs/decisions/ADR-003-frontmatter-roles.md` (seção "Limitações" ou "Gatilhos de revisão"): adicionar nota apontando para ADR-005 como extensão — "Modo `local` no path contract ([ADR-005](ADR-005-modo-local-gitignored-roles.md)) introduz trilho paralelo aos 3 default behaviors descritos aqui; aplica-se quando operador declara `paths.<role>: local`."

### Bloco 3 — /triage: branch modo local + regra de não-referenciar {reviewer: code}

- `skills/triage/SKILL.md`:
  - Sub-fluxo de criação canonical (topo do arquivo): adicionar nota "Quando o role está declarado `local` no path contract, skill cria em `.claude/local/<role>/` em vez de path canonical, sem disparar enum de criação."
  - Step 4 ("Produzir os artefatos"): em **BACKLOG**, **Plano**, **ADR**: ramificar para path local quando role em modo `local`. Plano em modo `local` (`plans_dir: local`) → criado em `.claude/local/plans/<slug>.md`; campo `**Linha do backlog:**` continua presente no plano local (matching textual do `/run-plan` ainda funciona).
  - Step 6 ("Reportar, propor commit"): quando `plans_dir: local`, mensagem de commit não cita slug do plano nem texto da linha do backlog (artefatos locais). Push + commit unificado: o conteúdo do plano local não vai pro repo (gitignored), então o commit unificado só inclui artefatos canonical (se houver mudança de ADR-canonical, atualização de domain.md, etc.).

### Bloco 4 — /new-adr: branch modo local {reviewer: code}

- `skills/new-adr/SKILL.md`:
  - Topo (descrição): adicionar nota "Quando `decisions_dir: local`, skill cria ADR em `.claude/local/decisions/` em vez de path canonical."
  - Step 1 (listar ADRs): ler de `.claude/local/decisions/` em vez de `docs/decisions/` quando modo local.
  - Step 4 (criar arquivo): path destino segue modo declarado.
  - Validação final: reportar caminho criado mantém clareza sobre local vs canonical.

### Bloco 5 — /run-plan: branch modo local + regra de não-referenciar {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - Pré-condição 1 ("Plano existe"): aceitar `plans_dir: local` → procurar `.claude/local/plans/<slug>.md`.
  - Pré-condição 2 ("Estado git do plano"): em modo local, plano não é tracked pelo git (por design); pré-condição 2 vira no-op (não há "modificado/untracked" para checar — operador edita livremente).
  - Step 3.4 ("Registro em Concluídos"): em `backlog: local`, transição acontece em `.claude/local/BACKLOG.md`; matching textual e move idênticos.
  - Step 4 (micro-commits): mensagens de commit não citam slug do plano quando `plans_dir: local`. Conteúdo do commit cobre apenas mudanças nos arquivos canonical (mudanças via plano local que tocam código canonical são commitadas; o plano em si fica fora do diff).
  - Step 4.7 ("Sugestão de publicação"): em modo `local`, PR descrição via `gh pr create --fill` herda da última commit (que já segue regra de não-referenciar). Branch name (slug) é metadata externa — em modo local, branch usa nome neutro (ex.: `local-<timestamp>` ou aceita slug do plano se operador autorizou explicitamente). Ponto sutil — documentar trade-off em prosa.

### Bloco 6 — /next: branch modo local {reviewer: code}

- `skills/next/SKILL.md`:
  - Adicionar nota "Quando `backlog: local`, skill lê de `.claude/local/BACKLOG.md`."
  - Restante do fluxo (analisa, sugere top 3) idêntico — operação de leitura é agnóstica a path.

### Bloco 7 — /release: confirmação de não-aplicação {reviewer: code}

- `skills/release/SKILL.md`:
  - `## O que NÃO fazer`: adicionar entrada "Não aceitar modo `local` para `version_files` e `changelog` — release sem push é caso especial já coberto pela skill (release local até push manual), mas `version_files` e `changelog` precisam ser commitados/visíveis para o registro de versão fazer sentido. Se operador declarar `paths.version_files: local` ou `paths.changelog: local`, skill recusa antes de iniciar."

## Verificação end-to-end

- `grep -rn "local" CLAUDE.md | grep "paths\."` → exibe novo schema com `local` documentado.
- `grep -n "ADR-005\|local-gitignored" docs/decisions/ADR-003-frontmatter-roles.md` → cross-ref presente.
- `grep -n "modo local\|\.claude/local/" skills/triage/SKILL.md skills/new-adr/SKILL.md skills/run-plan/SKILL.md skills/next/SKILL.md` → branches "modo local" presentes nas skills afetadas.
- `grep -n "Não aceitar modo \`local\`" skills/release/SKILL.md` → entrada de recusa presente.
- Read das 4 skills afetadas: branch "modo local" descrito coerente, sem contradição com modo canonical.

## Verificação manual

Surface não-determinística: parsing do path contract YAML para detectar modo `local`. Cenários enumerados:

1. **Modo canonical (default, sem mudança):** projeto sem declaração de modo `local` continua operando como antes — `/triage`, `/new-adr`, `/run-plan`, `/next` usam paths canonical.
2. **Modo local em `decisions_dir`:** projeto declara `paths.decisions_dir: local`. Invocar `/new-adr "Título"` → ADR criado em `.claude/local/decisions/ADR-NNN-slug.md`. Confirmar: arquivo está no path local, `.gitignore` cobre via `.claude/`, `git status` não mostra o ADR.
3. **Modo local em `backlog`:** projeto declara `paths.backlog: local`. Invocar `/next` → skill lê `.claude/local/BACKLOG.md` (criar primeiro com cabeçalho mínimo, ou skill propõe criar). Confirmar: arquivo está no path local, gitignored.
4. **Modo local em `plans_dir`:** projeto declara `paths.plans_dir: local`. Invocar `/triage <intenção>` → caminho-com-plano cria plano em `.claude/local/plans/<slug>.md`. `/run-plan <slug>` lê do mesmo path. Confirmar: plano está no path local, /run-plan executa normalmente.
5. **Regra de não-referenciar (`plans_dir: local`):** após `/run-plan` em modo local, mensagem de commit final, descrição de PR, e nome de branch não citam slug do plano nem `**Linha do backlog:**`. Em modo canonical (sem `local`), as referências aparecem como hoje.
6. **Modo local + worktree:** `/run-plan` em `plans_dir: local` cria worktree replicando `.claude/` (já coberto pelo `.worktreeinclude`); plano local visível dentro da worktree.
7. **Recusa em `/release`:** projeto declara `paths.version_files: local` ou `paths.changelog: local`. Invocar `/release` → skill para com mensagem clara recusando o modo local para esses roles.
8. **Coexistência canonical + local não-suportada:** projeto que declara `decisions_dir: local` mas tem `docs/decisions/ADR-XXX-*.md` versionados → skill respeita declaração `local` (ignora canonical existente; operador é responsável pela inconsistência). Documentar trade-off em prosa.

Cenários 2-4 + 7 exigem projeto consumidor com a versão pós-merge instalada — validação efetiva acontece após próximo `/release`. Validação textual do plano + revisão das skills modificadas é o gate corrente.

## Notas operacionais

- Ordem de implementação: Bloco 1 (CLAUDE.md) primeiro estabelece o schema; Blocos 3-7 referenciam o schema. Bloco 2 (ADR-003 cross-ref) pode ir em qualquer momento. Sugestão: 1 → 2 → 3 → 4 → 5 → 6 → 7.
- Branch name em `/run-plan` modo local (Bloco 5, step 4.7) é trade-off explícito — slug do plano vira branch name por default. Se operador quer ocultar slug, pode renomear branch antes do push. Documentar e aceitar.
- Inconsistência canonical+local (cenário 8) é trade-off por design (ADR-005 § Limitações). Plano não introduz mecanismo de detecção/recusa.
- Replicação de `.claude/local/<role>/` em worktrees é automática via `.worktreeinclude` que já lista `.claude/`. Sem mudança em `.worktreeinclude`.
- Release deste batch (`/release`): após implementar, criar nova versão para que cache do plugin atualize e modo local funcione efetivamente em projetos consumidores.
