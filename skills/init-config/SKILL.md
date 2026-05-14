---
name: init-config
description: Wizard interativo para configurar o bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md`. Use quando o operador quer configurar o plugin de uma vez em projeto novo ou reconfigurar bloco existente.
disable-model-invocation: false
---

# init-config

Wizard interativo para configurar o bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md` do projeto consumidor. Alternativa proativa à memorização one-shot per role do Resolution protocol (passo 4).

**Cobertura v1:** 4 roles com dor concreta — `decisions_dir`, `backlog`, `plans_dir` (aceitam local mode per [ADR-005](../../docs/decisions/ADR-005-modo-local-gitignored-roles.md)) e `test_command` (top-level no schema). Informational roles (`product_direction`, `ubiquitous_language`, `design_notes`) e `version_files`/`changelog` ficam fora — operador edita manualmente quando precisar.

Frontmatter sem `roles:` por design ([ADR-003](../../docs/decisions/ADR-003-frontmatter-roles.md) § Schema) — `/init-config` define o bloco que o Resolution protocol lê em vez de consumi-lo; cutucada de descoberta ([ADR-017](../../docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md)) não se aplica dentro desta skill.

## Argumentos

Sem argumentos. Skill puramente interativa — perguntas via `AskUserQuestion` per role.

## Passos

### 1. Probe do estado do consumer

1. **`CLAUDE.md` existe?** `ls CLAUDE.md`. Ausente → parar com mensagem `"este projeto não tem CLAUDE.md. Crie o arquivo antes — CLAUDE.md tem propósito mais amplo que o bloco config do plugin; /init-config não cria por design."`. Plugin não infere a necessidade do operador.

2. **Em repo git?** `git rev-parse --is-inside-work-tree`. Falha (não-git) → pular probe de gitignore (passo 3), prosseguir.

3. **`CLAUDE.md` gitignored?** `git check-ignore -q CLAUDE.md`. Retorno zero (gitignored) → **registrar flag interna** `claude_md_gitignored = true` para o step 4.5; prosseguir normalmente (per [ADR-030](../../docs/decisions/ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md): plugin honra o sinal do consumer via `.gitignore` e garante replicação via `.worktreeinclude` em vez de recusar). Retorno não-zero → flag fica falsa; comportamento canonical (tracked).

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

**Recusa de cross-mode (ADR-025).** Após coletar as 4 respostas, **antes** de prosseguir para step 4, verificar se a combinação resultante é `paths.backlog: local` AND `paths.plans_dir: canonical` (canonical = operador escolheu `Canonical` OR `paths.plans_dir` ficaria omitido como default). Combinação detectada → parar com mensagem literal:

> Combinação `backlog: local + plans_dir: canonical` recusada ([ADR-025](../../docs/decisions/ADR-025-recusar-cross-mode-backlog-local-init-config.md)). `**Linha do backlog:**` viraria mensageiro de texto privado para plano público — semanticamente incoerente. Re-execute `/init-config` escolhendo uma das combinações suportadas: `ambos canonical` (default — registro coletivo), `ambos local` (uso individual), `backlog canonical + plans_dir local` (registro coletivo + planos privados).

Postura editorial não-reparativa — sem re-prompt automático via `AskUserQuestion`, operador re-executa com escolhas corrigidas. Bloco YAML **não é gravado** quando a combinação inválida é detectada.

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

### 4.5. Garantir paths replicados em `.worktreeinclude` (invariantes de setup)

**Critério de disparo:** ≥1 role configurada como `local` no passo 3 OR `claude_md_gitignored = true` (sinalizado pelo step 3), **independente do caminho de entrada do passo 2** (bloco ausente → gravar novo; bloco presente + `Editar` → gravar atualizado). Nenhuma condição ativa → skip silente.

Mecânica determinística (sem `AskUserQuestion` — operação tem resultado óbvio, sem trade-off cross-team a confirmar per [ADR-018](../../docs/decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md)):

**Lista composta de paths a garantir** (cada adição é independente e idempotente; cada condição testada isoladamente; presença prévia da linha — de run anterior — é skip silente; step 4.5 nunca remove linhas):

