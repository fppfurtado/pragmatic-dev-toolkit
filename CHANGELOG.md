# Changelog

All notable changes to this plugin are documented here. Format inspired by [Keep a Changelog](https://keepachangelog.com/).

## [1.10.0] - 2026-05-04

### Added
- `docs/philosophy.md`: nova seção **"Convenção de pergunta ao operador"** define os dois modos complementares de coleta de input — `AskUserQuestion` (escolhas discretas) e prosa livre (explicação/justificativa) — com critério mecânico para optar.
- Skills migradas para `AskUserQuestion` nos pontos enum-naturais: resolução de papéis tri-state e oferta de memorização (philosophy + todas as skills); bifurcação arquitetural (`/new-feature` passo 2); `/new-feature` passos 5 (revisão de backlog), 6 (commit) e proposta de criação de `domain.md`/`design.md`; `/new-adr` passo 2 (formato atípico/misto); `/run-plan` pré-cond 2 (alinhamento sujo), passo 1.2 (`.worktreeinclude` multiSelect + gatilho cruzado de credencial), passo 2 (sanity escopo), passo 4.3 (sanity doc), passo 4.4 (backlog harvest).
- `CLAUDE.md`: ponteiro à nova convenção para preservar o modo de cada touchpoint ao editar skills.



### Added
- `/new-feature`: novo **passo 5 "Revisão do backlog"** entre o passo 4 (produção dos artefatos) e o passo de commit (renumerado para passo 6). Gate condicional — dispara apenas quando o passo 4 modificou o arquivo do papel `backlog` (linha da feature em curso, linhas de fora-de-escopo capturadas no passo 2, ou ambas); caminho que não tocou backlog (atualização pura de `domain.md`/`design.md`, ADR delegada sem linha de backlog acompanhante, papel `backlog` resolvido para "não temos") pula silenciosamente. Quando dispara: relê o arquivo do backlog após as edições do passo 4, flaga duplicatas entre linhas recém-adicionadas (incluindo itens fora-de-escopo do passo 2) e linhas pré-existentes nas três seções, flaga obsolescência conservadora (sobreposição nítida no texto, não similaridade vaga), mostra ao operador o estado atual de `## Próximos` (com `## Em andamento`/`## Concluídos` apenas se um flag tocar essas seções) e pergunta uma vez se algo precisa ser consolidado, reordenado ou removido antes do commit. Versão mínima da pergunta no caso frequente (sem flags + uma linha adicionada): "Backlog atualizado com `<linha>`. Ok?". Edits aprovados pelo operador entram no mesmo commit unificado proposto no passo 6. Duas novas entradas em `## O que NÃO fazer` codificam: não pular o gate quando o passo 4 modificou o backlog, e não consolidar/remover/reordenar linhas sem confirmação explícita do operador.

### Notes
- Mudança aditiva. Fecha a simetria do eixo **gates de qualidade no fim do fluxo**: `/run-plan` 4.4 (Backlog harvest, 1.7.0) captura **novos** itens emergidos durante execução; `/new-feature` 5 valida itens **recém-registrados** durante alinhamento. Sequência completa do eixo: 1.4 (commit dos artefatos), 1.5 (gate git no `/run-plan`), 1.6 (sanity check de documentação), 1.7 (backlog harvest + fora-de-escopo capture), 1.8 (cenários enumerados em validação manual), 1.9 (revisão do backlog em `/new-feature`). A heurística age **a partir** da próxima invocação da skill.

## [1.8.0] - 2026-05-03

### Added
- `/run-plan` passo 1.2: novo **gatilho cruzado de validação manual**, independente do estado prévio do `.worktreeinclude`. Quando o plano corrente tem `## Verificação manual` (matching semântico) E a raiz do repo tem gitignored típicos de credencial/config local (`.env`, `*.local.yaml`, `*.local.yml`, `secrets.*`) **não cobertos** pelo `.worktreeinclude` aplicado, a skill cutuca o operador antes do baseline: *"Plano tem `## Verificação manual` e `<credencial>` não está replicada na worktree. Validação manual provavelmente vai precisar do serviço real. Replicar agora? (s/n)"*. Os 3 casos do mundo real (`.worktreeinclude` ausente / com mas sem a credencial / vazio porque operador disse "não preciso" antes) viram instâncias da mesma cláusula — fio condutor é "credencial necessária para validação manual não está replicada", não estado prévio. Nova entrada em `## O que NÃO fazer` codifica que a cutucada **não pode ser silenciada** por resposta "não preciso" antiga quando o contexto mudou (plano corrente exige serviço real). Fecha o gap de "worktree sobe sem credencial necessária e validação manual quebra na primeira tentativa".
- `/new-feature` passo 2: gap existente *"Validação manual necessária?"* ganha **sub-bullet condicional** (não item top-level — refinamento de heurística > expansão da lista, alinhado a YAGNI). Quando o sim do gap vem de **surface não-determinística** (parsing, matching de strings, ou comportamento de agente LLM), exigir antes do plano: (a) **forma do dado real** — pedir 1-2 exemplos concretos do formato em produção (separadores, prefixos, capitalização inconsistente, ids internos que não devem vazar); (b) **cenários enumerados** — `## Verificação manual` deve listar passos concretos que exercitem essas formas, não direção genérica tipo "validar via interface real". Sub-bullet **não dispara** quando a primeira pergunta do gap resolveu "não" (refactor puro, doc-only). Fecha o gap de "matching contra dado sintético passa, dado real não" e "prompt vaza id interno descoberto por sorte".

### Notes
- Mudança aditiva. Fecha o quarteto de releases consecutivos no eixo **gate de validação manual**: 1.5 (gate git dos artefatos de alinhamento), 1.6 (sanity check de documentação), 1.7 (backlog harvest), 1.8 (cenários enumerados + credenciais replicadas). Dois bugs reais motivaram o 1.8 (matching falhou em formato de produção; agente LLM vazou id interno) — ambos passaram pelos reviewers automáticos e só foram pegos pela validação manual após o operador improvisar cenários por sorte. Decisões deliberadas de **não** propor: agente `prompt-reviewer` novo (uma sessão não justifica papel — YAGNI), seção `## Cenários do agente` no template de plano (criaria precedente para seção por tipo de feature), mudar mandato do `qa-reviewer` (reviewer age sobre diff, não conhece "dado real"; defesa fica upstream em `/new-feature`). A heurística age **a partir** da próxima invocação das skills.

## [1.7.0] - 2026-05-03

### Added
- `/new-feature` passo 2 (esclarecimento de gaps): nova diretiva **"Itens fora de escopo emergidos na conversa"** instrui a skill a manter atenção para coisas mencionadas pelo operador que não pertencem ao escopo da feature em curso (TODO adjacente, tech-debt revelado, bug menor avistado, melhoria não-essencial). Itens capturados são propostos como linhas separadas em `## Próximos` no backlog, distintas do artefato principal. Operador pode descartar com "deixa pra lá" — captura é sugestão, não imposição. Passo 4 (produção) clarifica que o backlog ganha linhas independentes da escolha de artefato principal: feature com plano/ADR/atualização de domínio também recebe linhas de itens fora-de-escopo em `## Próximos`.
- `/run-plan`: novo **passo 4.4 "Backlog harvest"** entre o sanity check de documentação e declarar done. Pergunta direta ao operador se algo emergiu durante a execução que deveria virar item separado no backlog (TODO adjacente, tech-debt revelado pela leitura, bug menor de passagem, melhoria não-essencial). Itens listados são tratados como **bloco extra** (atualizar `backlog` → revisor `code` → micro-commit) antes do done. Resposta "nada" fecha o gate. Escopo creep já absorvido pelo plano **não** entra aqui — harvest é para deferimento deliberado. Duas novas entradas em `## O que NÃO fazer` codificam: não pular o harvest (sempre perguntar), e não capturar itens que já foram absorvidos pelo plano corrente.

### Notes
- Mudança aditiva. Complementa simétricamente os bumps anteriores: 1.4.0 (commit dos artefatos de alinhamento em `/new-feature`), 1.5.0 (gate git em `/run-plan`), 1.6.0 (sanity check de documentação). Fecha o gap de **perda silenciosa de itens adjacentes** que emergem durante o fluxo. Cerimônia adicional é uma pergunta no fim do `/run-plan` ("nada" como resposta válida) e atenção passiva durante o gap analysis do `/new-feature` — custo desprezível frente à perda evitada. A heurística age **a partir** da próxima invocação das skills.

## [1.6.0] - 2026-05-03

### Added
- `/run-plan`: novo **passo 4.3 "Sanity check de documentação"** no gate final, entre confirmação de `## Verificação manual` e declarar done. Valida consistência de docs `.md` user-facing (README, install, CHANGELOG, outras `.md`) com o que foi implementado. Heurística tri-state: (i) **skip silente** quando o plano já listou `.md` em `## Arquivos a alterar` e o diff agregado os tocou — gate cumprido pelo plano; (ii) **skip silente** em refactor puro / internal-only — sinalizado por ausência de `## Verificação manual` E ausência de menção a superfície user-facing no `## Resumo da mudança`; (iii) caso contrário, **cutucar** (não bloquear) com pergunta direta ao operador. Updates levantados pelo operador são tratados como **bloco extra** (implementar → `test_command` → revisor `code` → micro-commit) antes de declarar done. Nova entrada em `## O que NÃO fazer` veda pular o check fora das duas condições de skip prescritas.

### Notes
- Mudança aditiva. Plano que naturalmente não toca user-facing surface (refactor, doc-only, cleanup interno) segue declarando done sem pergunta extra — nada de cerimônia onde claramente não se aplica. A heurística age **a partir** da próxima invocação de `/run-plan`.

## [1.5.0] - 2026-05-03

### Added
- `/run-plan`: nova **pré-condição 2** com checagem em duas camadas via `git status --porcelain` sobre o estado git dos artefatos de alinhamento. **Bloqueia** quando o próprio plano (`<plans_dir>/<slug>.md`) está modificado ou untracked — broken-by-construction, já que a worktree saída do HEAD não veria o plano que deveria executar; mensagem direciona para o commit explícito (e referencia o passo 5 do `/new-feature`). **Cutuca** (não bloqueia) quando papéis de alinhamento (`backlog`, `ubiquitous_language`, `design_notes`, arquivos sob `decisions_dir`) têm alterações uncommitted — a worktree perde esse contexto e reviewers podem não ver invariantes/ADRs que o plano assume documentados; operador decide commitar agora ou prosseguir. Outras alterações uncommitted no working tree (código de exploração/debug) **não** geram aviso — o operador as isolou intencionalmente, é o ponto da worktree. Nova entrada em `## O que NÃO fazer` veda contornar o bloqueio copiando o plano manualmente para dentro da worktree.

### Notes
- Complemento simétrico ao bump 1.4.0: `/new-feature` propõe o commit dos artefatos no passo 5; `/run-plan` agora valida que esse commit aconteceu (ou força a decisão explícita) antes de criar a worktree. A heurística age **a partir** da próxima invocação de `/run-plan`.

## [1.4.0] - 2026-05-03

### Changed
- `/new-feature`: passo 5 renomeado para **"Reportar, propor commit e devolver controle"**. Após o report dos artefatos produzidos, a skill agora **propõe um commit único** agrupando linha de backlog, plano, atualização de `domain.md`/`design.md` etc. — mensagem segue a convenção de commits do projeto consumidor (default canonical Conventional Commits em inglês, tipo `docs:`/`chore:`). Confirmação explícita do operador é exigida antes do commit; etapa pulada quando não há alterações novas (ex.: caminho foi delegar para `/new-adr` que já fez commit próprio). Fecha o gap operacional em que `/run-plan`, ao criar worktree a partir do HEAD, não encontrava o plano que deveria executar porque os artefatos de alinhamento haviam ficado uncommitted. Nova entrada em `## O que NÃO fazer` codifica o guard ("não commitar sem confirmação").

### Notes
- Mudança aditiva no comportamento da skill. Operadores que preferem commitar manualmente ainda podem declinar a proposta; a skill apenas torna a etapa explícita em vez de silente. A heurística age **a partir** da próxima invocação de `/new-feature`.

## [1.3.0] - 2026-05-02

### Added
- `/new-feature`: passo 4 (produção de plano) agora prescreve linha **"Termos ubíquos tocados"** em `## Contexto` quando o passo 1 identificou termos do `ubiquitous_language` que o pedido toca (bounded context, agregado/entidade, RN, conceito ubíquo). O plano vira mensageiro explícito do vocabulário entre alinhamento e execução, sem onerar `/run-plan` com releitura de `docs/domain.md`. Planos para mudanças que não tocam domínio (refactor puro, doc-only, papel resolvido para "não temos") seguem sem a linha — silente.
- `agents/code-reviewer.md`: nova regra prescritiva na seção "Identificadores" — identificador novo que representa conceito declarado em `ubiquitous_language` deve usar o termo declarado, não sinônimo improvisado. Complementa a regra defensiva pré-existente ("renomeação cosmética não"); reviewer flagga apenas quando há termo declarado E identificador novo divergente, gracefully silente em projetos sem `docs/domain.md`.
- `docs/philosophy.md`: nova seção curta **"Linguagem ubíqua na implementação"** (entre "Cobertura de teste em planos" e "Convenção `.worktreeinclude`") codificando o pipeline `domain.md` → plano → review em três estágios e a decisão deliberada de não tocar `/run-plan` (plano é mensageiro, releitura duplicaria responsabilidade). Espelha o pipeline de invariantes do `qa-reviewer`.

### Notes
- Mudança aditiva. Planos pré-existentes seguem válidos; reviewer flagga apenas em divergência real. A heurística age **a partir** da próxima invocação de `/new-feature`.

## [1.2.0] - 2026-05-02

### Changed
- `/new-feature`: passo 1 (leitura do papel `ubiquitous_language`), passo 2 (gap "Aprendizado de domínio") e passo 3 (tabela de decisão "Atualizar `docs/domain.md`") agora prompta explicitamente bounded contexts e agregados/entidades, além de linguagem ubíqua e invariantes (RNxx). Alinha a skill com a frase-tese da filosofia (`docs/philosophy.md` linha 7) — bounded contexts e DDD estratégico são pilares e merecem registro em `docs/domain.md` ao mesmo título dos demais elementos.
- `docs/philosophy.md`: descrição do papel `ubiquitous_language` na tabela do path contract amplia para cobrir bounded contexts e agregados/entidades, fechando o gap entre a frase-tese e o contrato de papel.

### Notes
- Mudança aditiva. Projetos cujo `docs/domain.md` hoje contém apenas linguagem ubíqua e invariantes seguem válidos — registro de bounded contexts e agregados/entidades é orientação, não obrigatoriedade. A heurística age **a partir** da próxima invocação de `/new-feature`.

## [1.1.0] - 2026-05-02

### Added
- `/new-feature`: novo bullet "Cobertura de teste necessária?" no checklist de gaps (passo 2), com heurística tri-state codificada em `docs/philosophy.md` → "Cobertura de teste em planos". Eleva a probabilidade de planos prescreverem bloco de teste com `{reviewer: qa}` quando a feature toca invariantes (RNxx), integrações externas, persistência ou comportamento observável novo — sem TDD obrigatório, mantendo cerimônia proporcional ao risco. Refactor puro e doc-only seguem sem cerimônia adicional.
- `docs/philosophy.md`: nova seção "Cobertura de teste em planos" entre "Anotação de revisor em planos" e "Convenção `.worktreeinclude`". Codifica princípio (testes servem à confiança, não à métrica; ausência é fragilidade ampliada em fluxo assistido por IA), heurística tri-state operacionalizada por `/new-feature`, e relação com `qa-reviewer` (revisão do bloco que contém os testes) e scaffolders stack-specific (`/gen-tests-python` complementa, não substitui).
- `docs/install.md`: smoke test cobrindo a prescrição de bloco de teste em projeto com RNxx declarada.

### Notes
- Bump minor: convenção é additive — projetos consumidores não precisam mudar nada para continuar funcionando como antes; planos preexistentes seguem válidos. A heurística age **a partir** da próxima invocação de `/new-feature`.

## [1.0.0] - 2026-05-02

### Removed
- Alias deprecado `{revisor: ...}` (PT) em headers de blocos de plano. `/run-plan` agora recusa essa anotação antes de começar o bloco, indicando o bloco e a anotação ofensora. Migrar para `{reviewer: ...}` (EN).

### Fixed
- `docs/philosophy.md` (tabela path contract, linha de "convenção Claude Code"): exemplo de anotação migrado de `{revisor: qa}` / `{revisor: security}` para `{reviewer: qa}` / `{reviewer: security}` — escapou da migração de v0.11.0.

### Notes
- A coexistência prometida em v0.11.0 (`v0.11–v0.12`) foi reduzida para `v0.11.x` apenas. Cutover direto v0.11.x → v1.0 sem shipar v0.12 sentinel. Justificativa: v0.12 sem mudanças reais seria overhead sem ganho dada a baixa expectativa de uso externo do alias.
- Operadores com planos externos contendo `{revisor:}` precisam editar para `{reviewer:}` antes de invocar `/run-plan` (find/replace trivial).
- Bump major: primeira release com remoção breaking. Toda a história anterior (v0.1.0–v0.11.1) foi aditiva.

## [0.11.1] - 2026-05-01

### Changed
- `skills/new-feature/SKILL.md`: limite de gaps a esclarecer relaxado de "1–2" para "1–3" — duas perguntas podia ser pouco em pedidos com mais de uma área de gap real.

## [0.11.0] - 2026-05-01

### Changed
- `docs/philosophy.md` consolidada como single source of truth: cobre todas as skills em "Papel obrigatório vs informacional"; critérios mecânicos para "sinal claro" (idioma) e "predomínio claro" (commits) — ambos a ≥70%; contrato `{reviewer: ...}` formalizado com schema, idioma e suporte a múltiplos perfis; `.worktreeinclude` centralizado aqui; política de hooks vs idioma declarada (mecânica universal, sempre em inglês).
- `/run-plan` invoca **todos** os perfis listados em `{reviewer: ...}` (era "mais sensível vence"); aceita `{reviewer: code,qa,security}` agregando relatórios.
- `agents/qa-reviewer.md` deixa de assumir layout `tests/unit/`+`tests/integration/`; reviewer infere categoria por marker, não por path. Nova seção "Qualidade dos testes" com critério mecânico de caminho feliz.
- `agents/code-reviewer.md` ganha exemplos por categoria na rubric `.claude/settings*.json`; regra `application/`/`domain/`/`infrastructure/` aplicada apenas a código novo introduzido pelo diff (legacy não é flag); typing trivial sai do "NÃO flagrar" puro e ganha critério de exceção (motivo explicitável).
- `skills/new-adr/SKILL.md` template default `**Status:** Proposto` (era `Aceito`); reflexão dos workflows reais — ADR aprovado vira `Aceito` após revisão.
- `CLAUDE.md` deixa de duplicar "Naming convention" e "Hook auto-gating triple" — vira ponteiro para `docs/philosophy.md`.

### Added
- Anotação `{reviewer: ...}` em inglês como mecânica canônica; alias `{revisor: ...}` aceito com warning durante v0.11–v0.12, removido em v1.0.
- Chave reservada `language` no bloco YAML de config (`<!-- pragmatic-toolkit:config -->`) para forçar idioma do projeto consumidor.
- `qa-reviewer` e `security-reviewer` declaram divisão de trabalho explícita com `code-reviewer` (settings hygiene) e entre si.
- `security-reviewer` ganha fast-path para diffs doc-only e fallback heurístico quando `decisions_dir` resolve "não temos".
- `/debug` ganha critério de parada mecânico (duas hipóteses consecutivas refutadas sem ganho de evidência) e caminho dedicado para sintomas intermitentes (reprodução estatística).
- `/new-adr` e `/gen-tests-python` declaram explicitamente que **não fazem commit** — handoff ao operador.

### Fixed
- Tabela do path contract — `decisions_dir` é diretório, não pattern (pattern de filename migrou para `/new-adr`).
- Repetições removidas em `/new-feature`, `/run-plan`, `/debug`, `/gen-tests-python`.
- Keywords sincronizadas entre `plugin.json` e `marketplace.json`.
- `block_env` aceita lista expandida de template suffixes (`.j2`, `.erb`, `.mustache`, além dos antigos `.jinja`, `.tmpl`); constante `TEMPLATE_SUFFIXES` documentada.
- `run_pytest_python` extrai constante `TAIL_LINES` com racional empírico; literal `10` deixa de ser mágico.
- `hooks.json` ganha `description` por entry com racional dos timeouts (10s pre, 60s post).
- Description de manifests desacoplada de nomes de skills.
- Removido "sub-plugin" órfão do parágrafo introdutório de "Convenção de naming".

### Notes
- Bump minor: formaliza schema da anotação `{reviewer: ...}` (era convenção implícita), introduz chave reservada `language` e marca `{revisor: ...}` como alias deprecado. Backwards compat mecânico preservado durante v0.11–v0.12.
- v1.0 fica reservada para o release que **remove** o alias `{revisor: ...}`.
- Plugin é meta-tool (não aplica strict-mode suas próprias pré-condições) — `CLAUDE.md` continua em inglês como operating instructions.

## [0.10.0] - 2026-05-01

### Changed
- Agent `code-reviewer` ganha rubric específico para `.claude/settings.json` e `.claude/settings.local.json` na seção "Infra e configuração": flagga drift/duplicação entre arquivos shared e local, vazamento de entries pessoais para o compartilhado, hooks com paths não-portáveis, env vars literais em vez de `${VAR}`, e `permissions.allow` só-em-local sem racional explícito. Reaproveita o reviewer default de `/run-plan` — qualquer bloco que toque `.claude/settings*.json` é coberto sem precisar anotar `{revisor: ...}`.

### Notes
- `security-reviewer` não foi estendido: capability grants amplos em `permissions.allow` já caem em "Privilégios e permissões" (broad ACL / manifest permissions) — duplicar seria ruído.
- Sem princípio novo em `docs/philosophy.md`: higiene de settings é checklist mecânico, não tensão de design durável.

## [0.9.0] - 2026-05-01

### Added
- Skill `/debug <sintoma>` — diagnostica causa-raiz por método científico (precisar sintoma → reproduzir → isolar → testar hipóteses → causa-raiz com evidência). Produz **diagnóstico, não fix**: o operador escolhe o caminho de correção depois (revert, patch direto, ou `/new-feature` se virar mudança maior). Stack-agnóstico — orquestra método, não toolchain de debugger. Roles consumidos (todos informacionais): `test_command`, `ubiquitous_language`, `decisions_dir`, `design_notes`.

### Notes
- Skill enforca o paralelo de `/new-feature` no eixo de bug-fixing: "não corrigir sem isolar a causa". Sem essa disciplina explícita, debug em chat free-form pula etapas e regressões voltam.
- Não cria worktree, não escreve artefato no repo, não aplica instrumentação. Propor instrumentação ao operador é parte do passo "hipotetizar e testar"; aplicar fica com o operador no workspace dele.

## [0.8.0] - 2026-05-01

### Changed
- Agent `security-reviewer` generalizado para qualquer tipo de sistema (web, CLI, desktop, mobile, embedded, library, pipeline, IaC). Critérios passam a ser tratados como **princípios** que se manifestam diferente conforme stack: "Chamadas HTTP externas" vira "I/O externo" (qualquer I/O bloqueante — RPC, DB, file lock, socket, subprocess); "Tokens em URLs em vez de headers" generaliza para segredos em qualquer canal inseguro (argv visível, env herdada, query string); validação de entrada cobre fronteiras adicionais (IPC, deserialização, callback de SDK, stdin) e classes de injeção além de SQL (shell, path traversal, format string, deserialização unsafe, log injection).

### Added
- Nova seção "Privilégios e permissões" no `security-reviewer`: least-privilege em escalation, capability grants, scopes OAuth, roles IAM, manifest permissions, ACLs e entitlements.
- Frontmatter `description` do agent ganha pista explícita de aplicabilidade ("qualquer tipo de sistema") para evitar leitura como agent só-web. CLAUDE.md atualizado em paralelo.

### Notes
- Backwards compat preservado: diffs antes cobertos continuam cobertos. A superfície de detecção apenas expandiu.

## [0.7.0] - 2026-05-01

### Changed
- Skill `/run-plan` passa a seguir a **convenção de commits do projeto consumidor** ao gerar micro-commits. Detecção em três níveis: política explícita no projeto (CLAUDE.md, `CONTRIBUTING.md`, etc.) → padrão observado em `git log` → default canonical Conventional Commits em inglês. Backwards compat preservado: projetos sem política explícita e com histórico já em CC inglês mantêm comportamento idêntico ao v0.6.0.

### Added
- Princípio "Convenção de commits" em `docs/philosophy.md`: protocolo de detecção em três níveis, espelhando o pattern da Convenção de idioma.

### Notes
- Política de "um micro-commit por bloco" permanece invariante. `--amend`/rebase de commits de blocos já fechados continuam proibidos; emendar o último commit do bloco corrente passa a ser exceção localizada (typo, arquivo esquecido), não regra.

## [0.6.0] - 2026-05-01

### Changed
- Skills (`/new-feature`, `/new-adr`, `/run-plan`, `/gen-tests-python`) e agents (`code-reviewer`, `qa-reviewer`, `security-reviewer`) passam a **adaptar-se ao idioma do projeto consumidor** — prosa, headers de templates, nomes de teste e relatórios de revisão espelham o idioma já em uso. Default canonical: PT-BR (origem do toolkit). Backwards compat preservado para projetos PT-BR.
- `/run-plan` faz matching semântico dos headers de plano em vez de exigir literais PT-BR (`## Files to change` / `## Arquivos a alterar`, etc., aceitos como equivalentes).

### Added
- Princípio "Convenção de idioma" em `docs/philosophy.md`: idioma do projeto define a prosa; nomes de agents, frontmatter, paths, código e commits permanecem em inglês.

### Notes
- `CLAUDE.md` deste repo continua dizendo PT-BR — a regra do plugin é "espelhar o projeto consumidor", e o projeto consumidor neste caso (o próprio repo do plugin) opera em PT.

## [0.5.0] - 2026-05-01

### Changed
- Skill `/new-adr` consome agora o papel `decisions_dir` (default: `docs/decisions/`) em vez de path literal.
- Skill `/new-adr` passa a **inferir o formato de numeração** dos ADRs existentes no diretório resolvido: 3-dígitos padded (canonical), 4-dígitos padded ou sem padding. Diretório vazio mantém o default canonical (3-dígitos). Formatos mistos no diretório são flaggados ao operador antes da criação do novo ADR.

### Notes
- Bump minor: comportamento de numeração muda em projetos que usam variantes (4-dígitos ou sem padding) — antes a skill forçaria 3-dígitos. Backwards compat preservado para projetos com 3-dígitos.

## [0.4.1] - 2026-05-01

### Changed
- Skill `/gen-tests-python` e agents `qa-reviewer`, `security-reviewer`, `code-reviewer` passam a referenciar **papéis** (`ubiquitous_language`, `design_notes`, `decisions_dir`) ao invés de paths literais (`docs/domain.md`, `docs/design.md`, `docs/decisions/`). Default canonical citado entre parênteses para legibilidade. Backwards compat preservado.

## [0.4.0] - 2026-05-01

### Changed
- Path contract reframed como **convenção default por papel** (`docs/philosophy.md`). Skills consomem papéis (`product_direction`, `ubiquitous_language`, `design_notes`, `decisions_dir`, `plans_dir`, `backlog`, `test_command`), não paths literais. Backwards compat 100% preservado para projetos que seguem canonical paths.

### Added
- Mecanismo "Resolução de papéis" em `docs/philosophy.md`: protocolo `probe canonical → consultar bloco no CLAUDE.md → perguntar ao operador (tri-state)`, com bloco YAML fenced sob marcador HTML `<!-- pragmatic-toolkit:config -->` como mecanismo de declaração de variantes.
- Drift detection: skill flagga inconsistência ao operador quando canonical existe E CLAUDE.md declara variante diferente.
- Skills `/new-feature` e `/run-plan` portadas para o protocolo. Test gate em `/run-plan` passa a aceitar `test_command` declarado (ex.: `uv run pytest`, `npm test`, `cargo test`).
- `docs/install.md` e `README.md` documentam o bloco de config com exemplo de variantes típicas.

### Notes
- `/gen-tests-python`, agents (`qa-reviewer`, `security-reviewer`, `code-reviewer`) e `/new-adr` permanecem com referências literais ao path contract — serão portados em v0.4.1 (skills/agents) e v0.5.0 (numbering inferido em `/new-adr`).
- Hooks (`block_env`, `run_pytest_python`) inalterados — `.env*` e `pyproject.toml` são markers universais por ecossistema, não project-config.

## [0.3.1] - 2026-05-01

### Added
- Skill `/new-feature`: gap "Bifurcação arquitetural" no checklist + exceção à regra "1-2 perguntas" quando o pedido admite múltiplas implementações materialmente diferentes.
- Princípio "Nomear bifurcações arquiteturais" em `docs/philosophy.md`.

## [0.3.0] - 2026-04-30

### Added
- Agent: `qa-reviewer` — princípios de cobertura de testes (caminho feliz, invariantes, edge cases, mock vs real). Stack-agnóstico.
- Agent: `security-reviewer` — credenciais, validação de entrada, HTTP externo, dados sensíveis, invariantes em ADRs. Stack-agnóstico.
- Naming convention para agents documentada em `docs/philosophy.md` (critério: gera/executa = força sufixo; revisa princípios = não força).

## [0.2.1] - 2026-04-30

### Changed
- `plugin.json` and `marketplace.json` metadata refreshed to mention `/gen-tests-python` and the pytest hook; keywords/tags now include `python`, `pytest`, `testing` for marketplace discovery.

## [0.2.0] - 2026-04-30

### Added
- Skill: `/gen-tests-python` — gera testes pytest para módulos/funções de um projeto Python.
- Hook: `run_pytest_python` — auto-gated PostToolUse (extensão `.py` + ancestral `pyproject.toml`); roda pytest e imprime saída só em falha.
- Naming convention para skills e hooks stack-specific (em `docs/philosophy.md`).

## [0.1.0] - 2026-04-30

Initial release.

### Added
- Skills: `/new-feature`, `/new-adr`, `/run-plan`.
- Agent: `code-reviewer` (YAGNI rubric).
- Hook: `PreToolUse` blocking direct edits to `.env` files (standalone Python script).
- Marketplace manifest for install via `/plugin marketplace add fppfurtado/pragmatic-dev-toolkit`.
- Documentation: philosophy, path contract, install guide.
