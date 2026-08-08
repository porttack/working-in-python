#!/usr/bin/env python3
"""Assemble jupyterlite/content/ from chapters/ plus each chapter's vendored
runtime dependencies (the single-file helper modules Downey's download()
boilerplate cell otherwise fetches over the network).

JupyterLite's Pyodide kernel cannot run that download() cell as-is: urllib
can't open HTTPS URLs under Pyodide (no ssl module). download() only fetches
a file if it doesn't already exist, so placing the dependency next to the
notebook here makes the existing cell find it and skip the network entirely.
No notebook edits required. See AUDIT.md, 2026-08-07.

jupyterlite/content/ is generated; regenerate with this script (or `make
jupyterlite`), never hand-edit it.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = {
    "chap01.ipynb": ["thinkpython.py"],
}
CONTENT_DIR = ROOT / "jupyterlite" / "content"


def main():
    if CONTENT_DIR.exists():
        shutil.rmtree(CONTENT_DIR)
    CONTENT_DIR.mkdir(parents=True)

    for notebook, deps in CHAPTERS.items():
        src = ROOT / "chapters" / notebook
        if not src.exists():
            print(f"error: {src} not found", file=sys.stderr)
            return 1
        shutil.copy(src, CONTENT_DIR / notebook)
        for dep in deps:
            dep_src = ROOT / dep
            if not dep_src.exists():
                print(f"error: {dep_src} not found", file=sys.stderr)
                return 1
            shutil.copy(dep_src, CONTENT_DIR / dep)

    print(f"wrote {CONTENT_DIR} ({len(CHAPTERS)} notebook(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
