# Plano — `/next` planos em aberto competem no enum top-3

## Status

Pendente

## Contexto

A `/next` ganhou §4.6 hoje (commit `3626d64`, PR #117) materializando o bloco "Planos em aberto" via consumo do campo `## Status` codificado em [ADR-060](../decisions/ADR-060-heuristica-completude-planos-via-status.md). A redação herdou de §4.5 (pendências de validação) a regra "**não competem no enum** — operador escolhe via `Other` se quiser priorizar". A simetria foi adotada sem decisão independente sobre planos em aberto.

Já na 1ª invocação real da nova skill (esta sessão, 2026-06-12), o atrito apareceu: o plano `session-audit-skill` está `Pendente` e é o **trigger empírico nomeado** do próprio ADR-060 que acabou de fechar. Continuação natural da sessão é executá-lo (`/run-plan session-audit-skill`), mas a spec atual força o operador a digitar `Other` pra chegar lá. O atrito vai recorrer toda vez que houver plano `Pendente`/`Abortado` recente que seja continuação natural — `/run-plan` abortado por cross-cwd, plano committed sem executar, trigger de ADR shippado na sessão.

A semântica das duas seções é distinta e justifica políticas diferentes:

- **§4.5 — pendências de validação:** trabalho terminado (plano mergeou), ação composta (smoke real, qual cenário, qual ambiente), volume tipicamente alto (7 planos com pendências ativas hoje), urgência tipicamente baixa.
- **§4.6 — planos em aberto:** trabalho NÃO-terminado, ação direta (`/run-plan <slug>`), volume tipicamente baixo (1-3 planos simultâneos), urgência variável (trigger de ADR shippado = máxima).

**Decisão substantiva (do /triage que gerou este plano):**

- (B) Planos em aberto entram no enum; pendências continuam informativas — respeita assimetria semântica 4.5↔4.6.
- **Restrição a `Pendente`:** apenas planos com `Status: Pendente` competem no enum top-3. `Abortado` permanece visível somente no bloco informativo "Planos em aberto" (carrega signal de "decisão de parar já tomada"; sem trigger empírico para competir no enum top-3 per ADR-043 § Ockham operacionalizado critério 1).
- **Composição:** cap em 2 planos `Pendente` no top-3; BACKLOG mantém ≥1 slot sempre. N_Pendente=0 → 3 BACKLOG (status quo). N_Pendente=1 → 1 plano + 2 BACKLOG. N_Pendente≥2 → 2 planos + 1 BACKLOG. Planos `Pendente` além do cap viram bloco informativo residual (`Abortado` sempre fica no bloco).
- **Ordenação dentro do bloco informativo:** `Pendente` (residuais, quando há) > `Abortado`; dentro de cada estado, mais-recente-no-FS > mais-antigo (mtime); tiebreaker mtime empatado = ordem alfabética do slug. Mesma ordenação aplica-se aos `Pendente` que entram no top-3.
- **Pendências de validação:** seguem bloco informativo separado, regra atual preservada.

**ADRs candidatos:** ADR-060 (autoriza §4.6, cuja regra de composição é refinada — não-contradição), ADR-006 (bifurcação discreta presente → enum; força a favor de opções nomeadas competirem em vez de exigir `Other`).

**Linha do backlog:** plugin: /next planos em aberto competem no enum top-3 (cap em 2, BACKLOG ≥1 slot)

## Resumo da mudança

Refinar §4.6 + §5 da `/next` para que planos com `Status: Pendente` compitam no enum top-3 com BACKLOG, sob regra de composição cap-em-2 (BACKLOG ≥1 slot sempre) e ordenação mais-recente > mais-antigo (mtime; tiebreaker alfabético). Planos `Abortado` permanecem visíveis só no bloco informativo "Planos em aberto" — sem trigger empírico para competir no enum top-3 per ADR-043 § Ockham operacionalizado critério 1. Pendências de validação (§4.5) inalteradas. Ajustar § O que NÃO fazer linha 130 para refletir a nova semântica de "top-3".

## Arquivos a alterar

### Bloco 1 — `/next` §4.6 + §5 + § O que NÃO fazer {reviewer: code}

- `skills/next/SKILL.md`:
  - §4.6 cabeçalho (linha 91): remover "não compete no enum" do parêntese; substituir por "planos `Pendente` competem no enum top-3 sob regra de composição cap-2 (passo 5); planos `Abortado` permanecem no bloco informativo. Ortogonal ao bloco de pendências (§4.5)".
  - §4.6 sub-passo 3 (linha 98): trocar formulação "Acumular pares `(slug, estado)`" por "Acumular tuplas `(slug, estado, mtime)` ordenadas por `(estado: Pendente > Abortado, mtime: desc, slug: asc)`. Lista vazia → omitir o bloco informativo no passo 5; top-3 segue só do BACKLOG."
  - §5 (linhas 100-108) — **composição do top-3:** bullet "Top 3 candidatos" carrega regra explícita: "top-3 = primeiros `min(N_Pendente, 2)` planos `Pendente` (ordenação do §4.6) + restante do BACKLOG (ranking do passo 4). N_Pendente=0 → 3 BACKLOG. N_Pendente=1 → 1 plano + 2 BACKLOG. N_Pendente≥2 → 2 planos + 1 BACKLOG. Planos `Pendente` além do cap entram no bloco informativo residual junto com todos os `Abortado`."
  - §5 (mesmas linhas) — **renderização do enum + blocos:** Bullet "Pendências de validação em planos" inalterado (continua "não competem no enum"). Bullet "Planos em aberto" agora descreve o bloco informativo: todos os `Abortado` + `Pendente` residuais além do cap-2; lista vazia (nenhum `Abortado` E N_Pendente ≤ 2) → omitir o bloco. Enum exibe `<slug>` literal como label da opção `/run-plan <slug>` quando vem de plano `Pendente`; texto do BACKLOG quando vem da linha. `description` da opção carrega `Plano em aberto: Pendente` quando vem de plano (BACKLOG não precisa de marker análogo).
  - § O que NÃO fazer linha 130: substituir "Não apresentar mais de 3 sugestões no top" por "Não apresentar mais de 3 opções nomeadas no enum (Other é automático e fora do cap)". Editorial — invariante de cap-3 preservada, semântica de "top" estendida para misturar BACKLOG e planos em aberto.

## Verificação end-to-end

Inspeção textual sobre o `SKILL.md` modificado pré-merge (sem `test_command`).

1. **§4.6 cabeçalho refletindo nova regra:** `grep -n "competem no enum top-3" skills/next/SKILL.md` retorna ≥1 match (em §4.6); `grep -n "não competem no enum\|não compete no enum" skills/next/SKILL.md` retorna **apenas** o match em §5 referente a pendências de validação (1 match, na linha do bullet "Pendências"; texto do bullet "Planos em aberto" da §5 não contém mais a frase).
2. **§4.6 carrega mtime na tupla acumulada:** `grep -n "mtime" skills/next/SKILL.md` retorna ≥1 match em §4.6 (sub-passo 3 reformulado).
3. **§5 carrega regra de composição cap-2:** `grep -n "min(N_Pendente, 2)" skills/next/SKILL.md` retorna ≥1 match em §5.
4. **§5 cobre os 3 casos numéricos:** Read do bullet "Top 3 candidatos" da §5 confirma presença das 3 ramificações `N_Pendente=0`, `N_Pendente=1`, `N_Pendente≥2` com `min(N_Pendente, 2)` e contagem de BACKLOG correspondentes. Inspeção textual (counts hardcoded ficam fora de grep per diretriz canonical `templates/plan.md` § Verificação end-to-end #4).
5. **§5 distingue enum text de plano em aberto vs BACKLOG:** Read da §5 confirma que enum recebe `<slug>` literal quando vem de plano `Pendente` e texto da linha quando vem do BACKLOG; `description` do plano carrega "Plano em aberto: Pendente".
6. **§ O que NÃO fazer linha 130 reescrita:** `grep -n "Não apresentar mais de 3 opções nomeadas no enum" skills/next/SKILL.md` retorna 1 match; `grep -n "Não apresentar mais de 3 sugestões no top" skills/next/SKILL.md` retorna 0 matches.
7. **Pendências de validação inalteradas:** Read das linhas 77-87 (§4.5) confirma que nenhum texto foi tocado em §4.5; bullet "Pendências de validação em planos" da §5 mantém formulação "não competem no enum".
8. **`Abortado` excluído do enum:** Read da §5 bullet "Top 3 candidatos" e bullet "Planos em aberto" confirma que `Abortado` aparece exclusivamente no bloco informativo; nenhuma menção a `Abortado` no fluxo de composição do enum.
9. **Frontmatter intacto:** `awk '/^---$/{flag++; next} flag==1{print}' skills/next/SKILL.md` retorna o mesmo bloco (`name`, `description`, `disable-model-invocation: false`, `roles`).

## Verificação manual

Smoke real pós-`/reload-plugins` em consumer com fixtures controladas. Cada cenário roda `/next` e verifica composição do top-3 + blocos informativos.

1. **Cenário 1 — N_Pendente=0, sem Abortado (regressão):** consumer com `plans_dir` contendo apenas planos sem `## Status` ou com Status `Concluído`. `/next` retorna top-3 = 3 BACKLOG. Bloco "Planos em aberto" omitido. Bloco "Pendências de validação" mostrado se houver pendências ativas. Comportamento idêntico ao status quo.

2. **Cenário 2 — N_Pendente=1, sem Abortado:** consumer com 1 plano `Status: Pendente`. `/next` retorna top-3 = 1 plano + 2 BACKLOG. Plano aparece com `<slug>` na opção do enum, `description` indicando "Plano em aberto: Pendente". Bloco "Planos em aberto" omitido (sem Abortado e Pendente cabe no cap).

3. **Cenário 3 — N_Pendente=1, 1 Abortado:** consumer com 1 Pendente + 1 Abortado. `/next` retorna top-3 = 1 plano Pendente + 2 BACKLOG. Bloco "Planos em aberto" lista o Abortado. `Abortado` NÃO aparece no enum.

4. **Cenário 4 — N_Pendente=2, 2 Abortado:** `/next` retorna top-3 = 2 planos Pendente (mais-recente antes) + 1 BACKLOG. Bloco "Planos em aberto" lista os 2 Abortado.

5. **Cenário 4b — N_Pendente=3, 1 Abortado (Pendente residual + Abortado):** `/next` retorna top-3 = 2 planos Pendente + 1 BACKLOG. Bloco "Planos em aberto" lista 1 Pendente residual (3º Pendente além do cap) seguido de 1 Abortado (ordenação `Pendente > Abortado` no bloco preservada).

6. **Cenário 5 — Pendências de validação ativas:** consumer com pendências de validação em ≥2 planos não-em-curso. `/next` mostra bloco "Pendências de validação em planos" separado; pendências NÃO entram no enum top-3 (regra preservada).

7. **Cenário 6 — Ordenação por mtime:** consumer com 2 planos Pendente; um arquivo mais recente que o outro. `/next` lista o mais-recente antes no enum top-3.

8. **Cenário 7 — Plano em aberto em-curso:** consumer com worktree ativa cujo slug bate em plano com `Status: Pendente`. Plano é tratado como "em curso" via filtro §4.5 (worktree-active) e NÃO entra no §4.6 nem no top-3.

## Notas operacionais

- Ordem de edit dentro do Bloco 1 não é crítica — todos os edits são cirúrgicos no mesmo arquivo; code-reviewer cobre coerência.
- `mtime` do plano consumido em §4.6 sub-passo 3 é o do arquivo no FS local (`stat -c '%Y' <plano>`); proxy razoável para "trigger mais quente". Não usar `git log` por plano — custo desnecessário; mtime já basta. Limitação aceitável: rebase/sync podem resetar mtime, mas a perda de signal é localizada e o operador consegue inferir prioridade por outros sinais (NOTES.md, BACKLOG, contexto da sessão).
- Quando há planos Pendente com mtime empatado (caso raro), tiebreaker = ordem alfabética do slug (determinístico, sem cutucada).
- A mudança não invalida o item da §4.6 que acabou de shippar (PR #117) — refina semântica do enum, preserva a detecção do `## Status` field e o bloco informativo (agora residual + Abortado completos).

## Decisões absorvidas

- `next-planos-aberto-enum.md:23` (§ Contexto Ordenação): tiebreaker mtime empatado = alfabética slug + ordenação aplica-se identicamente ao top-3 e ao bloco informativo residual (caminho-único).
- `next-planos-aberto-enum.md:58` (§ Verificação end-to-end #4): substituir `grep -c "N=0\|N=1\|N≥2"` por Read inspection per diretriz canonical templates/plan.md § Verificação end-to-end #4 (caminho-único).
- `next-planos-aberto-enum.md:40-41` (§ Arquivos a alterar Bloco 1 §5): split do bullet denso em 2 sub-bullets (composição vs renderização do enum) — clareza editorial para reviewer (caminho-único).
