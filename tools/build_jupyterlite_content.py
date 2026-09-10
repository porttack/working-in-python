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
    # Interlude between chapters 6 and 7 -- see CHAPTER_MANIFEST.md and
    # jb/_toc.yml's 2026-08-17 comment. Only downloads working_in_python.py,
    # no diagram.py: this chapter never draws a diagram.
    "chap06b.ipynb": ["working_in_python.py"],
    "chap07.ipynb": ["working_in_python.py", "diagram.py", "words.txt"],
    "chap08.ipynb": ["working_in_python.py", "diagram.py", "words.txt", "pg345.txt", "pg1184.txt"],
    "chap09.ipynb": ["working_in_python.py", "diagram.py", "words.txt"],
    "chap10.ipynb": ["working_in_python.py", "diagram.py", "words.txt"],
    "chap11.ipynb": ["working_in_python.py", "diagram.py", "structshape.py", "words.txt", "pg345.txt"],
    # chap12 downloads the book it analyzes (pg43.txt, Dr. Jekyll and Mr. Hyde)
    # directly from Project Gutenberg via download(), same mechanism as every
    # other vendored dependency here -- so it needs pre-bundling the same way.
    "chap12.ipynb": ["working_in_python.py", "diagram.py", "pg43.txt", "words.txt"],
    # chap13 downloads photos.zip (the images used for the file/database
    # examples) the same way.
    "chap13.ipynb": ["working_in_python.py", "diagram.py", "photos.zip", "words.txt"],
}
# Student-legible names for what CHAPTERS ships into the flat JupyterLite lab
# file browser, keyed by the same CHAPTERS notebook name -- chapters/*.ipynb
# itself never changes (see CLAUDE.md non-negotiable #2).
#
# Naming, since the 2026-08-16 cleanup (see AUDIT.md): front matter keeps a
# single leading underscore (`_Start-Here.ipynb`, `_Using-Notebooks.ipynb`) so
# it still sorts first; every chapter is `ChapterNN-<Title>.ipynb`, no prefix,
# so chapters cluster together right after front matter; the blanked
# classroom-projection copy (built from `projector/<name>`) is `blankNN-<Title>.ipynb`
# -- a *prefix*, deliberately, so blank copies sort as their own group *after*
# every chapter, not interleaved chapter-by-chapter. This is the one
# deliberate exception to "no prefix." Multi-word titles are Title Case with
# small words ("and") lowercase: `Chapter02-Variables-and-Statements.ipynb`.
#
# The dict key below is still `"teach"` (an internal identifier used
# throughout this script -- `teach_name_for()`, `teach_count`, etc.) even
# though the filename it produces and the chrome-bar link label both say
# "Blank" now, not "Teach" -- renaming the key itself would be a much larger,
# purely-internal refactor with no user-facing benefit. Don't be confused by
# the mismatch; the key name and what it ships are simply different things.
# A missing "teach" key means build() ships no blank variant at all for that
# notebook, even if build_blanks.py happens to have produced one in
# projector/ -- deliberately absent for entries with no live-instruction use
# for one (index.ipynb, chapters 14-19). This whole grouping only works
# because @jupyterlab/filebrowser-extension:browser's sortNotebooksFirst is
# set in the repo-root overrides.json, which buckets every notebook ahead of
# every helper .py/.txt file first, then sorts alphabetically within each
# bucket.
CONTENT_NAMES = {
    "index.ipynb": {"name": "_Start-Here.ipynb"},
    "jupyter_intro.ipynb": {
        "name": "_Using-Notebooks.ipynb",
        "teach": "blank-Using-Notebooks.ipynb",
    },
    "chap01.ipynb": {"name": "Chapter01-Welcome.ipynb", "teach": "blank01-Welcome.ipynb"},
    "chap02.ipynb": {
        "name": "Chapter02-Variables-and-Statements.ipynb",
        "teach": "blank02-Variables-and-Statements.ipynb",
    },
    "chap03.ipynb": {"name": "Chapter03-Functions.ipynb", "teach": "blank03-Functions.ipynb"},
    "chap04.ipynb": {
        "name": "Chapter04-Functions-and-Interfaces.ipynb",
        "teach": "blank04-Functions-and-Interfaces.ipynb",
    },
    "chap05.ipynb": {
        "name": "Chapter05-Conditionals-and-Recursion-v3.ipynb",
        "teach": "blank05-Conditionals-and-Recursion-v3.ipynb",
    },
    "chap06.ipynb": {
        "name": "Chapter06-Return-Values.ipynb",
        "teach": "blank06-Return-Values.ipynb",
    },
    # Interlude, not a numbered Think Python chapter -- "Chapter06b" (not
    # "Interlude...") is deliberate: the lab file browser only sorts
    # alphabetically (see the module docstring above), so this has to sort
    # next to Chapter06/Chapter07 by name, same as the filename and toc
    # placement. The book's own prose calls it an interlude regardless.
    "chap06b.ipynb": {
        "name": "Chapter06b-Docstrings-and-Doctests.ipynb",
        "teach": "blank06b-Docstrings-and-Doctests.ipynb",
    },
    "chap07.ipynb": {
        "name": "Chapter07-Iteration-and-Search-v2.ipynb",
        "teach": "blank07-Iteration-and-Search-v2.ipynb",
    },
    "chap08.ipynb": {
        "name": "Chapter08-Strings-and-Regex-v2.ipynb",
        "teach": "blank08-Strings-and-Regex-v2.ipynb",
    },
    "chap09.ipynb": {"name": "Chapter09-Lists.ipynb", "teach": "blank09-Lists.ipynb"},
    "chap10.ipynb": {"name": "Chapter10-Dictionaries.ipynb", "teach": "blank10-Dictionaries.ipynb"},
    "chap11.ipynb": {"name": "Chapter11-Tuples.ipynb", "teach": "blank11-Tuples.ipynb"},
    # Chapters 12-13: not yet in CHAPTERS above (pass-2/pass-4 haven't reached
    # them), but CLAUDE.md's treatment matrix gives them full blank markers
    # (teacher decision on VA removal, blank markers full), same as 1-11 --
    # so they get a "teach" name here already, ready for whenever they're
    # added to CHAPTERS.
    "chap12.ipynb": {
        "name": "Chapter12-Text-Analysis-and-Generation.ipynb",
        "teach": "blank12-Text-Analysis-and-Generation.ipynb",
    },
    "chap13.ipynb": {
        "name": "Chapter13-Files-and-Databases.ipynb",
        "teach": "blank13-Files-and-Databases.ipynb",
    },
    # Chapters 14-19: independent-study tier, no blank markers by design (see
    # CLAUDE.md treatment matrix) -- so no "teach" name, same as index.ipynb.
    "chap14.ipynb": {"name": "Chapter14-Classes-and-Functions.ipynb"},
    "chap15.ipynb": {"name": "Chapter15-Classes-and-Methods.ipynb"},
    "chap16.ipynb": {"name": "Chapter16-Classes-and-Objects.ipynb"},
    "chap17.ipynb": {"name": "Chapter17-Inheritance.ipynb"},
    "chap18.ipynb": {"name": "Chapter18-Python-Extras.ipynb"},
    "chap19.ipynb": {"name": "Chapter19-Final-Thoughts.ipynb"},
}
# Temporary aliases, 2026-08-16 naming cleanup: chapters 2 and 3 may already have
# students' in-progress work cached in their browser's IndexedDB under the OLD
# served name (JupyterLite's own storage is keyed by path -- see AUDIT.md).
# Serving the identical content under both the new canonical name and these old
# names keeps that cached work reachable, since the old path still resolves to a
# real, current file. Chapter 4 doesn't need one -- it's not live for students
# until Monday, under the new name from the start. Remove these entries after a
# few days, once no student could plausibly still need the old path.
#
# chap05 briefly got one too, 2026-08-24, alongside that day's rename (a fix
# for a content-staleness bug, not a filename cleanup -- see AUDIT.md). Removed
# the same day: shipping both names put two "Chapter05" entries side by side in
# the Lab file browser, confusing for every visitor, not just ones with an old
# bookmark -- confirmed even in a fresh incognito tab, where no stale content
# was ever at risk. An alias only helps someone who both has an old link AND
# hasn't already cached stale content under it; the visible duplication it
# causes for everyone else outweighs that narrow case here.
ALIASES = {
    "chap02.ipynb": ["__chap02-variables-and-statements.ipynb"],
    "chap03.ipynb": ["__chap03-functions.ipynb"],
}
# Whether to actually ship teach/blank copies into jupyterlite/content/ at
# all, 2026-08-16. Deliberately False for now -- what to call this file
# (teach/blank/teacher/etc.) and how to make it sort correctly in the lab
# file browser turned into an extended back-and-forth with no fully clean
# answer (every option either mismatches the file/label wording or sorts in
# an awkward position -- see AUDIT.md). Decided to stop shipping it into the
# student-facing lab entirely for now, planning to revisit with a genuinely
# separate teacher-facing lab/manifest later, rather than ship a compromise.
# CONTENT_NAMES still carries a "teach" key per chapter and teach_name_for()
# still resolves it -- none of that logic was removed, only gated here, so
# turning this back on later is a one-line flip once there's a real plan for
# where these copies should live. See CHANGELOG.md, 2026-08-16.
SHIP_TEACH_COPIES = False
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter01-Welcome.ipynb"></iframe>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter02-Variables-and-Statements.ipynb"></iframe>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter03-Functions.ipynb"></iframe>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter04-Functions-and-Interfaces.ipynb"></iframe>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter05-Conditionals-and-Recursion-v3.ipynb"></iframe>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter06-Return-Values.ipynb"></iframe>\n',
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
    # chap06b's page embeds a live JupyterLite iframe of itself, same
    # recursive-embed problem and same fix as chap01.ipynb above.
    "chap06b.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="6b" -->\n',
            '<p id="chap06b-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap06b-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap06b-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap06b-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter06b-Docstrings-and-Doctests.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap06b-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap06b-jupyterlite-pane");\n',
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
            "*(You're already running this interlude live -- that's this page.)*",
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter07-Iteration-and-Search-v2.ipynb"></iframe>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=_Using-Notebooks.ipynb"></iframe>\n',
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
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter08-Strings-and-Regex-v2.ipynb"></iframe>\n',
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
    # Chapters 9-13's pages also embed a live JupyterLite iframe of
    # themselves, same recursive-embed problem and same fix as chap01.ipynb
    # above. Chrome scope extended from 1-11 to 1-13, 2026-09-09 (maintainer
    # decision -- see AUDIT.md and mods/pass-4-chrome.md).
    "chap09.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="09" -->\n',
            '<p id="chap09-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap09-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap09-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap09-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter09-Lists.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap09-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap09-jupyterlite-pane");\n',
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
    "chap10.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="10" -->\n',
            '<p id="chap10-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap10-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap10-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap10-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter10-Dictionaries.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap10-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap10-jupyterlite-pane");\n',
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
    "chap11.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="11" -->\n',
            '<p id="chap11-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap11-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap11-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap11-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter11-Tuples.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap11-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap11-jupyterlite-pane");\n',
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
    "chap12.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="12" -->\n',
            '<p id="chap12-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap12-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap12-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap12-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter12-Text-Analysis-and-Generation.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap12-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap12-jupyterlite-pane");\n',
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
    "chap13.ipynb": {
        (
            '<!-- apcsp:begin type="note" chapter="13" -->\n',
            '<p id="chap13-jupyterlite-note"><em>Ignore this cell — used when running JupyterLite.</em></p>\n',
            '\n',
            '<style>\n',
            '#pst-secondary-sidebar { display: none !important; }\n',
            '#chap13-jupyterlite-pane {\n',
            '  display: block;\n',
            '  height: 600px;\n',
            '  background: #fff;\n',
            '  overflow: hidden;\n',
            '}\n',
            '#chap13-jupyterlite-pane iframe {\n',
            '  display: block;\n',
            '  width: 100%;\n',
            '  height: 100%;\n',
            '  border: 0;\n',
            '}\n',
            '</style>\n',
            '<div id="chap13-jupyterlite-pane">\n',
            f'<iframe src="{DEPLOY_PATH_PLACEHOLDER}/notebooks/index.html?path=Chapter13-Files-and-Databases.ipynb"></iframe>\n',
            '</div>\n',
            '<script>\n',
            '(function () {\n',
            '  var note = document.getElementById("chap13-jupyterlite-note");\n',
            '  var pane = document.getElementById("chap13-jupyterlite-pane");\n',
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
        ("# this cell installs the pyyaml package, which provides the yaml module\n", "\n", "try:\n", "    import yaml\n", "except ImportError:\n", "    !pip install pyyaml"): (
            "# this cell installs the pyyaml package, which provides the yaml module\n",
            "\n",
            "try:\n",
            "    import yaml\n",
            "except ImportError:\n",
            "    import micropip\n",
            "    await micropip.install('pyyaml')",
        ),
        # `!unzip` has no shell to run in under Pyodide either -- same class of
        # bug as chap08's `!head`/`!tail` above. `extractall()` overwrites
        # existing files the same way `-o` does, so this is a direct swap.
        ("!unzip -o photos.zip",): (
            "import zipfile\n",
            "zipfile.ZipFile('photos.zip').extractall()",
        ),
        (
            "# When you open a shelve file, a backup file is created that has the suffix `.bak`.\n",
            "# If you run this notebook more than once, you might see that file left behind.\n",
            "# This cell removes it so the output shown in the book is correct.\n",
            "\n",
            "!rm -f photo_info/captions.bak",
        ): (
            "# When you open a shelve file, a backup file is created that has the suffix `.bak`.\n",
            "# If you run this notebook more than once, you might see that file left behind.\n",
            "# This cell removes it so the output shown in the book is correct.\n",
            "\n",
            "import os\n",
            "if os.path.exists('photo_info/captions.bak'):\n",
            "    os.remove('photo_info/captions.bak')",
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
        for alias_name in ALIASES.get(notebook, []):
            write_notebook_variant(src, notebook, deps, deploy_id, alias_name)

        for dep in deps:
            dep_src = ROOT / dep
            if not dep_src.exists():
                print(f"error: {dep_src} not found", file=sys.stderr)
                return 1
            shutil.copy(dep_src, CONTENT_DIR / dep)

        teach_name = teach_name_for(notebook)
        projector_src = PROJECTOR_DIR / notebook
        if SHIP_TEACH_COPIES and projector_src.exists() and teach_name:
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
