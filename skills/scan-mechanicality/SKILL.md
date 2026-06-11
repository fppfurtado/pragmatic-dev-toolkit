---
name: scan-mechanicality
description: Aplica julgamento heurístico-semântico sobre prompt markdown arbitrário e classifica a substância como mecanizável >50% (POSITIVO), mistura (AMBÍGUO) ou heurístico-semântica dominante (NEGATIVO). Stack-agnóstica — aceita qualquer extensão de arquivo.
disable-model-invocation: false
roles:
  required: []
  informational: []
---

# scan-mechanicality

Skill diagnóstica universal: lê um prompt em markdown (SKILL.md, system prompt de agente, `agent.md`, `prompt.py`, blocos espalhados em código) e responde se a substância dali é predominantemente **mecanizável** — codificável como regra determinística, transformação declarativa, lookup de tabela — ou predominantemente **heurística-semântica** — julgamento contextual, decisão baseada em sinais difusos, prosa que exige interpretação.

A skill aplica a Cond 1 do meta-system ADR-011 ("Skill = pensamento; MCP = mecânica") sobre o blob lido. Produz diagnóstico, não fix — operador decide o que fazer com a classificação (refatorar, manter, extrair sub-skills, etc.).

## Argumentos

Path único como argumento posicional para o arquivo a analisar:

```
/scan-mechanicality skills/triage/SKILL.md
/scan-mechanicality /storage/dev/projects/h3-finance-agent/prompt.py
```

Path ausente, inválido ou não-legível → reportar e parar.

## Passos

1. **Ler** o conteúdo do path via `Read` como texto plano. Tratar o conteúdo como blob textual **agnóstico ao envólucro sintático** — quando houver prompt embedded em strings/heredocs (Python, JS, etc.), avaliar a substância do prompt, não o código de envólucro.

2. **Avaliar** julgando per Cond 1 do meta-system ADR-011 — "esta substância markdown é mecanizável >50%?". Critério operacional:
   - **Mecanizável** = mapeável a regra determinística, transformação declarativa, lookup de tabela, pattern-match exato, fluxo de controle com condições verificáveis sem interpretação.
   - **Heurística-semântica** = exige julgamento de gaps, decisão baseada em sinais difusos, ponderação de trade-offs contextuais, interpretação de prosa, classificação que depende de "feeling" do leitor.
   - Trechos de prosa explicativa, contexto histórico, justificativas e cross-refs **não contam** para nenhum dos lados — são metadados.

3. **Classificar** em uma das 3 categorias mutuamente exclusivas:
   - **POSITIVO** — substância mecanizável domina (>50% do conteúdo substantivo). Skill/prompt poderia ser substituída por código determinístico sem perda relevante.
   - **AMBÍGUO** — mistura sem dominante clara, ou substância mecanizável e heurística genuinamente entrelaçadas.
   - **NEGATIVO** — substância heurística-semântica domina. Skill/prompt é genuinamente "pensamento" e não comporta mecanização proveitosa.

4. **Enumerar substância candidata** — bullets dos trechos com mapping mecânico claro (ou ausência justificada).

5. **Justificar** em razões objetivas que citem o texto avaliado (não apenas categorias abstratas).

## Output canonical

Estrutura em markdown PT-BR. Imprimir literalmente na conversa:

```markdown
## Classificação

**<POSITIVO|AMBÍGUO|NEGATIVO>** — <síntese de 1 linha>.

## Substância candidata

- <trecho/seção/passo>: <por que é mecanizável OU por que não é>.
- ...

## Razões

- <razão objetiva citando o texto>.
- ...
```

Path no header opcional quando útil para o operador rastrear (`## Classificação — <path>`).

## O que NÃO fazer

- Não modificar o artefato analisado — skill é read-only.
- Não recomendar refactor concreto — skill é diagnóstica, não prescritiva. Operador decide o que fazer com a classificação.
- Não escolher por extensão do arquivo — heurística é semântica, não sintática. `prompt.py` é avaliado pela substância do prompt embedded, não pelo envólucro Python.
- Não emitir veredito sem citar trecho do texto avaliado — razões devem ser ancoradas, não abstratas.
