---
name: run-plan
description: Executa plano de docs/plans/<slug>.md em worktree isolada, com micro-commits, revisor por bloco e gate de validação manual. Use quando há plano pronto e o operador autorizou implementar.
disable-model-invocation: true
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

1. **Plano existe e tem `## Arquivos a alterar`** (papel: `plans_dir`, default: `docs/plans/`). Esqueleto canônico em `${CLAUDE_PLUGIN_ROOT}/templates/plan.md`.

2. **Estado git do plano** (`git status --porcelain`):
   - **Bloquear** se `<plans_dir>/<slug>.md` está modificado/untracked. Worktree é criada do HEAD e não veria o plano. Mensagem: commitar antes (ou usar `/triage`, que já propõe commit).

3. **Gate automático verde no branch atual.** Default: `make test`. Variante: `test_command` no CLAUDE.md. Se canonical ausente E operador não declarou `test_command: null`, perguntar uma vez (oferta única de memorização). Projetos sem suite (`test_command: null` E plano traz `## Verificação end-to-end`) → baseline vira inspeção textual dessa seção. Gate falha → escrever em `## Próximos` do papel `backlog` linha tipo `baseline vermelho no branch ao iniciar /run-plan <slug> — investigar`; informar; parar. Papel `backlog` = "não temos" → só informar.

4. **Worktree `.worktrees/<slug>/` não existe.** Se existir → escrever em `## Próximos` linha tipo `worktree .worktrees/<slug> existe de run anterior — remover antes de re-executar`; informar; parar. Papel `backlog` = "não temos" → só informar.

## Detecção de warnings pré-loop

Antes da worktree ser criada, detectar warnings de qualidade-de-mudança e classificá-los nos trilhos do passo 3.5 (Captura automática) — sem perguntar ao operador (ADR-002). Sem warnings detectados → silêncio total; skill segue para a worktree.

| Warning | Detecção | Trilho |
|---|---|---|
| **Alinhamento dirty** | papéis de alinhamento (`backlog`, `ubiquitous_language`, `design_notes`, arquivo sob `decisions_dir`) têm alterações uncommitted no `git status --porcelain` | **Aviso informativo** in situ: `"aviso: alinhamento uncommitted — <lista de arquivos>; reviewer pode não ver invariantes/ADRs uncommitted"`. Skill segue. Não alimenta a lista de captura. |
| **`.worktreeinclude` ausente** | raiz do repo tem gitignored típico em uso (`.env`, dbs locais, fixtures não versionadas) E `.worktreeinclude` não existe E operador não declarou `paths.worktreeinclude: null` | **Backlog**: `"capturei no backlog: criar .worktreeinclude listando <gitignored detectados> para replicação em worktrees"`. Alimenta a lista. |
| **Credencial não coberta** | plano tem `## Verificação manual` E raiz tem credencial gitignored típica (`.env`, `*.local.yaml`, `secrets.*`) não coberta pelo `.worktreeinclude` aplicado (quando existe) | **Validação**: `"capturei para verificação: cenário de validação manual não exercitado por falta da credencial <nome> na worktree"`. Alimenta a lista. |
| **Escopo divergente** | `## Contexto` ou `## Resumo da mudança` cita superfície externa (config, env, infra, deploy, webhook, integração externa, `.env`) ausente em `## Arquivos a alterar` | **Validação**: `"capturei para verificação: superfície externa <X> mencionada em Contexto/Resumo mas ausente em ## Arquivos a alterar — cenário não exercitado"`. Alimenta a lista. |

Estado prévio "não preciso" do `.worktreeinclude` **silencia** a captura de Backlog mas **não silencia** o gatilho cruzado de credencial — contexto mudou (plano corrente exige `## Verificação manual`).

Bloqueios (plano sujo, push esquecido, baseline vermelho, worktree órfã) ficam fora desta detecção — continuam parando a skill in situ com captura imediata.

## Passos

### 1. Setup da worktree

1. `git worktree add .worktrees/<slug> -b <slug>` a partir do branch atual.

2. **Replicar gitignored essenciais.** `.worktreeinclude` existe → ler e copiar cada path para a worktree (cópia, não symlink — isolamento real). Formato: 1 path por linha relativo à raiz do repo; `#` para comentário; linhas em branco ignoradas; globs são roadmap (hoje só paths literais). `.worktreeinclude` ausente → skip silente (warning já capturado na detecção pré-loop quando aplicável).

