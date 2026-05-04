# Corrigir descrição dos reviewers e adicionar /release no README

## Contexto

Auditoria da documentação contra o estado atual do plugin (v1.12.0) revelou duas frentes de drift:

1. **Reviewers `qa-reviewer` e `security-reviewer` descritos como "project-level only"** em quatro pontos da doc (`CLAUDE.md`, `docs/philosophy.md`, `skills/run-plan/SKILL.md`). Os agents existem em `agents/qa-reviewer.md` e `agents/security-reviewer.md` desde `44b442b feat(agents): add generic qa-reviewer and security-reviewer`. O design real, registrado em `docs/plans/qa-and-security-reviewers.md:133`, é: plugin entrega baseline genérico shipado; projeto consumidor pode sombrear via `.claude/agents/<nome>.md` (precedência convenção Claude Code). A doc atual contradiz esse design e contradiz o próprio `CLAUDE.md:16`, que lista os três reviewers como agents do plugin.

2. **`/release` ausente do `README.md`**. A skill chegou na v1.11.0 e está descrita em `plugin.json`, `CLAUDE.md` e `docs/install.md`, mas a tabela "O que vem" no README ficou para trás.

## Resumo da mudança

Alinhar a doc à realidade dos reviewers shipados (com override project-level opcional via convenção Claude Code) em quatro pontos, e adicionar a linha de `/release` na tabela de componentes do README.

## Arquivos a alterar

### Bloco 1 — reviewers shipados + override project-level

- `CLAUDE.md`:
  - **Linha 29** (seção "The role contract"): trocar "Plugin-internal: `.worktreeinclude` (consumed by `/run-plan`) and project-level `.claude/agents/qa-reviewer.md` / `security-reviewer.md` follow Claude Code conventions." por nota que cite os reviewers como agents shipados pelo plugin (já listados em `Plugin layout`), com override project-level opcional via `.claude/agents/<nome>.md` (convenção Claude Code).
  - **Linha 49** (descrição do `/run-plan` no Skill workflow contract): trocar "(default `code-reviewer`; `qa`/`security` resolve to project-level agents in `.claude/agents/`; multiple profiles aggregate reports)" por descrição que reflita resolução por nome do agent — baseline shipado pelo plugin, com override project-level opcional.

- `docs/philosophy.md`:
  - **Linha 37** (tabela do path contract, entrada "(convenção Claude Code)"): reescrever para descrever os reviewers `qa-reviewer`/`security-reviewer` como shipados pelo plugin (baseline genérico), com `.claude/agents/<nome>.md` no projeto consumidor agindo como **override shadowing** (convenção Claude Code) quando o projeto tem rubrica enriquecida (ex.: RNs específicas). Manter a referência a `/run-plan` invocando esses agents quando o bloco anota `{reviewer: qa}` / `{reviewer: security}`.

- `skills/run-plan/SKILL.md`:
  - **Linha 61** (passo 3, escolha de revisor): trocar "{reviewer: qa} ou {reviewer: security} → agent project-level correspondente em `.claude/agents/<role>-reviewer.md`." por descrição alinhada ao baseline shipado + override project-level (mesma forma do `code-reviewer` na linha 60: "incluído neste plugin"; pode-se acrescentar nota curta sobre override em `.claude/agents/<nome>.md`).

### Bloco 2 — `/release` na tabela do README

- `README.md`:
  - Adicionar linha em `## O que vem` (entre `/gen-tests-python` e `code-reviewer`) descrevendo `/release` como skill que faz bump de versão em `version_files`, escreve entrada em `changelog`, commit unificado e tag anotada local; sem push (operador publica). Manter o tom curto da tabela.

## Verificação end-to-end

Repo é plugin de markdown sem suite automatizada — verificação textual:

1. `grep -n "project-level" CLAUDE.md docs/philosophy.md skills/run-plan/SKILL.md` deixa de retornar a descrição "project-level only" para qa/security; ocorrências remanescentes (se houver) referem-se exclusivamente ao mecanismo de override.
2. `grep -n -i "release" README.md` retorna a nova linha da skill na tabela "O que vem".
3. Inspeção visual confirma consistência cruzada:
   - `CLAUDE.md:16` (agents bundled) coerente com a nova redação de `CLAUDE.md:29` e `CLAUDE.md:49`.
   - `docs/philosophy.md:37` coerente com `agents/qa-reviewer.md` e `agents/security-reviewer.md` shipados.
   - `skills/run-plan/SKILL.md:61` coerente com a descrição do `/run-plan` em `CLAUDE.md` e com `agents/code-reviewer.md` ("Revisor default invocado por `/run-plan`").
   - Linha de `/release` no README coerente com `plugin.json` (description), `CLAUDE.md` ("Skill workflow contract" item 5) e `docs/install.md` (cenário 10).

## Notas operacionais

- Mudança doc-only — patch bump natural (v1.12.1) via `/release` após o fechamento dos blocos.
- Sem alteração em mecânica de skill ou agent: `/run-plan` continua resolvendo o agent pelo `name:` do frontmatter; precedência project-over-plugin é convenção Claude Code, não código deste plugin.
