# Roadmap de execução — auditorias 2026-05-12

Sequência recomendada para implementar as propostas das duas auditorias do dia:

- `docs/audits/runs/2026-05-12-architecture-logic.md` — propostas com sufixo `_arch`.
- `docs/audits/runs/2026-05-12-prose-tokens.md` — propostas com sufixo `_prose`.

**Nota para sessão futura:** leia os 2 audits do dia antes de pegar um item daqui — cada proposta refere-se a achados específicos com contexto que não cabe nesta lista.

**Convenção de status:** `[ ]` pendente · `[~]` em andamento · `[x]` concluído (atualizar com link a commit/PR/ADR shippado + data curta).

**Convenção de encaminhamento:** cada item entra pelo fluxo padrão `/triage <proposta>` que decide artefato (linha de backlog, plano, ADR, atualização cirúrgica). Bundles indicados explicitamente abaixo passam por **um único** `/triage` produzindo plano cobrindo os itens agrupados.

---

## Onda 1 — antecipar gatilhos críticos

Cada item sozinho. ADR-worthy ou addendum. Ordem: mais barato primeiro; ADRs novos depois.

- [x] **C_arch** — [ADR-020](../../decisions/ADR-020-criterio-mecanico-admissao-warnings-pre-loop.md) (2026-05-12): critério mecânico de admissão de warnings pré-loop em `/run-plan`. Reabertura preventiva de ADR-002 antes do 6º warning. ADR sucessor (não adendo — rebatida em § Alternativas (a)) com 7 findings do `design-reviewer` absorvidos pré-commit.
- [x] **B_arch** — [ADR-021](../../decisions/ADR-021-curadoria-free-read-design-reviewer.md) + [plano](../../plans/curadoria-free-read-design-reviewer.md) + [PR #54](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/54) (2026-05-12): curadoria de free-read do `design-reviewer` em modo híbrido (anotação `**ADRs candidatos:**` + scan + threshold N=15). Implementação shippada em 3 blocos doc-only (design-reviewer + triage + template) + bloco extra do sanity de docs no README.
- [x] **E_arch** — [ADR-022](../../decisions/ADR-022-politica-archival-docs-plans.md) + [plano](../../plans/archive-plans.md) + [PR #55](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/55) (2026-05-12): política de archival para `docs/plans/` via skill nova `/archive-plans` (preview-first; layout `archive/<YYYY-Qx>/`; `git mv` non-destructive; threshold N=2 semanas calibrado pelo operador antes do primeiro uso). Implementação shippada em 2 blocos doc-only + bloco extra de calibração N=4→N=2.

## Onda 2 — bundle editorial auto-loaded

Um único `/triage` produz plano "tightening editorial — auto-loaded". Tudo toca CLAUDE.md + frontmatters; cada turn paga footprint inteiro — atacar junto faz a redução render imediatamente.

- [x] **A_arch** — [ADR-023](../../decisions/ADR-023-criterio-mecanico-disable-model-invocation-skills.md) + [plano](../../plans/tightening-editorial-auto-loaded.md) Bloco 1 + [PR #56](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/56) (2026-05-12): critério mecânico cumulativo (blast radius local + pushes/PRs gateados por enum + sem autoinvocação cross-turn → `false`) + tabela retroativa às 9 skills. ADR sucessor do BACKLOG `## Concluídos` linha 43. Caminho doutrinário-sem-ADR rejeitado por 2 findings altos do `design-reviewer` (3 ambiguidades concretas + memory `feedback_adr_threshold_doctrine`); 6 findings adicionais no draft do ADR-023 absorvidos pré-commit.
- [x] **A_prose** — [plano](../../plans/tightening-editorial-auto-loaded.md) Bloco 2 + [PR #56](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/56) (2026-05-12): 4 cicatrizes compactadas em CLAUDE.md (pattern "From v1.11.0 onward" erradicado nas 2 ocorrências; "Release cadence" comprimido 2→1 sentença; "Critério editorial" comprimido 4→2 sentenças). Auditoria flagrava 3 ocorrências; bundle executou as 4 instâncias do pattern (fidelidade ao pattern, não à enumeração).
- [x] **C_prose** — [plano](../../plans/tightening-editorial-auto-loaded.md) Bloco 3 + bloco extra + [PR #56](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/56) (2026-05-12): 4 frontmatter descriptions encurtadas (idioms internos saem dos descriptions auto-loaded; `Python`/`Java` preservados como anchors lexicais per finding 5 do `design-reviewer`). Bloco extra absorveu drifts user-facing pré-existentes expostos pelo bundle: README.md:14 (stack list de `/gen-tests` faltava Java) + docs/install.md:36 (smoke list omitia 3 skills shippadas) + docs/install.md:53 (prose duplicada do `/init-config`) + CLAUDE.md:15 (mesma omissão da smoke list).

## Onda 3 — bundles estruturais cross-skill

Dois `/triage` independentes; cada um produz um plano próprio.

### 3a — cleanup pós-merge extraído + forge bilateral

- [ ] **G_arch** — extrair "Cleanup pós-merge" de `/triage §0` para `templates/cleanup-pos-merge.md`. Toca `/triage` + `/release` (que referencia textualmente o passo 0 hoje).
- [ ] **D_arch** — estender auto-detect forge bilateral (`gh` + `glab`) ao cleanup extraído. **Depende de G_arch** — executar G primeiro torna D wire-up trivial.

### 3b — hub-and-spoke de doutrina

- [ ] **B_prose** — consolidar fórmula "Idioma do relatório" em CLAUDE.md (seção curta `## Reviewer/skill report idioma`) + referenciar nos 6 sites (5 agents + `/triage`).
- [ ] **D_prose** — migrar "Linguagem ubíqua na implementação" de `philosophy.md` para princípio puro (remover descrição do pipeline operacional).

## Onda 4 — trim cirúrgico em skills

Um único `/triage` produz plano "trim residual". Baixo risco, ganho cumulativo em clareza. Pode rodar em paralelo à Onda 3 se houver fôlego.

- [ ] **F_arch** — reposicionar `/triage` passo 5 (Consolidação do backlog) como sub-fluxo do passo 4.
- [ ] **F_prose** — compactar preâmbulo de `/init-config` (cicatriz "Diferente das demais skills do toolkit..." que explica doutrina interna).
- [ ] **G_prose** — remover bullet redundante em `/init-config ## O que NÃO fazer` ("Não emitir cutucada de descoberta de ADR-017 dentro desta skill" — já dito no preâmbulo).
- [ ] **E_prose** — trocar prosa por tabela em `/run-plan §3.3` (sanity check de docs).

## Diferida

- [ ] **H_arch** — recusar cross-mode `backlog: local + plans_dir: canonical` no `/init-config`. Só com evidência empírica de uso não-intencional (não acionar agora).

---

## Pontos de atenção cross-onda

- **Re-rodar `prose-tokens` depois da Onda 3a.** G_arch sozinho remove ~200 palavras de `/triage §0`; números finais da auditoria mudam materialmente. Refinar alvos restantes evita gastar prosa sobre realidade já alterada.
- **Release cadence.** Onda 1 sozinha já é coherent set (3 ADRs + addendum) → considerar `/release minor` ao fim. Ondas 2-4 podem acumular em `main` ou bumpar entre, conforme energia.
- **`design-reviewer` em B_arch.** Ele lê todos os ADRs por invocação (ADR-009), incluindo ADR-009/011 que B_arch refina. Ponto cego conhecido (ADR-009 § Limitações). Ler findings com atenção; pode rebater contradição com sua própria doutrina-base que está sendo reescrita.
- **Não bundle entre auditorias se a área não for a mesma.** Bundle válido: A_arch + A_prose + C_prose (mesmo eixo auto-loaded). Bundle inválido: B_arch (ADR de reviewer) + B_prose (consolidar idioma do relatório) — cross-purpose.

---

## Histórico de execução

(Atualizar conforme cada item shippa — link a commit/PR/ADR + data curta.)
