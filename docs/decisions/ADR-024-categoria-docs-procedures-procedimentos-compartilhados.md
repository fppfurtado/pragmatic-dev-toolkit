# ADR-024: Categoria docs/procedures/ para procedimentos operacionais compartilhados

**Data:** 2026-05-12
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-001](ADR-001-protocolo-de-templates.md) estabeleceu `templates/` como single source of truth para esqueletos canônicos de artefatos consumidos por múltiplas skills, com escopo limitado a `templates/plan.md` na v1 e gatilho de revisão "3+ artefatos com estrutura compartilhada" para considerar formato de manifesto. ADR-024 é sucessor parcial — não revoga ADR-001, complementa estabelecendo categoria distinta para procedimentos operacionais.
- **Investigação:** Auditoria `docs/audits/runs/2026-05-12-architecture-logic.md` § 2.6 (finding L1) identificou acoplamento textual entre `/release § Cleanup pós-merge` e `/triage §0` — `/release` referencia textualmente "skills/triage/SKILL.md `### 0. Cleanup pós-merge`"; renomear ou mover o passo 0 em `/triage` quebra `/release` silenciosamente. Proposta G da mesma auditoria sugere extrair o algoritmo (~30 linhas) para `templates/cleanup-pos-merge.md` ou subpasta `docs/protocols/`.

## Contexto

O plugin tem hoje 1 arquivo sob `templates/` (`plan.md`, esqueleto canônico de plano preenchido por `/triage` ao criar um plano e validado por `/run-plan` ao executar). ADR-001 chamou esta pasta de "single source of truth para **esqueletos canônicos** de artefatos" — template = esqueleto preenchível.

A proposta G_arch pede extrair um segundo tipo de conteúdo compartilhado: o procedimento "Cleanup pós-merge" (~30 linhas em `/triage §0`, referenciado textualmente por `/release § Cleanup pós-merge`). Este conteúdo **não é esqueleto preenchível** — é um **procedimento operacional referenciado em runtime**: skills consumidoras leem o arquivo e executam o algoritmo descrito (detecção de candidatos, cutucada por candidato, execução das seleções). Categoria semanticamente distinta de esqueleto.

Bifurcação real:

- **(a) Estender `templates/` para acomodar procedimentos** (flat ou subdir). Doutrina de ADR-001 antecipa "expansão futura é extensão deste protocolo, não nova decisão" — mas o foco do escopo original são esqueletos. Estender `templates/` para incluir procedimentos mistura dois tipos sob umbrella original, criando dívida cognitiva: leitor que abre `templates/` espera fill-in skeletons, encontra procedimento, precisa do ADR para disambiguar.
- **(b) Criar categoria nova `docs/procedures/`** para procedimentos compartilhados, paralela a `docs/decisions/`, `docs/plans/`, `docs/audits/`. Fronteira semântica nítida: `templates/` = esqueletos preenchíveis; `docs/procedures/` = procedimentos executáveis. Custo: 4ª categoria sob `docs/`. Benefício: cada categoria internamente pura — leitor sabe o tipo só pela localização, sem precisar de doutrina.

Critério de decisão: pureza semântica por localização reduz sobrecarga cognitiva sustentada em todas as leituras futuras; custo da categoria nova é pago uma vez na criação.

### Reinterpretação de ADR-001 § Decisão

ADR-001 § Decisão é literal: *"a pasta `templates/` é estabelecida com 1 arquivo; expansão futura é extensão deste protocolo, não nova decisão."* ADR-024 reinterpreta esse escopo de forma explícita:

- **"Expansão"** em ADR-001 § Decisão refere-se a **esqueletos preenchíveis adicionais** (`templates/adr.md`, `templates/release-notes.md`, etc.) — mesma categoria conceitual do `plan.md`, adicionados sob o mesmo protocolo de leitura+preenchimento em runtime.
- **Procedimentos operacionais** são categoria qualitativamente distinta (algoritmo executável vs esqueleto preenchível). Não são "expansão" do mesmo protocolo — são protocolo paralelo. Justificam decisão nova em vez de extensão silente.

Sem essa reinterpretação, mantenedor competente lê ADR-001 e conclui que ADR-024 é cerimonialmente desnecessário. O parágrafo amarra a fronteira entre os dois ADRs.

### Desambiguação lexical: "procedure" vs "protocol"

Toolkit já usa "protocol" / "protocolo" em ≥3 sentidos:

- **"Resolution protocol"** (CLAUDE.md § seção, ADR-003, ADR-005, ADR-011, ADR-017, ≥3 SKILLs) — algoritmo de resolução de papéis em runtime.
- **"Protocolo de templates"** (ADR-001 título) — sinônimo de doutrina/critério.
- **"Protocolo de envio"** e similares espalhados em prosa de skills — sinônimo de procedimento ad-hoc.

Reusar "protocol" como **categoria de artefato sob `docs/`** introduziria quarto significado da mesma palavra. Optou-se por **"procedure" / "procedimento"** (categoria `docs/procedures/`) — neutro, exato semanticamente (algoritmo operacional executável), sem colisão lexical. Conflito de nome evitado em vez de gerenciado por desambiguação.

