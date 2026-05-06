# Plano — Batch 3 / C1: gate de prontidão consolidado em /run-plan

## Contexto

Implementação do ADR-002 ("Gate de prontidão consolidado em /run-plan"). 4 enums de cutucada na fase pré-loop (pré-cond 2c, passo 1.2 worktreeinclude, passo 1.2 credencial, passo 2 escopo) viram **um único gate** com lista em prosa + enum binário (`Prosseguir mesmo assim` / `Pausar para corrigir manualmente`), executado **antes** da worktree ser criada. Bloqueios reais (plano sujo, baseline vermelho, worktree órfã) ficam fora do gate — continuam parando in situ.

**Linha do backlog:** plugin: batch 3/C1 — gate de prontidão consolidado em /run-plan (implementa ADR-002), antecipa detecção de warnings pré-loop e substitui 4 enums em cascata por um único gate informativo

**Escopo escolhido (a):** lista em prosa + enum binário, sem fix in-place. ADR-002 documenta o trade-off contra (b) multi-select com mapping ação-por-item.

## Resumo da mudança

Refactor da fase pré-loop em `skills/run-plan/SKILL.md`:

- **Nova seção "Gate de prontidão"** entre as pré-condições e o passo 1, executada **antes** de `git worktree add`. Detecta os 4 warnings hoje fragmentados (alinhamento dirty, `.worktreeinclude` ausente, credencial gitignored, sanity de escopo). Lista em prosa + enum binário único. Sem fix in-place.
- **Pré-condição 2c** (alinhamento dirty cutuca) — **removida** da seção "Pré-condições"; lógica migra para o gate. Apenas o sub-bullet de bloqueio remanescente em 2 fica (push esquecido — bloqueio, não cutucada).
- **Passo 1.2** — sub-bullet `.worktreeinclude` (propor criação) e sub-bullet credencial (gatilho cruzado de validação manual) **removidos**; lógica migra para o gate. Passo 1.2 fica apenas com a parte mecânica de copiar gitignored declarados em `.worktreeinclude` quando ele existe.
- **Passo 2** ("Sanity check de escopo") — **removido** como passo separado; lógica migra para o gate. Renumera passos subsequentes (passo 3 vira passo 2, etc.).
- **`## O que NÃO fazer`** — substituir o item "Não silenciar o gatilho cruzado de credencial (passo 1.2)..." por equivalente que aponta ao novo gate (gatilho cruzado preservado conceitualmente; localização migra).

Sem mudança em outras skills, agents, hooks. Sem CLI/flag/env nova.

## Arquivos a alterar

### Bloco 1 — refactor pré-loop em `/run-plan` SKILL.md {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **Seção "Pré-condições"**: remover sub-bullet 2c (alinhamento dirty cutuca). Manter 2 e 2 (plano modificado, push esquecido — bloqueios) e os outros itens (gate verde, worktree não existe — bloqueios).
  - **Inserir nova seção "Gate de prontidão"** entre "Pré-condições" e "Passo 1": detectar e listar warnings de alinhamento dirty, `.worktreeinclude`, credencial, escopo; enum binário `Prosseguir mesmo assim` / `Pausar para corrigir manualmente`; sem warnings → skip silente. Citar ADR-002.
  - **Passo 1.2**: remover sub-bullet de `.worktreeinclude` ausente (propor criação) e sub-bullet credencial cruzada. Passo 1.2 fica: copiar paths declarados no `.worktreeinclude` quando existe; ausente → skip (warning já levantado no gate).
  - **Passo 2** (Sanity check de escopo): remover. Renumerar "Passo 3 — Loop por bloco" para "Passo 2", "Passo 4 — Gate final" para "Passo 3", e atualizar referências internas (passo 4.5 → passo 3.5, etc.).
  - **`## O que NÃO fazer`**: substituir item "Não silenciar o gatilho cruzado de credencial (passo 1.2)..." por: "Não silenciar warnings detectados no gate de prontidão por estado prévio — quando o plano corrente exige `## Verificação manual` e há credencial gitignored não coberta, o aviso é obrigatório, mesmo que o `.worktreeinclude` tenha sido configurado em runs anteriores como 'não preciso'." Mantém o anti-padrão sutil; só atualiza o ponto de execução.
  - **Captura automática (passo 4.5 / novo 3.5)**: gatilho "Superfície faltante" agora é alimentado por escolha de `Prosseguir` no gate quando havia warning de escopo — atualizar texto.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **Gate consolidado presente**:
   - `grep -n "## Gate de prontidão\|Gate de prontidão" skills/run-plan/SKILL.md` retorna a seção nova.
   - Seção cita ADR-002.
   - 4 warnings listados (alinhamento dirty, `.worktreeinclude`, credencial, escopo).
   - Enum binário com header `Prontidão` e opções `Prosseguir mesmo assim` / `Pausar para corrigir manualmente`.

