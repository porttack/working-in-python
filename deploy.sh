#!/usr/bin/env bash
#
# Build (and optionally commit/push/publish) the Working in Python site. No
# manual venv activation needed -- wraps jb/build.sh (see HOW_TO_EDIT.md /
# PUBLISHING.md for what it actually does under the hood). Flags can combine;
# whatever's given runs in this order: commit, push, build.
#
# Usage:
#   ./deploy.sh --local             build only (site + JupyterLite) into
#                                    jb/_build/html -- never publishes.
#                                    Always run this before --publish.
#   ./deploy.sh --publish           the above, then force-pushes gh-pages --
#                                    goes live at python.porttack.com. Asks
#                                    for a typed confirmation first.
#   ./deploy.sh --commit "message"  git add -u && commit tracked changes
#                                    (never adds new untracked files) before
#                                    whatever else is asked for
#   ./deploy.sh --push              git push origin <current branch>
#
#   # combine for the old one-shot habit:
#   ./deploy.sh --commit "message" --push --publish
#
#   ./deploy.sh --help              this message
#
# No args, or --commit/--push with no build flag, does no build/publish --
# running deploy.sh out of habit with no flags just prints this message.
#
# There's no separate merge-to-v3 step: v3 is the branch you commit to and
# publish from directly (jb/build.sh builds v3 -> gh-pages). The unrelated
# `v3-preview` branch is a separate static snapshot site, not part of this
# pipeline -- this script does not touch it.
#
# jb/build.sh itself refuses to run at all if ../chapters/ has uncommitted
# changes, so use --commit (or commit yourself) before --local/--publish.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  sed -n '2,/^[^#]/p' "${BASH_SOURCE[0]}" | sed '$d' | sed 's/^#$//; s/^# //'
}

commit_msg=""
do_push=0
mode=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --commit)
      commit_msg="${2:?--commit requires a message}"
      shift 2
      ;;
    --push)
      do_push=1
      shift
      ;;
    --local|--publish)
      mode="$1"
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$commit_msg" && "$do_push" -eq 0 && -z "$mode" ]]; then
  usage
  exit 0
fi

if [[ -n "$commit_msg" ]]; then
  git -C "$REPO" add -u
  git -C "$REPO" commit -m "$commit_msg"
fi

if [[ "$do_push" -eq 1 ]]; then
  git -C "$REPO" push origin "$(git -C "$REPO" branch --show-current)"
fi

case "$mode" in
  --local)
    source "$REPO/.venv/bin/activate"
    cd "$REPO/jb"
    ./build.sh --local
    ;;
  --publish)
    source "$REPO/.venv/bin/activate"
    cd "$REPO/jb"
    echo "This force-pushes gh-pages and goes live at https://python.porttack.com/"
    read -r -p "Type 'publish' to continue: " confirm
    if [[ "$confirm" != "publish" ]]; then
      echo "Aborted." >&2
      exit 1
    fi
    ./build.sh
    ;;
esac
