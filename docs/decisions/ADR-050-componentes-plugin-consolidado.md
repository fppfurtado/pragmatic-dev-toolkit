# ADR-050: Componentes plugin consolidado

**Data:** 2026-05-31
**Status:** Aceito

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 1 § Implementação — esta Onda G materializa migração do cluster componentes plugin (5º cluster temático per sketch literal + refinamento editorial). Sucessor parcial de 6 ADRs sob política de consolidação.
- **Templates de migração:** [ADR-046](ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) (template Onda C — pattern de migração + F1 link rot 2 categorias + F4 cond 5 isolada + F9 fronteira ADR-024) + [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) (template Onda D — primeira sem procedure file + F2 absorção assimétrica) + [ADR-048](ADR-048-free-read-design-reviewer-consolidado.md) (template Onda E — calibração descendente + auto-consistência da always-include) + [ADR-049](ADR-049-execucao-run-plan-consolidado.md) (template Onda F — refinamento editorial documentado por exclusão + pattern editorial para G-X).
- **Decisões absorvidas (sucessores parciais primários per ADR-034 cond 5):**
  - ADR-008 (skills geradoras stack-agnósticas via dispatch interno por marker; sub-blocos canonical por stack; gatilho de revisão "stack nova adicionada");
  - ADR-013 (CI lint mínimo como categoria distinta das 3 vetadas pela frase canonical; 4 critérios cumulativos; cobertura positiva/negativa explícita);
  - ADR-015 (hook block_env por sufixo `.env`; defesa universal por filename; primeiro PreToolUse block hook do plugin);
  - ADR-016 (hook block_gitignored por sinal do consumer `.gitignore`; postura "consumer signal first"; 7 alternativas rejeitadas);
  - ADR-023 (critério mecânico cumulativo para `disable-model-invocation` explícito em SKILLs; 3 critérios; tabela retroativa às 9 skills);
  - ADR-040 (hook block_settings_drift por content regex em `.claude/settings.json`; sucessor parcial lateral de ADR-015 família PreToolUse block hooks).
- **Critério editorial:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) cond 5 (sucessor parcial primário absorvendo 6 ADRs em 1 consolidado); cond 4 **NÃO aplica** (ADR-045 carrega categoria meta da redesign; ADR-050 é quinta instância — F4 lesson Onda C reaplicada literal); cond 1 **NÃO aplica** (ADR-045/-046/-047/-048/-049 são ancestrais codificados em sequência); cond 2 **NÃO aplica** — regra central de cada ADR absorvido preservada integralmente em § Decisão (a)-(g); nenhum ADR é marcado como `Substituído`; nenhuma inversão de decisão central.
- **Link rot doutrinal ativa identificada pré-execução (categoria-b de F1 lesson Onda C):** ADR-019 (qa-reviewer ↔ /gen-tests cross-ref) cita ADR-008 como "single source of truth" em 7 ocorrências; ADR-020 (warnings pré-loop) + ADR-022 (archival docs/plans) reusam pattern "critério mecânico cumulativo" de ADR-013; ADR-027 (`/draft-idea` skill) cita ADR-008 + ADR-023 como decisões base. Substância dessas referências absorvida em ADR-050 § Decisão fecha gap; ADRs vigentes mantêm-se imutáveis (cross-refs resolvem via redirect canonical ADR-008/-013/-023 archived → ADR-050).
- **Composição vs sketch original:** sketch do charter (NOTES 2026-05-30T06:08:04Z linha 238) absorvia **5 ADRs** (008+013+016+023+040 — ADR-015 omitido). Onda G inclui ADR-015 no cluster — ADR-015 pertence semanticamente à família PreToolUse block hooks (ADR-040 § Origem explicitamente cita ADR-015 como "ancestral direto — primeiro PreToolUse block hook do plugin"); excluir deixaria órfão membro da família coesa. Inclusão cabe em ADR-045 § Decisão linha 56 fronteira *"absorção de ADR em consolidado diferente do sketch original"* como ajuste editorial. Documentação editorial post-merge consolida em charter § Atualização pós-execução.

## Contexto

A camada doutrinal do plugin pós-v2.14.0 carregava **6 ADRs vigentes** codificando dimensões dos tipos canônicos do plugin (skills/agents/hooks per CLAUDE.md "Plugin component naming and hook auto-gating") + infra do plugin (CI lint):

- **Skills convention:** ADR-008 (skills geradoras sem sufixo, sub-blocos por stack) + ADR-023 (`disable-model-invocation` explícito).
- **Hooks defensivos:** ADR-015 (block_env por sufixo `.env`) + ADR-016 (block_gitignored por `.gitignore` do consumer) + ADR-040 (block_settings_drift por regex em `settings.json`).
- **Infra do plugin:** ADR-013 (CI lint mínimo permitido).

Os 6 ADRs foram criados em sequência empírica (Maio 2026, intervalos de dias a semanas) cada um codificando uma decisão pontual em resposta a incidente concreto — sem coordenação editorial inicial. Pós-v2.14.0 reforma doutrinária (3 princípios fundamentais como raiz epistêmica per ADR-043) e ADR-045 (redesign da camada doutrinal codificando consolidação 45 → ~13-15 ADRs + política de admissão going forward), o cluster ficou identificado como candidato natural de consolidação por 3 critérios:

