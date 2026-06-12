# Refatorar philosophy.md para princípios apenas

## Contexto

philosophy.md cresceu de "princípios e guidelines" para "manual operacional do toolkit" — 18 seções, ~4170 palavras. Boa parte é mecânica (Resolução de papéis passo-a-passo, schema do bloco de config, ciclo de vida do backlog, consolidação, classificação de capturas, anotação de revisor, cobertura de teste, `.worktreeinclude`) que tem dono real noutro lugar (skill ou CLAUDE.md) mas mora em philosophy.md por inércia. O documento é referenciado por todas as skills via `(ver docs/philosophy.md → X)` — cada referência é convite a Read no arquivo de 4170 palavras. Input recorrente alto, mecânicas com múltiplos donos (drift entre fontes), e philosophy.md virou vítima do que prega.

Após os passos B+C de compactação, várias skills já têm mecânicas inline (ciclo de vida do backlog em `/triage` e `/run-plan`; cobertura de teste em `/triage`; classificação de capturas em `/run-plan`); a migração agora é: (a) absorver nos destinos os passos-a-passo restantes que ainda moram só em philosophy.md; (b) cortar o conteúdo migrado em philosophy.md, deixando apenas princípios.

**Linha do backlog:** philosophy.md: refatorar para conter apenas princípios; migrar mecânicas para os consumidores reais (skills/CLAUDE.md/README)

## Resumo da mudança

**philosophy.md mantém** apenas princípios (8 seções):

- A filosofia em uma frase
- Nomear bifurcações arquiteturais
- Path contract (tabela conceitual + 1 frase de resolução pointing CLAUDE.md)
- Convenção de naming
- Convenção de idioma
- Convenção de commits
- Convenção de pergunta ao operador
- Linguagem ubíqua na implementação (pipeline em forma curta)

**philosophy.md migra** para destino consumidor:

| Seção atual | Destino |
| --- | --- |
| Resolução de papéis (passo-a-passo) | CLAUDE.md (sob "The role contract") |
| Bloco de configuração no CLAUDE.md (schema YAML) | CLAUDE.md (auto-canonical) |
| Anotação de revisor em planos (schema completo) | `/triage` passo 4 + `/run-plan` passo 3 inline |
| Cobertura de teste em planos | `/triage` (heurística já inline; reforçar critério `{reviewer: qa}`) |
| Ciclo de vida do backlog | `/triage` (transição inicial) + `/run-plan` (transição final) inline |
| Consolidação do backlog | `/triage` passo 5 + `/run-plan` passo 4.5 inline |
| Classificação de capturas automáticas | `/run-plan` passo 4.5 (único consumidor) |
| Convenção `.worktreeinclude` | `/run-plan` passo 1.2 |
| Companion | README |

Alvo: philosophy.md ~4170 → ~1700 palavras (−59%).

Estratégia: **absorver primeiro nos destinos (blocos 1-4); substituir referências órfãs (bloco 5); cortar philosophy.md por último (bloco 6)**. Evita janela em que mecânicas ficam só em philosophy.md durante a transição.

## Arquivos a alterar

### Bloco 1 — CLAUDE.md absorve Resolução de papéis + Bloco de configuração

CLAUDE.md já tem versão resumida do role contract (3 linhas) e o bloco YAML de config. Absorver de philosophy.md:

- **Protocolo de Resolução de papéis** (4 passos: probe canonical → consultar bloco no CLAUDE.md → perguntar ao operador tri-state → oferta única de memorização). Inserir como subseção sob "The role contract (load-bearing)".
- **Drift detection** (canonical existe E config diferente → flagga inconsistência).
- **Distinção papel obrigatório vs informacional** (lista por skill).
- **Schema do bloco `<!-- pragmatic-toolkit:config -->`**: chaves reservadas, semântica de chave ausente / `null` / chaves desconhecidas, marcador HTML obrigatório. Manter inline com o exemplo YAML já presente.

Cortar a referência `(ver docs/philosophy.md → "Resolução de papéis")` em "The role contract" — protocolo agora mora aqui.

### Bloco 2 — /triage absorve Anotação de revisor + Consolidação do backlog

Skill já tem ciclo de vida do backlog e cobertura de teste inline (passo B+C). Absorver de philosophy.md:

- **Anotação de revisor em planos (schema completo)**: perfis válidos (`code|qa|security`), múltiplos perfis (`code,qa,security`), default `code` sem anotação, exemplo canônico. Inserir no passo 4 (onde a anotação é decidida pelo planner).
- **Consolidação do backlog (mecânica passo-a-passo)**: reler arquivo após edits → flagar duplicatas e obsolescência → sem flags = skip silente; com flags = enum `Backlog` (header curto, opções `Está bom, prosseguir` / `Aplicar edits`; Other → operador descreve em prosa). Inserir no passo 5 (onde já é referenciada).

Substituir as referências `(ver docs/philosophy.md → ...)` correspondentes pelos blocos inline.

### Bloco 3 — /run-plan absorve Anotação de revisor + Consolidação + .worktreeinclude

Skill já tem classificação de capturas e ciclo de vida inline (passo B+C). Absorver de philosophy.md:

- **Anotação de revisor em planos** (resumo operacional curto, não duplicar palavra-a-palavra com /triage; pode-se usar referência interna `ver /triage SKILL → passo 4 sobre {reviewer:}`). Inserir no passo 3.3 (onde a anotação é lida).
- **Consolidação do backlog** (mesmo conteúdo do bloco 2; preferência: inline curto no passo 4.5; alternativa: referência interna ao /triage). Decidir na execução qual fica mais limpo dado o tom da skill.
- **Convenção `.worktreeinclude`** (formato: 1 path por linha, `#` para comentário, globs são roadmap; mecânica de leitura/cópia). Inserir/expandir no passo 1.2 (onde o arquivo é lido). Skill já tem parte; absorver o que falta de philosophy.md.

