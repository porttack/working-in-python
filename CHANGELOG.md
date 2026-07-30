# Changelog

All notable changes to this adaptation are documented here, dated, at a summary level.
For a generated, per-exercise breakdown, see `CHANGELOG_DETAIL.md`.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Repo scaffold for the AP CSP adaptation: `CHAPTER_MANIFEST.md`, `AUDIT.md`,
  `data/exercise-ledger.json`, `tools/build_ledger.py`, `tools/check_sync.py`, `Makefile`.
- `data/exercise-ledger.json` seeded with all 81 existing exercises, classified and
  counted but not yet modified.

### Changed
- Nothing in `chapters/` yet — Pass 1 is read-only analysis plus tooling.

## 2026-07-29 — Pass 2, chapters 1–2

### Added
- Front matter: a one-paragraph hand-work policy note in `chap00` ("Doing the work by
  hand"), inside a `type="note"` sentinel. Stated once, not repeated per chapter.
- Blank markers for live projection in chapters 1 and 2: 5 prose blanks and 3 spoken
  prompts each, no code blanks (upstream's `blank/` already clears every code cell).

### Removed
- `chap01`, `chap02`: the "Ask a virtual assistant" section from each Exercises section
  (kind B — suggested-prompt lists with no graded task), removed whole, no replacement.
- `chap01` exercise 1 and `chap02` exercise 2: the inline virtual-assistant asides
  (kind C). Tasks and solution cells unchanged; no prose repair was needed in either case.

## 2026-07-30 — Pass 2, chapters 3–5 (repo adopts .ipynb-only chapters/, mid-batch)

### Changed
- `chapters/*.md` and `projector/*.md` (the parallel Markdown exports added in Pass 2
  prep) were removed outside this pass; `chapters/*.ipynb` is now the sole source of
  truth, matching what upstream ships. `.gitignore` updated to match.

### Added
- Blank markers in chapters 3–5: 5 prose blanks and 3 spoken prompts each, no code
  blanks (upstream's `blank/` empties every code cell in these three chapters too, same
  as chapters 1–2). `chap03`'s 4 Pass-1 verification markers were topped up to the same
  pattern rather than left as a smaller, differently-shaped set.
- `chap05` exercise `ch05-ex07`: a self-contained `draw_sierpinski(size, degree)` spec,
  replacing the book's first kind-A exercise (`ch05-ex06`, "ask a VA for a Sierpiński
  triangle, then debug it"). Same function name, parameters, and solution/demo cells as
  the original. The recursive algorithm was independently verified — simulated headlessly
  against `jupyturtle` and checked to reproduce the exact standard Sierpiński-gasket edge
  set at depths 0–4 — before being reduced to the geometric description given to
  students.

### Removed
- `chap03`, `chap04`, `chap05`: the "Ask a virtual assistant" section from each
  Exercises area (kind B), removed whole, no replacement. `chap05`'s version is larger
  than the others (it interleaves a countdown_by_two debugging vignette with the prompt
  list); see `AUDIT.md` for a flagged classification question about that vignette.
- `chap03` (stack-diagram aside), `chap05` exercise 5 (Koch curve opening line) and
  exercise 4 (closing line): inline virtual-assistant asides (kind C). Tasks and
  solution cells unchanged; no prose repair was needed in any case.

## 2026-07-30 — Modification footer, all chapters

### Added
- Every file in `chapters/` (chap00–chap19 and jupyter_intro, 21 files) gets a
  `type="note"` sentinel appended to its existing Downey copyright/license footer:
  attribution to Eric Brown for a high school CS class, with a link to
  `github.com/porttack/ThinkPython`. Applied uniformly regardless of which chapters
  have otherwise been touched by Pass 2 yet. No email address included (public repo).
