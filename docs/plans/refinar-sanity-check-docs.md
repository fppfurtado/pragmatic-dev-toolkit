# Refinar sanity check de documentação no /run-plan

## Contexto

O passo 4.3 de `skills/run-plan/SKILL.md` define um sanity check de consistência de documentação user-facing antes de declarar done. Três pontos do mecanismo atual divergem da filosofia codificada:

1. **Tensão com `/release` sobre CHANGELOG.** A pergunta enum cita `CHANGELOG` como candidato típico, mas a partir de v1.11.0 o `/release` compõe a entrada do changelog automaticamente a partir da CC log desde a última tag (ver `CLAUDE.md` → bloco sobre `/release`). Sugerir CHANGELOG aqui empurra o operador para um update que o `/release` posterior vai duplicar/conflitar.

2. **Heurística do segundo skip silente é frouxa.** A regra atual: "skip silente se o plano não tem `## Verificação manual` **e** o `## Resumo da mudança` não menciona superfície user-facing". Usar ausência de `## Verificação manual` como proxy é redundante — planos com validação manual puramente operacional (smoke test interno, validar refactor em ambiente local) não têm mudança user-facing e ainda assim disparariam a cutucada por presença do header. O sinal positivo no `## Resumo da mudança` (categorias concretas: CLI, env var, endpoint, comportamento perceptível, integração externa, instalação/configuração) é suficiente.

3. **Redação do enum induz cerimônia.** A opção `Atualizar arquivos .md (Other → operador lista os arquivos em prosa)` mistura uma escolha discreta com um redirecionamento implícito para Other. Pelo padrão de "Convenção de pergunta ao operador" (`docs/philosophy.md`), Other é a válvula natural quando a resposta é prosa livre — opção única `Sim, consistente` deixa Other absorver a lista de arquivos sem opção intermediária redundante.

**Linha do backlog:** /run-plan: refinar sanity check de documentação no passo 4.3

## Resumo da mudança

Refinar três pontos do sanity check de documentação no passo 4.3 de `skills/run-plan/SKILL.md`: remover CHANGELOG dos candidatos típicos sugeridos, simplificar a heurística do segundo skip silente para usar apenas o sinal positivo no `## Resumo da mudança`, e reduzir o enum a opção única `Sim, consistente` deixando Other absorver naturalmente a lista de arquivos a atualizar.

## Arquivos a alterar

### Bloco 1 — skills/run-plan/SKILL.md

Três ajustes coordenados no passo 4.3 ("Sanity check de documentação"), mesmo bloco para preservar coesão da prosa:

1. **Segundo skip silente** — substituir o critério atual "se o plano **não** tem `## Verificação manual` **e** o `## Resumo da mudança` não menciona superfície user-facing" por critério único: skip silente quando o `## Resumo da mudança` não menciona nenhuma das categorias concretas (CLI/flag nova, env var nova, endpoint novo, comportamento perceptível, integração externa, alteração de instalação/configuração). Refactor puro / internal-only segue coberto pelo mesmo critério. Remover a referência a `## Verificação manual` neste critério.

2. **Enum reduzido** — substituir as duas opções atuais (`Sim, consistente` e `Atualizar arquivos .md (Other → operador lista os arquivos em prosa)`) por opção única `Sim, consistente`. Other absorve naturalmente a lista de arquivos quando o operador quer atualizar. A pergunta segue citando a superfície user-facing inferida do plano.

3. **Candidatos típicos** — ajustar a frase "candidatos típicos (README, install, CHANGELOG)" para excluir CHANGELOG, com nota explícita do motivo: "candidatos típicos (README, install, docs internas); CHANGELOG é responsabilidade do `/release`".

Verificar também `## O que NÃO fazer` (linha sobre o sanity check) — atualizar a redação se ficar inconsistente com o novo critério único de skip.

## Verificação end-to-end

Repo sem suite automatizada (`test_command: null` no `CLAUDE.md`). Verificação textual sobre o diff agregado do bloco:

- `skills/run-plan/SKILL.md` passo 4.3 lê coerente: (a) os dois bullets de skip silente cobrem os cenários sem proxy redundante; (b) o enum não menciona "Other" no texto da opção; (c) candidatos típicos cita README e install, exclui CHANGELOG e nota responsabilidade do `/release`.
- Entrada correspondente em `## O que NÃO fazer` consistente com o novo critério.
- Diff não toca outros passos do `/run-plan`, nem `docs/philosophy.md`, nem `CLAUDE.md` (escopo cirúrgico).

## Verificação manual

Mudança comportamental em outra skill (`/run-plan`). Exercitar mentalmente os três cenários de skip alterados pelo bloco:

1. **Cenário "user-facing claro, sem validação manual"** — plano com `## Resumo da mudança` mencionando "novo comando CLI `/foo`" e sem `## Verificação manual`. **Antes:** depende de qual cláusula vencia (era `(sem manual) E (sem user-facing)` para skip; presença do user-facing no resumo já fazia cutucar). **Depois:** cutuca esperada (sinal positivo no resumo).

2. **Cenário "validação manual operacional, sem user-facing"** — plano com `## Verificação manual` (smoke test interno) e `## Resumo da mudança` sem categorias user-facing concretas. **Antes:** cutucava (presença de `## Verificação manual` impedia o segundo skip mesmo sem user-facing). **Depois:** skip silente esperado (sem sinal positivo no resumo, ausência de `## Verificação manual` deixou de ser exigida).

3. **Cenário "operador escolhe atualizar"** — plano com superfície user-facing detectada, sanity check cutuca via enum com opção única `Sim, consistente`. Operador escolhe Other e digita lista de arquivos. Resultado: bloco extra disparado (implementar → `test_command` → revisor `code` → micro-commit) com os arquivos informados.

Cada cenário requer apenas leitura do passo 4.3 atualizado e simulação textual — não há fixture exercitável neste repo.

## Notas operacionais

- Edit cirúrgico em prosa, sem migração e sem schema.
- Auto-aplicação consistente: o `## Resumo da mudança` deste plano não menciona nenhuma categoria user-facing concreta — pelo critério novo, quando `/run-plan` executar este plano, o sanity check do gate final será skip silente. Recursão coerente.
