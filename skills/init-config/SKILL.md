---
name: init-config
description: Wizard interativo para configurar o bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md`. Use quando o operador quer configurar o plugin de uma vez.
disable-model-invocation: false
---

# init-config

Wizard interativo para configurar o bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md` do projeto consumidor. Alternativa proativa à memorização one-shot per role do Resolution protocol (passo 4).

**Cobertura:** 5 roles — `decisions_dir`, `backlog`, `plans_dir` (aceitam local mode per [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md); `backlog` adicionalmente aceita forge mode per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md)), `test_command` (top-level no schema) e `ubiquitous_language` (informational; sem local mode). Outros informational roles (`product_direction`, `design_notes`) e `version_files`/`changelog` ficam fora — operador edita manualmente quando precisar; adicionar incrementalmente ao wizard conforme dor concreta emergir.

Frontmatter sem `roles:` por design ([ADR-003](../../docs/decisions/ADR-003-frontmatter-roles.md) § Schema) — `/init-config` define o bloco que o Resolution protocol lê em vez de consumi-lo; cutucada de descoberta ([ADR-046](../../docs/decisions/ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md)) não se aplica dentro desta skill.

## Argumentos

Sem argumentos. Skill puramente interativa — perguntas via `AskUserQuestion` per role.

## Passos

### 1. Probe do estado do consumer

1. **`CLAUDE.md` existe?** `ls CLAUDE.md`. Ausente → parar com mensagem `"este projeto não tem CLAUDE.md. Crie o arquivo antes — CLAUDE.md tem propósito mais amplo que o bloco config do plugin; /init-config não cria por design."`. Plugin não infere a necessidade do operador.

2. **Em repo git?** `git rev-parse --is-inside-work-tree`. Falha (não-git) → pular probe de gitignore (passo 3), prosseguir.

3. **`CLAUDE.md` gitignored?** `git check-ignore -q CLAUDE.md`. Retorno zero (gitignored) → **registrar flag interna** `claude_md_gitignored = true` para o step 4.5; prosseguir normalmente (per [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md): plugin honra o sinal do consumer via `.gitignore` e garante replicação via `.worktreeinclude` em vez de recusar). Retorno não-zero → flag fica falsa; comportamento canonical (tracked).

### 2. Detectar bloco config existente

`grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna:

- **Zero (marker presente).** Tentar parsear o YAML adjacente (fenced ```yaml depois do marker até próximo ```):
  - **Parse OK** → exibir bloco atual ao operador. Cutucada via `AskUserQuestion` (header `Config`) com opções `Editar` / `Cancelar`. `Cancelar` → skill devolve sem tocar arquivo, reporta no-op. `Editar` → procede para passo 3 (perguntas sobrescrevem os valores atuais).
  - **Parse falha / múltiplos markers / marker órfão sem YAML adjacente** → **parar** com diagnóstico textual identificando linha e tipo de anomalia (ex.: `"marker encontrado em CLAUDE.md linha 134 mas YAML adjacente não parseia: <erro do parser>"`). Não reescrever, não fundir, não tomar o primeiro. Postura editorial não-reparativa (paralelo com não-criar-CLAUDE.md no passo 1).
- **Não-zero (marker ausente).** Procede para passo 3.

### 3. Perguntar per role

#### 3.0. Pré-probe do forge (para role `backlog`)

Executado antes da tabela de perguntas. Resolve disponibilidade do forge no consumer corrente; usado para condicionar a opção `Forge` da pergunta do role `backlog`.

- **Clause defensiva não-git:** se step 1 sinalizou não-git (precondição `git rev-parse --is-inside-work-tree` falhou), pular pré-probe e tratar `forge_disponivel = false` (paralelo a `unsupported-host`). `forge-auto-detect.md` § Algoritmo bullet 1 (`git remote get-url origin`) lança erro shell em não-git, não retorna output controlado — clause cobre o gap.
- Caso git válido: seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md` uma vez.
- Registrar `forge_disponivel = true` se output é `gh` ou `glab`; `false` se `no-detection` ou `unsupported-host`.
- Probe é silente (sem reportar ao operador agora — eventual nota emitida no §5 quando operador escolheu `Forge`).

**Convenção de Recommended em modo Editar:** Recommended estático (`Canonical (Recommended)`) preservado mesmo quando bloco existente declara modo diferente (passo 2 / `Editar`). Operador re-seleciona ativamente o valor atual. Sem dinâmica de Recommended dependente de estado anterior — aderente a `CLAUDE.md` → "AskUserQuestion mechanics" (`(Recommended)` só quando default é estatisticamente estável; estado anterior ≠ default estatístico).

#### 3.1. Perguntas per role

