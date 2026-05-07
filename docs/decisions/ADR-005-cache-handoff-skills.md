# ADR-005: Cache de handoff entre skills coreografadas

**Data:** 2026-05-07
**Status:** Proposto

## Origem

- **Investigação:** Item registrado em `## Próximos` do BACKLOG na revisão arquitetural pós-v1.20.0: "/debug → /triage handoff perde contexto em sessão longa". O `/debug` produz diagnóstico estruturado (incluindo ledger de hipóteses) **na conversa**, não em arquivo. Em sessão longa onde o contexto é compactado, o diagnóstico cai do diálogo antes de o operador invocar `/triage` para implementar o fix. Resultado: operador repete o raciocínio do `/debug`, abre conversa nova só pra ler o diagnóstico antigo, ou parte para o `/triage` sem o ledger de hipóteses como base.
- **Decisão base:** D2/ADR-004 estabeleceu "state-tracking em git/forge, não em markdown". Esta decisão é categoria diferente — não é state de **trabalho em andamento**, é **memória entre invocações de skills coreografadas no mesmo workflow** (`/debug` produz diagnóstico → operador decide `/triage` → plano absorve diagnóstico). Vale registrar a distinção para evitar drift conceitual.

## Contexto

Algumas skills do plugin formam **workflows coreografados** — uma produz output que outra consome:

- `/triage` → `/run-plan`: o handoff é **arquivo persistente** (`docs/plans/<slug>.md` commitado). Robusto a sessão e a máquina.
- `/debug` → `/triage`: o handoff é **prosa em conversa**. Frágil a compactação de contexto e a sessões diferentes.

A diferença é que o produto do `/triage` (plano) é artefato estrutural do workflow do projeto, enquanto o produto do `/debug` (diagnóstico) é efêmero por natureza — só serve durante o ciclo "diagnosticar → corrigir". Mas "efêmero" não é "instantâneo": em sessão longa, o ciclo pode levar horas, e o diagnóstico precisa sobreviver a esse intervalo.

Soluções consideradas:

1. **Snippet pronto no `/debug` passo 6** — operador copia/cola invocação de `/triage` antes do contexto cair. Cobre o caso "sessão curta, ação imediata" mas não o pain reportado (operador deixa pra invocar /triage horas depois, no meio da mesma sessão longa, e contexto já caiu).

2. **Cache local em arquivo** — `/debug` grava sumário estruturado em `.cache/debug-<timestamp>.md` (gitignored); `/triage` passo 1 absorve cache recente automaticamente. Persistência sobrevive à compactação e a fechamento/reabertura de sessão na mesma máquina.

3. **Cache + snippet** — cobre os dois cenários (imediato + tardio).

## Decisão

**Implementar cache + snippet pronto** (caminho rico):

### Cache em `.cache/debug-<timestamp>.md`

`/debug` passo 6, antes de "Reportar e devolver controle", grava sumário estruturado com os campos do passo 5 do skill:

```
.cache/debug-<YYYY-MM-DD-HHMMSS>.md
```

Conteúdo do arquivo:

```markdown
# Diagnóstico /debug — <YYYY-MM-DD HH:MM:SS>

## Sintoma

<descrição operacional>

## Hipóteses testadas

<ledger se ≥2 hipóteses; omitido se hipótese única>

## Causa-raiz

<arquivo:linha + mecanismo>

## Evidência

<o que foi observado/rodado>

## Escopo de impacto

<quem mais é afetado>

## Caminhos de correção

<um ou mais caminhos com trade-off>
```

`/triage` passo 1 acrescenta verificação: `.cache/debug-*.md` modificado nas últimas 24h (`mtime`) → absorver no `## Contexto` do plano produzido como `**Diagnóstico /debug:**` (resumo curto + path do arquivo para referência completa). Sem cache recente → segue silente. Múltiplos arquivos recentes → usar o mais recente; reportar os outros como contexto adicional disponível.

### Snippet pronto no `/debug` passo 6

Após gravar o cache e antes de "Reportar e devolver controle", emitir bloco-comando pronto:

```
/triage <intent composta a partir do diagnóstico>
```

