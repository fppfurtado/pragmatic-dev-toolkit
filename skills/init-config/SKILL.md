---
name: init-config
description: Wizard de configuração inicial dos papéis do plugin no consumer — pergunta cada role (canonical/local/null), detecta `test_command` stack-aware, grava o bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md. Use quando o operador quer configurar o plugin de uma vez em projeto novo ou reconfigurar bloco existente.
---

# init-config

Wizard interativo para configurar o bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md` do projeto consumidor. Alternativa proativa à memorização one-shot per role do Resolution protocol (passo 4).

**Cobertura v1:** 4 roles com dor concreta — `decisions_dir`, `backlog`, `plans_dir` (aceitam local mode per [ADR-005](../../docs/decisions/ADR-005-modo-local-gitignored-roles.md)) e `test_command` (top-level no schema). Informational roles (`product_direction`, `ubiquitous_language`, `design_notes`) e `version_files`/`changelog` ficam fora — operador edita manualmente quando precisar.

Diferente das demais skills do toolkit, `/init-config` **não** consome roles via Resolution protocol — ela **define** o bloco que o protocol lê. Frontmatter sem `roles:` por design (per [ADR-003](../../docs/decisions/ADR-003-frontmatter-roles.md) § Schema, listas vazias podem ser omitidas). Cutucada de descoberta do [ADR-017](../../docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) **não dispara dentro de `/init-config`**.

## Argumentos

Sem argumentos. Skill puramente interativa — perguntas via `AskUserQuestion` per role.

## Passos

### 1. Probe do estado do consumer

1. **`CLAUDE.md` existe?** `ls CLAUDE.md`. Ausente → parar com mensagem `"este projeto não tem CLAUDE.md. Crie o arquivo antes — CLAUDE.md tem propósito mais amplo que o bloco config do plugin; /init-config não cria por design."`. Plugin não infere a necessidade do operador.

2. **Em repo git?** `git rev-parse --is-inside-work-tree`. Falha (não-git) → pular probe de gitignore (passo 3), prosseguir.

3. **`CLAUDE.md` gitignored?** `git check-ignore -q CLAUDE.md`. Retorno zero (gitignored) → **parar** com mensagem alinhada com [ADR-016](../../docs/decisions/ADR-016-manter-block-gitignored-scripts-no-consumer.md):

   > `CLAUDE.md está gitignored neste projeto (.gitignore). Per ADR-016 do toolkit, o caminho doutrinário é reconsiderar a decisão organizacional de gitignorar CLAUDE.md — é artefato compartilhável por design. Plugin não prescreve workaround manual nem oferece caminho alternativo de gravação.`

   Sem ação adicional. Operador resolve no consumer.

### 2. Detectar bloco config existente

`grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna:

- **Zero (marker presente).** Tentar parsear o YAML adjacente (fenced ```yaml depois do marker até próximo ```):
  - **Parse OK** → exibir bloco atual ao operador. Cutucada via `AskUserQuestion` (header `Config`) com opções `Editar` / `Cancelar`. `Cancelar` → skill devolve sem tocar arquivo, reporta no-op. `Editar` → procede para passo 3 (perguntas sobrescrevem os valores atuais).
  - **Parse falha / múltiplos markers / marker órfão sem YAML adjacente** → **parar** com diagnóstico textual identificando linha e tipo de anomalia (ex.: `"marker encontrado em CLAUDE.md linha 134 mas YAML adjacente não parseia: <erro do parser>"`). Não reescrever, não fundir, não tomar o primeiro. Postura editorial não-reparativa (paralelo com não-criar-CLAUDE.md no passo 1).
- **Não-zero (marker ausente).** Procede para passo 3.

### 3. Perguntar per role

Quatro perguntas via `AskUserQuestion`. Agrupar numa única chamada quando viável (limite 4 questions per chamada, regra de unificação em `CLAUDE.md` → "AskUserQuestion mechanics"). Para os 3 roles que aceitam local mode, **labels** ficam curtos (`Canonical` / `Local` / `Não usamos`) e o **path resolvido** vai em `description` (carrega o trade-off concreto per convenção `AskUserQuestion mechanics`):

| Role | Header | Opções (label / description) |
|---|---|---|
| `decisions_dir` | `Decisions` | `Canonical` (`grava em docs/decisions/ — default canonical do toolkit`) (Recommended) / `Local` (`grava em .claude/local/decisions/ — gitignored, não compartilhado`) / `Não usamos` (`grava paths.decisions_dir: null — skill subsequente trata como absent sem perguntar`) |
| `backlog` | `Backlog` | análogo (paths `BACKLOG.md` / `.claude/local/BACKLOG.md` / null) |
| `plans_dir` | `Plans` | análogo (paths `docs/plans/` / `.claude/local/plans/` / null) |
| `test_command` | `TestCmd` | opções dependem do probe — ver abaixo |

**Probe stack-aware para `test_command`** antes de perguntar — testa markers do consumer e propõe valor inicial:

