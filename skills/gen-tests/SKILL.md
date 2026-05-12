---
name: gen-tests
description: Gera arquivo de teste para módulo, função ou descrição livre, com idioms da stack do projeto consumidor (Python e Java suportadas). Use quando o operador pedir testes.
disable-model-invocation: false
roles:
  informational: [ubiquitous_language, design_notes]
---

# gen-tests

Workflow de scaffolding de testes stack-agnóstico. Detecta a stack do projeto consumidor por marker e despacha para o sub-bloco com convenções idiomáticas daquela stack. Idioms vivem nos sub-blocos do próprio SKILL.md (per [ADR-008](../../docs/decisions/ADR-008-skills-geradoras-stack-agnosticas.md) — geradores stack-agnósticos via dispatch interno).

Princípio: **não exigir TDD estrito; exigir confiança no que vai pra produção**. Cobertura serve à confiança, não a métricas.

Gera arquivo e devolve o controle ao operador. **Não faz commit** — o operador (ou `/run-plan`) commita conforme convenção do projeto.

A skill **não** descobre regras de negócio sozinha — consulta `ubiquitous_language` para identificar invariantes (RNxx) que o alvo exerce. Resolveu "não temos" → cobrir caminho feliz + edge cases que o código realmente trata.

## Argumentos

Categorias de alvo (sintaxe específica em cada sub-bloco):

- Módulo (path do arquivo de produção).
- Função (entry point dentro de um módulo).
- Descrição livre.

Ambíguo ou ausente → perguntar antes de gerar.

## Detecção de stack

Walking ancestors do diretório corrente até encontrar marker:

| Marker | Stack |
|---|---|
| `pyproject.toml` | Python |
| `pom.xml` | Java |

(Stacks futuras adicionam linha + sub-bloco abaixo.)

**Fallback:**

- **Marker ausente** → `AskUserQuestion` (header `Stack`) listando stacks com sub-bloco implementado (hoje `Python`, `Java`).
- **Múltiplos markers** (monorepo) → mesma pergunta, citando os markers detectados como contexto da prosa introdutória.
- **Stack detectada sem sub-bloco** → parar com mensagem `"stack <X> detectada mas sub-bloco ausente em skills/gen-tests/SKILL.md — abrir issue ou contribuir sub-bloco"`.

## Sub-blocos por stack

### Stack: Python

#### Stack assumida

- **pytest** + **pytest-asyncio** com `asyncio_mode = "auto"` (funções `async def` viram testes assíncronos sem decorator).
- **respx** para mock de HTTP (não usar `unittest.mock` para rede).
- **`tmp_path`** para SQLite — não mockar o banco (mock/prod divergence em persistência é caso clássico de bug em produção).
- `pythonpath = ["src", "tests"]` — imports diretos a partir de `src/`.

`pyproject.toml` contradiz alguma premissa (usa `unittest`, sem pytest-asyncio) → parar e reportar antes de gerar.

#### Estrutura

- `tests/unit/` — rápido, sem I/O real, sem rede. Mockar HTTP com `respx`.
- `tests/integration/` — marker `@pytest.mark.integration`. SQLite real via `tmp_path`; fixtures em disco em `tests/fixtures/`.

#### Argumentos

Alvo do teste:

- Módulo: `src/<pacote>/<módulo>.py`
- Função: `src/<pacote>/<módulo>.py::<função>`
- Descrição livre: `"o caso de uso de registrar pagamento"`

#### Passos

1. **Ler o alvo.** `Read` no arquivo, identificar funções públicas e assinaturas. Descrição livre → localizar entry point com `grep`.
2. **Mapear invariantes.** Consultar `ubiquitous_language` e identificar RNs que o alvo exerce. Para cada invariante exercida, gerar **dois testes**: caminho feliz (satisfeita) e violação (deve falhar/recusar). Papel "não temos" → derivar invariantes do próprio código (asserts, raises, validações).
3. **Decidir unit vs integration.** Unit se não toca SQLite nem rede real. Integration se toca SQLite ou exerce pipeline ponta-a-ponta.
4. **Edge cases típicos.** Revisar `design_notes` (peculiaridades de integrações externas). Papel "não temos" → cobrir edge cases que o próprio código trata explicitamente (raises, branches de erro, validações).
5. **Gerar arquivo** em `tests/unit/test_<módulo>.py` ou `tests/integration/test_<módulo>.py`.
6. **Decisão de fixture.** Se alguma fixture é usada por mais de um teste ou módulo, cutucar via `AskUserQuestion` (header `Fixture`) com opções `No próprio arquivo de teste (Recommended)` / `Em conftest.py`. `description` carrega trade-off (isolamento vs. compartilhamento).

