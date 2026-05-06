# Plano — Batch 3 / C1: eliminar gates de cutucada na fase pré-loop do /run-plan

## Contexto

Implementação do ADR-002 ("Eliminar gates de cutucada na fase pré-loop do /run-plan"). Os 4 enums de cutucada da pré-loop (pré-cond 2c, passo 1.2 worktreeinclude, passo 1.2 credencial, passo 2 escopo) são **eliminados**. Cada warning detectado é classificado e materializado nos trilhos do passo 4.5 (`## Pendências de validação` no plano para warnings de alto custo de detecção tardia; `## Próximos` do backlog para warnings que viram items de feature/config; aviso informativo + segue para warnings de baixo custo). Skill nunca interrompe por cutucada na fase pré-loop.

**Linha do backlog:** plugin: batch 3/C1 — eliminar gates de cutucada na fase pré-loop do /run-plan (implementa ADR-002), capturar warnings via trilhos existentes do passo 4.5

**Escopo escolhido (c):** zero-gate. ADR-002 documenta os trade-offs contra (a) gate informativo binário e (b) multi-select com fix in-place.

## Resumo da mudança

Refactor da fase pré-loop em `skills/run-plan/SKILL.md`:

- **Pré-condição 2c** (alinhamento dirty cutuca) — **removida**. Detecção migra para nova seção "Detecção de warnings pré-loop"; classificação: aviso informativo + segue.
- **Passo 1.2** — sub-bullet `.worktreeinclude` (propor criação) e sub-bullet credencial (gatilho cruzado) **removidos**. Detecção migra para a nova seção; classificação: Backlog (worktreeinclude) e Validação (credencial).
- **Passo 2** ("Sanity check de escopo") — **removido como passo separado**. Detecção migra para a nova seção; classificação: Validação. Renumera passos subsequentes (passo 3 vira passo 2, etc.).
- **Nova mecânica "Detecção de warnings pré-loop"** entre as pré-condições e o passo 1: detecta os 4 warnings e classifica via mesmas categorias do passo 4.5 (renomeado para 3.5 após renumeração). Sem perguntas. Mensagens uniformes ao operador.
- **Passo 4.5 (Captura automática de imprevistos)** — texto generalizado para reconhecer warnings vindos da fase pré-loop como entrada legítima da lista de captura. Materialização no gate final continua igual: bloco extra com revisor `code` + micro-commit.
- **`## O que NÃO fazer`** — substituir item "Não silenciar o gatilho cruzado de credencial..." por "Não silenciar warnings detectados pré-loop com base em estado prévio do `.worktreeinclude` — quando o plano corrente exige `## Verificação manual` e há credencial gitignored não coberta, a captura em Validação é obrigatória, mesmo se o operador declarou anteriormente 'não preciso'." Mantém o anti-padrão sutil; só atualiza o ponto de execução.

Sem mudança em outras skills, agents, hooks. Sem CLI/flag/env nova.

## Arquivos a alterar

### Bloco 1 — refactor pré-loop em /run-plan SKILL.md {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **Seção "Pré-condições"**: remover sub-bullet 2c (alinhamento dirty cutuca). Manter os sub-bullets de bloqueio em 2 (plano modificado, push esquecido) e os outros itens (gate verde, worktree não existe — bloqueios).
  - **Inserir nova seção "Detecção de warnings pré-loop"** entre "Pré-condições" e "Passo 1": cita ADR-002. Lista os 4 warnings com classificação (Aviso / Backlog / Validação) e mensagens-padrão uniformes (espelham 4.5: "aviso: ...", "capturei no backlog: ...", "capturei para verificação: ..."). Sem warnings → silêncio total.
  - **Passo 1.2**: remover sub-bullet de `.worktreeinclude` ausente (propor criação) e sub-bullet credencial (gatilho cruzado de validação manual). Passo 1.2 fica: copiar paths declarados em `.worktreeinclude` quando existe; `.worktreeinclude` ausente → skip silente (warning já capturado na detecção pré-loop).
  - **Passo 2** (Sanity check de escopo): remover. Renumerar "Passo 3 — Loop por bloco" → "Passo 2", "Passo 4 — Gate final" → "Passo 3"; atualizar referências internas (passo 4.5 → 3.5, passo 4.7 → 3.7, etc.).
  - **Passo 3.5 (antigo 4.5) — Captura automática**: generalizar texto para reconhecer entradas vindas da fase pré-loop. Manter os 6 gatilhos hoje listados (4 durante execução + 2 durante validação manual) e adicionar parágrafo: "Warnings detectados na fase pré-loop (alinhamento dirty, `.worktreeinclude` ausente, credencial não coberta, escopo divergente) já entram nesta lista quando classificados como Backlog ou Validação na detecção; aviso informativo (alinhamento dirty) é reportado in situ e não alimenta a lista." Materialização final no bloco extra continua igual.
  - **`## O que NÃO fazer`**: substituir item "Não silenciar o gatilho cruzado de credencial (passo 1.2)..." pelo equivalente referente à detecção pré-loop (texto exato no Resumo da mudança acima). Manter os outros itens.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **Cutucadas removidas**:
   - Pré-condição 2c (cutucada de alinhamento dirty) ausente — `grep -n "Commitar agora.*Continuar mesmo assim\|enum.*Alinhamento\|alterações uncommitted.*cutucar\|Cutucar.*alterações uncommitted" skills/run-plan/SKILL.md` retorna 0 ou apenas refs em prosa do gate de detecção sem `AskUserQuestion`.
   - Passo 1.2 sub-bullet `.worktreeinclude` propor criação ausente — `grep -n "propor criação.*uma vez por projeto\|enum.*Worktree" skills/run-plan/SKILL.md` retorna 0.
   - Passo 1.2 sub-bullet credencial cruzada ausente — `grep -n "Gatilho cruzado de validação manual\|enum.*Credencial" skills/run-plan/SKILL.md` retorna 0.
   - Passo 2 (Sanity check de escopo) ausente como header — `grep -n "^### 2\. Sanity check de escopo\|enum.*Escopo" skills/run-plan/SKILL.md` retorna 0.
   - **Nenhum `AskUserQuestion` na fase pré-loop**: `grep -n "AskUserQuestion" skills/run-plan/SKILL.md` retorna apenas as ocorrências do passo 4.5 / 4.7 / passos pós-loop (legítimas).

