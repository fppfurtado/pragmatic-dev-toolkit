# Plano — Skip silente doc-reviewer em edits conservadores

## Contexto

`/run-plan §2 item 3` codifica hierarquia mais-específico-vence para dispatch de reviewer per bloco (per ADR-062 § Pattern de dispatch). Atualmente toda invocação em doc-only ampla dispara `doc-reviewer`. Pattern empírico cross-week 2026-06-15 → 2026-06-20 (6 invocações em 4 sessões consecutivas, todas close-clean) sinaliza cerimônia per ADR-002 § Decisão.

[ADR-067](../decisions/ADR-067-skip-silente-doc-reviewer-em-edits-conservadores-via-predicado-de-sibling-pattern.md) (criado neste `/triage`, status Proposto) codifica skip silente como nova exceção posicionada APÓS as 3 exceções ADR-062 + só ativa quando resolvido para `doc-reviewer`. Predicado heurístico-semântico (predominantemente additive AND bullet inserido em ≥2 siblings imediatos de mesmo gabarito sintático) avaliado pelo LLM em runtime.

ADR-067 inclui **§ Override do critério N=3** explicitando 7ª aplicação consecutiva da onda Override (após ADR-057/-061/-062/-063/-064/-065) — fragilidade epistêmica reconhecida (cluster homogêneo cross-week numa mesma reforma editorial). Critério de erosão auditável codifica 3 cláusulas (false-positive + false-negative + over-fitting >80% same-cluster) para monitoring mecânico.

**Linha do backlog:** #131: `/run-plan` — dispatch logic para skip `doc-reviewer` em edits conservadores (sub-N3)

**ADRs candidatos:** ADR-067 (sucessor parcial primário — esta implementação materializa § Decisão), ADR-062 (sucessor parcial — extends § Pattern de dispatch), ADR-002 (anti-cerimônia — princípio materializado), ADR-043 § Ockham operacionalizado #4 (critério satisfeito no piso com fragilidade).

## Resumo da mudança

Refinement prose-only de `skills/run-plan/SKILL.md §2 item 3` adicionando cláusula de skip silente `doc-reviewer` per ADR-067 § Decisão. Cláusula posicionada APÓS as 3 exceções pré-existentes da hierarquia (narrow → `prompt-reviewer`; ampla → `doc-reviewer`; misto → `doc-reviewer`), atua como filtro de pós-processamento sobre resolução `doc-reviewer`. Resolução para `prompt-reviewer` ou `code-reviewer` não aciona skip — fora do escopo empírico per § Limitações.

Predicado heurístico-semântico (predominantemente additive + bullet em ≥2 siblings imediatos de mesmo gabarito sintático), avaliado pelo LLM em runtime; default-conservador resolve a favor do dispatch normal quando qualifiers ambíguos.

Alternativas rebatidas no `/triage` + ADR-067 § Alternativas considerada: (a) sub-tool determinístico (predicado é semantic by design); (b) inclusão de predicado P2 template replication (défice de evidência empírica — 1 caso edge fora do P1); (c) scope generalizado para todos reviewers (cluster específico a doc-reviewer); (d) posicionamento ANTES das exceções ADR-062 (engoliria prompt-reviewer em paths narrow puros — contradição com § Limitações).

## Arquivos a alterar

### Bloco 1 — skip clause em §2 item 3 {reviewer: prompt}

- `skills/run-plan/SKILL.md`
  - §2 item 3 — adicionar nova exceção **APÓS** as 3 exceções existentes da hierarquia (não antes): "**Exceção skip silente doc-reviewer em edits conservadores** (per ADR-067): SE a hierarquia anterior resolveu o bloco para `doc-reviewer` (ampla OR misto narrow+ampla) AND o diff satisfaz predicado heurístico-semântico — **predominantemente additive** (sem deletes ≥2 linhas de conteúdo prose; whitespace/typo correction permitido) AND **bullet/linha nova inserida em seção/lista onde ≥2 siblings imediatos seguem mesmo gabarito sintático** (mesmo prefixo bold, mesmo nível de indent, mesma estrutura grosso modo) — → skip silente (sem invocação de reviewer). Resolução para `prompt-reviewer` (path narrow puro) OR `code-reviewer` (default) → skip não ativa. Default-conservador a favor do dispatch normal quando qualifiers ambíguos."
  - Manter prosa cirúrgica — preservar estrutura das 3 exceções pré-existentes (narrow, ampla, bloco misto) e do default `code-reviewer`.

