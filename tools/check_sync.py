#!/usr/bin/env python3
"""Verify structural invariants across chapters/ before a commit.

Checks:
  1. Sentinel blocks (<!-- apcsp:begin type="..." chapter="NN" --> ... <!-- apcsp:end -->)
     are balanced, well-formed, and use a valid `type`.
  2. Every AP/CA standards code referenced in a chapter resolves against
     standards/apcsp.json and standards/castandards.json -- skipped while those
     indexes are still empty (Pass 1/2), since there's nothing to resolve against yet.
  3. No chapter outside its blank-marker treatment tier (CLAUDE.md's treatment matrix)
     carries blank markers: chapters 1-13 may have them, chapters 14-19 (and
     non-numbered front matter) may not.

Exit codes: 0 clean, 1 one or more problems found (all are printed, not just the first).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "chapters"
STANDARDS_DIR = ROOT / "standards"

VALID_SENTINEL_TYPES = {"standards", "glossary", "exercise", "note", "pseudocode"}

# chapters 14-19 (independent study) get no blank markers at all (CLAUDE.md treatment
# matrix). chap00 and jupyter_intro are front matter, never numbered chapters, and never
# get blank markers either.
NO_BLANK_MARKER_CHAPTERS = {f"chap{n:02d}" for n in range(14, 20)} | {"chap00", "jupyter_intro"}

SENTINEL_BEGIN_RE = re.compile(
    r'<!--\s*apcsp:begin\s+type="([^"]*)"(?:\s+chapter="([^"]*)")?\s*-->'
)
SENTINEL_END_RE = re.compile(r'<!--\s*apcsp:end\s*-->')

BLANK_MARKER_RE = re.compile(r'<!--blank-->|<!--/blank-->|<!--blank-only:|#\s?blank\s*$', re.M)

AP_CODE_RE = re.compile(r'\b[A-Z]{2,4}-\d+\.[A-Za-z0-9]+\b')
CA_CODE_RE = re.compile(r'\b\d{1,2}-\d{1,2}\.[A-Z]{2,4}\.\d+\b')


def read_text(path):
    if path.suffix == ".ipynb":
        try:
            nb = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return ""
        parts = []
        for cell in nb.get("cells", []):
            src = cell.get("source", "")
            parts.append("".join(src) if isinstance(src, list) else (src or ""))
        return "\n".join(parts)
    return path.read_text(encoding="utf-8")


def check_sentinels(name, text, problems):
    begins = list(SENTINEL_BEGIN_RE.finditer(text))
    end_count = len(SENTINEL_END_RE.findall(text))
    if len(begins) != end_count:
        problems.append(
            f"{name}: {len(begins)} apcsp:begin vs {end_count} apcsp:end -- unbalanced"
        )
    for m in begins:
        sentinel_type = m.group(1)
        if sentinel_type not in VALID_SENTINEL_TYPES:
            problems.append(
                f"{name}: invalid sentinel type {sentinel_type!r} "
                f"(valid: {', '.join(sorted(VALID_SENTINEL_TYPES))})"
            )
    # A begin tag that's malformed (missing its type attribute, missing "-->", etc.)
    # won't match SENTINEL_BEGIN_RE, so it won't be counted in `begins` even though the
    # literal string "apcsp:begin" is present in the file. That silently produces a
    # mismatch against the apcsp:end count, which the unbalanced check above already
    # catches -- so malformed begin tags surface as "unbalanced" rather than needing a
    # separate stray-tag scan.
    return begins


def check_standards_codes(name, text, apcsp_codes, castandards_codes, problems):
    if not apcsp_codes and not castandards_codes:
        return  # indexes empty -- pass 1/2, nothing to resolve against yet
    for code in AP_CODE_RE.findall(text):
        if apcsp_codes and code not in apcsp_codes:
            problems.append(f"{name}: AP code {code!r} not found in standards/apcsp.json")
    for code in CA_CODE_RE.findall(text):
        if castandards_codes and code not in castandards_codes:
            problems.append(f"{name}: CA code {code!r} not found in standards/castandards.json")


def check_blank_marker_tier(name, stem, text, problems):
    if stem in NO_BLANK_MARKER_CHAPTERS and BLANK_MARKER_RE.search(text):
        problems.append(
            f"{name}: contains blank markers but {stem} is in the no-markers tier "
            f"(chapters 14-19 / front matter, per CLAUDE.md treatment matrix)"
        )


def load_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def apcsp_valid_codes(data):
    # Placeholder shape (pre-Pass-3-Step-1) is `{}` -- no "topics" key, empty set.
    # Real shape: topic-level codes ("3.10") plus each topic's nested LO codes
    # ("AAP-2.N"), since a chapter insert or exercise note might cite either.
    codes = set()
    for topic in data.get("topics", []):
        if "code" in topic:
            codes.add(topic["code"])
        codes.update(topic.get("los", []))
    return codes


def castandards_valid_codes(data):
    # Placeholder shape is `{}` -- no "standards" key, empty set.
    return {s["code"] for s in data.get("standards", []) if "code" in s}


def main():
    if not CHAPTERS_DIR.is_dir():
        print(f"error: {CHAPTERS_DIR} not found", file=sys.stderr)
        return 1

    apcsp_codes = apcsp_valid_codes(load_json(STANDARDS_DIR / "apcsp.json"))
    castandards_codes = castandards_valid_codes(load_json(STANDARDS_DIR / "castandards.json"))

    problems = []
    sources = sorted(
        p for p in CHAPTERS_DIR.iterdir()
        if p.suffix in (".ipynb", ".md") and not p.name.startswith(".")
    )

    for path in sources:
        text = read_text(path)
        check_sentinels(path.name, text, problems)
        check_standards_codes(path.name, text, apcsp_codes, castandards_codes, problems)
        check_blank_marker_tier(path.name, path.stem, text, problems)

    if problems:
        print(f"check_sync: {len(problems)} problem(s) found", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1

    skip_note = ""
    if not apcsp_codes and not castandards_codes:
        skip_note = " (standards code resolution skipped -- indexes are empty)"
    print(f"check_sync: clean ({len(sources)} files checked){skip_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
