# Auditoria — arquitetura & lógica

Auditoria periódica do **eixo estrutural** do plugin. Foca em **o que** está estruturado e por quê, não em **como** está dito (esse é o eixo da `prose-tokens.md` — auditorias complementares, podem rodar em sequência ou independentes).

## Escopo

Arquitetura e mecânica do plugin como um todo, e a lógica de cada artefato individualmente e nas suas relações com outros artefatos. Todas as alavancas são alvo legítimo de proposta — criar, editar ou remover:

- skills, agents, hooks, scripts auxiliares
- `CLAUDE.md`, `docs/philosophy.md`, ADRs, role contract
- gates, frontmatter (`disable-model-invocation`, `roles.required/informational`), comandos hardcoded em prosa
- estrutura de manifests (`plugin.json`, `marketplace.json`), modo local, integração com forge
- divisão de responsabilidades entre componentes; quem é dono de qual mecânica

## Critérios

- **Funcionalidade & simplicidade arquitetural** — toda peça tem razão de existir; sobreposições e indireções desnecessárias são candidatas a colapso.
- **Alinhamento a `docs/philosophy.md`** — flat & pragmático; YAGNI; sem abstrações prematuras; bifurcações nomeadas onde existem trade-offs reais.
- **Efetividade das funcionalidades** — cada skill/agent/hook está cumprindo o que promete, na cadência prevista? Há gates desligados na prática? Há features dormentes?
- **Redução de gates & verbosidade desnecessários** — perguntas ao operador que poderiam ser inferidas; confirmações duplicadas; cerimônia que não troca decisão.
- **Otimização de tokens (input/output)** — não pelo lado redacional (esse é o outro eixo), e sim pelo lado **arquitetural**: artefatos auto-loaded, leituras encadeadas (skill A puxa skill B puxa philosophy.md), ADRs/planos referenciados em alta frequência, redundância entre dono e consumidor da regra.
- **Lógica e relações entre artefatos** — quem invoca quem, quem lê quem, dependências cíclicas, contratos implícitos, dono único de cada regra.

## Formato de saída

Análise estruturada em quatro seções:

1. **Mapa de componentes & relações** — quem invoca quem (skills→skills, skills→agents, hooks→nada), quem lê quem (referências cruzadas em prosa), gates ativos por skill.
2. **Diagnóstico por critério** — um sub-bloco por critério, com exemplos concretos citando arquivo, função, gate ou relação.
3. **Propostas** — letras (A, B, C…); cada uma marca explicitamente se é **criar**, **editar** ou **remover**; com escopo, impacto esperado, risco e dependências entre propostas.
4. **Sequenciamento sugerido** — ordem por leverage e risco, identificando propostas que destrancam outras.

## Pré-checagem obrigatória

Antes de propor: **ler `BACKLOG.md ## Concluídos`** e o índice de `docs/decisions/` para descartar propostas já shippadas ou já decididas em ADR (uma proposta que reverte ADR existente precisa ser declarada como tal e justificar a inversão — ver memória de feedback sobre limiar de ADR).

## Modo

Análise profunda, sem pressa. **Só diagnóstico + propostas, zero alteração** — não criar plano em `docs/plans/`, não abrir PR, não tocar artefato.

## Saída persistente

Antes de devolver controle, gravar o resultado completo (mapa de componentes + diagnóstico + propostas + sequenciamento) em `docs/audits/runs/<YYYY-MM-DD>-architecture-logic.md`. Permite que a próxima auditoria compare deltas e que propostas não evaporem se a sessão fechar.

## Encaminhamento das propostas

Propostas aceitas pelo operador **não viram PR direto**. Cada uma entra pelo fluxo padrão: `/triage <proposta>` decide o artefato (linha de backlog, plano, ADR, atualização de domain/design) e segue dali. A auditoria produz a lista; o `/triage` faz o alinhamento individual.
