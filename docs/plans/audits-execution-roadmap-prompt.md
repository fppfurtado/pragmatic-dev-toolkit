# Plano — Terceiro prompt de auditoria: `execution-roadmap.md`

## Contexto

Os ciclos de auditoria 2026-05-12 e 2026-05-15/16 mostraram um padrão: cada ciclo produz **2 runs** (architecture-logic + prose-tokens) e **1 roadmap** consolidado que sintetiza propostas, identifica sobreposições entre eixos (ex.: `G_arch ≡ C_prose` no ciclo 2026-05-15/16) e ordena dependências em ondas executáveis. O roadmap consolidado tem sido **redigido manualmente** sob demanda — não há prompt dedicado em `docs/audits/`, apesar dos 2 prompts irmãos existirem (`architecture-logic.md`, `prose-tokens.md`).

O custo de redigir manualmente é o operador (ou agente sem prompt) repetir o algoritmo de consolidação a cada ciclo: identificar onde as 2 auditorias se sobrepõem, ordenar propostas por dependência real, agrupar em ondas, registrar pontos de atenção cross-onda. Em ondas grandes, isso vira meio-arquivo de prosa cuja estrutura sai certa por experiência editorial, não por contrato documentado.

**ADRs candidatos:** ADR-001 (templates centralizados — critério de compartilhamento, expandido implicitamente para `docs/procedures/`), ADR-024 (categoria `docs/procedures/`, hoje Medium por "categoria com 1 item suspeita" — terceiro prompt em `docs/audits/` segue o mesmo eixo: categoria ganha 3º item, deixa de ser singleton).

**Linha do backlog:** plugin: criar `docs/audits/execution-roadmap.md` como terceiro prompt de auditoria — consome 1-N runs em `docs/audits/runs/` e produz roadmap consolidado identificando sobreposições entre eixos (ex.: G_arch ≡ C_prose no ciclo 2026-05-15/16) e dependências cruzadas. Preserva os 2 prompts atuais (`architecture-logic.md`, `prose-tokens.md`) com critérios distintos por eixo — cada run continua sendo entregável por si. Padrão paralelo a `docs/procedures/` (artefato compartilhado). ADRs vizinhos: ADR-001 (templates centralizados, critério de compartilhamento), ADR-024 (categoria `docs/procedures/`, hoje Medium por "categoria com 1 item suspeita"). Motivação: ciclo 2026-05-15/16 mostrou que síntese manual do roadmap repete trabalho de identificar sobreposições e ordenar dependências; prompt dedicado captura o algoritmo como invariante. Reavaliar como plano quando entrar em fila — sub-variantes de mecânica de consumo dos runs (standalone vs invocado-ao-final-da-2ª-auditoria vs argumento-lista-runs) têm trade-offs reais.

## Resumo da mudança

Criar `docs/audits/execution-roadmap.md` — terceiro prompt na categoria `docs/audits/`, paralelo a `architecture-logic.md` e `prose-tokens.md`. Mecânica de consumo decidida via cutucada do `/triage`: **invocado-após-2ª-auditoria do ciclo corrente** — o prompt assume os 2 runs imediatamente anteriores na janela (architecture-logic + prose-tokens com datas próximas) como input implícito; sem heurística de descoberta interna. Alinha com o fluxo observado nos 2 ciclos passados (manual de qualquer jeito) e elimina ambiguidade de seleção de runs.

Decisões-chave:

- **Mecânica de consumo (bifurcação fechada):** invocado-após-2ª-auditoria, não standalone-com-heurística (descartada por carregar lógica de descoberta no prompt) nem argumento-lista-runs (descartada por cerimônia desnecessária no caso comum).
- **Algoritmo de consolidação codificado:** (a) detectar sobreposições entre propostas dos 2 runs (mesmo refator por eixos distintos — ex.: `G_arch ≡ C_prose`); (b) extrair dependências reais (quem destranca quem); (c) ordenar em ondas por leverage/risco × dependência; (d) flagar bundles legítimos vs inválidos (mesmo eixo OK; cross-purpose não); (e) registrar pontos de atenção cross-onda.
- **Output canonical:** `docs/audits/runs/<YYYY-MM-DD>-execution-roadmap.md`, com convenções de status (`[ ]`/`[~]`/`[x]`), encaminhamento (`/triage` por item), e histórico de execução — padrão já validado no roadmap 2026-05-16.
- **Os 2 prompts existentes ficam intocados.** Cada run continua sendo entregável por si; `execution-roadmap.md` é consumidor, não substituto.
- **Fallback editorial para ambiguidade de pareamento:** o critério "2 runs imediatamente anteriores na janela" funciona no caso mainstream (1 architecture-logic + 1 prose-tokens com datas próximas), mas pode ser ambíguo em cenários como `2026-05-12-prose-tokens.md` + `2026-05-12b-prose-tokens.md` (sufixo `b` para re-execução) ou gap temporal entre eixos. § `## Escopo` do prompt declara que **operador pode anunciar quais 2 runs consumir na própria invocação** quando houver ambiguidade — desloca a regra de seleção para o operador em vez de codificá-la, preservando a virtude da opção escolhida.

