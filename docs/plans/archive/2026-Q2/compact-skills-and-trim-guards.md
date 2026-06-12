# Compactar prosa e enxugar `## O que NÃO fazer` nas 7 skills

## Contexto

Skill body é input recorrente — cada palavra paga toda vez que a skill é invocada. Análise prévia (revisão geral dos artefatos) identificou três fontes consistentes de bloat: (a) prosa narrativa onde bullets/tabela bastam; (b) paráfrases de referência (`via X (ver philosophy.md → Y)`) quando o nome do tool sozinho ou uma regra inline já bastaria; (c) justificativas reactivas (`Por quê separar:`, `A diferença operacional:`) que são cicatrizes de discussões passadas, não orientação para edge case. Em paralelo, `## O que NÃO fazer` virou recapitulação do body em vez de scope guards genuínos — `/run-plan` tem 18 itens, `/triage` 13, `/release` 10.

**Linha do backlog:** Skills: compactar prosa e enxugar `## O que NÃO fazer` para reduzir input recorrente

## Resumo da mudança

Dois eixos por skill, um bloco por skill (7 blocos, todos com reviewer `code` default):

**Eixo 1 — Compactação.**
- Prosa narrativa procedural → bullets curtos.
- Justificativas reactivas → cortar quando não orientam decisão em edge case; manter quando o "por quê" guia julgamento.
- Paráfrases de referência → inline a regra quando cabe em 1 frase; manter `(ver philosophy.md → X)` no máximo uma vez por skill (geralmente nas pré-condições) quando o destino é load-bearing.
- Linhas de "Idioma de saída" repetidas → manter só nas skills que produzem prosa user-facing; cortar nas demais.
- Exemplos longos quando o padrão é óbvio.

**Eixo 2 — `## O que NÃO fazer`.**
- **Manter** scope guards genuínos — o que a skill **não pode** fazer mesmo que pareça lógica (ex.: "Não implementar nesta skill", "Não corrigir, só diagnosticar", "Não fazer push automático").
- **Remover** itens que recapitulam o body (a procedura já diz como fazer).

Alvo agregado: somatório `wc -w` das 7 skills ≥−25% sobre o atual (alvo do operador −30%, com margem). Sem alvo prescritivo por skill — reviewer julga proporção caso a caso (skills mais enxutas como `/debug`, `/new-adr` admitem menos corte que `/run-plan` e `/triage`).

## Arquivos a alterar

### Bloco 1 — skills/triage/SKILL.md

Compactar passos 1-6 e pré-condições. Substituir prosa procedural longa por bullets. Substituir paráfrases (`(ver "Convenção de pergunta ao operador" em docs/philosophy.md)`) por inline (`via AskUserQuestion`). Manter: tabela do passo 3 (caminhos), unidade atômica commit+push do passo 6, núcleo de gaps do passo 2. `## O que NÃO fazer` 13→~6: não implementar, não duplicar conteúdo das fontes, não pular consolidação, não separar commit+push no caminho-com-plano, não recuperar push falho via flags, não cutucar escolha de seção.

### Bloco 2 — skills/run-plan/SKILL.md

Skill mais longa, maior ganho potencial. Compactar pré-condições (prosa→bullets), passo 3 (loop por bloco) e passo 4 (gate final — especialmente 4.5 captura e 4.7 detecção de divergência, que estão dispersas em prosa). Tabela para gatilhos de captura imediata vs deferida; tabela ou bullets compactos para regras de conflito BACKLOG em 4.7. `## O que NÃO fazer` 18→~6: não declarar done sem confirmação manual, não pular revisor, não interpretar `{revisor:}` (PT alias), não contornar plano sujo copiando para worktree, não silenciar gatilho cruzado de validação manual, não executar push/PR sem confirmação.

### Bloco 3 — skills/release/SKILL.md

Compactar pré-condições e passos 1-4. Sub-caminhos 1a/1b/1c viram tabela. Bloco de review consolidado (passo 4) já está estruturado — só compactar prosa adjacente. `## O que NÃO fazer` 10→~5: não push, não criar GitHub Release, não tocar fora de version_files, não inferir bump de log não-CC sem perguntar, não sobrescrever tag.

### Bloco 4 — skills/debug/SKILL.md

Skill relativamente compacta. Cortar prosa explicativa nos passos 4-5 (formato do diagnóstico). Manter sub-caminho do ledger de hipóteses (lógica condicional). `## O que NÃO fazer` 6→5: tirar 1 item recapitulativo se houver.

### Bloco 5 — skills/new-adr/SKILL.md

Cortar variantes detalhadas de bullets de Origem e critério de escolha — exemplos abreviados. Template skeleton intacto. `## O que NÃO fazer` 3 itens — mínimo, manter.

### Bloco 6 — skills/next/SKILL.md

Compactar passo 4 (avaliação por critérios) — definições "alto/médio/baixo", "ampla/média/restrita" viram bullets. `## O que NÃO fazer` 5→4 se houver redundância com body.

### Bloco 7 — skills/gen-tests-python/SKILL.md

Cortar prosa em "Padrões úteis" (exemplos longos). "Stack assumida" e "Estrutura" compactam para bullets se possível. `## O que NÃO fazer` 3 itens — mínimo, manter.

## Verificação end-to-end

Repo tem `test_command: null`. Substituto textual aplicado ao final de cada bloco e no gate final:

1. `wc -w skills/*/SKILL.md` somatório ≥−25% sobre o atual (alvo do operador −30%).
2. Cada skill ainda tem suas seções estruturais (`## Argumentos`, `## Pré-condições` quando aplicável, `## Passos` ou equivalente, `## O que NÃO fazer`).
3. Cada `## O que NÃO fazer` tem ≤7 itens; cada item é scope guard genuíno, não recapitulação do body.
4. Frontmatter intacto (alterado em passo D anterior — não tocar `description`).
5. Comportamento operacional preservado por inspeção textual: cada skill ainda descreve argumentos, condições de parada, output esperado e revisão (no caso do `/run-plan`).
6. Reviewer `code-reviewer` por bloco confirma ausência de cerimônia reintroduzida e ausência de recapitulação ressuscitada.
