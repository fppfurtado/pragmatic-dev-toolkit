# Plano — Batch 1: tightening editorial pós-v1.20.0

## Contexto

Análise arquitetural pós-v1.20.0 identificou 5 mudanças cirúrgicas de mesmo eixo (compressão / disciplina editorial) que cabem num batch único de baixo risco e sem interdependência. Cada mudança aplica a própria filosofia do plugin a um ponto que ficou desalinhado nas releases anteriores.

**Linha do backlog:** plugin: batch 1 de tightening editorial pós-v1.20.0 — sanity check de docs como prosa (/run-plan 4.3), trim disciplinado de `## O que NÃO fazer` + critério editorial em CLAUDE.md, `disable-model-invocation` em /release e /run-plan, single-reviewer como caso normal (multi como exceção), /next propõe commit das movimentações automáticas

## Resumo da mudança

Cinco eixos independentes:

- **C2** — `/run-plan` passo 4.3 (sanity check de docs user-facing) hoje usa `AskUserQuestion` com opção única `Sim, consistente` + Other; o caminho real é Other. Por `philosophy.md` → "Convenção de pergunta ao operador": "quando a maioria das respostas reais cairia em Other, o modo certo era prosa desde o início." Reescrever como prosa livre.

- **C3** — `## O que NÃO fazer` cresceu além do necessário em várias skills; itens repetem prosa anterior do próprio skill (ex.: "não implementar" em `/triage`, "não corrigir" em `/debug`, "não criar ADR sem título" em `/new-adr`). Trim mantendo apenas guardas que documentam anti-padrão não-óbvio. Acrescentar critério editorial explícito em `CLAUDE.md` → "Editing conventions" para travar reinflação futura. `/run-plan` ganhou um item legítimo no #27 (não executar `gh pr create`); preservar.

- **D4** — `/new-adr` tem `disable-model-invocation: true` por ser ato deliberado. `/release` e `/run-plan` produzem efeitos visíveis comparáveis (commits, tags, push, micro-commits) e devem seguir a mesma disciplina. Adicionar o flag.

- **D1** — Schema multi-reviewer (`{reviewer: code,qa,security}`) está spec'ado como cidadão de primeira classe em 4 lugares (philosophy, /triage, /run-plan, exemplos). Uso real no repo: 73% single-reviewer, 9% combinações — e quase todas as combinações estão em planos auto-referentes (sobre adicionar a feature de combinação). Reframe textual: single-reviewer é o caso normal; combinações são exceção rara — preferir separar em blocos quando faz sentido revisar eixos diferentes.

- **E2** — `/next` move linhas para `## Concluídos` automaticamente quando detecta evidência forte. Mutação fica em disco sem commit; em sessão longa, divergência entre BACKLOG.md e estado git se acumula. Espelhar o padrão do `/triage` step 6: ao final, propor commit unificado das movimentações via gate enum (`Confirmar movimentações` / `Reverter`).

Refactor puramente editorial — sem comportamento novo, sem invariante de domínio tocada, sem integração nova.

## Arquivos a alterar

### Bloco 1 — `/run-plan` 4.3 sanity check de docs como prosa {reviewer: code}

- `skills/run-plan/SKILL.md` — passo 4.3 (linhas ~82-86):
  - Substituir `AskUserQuestion` (header `Docs`, opção única `Sim, consistente`; Other absorve a lista) por **prosa livre**.
  - Estrutura da prosa: citar superfície inferida, listar candidatos típicos (README, docs/install.md, docs internas), pedir resposta livre — `"consistente"` ou listagem de arquivos a atualizar. `CHANGELOG` segue fora (responsabilidade do `/release`).
  - Trabalho subsequente (atualizações listadas → bloco extra com `test_command` + revisor `code` + micro-commit antes do done) permanece igual.
  - Atualizar referência interna no `## O que NÃO fazer` se houver alusão ao enum.

### Bloco 2 — trim de `## O que NÃO fazer` + critério editorial {reviewer: code,doc}

Critério aplicado: manter **apenas guardas que documentam anti-padrão não-óbvio** — uma reflexão razoável a partir do resto do skill não evitaria o erro. Remover itens que apenas reafirmam prosa anterior do próprio documento.

- `skills/triage/SKILL.md` — `## O que NÃO fazer` (4 itens):
  - Remover `"Não implementar — esta skill é alinhamento puro"` (já dito no parágrafo de abertura).
  - Manter os 3 itens de commit/push (não-óbvios — vieram de incidentes de fan-out e merge artifact).