2. **Detecção pré-loop presente**:
   - `grep -n "Detecção de warnings pré-loop\|^## Detecção de warnings\|^### Detecção" skills/run-plan/SKILL.md` retorna a nova seção.
   - Seção cita ADR-002.
   - 4 warnings listados com classificação (Aviso, Backlog, Validação) e mensagens-padrão.

3. **Renumeração consistente**:
   - `grep -n "^### " skills/run-plan/SKILL.md` mostra "1. Setup da worktree", "2. Loop por bloco", "3. Gate final".
   - Referências internas (`passo 4.5`, `passo 4.7`, `passo 3` em `## O que NÃO fazer`) atualizadas.

4. **Captura automática expandida**:
   - Passo 3.5 (antigo 4.5) menciona warnings da fase pré-loop como entradas legítimas.
   - Materialização (bloco extra revisor `code` + micro-commit) inalterada.

5. **`## O que NÃO fazer`**:
   - Item antigo "Não silenciar o gatilho cruzado de credencial (passo 1.2)..." substituído pelo equivalente referente à detecção pré-loop.
   - Outros itens intactos.
   - Critério editorial preservado (CLAUDE.md → "Editing conventions": só guardas não-óbvias).

6. **Cross-cutting**:
   - Skills/agents que referenciam "passo 4.5", "passo 2 (Sanity check de escopo)" ou "passo 1.2 credencial" do `/run-plan` continuam apontando para conteúdo certo após renumeração — `grep -rn "/run-plan.*passo\|run-plan.*4\.5\|run-plan.*sanity check\|run-plan.*1\.2" --include="*.md" .` para conferir; atualizar onde aplicável.
   - Planos antigos em `docs/plans/*.md` não tocados — referenciam comportamento antigo, válido como histórico per convenção do CHANGELOG v1.14.0.

## Verificação manual

**Smoke test do zero-gate em uso real** (pós-merge+reload do plugin): invocar `/run-plan` em um plano fictício que dispare ao menos 1 warning detectável (ex.: plano com `## Verificação manual` num repo onde `.env` existe gitignored mas o `.worktreeinclude` não cobre). Confirmar:

- **Nenhuma pergunta** disparada na fase pré-loop.
- Mensagens de captura aparecem **antes** da criação da worktree (ou no momento adequado de cada detecção): `"capturei para verificação: <linha>"` para credencial não coberta; `"capturei no backlog: <linha>"` para `.worktreeinclude` ausente; `"aviso: <descrição>"` para alinhamento dirty.
- Skill prossegue para criar a worktree sem aguardar resposta.
- No gate final, `## Pendências de validação` no plano e `## Próximos` no backlog refletem as capturas; bloco extra final agrega revisor `code` + micro-commit.

**Cenário sem warnings**: invocar `/run-plan` em plano simples sem nenhum dos gatilhos. Confirmar silêncio total na fase pré-loop — sem mensagens de detecção, sem perguntas. Skill cria worktree direto.

**Critério de aceitação**: ambos cenários (com warnings, sem warnings) validados.

## Notas operacionais

- Após merge do PR, validar em uso real antes de prosseguir para B2 (frontmatter declarativo `roles:` — último item do roteiro).
- Mudança elimina friction-point conhecido (4 cascadas de cutucada). Pain reportado depois pode justificar reabrir o ADR (gatilhos de revisão registrados em ADR-002).

## Pendências de validação

- Smoke test do zero-gate em uso real: invocar `/run-plan` pós-merge+reload em (i) plano fictício que dispare ao menos 1 warning detectável; (ii) plano simples sem nenhum gatilho. Confirmar: zero `AskUserQuestion` na fase pré-loop nos dois casos; mensagens de captura aparecem antes da worktree quando há warnings; skill segue silente quando não há; `## Pendências de validação` e `## Próximos` do backlog refletem as capturas no done. Não realizado durante o /run-plan corrente: o cache instalado do plugin é v1.20.0 e ainda não tem o refactor — smoke real depende de merge + reload.
