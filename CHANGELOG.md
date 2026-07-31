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
  `github.com/porttack/python-notebook`. Applied uniformly regardless of which chapters
  have otherwise been touched by Pass 2 yet. No email address included (public repo).

## 2026-07-30 — Pass 3, Step 1 (AP index)

### Added
- `standards/apcsp.json`: full AP CSP index built from the 2023 CED — 35 topics, all
  5 Big Ideas, 66 learning objectives, 8 exclusion statements, exam and practice
  weights, all cross-checked against the source PDF's own tables. Every LO code in the
  document is accounted for exactly once.

Stopped at the Step 1 gate by request; Steps 2–5 (California index, crosswalk,
alignment docs, standards inserts, appendices) not started. Findings — including a
partial-coverage gap on iteration (no `while` loop anywhere in the book) and several
fully unassigned topics (binary search, simulations, algorithmic efficiency, among
others) — are detailed in `AUDIT.md`.

## 2026-07-30 — Pass 3, corrections + Step 2 (CA index)

### Fixed
- `standards/apcsp.json` `meta.mcq_format`: corrected an arithmetic error (question
  counts summed to 78, not the exam's actual 70) after rechecking the CED's exam-format
  table.
- `standards/apcsp.json`: all 7 previously-`unassigned` topics reassigned to
  `carrier: "supplement"` with a note on where each is taught (CS50T Multimedia for
  binary numbers/data compression; the November algorithms block for binary search,
  simulations, algorithmic efficiency, and undecidable problems; continuous lab-pair
  work and the Create Performance Task for collaboration).

### Added
- `standards/castandards.json`: full California 9-12 CS standards index built from
  `csstandards.pdf` — all 30 core standards across the five strands, extraction matching
  the expected shape exactly. Stopped at the Step 2 gate; Steps 3–5 not started. Details,
  including 8 flagged `unassigned` standards, in `AUDIT.md`.

## 2026-07-30 — Pass 3, Step 3 (crosswalk + alignment docs)

### Added
- `standards/crosswalk.json`: 33 AP CSP ↔ California pairings (18 strong, 8 partial, 6
  related), honest about strength rather than forcing full coverage.
- `alignment/standards_alignment.md`: four views (by chapter, by AP topic, by CA
  standard, gaps) plus the Step 3 scope question, answered with evidence — chapters
  14–19 are not required by any CA 9-12 core standard.
- `alignment/supplement-plan.md`: the division of labor across this book, Little
  Brother, CS50T Multimedia, the November algorithms block, and lab/CPT practice, plus
  a punch list of standards with no assigned carrier anywhere yet.
- `alignment/glossary-map.md`: concept-level vocabulary mapping, led by the
  point-costing substitution table (function/procedure, 0- vs. 1-based indexing, etc.).

Stopped at the Step 3 gate; Steps 4–5 (standards inserts, appendices) not started.
Details in `AUDIT.md`.

## 2026-07-30 — Pass 3, Step 4 (standards inserts, chapters 1-3)

### Fixed
- `tools/check_sync.py`: standards-code validation assumed the wrong JSON shape for
  `standards/apcsp.json`/`castandards.json` (a leftover from when those files were empty
  Pass 1 placeholders). Every legitimate code citation would have failed `make check`.
  Fixed with schema-aware code extraction; the tool's other behaviors are unchanged.

### Added
- `type="standards"` sentinel in chap01, chap02, and chap03's back matter, each citing
  AP CSP topics and (where one exists) a California 9-12 standard, with codes and exam
  weights read from the JSON rather than hardcoded. Appended into the existing footer
  cell rather than a new cell, so cell counts are unchanged. `make check` passes; `make
  ledger` regenerates byte-identical (no replacement exercises exist yet in chapters
  1-3, so there was nothing to backfill).

Scoped to chapters 1-3 only, by request. Chapters 4-19 and Step 5 (appendices) not
started. Details in `AUDIT.md`.

## 2026-07-30 — Pass 2, chapters 6–8 (batch complete)

### Added
- Blank markers in chapters 6–8: 5 prose blanks and 3 spoken prompts each, no code
  blanks (upstream's `blank/` empties every code cell in all three chapters).
- `chap07` exercises `ch07-ex06r` and `ch07-ex07r`: self-contained specs for writing
  `uses_all` in terms of `uses_only` (swapped-argument hint) and in terms of `uses_any`
  (loop hint), replacing the book's last two kind-A exercises. Both verified against the
  chapter's existing doctests before being finalized.

### Removed
- `chap06`, `chap07`, `chap08`: the "Ask a virtual assistant" section from each
  Exercises area (kind B), removed whole, no replacement.
- `chap07` exercises `ch07-ex06` and `ch07-ex07`: the two remaining kind-A exercises
  (ask a VA to derive `uses_all`), replaced as above. `ch07-ex07`'s cell also contained a
  ChatGPT-attributed answer pasted directly into the notebook; removed along with the
  prompt.
- `chap08` exercise 1 and exercise 4: inline virtual-assistant asides (kind C).
  Exercise 4's aside was cut cleanly; exercise 1's was repaired rather than deleted, to
  keep the substantive constraint ("don't use `with` or `try` — not covered yet")
  independent of the virtual-assistant framing it was attached to.

This completes the "chapters 3–8" batch from `mods/pass-2-surgery.md`'s order of work
(chapters 3–5 landed in an earlier session). All four of the book's kind-A replacement
exercises are now written. Details in `AUDIT.md`.

## 2026-07-30 — Book retitled to *A Python Notebook*

### Changed
- Retitled this fork *A Python Notebook*, subtitle *adapted from Allen Downey's Think
  Python, Third Edition*: `README.md` and `jb/_config.yml` (title/subtitle), the internal
  "ThinkPython" shorthand for this book in `mods/pass-3-alignment.md` and the alignment
  docs, the standards crosswalk `carrier` slug (`thinkpython` -> `python_notebook`), and
  the GitHub repository itself (`porttack/ThinkPython` -> `porttack/python-notebook`),
  with every link updated to match. Downey's own book and repository credits, and all
  vendored Downey reference material, were left untouched. Details in
  `AP_MODIFICATIONS.md`'s Naming section.
- Reordered the `type="note"` modification footer in all 21 files under `chapters/` (and
  regenerated `projector/` to match) to appear *before* Downey's copyright/license block
  rather than after it, and reworded it to lead with this book's own title. Previously a
  reader hit "Think Python: 3rd Edition" first and the fork's own attribution second,
  which read as if the fork were still called Think Python. Content of Downey's
  copyright/license block is unchanged, only its position relative to the sentinel note.

## 2026-07-30 — Standards inserts: horizontal rule + framework links (chapters 1-3)

### Changed
- `type="standards"` sentinel in chap01, chap02, and chap03 (and the Step 4 templates in
  `mods/pass-3-alignment.md`): added a leading `---` markdown rule to visually separate
  the insert from the license block above it, and linked the **AP CSP** / **California
  9-12** labels to CodeHS's framework pages (`codehs.com/standards/framework/APCSP20` and
  `/CA_9-12`) wherever a line actually cites a code. `projector/` regenerated to match;
  `make check` passes.

Confirmed CodeHS's framework pages are client-rendered grids with no per-standard anchor
or `id`, so the link reaches the whole framework, not a specific row — noted in
`mods/pass-3-alignment.md` so a future maintainer doesn't try to guess a deeper URL.
