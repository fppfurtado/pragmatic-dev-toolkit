# ADR-028: Campo Branch opcional no plano para fluxo issue-first

**Data:** 2026-05-14
**Status:** Proposto

## Origem

- **Investigação:** Operador questionou (2026-05-14) por que o plugin não acomoda o fluxo de projetos GitLab onde a issue é especificada no forge antes do desenvolvimento e a branch já existe (criada via "Create branch" da issue) quando o trabalho começa. `/run-plan` no setup da worktree sempre cria branch nova a partir do HEAD, sem caminho para reaproveitar branch pré-existente.

## Contexto

`/run-plan` no passo 1 (setup da worktree) executa `git worktree add .worktrees/<slug> -b <slug>` — cria branch nova nomeada pelo slug do plano, a partir do HEAD da invocação. Comportamento implícito: o plugin **nomeia** a branch e **cria** ela junto com a worktree.

Esse design assume um fluxo onde o desenvolvimento começa pela ideia (`/triage` decide artefato → plano → `/run-plan` cria branch e executa). Não acomoda fluxos onde a branch já existe antes do plano:

- **GitLab issue-first:** issue é aberta e especificada no forge; "Create branch" gera branch nomeada pelo padrão do projeto (ex.: `123-feature-name`); developer faz checkout dessa branch antes de invocar o plugin.
- **GitHub Projects ou similares** onde o fluxo da equipe define que branches nascem do forge, não do shell.
- **Reaproveitar branch de PR existente** que precisa de retrabalho não-trivial e o operador quer redigir plano sob ela.

Hoje o operador nesses fluxos tem três caminhos ruins:

1. Aceita que o `/run-plan` crie `<slug>` como branch nova e perde o link issue↔branch que o forge automatizou.
2. Renomeia a branch existente para casar com o slug do plano (frágil, depende de convenção informal).
3. Usa o plugin sem `/run-plan` (perde worktree isolada, micro-commits, gates).

A frase "branch é cidadã primeira de state" (ADR-004 codificou: "em andamento = branch fora de main com PR aberto") reforça que o nome da branch frequentemente carrega significado externo (issue ID, convenção do forge) que o slug-do-plano não deveria sobrescrever.

A separação **nome do diretório de worktree** (interno ao plugin, derivado do slug) **vs nome da branch** (externo, carregado pelo fluxo da equipe ou do forge) hoje é colapsada — slug é ambos. O issue-first quer desacoplar.

## Decisão

**Adicionar campo opcional `**Branch:**` no `## Contexto` do `templates/plan.md`. Quando presente, `/run-plan` faz checkout da branch existente em vez de criar; quando ausente, comportamento atual preservado.**

### Mecânica

**Template (`templates/plan.md`).** Novo campo no bloco de "campos especiais" do `## Contexto`, ao lado de `**Termos ubíquos tocados:**`, `**ADRs candidatos:**`, `**Linha do backlog:**`:

```markdown
**Branch:** <nome-da-branch> — incluir quando a branch já existe (issue-first GitLab, retrabalho de PR, etc.); ausência = /run-plan cria <slug> a partir do HEAD.
```

**`/triage` (caminho-com-plano).** No passo 4 (Produzir plano), após `git branch --show-current` retornar nome ≠ default (resolvido via `git symbolic-ref refs/remotes/origin/HEAD`; fallback `main`), perguntar via `AskUserQuestion`:

- `header`: `Branch`
- `question`: `"Usar '<branch-atual>' como branch de execução do plano?"`
- Opções: `Sim, usar essa branch` (Recommended) / `Não, /run-plan cria <slug>`
- `description` da primeira: `"Plano grava **Branch:** <branch-atual>; /run-plan faz checkout dela em vez de criar nova"`
- `description` da segunda: `"Comportamento default; /run-plan cria branch <slug> a partir do HEAD da invocação"`

Branch atual == default → omitir pergunta (silêncio); o cenário comum de "estou em main, vou triagear feature nova" não vê fricção.

**`/run-plan` (passo 1, setup da worktree).** Após ler o plano, detectar campo `**Branch:**`:

