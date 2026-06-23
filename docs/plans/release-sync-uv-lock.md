# Plano — `/release` sincroniza `uv.lock` após bump (stack-gated, uv-only)

## Contexto

`/release` passo 2 atualiza os `version_files` declarados (`.json`/`.toml`) mas **não** toca o lockfile. Em projetos Python que usam **uv**, o `uv.lock` carrega uma entrada do pacote editável self-referenciado (`[[package]]` com `source = { editable = "." }`) cujo `version` espelha o `pyproject.toml`. Após o bump, esse `version` fica defasado; o próximo `uv run`/`uv sync` re-sincroniza o lock, modificando a working tree e forçando um commit extra `chore: sync uv.lock`.

Dor empírica concreta: 2 releases consecutivos do consumer **tjpa-tools** exigiram sync manual (v0.11.0 → `c7f10b3`/`d69343a`; v0.12.0 → `b91d8ab`; issue de origem `fppfurtado/tjpa-tools#16`).

**Decisão (fix (a) da issue, não o paliativo (b)):** passo pós-bump **stack-gated** no `/release` — se o projeto usa uv (`uv.lock` presente na raiz), re-lock antes do commit do bump e incluir `uv.lock` no mesmo commit `chore(release): bump version to X.Y.Z`. Escopo inicial **uv-only** — npm/cargo não duplicam a versão do próprio pacote no lock, não precisam. Aplicação do pattern stack-aware já existente em skill (precedente: `/run-plan §1.3` faz `uv sync`/`npm ci`/`cargo fetch` por marker de stack) — **não exige ADR novo** (sem inversão, sem categoria nova).

**ADRs candidatos:** ADR-050 (componentes plugin — § hook auto-gating triplo é o doutrina-mãe do stack-gating; aqui o gate vive em skill, não hook, mas a mecânica de degradação silenciosa é análoga)
**Linha do backlog:** #149: feat(release): sincronizar lockfile (uv.lock) após bump de version_files em projetos uv

## Resumo da mudança

- Adicionar passo **stack-gated** ao `/release` que, quando `uv.lock` existe na raiz do repo **e** o toolchain `uv` está disponível, re-locka o `uv.lock` (preferir `uv lock --offline` — só re-resolve do cache, suficiente quando a única mudança é o self-version bump) **após** escrever os `version_files` e **antes** do `git commit` do bump, incluindo `uv.lock` no `git add` da sequência de aplicação.
- **Gate triplo análogo ao de hooks** (degradação silenciosa, nunca falha a release): (1) `uv.lock` ausente na raiz → skip silente; (2) presente mas `uv` não instalado/no PATH → skip silente + nota informativa ao operador (release segue sem o sync; operador re-locka manualmente se quiser); (3) `uv lock --offline` falha (cache miss raro) → reportar stderr literal, seguir a release sem incluir `uv.lock` (não abortar — o sync é conveniência, não invariante de release).
- Refletir o `uv.lock` no bloco consolidado do passo 4 (seção **Arquivos de versão**) quando o gate ativa, para o operador ver que entra no commit.

Fora do escopo: outros lockfiles (npm `package-lock.json`/`pnpm-lock.yaml`/cargo `Cargo.lock` não self-versionam o próprio pacote); generalizar o schema de `version_files` para lockfiles; tornar o comando de re-lock configurável.

## Arquivos a alterar

### Bloco 1 — `skills/release/SKILL.md` (passo 2 detecção + passo 4 aplicação + § O que NÃO fazer) {reviewer: prompt}

- `skills/release/SKILL.md`:
  - **Passo 2 (`### 2. Atualizar version_files`, após a computação em memória):** adicionar parágrafo de **detecção stack-gated** — probe `uv.lock` na raiz do repo (`git rev-parse --show-toplevel`); presente → planejar re-lock no passo 4 e marcar `uv.lock` para inclusão no commit. Ausente → skip silente. Texto deixa explícito que a escrita/execução só acontece no gate do passo 4 (consistente com a regra "Escrita acontece no gate do passo 4").
  - **Passo 4 item 4 (bloco consolidado, seção `Arquivos de versão`):** quando o gate uv ativa, listar `uv.lock` entre os arquivos que entram no commit (com nota "re-lock via `uv lock --offline`").
  - **Passo 4 item 5 `Aplicar` (sequência (a)–(e)):** inserir sub-passo **após (a) escrever version_files e (b) inserir changelog, imediatamente antes de (c) `git add`** — o `uv lock` precisa do `pyproject.toml` já escrito (depende de (a)); (b) não toca `pyproject.toml`, então a ordem relativa a (b) é funcionalmente inócua mas fixada nesta posição para evitar ambiguidade na execução. Se o gate uv ativou: rodar `uv lock --offline` (gate de toolchain: `uv` ausente → skip + nota; comando falha → reportar stderr, seguir sem o sync); incluir `uv.lock` na lista de paths-específicos do `git add` do item (c). Preservar a regra **não** `git add -A`.
  - **§ O que NÃO fazer:** adicionar bullet — "Não abortar a release quando o re-lock de `uv.lock` falhar ou `uv` não estiver disponível — o sync é conveniência stack-gated (degrada silenciosamente), não invariante de release; abortar regrediria releases em ambientes sem uv."

