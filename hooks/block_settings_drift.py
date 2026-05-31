#!/usr/bin/env python3
"""PreToolUse hook: block absolute-path drift in `.claude/settings.json`.

Reads a JSON event from stdin (Claude Code hook payload). The hook blocks
edits to `.claude/settings.json` whose new content introduces absolute
paths matching `/home/<user>/` or `/Users/<user>/` — typical pattern of
session-permission entries that pollute the tracked settings file. The
gitignored `.claude/settings.local.json` is out of scope (personal paths
are expected there). Per ADR-050 § Decisão (f).
"""
import json
import re
import sys

TARGET_FILE = ".claude/settings.json"
ABSOLUTE_PATH_PATTERN = re.compile(r"/(?:home|Users)/[^/]+/")


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = event.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not (file_path.endswith("/" + TARGET_FILE) or file_path == TARGET_FILE):
        return 0

    new_content = tool_input.get("content") or tool_input.get("new_string") or ""

    match = ABSOLUTE_PATH_PATTERN.search(new_content)
    if not match:
        return 0

    sys.stderr.write(
        f"Blocked: edit to {file_path} introduces absolute path '{match.group(0)}'. "
        f"Tracked settings.json should not carry user-specific paths. Options: "
        f"(a) move the entry to .claude/settings.local.json (gitignored, personal), "
        f"(b) replace with a variable like $HOME/ or ~/, "
        f"(c) edit outside Claude Code if intentional.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
