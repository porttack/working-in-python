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
#
# Alongside sphinx-autobuild's own --open-browser window (whatever the OS
# default browser is, sized however that browser last left it), this also
# opens a second, independent Safari window pinned to 390x844 -- an iPhone
# 12/13/14 portrait viewport -- so a chapter's embedded JupyterLite pane can
# be checked at actual phone width without resizing, or disturbing, the
# normal-size window. Defaults to jupyter_intro.html; override with:
#
#   PHONE_PATH=chap03.html ./watch.sh

set -euo pipefail

if [[ "${1:-}" == "--clean" ]]; then
  rm -rf _build
fi

rm -f chap*.ipynb jupyter_intro.ipynb index.ipynb
cp ../chapters/chap[0-1][0-9].ipynb .
cp ../chapters/jupyter_intro.ipynb .
cp ../chapters/index.ipynb .

# chap01.ipynb, jupyter_intro.ipynb, and index.ipynb carry a placeholder instead
# of a hardcoded JupyterLite deploy path (see tools/build_jupyterlite_content.py);
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

# Backgrounded so it never blocks the exec below. Polls instead of reusing
# sphinx-autobuild's own --open-browser delay/race (see utils.open_browser in
# the sphinx_autobuild package: it opens the browser, via a fixed sleep, then
# starts uvicorn -- the browser request often lands before the port exists)
# because a Safari window that opens before anything is listening does not
# retry, it just shows "can't connect".
PHONE_PATH="${PHONE_PATH:-jupyter_intro.html}"
(
  for _ in $(seq 1 60); do
    curl -s -o /dev/null "http://127.0.0.1:8000/" && break
    sleep 0.5
  done
  osascript <<OSA
tell application "Safari"
  activate
  make new document with properties {URL:"http://127.0.0.1:8000/$PHONE_PATH"}
  set bounds of front window to {80, 80, 470, 924}
end tell
OSA
) &

exec sphinx-autobuild . _build/html \
  --watch ../chapters \
  --re-ignore '.*/jb/chap[0-9]+\.ipynb$' \
  --re-ignore '.*/jb/jupyter_intro\.ipynb$' \
  --re-ignore '.*/jb/index\.ipynb$' \
  --re-ignore '.*/jb/_build/.*' \
  --pre-build "bash -c 'rm -f chap*.ipynb jupyter_intro.ipynb index.ipynb && cp ../chapters/chap[0-1][0-9].ipynb . && cp ../chapters/jupyter_intro.ipynb . && cp ../chapters/index.ipynb . && python prep_notebooks.py'" \
  --open-browser
