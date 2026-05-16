# Plano — Extrair forge auto-detect para docs/procedures/

## Contexto

Onda 3 (parte 2) do roadmap `docs/audits/runs/2026-05-16-execution-roadmap.md` — proposta B_prose. Extrai a mecânica "auto-detect de forge" (parse `git remote get-url origin` → host detection → `gh` / `glab` / fallback) hoje duplicada em 4 SKILLs (`/release §5`, `/next §4.5`, `/run-plan §3.7`, `/archive-plans §1` critério 6) + 1 procedure existente (`docs/procedures/cleanup-pos-merge.md` — passo "Detecção de candidatos" §3) para um procedure consolidado em `docs/procedures/forge-auto-detect.md`. 3º item da categoria `docs/procedures/` (junto com `cleanup-pos-merge.md` e `cutucada-descoberta.md` da Onda 3 parte 1) — promove categoria para 3 itens, alinha critério Strong-stable de ADR-024 (hoje Medium por "categoria com 1 item suspeita").

**ADRs candidatos:** ADR-024 (categoria `docs/procedures/` — 3º item consolida critério para A_arch). ADR-022 § Decisão critério 6 documenta o caso `search <slug>` em prosa descritiva — não-tocado neste plano; procedure novo cross-refs ADR-022 como decisão de origem do uso (paralelo a tratamento de ADR-017+029 no Plan 1: ADR canonical de doutrina, procedure de mecânica derivada).

**Linha do backlog:** plugin: extrair auto-detect de forge (parse remote → gh/glab/fallback) para `docs/procedures/forge-auto-detect.md` — consolida mecânica hoje duplicada em 4 SKILLs (`/release §5`, `/next §4.5`, `/run-plan §3.7`, `/archive-plans §1` critério 6) + `docs/procedures/cleanup-pos-merge.md`. Onda 3 parte 2 (B_prose) do roadmap 2026-05-15/16; promove categoria `docs/procedures/` para 3 itens (fortalece ADR-024 para promoção via A_arch).

**Verificação dos 3 critérios cumulativos de ADR-024 § Decisão** (obrigatória per linha 65 do ADR):

- (i) Procedimento operacional: forge auto-detect é algoritmo executável (parse remote + match host + probe CLI), não esqueleto preenchível.
- (ii) ≥2 skills referenciam: 4 SKILLs (`/release`, `/next`, `/run-plan`, `/archive-plans`) + 1 procedure (`cleanup-pos-merge.md`) = 5 referrers.
- (iii) Acoplamento textual concreto: 5 sites duplicam hoje o parse `git remote get-url origin` + match `github.com`/`^gitlab\.` + fallback. Drift potencial entre sites já é classe de risco para `cleanup-pos-merge.md` ↔ /archive-plans critério 6 (regex idêntico).

## Resumo da mudança

Cria `docs/procedures/forge-auto-detect.md` (~30 linhas: algoritmo parse `git remote get-url origin` → match `github.com` → CLI `gh`; regex `^gitlab\.` → CLI `glab`; outros hosts → `unsupported-host`; CLI ausente OR jq ausente em GitLab path → `no-detection`). 4 SKILLs substituem ~25 w de detect inline por ~1 linha de referência ao procedure. `cleanup-pos-merge.md` também substitui seu próprio detect inline por ref ao novo procedure (evita duplicação cross-procedure). Net: ~100 w cross-skill.

Procedure devolve **4 outputs distintos** (`gh` / `glab` / `no-detection` / `unsupported-host`) — cada consumer decide policy local. Preserva exatamente as semânticas existentes:

- `cleanup-pos-merge.md` recebe `no-detection` para jq ausente em GitLab path → silently skip candidate (não cleanar > cleanar errado, doutrina atual preservada).
- `/archive-plans` critério 6 recebe `no-detection` → `degraded` (não-elegível esta invocação, retry após instalar).
- `/release`, `/next`, `/run-plan` recebem `no-detection` / `unsupported-host` → fallback textual com suggestion ao operador.

