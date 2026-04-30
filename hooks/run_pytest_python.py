#!/usr/bin/env python3
"""PostToolUse hook: run pytest after edits inside a Python project.

Triple auto-gating so this is safe to ship in a multi-stack plugin:
  1. extension: only `.py` files trigger.
  2. stack marker: only fires if an ancestor directory contains
     `pyproject.toml`.
  3. toolchain: prefer `uv run pytest`; fall back to `python -m pytest`.

Output ergonomics: silent on green; print the last 10 lines of pytest
output (stdout+stderr) only when pytest exits non-zero. PostToolUse must
not block subsequent hooks, so we always exit 0.
"""
import json
import os
import shutil
import subprocess
import sys


def find_project_root(file_path: str) -> str | None:
    """Walk ancestors from the edited file looking for `pyproject.toml`.

    Use the file's location, not the Claude process cwd — essential in
    monorepos with multiple Python projects.
    """
    if not file_path:
        return None
    d = os.path.dirname(os.path.abspath(file_path))
    while d != "/":
        if os.path.isfile(os.path.join(d, "pyproject.toml")):
            return d
        d = os.path.dirname(d)
    return None


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    file_path = event.get("tool_input", {}).get("file_path", "")

    # Layer 1: extension gate.
    if not file_path.endswith(".py"):
        return 0

    # Layer 2: stack marker gate.
    root = find_project_root(file_path)
    if root is None:
        return 0

    # Layer 3: toolchain — prefer uv, fall back to python -m pytest.
    # subprocess.run with a list, never a string — file_path never reaches a shell.
    if shutil.which("uv"):
        cmd = ["uv", "run", "pytest", "-q", "--no-header"]
    else:
        cmd = [sys.executable, "-m", "pytest", "-q", "--no-header"]

    try:
        res = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    except FileNotFoundError:
        return 0

    if res.returncode != 0:
        tail = "\n".join((res.stdout + res.stderr).splitlines()[-10:])
        sys.stderr.write(tail + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
