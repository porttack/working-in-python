#!/usr/bin/env python3
"""Fetch a single chapter notebook fresh from GitHub.

The normal weekly way to get a chapter is still typing the curl command by
hand -- see the "Using a Codespace" page. This is a convenience for the
exceptions: re-fetching a chapter you already have (a fix went out after you
downloaded it), or grabbing one out of the usual order (catching up, review).

Uses urlretrieve() the same way every chapter's own bootstrap download()
cell does -- no extra package to install.
"""
import argparse
import re
import sys
from os.path import exists
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve

BASE_URL = "https://raw.githubusercontent.com/porttack/working-in-python/v3/chapters"


def normalize(chapter):
    """Turn "3" or "6b" into "chap03.ipynb" / "chap06b.ipynb", or None if
    chapter isn't shaped like a chapter number."""
    match = re.fullmatch(r"(\d{1,2})([a-zA-Z]?)", chapter)
    if not match:
        return None
    number, letter = match.groups()
    return f"chap{int(number):02d}{letter}.ipynb"


def main():
    parser = argparse.ArgumentParser(
        description="Fetch a single chapter notebook fresh from GitHub.",
        epilog="Behaves like cp/mv when the target already exists: asks first, unless -f.",
    )
    parser.add_argument("chapter", help="a chapter number (3) or interlude (6b)")
    parser.add_argument(
        "-f", "--force", action="store_true",
        help="overwrite an existing file without asking",
    )
    args = parser.parse_args()

    filename = normalize(args.chapter)
    if filename is None:
        print(f"Not a chapter number: {args.chapter} (try something like 3 or 6b)",
              file=sys.stderr)
        return 1

    if exists(filename) and not args.force:
        reply = input(f"{filename} already exists. Overwrite? (y/N) ")
        if reply.strip().lower() not in ("y", "yes"):
            print(f"Not overwriting {filename}.")
            return 0

    url = f"{BASE_URL}/{filename}"
    print(f"Fetching {filename} ...")
    try:
        urlretrieve(url, filename)
    except HTTPError as e:
        print(f"Could not fetch {filename}: {e}", file=sys.stderr)
        return 1
    except URLError as e:
        print(f"Could not reach GitHub: {e}", file=sys.stderr)
        return 1

    print(f"Wrote {filename}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
