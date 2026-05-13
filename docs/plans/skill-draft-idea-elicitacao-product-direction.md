# Plano — Skill /draft-idea para elicitação estruturada de IDEA.md

## Contexto

Implementa [ADR-027](../decisions/ADR-027-skill-draft-idea-elicitacao-product-direction.md). Adiciona ao toolkit a skill `/draft-idea`, geradora de `IDEA.md` (papel `product_direction`) via elicitação estruturada multi-turn. Skill opera upstream de `/triage` — quando o operador chega com ideia vaga (sem problema bem-definido, sem persona, sem critérios), `/draft-idea` conduz interview cobrindo problema, persona, restrições, critérios de sucesso e alternativas descartadas, e cristaliza o resultado em `IDEA.md`.

Modo de operação:

- `IDEA.md` ausente → one-shot full (interview completo do zero).
- `IDEA.md` presente → update seção-a-seção (operador escolhe quais seções revisar via enum).

**ADRs candidatos:** ADR-027 (decisão principal), ADR-008 (stack-agnóstica), ADR-023 (`disable-model-invocation: false`), ADR-003 (frontmatter `roles`), ADR-017 (cutucada de descoberta), ADR-010 (instrumentação de Tasks em skill multi-passo), ADR-005 (papel `product_direction` informational nas demais skills).

**Linha do backlog:** Skill `/draft-idea` para elicitação estruturada de `IDEA.md` (papel `product_direction`) com modo dual one-shot/update.

## Resumo da mudança

- **Nova skill** `skills/draft-idea/SKILL.md` com elicitação multi-turn, modo dual probe + (one-shot / update), sugestão de `/triage` no fim, instrumentação de progresso via Tasks.
- **Novo template** `templates/IDEA.md` — skeleton canônico do artefato (problema / persona / restrições / critérios / alternativas), consumido pela skill em modo one-shot e referência para o operador em modo update.
- **Edits a `CLAUDE.md`** — adicionar `/draft-idea` à lista de slash commands em "Plugin layout" e ao escopo da "Cutucada de descoberta" (skill declara `roles.required: [product_direction]`).
- Sem edits a `skills/triage/SKILL.md` — fronteira semântica é registrada apenas no ADR-027 e na descrição das duas skills; `/triage` não precisa detectar vaguidade e redirecionar.

**Decisões-chave** (todas em ADR-027):
- Naming `/draft-idea` (alinhado a `IDEA.md`).
- Sugerir `/triage` ao final.
- Stack-agnóstica.
- `disable-model-invocation: false`.

## Arquivos a alterar

### Bloco 1 — Template IDEA.md {reviewer: code}

- `templates/IDEA.md` (novo): skeleton em PT-BR canonical com 5 seções (problema, persona/usuário, restrições, critérios de sucesso, alternativas descartadas), cada uma com um comentário HTML descrevendo o que vai ali (paralelo a `templates/plan.md`). Skill copia/preenche; operador pode também usar como referência manual.

### Bloco 2 — Skill SKILL.md {reviewer: code}

- `skills/draft-idea/SKILL.md` (novo):
  - Frontmatter: `name: draft-idea`, `description`, `disable-model-invocation: false`, `roles.required: [product_direction]`.
  - **Sub-fluxo de presença (variante da track "Oferecer criação canonical" do ADR-003).** `/new-adr` usa a mesma track: required ausente → cria via enum. `/draft-idea` estende a variante: presença determina **modo** (não cancela operação).
    - `<product_direction>` ausente → modo **one-shot full** (skill cria o artefato).
    - `<product_direction>` presente → modo **update seção-a-seção** (skill edita o artefato existente).
  - Passos (instrumentação via Tasks conforme ADR-010, dado >3 passos substantivos):
    1. **Resolver papel `product_direction`** e decidir modo conforme sub-fluxo acima.
    2. **Modo one-shot:** conduzir interview multi-turn. **Perguntas vivem na prosa deste passo do SKILL.md** (não em comentários HTML do template — `templates/IDEA.md` é puro esqueleto, paralelo a `templates/plan.md`). Perguntas dirigidas para problema (prosa livre), persona/usuário (prosa livre), restrições (enum multi-select de categorias comuns + Other), critérios de sucesso (prosa livre, ≥1 critério), alternativas descartadas (prosa livre, opcional). Tom: estruturador, não inquisidor.
    3. **Modo update:** enum (`AskUserQuestion`) listando as 5 seções como multi-select; reconduzir elicitação só nas escolhidas; preservar conteúdo intacto das demais.
    4. **Síntese:** preencher `templates/IDEA.md` (lê o esqueleto canônico via `${CLAUDE_PLUGIN_ROOT}/templates/IDEA.md`) com respostas coletadas; gravar em `<product_direction>` resolvido. Idioma: espelhar projeto consumidor (default canonical PT-BR per philosophy.md).
    5. **Relatório.** Ordem fixa, três linhas potenciais:
       1. Path do arquivo gravado.
       2. Sugestão de próximo passo: `próximo passo: /triage <intenção concreta>`.
       3. Cutucada de descoberta per ADR-017 — **última linha** quando triple gating satisfeito (per ADR-017 § Decisão: "emit as the last line of the report").
  - Seção `## Argumentos`: input opcional (ideia em frase curta). Vazio → skill pede no início.
  - Seção `## O que NÃO fazer`:
    - Não inventar conteúdo — operador é a fonte; skill estrutura, não preenche por conta própria.
    - Não fazer interview exaustivo — ≤2 perguntas por seção, depois prosseguir.
    - Não detectar inconsistências cross-seção (limitação registrada em ADR-027 § Consequências).
    - Não invocar `/triage` automaticamente — só sugere; operador é quem dispara.

