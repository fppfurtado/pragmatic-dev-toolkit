# Plano — Campo Branch opcional no plano para fluxo issue-first

## Contexto

`/run-plan` no passo 1 sempre cria branch nova (`git worktree add .worktrees/<slug> -b <slug>`), o que não acomoda fluxos onde a branch já existe antes do plano (GitLab issue-first com "Create branch" da issue, retrabalho de PR existente, convenções de equipe que nascem branches no forge). Decisão estrutural codificada em ADR-028: adicionar campo opcional `**Branch:**` no `## Contexto` do `templates/plan.md`. Quando presente, `/run-plan` faz checkout da branch existente; quando ausente, comportamento atual preservado (backwards-compat trivial).

`/triage` no caminho-com-plano autodetecta `git branch --show-current` e, quando ≠ default (resolvido via `git symbolic-ref refs/remotes/origin/HEAD`; fallback `main`), pergunta via `AskUserQuestion` (enum Sim/Não) se a branch corrente deve ser registrada como `**Branch:**` no plano.

**ADRs candidatos:** ADR-028 (Campo Branch opcional no plano para fluxo issue-first).

## Resumo da mudança

Implementação de ADR-028 em três superfícies:

1. **`templates/plan.md`** — adicionar campo `**Branch:**` ao bloco de campos especiais do `## Contexto`, ao lado dos três existentes (`Termos ubíquos tocados`, `ADRs candidatos`, `Linha do backlog`).
2. **`skills/triage/SKILL.md` passo 4** — após resolver caminho-com-plano, probe `git branch --show-current` vs default; se diferente, enum confirmando uso da branch atual; preencher `**Branch:**` no plano conforme resposta.
3. **`skills/run-plan/SKILL.md` passo 1** — branching no `git worktree add` por presença do campo; falha de criação (branch inexistente) cai no padrão de bloqueio pré-loop existente (captura no `backlog`, informa, para).

Sem mudanças em CLAUDE.md (campo é detalhe do template + comportamento de skill, não convenção cross-cutting). Sem mudanças em `docs/install.md` (o fluxo issue-first é caso de uso emergente do mesmo `/triage` documentado, não nova feature de instalação).

## Arquivos a alterar

### Bloco 1 — Template canonical do plano {reviewer: doc}

- `templates/plan.md`: no bloco HTML de comentário do `## Contexto` (campos especiais), adicionar 4ª entrada após `**Linha do backlog:**`:

  ```markdown
  **Branch:** <nome-da-branch> — incluir quando a branch já existe (issue-first GitLab, retrabalho de PR, etc.); ausência = /run-plan cria <slug> a partir do HEAD.
  ```

  Posicionamento ao final do bloco de campos especiais (após `**Linha do backlog:**`) preserva ordem natural: domínio → decisões → state → execução.

### Bloco 2 — `/triage` passo 4 ganha probe e enum de branch {reviewer: code}

- `skills/triage/SKILL.md`: no passo 4, sub-fluxo "Plano (papel: `plans_dir`)", inserir 4º bullet no bloco de campos especiais do `## Contexto` (linhas 105-107, paralelo aos `**Termos ubíquos tocados:**` / `**ADRs candidatos:**` / `**Linha do backlog:**`):

  > - Se a branch corrente é a desejada para execução (caminho issue-first GitLab, retrabalho de PR), incluir `**Branch:** <nome-da-branch>` — mensageiro para `/run-plan` fazer checkout dela em vez de criar `<slug>`. Probe e cutucada descritos abaixo.

- Adicionar parágrafo subsequente ao bloco de bullets (antes da linha "BACKLOG.md **não aparece**...") detalhando a mecânica:

  > **Probe e cutucada do `**Branch:**`.** Executar `git branch --show-current`. Resolver branch principal via `git symbolic-ref refs/remotes/origin/HEAD` (parse final do path: `origin/main` → `main`); falha (repo sem upstream, clone via tarball, fork sem `origin/HEAD`) → fallback `main`. Branch atual == principal → omitir o campo (silêncio, fluxo default preservado). Branch atual ≠ principal → perguntar via `AskUserQuestion` (header `Branch`, opções literais `Sim, usar essa branch (Recommended)` / `Não, /run-plan cria <slug>`; descrições conforme ADR-028 § Mecânica). Resposta `Sim` → preencher `**Branch:** <branch-atual>` no `## Contexto`. Resposta `Não` → omitir o campo.

### Bloco 3 — `/run-plan` passo 1 ganha branching no setup da worktree {reviewer: code}

- `skills/run-plan/SKILL.md`: no passo "1. Setup da worktree" subitem 1 (`git worktree add .worktrees/<slug> -b <slug> a partir do branch atual.`), reescrever:

  > 1. Detectar campo `**Branch:**` no `## Contexto` do plano.
  >    - **Presente:** `git worktree add .worktrees/<slug> <branch>` (sem `-b`). git resolve nome em ordem natural (heads, depois remotes via DWIM se houver fetch prévio).
  >    - **Ausente:** `git worktree add .worktrees/<slug> -b <slug>` a partir do branch atual (comportamento atual preservado).
  >    - Falha de criação (branch inexistente, digitação errada, refs não-fetchadas) → escrever em `## Próximos` do `backlog` linha tipo `branch <branch> referenciada em **Branch:** do plano <slug> não existe — verificar nome ou rodar git fetch antes de re-executar`; informar; parar. Papel `backlog` = "não temos" → só informar.

