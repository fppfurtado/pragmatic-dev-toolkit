# Plano — Onda K: auditoria do inventário 27 vigentes pré-migração

## Contexto

Pós-Onda J encerrou 10 ondas shippadas da redesign (A-J + ADR-052 + Onda Promoção). Saldo: **27 ADRs vigentes** (54 criados - 27 archived). Target charter original 13-15; trajetória pós-Onda J projetada em "~3-5 ondas adicionais" (charter § Cap de ondas linha 188; BACKLOG umbrella linha 5; NOTES `tres-principios-4` § Candidatos K).

Charter § Cap de ondas marca a projeção como **"sujeito a re-auditoria do inventário 27 vigentes"** (texto literal); NOTES `tres-principios-4` § Como retomar item 2 recomenda re-auditoria explicitamente como passo 1 antes de Onda K. Candidatos K-X listados top-of-mind (discoverability/branding ADR-037+?, brainstorm standalone ADR-036, apex meta-cluster opcional) cobrem ~14 ADRs explicitamente — restam ~13 vigentes sem candidato declarado, em estado de assumption-not-evidence.

**Inversão do ônus da prova:** charter foi refinado incrementalmente (Onda C calibrou target 11 → 13-15; Onda F+G+H estabeleceram modos editoriais formalizados em ADR-052; Onda I aplicou modos formalmente; Onda J validou sketch literal sem aplicação formal). Cada onda contribuiu refinamento empírico. Onda K direta sem auditoria assumiria que NOTES top-of-mind cobre os remanescentes — pode errar cluster ou deixar órfãos. Auditoria substitui assumption por evidência mecânica (`ls docs/decisions/ADR-*.md` + mapeamento mecânico a candidatos K-X).

**Bifurcação resolvida no `/triage`:** (a) Re-auditoria primeiro vs (b) Cluster direto (b1 discoverability+? / b2 brainstorm standalone / b3 apex meta-cluster). Operador escolheu (a) — base empírica antes de decisão de cluster. Esta onda produz auditoria + projeção recalibrada; cluster Onda L downstream emerge como `/triage` subsequente.

**Linha do backlog:** plugin: **redesign da camada doutrinal** — consolidar 45 ADRs em ~10-12 temáticos sob hierarquia invertida pós-v2.14.0 + condensar `philosophy.md` (princípios + mapping operacional + ≥3 pattern como condição geral de YAGNI terminar; cortar § Codificação estrutural overhead) + codificar **política de admissão going forward** (*"isto é decisão reversível ou entendimento estabilizado?"*) como mecanismo de prevenção de re-acúmulo.

**ADRs candidatos:** ADR-045 (apex redesign + admission policy + fronteira "ajuste editorial vs revisão" — autoriza esta onda como categoria editorial livre vs revisão estrutural); ADR-052 (3 modos editoriais a/b/c com critério mecânico verificável — informa decisão de cluster downstream); ADR-048 (always-include hardcoded `[ADR-009, ADR-034, ADR-043]` — constraint para futura aplicação de modo (c)); ADR-053 (template Onda I — primeira aplicação formal modos a+c); ADR-054 (template Onda J calibração mínima sem aplicação formal).

## Resumo da mudança

Auditoria estruturada do inventário 27 ADRs vigentes pós-Onda J. Decomposta em **3 blocos**: 1 bloco de análise estruturada (cobrindo as 3 sub-análises 1-3) + 2 blocos de edits editoriais (4-5):