## Decisão

**Estabelecer `docs/procedures/` como categoria distinta de `templates/` para procedimentos operacionais compartilhados consumidos por múltiplas skills.**

- **`templates/`** (ADR-001, preservado): esqueletos canônicos de artefatos. Skills leem via Read em runtime e **preenchem** placeholders ao produzir o artefato. Exemplo: `templates/plan.md` lido por `/triage` ao criar plano novo.
- **`docs/procedures/`** (este ADR): procedimentos operacionais. Skills leem via Read em runtime e **executam** o algoritmo descrito ao referenciar o procedimento. Exemplo: `docs/procedures/cleanup-pos-merge.md` referenciado por `/triage` (passo 0) e `/release` (pré-condição).

Razões objetivas:

- **Pureza semântica por localização.** Reader sabe o tipo só pela pasta; não precisa abrir conteúdo nem consultar ADR para entender se é skeleton ou procedimento. Reduz sobrecarga cognitiva sustentada (a cada leitura, qualquer mantenedor futuro).
- **Fronteira intacta de ADR-001.** Definição original de `templates/` como esqueleto preenchível permanece honesta. Sem reescrita semântica, sem exceção silenciosa.
- **Forward-compat.** Próximas extrações de procedimentos compartilhados caem naturalmente em `docs/procedures/<nome>.md` sem reabrir doutrina.
- **Consumer-pattern reutilizado.** Skills consomem `docs/procedures/<nome>.md` via Read runtime, idêntico ao pattern de `templates/plan.md` — mecânica conhecida, sem categoria nova de invocação.

**Mecânica de consumo:** Read em runtime via path do plugin. Embed/copy reintroduz duplicação que o ADR resolve — descartado (mesmo critério de ADR-001).

**Critério para criação de novo procedimento em `docs/procedures/`** (cumulativo — todos devem se verificar):

- Conteúdo é **procedimento operacional** (algoritmo executável), não esqueleto preenchível;
- **≥2 skills referenciam** ou consumiriam o procedimento (1 consumer = manter inline na skill — extrair sem necessidade vira indireção pura);
- Extração **resolve acoplamento textual concreto** entre skills (análogo a L1 do audit). Skill nova hipotética não conta — quando a skill nova de fato aparecer (com plano aprovado em `docs/plans/` ou PR aberto), a extração acompanha.

**Verificação dos 3 critérios é obrigatória** no `/triage` ou ADR que propõe novo procedimento. Revisor (humano ou `design-reviewer`) registra a verificação explicitamente no plano/ADR. Sem essa verificação, a categoria fica sujeita a extração especulativa e perde o gating.

**Escopo inicial deste ADR:** `docs/procedures/cleanup-pos-merge.md` (extração G_arch + extensão D_arch via plano `docs/plans/procedures-cleanup-pos-merge.md`).

**Invariante de implementação do ADR-024:** plano que implementa este ADR **deve** adicionar bullet em ADR-001 § Status ou parágrafo final apontando para ADR-024 como complemento que estabelece categoria paralela para procedimentos. Sem essa edição, ADR-024 não está implementado. Mitigação não é "deferida ao plano" — é invariante mecânica do plano.

## Consequências

### Benefícios

- Pureza semântica sustentada: `templates/` continua sendo esqueletos; `docs/procedures/` é só procedimentos. Sem disambiguação a cada leitura.
- L1 do audit (acoplamento textual /release → /triage §0) eliminado — ambas skills referenciam um path estável.
- D_arch (forge bilateral) ganha 1 site único para implementação — sem precisar replicar em /triage §0 e /release § Cleanup pós-merge separadamente.
- Forward-compat para procedimentos compartilhados futuros sem reabrir doutrina.
- Sem colisão lexical com "protocol" usado em outros 3 sentidos no toolkit.

### Trade-offs

- Adiciona 4ª categoria sob `docs/` (`decisions/`, `plans/`, `audits/`, `procedures/`). Operador externo abrindo o repo encontra mais uma pasta para entender. Trade-off aceito pela pureza semântica. Discoverability: ADR poderá motivar adição de mini-README em `docs/` listando as 4 categorias e seus papéis se confusão emergir (gatilho pós-fato, não pré).
- Skills passam a depender de Read runtime em `docs/procedures/<nome>.md` além de `templates/<nome>.md`. File ausente (cache corrompido, instalação parcial) → skill que referencia falha.
- ADR-001 ganha cross-reference em § Status apontando para ADR-024 (invariante de implementação acima). Mantenedor que lê só ADR-001 a partir daí sabe que existe categoria paralela; antes da edição, esse risco existe e é o motivo do invariante.

### Limitações

