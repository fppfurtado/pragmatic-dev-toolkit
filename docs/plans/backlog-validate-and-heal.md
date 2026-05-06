# Validação pós-merge de BACKLOG.md + skill `/heal-backlog`

## Contexto

Conflito recorrente em BACKLOG.md ao mergear PRs em paralelo (3ª ocorrência documentada — última no fan-out de PRs #20+#21 da sessão de refatoração philosophy/skills). `/debug` da 3ª ocorrência isolou a causa-raiz: GitHub Squash Merge faz 3-way merge sobre BACKLOG.md sem entender que `-line from ## Em andamento` + `+line to ## Concluídos` são uma operação lógica única ("mover linha"); quando main avançou desde a branch base do PR, o contexto dos hunks da RIGHT não bate com LEFT, e git auto-resolve aplicando apenas metade do diff. Resultado: linha duplicada em ambas seções, ou linha sumida.

`/run-plan` 4.7 (PR #19) já detecta divergência em BACKLOG.md **antes** do push e rebase a worktree — mas o bug ocorre **depois** do push, no momento em que GitHub mergeia o PR em main. `/run-plan` já fechou e não governa.

Solução em duas pernas conforme recomendação do `/debug`:

1. **Action** dispara em push para main; valida BACKLOG.md (sem duplicatas em Em andamento+Concluídos, estrutura íntegra); abre issue se inválido.
2. **Skill `/heal-backlog`** detecta o padrão automaticamente reconhecível (duplicata) e propõe edit de cura via gate Aplicar/Cancelar — assistida; complementar à Action.

Operador roda `/heal-backlog` quando notificado pela issue. Out-of-scope: padrão "linha sumida" automático (requer estado pré-merge; cobertura via input manual do operador no skill); mudança estrutural do BACKLOG.md (status inline em vez de seções) — fica para ADR futuro se a fricção persistir.

**Linha do backlog:** /run-plan 4.7: auto-rebase pré-push não cobre fan-out de PRs — quando 2 PRs ficam abertos em paralelo e um merge muda BACKLOG.md em main, o segundo PR pode mergear com merge artifact (linha duplicada em Em andamento+Concluídos ou linha sumida). Ocorreu na 3ª vez ao mergear PR #20 + #21. Considerar: detecção pós-merge no main + script de cura, ou bloqueio de /triage quando há PR aberto que ainda não fundiu.

## Resumo da mudança

**Action (detecção pós-merge):**
- `.github/workflows/validate-backlog.yml` — trigger em `push` para `main` com `paths: [BACKLOG.md]`. Permissions mínimas (`contents: read`, `issues: write`); token = `GITHUB_TOKEN` built-in (sem secrets externos).
- `.github/scripts/validate_backlog.py` — Python 3 stdlib. Parse de BACKLOG.md em seções (`## Próximos`, `## Em andamento`, `## Concluídos`); detecta linhas presentes em mais de uma seção. Exit não-zero + JSON em stdout listando os problemas.
- Workflow on failure: `gh issue create` com label `backlog-merge-artifact` e body composto do JSON do script.

**Skill `/heal-backlog` (cura assistida):**
- `skills/heal-backlog/SKILL.md` — nova skill genérica (stack-agnóstica), output fixo (sempre cura BACKLOG.md), nome `<verb>-<artifact>` per convenção de naming.
- Pré-condições: papel `backlog` resolvido; gap report se "não temos".
- Passos: ler BACKLOG.md → detectar duplicata Em andamento+Concluídos → propor edit de cura (remover de Em andamento; mover já completou) → gate `AskUserQuestion` Aplicar/Cancelar → escrever + reportar.
- Caso degenerado (BACKLOG.md íntegro): reportar "íntegro" e encerrar sem edit/gate.
- Linha sumida (não auto-detectável): aceitar input manual do operador em prosa (qual linha, qual seção) e inserir.

**Docs:**
- `README.md`: nova linha em "O que vem" para `/heal-backlog`.
- `docs/install.md`: adicionar `/heal-backlog` no smoke-test checklist.

## Arquivos a alterar

### Bloco 1 — `.github/scripts/validate_backlog.py`

Validação determinística sobre BACKLOG.md:

- Parse: linhas iniciando com `- ` agrupadas por seção H2 anterior.
- Detecta linha exata presente em mais de uma seção entre `## Próximos`, `## Em andamento`, `## Concluídos`.
- Output (stdout): JSON com `{ "problems": [{"type": "duplicate", "line": "...", "sections": [...]}, ...] }`.
- Exit: 0 se sem problemas; 1 se houver.
- CLI: `python validate_backlog.py <path-para-BACKLOG.md>`.
- Stack: Python 3 stdlib only (sem dependências externas).

### Bloco 2 — `.github/workflows/validate-backlog.yml` {reviewer: code,security}

GitHub Action:

- Trigger: `on: push: branches: [main], paths: [BACKLOG.md]`.
- `permissions: { contents: read, issues: write }` (mínimas para o caso de uso).
- Steps: checkout → setup-python (3.11) → run `python .github/scripts/validate_backlog.py BACKLOG.md` → if non-zero, `gh issue create --label backlog-merge-artifact --title "BACKLOG.md merge artifact detected" --body <JSON formatado>`.
- Token: `GITHUB_TOKEN` built-in (sem PAT, sem secrets externos).

Reviewer combinado: `code` para YAML/lógica do workflow; `security` para permissions explícitas, ausência de exfiltração de dados, escopo de token mínimo.

### Bloco 3 — `skills/heal-backlog/SKILL.md`

Nova skill no plugin:

- Frontmatter: `name: heal-backlog`, `description: Detecta merge artifacts em BACKLOG.md (linha duplicada em Em andamento+Concluídos) e propõe edit de cura. Use quando a Action de validação abrir issue ou quando suspeitar de inconsistência manual.`
- Pré-condições: papel `backlog` (ver Resolução de papéis em CLAUDE.md → "The role contract"); resolveu "não temos" → gap report (sem backlog não há o que curar).
- Argumentos: opcionais — sem argumento usa o papel `backlog`; argumento explícito = path para arquivo.
- Passos:
  1. Ler arquivo. Parse seções H2 + linhas-bullet.
  2. Detectar **duplicata Em andamento+Concluídos**: linha exata presente em ambas seções.
  3. Detectar **inconsistência estrutural**: seção ausente, header malformado.
  4. Sem padrão detectado → reportar "BACKLOG.md íntegro" e encerrar.
  5. Com padrão duplicata → propor edit (remover de Em andamento). Mostrar diff. Gate `AskUserQuestion` (header `Heal`, opções `Aplicar` / `Cancelar`).
  6. Aplicar → escrever arquivo, reportar paths + linhas afetadas. Cancelar → abort silente, nada para reverter.
  7. **Linha sumida (manual)**: operador suspeita de linha que sumiu mas não está em nenhuma seção → skill aceita input prosa (qual texto, qual seção destino), insere e gate Aplicar/Cancelar.
- `## O que NÃO fazer`: não inventar linhas (operador descreve quando manual); não fazer commit (operador commita); não mover linhas além do padrão duplicata sem instrução explícita; não tocar arquivos fora do papel `backlog`.

### Bloco 4 — Docs (README + install)

- `README.md` "O que vem": nova linha:
  ```
  | `/heal-backlog` | Skill | Detecta merge artifacts em `BACKLOG.md` (linha duplicada em Em andamento+Concluídos) e propõe edit de cura via gate Aplicar/Cancelar. Complementar à Action de validação pós-merge. |
  ```
- `docs/install.md` smoke checklist: adicionar item verificando `/heal-backlog` aparece em `/plugin list` e roda em BACKLOG.md íntegro retornando "íntegro".

## Verificação end-to-end

Repo tem `test_command: null`. Substituto textual:

1. **Script standalone íntegro:** `python .github/scripts/validate_backlog.py BACKLOG.md` (com BACKLOG.md atual) retorna exit 0; JSON output `{"problems": []}`.
2. **Script standalone vermelho:** criar fixture com BACKLOG.md tendo linha duplicada em Em andamento+Concluídos; rodar script → exit 1, JSON output lista a duplicata com sections corretas.
3. **YAML lint:** `actionlint .github/workflows/validate-backlog.yml` (se disponível); senão inspeção manual contra schema GitHub Actions (trigger, permissions, steps).
4. **Skill estrutura:** `skills/heal-backlog/SKILL.md` tem frontmatter (`name`, `description`), seções (`## Pré-condições`, `## Argumentos`, `## Passos`, `## O que NÃO fazer`), `## O que NÃO fazer` ≤7 itens scope guards genuínos.
5. **Plugin install:** plugin atualizado em projeto consumidor → `/heal-backlog` aparece em `/plugin list`.
6. **Docs consistência:** README e install.md mencionam `/heal-backlog`.

## Verificação manual

Cenários enumerados (gate "ok, vai pra produção"):

1. **Action smoke (caso vermelho):** branch de teste; introduzir manual em BACKLOG.md de main uma linha duplicada em Em andamento+Concluídos via PR; mergear via squash. Verificar:
   - Workflow `validate-backlog` dispara em push para main.
   - Workflow falha com exit não-zero.
   - Issue criada automaticamente com label `backlog-merge-artifact`.
   - Issue body contém a linha duplicada e seções identificadas.

2. **Action smoke (caso verde):** push para main com BACKLOG.md íntegro (cenário comum). Verificar:
   - Workflow só dispara se `BACKLOG.md` é parte do push (paths filter).
   - Quando dispara, passa silenciosamente (exit 0).
   - Nenhuma issue criada.

3. **Skill `/heal-backlog` (cura aplicada):** criar artefato local em BACKLOG.md (linha duplicada em Em andamento+Concluídos). Rodar `/heal-backlog`. Verificar:
   - Skill detecta padrão duplicata.
   - Mostra diff proposto (remover de Em andamento, manter em Concluídos).
   - Gate `Aplicar` / `Cancelar` aparece.
   - Aplicar → edit aplicado, BACKLOG.md íntegro, report cita linhas afetadas.
   - Cancelar (em invocação separada com mesmo cenário) → nada alterado em disco.

4. **Skill (BACKLOG limpo):** rodar `/heal-backlog` com BACKLOG.md íntegro. Verificar reporta "BACKLOG.md íntegro" e encerra sem edit/gate.

5. **Skill (linha sumida — manual):** simular linha sumida (remover linha real de BACKLOG.md). Rodar `/heal-backlog`. Verificar:
   - Skill não detecta padrão automaticamente (esperado).
   - Pede ao operador (prosa) qual texto está faltando e em qual seção destino.
   - Insere conforme descrito; gate Aplicar/Cancelar.

## Notas operacionais

- Action triggers só em `push: main` (não PR), porque o bug se manifesta após o merge.
- Label `backlog-merge-artifact` deve existir no repo; criar manualmente uma vez antes do primeiro disparo (ou Action cria via `gh label create` no setup, alternativa).
- Script Python stdlib-only — rodável em runners ubuntu-latest sem setup-python obrigatório (mas explícito por clareza).
- Skill `/heal-backlog` é stack-agnóstica e aplicável a qualquer projeto consumidor que use `BACKLOG.md` no formato canônico.
- Out-of-scope deste plano: representação alternativa do BACKLOG.md (status inline em vez de seções). ADR-level se a fricção persistir após este fix.