### Bloco 2 — bullet ADR-067 em CLAUDE.md § Editing conventions {reviewer: doc}

- `CLAUDE.md`
  - § Editing conventions — adicionar bullet paralelo aos siblings dos ADRs irmãos da onda Override N=3 (ADR-057/-061/-062/-063/-064/-065): `**Skip silente doc-reviewer em edits conservadores via predicado de sibling pattern**: 7ª aplicação consecutiva onda Override N=3 (após ADR-057 → -065); crítério ADR-043 § Ockham operacionalizado #4 atingido no piso (3 cross-session em 5 dias adjacentes, contexto homogêneo) com fragilidade epistêmica reconhecida per [ADR-067](docs/decisions/ADR-067-skip-silente-doc-reviewer-em-edits-conservadores-via-predicado-de-sibling-pattern.md) § Override. Nova exceção em /run-plan §2 item 3 posicionada APÓS hierarquia ADR-062 + só ativa quando resolvido para doc-reviewer + predicado heurístico-semântico (predominantemente additive + bullet em ≥2 siblings imediatos de mesmo gabarito sintático) bate; monitoring via critério de erosão auditável 3 cláusulas (false-positive + false-negative + over-fitting >80% same-cluster).`
  - Edit replica template pré-existente (bullet sibling em § Editing conventions paralelo a ADR-057/-061/-062/-063/-064/-065). Diff predominantemente additive (sem deletes ≥2 linhas). **Auto-skip do doc-reviewer per ADR-067 § Decisão é elegível mecanicamente** — meta-recursivo: o próprio bullet codificando o skip é exemplo do pattern. Reviewer dispatch atual `{reviewer: doc}` honra spec até o `/run-plan` shipping; pós-shipping este tipo de edit cai no skip.

## Verificação end-to-end

Repo sem suíte de testes automatizada (`test_command: null` per CLAUDE.md). Validação centralizada em `## Verificação manual` abaixo. Critérios end-to-end mecânicos pré-merge:

- `grep -n "Filtro pós-resolução skip silente.*doc-reviewer" skills/run-plan/SKILL.md` retorna ≥1 linha (cláusula codificada; cláusula renomeada via prompt-reviewer F2 absorção pré-commit Bloco 1).
- `grep -n "ADR-067" skills/run-plan/SKILL.md` retorna ≥1 linha (cross-ref ao ADR).
- `awk` extrai posicionamento da cláusula §2 item 3 — confirmar APÓS as 3 exceções pré-existentes (narrow/ampla/misto), não antes.

## Verificação manual

Surface não-determinística (dispatch decision baseada em julgamento semântico do LLM sobre diff structure) — cenários exercitam casos positivos (skip esperado) e negativos (skip não esperado) extraídos do cluster cross-week + edge cases identificados em ADR-067 § Limitações.

**Casos POSITIVOS** (skip esperado — não invocar doc-reviewer):

- **C1: Bullet sibling paralelo em CLAUDE.md § Editing conventions** (cluster 2026-06-15 1ª-3ª intra-sessão). Diff insere bullet em mesmo indent level que ≥4 siblings imediatos (ADR-057/-061/-062/-063/-064 bullets). Esperado: SKILL prose direciona `/run-plan` a skipar doc-reviewer; commit avança sem invocação. Diff sintético exemplo (operador `git apply` em worktree de teste):

  ```diff
  @@ -X,Y +X,Z @@ ## Editing conventions
   - **Heurística Y existente per ADR-NNN**: ...
   - **Heurística Z existente per ADR-NNN**: ...
  +- **Decisão sintética irmã per ADR-TEST**: predicado bate (predominantemente additive + ≥2 siblings imediatos de mesmo prefixo bold `**X**:`).
  ```

- **C2: Sub-bullet em README.md § What's inside `/new-adr` entry** (cluster 2026-06-15 2ª intra-sessão). Diff insere sub-bullet em mesmo indent level que ≥2 siblings (entries de outras skills). Esperado: skip. (Mesmo formato C1; trocar surface para `README.md` tabela entries.)
- **C3: Parênteses paralelo em docs/install.md step 12** (cluster 2026-06-20). Diff substitui parênteses no contexto de sub-passos a-f com formato análogo. Esperado: skip. (Mesmo predicado bate; surface diferente — parênteses descritivo paralelo a sub-passos.)

