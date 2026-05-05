# Reduzir cerimônia de `AskUserQuestion` em skills do toolkit

## Contexto

Três skills perguntam ao operador via `AskUserQuestion` em pontos onde a resposta é um valor único derivado de decisão já confirmada upstream — pergunta cerimonial sem alternativa real entre opções. Padrão observado dogfooding `/release` v1.14.0 e estendido por inspeção a `/run-plan` e `/triage`:

- **`/release` passos 4 (commit) e 5 (tag):** mensagem de commit (`chore(release): bump version to X.Y.Z`) e nome de tag (formato `vX.Y.Z` detectado mecânicamente) são 100% derivados do bump confirmado no passo 1. Confirmar cada um separadamente é cerimônia sem decisão.
- **`/run-plan` 4.5 (backlog harvest):** pergunta sempre dispara antes de declarar done (`Nada a registrar` / `Há itens`). Quando nada emergiu durante a execução, "Nada a registrar" é a única resposta razoável — pergunta vira ruído.
- **`/triage` 5 (revisão do backlog):** versão minimal (sem flags de duplicata/obsolescência + 1 linha adicionada) pergunta `Ok` / `Ajustar` para confirmar uma linha que o operador acabou de decidir adicionar no passo 4.

A regra geral está implícita no critério "descrição-óbvia tipo 'escolha A' é sintoma de enum cosmético" da seção "Convenção de pergunta ao operador" (`docs/philosophy.md`), mas falta uma guarda explícita contra o caso "valor único derivado". Sem essa guarda, futuras skills vão recriar o mesmo padrão.

**Decisões já fechadas (não revisitar):**

- **Codificar a guarda em `docs/philosophy.md` antes de aplicar nas skills.** Bloco 1 estabelece o princípio; blocos 2-4 são aplicações concretas. Ordem load-bearing — referencias cruzadas das skills apontam para a nova guarda na philosophy.
- **`/release`: fundir passos 4 e 5 num único passo "Aplicar commit + tag (gate único)".** Renumera passo 6 (Reportar) para passo 5. Skill prepara mensagem + tag + verifica colisão + mostra `git status`/mensagem/tag num bloco único + uma única `AskUserQuestion`. Após `Aplicar`: executa commit + tag em sequência mecânica.
- **`/run-plan` 4.5: skill mantém lista de itens capturados durante execução** via sinal explícito do operador ("isso fica pra depois", "registra no backlog") ou finding de revisor marcado como fora-de-escopo. Lista vazia → skip silente. Lista não-vazia → mostra os itens em prosa e confirma/ajusta/descarta.
- **`/triage` 5: a checagem (releitura + flag) sempre roda.** Sem flags → skip silente. Com flags → pergunta dispara como hoje, mostrando o que precisa de decisão. Linhas adicionadas no passo 4 não precisam de re-confirm.
- **Manter pergunta editorial no `/release` passo 3 (CHANGELOG).** Composição da entrada envolve **prosa editorial** (a "história" do que mudou) — decisão real do operador, não cerimônia. Fora do escopo deste plano.
- **Sem migração para projetos consumidores.** Mudança é em skills do plugin; usuários atualizam ao puxar a nova versão. Não há breaking change de schema.

## Resumo da mudança

Quatro blocos sequenciados:

1. **Bloco 1 — Codificar guarda em `docs/philosophy.md`.** Adiciona parágrafo "Não perguntar por valor único derivado" abaixo dos dois bullets enum/prosa em "Convenção de pergunta ao operador". Bloco isolado porque é a referência que blocos 2-4 vão citar.
2. **Bloco 2 — `/release`: fundir passos 4 + 5 em gate único.** Reescreve a sequência commit → tag para um único passo "Aplicar commit + tag (gate único)". Renumera "Reportar e devolver controle" de passo 6 para passo 5. Atualiza `## O que NÃO fazer` com guarda contra confirmar separadamente.
3. **Bloco 3 — `/run-plan` 4.5: harvest condicional.** Reescreve a sub-seção "Backlog harvest": skill mantém lista durante execução, gate fecha silente quando vazia. Atualiza `## O que NÃO fazer` com guardas contra perguntar com lista vazia e contra fabricar itens via leitura tardia.
4. **Bloco 4 — `/triage` 5: revisão condicional.** Reescreve passos 3-4 (mostrar + perguntar) para depender de flags. Sem flags → skip silente. Com flags → pergunta dispara mostrando síntese. Atualiza `## O que NÃO fazer` clarificando que a checagem sempre roda; o que pula é a pergunta.

