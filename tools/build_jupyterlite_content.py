#!/usr/bin/env python3
"""Assemble jupyterlite/content/ from chapters/ plus each chapter's vendored
runtime dependencies -- the helper modules and data files that chapter
notebooks otherwise fetch over the network at the top of the notebook, via
either Downey's download() (urlretrieve) or, in chap08, raw `!wget`.

Neither works under Pyodide: urllib can't open HTTPS URLs (no ssl module),
and `!wget` has no shell/subprocess to run in at all. Both guards are
`if not exists(...)`, so placing the dependency next to the notebook here
makes the existing cell find it and skip the network path entirely. No
notebook edits required. See AUDIT.md, 2026-08-07 and 2026-08-08.

diagram.py imports matplotlib, which Pyodide does NOT auto-install for
imports made from inside an imported .py file (only for `import X`
statements typed directly in the executing cell -- confirmed empirically;
the documented `loadPyodideOptions.packages` kernel setting for preloading
at startup does not actually take effect in jupyterlite-pyodide-kernel
0.8.2). So for any chapter that pulls in diagram.py, a bootstrap cell doing
a plain top-level `import matplotlib.pyplot` is inserted as the new first
cell of the COPY in jupyterlite/content/ -- never in chapters/ -- which
triggers Pyodide's real auto-install path before diagram.py needs it.

jupyterlite/content/ is generated; regenerate with this script (or `make
jupyterlite`), never hand-edit it.
"""
import copy
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = {
    "chap01.ipynb": ["thinkpython.py"],
    "chap02.ipynb": ["thinkpython.py", "diagram.py"],
    "chap03.ipynb": ["thinkpython.py", "diagram.py"],
    "chap04.ipynb": ["thinkpython.py", "diagram.py", "jupyturtle.py"],
    "chap05.ipynb": ["thinkpython.py", "diagram.py", "jupyturtle.py"],
    "chap06.ipynb": ["thinkpython.py", "diagram.py"],
    "chap07.ipynb": ["thinkpython.py", "diagram.py", "words.txt"],
    "chap08.ipynb": ["thinkpython.py", "diagram.py", "words.txt", "pg345.txt", "pg1184.txt"],
    "chap09.ipynb": ["thinkpython.py", "diagram.py", "words.txt"],
    "chap10.ipynb": ["thinkpython.py", "diagram.py", "words.txt"],
    "chap11.ipynb": ["thinkpython.py", "diagram.py", "structshape.py", "words.txt", "pg345.txt"],
}
PRELOAD_ON_DEP = {
    "diagram.py": ["matplotlib.pyplot"],
}
CONTENT_DIR = ROOT / "jupyterlite" / "content"


def bootstrap_cell(modules):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "jupyterlite-preload-bootstrap",
        "metadata": {},
        "outputs": [],
        "source": [f"import {m}\n" for m in modules],
    }


def preload_modules_for(deps):
    modules = []
    for dep in deps:
        for module in PRELOAD_ON_DEP.get(dep, []):
            if module not in modules:
                modules.append(module)
    return modules


def main():
    if CONTENT_DIR.exists():
        shutil.rmtree(CONTENT_DIR)
    CONTENT_DIR.mkdir(parents=True)

    for notebook, deps in CHAPTERS.items():
        src = ROOT / "chapters" / notebook
        if not src.exists():
            print(f"error: {src} not found", file=sys.stderr)
            return 1

        modules = preload_modules_for(deps)
        if modules:
            nb = json.loads(src.read_text())
            nb["cells"] = [bootstrap_cell(modules)] + copy.deepcopy(nb["cells"])
            (CONTENT_DIR / notebook).write_text(json.dumps(nb, indent=1))
        else:
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
