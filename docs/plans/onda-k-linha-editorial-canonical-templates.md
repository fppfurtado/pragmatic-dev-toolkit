# Plano — Onda K' (editorial canonical templates: refinar `templates/plan.md` § Verificação end-to-end)

## Contexto

Onda K' promovida via cutucada resolvida no /triage da Onda K (commit `899a130`) precedendo Onda L cluster. 5 instâncias empíricas do bug lexical em critérios end-to-end de planos batem ADR-035 cond 4 (per ADR-043 § Ockham operacionalizado critério 4 — ≥3 pattern emergente):

1. **Onda Promoção crit 6** `grep "Substituído"` sem prefixo Status field — falso-positivo casando narrativa histórica em § Origem dos consolidados (capturado em `docs/plans/onda-promocao-batch-consolidados-aceito.md` § Pendências de validação).
2. **Onda J crit 6.4** `"contrato-declarado\|heurística filesystem"` com hífen decorativo — falso-negativo; texto real do ADR-054 usa "*contrato declarado*" (com espaço, sem hífen).
3. **Onda K crit 1 pré-absorção** `wc -l` literal esperava 33 + 27 sem filtrar Substituídos — absorvido pré-commit pelo design-reviewer no /triage.
4. **Onda K crit 6 pré-absorção** count `wc -l == 27` esperado pós-onda — substituído por `git status clean` git-based via cutucada absorvida opção (b).
5. **Onda K crit 1 pós-absorção** raw 27 + filtrado 26 (não esperados 33 + 27) — críticio mecânico literal não bate após cleanup órfãos FS pré-loop; substância cumprida; gap editorial registrado no plano § Pendências de validação (commit `e87ddcb`).

Pattern emergente: critérios end-to-end de planos com counts/greps literais hardcoded são frágeis a (a) typos lexicais, (b) variação de saldo entre ondas, (c) state pré-loop que altera assumptions. Diretrizes canonical absorvem o pattern em refinamento editorial do `templates/plan.md`.

