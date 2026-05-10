# Plano — marketplace prep batch 2 (CI validate + ADR-013)

## Contexto

Item `#6` do BACKLOG (Lote 2 da sequência marketplace prep): adicionar validação automática mínima dos manifests + parse Python dos hooks via GitHub Action. Fecha a classe "release quebrada por typo" — JSON malformado em `plugin.json`/`marketplace.json` ou syntax error em `hooks/*.py` instalam silenciosamente e quebram em runtime no consumidor.

**Tensão doutrinária formalizada como ADR.** `CLAUDE.md` "Editing conventions" diz: *"Don't introduce a build system, package manager, or test runner for this repo itself."* CI lint mínimo de manifests/sintaxe não cabe em nenhuma das 3 categorias vetadas (não compila, não instala, não roda testes) — é categoria distinta. Operador alinhou no `/triage` (após segundo find do `design-reviewer`) por elevar a ADR-013 em vez de nota editorial: o framing "fronteira/categoria distinta" preserva a frase canonical intacta e materializa a delimitação no registro decisório, em vez de abrir "Exception" no CLAUDE.md (que abriria porta para futuras exceções incrementais).

**Decisões do `/triage` 2026-05-10:**

- **Schema validation:** `python -m json.tool` apenas (portável, ~20 linhas YAML, sem dependência de CLI Claude). Cobertura sintática JSON; **complementada por assertions inline mínimas para chaves obrigatórias dos manifests** (per finding 2 do design-reviewer) — fecha a classe de erro detectada empiricamente no batch 1 (`$schema` URL fake, `description` em path errado), que `json.tool` puro deixaria passar. Schema completo via CLI fica como gatilho de revisão do ADR-013.
- **Estrutura:** passos inline no YAML, sem script separado em `scripts/`. YAGNI default; operador local copia comandos do YAML para validação manual.
- **Trigger:** apenas `pull_request` (sem `push: main` redundante — sob fluxo canônico do toolkit, todo commit em main chega via PR).
- **ADR-013 vs nota editorial:** elevado para ADR per memória `feedback_adr_threshold_doctrine` + reframing "fronteira" (não "exceção") sugerido pelo reviewer.

**Linha do backlog:** plugin: marketplace prep #6 (infra) — CI mínimo de validação de manifests via GitHub Action (~20 linhas YAML): `python -m json.tool` em `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `hooks/hooks.json`; `python -c "import ast; ast.parse(open(p).read())"` em cada `hooks/*.py`. Fecha classe inteira de "release quebrada por typo" sem suite de testes.

## Resumo da mudança

**Entra:**

1. **ADR-013** (`docs/decisions/ADR-013-ci-lint-minimo-no-build-runner.md` — template criado neste `/triage`, conteúdo preenchido no Bloco 1) codifica fronteira: "CI lint mínimo (validação de invariantes de manifest e sintaxe de hooks via `.github/workflows/validate.yml`) é categoria distinta das 3 vetadas pela frase canonical (build system / package manager / test runner)". Inclui escopo positivo enumerado, escopo negativo (limitações), 3 alternativas consideradas (sem CI / CI rico / pre-commit local), 5 gatilhos de revisão.
2. **Nota cross-ref em `CLAUDE.md`** "Editing conventions" — substituir o bullet "Don't introduce a build system, package manager, or test runner..." adicionando uma frase final curta: *"(Manifest/syntax invariant checks via CI lint are a distinct category — see ADR-013.)"* Mantém a frase canonical intacta; delega delimitação ao ADR.
3. **`.github/workflows/validate.yml`** (novo) — Action com trigger `pull_request`, ubuntu-latest, sem matriz, sem `actions/setup-python` (runner default ≥ 3.10). Steps:
   - `actions/checkout@v4`.
   - `python3 -m json.tool` em cada manifest + `hooks/hooks.json`.
   - Loop `ast.parse` em `hooks/*.py`.
   - Assertions inline para chaves obrigatórias dos manifests (per finding 2 do reviewer): `python -c "import json; d=json.load(open(p)); assert <chaves>"`.

**Fica de fora:**

