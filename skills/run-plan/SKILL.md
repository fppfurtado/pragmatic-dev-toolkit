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
2. **Estado git dos artefatos de alinhamento** — checagem em duas camadas via `git status --porcelain`:
   - **Bloquear** se `<plans_dir>/<slug>.md` estiver modificado ou untracked. Broken-by-construction: worktree é criada a partir do HEAD e não veria o plano que deveria executar. Mensagem direta ao operador: commitar o plano antes de prosseguir (ou usar `/new-feature` que já propõe o commit no passo 5). Não tentar contornar copiando o plano manualmente para a worktree.
   - **Cutucar** (não bloquear) se papéis de alinhamento — arquivos resolvidos pelos papéis `backlog`, `ubiquitous_language`, `design_notes`, ou qualquer arquivo sob `decisions_dir` — tiverem alterações uncommitted. A worktree perde esse contexto e reviewers podem não ver invariantes/ADRs que o plano assume documentados. Mensagem canônica: *"Alinhamento sujo: <lista>. Worktree não verá essas alterações. Commitar agora ou continuar mesmo assim?"*. Outras alterações uncommitted no working tree (código de exploração, debug) **não** geram aviso — o operador as isolou intencionalmente, é o ponto da worktree.
3. O gate automático de testes do projeto está verde no branch atual (rodar antes de começar). Default: `make test`. Variante: `test_command` declarado no CLAUDE.md (ex.: `uv run pytest`, `npm test`, `cargo test`). Caminho de decisão: se canonical (`make test`) ausente E operador ainda não declarou `test_command: null` no bloco de config, perguntar uma vez (oferta única de memorização). Em projetos sem suite automatizada (meta-tools, doc-only), `## Verificação end-to-end` do plano substitui o gate — caso de exceção, sinalizado pela ausência de `test_command` resolvido **e** por o plano explicitar essa verificação textual.
4. A worktree `.worktrees/<slug>/` ainda não existe.

Se qualquer pré-condição falhar, parar e reportar ao operador.

## Passos

### 1. Setup da worktree

1. `git worktree add .worktrees/<slug> -b <slug>` a partir do branch atual.
2. **Replicar gitignored files essenciais**:
   - Se `.worktreeinclude` existe na raiz do repo: ler (1 path por linha, comentários com `#`) e copiar cada path do repo origem para a worktree. **Cópia, não symlink** — a worktree precisa ser realmente isolada.
   - Se não existe e o operador ainda não declarou explicitamente que não precisa, propor criação **uma vez por projeto**: listar gitignored em uso aparente (`.env`, dbs locais, fixtures não versionadas) e perguntar quais devem ser replicados. Resposta "não preciso" é válida e o passo é pulado; nesse caso avisar que o gate baseline pode falhar por dependências locais ausentes.
   - **Gatilho cruzado de validação manual** (independente do estado prévio do `.worktreeinclude`): se o plano corrente tem `## Verificação manual` (matching semântico aceitando equivalente em outro idioma) E a raiz do repo tem gitignored típicos de credencial/config local (`.env`, `*.local.yaml`, `*.local.yml`, `secrets.*`), checar se cada um está coberto pelo `.worktreeinclude` aplicado. Para os não cobertos, **cutucar o operador**: *"Plano tem `## Verificação manual` e `<credencial>` não está replicada na worktree. Validação manual provavelmente vai precisar do serviço real. Replicar agora? (s/n)"*. "s" → adicionar ao `.worktreeinclude` (criar se não existir) e copiar; "n" → seguir, registrando que o operador foi avisado. O gatilho silencia estado prévio: `.worktreeinclude` ausente porque o operador disse "não preciso" antes **não** suprime a checagem quando `## Verificação manual` está presente — o contexto mudou (plano corrente exige serviço real).
3. `cd` na worktree. Sincronizar dependências executando o gerenciador idiomático da stack (ex.: `uv sync` Python, `npm ci` Node, `cargo fetch` Rust, `mvn install` Java). Stack inferida pelo marker do projeto. Rodar o `test_command` resolvido como baseline (default: `make test`). **Abortar se falhar** — o plano não roda em cima de testes vermelhos. Quando `test_command` resolve para "não temos" e o plano traz `## Verificação end-to-end`, o baseline vira inspeção textual conforme essa seção descreve.

### 2. Sanity check de escopo

Releia `## Contexto` e `## Resumo da mudança` do plano. Se houver menção a superfícies externas (configuração, ambiente, infraestrutura, compose, deploy, webhook, integração externa, `.env`) **que não aparecem em `## Arquivos a alterar`**, **avisar o operador** (cutucar, não bloquear) — o plano pode estar incompleto. Mensagem canônica: *"Plano menciona <superfície> mas `## Arquivos a alterar` não lista arquivo correspondente. Continuar mesmo assim?"*

### 3. Loop por bloco de `## Arquivos a alterar`

Para cada subseção do plano (geralmente um bloco por arquivo ou agrupamento lógico):

