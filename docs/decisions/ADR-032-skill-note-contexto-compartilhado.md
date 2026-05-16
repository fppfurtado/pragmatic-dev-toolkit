# ADR-032: Skill /note e store de contexto compartilhado em .claude/local/NOTES.md

**Data:** 2026-05-15
**Status:** Proposto

## Origem

- **Decisão base:** [ADR-005](ADR-005-modo-local-gitignored-roles.md) — define modo local-gitignored como padrão para state privado/efêmero, cobrindo 3 roles do path contract (`decisions_dir`/`backlog`/`plans_dir`) com canonical default e modo local opcional. Este ADR é **sucessor parcial** que **estende** ADR-005 para uma nova categoria: store doutrinário fixo non-role em `.claude/local/`, sem canonical (privacidade por design) e sem schema declarável. Segue precedente da entrada `(plugin-internal) | .worktreeinclude` na tabela "The role contract".
- **Investigação:** sessão CC 2026-05-15 — pivote de `/draft-idea` (descartado por ser feature em projeto maduro, regressão tratada pelo ADR-031) para `/triage` direto. Operador relatou pain real cross-project: investigação em `/storage/3. Resources/Projects/tjpa/pje-2.1` que se estendeu para `connector-pje-mandamus-tjpa` (sessão `pje-issue-1920`) — recopia manual entre sessões.
- **Plano:** [docs/plans/skill-note-contexto-compartilhado.md](../plans/skill-note-contexto-compartilhado.md) — materializa a implementação (skill nova `/note`, catálogo, ADR).

## Contexto

Dev solo operando ≥3 sessões Claude Code em paralelo perde frescor mental do contexto entre sessões. A memory nativa do Claude Code é **per-project** (path-encoded em `~/.claude/projects/<encoded>/memory/`) e **conversational** (auto-gravada com types `user|feedback|project|reference`). Cobre insights internos por-projeto bem; **não cobre cross-project**. Pain real reportado pelo operador em 2026-05-15: investigação em `/storage/3. Resources/Projects/tjpa/pje-2.1` que se estendeu para `connector-pje-mandamus-tjpa` (sessão `pje-issue-1920`) exigiu recopia manual de contexto entre sessões.

Critérios de sucesso (elicitação 2026-05-15):

1. Recuperação seletiva de info-chave (não tudo o que aconteceu — apenas o que operador ou Claude apontam como chave) sem reler N arquivos nem a sessão inteira.
2. Acesso cross-project **referenciável** (não-automático): operador ou Claude pode citar o path durante a conversa.
3. Fricção menor que ganho de re-contextualização.

[ADR-004](ADR-004-state-tracking-em-git.md) moveu state vivo (in-flight) para git/forge mas preservou `## Concluídos` como registro editorial append-only. NOTES.md cai na mesma categoria preservada — não é state competitivo (sem ciclo de merge artifact entre sessões paralelas), é registro de contexto cognitivo cross-session. Sem fonte em git/forge equivalente (sessões CC paralelas + cross-project não derivam de PRs/branches), o store mora em arquivo.

## Decisão

**Criar a skill `/note <conteúdo>` que faz append timestampado em `.claude/local/NOTES.md`** — store doutrinário fixo non-role, local-gitignored por design.

Razões objetivas:

- **Store em `.claude/local/NOTES.md` modo local-gitignored** (Q1=B). Path fixo doutrinário, non-role. Por-projeto, não-versionado. Atendido critério #2 do operador via referência conversacional (não-automático).
- **Captura operador-driven via skill `/note`** (Q2=A). Curadoria sustentável — operador chama explicitamente quando algo é chave. Claude pode informar em prosa *"vale uma nota?"* em marcos óbvios, sem virar enum. Atende critério #1 (recuperação seletiva, não inundação).
- **Extensão de ADR-005 para categoria nova "store doutrinário fixo non-role"**. ADR-005 § Decisão lista 3 roles do path contract com canonical default e modo local opcional. NOTES.md é qualitativamente diferente: local **por design** (canonical committed vazaria privacidade), sem alternativa de path, sem schema declarável. Segue precedente da entrada `(plugin-internal) | .worktreeinclude` na tabela "The role contract" — entrada non-role doutrinária. Materializado por uma linha nova na mesma tabela para `(plugin-internal) | .claude/local/NOTES.md`.
- **Cross-project read como fenômeno conversacional**. Skill `/note` é pura gravação; sem mecanismo de leitura ou busca. Quando operador menciona NOTES.md de outro projeto sem path absoluto (caso normal: *"olha NOTES.md de pje-2.1"*), Claude propõe candidato usando contexto da conversa (cwd, projetos já acessados, menções) e operador confirma ou fornece path. Em ambiguidade verdadeira (múltiplos projetos com nome similar), Claude lista candidatos via prosa. Sem auto-discovery agressivo, sem skill complementar de leitura/busca. Atende critério #3 (fricção mínima).
- **Complementa memory nativa CC** (não substitui). Memory cobre per-project insights conversacionais auto-gravados via types `user|feedback|project|reference`. `/note` cobre cross-project registro intencional do operador em markdown corrido com timestamps. Outputs distintos, escopos distintos. Coexistem sem coordenação mecânica.
- **Skill independente de CLAUDE.md / role contract**. Frontmatter sem `roles:` per ADR-003 § Schema (ambas listas vazias autorizam omitir). Usável em qualquer git repo. Cutucada de descoberta ([ADR-017](ADR-017-cutucada-uniforme-descoberta-config-ausente.md) / [ADR-029](ADR-029-cutucada-descoberta-cobre-claude-md-ausente.md)) não aplica.

