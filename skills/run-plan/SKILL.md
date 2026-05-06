---
name: run-plan
description: Executa plano de docs/plans/<slug>.md em worktree isolada, com micro-commits, revisor por bloco e gate de validação manual. Use quando há plano pronto e o operador autorizou implementar.
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

Paths e comandos seguem a **Resolução de papéis** (ver `docs/philosophy.md`): default canonical → bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md → pergunta ao operador. Headers de plano são citados em PT-BR canonical (`## Arquivos a alterar`, `## Verificação end-to-end`, etc.); planos em outro idioma usam matching semântico (`## Files to change`, `## End-to-end verification`, ...).

Falha de qualquer pré-condição → parar e reportar.

1. **Plano existe e tem `## Arquivos a alterar`** (papel: `plans_dir`, default: `docs/plans/`).

2. **Estado git dos artefatos de alinhamento** (`git status --porcelain`):
   - **Bloquear** se `<plans_dir>/<slug>.md` está modificado/untracked. Worktree é criada do HEAD e não veria o plano. Mensagem: commitar antes (ou usar `/triage`, que já propõe commit).
   - **Bloquear** se `git log origin/<branch-atual>..HEAD` retornar commits E o arquivo do papel `backlog` tem linha em `## Em andamento` — sinal de que o triage com transição Próximos→Em andamento não foi empurrado. Mensagem: `git push` antes da worktree (evita merge artifact em BACKLOG.md no merge do PR).
   - **Cutucar** (não bloquear) se papéis de alinhamento (`backlog`, `ubiquitous_language`, `design_notes`, ou arquivo sob `decisions_dir`) têm alterações uncommitted — worktree perde esse contexto, reviewers podem não ver invariantes/ADRs assumidos pelo plano. Modo: enum (`AskUserQuestion`, header `Alinhamento`) com `Commitar agora` (skill aguarda) ou `Continuar mesmo assim` (skill segue, registrando aviso). Mostrar lista. Outras alterações uncommitted (código de exploração, debug) **não** geram aviso — operador isolou intencionalmente.

3. **Gate automático verde no branch atual.** Default: `make test`. Variante: `test_command` no CLAUDE.md. Se canonical ausente E operador não declarou `test_command: null`, perguntar uma vez (oferta única de memorização). Projetos sem suite (`test_command: null` E plano traz `## Verificação end-to-end`) → baseline vira inspeção textual dessa seção. Gate falha → escrever em `## Próximos` do papel `backlog` linha tipo `baseline vermelho no branch ao iniciar /run-plan <slug> — investigar`; informar; parar. Papel `backlog` = "não temos" → só informar.

4. **Worktree `.worktrees/<slug>/` não existe.** Se existir → escrever em `## Próximos` linha tipo `worktree .worktrees/<slug> existe de run anterior — remover antes de re-executar`; informar; parar. Papel `backlog` = "não temos" → só informar.

## Passos

### 1. Setup da worktree

1. `git worktree add .worktrees/<slug> -b <slug>` a partir do branch atual.

2. **Replicar gitignored essenciais:**
   - `.worktreeinclude` existe → ler e copiar cada path para a worktree (cópia, não symlink — isolamento real). Formato: 1 path por linha relativo à raiz do repo; `#` para comentário; linhas em branco ignoradas; globs são roadmap (hoje só paths literais).
   - Não existe E operador não declarou que não precisa → propor criação **uma vez por projeto** via enum (`AskUserQuestion`, header `Worktree`, `multiSelect: true`) listando gitignored em uso aparente (`.env`, dbs locais, fixtures não versionadas). Sem seleção → pular passo, avisar que baseline pode falhar por dependências locais ausentes.
   - **Gatilho cruzado de validação manual** (independe do estado prévio): plano tem `## Verificação manual` E raiz do repo tem gitignored típico de credencial/config local (`.env`, `*.local.yaml`, `secrets.*`) não coberto pelo `.worktreeinclude` aplicado → **cutucar** via enum (header `Credencial`, opções `Replicar agora` / `Seguir sem replicar`); citar nome da credencial e motivo (validação manual provavelmente exige serviço real). `Replicar agora` → adicionar ao `.worktreeinclude` (criar se necessário) e copiar. Estado prévio "não preciso" **não silencia** este gatilho — contexto mudou (plano corrente exige serviço real).