1. **Implementar** as mudanças descritas no bloco.
2. **Rodar o `test_command` resolvido** uma vez no fim do bloco (não a cada arquivo). Se `test_command` é "não temos", aplicar a verificação textual definida no plano.
3. **Escolher o(s) revisor(es)** lendo a anotação `{reviewer: ...}` no header do bloco. Schema completo em `docs/philosophy.md` → "Anotação de revisor em planos". Resumo operacional:
   - Sem anotação → `code-reviewer` (incluído neste plugin).
   - `{reviewer: code}` → `code-reviewer`.
   - `{reviewer: qa}` ou `{reviewer: security}` → agent project-level correspondente em `.claude/agents/<role>-reviewer.md`.
   - `{reviewer: code,qa,security}` (múltiplos perfis) → invocar **todos** os perfis listados, em qualquer ordem, agregando relatórios.
   - Exemplo canônico: `### Bloco 1 — auth.py {reviewer: security}`.
4. **Aplicar correções** levantadas pelo(s) revisor(es) antes de prosseguir.
5. **Micro-commit** seguindo a **convenção de commits do projeto consumidor** (ver `docs/philosophy.md` → "Convenção de commits"): política explícita declarada → padrão observado no histórico (`git log`) → default canonical Conventional Commits em inglês. **Um commit por bloco**. Como regra, evitar `--amend` e rebase — micro-commits revertíveis são o ponto. Exceção localizada: corrigir o último commit ainda dentro do bloco corrente quando faz sentido (typo na mensagem, arquivo esquecido no stage, footer faltando). Commits de blocos já fechados ficam intocados.

### 4. Gate final

1. Rodar o `test_command` resolvido integralmente (gate automático sempre que houver). Quando `test_command` é "não temos", o gate é a inspeção textual de `## Verificação end-to-end` do plano.
2. **Plano com `## Verificação manual`**: ler os passos ao operador e **aguardar confirmação explícita** ("ok, valido") antes de prosseguir. Sem confirmação, a skill não fecha.
3. **Sanity check de documentação** — antes de declarar done, validar consistência das docs `.md` user-facing com o que foi implementado:
   - **Skip silente** se o plano já listou arquivos `.md` em `## Arquivos a alterar` e o diff agregado dos blocos os tocou — documentação fez parte do plano, gate cumprido.
   - **Skip silente** se o plano **não** tem `## Verificação manual` **e** o `## Resumo da mudança` não menciona superfície user-facing (CLI/flag nova, env var nova, endpoint novo, comportamento perceptível, integração externa, alteração de instalação/configuração). Refactor puro / internal-only não precisa do check.
   - Caso contrário, **cutucar** (não bloquear) com pergunta direta ao operador: *"Diff introduziu <superfície user-facing inferida do plano>. README / docs de install / CHANGELOG / outras `.md` consistentes? Sim → declarar done. Não → listar arquivos a atualizar."*. Se o operador listar updates, tratá-los como **bloco extra** (implementar → `test_command` → revisor `code` → micro-commit) e só então declarar done.
4. **Backlog harvest** — antes de declarar done, **cutucar** (não bloquear) com pergunta direta: *"Durante a execução, emergiu algo fora do escopo deste plano que deveria virar item separado no backlog (TODO adjacente, tech-debt revelado pela leitura, bug menor avistado de passagem, melhoria não-essencial)?"*. Se o operador listar itens, tratá-los como **bloco extra** (atualizar arquivo do papel `backlog` adicionando uma linha por item em `## Próximos` → revisor `code` → micro-commit) antes de declarar done. Resposta "nada" é válida e fecha o gate. Itens já incorporados ao plano corrente (escopo creep contido) **não** entram aqui — só itens deliberadamente deferidos.
5. **Declarar done**.

A skill termina na worktree com branch da feature. Caminho de fechamento (PR, merge, descarte) é decisão do operador.

## O que NÃO fazer

- Não declarar done sem confirmação humana **quando o plano exige validação manual**.
- Não pular revisor, mesmo em bloco trivial.
- Não tentar resolver merge/rebase no fim — a skill não fecha o branch.
- Não rodar a skill sem o plano revisado e aprovado pelo operador.
- Não interpretar `{revisor: ...}` (PT) — schema canônico é `{reviewer: ...}` em inglês. Recusar antes de começar o bloco, mensagem indicando o bloco e a anotação ofensora, sugerindo migrar para `{reviewer:}`.
- Não contornar plano sujo copiando o conteúdo manualmente para dentro da worktree. O bloqueio na pré-condição 2 existe para forçar o commit no branch correto — burlar quebra o histórico do branch da feature.
- Não pular o sanity check de documentação quando ele se aplica (passo 4.3) — skip só nas duas condições prescritas (`.md` já no plano e tocados, ou plano sem superfície user-facing). Em dúvida, perguntar.
- Não pular o backlog harvest (passo 4.4) — sempre perguntar antes de declarar done. Resposta "nada" é fechamento válido; silenciar é perder itens.
- Não capturar itens no harvest que já foram absorvidos pelo plano corrente (escopo creep contido) — backlog é para deferimento deliberado, não para registrar tudo que apareceu.
- Não silenciar o gatilho cruzado de validação manual (passo 1.2) por estado prévio do `.worktreeinclude` — quando o plano corrente tem `## Verificação manual` e há credencial gitignored típica não coberta, a cutucada é obrigatória independente da cláusula original "uma vez por projeto" ter sido respondida no passado.

## Convenção: `.worktreeinclude`

Ver `docs/philosophy.md` → "Convenção `.worktreeinclude`".
