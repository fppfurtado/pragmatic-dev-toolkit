# Plano — Skill /scan-mechanicality (Faceta 2 de mechanical-skills-scan)

## Contexto

Faceta 2 da decomposição arquitetural de `/mechanical-skills-scan` cristalizada em [meta-system ADR-017](https://github.com/fppfurtado/meta-system/blob/main/docs/decisions/ADR-017-decomposicao-faceta-ii-mecanicidade-universal-vs-target-specific.md). Materializa skill núcleo universal aplicando Cond 1 do [meta-system ADR-011](https://github.com/fppfurtado/meta-system/blob/main/docs/decisions/ADR-011-skill-pensamento-mcp-mecanica.md) ("esta substância markdown é mecanizável >50%?") sobre qualquer prompt em markdown — agnóstica a projeto, harness, target final.

Homing arquitetural correto: este repo (toolkit universal stack-agnóstico) per ADR-008 do meta-system. Precedente das demais facetas — Faceta 3 (refactor `/mechanical-skills-scan` no meta-system) e Faceta 4 (análise mecanicidade `prompt.py` no h3-finance-agent) aguardam interface técnica cristalizada aqui.

**Gate prescritive obrigatório** (ADR-017 § Mitigações): `design-reviewer` valida stack-agnosticism contra ≥2 inputs concretos de stacks distintos — uma SKILL.md da constelação meta + `prompt.py` do h3-finance-agent — **antes** de cristalizar interface. Operacionalizado em `## Verificação manual` deste plano + dispatch automático em `/triage` step 5 ([ADR-053](../decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b)).

**ADRs candidatos:** meta-system ADR-011 (Skill = pensamento; MCP = mecânica) cross-cutting, meta-system ADR-017 (decomposição faceta II) cross-cutting, meta-system ADR-016 (target-aware packaging) cross-cutting, [ADR-050](../decisions/ADR-050-componentes-plugin-consolidado.md) (componentes plugin — disable-model-invocation § Decisão (e); auto-gating não aplica pois skill é markdown), [ADR-051](../decisions/ADR-051-convencoes-editoriais-consolidado.md) (idioma PT-BR canonical, README EN), [ADR-008](../decisions/ADR-008-flatness-yagni-sem-defensividade-ornamental.md) (flatness do SKILL.md), [ADR-003](../decisions/ADR-003-skill-declara-roles-required-informational.md) (roles frontmatter).

**Linha do backlog:** plugin: Faceta 2 da decomposição `/mechanical-skills-scan` — materializar skill núcleo universal aplicando Cond 1 do ADR-011 do `meta-system` (julgamento "esta substância markdown é mecanizável >50%?") sobre qualquer prompt markdown (agnóstica a projeto/harness/target). Input: blob markdown arbitrário (SKILL.md, system prompt, agent.md, prompt.py, etc.). Output: classificação POSITIVO/AMBÍGUO/NEGATIVO + bullets de substância candidata + razões. Forma técnica: skill markdown (julgamento heurístico-semântico per ADR-011 § "Skill = pensamento"). Homing: este repo per ADR-008 do meta-system (toolkit universal stack-agnóstico). **Precedente das demais facetas** — Faceta 3 (refactor `/mechanical-skills-scan` em `meta-system`) + Faceta 4 (análise mecanicidade `prompt.py` em `h3-finance-agent`) aguardam interface técnica cristalizada aqui. **Gate prescritive obrigatório** no /triage: design-reviewer valida stack-agnosticism contra ≥2 inputs concretos de stacks distintos (SKILL.md da constelação meta + Python harness do h3) **antes** de cristalizar interface — registrado em ADR-017 do meta-system § Mitigações. Decisões pendentes pro /triage aqui: nome canonical (`/scan-mechanicality`?), interface técnica (path? glob? stdin?), formato de output. Contexto integral em `.claude/local/NOTES.md` § 2026-06-11. Cross-refs: ADR-017 + ADR-016 do meta-system; sessão CC `generalizacao-mecanizacao` upstream. Gatilho de execução: operador escolher.

## Resumo da mudança

Skill nova `/scan-mechanicality` no toolkit. Decisões cristalizadas neste `/triage` (operador confirmou):

- **Nome canonical:** `/scan-mechanicality` — verbo `scan` enfatiza varredura sobre artefato.
- **Interface técnica:** path único como argumento posicional (`/scan-mechanicality <path>`), paralelo a `/run-plan <slug>` / `/new-adr <título>` — 1 invocação = 1 artefato.
- **Formato de output:** markdown estruturado em PT-BR (idioma canonical do toolkit per ADR-051), com classificação POSITIVO/AMBÍGUO/NEGATIVO + bullets de substância candidata + razões objetivas.

Stack-agnosticism: skill lê o conteúdo do path como texto plano (sem parse sintático), aplica julgamento heurístico-semântico sobre a substância. Aceita qualquer extensão (`.md`, `.py`, `.txt`, sem extensão). `prompt.py` cai naturalmente no escopo — heurística avalia substância de prompt embedded em strings/heredocs, não envólucro Python.

Fora de escopo: glob/batch, stdin, output JSON, integração com pipelines downstream. Facetas 3 e 4 consumirão a interface de path único e poderão envolver loops/transformações nos respectivos repos.

## Arquivos a alterar

### Bloco 1 — Skill /scan-mechanicality {reviewer: code}

- `skills/scan-mechanicality/SKILL.md`: novo arquivo. Frontmatter com `name: scan-mechanicality`, `description` (1 linha curta em PT-BR), `roles.required: []`, `roles.informational: []`, `disable-model-invocation: false` (default per ADR-050 § Decisão (e) — 3 critérios cumulativos satisfeitos: blast radius local, sem push/PR, sem risco de loop destrutivo). Corpo PT-BR:
  - `## Argumentos`: path único como argumento posicional. Path ausente ou inválido → reportar e parar.
  - `## Passos`:
    1. Ler o conteúdo do path via `Read` como texto plano. Tratar o conteúdo como blob textual agnóstico ao envólucro sintático — quando houver prompt embedded em strings/heredocs (Python, JS, etc.), avaliar a substância do prompt, não o código de envólucro.
    2. Aplicar julgamento heurístico-semântico per Cond 1 do meta-system ADR-011 — "esta substância markdown é mecanizável >50%?". Avaliar substância (prosa heurística, decisões contextuais, julgamentos) vs mecânica (regras determinísticas, transformações declarativas, lookups de tabela).
    3. Classificar em **POSITIVO** (substância mecanizável domina, >50%) / **AMBÍGUO** (mistura sem dominante claro) / **NEGATIVO** (substância heurística-semântica domina).
    4. Enumerar bullets de substância candidata a extração mecânica (frases/blocos com mapping mecânico claro).
    5. Razões objetivas justificando a classificação.
  - `## Output canonical`: estrutura PT-BR — header com classificação, `## Substância candidata` (bullets), `## Razões` (justificativa objetiva).
  - `## O que NÃO fazer`: não modificar artefato (skill é read-only); não recomendar refactor concreto (skill é diagnóstica, não prescritiva); não escolher por extensão (heurística é semântica, não sintática).

### Bloco 2 — Discoverability no README {reviewer: doc}

- `README.md`: nova linha na tabela após `/debug` (tier de diagnóstico) descrevendo `/scan-mechanicality` em 1 linha em inglês (audience pública per ADR-051 § Decisão (b)).

## Verificação end-to-end

- `ls skills/scan-mechanicality/SKILL.md` retorna 1 linha.
- Frontmatter mecânico válido: `grep -cE '^(name|description|roles|disable-model-invocation):' skills/scan-mechanicality/SKILL.md` retorna `4`.
- Seções obrigatórias presentes: `grep -cE '^## (Argumentos|Passos|Output canonical|O que NÃO fazer)' skills/scan-mechanicality/SKILL.md` retorna `4`.
- README atualizado: `grep -cF '/scan-mechanicality' README.md` retorna ≥1.
- Inalterabilidade do CLAUDE.md: `git status --porcelain -- CLAUDE.md` retorna 0 linhas (skill não traversa Resolution protocol step 3 — sem dependência de role).

## Verificação manual

Operacionaliza o gate prescritive ADR-017 § Mitigações — exercita stack-agnosticism contra ≥2 inputs concretos de stacks distintos. Cenários obrigatórios antes de merge:

- **Cenário 1 — stack markdown nativo.** Invocar `/scan-mechanicality skills/triage/SKILL.md` (deste repo). Esperado: classificação coerente com substância heurística-semântica predominante (julgamento de gaps, decisão de artefato, bifurcações) — provável AMBÍGUO ou NEGATIVO. `## Substância candidata` enumera bullets que poderiam virar mecânica (ex.: tabela "decidir o artefato" linhas 134-141 pode ser lookup). `## Razões` cita exemplos concretos do texto.

- **Cenário 2 — stack Python (gate ADR-017 crítico).** Invocar `/scan-mechanicality` apontando para `prompt.py` do h3-finance-agent (path absoluto fora deste repo). Esperado: classificação independente do envólucro `.py` — skill avalia substância de prompts embedded em strings/heredocs, não código Python ao redor. `## Razões` justifica objetivamente sem mencionar a extensão como critério. **Gate falha se:** skill recusa input com base na extensão, exige preprocessing externo, ou emite classificação sobre código Python (lógica, controle de fluxo) em vez de substância de prompt.

Stack-agnosticism validada quando ambos cenários produzem julgamento coerente com a substância do artefato (não com o envólucro sintático). Cenário 2 é o gate crítico — falha aqui reabre Alternativa (c) do ADR-017 ou redesign de interface sem custo de churn pós-shipping.

## Notas operacionais

- **ADR não criado no toolkit nesta materialização.** Decisão upstream (meta-system ADR-017) cobre decomposição; ADR-050 toolkit cobre componentes plugin; ADR-051 cobre convenções editoriais. Sem categoria estrutural nova justificando ADR local (per ADR-034 critério mecânico — adendo vs novo ADR; nenhuma das 5 condições aplica).
- **Idioma:** PT-BR para corpo SKILL.md + output canonical (convenção do toolkit per ADR-051 § Decisão (b)); README EN (audience pública).
- **`disable-model-invocation: false`** per ADR-050 § Decisão (e) — 3 critérios cumulativos satisfeitos trivialmente (read-only, sem push/PR, sem loop destrutivo cross-turn). Auto-invocação ocasional sem path concreto absorvida como ruído tolerável. Caminho cutucado no `/triage` step 5: alternativa (b) `true` + refinar ADR-050 com critério 4 ("skill diagnóstica scope-amplo") descartada — registraria 1ª aplicação de pattern emergente, ainda prematuro para virar regra (ADR-043 § Ockham critério #4 exige ≥3).
- **Sem dependência de role:** skill não traversa Resolution protocol step 3 → não emite cutucada de descoberta → não incrementa contador de sites (ADR-046 linha 219 helper threshold permanece em 12 sites pós-`/curate-backlog`). Editorial inheritance da convenção de cutucada não aplica.
- **Downstream facetas:** Faceta 3 (refactor `/mechanical-skills-scan` no meta-system) e Faceta 4 (análise mecanicidade `prompt.py` no h3-finance-agent) consomem a interface de path único cristalizada aqui — cada uma vira `/triage` independente nos respectivos repos pós-merge desta Faceta 2.

## Pendências de validação

- ~~Cenários 1 e 2 do `## Verificação manual` (smoke real cross-stack contra SKILL.md meta + `prompt.py` do h3-finance-agent) exigem skill instalada no cache do plugin — exerciseáveis na 1ª invocação subsequente de `/scan-mechanicality` pós-merge + `/plugin update` + `/reload-plugins`. Inspeção textual inline validou estrutura mecânica (SKILL.md bem-formada, README atualizado); gate prescritive ADR-017 § Mitigações dependente de smoke comportamental real.~~ **Encerrada 2026-06-11:** execução manual nesta sessão CC (operador autorizou pós-merge) carregou SKILL.md como instrução mental e aplicou sobre os 2 cenários — Cenário 1 (`skills/triage/SKILL.md`) classificado AMBÍGUO; Cenário 2 (`/storage/dev/projects/h3/h3-finance-agent/src/agente/prompt.py`) classificado NEGATIVO. Gate ADR-017 § Mitigações passou: ambos os vereditos ancorados em substância (não envólucro sintático); `## Razões` citaram trechos do texto avaliado; estrutura de output canonical preservada. Smoke comportamental via skill instalada permanece como sanity check pós-`/plugin update` + `/reload-plugins` mas perdeu criticidade — gate prescritive resolvido empiricamente.
- ~~Critério 2 de `## Verificação end-to-end` (spec bug): `grep -cE '^(name|description|roles|disable-model-invocation):' skills/scan-mechanicality/SKILL.md` retorna **4**, não 5 como esperado — `roles.required: []` e `roles.informational: []` são nested (indentados sob `roles:`) e não casam com `^(...):`. SKILL.md está corretamente formada (frontmatter padrão); critério foi mal-especificado. Refinar para ancorar count real (4) ou usar pattern nested explícito (`^\s+(required|informational):` paralelo a `^(name|description|...):`).~~ **Encerrada 2026-06-11:** Opção 1 simplificada aplicada — count corrigido para `4` e glosa parentética descartada. Pattern nested paralelo (Opção 2) descartado: valida estrutura interna de `roles:` que ADR-003 não exige (contrato é declarar `required`/`informational`, forma interna é editorial). Condição inversa (Opção 3 per diretriz canonical Onda K' #4) descartada: diretriz mira counts que variam entre ondas; frontmatter SKILL.md tem estrutura fixa por design.

## Decisões absorvidas

- Bloco 1 `## Passos` passo 1: positivizar diretiva de stack-agnosticism (tratar conteúdo como blob textual agnóstico ao envólucro sintático; avaliar substância de prompts embedded, não código de envólucro) — gate ADR-017 § Mitigações merece pareamento defensivo no caminho positivo além do `## O que NÃO fazer` (caminho-único).
