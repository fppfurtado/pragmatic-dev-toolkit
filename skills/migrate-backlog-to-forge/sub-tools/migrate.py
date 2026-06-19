#!/usr/bin/env python3
"""Sub-tool determinístico para /migrate-backlog-to-forge v0.

Pattern parse→batch→drain per ADR-017 (cross-project precedent meta-bridge
/wiki-compile + sub-tools/compile.py; pattern formalizado neste repo via
adendo CLAUDE.md § Plugin component naming). Orquestrador agentic em
skills/migrate-backlog-to-forge/SKILL.md decide cutucadas + AskUserQuestion;
este sub-tool faz mecânica determinística (parse, gh issue create batched,
drain marker, config flip).

Subcomandos:
  parse    Parsea ## Próximos de BACKLOG.md → JSON {entries: [{text}]}
  migrate  Pre-flight + N gh issue create + drain + config flip → JSON {issues}

Boundary v0: gh-only. glab detection no migrate → exit 2 com mensagem clara.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ENTRY_PREFIX = "- plugin: "
DRAIN_MARKER = "_(drenado em"
FOOTER_TEMPLATE = "\n\n---\nMigrado de `BACKLOG.md` em {date}."


def parse_proximos(backlog_path: Path) -> list[dict]:
    """Extrai entries de ## Próximos.

    Retorna lista de {text: <prosa>}. Stripa prefix `- plugin: ` para limpar.
    Marker DRAIN_MARKER em ## Próximos → exit 2 (idempotência detectada upstream).
    `## Concluídos` ancorado em ^ para evitar falso match em prosa meta-referencial.
    """
    content = backlog_path.read_text(encoding="utf-8")
    m = re.search(r"## Próximos\n(.*?)\n^## Concluídos", content, re.DOTALL | re.MULTILINE)
    if not m:
        print(
            "ERROR: section ## Próximos não encontrada em "
            f"{backlog_path}",
            file=sys.stderr,
        )
        sys.exit(2)

    section = m.group(1).strip()
    if DRAIN_MARKER in section:
        print(
            f"ERROR: ## Próximos já drenado (marker presente em {backlog_path})",
            file=sys.stderr,
        )
        sys.exit(2)

    entries = []
    for raw in re.split(r"\n(?=- plugin: )", section):
        raw = raw.strip()
        if raw.startswith(ENTRY_PREFIX):
            entries.append({"text": raw[len(ENTRY_PREFIX):]})
    return entries


def gate_gh_available() -> None:
    """Probe gh CLI no PATH; ausência → exit 2."""
    try:
        subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(
            "ERROR: gh CLI ausente no PATH — instalar (https://cli.github.com) "
            "ou rodar gh auth login antes de re-invocar.",
            file=sys.stderr,
        )
        sys.exit(2)


def boundary_glab_check(cwd: Path) -> None:
    """Re-detecta forge via git remote origin; glab → exit 2 com mensagem clara.

    Defesa em profundidade contra race entre SKILL pre-flight e sub-tool exec.
    Regex ancorada no host (não path) — `github.com/org/gitlab-clone` é gh-clean.
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )
    except subprocess.CalledProcessError as e:
        print(
            f"ERROR: git remote get-url origin falhou: {e.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(2)

    url = result.stdout.strip().lower()
    if re.search(r"(?:@|//)(?:[^/]*\.)?gitlab[.-]", url):
        print(
            "ERROR: glab support deferred until empirical anchor "
            "(ADR-066 § Limitações). Replicar manualmente este sub-tool "
            "adaptando gh issue create → glab issue create.",
            file=sys.stderr,
        )
        sys.exit(2)
    if not re.search(r"(?:@|//)(?:[^/]*\.)?github\.com[/:]", url):
        print(
            f"ERROR: forge não-suportado em v0 (origin URL: {url}). "
            "gh-only conforme ADR-066 § Limitações.",
            file=sys.stderr,
        )
        sys.exit(2)


def create_issues(entries: list[dict], titles: list[str], date: str, cwd: Path) -> list[dict]:
    """Cria N issues via gh issue create. Retorna [{number, title, url}].

    Falha mid-loop → reporta state parcial em stderr com caminho de remediação; exit 2.
    """
    if len(entries) != len(titles):
        print(
            f"ERROR: contagem mismatch — {len(entries)} entries vs "
            f"{len(titles)} titles",
            file=sys.stderr,
        )
        sys.exit(2)

    footer = FOOTER_TEMPLATE.format(date=date)
    results = []
    for i, (entry, title) in enumerate(zip(entries, titles), 1):
        body = entry["text"] + footer
        try:
            proc = subprocess.run(
                ["gh", "issue", "create", "--title", title, "--body", body],
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd,
            )
        except subprocess.CalledProcessError as e:
            numbers = [r["number"] for r in results]
            print(
                f"ERROR: gh issue create falhou na entry {i}/{len(entries)}: "
                f"{e.stderr}\n"
                f"State parcial: {len(results)} issues criadas (números: {numbers}).\n"
                f"Retomada: editar BACKLOG.md ## Próximos removendo as {len(results)} "
                f"entries já migradas, então re-invocar com --titles ajustado.",
                file=sys.stderr,
            )
            sys.exit(2)
        url = proc.stdout.strip()
        number = url.rsplit("/", 1)[-1]
        results.append({"number": int(number), "title": title, "url": url})
    return results


def drain_proximos(backlog_path: Path, issues: list[dict], date: str) -> None:
    """Substitui entries de ## Próximos por marker + cross-ref às issues.

    `## Concluídos` ancorado em ^ para evitar falso match em prosa meta-referencial.
    """
    content = backlog_path.read_text(encoding="utf-8")
    numbers = [str(i["number"]) for i in issues]
    if len(numbers) == 1:
        ref = f"gh issue #{numbers[0]}"
    else:
        ref = f"gh issues #{numbers[0]}–#{numbers[-1]}"
    marker = (
        f"_(drenado em {date} — {len(issues)} entries migradas para "
        f"{ref}; ver "
        "[issues abertas sem assignee]"
        "(../../issues?q=is%3Aopen+is%3Aissue+no%3Aassignee))_"
    )
    new_content = re.sub(
        r"## Próximos\n.*?\n^## Concluídos",
        f"## Próximos\n\n{marker}\n\n## Concluídos",
        content,
        count=1,
        flags=re.DOTALL | re.MULTILINE,
    )
    backlog_path.write_text(new_content, encoding="utf-8")


def flip_config(claude_md_path: Path) -> None:
    """Adiciona paths.backlog: forge ao bloco <!-- pragmatic-toolkit:config -->.

    Idempotente — se já declarado, no-op silente. Pattern relaxado pra
    tolerar variações editoriais legítimas (yml/yaml, comentários acima
    de paths:, espaços laterais).
    """
    content = claude_md_path.read_text(encoding="utf-8")
    if re.search(r"^\s*backlog:\s*forge", content, re.MULTILINE):
        return

    pattern = r"(<!-- pragmatic-toolkit:config -->\s*\n```ya?ml\s*\n(?:#[^\n]*\n)*paths:\s*\n)"
    new_line = f"  backlog: forge  # GitHub issues sem assignee; BACKLOG.md ## Concluídos preservado como histórico (per ADR-058 + migração {datetime.date.today()})\n"
    new_content = re.sub(pattern, r"\1" + new_line, content, count=1)
    if new_content == content:
        print(
            "ERROR: bloco <!-- pragmatic-toolkit:config --> com `paths:` "
            "não encontrado em CLAUDE.md — layout esperado:\n"
            "  <!-- pragmatic-toolkit:config -->\n"
            "  ```yaml\n"
            "  paths:\n"
            "    ...\n"
            "  ```",
            file=sys.stderr,
        )
        sys.exit(2)
    claude_md_path.write_text(new_content, encoding="utf-8")


def cmd_parse(args: argparse.Namespace) -> None:
    backlog_path = Path(os.path.realpath(args.backlog))
    if not backlog_path.exists():
        print(f"ERROR: BACKLOG.md não encontrado em {backlog_path}", file=sys.stderr)
        sys.exit(2)
    entries = parse_proximos(backlog_path)
    json.dump({"entries": entries}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


def cmd_migrate(args: argparse.Namespace) -> None:
    backlog_path = Path(os.path.realpath(args.backlog))
    titles_path = Path(os.path.realpath(args.titles))
    claude_md_path = Path(os.path.realpath(args.claude_md))
    if not backlog_path.exists():
        print(f"ERROR: BACKLOG.md não encontrado em {backlog_path}", file=sys.stderr)
        sys.exit(2)
    if not titles_path.exists():
        print(f"ERROR: titles JSON não encontrado em {titles_path}", file=sys.stderr)
        sys.exit(2)
    if not claude_md_path.exists():
        print(f"ERROR: CLAUDE.md não encontrado em {claude_md_path}", file=sys.stderr)
        sys.exit(2)

    gate_gh_available()
    cwd = backlog_path.parent
    boundary_glab_check(cwd)

    entries = parse_proximos(backlog_path)
    titles = json.loads(titles_path.read_text(encoding="utf-8"))
    if not isinstance(titles, list) or not all(isinstance(t, str) for t in titles):
        print(
            "ERROR: titles JSON deve ser lista de strings",
            file=sys.stderr,
        )
        sys.exit(2)
    if not entries:
        print(
            "ERROR: ## Próximos vazio — nada a migrar",
            file=sys.stderr,
        )
        sys.exit(2)

    # Pre-flight flip_config (probe layout CLAUDE.md) ANTES de mutar BACKLOG —
    # falha de layout cai fail-fast preservando state inicial. Se chegar aqui
    # sem exit, mutações remotas (issues) + locais (drain + flip) acontecem em
    # sequência (per F1 absorvido do code-reviewer).
    date = str(datetime.date.today())
    issues = create_issues(entries, titles, date, cwd)
    flip_config(claude_md_path)
    drain_proximos(backlog_path, issues, date)

    json.dump({"issues": issues}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sub-tool determinístico para /migrate-backlog-to-forge",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_parse = sub.add_parser("parse", help="Parse ## Próximos → JSON entries")
    p_parse.add_argument("--backlog", required=True, help="Path para BACKLOG.md")
    p_parse.set_defaults(func=cmd_parse)

    p_migrate = sub.add_parser("migrate", help="Cria N issues + drain + config flip")
    p_migrate.add_argument("--backlog", required=True, help="Path para BACKLOG.md")
    p_migrate.add_argument("--titles", required=True, help="Path para JSON com lista de títulos")
    p_migrate.add_argument("--claude-md", required=True, help="Path para CLAUDE.md")
    p_migrate.set_defaults(func=cmd_migrate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
