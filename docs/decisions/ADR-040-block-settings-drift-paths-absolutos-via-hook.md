# ADR-040: Bloquear paths absolutos em `.claude/settings.json` via PreToolUse hook

**Data:** 2026-05-26
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-015](ADR-015-bloquear-env-files-por-sufixo.md) é o ancestral direto — primeiro PreToolUse block hook do plugin, estabelece pattern de gate por filename match com escape hatch documentado. ADR-040 estende a família lateralmente cobrindo classe nova (drift de paths absolutos em arquivo tracked específico) sem revogar nem substituir.
- **Decisão de referência metodológica:** [ADR-016](ADR-016-manter-block-gitignored-scripts-no-consumer.md) — segundo block hook, postura "consumer signal first, escape hatch documentado". ADR-040 herda a postura mas opera sobre file tracked específico (não há sinal de `.gitignore` a respeitar — `.claude/settings.json` é tracked por design Claude Code).
- **Critério editorial:** [ADR-034](ADR-034-criterio-adendo-vs-novo-adr-refinamento-doutrinal.md) Condição (5) "sucessor parcial lateral — estende ADR Aceito sem revogar" aplica em relação a ADR-015 (família PreToolUse block hooks).
- **Qualificação YAGNI interna:** [ADR-035](ADR-035-escopo-aplicacao-yagni-proprio-plugin.md) critério (1) "incidente recorrente" — `/insights` report (2026-05-26, 166 sessões analisadas) confirma múltiplos cleanup cycles em `.claude/settings.json` por session permission entries e absolute paths, exigindo cleanup commits repetidos antes de release.
- **Investigação:** ROADMAP item 5 (commit `d9e8896`) — último pendente da Onda 1 do plugin todo, único item de hygiene de execução não-coberto pelas waves anteriores.

## Contexto

O plugin já ship dois PreToolUse block hooks defensivos:

- `block_env.py` ([ADR-015](ADR-015-bloquear-env-files-por-sufixo.md)): bloqueia edits a env-files por sufixo `.env`. Defesa universal contra commit acidental de credenciais.
- `block_gitignored.py` ([ADR-016](ADR-016-manter-block-gitignored-scripts-no-consumer.md)): bloqueia edits a paths cobertos por `.gitignore` do consumidor. Defesa por sinal explícito do projeto.

Nenhum dos dois cobre o caso de **drift em arquivo tracked específico** que acumula entradas problemáticas por uso normal da ferramenta:

- `.claude/settings.json` é **tracked** (committed) por design Claude Code — guarda permissões compartilhadas da equipe.
- `.claude/settings.local.json` é **gitignored** por design — guarda permissões pessoais.

`/insights` report identifica friction recorrente: operador aceita uma permissão temporária durante uma sessão (Claude Code escreve em `settings.json` por default), e a entrada permanece tracked com `/home/<user>/path/absoluto` ou flag session-scoped. Próximo commit incluiria a entrada poluída se não for limpa manualmente. Mesmo cenário observado em múltiplas sessões da última onda.

`block_gitignored.py` não cobre — `settings.json` não está gitignored. `block_env.py` não cobre — não é env-file. Status quo: cleanup manual repetido antes de cada release que toca `.claude/`.

### Tensão com fronteira `.claude/` território Claude Code (ADR-018, ADR-005)

[ADR-018](ADR-018-replicacao-claude-em-modo-local-init-config.md) § Decisão estabelece "Plugin **nunca toca em `.claude/` raiz** — território do Claude Code, fora do escopo do plugin". [ADR-005](ADR-005-modo-local-gitignored-roles.md) § Mecânica de inicialização reafirma a invariante. ADR-040 introduz hook do plugin gating sobre conteúdo de `.claude/settings.json` — arquivo no território reservado.

Defesa: invariante ADR-018/ADR-005 proíbe **modificação proativa** do território `.claude/` pelo plugin (criação de arquivos, edição automática, replicação). Hook PreToolUse é categoria distinta — gate defensivo (exit 2 informativo) sobre conteúdo que o **operador** estaria escrevendo via Claude Code. Operador é o ator; hook só preserva higiene de arquivo tracked. Plugin não escreve, não cria, não move arquivo em `.claude/` — recusa edit que introduziria drift. Categoria paralela à de `block_env.py` que gateia edits em `.env` sem que isso seja considerado "tocar em env-files do consumer". Invariante ADR-018/ADR-005 preservada na sua leitura intencional (modificação proativa); ADR-040 opera em categoria diferente (gate defensivo reativo).

### Tensão com ADR-016 doutrina de hooks (consumer signal first)

[ADR-016](ADR-016-manter-block-gitignored-scripts-no-consumer.md) § Decisão estabelece que hooks consomem sinal do consumer (`.gitignore`) em vez de heurística codificada; § Alternativa (c) descartou explicitamente "heurística codificada que substitui parcialmente sinal do `.gitignore`". ADR-040 propõe content rule hardcoded (regex literal `/home/<user>/`, `/Users/<user>/`) sem consumer signal — exatamente o pattern que ADR-016 § (c) descartou.

