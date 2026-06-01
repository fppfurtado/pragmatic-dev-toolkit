# Plano — Onda Final A: admission policy enforcement em /new-adr + design-reviewer

## Contexto

**Linha do backlog:** plugin: **redesign da camada doutrinal** — consolidar 45 ADRs em ~10-12 temáticos sob hierarquia invertida pós-v2.14.0 + condensar `philosophy.md` (princípios + mapping operacional + ≥3 pattern como condição geral de YAGNI terminar; cortar § Codificação estrutural overhead) + codificar **política de admissão going forward** (*"isto é decisão reversível ou entendimento estabilizado?"*) como mecanismo de prevenção de re-acúmulo.

**ADRs candidatos:** ADR-045 § Decisão parte 2 (filtro de 3 saídas + heurísticas + critérios de desempate — substância alvo de materialização runtime), ADR-045 § Implementação operacional Onda final (declara 2 superfícies primárias: step 3.5 em /new-adr + design-reviewer `## O que flagrar` critério novo), ADR-045 § Condição de validade do enforcement (política sem enforcement = decoração doutrinal; bump v3.0.0 condicionante), ADR-053 § Decisão (b) wiring design-reviewer auto-fire (executa em /new-adr step 5 — Onda Final A adiciona critério ao reviewer que já roda automaticamente).

**Décima sexta onda da redesign + Onda Final A** (parte 1 da Onda final do charter linha 35). Materializa runtime per ADR-045 § Implementação operacional Onda final literal. **Sem refinamento doutrinal nesta onda** — ADR-045 vigente prescreve mecanismo; esta onda apenas codifica em runtime.

Operador escolheu **caminho A (2 superfícies primárias canonical)** sobre caminho B (apenas design-reviewer per § Condição de validade fallback). Razões registradas pré-plano:

- ADR-045 § Implementação operacional Onda final declara explicitamente 2 superfícies primárias (step 3.5 + reviewer); fallback B só ativa se step 3.5 declarado inviável.
- Belt-and-suspenders alinha com filosofia da redesign (mecanismo codificado, não confiado).
- Standalone `/new-adr` ganha valor real (prompt apresenta 3 saídas + heurísticas antes do operador investir em ADR draft).
- +1 clique na delegação /triage step 4 é overhead UX leve, aceitável vs robustez upfront.

**Onda Final A gateia Onda Final B (`/release v3.0.0`)** per ADR-045 § Condição de validade do enforcement: bump v3.0.0 condicionado a ≥1 superfície runtime efetiva. Pós-Onda Final A, condicionante satisfeita; B liberada.

## Resumo da mudança

Materializar admission policy enforcement em 2 superfícies runtime per ADR-045 § Implementação operacional Onda final:

1. **`skills/new-adr/SKILL.md` step 3.5 novo** — inserir entre step 3 (obter data) e step 4 (criar arquivo). Prompt informativo via `AskUserQuestion` (header `Filtro`, enum 3 saídas: `ADR — decisão estrutural reversível (Recommended)` / `CLAUDE.md ou philosophy.md — entendimento estabilizado` / `git log — evolução de processo`). `description` de cada saída carrega as heurísticas relevantes per ADR-045 § Decisão parte 2 + critérios de desempate na zona cinzenta. Saída `ADR` → seguir para step 4 (criar arquivo). Saídas `CLAUDE.md/philosophy.md` ou `git log` → reportar ao operador o destino alternativo e parar (não criar arquivo ADR); operador resolve manual conforme orientação.

2. **`agents/design-reviewer.md` § O que flagrar critério novo** — adicionar bullet documentando que candidato a ADR draft que **falha no filtro de admissão** (substância revela entendimento estabilizado que deveria ir pra `CLAUDE.md` ou `philosophy.md`; ou evolução de processo que deveria ir pra git log) é **finding pré-criação**. Reviewer ganha critério adicional avaliado durante /new-adr step 5 (já roda automaticamente per ADR-053 § Decisão (b)). Cross-ref a ADR-045 § Decisão parte 2.

Saldo inventário inalterado (26 entradas no FS preservado; sem ADR criado nesta onda). Tactical-only doc-only com 2 superfícies runtime. **Onda Final A gateia Onda Final B** (release v3.0.0) per ADR-045 § Condição de validade.

## Arquivos a alterar

### Bloco 1 — skills/new-adr/SKILL.md step 3.5 admission policy filter {reviewer: doc}

