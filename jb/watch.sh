#!/usr/bin/env bash
#
# Live-reload local preview.
#
#   one-time:  pip install jupyter-book ghp-import sphinx-autobuild
#   usage:     cd jb && ./watch.sh
#
# Unlike build.sh, this does not require a clean ../chapters/ tree and never
# publishes. It watches ../chapters/*.ipynb -- the source of truth -- and on
# every save re-runs the same copy + prep_notebooks.py step build.sh does,
# then rebuilds and refreshes the browser. Stop with Ctrl-C.
#
# Two things must be excluded from the watch, or every build retriggers the
# next one forever: the chap*.ipynb copies this script writes into jb/ (the
# same source directory sphinx-autobuild watches by default -- prep_notebooks.py
# rewrites them on every build), and _build/, the output directory, which
# lives inside that same watched source directory.
#
# Sphinx normally only re-renders pages whose source changed since the last
# build. That incremental cache is usually what you want, but pass --clean
# to wipe _build/ first and force every page to render from scratch:
#
#   ./watch.sh --clean

set -euo pipefail

if [[ "${1:-}" == "--clean" ]]; then
  rm -rf _build
fi

rm -f chap*.ipynb jupyter_intro.ipynb
cp ../chapters/chap[0-1][0-9].ipynb .
cp ../chapters/jupyter_intro.ipynb .
python prep_notebooks.py

# jb build does this step implicitly. sphinx-autobuild drives sphinx
# directly, so conf.py has to be generated once, up front, ourselves.
# jb/conf.py is gitignored; treat it as disposable, like jb/chap*.ipynb.
jb config sphinx .

exec sphinx-autobuild . _build/html \
  --watch ../chapters \
  --re-ignore '.*/jb/chap[0-9]+\.ipynb$' \
  --re-ignore '.*/jb/jupyter_intro\.ipynb$' \
  --re-ignore '.*/jb/_build/.*' \
  --pre-build "bash -c 'rm -f chap*.ipynb jupyter_intro.ipynb && cp ../chapters/chap[0-1][0-9].ipynb . && cp ../chapters/jupyter_intro.ipynb . && python prep_notebooks.py'" \
  --open-browser
