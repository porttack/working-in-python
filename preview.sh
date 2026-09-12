#!/usr/bin/env bash
#
# Local preview of the Working in Python site. No manual venv activation
# needed -- this activates the project's own .venv and delegates to the
# existing jb/ scripts and Makefile targets (see HOW_TO_EDIT.md for what
# each one does under the hood).
#
# Usage:
#   ./preview.sh              fast preview, auto-reload on save (jb/watch.sh)
#                             http://localhost:8000/ -- skips JupyterLite
#   ./preview.sh --clean      same, but wipe jb/_build first
#   ./preview.sh --full       full local build incl. JupyterLite
#                             (jb/build.sh --local), then serve it once at
#                             :8000 -- no auto-reload, use this as a last
#                             check before publishing
#   ./preview.sh --lite       standalone JupyterLite only, no site chrome
#                             (make jupyterlite + jupyterlite-serve),
#                             served at :8123
#   ./preview.sh --help       this message
#
# Nothing here ever publishes -- that's jb/build.sh with no flag, a separate,
# deliberate step. Stop any mode with Ctrl-C.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  sed -n '2,21p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
  --full)
    source "$REPO/.venv/bin/activate"
    cd "$REPO/jb"
    ./build.sh --local
    echo
    echo "Serving jb/_build/html at http://localhost:8000/ (Ctrl-C to stop; no auto-reload)"
    exec python3 -m http.server 8000 --directory _build/html
    ;;
  --lite)
    source "$REPO/.venv/bin/activate"
    cd "$REPO"
    make jupyterlite
    echo
    echo "Serving jupyterlite/_output at http://localhost:8123/ (Ctrl-C to stop)"
    exec make jupyterlite-serve
    ;;
  --clean|"")
    source "$REPO/.venv/bin/activate"
    cd "$REPO/jb"
    exec ./watch.sh "$@"
    ;;
  *)
    echo "Unknown option: $1" >&2
    usage >&2
    exit 1
    ;;
esac