- Presente → `git worktree add .worktrees/<slug> <branch>` (sem `-b`). git resolve nome em ordem natural (heads, depois remotes via DWIM se houver fetch prévio).
- Ausente → comportamento atual: `git worktree add .worktrees/<slug> -b <slug>`.
- Falha em criar worktree → discriminar pela stderr do `git worktree add` e escrever em `## Próximos` do `backlog` linha específica para cada motivo (mesmo padrão dos demais bloqueios pré-loop; informar; parar):
  - **Branch inexistente / digitação errada / refs não-fetchadas** (`fatal: invalid reference: <nome>`): `branch <nome> referenciada em **Branch:** do plano <slug> não existe — verificar nome ou rodar git fetch antes de re-executar`.
  - **Branch já checked out em outro worktree** (`fatal: '<nome>' is already used by worktree at '<path>'`): `branch <nome> referenciada em **Branch:** do plano <slug> está checked out em <path> — fazer checkout de outra branch lá antes de re-executar`. Não emitir `git checkout`/`git switch` no working tree principal para liberar a branch — operação altera estado externo ao plugin (ver `## O que NÃO fazer` de `/run-plan SKILL.md`).
  - **Diretório `.worktrees/<slug>/` já existe sem registro git** (race com sessão paralela ou execução interrompida que escapou da pré-condição 4): `diretório .worktrees/<slug>/ existe mas não está registrado como worktree git — remover manualmente antes de re-executar`.
  - **Outras falhas**: `falha em git worktree add para <nome> do plano <slug>: <stderr>` (operador investiga manual).

### Razões

- **Fluxos issue-first ficam suportados** sem inverter o default (sem flag global, sem novo papel no path contract).
- **Opt-in explícito por plano**: operador decide por plano, não por projeto inteiro. Equipe mista (alguns membros usam GitLab issue-first, outros redigem plano de zero) convive sem configuração compartilhada.
- **Backwards-compat trivial**: planos sem campo continuam funcionando idênticos; campo ausente = comportamento atual.
- **Desacopla worktree-name de branch-name**: slug continua nomeando o diretório (`/.worktrees/<slug>`), branch passa a ser independente. Útil mesmo fora de issue-first quando operador quer slug descritivo + branch concisa (ou vice-versa).
- **Cabe no `## Contexto` que `/triage` já redige**: mensageiro estrutural existente, mesma família de `**Linha do backlog:**` (ambos são "metadados de execução para `/run-plan` consumir").

### Modo local (`paths.plans_dir: local`)

Campo aceito normalmente. Plano em modo local é gitignored, mas o **nome da branch** já é metadata pública (visível em `git push`, refs remotas) — registrar a branch existente no plano local não viola a regra de não-referenciar do ADR-005, que protege referências **geradas pelo plugin** em commits/PRs/branches a partir de artefatos privados, não referências internas do plano local a metadata já pública. A direção do fluxo importa: plano local → branch pública (ok); plano local → mensagem de commit pública (proibido).

`/run-plan §3.7` em modo local oferece `Renomear branch antes` apenas quando a branch foi **criada pelo plugin** (campo `**Branch:**` ausente; nome derivado do slug do plano local). Branch **pré-existente** (vinda do campo, ex.: `123-feature-name` da issue) passa direto sem oferta de rename — operador já tomou deliberadamente a decisão de exposição ao carregar `**Branch:**` no plano local; oferecer renomear inverteria a intenção.

## Consequências

### Benefícios

- Plugin aplicável em projetos com fluxo GitLab issue-first sem fork/configuração paralela.
- Operador escolhe nível de acoplamento branch↔slug por plano, não por configuração global.
- `/triage` ganha cutucada barata (1 enum) que cobre o caso comum sem fricção quando irrelevante (silêncio em main).
- Template fica mais expressivo sobre o ciclo de vida do plano sem inflar (1 linha opcional no bloco de campos especiais).

### Trade-offs

