# ADR-022: Política de archival para docs/plans/

**Data:** 2026-05-12
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-014](ADR-014-inventario-editorial-main-unico.md) — manter main único com inventário editorial público. Gatilho § "Gatilhos de revisão" #4: *"`docs/plans/` ultrapassar 100 arquivos sem rotação — gestão editorial fica difícil; reabrir para considerar arquivamento (mover para tag/release archive) ou refatoração estrutural."*
- **Decisão base:** [ADR-004](ADR-004-state-tracking-em-git.md) — state-tracking em git/forge; pipeline canonical `**Linha do backlog:**` no plano → matching textual em `/run-plan §3.4`. Archival precisa preservar esse pipeline.
- **Investigação:** Auditoria arquitetural 2026-05-12 (`docs/audits/runs/2026-05-12-architecture-logic.md`, achado E2 + proposta E_arch). Hoje ~55 planos em `docs/plans/`. Ritmo recente do refactor sweep sugere atingir 100 em ~5 dias se mantido. Reabertura **preventiva**.
- **Calibração inicial:** N=2 semanas (era N=4 candidato no draft). Calibrado para 2 semanas em 2026-05-12 pelo operador antes do primeiro uso real — exercício antecipado do gatilho de revisão #1 (§ Gatilhos), consistente com a natureza heurística do parâmetro reconhecida em § Trade-offs.

## Contexto

`docs/plans/` cresce monotonicamente — cada `/triage` caminho-com-plano produz um plano que fica no diretório após shipping. ADR-014 manteve esse padrão deliberadamente:

- **Transparência editorial** preservada (visitor do repo vê histórico de decisões + planos).
- **Demonstração viva** do workflow que o plugin codifica.
- Refatoração estrutural (branch dev, repo separado, orphan publish, filter-repo) descartada por custo desproporcional.

ADR-014 § Trade-offs aceitou: *"Consumer clone arrasta inventário editorial (~600 KB de working tree). Aceito enquanto for ~1 MB; reabrir se cair em ordem de grandeza superior."* E gatilho explícito: *"`docs/plans/` ultrapassar 100 arquivos sem rotação → considerar arquivamento."*

A "rotação" não foi definida em ADR-014 — apenas anunciada como gatilho. **ADR-022 define-a.**

**Restrições editoriais:**

- **Não-destrutivo.** ADR-014 doutrina: inventário editorial permanece em main. Archival move arquivos, não apaga. `git log --follow` preserva archeology.
- **Reversível.** Operador pode mover plano arquivado de volta se referência ativa emergir.
- **Pipeline `**Linha do backlog:**`** preservado. Plano arquivado mantém o campo; matching textual com BACKLOG `## Concluídos` continua funcional para archeology no diretório `archive/`.

**Trigger natural escolhido** (decidido em `/triage` que originou este ADR): `/triage` é frequente; archival é raro → ruído cumulativo se for sub-passo. `/release` tem cadência irregular que não vincula bem ao ritmo temporal de archival. **Skill dedicada `/archive-plans`** é invocação sob demanda quando operador decide.

## Decisão

**Cria-se a skill `/archive-plans` para archival editorial periódico de planos em `docs/plans/`. Plano elegível move para `docs/plans/archive/<YYYY-Qx>/<slug>.md` via `git mv`. Mecanismo é determinístico, não-destrutivo, sob demanda, com preview obrigatório antes da execução.**

### Critérios cumulativos de elegibilidade

Plano em `docs/plans/<slug>.md` (não em `archive/`) é **elegível** quando satisfaz **todos os 6** critérios:

1. **Tem `**Linha do backlog:**`** no `## Contexto`. Sem o campo → não-elegível (skill reporta; archival manual).
2. **Linha matchável no `BACKLOG.md`** (matching textual exato em qualquer seção). Linha não localizada → editorial: `not eligible: <slug>.md — **Linha do backlog:** não localizada em BACKLOG.md; verificar matching`.
3. **Linha está em `## Concluídos`, não em `## Próximos`.** Linha em Próximos → **silente** (item não terminou; sem ruído no relatório).
4. **Linha entrou em Concluídos há ≥ N semanas.** Datação via **pickaxe** — `git log -S "<texto-da-linha>" --diff-filter=A --reverse BACKLOG.md | head -1` → primeiro commit que **adicionou** o texto exato (independente de reedições in-place posteriores). **N=2 semanas** (calibração inicial — ver § Origem; era N=4 candidato no draft).
5. **Sem worktree ativa nem órfã do slug:** `git worktree list --porcelain` não inclui `.worktrees/<slug>` **E** `test -d .worktrees/<slug>` falha (probe orphan — failure mode coberto também pela precondição 4 do `/run-plan`).
6. **Sem PR aberto referenciando o slug:** auto-detect forge — `gh pr list --search <slug>` (GitHub) ou `glab mr list --search <slug>` (GitLab regex `^gitlab\.`). **Forge inacessível** (CLI ausente, host não-mapeado) → plano **não-elegível nesta invocação** com mensagem `degraded: <slug>.md — forge inacessível; not eligible this run, retry após restaurar gh/glab`. **Não** assume seguro: vetor do risco é arquivar plano com PR aberto durante trabalho em curso.

