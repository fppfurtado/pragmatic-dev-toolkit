---
name: heal-backlog
description: Detecta merge artifacts em BACKLOG.md (linha duplicada em Em andamento+Concluídos) e propõe edit de cura via gate Aplicar/Cancelar. Use quando a Action de validação abrir issue ou quando suspeitar de inconsistência manual.
roles:
  required: [backlog]
---

# heal-backlog

Cura artefatos de merge em `BACKLOG.md` (linha duplicada em `## Em andamento`+`## Concluídos`). Escreve no arquivo, não commita.

## Argumentos

- Sem argumento: usa o path resolvido pelo papel `backlog`.
- `/heal-backlog <path>`: path explícito (útil para rodar contra outro arquivo).

## Passos

### 1. Ler e parsear

Ler arquivo do papel `backlog`. Parsear seções H2 (`## Próximos`, `## Em andamento`, `## Concluídos`) e bullets top-level (`- `).

### 2. Detectar padrões automáticos

Padrões reconhecíveis sem input do operador:

- **Duplicata Em andamento+Concluídos** — linha exata (após strip) presente em ambas seções. Cura: remover de Em andamento (a movimentação para Concluídos já completou).
- **Estrutural** — seção `## Próximos`, `## Em andamento` ou `## Concluídos` ausente do arquivo. Skill **não cria** seção vazia automaticamente — reportar e parar (operador edita estrutura manualmente; skill foi feita para curar dados, não estrutura).

### 3. Caso degenerado: sem padrão detectado

Sem duplicatas nem inconsistência estrutural → reportar `BACKLOG.md íntegro`. Em seguida, se o operador responder em prosa relatando linha sumida (texto exato + seção destino), executar passo 5; caso contrário, encerrar sem edit/gate.

### 4. Padrão automático detectado: propor cura

Mostrar ao operador a linha exata da duplicata e qual seção (`## Em andamento`) será removida — uma frase basta. Gate via `AskUserQuestion` (header `Heal`):

- **Aplicar** — escrever arquivo com edit; reportar paths e linhas afetadas. Operador commita conforme convenção.
- **Cancelar** — abort silente; nada para reverter (preparação ficou em memória).

### 5. Linha sumida (entrada manual do operador)

Disparado pelo passo 3 quando o operador relata em prosa qual linha sumiu e em qual seção destino. Skill insere a linha (texto exato fornecido pelo operador) no topo da seção e propõe via mesmo gate do passo 4.

### 6. Reportar e devolver controle

- Cura aplicada → reportar arquivo, linha afetada, e sugerir `git add <path> && git commit -m "chore(backlog): heal merge artifact"`.
- Cancelado → reportar abort.
- Íntegro → reportar e encerrar.

## O que NÃO fazer

- Não reconstruir linhas sumidas via `git log`, `git blame` ou histórico do PR — exigir texto exato do operador. Reconstrução automática gera dados inventados que parecem plausíveis.
- Não tocar arquivos fora do papel `backlog` resolvido.
- Não consolidar/reordenar linhas além da cura específica do padrão detectado — skill é mínima e cirúrgica.
