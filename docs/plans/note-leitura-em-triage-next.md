# Plano — /triage e /next leem .claude/local/NOTES.md como contexto suplementar

## Contexto

ROADMAP item 2 (commit 749896d). Convergência tripla de 3 análises: vídeo SV 2026 (MCP-to-prod feedback como design input), spec-kit (bidirectional feedback prod→spec), uso manual já estabelecido (memória `feedback_parallel_sessions.md` — exatamente o tipo de contexto cross-session que `/note` captura).

`/note` hoje é write-only por skill, read-only por humanos via `cat`. Decisões em `/triage` step 1 (carregar contexto mínimo para alinhamento de intenção) e `/next` step 1 (ranquear candidatos do backlog) ganhariam grounding quando há notas recentes mencionando trabalho em curso ou observações operacionais. Hoje o agente não consulta a store; este plano fecha o loop write→read.

**Mecanismo: prose em step 1 de ambas as skills (não frontmatter role).** Confirmado pelo operador em gap-clarification. Razão: ADR-032 define `.claude/local/NOTES.md` como "store doutrinário non-role" — consumidor não varia o path; adicionar ao frontmatter `roles.informational` contradiz a classificação e aciona Resolution protocol (probe canonical → consult CLAUDE.md → ask operator) sem sentido para path fixo. Prose preserva ADR-032 sem refinamento; instrução textual em step 1 cobre o ganho operacional.

**Escopo intencionalmente limitado a /triage + /next.** Essas são as 2 skills que consomem contexto *antes* de produzir decisão (artefato / ranking) — read-side simétrico do write-side do `/note`. As outras 3 skills doutrinariamente-adjacentes têm contexto canalizado por outro vetor:
- **`/run-plan`**: contexto de execução vem do plano + baseline; NOTES mid-execução poluiria foco operacional do loop por bloco.
- **`/debug`**: hipóteses derivam do sintoma observável (método científico); notas históricas viesariam hipótese pré-evidência.
- **`/draft-idea`**: entrevista estruturada one-shot por design (ADR-027); NOTES contaminaria fresh elicitação de `product_direction`.

Se uso real revelar gap em uma dessas 3 (ex.: operador relata "perdi contexto entre /run-plan de sessões paralelas"), reabrir wiring para a skill específica via novo `/triage`.

**Placement: leitura como sub-passo ADICIONAL em step 1, após os 5 sub-itens existentes em `/triage` (após `decisions_dir`) ou após a leitura do backlog em `/next`.** Posicionamento "depois" porque NOTES é contexto suplementar — não substitui os papéis estruturais; supplementa quando há.

**ADRs candidatos:** ADR-032 (define non-role do store `/note` e independência do role contract), ADR-005 (modo local-gitignored — leitura ocorre de path gitignored), ADR-003 (frontmatter roles — fundamenta por que NÃO entra em frontmatter).

**Linha do backlog:** plugin: /triage e /next leem .claude/local/NOTES.md como contexto suplementar

## Resumo da mudança

Edits em duas SKILLs, prose-only (frontmatter intocado em ambas):

1. **`skills/triage/SKILL.md` step 1:** adicionar sub-item 6 após o sub-item 5 (`decisions_dir`): "Se `.claude/local/NOTES.md` existir, ler na íntegra como contexto suplementar (store non-role per ADR-032; informational, nunca bloqueia). Notas recentes mencionando trabalho em curso ou observações operacionais podem informar decisão de artefato e gap clarification. **Reportar no step 1 se uma nota influenciou a leitura do pedido, ou explicitamente que o store estava presente sem material adjacente.** Ausente → skip silente."

2. **`skills/next/SKILL.md` step 1:** após a leitura do backlog (`## Próximos` extraído), adicionar parágrafo análogo: "Se `.claude/local/NOTES.md` existir, ler na íntegra para contexto suplementar de ranking — notas recentes podem revelar mudança de prioridade ou trabalho adjacente. **Reportar se uma nota influenciou o ranking, ou explicitamente que o store estava presente sem notas relacionadas aos candidatos.** Informational (per ADR-032 store non-role); nunca bloqueia."

