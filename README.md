# pragmatic-dev-toolkit

Claude Code plugin codifying the **flat & pragmatic** dev workflow: workflow skills for alignment, execution and diagnosis; YAGNI/QA/security/doc/design reviewers; self-gated hooks. Companion to [`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit).

## What's inside

| Component | Type | What it does |
|-----------|------|--------------|
| `/triage` | Skill | Aligns intent, surfaces gaps, decides which artifact (backlog line, plan, ADR, domain/design update) is needed before implementing. Without an argument, delegates to `/next`. |
| `/next` | Skill | Session orientation: reads the backlog, checks the codebase for what's already implemented, and suggests the top three impact candidates for triage. Also lists `## Pendências de validação` from merged plans as a separate block (not competing in the top 3). |
| `/new-adr` | Skill | Creates a new ADR in `docs/decisions/` with auto-numbering and a standardized template. |
| `/run-plan` | Skill | Executes a plan from `docs/plans/<slug>.md` in an isolated worktree, with Conventional Commits micro-commits, per-block reviewer dispatch, manual validation gate when applicable, and a push/PR suggestion at the end. |
| `/debug <symptom>` | Skill | Diagnoses root cause via scientific method (reproduce → isolate → hypothesize → evidence). Produces a diagnosis, not a fix — operator chooses revert / direct patch / `/triage` next. Stack-agnostic. |
| `/gen-tests` | Skill | Generates tests for a module/function/free description, using the consumer project's stack idioms. Stacks supported today: Python and Java. |
| `/release [<bump>\|<version>]` | Skill | Coordinated version bump across `version_files`, `changelog` entry, unified commit, and local annotated tag. Doesn't push — publication stays with the operator. |
| `/init-config` | Skill | Interactive wizard for the `<!-- pragmatic-toolkit:config -->` block in `CLAUDE.md`. Asks per role (`decisions_dir`, `backlog`, `plans_dir` canonical/local/null + `test_command` stack-aware probe) and writes the YAML block. Proactive alternative to the one-shot memoization of the Resolution protocol. |
| `/archive-plans [--quarter <YYYY-Qx>]` | Skill | Periodic editorial archival: moves plans in `docs/plans/` whose backlog line entered `## Concluídos` ≥2 weeks ago to `docs/plans/archive/<YYYY-Qx>/`. Preview-first with `Aplicar / Cancelar` gate; non-destructive (`git mv` preserves history). Doesn't push. |
| `code-reviewer` | Agent | YAGNI rubric: flags premature abstractions, redundant comments, defensive overhead, phantom backwards-compat. |
| `qa-reviewer` | Agent | Test coverage principles: happy path, documented invariants, declared edge cases, mock vs real. Stack-agnostic. |
| `security-reviewer` | Agent | Credentials, input validation, external HTTP, sensitive data, and ADR-documented invariants. Stack-agnostic. |
| `doc-reviewer` | Agent | Doc/code drift: identifiers cited in docs that don't exist in the repo, broken cross-refs/anchors, contradictory examples/snippets. Default for doc-only blocks in `/run-plan`. Stack-agnostic. |
| `design-reviewer` | Agent | Pre-fact reviewer for structural and design decisions in plans and ADR drafts: premature abstractions, missing alternatives, unformalized ADR-worthiness, contradictions with existing ADRs or `docs/philosophy.md`. Auto-read of `docs/decisions/` (curated above a small threshold per ADR-021) and `docs/philosophy.md`. Auto-dispatched in `/triage` (plan-producing path) and `/new-adr` (standalone or delegated) per ADR-011; manually via `@design-reviewer`. Stack-agnostic. |
| `block_env` | Hook | `PreToolUse` blocking direct edits to `.env` (and variants), accepting only `.env.example`. |
| `block_gitignored` | Hook | `PreToolUse` blocking edits in gitignored paths (dependencies, build artifacts, local caches). Triple auto-gating (empty path / non-git / `git` missing → no-op); `.claude/` is allowlisted (Claude Code territory). |
| `run_pytest_python` | Hook | `PostToolUse`, auto-gated (`.py` + ancestor `pyproject.toml`), runs pytest after edits and prints output only on failure. |
| `templates/plan.md` | Template | Canonical plan skeleton (consumed by `/triage` and `/run-plan`). Reference for hand-writing plans. |
| `docs/procedures/cleanup-pos-merge.md` | Procedure | Shared executable procedure consumed via `Read` by `/triage` (step 0) and `/release` (before preconditions). Detects merged worktrees and cuts cleanup via `gh`/`glab` auto-detect. Per ADR-024. |

## Installation

```
/plugin marketplace add fppfurtado/pragmatic-dev-toolkit
/plugin install pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```

Details and direct-path alternative in [`docs/install.md`](docs/install.md).

## Philosophy

**Bounded contexts and ubiquitous language yes, tactical ceremony no.** Bounded contexts (strategic DDD) and shared vocabulary between code and business are foundational. Tactical ceremony (formal `application/`/`domain/`/`infrastructure/` layers, universal ports/adapters, cascading mappers) creates many files for little value — add abstraction only when there's **real pain** (an unstable integration, a substitution you can already see coming). YAGNI by default.

For the full doctrine and path contract, see [`docs/philosophy.md`](docs/philosophy.md) (Portuguese).

## Companion

[`scaffold-kit`](https://github.com/fppfurtado/scaffold-kit) is the Copier template that produces the canonical default layout the skills assume (`IDEA.md`, `docs/domain.md`, `docs/design.md`, `docs/decisions/`, `docs/plans/`, `BACKLOG.md`, `Makefile`, `.worktreeinclude`). The two artifacts are decoupled — you can use one without the other.

The toolkit works in any project aligned with the philosophy, not only those generated by `scaffold-kit`. Skills consume **roles** (ubiquitous language, plan, decision, test gate…), not literal paths — projects with a different layout declare variants once via the `<!-- pragmatic-toolkit:config -->` block in their `CLAUDE.md`. Schema and details in [`docs/install.md`](docs/install.md).

## Contributing

Issues and PRs welcome. Structural changes to skills/agents go through ADRs in [`docs/decisions/`](docs/decisions/).

## License

MIT — see [LICENSE](LICENSE).
