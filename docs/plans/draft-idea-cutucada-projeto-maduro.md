# Plano — `/draft-idea` cutucada condicional em projeto maduro

## Contexto

Erro empírico detectado em 2026-05-15: operador rodou `/draft-idea` no toolkit (versão 2.8.1) com argumento descrevendo feature ("ferramenta de chaveamento de contexto entre sessões CC"), e a skill gravou `IDEA.md` monograficamente sobre a feature — regrediu a discoverability do papel `product_direction`, que segundo CLAUDE.md carrega *"what we're building and why. Product direction"* (direção do projeto inteiro, não direção de feature/iniciativa local).

Causa raiz: ADR-027 estabelece predicado de chaveamento **simples** (presença do `IDEA.md`: `ausente → one-shot full; presente → update seção-a-seção`). Assume tacitamente que `ausente` = "projeto novo, primeira cristalização da direção". Falha em projeto maduro onde `IDEA.md` nunca foi escrito — operador pode estar trazendo feature, não direção.

Decisão central (cutucada nominal-comparativa do `/triage` 2026-05-15 + cutucadas F1-F5 do design-reviewer):

- **Mudar o predicado de chaveamento da skill** de `presença(IDEA.md)` para `(presença(IDEA.md), maturidade(projeto))`. Modo update permanece inalterado; modo one-shot ganha gate de cutucada em projeto maduro (F1=b).
- **Critério mecânico de maturidade**: versão semver ≥ `1.0.0` com **cláusula default-conservadora** — ambiguidade (parse failure, formato não-semver, multi-arquivo divergente, `version_files` ausente/null) cutuca mesmo assim (F2=c; paralelo a ADR-026).
- **Parser de versão**: cobre JSON, TOML, YAML, XML (POM Maven) com recuperação explícita em falha de parse (F5=c+POM).
- **Description em CLAUDE.md universal** (sem caveat sobre critério mecânico) — preserva loose-coupling entre doutrina e mecânica (F3=universal).

**ADRs candidatos:** ADR-027 (sucessor parcial — refinamento do sub-fluxo de presença, com mudança no formato do predicado), ADR-003 (definição do papel `product_direction`).

## Resumo da mudança

1. **Passo 1.5 novo em `skills/draft-idea/SKILL.md`** (Task instrumentada per ADR-010): probe de versão via parser multi-formato (JSON/TOML/YAML/XML), critério ≥1.0.0 com default-conservador em ambiguidade, cutucada via `AskUserQuestion` ("direção-do-projeto" vs "direção-de-feature → /triage") quando maduro detectado **ou** ambiguidade. Resposta "feature → /triage" aborta skill com sugestão. `Other` no enum trata como "Direção do projeto" (default não-abortar). Modo update (`IDEA.md` presente) não dispara o passo 1.5.
2. **Bullet curto em `## O que NÃO fazer`** explicitando que `product_direction` é direção-do-projeto-inteiro, não feature/iniciativa local.
3. **Refinamento da definição do papel `product_direction`** na tabela "The role contract" de `CLAUDE.md` para frase universal (sem caveat sobre critério mecânico).
4. **ADR-031** (sucessor parcial de ADR-027) registra a doutrina nova, liderando com a mudança do predicado de chaveamento como decisão central.

Fora de escopo: alterar template `templates/IDEA.md` (esqueleto continua válido), criar nova skill, ou tocar `/triage`/`/new-adr` (caminhos paralelos não regridem).

## Arquivos a alterar

### Bloco 1 — passo 1.5 e `## O que NÃO fazer` em `skills/draft-idea/SKILL.md` {reviewer: code}

- `skills/draft-idea/SKILL.md`:
  - Inserir seção **`### 1.5 Cutucada condicional em projeto maduro`** entre passo 1 e passo 2. Algoritmo completo abaixo em "Algoritmo do passo 1.5".
  - Atualizar prosa de instrumentação (linha "5 passos substantivos") para **6 passos**, incluindo o 1.5 com lifecycle condicional (`pending` → não-maduro detectado sem ambiguidade: `completed` skip silente | maduro ou ambíguo: `in_progress` → cutucada → `completed`).
  - Em `## O que NÃO fazer`, adicionar bullet curto:
    > Não gravar feature/iniciativa local em `<product_direction>` — esse papel carrega direção do projeto inteiro. Para feature, usar `/triage`.

### Bloco 2 — definição do papel `product_direction` em `CLAUDE.md` {reviewer: code}

