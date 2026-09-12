#!/usr/bin/env python3
"""Read-only checks for one chapter notebook, or all of them. Never modifies a file.

Reuses check_sync.py's sentinel / blank-marker-tier / standards-code checks (the same
logic `make check` runs book-wide) and adds two checks check_sync.py doesn't do:

  - a cell-level diff against upstream/v3 (informational -- the human-eyeball step
    CLAUDE.md's "Done, every pass" list already asks for, just automated as a count)
  - a check for any notebook output or execution_count present in the working tree
    that wasn't already in the last commit (catches "I ran this notebook and forgot
    to clear outputs" before it becomes part of a diff)

Does not touch the open "nbstripout across the whole book" question in AUDIT.md --
that's about upstream's own pre-existing outputs, which this deliberately leaves alone.
This only flags drift you are about to introduce yourself.

Usage:
  python3 tools/check_notebook.py              every chapters/*.ipynb
  python3 tools/check_notebook.py chap09        just chapters/chap09.ipynb
  python3 tools/check_notebook.py chap09.ipynb  (same)
  python3 tools/check_notebook.py chapters/chap09.ipynb   (same)

Exit codes: 0 nothing failed, 1 one or more problems found (all printed, not just
the first). Upstream-diff and untracked-output notes are informational and never
affect the exit code.
"""
import argparse
import difflib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "chapters"

import check_sync  # noqa: E402 -- lives next to this file; reuse its checks, don't reimplement them


def resolve_target(name):
    """Turn a bare stem, filename, or path into a chapters/*.ipynb Path, or None."""
    p = Path(name)
    for candidate in (p, CHAPTERS_DIR / p.name, CHAPTERS_DIR / f"{name}.ipynb"):
        if candidate.is_file():
            return candidate
    return None


def git_show(rev, rel_path):
    """Text of rel_path at rev, or None if it doesn't exist there."""
    result = subprocess.run(
        ["git", "show", f"{rev}:{rel_path}"], cwd=ROOT, capture_output=True, text=True
    )
    return result.stdout if result.returncode == 0 else None


def load_notebook(text):
    try:
        nb = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
    return nb if isinstance(nb, dict) and isinstance(nb.get("cells"), list) else None


def cell_sources(nb):
    return [
        "".join(c["source"]) if isinstance(c.get("source"), list) else (c.get("source") or "")
        for c in nb["cells"]
    ]


def check_upstream_diff(name, rel_path, nb, notes):
    upstream_text = git_show("upstream/v3", rel_path)
    if upstream_text is None:
        notes.append(f"{name}: no upstream/v3 counterpart (interlude or new material) -- skipped")
        return
    upstream_nb = load_notebook(upstream_text)
    if upstream_nb is None:
        notes.append(f"{name}: upstream/v3 copy doesn't parse -- skipped")
        return
    theirs, ours = cell_sources(upstream_nb), cell_sources(nb)
    equal = edited = inserted = deleted = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=theirs, b=ours, autojunk=False).get_opcodes():
        if tag == "equal":
            equal += i2 - i1
        elif tag == "replace":
            edited += max(i2 - i1, j2 - j1)
        elif tag == "delete":
            deleted += i2 - i1
        elif tag == "insert":
            inserted += j2 - j1
    notes.append(
        f"{name}: vs upstream/v3 -- {equal} unchanged, {edited} edited, "
        f"{inserted} inserted, {deleted} deleted (of {len(theirs)} upstream cells)"
    )


def check_output_drift(name, rel_path, nb, problems, notes):
    flagged = [
        i for i, c in enumerate(nb["cells"])
        if c.get("cell_type") == "code" and (c.get("outputs") or c.get("execution_count") is not None)
    ]
    head_text = git_show("HEAD", rel_path)
    if head_text is None:
        if flagged:
            notes.append(
                f"{name}: untracked, {len(flagged)} code cell(s) carry output/execution_count "
                f"-- nothing committed yet to compare against"
            )
        return
    head_nb = load_notebook(head_text)
    if head_nb is None:
        notes.append(f"{name}: committed version doesn't parse -- skipped drift check")
        return
    head_cells = head_nb["cells"]
    if len(head_cells) != len(nb["cells"]):
        notes.append(
            f"{name}: cell count changed since last commit ({len(head_cells)} -> {len(nb['cells'])}) "
            f"-- skipped cell-aligned output/execution_count drift check"
        )
        return
    drifted = [
        i for i, (old, new) in enumerate(zip(head_cells, nb["cells"]))
        if new.get("cell_type") == "code"
        and ((old.get("outputs") or []) != (new.get("outputs") or [])
             or old.get("execution_count") != new.get("execution_count"))
    ]
    if drifted:
        problems.append(
            f"{name}: {len(drifted)} code cell(s) have new/changed outputs or execution_count "
            f"vs last commit (cell indices {drifted}) -- probably just ran the notebook; "
            f"clear outputs before committing"
        )


def check_one(path, apcsp_codes, castandards_codes, problems, notes):
    name = path.name
    text = path.read_text(encoding="utf-8")
    nb = load_notebook(text)
    if nb is None:
        problems.append(f"{name}: does not parse as notebook JSON (no top-level \"cells\" list)")
        return
    flat_text = check_sync.read_text(path)
    check_sync.check_sentinels(name, flat_text, problems)
    check_sync.check_standards_codes(name, flat_text, apcsp_codes, castandards_codes, problems)
    check_sync.check_blank_marker_tier(name, path.stem, flat_text, problems)

    rel_path = str(path.relative_to(ROOT))
    check_upstream_diff(name, rel_path, nb, notes)
    check_output_drift(name, rel_path, nb, problems, notes)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  Just finished editing chap09, before committing:\n"
            "    ./check.sh chap09\n"
            "\n"
            "  About to make a big commit touching several chapters:\n"
            "    ./check.sh\n"
            "\n"
            "  Ran a notebook interactively while testing a change and aren't sure\n"
            "  whether outputs/execution_counts got saved along with it:\n"
            "    ./check.sh chap09    # flags it under \"new/changed outputs\" if so\n"
        ),
    )
    parser.add_argument(
        "target", nargs="?", default=None,
        help="a chapter stem (chap09), filename (chap09.ipynb), or path; "
             "omit to check every chapters/*.ipynb",
    )
    args = parser.parse_args()

    if args.target:
        path = resolve_target(args.target)
        if path is None:
            print(f"error: no notebook found matching {args.target!r}", file=sys.stderr)
            return 1
        paths = [path]
    else:
        paths = sorted(CHAPTERS_DIR.glob("*.ipynb"))

    apcsp_codes = check_sync.apcsp_valid_codes(check_sync.load_json(ROOT / "standards" / "apcsp.json"))
    castandards_codes = check_sync.castandards_valid_codes(
        check_sync.load_json(ROOT / "standards" / "castandards.json")
    )

    problems, notes = [], []
    for path in paths:
        check_one(path, apcsp_codes, castandards_codes, problems, notes)

    for n in notes:
        print(n)

    if problems:
        print(f"\ncheck_notebook: {len(problems)} problem(s) found", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1

    print(f"\ncheck_notebook: clean ({len(paths)} file(s) checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