## Arquivos a alterar

### Bloco 1 — Guarda em `docs/philosophy.md` {reviewer: code}

- `docs/philosophy.md` seção "Convenção de pergunta ao operador" (após o segundo bullet "Prosa"):
  - Adicionar parágrafo novo iniciado por **"Não perguntar por valor único derivado."** (negrito). Conteúdo: quando o valor é 100% derivado de decisão já confirmada upstream (ex.: mensagem de commit mecânica após bump confirmado, nome de tag após formato detectado, conteúdo de arquivo gerado a partir de template), pular o confirm. Janela de "abort tardio" vem de tornar visível antes de aplicar — `git status` antes do commit, diff antes do write — não de cerimônia adicional. Confirms acumulam para ações irreversíveis ou destrutivas (push, force, drop), não para mecânica derivada. Skills que precisam aplicar N valores derivados da mesma decisão consolidam num gate único, mostrando todos os valores juntos.
  - Verificar que o parágrafo **não** quebra a referência da última frase da seção (que cita "Pontos do toolkit onde a convenção aplica") — o parágrafo entra antes dessa frase.

### Bloco 2 — `/release`: gate único de commit + tag {reviewer: code}

- `skills/release/SKILL.md`:
  - **Substituir passos 4 ("Commit unificado") e 5 ("Tag anotada") por um único passo 4 "Aplicar commit + tag (gate único)"**, com 7 sub-itens:
    1. Stagear apenas os arquivos modificados nos passos 2 e 3 (sem `git add -A`).
    2. Compor mensagem de commit (default `chore(release): bump version to X.Y.Z`; espelhar Convenção de commits do projeto consumidor se diverge).
    3. Detectar formato da tag em três níveis (política → padrão observado ≥70% → SemVer canonical `vX.Y.Z`).
    4. Verificar colisão de tag — se existe, gap report sem perguntar.
    5. Mostrar `git status` dos staged + mensagem de commit + tag a criar, num bloco único (janela de abort tardio).
    6. Gate único via `AskUserQuestion` (header `Release`, opções `Aplicar` e `Editar mensagens`).
    7. Após `Aplicar`: executar `git commit -m "<msg>"` seguido de `git tag -a <tag> -m "Release <tag>"`. Sem perguntas intermediárias.
  - Texto introdutório do passo 4 cita explicitamente: "Commit e tag são valores 100% derivados das decisões já confirmadas (bump no passo 1, conteúdo do changelog no passo 3) — confirmar cada um separadamente é cerimônia (ver `docs/philosophy.md` → 'Convenção de pergunta ao operador')."
  - **Renumerar** "Reportar e devolver controle" de passo 6 para passo 5. Atualizar bullets internos: "Hash do commit do passo 4. Nome da tag do passo 5." → "Hash do commit e nome da tag aplicados no passo 4."
  - **Adicionar guarda em `## O que NÃO fazer`:** "Não confirmar separadamente commit e tag — passo 4 tem gate único por construção; perguntar duas vezes por valores derivados da mesma decisão é cerimônia (ver `docs/philosophy.md` → 'Convenção de pergunta ao operador')."

### Bloco 3 — `/run-plan` 4.5: harvest condicional {reviewer: code}