2. **Cutucadas removidas dos 4 lugares antigos**:
   - Pré-condição 2c (alinhamento dirty cutuca) ausente — `grep -n "Cutucar.*alinhamento\|alterações uncommitted" skills/run-plan/SKILL.md` retorna apenas o gate consolidado.
   - Passo 1.2 sub-bullet `.worktreeinclude` propor criação ausente — `grep -n "propor criação" skills/run-plan/SKILL.md` retorna 0 ou apenas referência ao gate.
   - Passo 1.2 sub-bullet credencial cruzada ausente — `grep -n "Gatilho cruzado de validação manual" skills/run-plan/SKILL.md` retorna 0 ou apenas referência ao gate / `## O que NÃO fazer`.
   - Passo 2 (Sanity check de escopo como passo separado) ausente — `grep -n "^### 2. Sanity check de escopo" skills/run-plan/SKILL.md` retorna 0.

3. **Renumeração consistente**:
   - `grep -n "^### " skills/run-plan/SKILL.md` mostra "Passo 1 — Setup da worktree", "Passo 2 — Loop por bloco", "Passo 3 — Gate final" (ou "Passo 0 — Gate de prontidão" se contado como passo).
   - Referências internas (`passo 4.5`, `passo 4.7`, `passo 3` em `## O que NÃO fazer`) atualizadas para nova numeração ou substituídas por nomes de seção.

4. **`## O que NÃO fazer` preserva critério editorial**:
   - Item "Não silenciar..." atualizado, mantém o anti-padrão (gatilho condicional facilmente esquecido) — passa pelo critério não-óbvio de CLAUDE.md "Editing conventions".
   - Outros itens intactos.

5. **Cross-cutting**:
   - Skills/agents que referenciam `passo 4.5` ou `passo 2` do `/run-plan` continuam apontando para o conteúdo certo após renumeração — `grep -rn "/run-plan.*passo\|run-plan.*4\.5\|run-plan.*sanity check" --include="*.md" .` para conferir; atualizar se necessário.
   - Planos antigos em `docs/plans/*.md` não tocados — referenciam comportamento antigo do `/run-plan`, válido como histórico.

## Verificação manual

**Smoke test do gate em uso real**: invocar `/run-plan` em um plano fictício pós-merge+reload do plugin que dispare ao menos 1 warning detectável (ex.: plano com `## Verificação manual` num repo onde `.env` existe gitignored mas o `.worktreeinclude` não cobre). Confirmar:

- Gate aparece **antes** de `git worktree add`.
- Lista em prosa cita o(s) warning(s) detectado(s) com ação sugerida.
- Enum binário com as duas opções.
- `Prosseguir` → skill segue, worktree criada, warning fica registrado mentalmente para captura no gate final.
- `Pausar` → skill encerra reportando os warnings, sem criar worktree.

**Critério de aceitação**: pelo menos um cenário com warning ativo + um cenário sem warnings (skip silente do gate) validados.

## Notas operacionais

- Após merge do PR, validar em uso real antes de prosseguir para B2 (frontmatter declarativo `roles:` — último item do roteiro).
- Captura automática de imprevistos no gate final (passo 3.5 nova numeração) precisa continuar lendo a flag "Superfície faltante" — atualizar texto se necessário no Bloco 1.
