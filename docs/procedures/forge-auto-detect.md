# Forge auto-detect

Procedimento compartilhado para detectar o forge a partir do remote `origin`. Skills consumidoras leem este arquivo via Read e executam o algoritmo abaixo. Categoria `docs/procedures/` estabelecida em [ADR-024](../decisions/ADR-024-categoria-docs-procedures-procedimentos-compartilhados.md). Caso de uso de origem do consumer `/archive-plans` critério 6 — verificar PR aberto referenciando slug do plano — documentado em [ADR-022](../decisions/ADR-022-politica-archival-docs-plans.md) § Decisão; procedure carrega o algoritmo executável derivado daquela decisão.

Consumidores típicos: operações em PR/MR (listar/criar/checar status), em release (criar release), em archival (verificar PR aberto referenciando slug).

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

## Notas

- `gh --jq` embute jq (nenhuma dep externa adicional).
- `glab` **requer jq no PATH** para parse JSON (`glab ... --output json | jq -r ...`). Sem jq, glab ainda funciona em modo TTY mas o output não é programaticamente consumível — daí o output `no-detection` quando jq ausente.
- Discriminar `no-detection` vs `unsupported-host` preserva semânticas distintas em consumers existentes. Policy local por consumer:
  - `cleanup-pos-merge.md` — `no-detection` silent skip do candidato; `unsupported-host` fallback git-only (`git branch -r --merged origin/<main>`).
  - `/archive-plans` critério 6 — `no-detection` retorna `degraded` per [ADR-022](../decisions/ADR-022-politica-archival-docs-plans.md) § Decisão (não-elegível esta invocação); `unsupported-host` mesma classificação.
  - `/release`, `/next`, `/run-plan` — ambos caem em fallback textual com link da CLI esperada ([cli.github.com](https://cli.github.com/) ou [gitlab.com/gitlab-org/cli](https://gitlab.com/gitlab-org/cli)).
- Cada consumer mantém seu próprio comando pós-detect (não consolidar em comandos abstratos — cada uso tem semântica distinta: `gh release create` vs `gh pr list` vs `gh pr list --search <slug>`, etc.).
