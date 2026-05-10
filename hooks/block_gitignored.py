#!/usr/bin/env python3
"""PreToolUse hook: block direct edits to gitignored paths.

Reads a JSON event from stdin (Claude Code hook payload). If the targeted
file is covered by the host project's `.gitignore` (typical cases:
`.venv/`, `node_modules/`, `dist/`, `target/`, `.cache/`), write a short
message to stderr and exit 2 (block). Otherwise exit 0.

Triple auto-gating so this is safe to ship in a multi-stack plugin:
  1. extension-equivalent: empty `file_path` → exit 0.
  2. stack marker: file is not inside a git working tree → exit 0.
  3. toolchain: `git` not found on `PATH` → exit 0.
"""
import json
import os
import subprocess
import sys


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    file_path = event.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return 0

    abspath = os.path.abspath(file_path)
    anchor = os.path.dirname(abspath) or "/"

    # Layer 2: stack marker — bail unless `git -C <anchor>` reports a work tree.
    try:
        inside = subprocess.run(
            ["git", "-C", anchor, "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        return 0
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return 0

    # Layer 3 already covered above (FileNotFoundError → exit 0).
    try:
        check = subprocess.run(
            ["git", "-C", anchor, "check-ignore", "-q", abspath],
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        return 0

    # check-ignore: 0 = ignored, 1 = not ignored, 128 = error.
    if check.returncode == 0:
        sys.stderr.write(
            f"Blocked: edit of {file_path} is not allowed — path is gitignored "
            f"(dependency, build artifact, or local cache). Edit project sources "
            f"instead, or remove the entry from .gitignore if this is genuinely "
            f"tracked work.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
