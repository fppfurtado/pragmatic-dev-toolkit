# ADR-005: Modo local-gitignored para roles do path contract

**Data:** 2026-05-07
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-003](ADR-003-frontmatter-roles.md) — frontmatter declarativo `roles:`. Estabelece 3 trilhos (capture+stop, offer canonical creation, inform+stop) para required ausente. Este ADR adiciona um trilho paralelo: aceitar role como artefato local-gitignored opt-in via path contract.
- **Investigação:** Sessão pós-v1.21.0 reavaliando o contrato `required` por role individualmente. Identificado que `decisions_dir`, `backlog`, `plans_dir` são compartilhados (gitignored mata o ponto), mas o plugin deveria ser aplicável também em projetos que não mantêm essas estruturas no repo (uso individual, scratchpad pessoal).

## Contexto

Skills do plugin (`/triage`, `/new-adr`, `/run-plan`, `/next`) consomem `decisions_dir`, `backlog`, `plans_dir`. Quando o role canonical está ausente, ADR-003 prevê três trilhos:

- Skills com fluxo "Oferecer criação canonical via enum" (`/triage` step 4, `/new-adr` na primeira invocação) propõem criar em path canonical.
- Skill com fluxo "Inform and stop" para quando role essencial está ausente.
- Operador pode declarar `paths.<role>: null` ("não usamos esse papel") — skill segue sem o role, mas perde a função correspondente.

Lacuna: **nenhum trilho atual aceita "tenho esses artefatos mas só localmente, sem commitar"**. O plugin se aplica integralmente apenas a projetos que adotam a estrutura no repo.

Casos onde uso local faz sentido:

- Dev individual em projeto onde a equipe não usa ADRs/planos no repo, mas o operador quer adotar pragmáticamente para seu próprio fluxo.
- Scratchpad pessoal: backlog próprio paralelo ao do projeto.
- Plugin como ferramenta de organização cognitiva sem impor estrutura ao projeto consumidor.

Restrição editorial chave: artefatos locais são **invisíveis aos colaboradores**. Mensagens de commit e descrições de PR que referenciam ADR/plano/linha-de-backlog quebram quando esses arquivos não estão no repo.

`test_command` fica fora do escopo deste ADR — sua condicionalidade (required quando plano não tem `## Verificação end-to-end`, informational quando tem) já é tratada corretamente em ADR-003. `version_files`, `changelog` são opt-in via path contract atual. `ubiquitous_language`, `design_notes`, `product_direction` são informational em todas as skills, ausência já é tolerada.

## Decisão

**Adicionar modo `local` ao path contract para `decisions_dir`, `backlog`, `plans_dir`.** Sintaxe:

```yaml
paths:
  decisions_dir: local
  backlog: local
  plans_dir: local
```

### Comportamento

- Skill cria/lê o artefato em path gitignored sob `.claude/local/<role>/`. Paths concretos:
  - `decisions_dir: local` → `.claude/local/decisions/`
  - `backlog: local` → `.claude/local/BACKLOG.md`
  - `plans_dir: local` → `.claude/local/plans/`
- Resolution protocol ganha trilho paralelo: role declarado `local` → skill usa o path local diretamente, sem ofertar canonical creation, sem informar+parar. Path local é replicado para worktrees pelo `.worktreeinclude` (já cobre `.claude/`).
- **Regra de não-referenciar:** quando role está em modo `local`, skills geram mensagens de commit, descrições de PR e nomes de branch sem citar o artefato em modo local (ID do ADR, slug do plano, texto da linha do backlog não aparecem). Em modo canonical (default), comportamento atual de referência preservado.

### Mecânica de inicialização

Quando role declarado em modo `local` é resolvido pela primeira vez na invocação:

1. **Garantir diretório:** `mkdir -p .claude/local/<role>/` se ausente. Operação silenciosa.
2. **Probe de gitignore:** verificar se o path está coberto pelo `.gitignore` do projeto via `git check-ignore -q .claude/local/<role>/.probe`. Coberto → seguir silente. Não coberto → disparar gate.
3. **Gate `Gitignore`:** mostrar mensagem explícita ("modo `local` foi declarado mas `.claude/local/` não está coberto pelo `.gitignore` do projeto — adicionar entrada para garantir que artefatos não sejam commitados?"). Opções: `Adicionar entrada` (skill anexa `.claude/local/` ao `.gitignore` do projeto) / `Cancelar` (skill recusa modo local nesta invocação e informa risco).

Plugin **nunca toca em `.claude/` raiz** — território do Claude Code, fora do escopo do plugin. Probe roda uma vez por invocação (não a cada operação). Subsequentes invocações na mesma sessão herdam a resolução.

### Razões

