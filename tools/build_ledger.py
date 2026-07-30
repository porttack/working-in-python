#!/usr/bin/env python3
"""Generate CHANGELOG_DETAIL.md from data/exercise-ledger.json.

Idempotent: running it twice with an unchanged ledger produces byte-identical output.
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = ROOT / "data" / "exercise-ledger.json"
OUTPUT_PATH = ROOT / "CHANGELOG_DETAIL.md"

BANNER = (
    "<!-- GENERATED FILE. Do not hand-edit. -->\n"
    "<!-- Source: data/exercise-ledger.json -->\n"
    "<!-- Regenerate with: python3 tools/build_ledger.py (or `make ledger`) -->\n"
)


def load_ledger():
    with open(LEDGER_PATH) as f:
        return json.load(f)


def render(entries):
    by_chapter = defaultdict(list)
    for e in entries:
        by_chapter[e["chapter"]].append(e)

    lines = [BANNER, "", "# Changelog Detail", ""]
    lines.append(
        "Per-exercise record generated from `data/exercise-ledger.json`. "
        "See `AP_MODIFICATIONS.md` for the prose explanation and `CHANGELOG.md` "
        "for the dated summary."
    )
    lines.append("")

    kind_totals = defaultdict(int)
    action_totals = defaultdict(int)

    for chapter in sorted(by_chapter):
        chapter_entries = sorted(by_chapter[chapter], key=lambda e: e["id"])
        lines.append(f"## {chapter}")
        lines.append("")
        lines.append(f"{len(chapter_entries)} exercise(s).")
        lines.append("")
        lines.append("| ID | Anchor | Kind | Action | Replacement | Min before | Min after |")
        lines.append("|---|---|---|---|---|---|---|")
        for e in chapter_entries:
            kind_totals[e["kind"]] += 1
            action_totals[e["action"]] += 1
            lines.append(
                f"| {e['id']} | {e['anchor']} | {e['kind']} | {e['action']} | "
                f"{e['replacement_id'] or '—'} | {e['est_minutes_before']} | "
                f"{e['est_minutes_after']} |"
            )
        lines.append("")

    lines.append("## Totals")
    lines.append("")
    lines.append(f"Total exercises: {len(entries)}")
    lines.append("")
    lines.append("By kind: " + ", ".join(f"{k}={v}" for k, v in sorted(kind_totals.items())))
    lines.append("")
    lines.append("By action: " + ", ".join(f"{k}={v}" for k, v in sorted(action_totals.items())))
    lines.append("")

    return "\n".join(lines)


def main():
    if not LEDGER_PATH.exists():
        print(f"error: {LEDGER_PATH} not found", file=sys.stderr)
        return 1
    entries = load_ledger()
    output = render(entries)
    OUTPUT_PATH.write_text(output)
    print(f"wrote {OUTPUT_PATH} ({len(entries)} exercises)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
