# Plano — D2: state-tracking em git/forge (caminho parcial, ADR-004)

## Contexto

Implementação do ADR-004 ("State-tracking em git/forge, não em markdown"). Caminho **(b) parcial**: remove `## Em andamento` do `BACKLOG.md`; preserva `## Próximos` (curadoria) e `## Concluídos` (registro editorial append-only). Os 5 mecanismos defensivos contra merge artifact ficam obsoletos — skill `/heal-backlog` removida, Action `validate-backlog` removida, refactors em `/triage`, `/run-plan` e `/next` para parar de mutar Em andamento. State vivo de "o que está em andamento" descobrível via `git branch` / PRs abertos / worktree corrente.

**Linha do backlog:** plugin: BACKLOG.md como state-tracker é fonte recorrente de merge artifact — 5 mecanismos defensivos (`/triage` push pós-commit, `/run-plan` precondição 2, `/run-plan` 3.7 auto-rebase, Action `validate-backlog`, `/heal-backlog`) protegem o mesmo problema estrutural: o arquivo mistura curadoria (Próximos) com state-tracking (Em andamento, Concluídos), e dois PRs concorrentes mutam ambos. Reavaliar mover state para git/forge (PR aberto = em andamento, mergeado = concluído) — 4 dos 5 mecanismos viram desnecessários. Mudança grande, exige ADR antes de implementar. Flagado na revisão arquitetural pós-v1.20.0.

**Escopo escolhido (b):** parcial. ADR-004 documenta o trade-off contra (a) total.

**Action `validate-backlog` forge-agnostic** (terceira pendência do `## Próximos`) é absorvida aqui por **remoção** — sob D2, não há merge artifact a detectar; Action vira código morto, não candidato a generalizar. **E1** (handoff /debug → /triage) fica fora — explicitamente YAGNI na própria linha do backlog.

**Restrição de execução**: o header `## Em andamento` **não pode ser deletado durante o `/run-plan`** porque a linha do backlog vive lá no passo 2 (loop) e só sai no 3.4 (gate final). Deletar durante os blocos deixaria linha órfã. A remoção do header fica como **tarefa pós-merge** em commit direto em main — ver `## Notas operacionais`.

## Resumo da mudança

Refactor de fronteira que afeta múltiplas superfícies coordenadamente:

- **`/triage` SKILL**: passo 1 verificar item equivalente em Próximos+Concluídos apenas; passo 4 caminho-com-plano deixa de gravar linha em `## Em andamento` (apenas captura `**Linha do backlog:**` no Contexto do plano); passo 4 sub-fluxo "Criar em BACKLOG.md" gera cabeçalho mínimo com 2 seções; passo 6 mantém commit+push atômico (justificativa atualizada — visibilidade/recovery, não merge artifact).

- **`/run-plan` SKILL**: pré-condição 2 segunda metade removida (commits ahead + linha em Em andamento); transição inicial Próximos→Em andamento no passo 2 removida; passo 3.4 muda de "mover de Em andamento para Concluídos" para "**adicionar** em Concluídos"; passo 3.7 remove auto-rebase + resolução programática de conflito em Em andamento; `## O que NÃO fazer` enxuga itens que dependiam de Em andamento.

- **`/next` SKILL**: passo 1 lê apenas `## Próximos`; passo 5 remove o item "Em andamento: listar como informação".

- **`/heal-backlog` SKILL**: **removida** (diretório `skills/heal-backlog/` deletado).

- **`.github/workflows/validate-backlog.yml` + `.github/scripts/validate_backlog.py`**: **ambos removidos**.

- **`CLAUDE.md`**: description do role `backlog` na tabela menciona só `## Próximos`, `## Concluídos`; cita ADR-004.

- **`README.md`**: linha do `/heal-backlog` na tabela de componentes removida.

- **`docs/install.md`**: smoke test #11 (sobre /heal-backlog) removido; lista de skills no #2 atualizada.

- **`BACKLOG.md` schema**: header `## Em andamento` removido em **commit pós-merge** (não cabe num bloco do /run-plan; ver Notas operacionais).

Sem mudança em `docs/philosophy.md` (probe inicial não encontrou refs a Em andamento ou state-tracking; cross-check final no gate). Sem CLI/flag/env nova.

## Arquivos a alterar

### Bloco 1 — `/triage` SKILL: parar de gravar em Em andamento {reviewer: code}