- `actions/setup-python` para fixar versão Python — runners ubuntu trazem ≥3.10 default; pinning entra como gatilho de revisão do ADR-013 se runner cair abaixo.
- Cache de dependências — sem `pip install` no caminho, sem cache.
- Lint/format de markdown ou YAML do próprio repo — escopo do CI é manifest+hook integrity, não estilo doc. Categorizado explicitamente como "fora do escopo" no ADR-013.
- Matriz de SO ou versão Python — overhead sem retorno (hooks rodam no Linux do consumidor; Windows/macOS não são alvo).
- `claude plugin validate` no CI — recusado por dependência de CLI Claude no runner; reentrada como gatilho de revisão do ADR-013 se schema drift concreto surgir.
- Trigger `push: main` — redundante com `pull_request` sob fluxo canônico (per finding 3).
- Suite de testes do plugin — vetado pela frase canonical do CLAUDE.md, reafirmado no ADR-013 como fora do escopo.
- Badge do CI no README — adiar para depois do `validate.yml` provar estável.

## Arquivos a alterar

### Bloco 1 — ADR-013 conteúdo {reviewer: doc}

- `docs/decisions/ADR-013-ci-lint-minimo-no-build-runner.md`: substituir placeholders pelo conteúdo abaixo.
  - `## Origem`: bullet com **Investigação:** sessão `/triage` 2026-05-10 (Lote 2 da sequência marketplace prep, item `#6` do BACKLOG); design-reviewer reabriu a tensão com frase canonical do CLAUDE.md como ADR-worthy (default per memória `feedback_adr_threshold_doctrine`).
  - `## Contexto`: citar literal a frase canonical em `CLAUDE.md` (`Don't introduce a build system, package manager, or test runner for this repo itself`); explicar que CI lint mínimo de manifests/sintaxe não compila/instala/roda testes — não cabe nas 3 categorias vetadas. Sem ADR explícito, leitor futuro tropeça na questão "isso é exceção ou complemento?". Classe de bug "release quebrada por typo" emergiu empiricamente (batch 1 detectou `$schema` URL fake e `description` em path errado via `claude plugin validate` — gap que `json.tool` sozinho deixaria passar).
  - `## Decisão`: **CI lint mínimo de invariantes de manifest e sintaxe de hooks é categoria distinta das 3 vetadas pela frase canonical.** Critério mecânico para classificar artefato como "CI lint mínimo permitido" (opera sob este ADR): (i) valida invariantes sintáticas (parse de JSON/YAML/Python AST) ou estruturais mínimas (chaves obrigatórias presentes em manifests); (ii) sem instalação de dependências externas além do runtime do runner; (iii) sem execução de behavior de produção (não roda hooks, não invoca skills/agents); (iv) tempo de wall-clock < 30s. Cobertura positiva: `python -m json.tool` em `plugin.json` + `marketplace.json` + `hooks/hooks.json`; `python -c "import ast; ast.parse(...)"` em `hooks/*.py`; assertions inline para chaves obrigatórias dos manifests; parse de frontmatter (`name:`/`description:`) em `skills/*/SKILL.md` e `agents/*.md` quando vier a entrar (deixado fora desta primeira iteração — escopo controlado). Razões: audiência distinta da prosa operativa (Action protege release; doutrina vetava infra de produto); critério mecânico testável (tempo, dependências, behavior); preserva frase canonical intacta.
  - `## Consequências`:
    - **Benefícios:** classe "release quebrada por typo" fecha sem suite de testes; doutrina ganha fronteira nítida em vez de cláusula de exceção (que escala mal); skill author futuro consegue enquadrar gate novo de CI sem reabrir doutrina.
    - **Trade-offs:** dependência de runner externo (GitHub Actions); cobertura sintática ≠ semântica (não pega contrato quebrado, ex.: skill `name` que não bate com diretório); operador precisa lembrar do critério mecânico ao avaliar gates novos.
    - **Limitações:** schema completo via `claude plugin validate` fica fora (CLI dependency); lint de estilo (markdownlint, yamllint, ruff) fica fora (estilo ≠ invariante); test runner / package manager / build pipeline permanecem vetados pela frase canonical; matriz de SO/Python fora.
  - `## Alternativas consideradas`:
    - **(a) Sem CI nenhum (status quo).** Descartado: classe "release quebrada por typo" passa silente até consumidor reportar; custo de reverter v1.X.Y > custo de 20 linhas YAML.
    - **(b) CI rico com `claude plugin validate` + suite de testes.** Descartado: introduz exatamente o vetado pela frase canonical (test runner, setup de CLI, package install); custo de manutenção desproporcional ao retorno (sem código de produto compilável, sem behavior a testar).
    - **(c) Pre-commit hook local em vez de Action.** Descartado: depende de operador instalar localmente; não cobre PR aberto por colaborador externo nem release direto via UI do GitHub. Action é o único lugar onde o gate é incontornável.
  - `## Gatilhos de revisão`:
    - Schema completo via `claude plugin validate` virar viável (CLI Claude disponível em runners ubuntu sem setup ou setup ficar < 5 linhas) → reabrir para incluir.
    - Matriz de SO ou versão Python virar relevante (consumidor Windows/macOS, runner default cair abaixo de 3.10) → reabrir para considerar.
    - Suite de testes do próprio plugin emergir como necessidade (testes unitários de skills/agents/hooks) → reabrir; provavelmente requer ADR sucessor explicitamente revogando trecho da frase canonical.
    - Custo operacional do gate (flakes recorrentes, drift de runner) → reabrir para considerar pinning ou simplificação.
    - Fronteira disputada (proposta concreta de lint de markdown, badge automation, deploy de docs, etc.) → reabrir para reexaminar critério mecânico e ver se acomoda ou rejeita.
  - Status final do ADR: `Aceito` (após preencher e revisar).

