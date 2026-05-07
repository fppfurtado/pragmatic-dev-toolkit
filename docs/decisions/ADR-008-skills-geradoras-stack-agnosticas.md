# ADR-008: Skills geradoras stack-agnósticas via dispatch interno

**Data:** 2026-05-07
**Status:** Aceito

## Origem

- **Investigação:** Sessão sobre cobertura de teste em features multi-arquivo expôs duas dores em `gen-tests-python`: (i) per-arquivo (N invocações para feature multi-módulo); (ii) per-stack (sufixo obriga lembrar qual variante invocar). A primeira é assinatura; a segunda é doutrinária.
- **Decisão base:** "Convenção de naming" em `docs/philosophy.md` afirma que "Componentes que geram ou executam algo da stack carregam sufixo de stack — sintaxe e comando concreto não têm versão neutra". Convenção foi escrita com um único data point (`gen-tests-python`); este ADR refina o critério distinguindo skills (interface ao operador) de hooks (auto-fira).

## Contexto

A convenção atual cumpre dois papéis:

1. **Acoplamento explícito visível ao operador** — `/gen-tests-python` declara stack no nome.
2. **Multiplexação correta na auto-fira** — hooks dispararem em todo projeto onde o plugin está instalado exigem auto-gating triplo (extensão → marker → toolchain); sufixo é sinal ao autor do plugin de qual stack o componente serve.

Para skills, o papel (1) gera atrito real:

- Operador precisa lembrar sufixo a cada stack nova.
- Cada stack adicional vira proliferação `/gen-tests-python` + `/gen-tests-go` + `/gen-tests-jvm` + ...
- Não há mecanismo declarativo para detectar qual skill aplicar; operador precisa saber a stack do projeto para escolher invocação.

Hooks têm semântica diferente: firam sozinhos em **todo** projeto onde o plugin está instalado. Sufixo + auto-gating triplo é a forma de garantir silêncio fora da stack alvo. Inverter levaria hook genérico a ser ainda mais defensivo — filtrar extensão + marker + toolchain *antes* de qualquer dispatch interno. Mistura níveis (gating de execução vs idiom de stack); mantê-los suffixados preserva a separação.

## Decisão

**Skills geradoras (não hooks) perdem o sufixo de stack.** Idioms de cada stack vivem em sub-blocos por stack dentro do mesmo SKILL.md. A skill detecta stack por marker (idêntico ao auto-gating triplo de hooks: `pyproject.toml` → Python, `build.gradle*`/`pom.xml` → JVM, `package.json` → JS/TS, `Cargo.toml` → Rust, `go.mod` → Go) e despacha para o sub-bloco correspondente.

**Hooks mantêm sufixo de stack** e auto-gating triplo. A separação skill-vs-hook na convenção fica formalizada por este ADR.

### Escopo da inversão

- **Aplica-se:** skills cujo nome carrega `<verb>-<artifact>-<stack>` na tabela atual (`CLAUDE.md` → "Plugin component naming and hook auto-gating"). Hoje, apenas `gen-tests-python`. Skills futuras geradoras seguem o novo padrão (`<verb>-<artifact>` com sub-blocos internos).
- **Não aplica-se:** hooks (`run_pytest_python.py`, futuros `run_gradle_test_java.sh`, etc.) e agents stack-specific (`<role>-<stack>`, hipotéticos hoje).

### Mecânica de detecção e fallback

- **Marker único** detectado → despacha para o sub-bloco da stack identificada.
- **Marker ausente** → skill pergunta ao operador via `AskUserQuestion` (header `Stack`) com as stacks que têm sub-bloco como opções.
- **Múltiplos markers** (monorepo) → mesma pergunta, com aviso explícito dos markers detectados.
- **Stack detectada sem sub-bloco implementado** → skill para com mensagem clara: `"stack <X> detectada mas sub-bloco ausente em skills/<nome>/SKILL.md — abrir issue ou contribuir sub-bloco"`.

### Migração