Quatro perguntas via `AskUserQuestion`. Agrupar numa única chamada quando viável (limite 4 questions per chamada, regra de unificação em `CLAUDE.md` → "AskUserQuestion mechanics"). Para os 3 roles que aceitam local mode, **labels** ficam curtos (`Canonical` / `Local` / `Não usamos`) e o **path resolvido** vai em `description` (carrega o trade-off concreto per convenção `AskUserQuestion mechanics`):

| Role | Header | Opções (label / description) |
|---|---|---|
| `decisions_dir` | `Decisions` | `Canonical` (`grava em docs/decisions/ — default canonical do toolkit`) (Recommended) / `Local` (`grava em .claude/local/decisions/ — gitignored, não compartilhado`) / `Não usamos` (`grava paths.decisions_dir: null — skill subsequente trata como absent sem perguntar`) |
| `backlog` | `Backlog` | `Canonical` (Recommended) / `Local` / `Forge` (apenas se `forge_disponivel = true`, per §3.0) / `Não usamos`. Paths e trade-offs em `description`: `Canonical` (`grava em BACKLOG.md — default canonical do toolkit`), `Local` (`grava em .claude/local/BACKLOG.md — gitignored, não compartilhado`), `Forge` (`backlog vem do forge — issues abertas sem assignee via gh/glab; mutações remotas (criar/fechar issue) precedidas de cutucada AskUserQuestion. Aplica-se a backlog v1 (decisions_dir/plans_dir rejeitam). Identificador interno: '#<número>: <título>' per ADR-058`), `Não usamos` (`grava paths.backlog: null — skill subsequente trata como absent sem perguntar`) |
| `plans_dir` | `Plans` | análogo a `decisions_dir` (paths `docs/plans/` / `.claude/local/plans/` / null) |
| `ubiquitous_language` | `Domain` | `Canonical` (`grava em docs/domain.md — default canonical do toolkit`) / `Não usamos` (`grava paths.ubiquitous_language: null — skill subsequente trata como absent sem perguntar`) |
| `test_command` | `TestCmd` | opções dependem do probe — ver abaixo |

`forge_disponivel = false` → opção `Forge` **omitida** da pergunta (não exibida disabled — wizard enxuto per `## O que NÃO fazer`). Sem cutucada explicativa.

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

**Recusa de cross-mode (ADR-047).** Após coletar as 4 respostas, **antes** de prosseguir para step 4, verificar se a combinação resultante é `paths.backlog: local` AND `paths.plans_dir: canonical` (canonical = operador escolheu `Canonical` OR `paths.plans_dir` ficaria omitido como default). Combinação detectada → parar com mensagem literal:

> Combinação `backlog: local + plans_dir: canonical` recusada ([ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)). `**Linha do backlog:**` viraria mensageiro de texto privado para plano público — semanticamente incoerente. Re-execute `/init-config` escolhendo uma das combinações suportadas: `ambos canonical` (default — registro coletivo), `ambos local` (uso individual), `backlog canonical + plans_dir local` (registro coletivo + planos privados).

Postura editorial não-reparativa — sem re-prompt automático via `AskUserQuestion`, operador re-executa com escolhas corrigidas. Bloco YAML **não é gravado** quando a combinação inválida é detectada.

A recusa acima opera sobre modo `local` (mensageiro `**Linha do backlog:**` carrega texto privado). Em modo `forge`, o identificador `#<número>: <título>` é público por construção; combinações com `paths.backlog: forge` ficam fora desta recusa ([ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md) § (i)). Categoria semântica distinta vs exceção à regra original.

### 4. Compor e gravar bloco YAML no CLAUDE.md

Estratégia de composição (compactar — chave omitida significa canonical default per schema):

- Operador escolheu **canonical** → omitir chave do YAML (canonical é o default; explicitar polui).
- Operador escolheu **local** → incluir `paths.<role>: local`.
- Operador escolheu **null** → incluir `paths.<role>: null` (skill subsequente trata como absent sem perguntar de novo).
- Operador escolheu **forge** (apenas role `backlog`) → incluir `paths.backlog: forge`. Skill subsequente que consome o role executa probe do CLI na primeira invocação per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md) § (d) policy do caller; failure → erro explícito orientando setup.
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

**Critério de disparo:** ≥1 role configurada como `local` no passo 3 OR `claude_md_gitignored = true` (sinalizado pelo step 3), **independente do caminho de entrada do passo 2** (bloco ausente → gravar novo; bloco presente + `Editar` → gravar atualizado). Nenhuma condição ativa → skip silente. (Modo `forge` não dispara replicação — paralelo a canonical, sem store local sob `.claude/`. Per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md) § (a).)

Mecânica determinística (sem `AskUserQuestion` — operação tem resultado óbvio, sem trade-off cross-team a confirmar per [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)):

**Lista composta de paths a garantir** (cada adição é independente e idempotente; cada condição testada isoladamente; presença prévia da linha — de run anterior — é skip silente; step 4.5 nunca remove linhas):

