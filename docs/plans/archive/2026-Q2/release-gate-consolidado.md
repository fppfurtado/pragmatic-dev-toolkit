# Plano — colapsar gates de `/release` num único review consolidado

## Contexto

Hoje a skill `/release` (`skills/release/SKILL.md`) tem três gates separados depois da decisão de bump:

- **Passo 2** — confirmação por arquivo (ou agregada) dos diffs nos `version_files`.
- **Passo 3** — pergunta livre "editar antes de aplicar / aplicar como está" sobre a entrada de changelog.
- **Passo 4** — gate único de commit + tag com `Aplicar` / `Editar mensagens`.

Na prática:

- Gate 2 é mecânico — diff é sempre `X.Y.Z` → `X.Y.Z+1`, raramente negado.
- Gate 3 é teatral — o modelo resume melhor o que foi feito a partir do log CC do que o operador, que raramente assume o trabalho de editar.
- Gate 4 é redundante — a decisão real foi tomada no Passo 1; "abort tardio" antes do commit/tag é uma terceira confirmação para uma decisão já tomada.

**Decisão:** colapsar 2+3+4 num único **bloco de review final consolidado** que mostra todos os elementos prestes a serem aplicados (diffs dos `version_files`, entrada do changelog, mensagem de commit, tag a criar) com gate único `Aplicar` / `Editar` / `Cancelar`. Reduz fricção sem perder visibilidade no ponto de não-retorno local.

**Mudança conceitual de arquitetura:** passos 2 e 3 viram **preparação em memória** — computam as transformações sem escrever em disco. I/O em disco e operações git acontecem apenas no `Aplicar` do gate único. Isso simplifica `Cancelar` (nada para reverter em filesystem) e `Editar` (rascunho mutável até o gate aprovar).

**Linha do backlog:** release: colapsar gates de version_files, changelog e commit/tag num único review final consolidado

## Resumo da mudança

- **Passo 2** vira preparação silenciosa: computa diffs dos `version_files` em memória; reporta progressão (`"version_files preparados: <paths>"`); sem `AskUserQuestion`.
- **Passo 3** vira preparação silenciosa: compõe rascunho da entrada de changelog em memória; reporta progressão (`"entrada de changelog para X.Y.Z preparada"`); sem pergunta livre.
- **Passo 4** vira **gate único consolidado**:
  - Pré-validações **antes** do bloco: detecção de formato da tag (3 níveis) e anti-colisão. Falhas continuam disparando gap report sem chegar ao bloco.
  - **Bloco de review** mostra, em seções nomeadas:
    1. **Arquivos de versão** — diffs preparados no passo 2 (omitida se papel `version_files` desativado).
    2. **Changelog** — entrada preparada no passo 3 (omitida se papel `changelog` desativado).
    3. **Commit** — mensagem composta.
    4. **Tag** — `<tag>` (annotated, mensagem `Release <tag>`).
  - Gate via `AskUserQuestion` (header `Release`) com três opções:
    - **`Aplicar`** — escreve `version_files`, escreve `changelog`, `git add` específico (não `-A`), `git commit -m "<msg>"`, `git tag -a <tag> -m "Release <tag>"`.
    - **`Editar`** — prosa livre (operador descreve ajuste em qualquer elemento: trocar bullet do changelog de `### Notes` para `### Changed`, reescrever mensagem de commit, mudar formato da tag, etc.); skill atualiza rascunho em memória; re-exibe o bloco; re-pergunta o gate.
    - **`Cancelar`** — abort silente; nada para reverter em disco (preparação foi em memória); reportar.
- **Caminhos degenerados:**
  - `version_files` resolvido para `não temos` → passo 2 silente; bloco omite seção 1.
  - `changelog` resolvido para `não temos` → passo 3 silente; bloco omite seção 2.
  - Ambos desativados → bloco mostra apenas commit + tag (caso degenerado documentado).

## Arquivos a alterar

### Bloco 1 — `skills/release/SKILL.md`

- Reescrever **Passo 2** (`Atualizar version_files`):
  - Remover `AskUserQuestion` agregado/individual ("Aplicar todos / Cancelar").
  - Substituir "Mostrar diff de cada arquivo antes de aplicar via enum" por "Computar diff em memória; reportar progressão; aplicação fica para o gate único do passo 4".
  - Manter detecção de formato por extensão e gap report para formatos desconhecidos (essas decisões são pré-bloco; um formato desconhecido inviabiliza preparação).