**Caso BOUNDARY** (qualifiers ambíguos — default-conservador):

- **C5b: Edit em seção com mistura parcial de sibling formats** (e.g., 1 sibling com prefixo `**Bold:**`, 1 sibling sem prefixo bold no mesmo indent level). Predicado bate parcialmente; LLM aplica default-conservador per ADR-067 § Decisão. Esperado: dispatch normal `doc-reviewer`.

**Casos NEGATIVOS** (skip não esperado — doc-reviewer deve disparar):

- **C4: Diff inclui DELETE de conteúdo significativo** (≥2 linhas de prose deletadas; não predominantemente additive). Esperado: dispatch normal doc-reviewer.
- **C5: Diff insere bullet em indent level onde há apenas 1 sibling adjacente.** Esperado: dispatch normal.
- **C6: Diff insere estrutura nova (e.g., novo header `##`, novo bloco code) que não replica sibling.** Esperado: dispatch normal.
- **C7: Path narrow puro (`docs/plans/<slug>.md`) com diff satisfazendo predicado.** Bloco resolvido para `prompt-reviewer` per ADR-062; cláusula skip NÃO ativa (escopo restrito a doc-reviewer per ADR-067 § Limitações). Esperado: `prompt-reviewer` dispara normalmente.
- **C8: Path code (`<module>.py`) sem anotação com diff satisfazendo predicado** (e.g., adicionar bullet a docstring com 4 itens análogos). Bloco resolvido para `code-reviewer` (default sem anotação); cláusula skip NÃO ativa (escopo restrito a doc-reviewer per ADR-067 § Limitações). Esperado: `code-reviewer` dispara normalmente.

Para cada cenário, executar `/run-plan` sobre plano sintético em worktree de teste; observar se doc-reviewer/prompt-reviewer é invocado (cenários NEGATIVOS + C7) ou skipado (cenários POSITIVOS).

## Notas operacionais

- ADR-067 já criado neste `/triage` via `/new-adr` delegada (status Proposto). Plano + ADR commitados como unidade atômica no `/triage` step 5.
- Edit em `skills/run-plan/SKILL.md` cai em path-set narrow (ADR-062 § Pattern de dispatch) → `prompt-reviewer` disparará no `/run-plan` per bloco. Findings sobre qualifiers semânticos do predicado podem emergir; absorver/cutucar per ADR-053 § Decisão (c) durante execução.
- ADR-067 § Override do critério N=3 explicita 7ª aplicação consecutiva da onda Override; fragilidade epistêmica monitorada via critério de erosão auditável (3 cláusulas: false-positive + false-negative + over-fitting >80% same-cluster) em auditoria post-mortem semestral.

## Pendências de validação

- Smoke comportamental leve pós-`/reload-plugins` confirmando que `/run-plan` runtime aplica o filtro skip silente conforme cláusula "Filtro pós-resolução skip silente doc-reviewer" em `skills/run-plan/SKILL.md` §2 item 3 nos 9 cenários do `## Verificação manual` acima (C1-C8 + C5b). Manual simulation in-flight via leitura da worktree SKILL.md (não-autoritativa per dogfood-recursive limit) validou predicate logic 9/9 PASS; cache do plugin `~/.claude/plugins/cache/fppfurtado-pragmatic-dev-toolkit/pragmatic-dev-toolkit/3.12.0/skills/run-plan/SKILL.md` carrega versão pré-ADR-067 — pós-reload, comportamento real precisa confirmar.

## Decisões absorvidas

- F2 Bloco 1 anotação `{reviewer: prompt}`: mantida explícita (valor informativo) — reviewer reconheceu como aceitável (caminho-único).
- F3 § Verificação manual: adicionado C8 simétrico (path code `.py` com diff bate predicado → `code-reviewer` dispara) — cobertura simétrica per ADR-067 § Limitações (caminho-único).
- F4 § Verificação manual C1: adicionado snippet de diff sintético inline para materializar predicado em surface não-determinística; C2/C3 referenciam mesmo template (caminho-único).
- F5 § Verificação manual: adicionado C5b (boundary qualifiers ambíguos → default-conservador) materializando cláusula de ADR-067 § Decisão (caminho-único).
- F6 § Notas operacionais bullet 2: removida cross-ref supérflua a ADR-063 (auto-trigger em `/triage` step 5, não em `/run-plan` per-bloco) — preserva precisão (caminho-único).
