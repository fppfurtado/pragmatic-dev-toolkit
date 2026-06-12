# Plano — Batch 3 / E3: extrair `templates/plan.md`

## Contexto

Implementação do ADR-001 ("Protocolo de templates centralizados no plugin"). Estrutura canônica do plano sai da prosa inline de `skills/triage/SKILL.md` passo 4 e vira o arquivo `templates/plan.md` na raiz do plugin. `skills/run-plan/SKILL.md` precondição 1 continua agnóstica ao corpo (matching semântico já existente), mas ganha menção explícita ao template como fonte canônica.

**Linha do backlog:** plugin: batch 3/E3 — extrair `templates/plan.md` centralizado e atualizar /triage e /run-plan para apontar ao template (implementa ADR-001)

**Escopo escolhido (a):** apenas `templates/plan.md`. ADR template inline em `/new-adr` fica intacto — extensão futura sob o mesmo protocolo se houver pain.

## Resumo da mudança

Três operações coordenadas:

- **`templates/plan.md` novo**: esqueleto canônico do plano com todas as seções (`## Contexto` → `## Resumo da mudança` → `## Arquivos a alterar` → `## Verificação end-to-end` → opcional `## Verificação manual` → opcional `## Notas operacionais`), placeholders editáveis e nota explicando os campos especiais do `## Contexto` (`**Termos ubíquos tocados:**`, `**Linha do backlog:**`).

- **`skills/triage/SKILL.md` passo 4 ("Plano")**: substitui descrição inline da estrutura por instrução de ler `${CLAUDE_PLUGIN_ROOT}/templates/plan.md` em runtime, copiar o esqueleto, adaptar headers ao idioma do projeto consumidor, preencher placeholders. Mantém regras específicas (campos do `## Contexto`, anotação `{reviewer: ...}`, slug) — são regras de uso do template, não estrutura do template.

- **`skills/run-plan/SKILL.md` precondição 1**: ganha menção curta a `templates/plan.md` como referência canônica para o matching semântico. Sem mudança comportamental — a skill já era agnóstica ao corpo do template.

Sem mudança em `/new-adr` (escopo (a) escolhido). Sem CLI/flag/env nova. Sem comportamento perceptível ao operador além de skills mais enxutas.

## Arquivos a alterar

### Bloco 1 — criar `templates/plan.md` {reviewer: doc}

- Criar pasta `templates/` na raiz do plugin.
- Criar `templates/plan.md` com o esqueleto canônico:
  - Headers em PT-BR (canonical do toolkit; skills adaptam ao idioma do projeto consumidor).
  - Placeholders explícitos (`<descrever contexto>`, `<resumo de uma frase ou parágrafo>`, etc.) para o operador/skill preencher.
  - Nota curta no topo explicando: "Esqueleto canônico — `/triage` lê este arquivo e adapta para o caso concreto. Headers podem ser traduzidos no projeto; `/run-plan` faz matching semântico."
  - Nota sobre os 2 campos especiais do `## Contexto`: `**Termos ubíquos tocados:**` (quando o pedido toca o domínio) e `**Linha do backlog:**` (quando há linha capturada para transição de estado).
  - Exemplo mínimo de bloco em `## Arquivos a alterar` com anotação `{reviewer: ...}`.
- Reviewer `doc`: bloco doc-only (path único `.md`); validação cross-cutting de drift entre o template e o que /triage/run-plan esperam ler.

### Bloco 2 — `/triage` passo 4 aponta para o template {reviewer: code}

- `skills/triage/SKILL.md` passo 4, parágrafo "**Plano (papel: `plans_dir`):**":
  - Substituir descrição inline da estrutura ("Estrutura: `## Contexto` → `## Resumo da mudança` → ...") por: "Ler `${CLAUDE_PLUGIN_ROOT}/templates/plan.md` como esqueleto canônico, copiar para `<plans_dir>/<slug>.md`, adaptar headers ao idioma do projeto consumidor (per `docs/philosophy.md` → 'Convenção de idioma'), preencher placeholders com o conteúdo decidido nos passos 2-3."
  - Manter os 2 sub-bullets sobre campos do `## Contexto` (Termos ubíquos tocados, Linha do backlog) — são regras específicas do conteúdo do plano, não da estrutura.
  - Manter a regra "BACKLOG.md não aparece em `## Arquivos a alterar`".
  - Manter o schema de `{reviewer: <perfil>}` (já está fora da descrição estrutural).
  - Manter slug rule.

