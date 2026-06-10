# Forge auto-detect

Procedimento compartilhado para detectar o forge a partir do remote `origin`. Skills consumidoras leem este arquivo via Read e executam o algoritmo abaixo. Categoria `docs/procedures/` estabelecida em [ADR-051](../decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (c). Caso de uso de origem do consumer `/archive-plans` critério 6 — verificar PR aberto referenciando slug do plano — documentado em [ADR-022](../decisions/ADR-022-politica-archival-docs-plans.md) § Decisão; procedure carrega o algoritmo executável derivado daquela decisão.

Consumidores típicos: operações em PR/MR (listar/criar/checar status), em release (criar release), em archival (verificar PR aberto referenciando slug), em **issue** (listar/criar/fechar — consumidas por role `backlog: forge` per [ADR-058](../decisions/ADR-058-role-backlog-aceitar-forge.md)).

## Algoritmo

1. **Resolver remote origin:** `git remote get-url origin`. Sem remote → output `unsupported-host` (caller decide policy — geralmente skip silente da feature de forge).
2. **Host detection:**
   - URL casando `github.com` → host = GitHub.
   - URL casando regex `^gitlab\.` (gitlab.com OR GitLab corporativo `gitlab.<domínio>`) → host = GitLab.
   - Outros hosts (Bitbucket, Codeberg, custom) → output `unsupported-host`.
3. **CLI probe pelo host detectado:**
   - GitHub + `command -v gh` retorna zero → output `gh`.
   - GitLab + `command -v glab` retorna zero + `command -v jq` retorna zero → output `glab`.
   - Host mapeado mas dependência ausente (CLI ausente, ou jq ausente no caminho GitLab) → output `no-detection`.

## Outputs

4 valores distintos consumidos pela skill chamadora; cada consumer aplica policy local:

- **`gh`** — GitHub + gh disponível. Skill chama `gh pr list ...`, `gh release create ...`, etc.
- **`glab`** — GitLab + glab + jq disponíveis. Skill chama `glab mr list ... --output json | jq -r ...`, `glab release create ...`, etc.
- **`no-detection`** — host mapeado mas dependência ausente. Policy local por consumer descrita em Notas.
- **`unsupported-host`** — host não-mapeado (Bitbucket, Codeberg, custom) ou ausência de remote. Policy local por consumer descrita em Notas.

## Operações de issue (extensão neutra paralela ao PR/MR listing existente)

Adicionadas em [ADR-058](../decisions/ADR-058-role-backlog-aceitar-forge.md) — consumidas por role `backlog: forge` em 4 skills (`/next`, `/triage`, `/run-plan`, `/curate-backlog`). **Output discrimination idêntica** à seção Outputs acima (`gh` / `glab` / `no-detection` / `unsupported-host`); procedure permanece neutro; policy local em cada caller.

Comandos canonical compostos pelo caller após detection:

- **`issue list`** (issues abertas sem assignee — recorte canonical para role `backlog: forge` v1 per ADR-058 § (b)):
  - `gh` → `gh issue list --state open --search "no:assignee" --json number,title,createdAt --jq '.[]'`
  - `glab` → `glab issue list --opened --not-assignee --output json | jq -r '.[] | {number: .iid, title, createdAt: .created_at}'`
- **`issue close`** (mutação remota — sempre precedida de cutucada `AskUserQuestion` no caller per ADR-058 § (e)):
  - `gh` → `gh issue close N --reason completed --comment "<glosa>"` (close + comentário num único comando)
  - `glab` → `glab issue note N --message "<glosa>"` então `glab issue close N` (dois comandos sequenciais — `glab issue close` não aceita `--comment`; verificado em glab 1.89.0)
- **`issue create`** (mutação remota — sempre precedida de cutucada `AskUserQuestion` no caller):
  - `gh` → `gh issue create -t "<title>" -b "<body>" --json number,url`
  - `glab` → `glab issue create -t "<title>" -d "<body>"`

CLI requirements: `gh` 2.40+ ou `glab` 1.40+. `gh` filtra "sem assignee" via qualifier de busca `--search "no:assignee"` (não há flag dedicada); `glab` tem flag dedicada `--not-assignee`.

## Notas

- `gh --jq` embute jq (nenhuma dep externa adicional).
- `glab` **requer jq no PATH** para parse JSON (`glab ... --output json | jq -r ...`). Sem jq, glab ainda funciona em modo TTY mas o output não é programaticamente consumível — daí o output `no-detection` quando jq ausente.
- Discriminar `no-detection` vs `unsupported-host` preserva semânticas distintas em consumers existentes. Policy local por consumer:
  - `cleanup-pos-merge.md` — `no-detection` silent skip do candidato; `unsupported-host` fallback git-only (`git branch -r --merged origin/<main>`).
  - `/archive-plans` critério 6 — `no-detection` retorna `degraded` per [ADR-022](../decisions/ADR-022-politica-archival-docs-plans.md) § Decisão (não-elegível esta invocação); `unsupported-host` mesma classificação.
  - `/release`, `/next §4.5`, `/run-plan §3.7` — ambos caem em fallback textual com link da CLI esperada ([cli.github.com](https://cli.github.com/) ou [gitlab.com/gitlab-org/cli](https://gitlab.com/gitlab-org/cli)).
  - **4 skills consumidoras de operações de issue para role `backlog: forge`** (`/next` passo 1+3, `/triage` step 4, `/run-plan §3.4`, `/curate-backlog` H1) — `no-detection` e `unsupported-host` ambos **param com erro explícito** orientando setup (`gh auth login` / `glab auth login` / `dnf install jq`) ou declarar `paths.backlog: null` / path canonical. Categoria semântica distinta dos consumers acima: **role-declared dependency** (skill não pode degradar sem corromper o contrato do role); policy embutida no caller, não no procedure.
- Cada consumer mantém seu próprio comando pós-detect (não consolidar em comandos abstratos — cada uso tem semântica distinta: `gh release create` vs `gh pr list` vs `gh issue close N`, etc.).
