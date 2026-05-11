# ADR-016: Manter `block_gitignored` como está; falso-positivo em scripts operacionais é problema do consumer

**Data:** 2026-05-10
**Status:** Aceito

## Origem

- **Investigação:** Smoke-test do plugin v2.3.0 no projeto Java PJe (TJPA) reproduziu empiricamente falso-positivo do `block_gitignored.py` em scripts operacionais (`build_pje.sh`, `start_pje.sh`) — pontos de entrada do workflow de build/run local, gitignored via `*.sh` no `.gitignore` do consumer. Registro em `.claude/pragmatic-toolkit-validation.md` do PJe, achado #12 da fase 1. Triage 2026-05-10 avaliou 7 alternativas; todas com fricção doutrinária ou operacional inaceitável. Decisão de **não mudar o hook** + redirecionar pattern para responsabilidade do consumer merece formalização para evitar reabertura cíclica.

## Contexto

O hook `hooks/block_gitignored.py` (PreToolUse `Edit|Write`) bloqueia qualquer edit em path coberto pelo `.gitignore` do consumer. A intenção do design original (registrada quando o hook foi criado): "sinal vem de intenção declarada do repo (`.gitignore`), não de heurística codificada — robusto a stacks novas sem alterar o hook".

Pattern do consumer que gera atrito:

- `build_pje.sh`, `start_pje.sh` no PJe — pontos de entrada de build/run local. Gitignored via `*.sh` porque contêm paths locais hardcoded (`/home/<user>/...`) específicos por dev. Cada dev mantém o próprio.
- Análogos previsíveis em outros projetos legacy/IDE-heavy: scripts pessoais com paths hardcoded como entrypoints de workflow.

Quando o operador pede ao Claude para editar esses scripts, o hook bloqueia. Atrito recorrente em projetos com esse pattern.

**Tensão filosófica do problema:** o hook fundamenta-se em "sinal do consumer = `.gitignore`". Qualquer regra adicional no hook que **subverta esse sinal** introduz heurística codificada que contradiz parcialmente o design original e — mais profundamente — o **Path contract** de `docs/philosophy.md` (sinal vem do consumer via declaração; não há válvula de escape doutrinária para hooks per `docs/philosophy.md` → "Convenção de naming").

Alternativas avaliadas no triage (todas descartadas — detalhes em § Alternativas consideradas):

- **(a)** Allowlist via `pragmatic-toolkit:config`. Doutrinariamente puro no Path contract, mas torna hook config-aware — viola "hooks sem flags nem env vars".
- **(b)** Operador edita `.gitignore` adicionando `!build_pje.sh`. Doutrinariamente OK; operacionalmente exige tracked-by-default + `git update-index --skip-worktree`, transformando "script pessoal" em "template versionado com override local frágil" — mudança organizacional não desejada.
- **(c)** Hook não bloqueia paths na raiz do repo (libera por filename). Heurística codificada nova substitui sinal do `.gitignore` para arquivos da raiz — contradição parcial com Path contract.
- **(d)** Status quo (sem mudança, operador faz override caso a caso). Atrito recorrente em workflow legítimo do consumer.
- **(e)** Opt-in via env var/flag no hook. Contraria explicitamente "hooks sem flags nem env vars".
- **(f)** Parser de `.gitignore` para classificar padrões como "operational-like". Heurística sobre heurística; introduz I/O no hot path.
- **(e′)** Híbrido (c) + lista hardcoded de extensões bloqueadas. Tabela de patches infinitos.

**Achado decisivo (que fechou a análise):** o pattern do consumer (scripts pessoais como entrypoints de workflow) tem **solução pronta no ecossistema** que não exige mudança no plugin nem workaround técnico:

- **Makefile** com targets parametrizáveis via variáveis (`?=`); paths locais como defaults sobrescritíveis por env vars.
- **Dockerfile** + **docker-compose.yml** com bind mounts e `.env` para configuração por dev.
- Combinação dos dois: build target genérico no Make, runtime parametrizado via compose.

Esses artefatos são **tracked** (versionados pelo consumer), legíveis e editáveis pelo Claude sem disparar o hook. Devs com setup customizado parametrizam via env vars / `.env` files (este último coberto por `block_env.py` per ADR-015) ou variáveis na shell — sem hardcode em script gitignored.

