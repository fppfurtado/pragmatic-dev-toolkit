# Plano — Generalizar vocabulário do filtro de admissão para projetos consumidores

## Contexto

O filtro de admissão de [ADR-045](../decisions/ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 2 está codificado em 2 superfícies runtime: o `AskUserQuestion` de `/new-adr` step 3.5 (label + description da opção 2; texto pós-decisão da saída) e o bullet em `agents/design-reviewer.md` § "Candidato a ADR draft que falha no filtro de admissão". Em ambas, a redação assume vocabulário interno do plugin (`philosophy.md` existe só neste repo), criando zona cinzenta para operador em projeto consumidor — que tipicamente tem apenas `CLAUDE.md` e mapeia o "doc epistêmico" para algo próprio (ARCHITECTURE.md, principles.md, MANIFESTO.md, etc.) ou não tem doc epistêmico nomeado.

Escopo cresceu pós-design-review (cutucada F2 absorvida opção b) para também neutralizar a seção vizinha `### Contradição com ADRs existentes ou philosophy.md` no mesmo `agents/design-reviewer.md` (linhas 94, 98-100) — preserva concretude pedagógica das referências `ADR-049`/`ADR-050` movendo-as para parentéticos "ex.: deste plugin".

**ADRs candidatos:** ADR-045 (origina o filtro de admissão; § Risco a vigiar constrange refinements pós-redesign a CLAUDE.md/git log fora de ADR-045 § Decisão), ADR-035 (autoriza formalização interna do plugin sem dor empírica do consumidor quando dentro do escopo "decisões internas").

**Linha do backlog:** plugin: avaliar generalização da saída `CLAUDE.md ou philosophy.md` do filtro de admissão

## Resumo da mudança

Reescrever 7 trechos em 2 arquivos para vocabulário consumer-agnóstico, preservando a bifurcação útil **mecânica vs epistêmica** que ADR-045 § Decisão parte 2 formalizou — esse critério continua acionável em qualquer contexto. `philosophy.md` aparece como exemplo concreto do plugin em parentéticos "ex.: deste plugin" / "ou equivalente do projeto", nunca prescritivamente.

Caminho (a) generalização editorial puro escolhido sobre (b) nova role `philosophy_doc` opt-in — direção (b) registrada como alternativa preservada no item original do BACKLOG (commit `08953d2`). Sem ADR — refinamento editorial puro per ADR-045 § Risco a vigiar (refinements pós-redesign → `CLAUDE.md` ou git log, não ADR-045 § Decisão).

Fora de escopo: tocar ADR-045 § Decisão (congelado per § Risco a vigiar); tocar `CLAUDE.md` § Editing conventions bullet sobre admission policy (já cita só "filter mechanism", neutro); ocorrências de `philosophy.md` legítimas em ambos os arquivos (mecânica de free-read no `design-reviewer.md` linhas 8, 18, 24, 28; descrição da condição (ii) de cutucada em `skills/new-adr/SKILL.md` linha 64; guia de formato de citação em `agents/design-reviewer.md` linha 130).

## Arquivos a alterar

### Bloco 1 — generalizar vocabulário do filtro + neutralizar exemplos pedagógicos da categoria vizinha {reviewer: doc}

`skills/new-adr/SKILL.md`:

- **Linha 51** — label + description da opção 2 do `AskUserQuestion`. Reformular literal:
  - Label atual: `` `CLAUDE.md ou philosophy.md — entendimento estabilizado` `` → Novo: `` `Doutrina canonical — entendimento estabilizado` ``.
  - Description atual: `"Refinamento de mecanismo, esclarecimento doutrinal, regra editorial estabilizada. `philosophy.md` = princípio epistêmico / convenção cross-cutting; `CLAUDE.md` = mecânica do plugin (lifecycle, naming, gate concreto, schema YAML, AskUserQuestion convention)."` → Novo: `"Refinamento de mecanismo, esclarecimento doutrinal, regra editorial estabilizada. Destino canonical do projeto sob 2 eixos: mecânica concreta (lifecycle, naming, gate, schema, AskUserQuestion convention) → `CLAUDE.md`; princípio epistêmico / convenção cross-cutting → `philosophy.md` ou equivalente do projeto."`

- **Linha 57** — texto pós-decisão da saída. Reformular preservando coerência com novo label:
  - Atual: `` Saída `CLAUDE.md ou philosophy.md` → parar criação do arquivo ADR; reportar: "Substância não passou no filtro de admissão de ADR — direcionar para `CLAUDE.md` ou `philosophy.md` per critério de desempate da saída escolhida. Sem ADR criado. Operador edita o documento alvo + commit como `docs:`/`chore:` conforme convenção." ``
  - Novo: `` Saída `Doutrina canonical` → parar criação do arquivo ADR; reportar: "Substância não passou no filtro de admissão de ADR — direcionar para a doutrina canonical do projeto (mecânica → `CLAUDE.md`; epistêmica → `philosophy.md` ou equivalente do projeto) per critério de desempate da saída escolhida. Sem ADR criado. Operador edita o documento alvo + commit como `docs:`/`chore:` conforme convenção." ``

`agents/design-reviewer.md`:

- **Linha 94** — section header. Reformular: `### Contradição com ADRs existentes ou philosophy.md` → `### Contradição com ADRs existentes ou doutrina canonical do projeto`.

- **Linha 98** — bullet pedagógico 1. Preservar concretude via parentético "ex.:":
  - Atual: `` - Plano introduz camada formal sob módulo de negócio sem citar a posição "flat e pragmática" de `philosophy.md`. ``
  - Novo: `` - Plano introduz camada formal sob módulo de negócio sem citar a posição "flat e pragmática" da doutrina canonical do projeto (ex.: `philosophy.md` deste plugin). ``

- **Linha 99** — bullet pedagógico 2. Preservar concretude via parentético "ex.:":
  - Atual: `` - Plano grava state em arquivo onde ADR-049 § Decisão (a) disse "git/forge é a fonte da verdade". ``
  - Novo: `` - Plano grava state em arquivo onde ADR registrado do projeto disse "git/forge é a fonte da verdade" (ex.: `ADR-049` § Decisão (a) deste plugin). ``

- **Linha 100** — bullet pedagógico 3. Preservar concretude via parentético "ex.:":
  - Atual: `` - Plano cria componente stack-specific quando ADR-050 § Decisão (a) separou skills (genéricas) de hooks (suffixados). ``
  - Novo: `` - Plano cria componente stack-specific quando ADR registrado do projeto separa categorias de componente (ex.: `ADR-050` § Decisão (a) deste plugin separa skills genéricas de hooks suffixados). ``

- **Linha 108** — bullet do filtro de admissão. Reformular preservando bifurcação:
  - Atual: `` - **Substância revela entendimento estabilizado** que deveria ir pra `CLAUDE.md` ou `philosophy.md` (refinamento de mecanismo, esclarecimento doutrinal, regra editorial estabilizada). ``
  - Novo: `` - **Substância revela entendimento estabilizado** que deveria ir pra doutrina canonical do projeto — `CLAUDE.md` para mecânica concreta, `philosophy.md` ou equivalente para epistêmica (refinamento de mecanismo, esclarecimento doutrinal, regra editorial estabilizada). ``

## Verificação end-to-end

Gates mecânicos:

1. **Counts de `philosophy.md` por arquivo** — esperados pós-mudança via `grep -cE "philosophy\.md" <path>`:
   - `skills/new-adr/SKILL.md`: 3 (linhas 51, 57 em parentético; 64 unchanged como descrição do reviewer scope).
   - `agents/design-reviewer.md`: 7 (linhas 8, 18, 24, 28 mecânica do free-read; 98 + 108 em parentético; 130 guia de citação). Diferença −1 vs pré-mudança (line 94 header neutralizado removendo o termo).

2. **Counts das novas formulações canonical** — esperados via `grep -cE "<padrão>" <path>`:
   - `"doutrina canonical"`: ≥4 ocorrências no conjunto dos 2 arquivos (label + description SKILL, saída text SKILL, header design-reviewer, bullet filtro design-reviewer = 5 esperadas; tolerância para variação editorial menor).
   - `"ou equivalente do projeto"`: ≥3 ocorrências (description SKILL, saída text SKILL, bullet filtro design-reviewer).
   - `"deste plugin"`: ≥3 ocorrências (3 parentéticos "ex.:" em design-reviewer linhas 98-100).

3. **Ausência de prescrição residual** — `grep -nE "(deveria ir pra|direcionar para) (\`CLAUDE\.md\` ou \`philosophy\.md\`|\`philosophy\.md\`)" skills/new-adr/SKILL.md agents/design-reviewer.md` retorna 0 linhas (prescrição direta foi neutralizada).

4. **Read manual** de `skills/new-adr/SKILL.md` linhas 46-58 + `agents/design-reviewer.md` linhas 94-113 — bifurcação mecânica vs epistêmica permanece legível; concretude pedagógica preservada via "ex.:".

## Decisões absorvidas

- skills/new-adr/SKILL.md linha 51: comprometer reformulação literal do label `CLAUDE.md ou philosophy.md` → `Doutrina canonical`, removendo a sub-bifurcação implícita "permanecer vs reformular" do plano (caminho-único).
- Verificação end-to-end: critério qualitativo "ocorrências legítimas" substituído por gates mecânicos (counts por padrão + ausência de prescrição residual via grep) (caminho-único).