- `skills/triage/SKILL.md`:
  - **Passo 1** ("Carregar contexto mínimo") item 3: trocar "verificar item equivalente em **Próximos**, **Em andamento** ou **Concluídos**" por "verificar item equivalente em **Próximos** ou **Concluídos**".
  - **Passo 4** ("Produzir os artefatos", parágrafo BACKLOG): substituir "Caminho com plano → grava em `## Em andamento`" por "Caminho com plano → não grava no BACKLOG (state vivo é a worktree/PR aberto, ADR-004); a linha em `**Linha do backlog:**` no `## Contexto` do plano alimenta `/run-plan` 3.4 para adicionar em `## Concluídos` no done."
  - **Passo 4** sub-fluxo "Papel `não temos`": cabeçalho mínimo do `Criar em BACKLOG.md` → atualizar para `# Backlog\n\n## Próximos\n\n## Concluídos\n`.
  - **Passo 6** ("Reportar, propor commit e devolver controle"): manter commit+push atômico no caminho-com-plano. Atualizar a justificativa: "Sem o push, `/run-plan` criaria worktree de estado que o remote desconhece — merge do PR produz artefato no `BACKLOG.md`" → "Push imediato dá visibilidade do plano e permite recovery em outra máquina; sem ele, plano fica só local."

### Bloco 2 — `/run-plan` SKILL: remover transições de Em andamento {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **Pré-condição 2** segunda metade: remover bullet "**Bloquear** se `git log origin/<branch-atual>..HEAD` retornar commits E o arquivo do papel `backlog` tem linha em `## Em andamento`...". Restam os 2 bullets de bloqueio iniciais.
  - **Passo 2** ("Loop por bloco") parágrafo de abertura: substituir "**Antes do primeiro bloco:** capturar `**Linha do backlog:** <texto>`... Linha em `## Próximos` do `backlog` → mover para `## Em andamento`..." por "**Antes do primeiro bloco:** capturar `**Linha do backlog:** <texto>` do `## Contexto` se presente — usado pelo passo 3.4 para adicionar em `## Concluídos` no done. Plano sem campo, papel `backlog` 'não temos' → skip silente."
  - **Passo 3.4** ("Transição final do backlog"): reescrever de "mover para `## Concluídos`" para "**adicionar** ao topo de `## Concluídos`" (sem origem; Em andamento não existe). Bloco extra (atualizar `backlog` → revisor `code` → micro-commit) preservado.
  - **Passo 3.7** ("Sugestão de publicação"): remover toda a parte de detecção de divergência em BACKLOG.md + auto-rebase + resolução programática + `--force-with-lease`. Enum `Publicar` permanece com 3 opções sem prefixo de detecção.
  - **`## O que NÃO fazer`**: remover item "Não tentar resolver merge/rebase no fim — exceção única em 3.7 quando..." (a exceção desapareceu junto com a detecção).

### Bloco 3 — `/next` SKILL: ler apenas Próximos {reviewer: code}

- `skills/next/SKILL.md`:
  - **Passo 1** ("Ler o backlog"): remover bullet "`## Em andamento` — itens já comprometidos. Reportar ao final apenas como informação...".
  - **Passo 5** ("Apresentar resultado e colher escolha"): remover bullet "**Em andamento:** listar como informação".

### Bloco 4 — remover `/heal-backlog` skill {reviewer: code}

- `skills/heal-backlog/`: **deletar diretório inteiro** (`git rm -r skills/heal-backlog/`). Skill obsoleta sob D2.

### Bloco 5 — remover Action `validate-backlog` {reviewer: code}

- `.github/workflows/validate-backlog.yml`: **deletar arquivo**.
- `.github/scripts/validate_backlog.py`: **deletar arquivo**.

### Bloco 6 — atualizar CLAUDE.md, README, docs/install.md {reviewer: code,doc}

- `CLAUDE.md`: tabela "The role contract", linha do `backlog` description: substituir "Short exploratory list — `## Próximos`, `## Em andamento`, `## Concluídos`." por "Short exploratory list — `## Próximos` (curatorial) and `## Concluídos` (editorial registry, append-only). State of in-flight work lives in git/forge per ADR-004."
- `README.md`: tabela de componentes, linha do `/heal-backlog` → **remover**.
- `docs/install.md`:
  - Validação item 2: remover `/heal-backlog` da lista de skills mencionadas.
  - Validação item 11 (todo o item sobre /heal-backlog): **remover**.
- `docs/philosophy.md`: cross-check final via grep — confirmar que não há refs a "Em andamento" remanescentes; atualizar se houver.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **`/triage` parou de gravar em Em andamento**:
   - `grep -n "## Em andamento" skills/triage/SKILL.md` retorna 0.
   - `grep -n "Caminho com plano → grava em" skills/triage/SKILL.md` retorna 0.
   - Cabeçalho mínimo do `Criar em BACKLOG.md` (passo 4 sub-fluxo "não temos") atualizado para 2 seções.
   - Passo 1 item 3 cita só Próximos+Concluídos.

