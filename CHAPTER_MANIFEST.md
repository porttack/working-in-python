# Chapter Manifest

Filename → chapter mapping, resolved by reading each chapter's actual title (first
top-level heading in the `.md` rendering) and cross-checked against `jb/_toc.yml`, the
upstream Jupyter Book table of contents. Upstream numbering starts at `chap00`, which is
front matter (Preface), not Chapter 0. The "Chapters" part of the TOC runs `chap01`
through `chap19`, numbered, so **file number == chapter number for chap01–chap19.**
`jupyter_intro` is not listed in `jb/_toc.yml` at all — it's supplementary material read
before Chapter 1, not a numbered chapter.

VA decision originally followed the default proposed in `mods/pass-1-survey.md` Step 1
(chapters 1–8 `strip`, 9–11 `decide`, 12–13 `decide` leaning `keep`, 14–19 `keep`), finer-
grained than the treatment matrix in `CLAUDE.md` for chapters 1–11. That default was
superseded 2026-09-09: `CLAUDE.md`'s treatment matrix now sets VA removal to `strip` for
every tier, and every chapter's VA decision below reflects it — chapters 9–11's `decide`
was resolved, and 12–19's `keep` was reversed. Treatment tier is otherwise taken directly
from that matrix.

| File | Chapter # | Title | Treatment | VA decision |
|---|---|---|---|---|
| `chap00.md` / `.ipynb` | — (front matter) | Preface | not a chapter | n/a |
| `chap01.md` / `.ipynb` | 1 | Welcome | Live, 1–11 | strip |
| `chap02.md` / `.ipynb` | 2 | Variables and Statements | Live, 1–11 | strip |
| `chap03.md` / `.ipynb` | 3 | Functions | Live, 1–11 | strip |
| `chap04.md` / `.ipynb` | 4 | Functions and Interfaces | Live, 1–11 | strip |
| `chap05.md` / `.ipynb` | 5 | Conditionals and Recursion | Live, 1–11 | strip |
| `chap06.md` / `.ipynb` | 6 | Return Values | Live, 1–11 | strip |
| `chap07.md` / `.ipynb` | 7 | Iteration and Search | Live, 1–11 | strip |
| `chap08.md` / `.ipynb` | 8 | Strings and Regular Expressions | Live, 1–11 | strip |
| `chap09.md` / `.ipynb` | 9 | Lists | Live, 1–11 | strip (done 2026-09-09) |
| `chap10.md` / `.ipynb` | 10 | Dictionaries | Live, 1–11 | strip (done 2026-09-09) |
| `chap11.md` / `.ipynb` | 11 | Tuples | Live, 1–11 | strip (done 2026-09-09) |
| `chap12.md` / `.ipynb` | 12 | Text Analysis and Generation | May, post-exam, 12–13 | strip (done 2026-09-09) |
| `chap13.md` / `.ipynb` | 13 | Files and Databases | May, post-exam, 12–13 | strip (done 2026-09-09) |
| `chap14.md` / `.ipynb` | 14 | Classes and Functions | Independent study, 14–19 | strip (done 2026-09-09) |
| `chap15.md` / `.ipynb` | 15 | Classes and Methods | Independent study, 14–19 | strip (done 2026-09-09) |
| `chap16.md` / `.ipynb` | 16 | Classes and Objects | Independent study, 14–19 | strip (done 2026-09-09) |
| `chap17.md` / `.ipynb` | 17 | Inheritance | Independent study, 14–19 | strip (done 2026-09-09) |
| `chap18.md` / `.ipynb` | 18 | Python Extras | Independent study, 14–19 | strip (done 2026-09-09) |
| `chap19.md` / `.ipynb` | 19 | Final thoughts | Independent study, 14–19 | strip (done 2026-09-09) |
| `jupyter_intro.md` / `.ipynb` | not numbered | *Think Python* on Jupyter | supplementary, read before Ch. 1; absent from `jb/_toc.yml` | n/a |
| `interlude-a.ipynb` (no `.md`) | interlude, after ch. 19 | Docstrings and Doctests | see Interludes section below | strip |
| `interlude-b.ipynb` (no `.md`) | interlude, after ch. 19 | Representing Data | see Interludes section below | strip |

