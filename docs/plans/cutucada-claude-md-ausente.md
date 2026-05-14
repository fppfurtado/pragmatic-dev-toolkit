# Plano — Cutucada de descoberta cobre `CLAUDE.md` ausente

## Contexto

Sessão `/debug` 2026-05-14 surfou gap em projeto novo: skills com `roles.required` não emitem cutucada de descoberta de `/init-config` quando `CLAUDE.md` está **ausente** — condição 1 do triple gating em [ADR-017](../decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) ("`CLAUDE.md` existe") falha. Resultado: justamente o caso onde descoberta mais importa (operador onboarding em projeto novo) fica sem sinalização proativa. Limitação explícita em ADR-017 § Limitações (linha 81) + Alternativa (f) descartada (over-reach do plugin sobre estrutura do consumer).

Decisão: estender a cutucada com **string adaptada** que reconhece a ausência sem prescrever criação automática — preserva postura editorial não-reparativa (`/init-config` step 1 segue parando e orientando o operador a criar `CLAUDE.md` manualmente; cutucada apenas torna o sinal explícito 1 linha antes, na própria saída da skill que o operador acabou de invocar).

**ADRs candidatos:** ADR-029 (sucessor parcial de ADR-017 § Limitações + Alternativa (f) descartada).

**Linha do backlog:** plugin: ADR-029 + cutucada cobre `CLAUDE.md` ausente — sucessor parcial de ADR-017 § Limitações; string-B nova emitida pelas 5 skills com `roles.required` quando `CLAUDE.md` ausente; string-A preservada; dedup conversation-scoped por string; CLAUDE.md + 5 SKILLs tocadas (`/init-config` inalterada).

## Resumo da mudança

Gating sai do "triple" original para **três saídas do mesmo gate** parametrizadas pelo estado de `CLAUDE.md`:

- **`CLAUDE.md` ausente** → emitir string-B (adaptada): `Dica: este projeto não tem CLAUDE.md. Crie o arquivo e rode /init-config para configurar os papéis do plugin.`
- **`CLAUDE.md` presente sem marker** → emitir string-A (canonical atual, sem mudança).
- **`CLAUDE.md` presente com marker** → silêncio.
- **Dedup conversation-scoped** (per [ADR-010](../decisions/ADR-010-instrumentacao-progresso-skills-multi-passo.md)) aplicado **por string**: cada uma observa o histórico visível por si; sair de "ausente" para "presente sem marker" na mesma sessão pode disparar string-A mesmo após string-B já ter aparecido (são gaps distintos).

Escopo: as **5** skills atuais com `roles.required` — `/triage`, `/new-adr`, `/run-plan`, `/next`, `/draft-idea`. ADR-017 listava 4 quando foi escrito; `/draft-idea` foi adicionada por [ADR-027](../decisions/ADR-027-skill-draft-idea-elicitacao-product-direction.md) já herdando a convenção, e adere automaticamente à extensão. CLAUDE.md → "Cutucada de descoberta" atualizada para refletir a nova mecânica; herança editorial permanece (autor de skill nova com `roles.required` adiciona o paragrafo seguindo o template das 5 existentes).

`/init-config` segue inalterada — step 1 com `CLAUDE.md` ausente continua parando com mensagem orientadora; nada a alterar lá.

## Arquivos a alterar

### Bloco 1 — Seção "Cutucada de descoberta" em CLAUDE.md {reviewer: code}

- `CLAUDE.md` (seção `## Cutucada de descoberta`, linhas ~127-145):
  - Parágrafo introdutório passa a citar ADR-017 + ADR-029 (ambos), e descrever que a cutucada cobre **dois** gaps: (i) CLAUDE.md ausente; (ii) CLAUDE.md presente sem marker.
  - Bloco "Triple gating" renomeia para "Gating em dois casos"; lista cada caso com sua condição e sua string canonical.
  - Manter texto sobre dedup conversation-scoped (alinhado com ADR-010), com nota explícita de que o dedup é **por string** (cada uma independente).
  - Adicionar string-B em segundo blockquote, paralelo ao da string-A.
  - Manter cláusula "Editorial inheritance" referindo às 5 skills existentes como template.