3. **Sincronizar e baseline.** `cd` na worktree. Sincronizar dependências com o gerenciador idiomático da stack (`uv sync`, `npm ci`, `cargo fetch`, `mvn install`, ...) — stack inferida pelo marker do projeto. Rodar `test_command` resolvido como baseline. Falhar (install ou baseline vermelho) → escrever linha descritiva em `## Próximos` do `backlog` (ex.: `baseline vermelho na worktree de <slug> — investigar`); informar; parar. Papel `backlog` = "não temos" → só informar. `test_command` = "não temos" + plano com `## Verificação end-to-end` → baseline é inspeção textual dessa seção.

### 2. Sanity check de escopo

Reler `## Contexto` e `## Resumo da mudança` do plano. Menção a superfície externa (configuração, ambiente, infraestrutura, compose, deploy, webhook, integração externa, `.env`) **ausente em `## Arquivos a alterar`** → **avisar** (cutucar, não bloquear) via enum (header `Escopo`) com `Continuar mesmo assim` / `Pausar para ajustar plano`; citar superfície detectada.

### 3. Loop por bloco de `## Arquivos a alterar`

**Antes do primeiro bloco:** capturar `**Linha do backlog:** <texto>` do `## Contexto` se presente. Linha em `## Próximos` do `backlog` → mover para `## Em andamento`, informar, aplicar edit antes do primeiro bloco (entra no commit do bloco 1). Plano sem campo, linha não localizada, papel `backlog` "não temos" → skip silente (vale aqui e no passo 4.4).

**Captura automática.** Dois modos:
- **Imediata (pre-loop):** bloqueios em pré-condições 3/4 e passo 1 (baseline vermelho, worktree órfã, falha de setup) escrevem captura no `backlog` antes de parar — mecânica in situ.
- **Deferida:** durante passos 3 e 4.2, agente acumula gatilhos e materializa no gate final (passo 4.5).

Para cada subseção do plano (geralmente um bloco por arquivo ou agrupamento lógico):

1. **Implementar** as mudanças.
2. **Rodar `test_command`** uma vez no fim do bloco. "Não temos" → aplicar verificação textual do plano.
3. **Escolher revisor** lendo anotação `{reviewer: ...}` no header:
   - Sem anotação ou `{reviewer: code}` → `code-reviewer`.
   - `{reviewer: qa}` ou `{reviewer: security}` → agent correspondente (project-level `.claude/agents/<nome>.md` sobrescreve via convenção Claude Code).
   - `{reviewer: code,qa,security}` → invocar **todos**, agregando relatórios.
   - Exemplo: `### Bloco 1 — auth.py {reviewer: security}`.
4. **Aplicar correções** dos revisores antes de prosseguir.
5. **Micro-commit** seguindo a convenção do projeto (ver `docs/philosophy.md` → "Convenção de commits"; default canonical Conventional Commits em inglês). **Um commit por bloco**. Evitar `--amend`/rebase — micro-commits revertíveis são o ponto. Exceção localizada: corrigir o último commit ainda dentro do bloco corrente (typo, arquivo esquecido, footer faltando). Commits de blocos já fechados ficam intocados.

### 4. Gate final

1. **Gate automático.** Rodar `test_command` integralmente. "Não temos" → inspeção textual de `## Verificação end-to-end`.

2. **Validação manual.** Plano com `## Verificação manual` → ler passos ao operador, **aguardar confirmação explícita** ("ok, valido"). Sem confirmação, não fechar. Durante o diálogo, observar gatilhos de captura (passo 4.5) sem interromper.

3. **Sanity check de docs user-facing.** Antes do done:
   - **Skip** se o plano já listou `.md` user-facing (`README*`, `CHANGELOG*`, `install.md`, `docs/install.md`, `docs/guides/**`) em `## Arquivos a alterar` E o diff agregado o tocou. Arquivos `.md` de implementação (skills, agents, hooks, philosophy) **não** ativam o skip.
   - **Skip** se `## Resumo da mudança` não menciona superfície user-facing (CLI/flag nova, env var nova, endpoint novo, comportamento perceptível, integração externa, instalação/configuração).
   - **Cutucar** caso contrário via enum (header `Docs`, opção única `Sim, consistente`; Other absorve a lista de arquivos a atualizar). Citar superfície inferida e candidatos típicos (README, install, docs internas). `CHANGELOG` fica fora (responsabilidade do `/release`). Updates listados via Other → bloco extra (implementar → `test_command` → revisor `code` → micro-commit) antes do done.