**Bifurcação rebatida — cross-procedure dependency vs procedure auto-contido.** Optamos por cross-procedure dependency (`cleanup-pos-merge.md` referencia `forge-auto-detect.md`) em vez de procedure auto-contido para evitar 6º site de duplicação. Custo: leitura de `cleanup-pos-merge.md` agora exige seguir 1 cross-ref para entender a detection completa. Aceito porque o passo de detection é genuinamente compartilhado entre 5 sites — duplicar nele contradiz o motivo da extração. Cada SKILL/procedure consumidor mantém seu próprio contexto local — gate `AskUserQuestion`, comandos pós-detect (`gh pr list`, `glab mr list`, `gh release create`, etc.) ficam na SKILL. Só a parte de detection migra.

## Arquivos a alterar

### Bloco 1 — Criar docs/procedures/forge-auto-detect.md {reviewer: code}

- `docs/procedures/forge-auto-detect.md`: novo. Estrutura:
  - Linha inicial cita ADR-024 como categoria-base (parity com `cleanup-pos-merge.md`).
  - Cross-ref a ADR-022 § Decisão critério 6 como decisão de origem do uso `search <slug>` (ADR-022 mantém prosa; procedure carrega algoritmo runtime — simétrico a ADR-017+029 no Plan 1).
  - Intro 1-parágrafo: propósito (detectar forge a partir de `origin`), consumidores típicos (operações em PR/MR/release/archival).
  - Algoritmo passo-a-passo: (1) `git remote get-url origin`; (2) match `github.com` → host = GitHub; (3) regex `^gitlab\.` (gitlab.com ou GitLab corporativo) → host = GitLab; (4) outros hosts → `unsupported-host`.
  - Probe de CLI por host detectado: GitHub + `gh` no PATH → `gh`; GitLab + `glab` + jq no PATH → `glab`. CLI ausente (mapped) OR jq ausente (GitLab path) → `no-detection`.
  - Notas: `gh --jq` embute jq (nenhuma dep externa); `glab` requer `jq` no PATH (`glab ... --output json | jq -r ...`).
  - **4 outputs distintos consumidos pela skill chamadora:**
    - `gh` — GitHub + gh disponível.
    - `glab` — GitLab + glab + jq disponíveis.
    - `no-detection` — host mapeado mas dependência ausente (CLI ou jq); consumer decide policy local (silent skip / degraded / fallback textual).
    - `unsupported-host` — host não-mapeado (Bitbucket, Codeberg, custom); consumer decide policy local.

### Bloco 2 — Wire 4 SKILLs ao procedure {reviewer: code}

Substituir bloco inline de detection (~25 w cada, incluindo regex/match) por linha-ref `Detectar forge conforme `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md`; o output (`gh`/`glab`/`no-detection`/`unsupported-host`) alimenta o comando abaixo.` (paridade exata com pattern `cleanup-pos-merge.md`):

- `skills/release/SKILL.md` §5: preservar comandos pós-detect específicos (`gh release create` / `glab release create`); policy local para `no-detection`/`unsupported-host` = fallback textual com link de docs.
- `skills/next/SKILL.md` §4.5: preservar lógica de cruzar PR list com items do backlog; policy local para `no-detection`/`unsupported-host` = pular check de PR aberto (operador valida manualmente).
- `skills/run-plan/SKILL.md` §3.7: preservar lógica de gate `Push + abrir PR`; policy local para `no-detection`/`unsupported-host` = enum `Push` (sem abrir PR) ou fallback textual.
- `skills/archive-plans/SKILL.md` §1 critério 6: preservar lógica de cross-ref a slug do plano (`gh pr list --search <slug>`); policy local para `no-detection`/`unsupported-host` = `degraded` (não-elegível esta invocação) per ADR-022 critério 6.

### Bloco 3 — Atualizar cleanup-pos-merge.md para referenciar forge-auto-detect {reviewer: code}

- `docs/procedures/cleanup-pos-merge.md` § "Detecção de candidatos" passo 3: substituir "Host detection" bullet inline por ref ao novo procedure; preservar lógica squash-aware específica (queries `gh pr list --state merged --head <branch>` / `glab mr list --merged --source-branch <branch>` / fallback `git branch -r --merged`) que é particularidade do uso em cleanup, não da detection. Policy local para `no-detection` (jq ausente em GitLab path) preservada exata: silently skip candidate (doutrina atual). Policy local para `unsupported-host`: fallback `git branch -r --merged origin/<main>` (já é o caminho atual).

### Bloco 4 — Atualizar roadmap marcando B_prose shipped {reviewer: doc}