1. **Coesão semântica em 3 sub-dimensões** — todos os 6 codificam dimensões do que constitui "um componente do plugin" (skills/hooks/infra), com pattern recorrente "critério mecânico cumulativo" (ADR-013 estabeleceu; ADR-020+022+023 herdaram).
2. **Cross-refs múltiplos vigentes** — ADR-019/-020/-022/-027/-034/-035/-042/-046/-047 citam membros do cluster como autoridade vigente (link rot doutrinal ativa categoria-b identificada).
3. **Scope manejável dentro do pattern de migração validado** — 6 ADRs (vs 4 em D+F; 2 em C+E) testa scope máximo ascendente; pattern Onda F lessons aplicáveis (F4 cond 5 isolada + F1 link rot 2 categorias + F9 fronteira ADR-024 não aplica).

A consolidação preserva substância integralmente (todas as 7 dimensões a-g codificadas literalmente em § Decisão) e fecha link rot doutrinal ativa (substância de ADR-008/-013/-023 que ADR-019/-020/-022/-027 citam como autoridade vivendo em ADR-050). Frase canonical do CLAUDE.md "Don't introduce a build system, package manager, or test runner" permanece intacta — ADR-013 → ADR-050 § Decisão (b) preserva fronteira sem revogar a doutrina.

## Decisão

ADR-050 absorve substância integral dos 6 ADRs sob narrativa única coerente, organizada em 7 dimensões interconectadas que codificam o que constitui "um componente do plugin" e a infra que o valida:

### (a) Skills geradoras stack-agnósticas via dispatch interno por marker

**Skills geradoras (não hooks) perdem o sufixo de stack.** Idioms de cada stack vivem em sub-blocos por stack dentro do mesmo SKILL.md. A skill detecta stack por marker (idêntico ao auto-gating triplo de hooks): `pyproject.toml` → Python, `build.gradle*`/`pom.xml` → JVM, `package.json` → JS/TS, `Cargo.toml` → Rust, `go.mod` → Go.

**Hooks mantêm sufixo de stack** e auto-gating triplo (file extension → stack marker → toolchain). A separação skill-vs-hook na convenção fica formalizada — hooks firam sozinhos em todo projeto onde o plugin está instalado e exigem auto-gating defensivo; skills são invocadas pelo operador e ganham UX uniforme cross-stack.

**Escopo da inversão:**
- **Aplica-se:** skills cujo nome carrega `<verb>-<artifact>-<stack>`. Hoje, apenas `gen-tests` (Python sub-bloco; sufixo `-python` removido em sucessão a este ADR).
- **Não aplica-se:** hooks (`run_pytest_python.py`, futuros `run_gradle_test_java.sh`) e agents stack-specific (`<role>-<stack>`, hipotéticos hoje).

**Mecânica de detecção e fallback:**
- **Marker único** detectado → despacha para o sub-bloco da stack identificada.
- **Marker ausente** → skill pergunta ao operador via `AskUserQuestion` (header `Stack`) com as stacks que têm sub-bloco como opções.
- **Múltiplos markers** (monorepo) → mesma pergunta, com aviso explícito dos markers detectados.
- **Stack detectada sem sub-bloco implementado** → skill para com mensagem clara (`"stack <X> detectada mas sub-bloco ausente em skills/<nome>/SKILL.md"`).

**Single source of truth preservado:** idioms canonical por stack vivem em `skills/<gerador>/SKILL.md` sub-bloco da stack (substância de ADR-008). Agents reviewers (qa-reviewer) **referenciam** sub-blocos via cross-ref, **não duplicam** — relação codificada em ADR-019 (preservado vigente) com cross-ref a ADR-008 que agora resolve via redirect canonical para esta § Decisão (a). Convergência conceitual com pipeline de domínio (`philosophy.md` "Convenção de naming" + pipeline `**Termos ubíquos tocados:**`). Stack nova adicionada via sub-bloco em `/gen-tests` (gatilho explícito desta dimensão) ganha cobertura automática do eixo de revisão.

**Artefatos não-código** (skills geradoras cujo output é produto, não código — ex.: `/draft-idea` produz `IDEA.md`) operam no caminho stack-agnóstico — sem auto-detection por marker, sem sub-blocos por stack. Pattern preservado per ADR-027 § Decisão (referência categoria-b absorvida).

### (b) CI lint mínimo como categoria distinta das 3 vetadas pela frase canonical

**Frase canonical do CLAUDE.md preservada intacta:** "Don't introduce a build system, package manager, or test runner for this repo itself. The hooks are runnable Python scripts; the rest is markdown." CI lint mínimo de invariantes de manifest e sintaxe de hooks **não cabe em nenhuma das 3 categorias vetadas** (não compila, não instala dependências, não roda testes). Este ADR formaliza a fronteira sem abrir exceção na frase canonical — cross-ref de 1 linha à dimensão (b) delega delimitação sem editar a doutrina.

