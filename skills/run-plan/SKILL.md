---
name: run-plan
description: Executa um plano de docs/plans/<slug>.md em worktree isolada, com micro-commits Conventional Commits, revisão dirigida por bloco e gate de validação manual quando aplicável. Use quando o operador autorizou começar a implementação a partir de um plano pronto.
---

# run-plan

Executa um plano produzido por `/triage` (ou escrito à mão) seguindo a disciplina **worktree isolada → micro-commit por bloco → revisão dirigida → gate final**. Importa a parte boa de execução disciplinada (worktree, commits granulares, gate antes de declarar done) sem o overhead documental (spec separado, two-stage review universal, plano gigante).

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
   - **Bloquear** se `<plans_dir>/<slug>.md` estiver modificado ou untracked. Broken-by-construction: worktree é criada a partir do HEAD e não veria o plano que deveria executar. Mensagem direta ao operador: commitar o plano antes de prosseguir (ou usar `/triage` que já propõe o commit no passo 6). Não tentar contornar copiando o plano manualmente para a worktree.
   - **Cutucar** (não bloquear) se papéis de alinhamento — arquivos resolvidos pelos papéis `backlog`, `ubiquitous_language`, `design_notes`, ou qualquer arquivo sob `decisions_dir` — tiverem alterações uncommitted. A worktree perde esse contexto e reviewers podem não ver invariantes/ADRs que o plano assume documentados. Modo: enum via `AskUserQuestion` (header `Alinhamento`) com opções `Commitar agora` (skill aguarda commit antes de prosseguir) e `Continuar mesmo assim` (skill segue, registrando que o operador foi avisado). Mostrar a lista de arquivos sujos na pergunta. Outras alterações uncommitted no working tree (código de exploração, debug) **não** geram aviso — o operador as isolou intencionalmente, é o ponto da worktree.
3. O gate automático de testes do projeto está verde no branch atual (rodar antes de começar). Default: `make test`. Variante: `test_command` declarado no CLAUDE.md (ex.: `uv run pytest`, `npm test`, `cargo test`). Caminho de decisão: se canonical (`make test`) ausente E operador ainda não declarou `test_command: null` no bloco de config, perguntar uma vez (oferta única de memorização). Em projetos sem suite automatizada (meta-tools, doc-only), `## Verificação end-to-end` do plano substitui o gate — caso de exceção, sinalizado pela ausência de `test_command` resolvido **e** por o plano explicitar essa verificação textual.
4. A worktree `.worktrees/<slug>/` ainda não existe.

Se qualquer pré-condição falhar, parar e reportar ao operador.

## Passos

### 1. Setup da worktree

1. `git worktree add .worktrees/<slug> -b <slug>` a partir do branch atual.
2. **Replicar gitignored files essenciais**:
   - Se `.worktreeinclude` existe na raiz do repo: ler (1 path por linha, comentários com `#`) e copiar cada path do repo origem para a worktree. **Cópia, não symlink** — a worktree precisa ser realmente isolada.
   - Se não existe e o operador ainda não declarou explicitamente que não precisa, propor criação **uma vez por projeto** via enum (`AskUserQuestion`, header `Worktree`, `multiSelect: true`) listando os gitignored em uso aparente (`.env`, dbs locais, fixtures não versionadas) como opções selecionáveis. Operador pode escolher múltiplos. Sem seleção → o passo é pulado e a skill avisa que o gate baseline pode falhar por dependências locais ausentes.
   - **Gatilho cruzado de validação manual** (independente do estado prévio do `.worktreeinclude`): se o plano corrente tem `## Verificação manual` (matching semântico aceitando equivalente em outro idioma) E a raiz do repo tem gitignored típicos de credencial/config local (`.env`, `*.local.yaml`, `*.local.yml`, `secrets.*`), checar se cada um está coberto pelo `.worktreeinclude` aplicado. Para os não cobertos, **cutucar o operador** via enum (`AskUserQuestion`, header `Credencial`, opções `Replicar agora` e `Seguir sem replicar`); a pergunta cita o nome da credencial e o motivo (validação manual provavelmente exige serviço real). `Replicar agora` → adicionar ao `.worktreeinclude` (criar se não existir) e copiar; `Seguir sem replicar` → registrar que o operador foi avisado e prosseguir. O gatilho silencia estado prévio: `.worktreeinclude` ausente porque o operador disse "não preciso" antes **não** suprime a checagem quando `## Verificação manual` está presente — o contexto mudou (plano corrente exige serviço real).
