---
name: new-adr
description: Cria novo ADR no decisions_dir com numeração inferida e template padronizado. Use quando o operador pedir registro de decisão estrutural duradoura.
disable-model-invocation: false
roles:
  required: [decisions_dir]
---

# new-adr

Cria um novo Architecture Decision Record no papel `decisions_dir` (default: `docs/decisions/`) seguindo o template do toolkit.

Esta skill cria o arquivo e devolve o controle ao operador. **Não faz commit** — o operador (ou `/run-plan` num plano que inclui o ADR) commita conforme a convenção do projeto.

`decisions_dir` ausente → sub-fluxo "oferecer criação canonical via enum" (`Criar em <path>` / `Não usamos esse papel`); sem `Criar`, skill para (ADR sem diretório de decisões não tem onde morar).

`decisions_dir` em modo `local` (`paths.decisions_dir: local`) → resolvido para `.claude/local/decisions/` pelo Resolution protocol do CLAUDE.md (mecânica `mkdir`/probe/gate `Gitignore` aplicada lá). Skill segue agnóstica ao path resolvido — passos abaixo operam sobre `<decisions_dir>` que já carrega o path correto.

## Argumentos

Título da decisão (string curta e descritiva). Exemplo: `/new-adr "Política de retentativas para chamadas HTTP externas"`.

Sem título → pedir antes de prosseguir.

## Passos

1. **Listar ADRs existentes** para descobrir próximo número e formato:
   ```bash
   ls <decisions_dir>/ADR-*.md 2>/dev/null
   ```

   **Inferir formato a partir dos arquivos (não hardcode):**
   - Todos batem `ADR-\d{4}-` → 4-dígitos com padding (`0006`, `0007`).
   - Todos batem `ADR-\d{3}-` → 3-dígitos com padding (`006`, `007`) — canonical do toolkit.
   - Pelo menos um sem zero à esquerda (`ADR-1-`, `ADR-12-`) → sem padding (`6`, `7`).
   - **Mistos** (alguns padded, outros não) → enum (`AskUserQuestion`, header `Numeração`) nomeando formatos detectados (`Padding 4-dígitos`, `Sem padding`). Escolha rege apenas este ADR; saneamento histórico é decisão separada.
   - **Atípicos** (`ADR-007a-`, `ADR-DRAFT-`, sufixos) → enum (`Seguir canonical 3-dígitos` / `Manter formato atípico detectado`; Other → customizado). Não-fatal.
   - **Diretório vazio** → default 3-dígitos com padding.

   Extrair maior número (independente do padding), somar 1, aplicar formato inferido.

2. **Gerar slug** do título: lowercase, espaços/acentos→hífens, remover caracteres especiais. Ex.: `"Política de retentativas para chamadas HTTP externas"` → `politica-de-retentativas-chamadas-http-externas`.

3. **Obter data** em `YYYY-MM-DD` (`currentDate` do contexto se disponível, senão `date +%Y-%m-%d`).

3.5. **Filtro de admissão** (per [ADR-045](../../docs/decisions/ADR-045-redesign-camada-doutrinal-consolidacao-politica-admissao.md) § Decisão parte 2). Antes de criar o arquivo ADR, surfar o filtro mecânico de 3 saídas como prompt informativo. Critérios de desempate na zona cinzenta vivem em ADR-045 § Decisão parte 2; default conservador (dúvida) → operador escolhe `ADR` (Recommended); design-reviewer no step 5 audita drift pós-criação.

   `AskUserQuestion` header `Filtro`, 3 opções:

   - **`ADR — decisão estrutural reversível (Recommended)`** — `description`: "Cenário concreto de reversão nomeável (incidente empírico, sinal de uso divergente, mudança de plataforma, restrição externa); categoria conceitual nova; codifica restrição externa (regulatória, contratual, integração estável); pattern emergente ≥3 aplicações ad hoc."
   - **`Doutrina canonical — entendimento estabilizado`** — `description`: "Refinamento de mecanismo, esclarecimento doutrinal, regra editorial estabilizada. Destino canonical do projeto sob 2 eixos: mecânica concreta (lifecycle, naming, gate, schema, AskUserQuestion convention) → `CLAUDE.md`; princípio epistêmico / convenção cross-cutting → `philosophy.md` ou equivalente do projeto."
   - **`git log — evolução de processo`** — `description`: "Altera apenas implementação/estilo sem afetar runtime de outros componentes. Refactor sem decisão estrutural, iteração editorial."

   **Pós-decisão:**

   - Saída `ADR` → seguir para step 4 (criar arquivo). Fluxo default preservado.
   - Saída `Doutrina canonical` → parar criação do arquivo ADR; reportar: "Substância não passou no filtro de admissão de ADR — direcionar para a doutrina canonical do projeto (mecânica → `CLAUDE.md`; epistêmica → `philosophy.md` ou equivalente do projeto) per critério de desempate da saída escolhida. Sem ADR criado. Operador edita o documento alvo + commit como `docs:`/`chore:` conforme convenção."
   - Saída `git log` → parar criação do arquivo ADR; reportar: "Substância não passou no filtro — evolução de processo registrada apenas em commit message. Operador faz o commit relevante sem documento. **Nota orientacional:** chegar a `/new-adr` standalone com saída `git log` tipicamente sinaliza erro de framing upstream (substância pré-cristalizada como título mas era iteração editorial). Operador faz commit relevante com a substância no message; futuras invocações de `/new-adr` que detectem este padrão recorrente são candidato a refinamento do critério de entrada upstream (`/triage` step 3)."

