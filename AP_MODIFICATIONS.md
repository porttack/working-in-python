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

This fork is titled *A Python Notebook*, subtitle *adapted from Allen Downey's Think
Python, Third Edition*. The book title changed; the underlying text, structure, and
attribution to Downey did not. Concretely, on 2026-07-30:

- The title itself: `README.md`'s heading and `jb/_config.yml`'s `title`/`subtitle`
  fields.
- Internal references to this book's own name, wherever they occurred as prose (`mods/pass-3-alignment.md`,
  `alignment/glossary-map.md`, `alignment/supplement-plan.md`) — not schema keys, see below.
- The `carrier` slug used throughout `standards/apcsp.json`, `standards/castandards.json`,
  and the generated alignment docs to mean "this book carries this standard": renamed from
  `thinkpython` to `python_notebook`.
- The GitHub repository itself was renamed from `porttack/ThinkPython` to
  `porttack/python-notebook`; every link to it (the `type="note"` modification footer in
  each of the 21 files under `chapters/`, plus references in `CHANGELOG.md` and
  `AUDIT.md`) was updated to match.

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