3. `cd` na worktree. Sincronizar dependências executando o gerenciador idiomático da stack (ex.: `uv sync` Python, `npm ci` Node, `cargo fetch` Rust, `mvn install` Java). Stack inferida pelo marker do projeto. Rodar o `test_command` resolvido como baseline (default: `make test`). **Abortar se falhar** — o plano não roda em cima de testes vermelhos. Quando `test_command` resolve para "não temos" e o plano traz `## Verificação end-to-end`, o baseline vira inspeção textual conforme essa seção descreve.

### 2. Sanity check de escopo

Releia `## Contexto` e `## Resumo da mudança` do plano. Se houver menção a superfícies externas (configuração, ambiente, infraestrutura, compose, deploy, webhook, integração externa, `.env`) **que não aparecem em `## Arquivos a alterar`**, **avisar o operador** (cutucar, não bloquear) — o plano pode estar incompleto. Modo: enum via `AskUserQuestion` (header `Escopo`) com opções `Continuar mesmo assim` e `Pausar para ajustar plano`; a pergunta cita a superfície detectada.

### 3. Loop por bloco de `## Arquivos a alterar`

**Antes do primeiro bloco:** capturar `**Linha do backlog:** <texto>` do `## Contexto` do plano se presente. Se a linha está em `## Próximos` do arquivo do papel `backlog`, mover automaticamente para `## Em andamento`, informar o operador, e aplicar o edit no arquivo do backlog antes do primeiro bloco (edit entra no commit do primeiro bloco). Plano sem o campo, linha não localizada, papel `backlog` "não temos" → skip silente sem mencionar (vale para esta transição e para a do passo 4.4). Ver `docs/philosophy.md` → "Ciclo de vida do backlog".

**Captura automática durante a execução:** ao longo de todo o passo 3 (e estendendo-se ao passo 4.2), o agente observa gatilhos de **imprevistos detectados automaticamente**. Lista, gatilhos e materialização final em 4.5.

Para cada subseção do plano (geralmente um bloco por arquivo ou agrupamento lógico):

1. **Implementar** as mudanças descritas no bloco.
2. **Rodar o `test_command` resolvido** uma vez no fim do bloco (não a cada arquivo). Se `test_command` é "não temos", aplicar a verificação textual definida no plano.
3. **Escolher o(s) revisor(es)** lendo a anotação `{reviewer: ...}` no header do bloco. Schema completo em `docs/philosophy.md` → "Anotação de revisor em planos". Resumo operacional:
   - Sem anotação → `code-reviewer` (incluído neste plugin).
   - `{reviewer: code}` → `code-reviewer`.
   - `{reviewer: qa}` ou `{reviewer: security}` → `qa-reviewer` ou `security-reviewer` (incluídos neste plugin; projeto consumidor pode sobrescrever com `.claude/agents/<nome>.md`, que vence por convenção Claude Code).
   - `{reviewer: code,qa,security}` (múltiplos perfis) → invocar **todos** os perfis listados, em qualquer ordem, agregando relatórios.
   - Exemplo canônico: `### Bloco 1 — auth.py {reviewer: security}`.
