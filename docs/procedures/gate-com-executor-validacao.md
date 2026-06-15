# Procedure — gate-com-executor-validacao

Procedure shared codificando a categoria `gate-com-executor-validacao` em fonte canonical única (per [ADR-064](../decisions/ADR-064-gate-com-executor-validacao-2-sites.md)). Consumida por `skills/run-plan/SKILL.md` §3.2 (gate manual) e `skills/session-audit/SKILL.md` (passo 6, tipo derivado `executar_validacao_pendente`). Mudança da heurística vive aqui; SKILL.mds referenciam este arquivo como fonte canonical. Paralelo editorial a `docs/procedures/cutucada-descoberta.md` (consumido por 6 skills) e `docs/procedures/forge-auto-detect.md` (consumido por 5 skills).

## 1. Heurística de classificação

Para cada cenário do plano (bullet de `## Verificação manual` em `/run-plan §3.2`, ou bullet de `## Pendências de validação` em `/session-audit`), classificar em uma das 3 etiquetas:

- **[executável-pra-mim]** — cenário cobrível por:
  - Bash/Read/grep/sed sobre arquivos do repo.
  - AST parse (`python3 -c "import ast; ast.parse(...)"` e equivalentes).
  - Comando shell de teste localizado (sem mutação remota).
  - Invocação de reviewer subagent retroativo sobre commit já existente.
  - Fixture mecânico controlado (criação de plans/files no próprio repo + simulação + cleanup).
  - Comparação textual entre arquivos.

  Substância concreta: comando shell verificável, padrão grep, invocação de reviewer, comparação textual. Cenário descreve o **como** mecanicamente (não só o **que**).

- **[exige-operador]** — cenário descreve:
  - UI interaction (clicar, navegar, screenshot).
  - Dependência de dado real de produção (volume, latência, integração externa).
  - Business judgment (avaliação subjetiva de UX, fluxo, redação).
  - Sistema externo controlado pelo operador (TJPA real, Bitbucket, repos terceiros).

- **[ambíguo]** → cláusula default-conservadora → classificar como **[exige-operador]** (preserva consent + visibilidade da fronteira; over-correção em direção a delegar é a polaridade defensiva correta).

## 2. Cláusula blast-radius compartilhado

**Nunca** classificar como [executável-pra-mim] cenário que envolve mutação remota:

- `git push` em qualquer branch.
- `gh release create` ou equivalente forge.
- `gh issue create` / `glab issue create`.
- `gh issue close` / `glab issue close`.
- Qualquer comando com efeito imediato fora da worktree corrente (deploy, webhook, mensagem em chat externo, mutação em repo terceiro).

Tais cenários são **sempre** [exige-operador] independente de "executável tecnicamente". Preserva o princípio CLAUDE.md global de confirmação para ações de blast-radius compartilhado + ADR-049 § Decisão (a) + bullet "não classificar cenários como [executável-pra-mim] que mutam state remoto" no `## O que NÃO fazer` das SKILL.mds consumidoras.

## 3. Formato canonical do reporte de classificação

Antes do enum/cutucada (em `/run-plan §3.2` ou `/session-audit`), reportar a classificação como prosa informativa — 1 bullet por cenário com tag explícita + razão:

```
- [executável] Cenário N: <texto curto do cenário>. Razão: <heurística aplicada — ex.: "smoke programático via Bash grep", "AST parse mecânico", "reviewer retroativo sobre commit <hash>">.
- [exige-operador] Cenário M: <texto curto do cenário>. Razão: <heurística aplicada — ex.: "UI interaction explícito", "depende de dado TJPA real", "business judgment sobre framing">.
- [exige-operador] Cenário K: <texto curto do cenário>. Razão: cláusula blast-radius — muta state remoto (gh release create).
```

Razão é obrigatória — permite operador discordar com base concreta se classification model errar.

## 4. Cláusula de execução

Quando opção `Executar [executável]` (ou equivalente no site consumidor) for escolhida pelo operador:

1. **Rodar cenários [executável] em sequência.** Paralelo onde tool calls permitem sem dependência ordenada; serial onde há dependência (ex.: smoke 2 lê output de smoke 1).
2. **Reportar verdict per cenário** em formato concreto: `PASS` / `FAIL` / `CLEAN (0 findings)` / `N findings: <síntese curta>` / `erro literal: <stderr>`.
3. **Deferir cenários [exige-operador] explicitamente** em prosa: `"Defere para sua validação manual: cenário N, M, K (razões reportadas acima)."`.
4. **Após execução completa**, devolver controle ao site consumidor para próximo passo (re-dispatch do enum binário original `Validei (Recommended)` / `Falhou — descrever` em `/run-plan §3.2`; marcar `Encerrada YYYY-MM-DD` no plan body em `/session-audit`).

Falha mid-execução (cenário [executável] erra fora do esperado) → parar; reportar status até ali; deixar restantes como pendentes; devolver controle. Operador decide reverter ou seguir.

## 5. Consumidores

- **`skills/run-plan/SKILL.md` §3.2** (gate manual de validação): classificação prévia + 3ª opção condicional sobre enum binário (`Validei` / `Falhou — descrever`) + re-dispatch binário pós-execução.
- **`skills/session-audit/SKILL.md`** (passo 6, tipo derivado `executar_validacao_pendente`): detecção de planos com `## Pendências de validação` tocados pela sessão + classificação + addendum `Pendências de validação executáveis` no relatório + 4ª opção condicional na cutucada batched + execução + marcar `Encerrada YYYY-MM-DD` no plan body.

Mudança da heurística (etiquetas, blast-radius, formato do reporte, cláusula de execução) vive **aqui** — SKILL.mds referenciam o procedure literalmente, não duplicam substância.