- `skills/run-plan/SKILL.md` passo 4.5 ("Backlog harvest"):
  - **Reescrever a sub-seção** para: "durante a execução dos blocos (passo 3), capturar itens que **emergiram explicitamente** via sinal do operador ('isso fica pra depois', 'registra no backlog', 'deferir') ou via finding de revisor marcado como fora-de-escopo deste plano. A skill mantém essa lista enquanto progride. No gate final:
    - **Lista vazia** → skip silente (nada emergiu, nada a registrar; pergunta cerimonial só ruidaria — ver `docs/philosophy.md` → 'Convenção de pergunta ao operador').
    - **Lista não-vazia** → mostrar os itens capturados ao operador em prosa e perguntar (livre): 'Capturei estes itens durante a execução. Confirma o registro como está, ajusta a redação, ou descarta algum?'. Após confirmação, tratar como **bloco extra** (atualizar arquivo do papel `backlog` adicionando uma linha por item em `## Próximos` → revisor `code` → micro-commit) antes de declarar done."
  - **Atualizar `## O que NÃO fazer`:** substituir a guarda atual "Não pular o backlog harvest (passo 4.5) — sempre perguntar antes de declarar done. Resposta 'nada' é fechamento válido; silenciar é perder itens." por duas guardas:
    - "Não perguntar no backlog harvest (passo 4.5) quando nenhum item emergiu explicitamente durante a execução — pergunta cerimonial sem decisão real é ruído. Lista vazia fecha o gate em silêncio."
    - "Não fabricar itens no harvest a partir de leitura tardia do diff — o critério é sinal explícito (operador ou revisor) durante a execução, não inferência retroativa do que 'poderia' ter sido capturado."
  - Manter intacta a guarda existente "Não capturar itens no harvest que já foram absorvidos pelo plano corrente (escopo creep contido) — backlog é para deferimento deliberado, não para registrar tudo que apareceu."

### Bloco 4 — `/triage` 5: revisão condicional {reviewer: code}

- `skills/triage/SKILL.md` passo 5 ("Revisão do backlog"), bloco "Quando dispara":
  - **Substituir os itens 3 e 4 atuais e o parágrafo final ("Sem flags **e** com apenas uma linha adicionada...")** por dois itens novos:
    3. **Sem flags** → skip silente. As linhas adicionadas no passo 4 já foram decididas pelo operador; perguntar `Ok?` para confirmá-las novamente é cerimônia (ver `docs/philosophy.md` → "Convenção de pergunta ao operador"). Gate fecha sem ruído.
    4. **Com flags** → mostrar ao operador a síntese dos flags e o estado atual de `## Próximos` (e `## Em andamento`/`## Concluídos` apenas se um flag tocar essas seções), com as linhas recém-adicionadas marcadas. Perguntar uma vez via enum (`AskUserQuestion`, header `Backlog`, opções `Está bom, prosseguir` e `Aplicar edits` — Other → operador descreve em prosa quais edits, ex.: consolidar duplicatas X+Y, remover linha obsoleta Z, reordenar). Edits descritos pelo operador são aplicados ao arquivo do backlog e ficam parte do mesmo commit unificado proposto no passo 6.
  - Manter intactos: parágrafo de disparo (passo 5 só aciona se passo 4 modificou backlog), itens 1 (releitura) e 2 (flagar).
  - **Atualizar `## O que NÃO fazer`:** substituir a guarda atual "Não pular a revisão do backlog (passo 5) quando o passo 4 modificou o arquivo do papel `backlog`." por duas guardas:
    - "Não pular a revisão do backlog (passo 5) quando o passo 4 modificou o arquivo do papel `backlog` — releitura e flag de duplicatas/obsolescência sempre rodam. O que pula com flags vazios é a **pergunta**, não a checagem."
    - "Não perguntar no passo 5 quando nenhum flag de duplicata/obsolescência disparou — linhas já confirmadas no passo 4 não precisam de re-confirm."
  - Manter intacta a guarda existente "Não consolidar, remover ou reordenar linhas do backlog sem confirmação explícita do operador na pergunta do passo 5."

## Verificação manual

Repo não tem suite de testes (`test_command: null` em `CLAUDE.md`). Validação é instalação local + smoke test no Claude Code:

