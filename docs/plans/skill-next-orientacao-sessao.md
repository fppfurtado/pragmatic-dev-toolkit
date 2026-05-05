# skill /next — orientação de sessão com análise de backlog

## Contexto

`/triage` invocado sem argumento não tem comportamento útil definido — a skill pede a intenção ao operador e para. O operador que abre uma sessão sem intenção formada precisa consultar o backlog manualmente antes de saber o que perguntar.

Este plano adiciona uma skill `/next` como pré-passo de orientação de sessão e atualiza `/triage` para delegar a ela quando não receber argumento.

**Decisões fechadas na conversa de alinhamento (não revisitar):**

- **Skill separada, não inline em `/triage`.** Permite invocação direta (`/next`) sem passar por `/triage`, mantém `/triage` com escopo único e coloca o comportamento em um único lugar.
- **Verificação de código por item.** `/next` lê os seis primeiros `## Próximos` e busca evidência de implementação antes de ranquear. Itens já implementados são descartados (ou informados se evidência for fraca) antes de chegar ao top 3.
- **Evidência forte → mover para `## Concluídos` automaticamente.** Sem confirmação: limpar backlog desatualizado é baixo risco e o operador pode verificar via git. Evidência fraca → informar apenas, deixar operador decidir.
- **Ranking por alinhamento estratégico + amplitude de toque.** Ambos são critérios factuais e auditáveis (lidos de `product_direction` e do código), não scoring opaco. Raciocínio explícito por item — operador pode discordar.
- **`## Em andamento` informa, não sugere.** Itens em andamento são listados como contexto de sessão ("algo em curso em outra sessão"), não como candidatos.
- **Sem guard de falha em `/triage`.** `/next` e `/triage` fazem parte do mesmo plugin — instalação parcial não é cenário real de operação.
- **Delegação por path literal em `/triage`.** `skills/next/SKILL.md` é o ponto de referência — rastreável e sem ambiguidade de nome.

**Linha do backlog:** `skill /next: orientação de sessão — analisa backlog, verifica implementados e sugere top 3 por impacto; /triage delega a /next quando invocada sem argumento`

## Resumo da mudança

- Criar `skills/next/SKILL.md` com o workflow completo de orientação de sessão (6 passos: ler backlog → selecionar candidatos → verificar código → avaliar e ranquear → apresentar e colher escolha → continuar com `/triage`).
- Atualizar uma linha em `skills/triage/SKILL.md` na seção `## Argumentos`: substituir "peça ao usuário a intenção antes de prosseguir" por delegação a `skills/next/SKILL.md`.

## Arquivos a alterar

### Bloco 1 — `skills/next/SKILL.md` (arquivo novo) {reviewer: code}

Criar o arquivo com frontmatter (`name: next`, `description`) e os seguintes passos:

1. **Pré-condições**: resolver `backlog` (obrigatório funcional — sem backlog interrompe) e `product_direction` (informacional).
2. **Ler backlog**: extrair `## Próximos` (candidatos) e `## Em andamento` (só informar, não analisar).
3. **Selecionar candidatos**: seis primeiros de `## Próximos` por ordem de aparição (topo = mais antigo).
4. **Verificar implementação no código**: para cada item, buscar evidência. Evidência forte → mover para `## Concluídos` + reportar. Evidência fraca → reportar sem mover.
5. **Avaliar e ranquear restantes**: alinhamento estratégico (`product_direction`) + amplitude de toque (código). Raciocínio explícito por item. Empate desfeito por ordem de aparição no backlog.
6. **Apresentar e colher escolha**: reportar movimentações, itens em andamento (informativo), top 3 com raciocínio. `AskUserQuestion` (header `Próximo`) com as 3 opções + Other.
7. **Continuar com `/triage`**: executar fluxo de `/triage` a partir do Passo 1, usando a escolha como intenção. Não repetir resolução de papéis já realizados.

Seção `## O que NÃO fazer` obrigatória ao final (ver convenção em `CLAUDE.md`).

### Bloco 2 — `skills/triage/SKILL.md` (uma linha na seção `## Argumentos`) {reviewer: code}

Substituir:

```
Se o input estiver vazio ou genericamente "o que vamos fazer hoje?", peça ao usuário a intenção antes de prosseguir.
```

Por:

```
Se o input estiver vazio ou genericamente "o que vamos fazer hoje?", ler e seguir o workflow definido em `skills/next/SKILL.md`.
```

## Verificação manual

Testar num projeto consumidor com plugin instalado e backlog populado:

1. **Delegação**: invocar `/triage` sem argumento → fluxo de `/next` deve iniciar (leitura de backlog, verificação de código, ranqueamento, AskUserQuestion).
2. **Detecção com evidência forte**: adicionar ao backlog um item claramente implementado no código do projeto → `/next` deve identificá-lo, mover para `## Concluídos` e informar o operador com justificativa de 1 linha.
3. **Evidência fraca**: adicionar item parcialmente implementado (feature similar mas escopo diferente) → deve aparecer no relatório de "evidência fraca" sem ser movido.
4. **Em andamento não sugerido**: ter ao menos um item em `## Em andamento` → deve aparecer no relatório como informação, não no top 3.
5. **Ranking auditável**: os top 3 devem trazer raciocínio explícito de alinhamento estratégico + amplitude de toque — não só a lista de itens.
6. **Fluxo contínuo**: escolher um dos 3 via AskUserQuestion → skill deve prosseguir com `/triage` passo 1 usando o item escolhido como intenção, sem pedir a intenção novamente.
7. **Invocação direta**: invocar `/next` diretamente (sem passar por `/triage`) → mesmo fluxo dos itens 1–6.
