> **ARCHIVED 2026-05-31** — content absorbed into [ADR-050](../ADR-050-componentes-plugin-consolidado.md); see that ADR for current authority. Body below preserved verbatim for historical record.

# ADR-013: CI lint mínimo como complemento à doutrina no-build/runner

**Data:** 2026-05-10
**Status:** Aceito

## Origem

- **Investigação:** Sessão `/triage` 2026-05-10 do item `marketplace prep #6` do BACKLOG (Lote 2 da sequência marketplace prep). `design-reviewer` reabriu a tensão com a frase canonical do `CLAUDE.md` — adicionar `Exception: minimal CI lint` ao bullet `Don't introduce a build system, package manager, or test runner` lê como introdução de classe nova de artefato (CI/Action), não como esclarecimento de zona não-coberta. Memória do operador `feedback_adr_threshold_doctrine` (refinar/inverter doutrina, mesmo parcialmente, → default ADR) aplicou.

## Contexto

`CLAUDE.md` "Editing conventions" tem a frase canonical:

> Don't introduce a build system, package manager, or test runner for this repo itself. The hooks are runnable Python scripts (`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<script>.py`); the rest is markdown.

A frase lista 3 categorias específicas (build system, package manager, test runner) com motivação implícita: este repo não tem código compilável nem suite, então a infra correspondente seria cerimônia tática.

CI lint mínimo de manifests/sintaxe **não cabe em nenhuma das 3 categorias vetadas**: não compila nada, não instala dependências, não roda testes. Mas está na vizinhança o suficiente para gerar dúvida — sem ADR explícito, leitor futuro tropeça em "isso é exceção à frase canonical ou complemento dela?". Sem critério mecânico, a próxima proposta de gate (lint de markdown, deploy de docs, badge automation) re-abre a doutrina caso a caso.

A classe de bug "release quebrada por typo" emergiu empiricamente no batch 1 da sequência marketplace prep: `claude plugin validate` rejeitou `marketplace.json` por `$schema` URL fake (404) e `description` em path top-level errado (campo só aceito em `metadata.description`). Esses erros ficaram instalados no repo até o batch 1, sem nenhum gate que os pegasse no PR. Sem CI lint, o próximo typo (vírgula mal colocada, key obrigatória renomeada) tem o mesmo destino — silente até consumidor reportar.

## Decisão

**CI lint mínimo de invariantes de manifest e sintaxe de hooks é categoria distinta das 3 vetadas pela frase canonical.** A frase canonical permanece intacta; este ADR formaliza a fronteira (não abre exceção).

**Critério mecânico para classificar um gate como "CI lint mínimo permitido"** (cumulativo — todos os 4 critérios devem aplicar):

1. Valida invariantes **sintáticas** (parse de JSON/YAML/Python AST) ou **estruturais mínimas** (chaves obrigatórias presentes em manifests).
2. Sem instalação de dependências externas além do runtime base do runner (Python ≥3.10 default em ubuntu-latest).
3. Sem execução de behavior de produção — não roda hooks, não invoca skills/agents, não dispara workflow do plugin.
4. Tempo de wall-clock < 30s no runner default.

**Cobertura positiva** (gates dentro do escopo):

