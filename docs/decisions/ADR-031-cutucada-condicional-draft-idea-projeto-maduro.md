# ADR-031: Cutucada condicional em /draft-idea para projeto maduro

**Data:** 2026-05-15
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-027](ADR-027-skill-draft-idea-elicitacao-product-direction.md) — define o sub-fluxo de presença da skill `/draft-idea` (`ausente → one-shot full; presente → update seção-a-seção`). Este ADR é **sucessor parcial**, refinando o caso `ausente` para distinguir projeto novo (cristalização inicial legítima) de projeto maduro (onde `IDEA.md` ausente pode mascarar uso indevido para feature).
- **Investigação:** sessão CC de 2026-05-15 rodou `/draft-idea` no toolkit (versão 2.8.1) com argumento descrevendo feature ("ferramenta de chaveamento de contexto entre sessões"); a skill gravou `IDEA.md` monograficamente sobre a feature, regredindo a discoverability do papel `product_direction` definido em CLAUDE.md como direção-do-projeto-inteiro.
- **Plano:** [docs/plans/draft-idea-cutucada-projeto-maduro.md](../plans/draft-idea-cutucada-projeto-maduro.md) — materializa a implementação (passo 1.5 da skill + refinamento do papel no CLAUDE.md).

## Contexto

ADR-027 estabeleceu predicado de chaveamento **simples** para a skill `/draft-idea`: presença do `IDEA.md` decide modo de operação (`ausente → one-shot full; presente → update seção-a-seção`). O predicado funciona em projeto novo onde `ausente` significa "primeira cristalização da direção". Falha em **projeto maduro** onde `IDEA.md` nunca foi escrito — o argumento da skill pode descrever feature/iniciativa local em vez de direção-do-projeto, e a skill grava `IDEA.md` monograficamente sobre a feature, regredindo a discoverability do papel `product_direction` (que [CLAUDE.md → "The role contract"](../../CLAUDE.md#the-role-contract-load-bearing) carrega como "direção do projeto como um todo, não feature/iniciativa local"). Sessão CC de 2026-05-15 materializou exatamente esse modo de falha (ver Origem).

## Decisão

**Mudar o predicado de chaveamento da skill `/draft-idea` de `presença(IDEA.md)` para `(presença(IDEA.md), maturidade(projeto))`.** Modo update permanece inalterado (não consulta maturidade — decisão implícita pela presença do arquivo); modo one-shot ganha gate de cutucada quando o projeto é maduro **ou ambíguo**.

Razões objetivas:

- **Predicado bidimensional resolve a regressão sem ampliar superfície.** Update já tem decisão implícita; one-shot é o único caminho que precisa de defensividade. Passo 1.5 novo é cirúrgico — não toca passos 2/3.
- **Critério mecânico de maturidade = semver ≥ 1.0.0 com cláusula default-conservadora.** Versão extraída de `version_files` declarado no bloco `<!-- pragmatic-toolkit:config -->`. Ambiguidade (parse failure, formato não-semver, multi-arquivo divergente, `version_files` ausente/null) cutuca mesmo assim — falso positivo (cutucada extra) é menos custoso que falso negativo (regressão como a desta sessão).
- **Parser cobre 4 formatos (JSON/TOML/YAML/XML-POM)** — cobertura mínima viável para consumers típicos do toolkit. Outros formatos caem em ambíguo (não silente). Single-signal por simplicidade — alternativa `decisions_dir populado` descartada (ver Alternativas). Detalhe das chaves canonical vive em `skills/draft-idea/SKILL.md` § passo 1.5.
- **Description do papel `product_direction` em CLAUDE.md permanece universal** (sem caveat sobre o critério mecânico). Doutrina (regra do papel) e mecânica (gatilho de detecção) ficam loose-coupled: o critério pode evoluir sem editar CLAUDE.md.

## Consequências

### Benefícios

- A regressão observada em 2026-05-15 não se repete em projetos canonical (toolkit `2.8.1`, consumers Python/Java/Node maduros).
- Gate determinístico em projeto maduro: enum `Direção` ancora a decisão em momento explícito, eliminando deriva editorial.
- Parser autocontido na skill: nenhuma dependência interna entre `/draft-idea` e `/release` (que também consome `version_files`); cada um carrega sua resolução.
- Anti-padrão registrado em `## O que NÃO fazer` do `skills/draft-idea/SKILL.md` para leitura humana.

### Limitações

- **Cobertura do parser limitada a 4 formatos.** Calver (`2026.05.15`), 0ver deliberado (`0.7.0` mantido por convenção), build metadata complexo (`1.0.0+abc`), versão via git tag (`setuptools_scm`, `hatch-vcs` apontando para placeholder no arquivo) caem em ambíguo ou falso negativo. Default-conservador mitiga a maioria; 0ver deliberado fica como falso negativo aceito (raro em consumers do toolkit; operador pode invocar `/triage` manualmente quando detectar o caso).
- **Cutucadas extras em projetos novos sem `version_files` declarado ou com versão não-parseável.** Operador greenfield paga 1 pergunta extra em troca de robustez. Projeto novo com versão parseável < 1.0.0 (greenfield versionado) é detectado como não-maduro sem ambiguidade e pula a cutucada silenciosamente.

## Alternativas consideradas

### Cutucada sempre (mesmo em projeto novo)

Descartada via cutucada do `/triage` 2026-05-15. Adicionaria pergunta extra em projetos onde a resposta é óbvia (greenfield com argumento de produto), violando flatness sem ganho real.

### Só editorial (refinar `## O que NÃO fazer` + definição em CLAUDE.md sem nova mecânica)

Descartada via cutucada do `/triage` 2026-05-15. Caminho original que falhou nesta sessão — operador (ou agente) lê a regra e ignora porque não há gate mecânico.

### Trocar sinal de maturidade para `decisions_dir populado` (cutucada F2 alternativa b)

Descartada. Sinal mais robusto em projetos sem versionamento semver, mas muda a fonte natural ("projeto maduro" via convenção de versão é mais alinhado com o vocabulário do toolkit que consome `version_files` em outras skills como `/release`). Reabertura futura legítima se evidência empírica mostrar drift entre versão declarada e maturidade real.

### Semver estrito sem cláusula default-conservadora (cutucada F2 alternativa a)

Descartada. Aceitaria falsos negativos como design (calver/0ver passariam direto sem cutucada). Trade-off invertido — a regressão desta sessão foi falso negativo, e default-conservador corrige o viés.

### Description do papel em CLAUDE.md com caveat de maturidade (cutucada F3 alternativa não-universal)

Descartada. Amarração indevida entre doutrina e mecânica; mudaria CLAUDE.md cada vez que o critério evolua.

### Parser delegado a `/release` (cutucada F5 alternativa a)

Descartada. Cria acoplamento entre skills; benefício (DRY) não justifica fragilidade (renomeação de campo em `/release` quebraria `/draft-idea` silenciosamente). Duplicação aceita.

### Parser só JSON (cutucada F5 alternativa b)

Descartada. Cobertura insuficiente para projetos Python (TOML) e Java/Maven (XML/POM) que são consumers prováveis do toolkit. Caminho final cobre 4 formatos.
