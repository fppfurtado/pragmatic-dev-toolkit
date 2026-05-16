# Auditoria — roadmap de execução

Consolidação dos runs do ciclo corrente em **roadmap acionável** com ondas sequenciadas, sobreposições entre eixos identificadas como itens unificados e dependências cruzadas explicitadas. Foca em **como executar** as propostas levantadas pelas auditorias de eixo (`architecture-logic.md`, `prose-tokens.md`), não em re-discutir os achados — isso já vive nos próprios runs.

## Escopo

Consome os **2 runs imediatamente anteriores na janela** (architecture-logic + prose-tokens com datas próximas) em `docs/audits/runs/` como input implícito. Sem heurística interna de descoberta — assume o ciclo recém-fechado.

**Fallback editorial:** quando os "2 runs imediatamente anteriores" forem ambíguos (sufixo `b` em runs, gap temporal entre eixos, mais de 2 runs disponíveis na janela), operador anuncia explicitamente os paths na invocação. Desloca a regra de seleção para o operador em vez de codificá-la.

## Critérios de consolidação

- **Sobreposições entre eixos** — mesma intervenção vista por critérios distintos. Exemplo do ciclo 2026-05-15/16: `G_arch ≡ C_prose` (helper cutucada de descoberta — eixo arquitetural via "antecipar gatilho ADR-029"; eixo prosa via "~120w líquidos cross-skill"). Tratar como **item único** no roadmap, referido pelo identificador composto.
- **Dependências reais entre propostas** — quem destranca quem. Pré-requisitos viram primeiro; itens destrancados em ondas posteriores. Dependências cross-auditoria valem tanto quanto intra-auditoria.
- **Ondas por leverage/risco × dependência** — primeira onda concentra alto-leverage e baixo-risco com gatilhos próximos; ondas seguintes seguem por proporcionalidade. Auto-loaded vs por-invocação é eixo legítimo de separação (impacto a cada turn vs custo por invocação afetada).
- **Bundles legítimos vs inválidos** — agrupar itens do **mesmo eixo arquitetural** em um único `/triage` é virtude; combinar itens cross-purpose (ex.: ADR de reviewer + refactor editorial) fragmenta foco e dilui design-reviewer. Roadmap declara explícitamente quais bundles propor e quais sequenciar isolados.
- **Pontos de atenção cross-onda** — restrições editoriais que cruzam ondas (release cadence, custo de tokens em auditor que cresce com inventário, refator que destrancaria onda futura). Não viram itens próprios; ficam em seção dedicada.

## Formato de saída

Espelha o run de referência `docs/audits/runs/2026-05-16-execution-roadmap.md`. Estrutura mínima:

- **Cabeçalho** identificando os 2 runs consumidos + ponto-mãe consolidado quando aplicável.
- **Sobreposição declarada** — se houver, citar a equivalência `X_<eixo1> ≡ Y_<eixo2>` como item unificado antes da primeira onda.
- **Ondas numeradas** com checkboxes (`[ ]`/`[~]`/`[x]`), cada item descrevendo: escopo, sub-tarefas destrancadoras (se houver), encaminhamento sugerido.
- **Pontos de atenção cross-onda** — bundles inválidos, dependências sutis, restrições editoriais (release cadence, custo de tokens).
- **Redução total estimada** (quando o eixo `prose-tokens` for um dos runs consumidos) em tabela `Onda | Auto-loaded | Por invocação | Tokens estimados`.
- **Histórico de execução** vazio no nascimento; preenchido conforme cada item shippa (link a commit/PR/ADR + data curta).

**Convenções herdadas:**

- Status `[ ]` pendente · `[~]` em andamento · `[x]` concluído.
- Encaminhamento padrão: cada item entra pelo fluxo `/triage <proposta>`. Bundles indicados explicitamente passam por **um único** `/triage` produzindo plano cobrindo os itens agrupados.

## Pré-checagem obrigatória

Antes de consolidar:

- **Ler os 2 runs alvo** na íntegra — propostas, diagnósticos, dependências internas declaradas.
- **Ler `BACKLOG.md ## Concluídos`** para descartar propostas já shippadas entre o snapshot dos runs e o momento da consolidação (drift entre auditoria e implementação é vetor real — ver caso 2026-05-15/16 onde PR #67 promoveu 7 ADRs antes do roadmap ser gerado).
- **Ler índice de `docs/decisions/`** com filtro pelos ADRs citados nos runs para confirmar status atual (Aceito vs Proposto) — auditorias podem registrar status defasado.

## Modo

Análise editorial estruturada, sem pressa. **Só consolidação + sequenciamento, zero alteração** — não criar plano em `docs/plans/`, não abrir PR, não tocar artefato dos eixos. Propostas individuais seguem para `/triage` separadamente.

## Saída persistente

Antes de devolver controle, gravar o resultado completo em `docs/audits/runs/<YYYY-MM-DD>-execution-roadmap.md`. Permite acompanhar checkboxes durante a execução das ondas e que decisões de bundle/dependência não evaporem se a sessão fechar.

## Encaminhamento das propostas

Propostas consolidadas pelo roadmap **não viram PR direto**. Cada onda decide entre dois caminhos:

- **Item solo:** `/triage <proposta>` por item.
- **Bundle declarado:** `/triage <bundle>` único produzindo plano cobrindo todos os itens do bundle (mesmo eixo arquitetural).

A auditoria de consolidação produz o roadmap; o `/triage` faz o alinhamento individual ou de bundle. Atualizações de status (`[x]` + link a PR) ficam por conta do operador conforme cada item shippa.