- `skills/new-adr/SKILL.md`: inserir step 3.5 entre o step 3 atual ("Obter data") e o step 4 atual ("Criar arquivo"). Conteúdo do step 3.5:
  - **Cabeçalho:** "3.5. **Filtro de admissão** (per [ADR-045](../../docs/decisions/ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 2). Antes de criar o arquivo ADR, surfar o filtro mecânico de 3 saídas como prompt informativo."
  - **Prompt enum:** `AskUserQuestion` header `Filtro`, 3 opções:
    - `ADR — decisão estrutural reversível (Recommended)`: description carrega heurísticas primárias (`Reversibilidade positiva: nomear cenário concreto de reversão; Categoria nova; Codifica restrição externa; Pattern emergente ≥3 aplicações`).
    - `CLAUDE.md ou philosophy.md — entendimento estabilizado`: description cita critério de desempate (`philosophy.md = princípio epistêmico/convenção cross-cutting; CLAUDE.md = mecânica do plugin: lifecycle, naming, gate concreto, schema YAML, AskUserQuestion convention`).
    - `git log — evolução de processo`: description cita "altera apenas implementação/estilo sem afetar runtime de outros componentes".
  - **Pós-decisão:**
    - Saída `ADR` → seguir para step 4 (criar arquivo). Fluxo default preservado.
    - Saída `CLAUDE.md ou philosophy.md` → parar criação do arquivo ADR; reportar ao operador: "Substância não passou no filtro de admissão de ADR — direcionar para `CLAUDE.md` ou `philosophy.md` per critério de desempate da saída escolhida. Sem ADR criado. Operador edita o documento alvo + commit como `docs:`/`chore:` conforme convenção."
    - Saída `git log` → parar criação do arquivo ADR; reportar: "Substância não passou no filtro — evolução de processo registrada apenas em commit message. Operador faz o commit relevante sem documento. **Nota orientacional:** chegar a `/new-adr` standalone com saída `git log` tipicamente sinaliza erro de framing upstream (substância pré-cristalizada como título mas era iteração editorial). Operador faz commit relevante com a substância no message; futuras invocações de /new-adr que detectem este padrão recorrente são candidato a refinamento do critério de entrada upstream (/triage step 3)."
  - **Cross-ref a critérios de desempate na zona cinzenta** (ADR-045 § Decisão parte 2 linhas 79-83): mencionar em prosa próxima ao enum que critérios canonical de desempate vivem em ADR-045 § Decisão parte 2 + reviewer cobre default conservador (dúvida → cutucar).
  - **Cláusula default-conservadora** per ADR-045 § Decisão parte 2 linha 83: "Cláusula default-conservadora: dúvida na classificação → operador escolhe `ADR` (default Recommended); design-reviewer no step 5 audita drift pós-criação."
  - **Renumerar steps subsequentes:** step 4 (criar arquivo) → step 4 (preservado); step 5 (revisão pré-retorno) → step 5 (preservado). Step 3.5 fica intercalado sem renumeração dos demais (numeração não-densa per convenção: paralelo a /run-plan §3.5).

### Bloco 2 — agents/design-reviewer.md § O que flagrar critério novo {reviewer: doc}

- `agents/design-reviewer.md`: adicionar bullet em `## O que flagrar` documentando o critério novo per ADR-045 § Decisão parte 2 + § Implementação operacional Onda final. Conteúdo do bullet:
  - **Texto:** "**Candidato a ADR draft que falha no filtro de admissão** (per [ADR-045](../docs/decisions/ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 2): substância revela **entendimento estabilizado** que deveria ir pra `CLAUDE.md` ou `philosophy.md` (refinamento de mecanismo, esclarecimento doutrinal, regra editorial estabilizada); ou **evolução de processo** que deveria ir pra git log (refactor sem decisão estrutural, iteração editorial). Finding pré-commit do ADR draft criado (reviewer roda em /new-adr step 5 após operador ter escolhido `ADR` no step 3.5): operador absorve abandonando o ADR draft (delete + redirect substância para destino correto) **ou** refinando o draft para cumprir o filtro (acrescentar cenário concreto de reversão / categoria nova / restrição externa). Critério de desempate na zona cinzenta vive em ADR-045 § Decisão parte 2; default conservador (dúvida) → operador escolheu ADR no step 3.5, reviewer flagra pós-criação se drift evidente."
  - **Posicionamento:** após bullets existentes em `## O que flagrar` (continuar lista; não substituir).
  - **Cross-ref bilateral mantida:** ADR-045 já não menciona reviewer.md como invariante; cross-ref unilateral aceitável (paralelo a outros critérios em `## O que flagrar` que citam ADRs específicos sem invariante bilateral).