- `templates/plan.md` ganha 1 campo opcional (4ª entrada no bloco de campos especiais — leve aumento de superfície editorial no template canonical).
- `/triage` passo 4 ganha probe de `git branch --show-current` + comparação com default + enum condicional (~5 linhas de prosa nova).
- `/run-plan` passo 1 ganha branching de comportamento por presença do campo (~3 linhas).
- Operador pode esquecer de listar a branch e rodar `/run-plan`, que cria branch nova `<slug>` a partir do HEAD **sem sinal de erro** — link issue↔branch perde-se silenciosamente (branch da issue continua intacta no repo, mas sem worktree associada; trabalho da feature acaba na branch errada). O enum `/triage` step 4 mitiga (perguntando proativamente quando branch atual ≠ default), mas não elimina (operador pode dizer "Não" por reflexo). `/run-plan` precondição 4 (worktree órfã) cobre re-execução do mesmo plano; caso "branch local órfã sem worktree associada" (`<slug>` já existe como branch mas worktree foi limpa) não está coberto e pode emergir como follow-up se atrito real surgir.

### Limitações

- Nenhuma autodetecção de "branch atual está vinculada a issue" — operador é responsável por confirmar no enum do `/triage` que a branch corrente é a desejada para execução.
- Não há suporte a "criar branch a partir de outra branch base" (caso `git worktree add -b <novo> <base>`). Branch nasce do HEAD do operador como hoje, ou é checkout de existente. Caso emergir, reabrir.
- Sem heurística de matching slug ↔ branch existente (ex.: slug `exportar-csv` reaproveita branch `exportar-csv` se existir). Considerada e rejeitada — frágil, depende de convenção informal e mascara o opt-in explícito.

## Alternativas consideradas

### Detectar e reaproveitar branch existente quando o nome bate

Se `<slug>` já existe em `refs/heads/` ou `refs/remotes/origin/`, `/run-plan` faz checkout em vez de criar. Mudança de ~5 linhas, sem novo papel/config. **Rejeitado**: depende do operador escolher slug do plano coincidente com a branch da issue (`123-feature-name`), que é convenção frágil e mascara o opt-in. Comportamento implícito é difícil de descobrir e debugar quando ocorre por acidente.

### Inverter default — adotar branch atual quando ≠ principal

Se `git symbolic-ref refs/remotes/origin/HEAD` ≠ HEAD corrente, `/run-plan` faz worktree a partir da branch atual sem criar nova. **Rejeitado**: muda comportamento global do plugin (não opt-in), e há risco de o operador esquecer de trocar de branch antes de invocar e empilhar trabalho na branch errada. Operador atual que usa o fluxo padrão "redijo plano em main → /run-plan cria branch" perde rede de proteção.

### Novo papel no path contract (`paths.run_plan_branch_mode`)

Configuração no `<!-- pragmatic-toolkit:config -->` selecionando `create` (default) ou `adopt`. **Rejeitado**: granularidade errada — fluxo issue-first vs from-scratch é decisão por plano, não por projeto. Equipe mista (alguns planos issue-first, outros from-scratch) ficaria mal servida por configuração compartilhada. Campo opcional no plano resolve sem inflar o schema do path contract.

### Addendum em ADR-001 estendendo o template

ADR-001 codifica protocolo de centralização de templates; este ADR poderia ser nota anexa. **Rejeitado**: pureza semântica — ADR-001 é sobre **onde** o template mora (mecanismo); este é sobre **conteúdo** estrutural novo no template para suportar um fluxo de trabalho específico. Decisões com perguntas distintas merecem ADRs distintos; addendum confunde a leitura futura.

## Gatilhos de revisão

- Padrão recorrente de re-execução de `/run-plan` em plano cujo slug colide com nome de branch local existente sem worktree associada → considerar precondição explícita análoga à precondição 4 (worktree órfã) para o caso de "branch local órfã".
- ≥3 invocações reportando atrito por não suportar "criar branch a partir de outra base" (ex.: `git worktree add -b <novo> <base>`) → reabrir para considerar campo `**Base:**` adicional.
- Heurística automática de matching slug ↔ branch existente reaparecer como pedido (rejeitada acima) → reavaliar com evidência empírica concreta.
- Equipe adotar convenção rígida de naming para branches do forge → considerar gerar slug a partir da branch atual no `/triage` (inversão da relação atual: hoje o operador confirma branch para o plano; lá, plano herdaria slug da branch).