## Verificação end-to-end

Inspeção textual (repo sem suite — `test_command: null`; repo markdown sem `uv.lock` próprio):

1. `grep -n "uv.lock" skills/release/SKILL.md` → ≥3 matches (passo 2 detecção + passo 4 item 4 bloco consolidado + passo 4 item 5 sequência de aplicação).
2. `grep -n "uv lock --offline" skills/release/SKILL.md` → ≥1 match no passo 4 item 5.
3. `grep -n "git add -A" skills/release/SKILL.md` → a regra "não `git add -A`" permanece intacta (o sub-passo uv adiciona `uv.lock` à lista de paths-específicos, não troca por `-A`).
4. `grep -c "uv.lock\|uv lock\|stack-gated" skills/release/SKILL.md` → § O que NÃO fazer ganhou o bullet de não-abortar (degradação silenciosa).

## Verificação manual

Comportamental — o repo do toolkit não tem `uv.lock`, então o caminho-feliz só é exercitável num consumer uv real:

- **C1 — projeto uv (consumer real, ex. tjpa-tools), gate ativo:** na próxima release dogfood de um consumer com `uv.lock` na raiz e `uv` instalado, rodar `/release`. Observar: (i) bloco consolidado do passo 4 lista `uv.lock` entre os arquivos de versão; (ii) `uv lock --offline` roda após escrever `pyproject.toml`; (iii) `uv.lock` entra no **mesmo** commit `chore(release): bump version to X.Y.Z`; (iv) `git status` limpo pós-release (sem `chore: sync uv.lock` extra forçado pelo próximo `uv run`).
- **C2 — projeto não-uv (este repo markdown), gate inativo:** rodar `/release` no toolkit (sem `uv.lock`). Observar skip silente do sub-passo uv — comportamento atual preservado, nenhuma menção a `uv.lock` no bloco consolidado, nenhuma regressão.
- **C3 — projeto uv sem `uv` no PATH (gate de toolchain):** simular ambiente sem `uv` instalado (ou `PATH` sem uv). Observar skip + nota informativa "uv.lock presente mas `uv` indisponível — re-lock pulado; re-locke manualmente se desejar"; a release **completa** normalmente (não aborta).

## Pendências de validação

- [capture:validacao] Smoke comportamental C1/C3 em consumer uv real (tjpa-tools ou outro) na próxima release dogfood pós-`/reload-plugins` — caminho-feliz (gate ativo, `uv.lock` no commit do bump, sem commit extra) e gate de toolchain (uv ausente → skip+nota, release completa). Não exercitável neste repo markdown (sem `uv.lock` próprio). C2 (gate inativo) é exercitável aqui na própria validação do `/run-plan`.
- [capture:validacao] Ramo (3) do gate triplo (`uv lock --offline` falha por cache-miss com `uv` presente) fica **não-exercitado** — exigiria cache vazio + offline, condição rara. Validação oportunística aceita: se um cache-miss real ocorrer num release dogfood, confirmar que a release completa reportando stderr sem incluir `uv.lock` (não aborta).

## Decisões absorvidas

- Bloco 1 § passo 4 item 5: posição do re-lock na sequência precisada para "após (a)/(b), imediatamente antes de (c) `git add`" — (b) changelog é inócuo a `pyproject.toml`, ordem fixada para evitar ambiguidade na execução (caminho-único).
- § Pendências de validação: ramo (3) do gate (cache-miss com `uv` presente) registrado como não-exercitado / validação oportunística — gap consciente, cenário raro de simular (caminho-único).
