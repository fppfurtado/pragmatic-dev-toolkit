# ADR-072: Role `annotations` plugável (backends local/logseq/null) — sucessor parcial de ADR-054

**Data:** 2026-06-25
**Status:** Aceito (2026-06-25)

**Próxima revisão:** 2026-12-25
**Cadência:** trimestral
**Critério de erosão auditável:** reabrir se **qualquer**: (i) ≥2 projetos consumidores declaram `paths.annotations: null` ou um backend custom fora do trio `local`/`logseq`/`null` — sinal de que o espaço de backends foi mal-dimensionado; **OU** (ii) ao materializar o backend `logseq` (meta-bridge#41), a abstração de role se mostrar incapaz de acomodar o write-while-open sem vazar mecânica PKM-específica do Logseq nas 4 skills consumidoras — sinal de que o role é a fronteira errada; **OU** (iii) [ADR-054](ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a) for revisado de forma a reintroduzir NOTES como *non-role*, contradizendo este sucessor.

## Origem

- **Decisão base:** [ADR-054](ADR-054-bridge-cross-project-note-consolidado.md) § Decisão (a) — estabeleceu `.claude/local/NOTES.md` como *store doutrinário fixo non-role*. Este ADR revisa **apenas** a classificação *non-role → role* dessa sub-decisão (sucessor parcial); preserva toda a mecânica de `/note` (append timestampado, flag `--to` cross-project write, discovery via `$PROJECTS_DIR`, critério contrato-vs-heurística, invariante `.worktreeinclude`/2º-dispatcher) e toda a § Decisão (b). O alvo da revisão é a categoria do path-contract, não o comportamento de `/note`.
- **Decisão base materialmente conectada:** meta-system [ADR-025](https://github.com/fppfurtado/meta-system/blob/main/docs/decisions/ADR-025-contrato-coerencia-pendencias-cross-store.md) — contrato de coerência de pendências cross-store (Aceito 2026-06-25). Define o SSOT split por domínio que este role operacionaliza no toolkit; este ADR é o filho-toolkit que o contrato pai prevê.
- **Investigação:** issue [#154](https://github.com/fppfurtado/pragmatic-dev-toolkit/issues/154) + Logseq `[[constelacao-coerencia-pendencias]]` (sessão CC `remote-control`, 2026-06-24).

## Contexto

A constelação tem 3 stores de pendência (Forge, NOTES.md, Journal Logseq). Hoje o store de anotações é **non-role hardcoded**: ADR-054 § Decisão (a) fixou `.claude/local/NOTES.md` como categoria "store doutrinário fixo non-role", e 5 skills (`/note`, `/next`, `/triage`, `/session-audit`, `/curate-backlog`) referenciam esse path literalmente (`grep -rl "NOTES.md" skills/`).

O contrato pai (ADR-025, Aceito) decidiu o **SSOT split por domínio** — Forge = acionável de código, Journal = acionável de vida, `annotations` = scratch que promove-ou-descarta na fronteira. Para o toolkit operacionalizar sua parte do contrato — tornar a escolha NOTES-vs-Journal uma **config por projeto** em vez de duplicação hardcoded — o store de anotações precisa deixar de ser path fixo e virar role plugável, análogo ao `backlog` (que já aceita backend `forge` per ADR-058).

## Decisão

Promover o store de anotações de *non-role* → **role `annotations`** de primeira classe, com backend plugável por projeto via `paths.annotations: <backend>`:

- **`local`** (default; ausência da chave → `local`) → `.claude/local/NOTES.md`. Comportamento **idêntico ao atual** — ADR-054 § Decisão (a) preservado como o default do role, não removido.
- **`logseq`** → PKM via Logseq HTTP API (write-while-open). **Deferido** a meta-bridge#41 (write-path v2); declarar `logseq` sem o write-path materializado faz a skill **degradar como backend ausente** (graceful, mesmo padrão do `backlog: forge` sem `gh`).
- **`null`** → sem anotações; skills consumidoras pulam silenciosamente (paralelo a `paths.<role>: null` dos demais roles).
- **Sem `forge`** — anotação ≠ tarefa; o canal de tarefa é o `backlog`.

Razões:

- **Operacionaliza o contrato pai (ADR-025) no toolkit.** O role é a forma toolkit-side da decisão de SSOT split — sem ele, a escolha de store fica hardcoded e o desync cross-store não tem como ser config.
- **Simetria com `backlog`.** O pai #54 pediu explicitamente "análogo ao `backlog`"; o role + backend plugável replica o eixo `paths.<role>: <modo>` já consolidado (canonical/local/null/forge → aqui local/logseq/null). **A simetria é estrutural, não equifuncional na v1:** diferente de ADR-058, onde `forge` já era funcional na v1 inteira (infra `forge-auto-detect.md` pré-existente), aqui o ADR entrega de fato 2 backends (`local` = status quo renomeado, `null` = paralelo trivial) e *promete* o terceiro (`logseq`, deferido a meta-bridge#41). A generalização para `logseq` é justificada agora pelo contrato pai (ADR-025 pede a abstração), não por evidência empírica de ≥3 backends — extensão deliberada antes do caso de uso que a estressa, com o risco coberto pelo critério de erosão (ii).
- **Preserva ADR-054 por construção.** O default `local` é o comportamento vigente; nenhum consumidor existente muda sem declarar a chave.

Resolução via Resolution protocol do `CLAUDE.md` como os demais roles; default canonical `.claude/local/NOTES.md`. Consumidores: `/note` (write), `/next` (read p/ ranking), `/triage` (read p/ contexto), `/session-audit` (read p/ captura), `/curate-backlog` (read H4 p/ sinais editoriais + write signal-queue no caminho worktree-deferred).

## Consequências

### Benefícios

- Colapsa 3 stores → 2 como **escolha de config** (NOTES-vs-Journal), atacando a raiz do desync cross-store identificado em ADR-025 § Contexto.
- A regra de não-referenciar de [ADR-047](ADR-047-modo-local-paths-replicacao-cross-mode.md) já cobre o backend `local` (gitignored) sem trabalho novo.

### Trade-offs

- As 5 skills passam a resolver um role onde antes liam path fixo — custo de resolução adicionado, amortizado pela mecânica de Resolution protocol já existente.
- Adiciona uma linha `annotations` à tabela "The role contract" do `CLAUDE.md` (mecânica detalhada fica no plano de fiação, não neste ADR).

### Limitações

- O backend `logseq` é **não-funcional** até meta-bridge#41 (write-path v2). Este ADR define a **fronteira do role**; não define o write-path PKM, que vive no meta-bridge por separação de responsabilidade (ADR-025 § Mapa de arquitetura).
- O *reconciler* (ritual de abertura, meta-bridge#42) opera sobre roles resolvidos mas é ortogonal a este ADR — depende do contrato pai, não desta promoção.
- **Cross-ref doutrinário a reformular:** `/curate-backlog` ancora textualmente "NOTES.md mantém status non-role (ADR-054 § Decisão (a))" em duas justificativas load-bearing de H4 ser informacional (`skills/curate-backlog/SKILL.md` linhas 92 e 190). Como este ADR revisa essa classificação para *role*, o plano de fiação **deve** reformular essas âncoras para "role `annotations` backend `local`" — caso contrário sobra referência a doutrina revogada (contradição doutrina↔código).

## Alternativas consideradas

### (a) Manter non-role (status quo ADR-054)

Descartada. O hardcode de `.claude/local/NOTES.md` impede a config NOTES-vs-Journal que o contrato ADR-025 exige. Manter força o desync cross-store a permanecer estrutural em vez de virar escolha declarada.

### (b) Switch hardcoded `logseq`-vs-`local` sem abstração de role

Descartada. Um booleano "usar Logseq?" nas 5 skills resolveria o caso `logseq`, mas não generaliza para `null` (desligar anotações) nem para backends futuros, e quebra a simetria com `backlog` que o pai #54 pediu. A abstração de role é o custo mínimo que entrega os 3 backends + extensibilidade sob o mesmo eixo `paths.<role>` já consolidado.

### (c) Role é a fronteira errada para um write-path PKM

Rebatida (não descartada — registrada como risco vivo). A contra-leitura: `logseq` (API PKM externa, write-while-open) não é o mesmo eixo que `local` (arquivo gitignored append-only); forçá-los sob `paths.annotations` poderia vazar mecânica PKM-específica do Logseq nas skills consumidoras, sinalizando que o role abstrai a fronteira errada. Rebate: a mecânica de escrita PKM mora no meta-bridge (write-path v2, #41), não nas skills — o role expõe apenas *resolve backend → delega write/read*; as skills permanecem agnósticas ao substrato (paralelo a como `backlog: forge` não vaza mecânica `gh` para `/next`). O risco é real mas só se materializa se a delegação não segurar a fronteira; por isso é exatamente o critério de erosão (ii), não um veto.

## Auto-aplicação coerente per ADR-034

Enquadramento como **novo ADR (sucessor parcial)**, não adendo em ADR-054, percorrendo as 5 condições de [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md):

- **Cond 5 (sucessor parcial) — APLICA, primária.** Refina a classificação *non-role → role* de ADR-054 § Decisão (a) sem revogar as demais sub-decisões de (a) nem (b). É o enquadramento único.
- **Cond 4 (introduz categoria nova) — não aplica.** Rebate análogo a ADR-058 § Auto-aplicação: `annotations` não cria categoria ontológica nova de artefato — entra como **4ª natureza dentro da família `paths.<role>` já existente** (assim como `forge` entrou para `backlog`). É extensão do path-contract consolidado, não categoria nova.
- **Cond 1 (decisão estrutural sem ancestral) — não aplica.** Tem ancestral nítido (ADR-054 § (a)).
- **Cond 2 (substitui ADR ancestral inteiro) — não aplica.** ADR-054 permanece vigente em todas as demais sub-decisões; só a classificação non-role é revisada.
- **Cond 3 (codifica restrição externa) — não aplica como gatilho.** A motivação é o contrato pai ADR-025, que é **interno à constelação** (não restrição regulatória/contratual/integração externa).

**Adendo em ADR-054 rejeitado:** ADR-054 é Aceito/imutável (invariante "Não alterar ADRs existentes" do `/new-adr`); a revisão da classificação non-role é **decisória, não explicativa**, e toca a decisão central de § (a) — falha o teste de adendo (que exige decisão central intacta + caráter explicativo).
