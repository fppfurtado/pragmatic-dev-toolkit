# Plan: qa-reviewer + security-reviewer (generic agents) — v0.3.0

## Contexto

Após o release da v0.2.1, o operador questionou por que `qa-reviewer` e `security-reviewer` — que existem em `h3-finance-agent/.claude/agents/` — ficaram fora do plugin. A justificativa original ("saturados de RN01–RN21, GestaoClick, n8n; tirar isso deixa pouco") não resistiu à releitura: ambos têm **núcleo genérico substancial**; a fração h3-specific é separável.

Diferente de skills e hooks, **agents não geram nem executam código** — só leem diff e reportam. Os princípios que aplicam (cobertura de invariantes, mock vs real, credenciais em logs, validação na fronteira, HTTP timeouts) são universais. Por isso não precisam de sufixo de stack: ambos vão como `qa-reviewer` e `security-reviewer` (sem `-python`).

Critério a codificar em `docs/philosophy.md`: **gera ou executa = força sufixo; revisa princípios = não força**.

Mudança 100% aditiva — surface de v0.2.x intacta.

## Resumo da mudança

1. **Agent `qa-reviewer`** — lift de `h3-finance-agent/.claude/agents/qa-reviewer.md` com drop de project framing e exemplos h3-specific.
2. **Agent `security-reviewer`** — lift de `h3-finance-agent/.claude/agents/security-reviewer.md` com a mesma operação.
3. **`docs/philosophy.md`**: nova linha de Agent na tabela de naming convention + parágrafo curto explicando o critério.
4. **`README.md`**: tabela de componentes ganha duas linhas.
5. **`docs/install.md`**: seção "Validação" ganha invocação smoke dos dois agents.
6. **`CHANGELOG.md`**: entrada `## [0.3.0]`.
7. **Bumps**: `plugin.json` + `marketplace.json` para `0.3.0`; `description` ganha menção a QA/security reviewers.
8. **Tag `v0.3.0`** após smoke verde.

## Pré-condição (smoke do shadowing) — bloqueante

A estratégia inteira depende de `.claude/agents/<nome>.md` no projeto consumidor (h3) ter precedência sobre o agent homônimo do plugin quando há colisão de nome. Se não tiver, instalar o plugin em h3 ofuscaria as versões h3-rich e regrediria a experiência.

Smoke a fazer **antes** de implementar a v0.3:

1. Instalar o plugin em h3 via marketplace (`/plugin marketplace add fppfurtado/pragmatic-dev-toolkit` + `/plugin install pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit`). v0.2.1 já está publicada.
2. Forçar invocação que exercite `code-reviewer` (já há colisão de nome com `h3-finance-agent/.claude/agents/code-reviewer.md`). Diff sintético com factory sobre-abstraída e pedir review.
3. Confirmar empiricamente qual versão executou: o `code-reviewer` do h3 menciona "GestaoClick", "MovimentoFinanceiro", `infra/n8n/`; o do plugin não. O conteúdo do report deixa óbvio qual venceu.

**Resultado esperado:** project-level wins. Se confirmar → seguir o plano como descrito.
**Se plugin wins:** pivot — renomear no plugin para `qa-reviewer-pragmatic` e `security-reviewer-pragmatic` para evitar colisão. O operador escolhe explicitamente qual invocar via `{revisor: ...}` no plano. Plano permanece, só mudam os nomes dos arquivos e referências.

## Arquivos a alterar

### Bloco 1 — qa-reviewer agent {revisor: code}

- **`agents/qa-reviewer.md`** (novo).
  - Frontmatter: `name: qa-reviewer`. Description: "Revisor de qualidade de testes focado em cobertura de invariantes documentadas, edge cases declarados e separação mock-vs-real. Acionar antes de PR para verificar se a mudança tem testes alinhados."
  - **Manter** verbatim os 4 buckets do original (caminho feliz / invariantes / edge cases / mock vs real) e a seção "Como reportar".
  - **Generalizar:**
    - Mapa "Módulo → RNs" → "Quando o diff toca lógica que exerce invariantes documentadas em `docs/domain.md` (RNxx ou equivalentes), verifique cobertura para cada uma — tanto satisfeita quanto violada."
    - "Padrões esperados" → "Unit: rápido, sem I/O. Integration: marker correspondente da stack do projeto. Camada de persistência (DB) NÃO mockada — usar arquivo temporário/`tmp_path`/equivalente. Datas explícitas (parâmetros), não relógio do sistema." Sem citar `respx`/`asyncio_mode` — esses ficam no `gen-tests-python`.
    - Edge cases nominais (Conciliação/OFX/Bot/n8n) → "Cobrir edge cases que o diff/código alvo trata explicitamente (raises, branches de erro), e os declarados em `docs/design.md` quando relevantes."
    - "Mock vs real" → "Camada de persistência mockada em integration → bug clássico (mock/prod divergence). HTTP externo: usar a ferramenta de mock idiomática da stack, não bibliotecas genéricas tipo `unittest.mock`."

