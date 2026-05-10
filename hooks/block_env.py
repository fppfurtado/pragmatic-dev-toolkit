#!/usr/bin/env python3
"""PreToolUse hook: block direct edits to env-files.

Reads a JSON event from stdin (Claude Code hook payload). The hook blocks
when the filename (after stripping a `TEMPLATE_SUFFIXES` suffix) ends in
`.env` or starts with `.env.`, with one exception: any name ending in
`.env.example` passes. This covers both the dotfile convention (`.env`,
`.env.production`) and the per-instance convention common in Java/PHP/Rails
legacy (`1g.env`, `production.env`), per ADR-015.
"""
import json
import sys

# Common template suffixes across the ecosystem; new ones can be appended
# without changing the loop below.
TEMPLATE_SUFFIXES = (".jinja", ".tmpl", ".j2", ".erb", ".mustache")


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    file_path = event.get("tool_input", {}).get("file_path", "")
    name = file_path.rsplit("/", 1)[-1]

    # Strip template suffixes so .env.example.jinja / .env.example.tmpl pass through.
    base = name
    for suffix in TEMPLATE_SUFFIXES:
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break

    if (base.endswith(".env") or base.startswith(".env.")) and not base.endswith(".env.example"):
        sys.stderr.write(
            f"Blocked: direct edit of {name} is not allowed. "
            f"Use .env.example as the versioned template; keep secrets out of git.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
