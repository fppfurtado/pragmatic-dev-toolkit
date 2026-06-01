# Plano — <Título curto>

<!--
Esqueleto canônico de plano consumido por /triage e /run-plan (ADR-055, originalmente ADR-001).
/triage lê este arquivo, copia para `<plans_dir>/<slug>.md`, adapta headers ao idioma do projeto consumidor, preenche placeholders.
/run-plan faz matching semântico contra os headers — equivalentes em outro idioma (`## Files to change`, etc.) são aceitos contanto que a estrutura informacional bata.
Seções opcionais (## Verificação manual, ## Notas operacionais, ## Decisões absorvidas) só aparecem quando há substância — não criar vazias.
-->

## Contexto

<Descrever o contexto: o que motivou a mudança, qual problema resolve, restrições relevantes.>

<!--
Campos especiais (incluir só quando aplicáveis):

**Termos ubíquos tocados:** <Termo> (<categoria>) — bounded context|agregado|entidade|RN|conceito ubíquo; omitir em refactor/doc-only.
**ADRs candidatos:** ADR-NNN (motivo) — opcional; reviewer prioriza esses, scan cobre os demais (ADR-048).
**Linha do backlog:** <texto exato> — incluir quando há linha no BACKLOG; mensageiro pra /run-plan operar transições.
**Branch:** <nome-da-branch> — incluir quando a branch já existe (issue-first GitLab, retrabalho de PR, etc.); ausência = /run-plan cria <slug> a partir do HEAD (ADR-049 § Decisão (b)).
**Modo:** runbook — incluir em planos de system-surgery (operações fora de diff git: `mv`, `systemctl`, edits em `~/`, ops em múltiplos repos coordenados, etc.); **tipicamente hand-written, não derivado de /triage**; bypassa worktree + micro-commit + reviewer per bloco + validação centralizada do /run-plan (ADR-049 § Decisão (d)). Ausência = fluxo default. Único valor aceito: `runbook`.
-->

## Resumo da mudança

<Síntese da mudança: o que entra, o que fica de fora, decisões-chave (incluindo escolha entre caminhos quando houve bifurcação).>

## Arquivos a alterar

<!--
Um bloco H3 por arquivo ou agrupamento lógico.
Anotação `{reviewer: <perfil>}` no fim do header orienta /run-plan:
  - Sem anotação → default code-reviewer (ou doc-reviewer se paths todos .md/.rst/.txt).
  - Um perfil: {reviewer: code|qa|security|doc} (caso normal).
  - Combinações ({reviewer: code,doc}, etc.) → exceção rara; preferir separar em blocos quando viável.
BACKLOG.md NUNCA aparece aqui — transições são geridas pelo campo `**Linha do backlog:**` acima e pelo mecanismo do /run-plan.
-->

### Bloco 1 — <descrição curta> {reviewer: code}

- `<path>`: <o que muda neste arquivo>
- ...

## Verificação end-to-end

<Critérios objetivos para considerar a mudança válida. Cite comandos concretos quando aplicáveis (grep, ls, exec do test_command). Para projetos sem suite, transformar em inspeção textual passo-a-passo.>

<!--
Diretrizes canonical para critérios end-to-end (per Onda K' editorial — 5 evidências empíricas absorvidas: Onda Promoção crit 6 + Onda J crit 6.4 + Onda K crit 1 pré-absorção + Onda K crit 6 pré-absorção + Onda K crit 1 pós-absorção). Aplicação forward apenas — planos mergeados anteriormente com counts literais não são tocados retroativamente.

1. **Greps de Status field**: prefixar com `^\*\*Status:\*\*` para discriminar Status canonical vs narrativa histórica em § Origem histórica (lição Onda Promoção crit 6 — `grep "Substituído"` sem prefixo casa referências históricas).

2. **Verificações de inalterabilidade de inventário**: preferir `git status --porcelain -- <paths>` git-based vs `wc -l` count lexical hardcoded — counts mudam entre ondas e estado pré-loop pode alterar assumption; git status detecta mutação independente de saldo (lição Onda K crit 6 — `git status clean` substituiu count == 27 esperado).

3. **Formulações de termos canonical**: citar termos exatamente como aparecem no texto-alvo (preservar espaços, hífens, capitalização). Verificar via Read do texto antes de hardcodar grep (lição Onda J crit 6.4 — texto real do ADR-054 usa "*contrato declarado*" sem hífen vs grep com hífen decorativo).

4. **Counts esperados**: citar valor como variável (`<saldo>`) ou amarrar condição inversa (`git status --porcelain -- <paths>` retorna 0 linhas; ausência de matches em grep) em vez de número literal hardcoded — saldos mudam entre ondas e estado pré-loop pode alterar assumption (lição Onda K crit 1 pré-absorção esperava raw 33 + filtrado 27; estado pós-cleanup órfãos FS pré-loop produziu raw 27 + filtrado 26).
-->

<!-- Seções abaixo são opcionais — incluir só se houver substância. -->

## Verificação manual

<Passos para o operador exercitar comportamento perceptível. Obrigatório quando a mudança toca fluxo crítico, integração frágil, ou superfície não-determinística (parsing, matching contra dado real, comportamento de agente LLM). Cenários enumerados, não direção genérica.>

## Notas operacionais

<Particularidades de execução: ordem dos blocos quando importa, pontos de atenção para reviewers, follow-ups previstos para batches subsequentes.>

## Decisões absorvidas

<!--
Mirror do bloco `## design-reviewer findings absorvidos` do commit message deste plano (per ADR-053 § Decisão (c) + (d)).
Bullet format idêntico:
- <localização breve>: <correção aplicada> (caminho-único).

Preenchido por /triage step 5 quando findings são absorvidos pré-commit; consumido por /run-plan §2.3 que passa a seção como contexto aos reviewers por bloco. code-reviewer (per agent def) trata estruturas listadas como out-of-scope da rubrica YAGNI.
Seção omitida quando não há findings absorvidos (zero overhead no caso comum).
-->

- <localização>: <correção> (caminho-único).