- **Aplicabilidade ampliada:** plugin vira utilizável em projetos onde a equipe não adotou as estruturas no repo, sem impor imposição estrutural.
- **Trade-off explícito:** ADR perde propriedade compartilhada (registro coletivo); aceito quando o uso é individual/scratchpad.
- **Trilho aditivo, não destrutivo:** modo canonical (default) inalterado. ADR-003 § "Default behavior for absent required role" continua válido para casos onde role é canonical-ausente sem declaração local.
- **Regra de não-referenciar evita commit órfão:** mensagem de commit citando `ADR-005` que ninguém vê confunde reviewer/colaborador.

## Consequências

### Benefícios

- Plugin aplicável em projetos que não adotam ADRs/planos/backlog no repo.
- Operador escolhe explicitamente nível de compartilhamento via path contract — sem flag implícita.
- Resolution protocol estende sem quebrar comportamento canonical.
- Worktree replication via `.worktreeinclude` já cobre `.claude/` — sem nova mecânica.

### Trade-offs

- Skills ganham branch "modo local" na prosa — leve aumento editorial (cada skill afetada explicita o trilho).
- Regra de não-referenciar exige consistência entre skills geradoras de commit/PR (`/triage`, `/run-plan`). `/release` fica fora — recusa modo local para `version_files`/`changelog`.
- Artefato local não rastreável pós-fato em outras máquinas — operador é responsável por backup/sincronização individual.

### Limitações

- Modo `local` não interopera com canonical — operador não pode ter ADRs versionados E ADRs locais no mesmo projeto sem fricção. Por design: simplicidade vence flexibilidade.
- Path concreto (`.claude/local/<role>/`) é hardcoded — sem opção de customizar destino do modo local. Reavaliar se atrito surgir.
- `/release` em modo local fica anômalo (release pessoal não-publicada faz pouco sentido) — release segue exigindo `version_files` e `changelog` em modo canonical; modo local não se aplica a esses roles.

## Alternativas consideradas

### Manter status quo (`paths.<role>: null` + skill desativada)

Rejeita o caso de uso ("uso o plugin localmente sem commitar"). Skill desativada perde funcionalidade que o operador quer usar — operador acaba criando os artefatos manualmente sem ajuda da skill.

### Role paralelo por role (`paths.local_decisions_dir: <path>`)

Dobra superfície do schema sem ganho. Operador escolheria entre canonical e local-paralelo em chaves separadas; nada nos forçaria a tratar uniformemente. Modo `local` como valor é mais expressivo.

### Modo "local" implícito por convenção (artefato em path gitignored sem declaração)

Opacidade — operador veria ADR criado em `.claude/local/decisions/` mas não saberia que está local. Declaração explícita no path contract é mais legível e evita surpresa.

### `test_command` como required absoluto + demais como local-opt-in

Considerado e descartado durante a triagem desta decisão. Quebra o caso self-hosting de repos sem suite (como este próprio plugin, que declara `test_command: null`). A invariante real do `/run-plan` é "critério de done auditável" — `test_command` resolvido **ou** plano com `## Verificação end-to-end` —, e ambos os caminhos são legítimos. ADR-003 já codifica isso corretamente como condicional; manter inalterado.

## Gatilhos de revisão

- 3+ projetos consumidores adotam modo `local` para algum role → reavaliar se o path concreto (`.claude/local/<role>/`) deveria ser customizável.
- Aparecer caso onde role precisa coexistir canonical + local no mesmo projeto → reabrir limitação atual.
- Skill nova introduz role passível de modo local não previsto aqui → revisar escopo deste ADR.
- Regra de não-referenciar gerar atrito (operador esquece, reviewer flag incorretamente) → considerar mecanismo de detecção automática (probe do path contract antes de redigir mensagem).

## Implementação

Commits da branch `roles-local-mode` que estenderam o plugin para suportar esta decisão (skills, CLAUDE.md, docs/install.md, BACKLOG). Útil para rastreabilidade ADR ↔ código, especialmente em modo `local` onde a regra de não-referenciar impede o caminho inverso (commit → ADR):

- [`6fc3749`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/6fc3749) feat(claude.md): add local mode to path contract schema and resolution
- [`3c0ce13`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/3c0ce13) docs(adr-003): cross-ref ADR-005 in Limitações
- [`6e3ffdd`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/6e3ffdd) feat(triage): branch local mode + per-role no-reference rule
- [`a4721e0`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/a4721e0) feat(new-adr): note local mode resolution
- [`40ffb6b`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/40ffb6b) feat(run-plan): branch local mode with cross-mode handling
- [`6c2e64e`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/6c2e64e) feat(next): branch local mode for backlog reading and persistence
- [`3983774`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/3983774) feat(release): refuse local mode for version_files and changelog
- [`e3cc513`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/e3cc513) docs(install): document `local` value in path contract schema
- [`4e659a4`](https://github.com/fppfurtado/pragmatic-dev-toolkit/commit/4e659a4) chore(backlog): move roles-local-mode line to Concluídos