### Bloco 2 — `CLAUDE.md` cross-ref {reviewer: doc}

- `CLAUDE.md` "Editing conventions" (bullet "Don't introduce a build system..."): adicionar **uma frase curta** ao final do bullet, **mantendo o texto canonical intacto**, sob forma de cross-ref:
  - Direção: ao final do bullet (antes do ponto final que fecha o bullet existente), inserir: " (Manifest/syntax invariant checks via CI lint are a distinct category — see [ADR-013](docs/decisions/ADR-013-ci-lint-minimo-no-build-runner.md).)"
  - **Não** usar palavra "Exception"; reframing "distinct category" preserva a frase canonical e delega delimitação ao ADR.
  - Preservar resto do parágrafo e bullet seguinte.

### Bloco 3 — `.github/workflows/validate.yml` (novo) {reviewer: code}

- `.github/workflows/validate.yml`: criar Action mínima.
  - Trigger: `on: pull_request` (sem `push: main` — redundante per finding 3).
  - Job único `validate` em `ubuntu-latest`.
  - Steps:
    1. `actions/checkout@v4`.
    2. JSON parse: `python3 -m json.tool .claude-plugin/plugin.json > /dev/null && python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && python3 -m json.tool hooks/hooks.json > /dev/null`.
    3. Manifest invariants (assertions inline per finding 2):
       ```
       python3 -c "import json; d=json.load(open('.claude-plugin/plugin.json')); assert {'name','version','description'} <= set(d.keys()), f'plugin.json missing required keys: {d.keys()}'"
       python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); assert {'name','plugins'} <= set(d.keys()), f'marketplace.json missing required top-level keys: {d.keys()}'; assert all({'name','source'} <= set(p.keys()) for p in d['plugins']), 'marketplace.json plugin entries missing name/source'"
       ```
    4. Hook AST parse: `for f in hooks/*.py; do python3 -c "import ast; ast.parse(open('$f').read())"; done`.
  - Sem `permissions:` (default read-only suficiente).
  - Nome do workflow: `validate` (visível no UI do PR).
  - Sintaxe YAML 2-space indent, key order canônico GitHub Actions.

## Verificação end-to-end

- `docs/decisions/ADR-013-ci-lint-minimo-no-build-runner.md`: cross-ref para CLAUDE.md (link ou citação) e citação literal da frase canonical em `## Contexto` resolvendo; alternativas (a/b/c) listadas; gatilhos de revisão (5) listados; status `Aceito`; framing "categoria distinta" (não "exceção").
- `CLAUDE.md` "Editing conventions": frase canonical intacta + cross-ref a ADR-013 ao final do bullet; **não** usa palavra "Exception".
- `.github/workflows/validate.yml` existe e parsa como YAML válido: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/validate.yml').read())"` → exit 0.
- Action segue convenções GitHub Actions: top-level `name`, `on`, `jobs`; job tem `runs-on` e `steps`. Trigger é `pull_request` (sem `push:`).
- Localmente, simular o que o CI fará — rodar todos os comandos de validação e confirmar exit 0:
  ```
  python3 -m json.tool .claude-plugin/plugin.json > /dev/null && \
  python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && \
  python3 -m json.tool hooks/hooks.json > /dev/null && \
  python3 -c "import json; d=json.load(open('.claude-plugin/plugin.json')); assert {'name','version','description'} <= set(d.keys())" && \
  python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); assert {'name','plugins'} <= set(d.keys()); assert all({'name','source'} <= set(p.keys()) for p in d['plugins'])" && \
  for f in hooks/*.py; do python3 -c "import ast; ast.parse(open('$f').read())"; done && \
  echo "all green"
  ```
