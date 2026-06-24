# Plano — session-audit cria issue forge direto para substância cristalizada

## Contexto

`/session-audit` em modo `paths.backlog: forge` sempre defere findings `captura_backlog` para `/triage` (passo 1.5 + passo 6 da `skills/session-audit/SKILL.md`), com a justificativa "duplicar a mecânica de forge quebraria a fronteira editorial". Na prática, quando a substância já está cristalizada, isso cria um passo extra desnecessário (encerrar audit → re-invocar `/triage` → repassar substância), como materializado no incidente `triage-chamado` 2026-06-22 (finding "GLPI_HOST duplicado" exigiu `gh issue create` manual). [ADR-070](../decisions/ADR-070-session-audit-forge-direto-substancia-cristalizada.md) decide discriminar substância cristalizada (criação direta na cutucada batched do passo 5) vs não-cristalizada (defer, status quo).

**ADRs candidatos:** ADR-070 (decisão implementada por este plano), ADR-061 (categoria editorial `/session-audit`, defer-stance refinado), ADR-058 § (e) (policy cutucada por mutação remota; 3ª instância batched), ADR-069 (gate verificar-estado que o caminho direto internaliza).

**Linha do backlog:** #145: feat(session-audit): criar issue no forge diretamente quando substância está cristalizada

## Resumo da mudança

Substituir o defer incondicional de `captura_backlog` em modo forge por uma discriminação cristalizado-vs-defer na `skills/session-audit/SKILL.md`:

- **Entra:** classificação cristalizado/não-cristalizado no passo 1.5; opção de criação direta no forge dentro da cutucada batched do passo 5 (description carrega título + body draft); execução `gh`/`glab issue create` no passo 6 para findings cristalizados, com o gate de ADR-069 internalizado antes da criação para capturas NOTES-sourced; bullet em `CLAUDE.md` § Editing conventions.
- **Fica de fora:** extração de procedure dedicada para criação forge (YAGNI — comando único; `forge-auto-detect.md` já é o procedure compartilhado); mudança no caminho de defer (preservado integralmente para substância não-cristalizada).
- **Decisão-chave (per ADR-070):** default-conservador — ambíguo → não-cristalizado → defer (`/triage` como rede a jusante). Criação direta só dispara quando a skill tem confiança de cristalização; cutucada de confirmação contém o blast radius (policy de ADR-058 § (e) preservada).

## Arquivos a alterar

### Bloco 1 — discriminação cristalizado/defer na session-audit {reviewer: prompt}