**Critério mecânico cumulativo** (todos os 4 devem aplicar):

1. Valida invariantes **sintáticas** (parse de JSON/YAML/Python AST) ou **estruturais mínimas** (chaves obrigatórias presentes em manifests).
2. Sem instalação de dependências externas além do runtime base do runner (Python ≥3.10 default em ubuntu-latest).
3. Sem execução de behavior de produção — não roda hooks, não invoca skills/agents, não dispara workflow do plugin.
4. Tempo de wall-clock < 30s no runner default.

**Cobertura positiva** (gates dentro do escopo):
- `python -m json.tool` em `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `hooks/hooks.json`.
- `python -c "import ast; ast.parse(...)"` em cada `hooks/*.py`.
- Assertions inline em `python -c` para chaves obrigatórias dos manifests.
- Frontmatter parse de `skills/*/SKILL.md` e `agents/*.md` (`name:`, `description:` presentes) — aceitável sob o critério; permanece fora da cobertura atual do CI lint conforme decisão original (escopo controlado da primeira iteração); reabertura via gatilho específico.

**Cobertura negativa** (fora do escopo, permanece vetado pela frase canonical):
- Suite de testes do próprio plugin (test runner).
- Package install no CI (package manager).
- Build pipeline (build system).
- Schema validation completa via `claude plugin validate` (exige setup de CLI Claude; fica como gatilho de revisão).
- Lint de estilo (`markdownlint`, `yamllint`, `ruff format`) — estilo ≠ invariante.

### (c) Hook PreToolUse block_env por sufixo `.env` (defesa universal)

**Primeiro PreToolUse block hook do plugin.** Estabelece pattern de gate por filename match com escape hatch documentado. Bloqueia qualquer arquivo cujo nome termine em `.env`, preservando exceções para templates.

**Predicado** (após strip de `TEMPLATE_SUFFIXES`):
- Termina em `.env` (cobre `.env`, `1g.env`, `production.env`, `1g.integ.env`); **ou**
- Começa com `.env.` (cobre `.env.production`, `.env.local`);
- **Exceto** quando termina em `.env.example` (espelha exceção atual para qualquer prefixo: `1g.env.example`, `production.env.example`).

**Política universal** — não inspeciona conteúdo; não respeita carve-out de `.claude/` que aplica a block_gitignored. Cenário concreto: `.claude/local/secrets/1g.env` é bloqueado, mesmo sob território do operador. Editar `*.env` legítimo nesses contextos exige template `*.env.example` versionado + processo de deploy, override pontual fora do Claude, ou pedir bypass explícito.

**Defesa não-bypass-proof** — operador pode editar fora do Claude (escape hatch universal). Hook é gate defensivo, não política de segurança forçada.

### (d) Hook PreToolUse block_gitignored por sinal do consumer (consumer signal first)

**Segundo PreToolUse block hook do plugin.** Bloqueia qualquer edit em path coberto pelo `.gitignore` do consumer. Postura: sinal vem de intenção declarada do repo (`.gitignore`), não de heurística codificada — robusto a stacks novas sem alterar o hook.

**7 alternativas rejeitadas** (registradas para evitar reabertura cíclica):
- (a) Allowlist via `pragmatic-toolkit:config` — viola "hooks sem flags nem env vars".
- (b) Operador adiciona `!entry` ao `.gitignore` + `skip-worktree` — muda contrato organizacional do arquivo.
- (c) Hook não bloqueia paths na raiz do repo — heurística codificada substitui parcialmente o sinal.
- (d) Status quo com override manual — atrito sem caminho institucional.
- (e) Opt-in via env var / flag — contraria "hooks sem flags nem env vars".
- (f) Parser de `.gitignore` para classificar padrões — heurística sobre heurística.
- (e′) Híbrido (c) + lista hardcoded de extensões — tabela de patches infinitos.

**Pattern do consumer não-acomodado no plugin.** Script gitignored como entrypoint de workflow (caso PJe TJPA `build_pje.sh`/`start_pje.sh`) é responsabilidade do consumer refatorar via Makefile/Docker/compose. Plugin preserva integralmente Path contract (sinal vem do consumer) e doutrina de naming/auto-gating de hooks (sem flags, sem env vars, sem config-aware).

**Carve-out de `.claude/`** allowlisted (território do harness; load-bearing para modo local-gitignored per ADR-047). Hook é auto-gated em três camadas (file_path vazio / fora de repo git / `git` ausente do PATH → no-op silencioso); quando dispara, executa `git check-ignore` uma vez e bloqueia (exit 2) se path coberto.

### (e) Critério mecânico cumulativo para `disable-model-invocation` explícito em SKILLs

**Toda `SKILL.md` do toolkit declara `disable-model-invocation` explicitamente no frontmatter** (sem omissão) com valor dado por critério mecânico cumulativo.

**Declara `false`** quando **todos** os critérios valem:

1. **Blast radius estritamente local pela ação direta da skill.** Mutação restrita ao working tree do consumer (arquivos, commits locais, criação/edição de worktrees). Push para remote, abertura de PR/MR, ação destrutiva remota, mensagem externa ou efeito imediato em sistema cross-team **não** contam como "local".
2. **Pushes/PRs gateados por enum upstream contam como local.** Quando push só acontece após `AskUserQuestion` cancel-friendly que o operador pode interromper, o gate é a fronteira, não a ação. A skill mantém blast-radius classificado pelo que faz **antes** do gate.
3. **Sem risco de autoinvocação recursiva destrutiva pelo modelo.** A execução da skill não pode disparar autoinvocação cross-turn da própria skill (ou de outra skill `disable-model-invocation: false`) em loop não-terminado por gate operador. **Não conta:** loop interno determinístico dentro do mesmo turn — cláusula visa dispatch do modelo entre invocações, não iteração intra-turn.

**Declara `true`** quando **qualquer** critério falha — ação direta cross-team (push automático sem gate, release publicada, mensagem externa enviada), ou risco de loop autoinvocado cross-turn pelo modelo.

**Tabela retroativa às 9 skills shippadas** preservada literal de ADR-023 § Aplicação (todas declaram `false`; zero declaram `true`; universo válido hoje):

| Skill | Valor | Justificativa pelo critério |
|---|---|---|
| `/triage` | `false` | Push pós-commit no caminho-com-plano é gateado pelo enum `Commit` upstream (commit+push como unidade atômica). Push do step 0 cleanup (`git push origin --delete`) é opt-in explícito por candidato no `multiSelect` (default desmarcado → skip). Antes dos gates, mutação é local. Sem loop autoinvocado. |
| `/run-plan` | `false` | Opera em worktree isolada, micro-commits locais. Push é gateado pelo enum `Publicar`. Sem loop. |
| `/new-adr` | `false` | Cria 1 markdown local. Não commita. Sem push. Sem loop. |
| `/release` | `false` | Bump local + commit local + tag local. **Push permanece manual** (operador executa `git push --follow-tags` fora da skill). Blast radius da skill é estritamente local. Sem loop. |
| `/debug` | `false` | Produz diagnóstico em texto na conversa. Não escreve código, não cria commit, não aplica instrumentação. Blast radius zero no working tree. Sem loop. |
| `/gen-tests` | `false` | Gera arquivo de teste local. Não commita. Sem push. Sem loop. |
| `/next` | `false` | Lê backlog, propõe candidatos. Movimentações em backlog são gateadas pelo enum `Movimentações`. Sem loop autoinvocado. |
| `/init-config` | `false` | Muta `CLAUDE.md` (escrita direta após coleta interativa role-a-role via `AskUserQuestion`), `.gitignore` (gate `Gitignore` aplicado pelo modo `local` quando primeira escrita sob `.claude/local/` ocorre — fora desta skill), `.worktreeinclude` (escrita determinística sem `AskUserQuestion` — resultado óbvio, sem trade-off cross-team). Todas mutações no working tree do consumer; sem push, sem loop. Mutação cross-skill de config compartilhada **não** quebra "blast radius local" — fronteira do critério é cross-team, não cross-skill. |
| `/archive-plans` | `false` | Preview-first + enum `Aplicar/Cancelar`. `git mv` local + commit local. Sem push. Sem loop. |

Skill futura com `true` justifica explicitamente citando este ADR no próprio `SKILL.md` (paralelo à herança editorial de ADR-046 § Editorial inheritance). Convenção sustentada por `code-reviewer` e revisor humano em PRs introduzindo SKILL.md novo — sem enforcement mecânico.

### (f) Hook PreToolUse block_settings_drift por content regex em `.claude/settings.json`

**Terceiro PreToolUse block hook do plugin.** Sucessor parcial lateral de dimensão (c) (família PreToolUse block hooks). Bloqueia drift de paths absolutos em arquivo tracked específico.

**4 cláusulas:**

1. **Target file específico**: bloqueio só dispara quando `tool_input.file_path` termina em `.claude/settings.json` exatamente. `.claude/settings.local.json` fora do escopo (gitignored, paths absolutos lá são esperados).

2. **Content patterns via regex bruta**: scan do conteúdo novo (campo `content` para `Write`, `new_string` para `Edit`) por regex `/home/[^/]+/` ou `/Users/[^/]+/`. Match → bloqueia. Sem match → exit 0.

3. **Escape hatch documentado**: 3 caminhos conhecidos — (a) mover para `settings.local.json`; (b) substituir por variável (`$HOME/`, `~/`) que regex não casa; (c) editar via outras ferramentas fora do Claude Code. Mensagem stderr do hook lista os 3.

4. **Windows fora de escopo desta versão**: regex não cobre `C:\Users\<user>\` ou prefixos Windows. Plugin é primariamente Linux/macOS; sem incidente Windows reportado. Reabrir em ADR sucessor se incidente surgir.

**Tensões com sub-decisões anteriores defendidas:**
- **Tensão com ADR-018 / ADR-047 (`.claude/` território Claude Code)**: invariante proíbe **modificação proativa** do território (criação de arquivos, edição automática, replicação). Hook PreToolUse é categoria distinta — gate defensivo (exit 2 informativo) sobre conteúdo que o operador estaria escrevendo. Plugin não escreve, não cria, não move arquivo em `.claude/`.
- **Tensão com dimensão (d) "consumer signal first"**: dimensão (d) cobre caso onde sinal do consumer já existe (`.gitignore`). Aqui o objeto protegido é tracked por design Claude Code (sem `.gitignore` a respeitar); pattern protegido é universal (paths absolutos `/home/<user>/` nunca pertencem a settings tracked).
- **Tensão com dimensão (c) § Alternativa (d) content-inspection no hot path**: defesa por escopo restrito viabiliza — file alvo único + formato estável JSON + regex curto + ganho não-marginal (`/insights` report).

### (g) Pattern "critério mecânico cumulativo" como meta-doutrina herdada

**Pattern editorial estabelecido por dimensão (b) § Critério mecânico.** Replica-se quando uma categoria cresce além do data point original e exige classificação preventiva (gate de CI lint; warning de qualidade-de-mudança; candidato a arquival; valor de `disable-model-invocation` em skill nova).

**Reusos documentados** (preservados vigentes após Onda G):
- **ADR-020** (criterio-mecanico-admissao-warnings-pre-loop): 3 cumulativos + 1 pré-requisito explícito; cita dimensão (b) como precedente direto.
- **ADR-022** (politica-archival-docs-plans): 6 critérios cumulativos paralelos; cita dimensão (b) + ADR-020.
- **Dimensão (e) deste ADR** (`disable-model-invocation`): 3 cumulativos; pattern reusado internamente.

Pattern editorial preservado em ADR-050 § Decisão (b) + (e) + (g); ADR-020 e ADR-022 mantêm-se vigentes citando pattern via referência ao consolidado. Substância "critério mecânico cumulativo" como meta-doutrina não pode ser perdida — anti-regression checklist § Convenções editoriais do charter preserva.

## Origem histórica

Cada dimensão consolida 1 incidente empírico, preservado integralmente na trilha histórica:

- **Dimensão (a)** — Sessão sobre cobertura de teste em features multi-arquivo (2026-05-07) expôs 2 dores em `gen-tests-python`: (i) per-arquivo (N invocações para feature multi-módulo); (ii) per-stack (sufixo obriga lembrar variante). A primeira é assinatura; a segunda é doutrinária. Convenção atual em `philosophy.md` "Convenção de naming" foi escrita com um único data point (`gen-tests-python`); refinamento distinguiu skills (interface ao operador) de hooks (auto-fira).

- **Dimensão (b)** — Sessão `/triage` 2026-05-10 do item "marketplace prep #6" do BACKLOG. `design-reviewer` reabriu tensão com frase canonical do `CLAUDE.md` — `Exception: minimal CI lint` lia como introdução de classe nova de artefato, não como esclarecimento de zona não-coberta. Memória `feedback_adr_threshold_doctrine` aplicou. Classe de bug "release quebrada por typo" emergiu empiricamente no batch 1 da marketplace prep: `claude plugin validate` rejeitou `marketplace.json` por `$schema` URL fake (404) e `description` em path top-level errado. Esses erros ficaram instalados no repo até o batch 1 sem nenhum gate.

- **Dimensão (c)** — Smoke-test do plugin no projeto Java PJe (TJPA) reproduziu cenário em que `envs/1g.env` — contendo credenciais reais de DB — passou sem bloqueio pelo `block_env.py`. Registro completo em `.claude/pragmatic-toolkit-validation.md` do PJe, achado #1 da fase 1. Heurística dotfile-only refletia convenção Python/Node; ecossistemas Java/PHP/Rails usam env-file por instância (`<nome>.env`) que escapava do regex.

- **Dimensão (d)** — Smoke-test do plugin v2.3.0 no projeto Java PJe (TJPA) reproduziu falso-positivo do `block_gitignored.py` em scripts operacionais (`build_pje.sh`, `start_pje.sh`) — pontos de entrada do workflow de build/run local, gitignored via `*.sh` no `.gitignore` do consumer. Registro em `.claude/pragmatic-toolkit-validation.md` do PJe, achado #12 da fase 1. Triage 2026-05-10 avaliou 7 alternativas; todas com fricção doutrinária ou operacional inaceitável. Achado decisivo: pattern do consumer tem **solução pronta no ecossistema** (Makefile + Docker/compose) que não exige mudança no plugin.

- **Dimensão (e)** — Auditoria editorial 2026-05-12 (`docs/audits/runs/2026-05-12-architecture-logic.md` § 3) diagnosticou drift editorial — 5 skills (`/triage`, `/debug`, `/gen-tests`, `/next`, `/init-config`) omitiam o campo enquanto 4 declaravam explicitamente `false`. Plano `tightening-editorial-auto-loaded` (Onda 2 das auditorias) recebeu 2 findings altos do `design-reviewer`: (1) wording em embrião do critério criava 3 ambiguidades quando aplicado retroativamente (`/triage` faz `git push` gateado, `/init-config` muta arquivos do consumer, `/release` é local mas exemplo inicial classificava push de release como `true`); (2) formalizar critério parcial documentado é ADR-worthy.

- **Dimensão (f)** — `/insights` report (2026-05-26, 166 sessões analisadas) confirma múltiplos cleanup cycles em `.claude/settings.json` por session permission entries e absolute paths, exigindo cleanup commits repetidos antes de release. ROADMAP item 5 da Onda 1 do plugin todo (commit `d9e8896`) — último pendente, único item de hygiene de execução não-coberto pelas waves anteriores.

§ Gatilhos abaixo consolida triggers das 6 decisões em formato unificado.

## Consequências

### Benefícios

- **Cluster componentes plugin migrado em 1 ADR** (vs 6 fragmentados) — leitura linear das 7 dimensões interconectadas em vez de cross-refs entre 6 arquivos.
- **Link rot doutrinal ativa categoria-b fechado** — substância citada por ADR-019/-020/-022/-027 absorvida em § Decisão; ADRs vigentes preservados sem edição (imutáveis); cross-refs resolvem via redirect canonical.
- **Frase canonical do CLAUDE.md preservada intacta** — dimensão (b) formaliza fronteira sem revogar; precedente para futuras zonas cinza na infra do plugin.
- **Pattern editorial "critério mecânico cumulativo" centralizado** — dimensão (g) preserva meta-doutrina; ADR-020/-022 vigentes mantêm cross-ref via redirect.
- **Família PreToolUse block hooks unificada** — dimensões (c)+(d)+(f) coexistem em 1 ADR com defesa em camadas explícita; cada hook tem política própria sobre classe específica sem sobreposição.
- **Single source of truth para idioms por stack preservado** — ADR-019 cross-ref permanece coerente via dimensão (a) absorvida.

### Trade-offs

- **6 ADRs arquivados** — drop líquido de 5 no inventário (maior drop até hoje; alinha com scope máximo do cluster). Cross-refs em immutable docs (ADRs antigos + planos históricos) ficam como link rot consciente categoria (a) — redirect canonical em archive fecha o gap.
- **§ Decisão extensa (7 dimensões)** — leitor que busca regra pontual precisa scrollar por mais dimensões. Mitigação: sub-headers `§ Decisão (a/b/c/d/e/f/g)` permitem cross-ref preciso; pattern editorial Onda E (sub-headers em ADR-048) reaplicado.
- **Aderência estrita reviewer-per-bloco** — pendência operacional Onda F endereçada; convergência empírica em Ondas C+D+E+F não justifica skip do doc-reviewer no Bloco 1 (archive). Convergência empírica não admite exceção à doutrina explícita "Não pular revisor".

### Limitações

- **Gap operacional `block_gitignored.py` preservado** (NOTES 2026-05-30T05:26:59Z): mensagem do hook assume 3 categorias enumeradas (dependency, build artifact, local cache) sem reconhecer 4ª categoria (store doutrinário declarado por ADR-047 + ADR-032 — `.claude/local/` como source primária de captura). Operador fica sem caminho canonical para re-edição (workaround: `cat > tmp + mv` em Bash; `/note` skill bypassa via `cat >>` append puro). Endereçamento ainda pendente; reservar espaço de extensão. Charter linha 87 antecipou esta preservação per ADR-045 § Implementação.
- **Heurística continua sobre nome de arquivo** (dimensão (c)) — arquivo com `KEY=VALUE` que não termine em `.env` continua escapando (status quo, sem ambição de cobrir).
- **Defesa não-bypass-proof** (dimensões (c)+(d)+(f)) — operador pode editar fora do Claude Code (escape hatch universal). Hooks são gates defensivos, não política de segurança forçada.
- **Sem enforcement mecânico** para `disable-model-invocation` (dimensão (e)) — skill nova esquecendo a declaração cai no default da harness. Herança é editorial (paralelo a ADR-046 § Editorial inheritance). Validação automática no CI lint (dimensão (b)) está fora-de-escopo desta iteração.
- **Schema completo via `claude plugin validate` fora do CI lint** (dimensão (b)) — instalação do CLI no runner é setup desproporcional. Reentrada como gatilho de revisão.
- **Windows fora de escopo** (dimensão (f)) — sem incidente reportado para justificar cobertura.

### Mitigações

- **Anti-regression checklist § Componentes do plugin + § Skills e fluxo + § Convenções editoriais** atualizado em charter post-merge garante substância das 7 dimensões preservada em validação operacional de ondas H-X (design-reviewer aplica checklist como rubric extra).
- **Substância para link rot categoria-b** preservada literal em § Decisão (a) + (b) + (e) + (g) — design-reviewer e doc-reviewer auditam fidelidade vs ADR-008/-013/-015/-016/-023/-040 originais.
- **Pendência operacional Onda F endereçada como invariante desta onda** — Bloco 1 (archive) DEVE invocar `doc-reviewer` obrigatório.
- **Inclusão de ADR-015 ao cluster vs sketch documentada** em § Origem ("Composição vs sketch original") + charter § Atualização pós-execução post-merge — cabe em ADR-045 § Decisão linha 56 fronteira "absorção em consolidado diferente do sketch".

## Alternativas consideradas

### (a) Manter 6 ADRs vigentes (status quo)

Status quo pré-Onda G. Descartado: cluster identificado em ADR-045 § Decisão parte 1 § Implementação como candidato natural de consolidação; link rot doutrinal ativa categoria-b em 4 ADRs vigentes (-019/-020/-022/-027) reabre cada vez que reader busca substância citada; redesign declarou consolidação como invariante doutrinal pós-v2.14.0.

### (b) Consolidar em sub-clusters menores (skills / hooks / infra separados)

Criar 3 ADRs consolidados (ADR-050 skills [008+023]; ADR-051 hooks [015+016+040]; ADR-052 infra [013]) em vez de 1. Descartado:
- **Spírito ADR-045**: target 13-15 ADRs vigentes; sub-clusters multiplicariam ADRs sem ganho proporcional.
- **Coesão semântica ampla**: as 3 sub-dimensões coexistem como componentes do plugin per CLAUDE.md "Plugin component naming and hook auto-gating" — separação artificial perderia narrativa.
- **Pattern editorial "critério mecânico cumulativo"** (dimensão g) transcende sub-clusters — codificar em ADR único alinha pattern central.
- **Family PreToolUse block hooks** (c+d+f) explicitamente conectada via § Origem de ADR-040 ("ADR-015 é ancestral direto") — separar quebraria narrativa de defesa em camadas.

### (c) Excluir ADR-013 (CI lint) do cluster por pertencer a "infra/release pipeline"

Refinamento editorial F-pattern por exclusão similar a ADR-037 da Onda F. Descartado:
- **Coesão semântica preserved**: CI lint mínimo é codificado em CLAUDE.md "Editing conventions" bullet imediatamente após "Don't introduce a build system" — frase canonical do plugin sobre componentes/infra.
- **Pattern "critério mecânico cumulativo"** estabelecido por ADR-013 é herdado por ADRs (e) e (g) deste ADR — separar quebraria pattern editorial central.
- **Sem cluster alternativo natural**: nenhum outro cluster da redesign (cutucadas/modo local/reviewers/execução/alinhamento/convenções) absorveria ADR-013 com coesão clara.

### (d) Manter ADR-015 fora do cluster (seguir sketch original literal)

Sketch original do charter omitia ADR-015. Onda G poderia seguir literal (cluster de 5: 008+013+016+023+040). Descartado:
- **Família PreToolUse block hooks** explicitamente codificada em ADR-040 § Origem ("ADR-015 é ancestral direto — primeiro PreToolUse block hook"): excluir deixaria órfão membro da família coesa.
- **Inclusão de ADR-015 ao cluster** cabe em ADR-045 § Decisão linha 56 fronteira "absorção de ADR em consolidado diferente do sketch original" como ajuste editorial livre.
- **Defesa em camadas** (dimensões c+d+f) ganha narrativa única coerente; separar ADR-015 dilui defesa em camadas.

### (e) Absorver também ADR-019 (qa-reviewer ↔ /gen-tests)

ADR-019 cita ADR-008 como autoridade vigente em 7 ocorrências; absorvê-lo no cluster fecharia link rot doutrinal ativa diretamente em vez de via referência. Descartado:
- **Categoria semântica distinta**: ADR-019 codifica relação **inter-componente** (reviewer ↔ skill geradora), não convenção interna do plugin (skills/hooks/infra).
- **Pertenceria a cluster reviewers/curadoria**: cluster Onda E (ADR-048) já consolidou reviewers sem absorver ADR-019. Absorver agora seria revisão estrutural de ADR-048.
- **Substância preservada via cross-ref**: ADR-019 mantém-se vigente; redirect canonical de ADR-008 archived → ADR-050 § Decisão (a) preserva "single source of truth" coerência.

## Auto-aplicação per ADR-034

ADR-050 é ele próprio refinamento doutrinal — codifica regra que vivia distribuída em 6 ADRs vigentes. Pela classificação editorial de ADR-034:

- **Cond 5 (sucessor parcial primário absorvendo ADR Aceito sem revogar)**: aplica primária — absorve ADR-008+ADR-013+ADR-015+ADR-016+ADR-023+ADR-040 em 1 consolidado preservando regra central de cada um integralmente em § Decisão (a)-(g).
- **Cond 4 (categoria conceitual nova de artefato)**: **NÃO aplica** — ADR-045 já carrega categoria meta da redesign ("consolidação 45 → ~13-15 ADRs"); ADR-050 é quinta instância de migração cluster (C+D+E+F+G), não primeira instância de categoria nova. F4 lesson Onda C reaplicada literal.
- **Cond 1 (decisão estrutural sem ancestral)**: **NÃO aplica** — ADR-045 (charter da redesign) + ADR-046+ADR-047+ADR-048+ADR-049 (templates de migração) são ancestrais codificados em sequência direta. ADR-050 é instância do pattern, não decisão sem ancestral.
- **Cond 2 (substitui ADR ancestral invertendo decisão central)**: **NÃO aplica** — regra central de cada um dos 6 ADRs absorvidos está preservada integralmente em § Decisão (a) até (g); nenhum ADR é marcado como `Substituído` (ficam `Aceito` com redirect canonical no topo per pattern de archive); nenhuma inversão de decisão central. Há consolidação de cross-refs em narrativa única, não substituição doutrinal.
- **Cond 3 (codifica restrição externa de longa duração)**: **NÃO aplica** — sem restrição externa nova (regulatória, contratual, integração estável); decisão é editorial interna.

**Justificativa para novo ADR vs adendos cross-ref:** cond 5 primária isolada justifica novo ADR. Pattern editorial F4 Onda C/D/E/F/G estabilizado — auto-aplicação coerente.

## Gatilhos de revisão

Consolida triggers das 6 decisões absorvidas:

### Para dimensão (a) skills geradoras

- Surge **skill executora** stack-specific (não geradora) → reavaliar se a separação skill/hook deste ADR cobre o novo caso ou se executores precisam de critério próprio.
- SKILL.md de gerador ultrapassa ~500 linhas com 3+ sub-blocos → reabrir para considerar split em sub-skills delegadas.
- Detecção por marker falha em ≥2 projetos consumidores reais (monorepo, marker ambíguo, falta de marker) → reabrir para considerar declaração explícita de stack via path contract.
- Contribuidor adiciona sub-bloco com qualidade inferior aos atuais → sinal de que critério editorial precisa ser explicitado em CLAUDE.md.

### Para dimensão (b) CI lint

- Schema completo via `claude plugin validate` virar viável no runner (CLI disponível sem setup) → reabrir para incluir.
- Matriz de SO ou versão Python virar relevante → reabrir para considerar `actions/setup-python` ou matriz.
- Suite de testes do próprio plugin emergir como necessidade → ADR sucessor explicitamente revogando trecho da frase canonical.
- Custo operacional do gate (flakes recorrentes, latência > 30s) → reabrir para pinning ou abandono.
- Fronteira disputada (proposta concreta de gate novo) → reexaminar critério mecânico cumulativo.

### Para dimensão (c) block_env

- Falso-positivo recorrente: ≥2 reports independentes de operador em consumidor sobre arquivo `*.env` que não é env-file e bloqueio atrapalha workflow legítimo.
- Pedido recorrente para bypass via config: sinal de que allowlist viraria pertinente.
- Surgir convenção de naming nova (`*.envrc`, `*.env.encrypted`) que mereça revisão da política — abrir ADR sucessor.

### Para dimensão (d) block_gitignored

- **≥2 consumers independentes reportarem** o mesmo pattern de atrito (script operacional gitignored como entrypoint) **e** indicarem que refatorar via Makefile/compose não é viável.
- **Incidente concreto** em que operador edita script local via workaround manual e introduz bug por copy/paste truncado.
- **Mudança na doutrina de naming/auto-gating** (revisitando para permitir hooks config-aware).
- **Convenção de ecossistema mudar** — stack mainstream emite build artifact diretamente na raiz.
- **Gap operacional `.claude/local/` 4ª categoria** (NOTES 2026-05-30T05:26:59Z) endereçado em ADR sucessor.

### Para dimensão (e) `disable-model-invocation`

- **Skill nova violando o critério.** PR introduzindo `SKILL.md` que declara o valor "errado" → revisitar wording ou tabela retroativa.
- **Sub-fluxo onde blast radius muda dinamicamente.** Skill que ora roda local ora roda em deploy → revisitar se sub-fluxo seguro merece `false`.
- **Mudança na semântica default da harness sobre autoinvocação** → regra precisa ser reescrita.
- **Cláusula "risco de autoinvocação cross-turn" exercida concretamente** → primeira skill nova que justificar `true` pelo critério 3 valida ou pede refinamento.

### Para dimensão (f) block_settings_drift

- **Falso-positivo recorrente**: ≥2 reports independentes → JSON parse + key-targeted vira pertinente.
- **Recorrência de session perms**: ≥2 cleanup commits por session-perm drift em 30 dias → cobertura de session perms vira pertinente.
- **Incidente Windows**: report de operador com path `C:\Users\<user>\` poluindo settings.json → reabrir cláusula 4.
- **Mudança no formato Claude Code settings**: novo campo de permissões ou renomeação de `permissions.*` → reavaliar regex bruta.
- **Pedido recorrente para bypass via config**: allowlist configurável vira pertinente.

### Para dimensão (g) pattern "critério mecânico cumulativo"

- **Nova categoria emergir** que justifique critério mecânico cumulativo (5ª instância pós-ADR-013/-020/-022 + dimensão (e)) → confirmar pattern como meta-doutrina estabilizada; considerar codificação em `philosophy.md` se ≥6 instâncias acumularem.
- **Instância existente requerer revisão de critérios** (ex.: ADR-022 6 critérios provarem-se rigid demais) → revisar pattern, mantendo retro-compatibilidade.

### Para meta-decisão de consolidação (Onda G)

- **Cluster outro reabre consolidação em sub-clusters menores** (alternativa b) durante ondas H-X → pode ser sinal de que padrão 1-ADR-por-cluster precisa refinamento; charter § Atualização pós-execução documenta evolução.
- **Refinamento editorial extra-direção** emerge em ondas H-X (modificação além de exclusão/adição) → revisitar ADR-045 fronteira "ajuste editorial vs revisão".
