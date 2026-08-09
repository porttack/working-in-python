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

DEPLOY_PATH_PLACEHOLDER / --print-deploy-id: chap01.ipynb and jupyter_intro.ipynb
each embed a live JupyterLite iframe of themselves, which needs to know the
path it's deployed under (jupyterlite-<id>/...) -- but that path used to be a
literal hardcoded in the source notebook, requiring a manual find-and-replace
across several files every time it changed (see AUDIT.md, 2026-08-08 follow-ups
8-10). Replaced with a placeholder token the source notebooks carry permanently
(DEPLOY_PATH_PLACEHOLDER below) plus a deploy id computed here from a hash of
everything that affects what ships in jupyterlite/content/ -- the CHAPTERS
notebooks, their dependency files, SHARED_FILES, and this script itself.
`--print-deploy-id` prints just that id, so jb/build.sh and jb/watch.sh can
capture it once and pass it to jb/prep_notebooks.py (which does the matching
substitution for the copies that ship on the JB site itself) without either
script duplicating the hash logic. See AUDIT.md, 2026-08-08 follow-up 12.
"""
import argparse
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEPLOY_PATH_PLACEHOLDER = "JUPYTERLITE_DEPLOY_PATH"
CHAPTERS = {
    "jupyter_intro.ipynb": ["thinkpython.py"],
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
    # Teacher-authored exercises notebooks, separate from the chapters
    # themselves (not one of Downey's 19 chapters -- just needs the same
    # JupyterLite treatment so its own link works). No deps: blank for now.
    "chap01-exercises.ipynb": [],
    "chap02-exercises.ipynb": [],
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
    # chap01's web page embeds a live JupyterLite iframe of chap01 itself.
    # Left as-is, that same cell would ship inside this very notebook, so a
    # student already running it in JupyterLite would see it try to embed
    # another copy of itself in an iframe, recursively. Replaced here, in the
    # jupyterlite/content/ copy only, with a one-line note. (Briefly removed
    # from chap01.ipynb entirely, then restored -- see AUDIT.md, 2026-08-08
    # follow-up 17.)
    "chap01.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="01" -->\n',
            '**Try it here.** This chapter also runs live on this page, no sign-in and nothing to install.\n',
            'Drag the thin divider next to the left nav to resize it.\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap01-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap01-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap01-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=chap01.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  var pane = document.getElementById("chap01-jupyterlite-pane");\n',
            '  if (!sidebar || !pane) return;\n',
            '  // Only take over the viewport when running inside the Sphinx book site,\n',
            '  // where the primary sidebar this pane is docked next to actually exists.\n',
            '  // height:auto (rather than the 600px stylesheet fallback, which only\n',
            '  // exists for contexts where this script never runs, e.g. viewing the raw\n',
            '  // notebook in VS Code) lets top+bottom determine the height, so the pane\n',
            '  // fills the whole right side, not a fixed 600px slice of it.\n',
            '  pane.style.position = "fixed";\n',
            '  pane.style.top = "0";\n',
            '  pane.style.right = "0";\n',
            '  pane.style.bottom = "0";\n',
            '  pane.style.height = "auto";\n',
            '  pane.style.zIndex = "2000";\n',
            '  function positionPane() {\n',
            '    pane.style.left = sidebar.getBoundingClientRect().right + "px";\n',
            '  }\n',
            '  new ResizeObserver(positionPane).observe(sidebar);\n',
            '  positionPane();\n',
            '})();\n',
            '</script>\n',
            '<!-- apcsp:end -->',
        ): (
            "*(You're already running this chapter live -- that's this page.)*",
        ),
    },
    # chap02's page embeds a live JupyterLite iframe of itself, same
    # recursive-embed problem and same fix as chap01.ipynb above.
    "chap02.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="02" -->\n',
            '**Try it here.** This chapter also runs live on this page, no sign-in and nothing to install.\n',
            'Drag the thin divider next to the left nav to resize it.\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap02-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap02-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap02-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=chap02.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  var pane = document.getElementById("chap02-jupyterlite-pane");\n',
            '  if (!sidebar || !pane) return;\n',
            '  // Only take over the viewport when running inside the Sphinx book site,\n',
            '  // where the primary sidebar this pane is docked next to actually exists.\n',
            '  // height:auto (rather than the 600px stylesheet fallback, which only\n',
            '  // exists for contexts where this script never runs, e.g. viewing the raw\n',
            '  // notebook in VS Code) lets top+bottom determine the height, so the pane\n',
            '  // fills the whole right side, not a fixed 600px slice of it.\n',
            '  pane.style.position = "fixed";\n',
            '  pane.style.top = "0";\n',
            '  pane.style.right = "0";\n',
            '  pane.style.bottom = "0";\n',
            '  pane.style.height = "auto";\n',
            '  pane.style.zIndex = "2000";\n',
            '  function positionPane() {\n',
            '    pane.style.left = sidebar.getBoundingClientRect().right + "px";\n',
            '  }\n',
            '  new ResizeObserver(positionPane).observe(sidebar);\n',
            '  positionPane();\n',
            '})();\n',
            '</script>\n',
            '<!-- apcsp:end -->',
        ): (
            "*(You're already running this chapter live -- that's this page.)*",
        ),
    },
    # jupyter_intro.ipynb's own page embeds a live JupyterLite iframe of
    # itself, same recursive-embed problem and same fix as chap01.ipynb above.
    "jupyter_intro.ipynb": {
        (
            '<!-- apcsp:begin type="note" -->\n',
            '**Try it here.** This notebook also runs live on this page, no sign-in and nothing to install.\n',
            'Drag the thin divider next to the left nav to resize it.\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#jupyter-intro-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#jupyter-intro-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="jupyter-intro-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=jupyter_intro.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  var pane = document.getElementById("jupyter-intro-jupyterlite-pane");\n',
            '  if (!sidebar || !pane) return;\n',
            '  // Only take over the viewport when running inside the Sphinx book site,\n',
            '  // where the primary sidebar this pane is docked next to actually exists.\n',
            '  // height:auto (rather than the 600px stylesheet fallback, which only\n',
            '  // exists for contexts where this script never runs, e.g. viewing the raw\n',
            '  // notebook in VS Code) lets top+bottom determine the height, so the pane\n',
            '  // fills the whole right side, not a fixed 600px slice of it.\n',
            '  pane.style.position = "fixed";\n',
            '  pane.style.top = "0";\n',
            '  pane.style.right = "0";\n',
            '  pane.style.bottom = "0";\n',
            '  pane.style.height = "auto";\n',
            '  pane.style.zIndex = "2000";\n',
            '  function positionPane() {\n',
            '    pane.style.left = sidebar.getBoundingClientRect().right + "px";\n',
            '  }\n',
            '  new ResizeObserver(positionPane).observe(sidebar);\n',
            '  positionPane();\n',
            '})();\n',
            '</script>\n',
            '<!-- apcsp:end -->',
        ): (
            "*(You're already running this notebook live -- that's this page.)*",
        ),
    },
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
# Every chapter in CHAPTERS that also has a generated projector/ copy (the
# blanked-out version for live classroom projection, built by
# tools/build_blanks.py -- see CLAUDE.md) gets that copy shipped into
# JupyterLite too, automatically, under a "-projector" suffix. No separate
# list to maintain: add a chapter to CHAPTERS as usual, and if
# projector/<name> exists, its projector variant just comes along. See
# AUDIT.md, 2026-08-08 follow-up 15.
PROJECTOR_DIR = ROOT / "projector"


def projector_output_name(notebook):
    return notebook.removesuffix(".ipynb") + "-projector.ipynb"


def compute_deploy_id():
    """Hash every input that affects what ships in jupyterlite/content/, so
    the deploy path changes automatically whenever that content does, and
    never needs a human to remember to bump anything. Order is fixed (not
    dict/set iteration order) so the hash is reproducible run to run."""
    digest = hashlib.sha256()
    digest.update(Path(__file__).read_bytes())
    dep_files = sorted({dep for deps in CHAPTERS.values() for dep in deps})
    for notebook in sorted(CHAPTERS):
        digest.update((ROOT / "chapters" / notebook).read_bytes())
        projector_src = PROJECTOR_DIR / notebook
        if projector_src.exists():
            digest.update(projector_src.read_bytes())
    for dep in dep_files:
        digest.update((ROOT / dep).read_bytes())
    for shared in sorted(SHARED_FILES):
        digest.update((ROOT / "jupyterlite" / shared).read_bytes())
    return f"jupyterlite-{digest.hexdigest()[:10]}"


def substitute_deploy_path(cells, deploy_id):
    substituted = []
    for cell in cells:
        source = cell.get("source", [])
        is_list = isinstance(source, list)
        text = "".join(source) if is_list else source
        if DEPLOY_PATH_PLACEHOLDER not in text:
            substituted.append(cell)
            continue
        text = text.replace(DEPLOY_PATH_PLACEHOLDER, deploy_id)
        cell = copy.deepcopy(cell)
        cell["source"] = text.splitlines(keepends=True) if is_list else text
        substituted.append(cell)
    return substituted


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


def check_shell_magic(notebook, src, label, problems):
    if not src.exists():
        problems.append(f"{label}: source file not found at {src}")
        return
    nb = json.loads(src.read_text())
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        lines = "".join(cell.get("source", [])).splitlines()
        if any(is_shell_magic_line(line) for line in lines):
            if not is_handled_shell_magic_cell(notebook, cell):
                problems.append(
                    f"{label}: code cell {i} has an unhandled '!' shell-magic line "
                    f"-- add a CELL_PATCHES entry (see AUDIT.md, 2026-08-08)"
                )


def check():
    problems = []
    projector_count = 0
    for notebook in CHAPTERS:
        check_shell_magic(notebook, ROOT / "chapters" / notebook, notebook, problems)
        projector_src = PROJECTOR_DIR / notebook
        if projector_src.exists():
            check_shell_magic(
                notebook, projector_src, f"{notebook} (projector)", problems
            )
            projector_count += 1

    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        return 1
    print(
        f"jupyterlite check: clean ({len(CHAPTERS)} chapters, "
        f"{projector_count} projector variant(s) checked)"
    )
    return 0


def write_notebook_variant(src, notebook, deps, deploy_id, output_name):
    """Read src (a chapters/ or projector/ notebook), apply the same
    CELL_PATCHES/deploy-path/preload treatment as the regular chapter build,
    and write it to CONTENT_DIR under output_name. notebook is always the
    CHAPTERS key (e.g. "chap01.ipynb"), even for the projector variant, since
    CELL_PATCHES and PRELOAD_ON_DEP are keyed by chapter, not by which
    directory the source came from."""
    nb = json.loads(src.read_text())
    cells = apply_cell_patches(notebook, nb["cells"])
    cells = substitute_deploy_path(cells, deploy_id)
    modules = preload_modules_for(deps)
    if modules:
        cells = [bootstrap_cell(modules)] + cells
    nb["cells"] = cells
    (CONTENT_DIR / output_name).write_text(json.dumps(nb, indent=1))


def build():
    deploy_id = compute_deploy_id()

    if CONTENT_DIR.exists():
        shutil.rmtree(CONTENT_DIR)
    CONTENT_DIR.mkdir(parents=True)

    for shared in SHARED_FILES:
        shared_src = ROOT / "jupyterlite" / shared
        if not shared_src.exists():
            print(f"error: {shared_src} not found", file=sys.stderr)
            return 1
        shutil.copy(shared_src, CONTENT_DIR / shared)

    projector_count = 0
    for notebook, deps in CHAPTERS.items():
        src = ROOT / "chapters" / notebook
        if not src.exists():
            print(f"error: {src} not found", file=sys.stderr)
            return 1
        write_notebook_variant(src, notebook, deps, deploy_id, notebook)

        for dep in deps:
            dep_src = ROOT / dep
            if not dep_src.exists():
                print(f"error: {dep_src} not found", file=sys.stderr)
                return 1
            shutil.copy(dep_src, CONTENT_DIR / dep)

        projector_src = PROJECTOR_DIR / notebook
        if projector_src.exists():
            write_notebook_variant(
                projector_src, notebook, deps, deploy_id, projector_output_name(notebook)
            )
            projector_count += 1

    print(
        f"wrote {CONTENT_DIR} ({len(CHAPTERS)} notebook(s), "
        f"{projector_count} projector variant(s), deploy id {deploy_id})"
    )
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--print-deploy-id",
        action="store_true",
        help="print the content-derived deploy id (jupyterlite-<hash>) and exit",
    )
    args = parser.parse_args()
    if args.print_deploy_id:
        print(compute_deploy_id())
        return 0
    return check() if args.check else build()


if __name__ == "__main__":
    sys.exit(main())