- `skills/session-audit/SKILL.md` passo 1.5 (linha ~33): substituir o defer incondicional por classificação. Em modo `forge`, classificar cada finding `captura_backlog` em **cristalizado** (`ação_sugerida_prosa_curta` já contém título + contexto suficientes para issue como-está, sem bifurcação de escopo/arquitetura nem decomposição) → criação direta no forge na cutucada batched do passo 5; **não-cristalizado** (vago, abre bifurcação, ou requer decisão de `/triage`) → defer pra `/triage` com nota informativa (status quo). Default-conservador explícito: ambíguo → não-cristalizado → defer. Remover/reescrever a frase "Skill **não** propõe `gh issue create` / `glab issue create` direto — duplicar quebraria a fronteira editorial" para refletir que a fronteira é preservada pela cutucada de confirmação, não pelo defer (per ADR-070 § Decisão).
- `skills/session-audit/SKILL.md` passo 5 (cutucada batched, linhas ~109-114): integrar a criação direta às opções condicionais existentes (que já variam 3↔4 opções per ADR-064). **Forma da enum (per ADR-058 § (e), crítica):** a criação forge é mutação remota irreversível e **não pode ser absorvida** no `Aplicar tudo` genérico que cobre edits locais reversíveis (NOTES/doutrina) — isso agruparia decisão irreversível com reversíveis num clique, exatamente o que ADR-058 § (e) recusa. Quando há ≥1 finding `captura_backlog` cristalizado forge, a criação direta entra como **opção(ões) distinta(s) com confirmação própria** (forma batched-com-seleção paralela a `/run-plan §3.5` — `Aplicar todas as criações forge` / `Selecionar quais` / `Manter como defer`), separada do gate de edits locais. A `description` de cada opção de criação carrega a operação concreta `gh issue create -t "<título>" -b "<body draft>"` para revisão pré-confirmação (paralelo a ADR-058 § (e): description carrega a operação concreta). Preservar a composição com a 4ª opção `Executar [executável] também` (ADR-064) — as três famílias de opção (edits locais / criações forge / executáveis) compõem sem conflito porque cada uma é gate próprio; nenhuma absorve mutação remota.
- `skills/session-audit/SKILL.md` passo 6 (linha ~121): substituir `captura_backlog em modo forge: defer pra /triage` por dois ramos. **Cristalizado:** internalizar o gate de [ADR-069](../decisions/ADR-069-gate-verificacao-estado-antes-materializar-captura-notes.md) — se a `citação_transcript` aponta para entry pré-existente do `.claude/local/NOTES.md`, aplicar `verify-state-before-materialize.md` **antes** do `issue create`: já-resolvido → baixa via append no NOTES.md + pular criação (reportar no done); pendente/indeterminado → segue. Substância fresca da sessão → sem gate. Depois, criar via `gh issue create -t "<título>" -b "<body draft>" --json number,url` (gh) ou `glab issue create -t -d` (glab), seguindo `forge-auto-detect.md`. **Salvaguarda worktree-probe não aplica neste ramo forge** (per [ADR-058](../decisions/ADR-058-role-backlog-aceitar-forge.md) § (g) — mutação remota idempotente, sem arquivo local concorrente; a razão da probe é concorrência sobre `BACKLOG.md`); a probe permanece só no ramo modo-arquivo (linha 120). **Não-cristalizado:** defer pra `/triage` (preserva o texto atual da linha 121, incluindo a nota sobre dependência do wiring de `/triage` passo 4 para o caso deferido).
- `skills/session-audit/SKILL.md` § O que NÃO fazer: adicionar guarda "Não criar issue forge para substância **não-cristalizada** — default-conservador defere pra `/triage`; criação direta só para finding cujo `ação_sugerida_prosa_curta` já carrega título+contexto suficientes (per ADR-070 § Decisão § default-conservador)". Guarda documenta o anti-padrão não-óbvio (over-creation de issue-fantasma que `/triage` teria refinado).

### Bloco 2 — atualizar docs canonical (procedure + CLAUDE.md) {reviewer: doc}

- `docs/procedures/verify-state-before-materialize.md` §6 (linha ~57): corrigir o drift doc↔doc. O texto atual afirma *"Modo forge: `captura_backlog` já é deferido a `/triage` (step 1.5) — o gate aplica lá"* — falso após este plano. Reescrever para discriminar: ramo **cristalizado** internaliza o gate localmente na `/session-audit` passo 6 antes do `issue create`; ramo **não-cristalizado** continua deferindo ao `/triage` (gate aplica lá). Verificar §1 também por afirmação correlata de "forge sempre defere".
- `CLAUDE.md` § Editing conventions: adicionar bullet referenciando ADR-070 (discriminação cristalizado-vs-defer em `/session-audit` modo forge; criação direta na cutucada batched do passo 5 como opção distinta per ADR-058 § (e); gate ADR-069 internalizado no caminho direto; 3ª instância batched de ADR-058 § (e); 8ª aplicação da onda Override N=3 + débito de meta-avaliação registrado). Seguir o gabarito sintático dos bullets-irmãos (ADR-067/-069).

## Verificação end-to-end

Projeto sem suite de testes (markdown) — inspeção textual:

1. (negativo) `grep -c "não.*propõe.*gh issue create\|quebraria a fronteira editorial" skills/session-audit/SKILL.md` retorna 0 (frase do defer incondicional removida/reescrita); **e** (positivo) `grep -n "fronteira.*preservada.*cutucada\|cutucada de confirmação" skills/session-audit/SKILL.md` retorna match no passo 1.5 (reescrita materializou a semântica nova, não só removeu a antiga).
2. `grep -n "cristaliz" skills/session-audit/SKILL.md` retorna matches no passo 1.5, passo 5, passo 6 e § O que NÃO fazer (discriminação presente nos 4 sites).
3. `grep -n "issue create" skills/session-audit/SKILL.md` retorna match no passo 6 (criação direta do ramo cristalizado).
4. `grep -n "verify-state-before-materialize\|ADR-069" skills/session-audit/SKILL.md` retorna match no passo 6 ramo cristalizado (gate internalizado).
5. `grep -n "ADR-070" CLAUDE.md` retorna o bullet novo em § Editing conventions.
6. Ler o passo 5 e confirmar que a composição com a 4ª opção `Executar [executável] também` (ADR-064) permanece coerente — opções condicionais não se contradizem; criação forge é opção distinta, não absorvida no `Aplicar tudo`.
7. `grep -n "internaliza\|cristalizado" docs/procedures/verify-state-before-materialize.md` retorna match no §6 (drift doc↔doc corrigido — não afirma mais "forge já é deferido a /triage" incondicionalmente).

