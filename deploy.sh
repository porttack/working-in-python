#!/usr/bin/env bash
#
# One-shot deploy: push the current branch, then build and publish the
# site to gh-pages via jb/build.sh (which does the real work -- Sphinx
# build, JupyterLite rebuild, force-push to gh-pages). No --local pause;
# this always publishes for real.
#
# Usage:
#   ./deploy.sh                    push + build + publish
#   ./deploy.sh "commit message"   also commit all pending tracked changes first
#
# git add -u only stages modifications/deletions to already-tracked files
# (never new untracked files), so stray files like .DS_Store are never
# swept in by accident.

set -euo pipefail
cd "$(dirname "$0")"

if [[ $# -gt 0 ]]; then
  git add -u
  git commit -m "$1"
fi

git push origin "$(git branch --show-current)"

source .venv/bin/activate
cd jb
./build.sh
