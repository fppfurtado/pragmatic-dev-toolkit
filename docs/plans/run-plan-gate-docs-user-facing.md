# run-plan-gate-docs-user-facing

## Contexto

O primeiro skip silente do gate 4.3 de `/run-plan` verifica apenas se "arquivos `.md`" foram listados no plano e tocados pelo diff — sem distinguir `.md` de implementação (skills, agents, philosophy) de `.md` user-facing (README, install, changelog, guides).

Consequência: um plano que edita `skills/run-plan/SKILL.md` dispara o skip silente do gate, mesmo que README e install.md não tenham sido atualizados. O gate existe precisamente para capturar esse caso.

Correção: **positive list** — o skip só dispara quando o plano listou E tocou pelo menos um `.md` que bate nos padrões user-facing: `README*`, `CHANGELOG*`, `install.md`, `docs/install.md`, `docs/guides/**`. Qualquer outro `.md` (skills, agents, hooks, philosophy) não conta para o skip.

**Linha do backlog:** /run-plan: condição de skip do sanity check de docs (4.3) não distingue arquivos de implementação .md de documentação user-facing — restringir a arquivos README/install/changelog/guias ou adicionar critério negativo para arquivos de skill/agent

## Resumo da mudança

Qualificar o primeiro bullet do passo 4.3 em `skills/run-plan/SKILL.md`: substituir a referência genérica a "arquivos `.md`" pela noção de "arquivo `.md` user-facing" com a positive list explícita.

## Arquivos a alterar

### Bloco 1 — `skills/run-plan/SKILL.md` {reviewer: code}

No passo **4. Gate final**, subseção **3. Sanity check de documentação**, primeiro bullet:

**Antes:**
> Skip silente se o plano já listou arquivos `.md` em `## Arquivos a alterar` e o diff agregado dos blocos os tocou — documentação fez parte do plano, gate cumprido.

**Depois:**
> Skip silente se o plano já listou pelo menos um arquivo `.md` **user-facing** em `## Arquivos a alterar` e o diff agregado dos blocos o tocou — padrões que contam: `README*`, `CHANGELOG*`, `install.md`, `docs/install.md`, `docs/guides/**`. Arquivos `.md` de implementação (skills, agents, hooks, philosophy) não ativam o skip; o gate continua e pergunta sobre docs.

## Verificação end-to-end

Verificação textual (sem test suite):

1. Ler o bullet 4.3 modificado e confirmar que a distinção user-facing vs implementação está explícita e os padrões estão listados.
2. Aplicar o critério mentalmente a dois cenários:
   - Plano que lista `skills/run-plan/SKILL.md` em `## Arquivos a alterar` → skip **não** dispara → gate pergunta sobre docs.
   - Plano que lista `README.md` em `## Arquivos a alterar` → skip dispara → gate omitido.
3. Confirmar que a segunda condição de skip (Resumo da mudança sem surface user-facing) permanece inalterada.