- `skills/run-plan/SKILL.md` — `## O que NÃO fazer` (8 itens, pós-#27):
  - Avaliar cada item pelo critério; remover apenas os que apenas paráfrazem o próprio skill. Items vindos de incidentes (`{revisor: ...}` PT, push falho via --force, gatilho cruzado de credencial, "não executar comando de abertura de PR/MR") são todos não-óbvios — preservar.
  - Esperado: redução de 0-2 itens.

- `skills/release/SKILL.md` — `## O que NÃO fazer` (5 itens):
  - Avaliar; provavelmente todos não-óbvios (push automático, GitHub Release fora de escopo, version_files, inferência sem CC, sobrescrever tag). Esperado: 0 remoções.

- `skills/debug/SKILL.md` — `## O que NÃO fazer` (5 itens):
  - Remover `"Não corrigir."` (3ª repetição no documento — abertura, passo 6, e seção). Manter os outros 4 (não pular reprodução, não declarar causa-raiz sem evidência, não aplicar instrumentação, não escrever ADR/plano/backlog).

- `skills/new-adr/SKILL.md` — `## O que NÃO fazer` (3 itens):
  - Remover `"Não criar ADR sem título"` (já guardado nos Argumentos: "Sem título → pedir antes de prosseguir").
  - Manter os outros 2 (não inventar conteúdo, não alterar ADRs existentes).

- `skills/next/SKILL.md` — `## O que NÃO fazer` (3 itens):
  - Avaliar; provavelmente todos não-óbvios. Esperado: 0 remoções.

- `skills/gen-tests-python/SKILL.md` — `## O que NÃO fazer` (3 itens):
  - Avaliar; mock SQLite e mock HTTP via unittest são não-óbvios. Esperado: 0 remoções.

- `skills/heal-backlog/SKILL.md` — `## O que NÃO fazer` (3 itens):
  - Avaliar; "não reconstruir via git log" é não-óbvio. Esperado: 0 remoções.

- `CLAUDE.md` — seção "Editing conventions":
  - Acrescentar item: `"## O que NÃO fazer em skills lista apenas guardas que documentam anti-padrão não-óbvio — itens que apenas reafirmam prosa anterior do skill são ruído. Critério editorial: remoção do item não confundiria um leitor razoável que leu o resto do skill."`

### Bloco 3 — `disable-model-invocation` em /release e /run-plan {reviewer: code}

- `skills/release/SKILL.md` — frontmatter:
  - Adicionar linha `disable-model-invocation: true` após `description:`.

- `skills/run-plan/SKILL.md` — frontmatter:
  - Adicionar linha `disable-model-invocation: true` após `description:`.

### Bloco 4 — single-reviewer como norma, multi como exceção {reviewer: code}

Reframe textual; sem mudança de schema (combinações continuam suportadas, apenas deixam de ser apresentadas como cidadãs de primeira classe).

- `skills/triage/SKILL.md` — passo 4 ("Plano", schema de `{reviewer: ...}`):
  - Reordenar bullets: single-reviewer primeiro como caso normal; combinações como exceção rara, com nota: "preferir separar em blocos quando viável — combinar só quando o mesmo diff genuinamente merece olhares de eixos diferentes (ex.: bloco que acrescenta endpoint público novo)".
  - Reduzir exemplos: manter Bloco 1 (`{reviewer: security}`), Bloco 3 (sem anotação), Bloco 4 (`{reviewer: doc}`); remover ou simplificar Bloco 2 (`{reviewer: code,qa,security}`) — ou substituir por exemplo single-reviewer mais comum.

- `skills/run-plan/SKILL.md` — passo 3 ("Escolher revisor"):
  - Mesma reordenação: single primeiro, combinações como exceção.
  - Exemplos: manter `### Bloco 1 — auth.py {reviewer: security}` e `### Bloco 2 — README {reviewer: doc}`; remover combinações se presentes.

### Bloco 5 — /next propõe commit das movimentações {reviewer: code}

- `skills/next/SKILL.md` — passo 3 ("Verificar implementação no código") e passo 5 ("Apresentar resultado e colher escolha"):
  - Após passo 3 mover linhas para `## Concluídos` automaticamente, **não** commitar in situ.
  - Adicionar passo entre o atual 5 e 6 (ou estender 5): se `## Concluídos` foi modificado nesta invocação, propor commit unificado via enum (`AskUserQuestion`, header `Movimentações`, opções `Confirmar e commitar` / `Reverter movimentações`). Mensagem: `chore(backlog): mark <N> concluded item(s)` (ou equivalente PT-BR no projeto consumidor).
  - `Reverter movimentações` → desfazer edits in-memory antes de continuar para o passo 6 (apresentar candidatos). Operador segue para escolha do top 3 sem mutação persistida.
  - `## Concluídos` não modificado → skip silente do gate.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **C2** — `grep -n "AskUserQuestion" skills/run-plan/SKILL.md` não retorna mais o enum do passo 4.3 (header `Docs`); a prosa nova cita superfície inferida e candidatos típicos.
2. **C3** — cada SKILL.md ainda tem `## O que NÃO fazer` (load-bearing per CLAUDE.md); itens remanescentes passam pelo critério não-óbvio. Diff mostra remoções esperadas (`/triage`, `/debug`, `/new-adr`); `CLAUDE.md` ganha item editorial em "Editing conventions".
3. **D4** — `grep -A1 "^name:" skills/release/SKILL.md skills/run-plan/SKILL.md` mostra `disable-model-invocation: true` em ambas.
4. **D1** — `/triage` passo 4 e `/run-plan` passo 3 abrem com single-reviewer como caso normal; exemplos de combinação reduzidos ou ausentes; schema continua aceitando combinações.
5. **E2** — `skills/next/SKILL.md` passo 3 não commita; passo extra propõe commit unificado via enum quando `## Concluídos` modificado.

Conferência cruzada: nenhum link/referência interna apontando para o enum `Docs` removido (C2) ou para exemplos multi-reviewer expurgados (D1) ficou pendurado.
