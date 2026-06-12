# Plano — Auto-detect de forge em /run-plan e /release

## Contexto

`/run-plan` (passo 4.7) e `/release` (frase final) sugerem comandos de PR/MR e release como instrução textual neutra com exemplos por forge — operador precisa copiar/colar a cada demanda implementada. Atrito reportado em uso justifica sair do "reavaliar se" para "implementar" — direção: parse `git remote -v` → mapear domínio (`github.com` → `gh`, `gitlab.*` → `glab`) → executar comando do forge com gate de confirmação. Fallback textual quando CLI ausente ou remote desconhecido (preserva caminho atual).

**Linha do backlog:** plugin: implementar auto-detect de forge em `/run-plan` (4.7) e `/release` — parse `git remote -v` → mapear domínio (`github.com` → `gh`, `gitlab.*` → `glab`) → executar comando do forge com gate de confirmação; fallback textual quando CLI ausente ou remote desconhecido. Continuação do item "desacoplar de GitHub-específico" em ## Concluídos.

## Resumo da mudança

Substituir, em `/run-plan` 4.7 e `/release` final, a instrução textual neutra por mecânica de detect-and-execute:

1. **Detect host:** parse `git remote get-url origin` (mais confiável que `git remote -v` para script). Extrair host. `github.com` → CLI `gh`; host casando regex `^gitlab\.` (gitlab.com ou GitLab corporativo `gitlab.<domínio>`) → CLI `glab`. Outros hosts → fallback textual.
2. **Verificar CLI disponível:** `command -v <cli>` retorna não-zero → fallback textual mencionando o CLI esperado e link da UI web.
3. **Gate de confirmação:** mostrar comando montado via `AskUserQuestion` (header `Forge`) com opções `Executar` / `Pular`. Decline → skip silente; o comando exibido no gate serve de referência para o operador copiar se quiser executar manual depois.
4. **Executar:** `Bash` com o comando montado. Saída não-zero → reportar erro literal e parar; estado prévio (push em /run-plan ou tag em /release) permanece e operador resolve manualmente.

**Conteúdo do PR/MR e release** — usar defaults simples das ferramentas:

- `/run-plan` (PR/MR): `gh pr create --fill --base <branch-principal>` ou `glab mr create --fill --target-branch <branch-principal>`. `--fill` puxa título e body do último commit. Branch principal vem de `git symbolic-ref refs/remotes/origin/HEAD` (canonical) com fallback para `main`.
- `/release` (release): `gh release create <tag> --generate-notes` ou `glab release create <tag> --notes "<body-do-changelog>"`. Para `glab`, body montado pela skill a partir da entrada recém-prependada no `changelog` (mesmo bloco que o passo de Aplicar editou); `gh` usa autogen do GitHub.

Mudança remove as entradas correspondentes de `## O que NÃO fazer` em ambas as skills (a vedação inverte-se: agora a skill executa, com gate).

## Arquivos a alterar

### Bloco 1 — /run-plan: auto-detect e execução de PR/MR {reviewer: code}

- `skills/run-plan/SKILL.md` (passo 4.7): substituir opção atual `Push + sugerir PR/MR` (que apenas imprime exemplos) por `Push + abrir PR/MR` que (i) executa `git push -u origin <branch-atual>`, (ii) detecta forge via remote, (iii) verifica CLI, (iv) gate de confirmação com comando montado, (v) executa ou cai no fallback textual. Manter `Push` (sem PR/MR) e `Nenhum`. Sem remote → skip silente (atual).
- `skills/run-plan/SKILL.md` (`## O que NÃO fazer`): remover entrada "Não executar comando de abertura de PR/MR no forge — opção `Push + sugerir PR/MR` apenas imprime exemplos; abertura efetiva é decisão e ação do operador."

### Bloco 2 — /release: auto-detect e execução de release {reviewer: code}

- `skills/release/SKILL.md` (frase final fixa, "Release no forge (se aplicável)..."): substituir texto neutro por mecânica análoga (detect → CLI check → gate com comando montado → executar ou fallback). Manter o bloco textual de `git push --follow-tags` separado (push é decisão prévia ao forge).
- `skills/release/SKILL.md` (`## O que NÃO fazer`): remover entrada "Não criar release no forge — comandos como `gh release create` / `glab release create` ou UI web cobrem o caso, fora do escopo da skill."

## Verificação end-to-end

- `grep -n "imprimir instrução textual neutra" skills/run-plan/SKILL.md` → vazio (substituído).
- `grep -n "Não executar comando de abertura de PR" skills/run-plan/SKILL.md` → vazio (removido).
- `grep -n "Release no forge (se aplicável)" skills/release/SKILL.md` → vazio (substituído).
- `grep -n "Não criar release no forge" skills/release/SKILL.md` → vazio (removido).
- Read das duas skills: novo texto descreve detect → check CLI → gate → execute → fallback de forma coerente, com formas exatas de remote enumeradas em prosa quando relevante para o leitor da skill.

## Verificação manual

Cenários de detecção contra remote real (parsing é surface não-determinística — exigir cobertura concreta antes do done):

1. **GitHub via SSH:** `git@github.com:fppfurtado/repo.git` → host = `github.com` → CLI = `gh` → gate exibe `gh pr create --fill --base main`. Aceitar → PR criado.
2. **GitHub via HTTPS:** `https://github.com/fppfurtado/repo.git` → mesmo host → mesmo comando.
3. **GitLab.com via SSH:** `git@gitlab.com:group/project.git` → host casa `^gitlab\.` → CLI = `glab` → gate exibe `glab mr create --fill --target-branch main`.
4. **GitLab corporativo (HTTPS):** `https://gitlab.example.com/group/project.git` → host casa `^gitlab\.` → mesmo CLI/comando.
5. **Bitbucket (não-suportado):** `git@bitbucket.org:owner/repo.git` → host fora do mapeamento → fallback textual com instrução genérica (push aconteceu; operador abre PR pela UI ou CLI específica).
6. **CLI ausente:** remote GitHub mas `gh` não instalado → fallback textual mencionando `gh` como caminho sugerido + link `https://cli.github.com/`.
7. **Sem remote:** `git remote get-url origin` falha → skip silente (comportamento atual preservado).
8. **Decline do gate:** operador escolhe `Pular` → skip silente; o comando exibido no gate é a referência para cópia manual.
9. **Falha do comando:** `gh pr create` retorna não-zero (ex.: `gh` não autenticado, sem repo no GitHub correspondente) → reportar erro literal e parar; push em /run-plan já aconteceu (operador resolve manual).

Mesma matriz para `/release` substituindo o comando exibido por `gh release create <tag> --generate-notes` / `glab release create <tag> --notes "..."`.

## Notas operacionais

- Mapeamento `^gitlab\.` é deliberadamente liberal — qualquer host iniciando com `gitlab.` casa. Trade-off: `gitlab-foo.example.com` não casaria (não começa com `gitlab.`), o que é correto; `gitlab.foo-corp.com` casa, esperado. Hosts que se autodescrevem como GitLab mas com nome diferente (raro) caem no fallback do cenário 5.
- `--fill` (gh/glab) e `--generate-notes` (gh) são deliberadamente os defaults mais simples — operador pode customizar via flags adicionais depois (não é parte deste plano).
- `command -v <cli>` é o probe canônico POSIX. Não usar `which` (variations entre shells e ausência em alguns containers).
- Bloco 1 e Bloco 2 são independentes — pode executar em qualquer ordem.
- Push e tag (estados prévios à execução do forge) permanecem em caso de falha do CLI — operador resolve manual; não há rollback automático.