Substituir referências cruzadas correspondentes.

### Bloco 4 — README absorve Companion

README já tem seção "Companion" com referência ao scaffold-kit. Absorver o detalhe de philosophy.md sobre desacoplamento ("você pode usar um sem o outro, mas a sinergia é clara: bootstrap com scaffold-kit, automação com este plugin"). Edit cirúrgico — no máximo 2 frases adicionadas.

### Bloco 5 — Substituir referências órfãs nas skills

Após blocos 1-4, varrer skills/agents para referências cross-ref que ainda apontam para philosophy.md em mecânica que migrou. Substituir por destino correto:

- `Resolução de papéis` → `CLAUDE.md → "The role contract"` ou inline curto onde já não polui.
- `Anotação de revisor em planos` → já absorvido em blocos 2-3; remover referências externas remanescentes.
- `Ciclo de vida do backlog` → já inline (passo B+C); remover referências externas.
- `Consolidação do backlog` → já absorvido em blocos 2-3; remover externas.
- `Classificação de capturas automáticas` → /run-plan interna; remover externas (qa-reviewer, security-reviewer agents podem ter referências).
- `Cobertura de teste em planos` → /triage interna (heurística inline); remover externas.
- `Convenção .worktreeinclude` → /run-plan interna; remover externas.

Caça mecânica via `grep -r 'docs/philosophy.md →' skills/ agents/ CLAUDE.md README.md docs/install.md` listando todos os pointers; cada pointer para mecânica migrada vira inline ou desaparece.

### Bloco 6 — philosophy.md: cortar mecânicas, reter princípios

Reescrever philosophy.md preservando exclusivamente:

- **Frase-tese** (1 parágrafo abertura).
- **Nomear bifurcações arquiteturais** (princípio + crítica de inércia + verbos-abertos sintoma; modo de coleta enum `AskUserQuestion`).
- **Path contract** (tabela de papéis + 1 frase: "Resolução de cada papel: protocolo em CLAUDE.md → 'The role contract'").
- **Convenção de naming** (tabela de tipos; auto-gating triple para hooks; rationale).
- **Convenção de idioma** (princípio + critério mecânico ≥70%; default canonical PT-BR; hooks são exceção).
- **Convenção de commits** (princípio + 3 níveis curtos).
- **Convenção de pergunta ao operador** (princípio enum vs prosa; quando NÃO perguntar valor único derivado).
- **Linguagem ubíqua na implementação** (princípio + pipeline 3 estágios em forma curta; quando silencia).

Cortar inteiramente:

- Resolução de papéis → migrou para CLAUDE.md (bloco 1)
- Bloco de configuração no CLAUDE.md → migrou para CLAUDE.md (bloco 1)
- Anotação de revisor em planos → migrou para skills (blocos 2-3)
- Cobertura de teste em planos → migrou para /triage
- Ciclo de vida do backlog → migrou para skills (B+C + bloco 5)
- Consolidação do backlog → migrou para skills (blocos 2-3)
- Classificação de capturas automáticas → migrou para /run-plan
- Convenção `.worktreeinclude` → migrou para /run-plan (bloco 3)
- Companion → migrou para README (bloco 4)

Alvo: ≤1800 palavras (margem +100 sobre alvo do operador 1700).

## Verificação end-to-end

`test_command: null`. Substituto textual:

1. `wc -w docs/philosophy.md` ≤ 1800.
2. philosophy.md final tem exatamente 8 headers H2 (frase-tese vira parágrafo de abertura sem header):
   - `## Nomear bifurcações arquiteturais`
   - `## Path contract`
   - `## Convenção de naming`
   - `## Convenção de idioma`
   - `## Convenção de commits`
   - `## Convenção de pergunta ao operador`
   - `## Linguagem ubíqua na implementação`
   - (mais o cabeçalho `# Philosophy` H1)
3. **Dono único por regra** — para cada mecânica migrada, `grep -rln '<padrão load-bearing>'` em `docs/philosophy.md skills/ agents/ CLAUDE.md README.md` retorna 1 arquivo (o destino). Padrões mínimos a verificar:
   - "probe canonical" → CLAUDE.md only
   - "pragmatic-toolkit:config" schema bullets → CLAUDE.md only
   - `{reviewer: code,qa,security}` schema completo → /triage e /run-plan (compartilhado por destino-de-execução é OK)
   - "Reler o arquivo do backlog na íntegra" → /triage e/ou /run-plan only
   - "capturei para verificação" / "capturei no backlog" mensagens → /run-plan only
   - "1 path por linha, comentários com `#`" `.worktreeinclude` → /run-plan only
4. **Sem referências órfãs** — `grep -rh 'docs/philosophy.md →' skills/ agents/ CLAUDE.md README.md docs/install.md` lista pointers retidos; cada um aponta para um header H2 que ainda existe em philosophy.md (verificável cruzando com headers do item 2).
5. CLAUDE.md final ≤1100 palavras (atual ~740 + adições do bloco 1).
6. Cada skill ainda satisfaz verificação estrutural do passo B+C (Argumentos / Pré-condições when applicable / Passos / O que NÃO fazer presentes; `## O que NÃO fazer` ≤7 itens).
7. `git diff --stat` por bloco confirma escopo: blocos 1-4 monoarquivo (CLAUDE.md, /triage, /run-plan, README); bloco 5 multiarquivo (skills); bloco 6 só philosophy.md.
8. Reviewer `code-reviewer` por bloco confirma absorção sem cerimônia reintroduzida e cuts limpos sem perda de princípio load-bearing.
