# Plano — /new-adr clarifica spec "Não inventar" vs "preencher com inputs do operador"

## Contexto

ROADMAP item 9 (commit `b3d2e3d`, último pendente da Onda 2). Resolve zona cinza observada no item 3 desta sessão (criação de ADR-037): `/new-adr` `## O que NÃO fazer` diz literalmente *"Não inventar conteúdo de Contexto/Decisão — quem decide é o operador, a skill só estrutura."*. Mas para ADR-037 (e itens 6+8 que criaram ADR-038/ADR-039 via mesmo pattern), operador já tinha decidido substância via ROADMAP / plano upstream / conversa. Eu julguei e preenchi com base nesses inputs; design-reviewer auditou. Funcionou nas 3 invocações, mas a regra "Não inventar" tem zona ambígua que dependeu de meu julgamento.

Risco editorial: outra invocação (modelo diferente, sessão fresh, contribuidor novo) lendo a regra literalmente produziria ADR vazio com placeholders; `design-reviewer` (per ADR-011 wiring no /new-adr step 5) flagaria como rede de segurança pós-fato, mas o ciclo skill→reviewer→reedição→reviewer é retrabalho desnecessário quando a clarificação no spec corta para skill-correta-na-primeira (skill→reviewer-audita-síntese). Operador também perde tempo manualmente preenchendo o que já tinha decidido em ROADMAP/plano/conversa.

**Mecanismo:** 1 frase adicional no spec do `/new-adr` clarificando: "Preencher com conteúdo derivado de inputs explícitos do operador (ROADMAP, plano upstream, conversa recente). Placeholders apenas quando nenhum input substantivo existir." Distinção: "inventar" = criar substância sem base; "preencher" = sintetizar substância já decidida em outro lugar pelo operador.

Sem novo mecanismo, sem ADR. Refinamento editorial puro — clarifica intenção sem mudar comportamento prescrito (já é o comportamento empírico observado em ADR-037/038/039 desta sessão). `design-reviewer` continua sendo o auditor de drift entre input do operador e conteúdo gerado (per ADR-011 wiring no /new-adr step 5) — clarificação encurta o ciclo, não substitui o auditor.

**Por que edit-direto-no-SKILL.md vs adendo cross-ref em ADR (F1 absorbed via rebuttal de alternativa):** Por ADR-034 a clarificação satisfaz as 4 condições de adendo (decisão central do `/new-adr` intacta + sem categoria nova + sem restrição externa + caráter explicativo) — adendo em ADR-027 (skill paralela com elicitation) ou ADR-026 (mecânica do reviewer no /new-adr step 5) seria caminho doutrinariamente articulável. Mas a regra refinada é **mecânica interna do spec de 1 skill** (`/new-adr`), não doutrina cross-componente — edit textual no SKILL.md preserva fonte única (regra vive onde é consumida); adendo em ADR criaria 2 lugares de leitura para a mesma regra editorial. Precedente: outras regras editoriais de mecânica intra-skill vivem nos respectivos SKILL.md sem espelho em ADR (ex.: heurísticas de gap-clarification de `/triage` step 2, ordem dos bullets de checklist mental). Escolha mantém fronteira ADR-034 nítida: ADRs cobrem doutrina cross-componente; SKILL.md prose cobre mecânica intra-skill.

**ADRs candidatos:** [ADR-027](../decisions/ADR-027-skill-draft-idea-elicitacao-product-direction.md) (skill /draft-idea — adjacente, mesma classe de skill com elicitation/preenchimento de artefato a partir de inputs upstream), [ADR-026](../decisions/ADR-026-criterio-mecanico-absorcao-findings-design-reviewer.md) (mecânica de design-reviewer absorption no /new-adr step 5 — adjacente, audita drift entre input e conteúdo), [ADR-011](../decisions/ADR-011-wiring-design-reviewer-automatico.md) (wiring automático que dispara o auditor).

**Linha do backlog:** plugin: /new-adr clarifica spec "Não inventar" vs "preencher com inputs do operador"

## Resumo da mudança

1 edit em `skills/new-adr/SKILL.md` seção `## O que NÃO fazer`:

Substituir/refinar o bullet atual:

> Não inventar conteúdo de Contexto/Decisão — quem decide é o operador, a skill só estrutura.

Para versão clarificada:

> Não inventar conteúdo de Contexto/Decisão **sem base em input explícito do operador**. Preencher com conteúdo derivado de inputs disponíveis (ROADMAP, plano upstream, conversa recente, entrevista). Placeholders apenas quando nenhum input substantivo existe — quem decide a substância é o operador, a skill sintetiza/estrutura. design-reviewer (per [ADR-011](../../docs/decisions/ADR-011-wiring-design-reviewer-automatico.md)) audita drift entre input e síntese.

Distinção fundamental:
- **Inventar** (continua proibido): criar substância sem base nos inputs disponíveis.
- **Preencher** (permitido e esperado quando há inputs): sintetizar substância já decidida em ROADMAP / plano upstream / conversa em estrutura ADR canonical.

Sem mecanismo novo, sem ADR, sem cross-file edits. Refinamento editorial puro.

## Arquivos a alterar

### Bloco 1 — skills/new-adr/SKILL.md clarifica spec preencher vs skeleton {reviewer: code}

- `skills/new-adr/SKILL.md`: na seção `## O que NÃO fazer`, refinar o bullet existente "Não inventar conteúdo de Contexto/Decisão — quem decide é o operador, a skill só estrutura." para versão clarificada (3 frases) distinguindo "inventar" (proibido — sem base) de "preencher" (esperado quando há inputs do operador em ROADMAP/plano/conversa). Cross-ref a ADR-011 (design-reviewer audita drift).

## Verificação end-to-end

- `grep -n "Preencher com conteúdo derivado" skills/new-adr/SKILL.md` retorna match na seção `## O que NÃO fazer`.
- `grep -n "Placeholders apenas quando" skills/new-adr/SKILL.md` retorna match na clarificação.
- `grep -n "Não inventar" skills/new-adr/SKILL.md` retorna match preservado (regra original mantida, refinada com qualificador "sem base em input explícito").
- `grep -n "ADR-011" skills/new-adr/SKILL.md` retorna ≥1 match (cross-ref ao auditor).
- Inspeção textual: bullet refinado distingue "inventar" (proibido) de "preencher" (esperado quando há inputs); cita 4 fontes de inputs (ROADMAP, plano upstream, conversa recente, entrevista).

## Notas operacionais

- Plano single-block, single-file — sem dependências internas, sem ordem editorial complexa.
- design-reviewer dispatcha automaticamente pré-commit (ADR-011); free-read prioriza ADRs candidatos em `## Contexto`.
- Sem `## Verificação manual` — validação runtime ("próximo /new-adr opera per spec clarificado") emerge naturalmente em uso real. Refinamento editorial micro não precisa cenários enumerados.
- Refinamento codifica comportamento empírico observado em 3 invocações desta sessão (ADR-037, ADR-038, ADR-039 todos preenchidos a partir de inputs explícitos do operador, todos auditados sem flag de "inventar conteúdo"). Spec clarificado alinha o doc à prática.