Tabela de comportamento por critério falho:

| Critério falho | Categoria | Mensagem |
|---|---|---|
| (1) | Editorial | `not eligible: <slug>.md — sem **Linha do backlog:**; archival manual` |
| (2) | Editorial | `not eligible: <slug>.md — **Linha do backlog:** não localizada; verificar matching` |
| (3) — linha em Próximos | Silente | (item não terminou; sem reporte) |
| (4) — idade < N | Silente | (não reporta cada plano não-elegível por idade; conta no resumo final) |
| (5) — worktree ativa | Aviso | `not eligible: <slug>.md — worktree em .worktrees/<slug> (registrada/órfã); trabalho em curso` |
| (6) — PR aberto | Aviso | `not eligible: <slug>.md — PR/MR aberto referenciando <slug>; trabalho em curso` |
| (6) — forge inacessível | Degraded | `degraded: <slug>.md — forge inacessível; not eligible this run` |

Critério (3) tem semântica de **gate temporal** (item ainda não terminou; silente porque não há decisão a tomar). Critérios (5)/(6) têm semântica de **gate de segurança** (trabalho em curso; aviso para operador notar). Diferença deliberada — registrada aqui em vez de fingir uniformidade.

### Layout do archive

Plano elegível move para `docs/plans/archive/<YYYY-Qx>/<slug>.md`, onde:

- `YYYY` = ano de entrada da linha em Concluídos (extraído do commit identificado pelo critério 4).
- `Qx` = quarter calendar (`Q1` Jan-Mar; `Q2` Abr-Jun; `Q3` Jul-Set; `Q4` Out-Dez).

Granularidade por quarter porque: (i) ano-only acumula demais; (ii) mês-only fragmenta excessivamente; (iii) ciclo natural de projeto open-source toolkit alinha mais com quarter que com mês ou ano. Diretório `docs/plans/archive/<YYYY-Qx>/` criado automaticamente quando primeiro archival do quarter ocorre.

### Operação com preview obrigatório

`/archive-plans` é skill rara invocada sob demanda; operação resulta em `git mv` + commit. **Toda invocação é preview-first** — sem flag `--dry-run` separada porque o default já é preview, e a natureza low-frequency da skill não justifica o atalho de aplicação direta.

Fluxo:

1. **Coletar** todos os planos em `docs/plans/<slug>.md` (não em `archive/`); para cada um, avaliar os 6 critérios.
2. **Detectar cross-refs** para cada elegível: `grep -rn "docs/plans/<slug>.md" docs/decisions/` — lista links em prosa de ADRs (incluindo `## Implementação` e referências cruzadas).
3. **Apresentar preview** ao operador em formato estruturado:
   - Lista de **elegíveis** com destino: `<slug>.md → archive/<YYYY-Qx>/`.
   - Lista de **cross-refs detectados** por plano elegível (incluindo ADR-NNN:linha:trecho) — sinal para operador decidir se atualiza ADRs antes do archival ou aceita link relativo quebrado.
   - Lista de **não-elegíveis** com mensagem por categoria (editorial, aviso, degraded — silentes omitidos).
   - Resumo: `N planos elegíveis; M cross-refs detectados; K não-elegíveis (categoria)`.
4. **Gate via `AskUserQuestion`** (header `Archive`, opções `Aplicar` / `Cancelar`).
   - `Aplicar` → executa archival; mensagem do commit lista os planos arquivados.
   - `Cancelar` → abort silente; nada para reverter (nenhum `git mv` aconteceu).
5. **Aplicar:** para cada elegível, `mkdir -p docs/plans/archive/<YYYY-Qx>/` + `git mv docs/plans/<slug>.md docs/plans/archive/<YYYY-Qx>/<slug>.md`. Commit unificado:

```
chore: archive <N> historical plans

archive/<YYYY-Qx>/<slug-1>.md
archive/<YYYY-Qx>/<slug-2>.md
...
```

Skill **não pusha** — segue convenção `/release` (operação visível ao restante do sistema é decisão deliberada do operador).