Operador copia/cola se quiser invocar imediatamente. Útil para sessão curta onde o contexto não vai cair antes da invocação.

### Categorização vs ADR-004 (state-tracking)

**Cache de handoff** ≠ **state-tracking**:
- State-tracking (D2): "trabalho em andamento" — descobrível via git/forge (branches, PRs); persistente, observável por terceiros, fonte da verdade.
- Cache de handoff (D5): "memória entre skills coreografadas" — local, efêmero (mtime + expiração 24h), invisível ao git, não-fonte-da-verdade. O diagnóstico **autoritativo** é o produzido em runtime; o cache é só uma cópia pra sobreviver compactação de contexto.

A distinção é importante para futura extensão: nem toda persistência local quebra o princípio do D2.

### Expiração e gitignore

- **Expiração**: 24h por `mtime`. `/triage` ignora arquivos mais antigos. Limpeza física é responsabilidade do operador (ou ferramenta externa); skill não removepara evitar destruir cache de outras invocações simultâneas.
- **`.gitignore`**: adicionar `.cache/`. Cache é local efêmero; commitá-lo seria erro categorial (state em markdown que ADR-004 rejeita).

## Consequências

### Benefícios

- **Pain reportado resolvido**: diagnóstico do `/debug` sobrevive compactação de contexto e fechamento/reabertura da sessão.
- **Snippet pronto** cobre o cenário ativo "operador invoca /triage agora mesmo" sem fricção.
- **Padrão extensível**: caso futura skill precise de handoff via cache (ex.: `/gen-tests-python` produz teste para `/run-plan` validar), `.cache/<skill>-*.md` segue o mesmo modelo.

### Trade-offs

- **Nova superfície local**: `.cache/` gitignored. Custos de manutenção mínimos (sem limpeza automática; expiração só no consumo).
- **Cache pode confundir** se operador trabalha em múltiplos projetos com `.cache/` no PATH errado. Mitigação: `.cache/` é por-repo (gitignored em cada repo), não global. Path absoluto coletado em runtime.
- **Snippet + cache podem divergir** se o operador editar manualmente o cache antes de invocar `/triage` mas o diagnóstico em conversa for diferente. Aceito: editar cache manualmente é caso de canto; cache é a verdade do que `/debug` capturou no momento.

### Limitações

- Cache **não atravessa máquinas** (gitignored). Se operador troca de máquina entre `/debug` e `/triage`, cache não vai. Aceito: cenário raro; operador pode reinvocar `/debug` na nova máquina ou copiar manualmente o arquivo.
- Sumário estruturado em arquivo é **fixo** no formato definido aqui. Se `/debug` evoluir o passo 5 com novos campos, este ADR precisa ser revisado para incluir os novos campos no sumário.

## Alternativas consideradas

- **Apenas snippet (sem cache)**: descartado — não resolve o pain reportado (sessão longa, contexto caiu). Snippet só ajuda no caso imediato.
- **Apenas cache (sem snippet)**: caminho mínimo válido. Operador escolheu (b) por bonus de UX em sessão curta.
- **Cache em arquivo commitado** (não gitignored): rejeitado — viola o princípio de D2 (state em git/forge, não em markdown). Cache não é state-tracking; é memória efêmera.
- **Cache em estrutura externa** (ex.: `~/.cache/pragmatic-dev-toolkit/`): mais portável, mas perde o "por-projeto" (cache de outro projeto pode interferir). `.cache/` no repo é mais seguro.
- **Cache em formato JSON/YAML estruturado**: rejeitado — markdown estruturado é mais legível para o operador inspecionar diretamente; `/triage` lê markdown sem parser dedicado.

## Gatilhos de revisão

- Pain reportado de cache obsoleto sobrevivendo trabalho em PR diferente (>24h é tempo razoável?) → revisar expiração.
- Surge skill nova precisando de handoff via cache → reabrir para extrair padrão (`templates/cache-<skill>.md` análogo a `templates/plan.md`?).
- `.cache/` cresce sem limpeza e cria fricção (centenas de arquivos antigos) → adicionar limpeza automática em alguma skill (ex.: `/release` remove arquivos `.cache/*.md` mais antigos que 7 dias) ou hook.
