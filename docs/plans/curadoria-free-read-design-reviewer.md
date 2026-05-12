# Plano — Curadoria do free-read do design-reviewer

## Contexto

Implementação editorial do [ADR-021](../decisions/ADR-021-curadoria-free-read-design-reviewer.md) — modo híbrido (anotação `**ADRs candidatos:**` + scan por keyword nos demais + threshold N=15) para o free-read do `design-reviewer`. Reabertura preventiva dos gatilhos de revisão #2 de [ADR-009](../decisions/ADR-009-revisor-design-pre-fato.md) e [ADR-011](../decisions/ADR-011-wiring-design-reviewer-automatico.md) (≥30 ADRs), antes de bater (hoje 21 com ADR-021 incluso; ritmo recente sugere 1-2 semanas).

Origem: proposta B_arch da auditoria arquitetural 2026-05-12 (`docs/audits/runs/2026-05-12-architecture-logic.md`), segundo item da Onda 1 do roadmap `docs/audits/runs/2026-05-12-execution-roadmap.md`.

**ADRs candidatos:** ADR-021 (matéria deste plano), ADR-009 (mecanismo refinado: free-read), ADR-011 (wiring automático que paga o custo de tokens), ADR-019 (precedente de cross-reference reviewer↔skill geradora; padrão paralelo).

(Campo `**ADRs candidatos:**` exercitado pré-implementação como dogfood — mecanismo de scan ainda não está no `design-reviewer`; design-reviewer fará free-read integral até o Bloco 1 landar. Anotação serve como preview e meta-coerência editorial.)

## Resumo da mudança

3 arquivos editoriais; nenhum código de produção. Mecânica do scan (mecânica editorial per ADR-021 § Trade-offs) é cristalizada **neste plano** como primeira iteração — refinamento iterativo previsto.

**Decisão de mecânica concreta (primeira iteração):**

- **Extração de keywords** do plano/draft: tokens significativos (≥4 chars, não-numéricos) do `## Contexto` + `## Resumo da mudança` (plano) ou `## Origem` + `## Decisão` (ADR draft), exceto stop-words.
- **Stop-words mínimas** (PT + EN comuns + meta-ambientais apenas): `o, a, os, as, de, do, da, dos, das, em, no, na, nos, nas, com, por, para, que, qual, e, ou, mas, the, of, and, or, but, in, on, at, for, to, with, by, from, this, that, these, those, plugin, toolkit, projeto, repo`. **Não stop-wordar** termos doutrinariamente significativos (`ADR`, `reviewer`, `mecanismo`, `dispatch`, `doutrina`, `skill`, `agent`, `hook`, `operador`, `plano`) — são exatamente o vocabulário em que decisões estruturais se exprimem; stop-wordar subtrai sinal. Trade-off: lista mais inclusiva produz match mais frequente (mais false-positives via plano que toca "skill" matchando ADR genérico sobre skill); aceito na primeira iteração porque false-positive custa tokens, false-negative custa cobertura.
- **Cabeçalho do ADR não-anotado para scan:** linhas 1-N onde N inclui pelo menos até o final da `## Decisão` (ADRs do plugin **não têm frontmatter**; começam com `# ADR-NNN: <título>` + `**Data:**` + `**Status:**` + `## Origem` + `## Contexto` + `## Decisão`). Heurística operacional: ler até o segundo `##` após `## Decisão`, ou primeiras 60 linhas se delimiter não bater — suficiente para capturar título + Origem + Contexto + Decisão (núcleo doutrinário; § Consequências/Alternativas/Gatilhos ficam fora).
- **Critério de match:** case-insensitive substring; **≥2 keywords** matches no cabeçalho confirma relevância. Alternativas rebatidas:
  - `≥1` é permissivo demais: ADR só compartilhando termo genérico (`feature`, `política`) matcharia acidentalmente. Mesmo com stop-wordless agressivo, há vocabulário cruzado entre ADRs sem doutrina compartilhada.
  - `≥3` é restritivo demais: ADR pequeno com matching legítimo em 2 termos (ex.: "warning" + "pré-loop" no ADR-020 contra plano sobre `/run-plan`) ficaria fora. Primeira iteração calibra inclusiva; gatilho de revisão ajusta.
- **Threshold de ativação:** `#ADRs em docs/decisions/*.md ≤ 15` → mecanismo desliga, free-read completo. Acima → scan ativa.

## Arquivos a alterar

### Bloco 1 — `agents/design-reviewer.md` {reviewer: doc}

Adicionar seção `## Curadoria do free-read` (após `## Free-read em runtime` ou substituindo-a) descrevendo:

- Leitura prioritária dos ADRs listados em `**ADRs candidatos:**` (do `## Contexto` do plano ou `## Origem` do ADR draft). Integral.
- Scan dos demais ADRs com mecânica concreta acima (extração de keywords + stop-words + cabeçalho + match).
- Threshold N=15: `ls docs/decisions/ADR-*.md | wc -l ≤ 15` → modo legacy (free-read completo); acima → scan ativa.
- `docs/philosophy.md` sempre integral (volume pequeno, doutrina-base cross-cutting).
- **Invariante de relatório:** reportar quais ADRs foram lidos integralmente (anotados + scan-matched) vs filtrados — transparência sobre o subset analisado. **Site editorial:** nota explícita ao final da seção `## Curadoria do free-read` declarando o invariante; **não** acrescentar bullet em `## Como reportar` (que é template por-finding, escopo diferente).

Prosa deve declarar mecânica determinística (per ADR-021 § Trade-offs) — operador deve conseguir reproduzir mentalmente quais ADRs entram no input.

### Bloco 2 — `skills/triage/SKILL.md` {reviewer: doc}

