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
| `chap06b.md` / `.ipynb` | interlude, between 6 and 7 | Docstrings and Doctests | Live, 1–11 (inherited from its neighbors — see below) | strip |
| `chap07.md` / `.ipynb` | 7 | Iteration and Search | Live, 1–11 | strip |
| `chap07b.md` / `.ipynb` | interlude, between 7 and 8 | Representing Data | Live, 1–11 (inherited from its neighbors — see below) | strip |
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

## Non-chapter files, confirmed

- **`chap00`** — Preface. Front matter, precedes the numbered chapters in
  `jb/_toc.yml`'s "Front Matter" part. No chapter number.
- **`jupyter_intro`** — a standalone notebook/orientation to Jupyter, linked from Chapter 1
  (`chap01.md` references it directly as "Jupyter notebook introduction"). Not present in
  `jb/_toc.yml` at all, so upstream doesn't treat it as part of the chapter sequence either.
- No separate appendix files exist under `chapters/`. `chap18` ("Python Extras") is the
  closest thing to an appendix but is a numbered chapter (19 total: 1–19) and is treated as
  such.

## Interludes: an exception to "file number == chapter number", added 2026-08-17

**`chap06b`** is the first of a new category: an *interlude* — original content, not part
of *Think Python*, inserted between two of Downey's numbered chapters (here, 6 and 7) to
teach something the AP course needs at that point in the sequence (here, docstrings and
doctests, right after functions start returning values). More are planned: at least one
on unit testing (anticipated near chapter 9) and one on binary. The book's own prose calls
these "interludes," never "chapters," to keep them visually and conceptually distinct from
Downey's numbered sequence.

**`chap07b`**, added 2026-08-17, is the second — between chapters 7 and 8, "Representing
Data," and it fills the "one on binary" slot named above (it covers AP 2.1/2.2 and CA
DA.8/DA.9: bits, place value, binary/decimal/hex conversion, ASCII/Unicode, RGB, analog
vs. digital, sampling, overflow/roundoff, and lossless/lossy compression). **As of this
writing it exists only as an outline** — section headings, vocabulary, standards claims,
and open authoring questions, but no drafted prose and no exercises (`chapters/chap07b.ipynb`
says so explicitly in its own first cell). It has been wired into `jb/_toc.yml` (same
three-way split as chap06b) and into the vocabulary and standards back matter — see
`AUDIT.md`'s 2026-08-17 handoff — on the reasoning that a placeholder in the TOC is more
useful than an invisible one once the standards claims are being made for real. **Not yet
done, deliberately, pending actual authoring:** Pass 4 chrome (link bar, embedded
JupyterLite pane, exercises notebook, attribution rule — see `mods/pass-4-chrome.md`),
Pass 5 JupyterLite wiring (`tools/build_jupyterlite_content.py`'s `CHAPTERS`/
`CONTENT_NAMES`/`CELL_PATCHES`, though `jb/build.sh`'s glob already covers it), and
`data/exercise-ledger.json` (no exercises exist yet to log). Do this work in the same pass
that writes the chapter's actual prose, not before.

Renumbering chapters 7–19 to make room was considered and rejected — it would break every
already-deployed `chapNN.html` link and contradict `CLAUDE.md`'s "small, legible diffs
against upstream." An interlude instead keeps the `chapNN`-plus-letter filename (sorts
correctly everywhere: filesystem, `jb/_toc.yml`, every dict in
`tools/build_jupyterlite_content.py`) and consumes no chapter number of its own.

This has one non-obvious consequence, confirmed by an actual local `jupyter-book build`
(not just read from docs): `jb/_toc.yml`'s single numbered "Chapters" part had to be split
into three around `chap06b`, with `caption:` kept on only the first piece, so the interlude
gets no number and chapters 7–19 keep theirs (`sphinx-multitoc-numbering`, bundled with
Jupyter Book, continues numbering across the split instead of restarting — verified, not
assumed). See `jb/_toc.yml`'s comment at the "Chapters" part for the exact mechanism; reuse
that same split-with-one-caption pattern for every future interlude.

Treatment tier is inherited from an interlude's neighbors, not looked up independently: an
interlude sitting between two Live/1–11 chapters gets `strip`/full blanks/full standards
form, the same as if it were one of them. A future interlude between two Independent-study
chapters (14–19) would get `keep`/no blanks/short form instead. This isn't stated in
`CLAUDE.md`'s treatment matrix, which is keyed by chapter number — record the inherited
tier here, in this file, for each interlude as it's added.

Wiring an interlude touches, beyond the chapter file itself: `jb/_toc.yml` (three-way part
split, see above), `jb/build.sh`'s chapter-copy glob (`chap[0-1][0-9]*.ipynb`, not
`chap[0-1][0-9].ipynb` — a bare two-digit glob silently excludes it from the built site),
`tools/build_jupyterlite_content.py`'s `CHAPTERS`/`CONTENT_NAMES`/`CELL_PATCHES`, and
`data/exercise-ledger.json` (see its "kind": "original" note for chap06b's entries). Pass
4's chrome steps and Pass 5's naming steps both apply unchanged otherwise.

**Also touches Pass 3's back matter — easy to miss, not caught by `make check`.** If the
interlude has its own `## Glossary` section (chap06b does), add it to
`alignment/vocabulary-by-chapter.md` and `.html` (new section, reading-order position,
running total bumped) and check every term against `alignment/ap-vocabulary-coverage.md` —
an interlude authored specifically to teach exam-adjacent vocabulary (chap06b: program
purpose/function/input/output, test case, hand tracing) is exactly the kind of chapter that
flips existing `gap` rows to `in book`. Recount that doc's totals programmatically after
editing, not by hand. `alignment/glossary-map.md` is curated analysis, not a mechanical
listing — update it only where the interlude adds a genuinely new concept-level mapping, not
term-for-term. See AUDIT.md, 2026-08-17 follow-up 6, for the chap06b example end to end.

**Also touches `standards/apcsp.json` and `standards/castandards.json` directly, when the
interlude is the first carrier for a topic that was previously `unassigned`/`carriers: []`
— easy to miss a second time, since chap06b's own wiring never did this (its testing
vocabulary landed in `ap-vocabulary-coverage.md` but chap06b was never added to any
topic's `carriers` list in `apcsp.json`/`castandards.json`, nor to `standards_alignment.md`'s
View 1 chapter table — a real gap, left alone rather than fixed retroactively, since fixing
it wasn't asked for and touching chap06b's standards claims is a separate decision). chap07b
did get this treatment, since it's the first carrier for AP 2.1/2.2 and CA DA.8/DA.9: see
`AUDIT.md`'s 2026-08-17 handoff for the full list of files touched (`apcsp.json`,
`castandards.json`, `alignment/supplement-plan.md`, `alignment/standards_alignment.md`).
Note the `carriers` schema's `"chapters"` field is a JSON list of ints everywhere else in
both files (e.g. `[1, 5]`) — there's no established convention for a lettered interlude, so
chap07b's entries use the string `"7b"` in that list instead. If a later interlude needs
this too, keep using the string form for consistency rather than inventing a new shape.

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
