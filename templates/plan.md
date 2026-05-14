# Plano — <Título curto>

<!--
Esqueleto canônico de plano consumido por /triage e /run-plan (ADR-001).
/triage lê este arquivo, copia para `<plans_dir>/<slug>.md`, adapta headers ao idioma do projeto consumidor, preenche placeholders.
/run-plan faz matching semântico contra os headers — equivalentes em outro idioma (`## Files to change`, etc.) são aceitos contanto que a estrutura informacional bata.
Seções opcionais (## Verificação manual, ## Notas operacionais) só aparecem quando há substância — não criar vazias.
-->

## Contexto

<Descrever o contexto: o que motivou a mudança, qual problema resolve, restrições relevantes.>

<!--
Campos especiais (incluir só quando aplicáveis):

**Termos ubíquos tocados:** <Termo> (<categoria>) — bounded context|agregado|entidade|RN|conceito ubíquo; omitir em refactor/doc-only.
**ADRs candidatos:** ADR-NNN (motivo) — opcional; reviewer prioriza esses, scan cobre os demais (ADR-021).
**Linha do backlog:** <texto exato> — incluir quando há linha no BACKLOG; mensageiro pra /run-plan operar transições.
**Branch:** <nome-da-branch> — incluir quando a branch já existe (issue-first GitLab, retrabalho de PR, etc.); ausência = /run-plan cria <slug> a partir do HEAD (ADR-028).
-->

## Resumo da mudança

<Síntese da mudança: o que entra, o que fica de fora, decisões-chave (incluindo escolha entre caminhos quando houve bifurcação).>

## Arquivos a alterar

<!--
Um bloco H3 por arquivo ou agrupamento lógico.
Anotação `{reviewer: <perfil>}` no fim do header orienta /run-plan:
  - Sem anotação → default code-reviewer (ou doc-reviewer se paths todos .md/.rst/.txt).
  - Um perfil: {reviewer: code|qa|security|doc} (caso normal).
  - Combinações ({reviewer: code,doc}, etc.) → exceção rara; preferir separar em blocos quando viável.
BACKLOG.md NUNCA aparece aqui — transições são geridas pelo campo `**Linha do backlog:**` acima e pelo mecanismo do /run-plan.
-->

### Bloco 1 — <descrição curta> {reviewer: code}

- `<path>`: <o que muda neste arquivo>
- ...

## Verificação end-to-end

<Critérios objetivos para considerar a mudança válida. Cite comandos concretos quando aplicáveis (grep, ls, exec do test_command). Para projetos sem suite, transformar em inspeção textual passo-a-passo.>

<!-- Seções abaixo são opcionais — incluir só se houver substância. -->

## Verificação manual

<Passos para o operador exercitar comportamento perceptível. Obrigatório quando a mudança toca fluxo crítico, integração frágil, ou superfície não-determinística (parsing, matching contra dado real, comportamento de agente LLM). Cenários enumerados, não direção genérica.>

## Notas operacionais

<Particularidades de execução: ordem dos blocos quando importa, pontos de atenção para reviewers, follow-ups previstos para batches subsequentes.>