1. **Listar 27 vigentes mecanicamente** via `ls docs/decisions/ADR-*.md` + cross-check contra `docs/decisions/archive/README.md`.
2. **Mapear cada vigente a candidato K-X** declarado em charter/NOTES; identificar órfãos (sem candidato listado).
3. **Identificar agrupamentos semânticos novos** ocultos em órfãos (clusters não-listados que ≥2 órfãos coesionam).
4. **Refinar charter § Cap de ondas + § Atualização pós-execução** com saldo da auditoria (lista exaustiva + cluster sequence recalibrada — incluindo **Onda K' editorial canonical templates** promovida via cutucada resolvida desta `/triage` — + projeção empírica de ondas restantes).
5. **Atualizar BACKLOG umbrella linha 5** com saldo da Onda K + cluster sequence atualizada (K → K' → L) + recommendation de cluster Onda L downstream.

**Não-escopo desta onda:**
- Decisão final de cluster Onda L (auditoria produz recomendação; `/triage` subsequente confirma).
- Criação de ADR consolidado ou migração de cluster (cada cluster é onda própria downstream).
- Refinamento de `templates/plan.md` § Verificação end-to-end (escopo da **Onda K' editorial canonical templates** promovida via cutucada resolvida desta `/triage` — tactical-only paralela, precede Onda L cluster).
- Apex meta-cluster (NOTES `tres-principios-4` marca "risco alto auto-referência"; auditoria pode confirmar skip definitivo).

## Arquivos a alterar

### Bloco 1 — Auditoria do inventário vigente {reviewer: doc}

Bloco de **análise estruturada** (não-edit) cujo output materializa em (a) prosa estruturada no commit message + plano `## Decisões absorvidas`, OU (b) captura via TaskCreate `[capture:auditoria]` materializada em §3.5 do `/run-plan` se output longo demais.

Producer/consumer:
- **Producer mecânico:** `ls /storage/dev/projects/pragmatic-dev-toolkit/docs/decisions/ADR-*.md | sort` + `ls /storage/dev/projects/pragmatic-dev-toolkit/docs/decisions/archive/ADR-*.md | sort` + verificação `grep -l "^\*\*Status:\*\* Substituído" docs/decisions/ADR-*.md` para excluir Substituído vigentes mascarados.
- **Consumer analítico:** lista de 27 vigentes × candidatos K-X declarados em charter § Atualização pós-execução linha 188 + NOTES `tres-principios-4` § Candidatos K + BACKLOG umbrella linha 5.
- **Output esperado:** tabela `ADR-NNN | título curto | candidato cluster (K-X) ou "órfão"` cobrindo 27 linhas.

Doc-reviewer revisa qualidade do mapeamento (cada vigente tem candidato declarado ou "órfão" com justificativa de por que não cabe em candidatos existentes).

### Bloco 2 — Refinar charter projeção {reviewer: doc}

- `docs/plans/redesign-camada-doutrinal-charter.md`:
  - § Atualização pós-execução tabela: adicionar linha **"K — Auditoria do inventário vigente"** com Status ✓ + Commit/PR + Substância (saldo mecânico 27 vigentes + cluster sequence recalibrada + projeção empírica).
  - § Cap de ondas linha 188: substituir texto literal "sujeito a re-auditoria do inventário 27 vigentes" por projeção empírica pós-auditoria (`Target NN consolidados em MM ondas adicionais conforme cluster sequence X→Y→Z`).
  - § Anti-regression checklist se categoria nova de carga doutrinal emergiu durante auditoria (provavelmente não — auditoria é informação, não doutrina).

Doc-reviewer revisa coerência cross-doc (charter ↔ BACKLOG ↔ NOTES) + ausência de drift numérico vs Bloco 1.

### Bloco 3 — Atualizar BACKLOG umbrella linha 5 {reviewer: doc}

- `BACKLOG.md` linha 5: adicionar segmento `**Onda K** — auditoria do inventário vigente — commit \`<hash>\` + PR #<NN> — produto: lista exaustiva 27 vigentes + cluster sequence recalibrada (Onda K → Onda K' editorial canonical templates → Onda L cluster decidido pela auditoria) + recommendation cluster Onda L downstream. NÃO migrou cluster (tactical-only paralelo a Onda Promoção); saldo inventário 27 vigentes preservado.` Atualizar texto final da linha (lista candidatos K-X) com cluster sequence recalibrada incluindo Onda K' promovida.

Doc-reviewer revisa formato paralelo a updates anteriores de Onda na linha 5 (uso de **negrito**, formato de commit hash, presença de PR #).

## Verificação end-to-end

1. **Bloco 1 mecânico:** count vigente **filtrado** bate com 27. `ls /storage/dev/projects/pragmatic-dev-toolkit/docs/decisions/ADR-*.md | wc -l` retorna total bruto (esperado 33, inclui ADRs marcados `Status: Substituído` preservados in-place); `grep -L "^\*\*Status:\*\* Substituído" /storage/dev/projects/pragmatic-dev-toolkit/docs/decisions/ADR-*.md | wc -l` retorna 27 (saldo vigente declarado em NOTES + BACKLOG). Se discrepância pós-filtragem, auditar antes de prosseguir.
2. **Bloco 1 cobertura:** mapeamento contém entrada para cada um dos 27 vigentes (zero faltantes); cada entrada classificada como (a) candidato K-X declarado OU (b) órfão com justificativa textual.
3. **Bloco 2 charter:** `grep -c "^| \*\*K\*\*" docs/plans/redesign-camada-doutrinal-charter.md` retorna 1 (linha Onda K adicionada à tabela § Atualização pós-execução).
4. **Bloco 2 charter:** `grep "sujeito a re-auditoria" docs/plans/redesign-camada-doutrinal-charter.md` retorna 0 matches (texto antigo substituído por projeção empírica). Verificar também ausência de drift entre projeção e saldo do Bloco 1.
5. **Bloco 3 BACKLOG:** `grep "Onda K" BACKLOG.md` retorna ≥1 match no contexto da linha 5 (segmento Onda K adicionado à umbrella).
6. **Saldo inventário pós-onda:** `git status docs/decisions/ docs/decisions/archive/` retorna `clean` (zero mutação — auditoria não muta inventário, apenas produz informação). Verificação git-based detecta qualquer alteração com 1 comando, sem dependência de count lexical (per cutucada do design-reviewer resolvida — alternativa de filtragem simétrica `grep -L | wc -l` descartada por fragilidade lexical recorrente).
7. **Push imediato pós-commit:** caminho-com-plano padrão (commit + push como unidade atômica via `/run-plan §Publicar`).

## Notas operacionais

**Decomposição cluster Onda L → `/triage` subsequente.** Onda K (esta) produz auditoria + projeção; cluster Onda L downstream emerge como `/triage` separado consumindo o produto desta auditoria. Pattern operacional paralelo a **Onda Promoção** (tactical-only batch promotion) precedendo Onda I — onda dedicada a informação/preparação precede onda de migração que consome.

**Sem ADR criado.** Auditoria é descoberta + refinamento editorial per ADR-045 § Decisão linha 56 fronteira *"absorção/projeção em consolidado diferente do sketch original"* — categoria editorial livre durante execução das ondas. Auto-aplicação ADR-034 § Decisão (paralelo a ADR-053/-054 § Origem):

- **Cond 1 (decisão estrutural sem ancestral):** NÃO aplica — ADR-045 é ancestral codificado direto.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — substância de ADR-045 preservada integralmente.
- **Cond 3 (codifica restrição externa):** NÃO aplica — auditoria é trabalho interno do plugin.
- **Cond 4 (categoria nova):** NÃO aplica — auditoria empírica é aplicação operacional, não meta-pattern editorial codificável (ainda).
- **Cond 5 (sucessor parcial):** NÃO aplica **isoladamente** — esta é a 1ª instância de auditoria pré-cluster; se ≥3 emergirem em redesigns futuras, gatilho de revisão dispara para promover a meta-pattern paralelo a ADR-052 (formalização de auditoria pré-cluster como modo editorial canonical das ondas tactical-only).

**Rebatimento da recursão flagada em ADR-045 § Limitações.** Auditoria pode revelar (i) cluster sequence reordering ou (ii) cluster semântico novo não-previsto no sketch. Caso (i) cabe no primeiro item da fronteira ADR-045 § Decisão linha 56 — categoria editorial livre, ajuste de ordem de migração. Caso (ii) cabe em § Gatilhos de revisão de ADR-045 *"Estrutura-alvo (~10-12 ADRs) revelada inadequada durante migração"* — gatilho disparado apenas se design-reviewer flagrar inadequação em ≥2 ondas. Onda K é descoberta empírica que alimenta § Gatilhos, não disparo do gatilho per se. Recursão mitigada por separar (descoberta) de (decisão estrutural).

**Paralelo a Onda Promoção (tactical-only).** Onda K herda pattern de Onda Promoção: onda dedicada a preparação/informação cujo produto é input para onda de migração subsequente. Onda Promoção promoveu Status de 7 consolidados pré-Onda I; Onda K mapeia inventário pré-Onda L. Saldo inventário inalterado em ambas (zero migrations, zero criações líquidas).

**Onda K' editorial canonical templates promovida.** 3 instâncias empíricas do bug lexical em critérios end-to-end (Onda Promoção critério 6 `Substituído` sem prefixo Status field + Onda J critério 6.4 `contrato-declarado` com hífen + critérios 1+6 deste plano antes da absorção pré-commit do design-reviewer) batem ADR-035 critério 4 (per ADR-043) — ≥3 pattern emergente. Onda K' promovida de "candidato condicional futura" para **execução tactical-only paralela** precedendo Onda L cluster. Cluster sequence atualizada: **Onda K (esta auditoria) → Onda K' editorial canonical templates → Onda L (cluster decidido pela auditoria)**. Onda K' produz: (a) refinamento de `templates/plan.md` § Verificação end-to-end (prefixar `^\*\*Status:\*\*` em greps de Status field; formulações canonical sem hífens decorativos; preferir `git status` git-based vs counts lexicais quando aplicável); (b) atualização charter § Atualização pós-execução; (c) BACKLOG umbrella linha 5 update. Sem ADR criado (Onda K' é refinamento editorial puro per ADR-045 § Decisão linha 56 primeira fronteira — categoria editorial livre paralela a Onda Promoção tactical-only).

**Gatilho ADR-045 (meta-pattern de auditoria pré-cluster) deferido.** Reviewer flagou sinal a observar: se ≥2 auditorias pré-cluster emergirem em redesigns futuras, promover formalização de "auditoria pré-cluster" como modo editorial canonical paralelo a ADR-052 (que codificou 3 modos editoriais de composição de cluster). 1ª instância (esta Onda K) NÃO justifica edit em ADR-045 vigente apex per admission policy anti-recursão (ADR-045 § Limitações). Registrar em NOTES pós-merge como sinal a observar.

**Apex meta-cluster decision-making.** NOTES + charter listam apex meta-cluster (ADR-009+034+035+043+045+046+047+048+049+050+051+052+053+054 — 14 ADRs apex) como candidato "opcional; risco alto auto-referência". Auditoria deve produzir veredito: skip definitivo OU candidato real para onda final. Se skip, charter § Cap de ondas reflete; se candidato real, cluster sequence inclui como onda terminal.

**Decomposição em 3 blocos.** Razão: doc-reviewer roda per-bloco (invariante 11 instâncias consecutivas pós-Onda F); separação Bloco 1 (auditoria estruturada) ↔ Bloco 2 (charter) ↔ Bloco 3 (BACKLOG) protege contra drift cross-doc, com cada superfície tendo seu próprio reviewer pass. Colapso em 1 bloco replicaria o anti-pattern da pendência Onda F (Bloco 1 commitado sem doc-reviewer). Onda Promoção colapsou em 1 bloco principal porque produto era state change in-place (Status field), não 3 superfícies distintas.

**Captura §3.5 reservada.** Se auditoria revelar gap ou inconsistência editorial (ex.: ADR vigente que devia estar archived, archive index incompleto, drift entre saldo declarado e count mecânico), capturar via TaskCreate `[capture:auditoria]` materializada em §3.5 do `/run-plan` — pendência para onda corretiva futura, não bloqueante desta onda.

## Pendências de validação

- ~~**Critério 1 do plano (specification bug — 5ª evidência empírica pattern lexical):** após absorção pré-commit do design-reviewer no /triage, critério 1 esperava raw==33 + filtrado==27. Estado pós-cleanup de órfãos FS (commit `d5e6102` precedente): raw==27 + filtrado==26. Substância da auditoria cumprida (saldo correto 26 vigentes substantivos + 1 Substituído = 27 entradas refletido em charter linha 152+188 + BACKLOG linha 5 segmento Onda K). Critério mecânico literal não bate porque assumption do raw count (33) não previu cleanup de órfãos pré-loop. **Escopo Onda K' editorial canonical templates** — adicionar diretriz canonical: *"critérios end-to-end baseados em count mecânico (`wc -l`, etc.) devem citar valor esperado como variável (`<saldo>`) ou amarrar a condição inversa (`git status clean`) em vez de número literal hardcoded — números mudam de uma onda para a próxima."* Não bloqueante para Onda K — substância cumprida.~~ **Encerrada 2026-06-01:** resolvida sistemicamente via Onda K' (PR #102, commit `c713238`) — diretriz canonical #4 (counts como variável ou condição inversa, aplicação forward apenas) codificada em `templates/plan.md` § Verificação end-to-end comentário HTML inline.

## Decisões absorvidas

- § Verificação end-to-end critério 1: bug lexical do `wc -l` literal (retorna 33, não 27) corrigido com filtragem `grep -L "^\*\*Status:\*\* Substituído"` (caminho-único).
- § Resumo da mudança: clarificada correspondência 5 sub-análises → 3 blocos (1 análise estruturada cobrindo 3 sub-análises + 2 edits editoriais) eliminando drift Resumo↔Arquivos a alterar (caminho-único).
- § Notas operacionais "Sem ADR criado": auto-aplicação ADR-034 § Decisão reformulada de parágrafo descritivo para enumeração mecânica das 5 condições paralela a ADR-053/-054 § Origem (caminho-único).
- § Notas operacionais: rebatimento explícito da recursão flagada em ADR-045 § Limitações adicionado separando casos (i) cluster sequence reordering (categoria editorial livre) de (ii) cluster semântico novo (gatilho de revisão se ≥2 ondas confirmarem) — Onda K é descoberta empírica, não disparo do gatilho (caminho-único).
- § Notas operacionais: justificativa para decomposição em 3 blocos adicionada (doc-reviewer per-bloco invariante; gate per-superfície protege contra drift cross-doc) (caminho-único).