## Verificação end-to-end

<!-- Diretrizes canonical da Onda K' aplicadas: (1) `^\*\*Status:\*\*` prefix; (2) `git status --porcelain -- <paths>` git-based vs counts lexicais; (3) fidelidade ao texto-alvo via Read antes de hardcodar grep; (4) counts como variável ou condição inversa; aplicação forward apenas. -->

1. **Bloco 1 step 3.5 inserido em /new-adr SKILL.md (presença positiva + diretriz 3 fidelidade ao texto-alvo):** `grep -nE "^3\.5\.|Filtro de admissão|3 saídas" skills/new-adr/SKILL.md` retorna ≥1 ocorrência por padrão (step 3.5 cabeçalho + título "Filtro de admissão" + menção a "3 saídas").
2. **Bloco 1 ordem dos steps preservada:** `grep -nE "^[0-9]+(\.[0-9]+)?\.\s+\*\*" skills/new-adr/SKILL.md` retorna sequência `1 → 2 → 3 → 3.5 → 4 → 5` (numeração não-densa per convenção; paralelo a /run-plan §3.5).
3. **Bloco 1 cross-ref a ADR-045 explícito:** `grep -nE "ADR-045.*§ Decisão parte 2|admission policy" skills/new-adr/SKILL.md` retorna ≥1 ocorrência (cross-ref direta à substância).
4. **Bloco 2 critério novo em design-reviewer § O que flagrar:** `grep -nE "filtro de admissão|admission policy|falha no filtro" agents/design-reviewer.md` retorna ≥1 ocorrência; `grep -nE "ADR-045" agents/design-reviewer.md` retorna ≥1 ocorrência.
5. **Bloco 2 posicionamento no § O que flagrar** (robustez per diretriz Onda K' #2 — delimitador explícito de próximo `## ` top-level vs `## ` qualquer): `awk '/^## O que flagrar/{f=1; next} /^## [A-Z]/{f=0} f' agents/design-reviewer.md | grep -E "filtro de admissão|admission policy|falha no filtro"` retorna ≥1 linha dentro da seção `## O que flagrar` (não em hipotético sub-`## ` errôneo).
6. **ADR-045 inalterado per immutability** (ADR Aceito não tocado): `git status --porcelain -- docs/decisions/ADR-045*.md` retorna vazio.
7. **Saldo inventário preservado** (sem ADR criado nesta onda): `find docs/decisions -maxdepth 1 -name 'ADR-*.md' | wc -l` retorna 26 (igual ao saldo pós-Onda M); `git status --porcelain -- docs/decisions/` retorna vazio (nenhuma modificação em decisions/ raiz).
8. **Diff escopo total Bloco 1 + Bloco 2:** `git status --porcelain -- skills/new-adr/SKILL.md agents/design-reviewer.md docs/plans/onda-final-a-admission-policy-enforcement.md` lista apenas esses 3 paths como modificados/novos.

## Verificação manual

**Cenário 1 — Standalone /new-adr saída ADR:** invocar `/new-adr "Política X reversível"` diretamente (não via /triage). Esperado: step 3.5 dispara enum `Filtro`; operador escolhe `ADR — decisão estrutural reversível (Recommended)`; fluxo prossegue para step 4 (criar arquivo) sem interrupção. Saída padrão preserved.

**Cenário 2 — Standalone /new-adr saída CLAUDE.md (filtro flagra entendimento estabilizado):** invocar `/new-adr "Esclarecimento sobre default conservador no /triage"`. Esperado: operador escolhe `CLAUDE.md ou philosophy.md — entendimento estabilizado`; skill para sem criar arquivo; reporta destino alternativo + sugere edit em CLAUDE.md + commit `docs:`/`chore:` conforme convenção.

**Cenário 3 — Standalone /new-adr saída git log (evolução de processo):** invocar `/new-adr "Refactor interno do parsing do schema YAML"`. Esperado: operador escolhe `git log — evolução de processo`; skill para sem criar arquivo; reporta que substância vai apenas em commit message.

**Cenário 4 — Delegação /triage step 4 → /new-adr (caminho-com-plano + ADR):** rodar /triage que escolha caminho ADR; step 4 delega `/new-adr` via `Skill` tool. Esperado: step 3.5 dispara enum no /new-adr; `(Recommended)` em `ADR` reduz fricção (default forte); operador confirma `ADR` em 1 clique (re-confirmação per ADR-045 belt-and-suspenders); fluxo prossegue. +1 clique vs sem step 3.5 — overhead UX aceitável per decisão caminho A.

**Cenário 5 — design-reviewer flagra drift pós-criação (default conservador):** operador escolhe `ADR` no step 3.5 (caminho default), mas substância do draft revela entendimento estabilizado (não cenário concreto de reversão; sem categoria nova; etc.). Esperado: design-reviewer no step 5 emite finding "candidato a ADR draft falha no filtro de admissão (substância é entendimento estabilizado que deveria ir pra CLAUDE.md)"; operador absorve pre-commit per ADR-053 § Decisão (c) — finding tipicamente cai em **caminho-único** (substância "falhou no filtro" não satisfaz condição (i) "≥2 alternativas legítimas competindo" nem (ii) "contradiz decisão documentada" — falhar no filtro é exatamente seguir o filtro corretamente). Operador decide: (a) refinar ADR draft com cenário concreto de reversão (cumpre filtro mantendo ADR); (b) abandonar ADR draft (delete + redirect substância para CLAUDE.md/philosophy.md per critério de desempate de ADR-045 § Decisão parte 2). Disparo de cutucada AskUserQuestion **apenas** se ≥2 saídas legítimas competirem (ex.: substância sit on the fence entre `CLAUDE.md` e `philosophy.md` — condição (i) ativa).

## Notas operacionais

**Convenção decimal-retroativa step 3.5 — 1ª aplicação honesta.** Step 3.5 intercalado entre step 3 e step 4 sem renumeração dos demais. **Esta é a 1ª aplicação da convenção decimal-retroativa** nas 9 skills do toolkit (precedente `/run-plan §3.5` é decimal **sequential** após §3.4, não decimal-retroativo intercalado entre inteiros). ADR-045 § Decisão parte 2 linha 88 sugeriu explicitamente "step novo (provavelmente 3.5)" — esta onda honra a sugestão literal do ADR Aceito. Trade-off vs cascade simples (steps 4+5 → 5+6): preserva cross-refs históricas a "step 5" (revisão pré-retorno) intactas + honra ADR-045 literal; aceita 1ª aplicação convenção sem precedente. **Gatilho de revisão da convenção:** se 2ª/3ª inserção decimal-retroativa em outra skill mostrar inconsistência editorial, considerar codificar como pattern canonical (ADR sucessor ou diretriz canonical via `templates/plan.md` paralelo a Onda K').

**`(Recommended)` em `ADR` no enum step 3.5.** Default estatisticamente estável: maioria das invocações de /new-adr vem de /triage step 4 delegação que já decidiu "ADR" upstream; standalone /new-adr também tipicamente intent "criar ADR". `(Recommended)` ancora default; saídas `CLAUDE.md/philosophy.md` e `git log` são exceções intencionais. Per CLAUDE.md "AskUserQuestion mechanics" linha "Recommended só quando default é estatisticamente estável" — critério satisfeito.

**Cláusula default-conservadora ADR-045 § Decisão parte 2 linha 83 preservada literal.** Dúvida na classificação → operador escolhe `ADR` (default Recommended); design-reviewer no step 5 audita drift pós-criação. Não criar ADR por inércia retórica; não suprimir ADR por economia editorial.

**Onda Final A gateia Onda Final B (release v3.0.0).** Per ADR-045 § Condição de validade do enforcement linha 90: "bump v3.0.0 condiciona a essa garantia: política sem enforcement é decoração doutrinal". Pós-Onda Final A merge, condicionante satisfeita (≥1 superfície runtime efetiva — na verdade 2: step 3.5 + design-reviewer). Onda Final B pode disparar `/release v3.0.0` per spec.

**Pendência editorial registrada** (não-bloqueante para Onda Final A): /triage step 3 tabela canonical de caminhos (`Só linha BACKLOG` / `Plano em docs/plans/` / `ADR via /new-adr` / `Atualizar docs/domain.md` / `Atualizar docs/design.md`) **não inclui** "atualizar CLAUDE.md/philosophy.md" como caminho explícito — gap doutrinal vs filtro 3 saídas de ADR-045 (`ADR` / `CLAUDE.md ou philosophy.md` / `git log`). Não é escopo desta onda; pode emergir como pattern editorial futuro. **Cenário concreto UX a vigiar:** operador via /triage step 3 escolhe `ADR via /new-adr` (única saída tipo-ADR na tabela canonical); step 3.5 de /new-adr cutuca para `CLAUDE.md/philosophy.md`; operador volta loop. Fricção dupla é sinal de que /triage step 3 precisa incorporar as 3 saídas de ADR-045 como caminhos explícitos. **Gatilho de revisão concreto:** 2+ invocações reportando fricção dupla nesse loop dispara refinamento de /triage step 3 — caminho via ADR sucessor de ADR-045 refinando decision tree OU pattern editorial cabível em modo ADR-052 a/b/c se categoria sub-3c-like emergir.

**Risco a vigiar nesta onda:** step 3.5 fricciona delegação /triage step 4 acima do tolerável → operador reverte para fallback B (apenas design-reviewer) per § Condição de validade. Mitigação: `(Recommended)` em `ADR` reduz fricção a 1 clique de confirmação; design-reviewer audita drift independente. Reabrir se 2+ invocações reportarem fricção excessiva — gatilho de revisão do step 3.5.

**Pós-merge:** post-merge chore atualizando charter linha 192+ (Onda Final A shipped) + BACKLOG umbrella linha 5 segmento Onda Final A. Pattern paralelo a chores Onda M (`7b16b3b`), L (`2f72795`), Promoção II (`98ac852`), K' (`ff41dba`), K (`1a28201`). Após chore, /triage Onda Final B (release v3.0.0) liberada.

## Decisões absorvidas

- Cenário 5 da § Verificação manual: cross-ref `ADR-026 condição (ii)` substituído por `ADR-053 § Decisão (c) condição (ii)` (ADR-026 archived na Onda I via ADR-053); lógica do cenário 5 reescrita para refletir runtime real do design-reviewer per ADR-053 § Decisão (c) — finding tipicamente cai em caminho-único (substância "falhou no filtro" não satisfaz condição (i) "≥2 alternativas competindo" nem (ii) "contradiz decisão documentada"); cutucada AskUserQuestion apenas se ≥2 saídas legítimas competirem (caminho-único — F1 reviewer).
- Bloco 1 step 3.5 saída `git log` § Pós-decisão: adicionada nota orientacional honesta "chegar a /new-adr standalone com saída git log tipicamente sinaliza erro de framing upstream" + sugestão de refinamento futuro do /triage step 3 critério de entrada (caminho-único — F3 reviewer).
- Bloco 2 texto do bullet design-reviewer: "Finding pré-criação" substituído por "Finding pré-commit do ADR draft criado" + cláusula explicitada "reviewer roda em /new-adr step 5 após operador ter escolhido `ADR` no step 3.5" — fidelidade ao runtime real per ADR-053 § Decisão (b) (caminho-único — F6 reviewer).
- § Verificação end-to-end critério 5: awk pattern refinado para `^## [A-Z]` delimitador (robustez per diretriz Onda K' #2 vs `^## ` qualquer que cobria falso-positivo em hipotético sub-`## ` errôneo) (caminho-único — F5 reviewer).
- § Notas operacionais "Convenção decimal-retroativa step 3.5 — 1ª aplicação honesta": precedente `/run-plan §3.5` declarado fraco (decimal sequential vs decimal-retroativo intercalado); registro honesto de 1ª aplicação convenção sem invocar paralelo inexistente; gatilho de revisão registrado para 2ª/3ª inserção decimal-retroativa futura (cutucada F2 reviewer absorvida opção (b) manter 3.5 intercalado — ADR-045 § Decisão parte 2 linha 88 sugeriu literal "provavelmente 3.5"; honrar sugestão upstream + preservar cross-refs históricas a step 5).
- § Notas operacionais pendência editorial: expandido com cenário concreto UX a vigiar ("operador via /triage step 3 escolhe ADR via /new-adr; step 3.5 cutuca para CLAUDE.md/philosophy.md; operador volta loop") + gatilho de revisão concreto "2+ invocações reportando fricção dupla dispara refinamento /triage step 3" (caminho-único — F4 reviewer).
