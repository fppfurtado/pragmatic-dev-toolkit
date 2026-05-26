# Plano — README com framing Product Engineer harness e contraste spec-first

## Contexto

ROADMAP item 4 (commit 18cb8ff). Depende de [ADR-037](../decisions/ADR-037-codigo-como-fonte-de-verdade-vs-intent-as-truth.md) (commit `fe97ab6`) que codifica a antítese doutrinária com spec-first; agora destravado. README hoje vende componentes (tabela `## What's inside` com 12 skills + 5 agents + 2 hooks); deveria vender problema/posicionamento primeiro para o anglófono em scroll rápido.

Vídeo "Voltei do Vale do Silício 2026" (Waldemar Neto) deu o framing concreto — **"Product Engineer harness"** articula o que este plugin entrega: infraestrutura para o engenheiro consumidor cristalizar intenção, executar com disciplina e ancorar decisões. Spec-kit dá o contraste de posicionamento — abordagens spec-first generativas (specs como executable artifacts que regeneram código) são antípoda doutrinária codificada em ADR-037.

**Absorve item de polimento backlog "marketplace prep #7"** (visual walkthrough/GIFs) — mesmo goal de discoverability EN para scroller anglófono; prose framing é entrega mais barata do mesmo objetivo. Confirmado pelo operador em gap-clarification. Visual escalation pode reabrir se métrica futura mostrar gap.

**ADRs candidatos:** [ADR-012](../decisions/ADR-012-idioma-artefatos-discoverability-landing.md) (idioma EN do README per discovery channel target audience — fundamenta que mudança fica em EN), [ADR-037](../decisions/ADR-037-codigo-como-fonte-de-verdade-vs-intent-as-truth.md) (código-como-fonte-de-verdade vs intent-as-truth — fonte do contraste citado).

**Linha do backlog:** plugin: README com framing Product Engineer harness e contraste spec-first

## Resumo da mudança

Editorial em duas frentes (ambas doc-only):

1. **`README.md`**: adicionar parágrafo de posicionamento entre o título (`# Pragmatic Dev Toolkit`) e a seção `## What's inside`. Substância (~2-4 frases curtas em EN): (a) framing "Product Engineer harness" — plugin entrega harness para o consumer engineer cristalizar intenção, executar com disciplina (plan + reviewer-per-block) e ancorar decisões em doctrine; (b) contraste curto com spec-first generativo — neste plugin doctrine records intent, code remains the source of truth (vs SDD que inverte: spec é primary, code regenerated); (c) link inline a ADR-037 para o leitor que quer aprofundar.

2. **`BACKLOG.md`**: mover linha "plugin: marketplace prep #7 (polimento) — README walkthrough visual / GIFs..." de `## Próximos` para `## Concluídos` (topo), prefixo preservado + nota de absorção curta (apontando para o commit deste plano e indicando que visual escalation pode reabrir se métrica futura mostrar gap).

Sem nova mecânica, sem cross-ref bidirecional novo (apenas link já existente a ADR-037).

## Arquivos a alterar

### Bloco 1 — README.md positioning paragraph at top {reviewer: doc}

- `README.md`: após o título de nível 1 (`# Pragmatic Dev Toolkit`, linha 1) e antes da seção `## What's inside`, inserir parágrafo de posicionamento (~2-4 frases) com (a) framing "Product Engineer harness", (b) contraste curto com spec-first generativo, (c) link inline para ADR-037. Texto em EN per ADR-012. Tom descritivo (não combativo) — cada ferramenta opta por uma estratégia.

### Bloco 2 — BACKLOG.md absorção marketplace #7 {reviewer: doc}

- `BACKLOG.md`: remover linha 6 ("plugin: marketplace prep #7 (polimento) — README walkthrough visual / GIFs...") de `## Próximos`; adicionar entrada equivalente no topo de `## Concluídos` com prefixo preservado e nota curta indicando absorção pelo prose framing deste plano (referência ao commit do Bloco 1) + cláusula de reabertura ("visual escalation pode reabrir se métrica de engajamento futura mostrar gap, per intenção original do item").

## Verificação end-to-end

- `grep -n "Product Engineer" README.md` retorna match no parágrafo de posicionamento (top).
- `grep -n "ADR-037" README.md` retorna link inline ao ADR.
- `head -10 README.md` mostra o parágrafo ANTES da seção `## What's inside`.
- `grep -n "marketplace prep #7" BACKLOG.md` retorna match único em `## Concluídos` (não mais em `## Próximos`).
- Inspeção textual: framing usa termo "Product Engineer harness" literal; contraste com spec-first é curto (1-2 frases, não tese longa); link a ADR-037 com texto descritivo, não URL nu; tom descritivo (não combativo).

## Verificação manual

- Operador anglófono lê README do topo: o parágrafo de posicionamento responde "o que este plugin entrega para mim?" antes da tabela de componentes — não precisa rolar para descobrir.
- Contraste com spec-first lê como posicionamento descritivo (cada ferramenta opta por uma estratégia), não como ataque às outras.
- BACKLOG: marketplace #7 não aparece mais em Próximos; aparece em Concluídos com nota de absorção que torna óbvio o motivo da movimentação para futuro leitor.

## Notas operacionais

- Plano bloco-único conceptual (substância no Bloco 1; Bloco 2 é housekeeping de backlog).
- design-reviewer dispatcha automaticamente pré-commit (ADR-011); free-read prioriza ADRs candidatos em `## Contexto`.
- doc-reviewer revisa ambos blocos (paths `.md`).
- §3.4 `/run-plan` adiciona a linha deste plano em Concluídos como sempre; Bloco 2 (separado) movimenta marketplace #7 — dois edits a BACKLOG.md em commits distintos, ordem editorial.
