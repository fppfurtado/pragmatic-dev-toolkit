---
name: run-plan
description: Executa um plano de docs/plans/<slug>.md em worktree isolada, com micro-commits Conventional Commits, revisão dirigida por bloco e gate de validação manual quando aplicável. Use quando o operador autorizou começar a implementação a partir de um plano pronto.
---

# run-plan

Executa um plano produzido por `/new-feature` (ou escrito à mão) seguindo a disciplina **worktree isolada → micro-commit por bloco → revisão dirigida → gate final**. Importa a parte boa de execução disciplinada (worktree, commits granulares, gate antes de declarar done) sem o overhead documental (spec separado, two-stage review universal, plano gigante).

Esta skill **executa** mudanças. Deve ser chamada explicitamente pelo operador, após o plano estar revisado.

## Argumentos

Slug do plano (filename em `<plans_dir>/<slug>.md` sem o `.md`, default `docs/plans/<slug>.md`):

```
/run-plan exportar-movimentos-csv
```

Se o slug não corresponder a nenhum arquivo, parar e listar os planos disponíveis.

## Pré-condições

Paths e comandos abaixo seguem a **Resolução de papéis** (ver `docs/philosophy.md`): default canonical → bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md → pergunta ao operador.

Headers de plano (`## Arquivos a alterar`, `## Verificação end-to-end`, `## Verificação manual`, `## Contexto`, `## Resumo da mudança`) são citados em PT-BR canonical. Em planos escritos em outro idioma, fazer **matching semântico** pelo equivalente lingüístico (`## Files to change`, `## End-to-end verification`, etc.) — ver "Convenção de idioma" em `docs/philosophy.md`.

1. `<plans_dir>/<slug>.md` existe e tem `## Arquivos a alterar` (papel: `plans_dir`, default: `docs/plans/`).
2. O gate automático de testes do projeto está verde no branch atual (rodar antes de começar). Default: `make test`. Variante: `test_command` declarado no CLAUDE.md (ex.: `uv run pytest`, `npm test`, `cargo test`). Em projetos sem suite automatizada (meta-tools, doc-only), `## Verificação end-to-end` do plano substitui o gate — caso de exceção, sinalizado pela ausência de `test_command` resolvido **e** por o plano explicitar essa verificação textual.
3. A worktree `.worktrees/<slug>/` ainda não existe.

Se qualquer pré-condição falhar, parar e reportar ao operador.

## Passos

### 1. Setup da worktree

1. `git worktree add .worktrees/<slug> -b <slug>` a partir do branch atual.
2. **Replicar gitignored files essenciais**:
   - Se `.worktreeinclude` existe na raiz do repo: ler (1 path por linha, comentários com `#`) e copiar cada path do repo origem para a worktree. **Cópia, não symlink** — a worktree precisa ser realmente isolada.
   - Se não existe e o operador ainda não declarou explicitamente que não precisa, propor criação **uma vez por projeto**: listar gitignored em uso aparente (`.env`, dbs locais, fixtures não versionadas) e perguntar quais devem ser replicados. Resposta "não preciso" é válida e o passo é pulado; nesse caso avisar que o gate baseline pode falhar por dependências locais ausentes.
3. `cd` na worktree. Sincronizar dependências conforme a stack (ex.: `uv sync` em Python). Rodar o `test_command` resolvido como baseline (default: `make test`). **Abortar se falhar** — o plano não roda em cima de testes vermelhos. Quando `test_command` resolve para "não temos" e o plano traz `## Verificação end-to-end`, o baseline vira inspeção textual conforme essa seção descreve.

### 2. Sanity check de escopo

Releia `## Contexto` e `## Resumo da mudança` do plano. Se houver menção a superfícies externas (configuração, ambiente, infraestrutura, compose, deploy, webhook, integração externa, `.env`) **que não aparecem em `## Arquivos a alterar`**, **avisar o operador** (cutucar, não bloquear) — o plano pode estar incompleto.

### 3. Loop por bloco de `## Arquivos a alterar`

Para cada subseção do plano (geralmente um bloco por arquivo ou agrupamento lógico):

1. **Implementar** as mudanças descritas no bloco.
2. **Rodar o `test_command` resolvido** uma vez no fim do bloco (não a cada arquivo). Se `test_command` é "não temos", aplicar a verificação textual definida no plano.
3. **Escolher o revisor**:
   - Se o título do bloco tem anotação `{revisor: code}`, usar `code-reviewer` (incluído neste plugin).
   - Se a anotação for `qa` ou `security` e o projeto fornece um agent correspondente em `.claude/agents/` (ex.: `qa-reviewer`, `security-reviewer`), usar esse agent project-level.
   - Sem anotação, default = `code-reviewer`.
   - Bloco com perfis mistos: invocar o mais sensível (`security` > `qa` > `code`).
4. **Aplicar correções** levantadas pelo revisor antes de prosseguir.
5. **Micro-commit** seguindo a **convenção de commits do projeto consumidor** (ver `docs/philosophy.md` → "Convenção de commits"): política explícita declarada → padrão observado no histórico (`git log`) → default canonical Conventional Commits em inglês. **Um commit por bloco**. **Nunca** `--amend` ou rebase de commits anteriores do `/run-plan`.

### 4. Gate final

1. Rodar o `test_command` resolvido integralmente (gate automático sempre que houver). Quando `test_command` é "não temos", o gate é a inspeção textual de `## Verificação end-to-end` do plano.
2. Se o plano tem seção `## Verificação manual`: ler os passos ao operador e **aguardar confirmação explícita** ("ok, valido") antes de declarar done. Sem confirmação, a skill não fecha.
3. Sem `## Verificação manual`: gate automático verde (ou inspeção textual completa) já é gate suficiente. Declarar done.

A skill termina na worktree com branch da feature. Caminho de fechamento (PR, merge, descarte) é decisão do operador.

## O que NÃO fazer

- Não declarar done sem confirmação humana **quando o plano exige validação manual**.
- Não pular revisor, mesmo em bloco trivial.
- Não fazer `git commit --amend` ou rebase de commits anteriores do `/run-plan` — micro-commits revertíveis são o ponto.
- Não tentar resolver merge/rebase no fim — a skill não fecha o branch.
- Não rodar a skill sem o plano revisado e aprovado pelo operador.

## Convenção: `.worktreeinclude`

Arquivo opcional na raiz do repo (versionado) que lista paths gitignored a replicar em worktrees novas. Formato:

```
# Configuração local (segredos pessoais)
.env

# Banco SQLite local persistido entre runs
local.sqlite3
```

Comentários com `#`, um path por linha. Caminhos relativos à raiz do repo. Globs simples (`*.local.json`) podem ser suportados em iteração futura — primeira versão é literal.