- Reescrever **Passo 3** (`Compor entrada de changelog`):
  - Remover pergunta livre "editar antes de aplicar / aplicar como está".
  - Substituir item 4 por "Compor entrada em memória; reportar progressão; gravação fica para o gate único do passo 4".
  - Manter detecção de formato (Keep-a-Changelog) e gap report para formatos desconhecidos.
- Reescrever **Passo 4** (`Aplicar commit + tag`):
  - Substituir os 7 itens atuais por 5 itens:
    1. Detectar formato da tag em três níveis (mantido).
    2. Verificar colisão de tag (mantido — gap report antes do bloco).
    3. Compor mensagem de commit (mantido).
    4. **Mostrar bloco de review consolidado** com as 4 seções (Arquivos de versão / Changelog / Commit / Tag), omitindo seções de papéis desativados.
    5. **Gate único** via `AskUserQuestion` (header `Release`) com `Aplicar` / `Editar` / `Cancelar`:
       - `Aplicar` → escreve em disco na ordem (version_files → changelog), `git add <paths-específicos>`, `git commit`, `git tag -a`.
       - `Editar` → prosa livre; skill aplica edits em memória (mesmo padrão atual de "Editar mensagens", mas escopo expandido para os 4 elementos); re-display; re-pergunta o gate.
       - `Cancelar` → reporta abort; nada em disco para reverter.
- Atualizar a seção `## O que NÃO fazer`:
  - Remover ou ajustar o item "Não pular o passo de changelog quando o papel está resolvido" se a redação do passo 3 mudou de forma incompatível.
  - Confirmar que "Não fazer push automático", "Não criar GitHub Release", "Não tocar arquivos de versão fora dos paths declarados", "Não inferir bump de log que não segue CC sem perguntar", "Não fazer release com working tree sujo", "Não sobrescrever tag existente", "Não amend commit de release publicada" continuam aplicáveis.

### Bloco 2 — `BACKLOG.md`

- Substituir a linha em `## Próximos`:
  - **De:** `release: gravar alterações no changelog sem confirmação do operador (espelhar política do backlog)`
  - **Para:** `release: colapsar gates de version_files, changelog e commit/tag num único review final consolidado`
- Mover a linha substituída para `## Em andamento` (caminho com plano).

## Verificação end-to-end

Sem suite automatizada (`test_command: null`). Verificação acontece via `## Verificação manual` abaixo.

## Verificação manual

Disparar `/release` neste próprio repo (dogfood) cobrindo cenários:

1. **Caminho feliz com bump inferido** — desde a última tag (`v1.16.0`) há ≥3 commits CC. Verificar:
   - Passo 1 propõe minor (com base nos commits desde a tag).
   - Passos 2 e 3 reportam progressão sem perguntar.
   - Passo 4 mostra bloco consolidado com 4 seções (Arquivos de versão / Changelog / Commit / Tag).
   - `Aplicar` escreve arquivos, cria commit + tag.
2. **Caminho `Editar` no bloco** — escolher `Editar`; descrever ajuste no changelog (ex.: mover bullet de `### Notes` para `### Changed`). Verificar:
   - Skill aplica edit em memória.
   - Re-exibe o bloco com a seção Changelog atualizada.
   - Re-pergunta o gate.
3. **Caminho `Cancelar`** — escolher `Cancelar` no bloco. Verificar:
   - Reporta abort.
   - `git status --porcelain` permanece vazio (nenhum arquivo alterado em disco).
   - Nenhum commit ou tag criado.
4. **Tag colidida** — forçar `/release 1.16.0` cuja tag já existe. Verificar:
   - Gap report dispara antes do bloco (no item 2 do passo 4 reescrito).
   - Bloco consolidado nunca é mostrado.
5. **`version_files` desativado** — em projeto consumidor de teste sem o papel (ou com `paths.version_files: null`). Verificar:
   - Passo 2 silente.
   - Bloco consolidado omite a seção "Arquivos de versão" e mostra apenas Changelog + Commit + Tag.
6. **`changelog` desativado** — em projeto consumidor de teste sem `CHANGELOG.md` e sem declaração no config. Verificar:
   - Passo 3 silente.
   - Bloco consolidado omite a seção "Changelog" e mostra apenas Arquivos de versão + Commit + Tag.

## Notas operacionais

- Hooks não são tocados.
- Convenção de commits do repo (Conventional Commits em inglês) preservada — release commit continua `chore(release): bump version to X.Y.Z`.
- Reverter alterações em disco no `Cancelar` deixa de ser uma preocupação porque preparação é em memória — esse é o ganho da mudança conceitual.
- Próxima release deste repo após implementar este plano dogfooda a nova UX (validação real do cenário 1).
