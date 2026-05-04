---
name: release
description: Bump de versão coordenado em arquivos declarados, entrada de changelog, commit unificado e tag anotada. Use quando o operador autorizou publicar uma release a partir de commits acumulados desde a última tag.
---

# release

Mecaniza a release de software num único ciclo: detecta a próxima versão a partir do log Conventional Commits desde a última tag, atualiza os arquivos declarados em `version_files`, escreve uma entrada no `changelog`, faz commit unificado e cria tag anotada local.

Esta skill **faz commit local e tag local; não faz push**. Publicação fica com o operador (`git push --follow-tags`) — release é ato visível a outros, decisão deliberada que sai da blast radius da skill.

## Argumentos

Todos opcionais:

- `/release` — sem argumento; skill infere bump do log CC desde a última tag.
- `/release <bump>` — força tipo do bump: `major | minor | patch`.
- `/release <X.Y.Z>` — força versão explícita (útil para primeira release ou correção pontual).

Argumento explícito vence inferência. Sem argumento e sem CC extraível no log → pergunta livre ao operador.

## Pré-condições

Para `version_files` e `changelog`, aplicar **Resolução de papéis** (ver `docs/philosophy.md`): probe canonical → bloco `<!-- pragmatic-toolkit:config -->` no CLAUDE.md → pergunta tri-state ao operador. Ambos informacionais — skill segue mesmo com `não temos` em ambos. Caso degenerado: só commit + tag (ver passo 1, sub-caminho 1c).

1. **Working tree limpo (bloqueia).** `git status --porcelain` deve ser vazio. Release com working tree sujo gera commit que mistura release com mudança não-revisada — broken-by-construction. Mensagem cita o que está sujo e direciona para `git stash` ou commit prévio. Skill aborta sem perguntar.
2. **Branch é o default do projeto (cutuca, não bloqueia).** `git symbolic-ref --short HEAD` vs `main`/`master`/equivalente. Se diferente, enum via `AskUserQuestion` (header `Branch`) com opções `Prosseguir nesta branch` e `Cancelar e mudar`. Operador pode legitimamente fazer release de hotfix branch.

## Passos

### 1. Detectar versão atual e calcular bump

1. Buscar última tag: `git describe --tags --abbrev=0 2>/dev/null` (fallback `git tag --sort=-v:refname | head -n 1`).
2. **Se há tag prévia:** listar commits desde a tag com `git log <last-tag>..HEAD --pretty=format:"%h %s"`. Classificar por prefixo Conventional Commits (ignorar escopo entre parênteses):
   - `feat:` → minor
   - `fix:` / `refactor:` / `perf:` → patch
   - `feat!:` ou `BREAKING CHANGE:` no body → major
   - `docs:` / `chore:` / `style:` / `test:` sozinhos → patch (release pequena, mas válida)
   - **Critério mecânico ≥70%** dos commits seguindo CC para confiar na inferência (espelho da Convenção de commits em `docs/philosophy.md`). Senão, cair no sub-caminho 1b.
3. **Sub-caminho 1a — bump inferido com confiança (≥70% CC + tipo dominante claro):** enum via `AskUserQuestion` (header `Release`) com proposta como primeira opção: `(a) <bump-proposto> → vX.Y.Z` e segunda opção `(b) Outro bump` (Other → operador especifica `minor|patch|major|X.Y.Z`). `description` de cada opção carrega o trade-off (tipo + contagem de commits que motivou).
4. **Sub-caminho 1b — histórico CC ambíguo (<70% ou empate entre tipos):** prosa livre — mostrar resumo dos commits agrupados por prefixo, perguntar ao operador qual bump aplicar.
5. **Sub-caminho 1c — primeira release (sem tag prévia):** propor `0.1.0` como default canonical via enum (`(a) 0.1.0` / `(b) 1.0.0` / Other → versão explícita).
6. **Atalho:** se o operador passou argumento (`/release minor`, `/release 2.0.0`), pular pergunta — argumento vence.

### 2. Atualizar `version_files`

Disparar **apenas** se o papel `version_files` está resolvido e a lista é não-vazia. Papel `não temos` ou lista vazia → pular silenciosamente.

Para cada path declarado, ler o arquivo e detectar formato por extensão:

- **`.json`:** atualizar chave `version` no top-level. Regex conservadora preservando indentação.
- **`.toml`:** atualizar primeira ocorrência de `version = "..."` no top-level. Se não encontrada, tentar dentro de `[project]`, `[tool.poetry]` ou `[package]`. Se ainda não encontrada, gap report.
- **Outros formatos:** gap report — skill não mexe em formato desconhecido. Reportar ao operador qual arquivo, pedir edição manual, aguardar via enum (`Editado, prosseguir` / `Cancelar release`). Path canonical de extensibilidade futura.

Mostrar diff de cada arquivo antes de aplicar. Quando todos os diffs são mecânicos (mesma troca `X.Y.Z` → `X.Y.Z+1`), uma confirmação enum única (`Aplicar todos` / `Cancelar`) basta.

### 3. Compor entrada de changelog

Disparar **apenas** se o papel `changelog` está resolvido. Papel `não temos` → pular silenciosamente.

