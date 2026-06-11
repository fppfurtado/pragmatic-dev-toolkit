# Plano — Paralelizar verificação "já implementado?" em /next via Agent (Explore)

## Contexto

`/next` passo 3 ("Verificar implementação no código") itera serialmente sobre os candidatos lidos no passo 2 (parametrizado por `N` per commit `12b3185`), procurando evidência no codebase do consumer. Em consumers com backlog grande (`tjpa/pje-2.1` com 100+ issues em modo `forge`, meta-system com volume análogo), `/next 20` (ou padrão 10 contra `## Próximos` grande) faz N round-trips serialmente — latência cresce linearmente.

YAGNI registrado na linha do BACKLOG ("backlog crescer ≥20 itens ou pain real surgir") **materializou-se empiricamente** em consumers reais, contradizendo o estado original do plugin (~3 itens em `## Próximos`). Decisão estrutural correlata (uso de subagent em loop interno de skill) contradiz precedente de **ADR-009** (rejeitou subagent para design-reviewer por overhead vs volume pequeno) e seu sucessor arquivado **ADR-011**. Refinamento doutrinal: subagent aceitável quando a shape é **per-item probe** (paralelismo cresce com `N`) + threshold mínimo, distinta do shape "scan único" do reviewer.

**ADRs candidatos:** ADR-009 (sucessor parcial — refina critério "volume vs subagent overhead" para shape per-item), ADR-059 (companion já materializado pré-`/run-plan` via delegação `/triage` → `/new-adr`; codifica decisão estrutural; plano executa a consequência).

**Linha do backlog:** plugin: paralelizar verificação "já implementado?" em `/next` via Agent (Explore) por candidato — spawn 1 subagent por linha de `## Próximos`, retorna verdict (sim/não/parcial + path). Hoje serial em main; latência cresce linearmente com tamanho do backlog. YAGNI até backlog crescer ≥20 itens ou pain real surgir; backlog atual (~3 itens em Próximos) não justifica overhead de subagent.

## Resumo da mudança

`/next` passo 3 passa a paralelizar a verificação de evidência via Agent (Explore), com escolhas:

- **Granularidade:** 1 subagent por candidato. Maximiza paralelismo; cold-start replicado mas latência total ≈ max(individual) em vez de soma.
- **Threshold de ativação:** `N ≥ 5`. Backlog pequeno (`N < 5`) preserva loop serial — cold-start de subagent perde para grep direto. Threshold é editorial; gatilho de revisão concreto no ADR (refinar quando dor empírica surgir).
- **Subagent type:** `Explore` (read-only, codebase-focused, recomendado para "lookup/grep" focado per system prompt; rebatida `general-purpose` por cold-start maior e instruções não-otimizadas para lookup focado — ver ADR-059 § Decisão).
- **Contrato de retorno do subagent:** texto curto estruturado — verdict (`forte` / `fraca` / `sem`) + path:line de evidência quando aplicável + justificativa de 1 linha.
- **Mode-agnóstico:** mesmo algoritmo em modo arquivo e `forge`; em ambos os modos, a verificação procura evidência no codebase do consumer (não no forge).
- **Falha de subagent:** verdict assumido como `sem evidência` + warning reportado; não bloqueia outros candidatos.

Não muda passos 1, 2, 4, 4.5, 5, 6, 7 do `/next`. Não muda /triage nem /run-plan.

ADR-059 (sucessor parcial de ADR-009) codifica o critério mecânico para "subagent em loop interno de skill" — **já materializado pré-`/run-plan`** via delegação `/triage` → `/new-adr`. Plano executa só a consequência (SKILL refactor).

## Arquivos a alterar

### Bloco 1 — refactor /next passo 3 para spawn paralelo {reviewer: code}

- `skills/next/SKILL.md`:
  - Atualizar passo 3 ("Verificar implementação no código") para descrever caminho serial (`N < 5`) e caminho paralelo (`N ≥ 5`) com subagent `Explore` por candidato.
  - Adicionar contrato de prompt do subagent (input: linha do candidato + briefing do que classificar; output: verdict + path:line + justificativa de 1 linha) como sub-bloco do passo 3.
  - Adicionar bullet em `## O que NÃO fazer`: "Não paralelizar quando `N < 5` — cold-start perde para grep direto."
  - Referenciar ADR-059 no passo 3 (cita curta + link interno).

## Verificação end-to-end

1. Passo 3 do `skills/next/SKILL.md` contém 3 marcadores estruturais distintos identificáveis (sub-bloco `caminho serial` para `N < 5`, sub-bloco `caminho paralelo` para `N ≥ 5`, sub-bloco `contrato do subagent` com formato de input + output). Inspeção textual dos headers/parágrafos.
2. Bullet de guardrail (`N < 5` → não paralelizar) presente em `## O que NÃO fazer` do `skills/next/SKILL.md`.
3. ADR-059 referenciado no passo 3 do `skills/next/SKILL.md` (link interno ou cita em prosa). `git status --porcelain -- docs/decisions/ADR-059-*.md` retorna vazio (ADR vigente não foi mutado pelo plano).