### Sub-fluxo: des-arquivar (rara)

Operador querendo retomar plano arquivado: `git mv docs/plans/archive/<YYYY-Qx>/<slug>.md docs/plans/<slug>.md`. **Sem comando dedicado na skill** (YAGNI até reverter virar recorrente).

## Consequências

### Benefícios

- **`docs/plans/` enxuto** para descoberta — visitor do repo vê planos ativos/recentes; archeology preservada em `archive/`.
- **Archeology completa.** `git log --follow docs/plans/archive/<YYYY-Qx>/<slug>.md` segue histórico do plano desde criação.
- **Critério mecânico testável.** 6 critérios cumulativos paralelos a ADR-013 e ADR-020; skill author/contribuidor classifica candidato sem reabrir ADR.
- **Preview-first elimina classe de erro irreversível-ish.** Operador vê cross-refs e elegibilidades antes do `git mv`, decide com input completo. Mesmo pattern de `/release §4 Aplicar/Editar/Cancelar`.
- **Não-destrutivo + non-temático.** Sem `filter-repo`, sem reescrita de history. Compatível com ADR-014 doutrina.
- **Skill dedicada minimiza ruído.** Invocada quando operador quer; outras skills (frequentes) ficam intactas.
- **Pipeline ADR-004 preservado.** `**Linha do backlog:**` continua funcional para archeology no plano arquivado.

### Trade-offs

- **+1 skill no plugin** (8 → 9). Custo de manutenção marginal; superfície semelhante a `/release` (operação periódica do mantenedor, baixa frequência).
- **N=2 semanas é heurística com observabilidade pior que N=15 do ADR-021.** ADR-021 N=15 erra para baixo/alto e operador detecta na invocação do reviewer (loop frequente). ADR-022 N=2 semanas erra para baixo arquivando plano ativo — só detectado quando operador ou cross-ref tenta achar o plano e falha. **Preview-first mitiga** (operador vê lista antes do `git mv`); gatilho de revisão registra incidentes pós-fato. Trade-off explícito: assimetria de observabilidade reconhecida; preview cobre o gap sem instrumentação automatizada.
- **Granularidade YYYY-Qx é heurística.** Vincula ao calendário, não ao ritmo de release (irregular no plugin). Plugin sem cadência fixa pode ter quarters com 0 archivals (diretório vazio nunca criado — sem dano). Aceito.
- **Detecção de PR via forge auto-detect** herda fragilidade de `/run-plan §3.7` / `/release §5` (CLI ausente → degradação por plano específico, **não** assume seguro). Plano fica em `docs/plans/` até forge voltar.
- **Datação via `git log -S` pickaxe** captura primeiro commit que **adicionou** o texto, robusto a reedições in-place pós-Concluído (typo fix, reword cosmético). Frágil apenas a `filter-repo` retroativo — não previsto por ADR-014.
- **Cross-refs em ADRs `## Implementação`** entram no **preview** como informação ao operador (não bloqueia, não passa silente). Autor pode aceitar link relativo quebrado deliberadamente (referência a estado histórico); bloqueio forçaria edição em massa de ADRs com cross-ref histórico. Preview delega a decisão sem prescrever.

### Limitações

- ADR cobre apenas `docs/plans/`. `docs/audits/runs/` (auditoria reuses) e `docs/decisions/archive/` (hipotético) não têm política análoga; volume baixo hoje, sem urgência.
- **Reversão tardia trivial mas manual.** Sem comando dedicado; operador roda `git mv` na mão. YAGNI até reverter virar recorrente.
- **Quarter cross-month não distinguido intra-quarter.** Plano arquivado em janeiro de Q1 e plano de março de Q1 ficam no mesmo diretório. Ordem cronológica perdida intra-quarter; aceito (granularidade do quarter é o ponto).
- **Pickaxe não pega edição que move o texto entre seções** sem mudar caracteres (raro mas possível: linha movida de Próximos para Concluídos sem reformatar). Datação aponta entrada original — pode ser anterior ao Concluído. Mitigação: cruzar com `git log -G "## Concluídos" ...` é mais robusto mas custoso; aceito como aproximação na primeira iteração.

## Alternativas consideradas

### (a) Sub-passo de `/triage §0` cleanup

Archival roda toda vez que `/triage` executa, detectando planos elegíveis.

Descartada:
- `/triage` é frequente; archival é raro. Verificar elegibilidade a cada `/triage` adiciona overhead a 99% das invocações.
- `/triage §0` hoje é cleanup git (worktrees mergeadas). Misturar archival de plans é mistura de eixos operacionais distintos.

### (c) Comando manual + receita em `docs/install.md`