| Path | Condição de disparo | Probe (presença) | ADR de origem |
|---|---|---|---|
| `.claude/` | ≥1 role local | `grep -qE "^\.claude(/|$)" .worktreeinclude` | [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) |
| `CLAUDE.md` | `claude_md_gitignored = true` | `grep -qE "^CLAUDE\.md$" .worktreeinclude` | [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) |

Procedimento por path com condição ativa:

1. **`.worktreeinclude` ausente** (primeira condição ativa do run) → criar com header de comentário (`# Gitignored paths to replicate into worktrees created by /run-plan.`) + linha em branco + linha do path.
2. **`.worktreeinclude` presente, probe retorna não-zero** (path ausente) → adicionar linha do path ao fim. Falso-negativo benigno aceito por simetria editorial — regex simples + linha redundante = sem dano funcional (replicação de path já replicado por entrada anterior é no-op real; per ADR-047 § Limitações).
3. **`.worktreeinclude` presente, probe retorna zero** (path já listado) → skip silente (idempotência).

Após processar todos os paths com condição ativa, reportar no relatório final:

> `.worktreeinclude <criado|atualizado|inalterado> em <path>; <lista de paths replicados> nas worktrees subsequentes do /run-plan.`

Onde `<lista de paths replicados>` é composta dos paths cujas condições dispararam (ex.: `.claude/`; `CLAUDE.md`; `.claude/ + CLAUDE.md` quando ambos).

Compatível com `.worktreeinclude` tracked ou gitignored — decisão organizacional do consumer.

### 5. Informar interações pendentes (não age)

Skill emite avisos informativos no relatório final — **não modifica** `.gitignore` automaticamente. Responsabilidade do operador.

**`CLAUDE.md` gitignored detectado** (`claude_md_gitignored = true`):

> `CLAUDE.md gitignored detectado — replicação garantida via .worktreeinclude por ADR-047.`

Substitui semanticamente a mensagem doutrinária revogada do step 3; cobre a transição da recusa anterior tornando a aceitação um ato deliberado visível.

**Modo local declarado em ≥1 role:**

> `Roles em modo local: <lista>. O gate "Gitignore" per ADR-047 dispara na primeira escrita subsequente sob .claude/local/<role>/ — quando você rodar /new-adr, /run-plan ou outra skill que grave lá. Naquele momento, operador confirma adicionar .claude/local/ ao .gitignore.`

**Modo `forge` declarado em `backlog`:**

> `Modo forge declarado em backlog. Primeira invocação de skill consumidora (/next passo 1, /triage step 4, /run-plan §3.4, /curate-backlog) executa probe via forge-auto-detect.md no momento e pode falhar com erro explícito se setup mudar (CLI desinstalada, repo movido para host não suportado, etc.). Cutucada AskUserQuestion precede cada mutação remota (criar/fechar issue) por blast radius imediato.`

## Probe stack-aware — adicionando stacks novas

A tabela de §3 é v1. Stacks adicionais (Gradle, Cargo, Cargo workspace, Bun, etc.) entram conforme aparecerem em consumers reais — não pré-implementar. Para adicionar nova linha: marker (arquivo presente no consumer) + valor proposto canônico daquela stack.

## O que NÃO fazer

- **Não criar `CLAUDE.md` se ausente.** Propósito mais amplo que o bloco config (instrução geral ao Claude Code). Passo 1 para com mensagem orientando o operador.
- **Não modificar `.gitignore` automaticamente.** Política git do consumer; gate específico do ADR-047 cobre quando necessário (primeira escrita sob `.claude/local/<role>/`).
- **Não pressionar doutrinariamente quando `CLAUDE.md` está gitignored.** [ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md) estabelece aceitação como ato deliberado da skill (operador sinaliza via `.gitignore`, plugin opera dentro); reintroduzir mensagem "reconsidere o gitignore" no step 3 ou step 5 revoga a decisão.
- **Não reescrever bloco config malformado / duplicado / órfão.** Parar com diagnóstico; operador resolve manualmente. Postura editorial, não reparativa.
- **Não invocar outras skills do toolkit em cascata.** `/init-config` é setup, não orquestrador. Operador chama as skills seguintes manualmente após config gravado.
- **Não emitir cutucada de descoberta (ADR-046):** `/init-config` define o bloco em vez de consumir.
- **Não acomodar cross-mode `backlog: local + plans_dir: canonical` via warning, re-prompt ou cobertura defensiva** ([ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)) — recusa hard é o ponto; "amaciar" a recusa em futura edição re-introduz leak de texto privado para plano público.
- **Não oferecer opção `Forge` quando pré-probe retorna `no-detection`/`unsupported-host`** ([ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md)) — operador veria opção que falha por construção. Opção omitida é silente, sem cutucada explicativa (mantém wizard enxuto; alternativa "disabled com diagnóstico inline" rebatida no plano original — `## O que NÃO fazer` registra a doutrina).