## Consequências

### Benefícios

- Cross-session e cross-project resolvidos para dev-solo workflow. Caso real `pje-issue-1920` deixa de exigir recopia manual.
- Curadoria sustentável: store não inunda porque captura é explícita. Operador controla o que entra.
- Estende doutrina existente sem inflar schema do path contract — categoria nova (non-role doutrinário) ao lado de `.worktreeinclude`, sem promover `notes` a role.
- Entrada `(plugin-internal) | .claude/local/NOTES.md` na tabela "The role contract" é discoverable para autores de skills futuras que considerem outros stores não-role.
- Skill usável em qualquer git repo, sem dependência de `CLAUDE.md` ou bloco config. Adoção zero-overhead.

### Limitações

- **Cross-project requer referência explícita validada pelo operador.** Fluxo conversacional pode ser mais longo em projetos com nomes ambíguos (vários `pje*` no filesystem). Trade-off aceito por preservar simplicidade da skill (sem path discovery).
- **Per-project store sem index global.** Não há mecanismo para listar todos os NOTES.md em todos os projetos do operador. Reabertura legítima se atrito real surgir (skill `/notes-find` agregando paths conhecidos, por exemplo).
- **YAGNI deliberado sobre leitura, busca e sincronização.** Skill é pura gravação. Operador lê via Read nativo, busca via grep do CC, e não há sincronização entre NOTES.md de projetos relacionados. Drift entre projetos é responsabilidade editorial do operador.
- **Hook auto-captura descartado.** Operadores que prefiram captura automática (sem skill explícita) ficam sem caminho — preferência por curadoria prevalece. Reabertura se grupos de uso real demandarem.

## Alternativas consideradas

### Cross-project em `~/.claude/notes/` (Q1 alternativa A)

Descartada via cutucada Q1 do `/triage` 2026-05-15. Cross-project natural (atravessa projetos sem referência), mas: (i) cria infra paralela à memory nativa CC sem reuso doutrinário; (ii) viola "extensão do plugin" (operador exigiu como restrição) ao introduzir convenção fora do repo; (iii) ganho automático cross-project não é exigência — critério #2 aceita referência explícita.

### NOTES.md committed no repo (Q1 alternativa C)

Descartada. Versionado expõe contexto privado (anotações de dev, info sensível) ao publicar. Risco real em repo open-source. Privacidade por design exige local-gitignored.

### Claude propõe cutucada de captura mid-conversa (Q2 alternativa B)

Descartada. Menos fricção que `/note` explícito, mas ruído potencial alto: Claude propõe em momento errado, atrapalha fluxo. Plus depende de Claude detectar bem "info-chave" — incerto. Curadoria via skill explícita é mais previsível.

### Hook lifecycle Stop com auto-captura (Q2 alternativa C)

Descartada. Zero fricção, zero curadoria — sumariza sessão inteira sem filtrar. Inunda o store com lixo. Operador perde sinal no ruído. Contradiz critério #1 (recuperação seletiva).

### Promover `notes` a role no path contract (F2 alternativa b)

Descartada. Schema novo (`paths.notes: local | null`) seria cerimônia para um caso singular doutrinário sem alternativa de path. Não há valor canonical possível (committed vaza), não há configuração que o operador faria. Extensão de categoria non-role (escolhida) preserva o caráter doutrinário sem inflar schema.

### Sempre exigir path absoluto para cross-project read (F4 alternativa a)

Descartada. Determinístico mas atrito alto — operador escreveria `/storage/3. Resources/Projects/tjpa/pje-2.1/.claude/local/NOTES.md` em cada referência. Quebra critério #3.

### Claude infere candidatos via path discovery (F4 alternativa b)

Descartada. Não há infra de discovery cross-project; qualquer heurística (`~/Projects/*/`, `find /storage/.../`) é específica do ambiente do operador, frágil. Plus inverte o controle (skill adivinha antes do operador confirmar) e Read pode operar em arquivo errado. Fenômeno conversacional (escolhido) reusa raciocínio do Claude sem novo código de discovery.