- `CLAUDE.md`:
  - Na tabela "The role contract" (seção "## The role contract (load-bearing)"), refinar description da linha `product_direction`:
    - Antes: `What we're building and why. Product direction.`
    - Depois: `Why the project exists and what direction it carries — about the project as a whole, not a feature/initiative within it. Features and local initiatives go through /triage.`
  - Nenhuma outra mudança no CLAUDE.md.

### Bloco 3 — preencher Contexto/Decisão/Consequências em `docs/decisions/ADR-031-*.md` {reviewer: code}

- `docs/decisions/ADR-031-cutucada-condicional-draft-idea-projeto-maduro.md`:
  - `## Contexto`: descrever o problema do predicado simples de ADR-027 e como ele falha em projeto maduro com `IDEA.md` ausente (≈1 parágrafo).
  - `## Decisão`: **liderar com mudança do predicado** de `presença(IDEA.md)` para `(presença, maturidade)`. Bullets descrevendo: critério semver ≥1.0.0 + default-conservador; parser 4 formatos (JSON/TOML/YAML/XML); refinamento da description em CLAUDE.md universal (sem caveat); bullet do `## O que NÃO fazer`.
  - `## Consequências`: trade-offs explícitos. Subseções `### Benefícios` / `### Limitações`. Limitações: cobertura limitada a 4 formatos; 0ver deliberado fica como falso negativo aceito; cutucadas extras em projetos sem `version_files`. Benefícios: regressão desta sessão evitada; gate determinístico em projetos maduros canonical.
  - `## Alternativas consideradas`: alternativas iniciais (cutucada-sempre / cutucada-condicional / só-editorial) + alternativas das cutucadas F1/F2/F3/F5 do design-reviewer com motivos de descarte.

## Algoritmo do passo 1.5

Conteúdo a inserir literalmente em `skills/draft-idea/SKILL.md`:

```markdown
### 1.5 Cutucada condicional em projeto maduro

Após resolver o papel `product_direction` (passo 1) e antes de decidir o modo (passos 2/3). Lifecycle Task condicional: `pending` → `completed` skip silente se não-maduro detectado **sem ambiguidade**, ou → `in_progress` → cutucada → `completed` se maduro **ou ambíguo**.

Modo update (`IDEA.md` presente) não dispara o passo 1.5 — decisão já implicitamente tomada.

1. **Probe de versão.** Resolver `version_files` do bloco `<!-- pragmatic-toolkit:config -->` no `CLAUDE.md`. Para cada arquivo declarado, tentar parsear versão semver por tipo:
   - JSON (`*.json`): campo `version` na raiz.
   - TOML (`*.toml`): campo `version` sob `[project]` ou raiz.
   - YAML (`*.yml`/`*.yaml`): campo `version`.
   - XML (`pom.xml` ou outros XML): elemento `/project/version` (canonical Maven).
   - Outros formatos → não-suportado, cair em ambíguo (não silente).
   - Falha de parse (exception, JSON inválido, syntax error TOML/YAML/XML) → log uma linha (`aviso: falha ao parsear <path>: <erro curto>`), cair em ambíguo.

   Primeiro arquivo com versão parseável bem-sucedida → usar. Multi-arquivo declarado com versões divergentes entre os arquivos parseáveis → ambíguo (não escolher arbitrariamente).

2. **Critério mecânico "projeto maduro":** versão semver `^\d+\.\d+\.\d+` (major.minor.patch) ≥ `1.0.0`. Pré-release (`-alpha`, `-rc`) trata-se como mesma major (`1.0.0-rc1` → maduro).

3. **Decisão de cutucada:**
   - **Não-maduro detectado sem ambiguidade** (versão parseável < 1.0.0): skip cutucada silente, prossegue para modo definido pelo passo 1.
   - **Maduro detectado** (versão parseável ≥ 1.0.0) **OU ambíguo** (formato não-suportado, parse failure, multi-arquivo divergente, `version_files` ausente/null): disparar `AskUserQuestion`:
     - `header`: `Direção`
     - `question`: `O argumento descreve direção do projeto inteiro ou direção de feature/iniciativa dentro do projeto?`
     - Opções:
       - `Direção do projeto` — *Continuar /draft-idea normalmente. IDEA.md descreverá o produto como um todo.*
       - `Direção de feature → /triage` — *Abortar /draft-idea. Feature dentro de projeto maduro é alvo de /triage.*

4. **Tratamento de respostas:**
   - `Direção do projeto` → seguir para passo 2 (interview completo).
   - `Direção de feature → /triage` → abortar skill com relatório: `Direção de feature em projeto maduro vai para /triage. Rode /triage <intenção> para o próximo passo.`
   - `Other` (resposta livre via prosa) → tratar como `Direção do projeto` (default não-abortar; paralelo à cláusula default-conservadora de ADR-026 — dúvida → caminho de menor surpresa). Anotar a resposta literal no contexto inicial do interview do passo 2.
```

