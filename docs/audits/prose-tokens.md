# Auditoria — prosa & tokens

Auditoria periódica do **eixo redacional** dos artefatos do plugin. Foca em **como** as coisas estão ditas, não em **o que** está estruturado (esse é o eixo da `architecture-logic.md` — auditorias complementares, podem rodar em sequência ou independentes).

## Escopo

Todos os artefatos de runtime do plugin: `CLAUDE.md`, `docs/philosophy.md`, `skills/*/SKILL.md`, `agents/*.md`, `hooks/*.py`, `hooks/hooks.json`, `.claude-plugin/*.json`, `README.md`, `docs/install.md`, `docs/decisions/ADR-*.md`. ADRs e planos de `docs/plans/` são contexto, não alvo de reescrita.

## Critérios

- **Coesão & coerência interna/externa** — cada artefato fala uma coisa só; artefatos que dialogam não se contradizem.
- **Clareza & desambiguação** — regras procedurais legíveis em uma passada; tri-state e classificações em tabela/pseudocódigo, não em prosa contínua.
- **Alinhamento a `docs/philosophy.md`** — prosa que viola "cerimônia tática não" é prioritária para corte.
- **Inflação de tokens** — input recorrente (auto-loaded) e por invocação. `CLAUDE.md` é sempre carregado; `philosophy.md` tende a ser puxado por referência cruzada das skills.
- **Duplicação cross-artifact** — mesma regra parafraseada em N lugares. Identificar dono único + referências curtas.
- **Justificativas-cicatriz** — "Por quê separar:", "A diferença operacional:", "Provável drift que..." costumam ser respostas a incidentes passados já internalizados.
- **Frontmatter `description`** — sempre carregado pelo roteador; foco no gatilho de invocação, não na descrição do output.
- **`## O que NÃO fazer`** — só scope guards genuínos (anti-padrão não-óbvio); item que recapitula o body é ruído. Critério editorial em `CLAUDE.md` § "Editing conventions".

## Formato de saída

Análise estruturada em três seções:

1. **Inventário & métricas** — tabela com linhas/palavras por artefato e modo de carregamento (auto-loaded / por invocação / sob demanda).
2. **Diagnóstico por critério** — um sub-bloco por critério, com exemplos concretos citando arquivo e trecho.
3. **Propostas** — letras (A, B, C…) com escopo, estimativa de redução em palavras/tokens e sequenciamento sugerido por leverage.

## Pré-checagem obrigatória

Antes de propor: **ler `BACKLOG.md ## Concluídos`** para descartar propostas já shippadas e evitar re-trabalho. Citar IDs/PRs quando uma proposta encosta em algo já tratado (e justificar por que ainda assim vale uma segunda passada, se for o caso).

## Modo

Análise profunda, sem pressa. **Só diagnóstico + propostas, zero alteração** — não criar plano em `docs/plans/`, não abrir PR, não tocar artefato.

## Saída persistente

Antes de devolver controle, gravar o resultado completo (inventário + diagnóstico + propostas) em `docs/audits/runs/<YYYY-MM-DD>-prose-tokens.md`. Permite que a próxima auditoria compare deltas e que propostas não evaporem se a sessão fechar.

## Encaminhamento das propostas

Propostas aceitas pelo operador **não viram PR direto**. Cada uma entra pelo fluxo padrão: `/triage <proposta>` decide o artefato (linha de backlog, plano, ADR, atualização de domain/design) e segue dali. A auditoria produz a lista; o `/triage` faz o alinhamento individual.