**Rename atômico** sem shim de compatibilidade (alinha com `CLAUDE.md` → "Avoid backwards-compatibility hacks"). `skills/gen-tests-python/` é excluído e `skills/gen-tests/` criado com sub-bloco Python carregando o conteúdo atual integralmente. CHANGELOG marca breaking. Versão nova de plugin = invocação `/gen-tests` (não mais `/gen-tests-python`).

### Documentação a atualizar

- `docs/philosophy.md` → seção "Convenção de naming" reescrita refletindo a divisão skills (sem sufixo) vs hooks (com sufixo).
- `CLAUDE.md` → tabela em "Plugin component naming and hook auto-gating" atualizada; coluna "Stack-specific" para skills geradoras vira indicador de sub-bloco interno em vez de sufixo.

## Consequências

### Benefícios

- **UX uniforme** entre stacks: operador invoca `/gen-tests` independente do projeto. Memória cognitiva reduzida; descoberta no marketplace simplificada.
- **Escalabilidade**: stack nova adiciona sub-bloco em arquivo existente, não nova skill. Convergência conceitual com hooks (single component, multi-stack) onde a auto-fira não é o ponto.
- **Idioms preservados**: convenções específicas (`respx`, `tmp_path`, `asyncio_mode = "auto"`) ficam fixadas no sub-bloco Python; não dependem de espelhamento de testes existentes (que falha em cold-start) nem da memória do modelo (qualidade variável).

### Trade-offs

- **SKILL.md cresce com cada stack adicional**; lido a cada invocação implica custo de input. Mitigação: sub-blocos curtos e auto-contidos; reavaliar split em sub-skills delegadas se SKILL.md ultrapassar ~500 linhas.
- **Detecção por marker é frágil em monorepo**. Mitigação: pergunta explícita ao operador no fallback.
- **Sem sinal visual de stack-coverage no nome**. Mitigação: `description` da skill enumera as stacks suportadas.

### Limitações

- ADR cobre só skills geradoras. Skills executoras stack-specific (não existem hoje) reabrem o critério caso surjam — sub-bloco interno ou sufixo dependem de saber se idioms vs comando concreto dominam.
- Stack adicionada por contribuidor que desconhece convenções idiomáticas pode degradar resultado. Mitigação editorial: sub-bloco novo entra via PR + revisão por mantenedor.

## Alternativas consideradas

- **Manter status quo (sufixo obrigatório em skills geradoras)** — descartado: cada stack nova exige skill nova; UX não escala; descoberta no marketplace fragmenta.
- **Skill genérica que delega a sub-skills `/gen-tests-python`/`/gen-tests-go`** — descartado: dispersa idioms entre múltiplos arquivos; aumenta superfície de manutenção; dispatch via Skill→Skill tem ergonomia inferior a sub-bloco no mesmo arquivo.
- **Espelhar testes existentes do projeto como style guide (sem sub-blocos fixos)** — descartado: falha em cold-start (projeto novo sem testes); idioms não-óbvios (`respx` vs `unittest.mock`, `tmp_path` para SQLite) não emergem de codebase mínimo.
- **Confiar no modelo para gerar idiomatic sem sub-bloco** — descartado: qualidade variável; convenções específicas precisam ser fixadas em prosa, não na memória pré-treinada.
- **Migração via shim `/gen-tests-python` → `/gen-tests`** — descartado: viola anti-shim do CLAUDE.md; plugin pequeno, blast radius baixo, breaking via CHANGELOG é honesto.

## Gatilhos de revisão

- Surge **skill executora** stack-specific (não geradora) → reavaliar se a separação skill/hook deste ADR cobre o novo caso ou se executores precisam de critério próprio.
- SKILL.md de gerador ultrapassa ~500 linhas com 3+ sub-blocos → reabrir para considerar split em sub-skills delegadas.
- Detecção por marker falha em ≥2 projetos consumidores reais (monorepo, marker ambíguo, falta de marker) → reabrir para considerar declaração explícita de stack via path contract (ex.: `paths.stack: python|go|jvm`).
- Contribuidor adiciona sub-bloco com qualidade inferior aos atuais → sinal de que critério editorial precisa ser explicitado em CLAUDE.md ou de que sub-skills delegadas trazem mais isolamento.