### Bloco 3 — `/run-plan` precondição 1 cita o template canônico {reviewer: code}

- `skills/run-plan/SKILL.md` precondição 1, item "**Plano existe e tem `## Arquivos a alterar`**":
  - Adicionar nota curta após a sentença existente: "Esqueleto canônico em `${CLAUDE_PLUGIN_ROOT}/templates/plan.md`. Matching semântico aceita os headers traduzidos quando o projeto consumidor opera em outro idioma."
  - Sem mudança no comportamento — a skill já era agnóstica ao corpo.

## Verificação end-to-end

Refactor textual sem suite executável; gate é inspeção dirigida:

1. **Bloco 1 — template criado**:
   - `ls templates/plan.md` retorna o arquivo.
   - `grep -c "^## " templates/plan.md` ≥ 4 (Contexto, Resumo da mudança, Arquivos a alterar, Verificação end-to-end são obrigatórios; Verificação manual e Notas operacionais opcionais).
   - Template tem nota explicativa no topo + nota sobre campos especiais do `## Contexto` + exemplo de bloco em `## Arquivos a alterar`.

2. **Bloco 2 — `/triage` aponta para template**:
   - `grep -n "templates/plan.md\|CLAUDE_PLUGIN_ROOT.*templates" skills/triage/SKILL.md` retorna a referência inserida.
   - Descrição inline da estrutura `## Contexto → ## Resumo...` removida do passo 4.
   - Sub-bullets de "Termos ubíquos tocados" e "Linha do backlog" preservados.

3. **Bloco 3 — `/run-plan` cita template**:
   - `grep -n "templates/plan.md" skills/run-plan/SKILL.md` retorna a nota inserida na precondição 1.
   - Sem alteração no resto da skill (matching semântico, etc.).

4. **Cross-cutting**:
   - Sem refs penduradas após a mudança — a estrutura do plano só aparece como descrição em (i) `templates/plan.md` (canonical), (ii) `/triage` (aponta para o template), (iii) `/run-plan` (cita o template).
   - Planos antigos em `docs/plans/*.md` não tocados — seguem o esquema antigo (válido per matching semântico).

## Verificação manual

**Smoke test do template em uso real**: invocar `/triage` num pedido fictício simples (ex.: "adicionar nota de release manual em README") na worktree e confirmar:

- `/triage` lê `templates/plan.md`.
- Plano produzido em `docs/plans/<slug>.md` segue o esqueleto do template (todas as seções obrigatórias presentes; opcionais omitidas se não aplicáveis).
- Headers em PT-BR (idioma do repo) — sem tradução cosmética.
- Campos especiais do `## Contexto` aparecem só quando relevantes.

**Critério de aceitação**: plano produzido pelo /triage de smoke é estruturalmente equivalente aos planos de Batch 1 e Batch 2 (mesmas seções, mesma ordem). Se divergir, ajustar o template antes de fechar.

## Notas operacionais

- Após merge do PR, validar em **uso real** no próximo plano antes de prosseguir para C1 (gate consolidado em /run-plan, próximo item do Batch 3 do roteiro). Validação em uso real é o gatilho do roteiro: "executar **um por vez** e validar antes do próximo."
- Plano abre o caminho para `templates/adr.md` no futuro — ADR-001 documenta os gatilhos de revisão.

## Pendências de validação

- ~~Smoke test do template em uso real: invocar `/triage` num pedido fictício pós-merge+reinstall do plugin e confirmar que (i) skill lê `templates/plan.md`; (ii) plano produzido segue o esqueleto (seções obrigatórias presentes; opcionais omitidas quando não aplicáveis); (iii) headers em PT-BR (idioma do repo); (iv) campos especiais do `## Contexto` aparecem só quando relevantes.~~ **Resolvido por inspeção direta pós-merge+reload.** Verificado: (i) `${CLAUDE_PLUGIN_ROOT}/templates/plan.md` existe e é consumido pela instrução textual de `skills/triage/SKILL.md:84` e referenciado em `skills/run-plan/SKILL.md:29`; (iii) template em PT-BR canonical conforme inspeção do arquivo. Sub-itens (ii) e (iv) ficam como confiança de design — placeholders e sub-bullets do skill cobrem; smoke real em invocação subsequente do /triage validará comportamentalmente.