Defesa: ADR-016 cobre o caso onde **sinal do consumer já existe** e pode ser consumido sem prescrever política (`.gitignore` declara intenção do projeto sobre o que é privado). Aqui o objeto protegido é tracked por design Claude Code — não há `.gitignore` a respeitar; settings.json é committed por contrato. Além disso, o pattern protegido é universal: paths absolutos `/home/<user>/` ou `/Users/<user>/` nunca pertencem a settings tracked, independente do consumer (são paths privados ao filesystem do operador específico, drift de session permission temporária). Categorias distintas — ADR-016 cobre "respeitar fronteira declarada pelo consumer"; ADR-040 cobre "bloquear drift universal em arquivo tracked específico". Leitura literal de ADR-016 preservada.

### Tensão com ADR-015 § Alternativa (d)

ADR-015 § Alternativa (d) descartou content-inspection no PreToolUse hot path com 3 razões: custo de I/O e parsing, markers heterogêneos entre stacks, ganho marginal sobre filename match. ADR-040 propõe **exatamente** content-inspection (regex no conteúdo novo do `Edit`/`Write`), em direção oposta. Reconhecimento explícito é necessário.

Defesa do escopo restrito que viabiliza content-inspection aqui:

- **File alvo único**: regex roda só quando `file_path` é exatamente `.claude/settings.json`. Hot path do hook permanece zero-custo para 99% dos edits (gate 1 filename match exclui antes do regex).
- **Formato estável**: settings.json é JSON estrito por design Claude Code; sem comments, sem heterogeneidade entre stacks; regex bruta é suficiente.
- **Regex curto**: dois patterns literais (`/home/[^/]+/`, `/Users/[^/]+/`); sem state machine, sem walk recursivo.
- **Ganho não-marginal**: friction empírica confirmada (`/insights` report, cleanup cycles documentados); status quo paga custo manual recorrente.

Defesa não revoga ADR-015 — Alternativa (d) continua válida para o caso geral de env-files (markers heterogêneos, ganho marginal). ADR-040 é exceção justificada por escopo restrito + formato estável.

## Decisão

Adicionar `hooks/block_settings_drift.py` como terceiro PreToolUse block hook do plugin, com 4 cláusulas:

1. **Target file específico**: bloqueio só dispara quando `tool_input.file_path` termina em `.claude/settings.json` exatamente. `.claude/settings.local.json` fora do escopo (gitignored, paths absolutos lá são esperados; permissões pessoais incluem paths do operador). Outros paths totalmente fora de escopo.

2. **Content patterns via regex bruta**: scan do conteúdo novo (campo `content` para `Write`, `new_string` para `Edit`) por regex `/home/[^/]+/` ou `/Users/[^/]+/`. Match → bloqueia. Sem match → exit 0. Regex bruta vs JSON parse + key-targeted: regex é suficiente porque settings.json não suporta comments e strings que carregam path absoluto em settings.json são quase sempre perm de fato (falso-positivo improvável).

3. **Escape hatch documentado**: operador que precisa legitimamente de path absoluto em `settings.json` (cenário raro, sinaliza setup atípico) tem caminhos conhecidos: (a) mover para `settings.local.json` (default — paths pessoais não pertencem a tracked); (b) substituir por variável (`$HOME/`, `~/`) que regex não casa; (c) editar via outras ferramentas fora do Claude Code (escape hatch universal). Mensagem stderr do hook lista os 3 caminhos.