3. **Sincronizar e baseline.** `cd` na worktree. Sincronizar dependências com o gerenciador idiomático da stack (`uv sync`, `npm ci`, `cargo fetch`, `mvn install`, ...) — stack inferida pelo marker do projeto. Rodar `test_command` resolvido como baseline. Falhar (install ou baseline vermelho) → escrever linha descritiva em `## Próximos` do `backlog` (ex.: `baseline vermelho na worktree de <slug> — investigar`); informar; parar. Papel `backlog` = "não temos" → só informar. `test_command` = "não temos" + plano com `## Verificação end-to-end` → baseline é inspeção textual dessa seção.

### 2. Loop por bloco de `## Arquivos a alterar`

**Antes do primeiro bloco:** capturar `**Linha do backlog:** <texto>` do `## Contexto` se presente — usado pelo passo 3.4 para adicionar em `## Concluídos` no done. Plano sem campo, papel `backlog` "não temos" → skip silente (vale aqui e no passo 3.4).

**Captura automática.** Três modos:
- **Pré-loop:** warnings detectados antes da worktree (alinhamento dirty, `.worktreeinclude` ausente, credencial não coberta, escopo divergente — ver "Detecção de warnings pré-loop" acima) já são classificados como Aviso/Backlog/Validação na detecção; os de Backlog e Validação alimentam a lista materializada no passo 3.5. Aviso informativo é reportado in situ e não alimenta a lista.
- **Imediata (in situ):** bloqueios em pré-condições 3/4 e passo 1 (baseline vermelho, worktree órfã, falha de setup) escrevem captura no `backlog` antes de parar — mecânica in situ.
- **Deferida:** durante passos 2 e 3.2, agente acumula gatilhos e materializa no gate final (passo 3.5).

**Linguagem ubíqua repassada ao reviewer.** Se o `## Contexto` do plano traz `**Termos ubíquos tocados:** <Termo> (<categoria>), ...`, esse subset entra como contexto da invocação do reviewer no bloco — `/run-plan` não relê `ubiquitous_language` em runtime; o plano é o ponto único de transferência entre alinhamento e execução. Plano sem a linha = mudança não toca domínio = nada a carregar.

Para cada subseção do plano (geralmente um bloco por arquivo ou agrupamento lógico):

1. **Implementar** as mudanças.
2. **Rodar `test_command`** uma vez no fim do bloco. "Não temos" → aplicar verificação textual do plano.
3. **Escolher revisor** lendo anotação `{reviewer: ...}` no header. Single-reviewer é o caso normal:
   - Sem anotação → default `code-reviewer`. **Exceção**: paths do bloco **não-vazios** e todos com extensão `.md`/`.rst`/`.txt` → default vira `doc-reviewer` (bloco vazio, path sem extensão, ou bloco misto caem na regra default).
   - `{reviewer: code|qa|security|doc}` → agent correspondente (project-level `.claude/agents/<nome>.md` sobrescreve via convenção Claude Code).
   - Combinações (`{reviewer: code,qa}`, `{reviewer: code,doc}`, etc.) → exceção rara: invoca todos os listados, agregando relatórios. Útil quando o mesmo diff genuinamente merece olhares de eixos diferentes que não cabem em blocos separados.
   - Exemplos: `### Bloco 1 — auth.py {reviewer: security}`; `### Bloco 2 — README {reviewer: doc}`.
4. **Aplicar correções** dos revisores antes de prosseguir.
5. **Micro-commit** seguindo a convenção do projeto (ver `docs/philosophy.md` → "Convenção de commits"; default canonical Conventional Commits em inglês). **Um commit por bloco**. Evitar `--amend`/rebase — micro-commits revertíveis são o ponto. Exceção localizada: corrigir o último commit ainda dentro do bloco corrente (typo, arquivo esquecido, footer faltando). Commits de blocos já fechados ficam intocados.

### 3. Gate final

1. **Gate automático.** Rodar `test_command` integralmente. "Não temos" → inspeção textual de `## Verificação end-to-end`.

2. **Validação manual.** Plano com `## Verificação manual` → ler passos ao operador, **aguardar confirmação explícita** ("ok, valido"). Sem confirmação, não fechar. Durante o diálogo, observar gatilhos de captura (passo 3.5) sem interromper.

