#!/usr/bin/env python3
"""Validate BACKLOG.md for merge artifacts.

Detects:
- Lines duplicated across the tracked sections (## Próximos, ## Em andamento, ## Concluídos).
- Required sections missing.

Output: JSON to stdout with `{"problems": [...]}`. Exit 0 if clean, 1 if problems.
"""
import json
import sys
from pathlib import Path

TRACKED_SECTIONS = ("Próximos", "Em andamento", "Concluídos")


def parse(text: str) -> dict[str, list[str]]:
    """Group top-level bullet lines by H2 section name."""
    sections: dict[str, list[str]] = {}
    current = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("## "):
            current = stripped[3:].strip()
            sections.setdefault(current, [])
        elif current is not None and raw.startswith("- "):
            sections[current].append(raw[2:].strip())
    return sections


def find_problems(sections: dict[str, list[str]]) -> list[dict]:
    problems: list[dict] = []

    for name in TRACKED_SECTIONS:
        if name not in sections:
            problems.append({"type": "missing_section", "section": name})

    line_to_sections: dict[str, list[str]] = {}
    for name in TRACKED_SECTIONS:
        for line in sections.get(name, []):
            line_to_sections.setdefault(line, []).append(name)

    for line, secs in line_to_sections.items():
        if len(secs) >= 2:
            problems.append({"type": "duplicate", "line": line, "sections": secs})

    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write("usage: validate_backlog.py <path-to-BACKLOG.md>\n")
        return 2

    path = Path(argv[1])
    if not path.is_file():
        sys.stderr.write(f"error: file not found: {path}\n")
        return 2

    sections = parse(path.read_text(encoding="utf-8"))
    problems = find_problems(sections)
    json.dump({"problems": problems}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
