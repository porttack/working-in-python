# AP Modifications

What changed in this fork and why, in prose. This document is the human-readable
counterpart to `data/exercise-ledger.json` and `CHANGELOG_DETAIL.md` — those are the
generated, itemized record; this is the narrative explanation a teacher or reviewer would
actually want to read.

Section headers only for now — content lands as each pass touches material. Do not
reproduce College Board CED or California framework prose here; paraphrase, and reference
codes only (see `CLAUDE.md`, Non-negotiable #1).

## Overview

<!-- What this fork is for, in two or three sentences. Filled in as passes complete. -->

## Naming

This fork is titled *Working in Python*, subtitle *adapted from Allen Downey's Think
Python, Third Edition*. It's published at
[python.porttack.com](https://python.porttack.com), and its GitHub repository is
`porttack/working-in-python`. The book title has changed twice since forking (briefly
*A Python Notebook* before this); the underlying text, structure, and attribution to
Downey have not. See `CHANGELOG.md` and `AUDIT.md` for the history of each rename.

Wherever this book needs its own name — `README.md`'s heading and `jb/_config.yml`'s
`title`/`subtitle` fields, prose in `mods/pass-3-alignment.md` and the `alignment/*`
docs, the `carrier` slug in `standards/apcsp.json`/`castandards.json` (currently
`working_in_python`), and the GitHub-repo link in the `type="note"` footer of all 21
files under `chapters/` — it's kept in sync with the current name. Historical narrative
in `CHANGELOG.md` and `AUDIT.md` describing a specific past rename is not rewritten when
the name changes again; only the current-state references above are.

Left untouched, deliberately: every reference to Downey's own book and its actual GitHub
repository (`AllenDowney/ThinkPython`) inside upstream chapter content, `ATTRIBUTION.md`,
and the vendored reference material (`ThinkPython_v3_Full.md`, `ThinkPythonSolutions/`,
`thinkpython.py`, the notebook zips). None of that names this fork — it names the book
this fork is adapted from, and per Non-negotiable #2, upstream content doesn't get
rewritten.

## Virtual-assistant material

<!-- What was stripped, kept, or replaced, chapter by chapter, and why. Pass 2. -->

## Standards alignment

<!-- How AP and CA standards map onto the existing chapter sequence, and where gaps are
carried by material outside this book (e.g. Little Brother for BI 4/5). Pass 3. -->

## Blank markers and live-session scaffolding

<!-- What blanks/ is, how it's used in class, and why chapters 14-19 don't get them. -->

## Chapters not treated as live instruction

<!-- Rationale for the 12-13 (post-exam) and 14-19 (independent study) tiers. -->

## Known gaps and deferred decisions

<!-- Anything raised-rather-than-decided per CLAUDE.md that hasn't been resolved yet. -->