- `python -m json.tool` em `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `hooks/hooks.json`.
- `python -c "import ast; ast.parse(...)"` em cada `hooks/*.py`.
- Assertions inline em `python -c` para chaves obrigatórias dos manifests (ex.: `assert {'name','version','description'} <= set(plugin.json.keys())`).
- Frontmatter parse de `skills/*/SKILL.md` e `agents/*.md` (`name:`, `description:` presentes) — aceitável sob este ADR, deixado fora desta primeira iteração por escopo controlado.

**Cobertura negativa** (fora do escopo, permanece vetado):

- Suite de testes do próprio plugin — `pytest`, `jest`, etc. (test runner pela frase canonical).
- Package install no CI — `pip install`, `npm ci`, `cargo fetch` (package manager pela frase canonical).
- Build pipeline — compilação, bundling, deploy de artefatos (build system pela frase canonical).
- Schema validation completa via `claude plugin validate` no runner — exige setup de CLI Claude (~30 linhas YAML extras + frágil); fica como gatilho de revisão.
- Lint de estilo — `markdownlint`, `yamllint`, `ruff format`, etc. Estilo ≠ invariante; mesmo peso operacional de test runner sem mesmo retorno.

Razões:

- **Audiência distinta da frase canonical.** A frase visou impedir cerimônia tática de produto (build/test/package); CI lint protege release de typo, não compete com a doutrina.
- **Critério mecânico testável.** Os 4 critérios cumulativos (tempo, dependências, behavior, sintaxe-vs-comportamento) permitem classificar gate novo sem reabrir doutrina.
- **Preserva frase canonical intacta.** Nenhuma cláusula de exceção; ADR é referência cruzada, não revisão.
- **Fecha classe empírica.** Erros do batch 1 (`$schema` 404, `description` top-level rejeitada) são exatamente o que `python -m json.tool` + assertions inline pegam.

## Consequências

### Benefícios

- Classe "release quebrada por typo" fecha sem suite de testes do plugin.
- Doutrina ganha fronteira nítida em vez de cláusula de exceção (que escala mal — abre porta para "exceptions" futuras).
- Skill author / contribuidor futuro consegue enquadrar gate novo de CI sem reabrir doutrina; critério mecânico decide.
- Frase canonical do `CLAUDE.md` permanece intacta; cross-ref de 1 linha ao ADR-013 delega delimitação sem editar a doutrina.

### Trade-offs

- Dependência de runner externo (GitHub Actions). Outage do runner = sem gate. Aceito — gate informativo, não bloqueante de release.
- Cobertura sintática ≠ semântica. CI não pega contrato quebrado (ex.: `name:` da skill que não bate com diretório, slug do plano que diverge do filename). Esse buraco fica.
- Operador precisa lembrar do critério mecânico ao avaliar proposta nova. Mitigação: gatilhos de revisão explícitos abrindo o ADR quando fronteira for disputada.

### Limitações

- **Schema completo** via `claude plugin validate` fica fora — instalação do CLI no runner é setup desproporcional (~30 linhas YAML extras, frágil). Reentrada como gatilho de revisão.
- **Lint de estilo** fica fora (markdownlint, yamllint, ruff format) — estilo é decisão editorial, não invariante.
- **Test runner / package manager / build pipeline** permanecem vetados pela frase canonical, reafirmados aqui.
- **Matriz de SO ou versão Python** fora — overhead sem retorno (hooks rodam no Linux do consumidor; Windows/macOS não são alvo do toolkit).

## Alternativas consideradas

- **(a) Sem CI nenhum (status quo pré-batch 1).** Descartado: classe "release quebrada por typo" passa silente até consumidor reportar (ou até validador externo testar, como no batch 1). Custo de reverter v1.X.Y > custo de 20 linhas YAML.
- **(b) CI rico com `claude plugin validate` + suite de testes do plugin.** Descartado: introduz exatamente o vetado pela frase canonical (test runner, setup de CLI, package install). Custo de manutenção desproporcional ao retorno (sem código de produto compilável; behavior do plugin é prosa de skill, não testável unitariamente).
- **(c) Pre-commit hook local em vez de GitHub Action.** Descartado: depende de operador instalar localmente. Não cobre PR aberto por colaborador externo nem release direto via UI do GitHub. Action é o único lugar onde o gate é incontornável.

## Gatilhos de revisão

- **Schema completo via `claude plugin validate` virar viável no runner** — CLI Claude disponível em runners ubuntu sem setup, ou setup ficar < 5 linhas YAML. Reabrir para incluir.
- **Matriz de SO ou versão Python virar relevante** — consumidor Windows/macOS reportar incompatibilidade, ou runner ubuntu-latest cair abaixo de 3.10. Reabrir para considerar `actions/setup-python` ou matriz.
- **Suite de testes do próprio plugin emergir como necessidade** — testes unitários de skills/agents/hooks. Reabrir; provavelmente requer ADR sucessor explicitamente revogando trecho da frase canonical do `CLAUDE.md` (test runner permite-se sob nova doutrina).
- **Custo operacional do gate** — flakes recorrentes, drift de runner default, latência > 30s. Reabrir para considerar pinning (`actions/setup-python` para fixar versão), simplificação ou abandono.
- **Fronteira disputada** — proposta concreta de gate novo (lint de markdown, badge automation, deploy de docs, smoke teste de skill) que crie tensão com a frase canonical. Reabrir para reexaminar o critério mecânico (4 cumulativos) e ver se acomoda ou rejeita.