Step 4, dentro de `**Plano (papel: `plans_dir`):**` → `No `## Contexto`:`, acrescentar bullet sobre `**ADRs candidatos:**` análogo ao bullet existente de `**Termos ubíquos tocados:**`:

```markdown
- Se o passo 1.5 (listar ADRs relacionados) identificou ADRs concretos tocados/contradictados pela mudança, incluir `**ADRs candidatos:** ADR-NNN (motivo curto), ADR-MMM (motivo curto)` — mensageiro para o design-reviewer priorizar leitura integral desses ADRs (paralelo a `**Termos ubíquos tocados:**`). Campo opcional: operador que não identifica ADR específico omite, e o reviewer faz scan dos demais (per ADR-021).
```

Step 1.5 (já existente em prosa: "decisions_dir — listar ADRs relacionados; ler na íntegra apenas os que o pedido contradiz/estende") fica como insumo natural — o passo já produz a lista que vira candidata para anotação.

### Bloco 3 — `templates/plan.md` {reviewer: doc}

Adicionar placeholder + comentário explicativo na seção `## Contexto`, dentro do `<!-- ... -->` que já documenta `**Termos ubíquos tocados:**` e `**Linha do backlog:**`:

```markdown
**ADRs candidatos:** ADR-NNN (motivo curto), ADR-MMM (motivo curto)
  Inclui ADRs que o operador identifica como tocados/contradictados pela mudança.
  Reviewer prioriza leitura integral desses; scan automático cobre os demais (per ADR-021).
  Campo opcional — operador que não sabe quais ADRs aplicam simplesmente omite.
```

## Verificação end-to-end

Sem `test_command` neste repo (per `CLAUDE.md`). Inspeção textual:

1. **Bloco 1 (agent):** abrir `agents/design-reviewer.md` e confirmar seção `## Curadoria do free-read` presente, descrevendo mecânica determinística (extração de keywords + stop-words + cabeçalho + match ≥2 + threshold N=15). Reviewer reportando subset analisado no relatório.
2. **Bloco 2 (skill):** abrir `skills/triage/SKILL.md` e confirmar bullet sobre `**ADRs candidatos:**` no step 4, paralelo a `**Termos ubíquos tocados:**`.
3. **Bloco 3 (template):** abrir `templates/plan.md` e confirmar placeholder + comentário no `<!-- ... -->` da seção `## Contexto`.
4. **Coerência cross-doc:** `grep -n "ADRs candidatos" agents/design-reviewer.md skills/triage/SKILL.md templates/plan.md` retorna 3 sites com nomenclatura consistente.

## Verificação manual

Cenários **enumerados** (per `/triage` § Surface não-determinística — matching de strings contra dado real exige cenários concretos, não direção genérica). Não-bloqueantes para o done; registram empiricamente o comportamento do mecanismo.

1. **Cenário "plano sobre wiring/reviewer"** (próxima `/triage` que produzir plano nessa área): invocar `design-reviewer` no plano e confirmar que o relatório inclui no subset analisado **ADR-009** (revisor design pré-fato) e **ADR-011** (wiring automático) — sejam por anotação manual em `**ADRs candidatos:**` ou por scan-match. Esperado: ambos presentes.
2. **Cenário "plano sobre idioma/audiência"** (hipotético — próximo plano que toque convenções de idioma): confirmar que o subset inclui **ADR-007** (artefatos informativos) e **ADR-012** (discoverability/landing). Confirmar que **ADR-013** (CI lint) **não** entra (sem overlap doutrinário com idioma). Validar discriminação.
3. **Cenário "próxima `/new-adr` standalone"** (qualquer ADR novo): confirmar relatório do `design-reviewer` lista explicitamente ADRs lidos integralmente vs filtrados — invariante editorial do Bloco 1 cumprida.
4. **Verificar false negative cumulativo:** se em qualquer dos cenários acima o operador identifica ADR doutrinariamente relevante que ficou de fora do subset, capturar como Validação (entrada em `## Pendências de validação`) para refinamento da heurística — exercita o gatilho de revisão #1 do ADR-021 (scan zero-match onde operador percebe omissão).
5. **Verificar tokens economizados (qualitativo):** comparar tamanho do contexto da invocação pós-shipping com a invocação que produziu o ADR-021 (free-read integral de 20 ADRs nessa sessão). Sem instrumentação automatizada — observação editorial; serve só para validar direção do trade-off do ADR-021.

## Notas operacionais

- **Ordem dos blocos importa pouco** — os 3 arquivos são independentes. Sugestão: Bloco 1 primeiro (agent codifica mecânica), depois 2-3 (skill + template que usam o campo declarado pelo agent).
- **Reviewer dispatch** durante o loop deste plano: ainda na mecânica legacy (free-read integral) até Bloco 1 mergear. Não há transição mid-plano — primeira invocação pós-Bloco-1 usa a nova mecânica.
- **Roadmap** (`docs/audits/runs/2026-05-12-execution-roadmap.md`) tem entrada `[ ] B_arch` que vira `[x] B_arch → ADR-021 + plano (2026-05-12)` no bloco extra do passo 3.4 do `/run-plan` — mas, sob convenção do C_arch, o roadmap é atualizado manualmente no commit unificado do `/triage` (sem linha BACKLOG granular).
- **Smoke pós-shipping no consumer externo** (e.g., PJe) é gatilho de validação adicional — observar se `/triage` sugere `**ADRs candidatos:**` em decisões estruturais e se operador percebe valor.
- **`docs/install.md` inalterado nesta iteração** — smoke do mecanismo coberto pela `## Verificação manual` deste plano. Promover para checklist em `docs/install.md` em release subsequente se o mecanismo estabilizar (sinal: nenhum gatilho de revisão do ADR-021 disparou em 2-3 invocações reais).