| Marker presente | Valor proposto |
|---|---|
| `pom.xml` | `mvn test -DfailIfNoTests=false` |
| `pyproject.toml` + `uv` no `PATH` | `uv run pytest -q --no-header` |
| `pyproject.toml` sem `uv` | `python -m pytest -q --no-header` |
| `package.json` com chave `scripts.test` | `npm test` |
| `Makefile` com target `test` (`grep -E "^test:" Makefile`) | `make test` |
| Nenhum match | (sem proposta) |

Pergunta via `AskUserQuestion` (header `TestCmd`):

- Probe deu match → opções `<valor proposto>` (Recommended) / `Não declarar (null) — /run-plan cai em "## Verificação end-to-end" manual` / Other (operador customiza).
- Probe sem match → opções `Não declarar (null)` (Recommended) / Other.

### 4. Compor e gravar bloco YAML no CLAUDE.md

Estratégia de composição (compactar — chave omitida significa canonical default per schema):

- Operador escolheu **canonical** → omitir chave do YAML (canonical é o default; explicitar polui).
- Operador escolheu **local** → incluir `paths.<role>: local`.
- Operador escolheu **null** → incluir `paths.<role>: null` (skill subsequente trata como absent sem perguntar de novo).
- `test_command` é top-level, não sob `paths`. Mesmo critério: canonical default = `make test`; valor customizado vira `test_command: "<valor>"`; null vira `test_command: null`.

Marker HTML fixo (string literal exata): `<!-- pragmatic-toolkit:config -->`.

**Forma do edit:**

- **Bloco existente (passo 2 / Editar)** → substituir o YAML adjacente ao marker in-place. Preservar marker, seção `## Pragmatic Toolkit`, e prosa antes/depois.
- **Bloco ausente (passo 2 / sem match)** → criar seção nova `## Pragmatic Toolkit` no fim do arquivo. Conteúdo da seção (composto na ordem):
  1. Header `## Pragmatic Toolkit`.
  2. Linha de prosa introdutória **opcional** — operador pode contextualizar a seção com 1 frase, ou skill omite (marker + YAML já se explicam). Default da skill: omitir parágrafo introdutório (canonical do toolkit em PT-BR; sem heurística de idioma).
  3. Linha do marker HTML literal: `<!-- pragmatic-toolkit:config -->`.
  4. Bloco YAML em fence ```yaml com chaves selecionadas conforme estratégia de composição acima.

Reportar path final ao operador:

> `Bloco config gravado em <path> linha <N>. Confirme com: grep -A8 'pragmatic-toolkit:config' CLAUDE.md`

### 5. Informar interações pendentes (não age)

Skill emite avisos informativos no relatório final — **não modifica** `.gitignore` nem `.worktreeinclude` automaticamente. Responsabilidade do operador.

**Modo local declarado em ≥1 role:**

> `Roles em modo local: <lista>. O gate "Gitignore" per ADR-005 dispara na primeira escrita subsequente sob .claude/local/<role>/ — quando você rodar /new-adr, /run-plan ou outra skill que grave lá. Naquele momento, operador confirma adicionar .claude/local/ ao .gitignore.`

**Modo local em `plans_dir` AND `.worktreeinclude` do consumer não cobre `.claude/local/` (ou `.claude/`):**

> `Atenção: /run-plan em modo local exige .claude/local/ replicado para a worktree fresca. Adicione .claude/local/ (ou .claude/) ao .worktreeinclude antes de rodar /run-plan — caso contrário a worktree não enxergará o plano local.`

Probe: existe `.worktreeinclude`? `grep -qE "^\.claude(/|$)" .worktreeinclude` em caso afirmativo (regex cobre `.claude`, `.claude/`, `.claude/local/`, `.claude/local/**`, etc. — falso-positivo é mais barato que falso-negativo aqui). Se ausente OU sem cobertura, emitir o aviso.

## Probe stack-aware — adicionando stacks novas

A tabela de §3 é v1. Stacks adicionais (Gradle, Cargo, Cargo workspace, Bun, etc.) entram conforme aparecerem em consumers reais — não pré-implementar. Para adicionar nova linha: marker (arquivo presente no consumer) + valor proposto canônico daquela stack.

## O que NÃO fazer

- **Não modificar `.gitignore` automaticamente.** Modo local pode exigir entrada — esse gate é responsabilidade de ADR-005, dispara na primeira escrita subsequente em `.claude/local/<role>/`, não dentro de `/init-config`.
- **Não modificar `.worktreeinclude` automaticamente.** Interação é responsabilidade do operador; skill apenas informa no passo 5.
- **Não reescrever bloco config malformado / duplicado / órfão.** Parar com diagnóstico; operador resolve manualmente. Postura editorial, não reparativa.
- **Não invocar outras skills do toolkit em cascata.** `/init-config` é setup, não orquestrador. Operador chama as skills seguintes manualmente após config gravado.
- **Não emitir cutucada de descoberta de ADR-017 dentro desta skill.** Escopo da cutucada (ADR-017) é skills com `roles.required`; `/init-config` é fora desse universo.