- `git log` mostra 3 commits coerentes (1 por bloco).

## Verificação manual

Cenários enumerados (não direção genérica), per critério para superfícies não-determinísticas (Action roda em runner externo):

1. **Action roda verde no PR.** Após push, confirmar via `gh pr checks <num>` (ou aba Checks no UI) que o workflow `validate` aparece e completa em verde dentro de ~30s.
2. **Cenário de falha exercitado localmente** (não-opcional per finding 7): operador introduz typo em `plugin.json` (vírgula extra, aspa quebrada, ou remove uma das chaves obrigatórias `name`/`version`/`description`), roda o snippet completo de "Verificação end-to-end" acima, **confirma exit non-zero**, depois reverte o typo. Custo: ~30s. Falso-positivo de "Action verde sem step" fica descartado — comandos exatos do YAML pegam o caso.
3. **Versão Python no runner.** Após verde no cenário 1, inspecionar log do step e confirmar `python3 --version` ≥ 3.10. Se runner trouxe versão menor, gap real do escopo de Verificação — registrar como `## Pendências de validação` (gatilho do ADR-013 já contempla, escopo de re-iteração).

## Notas operacionais

- **Ordem dos blocos.** Sequência prescrita: (1) ADR-013 conteúdo → (2) `CLAUDE.md` cross-ref → (3) `.github/workflows/validate.yml`. Doutrina (ADR) antes de doc espelhante (CLAUDE.md cross-ref); implementação por último. Acoplamento Bloco 2 → Bloco 1 explicitado: cross-ref cita `ADR-013-...md` que só existe após Bloco 1.
- **`design-reviewer` rodou 2 vezes** durante este `/triage` (2026-05-10): no plano (primeira passagem; flagrou 7 issues: ADR-worthiness do finding 1, schema gap do finding 2, trigger redundante do finding 3, validação manual frágil do finding 7, mais 3 informativos) e no draft do ADR-013 (flagrou framing "fronteira" vs "exceção", enumeração de fronteiras, 3 alternativas, 5 gatilhos de revisão). Findings consolidados nas direções dos 3 blocos. `/run-plan` **não precisa redisparar** `design-reviewer`; `doc-reviewer` (Blocos 1 e 2) e `code-reviewer` (Bloco 3) por bloco cobrem o resto.
- **Bloco 1 (ADR-013) status final `Aceito`.** Padrão do repo é heterogêneo (ADR-007/009/012 `Aceito`; ADR-011 `Proposto`); plano prescreve `Aceito` por consistência com a sessão atual de decisão (operador re-alinhou após reviewer; conteúdo materializa decisão tomada, não proposta a discutir).
- **Bloco 3 reviewer `code` — cerimônia previsível.** YAML de Action é DSL declarativa sem classe/abstração. `code-reviewer` provavelmente reporta "nada substantivo a flagar" (per finding 6 marginal do reviewer no plano). Aceitável manter — alternativa (`{reviewer: doc}`) é defensável mas convenção do template não cobre YAML; manter `code` como default sem-extensão-md/rst/txt.
- **Sem badge no README** neste plano (per Resumo da mudança "fica de fora"). Reabrir como follow-up se publicação ampla justificar.

## Pendências de validação

- Cenário 1 da `## Verificação manual` (Action verde no PR via `gh pr checks`) — só validável após push; operador valida pós-`gh pr create`.
- Cenário 3 da `## Verificação manual` (Python ≥ 3.10 no runner via inspeção do log) — só validável inspecionando log do step após push; operador valida pós-`gh pr create`. Gap real do escopo de Verificação se runner trouxe versão menor — gatilho de revisão do ADR-013 já contempla.