1. **Detectar formato existente** lendo as primeiras ~30 linhas. Heurística: se há linha tipo `## [X.Y.Z] - YYYY-MM-DD` no topo do conteúdo, formato é Keep-a-Changelog (default canonical do toolkit). Outros formatos (changelog livre, Towncrier, etc.) → gap report; skill não tenta adivinhar, operador edita manualmente, depois confirma.
2. **Compor rascunho** agrupando commits por prefixo CC:
   - `feat:` → `### Added`
   - `fix:` → `### Fixed`
   - `refactor:` / `perf:` → `### Changed`
   - `docs:` / `chore:` / `style:` / `test:` → `### Notes` (compactado)

   Cada bullet referencia o subject do commit (sem hash — barulho num changelog editorial).
3. **Mostrar rascunho ao operador em prosa**, explicitando: o rascunho é mecânico; **prosa editorial** (a "história" do que mudou, conexão com bumps anteriores, racional de design) é responsabilidade do operador. Pergunta livre: "Eis o rascunho da entrada [X.Y.Z]. Quer editar antes de aplicar, ou aplicar como está?". Espelha o passo 5 do `/new-feature` — revisão sugere; operador decide.
4. Operador edita em prosa livre (citando seção/bullet e nova redação) ou aprova como está. Skill aplica edits e insere o bloco no topo do changelog (após cabeçalho `# Changelog`/intro, antes do bloco `## [versão-anterior]`).

### 4. Commit unificado

1. Stagear apenas os arquivos efetivamente modificados nos passos 2 e 3. **Não usar `git add -A`** — risco de capturar arquivos não-relacionados.
2. **Mensagem default:** `chore(release): bump version to X.Y.Z` — formato canonical para release commits em projetos CC. Se a Convenção de commits do projeto consumidor diverge (gitmoji, prefixos custom), espelhar (ver `docs/philosophy.md` → "Convenção de commits"; mesma mecânica de detecção das outras skills).
3. Confirmar via enum (`AskUserQuestion`, header `Commit`) — opções `Confirmar` e `Editar mensagem` (Other → mensagem alternativa).

### 5. Tag anotada

1. **Formato da tag detectado em três níveis** (mecânica embutida nesta skill, espelho da Convenção de commits):
   1. **Política explícita** declarada no projeto — bloco no CLAUDE.md, `CONTRIBUTING.md`, hook ou equivalente.
   2. **Padrão observado** nas últimas tags via `git tag --list --sort=-v:refname | head -n 10` — ≥70% seguindo um formato extraível (com `v`, sem `v`, prefixo custom como `release-`, etc.) vence.
   3. **Default canonical:** SemVer 2.0 com `vX.Y.Z`.

   Quando ≥70% das tags observadas omitem `v` (caso comum em alguns repos), usar formato sem prefixo. Skill **não** hardcoda `v`.
2. `git tag -a <tag> -m "Release <tag>"` por default. Operador pode customizar a mensagem da tag em prosa livre (raro — annotation costuma ser mecânica).
3. Confirmar via enum (`AskUserQuestion`, header `Tag`) — opções `Criar tag` e `Cancelar e desfazer commit`. `Cancelar` executa `git reset --hard HEAD~1` (destrutivo, mas é o que o operador pediu; ainda dentro da blast radius local).
4. **Verificar colisão.** Se `<tag>` já existe (`git rev-parse <tag> 2>/dev/null`), gap report — skill **não** sobrescreve tag (mover tag é destrutivo de história e fora da blast radius local). Reportar ao operador, sugerir `git tag -d <tag>` se intencional ou bump diferente.

### 6. Reportar e devolver controle

Reportar ao operador, em formato curto:

- Caminhos dos arquivos atualizados nos passos 2 e 3.
- Hash do commit do passo 4.
- Nome da tag do passo 5.

Frase final fixa:

> Release pronta localmente. Para publicar:
>
> ```
> git push --follow-tags
> ```
>
> GitHub Release (se aplicável): `gh release create <tag>`.

Os dois passos manuais ficam explícitos — push e GitHub Release são decisões do operador, fora da skill.

## O que NÃO fazer

- Não fazer push automático — release é local; publicação é decisão explícita do operador.
- Não criar GitHub Release — `gh release create` cobre o caso, fora do escopo da skill.
- Não tocar arquivos de versão fora dos paths declarados em `version_files` — escopo é o que o papel define.
- Não inferir bump de log que não segue Conventional Commits sem perguntar — falsa-confiança gera versionamento errado.
- Não fazer release com working tree sujo — pré-condição 1 bloqueia explicitamente; operador stash/commit primeiro.
- Não sobrescrever tag existente — colisão é gap report, não merge.
- Não amend commit de release de versão já publicada — `--amend` reescreve história já compartilhada (só seguro pré-push, e mesmo assim apenas dentro da janela de fixup; release é cadência diferente).
- Não pular o passo de changelog quando o papel está resolvido — drift entre código e changelog é exatamente a dor que motivou a skill.
- Não hardcodar formato `vX.Y.Z` — detectar do histórico de tags do repo (passo 5.1).
