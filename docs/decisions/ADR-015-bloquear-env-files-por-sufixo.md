# ADR-015: Bloquear env-files por sufixo `.env`, não apenas dotfile

**Data:** 2026-05-10
**Status:** Proposto

## Origem

- **Investigação:** smoke-test do plugin no projeto Java PJe (TJPA) reproduziu cenário em que `envs/1g.env` — contendo credenciais reais de DB — passou sem bloqueio pelo `block_env.py`. Registro completo em `.claude/pragmatic-toolkit-validation.md` do PJe, achado #1 da fase 1.

## Contexto

O hook `hooks/block_env.py` (PreToolUse `Edit|Write`) é a primeira linha de defesa contra edits acidentais em arquivos que contêm segredos. Hoje o predicado (linha 32) só casa o padrão **dotfile**:

```python
if base == ".env" or (base.startswith(".env.") and base != ".env.example"):
```

Cobre `.env`, `.env.production`, `.env.local`, etc., com exceção literal para `.env.example` e os sufixos de template em `TEMPLATE_SUFFIXES`.

Essa heurística reflete convenção forte de Python/Node, onde projetos têm tipicamente um único `.env` na raiz. Outros ecossistemas usam **env-file por instância**, com nome no formato `<nome>.env`:

- Java legacy: `envs/1g.env`, `envs/2g.env`, `envs/1g.integ.env` (PJe/TJPA, visto na fase 1).
- PHP, Rails, Spring Boot e variantes com configuração externalizada por ambiente.

Arquivos nesse formato **escapam do regex atual** e edits são aceitos sem bloqueio. Quando o conteúdo são segredos reais (caso do PJe), o gate falha silenciosamente.

Existe defesa em camadas via `block_gitignored.py` (em `main`, ainda sem release): cobre indiretamente quando `*.env` está em `.gitignore` do consumidor. Mas é cobertura colateral — depende da política do consumidor, não declara intenção do plugin. O `block_env.py` precisa ter política própria sobre o que é um env-file.

## Decisão

Estender o predicado de `block_env.py` para casar **qualquer arquivo cujo nome termine em `.env`**, preservando as exceções existentes. Após o strip de `TEMPLATE_SUFFIXES`, o hook bloqueia quando o nome:

- termina em `.env` (cobre `.env`, `1g.env`, `production.env`), **ou**
- começa com `.env.` (cobre `.env.production`, `.env.local`),

**exceto** quando termina em `.env.example` (espelha a exceção atual `.env.example` para qualquer prefixo: `1g.env.example`, `production.env.example`).

Cobertura resultante (bloqueia):

- `.env`, `.env.production`, `.env.local` (status quo preservado).
- `1g.env`, `production.env`, `staging.env`, `1g.integ.env` (cobertura nova).
- `.env.jinja`, `1g.env.tmpl`, `production.env.j2` — templates **do env-file principal** continuam bloqueando após o strip de `TEMPLATE_SUFFIXES` deixar base = `.env`/`<nome>.env`. Defensivo: template do principal pode conter ou produzir secrets ao ser instanciado.

Continua passando (apenas templates *example*):

- `.env.example`, `1g.env.example`, `production.env.example`.
- `.env.example.jinja`, `1g.env.example.tmpl`, `production.env.example.j2` — templates dos próprios *example*-templates passam, pois após o strip a base é `*.env.example`.

## Consequências

### Benefícios

- Gate cobre convenção `<nome>.env` real em Java/PHP/Rails/legacy, fechando classe de falha demonstrada em projeto consumidor.
- Política do hook fica explícita: "qualquer arquivo cujo nome termine em `.env` é env-file". Operador externo pode auditar sem ler o regex.
- Defesa não depende mais de `.gitignore` do consumidor cobrir `*.env`.

### Trade-offs

- Risco teórico de falso-positivo: arquivo cujo nome termine em `.env` sem ser env-file. Improvável dada a força da convenção — o sufixo `.env` é signal-rich.
- Operador legítimo que precise editar (rotação de credencial, etc.) tem caminhos conhecidos: editar via `*.env.example` versionado + processo de deploy, override pontual fora do Claude, ou pedir bypass explícito.

### Limitações

- Heurística continua sobre nome de arquivo; não inspeciona conteúdo. Arquivo com `KEY=VALUE` que não termine em `.env` continua escapando (status quo, sem ambição de cobrir).
- Carve-out de `.claude/` do `block_gitignored.py` ([ADR-005](ADR-005-modo-local-gitignored-roles.md), `hooks/block_gitignored.py:64-66`) **não** se aplica a `block_env.py`. Política de env-files é universal por design — segredos não ganham passe livre por estarem sob território do operador. Cenário concreto: `.claude/local/secrets/1g.env` é bloqueado, mesmo que o restante do conteúdo sob `.claude/` seja gerido localmente pelo operador. Editar `*.env` legítimo nesses contextos exige os caminhos descritos em Trade-offs (template versionado, override fora do Claude, bypass explícito).

## Alternativas consideradas

### (a) Manter dotfile-strict

Status quo. Descartado: deixa `<nome>.env` exposto em ecossistemas onde isso é a convenção dominante. Risco real reproduzido no PJe.

### (b) Sufixo `.env` + restrição de diretório

Bloquear apenas quando dentro de `envs/`, `env/`, `config/` etc. Descartado: aumenta complexidade (hardcode de paths? configurável?) sem benefício claro. A convenção `*.env` como env-file é forte o suficiente para tratar todos como bloqueáveis por default.

### (c) Allowlist explícita configurável via `pragmatic-toolkit:config`

Operador declara paths sensíveis no bloco YAML do CLAUDE.md (`paths.env_files: [...]`). Descartado: move complexidade para o consumidor; default precisa cobrir 99% dos casos sem config. Pode ser feature futura sob outro ADR se atrito real surgir.

### (d) Inspeção de conteúdo do arquivo

Detectar marker de template no conteúdo (placeholders `${VAR}`, `{{var}}`, valores vazios) e liberar arquivos não-instanciados. Seria ponte natural com a Limitação "não inspeciona conteúdo". Descartado:

- **Custo no hot path**: hook é PreToolUse com timeout 10s (`hooks.json:7`) e hoje opera só sobre filename. Adicionar I/O e parsing introduz latência em cada `Edit`/`Write` do consumidor.
- **Markers heterogêneos**: cada stack tem convenção de template diferente (`${VAR}`, `{{var}}`, `<value>`, valor-vazio após `=`). Cobrir bem exige lista grande de regras; cobrir mal gera falso-negativo (libera segredo) e falso-positivo (bloqueia template).
- **Ganho marginal**: arquivos de template já levam sufixo (`.example`, templates de `TEMPLATE_SUFFIXES`) e passam pelas exceções existentes. O caso que justificaria (d) é o de arquivos sem sufixo e com placeholder no conteúdo — raro o suficiente para não justificar o custo.

Reabrir se atrito real surgir.

## Gatilhos de revisão

- Falso-positivo recorrente: operador em consumidor reporta arquivo `*.env` que não é env-file e o bloqueio atrapalha workflow legítimo. Limiar prático: ≥2 reports independentes.
- Pedido recorrente para bypass via config: sinal de que (c) viraria pertinente.
- Surgir convenção de naming nova (`*.envrc`, `*.env.encrypted`, etc.) que mereça revisão da política — abrir ADR sucessor em vez de inchar este.
