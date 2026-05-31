# ADR-047: Modo local consolidado (paths gitignored + replicação `.claude/`/`CLAUDE.md` + recusa cross-mode)

**Data:** 2026-05-30
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-045](ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) (apex da redesign — § Decisão parte 1 § Implementação literal: *"Ondas C-X — migração de ADRs por cluster temático. Cada onda absorve 3-6 ADRs antigos em 1 consolidado..."*). Este ADR é a segunda instância concreta dessa migração (Onda D) consolidando o cluster modo local.
- **ADRs absorvidos:** ADR-005 (foundational do cluster — modo `local` para 3 roles + regra de não-referenciar + mecânica gitignored — agora absorvido e arquivado nesta onda em `docs/decisions/archive/`) + ADR-018 (sucessor parcial — replicação `.claude/` em `.worktreeinclude` via `/init-config` + `/note` como 2º dispatcher per Addendum 2026-05-27 — agora absorvido e arquivado) + ADR-025 (sucessor parcial — recusa assimétrica cross-mode `backlog: local + plans_dir: canonical` — agora absorvido e arquivado) + ADR-030 (sucessor parcial — aceitar `CLAUDE.md` gitignored com replicação via `.worktreeinclude` — agora absorvido e arquivado). Cluster index Addendum em ADR-005 (Onda 3 da reforma doutrinária, PR #86) reconheceu explicitamente ADR-018/-025/-030 como sucessores parciais — proof-of-concept de consolidação editorial agora preservado no archive como registro histórico que cumpriu sua função.
- **Decisão template:** [ADR-046](ADR-046-cutucada-uniforme-descoberta-gaps-configuracao.md) (primeira instância de migração cluster — Onda C). Pattern validado: header redirect canonical (blockquote + H1 preservado), archive index incremental, propagação de cross-refs em docs vivos apenas, link rot em 2 categorias (histórica + doutrinal ativa), auto-aplicação cond 5 primária isolada (cond 4 NÃO aplica; cond 1 NÃO aplica). Onda D reaplica literal + valida transferibilidade do pattern para cluster sem procedure file.
- **Investigação:** Onda D codificada em `docs/plans/onda-d-migracao-cluster-modo-local.md`. Cluster modo local escolhido como segunda migração por: (1) cluster Addendum já existente em ADR-005 (paralelo ao precedente Onda C em ADR-017); (2) 4 ADRs vs 2 em Onda C — scope médio que calibra pattern antes de clusters de 5-8 ADRs; (3) **primeira aplicação a cluster sem procedure file** — testa transferibilidade do pattern fora de cutucadas; (4) cluster coeso semanticamente (4 ADRs cobrem 4 dimensões da mesma decisão estrutural "modo local"; cada um estende ADR-005 num eixo distinto).

## Contexto

A camada doutrinal pós-v2.14.0 inclui 4 ADRs codificando dimensões do modo local-gitignored:

- **ADR-005 (foundational, 2026-05-07)** — estabeleceu modo `local` para 3 roles do path contract (`decisions_dir`, `backlog`, `plans_dir`) como trilho paralelo ao Resolution protocol de ADR-003. Sintaxe `paths.<role>: local`, comportamento sob `.claude/local/<role>/`, regra de não-referenciar (commit/PR/branch metadata sem ID de ADR/slug/linha de backlog em modo local), mecânica de inicialização (`mkdir` + probe `git check-ignore` + gate `Gitignore`). Recusa de modo local para `version_files`/`changelog` (`/release` para com mensagem clara).
- **ADR-018 (sucessor parcial, 2026-05-19)** — `/init-config` step 4.5 garante `.claude/` em `.worktreeinclude` quando ≥1 role em modo local. Mecânica determinística sem `AskUserQuestion` (operação sem trade-off cross-team a confirmar); idempotente; compatível com `.worktreeinclude` tracked ou gitignored. Addendum 2026-05-27 reconhece `/note` como 2º dispatcher universal da mesma invariante (paralelo idempotente cross-skill). Origem: smoke-test PJe 2026-05-11 follow-up.
- **ADR-025 (sucessor parcial, 2026-05-15)** — `/init-config` step 3 recusa assimétrica combinação `backlog: local + plans_dir: canonical` antes de gravar bloco config. Critério "direção do leak" (privado→público é incoerente; público→privado é normal); combinação simétrica permanece válida. Defensividade assimétrica em `/triage` step 1 cobre bloco legacy. Origem: H_arch do roadmap 2026-05-12 reaberto pós-diferimento.
- **ADR-030 (sucessor parcial, 2026-05-27)** — `/init-config` aceita `CLAUDE.md` gitignored como sinal deliberado do consumer (em vez de recusar). Step 3 reformulado para registrar flag interna `claude_md_gitignored = true` e prosseguir; step 4.5 estendido com cláusula OR (≥1 role local OR `claude_md_gitignored = true`) e tabela composta de paths a garantir (`.claude/` per ADR-018; `CLAUDE.md` per este ADR — cada adição independente e idempotente). Origem: PJe 2026-05-11 mid-stream.

Sob a redesign da camada doutrinal codificada em ADR-045, o cluster modo local é candidato natural para consolidação:

- **Decisão central estável** — modo local + paths + mecânica + replicação `.claude/` + recusa cross-mode + aceitar `CLAUDE.md` gitignored sem revisão pendente. Trade-offs absorvidos editorialmente nas Ondas 1-2 da reforma doutrinária (ADR-005:48/75/87 e :Addendum reformulações).
- **3 sucessores parciais já reconhecidos** — Cluster index Addendum em ADR-005 (Onda 3 da reforma) demonstrou que leitura única do thread completo é mais ergonômica que navegação cross-ADR; precedente operacional pontual absorvido por esta consolidação.
- **Sem procedure file equivalente** — diferente de cutucadas (Onda C tinha `docs/procedures/cutucada-descoberta.md` como par editorial), cluster modo local tem **toda sua mecânica em CLAUDE.md "Local mode" section + skills** (`/init-config` step 4.5 + `/triage` step 1 + `/note` § Ordem dos gates). Fronteira ADR-024 (procedure como executor canonical de mecânica) **não aplica antecipadamente** — só pertinente quando procedure pré-existe. Pattern de transferibilidade do pattern de migração Onda C **primeira vez testado** nesta onda.

Esta consolidação valida o pattern de migração para clusters sem procedure file (calibração para ondas E-X que podem ter clusters análogos: design-reviewer ecosystem 009+011+026+038; execução `/run-plan` 004+028+037+039+041; convenções editoriais 007+012+024+034 — alguns com procedure pré-existente, outros sem).

## Decisão

**Consolidar a doutrina sobre modo local em ADR único (este ADR-047), absorvendo substância de ADR-005 (foundational) + ADR-018 (replicação `.claude/`) + ADR-025 (recusa cross-mode) + ADR-030 (aceitar `CLAUDE.md` gitignored) sob narrativa única. Sem procedure file complementar — cluster sem split ADR/procedure per ausência de pré-existência (fronteira ADR-024 não aplica antecipadamente; aplicação prospectiva fica como gatilho de revisão futuro se ≥3 dispatchers da invariante `.claude/` em `.worktreeinclude` emergir per gatilho herdado de ADR-018 Addendum).**

### Escopo e mecanismo unificado

**4 dimensões integradas em narrativa única:**

#### (a) Paths suportados + sintaxe + comportamento + regra de não-referenciar + mecânica gitignored

Modo `local` aceito para 3 roles do path contract: `decisions_dir`, `backlog`, `plans_dir`. Sintaxe sob `<!-- pragmatic-toolkit:config -->`:

```yaml
paths:
  decisions_dir: local
  backlog: local
  plans_dir: local
```

Skill cria/lê o artefato em path gitignored sob `.claude/local/<role>/`:
- `decisions_dir: local` → `.claude/local/decisions/`
- `backlog: local` → `.claude/local/BACKLOG.md`
- `plans_dir: local` → `.claude/local/plans/`

Resolution protocol (CLAUDE.md → "Resolution protocol") ganha **trilho paralelo**: role declarado `local` → skill usa o path local diretamente, sem ofertar canonical creation, sem informar+parar.

**Regra de não-referenciar:** quando role está em modo `local`, skills geram mensagens de commit, descrições de PR e nomes de branch **sem citar** o artefato em modo local (ID do ADR, slug do plano, texto da linha do backlog não aparecem). Em modo canonical (default), comportamento atual de referência preservado.

**Mecânica de inicialização** (ativada na primeira escrita sob `.claude/local/<role>/` em cada invocação):
1. **`mkdir -p .claude/local/<role>/`** se ausente. Silent operation. Plugin **nunca toca `.claude/` root** — território Claude Code, fora do escopo do plugin.
2. **Probe gitignore:** `git check-ignore -q .claude/local/<role>/.probe`. Covered → proceed silent. Uncovered → trigger gate.
3. **Gate `Gitignore`:** propor adicionar `.claude/local/` entry ao `.gitignore` do projeto. Options: `Adicionar entrada` / `Cancelar`. Cancel → refuse local mode para esta invocação + report risk. Cria `.gitignore` se ausente; aborta com mensagem clara se não-git repo (`git rev-parse` retorna non-zero).

**Rejeições preservadas:** `version_files` e `changelog` **rejeitam** modo local — `/release` para com mensagem clara quando operador declara `paths.version_files: local` ou `paths.changelog: local` (bump de versão e changelog precisam ser commitados/visíveis para fazer sentido).

#### (b) Replicação `.claude/` em `.worktreeinclude` via `/init-config` step 4.5

`/init-config` step 4.5 garante que `.claude/` aparece em `.worktreeinclude` quando ≥1 role em modo local — invariante para que worktrees frescas criadas pelo `/run-plan` repliquem o store local-gitignored.

Mecânica determinística **sem `AskUserQuestion`** (operação sem trade-off cross-team a confirmar):
1. **`.worktreeinclude` ausente** → criar com header + `.claude/`.
2. **`.worktreeinclude` presente, probe retorna não-zero** (path ausente) → adicionar linha. Falso-negativo benigno aceito por simetria editorial (regex simples + linha redundante = sem dano funcional).
3. **`.worktreeinclude` presente, probe retorna zero** (path coberto) → skip silente.

Idempotente; compatível com `.worktreeinclude` tracked ou gitignored.

**`/note` como 2º dispatcher** (Addendum 2026-05-27 absorvido) — `/note` executa o mesmo gate `Worktree replication` step independente de role local declarada (NOTES.md como store non-role per ADR-032). Mecânica idêntica ao step 4.5 do `/init-config`; gate `Gitignore` executa **primeiro**, gate `Worktree replication` executa **em seguida**; cancel no gate `Gitignore` aborta antes do segundo. Sincronizar mudanças manualmente entre os 2 dispatchers se mecânica evoluir (drift control via cross-ref textual ao step 4.5 do `/init-config` como fonte canonical).

**Assimetria de trigger é deliberada** — `/init-config` step 4.5 dispara **condicionalmente** (≥1 role local declarada OR `claude_md_gitignored = true`); `/note` passo 1 dispara **universalmente** (toda invocação, sinal de necessidade de replicação é a própria invocação — há NOTES.md a gravar sob `.claude/local/`). Invariante preservada — `.claude/` em `.worktreeinclude` cobre simultaneamente `.claude/local/<role>/` e `.claude/local/NOTES.md`; eixos de extensão distintos (condicional vs universal) são critério load-bearing para futuros 3º/4º dispatchers (per gatilho de revisão herdado de ADR-018 Addendum, preservado em § Gatilhos).

Gatilho herdado: 4º dispatcher emergir → extrair pattern para `docs/procedures/worktree-replication-dispatch.md` (per ADR-018 Addendum gatilho original; preservado em § Gatilhos de revisão).

#### (c) Recusa assimétrica cross-mode `backlog: local + plans_dir: canonical`

`/init-config` step 3 verifica após coletar respostas se combinação é `paths.backlog: local` AND `paths.plans_dir: canonical` (canonical = `Canonical` escolhido OR omitido como default). Combinação detectada → parar antes de gravar bloco YAML com mensagem literal:

> Combinação `backlog: local + plans_dir: canonical` recusada ([ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md)). `**Linha do backlog:**` viraria mensageiro de texto privado para plano público — semanticamente incoerente. Re-execute `/init-config` escolhendo uma das combinações suportadas: `ambos canonical` (default — registro coletivo), `ambos local` (uso individual), `backlog canonical + plans_dir local` (registro coletivo + planos privados).

**Critério "direção do leak":** privado → público é incoerente (texto privado vaza para plano público via `**Linha do backlog:**`); público → privado é normal (combinação `backlog canonical + plans_dir local` permanece válida). Recusa é **assimétrica**.

**Defensividade em `/triage` step 1** cobre bloco legacy (operador editou bloco antigo manualmente sem rodar `/init-config`): após resolver `backlog` e `plans_dir`, mesma combinação detectada → mensagem análoga de recusa orientando reexecutar `/init-config`. `/run-plan` sem check (plano fora-do-`/triage` é fora-do-escopo).

#### (d) Aceitar `CLAUDE.md` gitignored com replicação no step 4.5

`/init-config` step 3 detecta `CLAUDE.md` gitignored via `git check-ignore -q CLAUDE.md`:
- **Retorno zero (gitignored)** → registrar flag interna `claude_md_gitignored = true` para o step 4.5; **prosseguir** normalmente. Plugin honra sinal deliberado do consumer via `.gitignore` em vez de recusar.
- **Retorno não-zero** → flag fica falsa; comportamento canonical (tracked).

Step 4.5 estendido com **cláusula OR** no critério (≥1 role local OR `claude_md_gitignored = true`) e tabela composta de paths a garantir:

| Path | Trigger | Probe |
|---|---|---|
| `.claude/` | ≥1 role local | `grep -qE "^\.claude(/\|$)" .worktreeinclude` |
| `CLAUDE.md` | `claude_md_gitignored = true` | `grep -qE "^CLAUDE\.md$" .worktreeinclude` |

Cada adição **independente e idempotente** — flag de role local + flag de CLAUDE.md gitignored podem disparar paralelo ou isolado. Step 5 emite mensagem de aceitação substituindo mensagem doutrinária revogada.

### Razões

- **Doutrina consolidada com clareza editorial.** Reader único navega thread completo (paths + mecânica + replicação + cross-mode + aceitar `CLAUDE.md` gitignored) em ADR único; não precisa saltar 4 ADRs nem inferir relação por leitura cruzada do Addendum cluster.
- **Sem procedure file — toda mecânica vive em docs vivos.** Cluster modo local não tem procedure pré-existente per ADR-024. Mecânica das 4 decisões opera distribuída: CLAUDE.md § "Local mode" + `/init-config` step 3+4.5+5 + `/triage` step 1 + `/note` § Ordem dos gates + `/run-plan` § Micro-commit (regra de não-referenciar) + `/release` § O que NÃO fazer (rejeição) + `/new-adr` § Implementação opcional. Substância semântica vive aqui (ADR-047); canonical defaults aplicam runtime via skills.
- **Pattern de migração validado em cluster sem procedure file.** Onda D demonstra que pattern Onda C (archive + redirect canonical + cross-refs em docs vivos + archive index incremental + cond 5 primária isolada) transfere para cluster onde fronteira ADR-024 não aplica. Calibração para ondas E-X que podem ter clusters análogos.
- **Trilha empírica preservada.** § Origem histórica deste ADR lista os 4 incidentes empíricos das decisões absorvidas; conteúdo original archivado em `docs/decisions/archive/` para registro auditável.
- **Volume de cross-refs significativamente maior — ~58 ocorrências em ~34 linhas distintas, 9 docs vivos vs ~12 ocorrências em ~7 linhas, 5 docs em Onda C — testa escalabilidade do propagation pattern.** `/init-config` SKILL.md sozinha carrega 21 ocorrências em 13 linhas (todas as 4 dimensões intersectam essa skill); doc-reviewer audita Bloco 3 do plano (skills herdeiras).

### Header redirect canonical + archive index — format herdado de ADR-046

Arquivos arquivados sob `docs/decisions/archive/` adotam **format de citação + header H1 original preservado** codificado em ADR-046 § Razões:

```markdown
> **ARCHIVED <YYYY-MM-DD>** — content absorbed into [ADR-MMM](../ADR-MMM-<slug>.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-NNN: <título original>

<body original integral...>
```

`docs/decisions/archive/README.md` (criado na Onda C) **estendido** com 4 linhas novas nesta onda (ADR-005, ADR-018, ADR-025, ADR-030 → ADR-047, Onda D). Pattern incremental por onda preservado per ADR-046 § Razões "Archive index incremental".

## Origem histórica

Incidentes empíricos das 4 decisões absorvidas preservados como contexto para reabertura informada:

### Atrito PJe 2026-05-11 onboarding (origem de ADR-005)

Sessão pós-v1.21.0 reavaliando o contrato `required` por role individualmente. Identificado que `decisions_dir`, `backlog`, `plans_dir` são compartilhados (gitignored mata o ponto), **mas o plugin deveria ser aplicável também em projetos que não mantêm essas estruturas no repo** (uso individual, scratchpad pessoal). Lacuna: nenhum trilho de ADR-003 (capture+stop, oferta canonical, inform+stop, `paths.<role>: null`) aceita "tenho esses artefatos mas só localmente". ADR-005 introduziu modo local como trilho paralelo via `paths.<role>: local`.

### Smoke-test PJe 2026-05-11 follow-up (origem de ADR-018)

Smoke-test pós-shipping de ADR-005 + onboarding PJe revelou gap: worktree fresca criada pelo `/run-plan` **não replicava** `.claude/local/` automaticamente. `.worktreeinclude` cobre o caso desde que `.claude/` seja listado lá — mas operador novo não sabe disso (cobertura editorial em `docs/install.md` + ADR-005 § Mecânica não basta). ADR-018 estabeleceu invariante proativa: `/init-config` step 4.5 **garante** `.claude/` em `.worktreeinclude` quando ≥1 role local. `/run-plan` SKILL.md:36 (safety net) preservado por simetria editorial. Addendum 2026-05-27 absorveu `/note` como 2º dispatcher universal — gap fechado entre ADR-018 (gate owned by `/init-config`, conditional) e ADR-032 (NOTES.md como store non-role, independente de role local).

### H_arch roadmap 2026-05-12 (origem de ADR-025)

Auditoria estrutural 2026-05-12 identificou H_arch ("recusar cross-mode `backlog: local + plans_dir: canonical` no `/init-config`") como item da Onda 4 do roadmap, **diferido** ("só com evidência empírica de uso não-intencional"). Operador absorveu trade-off de YAGNI sem evidência registrada, reabrindo pós-diferimento per próxima sessão de execução de roadmap. ADR-025 codificou recusa assimétrica com critério "direção do leak"; defensividade em `/triage` step 1 cobre bloco legacy. 11 findings absorvidos pré-commit (6 no ADR + 5 no plano).

### Mid-stream PJe 2026-05-11 (origem de ADR-030)

Smoke-test PJe 2026-05-11 mid-stream surfou caso adicional: consumer com `CLAUDE.md` gitignored (decisão deliberada do consumer — onboarding do plugin sem tracking do arquivo de configuração local). `/init-config` step 3 inicialmente **recusava** com mensagem doutrinária orientando reconsiderar `.gitignore`. ADR-030 inverteu: plugin **aceita** o sinal deliberado do consumer e garante replicação via `.worktreeinclude` em vez de recusar. Sucessor parcial da extrapolação informal de ADR-016 em `/init-config` step 3 (que recusava); ADR-016 literal scope (hooks/scripts) preservado. 4 findings absorvidos no ADR + 3 no plano + 1 cutucada absorvida (reabrir ADR-029 § Limitações editorialmente).

## Consequências

### Benefícios

- Reader navega thread completo do modo local em 1 ADR (era 4 ADRs + Addendum sustentando o thread).
- Pattern de migração validado para clusters sem procedure file — calibração para ondas E-X.
- Mecânica preservada distribuída em docs vivos onde executa (CLAUDE.md + skills) — sem duplicação, sem stranding de substância em ADRs imutáveis.
- Trilha empírica preservada via archive + § Origem histórica.
- Saldo inventário: 44 vigentes pós-Onda C + 1 novo ADR-047 - 4 archivados = **41 vigentes pós-Onda D** (drop líquido de 3 — vs 2 em Onda C; calibração para ondas com clusters maiores).

### Trade-offs

- **Link rot em ADRs imutáveis tem 2 categorias distintas (F1 lesson de Onda C reaplicada).**
  - **Categoria (a) — referências históricas/precedente** (vasta maioria dos ~16 ADRs imutáveis citantes — ADR-003/-010/-014/-015/-020/-021/-023/-024/-026/-027/-028/-039/-040/-041/-043 citam um ou mais do cluster em § Origem como precedente). **Archive resolve** — `docs/decisions/archive/<slug>.md` carrega corpo histórico completo per format codificado. Archive index incremental facilita descoberta. Cross-refs em ADRs imutáveis ficam como registro histórico, NÃO são editados.
  - **Categoria (b) — referências de substância doutrinal ativa** (subset identificado pré-execução para verificação no design-reviewer): ADR-032 cita ADR-005 como base do "store non-role" — substância já interna a ADR-032 (justificativa do store non-role completa); ADR-038 cita ADR-005 ↔ ADR-025 como precedente do partial-successor pattern com status `Proposto` — substância já interna; ADR-042 cita ADR-005 mecânica para cross-write — substância delegada; ADR-046 cita ADR-005 + ADR-017 como Addenda precedentes para archive pattern — substância delegada para ADR-046. **Hipótese: zero substância "doutrinal ativa" perdida** — pre-existente Addendum de ADR-005 (Onda 3) explicitamente reconheceu ADR-018/-025/-030 como sucessores parciais; consolidação preserva isso. design-reviewer valida hipótese.
  - Edição dos ~16 ADRs imutáveis citantes evitada por preservar ADR-classical convention; substância absorvida em ADR-047 (§ Decisão + § Origem histórica) é a mitigação real.
- **Custo do refactor de cross-refs significativamente maior que Onda C** — 9 docs vivos atualizados (vs 5 em Onda C); ~58 ocorrências em ~34 linhas distintas (vs ~12 ocorrências em ~7 linhas). Pattern de propagation testado em escala ~5× maior. doc-reviewer audita cada bloco; threshold "≥10 findings" no Bloco 3 (skills) preservado como conservador (sinal de pausar para revisitar pattern antes de aplicar a clusters maiores 5-8 ADRs), independente do volume — escalar proporcionalmente diluiria o sinal de saúde.
- **Pattern de migração sem procedure file — primeira instância.** Onda C estabeleceu fronteira ADR-024 codificada (F9 lesson). Onda D demonstra que **ausência de procedure file** é caso natural, não gap — toda mecânica vive em docs vivos (CLAUDE.md + skills); fronteira aplica antecipadamente apenas quando procedure pré-existe. Calibração para ondas E-X: design-reviewer audita por cluster se procedure absorption, preservation, ou ausência aplica.
- **CHANGELOG.md preservado intacto** — registro histórico imutável paralelo a ADRs imutáveis. Múltiplas linhas referenciando ADR-005/-018/-025/-030 nas versões v2.0.0 → v2.14.0; preservadas como registro de versionamento, NÃO editadas. Link rot histórico aceito.
- **Implementação history das 4 decisões absorvidas permanece em `archive/ADR-005-*.md` (§ Implementação com 9 commits da branch `roles-local-mode`) + bodies originais dos demais archives** — NÃO duplicada em ADR-047 (paralelo ao precedente Onda C, ADR-046 igualmente delegou ao archive). Reader que precisa de hash → 1 hop via redirect canonical do archive. Padrão editorial para ondas E-X: delegar implementação history ao archive sempre (preserva ADR-047 enxuto + format canonical do archive carrega hashes sem custo adicional).

### Limitações

- **Herda gap do `block_gitignored.py`** (NOTES 2026-05-30T05:26:59Z) — hook recusa `Edit` em `.claude/local/NOTES.md` com mensagem assumindo 3 categorias (dependency, build artifact, local cache); `.claude/local/` como store doutrinário declarado (ADR-005 + ADR-032 absorvidos) é **quarta categoria** intencionalmente gitignored por contrato de privacidade, não por ser derivado. Endereçamento pendente — **NÃO consolidado como decidido nesta redesign** per anti-regression checklist do charter § Componentes do plugin. Reservado espaço de extensão em ADR consolidado equivalente quando hook receber endereçamento (allowlist específico, mensagem reformulada, `/note --rewrite`, ou alternativa).
- **Defensividade assimétrica em `/triage` step 1** (recusa cross-mode) cobre **bloco legacy** (operador editou bloco manualmente sem rodar `/init-config`). NÃO cobre planos criados fora-do-`/triage` — `/run-plan` aceita combinação inconsistente sem check upstream. Trade-off de YAGNI aceito em ADR-025; preservado.
- **Cross-write `/note --to`** (per ADR-042) requer target inicializado em modo local (`.claude/local/` existe + gitignored). Target sem setup → recusa silente. NÃO replica setup do target a partir do origin — paralelo doutrinal de não mutar `.gitignore`/`.worktreeinclude` do target em cross-write per § Decisão (a) gate `Gitignore` e § Decisão (b) `Worktree replication` (mutações cross-contextuais ferem blast-radius compartilhado).
- **`/init-config` step 4.5 tem 2 dispatchers documentados** (init-config + /note); 3º dispatcher emergir → extrair pattern para `docs/procedures/worktree-replication-dispatch.md` (gatilho herdado de ADR-018 Addendum, preservado em § Gatilhos de revisão).

### Mitigações

- **Anti-regression checklist do charter** § Path contract lista os ~10 elementos load-bearing (paths suportados, sintaxe, comportamento `.claude/local/`, regra de não-referenciar, mecânica `mkdir` + probe + gate, recusas cross-mode, invariante `.claude/` em `.worktreeinclude`, aceitar `CLAUDE.md` gitignored, dispatcher pattern, `/note` como 2º dispatcher) — design-reviewer audita preservação em ADR-047 § Decisão. Plano § Verificação end-to-end critério 10 prescreve audit explícito.
- **Plano § Verificação end-to-end critérios 4-7** prescrevem grep explícito de ADR-005/-018/-025/-030 em paths concretos como invariante de sucesso da onda; `doc-reviewer` audita o diff conforme insumo curado pelo plano per ADR-009 padrão diff-level. Pattern reaplicado da Onda C: critério de cross-ref propagation vive no plano, não na mecânica de reviewer.
- **Archive index estendido nesta Onda D** (4 linhas novas em `docs/decisions/archive/README.md`) — link rot mitigation **ativa** desde já para o cluster modo local. Reader que cai em archive/ADR-005-*.md vê redirect proeminente para ADR-047 + corpo histórico abaixo.
- **F4 lesson de Onda C reaplicada literal** — auto-aplicação cond 5 primária isolada (cond 4 NÃO aplica; cond 1 NÃO aplica). Evita inflação de cond 4 em cada onda E-X ("primeira/N-ésima instância como categoria nova" auto-justificativa).

## Alternativas consideradas

### (a) Manter ADR-005, ADR-018, ADR-025, ADR-030 com cluster Addendum (status quo Onda 3)

Continuar com estrutura atual: ADR-005 foundational + 3 sucessores parciais + cluster Addendum em ADR-005 (criado na Onda 3 da reforma doutrinária).

Descartada per ADR-045 § Decisão parte 1: cluster Addenda foram **prova de conceito** de consolidação editorial; a redesign generaliza esse movimento para **archive + consolidado único**. Manter status quo perde benefício de leitura única do thread + mantém 4 ADRs onde 1 cabe sob a nova estrutura.

### (b) Edit in-place em ADR-005 absorvendo ADR-018/-025/-030

Reescrever ADR-005 incorporando substância dos 3 sucessores, mantendo ADR-005 como ADR vigente; ADR-018/-025/-030 marcados `Substituído`.

Descartada:

- Viola convenção ADR-classical (ADRs são registros imutáveis; supersedeção via novo ADR).
- Apaga trajetória editorial (ADR-018 documentou smoke-test PJe follow-up + Addendum 2026-05-27; ADR-025 documentou H_arch reabertura pós-diferimento; ADR-030 documentou inversão de extrapolação de ADR-016 — reescrever ADR-005 apaga essas narrativas).
- ADR-045 explicitamente prescreve archive + novo ADR consolidado, não edição in-place.
- ADR-046 (Onda C) já estabeleceu pattern de archive + novo consolidado; mudar pattern em Onda D fere consistência da redesign.

### (c) Criar `docs/procedures/local-mode.md` absorvendo a mecânica

Mover mecânica das 4 decisões para procedure file novo; ADR-047 carrega apenas substância doutrinária (decisão de modo local + 4 dimensões); procedure carrega `mkdir` + probe + gate + step 4.5 tabela composta + recusa cross-mode + aceitar `CLAUDE.md` gitignored.

Descartada:

- Cria procedure file **sem necessidade pré-existente** — pattern de Onda C explicita que procedure file separation per ADR-024 aplica quando procedure **pré-existe** (cutucadas tinha; modo local não tem). Criar antecipadamente reabre tensão que ADR-024 resolveu.
- Mecânica do modo local já está distribuída em docs vivos onde executa (CLAUDE.md + skills); mover para procedure cria 4ª localização sem ganho de coesão.
- Procedure tem categoria conceitual de **algoritmo prescritivo executor** (per ADR-024); mecânica do modo local é mais doutrinária (decisão sobre paths + mecânica de inicialização + comportamento de skills) — fit pobre.
- Gatilho de revisão preservado: se ≥3 dispatchers da invariante `.claude/` em `.worktreeinclude` emergirem (per ADR-018 Addendum gatilho original), extrair `docs/procedures/worktree-replication-dispatch.md` — caminho prospectivo via gatilho, não antecipatório.

### (d) Splits diferentes — separar ADR-005 (foundational) de ADR-018/-025/-030 (sucessores em eixos distintos)

Criar 2 ADRs novos: ADR-047a "Modo local foundational (paths + mecânica + regra de não-referenciar)" + ADR-047b "Sucessores do modo local (replicação + cross-mode + CLAUDE.md gitignored)".

Descartada:

- Splits artificiais — os 4 ADRs cobrem dimensões da **mesma decisão estrutural** (modo local como conceito + 3 dimensões operacionais). Cluster index Addendum em ADR-005 (Onda 3) já demonstrou que leitura única do thread é mais ergonômica.
- 2 ADRs onde 1 cabe — viola Ockham (entidades multiplicadas sem ganho).
- Charter sketch original previa **1 ADR consolidado** para cluster modo local (paralelo a ADR-003 da nova estrutura). Esta onda materializa fielmente; splits reabriria fronteira que sketch resolveu.
- Pattern de Onda C (1 consolidado por cluster) — mudar em Onda D fere consistência.

### (e) ADR-047 como índice apontando para os 4 ADRs originais (sem archive)

ADR-047 minimalista apontando para os 2 ADRs originais; nada movido para archive.

Descartada (paralelo a Alternativa (e) de ADR-046):

- Não materializa a redesign — ADR-045 prescreve absorção de conteúdo + archive de antigos, não indexação cosmética.
- Charter sketch explicita "novo ADR consolidado" como output das ondas C-X, não "ADR-index".
- Cluster Addendum em ADR-005 já cumpria função de índice; ADR-047 como índice seria redundante.
- Pattern de Onda C já estabeleceu absorção + archive; mudar em Onda D fere consistência.

## Gatilhos de revisão

Triggers das 4 decisões absorvidas consolidados + triggers específicos da consolidação:

### Herdados de ADR-005 (modo local foundational)

- **Operador adota modo local em projeto e reclama de friction** com regra de não-referenciar (slug do plano não aparecendo em commit/PR/branch) — sinal de que regra é severa demais ou redação dos commits precisa de variação. Reabrir para considerar opt-in de referenciar com explanação clara.
- **`version_files`/`changelog` em modo local emergir como gap reportado** — se equipe quiser bump local-only (release dev pessoal sem afetar registro coletivo), recusa de `/release` torna-se gap. Reabrir para considerar caminho `local` para essas roles com critério editorial (não-publicado).
- **Mudança na convenção de gitignore do consumer (`.git/info/exclude` em vez de `.gitignore`)** — probe `git check-ignore` deve cobrir; reabrir se sintaxe alternativa emergir.

### Herdados de ADR-018 (replicação `.claude/`)

- **4º dispatcher da invariante `.claude/` em `.worktreeinclude` emergir** — atual: `/init-config` step 4.5 + `/note` § Worktree replication. 3º dispatcher = pattern de drift control via cross-ref textual perde força; extrair para `docs/procedures/worktree-replication-dispatch.md` (per ADR-018 Addendum gatilho original preserved).
- **`/run-plan` SKILL.md:36 (safety net) divergir do step 4.5 do `/init-config`** — drift de mecânica entre safety net e dispatcher principal. Reabrir para considerar deprecation do safety net ou sincronização forçada.
- **`.worktreeinclude` tracked vs gitignored emergir como decisão consequente** — atualmente plugin é agnóstico. Se padrão emergir (tracked = team, gitignored = personal), reabrir para considerar canonical preference.

### Herdados de ADR-025 (recusa cross-mode)

- **Operador adota combinação `backlog: local + plans_dir: canonical` deliberadamente** (alguma justificativa de workflow não considerada) — reabrir para reconsiderar critério "direção do leak".
- **Operador edita bloco legacy manualmente reintroduzindo combinação recusada** sem rodar `/init-config` — defensividade em `/triage` step 1 cobre. Se gap surgir em outras skills (`/run-plan` aceitando plano com cross-mode declarado), reabrir para considerar defensividade adicional.
- **`backlog: canonical + plans_dir: local` (combinação simétrica) emergir como problemática** — atualmente permitida. Se evidência de leak na direção pública→privada surgir, reabrir critério.

### Herdados de ADR-030 (aceitar `CLAUDE.md` gitignored)

- **Mudança em `/init-config` step 1 sobre criação automática de CLAUDE.md** — se toolkit passar a criar CLAUDE.md em algum cenário, aceitação gitignored precisa reconsiderar interação.
- **Step 4.5 tabela composta crescer para ≥3 paths** — atualmente `.claude/` + `CLAUDE.md`. Se 3º trigger emergir (`docs/` local, `.envrc`, etc.), reabrir para considerar abstração da tabela.
- **Operador reverter `.gitignore` de CLAUDE.md após setup** — flag `claude_md_gitignored` ficou stale; reabrir para considerar re-probe periódico ou gate de drift.

### Específicos desta consolidação (Onda D)

- **Pattern de migração sem procedure file falhar em outra onda E-X** — design-reviewer flagrar gap material no pattern (substância de algum ADR não absorvível limpamente sem procedure file separado; link rot em ADRs imutáveis revelar substância "doutrinal ativa" que precisa procedure separado). Reabrir ADR-046 + ADR-047 como template combinado; pode requerer revisão de ADR-045 § Decisão parte 1.
- **Link rot em ADRs imutáveis gerar ≥3 reports de confusão** específicos para cluster modo local — sinal de que archive sem stub no path original é caro para reader em cluster muito citado. Reabrir para considerar redirect file no path antigo OR symlink OR edit de cross-refs em ADRs antigos (violaria ADR-classical mas pode ser trade-off).
- **Volume de cross-refs (32 em 8 docs vivos) gerar ≥10 findings de doc-reviewer no Bloco 3 (skills)** — pattern de propagation precisa refinamento antes de aplicar a clusters maiores (5-8 ADRs). Pausar redesign e revisitar charter per § Sinal de saúde.
- **Gap do `block_gitignored.py`** (NOTES 2026-05-30T05:26:59Z) receber endereçamento — reabrir ADR-047 para integrar substância da decisão (allowlist específico, mensagem reformulada, ou alternativa) OR criar ADR sucessor parcial específico do hook (per ADR-034 cond 5).

## Auto-aplicação coerente per ADR-034

- **Cond 5 (sucessor parcial):** aplica primária — consolidado absorve substância de ADR-005 (foundational) + ADR-018/-025/-030 (sucessores parciais cobrindo 3 dimensões adicionais) sob narrativa única. Os 4 ADRs vão para archive com header redirect canonical a este ADR. **Suficiente per ADR-034** *"novo ADR quando ≥1 das 5 condições aplica"*; cond 5 isolada justifica criação deste ADR.
- **Cond 4 (categoria nova):** **NÃO aplica** — ADR-045 § Decisão parte 1 § Implementação **já codificou a categoria** "consolidação editorial cross-ADR de cluster temático como decisão estrutural" no nível meta-pattern; ADR-046 estabeleceu primeira instância concreta (Onda C); ADR-047 é **segunda instância concreta** da categoria já estabelecida, não introduz categoria conceitual nova. **F4 lesson de Onda C reaplicada literal** — aplicar cond 4 aqui inflaria o critério em cada onda E-X ("N-ésima instância como categoria nova" auto-justificativa), diluindo a precisão de ADR-034.
- **Cond 1 (decisão estrutural sem ancestral direto):** **NÃO aplica** — ADR-045 § Decisão parte 1 § Implementação **é ancestral codificado direto** do pattern que ADR-047 instancia. ADR-046 já estabeleceu pattern como segunda fonte ancestral codificada (template direto da migração). Onda 3 cluster index Addendum em ADR-005 é precedente operacional pontual, mas ADR-045 elevou o pattern a decisão estrutural codificada — ADR-047 herda essa ancestralidade.
- **Cond 2 (substitui ADR ancestral):** NÃO aplica — operação é **absorção consolidatória** (substância das 4 decisões codificada integralmente em ADR-047 § Decisão sob narrativa única; archive preserva trajetória), **não revogação** (paralelo a ADR-043 → ADR-035, onde apex doutrinal foi invertido). Diferença pragmática: leitor de ADR-047 obtém regra vigente identicamente equivalente à composição dos 4 absorvidos; leitor de archive/ADR-005-*.md vê redirect canonical apontando para autoridade vigente sem ambiguidade. Pattern editorial para ondas E-X: cond 2 reservada para inversões/revogações; absorções consolidatórias seguem cond 5 isolada.
- **Cond 3 (codifica restrição externa):** NÃO aplica — decisão interna ao processo doutrinal do plugin.

Pattern editorial para ondas E-X: cada migração cluster aplica **cond 5 primária + outras condições conforme ancestralidade real**, não cond 4 inflada nem cond 1 espúria. ADR-045 § Decisão parte 1 + ADR-046 são ancestrais codificados de cada migração; ondas instanciam, não criam categoria. **F4 lesson de Onda C codificada nesta § como template para E-X.**