## Verificação manual

Superfície não-determinística (criação forge + discriminação heurística por LLM). Cenários enumerados pós-`/reload-plugins` em sessão CC com `paths.backlog: forge` ativo:

**Forma do dado real** (exemplos de `ação_sugerida_prosa_curta`):
- Cristalizado: `"GLPI_HOST duplicado em config_a.py e config_b.py — consolidar numa fonte única"` (título + contexto suficientes, sem bifurcação).
- Não-cristalizado: `"revisar arquitetura de configuração do projeto"` (vago, abre bifurcação de escopo).

**Cenários:**

- **C1 — cristalizado cria direto:** sessão gera finding cristalizado (exemplo acima); `/session-audit` → cutucada batched oferece opção de criação direta com título+body draft na `description`; `Aplicar` → `gh issue create` executa; issue aparece no forge. Issue de teste descartável (title prefixado `[dogfood] DELETE ME`); fechar manual após.
- **C2 — não-cristalizado defere:** finding vago (exemplo acima) → cutucada **não** oferece criação direta para ele; defer pra `/triage` com nota informativa.
- **C3 — ambíguo → default-conservador:** finding na fronteira (título plausível mas escopo incerto) → tratado como não-cristalizado → defer (não cria).
- **C4 — cristalizado NOTES-sourced + gate ADR-069:** finding cristalizado cuja `citação_transcript` aponta para entry pré-existente do NOTES.md → gate verificar-estado roda antes da criação; (a) artefato já-resolvido → baixa via append no NOTES.md + criação pulada (reportado no done); (b) pendente → criação segue.
- **C5 — modo arquivo inalterado:** repo com `paths.backlog` canonical/local → passo 6 segue o ramo modo-arquivo existente (sem criação forge); comportamento pré-ADR-070 preservado.
- **C6 — composição com ADR-064:** sessão com ≥1 cenário [executável] (ADR-064) **e** ≥1 finding cristalizado forge → cutucada batched apresenta ambos sem conflito; operador escolhe subset via Other.

## Pendências de validação

- `[capture:validacao]` Smoke comportamental C1-C6 pós-`/reload-plugins` em sessão CC real com `paths.backlog: forge` — exige forge real (gh/glab) + julgamento LLM sobre transcript; não exercitável na execução do `/run-plan` (depende do plugin recarregado + estado de sessão controlado). Operador roda manual; promover ADR-070 `Proposto` → `Aceito (YYYY-MM-DD)` após ≥1 invocação real bem-sucedida do caminho cristalizado.

## Decisões absorvidas

- Bloco 1 passo 6 (composição ADR-069): caminho de criação direta **internaliza** o gate verificar-estado localmente (responsabilidade que o defer delegava ao `/triage`); caminho de defer preserva a delegação (caminho-único).
- Bloco 1 passo 5 (forma da enum, ADR-058 § (e)): criação forge é opção distinta com confirmação própria, não absorvida no `Aplicar tudo` de edits locais reversíveis (caminho-único).
- Bloco 1 passo 6 (worktree-probe): cláusula explícita de que a probe não aplica no ramo forge per ADR-058 § (g) (caminho-único).
- Bloco 2 (drift doc↔doc): `verify-state-before-materialize.md` §6 adicionado aos arquivos a alterar — afirmava "forge já é deferido a /triage" incondicionalmente, falso após o plano (caminho-único).
- Verificação end-to-end crit 1: complementado com grep positivo da semântica nova, além do negativo da frase antiga (caminho-único).