Operador roda script bash manualmente.

Descartada:
- Viola filosofia do plugin (mecânica > prosa).
- Sem padronização; cada operador implementaria diferente.
- Comando manual vira tabela de patches infinitos.

### (d) Gesto do `/release`

`/release` dispara archival no final do fluxo: planos cujo Concluído entrou no ciclo da release são arquivados.

Descartada:
- `/release` ganha responsabilidade nova além de version+changelog+tag.
- Archival temporal vincula ao ritmo de release; quando releases são irregulares, archival fica intermitente.
- Acoplamento entre archival e cadência de release que nem sempre se alinham.

### (e) Sub-passo de `/next` após varredura

`/next` varre BACKLOG + pendências de validação; adicionar varredura de planos arquiváveis.

Descartada:
- `/next` é orientação de sessão (top 3 candidatos). Archival mid-flow distrai.
- `/next §6` cobre cleanup de BACKLOG (movimentar item entre seções), mas o pattern é diferente de archival de arquivos.

### (f) Sem archival; aumentar limiar de ADR-014

Aumentar gatilho de ≥100 para ≥500 e adiar decisão.

Descartada:
- ADR-014 gatilho foi calibrado por escala de manutenção (≥100 = "difícil de descobrir/navegar"); aumentar é negar o problema.
- Ritmo recente (~refactor sweep) torna ≥500 atingível em janelas; sucessor já se justifica preventivamente.

### (g) Threshold de ativação no `/archive-plans`

Skill faz no-op até `#planos em docs/plans/ ≥ M` (M candidato: 50).

Descartada nesta iteração:
- Skill é invocada sob demanda; operador já decide quando rodar. Adicionar threshold interno cria caso edge "rodei e nada aconteceu, qual o limite?" que confunde.
- Reabrir se operador reportar atrito (e.g., rodou e foi surpreso por archival agressivo em projeto pequeno).

### (h) Layout por release tag em vez de quarter

`docs/plans/archive/<tag>/<slug>.md` (ex.: `archive/v2.4.0/`, `archive/v2.5.0/`).

Descartada:
- **Vincula ao ritmo de release** (rejeitado em (d) por irregularidade). Plugin com refactor sweep rápido teria múltiplas releases em mesma semana; archival vincularia a microtags.
- **Granularidade variável.** Release com 1 plano arquivado e release com 30 planos ficam no mesmo nível hierárquico — quarter dá granularidade temporal previsível.
- **ADR-014** menciona "tag/release archive" como exemplo de rotação; ADR-022 escolhe **calendar quarter** como concretização porque tempo é dimensão estável (release é variável).
- Reabrir se ritmo de release estabilizar (e.g., mensal regular) e quarter virar grosseiro demais.

## Gatilhos de revisão

- **N=2 semanas mal-calibrado** (mecanismo arquiva cedo demais OU plano ativo é arquivado por confusão) — ajustar; primeira evidência empírica vem do primeiro `/archive-plans` no plugin.
- **Plano arquivado por erro 2+ vezes** apesar do preview — sinal de que preview é insuficientemente informativo; reabrir formato (mais cross-refs? mostrar última modificação do arquivo do plano?).
- **Cross-refs quebrados em ADRs `## Implementação`** após archival recorrente E operador reclama — sinal de que preview-first delega decisão demais. Considerar `--strict` flag que bloqueia archival quando cross-ref encontrado.
- **`docs/plans/archive/<YYYY-Qx>/` ficar grande demais** (> 50 planos por quarter) — granularidade quarter insuficiente; considerar mês ou layout (h) por release tag se cadência estabilizar.
- **Operador rodar `/archive-plans` < 1× por ano** — sinal de under-use; archival não atrai atenção. Considerar nudge editorial em `/release` (gesto opcional, não obrigatório).
- **Plano arquivado precisa ser des-arquivado >1× em janela curta** — sinal de critério inadequado; reabrir.
- **Consumer externo adota workflow muito diferente** (releases mensais com many planos por release) — N=2 semanas pode ser confuso. Considerar threshold custom via path contract.
- **Volume de `docs/plans/archive/`** crescer ao ponto de exigir sub-rotação (archive de archive) — extremo; revisitar layout.
- **Forge-degraded recorrente** (plano fica não-elegível 3+ invocações seguidas por forge inacessível) — sinal de que detecção de PR precisa fallback robusto. Considerar dispensar critério (6) se forge não-mapeado é o pattern do consumer.
- **Pickaxe falha** (linha movida sem reformatar Próximos → Concluídos sem alterar caracteres) — promover datação para cruzamento com `git log -G "## Concluídos"`.