3. **Sanity check de docs user-facing.** Antes do done:
   - **Skip** se o plano já listou `.md` user-facing (`README*`, `CHANGELOG*`, `install.md`, `docs/install.md`, `docs/guides/**`) em `## Arquivos a alterar` E o diff agregado o tocou. Arquivos `.md` de implementação (skills, agents, hooks, philosophy) **não** ativam o skip.
   - **Skip** se `## Resumo da mudança` não menciona superfície user-facing (CLI/flag nova, env var nova, endpoint novo, comportamento perceptível, integração externa, instalação/configuração).
   - **Cutucar** caso contrário em **prosa livre** (não enum — a maioria das respostas reais é uma listagem de arquivos a atualizar, território de "Other"). Citar a superfície inferida e os candidatos típicos (README, install, docs internas) e pedir resposta livre — `"consistente"` ou listagem dos arquivos a atualizar. `CHANGELOG` fica fora (responsabilidade do `/release`). Resposta listando atualizações → bloco extra (implementar → `test_command` → revisor `code` → micro-commit) antes do done.

4. **Registro em Concluídos.** `**Linha do backlog:**` capturada no passo 2 → **adicionar** ao topo de `## Concluídos`, informar, aplicar como **bloco extra** (atualizar `backlog` → revisor `code` → micro-commit) **antes** do passo 3.5. Sem origem em outra seção (state vivo é a worktree/branch corrente, ADR-004). Plano sem campo, papel `backlog` "não temos" → skip silente.

5. **Captura automática de imprevistos.** Materializar a lista mantida desde o passo 2 (e desde a fase pré-loop quando aplicável).

   **Gatilhos pré-loop** (capturados antes da worktree, ver "Detecção de warnings pré-loop"):
   - **Alinhamento dirty** — apenas aviso informativo; **não** alimenta esta lista.
   - **`.worktreeinclude` ausente + gitignored em uso** → entrada de Backlog.
   - **Credencial não coberta** → entrada de Validação.
   - **Escopo divergente** → entrada de Validação.

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
   - Lista de backlog não-vazia → escrever em `## Próximos` do `backlog`; aplicar consolidação (releitura → flag de duplicatas/obsolescência → sem flags skip silente; com flags enum `Backlog` único — algoritmo completo em `/triage` SKILL → passo 5).
   - As partes não-vazias entram em **um único** bloco extra (revisor `code` + micro-commit). Sem confirmação adicional sobre as capturas — operador foi informado a cada detecção.
   - Caso especial: papel `backlog` = "não temos" → lista de backlog vira relato final (sem registro persistido); lista de validação grava no plano sempre.

6. **Declarar done.**

7. **Sugestão de publicação.** Remote configurado (`git remote -v`) → enum (header `Publicar`):
   - `Push` → `git push -u origin <branch-atual>`.
   - `Push + sugerir PR/MR` → `git push -u origin <branch-atual>`; em seguida imprimir instrução textual neutra com exemplos por forge (ex.: `gh pr create` para GitHub, `glab mr create` para GitLab, ou abrir manualmente na UI web). Skill **não** executa o comando do forge.
   - `Nenhum` → encerrar sem ação.

   Sem remote → skip silente.

A skill termina na worktree com a branch da feature após oferecer publicação.

## O que NÃO fazer

- Não declarar done sem confirmação humana **quando o plano exige validação manual**.
- Não pular revisor, mesmo em bloco trivial.
- Não interpretar `{revisor: ...}` (PT) — schema canônico é `{reviewer: ...}` em inglês. Recusar antes de começar o bloco com mensagem indicando bloco e anotação ofensora.
- Não contornar plano sujo copiando o conteúdo manualmente para a worktree — bloqueio na pré-condição 2 existe para forçar commit no branch correto.
- Não silenciar warnings detectados pré-loop com base em estado prévio do `.worktreeinclude` — quando o plano corrente exige `## Verificação manual` e há credencial gitignored não coberta, a captura em Validação é obrigatória, mesmo se o operador declarou anteriormente `paths.worktreeinclude: null` ou "não preciso".
- Não executar push sem confirmação explícita via enum `Publicar`.
- Não executar comando de abertura de PR/MR no forge — opção `Push + sugerir PR/MR` apenas imprime exemplos; abertura efetiva é decisão e ação do operador.
