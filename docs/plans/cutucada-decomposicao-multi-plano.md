# Plano — Cutucada de decomposição multi-plano em /triage step 2

## Contexto

ROADMAP item 1 (commit 182b2b3): adicionar em `/triage` step 2 um bullet que detecte features grandes o suficiente para justificar decomposição em ≥2 planos coordenados, e intensificar a pergunta existente "caso menor que resolve 80%" para nomear essa alternativa. Pattern emergente confirmado pelo operador: ≥3 ocasiões históricas de partição manual via múltiplas invocações `/triage` por dor de tamanho.

Step 2 hoje tem três bullets que cobrem dimensões adjacentes mas distintas:

- **"Intenção vaga demais para triar"** (ADR-036, refinement #2): cutucada em prosa — resposta genuinamente free-form; intenção ainda não cristalizou.
- **"Escopo"**: pergunta direta sem cutucada formal — "o que entra/fica de fora; há caso menor que resolve 80%?".
- **"Bifurcação arquitetural"**: cutucada enum nominal-comparativa quando há 2 caminhos competindo; pressupõe intenção formada.

Gap: feature com intenção cristalizada + escopo claro + caminho único pode ainda ser grande demais para um plano. Nenhum dos 3 cobre. Resultado: plano único gigante OU múltiplos `/triage` manuais sem coordenação.

Modalidade da cutucada nova: **enum** (per ADR-006), confirmada pelo operador. Difere da cutucada de intenção vaga (prosa, ADR-036) porque a bifurcação YES/NO de decomposição é discreta — Other cobre descrições livres das facetas.

**Tensão com guardrail editorial do ADR-036.** Adicionar 4º bullet ao step 2 (já com 3 bullets-cutucada + 6 itens de checklist) aproxima do guardrail "não fazer entrevista exaustiva" citado em ADR-036 § Alternativas (b). Mitigação: o novo bullet só dispara via heurística qualitativa single-signal (operador consegue listar ≥3 facetas semanticamente independentes na descrição da intenção) — não é entrevista de descoberta; feature pequena não vê a pergunta. Se uso real revelar fricção (cutucada em features médias), revisitar via mecanismo de calibração descrito em `## Notas operacionais`.

Sem novo artefato; sem chain mechanism (campos `**Sucessor:**`/`**Predecessor:**` deferidos no ROADMAP).

**ADRs candidatos:** ADR-006 (enum em bifurcação discreta — fundamenta modalidade), ADR-036 (cutucada de intenção vaga em prosa no mesmo step — boundary + tensão de guardrail), ADR-035 (qualificação editorial: codifica pattern emergente ≥3x ad hoc).

**Linha do backlog:** plugin: cutucada de decomposição multi-plano em /triage step 2

## Resumo da mudança

Edits em `skills/triage/SKILL.md` step 2 ("Esclarecer gaps com o usuário"):

1. **Novo bullet "Tamanho / decomposição"** — inserido após "Escopo" e antes de "Superfícies além do código". **Heurística qualitativa single-signal**: "operador consegue listar ≥3 facetas semanticamente independentes na descrição da intenção (cada faceta seria objeto natural de seu próprio plano)". Sinal qualitativo aplicável em step 2 (timing antes do plano existir); alinha com estilo dos bullets adjacentes (intenção vaga: verbo aberto + objeto-direto ausente; bifurcação: 2 planos distintos satisfariam a frase). Cutucada via `AskUserQuestion` (header `Decomposição`, opções `Enumerar facetas como planos separados` / `Manter como plano único`; Other livre para variantes). Resposta `Enumerar` → operador descreve facetas em prosa pós-resposta; cada faceta vira `/triage` futuro isolado.

2. **Intensificar bullet "Escopo" existente** — após "Há caso menor que resolve 80%?", adicionar pointer: "Se não cabe em escopo menor, considerar bullet **Tamanho/decomposição** abaixo (pode ser ≥2 planos coordenados)."

3. **Boundary explícito enumerado** no texto do novo bullet:
   - **Com "Intenção vaga" (ADR-036):** lá intenção não cristalizou (sem critério operacional); aqui sim, mas escopo amplo.
   - **Com "Bifurcação arquitetural":** lá 2 caminhos competindo para mesmo objeto; aqui 1 caminho potencialmente dimensionado demais.
   - **Com "Escopo" (bullet imediatamente anterior):** lá pergunta "cabe num menor?"; aqui pergunta "precisa partir em ≥2?" como continuação quando a resposta foi "não".

4. **Precedência editorial:** cutucada de **Intenção vaga (ADR-036) precede** esta — decomposição pressupõe intenção cristalizada. Se ambas as heurísticas disparam na mesma execução, vagueness emerge primeiro; decomposition só faz sentido após intent ter critério operacional.

## Arquivos a alterar

### Bloco 1 — bullet decomposição + intensificação "Escopo" em /triage step 2 {reviewer: code}

- `skills/triage/SKILL.md`: em step 2, após o bullet "Escopo" e antes de "Superfícies além do código", inserir novo bullet "Tamanho / decomposição" com heurística qualitativa single-signal (operador consegue listar ≥3 facetas semanticamente independentes na descrição da intenção), texto da cutucada enum (header `Decomposição`, opções literais conforme `## Resumo da mudança`), boundaries enumeradas com 3 bullets adjacentes (Intenção vaga, Bifurcação arquitetural, Escopo), e nota de precedência editorial (Intenção vaga precede). Reformular bullet "Escopo" para terminar com pointer para "Tamanho/decomposição" mencionando "≥2 planos coordenados".

## Verificação end-to-end

- `grep -nE "Tamanho.*decomposi" skills/triage/SKILL.md` retorna ≥1 match no novo bullet.
- `grep -n "≥2 planos coordenados" skills/triage/SKILL.md` retorna match no bullet "Escopo" reformulado.
- `grep -n "Decomposição" skills/triage/SKILL.md` retorna match no header da cutucada.
- `grep -n "≥3 facetas" skills/triage/SKILL.md` retorna match no texto da heurística qualitativa.
- Inspeção textual: 3 boundary statements presentes (citando "Intenção vaga", "Bifurcação arquitetural", "Escopo"); nota de precedência presente.
- Bullet "Intenção vaga" (ADR-036) preservado intacto — novo bullet adiciona, não substitui.

## Verificação manual

- **Feature pequena** (operador consegue listar 1 faceta na descrição): nenhuma cutucada de decomposição emerge (heurística não dispara).
- **Feature ampla** (operador consegue listar ≥3 facetas semanticamente independentes; pode-se forçar com descrição rica): cutucada enum `Decomposição` aparece com opções literais especificadas; resposta `Manter como plano único` segue fluxo default sem fricção adicional.
- **Boundary com Intenção vaga** (verbo aberto + escopo grande, ex.: `/triage modernizar pipeline de export`): cutucada de **Intenção vaga** emerge primeiro (prosa, ADR-036); decomposição não dispara enquanto intenção não cristalizar com critério operacional.

## Notas operacionais

- Plano single-block — sem dependências internas.
- design-reviewer dispatcha automaticamente pré-commit (ADR-011); free-read prioriza ADRs candidatos listados em `## Contexto`.
- **Calibração da heurística qualitativa** (limiar de 3 facetas): operador roda `/note` ao ver a cutucada disparar pela primeira vez (e nas subsequentes se considerar over/under-trigger); reabre o limiar se ≥2 notas reportarem fricção concreta (cutucada em features médias = over-trigger; ausência de cutucada em features grandes = under-trigger). Paralelo aos gatilhos concretos de ADR-029 e ADR-031. Sem cross-ref ao item "Sucessor/Predecessor" do ROADMAP — aquele é sobre chain mechanism inter-plano, não calibração intra-bullet.
