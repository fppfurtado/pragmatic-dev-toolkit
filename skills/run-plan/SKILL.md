---
name: run-plan
description: Executa plano de docs/plans/<slug>.md em worktree isolada, com micro-commits, revisor por bloco e gate de validação manual. Use quando há plano pronto e o operador autorizou implementar.
disable-model-invocation: false
roles:
  required: [plans_dir]
  informational: [backlog, test_command]
---

# run-plan

Executa um plano produzido por `/triage` (ou escrito à mão) seguindo a disciplina **worktree isolada → micro-commit por bloco → revisão dirigida → gate final**. Importa execução disciplinada (worktree, commits granulares, gate antes do done) sem overhead documental.

Esta skill **executa** mudanças. Chamar explicitamente após o plano estar revisado.

## Argumentos

Slug do plano (filename em `<plans_dir>/<slug>.md` sem o `.md`, default `docs/plans/<slug>.md`):

```
/run-plan exportar-movimentos-csv
```

Slug sem arquivo correspondente → parar e listar planos disponíveis.

## Pré-condições

Headers de plano são citados em PT-BR canonical (`## Arquivos a alterar`, `## Verificação end-to-end`, etc.); planos em outro idioma usam matching semântico (`## Files to change`, `## End-to-end verification`, ...).

Falha de qualquer pré-condição → parar e reportar.