| Path | Condição de disparo | Probe (presença) | ADR de origem |
|---|---|---|---|
| `.claude/` | ≥1 role local | `grep -qE "^\.claude(/|$)" .worktreeinclude` | [ADR-018](../../docs/decisions/ADR-018-replicacao-claude-em-modo-local-init-config.md) |
| `CLAUDE.md` | `claude_md_gitignored = true` | `grep -qE "^CLAUDE\.md$" .worktreeinclude` | [ADR-030](../../docs/decisions/ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md) |

Procedimento por path com condição ativa:

1. **`.worktreeinclude` ausente** (primeira condição ativa do run) → criar com header de comentário (`# Gitignored paths to replicate into worktrees created by /run-plan.`) + linha em branco + linha do path.
2. **`.worktreeinclude` presente, probe retorna não-zero** (path ausente) → adicionar linha do path ao fim. Falso-negativo benigno aceito por simetria editorial — regex simples + linha redundante = sem dano funcional (replicação de path já replicado por entrada anterior é no-op real; per ADR-018 § Limitações).
3. **`.worktreeinclude` presente, probe retorna zero** (path já listado) → skip silente (idempotência).

Após processar todos os paths com condição ativa, reportar no relatório final:

> `.worktreeinclude <criado|atualizado|inalterado> em <path>; <lista de paths replicados> nas worktrees subsequentes do /run-plan.`

Onde `<lista de paths replicados>` é composta dos paths cujas condições dispararam (ex.: `.claude/`; `CLAUDE.md`; `.claude/ + CLAUDE.md` quando ambos).

Compatível com `.worktreeinclude` tracked ou gitignored — decisão organizacional do consumer.

### 5. Informar interações pendentes (não age)

Skill emite avisos informativos no relatório final — **não modifica** `.gitignore` automaticamente. Responsabilidade do operador.

**`CLAUDE.md` gitignored detectado** (`claude_md_gitignored = true`):

> `CLAUDE.md gitignored detectado — replicação garantida via .worktreeinclude por ADR-030.`

Substitui semanticamente a mensagem doutrinária revogada do step 3; cobre a transição da recusa anterior tornando a aceitação um ato deliberado visível.

**Modo local declarado em ≥1 role:**

> `Roles em modo local: <lista>. O gate "Gitignore" per ADR-005 dispara na primeira escrita subsequente sob .claude/local/<role>/ — quando você rodar /new-adr, /run-plan ou outra skill que grave lá. Naquele momento, operador confirma adicionar .claude/local/ ao .gitignore.`

## Probe stack-aware — adicionando stacks novas

A tabela de §3 é v1. Stacks adicionais (Gradle, Cargo, Cargo workspace, Bun, etc.) entram conforme aparecerem em consumers reais — não pré-implementar. Para adicionar nova linha: marker (arquivo presente no consumer) + valor proposto canônico daquela stack.

## O que NÃO fazer

- **Não criar `CLAUDE.md` se ausente.** Propósito mais amplo que o bloco config (instrução geral ao Claude Code). Passo 1 para com mensagem orientando o operador.
- **Não modificar `.gitignore` automaticamente.** Política git do consumer; gate específico do ADR-005 cobre quando necessário (primeira escrita sob `.claude/local/<role>/`).
- **Não pressionar doutrinariamente quando `CLAUDE.md` está gitignored.** [ADR-030](../../docs/decisions/ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md) estabelece aceitação como ato deliberado da skill (operador sinaliza via `.gitignore`, plugin opera dentro); reintroduzir mensagem "reconsidere o gitignore" no step 3 ou step 5 revoga a decisão.
- **Não reescrever bloco config malformado / duplicado / órfão.** Parar com diagnóstico; operador resolve manualmente. Postura editorial, não reparativa.
- **Não invocar outras skills do toolkit em cascata.** `/init-config` é setup, não orquestrador. Operador chama as skills seguintes manualmente após config gravado.
- **Não emitir cutucada de descoberta (ADR-017):** `/init-config` define o bloco em vez de consumir.
- **Não acomodar cross-mode `backlog: local + plans_dir: canonical` via warning, re-prompt ou cobertura defensiva** ([ADR-025](../../docs/decisions/ADR-025-recusar-cross-mode-backlog-local-init-config.md)) — recusa hard é o ponto; "amaciar" a recusa em futura edição re-introduz leak de texto privado para plano público.