#### Padrões úteis

- Tempo: injetar data de referência explícita — não depender de `datetime.now()`.
- Identificadores externos repetidos (ex.: FITID OFX): chave determinística (hash de campos estáveis), não `uuid4()`.
- Nomes de teste no idioma do projeto, alinhados ao vocabulário ubíquo. Ex.: PT `test_pareamento_recusa_movimentos_sem_data_liquidacao`, EN `test_matching_rejects_entries_without_settlement_date`.
- Asserts diretos: `assert resultado == esperado`. Evitar pytest-mock e libs auxiliares.

#### Validação

```bash
python -m pytest <arquivo_gerado> -x --no-header
```

(Ou `uv run pytest ...` se o projeto usa `uv`.)

Não entregar teste vermelho. Falha por bug no código alvo (não no teste) → reportar ao operador em vez de "consertar" o teste.

#### O que NÃO fazer (Python)

- Não mockar SQLite — usar `tmp_path`.
- Não usar `unittest.mock` para HTTP — usar `respx`.

### Stack: Java

#### Stack assumida

- **JUnit 5** (Jupiter API): `org.junit.jupiter.api.Test`, `org.junit.jupiter.api.Assertions.*`.
- **Mockito** para mock de dependências injetáveis (não mockar tipos de JDK como `List`/`Map`; não mockar `Connection`/`ResultSet` — sintoma de design ruim sob teste).
- Layout Maven padrão: `<módulo>/src/main/java/<package>/`, `<módulo>/src/test/java/<package>/`.
- **Maven Surefire** (default) descobre testes por convenção de nome — `*Test.java` (unit) roda em `mvn test`; `*IT.java` (Failsafe) ou `*IntegrationTest.java` em fase separada.

`pom.xml` contradiz alguma premissa (`<dependency>` em `junit:junit:4.*` sem `junit-jupiter`; uso de TestNG; PowerMock) → parar e reportar antes de gerar. JUnit 4 entra como gatilho de revisão da skill se aparecer em consumer real — v1 cobre JUnit 5 only.

**Não cobrir** aqui idioms Spring/Spring Boot (`@SpringBootTest`, `@WebMvcTest`, `MockMvc`, `@DataJpaTest`) — escopo deste sub-bloco é Java puro + Maven legacy/Seam. Spring entra como sub-bloco futuro se demandar.

#### Estrutura

- **Unit** (`*Test.java`) — rápido, sem I/O real, sem rede, sem DB. Mockar dependências injetáveis com Mockito.
- **Integration** (`*IT.java` ou `*IntegrationTest.java` conforme convenção do projeto) — toca DB real (H2 in-memory ou Testcontainers), rede real (WireMock/MockWebServer), ou exerce pipeline ponta-a-ponta. Pode estar excluído do default `mvn test` por design (PJe exclui `*IntegrationTest.java` via Surefire excludes); confirmar com o operador antes de gerar nessa categoria.

#### Argumentos

Alvo do teste:

- Classe: `<módulo>/src/main/java/<package>/<Classe>.java`
- Método: `<módulo>/src/main/java/<package>/<Classe>.java::<método>`
- Descrição livre: `"o caso de uso de remeter manifestação processual"`

`<módulo>` é o nome do diretório do módulo Maven (ex.: `pje-web`, `pje-comum`). Projeto single-module → omitir.

#### Passos