## Non-chapter files, confirmed

- **`chap00`** — Preface. Front matter, precedes the numbered chapters in
  `jb/_toc.yml`'s "Front Matter" part. No chapter number.
- **`jupyter_intro`** — a standalone notebook/orientation to Jupyter, linked from Chapter 1
  (`chap01.md` references it directly as "Jupyter notebook introduction"). Not present in
  `jb/_toc.yml` at all, so upstream doesn't treat it as part of the chapter sequence either.
- No separate appendix files exist under `chapters/`. `chap18` ("Python Extras") is the
  closest thing to an appendix but is a numbered chapter (19 total: 1–19) and is treated as
  such.

## Interludes

An *interlude* is original content, not part of *Think Python*, that teaches something the
AP course needs but that Downey's own sequence has no chapter for. The book's own prose
calls these "interludes," never "chapters," to keep them visually and conceptually distinct
from Downey's numbered sequence. Two exist:

- **Interlude A**, `chapters/interlude-a.ipynb` — Docstrings and Doctests. Fully drafted,
  live content.
- **Interlude B**, `chapters/interlude-b.ipynb` — Representing Data (AP 2.1/2.2, CA
  DA.8/DA.9: bits, place value, binary/decimal/hex conversion, ASCII/Unicode, RGB, analog
  vs. digital, sampling, overflow/roundoff, lossless/lossy compression). **Still an outline
  only** — section headings, vocabulary, standards claims, and open authoring questions, but
  no drafted prose and no exercises (its own first cell says so explicitly). Not wired into
  `tools/build_jupyterlite_content.py`'s `CHAPTERS`/`CONTENT_NAMES`/`CELL_PATCHES`, and has
  no `data/exercise-ledger.json` entries, for the same reason — do that work in the same
  pass that writes its actual prose.

**Position, and how it got here.** Both interludes originally sat inline: Interlude A
between chapters 6 and 7, Interlude B between 7 and 8, each inheriting VA/blanks/standards
treatment from its neighbors, per the treatment matrix's original design. That reasoning
didn't hold up in practice — the scope and sequence it assumed didn't work out as hoped —
so both were renamed and repositioned 2026-09-13 to the end of the book, after chapter 19,
in both the reading sequence (`jb/_toc.yml`) and the JupyterLite Lab file browser. They were
`chap06b`/`chap07b` before this move; the rename to `interlude-a`/`interlude-b` is a real
file rename, not just a display-name change — every reference throughout the repo (sentinel
`chapter="..."` attributes, iframe pane ids, `tools/build_jupyterlite_content.py`'s
`CHAPTERS`/`CONTENT_NAMES`/`CELL_PATCHES`/`ALIASES`, `working_in_python_v2.py`'s
`_resolve_notebook_path()`, `fetch.py`, `standards/carriers/working-in-python.json`, and the
vocabulary/alignment back matter) was updated to match. See `AUDIT.md`'s 2026-09-13 handoff
for the full list of files touched.

Renumbering chapters 7–19 to make room, when the interludes were still inline, was
considered and rejected — it would have broken every already-deployed `chapNN.html` link
and contradicted `CLAUDE.md`'s "small, legible diffs against upstream." That's also why an
interlude still consumes no chapter number of its own even now that it's moved: its filename
identifies it directly (`interlude-a`/`interlude-b`), with no chapter-number-plus-letter
scheme needed. Moving both to the end of `jb/_toc.yml` actually *simplified* the TOC:
keeping an interlude unnumbered while inline required splitting the single numbered
"Chapters" part into three pieces (so `sphinx-multitoc-numbering` would continue counting
across the split instead of restarting); with both interludes at the end instead, the
Chapters part is whole again (`chap01`–`chap19`, one part, no split), followed by a single
trailing unnumbered part holding both interludes. Reuse that trailing-part pattern for any
future interlude.

