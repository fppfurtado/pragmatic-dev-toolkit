# ADR-007: Idioma de artefatos informativos segue convenção de commits

**Data:** 2026-05-07
**Status:** Aceito

## Origem

- **Investigação:** Drift entre commits (EN) e `CHANGELOG.md` (PT) descoberto durante `/triage` da demanda de síntese de tag em `/release` (sessão de 2026-05-07). v1.23.0 commitada localmente seguiria o mesmo padrão; tag synthesis herdaria o drift e tornaria o problema visível em mais artefatos. Gap subjacente: nem `philosophy.md` → "Convenção de idioma" (escopo: prosa de skills/agents/templates/reports) nem "Convenção de commits" (escopo: mensagens de micro-commit) cobrem **artefatos informativos do registro de mudanças**.

## Contexto

`docs/philosophy.md` hoje tem dois eixos de convenção de idioma:

- **"Convenção de idioma"** — prosa dirigida ao operador (skills, agents, headers de templates, relatórios) espelha o idioma do projeto consumidor (default canonical PT-BR).
- **"Convenção de commits"** — mensagens de micro-commit seguem a política do projeto (Conventional Commits + idioma extraído de `git log` ≥70%; default canonical EN).

Falta convenção explícita para uma terceira categoria: **artefatos informativos** que registram mudanças do projeto e são consumidos junto com `git log` — `CHANGELOG.md`, mensagens de tag anotada (incluindo qualquer síntese), descrições de PR. Sem regra explícita, projeto consumidor pode ficar com:

- Commits CC EN + `CHANGELOG.md` PT + tags trivial-EN (caso real deste repo: ~40 entradas históricas em PT vs commits EN consistentes).
- Tag synthesis composta a partir do CHANGELOG ficaria em PT enquanto a tag em si (mensagem fixa `Release vX.Y.Z`) e os commits seguem EN — drift triplo no mesmo registro.

A regra atual de "espelhar projeto consumidor" da Convenção de idioma resolve para os artefatos operativos (cuja audiência é o dev escrevendo/lendo durante desenvolvimento), mas não para artefatos informativos (cuja audiência é o leitor de release inspecionando o histórico). As duas audiências não precisam compartilhar idioma.

## Decisão

**Artefatos informativos do projeto seguem o idioma da convenção de commits do projeto.**

Cobertura explícita:

- **`CHANGELOG.md`** (entradas e nova prepend a cada release).
- **Mensagem de tag anotada** (a frase fixa `Release vX.Y.Z` continua válida; qualquer síntese de mudanças incluída na annotation acompanha o idioma dos commits).
- **Descrição de PR** quando composta pelo toolkit (ex.: `gh pr create --fill` deriva da mensagem de commit, então herda naturalmente; ferramentas que compõem PR body próprio devem alinhar).

**Fora do escopo:**

- Arquivos `.md` operativos/editoriais — SKILLs, agents, `philosophy.md`, `CLAUDE.md`, ADRs, planos em `docs/plans/`, `BACKLOG.md`, `install.md`, `README.md`. Esses ficam livres — escolha do dev/projeto, audiência diferente, sem benefício de alinhar com idioma de commit.

**Para este repo:** commits EN → `CHANGELOG.md` e tag synthesis em EN; demais `.md` ficam em PT (status quo do repo).

Razões:

- **Coerência narrativa.** Leitor consumindo registro de mudanças (`git log`, `CHANGELOG.md`, `git show <tag>`, PR description) está numa única travessia textual. Mudar idioma entre os artefatos divide a leitura sem benefício.
- **Eliminação de tradução implícita.** Skill que compõe changelog/tag a partir dos commits não precisa traduzir. Tradução automática introduz erro silencioso; tradução manual obriga o operador a redigir o mesmo conteúdo duas vezes.
- **Audiência única do registro de mudanças.** `CHANGELOG`, tag annotation e commits são consumidos pela mesma pessoa (dev examinando release, operador rodando archeology). Operativo (.md de skill/agent/philosophy/ADR/plan) tem audiência diferente (dev escrevendo/lendo durante desenvolvimento) e pode legitimamente ficar no idioma natural do dev.

