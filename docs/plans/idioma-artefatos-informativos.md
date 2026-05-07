# Plano — Convenção: idioma de artefatos informativos segue commits

## Contexto

Materializa [ADR-007](../decisions/ADR-007-idioma-artefatos-informativos.md) (Aceito): artefatos informativos do projeto (`CHANGELOG.md`, mensagens de tag anotada, descrições de PR) seguem o idioma da convenção de commits do projeto. `.md` operativos/editoriais (SKILLs, agents, `philosophy.md`, `CLAUDE.md`, ADRs, planos, `BACKLOG.md`, `install.md`, `README.md`) ficam livres.

Para este repo: commits EN (estabelecidos desde v0.1.0) → `CHANGELOG.md` e tag annotations em EN; demais `.md` continuam em PT.

**Estado de partida:** v1.23.0 já está publicada em origin (commit `c8be34b` + tag `v1.23.0` foram pushados manualmente entre sessões). Reverter no remote exigiria force-push em main, fora da blast radius. Aceito: tag `v1.23.0` permanece com annotation `Release v1.23.0` (idioma-neutro, ok); commit `c8be34b` mantém o diff em PT no histórico git (irrelevante para leitor do CHANGELOG.md atual). Bloco 3 deste plano traduz a entry de v1.23.0 no CHANGELOG.md para EN junto com as demais.

**Linha do backlog:** plugin: convenção que CHANGELOG.md e mensagens de tag anotada seguem idioma dos commits (ADR-007); migração retroativa do CHANGELOG histórico de PT para EN

## Resumo da mudança

Três blocos: (1) `philosophy.md` ganha parágrafo que torna a convenção explícita + cross-refs em "Convenção de idioma" e "Convenção de commits"; (2) `/release` passo 3 ganha nota explicitando que o changelog draft segue idioma dos commits (cross-ref a ADR-007); (3) `CHANGELOG.md` migrado retroativamente — todas as entradas atualmente em PT (v0.2.0 até v1.23.0) traduzidas para EN. Entradas já em EN (e.g., v0.2.1 metadata refresh, v0.1.0 initial release) permanecem.

**Decisões-chave:**
- **ADR-007 já aceito** — plano apenas materializa.
- **v1.23.0 publicada permanece** — entry no CHANGELOG.md atual vira EN; tag annotation `Release v1.23.0` (literal idioma-neutro) intocada; diff PT em `c8be34b` fica como artefato histórico. Sem force-push.
- **Reviewer por bloco**: `doc` para philosophy.md e CHANGELOG.md (drift entre doutrina/registro e código); `code` para /release SKILL (operativo).
- **Sem `## Verificação manual`**: doc-only; sem comportamento perceptível em runtime para o usuário do plugin. Verificação textual basta. Validação prática real é o próximo `/release` que comporá o entry da próxima versão em EN.

**Fora de escopo:**
- Não tocar `BACKLOG.md`, ADRs, planos, `philosophy.md` outros campos, `CLAUDE.md`, SKILLs/agents/install/README — todos cobertos por "fica livre" na convenção.
- Não tocar mensagens de commit históricas (já estão em EN).
- Não fazer release nova dentro deste plano — fica para `/release` pós-merge.

## Arquivos a alterar

### Bloco 1 — `philosophy.md`: convenção de idioma para artefatos informativos {reviewer: doc}

- `docs/philosophy.md`:
  - **Após o parágrafo de "Convenção de idioma"** (atualmente termina em "...identificadores de código. ... Mensagens de commit têm convenção própria — ver 'Convenção de commits'."), inserir parágrafo novo:
    - Texto: "**Artefatos informativos do registro de mudanças** — `CHANGELOG.md`, mensagens de tag anotada (incluindo síntese), descrições de PR — seguem o idioma da **convenção de commits do projeto** (ver abaixo), não o da prosa operativa. Audiência diferente: leitor de release inspeciona junto com `git log`, prosa operativa é dev escrevendo/lendo durante desenvolvimento. Detalhes em [ADR-007](decisions/ADR-007-idioma-artefatos-informativos.md)."
  - **Em "Convenção de commits"** (parágrafo final), adicionar uma frase ao final: "O idioma extraído desta convenção rege também os artefatos informativos (CHANGELOG, tag annotations, PR descriptions) — ver acima."