**0. Detecção de modo** (per [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (d)). Ler `**Modo:**` do `## Contexto` do plano. Ausência = canonical (default total). Presença e valor `runbook` → ativar fluxo alternativo descrito em **## Modo runbook** abaixo (afeta as pré-condições subsequentes, a detecção de warnings pré-loop e os §1/§2/§3 dos Passos). Valor diferente de `runbook` (incluindo `**Modo:** canonical` explícito, `default`, `standard`, etc.) → parar com mensagem `"valor do campo **Modo:** desconhecido: <valor> — valor aceito: runbook (omitir campo para fluxo canonical)"`. Combinação `**Modo:** runbook` + `**Branch:** <nome>` → parar com mensagem `"**Modo:** runbook + **Branch:** incompatíveis — runbook executa no working tree principal, sem worktree"`.

1. **Plano existe e tem `## Arquivos a alterar`** (papel: `plans_dir`, default: `docs/plans/`). Esqueleto canônico em `${CLAUDE_PLUGIN_ROOT}/templates/plan.md`. Em modo `local` (`paths.plans_dir: local`), plano lido de `.claude/local/plans/<slug>.md`.

2. **Estado git do plano** (`git status --porcelain`):
   - **Bloquear** se `<plans_dir>/<slug>.md` está modificado/untracked. Worktree é criada do HEAD e não veria o plano. Mensagem: commitar antes (ou usar `/triage`, que já propõe commit).
   - Em modo `local`: plano não é tracked pelo git (artefato gitignored em `.claude/local/plans/`). Verificação de tracking vira no-op — operador edita livremente. **Mas** worktree é criada do HEAD e só enxerga o plano local se `.claude/` (ou `.claude/local/`) está listado em `.worktreeinclude`. Não coberto → **bloquear** com mensagem `worktree não verá plano local — adicionar .claude/local/ ao .worktreeinclude antes de re-executar`.

3. **Gate automático verde no branch atual.** Default: `make test`. Variante: `test_command` no CLAUDE.md. Se canonical ausente E operador não declarou `test_command: null`, perguntar uma vez (oferta única de memorização). Projetos sem suite (`test_command: null` E plano traz `## Verificação end-to-end`) → baseline vira inspeção textual dessa seção. Gate falha → escrever em `## Próximos` do papel `backlog` linha tipo `baseline vermelho no branch ao iniciar /run-plan <slug> — investigar`; informar; parar. Papel `backlog` = "não temos" → só informar.

4. **Worktree `.worktrees/<slug>/` não existe.** Se existir → escrever em `## Próximos` linha tipo `worktree .worktrees/<slug> existe de run anterior — remover antes de re-executar`; informar; parar. Papel `backlog` = "não temos" → só informar.

**Aplicabilidade em modo runbook:** #1 aplica (plano existe e tem `## Arquivos a alterar`); #2 aplica (plano commitado — embora worktree não seja criada, `/run-plan` lê o plano-arquivo e edit não-commitado pode dessincronizar entre leitura inicial e blocos posteriores se operador editar mid-execução); #3 não aplica (sem baseline automático — `## Verificação end-to-end` é referência textual no done); #4 não aplica (sem worktree).

## Detecção de warnings pré-loop

Antes da worktree ser criada, detectar warnings de qualidade-de-mudança e classificá-los nos trilhos do passo 3.5 (Captura automática) — sem perguntar ao operador (ADR-002). Sem warnings detectados → silêncio total; skill segue para a worktree.

| Warning | Detecção | Trilho |
|---|---|---|
| **Alinhamento dirty** | papéis de alinhamento (`backlog`, `ubiquitous_language`, `design_notes`, arquivo sob `decisions_dir`) têm alterações uncommitted no `git status --porcelain` | **Aviso informativo** in situ: `"aviso: alinhamento uncommitted — <lista de arquivos>; reviewer pode não ver invariantes/ADRs uncommitted"`. Skill segue. Não alimenta a lista de captura. |
| **`.worktreeinclude` ausente** | raiz do repo tem gitignored típico em uso (`.env`, dbs locais, fixtures não versionadas) E `.worktreeinclude` não existe E operador não declarou `paths.worktreeinclude: null` | **Backlog**: `"capturei no backlog: criar .worktreeinclude listando <gitignored detectados> para replicação em worktrees"`. Alimenta a lista. |
| **Credencial não coberta** | plano tem `## Verificação manual` E raiz tem credencial gitignored típica (`.env`, `*.local.yaml`, `secrets.*`) não coberta pelo `.worktreeinclude` aplicado (quando existe) | **Validação**: `"capturei para verificação: cenário de validação manual não exercitado por falta da credencial <nome> na worktree"`. Alimenta a lista. |
| **Escopo divergente** | `## Contexto` ou `## Resumo da mudança` cita superfície externa (config, env, infra, deploy, webhook, integração externa, `.env`) ausente em `## Arquivos a alterar` | **Validação**: `"capturei para verificação: superfície externa <X> mencionada em Contexto/Resumo mas ausente em ## Arquivos a alterar — cenário não exercitado"`. Alimenta a lista. |
| **Cobertura ausente** | `## Arquivos a alterar` lista ao menos 1 path de **código de produção** E nenhum path casa **test pattern**. *Código de produção* = path que NÃO é doc (`.md`/`.rst`/`.txt`), NÃO é test pattern, NÃO é manifesto/config (`pyproject.toml`, `package.json`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `Gemfile`, `go.mod`, `go.sum`, `requirements*.txt`, `Pipfile*`, `tsconfig*.json`, `.eslintrc*`, `.prettierrc*`, `Dockerfile*`, `compose.y*ml`, `docker-compose.y*ml`, `*.lock`), NÃO está sob infra/ci/meta (`.github/`, `.gitlab/`, `.circleci/`, `.azuredevops/`, `infra/`, `deploy/`, `.claude/`, `docs/`). *Test patterns* (qualquer um suprime warning): `tests/`, `**/test_*`, `**/*_test.*`, `**/*.test.*`, `**/*.spec.*`, `__tests__/`, `src/test/` | **Validação**: `"capturei para verificação: cenário sem cobertura nova exercitada — código de produção em ## Arquivos a alterar sem teste correspondente (<paths>)"`. Alimenta a lista. |

Cada warning Backlog/Validação emite `TaskCreate` com marker — mecanismo unificado descrito em §3.5 (per [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (c)).

Estado prévio "não preciso" do `.worktreeinclude` **silencia** a captura de Backlog mas **não silencia** o gatilho cruzado de credencial — contexto mudou (plano corrente exige `## Verificação manual`).

Bloqueios (plano sujo, push esquecido, baseline vermelho, worktree órfã) ficam fora desta detecção — continuam parando a skill in situ com captura imediata.

**Em modo runbook:** pular toda a tabela acima — warnings pressupõem fluxo canonical (alinhamento dirty é sobre repo, runbook muta sistema; `.worktreeinclude` pressupõe worktree; cobertura ausente pressupõe diff git). Skip silente.

## Modo runbook

Ativado pela pré-condição 0 quando o plano declara `**Modo:** runbook` no `## Contexto` (per [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (d)). Modo cobre planos de **system-surgery** — operações cuja semântica não é diff git no repo (FS migration, infra reconfig, dotfiles sync, multi-repo edits, ops em `~/`). Bypassa 4 dimensões do canonical:

| Dimensão | Comportamento em runbook |
|---|---|
| Sem worktree | Pula §1 inteiro (setup, replicação `.worktreeinclude`, sync, baseline). Executa no working tree principal. Operador é responsável por backup/snapshot prévio fora da skill. |
| Sem commit-per-bloco | Pula item 5 do loop §2 (micro-commit). Blocos podem não produzir diff git; rollback é responsabilidade do operador (snapshot/tarball/manual), não `git revert`. |
| Gate de confirmação por bloco | Substitui itens 3-4 do loop §2 (escolher revisor + aplicar correções) por `AskUserQuestion` (header `Bloco N`, opções `Validei e seguir` / `Falhou — descrever`). Pattern paralelo a §3.2 do canonical (validação manual). |
| Validação intercalada | Cada bloco descreve sua própria validação inline. Gate final §3 reduz a §3.4 (Concluídos via `**Linha do backlog:**`) + §3.5 (captura automática) + §3.6 (declarar done). §3.1 (gate automático), §3.2 (validação manual centralizada), §3.3 (sanity check docs) e §3.7 (publicação) pulados. |

**Materialização de capturas no `Falhou`.** Ao operador escolher `Falhou — descrever` em qualquer bloco, antes de a skill parar, materializar capturas acumuladas em `TaskList` filtrada por `[capture:*]`: escrever em `## Pendências de validação` do plano e `## Próximos` do `backlog` conforme tipo da Task (paralelo a §3.5, disparado pelo `Falhou` ao invés do gate final). Skill termina após materialização. Evita perda de capturas dos blocos anteriores quando a execução para mid-plano.

**Reviewer per bloco ausente é intencional** — invariantes do bloco ficam por conta do gate humano de confirmação inline + revisão upstream manual por `@design-reviewer` sobre o plano-documento antes de invocar `/run-plan` (operador é responsável). Reviewer automático sobre diff inexistente não tem trabalho a fazer.

## Passos

### 1. Setup da worktree

**Em modo runbook:** pular §1 inteiro — executa no working tree principal (ver "## Modo runbook" acima).

1. **Criar worktree.** Detectar campo `**Branch:** <nome>` no `## Contexto` do plano (per [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (b)).
   - **Presente:** `git worktree add .worktrees/<slug> <nome>` (sem `-b`). git resolve `<nome>` em ordem natural (heads, depois remotes via DWIM se houver fetch prévio).
   - **Ausente:** `git worktree add .worktrees/<slug> -b <slug>` a partir do branch atual (comportamento default preservado).
   - Falha de criação → escrever em `## Próximos` do `backlog` linha descrevendo o motivo concreto, discriminado pela stderr do `git worktree add`:

     | Detecção (stderr regex) | Linha do backlog |
     |---|---|
     | `fatal: invalid reference: <nome>` (branch inexistente / digitação errada / refs não-fetchadas) | `branch <nome> referenciada em **Branch:** do plano <slug> não existe — verificar nome ou rodar git fetch antes de re-executar` |
     | `fatal: '<nome>' is already used by worktree at '<path>'` (branch checked out em outro worktree) | `branch <nome> referenciada em **Branch:** do plano <slug> está checked out em <path> — fazer checkout de outra branch lá antes de re-executar` (`<path>` literal extraído da stderr) |
     | `fatal: '.worktrees/<slug>' already exists` (diretório existe sem registro git — race com sessão paralela ou execução interrompida que escapou da pré-condição 4) | `diretório .worktrees/<slug>/ existe mas não está registrado como worktree git — remover manualmente antes de re-executar` |
     | Demais falhas | `falha em git worktree add para <nome> do plano <slug>: <stderr>` (operador investiga manual) |

     Todos os casos: informar; parar. Papel `backlog` = "não temos" → só informar.

2. **Replicar gitignored essenciais.** `.worktreeinclude` existe → ler e copiar cada path para a worktree (cópia, não symlink — isolamento real). Formato: 1 path por linha relativo à raiz do repo; `#` para comentário; linhas em branco ignoradas; globs são roadmap (hoje só paths literais). `.worktreeinclude` ausente → skip silente (warning já capturado na detecção pré-loop quando aplicável).

3. **Sincronizar e baseline.** `cd` na worktree. Sincronizar dependências com o gerenciador idiomático da stack (`uv sync`, `npm ci`, `cargo fetch`, `mvn install`, ...) — stack inferida pelo marker do projeto. Rodar `test_command` resolvido como baseline em background com `Monitor` para streamar stdout. Falhar (install ou baseline vermelho) → escrever linha descritiva em `## Próximos` do `backlog` (ex.: `baseline vermelho na worktree de <slug> — investigar`); informar; parar. Papel `backlog` = "não temos" → só informar. `test_command` = "não temos" + plano com `## Verificação end-to-end` → baseline é inspeção textual dessa seção.

### 2. Loop por bloco de `## Arquivos a alterar`

**Em modo runbook:** itens 3-4 (escolher revisor + aplicar correções) substituídos por gate de confirmação por bloco; item 5 (micro-commit) pulado; ver "## Modo runbook" acima para a mecânica completa incluindo materialização de capturas no `Falhou`.

**Antes do primeiro bloco:** capturar `**Linha do backlog:** <texto>` do `## Contexto` se presente — usado pelo passo 3.4 para adicionar em `## Concluídos` no done. Plano sem campo, papel `backlog` "não temos" → skip silente (vale aqui e no passo 3.4).

**Captura automática.** Três modos:
- **Pré-loop:** warnings detectados antes da worktree (alinhamento dirty, `.worktreeinclude` ausente, credencial não coberta, escopo divergente, cobertura ausente — ver "Detecção de warnings pré-loop" acima) já são classificados como Aviso/Backlog/Validação na detecção; os de Backlog e Validação alimentam a lista materializada no passo 3.5. Aviso informativo é reportado in situ e não alimenta a lista.
- **Imediata (in situ):** bloqueios em pré-condições 3/4 e passo 1 (baseline vermelho, worktree órfã, falha de setup) escrevem captura no `backlog` antes de parar — mecânica in situ.
- **Deferida:** durante passos 2 e 3.2, cada captura emergente cria `TaskCreate` com marker `[capture:validacao] <linha>` ou `[capture:backlog] <linha>` no subject (per [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (c)). Materialização em §3.5.

**Linguagem ubíqua repassada ao reviewer.** Se o `## Contexto` do plano traz `**Termos ubíquos tocados:** <Termo> (<categoria>), ...`, esse subset entra como contexto da invocação do reviewer no bloco — `/run-plan` não relê `ubiquitous_language` em runtime; o plano é o ponto único de transferência entre alinhamento e execução. Plano sem a linha = mudança não toca domínio = nada a carregar.

**Decisões absorvidas repassadas ao reviewer ([ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (d)).** Se o body do plano contém seção `## Decisões absorvidas` (mirror do bloco do commit message, escrito por `/triage` step 5), o conteúdo da seção entra como contexto adicional da invocação do reviewer no bloco — uniform protocol: passa a **todos** os reviewers invocados (code/doc/qa/security), não só ao `code-reviewer`. Plano sem a seção = nada a passar (skip silente).

**Instrução de `Read` antes de análise no prompt do reviewer.** Ao compor o prompt do reviewer escolhido para o bloco, seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/reviewer-invocation-read.md` — instrução defensiva que força refresh do arquivo alvo via `Read` antes da análise (resiliência contra stale-view por timing Edit → Agent).

**Instrumentação de progresso (ADR-010).** Loop por bloco e sub-passos do gate final são instrumentados via `Task` por unidade (bloco do §2; sub-passos do §3 cujas condições de execução disparam). Lifecycle padrão `pending` → `in_progress` → `completed`. Plano de bloco único E gate com ≤1 sub-passo efetivo → skip silente.

Para cada subseção do plano (geralmente um bloco por arquivo ou agrupamento lógico):

1. **Implementar** as mudanças.
2. **Rodar `test_command`** uma vez no fim do bloco. "Não temos" → aplicar verificação textual do plano.
3. **Escolher revisor** lendo anotação `{reviewer: ...}` no header. Single-reviewer é o caso normal. Hierarquia default mais-específico-vence (per [ADR-062](../../docs/decisions/ADR-062-criar-subagent-prompt-reviewer.md) § Pattern de dispatch):
   - Sem anotação → default `code-reviewer`.
   - **Exceção doc-only narrow** (per ADR-062): paths do bloco **não-vazios** e todos em `agents/*.md` ∪ `skills/**/SKILL.md` ∪ `docs/plans/*.md` → default vira `prompt-reviewer`.
   - **Exceção doc-only ampla**: paths do bloco **não-vazios** e todos com extensão `.md`/`.rst`/`.txt` fora dos paths acima → default vira `doc-reviewer` (bloco vazio, path sem extensão, ou bloco misto entre código + doc caem na regra default `code-reviewer`).
   - `{reviewer: code|qa|security|doc|prompt}` → agent correspondente (project-level `.claude/agents/<nome>.md` sobrescreve via convenção Claude Code).
   - Combinações (`{reviewer: code,qa}`, `{reviewer: code,doc}`, etc.) → exceção rara: invoca todos os listados, agregando relatórios. Útil quando o mesmo diff genuinamente merece olhares de eixos diferentes que não cabem em blocos separados.
   - Exemplos: `### Bloco 1 — auth.py {reviewer: security}`; `### Bloco 2 — README {reviewer: doc}`; `### Bloco 3 — agents/foo.md` (sem anotação → `prompt-reviewer` per exceção narrow).
4. **Aplicar correções** dos revisores antes de prosseguir.
5. **Micro-commit** seguindo a convenção do projeto (ver `docs/philosophy.md` → "Convenção de commits"; default canonical Conventional Commits em inglês). **Um commit por bloco**. Evitar `--amend`/rebase — micro-commits revertíveis são o ponto. Exceção localizada: corrigir o último commit ainda dentro do bloco corrente (typo, arquivo esquecido, footer faltando). Commits de blocos já fechados ficam intocados. **Modo local** (`paths.plans_dir: local`): mensagem de commit não cita slug do plano (regra de não-referenciar, ADR-047); papel `backlog` em modo `local` análogo (não citar texto da linha).

### 3. Gate final

**Em modo runbook:** pular §3.1 (gate automático), §3.2 (validação manual centralizada — já intercalada por bloco), §3.3 (sanity check docs — runbook não toca docs user-facing do projeto), §3.7 (publicação — sem branch de feature). Aplicar §3.4 (Concluídos via `**Linha do backlog:**` — operador edita `backlog` no working tree principal; commit do bloco extra segue padrão canonical Conventional Commits), §3.5 (captura automática para Tasks acumuladas que não foram materializadas via `Falhou`) e §3.6 (declarar done).

1. **Gate automático.** Rodar `test_command` em background com `Monitor` para streamar stdout. "Não temos" → inspeção textual de `## Verificação end-to-end`.

2. **Validação manual.** Plano com `## Verificação manual` → ler passos ao operador e cutucar via `AskUserQuestion` (header `Validação`) com opções `Validei (Recommended)` / `Falhou — descrever`. Sem resposta positiva (Validei OU descrição não-vazia em Other), não fechar. Durante o diálogo, observar gatilhos de captura (passo 3.5) sem interromper.

3. **Sanity check de docs user-facing.** Antes do done:

   | Condição | Skip silente? | Ação |
   |---|---|---|
   | Plano lista `.md` user-facing em `## Arquivos a alterar` E diff o tocou | sim | — |
   | `## Resumo da mudança` sem superfície user-facing | sim | — |
   | Grep dos identificadores tocados nos paths user-facing retorna vazio | sim (empírico) | — |
   | Caso contrário | não | Listar referrers concretos como prosa informativa, então cutucar enum `Docs` |

   **Definições.** *User-facing* (positive list): `README*`, `CHANGELOG*`, `install.md`, `docs/install.md`, `docs/guides/**`. Arquivos `.md` de implementação (skills, agents, hooks, philosophy) **não** ativam o primeiro skip. *Superfície user-facing*: CLI/flag nova, env var nova, endpoint novo, comportamento perceptível, integração externa, instalação/configuração. *Identificadores tocados* = filenames base sem extensão de `## Arquivos a alterar` (ex.: `skills/triage/SKILL.md` → `triage`) + nomes de skill/agent/comando textualmente presentes no `## Resumo da mudança` (ex.: `/triage`, `code-reviewer`).

   **Mecânica da cutucada.** Antes do enum, listar os referrers concretos do grep como prosa informativa (`<path>:<linha>: <trecho>`) — não candidatos genéricos. Grep é lexical: matches espúrios viram cutucada legítima absorvida pelo `Consistente`. `CHANGELOG` fica fora (responsabilidade do `/release`). `AskUserQuestion` (header `Docs`) com opções `Consistente` / `Listar arquivos a atualizar` (sem `Recommended` — heurística de gatilho aponta gap potencial; ambos os caminhos são igualmente prováveis). `description` da segunda diz "use Other para informar os paths". Resposta `Consistente` → segue para o passo 3.4. Resposta com listagem (Other) → bloco extra (implementar → `test_command` → revisor `code` → micro-commit) antes do done.

4. **Registro em Concluídos.** `**Linha do backlog:**` capturada no passo 2 → **mover** para o topo de `## Concluídos`: se a linha existe em `## Próximos` (matching texto exato), remover de lá e adicionar em Concluídos; se não existe em Próximos (operador registrou via /triage caminho-com-plano sob ADR-049 § Decisão (a), que não grava no BACKLOG), apenas adicionar em Concluídos. Informar, aplicar como **bloco extra unificado** (atualizar `backlog` + remover bloco `## Status` do plan body → revisor `code` cobre os 2 edits → micro-commit único) **antes** do passo 3.5. Per [ADR-060](../../docs/decisions/ADR-060-heuristica-completude-planos-via-status.md) § Wiring nas skills, mesmo commit edita os 2 arquivos como sequência atômica — bloco `## Status` (criado por `/triage` step 4) chega ao fim do ciclo aqui; plano transiciona para "git/forge canonical" via `archive/` presence + linha em `## Concluídos`. Plano sem campo `## Status` (legacy ou hand-written), remover é noop; plano sem `**Linha do backlog:**`, papel `backlog` "não temos" → skip silente. Em modo `local` (`paths.backlog: local`), transição opera sobre `.claude/local/BACKLOG.md` — matching textual e move idênticos ao caso canonical; mensagem de commit do bloco extra não cita o texto da linha (regra de não-referenciar).

   **Em modo `forge`** (`paths.backlog: forge`, per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md)): `**Linha do backlog:**` carrega `#<número>: <título>` (per ADR-058 § (c), gravado pelo `/triage` step 4 em modo forge). Extrair `<número>` via regex `#(\d+):`. Seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`; output `no-detection` ou `unsupported-host` → **parar com erro explícito** orientando setup (`gh auth login` / `glab auth login` / `dnf install jq`) ou declarar `paths.backlog: null` ou path canonical (policy do caller per ADR-058 § (d)). Disparar cutucada `AskUserQuestion` (header `Forge`, opções `Aplicar no forge` (Recommended) / `Cancelar (não aplicar)`) — `description` da opção `Aplicar no forge` carrega o(s) comando(s) concreto(s) (ex.: `gh issue close #<número> --reason completed --comment '<glosa>'`). Confirmação → em `gh`, `gh issue close #<número> --reason completed --comment "<glosa>"` (close + comentário num único comando); em `glab`, dois comandos sequenciais — `glab issue note <número> --message "<glosa>"` então `glab issue close <número>` (CLI assimétrica: `glab issue close` não aceita `--comment`). Glosa pode citar PR # do done ou commit hash. **Sem bloco extra** (sem `atualizar backlog → revisor → micro-commit`) — mutação é remota, sem commit local; comentário no `issue close` é o registro editorial (per ADR-058 § (h) "valor editorial via comentários em issues fechadas"). Cancelamento → operador informado, segue para §3.5 sem mutação remota. **Remoção do bloco `## Status` do plan body** (per ADR-060 § Wiring nas skills) **continua aplicando em modo forge** como edit isolado (revisor `code` → micro-commit) — o "sem bloco extra" desta cláusula se refere apenas à parte do `backlog` (mutação remota substitui mark local em `## Concluídos`); plan body permanece local em ambos os modos.

5. **Captura automática de imprevistos.** Materializar via leitura de `TaskList` filtrada por marker `[capture:*]` (per [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (c)). Para cada Task pendente, escrever no destino correto conforme tipo + modo do role `backlog`:

   - **`[capture:validacao]`** → `## Pendências de validação` no plano corrente (criar se não existe). Inalterado em ambos os modos do backlog — plano é local em `<plans_dir>`.
   - **`[capture:backlog]` em modo arquivo** (canonical ou `local`) → `## Próximos` do papel `backlog`.
   - **`[capture:backlog]` em modo `forge`** (`paths.backlog: forge`, per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md)) → escrever bullet em `## Capturas backlog em modo forge` do plano corrente (criar seção se não existe; append no fim). Sem cutucada na materialização individual — paralelo a `[capture:validacao]`. Cutucada batched-com-seleção dispara após esta etapa (ver "Cutucada batched-com-seleção em modo forge" abaixo).

   Após escrita, marcar Tasks como `completed` via `TaskUpdate` (signal materializado em local visível; lifecycle 2-estados ADR-049 § Decisão (c) preservado em todos os modos). TaskList sem matches do marker → skip silente (nenhuma captura emergiu na execução).

   **Gatilhos pré-loop** (capturados antes da worktree, ver "Detecção de warnings pré-loop"):
   - **Alinhamento dirty** — apenas aviso informativo; **não** alimenta esta lista.
   - **`.worktreeinclude` ausente + gitignored em uso** → entrada de Backlog.
   - **Credencial não coberta** → entrada de Validação.
   - **Escopo divergente** → entrada de Validação.
   - **Cobertura ausente** → entrada de Validação.

   **Gatilhos durante execução (passo 2):**
   - **Falha contornada** — `test_command` (ou verificação textual) falha e o agente segue contornando (skip de teste, retry frágil, fallback ad-hoc) sem solucionar a causa-raiz.
   - **Finding fora-do-escopo** — reviewer levanta problema real fora do bloco/plano corrente.
   - **Hook bloqueando** — hook do plugin retorna exit ≠ 0 sinalizando gap real; agente pivota e segue.

   *(Bloqueios de pré-condição 3/4 e passo 1 — baseline vermelho, worktree órfã, falha de setup — geram captura imediata in situ; não alimentam esta lista.)*

   **Gatilhos durante validação manual (passo 3.2):**
   - **Divergência do plano** — operador reporta comportamento divergente do esperado por `## Verificação manual`.
   - **Bug colateral** — operador menciona bug não relacionado ao gate corrente.

   **Classificação no momento da captura:**
   - **Validação** (pré-requisito para done) — cenário não exercitado, divergência do plano, gap de verificação, reviewer pulado sem justificativa. Mensagem: `"capturei para verificação: <linha>"`. Destino: `## Pendências de validação` no plano corrente (criar se não existe).
   - **Backlog** (independente do gate) — feature/fix/doc/regra nova, bug colateral, finding fora-do-escopo, gap de hook. Mensagem: `"capturei no backlog: <linha>"`. Destino: `## Próximos` do papel `backlog`.

   Sinal explícito do operador vence a classificação automática ("registra no backlog X" / "registra no plano Y" / "descarta esse" — operador pode descartar entre o aviso e a materialização).

   **Materialização no gate final:**
   - Ambas as listas vazias → skip silente.
   - Lista de validação não-vazia → escrever em `## Pendências de validação` do plano (uma linha por item).
   - Lista de backlog em **modo arquivo** não-vazia → escrever em `## Próximos` do `backlog`; aplicar consolidação (releitura → flag de duplicatas/obsolescência → sem flags skip silente; com flags enum `Backlog` único — algoritmo completo em `/triage` SKILL → passo 4 sub-fluxo "Consolidação (quando há edit em `backlog`)"). As partes não-vazias entram em **um único** bloco extra (revisor `code` + micro-commit). Sem confirmação adicional sobre as capturas — operador foi informado a cada detecção.
   - Lista de backlog em **modo `forge`** não-vazia → bullets já materializados na seção `## Capturas backlog em modo forge` do plano (escrita inline acima); **sem bloco extra próprio** para essas escritas — vão no commit que materializou as edições do plano corrente. Cutucada batched-com-seleção dispara após (ver bloco seguinte).
   - Caso especial: papel `backlog` = "não temos" → lista de backlog vira relato final (sem registro persistido); lista de validação grava no plano sempre.

   **Cutucada batched-com-seleção em modo `forge`** (per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md) § (e) 2ª instância do sub-caso editorial — forma batched). Se esta execução escreveu ≥1 bullet em `## Capturas backlog em modo forge` do plano corrente, disparar **uma única** cutucada `AskUserQuestion` após materialização e antes do passo 3.6:

   - Header: `Forge`
   - Opções: `Aplicar todas` (Recommended) / `Selecionar quais` (Other) / `Manter como pendentes`
   - `description` da opção `Aplicar todas`: `"Criar N issues no forge — gh/glab issue create para cada bullet de ## Capturas backlog em modo forge"` (N = contagem).
   - `description` da opção `Selecionar quais`: `"Escolher subset via Other (ex.: 'bullets 1 e 3'); restante permanece como pendente"`.
   - `description` da opção `Manter como pendentes`: `"Bullets permanecem em ## Capturas backlog em modo forge para revisão futura; sem mutação remota"`.

   **`Aplicar todas`:** seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`; output `no-detection`/`unsupported-host` → **parar com erro explícito** orientando setup (`gh auth login` / `glab auth login` / `dnf install jq`) ou declarar `paths.backlog: null`/path canonical (policy do caller per ADR-058 § (d)). Bullets permanecem intactos como pendentes na seção. Para cada bullet: extrair `<linha>` (texto após `- `); montar contexto auto-gerado (template 3 linhas: `Capturado por /run-plan §3.5 do plano <slug>.` + `Origem: <bloco | passo | warning pré-loop conforme rastreável>.` + `Linha: <linha literal>`); executar `gh issue create -t "<linha>" -b "<contexto>" --json number,url` (gh) ou `glab issue create -t "<linha>" -d "<contexto>"` (glab). Substituir bullet no plano por `- #<número>: <linha>` (ref à issue criada — auditabilidade pós-fact). Falha mid-loop (rate limit, network drop) → parar; reportar status (bullets aplicados como refs vs pendentes restantes); operador re-invoca ou aplica manualmente.

   **`Selecionar quais`:** operador descreve subset em prosa via Other (ex.: "aplicar bullets 1 e 3, manter os outros como pendentes"). Aplicar subset com mesma mecânica de `Aplicar todas`. Bullets restantes permanecem intactos como pendentes na seção.

   **`Manter como pendentes`:** seção `## Capturas backlog em modo forge` permanece intacta no plano. Sem criação de issues. Operador endereça depois manualmente ou via futura invocação de `/curate-backlog`. Paralelo semântico a `## Pendências de validação` (gate único editorial não-mutativo no done).

   Cutucada bate no done (gate único editorial paralelo a §3.4), não na fase pré-loop nem na materialização individual de Task — ADR-002 § Decisão "skill nunca interrompe por cutucada na fase pré-loop" preservado por construção. Justificativa de forma batched (vs cutucada granular por mutação das 4 superfícies primárias de ADR-058 § (e)) em [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md) § (e) 2ª instância: signal acumula em múltiplos passos do `/run-plan`; cutucada granular geraria N cliques.

6. **Declarar done.** No parágrafo final do done (após resumo dos blocos), incluir 1 linha informativa de extension hint imediatamente antes do marker canonical, em parágrafo separado: `Considere /session-audit antes de fechar a sessão pra verificar captura pendente.` Hint é não-bloqueante (texto informativo, não `AskUserQuestion`); operador decide invocar livre. Em seguida imprimir literalmente o marker canonical `Plan done. [PRAGMATIC: plan-done]` em linha própria. Marker é mecânica-universal igual a hooks — **não traduz por idioma do projeto consumidor**. Pattern para plugins terceiros que queiram reagir ao fim de `/run-plan` via Claude Code `Stop` event: grep marker em `transcript_path` (recebido via stdin payload do hook). Não há outro mecanismo nativo de detecção; este marker é opt-in contract publicado pelo toolkit.

7. **Sugestão de publicação.** Remote configurado (`git remote get-url origin` retorna sucesso) → `AskUserQuestion` (header `Publicar`) com opções montadas conforme o modo:
   - **Modo `local`** (`plans_dir: local`) **com campo `**Branch:**` ausente**: `Renomear branch antes (Recommended)` / `Push` / `Push + abrir PR/MR` / `Nenhum`. `Renomear branch antes` emite `git branch -m <novo-nome>` como sugestão (`description` informa: "branch name é metadata pública — não aparece em mensagem de commit nem em PR --fill, mas o nome é visível ao push") e encerra; operador roda o `git branch -m` manual e re-invoca para escolher Push.
   - **Modo `local`** com campo `**Branch:**` **presente**: enum cai para `Push (Recommended)` / `Push + abrir PR/MR` / `Nenhum` (idêntico ao modo canonical) — branch pré-existente já carrega decisão de exposição do operador (cf. [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (b) § Modo local; oferta de rename inverteria a intenção).
   - **Modo canonical**: `Push (Recommended)` / `Push + abrir PR/MR` / `Nenhum`.

   Comportamento das opções de push (idêntico nos dois modos):
   - `Push` → `git push -u origin <branch-atual>`.
   - `Push + abrir PR/MR` → `git push -u origin <branch-atual>`; em seguida auto-detect do forge:
     1. **Detect forge:** seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`. Output `gh` ou `glab` → segue para etapa 2; `no-detection` ou `unsupported-host` → fallback textual (push aconteceu; operador abre PR/MR pela UI web ou CLI específica do forge); skip etapas 2-3.
     2. **Gate de confirmação:** montar comando (`gh pr create --fill --base <branch-principal>` ou `glab mr create --fill --target-branch <branch-principal>`). Branch principal lido de `git symbolic-ref refs/remotes/origin/HEAD`; saída não-zero → fallback `main`. Apresentar via `AskUserQuestion` (header `Forge`) com opções `Executar` / `Pular`. Decline → skip silente; o comando exibido no gate é a referência para cópia manual.
     3. **Executar:** `Bash` com o comando montado. Saída zero → reportar saída do CLI (URL do PR/MR) e seguir. Saída não-zero → reportar erro literal e parar; push já aconteceu, operador resolve manual.
   - `Nenhum` → encerrar sem ação.

   Sem remote → skip silente.

A skill termina na worktree com a branch da feature após oferecer publicação.

**Cutucada de descoberta.** Antes de encerrar, executar a cutucada conforme `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md`.

## O que NÃO fazer

- Não declarar done sem confirmação humana **quando o plano exige validação manual**.
- Não pular revisor, mesmo em bloco trivial.
- Não interpretar `{revisor: ...}` (PT) — schema canônico é `{reviewer: ...}` em inglês. Recusar antes de começar o bloco com mensagem indicando bloco e anotação ofensora.
- Não contornar plano sujo copiando o conteúdo manualmente para a worktree — bloqueio na pré-condição 2 existe para forçar commit no branch correto.
- Não emitir comando destrutivo no working tree principal (ex.: `git reset --hard`, `git worktree remove`) para contornar falha de `git worktree add` no §1.1. A doutrina é parar e escrever no backlog — CLAUDE.md global exige confirmação explícita para ações de blast-radius compartilhado.
- Não silenciar warnings detectados pré-loop com base em estado prévio do `.worktreeinclude` — quando o plano corrente exige `## Verificação manual` e há credencial gitignored não coberta, a captura em Validação é obrigatória, mesmo se o operador declarou anteriormente `paths.worktreeinclude: null` ou "não preciso".
- Não executar push sem confirmação explícita via enum `Publicar`.
- Não executar fluxo canonical (worktree + micro-commits + reviewer per bloco) em plano com `**Modo:** runbook` — modo runbook reflete que ambiente é o escopo, não o repo (per [ADR-049](../../docs/decisions/ADR-049-execucao-run-plan-consolidado.md) § Decisão (d)); aplicar canonical corrompe working tree silenciosamente (worktree dentro do FS migrado, commits artificiais que rollback btrfs sobrescreve, reviewer sobre diff inexistente).
