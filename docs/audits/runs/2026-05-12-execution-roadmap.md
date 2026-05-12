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

- [x] **G_arch** — [ADR-024](../../decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md) + [plano](../../plans/procedures-cleanup-pos-merge.md) + [PR #57](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/57) (2026-05-12): extração de "Cleanup pós-merge" de `/triage §0` para `docs/procedures/cleanup-pos-merge.md` (categoria nova estabelecida em ADR-024 — sucessor parcial de ADR-001, paralela a `templates/`). `/triage` e `/release` referenciam o procedimento via `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cleanup-pos-merge.md`. Resolve L1 do audit (acoplamento textual). Path original `templates/cleanup-pos-merge.md` (proposto pelo audit) rejeitado por design-reviewer: colisão lexical com "Resolution protocol" + estiraria semântica de `templates/` (esqueletos preenchíveis vs procedimentos executáveis); decidido por pureza semântica via 4ª categoria sob `docs/`.
- [x] **D_arch** — [plano](../../plans/procedures-cleanup-pos-merge.md) Bloco 2 + [PR #57](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/57) (2026-05-12): auto-detect forge bilateral (`gh`+`glab`) aplicado no procedimento extraído (após G_arch). Sintaxe canonical para GitLab: `glab mr list --merged --source-branch <branch> --output json | jq -r '.[0].iid // empty'` (confirmada via docs oficiais durante gate; wording-alvo inicial divergia em `--state merged` e `--fields iid`). Gap operacional documentado: GitLab via `glab` requer `jq` no PATH — `glab` não embute jq como `gh --jq`.

**Onda 3a fechada (2026-05-12).** Bundle G_arch + D_arch shipped via [PR #57](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/57) (plano `procedures-cleanup-pos-merge`).

### 3b — hub-and-spoke de doutrina

- [x] **B_prose** — [plano](../../plans/hub-and-spoke-doutrina.md) Bloco 1 + [PR #58](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/58) (2026-05-12): nova seção `## Reviewer/skill report idioma` em CLAUDE.md operacionaliza, para 5 reviewers + `/triage`, a regra-mãe em `philosophy.md` → "Convenção de idioma"; ADR-007 cobre artefatos informativos fora deste escopo. 6 spokes referenciam o hub. Assimetria intencional: `code-reviewer` retém linha sobre rótulos estruturados (`Localização`/`Problema`/`Filosofia violada`/`Sugestão`) — subagent isolado não tem CLAUDE.md auto-loaded. Findings altos do design-reviewer absorvidos pré-commit (operacionalização vs fonte; rótulos no spoke; anti-drift grep).
- [x] **D_prose** — [plano](../../plans/hub-and-spoke-doutrina.md) Bloco 2 + [PR #58](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/58) (2026-05-12): seção "Linguagem ubíqua na implementação" em `philosophy.md` trimmed de 3 frases (princípio + dangling "frase-tese" + descrição de pipeline operacional `/triage` passo 4 → `/run-plan` passo 2 → `code-reviewer`) para 3 frases enxutas (princípio + frase-âncora sem dangling + remete a skills/agents). Sustenta onda anterior "philosophy.md: refatorar para conter apenas princípios" (BACKLOG `## Concluídos`). "no domínio" preservado vs `ubiquitous_language` (finding 3 do design-reviewer — papel é mecânica do toolkit; princípio em philosophy deve ler em termos universais).

**Onda 3b fechada (2026-05-12).** Bundle B_prose + D_prose shipped via [PR #58](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/58) (plano `hub-and-spoke-doutrina`).

## Onda 4 — trim cirúrgico em skills

Um único `/triage` produz plano "trim residual". Baixo risco, ganho cumulativo em clareza. Pode rodar em paralelo à Onda 3 se houver fôlego.

- [x] **F_arch** — commit cirúrgico (2026-05-12): passo 5 "Consolidação do backlog" absorvido como sub-fluxo do passo 4 (após subseção BACKLOG); passo 6 renumerado para 5. Caminho-sem-plano + edit cirúrgico direto no main (análogo a atualização cirúrgica de `docs/domain.md`/`docs/design.md` per spec §3); 2 drifts cross-SKILL pré-commit corrigidos (`/run-plan §3.5` ref para "passo 4 sub-fluxo Consolidação"; `/new-adr` ref para "passo 5"). Comportamento idêntico — refactor editorial puro.
- [x] **F_prose** — [plano](../../plans/trim-residual-editorial-onda4.md) Bloco 5(a) + [PR #59](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/59) (2026-05-12): preâmbulo de `/init-config` linha 13 compactado de ~50 → 32 palavras preservando refs ADR-003 + ADR-017 e a ratio (define o bloco vs consume).
- [x] **G_prose** — [plano](../../plans/trim-residual-editorial-onda4.md) Bloco 5(b) + [PR #59](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/59) (2026-05-12): bullet de `/init-config ## O que NÃO fazer` linha 128 **encolhido** (~30 → 15 palavras) em vez de removido — design-reviewer flagou bullet como guarda-checklist contra exceção localizada (per critério editorial em CLAUDE.md + ADR-017 § Editorial inheritance); operador escolheu opção "encolher" sobre 3 alternativas pós-finding, preservando função-checklist sem duplicar a ratio do preâmbulo.
- [x] **E_prose** — [plano](../../plans/trim-residual-editorial-onda4.md) Bloco 4 + [PR #59](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/59) (2026-05-12): `/run-plan §3.3` sanity check de docs convertido de 3 bullets de skip + 1 cutucada em prosa contínua → tabela `Condição | Skip silente? | Ação` + prosa pós-tabela com definições + mecânica da cutucada. Comportamento preservado integralmente.

### Onda 4 — achados extras absorvidos no mesmo PR

Re-execução de `prose-tokens` ([2026-05-12b](2026-05-12b-prose-tokens.md)) pós-fechamento das Ondas 1-3b identificou 4 cicatrizes residuais não-flagadas na run anterior. Incorporadas ao mesmo plano `trim-residual-editorial-onda4` como blocos adicionais:

- [x] **B-NEW** — [plano](../../plans/trim-residual-editorial-onda4.md) Bloco 1 + [PR #59](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/59) (2026-05-12): `agents/doc-reviewer.md` description 48 → 22 palavras removendo enumeração de 3 tipos de drift que duplicava `## O que flagrar` do body. **Auto-loaded por roteador a cada turn**.
- [x] **C-NEW** — [plano](../../plans/trim-residual-editorial-onda4.md) Bloco 2 + [PR #59](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/59) (2026-05-12): `CLAUDE.md` linhas 15-17 (Plugin layout / Agents) reduzidas a 1 frase apontando para "The role contract" table (linha 43). Single source para dispatch de reviewers. **Auto-loaded por turn**.
- [x] **A-NEW** — [plano](../../plans/trim-residual-editorial-onda4.md) Bloco 3 + [PR #59](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/59) (2026-05-12): `templates/plan.md` comentário dos 3 campos especiais (Termos ubíquos, ADRs candidatos, Linha do backlog) condensado de 2-3 linhas cada → 1 linha cada. Doc-reviewer flagou drift `conceito` vs `conceito ubíquo` no vocabulário canonical; corrigido pré-commit.
- [x] **D-NEW** — [plano](../../plans/trim-residual-editorial-onda4.md) Bloco 6 + [PR #59](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/59) (2026-05-12): `/release §4.5 item 5 "Aplicar"` sentença ~250 palavras reescrita como 4 sub-itens enumerados (Recovery condicional → Sync sempre → Reportar → Aplicar (a)-(e)). Tentativa inicial usou tabela `Estado | Ação | Sub-ações`; doc-reviewer flagou drift de comportamento (Recovery/Sync como mutuamente excludentes); reescrita preserva pipeline sequencial.

**Onda 4 fechada (2026-05-12).** Bundle E/F/G_prose + A/B/C/D-NEW shipped via [PR #59](https://github.com/fppfurtado/pragmatic-dev-toolkit/pull/59) (plano `trim-residual-editorial-onda4`). Redução agregada: -122 palavras em 6 arquivos (CLAUDE.md, agents/doc-reviewer.md, templates/plan.md, skills/run-plan, skills/init-config, skills/release). Item residual: F_arch (structural — reposicionar `/triage` passo 5; YAGNI até pain real surgir).

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