4. **Transição final do backlog.** `**Linha do backlog:**` capturada no passo 3 E linha em `## Em andamento` (ou ainda em `## Próximos`, se a transição inicial não ocorreu) → mover para `## Concluídos`, informar, aplicar como **bloco extra** (atualizar `backlog` → revisor `code` → micro-commit) **antes** do passo 4.5. Linha não localizada ou referência não capturada → skip silente.

5. **Captura automática de imprevistos.** Materializar a lista mantida desde o passo 3.

   **Gatilhos durante execução (passo 3):**
   - **Falha contornada** — `test_command` (ou verificação textual) falha e o agente segue contornando (skip de teste, retry frágil, fallback ad-hoc) sem solucionar a causa-raiz.
   - **Finding fora-do-escopo** — reviewer levanta problema real fora do bloco/plano corrente.
   - **Hook bloqueando** — hook do plugin retorna exit ≠ 0 sinalizando gap real; agente pivota e segue.
   - **Superfície faltante** — passo 2 detectou superfície externa em Contexto/Resumo ausente em `## Arquivos a alterar` e o operador escolheu `Continuar mesmo assim`.

   *(Bloqueios de pré-condição 3/4 e passo 1 — baseline vermelho, worktree órfã, falha de setup — geram captura imediata in situ; não alimentam esta lista.)*

   **Gatilhos durante validação manual (passo 4.2):**
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

7. **Sugestão de publicação.** Antes do enum `Publicar`, detectar divergência em BACKLOG.md.

   `git fetch origin` e `git log HEAD..origin/main --oneline -- BACKLOG.md`. Sem commits → enum inalterado. Com commits → tentar `git rebase origin/main`:

   - **Rebase limpo:** informar `"main avançou em BACKLOG.md; rebase aplicado — push usará --force-with-lease"`. Substituir `-u` por `--force-with-lease` nas opções `Push` e `Push + abrir PR`.
   - **Conflito apenas em BACKLOG.md em `## Em andamento`** E `**Linha do backlog:**` foi capturada: resolver programaticamente — (a) ler arquivo com markers; (b) do lado `<<<<<<< HEAD`, extrair itens de Em andamento; (c) remover o que casa exato com `**Linha do backlog:**`; (d) manter os demais; (e) adicionar o removido ao topo de Concluídos; (f) `git add BACKLOG.md && git rebase --continue`. Informar resolução automática e usar `--force-with-lease`.
   - **Qualquer outro conflito** (outros arquivos, BACKLOG.md fora de Em andamento, ou linha não capturada): `git rebase --abort`; avisar `"main divergiu em BACKLOG.md com conflito não-resolvível automaticamente — resolver manualmente"`. Push sem force.

   Remote configurado (`git remote -v`) → enum (header `Publicar`):
   - `Push` → `git push -u origin <branch-atual>`.
   - `Push + abrir PR` → push + `gh pr create`.
   - `Nenhum` → encerrar sem ação.

   Sem remote → skip silente.

A skill termina na worktree com a branch da feature após oferecer publicação.

## O que NÃO fazer

- Não declarar done sem confirmação humana **quando o plano exige validação manual**.
- Não pular revisor, mesmo em bloco trivial.
- Não tentar resolver merge/rebase no fim — exceção única em 4.7 quando: (i) único arquivo em conflito é BACKLOG.md; (ii) conflito restrito a `## Em andamento`; (iii) `**Linha do backlog:**` capturada. Qualquer outra situação: `git rebase --abort` e aviso.
- Não interpretar `{revisor: ...}` (PT) — schema canônico é `{reviewer: ...}` em inglês. Recusar antes de começar o bloco com mensagem indicando bloco e anotação ofensora.
- Não contornar plano sujo copiando o conteúdo manualmente para a worktree — bloqueio na pré-condição 2 existe para forçar commit no branch correto.
- Não silenciar o gatilho cruzado de credencial (passo 1.2) por estado prévio do `.worktreeinclude` — quando o plano tem `## Verificação manual` e há credencial gitignored não coberta, a cutucada é obrigatória.
- Não executar push ou abrir PR sem confirmação explícita via enum `Publicar`.