## Verificação end-to-end

O projeto não tem suite de testes (`test_command: null`). Validação por inspeção textual:

- `grep -n "1.5 Cutucada condicional" skills/draft-idea/SKILL.md` → 1 match.
- `grep -n "Não gravar feature/iniciativa local" skills/draft-idea/SKILL.md` → 1 match.
- `grep -n "not a feature/initiative" CLAUDE.md` → 1 match na tabela "The role contract".
- `grep -n "presença, maturidade\|presença(IDEA.md), maturidade" docs/decisions/ADR-031-*.md` → ≥1 match (decisão central nomeada).
- `grep -n "default-conservador\|cláusula default" docs/decisions/ADR-031-*.md` → ≥1 match.
- `grep -n "pom.xml\|XML" docs/decisions/ADR-031-*.md skills/draft-idea/SKILL.md` → matches em ambos.

## Verificação manual

Cenários para smoke-test mental e pós-release em consumer real:

1. **Projeto novo sem `version_files` declarado** + arg direção-de-produto → ambíguo (`version_files` ausente) → cutucada dispara, operador responde "Direção do projeto" → interview normal.
2. **Projeto novo com `version_files`, versão 0.3.0** + arg direção-de-produto → não-maduro sem ambiguidade → skip silente, interview normal.
3. **Projeto maduro (versão 2.8.1, caso real desta sessão)** + arg que parece feature → cutucada dispara, operador responde "feature → /triage", skill aborta com mensagem.
4. **Projeto maduro (versão 1.4.0)** + arg direção-de-produto genuína → cutucada dispara, operador responde "Direção do projeto" → interview normal.
5. **Projeto maduro com `IDEA.md` presente** → passo 1.5 não dispara (modo update), operador entra direto em revisão seção-a-seção.
6. **Projeto Maven (`pom.xml`, versão 2.1.0)** → parser XML extrai versão → maduro → cutucada dispara.
7. **Projeto Python (`pyproject.toml`, versão 1.0.0-rc1)** → maduro (pré-release de 1.0.0) → cutucada dispara.
8. **Projeto Node (`package.json`, versão 0.9.0-beta)** → não-maduro sem ambiguidade → skip silente.
9. **Projeto com calver (`2026.05.15` em `version_files`)** → não-semver → ambíguo → cutucada dispara via default-conservador (NÃO skip).
10. **Projeto com 0ver deliberado (Bun-style: `0.7.0`)** → não-maduro sem ambiguidade → skip silente. Falso negativo aceito como design (0ver delib é raro em consumers do toolkit; ADR documenta).
11. **Multi-arquivo divergente** (`pyproject.toml` 1.5.0 + `package.json` 0.9.0) → ambíguo → cutucada dispara.
12. **`version_files` aponta para JSON malformado** → exception, log aviso, ambíguo → cutucada dispara.
13. **Resposta `Other` no enum Direção** → tratado como "Direção do projeto", interview prossegue com resposta literal no contexto.

## Pendências de validação

- Smoke real pós-release em ≥1 consumer maduro (versão semver ≥ 1.0.0) e ≥1 consumer novo, exercitando cenários 3, 4, 6, 9 e 13 acima. Spec para o operador rodar manualmente.

## Notas operacionais

- Ordem dos blocos: 1 (SKILL.md) e 2 (CLAUDE.md) são independentes. Bloco 3 (preencher ADR-031) tem afinidade conceitual com os anteriores mas pode rodar em qualquer ordem.
- ADR-031 já existe como stub (Origem preenchida); Bloco 3 preenche Contexto/Decisão/Consequências.
- O parser do passo 1.5 deve ser **autocontido** na skill (não delegar a `/release`) para evitar acoplamento entre skills.
- Cláusula default-conservadora gera **mais cutucadas** que o plano original — operador em projeto novo sem `version_files` declarado vai ver enum extra na primeira invocação. Trade-off aceito por F2=(c).
