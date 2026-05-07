---
name: release
description: Bump de versão em version_files, entrada de changelog, commit unificado e tag anotada local (não faz push). Use quando o operador autorizou publicar release.
disable-model-invocation: false
roles:
  informational: [version_files, changelog]
---

# release

Mecaniza a release num único ciclo: detecta a próxima versão a partir do log Conventional Commits desde a última tag, atualiza os arquivos declarados em `version_files`, escreve entrada no `changelog`, faz commit unificado e cria tag anotada local.

**Faz commit local e tag local; não faz push.** Publicação fica com o operador (`git push --follow-tags`) — release é ato visível, decisão deliberada que sai da blast radius da skill.

## Argumentos

Todos opcionais. Argumento explícito vence inferência.

- `/release` — sem argumento; skill infere bump do log CC.
- `/release <bump>` — força tipo: `major | minor | patch`.
- `/release <X.Y.Z>` — força versão explícita (primeira release ou correção pontual).

Sem argumento e sem CC extraível → pergunta livre ao operador.

## Pré-condições

1. **Working tree limpo (bloqueia).** `git status --porcelain` vazio. Release com WT sujo mistura release com mudança não-revisada — broken-by-construction. Skill aborta sem perguntar; mensagem cita o sujo e direciona para stash/commit.
2. **Branch é o default do projeto (cutuca).** `git symbolic-ref --short HEAD` vs `main`/`master`. Diferente → enum (`AskUserQuestion`, header `Branch`) com `Prosseguir nesta branch` / `Cancelar e mudar`. Operador pode legitimamente fazer release de hotfix branch.

## Passos

### 1. Detectar versão e calcular bump

Buscar última tag (`git describe --tags --abbrev=0 2>/dev/null`; fallback `git tag --sort=-v:refname | head -n 1`). Atalho: argumento explícito (`/release minor`, `/release 2.0.0`) → pular pergunta.

Caso contrário, três sub-caminhos:

| Sub-caminho | Quando | Ação |
| --- | --- | --- |
| **1a** Bump inferido | ≥70% commits desde a tag seguem CC + tipo dominante claro | Enum (`AskUserQuestion`, header `Release`): `(a) <bump-proposto> → vX.Y.Z` / `(b) Outro bump` (Other → operador especifica). `description` carrega trade-off (tipo + contagem que motivou). |
| **1b** Histórico ambíguo | <70% CC ou empate entre tipos | Prosa livre — mostrar resumo dos commits agrupados por prefixo, perguntar qual bump. |
| **1c** Primeira release | Sem tag prévia | Enum: `(a) 0.1.0` (default canonical) / `(b) 1.0.0` / Other. |

Classificação CC (ignorar escopo entre parênteses):

- `feat:` → minor
- `fix:` / `refactor:` / `perf:` → patch
- `feat!:` ou `BREAKING CHANGE:` no body → major
- `docs:` / `chore:` / `style:` / `test:` sozinhos → patch (release pequena, mas válida)

### 2. Atualizar `version_files`

Disparar **apenas** se papel resolvido e lista não-vazia. "Não temos" ou vazio → skip silente.

Para cada path declarado, detectar formato por extensão:

- **`.json`:** atualizar chave `version` no top-level com regex conservadora preservando indentação.
- **`.toml`:** atualizar primeira ocorrência de `version = "..."` no top-level. Se ausente, tentar dentro de `[project]`, `[tool.poetry]`, `[package]`. Ainda ausente → gap report.
- **Outros formatos:** gap report — operador edita manualmente, confirma via enum (`Editado, prosseguir` / `Cancelar release`).

Computar transformação **em memória**. Reportar progressão (`version_files preparados: <paths>`). Escrita acontece no gate do passo 4.

### 3. Compor entrada de changelog

Disparar **apenas** se papel resolvido. "Não temos" → skip silente.

1. **Detectar formato** lendo as primeiras ~30 linhas. `## [X.Y.Z] - YYYY-MM-DD` no topo → Keep-a-Changelog (default canonical). Outros formatos (changelog livre, Towncrier) → gap report; operador edita, confirma.
2. **Compor rascunho** agrupando commits por prefixo:
   - `feat:` → `### Added`
   - `fix:` → `### Fixed`
   - `refactor:` / `perf:` → `### Changed`
   - `docs:` / `chore:` / `style:` / `test:` → `### Notes` (compactado)

   Cada bullet = subject do commit (sem hash — ruído num changelog editorial).
3. Manter rascunho **em memória**. Reportar progressão (`entrada de changelog para X.Y.Z preparada`). Escrita acontece no gate do passo 4 (inserir após cabeçalho `# Changelog`/intro, antes do bloco `## [versão-anterior]`).

### 4. Bloco de review consolidado e aplicação

Único ponto de I/O em disco e de operações git. Apresenta tudo o que os passos 2-3 prepararam em memória num bloco único.

1. **Detectar formato da tag em três níveis:**
   1. **Política explícita** (CLAUDE.md, CONTRIBUTING.md, hook).
   2. **Padrão observado** — `git tag --list --sort=-v:refname | head -n 10`; ≥70% seguindo formato extraível vence.
   3. **Default canonical:** SemVer 2.0 com `vX.Y.Z`.

   ≥70% das tags omitem `v` → usar sem prefixo. Skill **não** hardcoda `v`.