1. **Ler o alvo.** `Read` no arquivo, identificar métodos públicos e assinaturas. Descrição livre → localizar entry point com `grep`. Verificar encoding do arquivo (`<sourceEncoding>` em `pom.xml`) — se ISO-8859-1, preservar.
2. **Mapear invariantes.** Consultar `ubiquitous_language` e identificar RNs que o alvo exerce. Para cada invariante exercida, gerar **dois testes**: caminho feliz (satisfeita) e violação (deve falhar/recusar via `assertThrows` ou retorno explícito). Papel "não temos" → derivar do próprio código (`throw new ...`, validações, branches de erro).
3. **Decidir unit vs integration.** Unit se não toca DB real, file system, ou rede. Integration se toca. Em monolitos com `Seam`/CDI, classes com `@In`/`@Inject` exigem inversão da injeção via constructor ou setter para mock; se a classe usa lookup de contexto Seam direto (`Component.getInstance(...)`), considerar refactor antes do teste — flagar ao operador.
4. **Edge cases típicos.** Revisar `design_notes`. Sem → cobrir branches de erro/`throw` explícitos no código. Para classes que tocam Hibernate, atenção a lazy-loading (`LazyInitializationException` em testes sem sessão aberta).
5. **Gerar arquivo** em `<módulo>/src/test/java/<package>/<Classe>Test.java` (unit) ou `<Classe>IT.java`/`<Classe>IntegrationTest.java` (integration, espelhando convenção observada no projeto).
6. **Decisão de mock-vs-real para dependências.** Se a classe tem ≥1 dependência injetável e ≥1 dependência pode ser substituída por implementação real leve (DTO, value object, repository in-memory), cutucar `AskUserQuestion` (header `Mock`) com opções `Mockito para externos, real para interno (Recommended)` / `Mockito para tudo`. `description` carrega trade-off (fidelidade do teste vs. isolamento puro).

#### Padrões úteis

- Tempo: injetar `Clock` ou `Supplier<Instant>` — não usar `LocalDateTime.now()`/`Instant.now()` direto.
- IDs externos repetidos: chave determinística (hash de campos estáveis), não `UUID.randomUUID()`.
- Nomes de teste no idioma do projeto. JUnit 5 idiomatic é camelCase (`matchingRejectsEntriesWithoutSettlementDate`); `@DisplayName("Pareamento recusa movimentos sem data de liquidação")` complementa quando o nome técnico é longo demais. PJe usa identificadores PT-BR — método pode ser `pareamentoRecusaMovimentosSemDataLiquidacao` para alinhar com vocabulário do código.
- Asserts diretos: `assertEquals(expected, actual)`, `assertTrue(condition)`, `assertThrows(SomeException.class, () -> ...)`. Não introduzir AssertJ/Hamcrest sem necessidade — reduz dep externa.
- Estrutura `Arrange / Act / Assert` (ou `Given / When / Then`) em comentários só quando o teste tem ≥3 passos de setup; teste de 1 linha não precisa.

#### Validação

```bash
# Multi-module
mvn -pl <módulo> test -Dtest=<NomeClasse> -DfailIfNoTests=false

# Single-module
mvn test -Dtest=<NomeClasse> -DfailIfNoTests=false
```

Para integration excluída por padrão (PJe `*IntegrationTest`): override do exclude — `mvn -pl <módulo> test -Dtest=<NomeClasse> -Dsurefire.excludes= -DfailIfNoTests=false`.

Não entregar teste vermelho. Falha por bug no código alvo (não no teste) → reportar ao operador em vez de "consertar" o teste.

#### O que NÃO fazer (Java)

- Não usar PowerMock — sinal de design ruim sob teste (estática/final/private inevitáveis); preferir refatorar para injeção ou marcar como integration.
- Não mockar tipos de JDK (`List`, `Map`, `String`) nem `java.sql.*` (`Connection`, `ResultSet`, `PreparedStatement`) — mockar interfaces de domínio/integração; persistência via DAO/Repository mockado ou H2 in-memory.
- Não cobrir Spring/Spring Boot test idioms — fora de escopo do sub-bloco v1.

## O que NÃO fazer

- Não testar invariantes que o código alvo não exerce — só comportamento real do código.
