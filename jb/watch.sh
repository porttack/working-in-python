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

# chap01.ipynb and jupyter_intro.ipynb carry a placeholder instead of a
# hardcoded JupyterLite deploy path (see tools/build_jupyterlite_content.py);
# prep_notebooks.py substitutes it using this id. Computed once here, at
# startup, not per-rebuild -- watch.sh never rebuilds the JupyterLite side
# itself (see HOW_TO_EDIT.md for that), so a fixed id for the whole session
# is what actually matches whatever's sitting in jb/_build/html/. `export`
# here reaches the --pre-build subprocess below too, since it inherits this
# script's environment.
export JUPYTERLITE_DEPLOY_ID=$(cd .. && python3 tools/build_jupyterlite_content.py --print-deploy-id)

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