### Bloco 2 — security-reviewer agent {revisor: code}

- **`agents/security-reviewer.md`** (novo).
  - Frontmatter: `name: security-reviewer`. Description: "Revisor de segurança focado em credenciais, validação de entrada, chamadas HTTP externas, dados sensíveis e invariantes documentadas em ADRs. Acionar antes de PR quando a mudança envolver tokens, handlers de fronteira ou persistência de dados sensíveis."
  - **Manter** verbatim os 5 buckets (credenciais, validação de entrada, HTTP externo, dados sensíveis, invariantes pós-erro) e "Como reportar".
  - **Generalizar:**
    - Tokens nominais (`GESTAOCLICK_ACCESS_TOKEN`, `P06_N8N_BEARER_TOKEN`, `TELEGRAM_BOT_TOKEN`...) → "tokens declarados em `.env.example` do projeto". Princípios (não vazar em log, sem hardcode, headers vs URL) preservados.
    - Exemplos de "Validação de entrada" h3-specific (`TELEGRAM_ALLOWED_CHAT_IDS`, FITID OFX, ids GestaoClick) → "validação na fronteira (HTTP/CLI/parser/mensagem) antes de efeitos laterais; limites de tamanho declarados; identificadores externos parametrizados em SQL".
    - "Chamadas HTTP externas": **manter verbatim** (httpx-agnóstico já é genérico).
    - "Dados financeiros" → renomear para "Dados sensíveis": "Dados sensíveis declarados no domínio do projeto (PII, identificadores fiscais, valores monetários, credenciais de terceiros) — não expor em mensagens de erro / logs / respostas HTTP sem necessidade."
    - "Estado local Conciliado" + ADR-004 → "Invariantes pós-erro documentadas em ADRs: ADRs que definem comportamento de rollback, retry com efeito colateral, ou divergência entre estado local e externo. Verificar se o diff respeita essas invariantes."

### Bloco 3 — docs {revisor: code}

- **`docs/philosophy.md`** (edit).
  - Adicionar linha na tabela de "Convenção de naming":

    | Tipo | Genérico | Stack-specific |
    |---|---|---|
    | Agent (frontmatter `name`) | `<role>` (ex.: `code-reviewer`, `qa-reviewer`, `security-reviewer`) | `<role>-<stack>` (apenas se princípios mudarem com a stack) |

  - Adicionar parágrafo curto: "Componentes que **geram ou executam** algo da stack (skills geradoras de código, hooks que invocam toolchain) precisam de sufixo — sintaxe ou comando concreto não tem versão neutra. Componentes que **revisam princípios** lidos do diff não precisam — o stack está no próprio diff."
- **`README.md`** (edit).
  - Tabela de componentes ganha duas linhas:
    - `qa-reviewer` (Agent) — princípios de cobertura de testes.
    - `security-reviewer` (Agent) — credenciais, HTTP, dados sensíveis, invariantes em ADRs.
- **`docs/install.md`** (edit).
  - Seção "Validação" ganha:
    - "Invocar `qa-reviewer` num diff que adiciona função pública sem teste correspondente → flag esperado."
    - "Invocar `security-reviewer` num diff que loga um valor de variável de ambiente em mensagem de erro → flag esperado."

### Bloco 4 — versionamento {revisor: code}

