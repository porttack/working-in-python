#!/usr/bin/env python3
"""
build_blanks.py - generate fill-in-the-blank teaching copies from chapter sources.

    python3 tools/build_blanks.py                 # build blanks/ from chapters/
    python3 tools/build_blanks.py --check         # exit 1 if blanks/ is stale
    python3 tools/build_blanks.py --only chap09   # rebuild one chapter

Design: chapters/ is the single source of truth and needs NO build step. All markers
are HTML comments, which Jupyter and Markdown render as invisible, so a chapter file
displays correctly as written. Only blanks/ is generated.

MARKERS

  Prose (markdown cells):

    <!--blank-->the visible text<!--/blank-->
        chapters: renders "the visible text" (the comments are invisible)
        blanks:   replaced with underscores, sized to the original

    <!--blank-only: text that appears only in the blanks version-->
        chapters: invisible
        blanks:   renders the text
        Use for prompts, e.g. "<!--blank-only: What does this loop do?-->"

  Code (code cells):

    any line ending in "# blank" or "#blank"
        blanks: the code on that line is replaced with underscores, indentation kept

    a cell tagged "blank" in its metadata
        blanks: the whole cell body is replaced with a stub

Stdlib only. No dependencies.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------- config

GENERATED_BANNER = "GENERATED FROM {src} - DO NOT EDIT. Source of truth is chapters/."

MIN_RULE = 8      # shortest blank line
MAX_RULE = 48     # longest blank line
CODE_STUB = "# your code here"

BLANK_RE = re.compile(r"<!--blank-->(.*?)<!--/blank-->", re.DOTALL)
BLANK_ONLY_RE = re.compile(r"<!--blank-only:(.*?)-->", re.DOTALL)
CODE_BLANK_RE = re.compile(r"^(\s*)(.*?)\s*#\s?blank\s*$")


# ----------------------------------------------------------------------- transforms

def rule(text):
    """An underscore run roughly proportional to what it replaces."""
    n = len(text.strip())
    return "_" * max(MIN_RULE, min(n, MAX_RULE))


def blank_markdown(text):
    """Apply prose markers to one markdown cell."""
    text = BLANK_RE.sub(lambda m: rule(m.group(1)), text)
    text = BLANK_ONLY_RE.sub(lambda m: m.group(1).strip(), text)
    return text


def strip_markdown(text):
    """What a chapter cell looks like once markers are resolved for the full version.

    Used only by --check to confirm markers are well-formed; chapters are never
    rewritten by this script.
    """
    text = BLANK_RE.sub(lambda m: m.group(1), text)
    text = BLANK_ONLY_RE.sub("", text)
    return text


def blank_code(source, tagged):
    """Apply code markers to one code cell."""
    if tagged:
        lines = source.splitlines()
        head = lines[0] if lines else ""
        keep = head if head.strip() else ""
        # Match the indentation of the first non-blank body line so the stub stays
        # syntactically plausible under a def/for/if header.
        indent = ""
        for line in lines[1:]:
            if line.strip():
                indent = line[: len(line) - len(line.lstrip())]
                break
        if not indent and keep.rstrip().endswith(":"):
            indent = "    "
        body = [keep] if keep else []
        body.append(f"{indent}{CODE_STUB}")
        return "\n".join(body) + "\n"

    out = []
    for line in source.splitlines():
        m = CODE_BLANK_RE.match(line)
        if m:
            indent, code = m.group(1), m.group(2)
            out.append(f"{indent}{rule(code)}")
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if source.endswith("\n") else "")


# ------------------------------------------------------------------------- notebooks

def as_text(src):
    return "".join(src) if isinstance(src, list) else (src or "")


def transform_notebook(nb, src_name):
    """Return a new notebook dict with markers applied."""
    cells = []
    banner = {
        "cell_type": "markdown",
        "metadata": {"tags": ["generated-banner"]},
        "source": [f"*{GENERATED_BANNER.format(src=src_name)}*\n"],
    }
    cells.append(banner)

    for cell in nb.get("cells", []):
        cell = json.loads(json.dumps(cell))  # deep copy
        text = as_text(cell.get("source"))
        tags = cell.get("metadata", {}).get("tags", []) or []

        if cell.get("cell_type") == "markdown":
            text = blank_markdown(text)
        elif cell.get("cell_type") == "code":
            text = blank_code(text, tagged="blank" in tags)
            cell["outputs"] = []
            cell["execution_count"] = None

        cell["source"] = text.splitlines(keepends=True)
        cells.append(cell)

    out = json.loads(json.dumps(nb))
    out["cells"] = cells
    for c in out["cells"]:
        if c.get("cell_type") == "code":
            c.setdefault("outputs", [])
            c["execution_count"] = None
    return out


def transform_markdown(text, src_name):
    body = []
    for line in text.splitlines(keepends=True):
        body.append(line)
    joined = "".join(body)
    joined = blank_markdown(joined)
    return f"<!-- {GENERATED_BANNER.format(src=src_name)} -->\n\n{joined}"


# ------------------------------------------------------------------------ validation

def validate(path, raw):
    """Catch unbalanced or malformed markers before they silently do nothing."""
    problems = []
    opens = raw.count("<!--blank-->")
    closes = raw.count("<!--/blank-->")
    if opens != closes:
        problems.append(f"{path}: {opens} <!--blank--> vs {closes} <!--/blank-->")
    for m in BLANK_RE.finditer(raw):
        if "<!--blank-->" in m.group(1):
            problems.append(f"{path}: nested <!--blank--> near {m.start()}")
    stray = re.findall(r"<!--\s*blank[^-]*?-->", raw)
    for s in stray:
        if not (s.startswith("<!--blank-->") or s.startswith("<!--blank-only:")):
            problems.append(f"{path}: unrecognized marker {s!r}")
    return problems


# ------------------------------------------------------------------------------ main

def render(src_path):
    """Return (relative_output_name, rendered_bytes) for one source file."""
    raw = src_path.read_text(encoding="utf-8")
    problems = validate(src_path.name, raw)
    if problems:
        return None, problems

    if src_path.suffix == ".ipynb":
        nb = json.loads(raw)
        out = transform_notebook(nb, src_path.name)
        return src_path.name, json.dumps(out, indent=1, ensure_ascii=False) + "\n"

    if src_path.suffix == ".md":
        return src_path.name, transform_markdown(raw, src_path.name)

    return None, []


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="chapters", type=Path)
    ap.add_argument("--dst", default="blanks", type=Path)
    ap.add_argument("--only", default=None,
                    help="stem of a single chapter to rebuild, e.g. chap09")
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if blanks/ differs from a fresh build")
    args = ap.parse_args()

    if not args.src.is_dir():
        sys.exit(f"source directory not found: {args.src}")

    sources = sorted(
        p for p in args.src.iterdir()
        if p.suffix in (".ipynb", ".md") and not p.name.startswith(".")
    )
    if args.only:
        sources = [p for p in sources if p.stem == args.only]
        if not sources:
            sys.exit(f"no chapter matching {args.only!r} in {args.src}")

    all_problems, stale, written = [], [], 0

    for src in sources:
        name, result = render(src)
        if name is None:
            all_problems.extend(result if isinstance(result, list) else [])
            continue

        target = args.dst / name
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != result:
                stale.append(str(target))
        else:
            args.dst.mkdir(parents=True, exist_ok=True)
            target.write_text(result, encoding="utf-8")
            written += 1

    if all_problems:
        print("Marker problems:", file=sys.stderr)
        for p in all_problems:
            print("  " + p, file=sys.stderr)
        sys.exit(2)

    if args.check:
        if stale:
            print("blanks/ is stale. Run: python3 tools/build_blanks.py", file=sys.stderr)
            for s in stale:
                print("  " + s, file=sys.stderr)
            sys.exit(1)
        print(f"blanks/ up to date ({len(sources)} source files)")
        return

    print(f"wrote {written} file(s) to {args.dst}/")


if __name__ == "__main__":
    main()
