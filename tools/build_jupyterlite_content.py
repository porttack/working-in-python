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
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEPLOY_PATH_PLACEHOLDER = "JUPYTERLITE_DEPLOY_PATH"
# Matches the absolute link every chapter's chrome uses to reach another
# JupyterLite notebook (Exercises / JupyterLite / Teach Copy), e.g.
# "https://python.porttack.com/jupyterlite-<hash>/notebooks/index.html?path=X"
# -- see relativize_sibling_links(). Anchored to the surrounding parens of a
# markdown link target `(url)`, not just the URL text, so this can never touch
# an HTML attribute value (e.g. a self-embedding iframe's src="...") even for
# a future chapter that adds one without a matching CELL_PATCHES entry yet.
SIBLING_LINK_RE = re.compile(r"\(https://\S*?/notebooks/index\.html\?path=([^)\s\"]+)\)")
CHAPTERS = {
    "index.ipynb": [],
    "jupyter_intro.ipynb": ["working_in_python.py"],
    "chap01.ipynb": ["working_in_python.py"],
    "chap02.ipynb": ["working_in_python.py", "diagram.py"],
    "chap03.ipynb": ["working_in_python.py", "diagram.py"],
    "chap04.ipynb": ["working_in_python.py", "diagram.py", "jupyturtle.py"],
    "chap05.ipynb": ["working_in_python.py", "diagram.py", "jupyturtle.py"],
    "chap06.ipynb": ["working_in_python.py", "diagram.py"],
    "chap07.ipynb": ["working_in_python.py", "diagram.py", "words.txt"],
    "chap08.ipynb": ["working_in_python.py", "diagram.py", "words.txt", "pg345.txt", "pg1184.txt"],
    "chap09.ipynb": ["working_in_python.py", "diagram.py", "words.txt"],
    "chap10.ipynb": ["working_in_python.py", "diagram.py", "words.txt"],
    "chap11.ipynb": ["working_in_python.py", "diagram.py", "structshape.py", "words.txt", "pg345.txt"],
    # Teacher-authored exercises notebooks, separate from the chapters
    # themselves (not one of Downey's 19 chapters -- just needs the same
    # JupyterLite treatment so its own link works). Deps listed per-notebook
    # as its own exercises start using external modules; blank otherwise.
    # working_in_python.py on every one of these: each ends with a cell
    # calling its show_copy_notebook_button(), and chapters 5-8 additionally
    # call enable_docstring_reminders() -- see AUDIT.md, 2026-08-16.
    "chap01-exercises.ipynb": ["working_in_python.py"],
    "chap02-exercises.ipynb": ["working_in_python.py"],
    "chap03-exercises.ipynb": ["working_in_python.py"],
    "chap04-exercises.ipynb": ["working_in_python.py", "jupyturtle.py"],
    "chap05-exercises.ipynb": ["working_in_python.py"],
    "chap06-exercises.ipynb": ["working_in_python.py"],
    "chap07-exercises.ipynb": ["working_in_python.py"],
    "chap08-exercises.ipynb": ["working_in_python.py"],
}
# Student-legible names for what CHAPTERS ships into the flat JupyterLite lab
# file browser, keyed by the same CHAPTERS notebook name -- chapters/*.ipynb
# itself never changes (see CLAUDE.md non-negotiable #2). Underscore-prefix
# groups sort ahead of the upstream helper .py/.txt files below them, most
# underscores first: "___" front matter, "__" chapters, "_" exercises. "teach"
# is the optional fourth entry -- the blanked classroom-projection copy built
# from projector/<name> -- and is deliberately *absent* for entries that have
# no live-instruction use for one (index.ipynb, the exercises notebooks,
# which are a title and one empty cell). A missing "teach" key means build()
# ships no blanked variant for that notebook at all, even if build_blanks.py
# happens to have produced one in projector/. See CLAUDE.md's treatment
# matrix and AUDIT.md for why "teach" (not "blank"/"projector") sorts among
# the notebooks only if @jupyterlab/filebrowser-extension:browser's
# sortNotebooksFirst is set -- see the repo-root overrides.json.
CONTENT_NAMES = {
    "index.ipynb": {"name": "___start-here.ipynb"},
    "jupyter_intro.ipynb": {
        "name": "___using-notebooks.ipynb",
        "teach": "teach-using-notebooks.ipynb",
    },
    "chap01.ipynb": {"name": "__chap01-welcome.ipynb", "teach": "teach01-welcome.ipynb"},
    "chap02.ipynb": {
        "name": "__chap02-variables-and-statements.ipynb",
        "teach": "teach02-variables-and-statements.ipynb",
    },
    "chap03.ipynb": {"name": "__chap03-functions.ipynb", "teach": "teach03-functions.ipynb"},
    "chap04.ipynb": {
        "name": "__chap04-functions-and-interfaces.ipynb",
        "teach": "teach04-functions-and-interfaces.ipynb",
    },
    "chap05.ipynb": {
        "name": "__chap05-conditionals-and-recursion.ipynb",
        "teach": "teach05-conditionals-and-recursion.ipynb",
    },
    "chap06.ipynb": {
        "name": "__chap06-return-values.ipynb",
        "teach": "teach06-return-values.ipynb",
    },
    "chap07.ipynb": {
        "name": "__chap07-iteration-and-search.ipynb",
        "teach": "teach07-iteration-and-search.ipynb",
    },
    "chap08.ipynb": {
        "name": "__chap08-strings-and-regex.ipynb",
        "teach": "teach08-strings-and-regex.ipynb",
    },
    "chap09.ipynb": {"name": "__chap09-lists.ipynb", "teach": "teach09-lists.ipynb"},
    "chap10.ipynb": {"name": "__chap10-dictionaries.ipynb", "teach": "teach10-dictionaries.ipynb"},
    "chap11.ipynb": {"name": "__chap11-tuples.ipynb", "teach": "teach11-tuples.ipynb"},
    # Chapters 12-13: not yet in CHAPTERS above (pass-2/pass-4 haven't reached
    # them), but CLAUDE.md's treatment matrix gives them full blank markers
    # (teacher decision on VA removal, blank markers full), same as 1-11 --
    # so they get a "teach" name here already, ready for whenever they're
    # added to CHAPTERS.
    "chap12.ipynb": {
        "name": "__chap12-text-analysis-and-generation.ipynb",
        "teach": "teach12-text-analysis-and-generation.ipynb",
    },
    "chap13.ipynb": {
        "name": "__chap13-files-and-databases.ipynb",
        "teach": "teach13-files-and-databases.ipynb",
    },
    # Chapters 14-19: independent-study tier, no blank markers by design (see
    # CLAUDE.md treatment matrix) -- so no "teach" name, same as index.ipynb.
    "chap14.ipynb": {"name": "__chap14-classes-and-functions.ipynb"},
    "chap15.ipynb": {"name": "__chap15-classes-and-methods.ipynb"},
    "chap16.ipynb": {"name": "__chap16-classes-and-objects.ipynb"},
    "chap17.ipynb": {"name": "__chap17-inheritance.ipynb"},
    "chap18.ipynb": {"name": "__chap18-python-extras.ipynb"},
    "chap19.ipynb": {"name": "__chap19-final-thoughts.ipynb"},
    "chap01-exercises.ipynb": {"name": "_exercises01-welcome.ipynb"},
    "chap02-exercises.ipynb": {"name": "_exercises02-variables-and-statements.ipynb"},
    "chap03-exercises.ipynb": {"name": "_exercises03-functions.ipynb"},
    "chap04-exercises.ipynb": {"name": "_exercises04-functions-and-interfaces.ipynb"},
    "chap05-exercises.ipynb": {"name": "_exercises05-conditionals-and-recursion.ipynb"},
    "chap06-exercises.ipynb": {"name": "_exercises06-return-values.ipynb"},
    "chap07-exercises.ipynb": {"name": "_exercises07-iteration-and-search.ipynb"},
    "chap08-exercises.ipynb": {"name": "_exercises08-strings-and-regex.ipynb"},
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
            '<p id="chap01-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=__chap01-welcome.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap01-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap01-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
            '<p id="chap02-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=__chap02-variables-and-statements.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap02-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap02-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
    # chap03's page embeds a live JupyterLite iframe of itself, same
    # recursive-embed problem and same fix as chap01.ipynb above.
    "chap03.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="03" -->\n',
            '<p id="chap03-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap03-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap03-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap03-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=__chap03-functions.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap03-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap03-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
    # chap04's page embeds a live JupyterLite iframe of itself, same
    # recursive-embed problem and same fix as chap01.ipynb above.
    "chap04.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="04" -->\n',
            '<p id="chap04-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap04-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap04-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap04-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=__chap04-functions-and-interfaces.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap04-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap04-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
    # chap05's page embeds a live JupyterLite iframe of itself, same
    # recursive-embed problem and same fix as chap01.ipynb above.
    "chap05.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="05" -->\n',
            '<p id="chap05-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap05-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap05-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap05-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=__chap05-conditionals-and-recursion.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap05-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap05-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
    # chap06's page embeds a live JupyterLite iframe of itself, same
    # recursive-embed problem and same fix as chap01.ipynb above.
    "chap06.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="06" -->\n',
            '<p id="chap06-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap06-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap06-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap06-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=__chap06-return-values.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap06-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap06-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
    # chap07's page embeds a live JupyterLite iframe of itself, same
    # recursive-embed problem and same fix as chap01.ipynb above.
    "chap07.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="07" -->\n',
            '<p id="chap07-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap07-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap07-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap07-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=__chap07-iteration-and-search.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap07-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap07-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
            '<p id="jupyter-intro-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=___using-notebooks.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("jupyter-intro-jupyterlite-note");\n',
            '  var pane = document.getElementById("jupyter-intro-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
    # chap08's page also embeds a live JupyterLite iframe of itself, same
    # recursive-embed problem and same fix as chap01.ipynb above -- merged
    # into this chapter's existing entry (the !head/!tail shell-magic fixes
    # below) rather than a second top-level "chap08.ipynb" key, since a
    # duplicate dict-literal key would silently drop one or the other.
    "chap08.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="08" -->\n',
            '<p id="chap08-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap08-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap08-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap08-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=__chap08-strings-and-regex.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap08-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap08-jupyterlite-pane");\n',
            '  if (!pane) return;\n',
            '  if (new URLSearchParams(location.search).has("readonly")) {\n',
            '    pane.style.display = "none";\n',
            '    if (note) note.style.display = "none";\n',
            '    return;\n',
            '  }\n',
            '  var sidebar = document.getElementById("pst-primary-sidebar");\n',
            '  if (!sidebar) return;\n',
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
# A CHAPTERS entry ships its blanked live-instruction copy (built by
# tools/build_blanks.py into projector/ -- see CLAUDE.md) only if
# CONTENT_NAMES gives it a "teach" name AND projector/<name> exists. Both
# conditions matter: without the CONTENT_NAMES gate, every notebook with a
# projector/ copy would ship one, including the exercises notebooks (a title
# and one empty cell -- a blanked copy of that is meaningless clutter). See
# AUDIT.md, 2026-08-08 follow-up 15 and 2026-08-09 (naming pass).
PROJECTOR_DIR = ROOT / "projector"


def content_name_for(notebook):
    return CONTENT_NAMES.get(notebook, {}).get("name", notebook)


def teach_name_for(notebook):
    return CONTENT_NAMES.get(notebook, {}).get("teach")


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


def relativize_sibling_links(cells):
    """Every chapter's chrome links to its Exercises/JupyterLite/Teach Copy
    notebook via the *notebooks* app's absolute ?path= URL -- correct on the JB
    site and from Colab, where that's the only way to reach JupyterLite at all.
    But once a chapter is already running *inside* JupyterLite (lab or
    notebooks), that same absolute URL points at a different, self-contained
    JupyterLite application, and JupyterLab's own markdown-link renderer forces
    target="_blank" on it (confirmed by reading the built bundle's rendermime
    handleUrls/isLocal: any href with a URL scheme is treated as external).
    That's a full second application loading in a new browser tab, not a tab
    inside the session the student is already in.

    The notebook these links point at is always a flat sibling file in this
    same jupyterlite/content/ directory, so once a notebook ships *inside*
    JupyterLite, rewrite the link down to a bare relative filename -- no
    scheme, so isLocal is true, so JupyterLab resolves and opens it as a tab
    in the current session instead. See AUDIT.md, 2026-08-09."""
    relativized = []
    for cell in cells:
        source = cell.get("source", [])
        is_list = isinstance(source, list)
        text = "".join(source) if is_list else source
        new_text = SIBLING_LINK_RE.sub(lambda m: f"({m.group(1)})", text)
        if new_text == text:
            relativized.append(cell)
            continue
        cell = copy.deepcopy(cell)
        cell["source"] = new_text.splitlines(keepends=True) if is_list else new_text
        relativized.append(cell)
    return relativized


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
    teach_count = 0
    for notebook in CHAPTERS:
        check_shell_magic(notebook, ROOT / "chapters" / notebook, notebook, problems)
        projector_src = PROJECTOR_DIR / notebook
        if projector_src.exists() and teach_name_for(notebook):
            check_shell_magic(
                notebook, projector_src, f"{notebook} (teach)", problems
            )
            teach_count += 1

    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        return 1
    print(
        f"jupyterlite check: clean ({len(CHAPTERS)} chapters, "
        f"{teach_count} teach variant(s) checked)"
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
    cells = relativize_sibling_links(cells)
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

    teach_count = 0
    for notebook, deps in CHAPTERS.items():
        src = ROOT / "chapters" / notebook
        if not src.exists():
            print(f"error: {src} not found", file=sys.stderr)
            return 1
        write_notebook_variant(src, notebook, deps, deploy_id, content_name_for(notebook))

        for dep in deps:
            dep_src = ROOT / dep
            if not dep_src.exists():
                print(f"error: {dep_src} not found", file=sys.stderr)
                return 1
            shutil.copy(dep_src, CONTENT_DIR / dep)

        teach_name = teach_name_for(notebook)
        projector_src = PROJECTOR_DIR / notebook
        if projector_src.exists() and teach_name:
            write_notebook_variant(projector_src, notebook, deps, deploy_id, teach_name)
            teach_count += 1

    print(
        f"wrote {CONTENT_DIR} ({len(CHAPTERS)} notebook(s), "
        f"{teach_count} teach variant(s), deploy id {deploy_id})"
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
