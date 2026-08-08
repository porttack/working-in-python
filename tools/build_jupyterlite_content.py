#!/usr/bin/env python3
"""Assemble jupyterlite/content/ from chapters/ plus each chapter's vendored
runtime dependencies -- the helper modules and data files that chapter
notebooks otherwise fetch over the network at the top of the notebook, via
either Downey's download() (urlretrieve) or, in chap08, raw `!wget`.

Neither works under Pyodide: urllib can't open HTTPS URLs (no ssl module),
and `!` shell magic has no shell/subprocess to run in at all. The download()
and `!wget` cases are both guarded by `if not exists(...)`, so placing the
dependency next to the notebook here makes the existing cell find it and
skip the network path entirely -- no notebook edits needed. See AUDIT.md,
2026-08-07 and 2026-08-08.

diagram.py imports matplotlib, which Pyodide does NOT auto-install for
imports made from inside an imported .py file (only for `import X`
statements typed directly in the executing cell -- confirmed empirically;
the documented `loadPyodideOptions.packages` kernel setting for preloading
at startup does not actually take effect in jupyterlite-pyodide-kernel
0.8.2). So for any chapter that pulls in diagram.py, a bootstrap cell doing
a plain top-level `import matplotlib.pyplot` is inserted as the new first
cell of the COPY in jupyterlite/content/ -- never in chapters/ -- which
triggers Pyodide's real auto-install path before diagram.py needs it.

Some `!` shell-magic cells have no exists() guard because they're not
fetching anything -- they're previewing a file already created earlier in
the same notebook (chap08's `!head`/`!tail` calls on pg345_cleaned.txt).
There's nothing to pre-bundle for those, so CELL_PATCHES below rewrites
their exact source to a pure-Python equivalent, again only in the
jupyterlite/content/ copy. `--check` scans every notebook already in
CHAPTERS for `!`-prefixed lines that are neither covered by CELL_PATCHES
nor part of the known guarded-download pattern (`!wget` alongside an
`exists(` check in the same cell) -- run it (via `make check`) after adding
a new chapter to CHAPTERS, or after pulling an upstream chapter update, to
catch a new instance of this same class of bug before it silently breaks
in JupyterLite. See AUDIT.md, 2026-08-08.

jupyterlite/content/ is generated; regenerate with this script (or `make
jupyterlite`), never hand-edit it.
"""
import argparse
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
# Files that live in jupyterlite/ itself (not repo root, not chapter deps) and
# get copied once into the flat content/ directory, where every chapter's
# notebook can see and import them as a sibling file -- no per-chapter wiring
# needed. See AUDIT.md, 2026-08-08.
SHARED_FILES = ["ascii_art.py", "check.py"]
CELL_PATCHES = {
    "chap08.ipynb": {
        ("!head pg345_cleaned.txt",): (
            "print(''.join(open('pg345_cleaned.txt').readlines()[:10]), end='')",
        ),
        ("!tail pg345_cleaned.txt",): (
            "print(''.join(open('pg345_cleaned.txt').readlines()[-10:]), end='')",
        ),
        ("!head pg345_cleaned.txt > pg345_cleaned_10_lines.txt",): (
            "open('pg345_cleaned_10_lines.txt', 'w')"
            ".writelines(open('pg345_cleaned.txt').readlines()[:10])",
        ),
        ("!head -100 pg345_cleaned.txt > pg345_cleaned_100_lines.txt",): (
            "open('pg345_cleaned_100_lines.txt', 'w')"
            ".writelines(open('pg345_cleaned.txt').readlines()[:100])",
        ),
        ("!tail pg345_cleaned_100_lines.txt",): (
            "print(''.join(open('pg345_cleaned_100_lines.txt').readlines()[-10:]), end='')",
        ),
    },
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


def apply_cell_patches(notebook, cells):
    patches = CELL_PATCHES.get(notebook, {})
    if not patches:
        return cells
    patched = []
    for cell in cells:
        replacement = patches.get(tuple(cell.get("source", [])))
        if replacement is not None:
            cell = copy.deepcopy(cell)
            cell["source"] = list(replacement)
        patched.append(cell)
    return patched


def is_shell_magic_line(line):
    return line.strip().startswith("!")


def is_handled_shell_magic_cell(notebook, cell):
    source = cell.get("source", [])
    if tuple(source) in CELL_PATCHES.get(notebook, {}):
        return True
    text = "".join(source)
    if "wget" in text and "exists(" in text:
        return True
    return False


def check():
    problems = []
    for notebook in CHAPTERS:
        src = ROOT / "chapters" / notebook
        if not src.exists():
            problems.append(f"{notebook}: source file not found at {src}")
            continue
        nb = json.loads(src.read_text())
        for i, cell in enumerate(nb["cells"]):
            if cell.get("cell_type") != "code":
                continue
            lines = "".join(cell.get("source", [])).splitlines()
            if any(is_shell_magic_line(line) for line in lines):
                if not is_handled_shell_magic_cell(notebook, cell):
                    problems.append(
                        f"{notebook}: code cell {i} has an unhandled '!' shell-magic line "
                        f"-- add a CELL_PATCHES entry (see AUDIT.md, 2026-08-08)"
                    )

    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        return 1
    print(f"jupyterlite check: clean ({len(CHAPTERS)} chapters checked)")
    return 0


def build():
    if CONTENT_DIR.exists():
        shutil.rmtree(CONTENT_DIR)
    CONTENT_DIR.mkdir(parents=True)

    for shared in SHARED_FILES:
        shared_src = ROOT / "jupyterlite" / shared
        if not shared_src.exists():
            print(f"error: {shared_src} not found", file=sys.stderr)
            return 1
        shutil.copy(shared_src, CONTENT_DIR / shared)

    for notebook, deps in CHAPTERS.items():
        src = ROOT / "chapters" / notebook
        if not src.exists():
            print(f"error: {src} not found", file=sys.stderr)
            return 1

        nb = json.loads(src.read_text())
        cells = apply_cell_patches(notebook, nb["cells"])
        modules = preload_modules_for(deps)
        if modules:
            cells = [bootstrap_cell(modules)] + cells
        nb["cells"] = cells
        (CONTENT_DIR / notebook).write_text(json.dumps(nb, indent=1))

        for dep in deps:
            dep_src = ROOT / dep
            if not dep_src.exists():
                print(f"error: {dep_src} not found", file=sys.stderr)
                return 1
            shutil.copy(dep_src, CONTENT_DIR / dep)

    print(f"wrote {CONTENT_DIR} ({len(CHAPTERS)} notebook(s))")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else build()


if __name__ == "__main__":
    sys.exit(main())