2. **`/run-plan` removeu transições de Em andamento**:
   - `grep -n "## Em andamento" skills/run-plan/SKILL.md` retorna 0.
   - `grep -n "auto-rebase\|--force-with-lease.*BACKLOG\|resolver programaticamente" skills/run-plan/SKILL.md` retorna 0.
   - Passo 3.4 cita "adicionar" em vez de "mover".
   - Passo 3.7 enum `Publicar` permanece com 3 opções (Push / Push + sugerir PR/MR / Nenhum).

3. **`/next` lê apenas Próximos**:
   - `grep -n "Em andamento" skills/next/SKILL.md` retorna 0.

4. **`/heal-backlog` removida**:
   - `ls skills/heal-backlog/ 2>&1` retorna "No such file or directory".

5. **Action removida**:
   - `ls .github/workflows/validate-backlog.yml .github/scripts/validate_backlog.py 2>&1` retorna ambos "No such file or directory".

6. **Docs atualizados**:
   - `CLAUDE.md` description do role backlog cita só Próximos+Concluídos; menciona ADR-004.
   - `README.md` tabela não tem mais `/heal-backlog`.
   - `docs/install.md` smoke #11 ausente; lista de skills no #2 sem /heal-backlog.

7. **Cross-cutting final**:
   - `grep -rn "Em andamento" --include="*.md" .` (excluindo docs/plans/, CHANGELOG, docs/decisions/, .worktrees/, BACKLOG.md histórico) retorna 0 ocorrências em arquivos vivos (skills/, agents/, README, CLAUDE.md, docs/install.md, docs/philosophy.md).
   - `grep -rn "/heal-backlog" --include="*.md" .` (mesma exclusão + BACKLOG.md ## Concluídos) retorna 0.

## Verificação manual

**Smoke test em uso real** (pós-merge+reload do plugin):

- **Cenário 1 — `/triage` caminho-com-plano**: invocar `/triage` num pedido que justifique plano. Confirmar: skill cria plano, **não** grava linha em BACKLOG.md (apenas commit+push do plano + linha do backlog no Contexto).
- **Cenário 2 — `/run-plan` done com transição**: rodar `/run-plan` num plano que tenha `**Linha do backlog:**` no Contexto. Confirmar: skill **adiciona** linha ao topo de `## Concluídos` no done (sem origem em Em andamento), bloco extra `code-reviewer` + micro-commit antes do passo 3.5.
- **Cenário 3 — `/next` reporta sem Em andamento**: invocar `/next` no repo. Confirmar: relatório não tem seção "Em andamento" — apenas top 3 candidatos de `## Próximos`.

**Critério de aceitação**: os 3 cenários se comportam conforme ADR-004; nenhuma tentativa de mutar `## Em andamento` em qualquer skill; merge artifact estruturalmente impossível.

## Pendências de validação

- ~~Smoke comportamental dos 3 cenários (`/triage` caminho-com-plano sem gravar em Em andamento; `/run-plan` done que adiciona em Concluídos sem origem; `/next` sem reportar Em andamento) exige merge + reload do plugin (cache instalado pré-D2). Inspeção direta pós-merge cobre o core do contrato (refactors em SKILLs presentes, Em andamento ausente, /heal-backlog removida, Action removida); smoke comportamental real fica para invocação subsequente.~~ **Encerrada 2026-05-10:** uso real subsequente do plugin sem regressão observada nos 3 cenários; contrato D2/ADR-004 estável.

## Notas operacionais

- **Cleanup pós-merge obrigatório**: dois ajustes em BACKLOG.md ficam fora dos blocos do plano e devem ser feitos em commit direto em main após o merge:
  1. **Remover header `## Em andamento`**: durante a execução do `/run-plan`, a linha do backlog corrente vive nessa seção (movida no passo 2 abertura, sai no 3.4 para Concluídos). Deletar a seção durante os blocos deixaria linha órfã. Pós-merge, a seção está vazia — remover header + linha em branco que segue.
  2. **Remover linha "Action `validate-backlog` forge-agnostic"** de `## Próximos` — esse item fica obsoleto sob D2 (Action removida no Bloco 5; não há mais o que generalizar). Hoje a linha continua em Próximos como pendência registrada; pós-merge pode ser removida.

  Commit único em main:
  ```
  $EDITOR BACKLOG.md  # remover header "## Em andamento" + linha "Action validate-backlog..."
  git add BACKLOG.md
  git commit -m "chore(backlog): clean up Em andamento header + obsolete Action item per ADR-004"
  git push
  ```
  Ato pequeno, único, isolado — análogo aos commits pós-merge de "marcar pendência como resolvida" feitos no E3/C1/B2.
- D2 fecha o último item estrutural do roteiro arquitetural pós-v1.20.0. Após merge + cleanup, plugin opera sem state em markdown.
- Próxima `/release` consolida v1.21.0 com os 5 PRs já mergeados + este — bump minor (D2 introduz mudanças de comportamento perceptíveis).
