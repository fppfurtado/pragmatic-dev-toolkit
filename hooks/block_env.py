#!/usr/bin/env python3
"""PreToolUse hook: block direct edits to `.env` files.

Reads a JSON event from stdin (Claude Code hook payload). If the targeted file
is `.env` or `.env.<anything>` other than `.env.example`, write a short message
to stderr and exit 2 (block). Otherwise exit 0 (continue).
"""
import json
import sys


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    file_path = event.get("tool_input", {}).get("file_path", "")
    name = file_path.rsplit("/", 1)[-1]

    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        sys.stderr.write(
            f"Blocked: direct edit of {name} is not allowed. "
            f"Use .env.example as the versioned template; keep secrets out of git.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