- `docs/audits/runs/2026-05-16-execution-roadmap.md`: linha do item `B_prose` em Onda 3 `[ ]` → `[x]` com data + ref PR/commit ao concluir; entrada no `## Histórico de execução` ao final.

## Verificação end-to-end

- `ls docs/procedures/forge-auto-detect.md` existe; `wc -l` ~30 linhas.
- `grep -c '${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md' skills/release/SKILL.md skills/next/SKILL.md skills/run-plan/SKILL.md skills/archive-plans/SKILL.md docs/procedures/cleanup-pos-merge.md` retorna ≥1 por arquivo (5 sites, paridade `${CLAUDE_PLUGIN_ROOT}/`).
- `grep -nE "git remote get-url origin" skills/*/SKILL.md docs/procedures/cleanup-pos-merge.md` retorna **vazio** (motor de detection inline extraído). Definição literal só em `docs/procedures/forge-auto-detect.md`.

## Verificação manual

Cenários:

1. **GitHub via `gh`.** `git remote get-url origin` → `https://github.com/owner/repo`. `gh` instalado. Esperado: output `gh`; SKILLs constroem `gh pr list ...` / `gh release create ...` etc. Exercitar via `/release` neste próprio repo (origin = github).
2. **GitLab corporativo via `glab` + jq.** `git remote get-url origin` → `git@gitlab.acme.com:org/repo.git`. `glab` + `jq` instalados. Esperado: output `glab`. (Validação textual sobre fixture — sem GitLab corporativo no ambiente.)
3. **GitLab corporativo + jq ausente.** Mesma fixture mas sem `jq`. Esperado: output `no-detection`; cleanup-pos-merge silently skips o candidato; /archive-plans marca `degraded`; /release/next/run-plan caem em fallback textual.
4. **Host não-mapeado (Bitbucket, Codeberg).** `git remote get-url origin` → `bitbucket.org/...`. Esperado: output `unsupported-host`; cada consumer aplica policy local (fallback textual ou skip per contexto).
5. **CLI ausente em host mapeado.** `github.com` mas `gh` não no PATH. Esperado: output `no-detection` (não tenta `gh` cego); consumer aplica policy local.

## Notas operacionais

- **Reviewer dispatch:** Blocos 1-3 `{reviewer: code}` (procedure novo + SKILL/procedure edits substituem mecânica); Bloco 4 `{reviewer: doc}`.
- **Verificar que ADR-001 carrega o cross-ref a ADR-024** estabelecido pelo plano `procedures-cleanup-pos-merge` (invariante ADR-024 § Decisão linha 69). Se ausente, este plano adiciona; presente, prossegue.
- **Não editar ADR-022 § critério 6** — ADR fica canonical de doutrina (porquê e contexto histórico do uso `search <slug>`); procedure é a redação mecânica derivada (algoritmo runtime). Cross-ref bidirecional: procedure cita ADR-022, ADR-022 não precisa citar o procedure (ADR é estável; procedure pode evoluir editorialmente). Simétrico ao tratamento de ADR-017+029 no Plan 1.
- **Não consolidar comandos pós-detect.** Cada consumer mantém comando contextual:
  - `/release` § 5 → `gh release create`/`glab release create`
  - `/next` § 4.5 → `gh pr list`/`glab mr list`
  - `/run-plan` § 3.7 → `gh pr create`/`glab mr create`
  - `/archive-plans` § 1 critério 6 → `gh pr list --search <slug>`/`glab mr list --search <slug>`
  - `cleanup-pos-merge.md` → `gh pr list --state merged --head <branch>`/`glab mr list --merged --source-branch <branch>`
  Tentar abstrair os comandos seria YAGNI (cada uso tem semântica distinta).
- **Dependência sequencial relativa ao plano `procedures-cutucada-descoberta.md`** — opcional. Roadmap define ordem (cutucada primeiro pela cardinalidade 5 vs 4 + proximidade ADR-029). Merge em qualquer ordem é seguro quanto a overlap de arquivos; se este PR mergear primeiro, ADR-024 fica com 2 itens (forge + cleanup); se cutucada mergear primeiro, fica com 2 (cutucada + cleanup); ambos shipados → 3 itens (gatilho A_arch ADR-024 promotion).
- **Probe textual sobre o diff** em casos sem ambiente concreto (cenários 2, 3, 4) é aceitável — mecânica preserva-se per construção (procedure é AS-IS do que vive hoje espalhado, com 4-output explícito).