Fora de escopo: heurística para detectar runs sem invocação explícita (caso (a1) descartado); critério mecânico de "sobreposição" via keyword/scan (algoritmo será editorial, não algorítmico — operador/agente lê os 2 runs e identifica equivalências); atualização do `docs/audits/runs/README.md` (não-essencial; pode emergir como bloco extra se sanity check apontar drift).

## Arquivos a alterar

### Bloco 1 — Prompt novo {reviewer: doc}

- `docs/audits/execution-roadmap.md`: novo arquivo, ~50-70 linhas, estrutura espelhando os 2 prompts irmãos:
  - Cabeçalho de 1 parágrafo posicionando o prompt como **terceiro eixo** (consolidação) complementar a architecture-logic + prose-tokens.
  - `## Escopo` — consome os 2 runs imediatamente anteriores na janela; produz roadmap acionável.
  - `## Critérios de consolidação` — algoritmo editorial em bullets: (1) identificar sobreposições explícitas entre propostas dos 2 runs (mesmo refator visto por eixos distintos); (2) extrair dependências reais entre propostas (quem destranca quem); (3) ordenar em ondas por leverage/risco × dependência; (4) registrar bundles legítimos (mesmo eixo) vs inválidos (cross-purpose); (5) pontos de atenção cross-onda.
  - `## Formato de saída` — tabelas + bullets espelhando o roadmap 2026-05-16: convenção de status, convenção de encaminhamento, ondas numeradas, sequenciamento, atenção cross-onda, redução total estimada, histórico de execução.
  - `## Pré-checagem obrigatória` — ler `BACKLOG.md ## Concluídos` para não bundlear itens já shippados; ler `MEMORY.md` para alinhamento de critério editorial.
  - `## Modo` — análise editorial, zero alteração (espelha os 2 irmãos).
  - `## Saída persistente` — gravar em `docs/audits/runs/<YYYY-MM-DD>-execution-roadmap.md`.
  - `## Encaminhamento` — cada item entra pelo `/triage` padrão.

## Verificação end-to-end

- `ls docs/audits/execution-roadmap.md` — arquivo criado.
- `grep -cE "^## (Escopo|Critérios|Formato|Pré-checagem|Modo|Saída persistente|Encaminhamento)" docs/audits/execution-roadmap.md` — retorna ≥ 6 (estrutura mínima esperada).
- `wc -l docs/audits/execution-roadmap.md` — entre 40-80 linhas (compatível com prompts irmãos: 43 + 52 linhas hoje).
- `grep -cE "2026-05-(12|15|16)|runs/.*execution-roadmap" docs/audits/execution-roadmap.md` — retorna ≥1 (prompt cita run(s) de referência do ciclo 2026-05-15/16 como exemplo do formato canônico).

## Verificação manual

Próxima janela de auditoria (cadência observada: ~3-4 dias entre ciclos no histórico recente, mas pode variar livremente). Cenário canônico:

1. Operador roda `architecture-logic.md` → produz `runs/<data>-architecture-logic.md`.
2. Operador roda `prose-tokens.md` → produz `runs/<data>-prose-tokens.md`.
3. Operador roda `execution-roadmap.md` → produz `runs/<data>-execution-roadmap.md` consolidado.
4. Output bate em estrutura com o roadmap 2026-05-16 (estrutura editorial canonical): ondas numeradas, dependências entre itens, encaminhamentos individuais via `/triage`.
5. Sobreposições reais entre os 2 runs (se houver) aparecem como item unificado no roadmap, igual `G_arch ≡ C_prose` apareceu no ciclo 2026-05-15/16.

Cenário pode ser exercitado opcionalmente em "dry-run" agora (rodar o prompt sobre os 2 runs do ciclo 2026-05-15/16 e comparar output com o roadmap 2026-05-16 manual existente) — validação retroativa do prompt. Fica como possibilidade pós-implementação, não pré-requisito do done.

## Notas operacionais

- **Doc-only:** bloco único, reviewer doc. Sem código, sem teste.
- **Idioma:** PT-BR canonical (espelha os 2 prompts irmãos).
- **Saída persistente do prompt:** gravar em `runs/<YYYY-MM-DD>-execution-roadmap.md`, exatamente como os 2 prompts irmãos persistem em `runs/<YYYY-MM-DD>-<eixo>.md`.
- **Posicionamento doutrinário:** o trio (`architecture-logic`, `prose-tokens`, `execution-roadmap`) estabelece `docs/audits/` como categoria com 3 itens — desloca `docs/procedures/` (hoje 1 item) do limbo "categoria singleton suspeita" no inventário comparativo (vide ADR-024 § Limitações). Não é objetivo da mudança, é externalidade positiva.
- **Reabertura preventiva:** se o 3º ciclo de auditorias produzir output do `execution-roadmap.md` divergente significativamente dos 2 roadmaps manuais anteriores (estrutura, ondas, encaminhamento), o algoritmo editorial não generalizou — reabrir para revisão do prompt em vez de aceitar o output.
