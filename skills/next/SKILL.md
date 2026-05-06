---
name: next
description: Lê o backlog, descarta itens já implementados e sugere top 3 candidatos por impacto estratégico. Invocável direto ou como pré-passo de /triage sem argumento.
---

# next

Skill de orientação de sessão: lê o backlog, limpa itens já implementados e indica os três candidatos de maior impacto — alimentando o fluxo de `/triage` a seguir.

## Pré-condições

Aplicar **Resolução de papéis** (ver `docs/philosophy.md`):

- `backlog` (default `BACKLOG.md`) — sem backlog não há o que analisar. Resolveu "não temos" → informar e interromper.
- `product_direction` (default `IDEA.md`) — informacional, usado para alinhamento estratégico. Papel ausente reduz profundidade da análise, nunca bloqueia.

## Passos

### 1. Ler o backlog

Ler o arquivo na íntegra. Extrair:

- **`## Próximos`** — candidatos a analisar.
- **`## Em andamento`** — itens já comprometidos. Reportar ao final apenas como informação; não analisar nem sugerir.

`## Próximos` vazio → informar e interromper.

### 2. Selecionar candidatos

Pegar os **seis primeiros** itens de `## Próximos` em ordem de aparição (topo = mais antigo). Seis dá margem para descartar implementados e ainda chegar a três finais.

### 3. Verificar implementação no código

Para cada candidato, buscar evidência no repo (funções, endpoints, modelos, comandos, fluxos correspondentes). Classificar:

- **Evidência forte** — código claro e diretamente mapeável (ex.: item "exportar movimentos em CSV" → handler de export CSV presente e funcional). Mover a linha para `## Concluídos` automaticamente e reportar com justificativa de 1 linha.
- **Evidência fraca** — código parcial, feature similar com escopo diferente, ou inferência incerta. Reportar o que foi encontrado; **não mover** — operador decide.
- **Sem evidência** — segue como candidato normal.

### 4. Avaliar e classificar os restantes

Para cada item que sobrou:

- **Alinhamento estratégico** vs `product_direction`: `alto` (menção direta ou relação clara) / `médio` (contexto geral) / `baixo` (não conectado).
- **Amplitude de toque** inferida da descrição + código existente: `ampla` (múltiplos módulos ou integração externa) / `média` (um módulo com ramificações) / `restrita` (localizada).

Combinar os dois critérios para ranking. Empate → ordem de aparição (mais antigo sobe). Mostrar o raciocínio por item — operador deve poder discordar sem aceitar caixa-preta.

### 5. Apresentar resultado e colher escolha

Reportar em formato curto:

- **Movidos para `## Concluídos`** (evidência forte): listar com justificativa.
- **Evidência fraca:** listar com o que foi encontrado.
- **Em andamento:** listar como informação.
- **Top 3 candidatos** em ordem decrescente de impacto, com raciocínio de alinhamento + amplitude.

Em seguida, enum (`AskUserQuestion`, header `Próximo`) com as 3 opções nomeadas pelo texto exato da linha + Other (operador digita intenção diferente). Escolha alimenta diretamente `/triage`.

### 6. Continuar com `/triage`

Com a intenção confirmada (item escolhido ou texto livre), executar o fluxo de `/triage` a partir do passo 1 — tratando a intenção como argumento. Reaproveitar papéis já resolvidos neste fluxo.

## O que NÃO fazer

- Não apresentar mais de 3 sugestões no top.
- Não iniciar `/triage` sem escolha explícita do operador.
- Não implementar nada — esta skill é orientação de sessão, não execução.
