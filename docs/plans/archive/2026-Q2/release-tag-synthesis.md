# Plano — `/release` síntese de mudanças na mensagem da tag

## Contexto

Mensagem da tag anotada em `/release` passo 4 sequência (e) é hoje fixa: `git tag -a <tag> -m "Release <tag>"`. Útil para identificação mas pobre para archeology offline — operador rodando `git tag -n3 v1.23.0` ou `git show v1.23.0` não vê o que a release contém sem abrir o CHANGELOG.md (que pode não estar acessível em ambientes só-git: bare clones, mirrors offline, archeology pós-rename de arquivo).

Decisões tomadas no /triage:
- **Síntese: frase curta por header.** Skill compõe 1 linha por header presente agregando subjects de commit em prosa compacta. Ex.: `Added: convert run-plan §3.2/§3.3/§3.7 prose to AskUserQuestion enum; unify debug §1 prose into single call.` Headers vazios omitidos.
- **Fonte da síntese: subjects dos commits desde a última tag**, **não** os bullets do CHANGELOG. Razão: idioma da mensagem da tag deve seguir a convenção de commits do projeto consumidor (`docs/philosophy.md` → "Convenção de commits"). CHANGELOG pode estar em outro idioma (este repo: commits em EN, CHANGELOG em PT). Reusar a mesma classificação CC do passo 2 (`feat:` → Added, `fix:` → Fixed, `refactor:`/`perf:` → Changed, `docs:`/`chore:`/`style:`/`test:` → Notes).
- **Mostrar no bloco consolidado do passo 4.** Item `Tag —` do bloco passa a exibir a mensagem completa multilinha. Opção `Editar` do gate único já cobre ajuste em prosa livre.
- **Sem ADR.** Mudança em 1 SKILL sem alterar doutrina escrita; refinamento de implementação, não política do sistema.

**Linha do backlog:** plugin: `/release` compor mensagem de tag com síntese das mudanças — em vez de `Release vX.Y.Z` fixo, `git tag -a -m` carrega resumo compacto dos headers do CHANGELOG (Added/Changed/Fixed em 1-3 linhas). Útil para archeology offline (`git tag -n3`, `git show <tag>`) onde CHANGELOG não está acessível. Trade-off: duplica conteúdo já versionado; reavaliar se uso real em archeology justificar o custo.

## Resumo da mudança

Single SKILL edit em `skills/release/SKILL.md`: passo 4 ganha sub-passo de composição da mensagem de tag (após item 3 que compõe a mensagem de commit), item 4 (bloco consolidado) mostra a mensagem completa, sequência (e) usa a mensagem composta em vez do literal `"Release <tag>"`.

**Edge cases:**
- Sem commits CC desde a última tag (ex.: 1c primeira release sem histórico CC, ou cenário 1b com <70% CC): síntese vazia → fallback ao formato atual `Release <tag>` (linha única).
- Categoria CC sem commits: omitir o header correspondente (ex.: release só com `feat:` → só `Added:` aparece).
- Subjects longos: truncar cada linha de síntese em ~120 chars; "..." se cortado. Evita tag message gigantesca em release com subjects verbosos.

**Fora de escopo:**
- Não muda mensagem de commit (continua `chore(release): bump version to X.Y.Z`).
- Não muda formato do changelog em si.
- Não toca o release no forge (`gh release create --generate-notes` continua usando o body do GitHub, não a tag annotation).

## Arquivos a alterar

### Bloco 1 — `/release` síntese da mensagem da tag {reviewer: code}