## Verificação manual

Cenário 1 — backlog pequeno (`N < 5`, caminho serial preservado): invocar `/next 3` em consumer com ≥3 itens em `## Próximos`; verificar via `TaskList` / output que **não há** spawn de subagent. Verdicts retornados pelo grep serial; report idêntico ao comportamento atual.

Cenário 2 — backlog médio (`N = 10`, paralelo ativado): invocar `/next` (default 10) em consumer com ≥10 itens em `## Próximos`. Esperado: 10 subagents Explore spawned em paralelo (batch único de tool calls); retorno consolidado com verdicts. Latência total ≈ latência do candidato mais lento, não soma. **Evidência observável:** transcript da sessão contém **1 mensagem do assistente** com N tool calls `Agent` em paralelo (não N mensagens sequenciais). Operador inspeciona via UI da sessão.

Cenário 3 — backlog grande (`N = 20+`, forge mode): em consumer com `paths.backlog: forge` e ≥20 issues abertas sem assignee (e.g., `tjpa/pje-2.1`), invocar `/next 20`. Esperado: 20 subagents spawned; verdicts retornados; movimentação remota via `gh/glab issue close` cutucada por evidência forte preserva comportamento atual. **Evidência observável:** mesma forma do cenário 2 (1 mensagem do assistente com 20 tool calls `Agent` paralelos).

Cenário 4 — falha de subagent: **verificação diferida** — Claude Code não expõe API para simular timeout ou injetar falha controlada em `Agent`. Primeira falha real observada em invocação de `/next` em consumer serve de teste empírico; até lá, código segue o caminho documentado (warning + `sem evidência` + continua). Reabrir cenário se incidente recorrente exigir teste reproduzível.

Cenário 5 — verdict `forte` em modo arquivo: subagent retorna `forte` para candidato X com path:line. Esperado: linha movida para `## Concluídos` no arquivo BACKLOG (mantém comportamento de passo 3 mode arquivo); commit no passo 6.

Cenário 6 — verdict `forte` em modo `forge`: subagent retorna `forte`. Esperado: cutucada `AskUserQuestion` por issue (header `Forge`, opções `Aplicar no forge` / `Cancelar`) seguindo policy atual; `gh/glab issue close` aplicado em confirmação. Mantém ADR-058 § (e).

## Notas operacionais

- **Spawn paralelo:** todos os subagents disparados num **único turno** via batch de tool calls (per `parallel tool calls where possible` no system prompt). Aguardar todos os retornos antes de classificar.
- **Briefing do subagent:** prompt curto e self-contained — não assume contexto da conversa principal. Inclui: descrição do plugin (1 linha), linha literal do candidato, instruções de classificação (`forte` exige código diretamente mapeável + path:line; `fraca` é evidência parcial/inferência incerta; `sem` é ausência), formato de output esperado.
- **Cold-start preservation `N < 5`:** caminho serial **não** muda — usa mesmo grep/glob direto do main thread. Garante que `/next 3` em backlog pequeno permanece barato.
- **ADR-059 materializado pré-`/run-plan`:** o ADR companion foi criado durante `/triage` via delegação a `/new-adr` (pré-revisado pelo `design-reviewer`, 2 findings absorvidos + 2 cutucados-resolvidos). `/run-plan` executa só o Bloco 1 (SKILL refactor); ADR não entra em `## Arquivos a alterar` para evitar dispatch duplo de write.

## Decisões absorvidas

- ADR-059 § Alternativas consideradas: adicionada alternativa "Cap mecânico em `N` sem paralelizar" rebatida com argumentos de visibilidade total + cerimônia de particionamento (caminho-único).
- ADR-059 § Contexto: parágrafo curto diferencia gatilho de revisão de ADR-009 (reviewer document-level) do que ADR-059 aciona (skill per-item probe) — eixos distintos (caminho-único).
- Plano § Verificação end-to-end: critérios 1+2 tautológicos (grep de keywords) substituídos por verificação estrutural de 3 marcadores no passo 3 do SKILL (caminho-único).
- Plano § Verificação manual cenários 2-3: âncora observável acrescentada (1 mensagem do assistente com N tool calls paralelos via UI da sessão) (caminho-único).
- Plano § Arquivos a alterar: Bloco 2 (criação do ADR) removido — ADR-059 já materializado pré-`/run-plan` via delegação `/triage` → `/new-adr`; nota explicativa em § Notas operacionais + atualização de § Verificação end-to-end critérios 3-5 (caminho-único).
- Plano § Verificação manual cenário 4: degradado para "verificação diferida — primeira falha real serve de teste; Claude Code não expõe API para indução controlada" (caminho-único).
- Plano § Resumo da mudança: rebut de `general-purpose` adicionado ao bullet Subagent type + ADR-059 incluído em `**ADRs candidatos:**` (caminho-único).