4. **Criar arquivo** `<decisions_dir>/ADR-<NNN>-<slug>.md` com o template abaixo. Preencher conteúdo derivado de inputs explícitos do operador (ROADMAP, plano upstream, conversa recente, entrevista) — sintetizar substância já decidida em estrutura canonical. Placeholders explícitos apenas quando nenhum input substantivo existe; nunca inventar substância sem base (ver `## O que NÃO fazer` para a fronteira completa).

4.5. **Bloco metadata de revisão temporal** (per [ADR-065](../../docs/decisions/ADR-065-prazo-canonical-revisao-temporal-adrs-futuros.md)). O template carrega 3 campos canonical entre `**Status:** Proposto` e `## Origem`: `**Próxima revisão:**`, `**Cadência:**`, `**Critério de erosão auditável:**`. Preencher conforme:

   - **`**Próxima revisão:**`** — default canonical auto-preenchido: `currentDate + 6 meses` (paralelo ao uso de `currentDate` no step 3). Sem cutucada; operador pode editar pós-criação.
   - **`**Cadência:**`** — default canonical auto-preenchido: `trimestral`. Sem cutucada; operador pode editar pós-criação.
   - **`**Critério de erosão auditável:**`** — **cutucada per-novo-ADR obrigatória** em **prosa-livre direta** (sem `AskUserQuestion` — bifurcação ausente; resposta esperada é prosa livre per `philosophy.md` → "Convenção de pergunta ao operador" → "Quando todas as respostas comuns são livres, o modo é prosa desde o início"). Prompt direto: "Que condição auditável reabriria este ADR? Substância semântica per-ADR — cite ADR/feature/restrição específica do conteúdo deste ADR, OR condição genérica mas auditável (e.g., 'inversão de doutrina X em § Decisão de outro ADR', '≥N incidentes em pattern Y'). Não aceitar placeholder cosmético (Goodhart guard — derrota o propósito do campo)."

   **Critério de aceitação tri-state mecânico** (inlinado de ADR-065 § Gatilhos #3):

   - (i) **Substantivo per-ADR** — cita conteúdo específico do ADR sendo criado (ADR/feature/restrição nomeados). Aceitar.
   - (ii) **Genérico mas auditável** — não cita conteúdo específico mas tem predicado mecânico verificável (inversão de doutrina X / ≥N incidentes em pattern Y). Aceitar.
   - (iii) **Cosmético** — paráfrase de "reavaliar quando relevante" / "revisar em N meses" / "verificar se faz sentido" / "quando o pattern empírico não bater" (vago + ausência de predicado verificável). Rejeitar.

   **Fallback de rejeição:** resposta vazia OR classificada em (iii) → re-perguntar **uma única vez** explicitando o Goodhart guard inline ("a resposta anterior é cosmética sob critério tri-state — categoria (iii) [cite trecho]; refine para substantivo per-ADR ou genérico mas auditável"). Segunda resposta ainda cosmética → registrar a resposta literal no campo + anexar flag inline `<!-- TODO: Critério a refinar — Goodhart guard fallback -->` no fim da linha do Critério. Operador pode revisar pós-criação.

   Pular o sub-passo (não chamar o prompt direto) é proibido. Saída `git log` ou `Doutrina canonical` no step 3.5 já fizeram pare; sub-passo 4.5 dispara apenas no caminho que efetivamente cria o ADR.

5. **Revisão pré-retorno.** Invocar `@design-reviewer` apontando para o ADR draft recém-criado. Sem cutucada de pré-execução — o reviewer dispara automaticamente conforme [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b). Ao compor o prompt da invocação, seguir `${CLAUDE_PLUGIN_ROOT}/docs/procedures/reviewer-invocation-read.md` (instrução defensiva de `Read` do ADR draft antes da análise). Para cada finding, aplicar critério de [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (c):

   - **Cutucar operador** via `AskUserQuestion` se finding satisfaz ≥1 das 3 condições: (i) ≥2 alternativas legítimas competindo (alternativa rebatida descritivamente pelo reviewer conta como 1 caminho; só conta como ≥2 quando o reviewer apresenta caminhos competindo sem rebater); (ii) contradiz decisão documentada em ADR/`philosophy.md`/`CLAUDE.md`; (iii) exige contexto fora do diff/plano/ADR. Cláusula default-conservadora: dúvida na classificação → cutucar.
   - **Absorver pré-commit** quando nenhuma condição dispara (caminho-único). Aplicar correção no ADR draft antes de devolver controle.

   Cobre tanto invocação standalone quanto delegada por `/triage` no caminho ADR-only — `/triage` passo 5 reconhece que `/new-adr` já cobriu e não redispara o reviewer.

   **Reportar absorções no relatório de retorno em forma pronta para colar.** Quando ≥1 finding foi absorvido, relatório final inclui o **bloco formatado** `## design-reviewer findings absorvidos` (idioma da convenção de commits per [ADR-051](../../docs/decisions/ADR-051-convencoes-editoriais-consolidado.md) § Decisão (a)) com bullets curtos no formato `- <localização breve>: <correção aplicada> (caminho-único).` — idêntico à forma prescrita no `/triage` step 5. Caller cola integralmente no commit message: no caminho delegado, `/triage` step 5 cola no commit unificado; no caminho standalone, operador cola no commit do ADR. `/new-adr` não faz commit diretamente (responsabilidade externa per spec).

   **Cutucada de descoberta.** Após reportar findings do design-reviewer e antes de devolver controle, executar a cutucada conforme `${CLAUDE_PLUGIN_ROOT}/docs/procedures/cutucada-descoberta.md`.

## Template

Idioma: espelhar ADRs existentes no projeto. Diretório vazio → default canonical PT-BR. Headers em PT-BR canonical:

```markdown
# ADR-NNN: <Título>

**Data:** <YYYY-MM-DD>
**Status:** Proposto

**Próxima revisão:** <currentDate + 6 meses>
**Cadência:** <trimestral|semestral|anual>
**Critério de erosão auditável:** <condição substantiva per-ADR; Goodhart guard explícito — não placeholder cosmético tipo "reavaliar em 6 meses">

## Origem

- **<rótulo do bullet>:** <fato/link/decisão prévia que motivou este ADR>

## Contexto

<Problema concreto. O que existe hoje, quais restrições, qual ambiguidade ou dor justifica decidir agora.>

## Decisão

<Frase direta do que foi decidido, seguida das razões objetivas em bullets.>

## Consequências

<Impacto da decisão. Texto corrido ou subseções (`### Benefícios`, `### Trade-offs`, `### Limitações`, `### Mitigações`) conforme a natureza.>
```

**Seções opcionais** (incluir só se houver substância — não criar vazias):

- `## Alternativas consideradas` — comparação concreta entre opções avaliadas (H3 por alternativa com motivo de descarte).
- `## Comparação objetiva` — trade-off mensurável (tabela ou bullets paralelos).
- `## Gatilhos de revisão` — condição clara que reabriria o ADR.
- `## Implementação` — lista de commits que materializaram a decisão (formato `[\`<hash>\`](<url>) <subject>`). Útil principalmente em modo `local` ([ADR-047](../../docs/decisions/ADR-047-modo-local-paths-replicacao-cross-mode.md)), onde a regra de não-referenciar impede o caminho inverso commit → ADR; em modo canonical é redundante com `git log --grep "ADR-NNN"` mas pode destacar a sequência de implementação. Adicionado pós-implementação, não no skeleton inicial.
- `## Referências` — material externo essencial (RFCs, posts, threads).

**Bullets de Origem.** Rótulos úteis: `**Investigação:**`, `**Decisão base:**` (link a ADR anterior), `**Direção de produto:**` (link a `product_direction`), `**Regra de domínio:**` (link a RN em `ubiquitous_language`). Múltiplos gatilhos aplicáveis → escolher pelo mais específico: ADR anterior > Direção de produto > Investigação > Regra de domínio.

## Validação

- Confirmar que o slug não colide com ADR existente.
- Reportar caminho do arquivo criado. Status default `Proposto`; após revisão vira `Aceito`. Revisão futura pode mudar para `Substituído` (com link para sucessor) ou `Revogado`.

## O que NÃO fazer

- Não inventar conteúdo de Contexto/Decisão **sem base em input explícito do operador**. Preencher com conteúdo derivado de inputs disponíveis (ROADMAP, plano upstream, conversa recente, entrevista). Placeholders apenas quando nenhum input substantivo existe — quem decide a substância é o operador, a skill sintetiza/estrutura. `design-reviewer` (per [ADR-053](../../docs/decisions/ADR-053-alinhamento-triage-ecosistema-design-reviewer-consolidado.md) § Decisão (b)) audita drift entre input e síntese.
- Não alterar ADRs existentes.
- Não aceitar placeholder cosmético em `**Critério de erosão auditável:**` (Goodhart guard per [ADR-065](../../docs/decisions/ADR-065-prazo-canonical-revisao-temporal-adrs-futuros.md) § Decisão § Mecânica de preenchimento). Cutucada do step 4.5 rejeita respostas tipo `"reavaliar em 6 meses"`, `"revisar quando relevante"`, `"verificar se faz sentido"` — exige condição substantiva per-ADR auditável (cita ADR/feature/restrição específica do conteúdo do ADR sendo criado, OR condição genérica mas auditável como "inversão de doutrina X em § Decisão de outro ADR" / "≥N incidentes em pattern Y").