Não toca frontmatter de nenhuma das skills. Não muda role contract. Não cria role nova. Preserva ADR-032 (`/note` continua "skill opera independente de CLAUDE.md / role contract").

## Arquivos a alterar

### Bloco 1 — leitura de .claude/local/NOTES.md em /triage step 1 + /next step 1 {reviewer: code}

- `skills/triage/SKILL.md`: em step 1 ("Carregar contexto mínimo"), após o sub-item 5 (`decisions_dir`), inserir novo sub-item 6 lendo `.claude/local/NOTES.md` condicionalmente, com cross-ref a ADR-032 (non-role), instrução explícita de reportar influência (ou ausência dela) no relato do step 1, e cláusula "informational, nunca bloqueia".
- `skills/next/SKILL.md`: em step 1 ("Ler o backlog"), após o parágrafo de extração de `## Próximos`, inserir parágrafo análogo lendo `.claude/local/NOTES.md` condicionalmente, com cross-ref a ADR-032 e instrução explícita de reportar influência (ou ausência dela) no ranking.

## Verificação end-to-end

- `grep -n "\.claude/local/NOTES" skills/triage/SKILL.md skills/next/SKILL.md` retorna ≥1 match em cada arquivo.
- `grep -n "ADR-032" skills/triage/SKILL.md skills/next/SKILL.md` retorna novo match em cada arquivo (cross-ref doutrinal).
- `grep -in "report" skills/triage/SKILL.md skills/next/SKILL.md` retorna match na nova instrução em cada arquivo (auditabilidade).
- Inspeção textual: instrução em ambas as skills contém (a) condicional "se existir", (b) classificação informational/não-bloqueante, (c) referência a ADR-032, (d) instrução de reporte.
- Frontmatter de ambas as skills intocado: `grep -A6 "^---$" skills/triage/SKILL.md skills/next/SKILL.md | head -20` mostra `roles.informational` sem entry referenciando `NOTES` ou `note`.

## Verificação manual

- **NOTES.md presente + `/triage`:** operador roda `/triage <pedido>` em projeto com `.claude/local/NOTES.md` populado; skill reporta no step 1 explicitamente: 1-2 notas relevantes ao pedido OU "store presente sem notas adjacentes ao pedido"; decisão de artefato considera o contexto quando aplicável.
- **NOTES.md ausente + `/triage`:** operador roda `/triage` em projeto sem o arquivo; nenhuma menção a NOTES no relato do step 1; fluxo segue idêntico ao atual.
- **NOTES.md presente + `/next`:** operador roda `/next`; ranking de candidatos reporta explicitamente se notas recentes informaram prioridade OU "notas presentes mas não relacionadas aos candidatos".

## Notas operacionais

- Plano single-block — sem dependências internas.
- design-reviewer dispatcha automaticamente pré-commit (ADR-011); free-read prioriza ADRs candidatos listados em `## Contexto`.
- `/note` SKILL.md **não é tocada** — leitura é responsabilidade da skill consumidora (`/triage`, `/next`); skill `/note` apenas escreve.
- CLAUDE.md role table **não é tocada** — `.claude/local/NOTES.md` permanece marcado `(plugin-internal)` non-role.
- **Crescimento monotonic de NOTES.md** (append-only por design, ADR-032 § Limitações não cobre limite de tamanho): "ler na íntegra" pode virar custo crescente em consumer de longa duração. Reavaliar quando consumer típico atingir >~500 linhas ou >~50KB — opções de retomada: cap por leitura (tail das últimas K entradas), skill complementar `/notes-prune` (já mencionada em ADR-032 § Consequências como reabertura legítima), ou índice/sumário separado. Não bloqueia escopo corrente; documentado como gatilho de revisão futura.