**Intent charter § Atualização pós-execução linha 189 (Onda K' Pendente — declaração pré-execução):** *"Refinamento de `templates/plan.md` § Verificação end-to-end (prefixar `^\*\*Status:\*\*` em greps de Status field; preferir `git status` git-based vs counts lexicais quando aplicável; formulações canonical sem hífens decorativos). Tactical-only; sem ADR criado."*

**Bifurcação resolvida no /triage:** (a) Apenas `templates/plan.md` vs (b) Template + bullet CLAUDE.md sem ADR vs (c) Criar ADR codificando diretrizes. Operador escolheu **(a)** — segue intent charter; pattern paralelo aos comentários HTML existentes nas linhas 14-22 do template; Ockham (sem cross-ref CLAUDE.md sem ADR — evita drift de pattern editorial canonical onde bullets meta-doutrinais cross-ref ADRs específicos).

**Linha do backlog:** plugin: **redesign da camada doutrinal** — consolidar 45 ADRs em ~10-12 temáticos sob hierarquia invertida pós-v2.14.0 + condensar `philosophy.md` (princípios + mapping operacional + ≥3 pattern como condição geral de YAGNI terminar; cortar § Codificação estrutural overhead) + codificar **política de admissão going forward** (*"isto é decisão reversível ou entendimento estabilizado?"*) como mecanismo de prevenção de re-acúmulo.

**ADRs candidatos:** ADR-001 (protocolo templates centralizados — ancestral codificado para `templates/plan.md`); ADR-033 (templates admite single-consumer declarativo — pattern editorial para esqueletos preenchíveis); ADR-045 (fronteira "ajuste editorial vs revisão" — autoriza esta onda como categoria editorial livre); ADR-052 (3 modos editoriais a/b/c — meta-pattern editorial precedente com critério mecânico verificável; informa decisão de não-codificar Onda K' como ADR per opção a).

## Resumo da mudança

Edit cirúrgico no template canonical + propagação editorial. Decomposta em **3 blocos**: 1 edit do template + 2 edits editoriais:

1. **`templates/plan.md` § Verificação end-to-end**: adicionar comentário HTML com 4 diretrizes canonical (paralelo aos comentários HTML existentes linhas 14-22 que já documentam campos especiais).
2. **Charter § Atualização pós-execução linha 189**: substituir `Pendente | — |` por `✓ | <hash>` + PR #<NN> + substância (5 evidências empíricas codificadas como diretrizes; decisão tactical-only sem ADR confirmada).
3. **BACKLOG umbrella linha 5**: adicionar segmento Onda K' shipped paralelo ao segmento Onda K.

**Não-escopo desta onda:**
- ADR codificando diretrizes (decisão (a) /triage; reabrir somente se 6ª instância emergir).
- Bullet CLAUDE.md cross-ref (decisão (a) /triage; pattern editorial não-padrão sem ADR).
- Refinamento de outros critérios canonical de templates (target restrito a § Verificação end-to-end).

## Arquivos a alterar

### Bloco 1 — Refinar `templates/plan.md` § Verificação end-to-end {reviewer: doc}

- `templates/plan.md`: adicionar comentário HTML inline em § Verificação end-to-end (linhas 44-46 atualmente) com 4 diretrizes canonical:
  1. **Greps de Status field**: prefixar com `^\*\*Status:\*\*` para discriminar Status canonical vs narrativa histórica em § Origem (lição Onda Promoção crit 6).
  2. **Verificações de inalterabilidade de inventário**: preferir `git status <path> | clean` git-based vs `wc -l` count lexical hardcoded — counts mudam entre ondas; git status detecta mutação independente de saldo (lição Onda K crit 6).
  3. **Formulações de termos canonical**: citar termos exatamente como aparecem no texto-alvo (preservar espaços, hífens, capitalização). Verificar via Read do texto antes de hardcodar grep (lição Onda J crit 6.4: texto real do ADR-054 usa "*contrato declarado*" sem hífen vs grep com hífen decorativo).
  4. **Counts esperados**: citar valor como variável (`<saldo>`) ou amarrar condição inversa (`git status --porcelain -- <paths>` retorna 0 linhas; ausência de matches em grep) em vez de número literal hardcoded — saldos mudam entre ondas e estado pré-loop pode alterar assumption (lição Onda K crit 1 pré e pós-absorção). **Aplicação forward apenas**: planos mergeados anteriormente com counts literais não são tocados retroativamente — substância dos critérios passados foi cumprida pela verificação manual mesmo com count literal.

Doc-reviewer revisa: (a) consistência do comentário HTML com pattern existente linhas 14-22; (b) diretrizes cobrem as 5 evidências empíricas listadas no § Contexto; (c) formulações são exemplificadas com referência às ondas onde a evidência emergiu (auditabilidade pós-fato).

### Bloco 2 — Atualizar charter § Atualização pós-execução linha 189 (Onda K' shipped) {reviewer: doc}

- `docs/plans/redesign-camada-doutrinal-charter.md`:
  - § Atualização pós-execução tabela linha 189 (Onda K' Pendente): substituir Status `Pendente` → `✓` + Commit/PR placeholder → commits reais + Substância expandida (5 evidências empíricas codificadas como 4 diretrizes canonical; decisão tactical-only sem ADR confirmada via /triage opção (a)). Atualizar contagem "4 evidências" da declaração Pendente original para "5 evidências" — substância correta: Onda K crit 1 pós-absorção é qualitativamente distinta (gap editorial pós-substantia cumprida vs typo lexical), justifica diretriz 4 por si só. "cleanup órfãos FS pré-loop" removido da lista (vive como item BACKLOG linha 7 separado, fora do escopo do pattern lexical de critérios end-to-end).

Doc-reviewer revisa: (a) formato paralelo a entries existentes da tabela (Ondas A-K + ADR-052 + Promoção I); (b) ausência de drift numérico vs Bloco 1; (c) coerência cross-doc com BACKLOG umbrella linha 5 segmento Onda K' (Bloco 3).

### Bloco 3 — Atualizar BACKLOG umbrella linha 5 segmento Onda K' {reviewer: doc}

- `BACKLOG.md` linha 5: adicionar segmento `**Onda K'** — editorial canonical templates — commits <hashes> + PR #<NN> — produto: refinamento de templates/plan.md § Verificação end-to-end com 4 diretrizes canonical absorvendo **5 evidências empíricas** (Onda Promoção crit 6 + Onda J crit 6.4 + Onda K crit 1 pré-absorção + Onda K crit 6 pré-absorção + Onda K crit 1 pós-absorção). Tactical-only paralelo a Onda Promoção; sem ADR criado per intent charter linha 189 + decisão /triage opção (a) — pattern editorial canonical não-padrão (CLAUDE.md cross-refs ADRs específicos; sem ADR, bullet seria primeiro do gênero — evitar drift). Saldo inventário 27 entradas preservado (zero archived, zero novos).` Atualizar contagem "4 evidências" da declaração Pendente original (segmento Onda K) para "5 evidências" — substância correta. "cleanup órfãos FS pré-loop" removido da lista de evidências (vive como item BACKLOG linha 7 separado). Atualizar texto final da linha (sequence pós-Onda K) substituindo "Onda K'" pendente por "Onda K'" shipped + ajustar projeção restante (Onda Promoção II → L → M opcional → apex SKIP).

Doc-reviewer revisa: formato paralelo a updates de Onda anteriores na linha 5 (uso de **negrito**, formato commit hash, presença de PR #, paralelo ao segmento Onda K).

## Verificação end-to-end

Aplicando as próprias diretrizes da Onda K' (dogfood):

1. **Bloco 1 template**: `git status templates/plan.md` em branch `onda-k-linha-editorial-canonical-templates` retorna modified (diff isolado ao § Verificação end-to-end com comentário HTML novo). Pós-merge: `git status templates/plan.md` clean.
2. **Bloco 1 cobertura editorial**: comentário HTML contém referência textual às 4 diretrizes nomeadas + cita ≥1 instância empírica por diretriz (Onda Promoção + J + K pré-absorção + K pós-absorção).
3. **Bloco 2 charter**: linha 189 deixa de matchear `Pendente` em Status field — `grep "^| \*\*K'\*\* —.*| Pendente |" docs/plans/redesign-camada-doutrinal-charter.md` retorna 0 matches pós-edit (condição inversa per diretriz 4).
4. **Bloco 3 BACKLOG**: linha 5 contém segmento Onda K' — `grep -c "Onda K'.*editorial canonical templates" BACKLOG.md` retorna ≥1 (presença positiva).
5. **Saldo inventário pós-merge**: `git status --porcelain -- docs/decisions/ docs/decisions/archive/` retorna 0 linhas (Onda K' tactical-only, zero mutação de inventário — git-based per diretriz 2). Verificação pós-merge na branch main; durante execução loop em worktree o teste só vale a partir do Bloco 2 (Bloco 1 edita `templates/plan.md` fora de `docs/decisions/`).
6. **Push imediato pós-commit**: caminho-com-plano padrão (commit + push como unidade atômica via `/run-plan §Publicar`).

## Notas operacionais

**Paralelo a Onda Promoção (tactical-only).** Onda K' herda pattern de Onda Promoção: onda dedicada a refinamento editorial canonical cujo produto é diretriz operacional para ondas downstream (Onda L cluster + futuras migrações que escreverão critérios end-to-end). Onda Promoção promoveu Status de 7 consolidados; Onda K' codifica diretrizes editoriais. Saldo inventário inalterado em ambas (zero migrations, zero criações líquidas).

**Sem ADR criado.** Decisão /triage opção (a). Auto-aplicação ADR-034 § Decisão (paralelo a ADR-053/-054/Onda K § Origem):

- **Cond 1 (decisão estrutural sem ancestral):** NÃO aplica — ADR-001 (protocolo templates) é ancestral codificado direto.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — refina template, não substitui ADR-001.
- **Cond 3 (codifica restrição externa):** NÃO aplica — refinamento interno do toolkit.
- **Cond 4 (categoria nova):** NÃO aplica sob **leitura estreita per ADR-052 § Auto-aplicação** — pattern editorial de critérios end-to-end refina sub-estrutura do eixo "templates canonical para artefatos do toolkit" (eixo já codificado em ADR-001 + ADR-033) sem criar 4º eixo conceitual paralelo. 5 evidências empíricas atingem critério ADR-043 § Ockham operacionalizado 4 (≥3 pattern) em rigor, mas substância cabe em refinamento direto do template (categoria editorial livre per ADR-045 § Decisão linha 56 primeira fronteira); ADR formal seria over-engineering — diretrizes não precisam de § Origem/§ Decisão/§ Gatilhos elaborados. Reabrir se 6ª instância emergir OU se diretriz precisar de § Gatilhos formais (gatilho próprio).
- **Cond 5 (sucessor parcial):** NÃO aplica — substância cabe em refinamento direto do template per ADR-045 fronteira editorial (acima); não é sucessor parcial de ADR-001, é exercício da fronteira editorial existente do próprio ADR-001 § protocolo templates.

**Diretrizes inline vs ADR formal.** Pattern Onda Promoção (tactical-only sem ADR) válido aqui. Se padrão de critérios end-to-end evoluir para meta-doutrina (≥6 instâncias OR exigência de § Gatilhos), promover via ADR sucessor parcial de ADR-001 § protocolo templates — gatilho próprio.

**Decomposição em 3 blocos.** Razão: doc-reviewer roda per-bloco (invariante mantido pós-Onda K — 14+ instâncias consecutivas); separação Bloco 1 (template) ↔ Bloco 2 (charter) ↔ Bloco 3 (BACKLOG) protege contra drift cross-doc, com cada superfície tendo seu próprio reviewer pass. Paralelo direto à decomposição da Onda K.

**Captura §3.5 reservada.** Se onda revelar 6ª evidência empírica do pattern lexical OR diretriz nova emergente (ex.: edits manuais futuros expondem caso edge não-coberto pelas 4 atuais), capturar via TaskCreate `[capture:auditoria]` materializada em §3.5 do `/run-plan` — pendência para revisão futura. Não bloqueante.

**Pós-Onda K' próxima ação:** `/triage` Onda Promoção II (tactical-only batch promotion 10 ADRs Proposto-shipped → Aceito formal; critério explícito declarado em charter linha 190 + BACKLOG linha 5 segmento Onda K').

## Decisões absorvidas

- § Contexto + Bloco 2 (charter) + Bloco 3 (BACKLOG): padronização cross-doc de "4 evidências" → "5 evidências" — Onda K crit 1 pós-absorção qualitativamente distinta justifica entrada própria; "cleanup órfãos FS pré-loop" removido da lista (vive como item BACKLOG separado linha 7). Decisão (a) via cutucada do design-reviewer absorvida.
- Bloco 1 diretriz 3: "padronizar com espaço (preferido canonical) vs hífen" removido (falsa dicotomia prescritiva; conflitava com convenções vigentes design-reviewer/doc-reviewer hifenadas). Simplificada para apenas fidelidade ao texto-alvo + verificar via Read antes de hardcodar grep (caminho-único).
- Bloco 1 diretriz 4: adicionada qualificação "Aplicação forward apenas; planos mergeados anteriormente com counts literais não são tocados retroativamente" evitando flags improdutivos sobre Ondas A-J shippadas (caminho-único).
- § Notas operacionais Auto-aplicação cond 4: reescrita invocando leitura estreita ADR-052 § Auto-aplicação ("refina sub-estrutura do eixo templates canonical sem criar 4º eixo conceitual paralelo") — alinha com precedente doutrinário; remove confusão entre cond 4 ADR-034 e Ockham filtro de admissão (caminho-único).
- § Notas operacionais Cond 5: simplificada — não é sucessor parcial, é exercício da fronteira editorial existente de ADR-001 (caminho-único).
- § Verificação end-to-end crit 5: reformulado para `git status --porcelain -- docs/decisions/ docs/decisions/archive/` retorna 0 linhas + nota temporal (pós-merge na main; durante loop em worktree só vale pós-Bloco 2) — pathspec robusto vs ambiguidade do critério original (caminho-único).
- § Verificação end-to-end crit 4: removida primeira alternativa "Onda K' shipped" do grep (fallback `Onda K'.*editorial canonical templates` cobre; Bloco 3 não usa "shipped" no segmento) — elimina circularidade editorial (caminho-único).
