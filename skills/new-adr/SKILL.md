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

4. **Criar arquivo** `<decisions_dir>/ADR-<NNN>-<slug>.md` com o template abaixo. Não preencher conteúdo — deixar placeholders explícitos para o operador.

5. **Revisão pré-retorno.** Invocar `@design-reviewer` apontando para o ADR draft recém-criado. Sem cutucada de pré-execução — o reviewer dispara automaticamente conforme [ADR-011](../../docs/decisions/ADR-011-wiring-design-reviewer-automatico.md). Reportar findings ao operador antes de devolver controle; findings são informativos, operador edita o ADR antes do commit (que é responsabilidade externa: `/triage` orquestra ou operador commita manualmente). Cobre tanto invocação standalone quanto delegada por `/triage` no caminho ADR-only — `/triage` passo 6 reconhece que `/new-adr` já cobriu e não redispara o reviewer.

   **Cutucada de descoberta** (per [ADR-017](../../docs/decisions/ADR-017-cutucada-uniforme-descoberta-config-ausente.md)). Após reportar findings do design-reviewer e antes de devolver controle, verificar: (a) `CLAUDE.md` existe; (b) `grep -q '<!-- pragmatic-toolkit:config -->' CLAUDE.md` retorna não-zero (marker ausente); (c) string canonical da cutucada não aparece no contexto visível desta conversa CC. Todas as três satisfeitas → emitir como última linha do relatório a string canonical abaixo. Caso contrário → suprimir silenciosamente.

   > Dica: este projeto não declara o bloco `pragmatic-toolkit:config` no CLAUDE.md. Rode `/init-config` para configurar todos os papéis de uma vez.

## Template

Idioma: espelhar ADRs existentes no projeto. Diretório vazio → default canonical PT-BR. Headers em PT-BR canonical:

```markdown
# ADR-NNN: <Título>

**Data:** <YYYY-MM-DD>
**Status:** Proposto

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
- `## Implementação` — lista de commits que materializaram a decisão (formato `[\`<hash>\`](<url>) <subject>`). Útil principalmente em modo `local` ([ADR-005](docs/decisions/ADR-005-modo-local-gitignored-roles.md)), onde a regra de não-referenciar impede o caminho inverso commit → ADR; em modo canonical é redundante com `git log --grep "ADR-NNN"` mas pode destacar a sequência de implementação. Adicionado pós-implementação, não no skeleton inicial.
- `## Referências` — material externo essencial (RFCs, posts, threads).

**Bullets de Origem.** Rótulos úteis: `**Investigação:**`, `**Decisão base:**` (link a ADR anterior), `**Direção de produto:**` (link a `product_direction`), `**Regra de domínio:**` (link a RN em `ubiquitous_language`). Múltiplos gatilhos aplicáveis → escolher pelo mais específico: ADR anterior > Direção de produto > Investigação > Regra de domínio.

## Validação

- Confirmar que o slug não colide com ADR existente.
- Reportar caminho do arquivo criado. Status default `Proposto`; após revisão vira `Aceito`. Revisão futura pode mudar para `Substituído` (com link para sucessor) ou `Revogado`.

## O que NÃO fazer

- Não inventar conteúdo de Contexto/Decisão — quem decide é o operador, a skill só estrutura.
- Não alterar ADRs existentes.