O consumer não está pedindo essa refatoração ao plugin; está pedindo ao plugin que **acomode** o pattern atual. Mas o pattern em si (script gitignored como entrypoint de workflow) é a fonte do atrito — solução é mudar o consumer, não o plugin.

## Decisão

**Manter `block_gitignored.py` como está. Não introduzir liberação por filename, allowlist via config, env var, parser de padrões nem qualquer das 7 alternativas avaliadas.**

O pattern "script operacional gitignored como entrypoint de workflow" é **responsabilidade do consumer**. Consumers que encontrarem o falso-positivo devem refatorar o workflow para usar artefatos versionados (Makefile, Dockerfile, docker-compose) com parametrização por dev via env vars / `.env` files — não acomodar o pattern no plugin.

Razões:

- **Alinhamento doutrinário.** Cada alternativa (a)–(f), (e′) tem fricção doutrinária ou operacional inaceitável. Status quo é a opção que preserva integralmente o **Path contract** (sinal vem do consumer via `.gitignore`) e a **doutrina de naming/auto-gating de hooks** (sem flags, sem env vars, sem config-aware).
- **Custo do plugin estável.** Zero código novo, zero campo de config novo, zero acoplamento extra entre hook e contexto. O contrato com consumers existentes não muda.
- **Pattern do consumer tem solução pronta no ecossistema.** Makefile + Docker/compose resolvem o caso-classe sem exigir abstração no plugin. Refatorar mais tarde no consumer é mais barato do que abstrair cedo no plugin (`docs/philosophy.md` → "A filosofia em uma frase").
- **Decisão registrada.** Próximo encontro com este pattern (em outro consumer ou volta deste) não precisa repetir a análise das 7 alternativas — basta linkar este ADR e considerar gatilhos de revisão concretos.

## Consequências

### Benefícios

- Plugin preserva doutrina integral em duas frentes (Path contract + hooks sem flags).
- Zero refatoração de hook, zero campo de config novo, zero migração para consumers existentes.
- Investigação registrada — futuros operadores que encontrarem o mesmo problema têm caminho claro (refatorar workflow no consumer) sem reabrir a discussão.

### Trade-offs

- **Consumer com pattern atual ganha trabalho de refatoração.** Substituir `build_pje.sh` por target Makefile + Dockerfile/compose é trabalho não-trivial em projetos legacy (PJe usa JBoss EAP proprietário, podman/docker, paths que variam por dev). Esse trabalho **não é coberto pelo plugin** — fica como escopo separado para o consumer.
- **Atrito permanece** em consumers que decidirem não refatorar e continuarem com scripts gitignored como entrypoints. Aceito — é decisão organizacional do consumer, fora da blast radius do plugin.
- **Não cobre 100% dos casos** — consumer onde Makefile/compose não cobre (cenário raro envolvendo tooling proprietário não-containerizável) ficaria sem solução plugin-nativa.

### Limitações

- Esta decisão **só vincula o comportamento do hook do plugin**. Consumers livres para usar seus próprios overrides locais (bypass manual, edit fora do Claude, helpers próprios) — apenas o plugin não acomoda institucionalmente.
- Reversão tardia (introduzir uma das alternativas) tem custo proporcional à alternativa escolhida: (c) é o mais barato (regra de filename); (a) e (e) exigem mexer na doutrina de naming/auto-gating; (b) exige documentação/onboarding de pattern git; nenhum é destrutivo.

## Alternativas consideradas

### (a) Allowlist configurável via `pragmatic-toolkit:config`

Novo campo `paths.editable_local: ["build_pje.sh", "start_pje.sh", ...]` no bloco YAML do CLAUDE.md do consumer. Operador declara explicitamente paths editáveis mesmo gitignored.

Descartado:

- Torna o hook **config-aware** — viola `docs/philosophy.md` → "Convenção de naming" / `CLAUDE.md` → "Plugin component naming and hook auto-gating" ("hooks sem flags nem env vars para desligar"). Doutrina categórica, sem cláusula de escape documentada.
- Filosoficamente é o paragão do Path contract (consumer declara variantes via config), mas a doutrina específica de hooks vence a doutrina geral aqui.
- Reabertura exigiria ADR meta revisando a doutrina de naming/auto-gating de hooks antes desta.

### (b) Operador adiciona `!build_pje.sh` ao `.gitignore` + `git update-index --skip-worktree`