1. **Instalar o plugin localmente** num projeto consumidor que já usa o toolkit: `/plugin install /path/to/pragmatic-dev-toolkit --scope project`. Confirmar que `/triage`, `/run-plan`, `/release` aparecem em `/help`.
2. **`/release` (gate único):** num projeto consumidor com `version_files` declarado e CHANGELOG, rodar `/release patch`. Após o passo 3 (CHANGELOG), confirmar que **uma única pergunta** dispara no passo 4 (header `Release`, opções `Aplicar` / `Editar mensagens`), mostrando `git status`/mensagem/tag num bloco único. Após `Aplicar`, observar commit + tag executados em sequência mecânica (sem segunda pergunta). Total esperado: 3 perguntas no fluxo (bump, CHANGELOG, gate unificado), não 5.
3. **`/run-plan` 4.5 sem itens:** rodar plano simples sem deferir nada durante execução. Ao chegar no gate final, confirmar que **nenhuma `AskUserQuestion`** de harvest dispara — gate fecha silente após a transição final do backlog (4.4) e o sanity de docs (4.3).
4. **`/run-plan` 4.5 com itens:** durante execução de um bloco, dizer explicitamente "isso fica pra depois, registra no backlog" ou ter o `code-reviewer` flagar finding fora-de-escopo. No gate final, confirmar que pergunta livre dispara mostrando os itens capturados, com opção de confirmar/ajustar/descartar. Aprovar e observar bloco extra (commit micro adicionando linhas em `## Próximos`).
5. **`/triage` 5 sem flags:** triagem que adiciona 1 linha em `BACKLOG.md` sem duplicata/obsolescência (intent novo claramente distinto dos itens existentes). Confirmar que passo 5 **não dispara pergunta** — apenas releitura silenciosa, gate fecha. Próximo passo é o commit unificado (passo 6).
6. **`/triage` 5 com flags:** triagem que adiciona linha duplicada (intent já presente em `## Próximos` do `BACKLOG.md`). Confirmar que pergunta dispara mostrando síntese do flag (linha original + linha proposta) com opções `Está bom, prosseguir` / `Aplicar edits`.
7. **Inspeção textual:** `grep -n "AskUserQuestion" skills/release/SKILL.md` deve mostrar **uma** ocorrência menos que antes (passos 4 e 5 originais tinham um confirm cada; agora um único). `grep -n "AskUserQuestion" skills/run-plan/SKILL.md` mantém ocorrências (a pergunta condicional ainda existe). `grep -n "AskUserQuestion" skills/triage/SKILL.md` mantém ocorrências.

## Notas operacionais

- **Ordem dos blocos é load-bearing.** Bloco 1 (philosophy) primeiro porque blocos 2-4 referenciam a guarda nova. Blocos 2-4 entre si podem rodar em qualquer ordem (independentes), mas a sequência proposta segue do mais visível (`/release`, dogfooded recém) ao mais sutil (`/triage` 5, caso minimal).
- **Validação manual depende de projeto consumidor.** Worktree do `/run-plan` para este toolkit não consegue rodar `/release`/`/run-plan`/`/triage` sobre si mesma — skills só rodam em sessão Claude Code real com plugin instalado. Smoke test acontece na próxima invocação real em projeto consumidor (passo 1 da Verificação manual).
- **Worktree precisa de `.worktreeinclude`.** Verificar antes de rodar `/run-plan` que o arquivo lista pelo menos `skills/`, `docs/`, `CLAUDE.md` (ou globs equivalentes). Sem isso, a worktree não verá os arquivos a alterar.
- **`/run-plan` neste repo não tem `test_command`** (declarado `null` em `CLAUDE.md`). Baseline cai para inspeção textual — para markdown puro, baseline é trivialmente verde. Cada bloco ainda passa por revisor `code` antes do micro-commit.
- **Após merge:** rodar `/release minor` para v1.15.0. CHANGELOG ganha entrada com bullet único cobrindo as 4 mudanças sob `### Changed` (refactor de comportamento de skills) + `### Notes` apontando para o plano. Esta é a primeira release que dogfooda o gate único do `/release` em si — se a skill foi alterada corretamente, o próximo `/release` vai mostrar 1 pergunta no passo 4, não 2.