2. **Verificar colisão de tag.** `git rev-parse <tag> 2>/dev/null` indica existência → gap report sem perguntar. Skill **não** sobrescreve tag (mover tag é destrutivo de história e fora da blast radius local). Reportar; sugerir `git tag -d <tag>` se intencional ou bump diferente. Bloco consolidado nunca é mostrado quando há colisão.

3. **Compor mensagem de commit.** Default: `chore(release): bump version to X.Y.Z` — formato canonical para projetos CC. Convenção do projeto consumidor diverge → espelhar (ver `docs/philosophy.md` → "Convenção de commits").

4. **Mostrar bloco consolidado** com seções nomeadas:
   - **Arquivos de versão** — diffs do passo 2 (omitida se `version_files` desativado).
   - **Changelog** — entrada do passo 3 (omitida se `changelog` desativado).
   - **Commit** — mensagem composta no item 3.
   - **Tag** — `<tag>` (annotated, mensagem `Release <tag>`).

   Caso degenerado (ambos os papéis desativados): apenas Commit + Tag.

5. **Gate único** via `AskUserQuestion` (header `Release`) com três opções:
   - **`Aplicar`** — verificar HEAD: rodar `git symbolic-ref --short HEAD`. Se falha (detached) ou difere do branch da pré-condição 2, recovery proativo — `git status --porcelain`; se não-vazio, `git stash push -m "release v<X.Y.Z> auto-stash"`; depois `git checkout <branch-da-pré-condição-2>`. Em seguida, **antes da sequência (a)-(e)**: `git fetch origin <branch-da-pré-condição-2> 2>/dev/null`; `behind=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo 0)`; se `behind > 0`, `git pull --ff-only origin <branch-da-pré-condição-2>` — falha → abortar release com erro literal do git e instruir `git pull` manual. Reportar ao operador a ref-atual encontrada no início, o branch esperado, o nome da stash se criada, e o número de commits trazidos pelo pull se aplicável (operador roda `git stash pop` manualmente após release se desejar). Em seguida, executar em sequência: (a) escrever cada `version_file`; (b) inserir entrada no changelog; (c) `git add <paths-específicos>` (**não** `git add -A` — risco de capturar arquivos não-relacionados); (d) `git commit -m "<msg>"`; (e) `git tag -a <tag> -m "Release <tag>"`.
   - **`Editar`** — prosa livre. Operador descreve ajuste em qualquer elemento (bullet do changelog, mensagem do commit, nome da tag). Skill aplica no rascunho em memória, volta ao item 4 e re-pergunta.
   - **`Cancelar`** — abort silente. Nada para reverter em disco. Reportar.

### 5. Reportar e devolver controle

- Paths dos arquivos atualizados nos passos 2-3.
- Hash do commit e nome da tag aplicados no passo 4.

Frase final fixa:

> Release pronta localmente. Para publicar:
>
> ```
> git push --follow-tags
> # ou: git push && git push origin <tag>
> ```

Após exibir a instrução de push, oferecer criação de release no forge — auto-detect:

1. **Detect host:** parse `git remote get-url origin`. `github.com` → CLI `gh`; host casando regex `^gitlab\.` (gitlab.com ou GitLab corporativo `gitlab.<domínio>`) → CLI `glab`. Outros hosts → fallback textual com instrução genérica (operador cria release pela UI web ou CLI específica do forge); skip etapas 2-4.
2. **Verificar CLI:** `command -v <cli>` retorna não-zero → fallback textual mencionando o CLI esperado (`gh` em https://cli.github.com/, `glab` em https://gitlab.com/gitlab-org/cli) e link da UI web; skip etapas 3-4.
3. **Gate de confirmação:** montar comando — `gh release create <tag> --generate-notes` (autogen de notes pelo GitHub) ou `glab release create <tag> --notes "<body>"` (body lido da entrada recém-prependada no `changelog`: do header da nova versão até a linha imediatamente antes do próximo `## [versão-anterior]`, sem incluir o header da nova versão). Apresentar via `AskUserQuestion` (header `Forge`) com opções `Executar (após push)` / `Pular`. Decline → skip silente; o comando exibido no gate é a referência para cópia manual. O label `Executar (após push)` é o pré-requisito explícito — skill assume que operador rodou o push acima antes de aceitar.
4. **Executar:** `Bash` com o comando montado. Saída zero → reportar URL do release e seguir. Saída não-zero (ex.: tag ausente no remote, CLI não autenticado) → reportar erro literal e parar; release local permanece, operador resolve manual.

Sem remote configurado → skip auto-detect (release pronta localmente, push não aplicável).

## O que NÃO fazer

- Não fazer push automático — release é local; publicação é decisão explícita do operador.
- Não tocar arquivos de versão fora dos paths declarados em `version_files`.
- Não inferir bump de log que não segue Conventional Commits sem perguntar — falsa-confiança gera versionamento errado.
- Não sobrescrever tag existente — colisão é gap report, não merge.