### Bloco 3 — CLAUDE.md edits {reviewer: doc}

- `CLAUDE.md`:
  - Seção "Plugin layout" → lista de slash commands: incluir `/draft-idea` na enumeração de skills.
  - Seção "Cutucada de descoberta" → "Scope: 4 skills" vira "Scope: 5 skills" (adicionar `/draft-idea` à lista de skills que declaram `roles.required` e emitem a cutucada).
  - Sem outras edits — papel `product_direction` já está documentado na role contract; ADR-005 segue válido (não é revogado, apenas estendido).

## Verificação end-to-end

Repo sem suite de teste (`test_command: null` per `CLAUDE.md` → "Pragmatic Toolkit"). Validação por inspeção textual + smoke test em consumer project.

Comandos de inspeção (executar após implementação):

```bash
# Frontmatter e estrutura da skill
grep -E '^name: draft-idea$' skills/draft-idea/SKILL.md
grep -E '^disable-model-invocation: false$' skills/draft-idea/SKILL.md
grep -E '^  required: \[product_direction\]' skills/draft-idea/SKILL.md
grep -E '^## O que NÃO fazer$' skills/draft-idea/SKILL.md

# Template existe e tem as 5 seções
test -f templates/IDEA.md
grep -cE '^## ' templates/IDEA.md  # esperado: 5

# CLAUDE.md referencia a skill
grep -c '/draft-idea' CLAUDE.md  # esperado: ≥2 (Plugin layout + Cutucada de descoberta)
grep -E 'Scope:\*\* 5 skills' CLAUDE.md  # cutucada atualizada
```

## Verificação manual

Surface não-determinística (LLM elicitando prosa). Cenários enumerados:

**Formato de input real esperado** (ideia vaga em PT-BR, frase curta-a-média):
- `"uma ferramenta pra ajudar com brainstorm na hora de propor features"`
- `"sistema pra gerenciar membros e mensalidades de um clube"`
- `"alguma coisa pra estudar idioma melhor sem ficar preso em Anki"`

**Cenário 1 — One-shot, IDEA.md ausente.**
- Setup: consumer project sem `IDEA.md`. `/plugin install /storage/3. Resources/Projects/h3/pragmatic-dev-toolkit --scope project` aplicado.
- Ação: `/draft-idea "uma ferramenta pra ajudar com brainstorm de features"`.
- Esperado: skill detecta ausência, entra modo one-shot, conduz interview cobrindo as 5 seções (≤2 perguntas por seção), grava `IDEA.md` no path canonical com estrutura preenchida, sugere `/triage <intenção concreta>` ao final.
- Verificar: arquivo criado; cada seção do template populada com conteúdo do interview; idioma PT-BR; nada inventado além do que o operador respondeu.

**Cenário 2 — Update seção-a-seção, IDEA.md existente.**
- Setup: consumer project com `IDEA.md` populado (do Cenário 1).
- Ação: `/draft-idea` (sem argumento; operador quer refinar).
- Esperado: skill detecta presença, oferece enum multi-select listando as 5 seções, operador escolhe (ex.) `Restrições` e `Critérios de sucesso`; skill recoduz interview só nessas, preserva problema/persona/alternativas intactos.
- Verificar: arquivo atualizado; seções não-escolhidas idênticas ao estado prévio; seções escolhidas atualizadas com novo conteúdo.

**Cenário 3 — Operador escapa para prosa livre via "Other".**
- Setup: rodando interview do Cenário 1.
- Ação: na pergunta de "Restrições" (enum multi-select de categorias), escolher `Other` e digitar restrição customizada.
- Esperado: skill aceita prosa livre como restrição, integra na seção, segue para próximo passo.
- Verificar: `IDEA.md` final inclui a restrição customizada literalmente; sem perda de informação.

**Cenário 4 — Cutucada de descoberta.**
- Setup: consumer project sem `<!-- pragmatic-toolkit:config -->` em `CLAUDE.md` (ou sem `CLAUDE.md`).
- Ação: rodar `/draft-idea` qualquer cenário.
- Esperado: relatório final inclui a string canonical da cutucada (per ADR-017).
- Verificar: última linha do relatório bate exatamente com a string de ADR-017.

**Cenário 5 — Update + escape via "Other" (gatilho de revisão #1 do ADR-027).**
- Setup: consumer project com `IDEA.md` existente.
- Ação: rodar `/draft-idea`; no enum multi-select de seções, escolher só `Restrições`; dentro da elicitação de Restrições, escolher `Other` no enum de categorias e digitar restrição customizada em prosa livre.
- Esperado: skill integra prosa livre como restrição, atualiza só a seção `Restrições`, demais seções intactas.
- Verificar: `IDEA.md` final tem `Restrições` com a prosa livre integrada literalmente; problema, persona, critérios, alternativas idênticos ao estado prévio. Se >50% dos updates reais convergirem para "Other" em várias seções, gatilho de revisão #1 do ADR-027 dispara.

## Notas operacionais

- **Modo update sem inconsistência cross-seção:** limitação documentada em ADR-027; não é gap deste plano. Operador é responsável pela coerência ao concluir um update parcial.
- **Smoke test no toolkit:** o próprio toolkit não usa `IDEA.md` (papel informational ausente, sem config block). Validação manual exige consumer project — `scaffold-kit` ou projeto pessoal serve.