- `skills/release/SKILL.md` passo 4:
  - **Após item 3** ("Compor mensagem de commit"), inserir item novo **3.5** ("Compor mensagem de tag"):
    - Reusar a classificação CC do passo 3 (mesmos commits agrupados por prefixo: `feat:` → Added, `fix:` → Fixed, `refactor:`/`perf:` → Changed, `docs:`/`chore:`/`style:`/`test:` → Notes). **Idioma segue os subjects dos commits** (convenção do projeto consumidor, `docs/philosophy.md` → "Convenção de commits") — não traduzir, não recompor a partir do CHANGELOG.
    - Disparar **apenas** se ≥1 commit CC classificável. Caso contrário (ex.: 1c primeira release; 1b com <70% CC), mensagem de tag é o literal `Release <tag>` (fallback ao comportamento atual).
    - Para cada categoria com ≥1 commit:
      - 1 commit → usar o subject (sem o prefixo CC) truncado em ~120 chars.
      - 2+ commits → unir os subjects (sem prefixo CC) com `; `, truncar resultado em ~120 chars com `...` se cortar.
      - Categoria sem commits → omitir do output.
    - Compor mensagem multilinha:
      ```
      Release <tag>

      Added: <síntese>
      Changed: <síntese>
      Fixed: <síntese>
      Notes: <síntese>
      ```
      Linhas das categorias vazias omitidas. Headers ficam em EN (`Added`/`Changed`/`Fixed`/`Notes`) por serem rótulos canônicos do toolkit, alinhados ao Keep-a-Changelog; conteúdo (subjects) acompanha o idioma dos commits.
  - **Item 4 do gate** (Mostrar bloco consolidado): substituir a linha **Tag** atual (`<tag> (annotated, mensagem `Release <tag>`)`) pela exibição completa da mensagem multilinha composta no item 3.5. Operador vê e pode acionar `Editar` para ajuste em prosa livre.
  - **Sequência (e) do `Aplicar`**: trocar `git tag -a <tag> -m "Release <tag>"` por chamada com múltiplos `-m` (`git tag -a <tag> -m "<linha-1>" -m "<linha-2>" -m "<linha-3>" ...`). Git separa parágrafos com linha em branco entre cada `-m` automaticamente. Mais legível e portátil que process substitution / heredoc.
- Atualizar `## O que NÃO fazer` se necessário (revisar — o item "Não inferir bump de log que não segue Conventional Commits sem perguntar" continua válido; nenhum NÃO-fazer novo é introduzido).

## Verificação end-to-end

Sem suite de testes; verificação textual da SKILL editada.

- `grep -n "git tag -a" skills/release/SKILL.md` mostra a chamada com múltiplos `-m`; literal `"Release <tag>"` único permanece só como fallback explícito quando não há commits CC classificáveis.
- `grep -n "Compor mensagem de tag" skills/release/SKILL.md` retorna o novo sub-passo 3.5.
- `grep -n "Tag —" skills/release/SKILL.md` mostra a linha atualizada do item 4 referenciando a mensagem multilinha (não mais `mensagem `Release <tag>`` literal).
- SKILL menciona explicitamente "idioma segue os subjects dos commits" no passo 3.5.
- Edge case do fallback: SKILL menciona explicitamente "se ≥1 commit CC classificável" como gatilho; ausência → mensagem fica `Release <tag>`.
- Edge case do truncamento: SKILL menciona limite ~120 chars com `...`.

Validação prática deferida: a próxima invocação de `/release` (após o merge deste plano) será o teste real — operador roda `/release`, verifica no bloco consolidado se a mensagem composta faz sentido, aplica, depois `git show <tag>` para confirmar o resultado.

## Notas operacionais

- **Limite de 120 chars por linha** é heurístico — `git tag` não impõe limite, mas terminais `git tag -n3` truncam em ~80 chars por linha visível. 120 dá margem para subjects descritivos sem virar parágrafo.
- **Implementação com múltiplos `-m`** é mais legível que process substitution e mais portátil entre shells. Uma `-m` por linha de síntese (`-m "Release <tag>"`, `-m "Added: ..."`, `-m "Changed: ..."`, etc.). Git automaticamente separa parágrafos com linha em branco entre cada `-m`.
- **Idioma da síntese** acompanha os subjects dos commits, não o CHANGELOG. Em projetos consumidores onde commits e CHANGELOG estão em idiomas diferentes (ex.: este repo: commits EN, CHANGELOG PT), a tag fica em EN. Headers (`Added`/`Changed`/`Fixed`/`Notes`) ficam em EN sempre — rótulos canônicos do toolkit alinhados ao Keep-a-Changelog.
- **Reviewer code-reviewer** (não doc) — apesar do arquivo ser `.md`, a mudança é operativa (composição de string que vira comando shell), YAGNI/edge-cases relevantes.
