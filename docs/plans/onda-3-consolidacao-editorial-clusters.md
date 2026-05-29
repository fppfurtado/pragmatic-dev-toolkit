# Plano — Onda 3 da reforma doutrinária: consolidação editorial de 2 clusters densos

## Contexto

Onda 3 da reforma doutrinária codificada em `BACKLOG.md ## Próximos` (commit `4882629`; Ondas 1+2 shippadas — ADR-043 em commit `076354f` + Onda 2 em PR #85).

Consolidação editorial de 2 clusters densos de ADRs sucessores parciais. Cada cluster ganha `## Addendum (2026-05-29)` no ADR foundational servindo como "cluster index" — explica forma do cluster, lista sucessores parciais com cross-refs, aponta procedure files quando aplicável. Bodies dos sucessores intactos. Padrão editorial per [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) § Localização do adendo: as 4 condições aplicam (decisão central intacta, sem categoria nova, sem restrição externa, caráter explicativo).

**Cluster modo local** (4 ADRs): ADR-005 foundational (modo local-gitignored para roles do path contract) + 3 sucessores parciais — ADR-018 (replicação `.claude/` proativa no `/init-config`), ADR-025 (recusar cross-mode `backlog: local + plans_dir: canonical`), ADR-030 (aceitar `CLAUDE.md` gitignored via `.worktreeinclude`). Cross-refs entre eles já existem distribuídos no body de cada ADR; gap concreto: ADR-005 não referencia ADR-030 diretamente. Adendo no foundational fecha o gap + consolida a visão de cluster em 1 entrada de leitura.

**Cluster cutucadas** (2 ADRs + procedure file): ADR-017 foundational (cutucada uniforme em skills para descoberta de configuração ausente) + ADR-029 sucessor parcial (cutucada cobre `CLAUDE.md` ausente). Mecânica canonical hoje em `docs/procedures/cutucada-descoberta.md` (extraída em onda editorial 2026-05-15). Gaps concretos: ADR-017 não referencia ADR-029 (sucessor que cobre o gap documentado em § Limitações linha 81) nem o procedure file (canonical de execução). Adendo no foundational fecha ambos.

**ADRs candidatos:** ADR-005 (foundational modo local; alvo Bloco 1), ADR-017 (foundational cutucadas; alvo Bloco 2), ADR-018/-025/-030 (sucessores parciais modo local; referenciados sem alteração), ADR-029 (sucessor parcial cutucadas; referenciado sem alteração), ADR-043 (raiz doutrinária do plugin; cross-ref de grounding), ADR-034 (critério adendo vs ADR; já satisfeito).

Campo `**Linha do backlog:**` intencionalmente omitido deste plano — umbrella line cobre 4 ondas e Onda 4 ainda pende; matching prematuro pelo `/run-plan §3.4` moveria a umbrella para `## Concluídos`. Justificativa paralela ao plano da Onda 2 (commit `e1428e7`). Detalhamento em § Notas operacionais.

## Resumo da mudança

Para cada cluster, adicionar `## Addendum (2026-05-29)` no ADR foundational com formato uniforme:

- Reconhecimento do cluster como conjunto coordenado (não ADRs isolados).
- Listagem dos sucessores parciais com cross-ref clicável + descrição curta (1-2 sentenças) do que cada um refinou.
- Cross-ref ao procedure file quando aplicável (apenas cluster cutucadas, com `docs/procedures/cutucada-descoberta.md`).
- Cross-ref a ADR-043 (hierarquia doutrinal — Onda 1) para grounding nos fundamentais; ADR-005 e ADR-017 são meta-doutrinais e Ockham operacionalizado endossa ambos (custos do plugin estável; mecânica concreta sustenta operação).

Decisões centrais intactas em todos os ADRs envolvidos. Só estrutura editorial melhora — leitor entra pelo foundational e vê o thread completo sem precisar grep.

## Arquivos a alterar

### Bloco 1 — ADR-005 cluster index (modo local) {reviewer: doc}

- `docs/decisions/ADR-005-modo-local-gitignored-roles.md`: append `## Addendum (2026-05-29)` consolidando cluster modo local. Adendo:
  - Reconhece o cluster como 4 ADRs coordenados (foundational + 3 sucessores parciais).
  - Lista cada sucessor com cross-ref + 1-2 sentenças sobre o que refinou:
    - [ADR-018](ADR-018-replicacao-claude-em-modo-local-init-config.md): replicação proativa de `.claude/` em `.worktreeinclude` pelo `/init-config` step 4.5 quando ≥1 role declarada como `local`. Estendido pelo próprio Addendum (2026-05-27) reconhecendo `/note` como 2º dispatcher.
    - [ADR-025](ADR-025-recusar-cross-mode-backlog-local-init-config.md): recusa mecânica do cross-mode `backlog: local + plans_dir: canonical` no `/init-config` step 3 — leak semanticamente incoerente (texto privado vaza para plano público via `**Linha do backlog:**`).
    - [ADR-030](ADR-030-aceitar-claude-md-gitignored-via-worktreeinclude.md): `/init-config` aceita `CLAUDE.md` gitignored e garante replicação via `.worktreeinclude` step 4.5 cláusula OR — reverte parcialmente extrapolação informal de ADR-016 em step 3.
  - Cross-ref a [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § "Ockham operacionalizado em decisões internas do plugin" reconhecendo grounding do cluster: princípio "simplicidade vence flexibilidade" (declarado literalmente em § Limitações deste ADR e estendido pelos sucessores) é Ockham operacionalizado via os 2 critérios (texto literal de ADR-043 linhas 51-54):
    - **Critério 1** (*"Incidente recorrente ou padrão observado em uso real (não hipótese). Operacionaliza Verdade — empírico vence especulação."*): sinais empíricos do smoke-test PJe 2026-05-11 motivaram ADR-018 (replicação `.claude/`) e ADR-030 (`CLAUDE.md` gitignored).
    - **Critério 2** (*"Fronteira doutrinal borrada — categoria nova com fronteira nítida supera churn de refactor. Operacionaliza Ockham — modelar essa fronteira distingue conceitos que se confundiriam sem ela."*): partição canonical/local em ADR-005 estabeleceu a fronteira; ADR-025 refinou criterion distinguindo direção de leak (cross-mode assimétrico).

### Bloco 2 — ADR-017 cluster index (cutucadas) {reviewer: doc}

- `docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md`: append `## Addendum (2026-05-29)` consolidando cluster cutucadas. Adendo:
  - Reconhece o cluster como 2 ADRs + 1 procedure file coordenados (foundational + sucessor parcial + execução canonical).
  - Lista cada componente com cross-ref + 1-2 sentenças sobre o papel:
    - [ADR-029](ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md): sucessor parcial que cobre o caso `CLAUDE.md` ausente (gap documentado em § Limitações linha 81 deste ADR + § Alternativa (f) descartada). Estende gating de 2 saídas → 3 saídas; string-B nova adaptada ao ausente; dedup por string. Escopo expandido de 4 → 5 skills (ADR-027 introduziu `/draft-idea`).
    - `docs/procedures/cutucada-descoberta.md`: canonical da mecânica de execução (gating tri-state + 2 strings canonical literais + dedup conversation-scoped). Extraído em onda editorial 2026-05-15 das 5 SKILLs consumidoras; CLAUDE.md § "Cutucada de descoberta" trimmed para scope + herança editorial + ref ao procedure. Refactor adicional 2026-05-28 do procedure (tabela declarativa → algoritmo numerado prescritivo per item Concluído em BACKLOG.md).
  - Cross-ref a [ADR-043](ADR-043-hierarquia-doutrinal-fundamentais-raiz.md) § "Ockham operacionalizado em decisões internas do plugin" reconhecendo grounding do cluster: a expansão de gating de 2 → 3 saídas em ADR-029 é Ockham operacionalizado via os 2 critérios (texto literal de ADR-043 linhas 51, 53):
    - **Critério 1** (*"Incidente recorrente ou padrão observado em uso real (não hipótese). Operacionaliza Verdade — empírico vence especulação."*): atrito do PJe 2026-05-11 documentado em ADR-017 § Contexto + projetos novos sem `CLAUDE.md` documentado em ADR-029 § Contexto.
    - **Critério 3** (*"Contradição/refinamento de doutrina existente em ADR/`philosophy.md`/`CLAUDE.md`. Operacionaliza Verdade — corrigir drift entre doutrina vigente e descoberta posterior."*): inversão parcial de Alternativa (f) descartada em ADR-017 § Alternativas, reconhecida explicitamente em ADR-029 § Origem.

## Verificação end-to-end

- Ambos foundationals (ADR-005 e ADR-017) têm nova seção `## Addendum (2026-05-29)` no final do arquivo (antes do EOF).
- Adendo em ADR-005 referencia textualmente ADR-018, ADR-025, ADR-030 (os 3 sucessores parciais do cluster).
- Adendo em ADR-017 referencia textualmente ADR-029 (sucessor parcial) + `docs/procedures/cutucada-descoberta.md` (procedure canonical).
- Ambos adendos referenciam ADR-043 (cross-ref doutrinal).
- Body de ADR-005 e ADR-017 não foi alterado fora do bloco `## Addendum`. Verificação editorial via inspeção visual: `git diff origin/main..HEAD -- docs/decisions/ADR-005-*.md` e análogo para ADR-017; 2 arquivos pequenos doc-only humanamente verificáveis — gate mecânico seria overkill para caminho doc-only.
- Bodies dos sucessores (ADR-018, ADR-025, ADR-029, ADR-030) inalterados — verificação `git diff origin/main..HEAD -- docs/decisions/ADR-{018,025,029,030}-*.md` retorna vazio.

## Notas operacionais

- **Umbrella line da reforma:** linha em `BACKLOG.md ## Próximos` (commit `4882629`, atualizada com Ondas 1+2 shipped) cobre todas as 4 ondas. `**Linha do backlog:**` omitido deste plano para não disparar matching do `/run-plan §3.4` (umbrella moveria para `## Concluídos` antes da Onda 4 finalizar). Operador atualiza a umbrella manualmente após Onda 4 finalizada — ou edita progressivamente para refletir Onda 3 done. Paralelo ao plano da Onda 2 (commit `e1428e7`).

- **Ordem dos blocos:** independentes editorialmente. `/run-plan` pode executar sequencialmente; nenhum bloco depende de outro. Reviewer `doc-reviewer` por bloco audita drift de cross-refs (filenames corretos, seções referenciadas existem, descrições fiéis ao body dos sucessores).

- **Fato editorial — cluster modo local:** cross-refs entre ADRs já existem distribuídos no body de cada ADR:
  - ADR-005 § Limitações → ADR-025 (texto "Estendido por")
  - ADR-005 § Decisão linha 48 → ADR-018 (texto "per ADR-018")
  - ADR-005 § Benefícios → ADR-018 ("estendida pelo Addendum")
  - ADR-018 § Addendum 2026-05-27 → ADR-030, ADR-032
  - ADR-030 § Origem/Contexto → ADR-005, ADR-016, ADR-018, ADR-029
  - **Gap concreto:** ADR-005 não referencia ADR-030 diretamente. Adendo no Bloco 1 fecha esse gap + consolida.

- **Fato editorial — cluster cutucadas:**
  - ADR-017 § Limitações linha 81 documenta o gap (CLAUDE.md ausente)
  - ADR-029 § Origem → ADR-017 (Decisão base + Alternativa (f) descartada)
  - `docs/procedures/cutucada-descoberta.md` extraído das 5 SKILLs consumidoras na onda editorial 2026-05-15 (gating tri-state + 2 strings canonical + dedup conversation-scoped)
  - **Gap concreto:** ADR-017 não referencia ADR-029 (sucessor que cobre o gap documentado) nem o procedure file (canonical de execução). Adendo no Bloco 2 fecha ambos.

- **Status preservation dos sucessores:** ADR-025, ADR-029 e ADR-030 permanecem em status `Proposto` após esta onda. Adendo "cluster index" é caráter explicativo per [ADR-034](../decisions/ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 4 (decisão central intacta, sem categoria nova, sem restrição externa, caráter explicativo); promoção `Proposto → Aceito` é categoria editorial distinta e fora do escopo desta onda. Candidato a item separado de backlog ou onda editorial dedicada futura. Precedente: ADR-005 já cita ADR-025 (Proposto) sem fricção observável (§ Limitações final); pattern foundational-Aceito referenciando sucessor-Proposto é estabelecido no toolkit.

- **Onda 4 (free-read refinement) — próxima:** ADR sucessor parcial de ADR-021 + edit em `agents/design-reviewer.md` ampliando `**ADRs candidatos:**` (ADR-038) como mecanismo de scan-by-default com leitura integral on-demand. Alavanca real de token cost (~50-70% redução estimada vs ~10% das ondas 1-3 sozinhas). Esta Onda 3 não toca esse mecanismo; mantém escopo restrito aos 2 clusters densos.
