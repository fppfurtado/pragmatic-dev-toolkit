# Desacoplar GitHub-específico em skills

## Contexto

Duas skills do plugin chamam ou sugerem ferramenta `gh` (GitHub CLI) diretamente, sem alternativa para consumidores hospedados em GitLab (corporativo) ou outros forges:

- `skills/run-plan/SKILL.md:128` — passo 7 (Sugestão de publicação): opção `Push + abrir PR` do enum `Publicar` executa `git push` seguido de `gh pr create`. Consumidores fora do GitHub veem o comando falhar.
- `skills/release/SKILL.md:118` — passo 5 (Reportar e devolver controle): a frase final fixa termina com `> GitHub Release (se aplicável): `gh release create <tag>`.`. Texto puro (não executado), mas GitHub-específico.
- `skills/release/SKILL.md:123` — entrada em `## O que NÃO fazer` referencia `gh release create` para delimitar escopo.

URLs `https://github.com/...` em README/install/philosophy/marketplace são apenas hospedagem do plugin e não constringem o consumidor — ficam fora do escopo.

A direção é a mínima discutida no triage prévio: **substituir** chamada e textos por **sugestão neutra ao operador**, sem auto-detect (`git remote -v`) e sem novo role `forge` no path contract. Auto-detect e role `forge` voltam à mesa só se atrito recorrente justificar a abstração — registro do gancho fica na linha do backlog.

**Linha do backlog:** plugin: desacoplar de GitHub-específico — `/run-plan` (4.7) chama `gh pr create` no enum `Push + abrir PR`, e `/release` sugere `gh release create` no texto final; consumidores em GitLab (corporativo) ficam sem caminho. Direção mínima: substituir chamada e texto por sugestão neutra ao operador (push + instrução textual com exemplos `gh`/`glab`/UI web), sem auto-detect nem role `forge`. Reavaliar evolução (auto-detect via `git remote -v` ou role `forge` no path contract) só se atrito recorrente justificar a abstração.

## Resumo da mudança

- `/run-plan` passo 7: a opção do enum `Publicar` que abria PR vira **`Push + sugerir abertura de PR/MR`** — executa apenas `git push` (mesma flag que a opção `Push`) e imprime instrução textual neutra com exemplos por forge (`gh pr create` para GitHub, `glab mr create` para GitLab, ou UI web).
- `/release` frase final: substituir "GitHub Release (se aplicável): `gh release create <tag>`" por sugestão neutra de release no forge, com exemplos `gh release create`/`glab release create`/UI web.
- `/release` `## O que NÃO fazer`: generalizar a entrada equivalente — escopo é "não criar release no forge automaticamente", não específico do GitHub.

Mudanças não exigem novo código, novo role nem auto-detect. Mantém-se a propriedade de operação manual explícita já estabelecida (push e abertura de PR/MR são decisão humana).

## Arquivos a alterar

### Bloco 1 — `/run-plan` enum Publicar neutro {reviewer: code}

- `skills/run-plan/SKILL.md`
  - Linha 128 (`- \`Push + abrir PR\` → push + \`gh pr create\`.`): substituir por opção que faz apenas `git push -u origin <branch-atual>` e imprime instrução textual com exemplos por forge.
  - Conferir referências cruzadas internas no mesmo arquivo: linha 122 (rebase limpo) menciona "`Push` e `Push + abrir PR`" — atualizar nomes das opções para refletir a renomeação. Linha 143 (`## O que NÃO fazer`) menciona "abrir PR" — confirmar que continua coerente.

### Bloco 2 — `/release` frase final e guard neutros {reviewer: code}

- `skills/release/SKILL.md`
  - Linha 118 (`> GitHub Release (se aplicável): \`gh release create <tag>\`.`): substituir por sugestão neutra com exemplos por forge (e UI web).
  - Linha 123 (`- Não criar GitHub Release — \`gh release create\` cobre o caso, fora do escopo da skill.`): generalizar para "não criar release no forge — comandos como `gh release create`/`glab release create` ou UI cobrem o caso, fora do escopo da skill".

## Verificação end-to-end

Plugin tem `test_command: null` (sem suite). Validação é a inspeção textual desta seção e a manual abaixo.

- Diff de `skills/run-plan/SKILL.md` mantém a estrutura do enum `Publicar` (três opções, header `Publicar`, mesmo posicionamento) e as referências cruzadas no texto de rebase limpo continuam coerentes com os novos nomes.
- Diff de `skills/release/SKILL.md` preserva a estrutura da frase final (bloco em quote, comando de push antes, sugestão de release depois) e a entrada em `## O que NÃO fazer` mantém o tom conciso das demais entradas.
- Nenhuma menção a `gh ` ou `gh pr`/`gh release` permanece em texto que descreva comportamento default da skill — apenas em listas de exemplos.

## Verificação manual

Smoke test em consumidor real (este próprio repo é consumidor válido para `/run-plan` ao implementar este plano).

1. **`/run-plan` — enum Publicar (caminho-feliz, GitHub).** Executar este plano via `/run-plan desacoplar-gh-em-skills` em consumidor com remote `origin` GitHub e branch nova; chegar ao passo 7. Confirmar:
   - Enum `Publicar` aparece com três opções, sendo a do meio renomeada para algo equivalente a `Push + sugerir abertura de PR/MR` (sem mencionar GitHub no rótulo).
   - Selecionar a opção do meio: skill executa `git push` e em seguida imprime instrução textual mencionando `gh pr create` (ou `glab mr create`, ou UI web) como **exemplos**, sem disparar `gh pr create` automaticamente.
   - Selecionar `Push`: comportamento inalterado (apenas `git push`).
   - Selecionar `Nenhum`: comportamento inalterado (encerra).
2. **`/release` — frase final.** Em release dogfood subsequente neste repo (não exigir nova release apenas para validar; aproveitar próxima cadência), confirmar visualmente que a frase final menciona "release no forge" com exemplos `gh release create` / `glab release create` / UI, sem texto único "GitHub Release".

Cenários (1) e (2) cobrem ambos os pontos de mudança. Não há surface não-determinística (sem parsing de dado externo, sem comportamento de agente LLM dependente de input variado) — os "dados reais" são apenas o texto dos enums e da frase final, observáveis diretamente na execução.

## Notas operacionais

- Mudança contida (texto de instrução em duas skills); sem migração, sem impacto em hooks ou agentes.
- Se atrito recorrente surgir (operador frequentemente copiando comando do exemplo em vez de ter ação automatizada), reavaliar evolução: (a) auto-detect via `git remote -v` casando padrões `github.com`/`gitlab.com`/domínio corporativo; (b) role `forge` no path contract com override explícito. A linha do backlog registra o gancho para reabrir.

## Pendências de validação

- Cenário 1 do `## Verificação manual` (enum `Publicar` neutro) — não exercitável nesta execução porque o próprio `/run-plan` que aplicou as mudanças roda da versão instalada do plugin (sem os diffs). Validar na próxima invocação de `/run-plan` em consumidor com remote configurado, após estas mudanças entrarem em `main` e o plugin local ser atualizado.
- Cenário 2 do `## Verificação manual` (frase final neutra de `/release`) — observar visualmente na próxima release dogfood deste repo.
