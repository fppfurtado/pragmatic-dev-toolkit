---
name: next
description: Lê o backlog, descarta itens já implementados e sugere top 3 candidatos por impacto estratégico. Invocável direto ou como pré-passo de /triage sem argumento.
---

# next

Skill de orientação de sessão: lê o backlog, limpa itens já implementados e indica os três candidatos de maior impacto para o operador escolher — alimentando o fluxo de `/triage` a seguir.

## Pré-condições

Para cada papel necessário, aplicar **Resolução de papéis** (ver `docs/philosophy.md`):

- `backlog` (default canonical `BACKLOG.md`) — sem backlog não há o que analisar. Se o papel resolver para `não temos`, informar ao operador e interromper.
- `product_direction` (default canonical `IDEA.md`) — informacional: usado para avaliar alinhamento estratégico. Papel ausente reduz a profundidade da análise, nunca bloqueia.

## Passos

### 1. Ler o backlog

Ler o arquivo do papel `backlog` na íntegra. Extrair:

- **`## Próximos`** — candidatos a analisar.
- **`## Em andamento`** — itens já comprometidos, possivelmente em outra sessão. Não analisar nem sugerir; reportar ao final apenas como informação.

Se `## Próximos` estiver vazio, informar ao operador e interromper.

### 2. Selecionar candidatos

Pegar os **seis primeiros** itens de `## Próximos` em ordem de aparição (topo = mais antigo). Seis dá margem para descartar implementados e ainda chegar a três finais.

### 3. Verificar implementação no código

Para cada item selecionado, buscar no repositório evidência de implementação — funções, endpoints, modelos, comandos ou fluxos que correspondam ao que o item descreve.

Classificar em dois níveis:

- **Evidência forte:** código claro e diretamente mapeável ao item (ex.: item "exportar movimentos em CSV" → handler de export CSV presente e funcional). Ação: mover a linha para `## Concluídos` automaticamente e reportar ao operador com justificativa de 1 linha.
- **Evidência fraca:** código parcial, feature similar mas escopo diferente, ou inferência incerta. Ação: reportar ao operador com o que foi encontrado; não mover. O operador decide o destino fora deste fluxo.

Itens sem evidência seguem como candidatos normais.

### 4. Avaliar e classificar os candidatos restantes

Para cada item que sobrou (não descartado como implementado com evidência forte):

- **Alinhamento estratégico** — o item aparece ou se conecta com prioridades declaradas em `product_direction`? Classificar em: `alto` (menção direta ou relação clara com o que está sendo construído), `médio` (relacionado ao contexto geral), `baixo` (não conectado ou tangencial).
- **Amplitude de toque** — quantos domínios, módulos ou integrações o item provavelmente envolve, inferido da descrição e do código existente? `ampla` (cruza múltiplos módulos ou toca integração externa), `média` (um módulo com ramificações), `restrita` (mudança localizada).

Combinar os dois critérios para produzir um ranking. Empates são desfeitos pela ordem de aparição no backlog (mais antigo sobe). Mostrar o raciocínio explicitamente por item — o operador deve poder discordar sem aceitar uma caixa-preta.

### 5. Apresentar resultado e colher escolha

Reportar ao operador em formato curto:

- **Itens movidos para `## Concluídos`** (evidência forte): listar com justificativa.
- **Itens com evidência fraca**: listar com o que foi encontrado.
- **Itens `## Em andamento`**: listar como informação; não sugerir para trabalho.
- **Top 3 candidatos**: apresentar em ordem decrescente de impacto, com raciocínio de alinhamento + amplitude por item.

Em seguida, perguntar ao operador via `AskUserQuestion` (header `Próximo`) com as três opções nomeadas pelo texto exato da linha do backlog + "Other" (operador digita uma intenção diferente). A escolha alimenta diretamente o fluxo de `/triage` a seguir.

### 6. Continuar com `/triage`

Com a intenção confirmada (item escolhido ou texto livre), executar o fluxo completo de `/triage` a partir do **Passo 1 — Carregar contexto mínimo**, tratando a intenção como argumento fornecido pelo operador.

Não repetir resolução de papéis já realizados neste fluxo — reaproveitar o que já foi resolvido.

## O que NÃO fazer

- Não mover item para `## Concluídos` com evidência fraca — reportar e deixar o operador decidir.
- Não apresentar mais de três sugestões no top.
- Não iniciar o fluxo de `/triage` sem escolha explícita do operador.
- Não analisar nem sugerir itens de `## Em andamento` — apenas informar sua existência.
- Não implementar nada — esta skill é orientação de sessão, não execução.