### Bloco 2 — `/release` SKILL: cross-ref a ADR-007 no changelog draft {reviewer: code}

- `skills/release/SKILL.md` passo 3 ("Compor entrada de changelog"):
  - **Sub-passo 2** ("Compor rascunho agrupando commits por prefixo"), adicionar nota curta antes do mapping de prefixos (`feat:` → `### Added` etc.):
    - Texto: "Idioma das bullets segue o idioma dos commits agrupados (ADR-007). Skill não traduz — `Editar` no gate único cobre ajuste manual quando necessário."

### Bloco 3 — `CHANGELOG.md`: migração retroativa PT → EN {reviewer: doc}

- `CHANGELOG.md`:
  - Para cada entrada de versão entre v0.2.0 e v1.23.0 inclusive, traduzir o conteúdo PT para EN preservando:
    - Estrutura `## [X.Y.Z] - YYYY-MM-DD` + headers `### Added` / `### Changed` / `### Fixed` / `### Removed` / `### Notes`.
    - Cross-refs a PRs/issues (`(#NN)`), ADRs (`ADR-NNN`), planos (`docs/plans/<slug>.md`), e arquivos (`/release`, `docs/philosophy.md`, etc.) — preservar literalmente.
    - Code-spans (` `feat:` `, ` `git rev-parse` `, ` `pyproject.toml` `, etc.).
    - Listas, hierarquia, ordem dos itens.
  - Entradas já em EN ficam intactas:
    - v0.1.0 (Initial release).
    - v0.2.1 (plugin.json/marketplace.json metadata refreshed).
  - Entradas mistas (PT predominante com fragmentos EN inline tipo `Conventional Commits`/`disable-model-invocation`) seguem padrão das já-EN: termo técnico fica intato, prosa em volta vira EN.
  - Tom editorial: espelhar o estilo das entradas v0.2.1 e v0.1.0 (diretas, técnicas, sem floreios). Manter o tamanho aproximado de cada bullet — não condensar nem expandir.

## Verificação end-to-end

Sem suite; verificação textual.

- **Bloco 1**: `grep -n "Artefatos informativos" docs/philosophy.md` retorna o novo parágrafo; `grep -n "ADR-007" docs/philosophy.md` confirma cross-ref; `grep -n "rege também os artefatos informativos" docs/philosophy.md` confirma a frase em "Convenção de commits".
- **Bloco 2**: `grep -n "ADR-007" skills/release/SKILL.md` retorna o cross-ref; `grep -n "Idioma das bullets" skills/release/SKILL.md` confirma a nota.
- **Bloco 3**: spot-check ≥3 entradas (e.g., v1.23.0, v1.22.0, v1.10.0, v0.4.0) — não devem conter palavras PT comuns (`que`, `para`, `com`, `passa a`, `deixa de`, `papel`); devem conter EN (`that`, `for`, `with`, `now`, `passes`, `role`). Cross-refs (`#NN`, `ADR-NNN`, paths) preservados literalmente.
- **Cross-arquivo**: `grep -rn "ADR-007" docs/ skills/` mostra coerência entre ADR, philosophy.md e /release.
- **Headers preservados**: `grep -c "^## \[" CHANGELOG.md` retorna o mesmo número antes e depois.

## Notas operacionais

- **v1.23.0 publicada — não reverter.** Tag `v1.23.0` no remote permanece apontando a `c8be34b` com annotation `Release v1.23.0` (literal idioma-neutro). Diff de `c8be34b` mantém o entry PT como artefato histórico irrecuperável sem force-push. Bloco 3 traduz o entry no CHANGELOG.md atual; leitor que abre `git show v1.23.0` ainda vê o entry original PT como part do diff, mas o registro corrente (CHANGELOG.md HEAD) está em EN.
- **Bloco 3 é o maior do plano em volume textual** mas mecânico (tradução). Doc-reviewer foca em (a) cross-refs intactos, (b) estrutura de seções preservada, (c) tom consistente com entradas já-EN, (d) ausência de fragmentos PT remanescentes.
- **Ordem dos blocos importa parcialmente**: 1-2 (doutrina/SKILL) antes de 3 (migração) para que reviewer do bloco 3 valide alinhamento com a doutrina já editada.