## Consequências

### Benefícios

- **`/release` pode compor changelog e tag a partir dos commits sem traduzir nem reescrever.** Subjects entram diretamente como bullets/síntese.
- **Tag synthesis (plano `release-tag-synthesis`, futuro) ganha caminho claro:** ler subjects de commits classificados → compor síntese → idioma vem grátis.
- **CHANGELOG passa a ser leitura coerente com `git log`.**
- **Convenção codificada explicitamente** — skill author futuro não reinventa o critério.

### Trade-offs

- **Migração retroativa do CHANGELOG histórico** (entradas PT → EN) é trabalho one-time substancial. Aceito porque o repo tem commits EN consistentes desde o início; o drift se acumulou apenas no CHANGELOG, e migrar faz o registro voltar a ser coerente com a história git.
- **Mistura de idiomas no repo continua.** Prosa operativa em PT, registro de mudanças em EN. Operador precisa internalizar que o critério é audiência, não idioma global do projeto. Mitigação: convenção explícita em `philosophy.md` com a partição clara.
- **Dev brasileiro escrevendo CHANGELOG entry em EN gasta esforço de tradução cognitiva.** Aceito porque `/release` agora pode compor a maior parte automaticamente a partir dos commits — esforço marginal recai apenas na frase de "Notes" ocasional.

### Limitações

- ADR não cobre artefatos editoriais cross-project (issues, Discussions externos, comunicação corporativa de release). Esses ficam fora do escopo do toolkit.
- Em projetos consumidores que adotam fluxo bilíngue real (release notes internas em PT + público em EN), a convenção pode ficar apertada. Reabrir caso emerja.
- Tag annotations já publicadas em remote permanecem com seu conteúdo original — re-tag exige force-push de tag, fora da blast radius default. v1.23.0 deste repo é exemplo: foi publicada com PT no commit que adiciona o changelog entry; a entry textual no `CHANGELOG.md` atual será migrada para EN, mas o diff de `c8be34b` permanece PT no histórico git.

## Alternativas consideradas

- **(a) Manter status quo.** CHANGELOG livre, sem convenção. Descartado: drift recorrente; `/release` fica refém de tradução implícita ou de inconsistência permanente entre commits e changelog.
- **(b) Forçar idioma fixo (EN) para todos os artefatos informativos globalmente, ignorando convenção de commits do projeto consumidor.** Descartado: contradiz "Convenção de idioma" que defende espelhar projeto consumidor; projeto com commits PT teria CHANGELOG forçado em EN sem motivo.
- **(c) Forçar idioma fixo (EN) para CHANGELOG/tag mas deixar commits livres.** Descartado: cria o mesmo drift inverso (commits PT, CHANGELOG EN); resolve o sintoma deste repo mas não a regra geral.
- **(d) Estender "Convenção de idioma" para cobrir CHANGELOG/tag também sob "espelha projeto consumidor".** Descartado: o critério da Convenção de idioma é "audiência operativa do toolkit no projeto", artefatos informativos têm audiência distinta. Misturar os dois eixos torna a regra menos previsível em projetos com commits-em-um-idioma-prosa-em-outro.

## Gatilhos de revisão

- Projeto consumidor com fluxo bilíngue real (releases internos em PT, externos em EN) precisar suporte → reabrir para considerar dual-lang artifacts ou idioma override por artefato.
- Surgir novo artefato informativo no toolkit (release notes em formato distinto, summary boards, etc.) que não caiba na regra → re-avaliar definição de "informativo".
- Commits do projeto consumidor mudarem de idioma (raro, mas possível em refactor de processo) — Convenção de commits já cobre detecção; CHANGELOG/tag acompanham automaticamente a partir desse ponto, mas migração retroativa do CHANGELOG fica como decisão separada.
- Surgir artefato cuja função primária é discoverability/landing (README, manifest descriptions) → coberto por [ADR-012](ADR-012-idioma-artefatos-discoverability-landing.md); README sai da lista "fora do escopo" desta ADR via ADR-012.