4. **Aplicar correções** levantadas pelo(s) revisor(es) antes de prosseguir.
5. **Micro-commit** seguindo a **convenção de commits do projeto consumidor** (ver `docs/philosophy.md` → "Convenção de commits"): política explícita declarada → padrão observado no histórico (`git log`) → default canonical Conventional Commits em inglês. **Um commit por bloco**. Como regra, evitar `--amend` e rebase — micro-commits revertíveis são o ponto. Exceção localizada: corrigir o último commit ainda dentro do bloco corrente quando faz sentido (typo na mensagem, arquivo esquecido no stage, footer faltando). Commits de blocos já fechados ficam intocados.

### 4. Gate final

1. Rodar o `test_command` resolvido integralmente (gate automático sempre que houver). Quando `test_command` é "não temos", o gate é a inspeção textual de `## Verificação end-to-end` do plano.
2. **Plano com `## Verificação manual`**: ler os passos ao operador e **aguardar confirmação explícita** ("ok, valido") antes de prosseguir. Sem confirmação, a skill não fecha. Durante o diálogo, observar gatilhos de captura automática conforme passo 4.5 (alimentando a mesma lista do passo 3) sem interromper a validação.
3. **Sanity check de documentação** — antes de declarar done, validar consistência das docs `.md` user-facing com o que foi implementado:
   - **Skip silente** se o plano já listou pelo menos um arquivo `.md` **user-facing** em `## Arquivos a alterar` e o diff agregado dos blocos o tocou — padrões que contam: `README*`, `CHANGELOG*`, `install.md`, `docs/install.md`, `docs/guides/**`. Arquivos `.md` de implementação (skills, agents, hooks, philosophy) não ativam o skip; o gate continua e pergunta sobre docs.
   - **Skip silente** se o `## Resumo da mudança` não menciona nenhuma das categorias concretas de superfície user-facing (CLI/flag nova, env var nova, endpoint novo, comportamento perceptível, integração externa, alteração de instalação/configuração). Refactor puro / internal-only não precisa do check.
   - Caso contrário, **cutucar** (não bloquear) via enum (`AskUserQuestion`, header `Docs`) com opção única `Sim, consistente` — Other absorve naturalmente a lista de arquivos `.md` que o operador queira atualizar. A pergunta cita a superfície user-facing inferida do plano e os candidatos típicos (README, install, docs internas); `CHANGELOG` fica de fora porque é responsabilidade do `/release`. Se o operador listar updates via Other, tratá-los como **bloco extra** (implementar → `test_command` → revisor `code` → micro-commit) e só então declarar done.
4. **Transição final do backlog** — se a referência `**Linha do backlog:**` foi capturada no início do passo 3 E a linha está em `## Em andamento` (ou ainda em `## Próximos`, caso a transição inicial não tenha ocorrido), mover automaticamente para `## Concluídos`, informar o operador, e aplicar como **bloco extra** (atualizar arquivo do papel `backlog` → revisor `code` → micro-commit) antes de seguir para o passo 4.5. Linha não localizada (sumiu desde o registro) → skip silente. Sem referência capturada (plano sem o campo, papel `backlog` "não temos") → skip silente. Ver `docs/philosophy.md` → "Ciclo de vida do backlog".
5. **Captura automática de imprevistos** — materializar a lista mantida desde o início do passo 3 (alimentada também durante a validação manual no passo 4.2). Gatilhos prescritos:

   **Durante a execução dos blocos (passo 3):**
   - **Falha contornada** — `test_command` (ou verificação textual equivalente) falha e o agente segue contornando (skip de teste, retry frágil, fallback ad-hoc) sem solucionar a causa-raiz.
   - **Finding fora-do-escopo** — reviewer (`code`, `qa`, `security`) levanta problema real que não pertence ao bloco corrente nem ao plano corrente.
   - **Hook bloqueando** — hook do plugin retorna exit ≠ 0 sinalizando gap real (não bloqueio esperado já absorvido pela mecânica do hook); agente pivota e segue.
   - **Superfície faltante** — sanity check de escopo do passo 2 detecta menção a superfície externa em `## Contexto`/`## Resumo da mudança` que não aparece em `## Arquivos a alterar`, e o operador escolhe `Continuar mesmo assim`.

   **Durante a validação manual (passo 4.2):**
   - **Divergência do plano** — operador reporta comportamento que diverge do esperado por `## Verificação manual`.
   - **Bug colateral** — operador menciona bug menor não relacionado ao gate corrente.

   **Política de gravação:** a cada captura, o agente **informa o operador** com mensagem curta ("capturei no backlog: <linha>"; redação curta, descritiva do problema, não do gatilho) e segue sem aguardar resposta. O intervalo entre o aviso e a materialização final é a janela onde o operador pode dizer em prosa "descarta esse" — agente respeita e remove da lista.

   **No gate final:**
   - **Lista vazia** → skip silente (ver `docs/philosophy.md` → "Convenção de pergunta ao operador").
   - **Lista não-vazia** → bloco extra: (a) escrever uma linha por item em `## Próximos` do arquivo do papel `backlog`; (b) **aplicar consolidação** seguindo `docs/philosophy.md` → "Consolidação do backlog" (única pergunta admitida no passo é o enum `Backlog` da consolidação, condicional a flags); (c) revisor `code`; (d) micro-commit. Sem pergunta de confirmação sobre as capturas em si — operador já foi informado a cada detecção.

   **Caso especial:** papel `backlog` resolveu para "não temos" → skip silente do bloco extra; capturas viram apenas relato final ao operador (sem registro persistido).