Zero código no plugin; consumer decide caso a caso via mecanismo nativo do git.

Descartado:

- `!build_pje.sh` torna o arquivo **tracked-by-default**, invalidando o motivo original do `*.sh` no gitignore (script é pessoal por dev). Requer commitar uma versão template + `skip-worktree` em cada checkout para override local.
- Muda o **contrato do arquivo** de "script pessoal não-versionado" para "template versionado + customização local opaca". Mudança organizacional, não só técnica.
- `skip-worktree` é frágil (`git stash`/`git pull` podem mexer; novo dev precisa lembrar de aplicar; `git reset --hard` reverte).

### (c) Hook não bloqueia paths na raiz do repo

Regra implícita no hook: build artifacts/deps ficam SEMPRE em subdirs (`target/`, `node_modules/`); arquivos diretamente na raiz são fonte legítima editável mesmo gitignored.

Descartado:

- Introduz **heurística codificada** que substitui parcialmente o sinal do `.gitignore` — contradição parcial com Path contract.
- Perde cobertura para arquivos sensíveis gitignored na raiz: `*.pem`, `*.key`, `dump.sql`, `*.bak`. Mitigação parcial (`*.env` coberto por ADR-015), mas não cobre todos.
- Aceita lixo de runtime na raiz (`*.log`, `.DS_Store`, dumps de profile) como editável.
- **Mudança de contrato com operador:** quem usava `.gitignore` da raiz como defesa anti-edit pessoal (`scratch.md`, `secrets.local.txt`) perde a garantia.

### (d) Status quo + operador faz override caso a caso

Aceitar atrito; operador override manual (rodar comando fora do Claude, editar via vim direto, copy/paste para o Claude e cola de volta).

Não é alternativa **separada** desta decisão — é justamente o que esta decisão escolhe. A diferença em relação à (d) crua é que aqui está **registrada** como decisão consciente + direção concreta ao consumer (refatorar workflow para Make/Docker), não apenas resignação.

### (e) Opt-in via env var / flag no hook

Escape hatch tipo `PRAGMATIC_TOOLKIT_ALLOW_GITIGNORED_ROOT=1`.

Descartado:

- Contraria explicitamente `CLAUDE.md` → "Plugin component naming and hook auto-gating": "sem flags nem env vars para desligar". Aceitar abre precedente para outros hooks.
- Configuração ambiental fácil de esquecer/errar — pior UX que (a).

### (f) Hook lê `.gitignore` e classifica padrões como "operational-like"

Parser leve do `.gitignore` identifica padrões "comuns de script" (`*.sh`, `*.iml`) e libera; bloqueia padrões "comuns de artefato".

Descartado:

- Heurística sobre heurística — sem ganho líquido sobre (c).
- Parser no hot path do PreToolUse (mesma preocupação de I/O de ADR-015 alternativa (d)).
- Catálogo de padrões vira tabela de patches infinitos por nova convenção de stack.

### (e′) Híbrido (c) + lista hardcoded de extensões bloqueadas

(c) com escape: libera raiz por default mas mantém bloqueio para extensões sensíveis (`*.pem`, `*.key`, `*.sql`, `*.bak`).

Descartado:

- Lista hardcoded é tabela de patches infinitos.
- ADR-015 já cobre o caso mais crítico (`*.env`).
- Pode virar ADR sucessor de (c) se a dor recorrer — não vale criar agora.

## Gatilhos de revisão

- **≥2 consumers independentes reportarem** o mesmo pattern de atrito (script operacional gitignored como entrypoint) **e** indicarem que refatorar via Makefile/compose não é viável no contexto deles. Critério mecânico: 2 reports independentes com justificativa de impossibilidade técnica de refatoração no consumer.
- **Incidente concreto** em que o operador edita um script local via workaround manual e introduz bug por copy/paste truncado / contexto perdido. Sinal de que o atrito custou mais que tolerar.
- **Mudança na doutrina de naming/auto-gating** (ADR meta revisitando `docs/philosophy.md` → "Convenção de naming" para permitir hooks config-aware). Sem cenário concreto hoje; reabriria a alternativa (a) como caminho legítimo.
- **Convenção de ecossistema mudar** — stack mainstream emerge emitindo build artifact diretamente na raiz (invalidaria o pressuposto de (c) e mudaria também a leitura desta decisão).
