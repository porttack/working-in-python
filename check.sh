#!/usr/bin/env bash
#
# Read-only checks on one chapter notebook, or all of them. Never writes to a
# file -- safe to run any time, mid-edit or before a commit. Companion to
# `make check` (build_blanks --check + check_sync.py + jupyterlite --check),
# not a replacement -- still run `make check` before committing.
#
# What gets checked (see tools/check_notebook.py for the actual logic):
#   - the file parses as notebook JSON
#   - sentinel blocks (apcsp:begin/end) are balanced and use a valid type
#   - blank markers only appear in chapters whose treatment tier allows them
#   - AP/CA standards codes cited in the chapter resolve against standards/*.json
#   - a cell-level diff against upstream/v3 (informational count, not pass/fail)
#   - any notebook output or execution_count in the working tree that wasn't
#     already in the last commit (catches "ran it, forgot to clear outputs")
#
# Usage:
#   ./check.sh              check every chapters/*.ipynb
#   ./check.sh chap09       check just chapters/chap09.ipynb
#   ./check.sh -h/--help    full option list

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$REPO/.venv/bin/activate"
cd "$REPO"
exec python3 tools/check_notebook.py "$@"