- `docs/procedures/` é estabelecida com 1 arquivo inicial. Categoria nova com 1 item é YAGNI suspeito; justifica-se aqui por dois fatores cumulativos: (1) a extração resolve acoplamento concreto pré-existente (L1 do audit), não é especulação; (2) auditoria já registra **segundo candidato pipeline**: o pattern `auto-detect forge bilateral` replicado em 3 sites (`/run-plan §3.7`, `/release §5`, `/next §4.5`) é elegível para futura extração para `docs/procedures/auto-detect-forge.md` quando justificar. Categoria não nasce com 1 item teórico — nasce com 1 implementado + 1 candidato auditado concreto.

## Alternativas consideradas

### `templates/cleanup-pos-merge.md` flat

Reusar `templates/` como umbrella para esqueletos + procedimentos. Sob ADR-001 § Decisão "expansão futura é extensão deste protocolo, não nova decisão"; tecnicamente coberto pela doutrina existente.

Descartado por estender semântica de `templates/` (originalmente esqueletos) para incluir procedimentos. Reader que abre `templates/` precisa do conteúdo para disambiguar; doutrina fica parcialmente esticada de forma silenciosa.

### `templates/cleanup-pos-merge.md` com redefinição explícita de `templates/`

Mesma localização da anterior, mas adendo a ADR-001 redefine `templates/` como "shared runtime-read documents — skeletons + procedures". Doutrina honesta sobre a extensão.

Descartado por inferior em pureza local: nome da pasta `templates/` continua carregando conotação de esqueleto preenchível em qualquer leitor que não tenha lido o adendo redefinidor. Pureza por localização não é restaurada — só transferida para o ADR.

### `templates/procedures/cleanup-pos-merge.md` (subdiretório)

Subdiretório sob `templates/` marcando o tipo. Internamente discrimina sem categoria top-level nova.

Descartado por dois motivos:

- Assimetria: `templates/plan.md` flat vs `templates/procedures/cleanup-pos-merge.md` em subdir. Para simetria, `plan.md` migraria para `templates/skeletons/plan.md` — churn médio que toca `/triage` step 4 e `/run-plan` precondição 1, sem ganho sobre (b).
- Pré-organização de taxonomia para 1 arquivo: convenção de subdiretório vira regra a documentar; alternativa (b) categoria-pasta nova é igualmente pura sem regra interna a `templates/`.

### Renomear `templates/` para `shared/`

`shared/plan.md` + `shared/cleanup-pos-merge.md`. Umbrella mais honesto ("shared runtime-read content").

Descartado por dois motivos:

- Pureza inferior: `shared/` ainda mistura 2 tipos (esqueleto + procedimento). Umbrella honesto, internamente impuro.
- Churn alto: rename de pasta toca ADR-001 (rewrite), `/triage` step 4, `/run-plan` precondição 1, `docs/install.md`, possivelmente outros. Para conseguir o mesmo nível de clareza que (b) entrega, com mais churn.

### Embed procedimento em CLAUDE.md como doutrina

CLAUDE.md já documenta protocolos compartilhados (Resolution protocol, AskUserQuestion mechanics, hook auto-gating).

Descartado por dois motivos:

- CLAUDE.md hoje em 171 linhas, cap nominal 200. +30 linhas de procedimento ultrapassa cap.
- CLAUDE.md é auto-loaded a cada turn. Procedimento referenciado em 2 sites específicos cobrar leitura em todo turn é desproporcional ao uso real.

### Skill nova `/cleanup-post-merge` invocada via Skill tool

Tratar cleanup-pós-merge como sub-skill invocada por `/triage` e `/release`.

Descartado: skills no toolkit são slash-commands user-facing por convenção; sub-procedimento invocado só por outras skills infla taxonomia user-facing sem benefício para o operador. Mecânica de Read runtime sobre arquivo `.md` entrega a deduplicação sem promover o procedimento a skill.

### Nome alternativo `docs/runbooks/`

Convenção pop em DevOps/SRE para "algoritmo operacional executável compartilhado", semanticamente exato.

Descartado por conotação DevOps/incident-response forte. Toolkit é workflow plugin para desenvolvimento; "runbook" carrega expectativa de aplicabilidade a on-call / postmortem que não casa com o escopo. `procedures/` é neutro e mantém semântica precisa sem importar convenção alheia.

## Gatilhos de revisão

- **Próximo `docs/procedures/<nome>.md` proposto** em `/triage` ou em ADR → revisor (humano ou `design-reviewer`) verifica explicitamente os 3 critérios cumulativos da seção Decisão (procedimento operacional, ≥2 skills, acoplamento concreto) e registra a verificação no plano/ADR. Verificação ausente bloqueia merge. Checkpoint observável, não promessa de revisão.
- **`docs/procedures/` cresce para ≥5 arquivos** → reabrir para sub-organização (por skill consumidora ou por tipo de procedimento). Análogo ao gatilho de ADR-014 para `docs/plans/` ≥100.
- **Incidente concreto de mistura** (PR coloca procedimento em `templates/` ou esqueleto em `docs/procedures/`) → reabrir nomenclatura ou consolidar em umbrella único (volta à opção `shared/`).
