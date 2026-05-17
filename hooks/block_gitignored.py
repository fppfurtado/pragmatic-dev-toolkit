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

Allowlist: edits under `<repo>/.claude/` are never blocked. That root is
Claude Code's territory (skill state, local-mode artifacts per ADR-005);
the plugin's stated principle is to never touch it, which includes not
gating it. Without this carve-out, consumers that adopt local mode
(`paths.<role>: local`) would see `/triage`, `/new-adr`, `/run-plan`
fail to write under `.claude/local/`.
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

    # The file's parent may not exist yet (Write creating a new tree under
    # a gitignored dir). Walk up to the nearest existing ancestor so
    # `git -C <anchor>` can locate the repo.
    anchor = os.path.dirname(abspath) or "/"
    while anchor != "/" and not os.path.isdir(anchor):
        anchor = os.path.dirname(anchor) or "/"

    # Layer 2 + toplevel resolution in a single git call.
    try:
        meta = subprocess.run(
            ["git", "-C", anchor, "rev-parse",
             "--is-inside-work-tree", "--show-toplevel"],
            capture_output=True, text=True,
        )
    except FileNotFoundError:
        return 0
    if meta.returncode != 0:
        return 0
    lines = meta.stdout.splitlines()
    if len(lines) < 2 or lines[0].strip() != "true":
        return 0
    toplevel = lines[1].strip()
    if not toplevel:
        return 0

    # Allowlist: harness territory under `<repo>/.claude/` is never gated.
    # Hardcoded dependency on Claude Code's convention of placing harness
    # state under `.claude/`. Trigger for review: CC changes that convention
    # (e.g., `.claudecode/`, `.cc/`) — update the literal below and the
    # docstring. Audit `docs/audits/runs/2026-05-12-architecture-logic.md`
    # § L2 records this implicit dependency.
    relpath = os.path.relpath(abspath, toplevel)
    if relpath == ".claude" or relpath.startswith(".claude" + os.sep):
        return 0

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