6. **Declarar done**.

A skill termina na worktree com branch da feature. Caminho de fechamento (PR, merge, descarte) é decisão do operador.

## O que NÃO fazer

- Não declarar done sem confirmação humana **quando o plano exige validação manual**.
- Não pular revisor, mesmo em bloco trivial.
- Não tentar resolver merge/rebase no fim — a skill não fecha o branch.
- Não rodar a skill sem o plano revisado e aprovado pelo operador.
- Não interpretar `{revisor: ...}` (PT) — schema canônico é `{reviewer: ...}` em inglês. Recusar antes de começar o bloco, mensagem indicando o bloco e a anotação ofensora, sugerindo migrar para `{reviewer:}`.
- Não contornar plano sujo copiando o conteúdo manualmente para dentro da worktree. O bloqueio na pré-condição 2 existe para forçar o commit no branch correto — burlar quebra o histórico do branch da feature.
- Não pular o sanity check de documentação quando ele se aplica (passo 4.3) — skip só nas duas condições prescritas (`.md` user-facing já no plano e tocados, ou `## Resumo da mudança` sem nenhuma das categorias concretas de superfície user-facing). Em dúvida, perguntar.
- Não capturar com base em inferência tardia do diff — captura ocorre no momento do gatilho (passo 3 ou 4.2), não em pós-leitura.
- Não capturar itens que já foram absorvidos pelo plano corrente (escopo creep contido) — backlog é para imprevistos detectados, não para registrar tudo que apareceu.
- Não pedir confirmação ao operador sobre as capturas em si — política é "informar e seguir".
- Não silenciar o gatilho cruzado de validação manual (passo 1.2) por estado prévio do `.worktreeinclude` — quando o plano corrente tem `## Verificação manual` e há credencial gitignored típica não coberta, a cutucada é obrigatória independente da cláusula original "uma vez por projeto" ter sido respondida no passado.
- Não inferir a linha do backlog por matching textual heurístico — `**Linha do backlog:**` ausente é skip silente; presença é match exato. Slug do plano vs. frase da linha não conta como evidência.
- Não silenciar a transição final (passo 4.4) quando a linha está presente e localizada — a transição é automática; informar o operador é obrigatório.
- Não inverter a ordem entre transição final (4.4) e captura automática (4.5) — fechar a linha corrente da feature antes de materializar capturas. Eixos distintos, ordem importa.

## Convenção: `.worktreeinclude`

Ver `docs/philosophy.md` → "Convenção `.worktreeinclude`".
