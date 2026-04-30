---
name: new-adr
description: Cria um novo ADR em docs/decisions/ com numeração automática e template padronizado. Use quando o usuário pedir um novo ADR ou registrar uma decisão estrutural duradoura.
disable-model-invocation: true
---

# new-adr

Cria um novo Architecture Decision Record em `docs/decisions/` seguindo o template do toolkit.

## Argumentos

O usuário fornece o **título** da decisão (string curta e descritiva). Exemplo: `/new-adr "Política de retentativas para chamadas HTTP externas"`.

Se o usuário não fornecer título, peça antes de prosseguir.

## Passos

1. **Listar ADRs existentes** para descobrir o próximo número:
   ```bash
   ls docs/decisions/ADR-*.md 2>/dev/null
   ```
   Extrair o maior número da listagem (formato `ADR-NNN-slug.md`). O próximo é `maior + 1`, sempre com 3 dígitos (`006`, `007`, ...).

2. **Gerar slug** do título: lowercase, espaços/acentos para hífens, remover caracteres especiais. Exemplo: `"Política de retentativas para chamadas HTTP externas"` → `politica-de-retentativas-chamadas-http-externas`.

3. **Obter data de hoje** em formato `YYYY-MM-DD` (use a `currentDate` do contexto se disponível, senão `date +%Y-%m-%d`).

4. **Criar arquivo** `docs/decisions/ADR-NNN-<slug>.md` com o template abaixo. Não preencher o conteúdo das seções — deixar placeholders explícitos para o operador completar.

## Template

Esqueleto mínimo (sempre presente):

```markdown
# ADR-NNN: <Título>

**Data:** <YYYY-MM-DD>
**Status:** Aceito

## Origem

- **<rótulo do bullet>:** <fato/link/decisão prévia que motivou este ADR>

## Contexto

<Problema concreto. O que existe hoje, quais restrições, qual ambiguidade ou dor justifica decidir agora.>

## Decisão

<Frase direta do que foi decidido, seguida das razões objetivas em bullets.>

## Consequências

<Impacto da decisão. Pode ser texto corrido ou subseções, conforme a natureza do ADR.>
```

### Seções opcionais (incluir só se houver substância)

Não criar seções vazias — incluir apenas quando a decisão genuinamente exige.

- **`## Alternativas consideradas`** — quando há comparação concreta entre opções avaliadas. Use H3 por alternativa com motivo de descarte.
- **`## Comparação objetiva`** — quando a escolha envolve trade-off mensurável (libs, estratégias). Tabela ou bullets paralelos.
- **`## Gatilhos de revisão`** — quando há condição clara que reabriria o ADR (ex.: limite de volume, mudança de fornecedor).
- **`## Referências`** — quando há material externo essencial (RFCs, posts, threads).

### Subseções de Consequências (escolha conforme o caso)

Padrões úteis: `### Benefícios`, `### Trade-offs`, `### Limitações`, `### Mitigações`. **Não obrigatório** subdividir — ADRs curtos podem ter apenas texto corrido na seção.

### Bullets de Origem (escolha conforme o caso)

Variantes úteis: `**Investigação:**`, `**Decisão base:**` (link a ADR anterior), `**Direção de produto:**` (link a IDEA.md), `**Regra de domínio:**` (link a RN). Use o rótulo que melhor descreve o gatilho real.

## Validação

Após criar o arquivo:
- Confirmar que o número é o próximo livre (não duplicar).
- Confirmar que o slug não colide com nenhum ADR existente.
- Reportar ao usuário o caminho do arquivo criado. Se a decisão for revisada futuramente, o `Status` pode mudar para `Substituído` (com link para o sucessor) ou `Revogado`.

## O que NÃO fazer

- Não inventar conteúdo de Contexto/Decisão — quem decide é o operador, o skill só estrutura.
- Não criar ADR sem título.
- Não alterar ADRs existentes.
