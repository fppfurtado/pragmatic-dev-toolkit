# Plano — `/init-config` aceitar `paths.backlog: forge`

## Contexto

Gap descoberto pós-v3.4.0 (ADR-058 codificou `paths.backlog: forge` como quarta variante do role `backlog`): o wizard `/init-config` ainda só oferece 3 opções (Canonical/Local/Não usamos) para o role `backlog`, não codifica gravação de `paths.backlog: forge` no YAML, e a sua seção de Cobertura no header declara explicitamente que apenas 3 roles aceitam modo local (sem mencionar forge). Plano `role-backlog-aceitar-forge` (PR #112) tocou as 4 skills consumidoras + procedure + CLAUDE.md + BACKLOG predecessor mas **não tocou `/init-config`** — `/init-config` não consome backlog em runtime, mas precisa gravar a configuração nova.

Operador escolheu **pré-probe** (alternativa (a) cutucada no `/triage`): probe `forge-auto-detect.md` executado no início do passo 3 do wizard; opção `Forge` aparece como disponível se output é `gh`/`glab`, e é omitida com diagnóstico em `no-detection`/`unsupported-host`. UX melhor (operador não pode escolher algo que falha por construção).

**Linha do backlog:** plugin: estender `/init-config` wizard para suportar `paths.backlog: forge` (4ª variante do role backlog per ADR-058) — pré-probe via forge-auto-detect; revisão da Cobertura no header

**ADRs candidatos:** ADR-058 (decisão central de paths.backlog: forge — § (a) schema, § (b) recorte, § (d) policy do caller, § (i) coexistência), ADR-047 (família paths.<role>: <modo> + recusa cross-mode `backlog: local + plans_dir: canonical`), ADR-046 (cutucada de descoberta — `/init-config` define o bloco em vez de consumir, sem alteração).

## Resumo da mudança

Implementa quarta variante do role `backlog` no wizard interativo `/init-config`. **Entra:**

- Pré-probe via `forge-auto-detect.md` no início do passo 3 (antes de perguntar role `backlog`).
- Tabela §3 linha `backlog` ganha 4ª opção `Forge` com `description` carregando trade-off (issues abertas sem assignee via gh/glab; mutações remotas com cutucada). Probe `no-detection`/`unsupported-host` → opção omitida.
- §4 estratégia de composição ganha bullet para `forge`: grava `paths.backlog: forge`.
- Header `## Cobertura`: atualizado para refletir que `backlog` agora aceita 4 modos (3 com local + 1 com forge) e o conjunto canonical/local/null preservado para `decisions_dir` e `plans_dir`.
- §5 (Informar interações pendentes): nova linha quando operador escolheu `Forge` informando que primeira invocação de skill consumidora (`/next`, `/triage` step 4, `/run-plan §3.4`, `/curate-backlog`) executará probe e poderá falhar com erro explícito se setup mudar (CLI desinstalada, repo movido para Bitbucket etc.).

**Fica de fora (v1):**

- Não pré-probar quando bloco config existente já declara `paths.backlog: forge` no passo 2 (`Editar` mantém valor atual mas re-pergunta — probe acontece normalmente; se setup mudou, opção Forge fica omitida e operador escolhe outra).
- Sem nova regra de recusa cross-mode — combinações com `paths.backlog: forge` são todas válidas v1 per ADR-058 § (i); recusa existente (`backlog: local + plans_dir: canonical`) preservada inalterada.
- §4.5 (replicação `.worktreeinclude`) materialmente inalterado — modo forge não dispara replicação `.claude/` (sem store local, paralelo a canonical); apenas nota anti-drift adicionada.
- Sem mudança no critério de disparo da cutucada de descoberta (ADR-046) — `/init-config` continua não emitindo (define o bloco em vez de consumir).

**Alternativa rebatida (opção disabled com diagnóstico inline vs omissão silente):** considerada `Forge (gh não detectado — gh auth login)` apresentada visualmente mas desabilitada para seleção. Descartada — wizard enxuto + ADR-058 § (d) policy do caller cobre diagnóstico no momento que a skill consumidora invocar, sem antecipar setup que operador talvez não queira nunca. Operador buscando Forge em ambiente sem CLI vê opção ausente, infere setup faltante, instala CLI e re-roda `/init-config` — mesmo loop que outras opções condicionais.

## Arquivos a alterar

### Bloco 1 — `/init-config` SKILL.md com modo forge para role backlog {reviewer: code}

- `skills/init-config/SKILL.md`:
  - **Header `## Cobertura`** (após `# init-config`): atualizar contagem para refletir que `backlog` aceita 4 modos (canonical/local/null/forge). Texto sugerido: substituir "5 roles — `decisions_dir`, `backlog`, `plans_dir` (aceitam local mode per [ADR-047](...)), `test_command` (top-level no schema) e `ubiquitous_language` (informational; sem local mode)" por "5 roles — `decisions_dir`, `backlog`, `plans_dir` (aceitam local mode per [ADR-047](...); `backlog` adicionalmente aceita forge mode per [ADR-058](docs/decisions/ADR-058-role-backlog-aceitar-forge.md)), `test_command` (top-level no schema) e `ubiquitous_language` (informational; sem local mode)".
  - **§3 Probe pré-pergunta** (antes da tabela de perguntas per role): adicionar subseção `### 3.0. Pré-probe do forge (para role backlog)`. Mecânica:
    - **Clause defensiva não-git:** se step 1 sinalizou não-git (precondição `git rev-parse --is-inside-work-tree` falhou), pular pré-probe e tratar `forge_disponivel = false` (paralelo a `unsupported-host`). `forge-auto-detect.md` § Algoritmo bullet 1 (`git remote get-url origin`) lança erro shell em não-git, não retorna output controlado — clause cobre o gap.
    - Caso git válido: seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/forge-auto-detect.md` uma vez no início do passo 3.
    - Registrar `forge_disponivel = true` se output é `gh` ou `glab`; `false` se `no-detection` ou `unsupported-host`.
    - Resultado usado pela pergunta do role `backlog` na tabela §3.
    - Probe é silente (sem reportar ao operador agora — eventual nota emitida no §5 quando operador escolheu Forge).
    - **Convenção de Recommended em modo Editar:** Recommended estático ("Canonical (Recommended)") preservado mesmo quando bloco existente declara modo diferente (passo 2 / `Editar`). Operador re-seleciona ativamente o valor atual. Sem dinâmica de Recommended dependente de estado anterior — aderente a CLAUDE.md → "AskUserQuestion mechanics" ("Recommended só quando default é estatisticamente estável"; estado anterior ≠ default estatístico).
  - **§3 Tabela linha `backlog`**: atualizar opções para 4 (em vez das 3 atuais). Sintaxe (preservando estilo das outras linhas):
    | Role | Header | Opções |
    |---|---|---|
    | `backlog` | `Backlog` | `Canonical` (Recommended) / `Local` / `Forge` (apenas se `forge_disponivel = true`) / `Não usamos` |
    - `description` da nova opção `Forge`: `"backlog vem do forge — issues abertas sem assignee via gh/glab; mutações remotas (criar/fechar issue) precedidas de cutucada AskUserQuestion. Aplica-se a backlog v1 (decisions_dir/plans_dir rejeitam). Identificador interno: '#<número>: <título>'"`. Cross-ref a ADR-058.
    - Se `forge_disponivel = false`: opção `Forge` **omitida** da pergunta (não exibida disabled — keep it simple). Sem cutucada de explicação; nota concisa fica no §5 reportada apenas se operador resultou em Não usamos podendo ter querido forge.
  - **§3 Recusa cross-mode**: regra dura existente (`backlog: local + plans_dir: canonical`) preservada inalterada. Adicionar **frase autônoma após** o parágrafo de recusa com framing categorial (não como exceção parentética dentro da regra). Texto sugerido: `A recusa acima opera sobre modo local (mensageiro **Linha do backlog:** carrega texto privado). Em modo forge, o identificador #<número>: <título> é público por construção; combinações com paths.backlog: forge ficam fora desta recusa (ADR-058 § (i)).` Categoria semântica distinta vs exceção fragiliza menos a regra original.
  - **§4 Estratégia de composição**: adicionar bullet entre os existentes:
    - Operador escolheu **canonical** → omitir chave do YAML.
    - Operador escolheu **local** → incluir `paths.<role>: local`.
    - Operador escolheu **null** → incluir `paths.<role>: null`.
    - **NOVO:** Operador escolheu **forge** (apenas role `backlog`) → incluir `paths.backlog: forge`. Skill subsequente (consume role backlog) executa probe do CLI na primeira invocação per ADR-058 § (d) policy do caller; failure → erro explícito orientando setup.
  - **§4.5 Garantir paths replicados em .worktreeinclude**: critério de disparo (`≥1 role configurada como local OR claude_md_gitignored = true`) preservado. **Adicionar nota explícita anti-drift** ao fim do parágrafo introdutório (antes da tabela): `(Modo forge não dispara replicação — paralelo a canonical, sem store local sob .claude/. Per ADR-058 § (a).)`. 1 linha de prosa paga seu custo bloqueando re-introdução acidental de forge no critério OR em onda futura — design-reviewer auditando edição de §4.5 vê marcador semântico explícito.
  - **§5 Informar interações pendentes**: adicionar bullet quando operador escolheu `Forge` (paralelo aos existentes para CLAUDE.md gitignored e modo local):
    > Modo `forge` declarado em `backlog`. Primeira invocação de skill consumidora (`/next` passo 1, `/triage` step 4, `/run-plan §3.4`, `/curate-backlog`) executa probe via `forge-auto-detect.md` no momento e pode falhar com erro explícito se setup mudar (CLI desinstalada, repo movido para host não suportado, etc.). Cutucada `AskUserQuestion` precede cada mutação remota (criar/fechar issue) por blast radius imediato.
  - **§ O que NÃO fazer**: adicionar bullet de guardrail editorial:
    - Não oferecer opção `Forge` quando pré-probe retorna `no-detection`/`unsupported-host` — operador veria opção que falha por construção; opção omitida é silente, sem cutucada explicativa (mantém wizard enxuto).

## Verificação end-to-end

Critérios objetivos para considerar a mudança válida (inspeção textual; repo sem `make test`).

1. **Cobertura no header atualizada.** `grep -nE "ADR-058|backlog adicionalmente aceita forge" skills/init-config/SKILL.md` retorna ≥1 match na seção `## Cobertura`.

2. **Subseção §3.0 pré-probe presente.** `grep -nE "Pr[eé]-probe do forge|forge_disponivel" skills/init-config/SKILL.md` retorna ≥1 match no contexto de §3.

3. **Tabela §3 linha backlog tem 4ª opção `Forge`.** `grep -nE "^\| ` + "`" + `backlog` + "`" + ` \|" skills/init-config/SKILL.md` localiza a linha; `grep -E "Forge" skills/init-config/SKILL.md` retorna ≥1 match no contexto da tabela.

4. **§4 Estratégia de composição cobre forge.** `grep -nE "paths\.backlog: forge|escolheu \*\*forge\*\*" skills/init-config/SKILL.md` retorna ≥1 match.

5. **Recusa cross-mode preservada + nota sobre forge.** `grep -nE "backlog: local \+ plans_dir: canonical" skills/init-config/SKILL.md` retorna ≥1 match (regra existente intacta); `grep -nE "paths\.backlog: forge.*v[aá]lida|ADR-058 § \(i\)" skills/init-config/SKILL.md` retorna ≥1 match (clarificação anti-drift).

6. **§4.5 inalterado materialmente.** `grep -nE "≥1 role configurada como local|claude_md_gitignored = true" skills/init-config/SKILL.md` retorna 2 matches (critério de disparo original); nenhuma menção a `forge` no critério `OR`.

7. **§5 ganha bullet para modo forge.** `grep -nE "Modo .forge. declarado em .backlog." skills/init-config/SKILL.md` retorna ≥1 match.

8. **`## O que NÃO fazer` ganha bullet sobre opção omitida.** `grep -nE "Forge.*quando pr[eé]-probe.*no-detection" skills/init-config/SKILL.md` retorna ≥1 match.

9. **Anti-regression dos 3 modos existentes na tabela §3 linha backlog.** `grep -E '` + "`Canonical`" + `.*` + "`Local`" + `.*` + "`Forge`" + `.*` + "`Não usamos`" + `' skills/init-config/SKILL.md` retorna ≥1 match — cobertura única confirma que as 4 opções aparecem na mesma linha-tabela (ordem canonical/local/forge/não-usamos) e nenhum modo pré-existente foi removido. Crucial porque a tabela é a única fonte de verdade da pergunta runtime.

## Verificação manual

Cenários para o operador exercitar — toca surface não-determinística (probe contra repo real + parsing de output do forge-auto-detect). Operador tem ambiente TJPA real (GitLab) + repo GitHub pessoal.

### Cenário 1 — `/init-config` em repo GitHub com `gh` disponível

1. Em repo GitHub pessoal sem bloco config existente, invocar `/init-config`.
2. §3.0 pré-probe executa silente; output `gh`.
3. Pergunta do role `backlog` aparece com 4 opções: `Canonical` (Recommended) / `Local` / `Forge` / `Não usamos`.
4. Verificar `description` da opção `Forge` mencionando "issues abertas sem assignee" + "mutações remotas com cutucada AskUserQuestion" + cross-ref a ADR-058.
5. Escolher `Forge` → §4 grava `paths.backlog: forge` no YAML.
6. §5 emite bullet sobre primeira invocação executando probe e cutucada por mutação remota.
7. Confirmar grep no CLAUDE.md retorna `paths.backlog: forge`.

### Cenário 2 — `/init-config` em repo TJPA (GitLab) com `glab` + `jq` disponíveis

1. Em repo TJPA sem bloco config existente, invocar `/init-config`.
2. §3.0 pré-probe executa silente; output `glab`.
3. Mesmas 4 opções aparecem; `Forge` disponível.
4. Escolher `Forge` → mesmo comportamento do Cenário 1.

### Cenário 3 — `/init-config` em repo sem `gh` instalado (host GitHub)

1. Em ambiente sem `gh` no PATH, em repo GitHub, invocar `/init-config`.
2. §3.0 pré-probe executa silente; output `no-detection`.
3. Pergunta do role `backlog` aparece com **3 opções** (sem `Forge`): `Canonical` (Recommended) / `Local` / `Não usamos`.
4. Sem cutucada de explicação sobre opção omitida (wizard enxuto per `## O que NÃO fazer`).
5. Operador escolhe `Canonical` → comportamento canonical preservado.

### Cenário 4 — `/init-config` em repo Bitbucket (host não suportado)

1. Em repo Bitbucket (ou repo sem remote), invocar `/init-config`.
2. §3.0 pré-probe executa silente; output `unsupported-host`.
3. Pergunta do role `backlog` aparece com **3 opções** (sem `Forge`).
4. Mesmo comportamento do Cenário 3.

### Cenário 5 — `/init-config` editando bloco existente com `paths.backlog: forge`

1. Repo com bloco config já contendo `paths.backlog: forge` (configurado em invocação anterior).
2. Invocar `/init-config`; passo 2 detecta marker; mostra bloco atual; cutucada `Editar` / `Cancelar`.
3. Escolher `Editar`. §3.0 pré-probe executa (output `gh` ou `glab` no caso comum).
4. Pergunta do role `backlog` aparece com 4 opções; `Forge` ainda disponível.
5. Verificar se valor atual é destacado/Recommended (decisão editorial: se mostrar valor atual ou sempre default canonical — definir durante implementação).
6. Operador escolhe `Forge` novamente → YAML preservado.
7. Variação: operador muda para `Local` → YAML atualizado com `paths.backlog: local`; §4.5 dispara replicação `.claude/` em `.worktreeinclude` (modo local agora ativo).

### Cenário 6 — Anti-regression: combinações pré-existentes intactas

1. `/init-config` em repo sem CLI forge, escolher `Local` para `backlog` + `Canonical` para `plans_dir` (combinação proibida per ADR-047 § Decisão (c)).
2. Recusa cross-mode dispara com mensagem literal pré-existente.
3. Operador re-executa com combinações suportadas.
4. **Anti-regression:** regra original preservada; combinações com `forge` não foram introduzidas como caso de recusa.

### Cenário 7 — `forge` + `plans_dir: canonical` (combinação válida pós-ADR-058)

1. Em repo com `gh` disponível, invocar `/init-config`; escolher `Forge` para `backlog` + `Canonical` para `plans_dir`.
2. Combinação **não** é recusada (per ADR-058 § (i)).
3. YAML grava `paths.backlog: forge` (com `plans_dir` omitida porque é canonical).
4. Skills consumidoras (`/triage` step 4 caminho-com-plano) gravam `**Linha do backlog:** #<número>: <título>` no plano canonical sem leak (identificador é público).

## Notas operacionais

- **Ordem de implementação:** mudanças no SKILL.md são interdependentes (subseção §3.0 alimenta §3 tabela; §4 consome decisão; §5 reporta). Implementar em ordem cronológica do arquivo (cabeçalho → §3 → §4 → §5 → `## O que NÃO fazer`).
- **NÃO criar opção `Forge` para outros roles** (`decisions_dir`, `plans_dir`, `ubiquitous_language`). ADR-058 restringe forge a `backlog` v1. Operador que precisar de outros roles em forge abre `/triage` para extensão futura — atualização do schema antes do wizard.

## Decisões absorvidas

- § Arquivos a alterar Bloco 1 §3 Recusa cross-mode: reformulado de parêntese-em-regra-de-recusa para frase autônoma com framing categorial ("recusa opera sobre modo local — modo forge é categoria distinta, fora desta recusa") per ADR-058 § (i) (caminho-único; reduz fragilidade do anti-drift).
- § Arquivos a alterar Bloco 1 §3.0: sub-edit explícito materializa convenção de Recommended estático em modo Editar (decisão tática promovida de § Notas operacionais a edit concreto no SKILL.md) (caminho-único; aderente a CLAUDE.md → AskUserQuestion mechanics "Recommended só quando default é estatisticamente estável").
- § Arquivos a alterar Bloco 1 §4.5: nota anti-drift explícita adicionada (`Modo forge não dispara replicação — paralelo a canonical, sem store local sob .claude/. Per ADR-058 § (a).`) em vez de "decisão pendente" (caminho-único; 1 linha bloqueia re-introdução acidental de forge no critério OR em onda futura).
- § Arquivos a alterar Bloco 1 §3.0: clause defensiva não-git adicionada — se step 1 sinalizou não-git, pular pré-probe e tratar `forge_disponivel = false`. Cobre gap onde `forge-auto-detect.md` § Algoritmo bullet 1 (`git remote get-url origin`) lança erro shell em não-git ao invés de retornar output controlado (caminho-único; fronteira empírica do procedure pré-existente).
- § Resumo da mudança Fica de fora (v1): alternativa "opção disabled com diagnóstico inline" rebatida explicitamente — wizard enxuto + policy do caller cobre diagnóstico no momento da skill consumidora invocar (caminho-único; nomeação de alternativa rebatida per philosophy.md).
- § Verificação end-to-end critério 9: regex reformulada para sinal específico (`Canonical.*Local.*Forge.*Não usamos` na mesma linha-tabela) — gate de evidência robusto em vez de regex frágil com backticks escapados (caminho-único).
- § Notas operacionais: removida nota de latência ms (~ms total não distingue; YAGNI editorial) (caminho-único).
