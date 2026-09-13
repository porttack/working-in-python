#!/usr/bin/env bash
#
# Fetch a single chapter notebook fresh from GitHub. The normal weekly way to
# get a chapter is still typing the curl command by hand -- see the "Using a
# Codespace" page. This is a convenience for the exceptions: re-fetching a
# chapter you already have (a fix went out after you downloaded it), or
# grabbing one out of the usual order (catching up, review).
#
# Usage:
#   ./fetch.sh 3          fetch chapter 3 -- asks before overwriting an
#                         existing chap03.ipynb
#   ./fetch.sh 6b         fetch interlude 6b (chap06b.ipynb)
#   ./fetch.sh -f 3       fetch chapter 3, overwriting without asking
#   ./fetch.sh -h         this message
#
# Behaves like cp/mv when the target already exists: asks first, unless -f.

set -euo pipefail

usage() {
  sed -n '2,/^[^#]/p' "${BASH_SOURCE[0]}" | sed '$d' | sed 's/^#$//; s/^# //'
}

FORCE=0
CHAPTER=""

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    -f|--force)
      FORCE=1
      shift
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [ -n "$CHAPTER" ]; then
        echo "One chapter at a time." >&2
        exit 1
      fi
      CHAPTER="$1"
      shift
      ;;
  esac
done

if [ -z "$CHAPTER" ]; then
  usage >&2
  exit 1
fi

if [[ "$CHAPTER" =~ ^([0-9]{1,2})([a-zA-Z]?)$ ]]; then
  PADDED=$(printf "%02d" "${BASH_REMATCH[1]}")
  FILENAME="chap${PADDED}${BASH_REMATCH[2]}.ipynb"
else
  echo "Not a chapter number: $CHAPTER (try something like 3 or 6b)" >&2
  exit 1
fi

if [ -e "$FILENAME" ] && [ "$FORCE" -ne 1 ]; then
  REPLY=""
  read -r -p "$FILENAME already exists. Overwrite? (y/N) " REPLY || true
  case "$REPLY" in
    [yY]|[yY][eE][sS]) ;;
    *)
      echo "Not overwriting $FILENAME."
      exit 0
      ;;
  esac
fi

URL="https://raw.githubusercontent.com/porttack/working-in-python/v3/chapters/${FILENAME}"
echo "Fetching ${FILENAME} ..."
curl -fL -o "$FILENAME" "$URL"
echo "Wrote ${FILENAME}."
