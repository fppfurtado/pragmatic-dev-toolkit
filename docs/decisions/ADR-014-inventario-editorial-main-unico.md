# ADR-014: Inventário editorial permanece em `main` único; refatoração descartada por YAGNI

**Data:** 2026-05-10
**Status:** Aceito

## Origem

- **Investigação:** Sessão `/triage` 2026-05-10 do item `marketplace prep #8` do BACKLOG (Lote 4 da sequência marketplace prep). Item triado como ADR-worthy ("toca doutrina 'estado em git/forge', ADR-004"). Análise revelou que o "problema" original (clone inflado do consumer + ruído editorial no GitHub UI) tem fração reduzida resolvida por refatoração estrutural e custo desproporcional ao benefício; decisão consciente de **não refatorar** merece formalização para evitar reabertura cíclica.

## Contexto

Repo do plugin (`pragmatic-dev-toolkit`) em `main` contém hoje, além do essential publicado:

- `BACKLOG.md` — registro editorial (Próximos curatorial + Concluídos editorial).
- `docs/plans/` — ~55 planos históricos de mudanças passadas (artefato de `/triage` + `/run-plan`).
- `docs/audits/` — prompts reutilizáveis de auditoria + diretório `runs/` para registros (vazio hoje).

Esse inventário editorial vai no clone do consumer (instalação via `/plugin marketplace add`), aparece no GitHub UI quando visitante abre o repo, e cresce a cada feature.

**Caminhos avaliados no `/triage` (todos descartados, exceto status quo):**

- (b) **Repo dev separado** (`pragmatic-dev-toolkit-dev` privado + `pragmatic-dev-toolkit` público): complexidade de 2 repos com sync via cherry-pick ou pipeline; `/release` e CI precisam saber dos dois.
- (c) **Branch `dev` no mesmo repo** (`main` = published essential; `dev` = inventário): exigia refatorar 3 skills do toolkit (`/triage` step 4 push pós-commit em `main`, `/run-plan` precondição "main não à frente", `/release` step 32 HEAD-check em `main`), introduzir invariante "branch principal de trabalho" (papel novo no path contract OU hardcode neste repo), first migration ordem-dependente (criar `dev` ANTES de `git rm` em `main`), mecanismo de promoção `dev` → `main` definido (cherry-pick contínuo vs batch no release). Custo alto.
- (d) **Modo local-gitignored** ([ADR-005](ADR-005-modo-local-gitignored-roles.md)): declarar `paths.backlog: local`, `paths.plans_dir: local` no CLAUDE.md, artefatos vão para `.claude/local/` gitignored. Mecânica existente. Mas perde sync entre máquinas (inventário só vive em 1 máquina) e perde transparência editorial mesmo para o próprio operador em outra máquina.
- (e) **`internal/` + `.gitattributes export-ignore`**: cobre apenas `git archive` (tarball), não `git clone`. Marketplace usa clone. Alternativa irrelevante para o problema declarado.
- (f) **Branch orphan `published` via `/release`**: `main` continua como hoje; release cria orphan branch `published` com snapshot do essential; `marketplace.json source.ref: published`. Custo médio. Pré-requisito: marketplace honrar `source.ref: <branch arbitrária>` (não verificado empiricamente). Resolve clone pack size (orphan sem ancestors). Não resolve GitHub UI default ao abrir o repo (visitor cai em `main` por default; mudar default branch para `published` torna o repo estranho para quem visita).

**Achado-chave do `design-reviewer` (que mudou a análise):** `git clone` traz **histórico completo** do branch sempre — qualquer das opções (c) (d) (e) (f) limpa apenas working tree e GitHub UI surface, **não** o pack do `.git`. Limpar history mesmo exigiria `git filter-repo` retroativo (force-push, quebra forks/clones existentes, destrutivo). Para o "problema" declarado (clone size + ruído publicado), o ganho de (c) ou (f) versus status quo é menor que parecia.

**Cálculo de custo/benefício:** o repo hoje pesa ~1.2 MB (working tree ~700 KB + `.git` pack ~500 KB). Inventário editorial é ~600 KB do working tree (50% do clone). Mesmo (c) ou (f) só removeriam working tree do consumer — pack continua trazendo blobs históricos. Para 1.2 MB de overhead em clone único de plugin, o trabalho de refatoração toolkit-wide (c) ou de pipeline orphan (f) **não compensa** sem sinal real de atrito.

## Decisão

**Manter `main` único; inventário editorial (`BACKLOG.md`, `docs/plans/`, `docs/audits/`) permanece tracked e público no clone do consumer.** Refatoração estrutural para esconder esses artefatos é descartada por YAGNI; codificada aqui para evitar reabertura cíclica.

Razões:

- **Custo desproporcional ao benefício.** Caminhos (c) e (f) exigiriam refatorar 3 skills do toolkit ou introduzir pipeline orphan, contra ~600 KB de working tree extra no clone do consumer. Atrito real do tamanho não foi reportado por nenhum consumer; refatorar agora é abstração prematura per `docs/philosophy.md`.
- **Clone history vem completo de qualquer jeito.** A única forma de reduzir pack size é `git filter-repo` retroativo (destrutivo, force-push, quebra forks). Soluções não-destrutivas (c)/(d)/(e)/(f) só cosmetizam working tree e GitHub UI surface — ganho marginal.
- **Toolkit fica simples.** `main` único permite `/triage`, `/run-plan`, `/release` operarem sem invariante "branch principal de trabalho" extra; consumer também tem mecânica simples (`source.ref: main` é default, sem configuração especial).

## Consequências

### Benefícios

- Toolkit permanece com mecânica simples — `main` único é a invariante implícita assumida hoje.
- Transparência editorial preservada: visitante do repo vê o histórico de decisões e planos, demonstração viva do workflow que o plugin codifica.
- Zero refatoração de skills, zero pipeline novo, zero invariante nova no path contract.
- Decisão de NÃO refatorar fica registrada — reaberturas futuras precisam invocar gatilhos concretos, não opinião.

### Trade-offs

- Consumer clone arrasta inventário editorial (~600 KB de working tree). Aceito enquanto for ~1 MB; reabrir se cair em ordem de grandeza superior (≥ 10 MB de overhead editorial).
- GitHub UI ao abrir o repo mostra `BACKLOG.md`, `docs/plans/` (55+ arquivos), `docs/audits/`. Visitante anglófono casual pode ler como "repo bagunçado". Mitigado por (i) README EN limpo no topo (ADR-012); (ii) navegação convencional (consumer típico procura `/skills`, `/agents`, `/hooks`, README); (iii) inventário editorial é **demonstração** do workflow, não desordem.
- Ferramenta de pesquisa do GitHub indexa planos/audits/BACKLOG; busca por keywords do plugin retorna ruído. Aceito — busca pode ser restrita a `path:skills/` etc. pelo usuário interessado.

### Limitações

- Esta decisão **só vincula este repo** (plugin meta-toolkit publicado via marketplace). Projetos consumidores não enfrentam o mesmo problema (eles não são publicados como plugin); cada um decide seu próprio padrão.
- Reversão tardia (refatorar depois) tem custo médio: primeiros experimentos com (c) ou (f) ficam viáveis enquanto inventário não cresceu muito mais; ≥100 planos torna migração mais delicada.
- Não cobre clone **pack size** mesmo no caso de mudança futura de estratégia — só `git filter-repo` resolve essa fatia.

## Alternativas consideradas

- **(b) Repo dev separado** (`pragmatic-dev-toolkit-dev` privado + `pragmatic-dev-toolkit` público). Descartado: complexidade alta de 2 repos com sync; `/release` e CI precisariam orquestrar publicação cross-repo; primeira reorganização não-trivial.
- **(c) Branch `dev` no mesmo repo** (`main` = essential; `dev` = inventário; promoção `dev` → `main` no release). Descartado: refatoração toolkit-wide (3 skills) + invariante "branch principal de trabalho" nova + first migration ordem-dependente + mecanismo de promoção dev→main a definir (cherry-pick contínuo vs batch). Alto custo para ganho cosmético sobre status quo.
- **(d) Modo local-gitignored** ([ADR-005](ADR-005-modo-local-gitignored-roles.md) aplicado a `paths.backlog`, `paths.plans_dir`). Descartado: artefatos perderiam sync entre máquinas e mesmo a transparência editorial para o próprio operador em outra máquina. Mecânica existente, mas trade-off ruim para este repo.
- **(e) `internal/` + `.gitattributes export-ignore`**. Descartado: cobre só `git archive` (tarball), não `git clone`. Marketplace usa clone. Irrelevante para o problema declarado.
- **(f) Branch orphan `published` via `/release` + `source.ref: published` no marketplace.json**. Descartado: pré-requisito não-verificado (marketplace honra `source.ref` não-`main`?); script de release ganharia complexidade nova; ainda não resolveria GitHub UI default (visitor cai em `main` por default; mudar default branch para `published` torna repo estranho). Custo médio para ganho parcial.

## Gatilhos de revisão

- **Atrito real reportado por consumer** — issue ou comentário público sinalizando "clone grande demais", "ruído no repo", "não consigo encontrar `skills/`". Reabrir para considerar (c), (f), ou `filter-repo` conforme natureza do atrito.
- **Inventário editorial ≥ 10 MB de overhead** — clone do consumer cresce uma ordem de grandeza além do atual. Hoje ~1.2 MB; reabrir em ~10 MB. Critério mecânico, não opinativo.
- **Métricas de discoverability mostrarem queda atribuível a ruído editorial** — instalações caírem após PRs grandes em `docs/plans/` que aparecem no GitHub UI; correlação clara. Reabrir para considerar (c) ou (f).
- **`docs/plans/` ultrapassar 100 arquivos sem rotação** — gestão editorial fica difícil; reabrir para considerar arquivamento (mover para tag/release archive) ou refatoração estrutural. Critério: contagem mecânica.
- **Necessidade de schema/checks que dependem de `dev` branch separado** — surgir cenário onde toolkit precisa de branch principal de trabalho explícita. Sem cenário concreto hoje; reabrir só com gatilho específico.