**Treatment tier: flagged, not resolved, by the move.** Both interludes still ship `strip`
VA (universal per `CLAUDE.md`'s treatment matrix) and still carry their original inline-era
blank markers and full-form standards block, unchanged by the 2026-09-13 move. Whether a
relocated, no-longer-inline interlude should be demoted to the Independent-study tier (no
blanks, short-form standards) instead is an open question, not a decision made during the
move — see `AUDIT.md`'s 2026-09-13 handoff.

Wiring an interlude touches, beyond the chapter file itself: `jb/_toc.yml` (trailing part,
see above), `jb/build.sh`'s and `jb/watch.sh`'s chapter-copy steps (an explicit
`interlude-*.ipynb` glob, since an interlude's filename no longer matches the `chapNN`
glob at all), `tools/build_jupyterlite_content.py`'s `CHAPTERS`/`CONTENT_NAMES`/
`CELL_PATCHES` (plus a temporary `ALIASES` entry if the interlude was already live under an
older name), `working_in_python_v2.py`'s `_resolve_notebook_path()`, `fetch.py`'s
`normalize()`, and `data/exercise-ledger.json`. Pass 4's chrome steps and Pass 5's naming
steps both apply unchanged otherwise.

**Also touches Pass 3's back matter — easy to miss, not caught by `make check`.** If the
interlude has its own `## Glossary` section (Interlude A does), it needs a section in
`alignment/vocabulary-by-chapter.md` (parsed live by `tools/build_vocabulary_by_chapter.py`
and `build_vocabulary_glossary.py` from that file's own `## Interlude X — ...` headings —
keyed off the letter in the heading itself, not off how many interlude headings have been
seen so far, so reordering them is safe) and a check against every term in
`alignment/ap-vocabulary-coverage.md` (hand-maintained; recount its totals programmatically
after editing, not by hand). `alignment/glossary-map.md` is curated analysis, not a
mechanical listing — update it only where the interlude adds a genuinely new concept-level
mapping, not term-for-term.

**Also touches `standards/carriers/working-in-python.json` directly**, when the interlude
is the first carrier for a topic that was previously unassigned. Unlike the catalog files
next to it (`apcsp.json`, `castandards.json`, etc., synced read-only from the `learn` repo —
see `standards/README.md`), this one file is this book's own and is edited here directly.
Its `locator_url_template` bakes a literal `chap` prefix into every generated URL for this
source, so an interlude locator (which resolves to `interlude-a.html`, not `chapA.html`)
needs an explicit `locator_slugs` entry — this is set up already for both current interludes;
add one for any future interlude the same way, or its standards-page links will silently
404. `interlude_letters` maps `"6b"`/`"7b"` (the coverage locator values, kept for backward
compatibility and because `build_alignment.py`'s prose-humanizing regex depends on that
exact key shape) to the display letters `"A"`/`"B"` — a locator's coverage-list value and
its display letter are two different things and don't have to match.

## Naming collision to flag, not fix

A directory named **`blank/`** (singular) already exists at the repo root and is tracked
by `jb/_toc.yml` as an "End Matter" part. It is an **upstream build artifact**: each
`blank/chapNN.ipynb` is the same notebook with markdown prose kept but code cells and their
surrounding narration compressed out — not the same thing as this project's own
**`blanks/`** (plural), which will hold Pass 2/3-generated notebooks with blank markers
resolved to underscores. The two names are one character apart. Recommend leaving `blank/`
untouched and never pointing `tools/build_blanks.py` output at it. Confirming this instead
of silently renaming or deleting anything, per `CLAUDE.md`'s destructive-action guidance.

## Discrepancy to flag, not fix

`CLAUDE.md` states pass files live at `docs/pass-1-survey.md`, `docs/pass-2-surgery.md`,
`docs/pass-3-alignment.md`. The file actually supplied for this pass is
`mods/pass-1-survey.md` — a different directory. No `docs/` directory exists yet. Proceeding
on the explicit instruction to follow `mods/pass-1-survey.md`, but this should be reconciled
(rename `mods/` to `docs/`, or update `CLAUDE.md`) before Pass 2 starts, so the next cold
read doesn't stall on the same ambiguity.
