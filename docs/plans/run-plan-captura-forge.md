# Plano — `/run-plan §3.5` captura `[capture:backlog]` em modo forge

## Contexto

Gap descoberto durante execução do plano `role-backlog-aceitar-forge` (PR #112 mergeado): escopo era `/run-plan §3.4` (Registro em Concluídos via `**Linha do backlog:**`), §3.5 (Captura automática de imprevistos) ficou de fora. Hoje §3.5 materializa entradas `[capture:backlog]` em `## Próximos` do papel backlog **assumindo arquivo**; em modo forge (`paths.backlog: forge` per ADR-058), `## Próximos` é fonte remota (issues abertas sem assignee), não há arquivo a editar. Skill atual quebra ou silencia capturas backlog quando role está em modo forge.

ADR-058 § (e) **sub-caso editorial** (linhas 77-78) cobre "mutações remotas em superfícies não-primárias" como categoria editorial codificada. 1ª instância nomeada: consolidação do `/triage step 4`. Este plano adiciona `/run-plan §3.5` captura como **2ª instância** da mesma categoria editorial — mas com **forma de cutucada distinta**: batched-com-seleção ao final do plano, não cutucada granular por mutação. Justificativa da divergência codificada em § Resumo da mudança e materializada em ADR-058 § (e) edit.

**Decisão de design (resolvendo tensão com ADR-002 e fadiga de cutucadas múltiplas):** em modo forge, §3.5 **não cutuca na materialização** de cada Task `[capture:backlog]`. Em vez disso, materializa as Tasks como bullets em **seção própria do plano** (`## Capturas backlog em modo forge`) e cutuca uma única vez ao final do gate final com gate batched-com-seleção. Resolve:

- **Tensão com ADR-002:** ADR-002 § Decisão proíbe cutucada na fase pré-loop. Warnings pré-loop classificados como `[capture:backlog]` em modo arquivo são materializados silenciosamente em `## Próximos`. Em modo forge, cutucada batched bate no **done** (gate único editorial paralelo a §3.4), não na fase pré-loop nem na materialização individual. ADR-002 inalterado.
- **Fadiga de N cutucadas:** §3.5 pode acumular múltiplas Tasks (warnings pré-loop + passo 2 + passo 3.2 — até 5+ markers numa execução longa). Gate único `Aplicar todas / Selecionar quais / Manter como pendentes` elimina N cliques sem perder controle granular (operador seleciona subset via Other).
- **Lifecycle 2-estados ADR-049 § Decisão (c):** Task marcada `completed` assim que registrada na seção do plano (signal materializado em local visível); pendingness da decisão de mutação remota migra para arquivo (plano), não Task. Sem estado terceiro "cancelled" introduzido.

**Linha do backlog:** plugin: estender `/run-plan §3.5` captura automática `[capture:backlog]` para modo forge (`paths.backlog: forge`) — atualmente código materializa em `## Próximos` do papel backlog assumindo arquivo; em modo forge, `## Próximos` é fonte remota (issues). Adaptar para criar issue via `gh/glab issue create` com cutucada por mutação (paralelo a /triage step 4 sub-caso editorial per [ADR-058](docs/decisions/ADR-058-role-backlog-aceitar-forge.md) § (e)). Gap descoberto durante execução do plano `role-backlog-aceitar-forge` — escopo era §3.4 (Concluídos via Linha do backlog), não §3.5 captura.

**ADRs candidatos:** ADR-058 § (e) sub-caso editorial (ancestral direto — este plano adiciona 2ª instância com forma de cutucada distinta), ADR-049 § Decisão (c) (Task tool state-keeping — lifecycle 2-estados preservado), ADR-002 (gates pré-loop — inalterado; cutucada batched é no done, não pré-loop), ADR-053 § Decisão (d) (reviewer wiring — inalterado).

## Resumo da mudança

Implementa 2ª instância do sub-caso editorial de ADR-058 § (e) com **forma de cutucada distinta** (batched-com-seleção ao final, não granular por mutação).

**Entra:**

- `/run-plan §3.5` modo forge: materializa Tasks `[capture:backlog]` como bullets em **seção própria do plano corrente** (`## Capturas backlog em modo forge`, criando se não existe). Sem cutucada na materialização individual — paralelo a `[capture:validacao]` que sempre escreve no plano sem cutucada. Task marcada `completed` via `TaskUpdate`.
- **Novo sub-passo ao fim de §3.5** (após materializar `[capture:validacao]` + `[capture:backlog]` no destino correto): se §3.5 desta execução escreveu ≥1 bullet em `## Capturas backlog em modo forge`, disparar cutucada batched `AskUserQuestion` (header `Forge`, opções `Aplicar todas` (Recommended) / `Selecionar quais` (Other) / `Manter como pendentes`). `description` carrega resumo numérico ("N capturas a aplicar como issues no forge").
- **Aplicar todas:** para cada bullet, seguir `forge-auto-detect.md`; criar issue via `gh issue create -t "<linha>" -b "<contexto auto-gerado>"` ou `glab issue create`. Substituir bullet no plano por `- #<número>: <linha>` (ref à issue criada — auditabilidade pós-fact). Policy de erro do caller (per ADR-058 § (d)): `no-detection`/`unsupported-host` → parar com erro explícito (sem aplicar; bullets permanecem como pendentes).
- **Selecionar quais:** operador descreve subset em prosa via Other; criar issues do subset (mesma mecânica de Aplicar todas); restante permanece como bullets `## Capturas backlog em modo forge`.
- **Manter como pendentes:** seção permanece intacta no plano para revisão futura (paralelo semântico a `## Pendências de validação`). Plano arquivado via `/archive-plans` no tempo certo carrega capturas residuais para inspeção.
- ADR-058 § (e) atualizado: 2ª instância nomeada com forma batched-com-seleção (diferente da 1ª instância granular).
- ADR-058 § (g) tabela: linha nova para `/run-plan §3.5` em modo forge.

**Fica de fora (v1):**

- `[capture:validacao]` em modo forge mantém comportamento atual (escreve em `## Pendências de validação` do plano corrente — categoria distinta, mesmo arquivo).
- Cutucada por Task individual descartada per decisão F1+F2 unificada do operador (gate único batched-com-seleção substitui).
- Detecção de bullets pré-existentes em `## Capturas backlog em modo forge` de runs anteriores (improvável; capturas residuais ficam para inspeção manual ou futuro `/curate-backlog`). `§3.5.5` só dispara se **esta execução** escreveu ≥1 bullet.
- Materialização imediata em modo `Falhou` do runbook (per ADR-049 § Decisão (d)): mesmo branch aplica — escrita na seção do plano não bloqueia; cutucada batched fica pulada porque modo runbook usa materialização em §Falhou, não gate final canonical. Tasks vão para a seção do plano + Task completed; operador pode revisar manualmente após Falhou ou em re-execução.

## Arquivos a alterar

### Bloco 1 — `/run-plan` SKILL.md §3.5 + ADR-058 § (e)/(g) {reviewer: code}

- `skills/run-plan/SKILL.md`:
  - **§3.5 "Captura automática de imprevistos"**: dividir em sub-fluxos por marker + modo do role backlog:
    - `[capture:validacao]` → `## Pendências de validação` no plano corrente (inalterado em ambos os modos do backlog — plano é local em `<plans_dir>`).
    - `[capture:backlog]` em **modo arquivo** (canonical/local): escrever em `## Próximos` do papel backlog (comportamento atual preservado). Marcar Task completed.
    - `[capture:backlog]` em **modo forge** (`paths.backlog: forge`, per [ADR-058](../../docs/decisions/ADR-058-role-backlog-aceitar-forge.md)): escrever bullet em **`## Capturas backlog em modo forge`** do plano corrente (criar seção se não existe, append no fim). Sem cutucada na materialização individual — paralelo a `[capture:validacao]`. Marcar Task completed via `TaskUpdate` (signal materializado em local visível; lifecycle 2-estados ADR-049 § Decisão (c) preservado).
  - **Novo sub-passo final do §3.5** (após materializar todas as Tasks): se esta execução escreveu ≥1 bullet em `## Capturas backlog em modo forge` do plano corrente, disparar cutucada batched `AskUserQuestion`:
    - Header `Forge`
    - Opções: `Aplicar todas` (Recommended) / `Selecionar quais` (Other) / `Manter como pendentes`
    - `description` da opção `Aplicar todas`: `"Criar N issues no forge — gh/glab issue create para cada bullet de ## Capturas backlog em modo forge"`. Description das demais carrega trade-off.
  - **Aplicar todas:**
    - Seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`; output `no-detection`/`unsupported-host` → **parar com erro explícito** orientando setup (`gh auth login` / `glab auth login` / `dnf install jq`) ou declarar `paths.backlog: null`/path canonical (policy do caller per ADR-058 § (d)). Bullets permanecem intactos na seção do plano.
    - Para cada bullet na seção `## Capturas backlog em modo forge`: extrair `<linha>` (texto após `- `); montar contexto auto-gerado (template 3 linhas: `Capturado por /run-plan §3.5 do plano <slug>.` + `Origem: <bloco | passo | warning pré-loop conforme rastreável>.` + `Linha: <linha literal>`); executar `gh issue create -t "<linha>" -b "<contexto>" --json number,url` (gh) ou `glab issue create -t "<linha>" -d "<contexto>"` (glab). Substituir bullet no plano por `- #<número>: <linha>` (ref à issue criada). Se nenhum bullet falhou, seção fica com bullets refs-only (auditabilidade pós-fact).
    - Falha em criação remota mid-loop (ex.: rate limit) → parar; reportar quais bullets foram aplicados (refs já substituídos no plano) e quais permanecem pendentes; operador re-invoca ou completa manualmente.
  - **Selecionar quais:**
    - Operador descreve subset em prosa via Other (ex.: "aplicar bullets 1 e 3, manter os outros como pendentes").
    - Aplicar subset com mesma mecânica de Aplicar todas. Bullets restantes ficam intactos como pendentes.
  - **Manter como pendentes:**
    - Seção `## Capturas backlog em modo forge` permanece intacta no plano. Sem criação de issues. Operador endereça depois manualmente ou via futura invocação de `/curate-backlog` (que pode ganhar suporte a essa seção no futuro).
- `docs/decisions/ADR-058-role-backlog-aceitar-forge.md`:
  - **§ (e) sub-caso editorial** (após linha 77-78 que descreve a 1ª instância): adicionar texto sugerido:
    > **2ª instância: `/run-plan §3.5` captura `[capture:backlog]` em modo forge** — Task pendente materializa como bullet em `## Capturas backlog em modo forge` do plano corrente sem cutucada individual; cutucada batched-com-seleção (`Aplicar todas` / `Selecionar quais` / `Manter como pendentes`) ao final de §3.5. Categoria editorial idêntica à 1ª instância (blast radius remoto, policy de cutucada-por-mutação preservada — cada decisão de Aplicar/Manter/Selecionar é confirmação explícita de mutação remota); difere apenas na **forma de apresentação** (gate único batched vs cutucada granular por mutação da 1ª instância). Justificativa da forma distinta: signal `[capture:backlog]` acumula em múltiplos passos do `/run-plan` (warnings pré-loop + passo 2 + passo 3.2 — até 5+ markers); cutucada granular geraria N cliques fadigosos. Variação batched-com-seleção mantém controle granular (Selecionar quais) sem N cutucadas. Mecanismo paralelo a `## Pendências de validação` que também é gate único editorial ao final do plano.
  - **§ (g) tabela** (após linha que lista `/run-plan §3.4`): adicionar linha nova:
    > | `/run-plan §3.5` modo forge | Materializar `[capture:backlog]` | Escrever bullet em `## Capturas backlog em modo forge` do plano corrente; cutucada batched-com-seleção ao final (Aplicar todas / Selecionar quais / Manter como pendentes). Bullets aplicados viram refs `- #<número>: <linha>`. |

## Verificação end-to-end

Critérios objetivos para considerar a mudança válida (inspeção textual; repo sem `make test`).

1. **§3.5 ganha branch para modo forge.** `grep -nE "paths\.backlog.*forge|Em modo \`forge\`|## Capturas backlog em modo forge" skills/run-plan/SKILL.md` retorna ≥2 matches no contexto §3.5.

2. **Materialização em seção própria do plano em modo forge.** `grep -nE "Capturas backlog em modo forge.*plano corrente|escrever bullet em .## Capturas" skills/run-plan/SKILL.md` retorna ≥1 match.

3. **Cutucada batched-com-seleção ao final.** `grep -nE "Aplicar todas.*Selecionar quais.*Manter como pendentes" skills/run-plan/SKILL.md` retorna ≥1 match (no contexto §3.5 final).

4. **Header `Forge` na cutucada batched.** `grep -nE "header.*\`Forge\`" skills/run-plan/SKILL.md` retorna ≥2 matches (linha do §3.4 já existente per ADR-058 + nova linha do §3.5).

5. **Refs substitutos pós-aplicação.** `grep -nE "#<número>: <linha>|bullet.*ref" skills/run-plan/SKILL.md` retorna ≥1 match no contexto §3.5 Aplicar todas.

6. **Policy de erro do caller em §3.5.** `grep -nE "no-detection.*unsupported-host|forge-auto-detect\.md" skills/run-plan/SKILL.md` retorna ≥2 matches (§3.4 pré-existente + §3.5 novo).

7. **ADR-058 § (e) ganha 2ª instância nomeada com forma batched.** `grep -nE "2ª instância:|batched-com-sele[çc][ãa]o" docs/decisions/ADR-058-role-backlog-aceitar-forge.md` retorna ≥1 match no contexto § (e).

8. **ADR-058 § (g) tabela atualizada.** `grep -nE "/run-plan §3\.5.*modo forge|Capturas backlog em modo forge" docs/decisions/ADR-058-role-backlog-aceitar-forge.md` retorna ≥1 match no contexto da tabela § (g).

9. **Anti-regression do modo arquivo (§3.5).** `grep -nE "## Próximos.*papel backlog|backlog.*## Próximos" skills/run-plan/SKILL.md` retorna match — comportamento canonical do §3.5 preservado (escrita em `## Próximos` quando modo arquivo).

10. **Anti-regression do `[capture:validacao]`.** `grep -nE "\[capture:validacao\].*## Pendências de validação" skills/run-plan/SKILL.md` retorna ≥1 match — comportamento da Task `[capture:validacao]` não foi tocado (sempre escreve no plano corrente, independente do modo do backlog).

## Verificação manual

Cenários para o operador exercitar — toca surface não-determinística (mutação remota irreversível + cutucada batched-com-seleção). Operador tem ambiente TJPA real (GitLab) + repo GitHub pessoal.

### Cenário 1 — `/run-plan` em projeto TJPA com 1 captura backlog (golden path batched)

1. Em repo TJPA com `paths.backlog: forge` declarado, criar plano com 1 bloco que dispare 1 captura `[capture:backlog]` durante execução (ex.: finding fora-de-escopo do reviewer).
2. `/run-plan <slug>` executa; passo 2 emite `TaskCreate` com marker `[capture:backlog] <linha>`.
3. §3.5 detecta modo forge → escreve bullet em `## Capturas backlog em modo forge` do plano corrente (cria seção); marca Task completed.
4. Sub-passo final §3.5 dispara cutucada batched `Forge` (`Aplicar todas` / `Selecionar quais` / `Manter como pendentes`).
5. Escolher `Aplicar todas` → 1 issue criada no GitLab; bullet substituído por `- #<N>: <linha>` no plano.
6. Verificar no GitLab UI: title = `<linha>` literal; body = template 3 linhas (plano de origem, origem, linha literal).

### Cenário 2 — Múltiplas capturas com batched-com-seleção

1. Em repo TJPA, plano que dispara 4 capturas `[capture:backlog]` (warning pré-loop + 2 no passo 2 + 1 em validação manual).
2. §3.5 escreve 4 bullets em `## Capturas backlog em modo forge`; 4 Tasks completed.
3. Sub-passo final cutuca batched.
4. Operador escolhe `Selecionar quais` → descreve via Other "aplicar bullets 1, 2, 4; manter o 3 como pendente".
5. 3 issues criadas; bullets 1, 2, 4 viram refs `- #<N>: <linha>`; bullet 3 permanece como bullet original.
6. Plano fica com seção mista (3 refs + 1 bullet pendente).

### Cenário 3 — Manter como pendentes (zero mutação remota)

1. Mesmo setup do Cenário 1 ou 2.
2. Cutucada batched dispara.
3. Escolher `Manter como pendentes` → noop remoto; seção permanece intacta com N bullets originais.
4. Verificar: zero issues criadas no GitLab; plano contém `## Capturas backlog em modo forge` com bullets pendentes para revisão futura.

### Cenário 4 — Modo arquivo preservado (anti-regression)

1. Em repo com `paths.backlog: BACKLOG.md` (canonical) ou `paths.backlog: local`, plano com captura backlog emergente.
2. §3.5 detecta modo arquivo → grava em `## Próximos` (comportamento atual preservado, sem cutucada batched).
3. Verificar arquivo backlog mutado; nenhuma seção `## Capturas backlog em modo forge` criada no plano; nenhuma chamada a `gh/glab issue create`.

### Cenário 5 — CLI ausente / auth ausente (erro explícito em Aplicar)

1. Em ambiente sem `gh`/`glab` no PATH (ou sem auth), `/run-plan` com `[capture:backlog]` emergente em modo forge.
2. §3.5 escreve bullet em `## Capturas backlog em modo forge` normalmente (escrita local não depende de CLI). Task completed.
3. Cutucada batched dispara. Operador escolhe `Aplicar todas`.
4. forge-auto-detect retorna `no-detection`/`unsupported-host` → **parar com erro explícito** orientando setup. Bullets permanecem intactos como pendentes na seção. Zero issues criadas.
5. Reportar erro literal ao operador.

### Cenário 6 — `[capture:validacao]` inalterado em modo forge (anti-regression)

1. Em repo TJPA com `paths.backlog: forge`, plano com `[capture:validacao]` emergente.
2. §3.5 detecta marker `:validacao` → escreve em `## Pendências de validação` do plano corrente.
3. Verificar: arquivo do plano mutado em `## Pendências de validação`; **nenhuma** entrada em `## Capturas backlog em modo forge`; nenhuma issue criada (categoria distinta).

### Cenário 7 — Modo runbook com `Falhou` materializa em modo forge

1. Em repo TJPA com `paths.backlog: forge` e plano `**Modo:** runbook` (per ADR-049 § Decisão (d)) com `[capture:backlog]` emitido durante execução de bloco.
2. Operador escolhe `Falhou — descrever` em bloco posterior.
3. Modo runbook materializa capturas pendentes antes de parar — branch modo forge escreve bullets em `## Capturas backlog em modo forge` do plano runbook (criar seção).
4. Cutucada batched **pulada** em modo runbook (paralelo a §3.5 canonical: gate final não roda em runbook após `Falhou`). Bullets ficam pendentes; operador endereça manualmente.

### Cenário 8 — Falha mid-loop em Aplicar todas (rate limit / network)

1. Plano com 5 bullets em `## Capturas backlog em modo forge`. Operador escolhe `Aplicar todas`.
2. 3 primeiras issues criadas com sucesso (bullets viram refs no plano).
3. 4ª criação falha (rate limit do GitLab, network drop, etc.).
4. Skill para; reporta erro literal + status: "3 bullets aplicados (refs em #<N1>, #<N2>, #<N3>); 2 bullets permanecem pendentes". Operador re-invoca `/run-plan` ou aplica manualmente.

## Notas operacionais

- **ADR-002 preservado por design.** Cutucada batched bate no done (gate único editorial paralelo a §3.4 que também cutuca uma vez no done), **não na fase pré-loop** nem na materialização individual de Task. ADR-002 § Decisão "skill nunca interrompe por cutucada na fase pré-loop" intacto. Tensão potencial (cutucar pós-fact sobre warnings classificados silenciosamente pré-loop) resolvida pela forma da cutucada (batched-com-seleção no done), não pela rebatida textual — pattern editorial menos frágil.
- **Pattern "registrar + batched-com-seleção no done" estabelecido em ADR-058 § (e) variação.** Se 3ª superfície emergir com mesmo perfil (signal acumulado em múltiplos passos), reabrir consolidação editorial (talvez promover para wrapper helper compartilhado entre `/run-plan §3.5` e novas superfícies análogas). Gatilho registrado em ADR-058 § Gatilhos linha 227 (cutucada por mutação irrita power-user) **aplica também aqui**: se ≥3 vezes operador relatar fricção em §3.5 (mesmo com batched), reabrir forma da cutucada.
- **Lifecycle 2-estados ADR-049 § Decisão (c) preservado.** Task marcada `completed` assim que registrada na seção do plano (signal materializado em local visível); pendingness da decisão de mutação remota fica em arquivo (plano), não Task. Sem estado terceiro `cancelled` introduzido. F3 do design-reviewer absorvido por design — pendingness movida para forma editorial (seção do plano), não state de Task.
- **Contexto auto-gerado do body da issue:** template curto (3 linhas: plano de origem, origem do signal, linha literal). Suficiente para auditabilidade post-fact sem template longo decorativo. Operador edita issue depois se quiser.
- **NÃO criar wrapper helper compartilhado** entre §3.4 (close issue granular) e §3.5 (create issue batched-com-seleção) — formas distintas de cutucada justificam código distinto. Reabrir se 3ª superfície emergir com pattern batched-com-seleção (gatilho linha 227 do ADR-058).
- **Validação real exige `paths.backlog: forge` declarado** em consumer real (plugin não declara; mantém modo arquivo). 8 cenários ficam como pendências para dogfood em TJPA + GitHub pessoal — paralelo a `role-backlog-aceitar-forge` (PR #112).
- **ADR-058 Status: Aceito** já promovido em `role-backlog-aceitar-forge` done (PR #112). Este plano ADICIONA conteúdo a § (e) e § (g) sem alterar Status — adendo editorial dentro de ADR Aceito é prática estabelecida do toolkit (paralelo a ADR-005 § Addendum 2026-05-27). Edit direto em prosa de § (e) (vs `## Addendum` separada) é defensável porque substância é refinamento textual mínimo (2ª instância nomeada à categoria editorial já existente).

## Decisões absorvidas

- § Contexto + § Resumo da mudança + § Notas operacionais: F1+F2 unificados pelo operador em decisão criativa "registrar capturas em seção própria do plano + cutucada batched-com-seleção ao final do plano" — resolve tensão com ADR-002 (cutucada no done, não pré-loop) e fadiga de N cutucadas (gate único batched), com lifecycle 2-estados ADR-049 preservado (Task completed ao registrar; pendingness migra para arquivo). F3 (cancelamento mantém Task pending) absorvido por design — pendingness move para forma editorial (seção do plano), não state de Task (caminho-único; estado terceiro `cancelled` não introduzido).