4. **Windows fora de escopo**: regex não cobre `C:\Users\<user>\` ou prefixos Windows. Plugin é primariamente Linux/macOS (declarado em CLAUDE.md); sem incidente Windows reportado (critério ADR-035 "(1) incidente recorrente" ausente para incluir cobertura agora); inclusão exigiria escape duplo de backslash em regex sobre JSON-encoded strings, custo de manutenção não pago pela clareza no momento. Reabrir em ADR sucessor se incidente surgir.

## Consequências

### Benefícios

- Friction recorrente de cleanup manual em `.claude/settings.json` eliminada para 99% dos casos (paths absolutos `/home/`/`/Users/` são o pattern dominante reportado por `/insights`).
- Hook é silente em projetos consumer que não editam `settings.json` ou que editam sem introduzir paths absolutos.
- Defesa em camadas com block_env.py e block_gitignored.py: cada hook tem política própria sobre uma classe específica, sem sobreposição.
- Política explícita: "paths absolutos não pertencem a `settings.json` tracked". Operador externo pode auditor sem ler o regex.

### Trade-offs

- **Custo no hot path**: content-inspection sobre o conteúdo novo a cada `Edit`/`Write` que case gate 1. Mitigado por escopo restrito (gate 1 filename match exclui 99% dos edits antes do regex).
- **Falso-positivo possível**: regex casa qualquer string contendo `/home/<user>/` ou `/Users/<user>/`, incluindo comentário ou string não-perm (settings.json não suporta comments, mas pode ter docstring em algum campo futuro). Aceitável dado raridade e existência de escape hatch.
- **Mensagem stderr em inglês**: hooks são exceção universal à convenção de idioma do plugin (philosophy.md → Convenção de idioma; precedente block_env.py). Operador de projeto consumer em outro idioma vê mensagem em inglês — trade-off aceito por ADR-007 § Hooks.

### Limitações

- **Session perms fora do escopo desta versão**: `/insights` reportou duas classes de drift recorrente em `settings.json` — paths absolutos AND session-scoped permission entries. ADR-040 cobre só paths absolutos. Detectar session perms exigiria parse JSON + schema knowledge dos campos `permissions.allow/deny/ask`, frágil a mudanças futuras do formato Claude Code settings. Reabrir via Gatilho de revisão se incidentes recorrerem.
- **Windows fora**: cláusula 4 da Decisão. Reabrir via ADR sucessor com incidente real.
- **Defesa não bypass-proof**: operador pode editar `settings.json` fora do Claude Code (escape hatch — cláusula 3). Hook é gate defensivo, não política de segurança forçada.

## Alternativas consideradas

### (a) CI lint pós-fato

GitHub Action / pre-commit hook que valida `.claude/settings.json` no momento do commit (paralelo a `validate-backlog` de [ADR-013](ADR-013-ci-lint-minimo-no-build-runner.md)). Descartado:

- **Loop de feedback lento**: erro detectado no commit / push / PR; operador precisa pivotar contexto para limpar.
- **Cleanup ainda exigido**: lint flaga, operador roda cleanup manual mesmo assim.
- **Não previne acúmulo intra-sessão**: entrada poluída pode ficar dias na tree antes de tentar commitar.
- Ferramenta correta para a classe: PreToolUse hook bloqueia no momento da intenção; CI lint é última linha de defesa para casos que escapam (válido em camadas, não substitui).

### (b) JSON parse + key-targeted em `permissions.*`

Parse JSON do conteúdo novo, walk recursivo em `permissions.allow/deny/ask` arrays, check de cada string. Descartado:

- **Dep parse**: adiciona stdlib `json.loads` no hot path (toleráve), mas walk recursivo em estrutura arbitrária adiciona complexidade material.
- **Schema-awareness frágil**: depende de conhecer paths dos campos onde permissões vivem; mudanças futuras do formato Claude Code settings (novo campo, renomeação) quebram silenciosamente — hook deixa de bloquear sem aviso.
- **Ganho marginal**: regex bruta tem falso-positivo improvável em settings.json (sem comments, strings carregando path absoluto em settings.json são quase sempre perm de fato).
- Reabrir se falso-positivo recorrente reportado.

### (c) Cobertura de session perms

Adicionar detecção de session-scoped permission entries (campo type-specific no JSON, lifetime metadata). Descartado **desta versão**:

- Exige parse JSON + schema knowledge (mesmo problema de (c) ampliado).
- `/insights` não quantificou cleanup cycles por categoria; paths absolutos é o pattern com superfície mais visível e regex simples.
- Cobrir paths absolutos sozinho resolve a parte maior da friction; session perms vira Gatilho de revisão (abaixo).

### (d) Allowlist configurável via `pragmatic-toolkit:config`

Operador declara paths legítimos no bloco YAML do CLAUDE.md (`paths.settings_absolute_allowed: [...]`). Descartado: move complexidade para o consumer; default precisa cobrir 99% sem config. Pode virar feature futura sob ADR sucessor se atrito real surgir (ex.: setup atípico de empresa com path absoluto em settings.json tracked).

### (e) Agent-side rule (rule em CLAUDE.md, sem hook)

Instruir Claude via CLAUDE.md a nunca escrever paths absolutos em settings.json. Descartado: rules em prompt são best-effort, não forçadas. Hook PreToolUse é deterministic — exit 2 bloqueia. Operador continua podendo editar via outras ferramentas (escape hatch).

## Gatilhos de revisão

- **Falso-positivo recorrente**: operador em consumer reporta path legítimo `/home/<user>/` ou `/Users/<user>/` em settings.json bloqueado indevidamente. Limiar prático: ≥2 reports independentes → (b) JSON parse + key-targeted vira pertinente.
- **Recorrência de session perms**: ≥2 cleanup commits por session-perm drift em 30 dias após release de ADR-040 → (c) cobertura de session perms vira pertinente.
- **Incidente Windows**: report de operador em Windows com path `C:\Users\<user>\` poluindo settings.json → reabrir cláusula 4 da Decisão em ADR sucessor.
- **Mudança no formato Claude Code settings**: novo campo de permissões introduzido, ou renomeação de `permissions.*` — reavaliar se regex bruta ainda cobre adequadamente.
- **Pedido recorrente para bypass via config**: sinal de que (d) allowlist configurável viraria pertinente.
