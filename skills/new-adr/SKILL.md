---
name: new-adr
description: Cria um novo ADR no diretório de decisões do projeto com numeração automática (formato inferido dos ADRs existentes) e template padronizado. Use quando o usuário pedir um novo ADR ou registrar uma decisão estrutural duradoura.
disable-model-invocation: true
---

# new-adr

Cria um novo Architecture Decision Record no papel `decisions_dir` do projeto (default: `docs/decisions/`; resolução em `docs/philosophy.md`) seguindo o template do toolkit.

## Argumentos

O usuário fornece o **título** da decisão (string curta e descritiva). Exemplo: `/new-adr "Política de retentativas para chamadas HTTP externas"`.

Se o usuário não fornecer título, peça antes de prosseguir.

## Passos

1. **Resolver `decisions_dir`** seguindo a Resolução de papéis (default: `docs/decisions/`). Se o papel resolve para "não temos", parar e reportar — ADR sem diretório de decisões não tem onde morar.

2. **Listar ADRs existentes** no `decisions_dir` resolvido para descobrir o próximo número e o formato de numeração:
   ```bash
   ls <decisions_dir>/ADR-*.md 2>/dev/null
   ```
   - **Inferir o formato** a partir dos arquivos existentes (não hardcode):
     - Se todos batem `ADR-\d{4}-` → 4-dígitos com padding (`0006`, `0007`, …).
     - Se todos batem `ADR-\d{3}-` → 3-dígitos com padding (`006`, `007`, …) — formato canonical do toolkit.
     - Se há `ADR-\d+-` sem zero à esquerda em ao menos um (ex.: `ADR-1-`, `ADR-12-`) → sem padding (`6`, `7`, …).
     - Formatos mistos (alguns padded, outros não) → flagar ao operador antes de prosseguir; provável drift histórico que merece decisão antes de continuar.
     - **Diretório vazio**: default 3-dígitos com padding (canonical do toolkit).
   - Extrair o maior número numérico (independente do padding) e somar 1; aplicar o formato inferido.

3. **Gerar slug** do título: lowercase, espaços/acentos para hífens, remover caracteres especiais. Exemplo: `"Política de retentativas para chamadas HTTP externas"` → `politica-de-retentativas-chamadas-http-externas`.

4. **Obter data de hoje** em formato `YYYY-MM-DD` (use a `currentDate` do contexto se disponível, senão `date +%Y-%m-%d`).

5. **Criar arquivo** `<decisions_dir>/ADR-<NNN>-<slug>.md` (onde `<NNN>` segue o formato inferido) com o template abaixo. Não preencher o conteúdo das seções — deixar placeholders explícitos para o operador completar.

## Template

Idioma do template: **espelhar ADRs existentes no projeto consumidor**. Se o `decisions_dir` resolvido tem ADRs prévios, usar o idioma deles (headers, status, rótulos de bullets). Se está vazio, default canonical PT-BR mostrado abaixo. Ver "Convenção de idioma" em `docs/philosophy.md`.

Esqueleto mínimo (sempre presente, headers em PT-BR canonical):

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

Variantes úteis: `**Investigação:**`, `**Decisão base:**` (link a ADR anterior), `**Direção de produto:**` (link ao papel `product_direction` do projeto, default `IDEA.md`), `**Regra de domínio:**` (link a RN no papel `ubiquitous_language`). Use o rótulo que melhor descreve o gatilho real.

## Validação

Após criar o arquivo:
- Confirmar que o número é o próximo livre (não duplicar).
- Confirmar que o slug não colide com nenhum ADR existente.
- Reportar ao usuário o caminho do arquivo criado. Se a decisão for revisada futuramente, o `Status` pode mudar para `Substituído` (com link para o sucessor) ou `Revogado`.

## O que NÃO fazer

- Não inventar conteúdo de Contexto/Decisão — quem decide é o operador, o skill só estrutura.
- Não criar ADR sem título.
- Não alterar ADRs existentes.