### Bloco 2 — Gating estendido nas 5 skills com `roles.required` {reviewer: code}

Substituir, em cada SKILL.md, o parágrafo único de cutucada (gating + 1 blockquote de string canonical) por estrutura paralela cobrindo os dois casos, preservando a frase de posicionamento específica de cada skill ("Antes de devolver controle" / "Antes de encerrar" / "Após reportar findings..." / "Antes do enum a seguir" / "última linha quando..."). Template proposto (operador adapta o posicionamento por SKILL conforme prosa pré-existente):

> **Cutucada de descoberta** (per [ADR-017](../../docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md) + [ADR-029](../../docs/decisions/ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md)). <Frase de posicionamento pré-existente>, escolher caminho conforme estado de `CLAUDE.md`:
>
> - **`CLAUDE.md` ausente** + string-B abaixo não aparece no contexto visível desta conversa CC → emitir como última linha:
>   > Dica: este projeto não tem `CLAUDE.md`. Crie o arquivo e rode `/init-config` para configurar os papéis do plugin.
> - **`CLAUDE.md` presente** + `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna não-zero (marker ausente) + string-A abaixo não aparece no contexto visível → emitir como última linha:
>   > Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.
> - **CLAUDE.md presente com marker** OU **dedup hit em ambas** → suprimir silenciosamente.

Paths dos 5 sites:

- `skills/triage/SKILL.md` — passo 5, parágrafo "Cutucada de descoberta" (linhas ~179-181).
- `skills/run-plan/SKILL.md` — passo final de relatório, parágrafo "Cutucada de descoberta" (linhas ~170-172).
- `skills/new-adr/SKILL.md` — após reportar findings do design-reviewer, parágrafo "Cutucada de descoberta" (linhas ~57-59).
- `skills/next/SKILL.md` — antes do enum de seleção, parágrafo "Cutucada de descoberta" (linhas ~64-66).
- `skills/draft-idea/SKILL.md` — última linha do relatório, parágrafo "Cutucada de descoberta" (linhas ~92-94).

Cross-ref em cada SKILL: substituir citação solo de ADR-017 por citação dupla (ADR-017 + ADR-029).

**Posicionamento `/next` é exceção.** A SKILL atual emite a cutucada **antes do `AskUserQuestion` final** (não como "última linha do relatório" no sentido das outras 4). Frase de posicionamento pré-existente em `skills/next/SKILL.md:64-66` mantém "última linha do relatório (antes do enum)" — preservar essa parêntese ao aplicar o template. Não sub-blocar — variação fica como nota inline.

## Verificação end-to-end

- ADR-029 existe em `docs/decisions/` com status `Proposto`, cross-ref a ADR-017 (sucessor parcial de § Limitações + Alternativa (f)).
- `CLAUDE.md` seção "Cutucada de descoberta" descreve gating em dois casos, lista ambas as strings canonical em blockquotes separados, cita ADR-017 + ADR-029.
- Em cada um dos 5 SKILL.md (`triage`, `run-plan`, `new-adr`, `next`, `draft-idea`): parágrafo "Cutucada de descoberta" descreve os dois casos, lista ambas as strings, cita ADR-017 + ADR-029. Frase de posicionamento pré-existente preservada.
- `grep -l "este projeto não tem .CLAUDE.md.. Crie" skills/*/SKILL.md` retorna os 5 paths.
- `grep -l "este projeto não declara o bloco" skills/*/SKILL.md` retorna os 5 paths (string-A preservada literal).
- `grep -l "ADR-029" CLAUDE.md skills/*/SKILL.md` retorna 6 paths (CLAUDE.md + 5 skills).
- `! grep -q "Triple gating" CLAUDE.md` — rótulo antigo ausente (sinal de que o bloco migrou para "Gating em [dois casos|três saídas]").
- `grep -L "ADR-017.*ADR-029\|ADR-029.*ADR-017" skills/{triage,run-plan,new-adr,next,draft-idea}/SKILL.md` retorna vazio — todos os 5 contêm ambos os IDs na mesma referência (sem perda acidental de ADR-017).
- Sem outras superfícies tocadas: `docs/install.md`, `README.md`, `skills/init-config/SKILL.md` inalterados.

## Verificação manual

Cenários para smoke-test em consumer real (este repo não tem suite — gate é inspeção textual + execução manual):

1. **Projeto sem `CLAUDE.md`, primeira invocação de `/triage`** — diretório novo, `git init`, sem CLAUDE.md; rodar `/triage <intenção>`; confirmar que a última linha do relatório é a string-B literal (`Dica: este projeto não tem CLAUDE.md. Crie o arquivo e rode /init-config para configurar os papéis do plugin.`).

2. **Projeto sem `CLAUDE.md`, segunda skill na mesma sessão CC** — manter sessão; rodar segunda skill com `roles.required` (ex.: `/next` ou `/new-adr`); confirmar que string-B é **suprimida** (dedup conversation-scoped, string já visível no contexto). Se a string reaparecer, verificar se a sessão CC sofreu context compression (string-B fora da janela visível) — reaparecimento sob compression é aceito per ADR-010 + ADR-029 § Limitações, não regressão.

3. **Projeto com `CLAUDE.md` sem marker** — adicionar `CLAUDE.md` mínimo (1 linha) sem marker `<!-- pragmatic-toolkit:config -->`; rodar `/triage`; confirmar que string-A é emitida (comportamento ADR-017 preservado, sem regressão).

4. **Projeto com `CLAUDE.md` com marker** — adicionar marker + bloco YAML; rodar `/triage`; confirmar **silêncio** (gating fecha).

5. **Transição ausente → presente sem marker na mesma sessão** — começar sem CLAUDE.md, rodar `/triage` (vê string-B); criar CLAUDE.md mínimo sem marker; rodar `/new-adr`; confirmar que **string-A** aparece independente de string-B já estar no contexto (dedup é por string, não global). Como em #2, reaparição de string-A por context compression é aceita; o sinal de regressão seria string-A **não aparecer** apesar da janela visível não conter ocorrência anterior.

6. **Cobertura das 5 skills (string-B em projeto sem CLAUDE.md)** — em projeto sem CLAUDE.md, invocar cada skill com `roles.required` (`/triage`, `/new-adr`, `/run-plan`, `/next`, `/draft-idea`) em sessões CC novas; confirmar que cada uma dispara string-B na primeira invocação da sua sessão.

7. **Cobertura das 5 skills (string-A em projeto com CLAUDE.md sem marker)** — reaproveitar o projeto do cenário 3 (CLAUDE.md mínimo, sem marker); invocar as 5 skills em sessões CC novas; confirmar que cada uma dispara string-A. Fecha cobertura dos 10 ramos (5 skills × 2 strings); pega regressão onde, ao adaptar a frase de posicionamento por SKILL, o ramo string-A foi quebrado.

## Notas operacionais

- Ordem dos blocos: 1 (CLAUDE.md) → 2 (5 SKILLs). CLAUDE.md é a fonte editorial; SKILLs replicam. Editar SKILLs antes de CLAUDE.md cria drift transiente entre commits — `doc-reviewer` poderia flagrar. Bloco 1 primeiro fecha o loop.
- 5 sites × 2 strings = duplicação aceita per ADR-017 § Alternativa (g) (YAGNI sobre helper compartilhado). Mudança na redação de qualquer string, no marker, ou adição de skill nova com `roles.required` requer atualizar todos os sites — sustentação editorial (ADR-017 § Decisão).
- Validação manual fica como spec para smoke pós-release — repo do plugin não tem ambiente para exercitar interação real com Claude Code em consumer; operador roda no PJe ou outro consumer pós-reinstall.
- Cross-ref recíproco: ADR-029 cita ADR-017 (sucessor parcial); CLAUDE.md e 5 SKILLs citam ambos os ADRs.
- Reabertura prevista: se 5ª condição de revisão de ADR-017 ("5ª skill com `roles.required` aparecer") ocorrer no futuro, ambos os ADRs entram em reavaliação simultânea (alternativa (g) — helper compartilhado — fica mais atraente quando o universo dobra).
