# run-plan: classificar capturas automáticas — validação vs backlog

## Contexto

O passo 4.5 de `/run-plan` captura imprevistos detectados durante execução e validação manual e materializa todos em `## Próximos` do backlog. Isso mistura dois tipos de itens com destinos distintos:

- **Capturas de validação**: cenário não exercitado, divergência do plano, gap de verificação — pertencem ao plano corrente (em `## Pendências de validação`), porque sua resolução é pré-requisito para declarar a feature done.
- **Capturas de backlog**: feature/fix/doc/regra nova, bug independente, finding fora-do-escopo — pertencem a `## Próximos` do backlog (escopo futuro, sem relação com o gate corrente).

Misturar os dois dilui o sinal do backlog (radar de produto/engenharia) com pendências de execução, e deixa no backlog itens que bloqueiam a validação da feature atual.

**Linha do backlog:** `/run-plan + philosophy.md: distinguir capturas de validação (plano) de capturas de feature/correção (backlog) na regra de captura automática`

## Resumo da mudança

1. **`skills/run-plan/SKILL.md`** — refinar passo 4.5: classificar capturas em "validação" vs "backlog" no momento da detecção, rotear para o destino correto (plano ou backlog) e ajustar a mensagem ao operador. Duas adições a `## O que NÃO fazer`.
2. **`docs/philosophy.md`** — nova seção "Classificação de capturas automáticas" após "Consolidação do backlog", documentando a heurística e o porquê.

## Arquivos a alterar

### Bloco 1 — `skills/run-plan/SKILL.md` {reviewer: code}

No passo 4.5 "Captura automática de imprevistos":

**Substituir "Política de gravação"** pelo seguinte:

Classificar no momento da captura em dois tipos:

- **Validação** — item cuja resolução é pré-requisito para declarar a feature done: cenário não exercitado descoberto na execução, divergência do plano (comportamento observado diferente do esperado por `## Verificação manual`), gap de passo de verificação, reviewer pulado sem justificativa. Mensagem ao operador: `"capturei para verificação: <linha>"`.
- **Backlog** — item independente do gate corrente: feature/fix/doc/regra nova, bug colateral (não relacionado ao gate corrente), finding fora-do-escopo do plano, gap operacional sinalizado por hook. Mensagem ao operador: `"capturei no backlog: <linha>"`.

Sinal explícito do operador vence a classificação automática: se o operador instruir o destino ("registra no backlog X", "registra no plano Y"), obedecer sem questionar.

**Substituir os blocos "Lista vazia" e "Lista não-vazia" do gate final** pelo seguinte:

- **Ambas as listas vazias** → skip silente.
- **Lista de validação não-vazia** → parte do bloco extra: escrever seção `## Pendências de validação` no arquivo do plano corrente (adicionar ao final; criar a seção se não existe), uma linha por item.
- **Lista de backlog não-vazia** → parte do bloco extra: escrever uma linha por item em `## Próximos` do arquivo do papel `backlog`; **aplicar consolidação** conforme `docs/philosophy.md` → "Consolidação do backlog".
- As duas partes entram num único revisor `code` e micro-commit.

**Substituir "Caso especial"** pelo seguinte:

Papel `backlog` resolveu para "não temos" → lista de backlog vira relato final ao operador (sem registro persistido). Lista de validação é gravada no plano independentemente do estado do papel `backlog`.

**Adicionar ao final de `## O que NÃO fazer`:**

- Não rotear para o backlog capturas de validação (cenário não exercitado, divergência do plano, gap de verificação manual) — destino é `## Pendências de validação` no plano corrente.
- Não informar "capturei no backlog" para item classificado como validação — a mensagem ao operador deve refletir o destino real do item.

### Bloco 2 — `docs/philosophy.md` {reviewer: code}

Adicionar nova seção "Classificação de capturas automáticas" após a seção "Consolidação do backlog" (antes de "Linguagem ubíqua na implementação"):

```markdown
## Classificação de capturas automáticas

Toda captura detectada pelo `/run-plan` (passo 4.5) é classificada em dois tipos antes de ser roteada:

**Validação** — item cuja resolução é pré-requisito para declarar a feature done:
- Cenário não exercitado descoberto na execução
- Divergência do plano (comportamento observado diferente do esperado por `## Verificação manual`)
- Gap de passo de verificação manual
- Reviewer pulado sem justificativa

Destino: seção `## Pendências de validação` no arquivo do plano corrente (criada ao final se não existe). Independe do estado do papel `backlog`.

**Backlog** — item independente do gate corrente:
- Feature/fix/doc/regra nova, requisito novo
- Bug colateral (não relacionado ao gate corrente)
- Finding fora-do-escopo do plano (reviewer encontrou problema em outro módulo)
- Gap operacional sinalizado por hook

Destino: `## Próximos` do papel `backlog`. Sujeito à regra de "Consolidação do backlog".

**Sinal explícito do operador** vence a heurística — se o operador instruir o destino, obedecer sem questionar.

**Por quê separar:** o backlog é radar de produto/engenharia (o que vem depois). Misturar pendências de validação da feature corrente dilui o sinal e confunde priorização. Cada contêiner recebe o que lhe pertence.
```

## Verificação end-to-end

1. Ler o passo 4.5 atualizado em `skills/run-plan/SKILL.md` e verificar:
   - A classificação "validação" vs "backlog" é clara e cobre os 6 gatilhos existentes (falha contornada, finding fora-do-escopo, hook bloqueando, superfície faltante, divergência do plano, bug colateral).
   - As mensagens ao operador diferem conforme o tipo.
   - A materialização no gate final cobre os 4 casos: só validação, só backlog, ambos, ambos vazios.
   - O caso especial (papel `backlog` = "não temos") está correto: validação ainda vai para o plano.
   - `## O que NÃO fazer` contém as duas novas proibições.
2. Ler a nova seção em `docs/philosophy.md` e verificar:
   - A heurística está alinhada com o que está em `/run-plan`.
   - "Por quê separar" explica a motivação.
   - Referência a "Consolidação do backlog" está correta.