- §3.7 (Sugestão de publicação, modo local), linha 150 do `run-plan/SKILL.md`: condicionar a opção `Renomear branch antes (Recommended)` à **ausência** do campo `**Branch:**` no plano. Quando o campo está presente, o enum de publicação em modo local cai para `Push (Recommended)` / `Push + abrir PR/MR` / `Nenhum` (idêntico ao modo canonical) — branch pré-existente já carrega decisão de exposição do operador (cf. ADR-028 § "Modo local"). Cross-ref a ADR-028 na prosa do SKILL.

## Verificação end-to-end

- `templates/plan.md` contém o novo campo `**Branch:**` no bloco HTML de campos especiais do `## Contexto`, na 4ª posição (após `**Linha do backlog:**`).
- `skills/triage/SKILL.md` descreve no passo 4 (caminho-com-plano) o probe `git branch --show-current`, a resolução do default via `git symbolic-ref` com fallback, e o enum `AskUserQuestion` com header `Branch`.
- `skills/run-plan/SKILL.md` no passo 1 distingue presença/ausência do campo e cobre o caminho de falha; §3.7 condiciona a oferta de rename à ausência do campo.
- Cross-refs ao ADR-028 presentes em pelo menos um ponto de cada SKILL tocada.

## Verificação manual

Cenários para smoke-test em consumer real (este repo não tem suite — gate é inspeção textual + execução manual):

1. **Plano sem `**Branch:**` (regressão de fluxo atual)** — redigir plano sem o campo; rodar `/run-plan <slug>`; confirmar que worktree é criada com `git worktree add .worktrees/<slug> -b <slug>` (branch nova nomeada pelo slug, a partir do HEAD).

2. **Plano com `**Branch:**` apontando branch local existente** — checkout `feature-foo` localmente; redigir plano com `**Branch:** feature-foo`; rodar `/run-plan <slug>`; confirmar worktree em `.worktrees/<slug>` com branch `feature-foo` (sem `-b`).

3. **Plano com `**Branch:**` apontando branch só remota** — `git fetch origin`, sem checkout local; plano com `**Branch:** origin-only-feature`; rodar `/run-plan <slug>`; confirmar que git resolve via DWIM e cria worktree rastreando `origin/<branch>`.

4. **Plano com `**Branch:**` inexistente** — plano com `**Branch:** nao-existe-aqui`; rodar `/run-plan <slug>`; confirmar que falha cai no padrão de bloqueio pré-loop (linha gravada em `## Próximos` do backlog, mensagem clara, sem worktree criada).

5. **`/triage` em branch principal** — checkout `main`; invocar `/triage <intenção que vira plano>`; confirmar que o passo 4 **não pergunta** sobre branch (silêncio); plano sai sem `**Branch:**`.

6. **`/triage` em branch não-principal** — checkout `123-feature-name`; invocar `/triage <intenção>`; confirmar que enum `Branch` aparece com labels literais `Sim, usar essa branch (Recommended)` e `Não, /run-plan cria <slug>`. Resposta `Sim` → plano sai com `**Branch:** 123-feature-name`. Resposta `Não` → plano sai sem o campo.

7. **Modo local com `**Branch:**`** — `paths.plans_dir: local`; checkout branch pré-existente `123-issue-x`; `/triage` confirma uso; plano local em `.claude/local/plans/<slug>.md` com `**Branch:** 123-issue-x`. `/run-plan <slug>` faz checkout da branch existente; §3.7 **não oferece** `Renomear branch antes` (campo presente). Cross-check com cenário simétrico onde campo está ausente em modo local — oferta de rename **aparece** (comportamento preservado).

8. **Repo sem `origin/HEAD`** — clone fresco via tarball ou `git init` local; sem origin configurado; checkout branch arbitrária `dev`; invocar `/triage <intenção>`; confirmar que `git symbolic-ref refs/remotes/origin/HEAD` falha e fallback `main` é aplicado; enum aparece se `dev` ≠ `main`.

9. **Plano sem `**Branch:**` executado em branch não-principal sem `/triage` (trade-off documentado)** — checkout `123-feature-issue` (branch existente da issue); plano pré-existente sem campo (redigido manualmente ou em sessão anterior); rodar `/run-plan <slug>` direto; confirmar que worktree é criada com branch **nova** `<slug>` a partir do HEAD da `123-feature-issue` — link issue↔branch perdido silenciosamente, comportamento documentado como trade-off em ADR-028 § Trade-offs. Reforça que a cutucada do `/triage` (cenário 6) é o único ponto de mitigação.

## Notas operacionais

- Ordem dos blocos: 1 (template) → 2 (`/triage`) → 3 (`/run-plan`). Template fornece o esqueleto canonical que `/triage` preenche; `/run-plan` consome o produto. Inverter a ordem (skill antes do template) deixa `/triage` referenciando campo que ainda não existe no template entre commits.
- Validação manual fica como spec para smoke pós-release em consumer project — repo do plugin não tem ambiente para exercitar enum interativo nem fluxos com branches mock.
- Cross-ref recíproco: ADR-028 já cita `/run-plan §3.7` e o template; SKILLs tocadas devem citar `ADR-028` na nova prosa para fechar o loop.