- **`.claude-plugin/plugin.json`** (edit) — `version: "0.3.0"`. Atualizar `description`: "...workflow skills (/new-feature, /new-adr, /run-plan), Python testing skill (/gen-tests-python), **YAGNI/QA/security reviewers**, and self-gated hooks...". Manter keywords (já incluem `code-review`).
- **`.claude-plugin/marketplace.json`** (edit) — `version: "0.3.0"`. Atualizar `description` no item de plugin de modo análogo.
- **`CHANGELOG.md`** (edit) — adiciona acima de `[0.2.1]`:

  ```markdown
  ## [0.3.0] - <YYYY-MM-DD>

  ### Added
  - Agent: `qa-reviewer` — princípios de cobertura de testes (caminho feliz, invariantes, edge cases, mock vs real). Stack-agnóstico.
  - Agent: `security-reviewer` — credenciais, validação de entrada, HTTP externo, dados sensíveis, invariantes em ADRs. Stack-agnóstico.
  - Naming convention para agents documentada em `docs/philosophy.md` (critério: gera/executa = força sufixo; revisa princípios = não força).
  ```

### Bloco 5 — release manual

- Direto na `main` em micro-commits Conventional Commits (um por bloco), mesma disciplina das v0.2 e v0.2.1.
- `git tag v0.3.0 -m "v0.3: qa-reviewer + security-reviewer (generic agents)"` + `git push origin v0.3.0`.

## Verificação end-to-end

1. **Pré-condição passou** (ver seção acima): project-level shadowing confirmado em smoke prévio. Sem isso, o plano não roda.
2. JSONs parseiam: `python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))"` (e `marketplace.json`, `hooks.json`).
3. Frontmatter sanity: ambos `agents/{qa-reviewer,security-reviewer}.md` com `name:` e `description:` válidos.
4. **Drift check h3-isms** — nenhum dos novos arquivos do plugin pode mencionar termos project-specific:

   ```bash
   for f in agents/qa-reviewer.md agents/security-reviewer.md; do
     grep -nE 'GestaoClick|n8n|Telegram|Conciliação|Conciliado|ADR-004|RN0[0-9]|FITID|MovimentoFinanceiro' "$f" \
       && echo "DRIFT in $f" || echo "$f clean"
   done
   ```
5. `git diff --stat` mostra apenas os blocos esperados (sem drift fora do escopo).

## Verificação manual

Necessária — agents só fazem sentido em contexto real.

1. `/plugin marketplace update` + reinstall em projeto com v0.2.x → confirmar v0.3.0 carregada.
2. `/plugin list` lista ambos `qa-reviewer` e `security-reviewer`.
3. Invocar `qa-reviewer` num diff sintético que adiciona função pública sem teste → flag de "caminho feliz sem teste".
4. Invocar `qa-reviewer` num diff que mocka camada de DB em integration → flag de "mock vs real".
5. Invocar `security-reviewer` num diff que faz `logger.info(f"token={token}")` → flag de "credencial em log".
6. Invocar `security-reviewer` num diff de handler que faz I/O externo antes de validar input → flag de "validação na fronteira".
7. Em h3 (com o agent project-level rico ainda presente), confirmar que `/run-plan` num bloco `{revisor: qa}` invoca a versão **h3-rich** (que menciona GestaoClick/RNxx), não a do plugin. Mesma checagem para `{revisor: security}`.

Sem confirmação dos passos 1–7, não fechar o release.

## Notas operacionais

- **Por que sem sufixo de stack.** Reviewers lêem o diff e aplicam princípios; o stack está no diff. Skills geradoras (`gen-tests-python`) e hooks executores (`run_pytest_python`) precisam de sufixo porque produzem/operam em sintaxe específica. Critério agora codificado em `docs/philosophy.md`.
- **Coexistência com versões h3-rich.** O h3 mantém `.claude/agents/{qa-reviewer,security-reviewer}.md` próprios (com mapa RN, GestaoClick, n8n) — funcionam como **extensões shadowing** da versão genérica do plugin. Para projetos novos sem essa riqueza, a versão do plugin é o baseline.
- **Drift risk.** Quando o `qa-reviewer` rico do h3 evoluir, o plugin não acompanha sozinho. Se um pattern h3-specific virar útil em outros projetos, é candidato a promover ao plugin via novo PR — mesma regra "drop o que é específico, mantém o princípio".
- **Próxima evolução natural.** Quando aparecer agent stack-locked legítimo (ex.: `lint-reviewer-python` que aplica regras `ruff` específicas, ou `migration-reviewer-django` que conhece Django ORM), o sufixo entra. Para reviewers de princípios genéricos, manter sem sufixo.
