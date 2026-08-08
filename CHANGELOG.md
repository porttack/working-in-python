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

## 2026-08-08 — chap01 becomes a live split view; top navbar removed sitewide

### Changed
- `chapters/chap01.ipynb`: the chapter's page no longer shows its own markdown at all.
  The left book-nav sidebar stays; everything else is a live JupyterLite instance of
  chap01 itself, filling the page edge to edge. The pane's left edge tracks the primary
  sidebar's actual rendered width via a small inline script (a `ResizeObserver`, not a
  fixed percentage), so it holds even if the sidebar's width changes. The "Contents"
  mini-outline sidebar is hidden on this page only, since the pane replaces that space
  too. `tools/build_jupyterlite_content.py` gained a `CELL_PATCHES` entry so the
  JupyterLite copy of chap01 shows a one-line note instead of trying to embed another
  copy of itself.
- `jb/_static/custom.css` (sitewide): removed the top navbar from every page. It held
  only a search button, already duplicated in the primary sidebar by the theme itself,
  and two mobile-only sidebar-toggle buttons (real loss, but out of scope for a
  Chromebook-width classroom deployment).

See `AUDIT.md`, 2026-08-08 follow-ups 7-8, for the full build/verification detail.

## 2026-08-08 — Sitewide resizable sidebar; dead sidebar-toggle button removed

### Added
- `jb/_static/custom.js`: a draggable divider next to the primary (left nav) sidebar,
  on every page. Chosen width persists in `localStorage` and applies sitewide, not
  per-page — resizing on one chapter carries over to the home page, other chapters,
  everywhere. Wired in via `jb/_config.yml`'s new `html_js_files`. `chapters/
  chap01.ipynb`'s own copy of this control (added the same day, chap01-only) was
  removed now that it's sitewide; that chapter's cell keeps only what's actually
  chapter-specific — creating its JupyterLite pane and keeping it aligned with the
  sidebar's current width, whatever resized it.

### Fixed
- `jb/_static/custom.css`: removed a "toggle primary sidebar" hamburger button that
  the previous top-navbar removal left visible on every page doing nothing (it was
  never wired to anything at this book's desktop-only, non-collapsible sidebar width).

See `AUDIT.md`, 2026-08-08 follow-up 9.

## 2026-08-07 — JupyterLite build scaffold, chap01 only (spike, not yet linked from a chapter)

### Added
- `tools/build_jupyterlite_content.py` and `make jupyterlite`/`make jupyterlite-serve`
  targets: assemble a JupyterLite site whose only content is `chap01.ipynb` plus its
  vendored `thinkpython.py`, as a fallback for when Google Colab is unreachable. `jupyter
  lite build`'s Pyodide kernel can't run `urllib.request.urlretrieve()` over HTTPS, but
  Downey's `download()` cell only fetches a file if it's missing, so bundling the
  dependency alongside the notebook avoids the problem without touching any chapter.
  `jupyterlite/content/` and `jupyterlite/_output/` are generated and gitignored, same
  policy as `projector/`. See `AUDIT.md`, 2026-08-07, for the full inventory of what
  chapters 4, 5, and 11 would still need before they could get the same treatment.

### Changed
- Nothing in `chapters/` — no chapter links to JupyterLite yet; hosting is undecided.

## 2026-08-08 — JupyterLite extended to chapters 1-11 and wired into the real publish pipeline

### Added
- Vendored `jupyturtle.py` (BSD-3-Clause, `ramalho/jupyturtle`), `pg345.txt` (Dracula), and
  `pg1184.txt` (The Count of Monte Cristo) at repo root, alongside the existing
  `thinkpython.py`/`diagram.py`/`structshape.py`/`words.txt`, so all of chapters 1-11 have
  every dependency their `download()`/`!wget` cells need already available locally.
- `tools/build_jupyterlite_content.py` now covers chapters 1-11 (not just chap01) and injects
  a small bootstrap cell (plain `import matplotlib.pyplot`) as the first cell of any chapter
  that pulls in `diagram.py` — Pyodide doesn't auto-install packages imported from inside a
  vendored `.py` file, only ones named directly in the executing cell's own source. Fixes a
  real `ModuleNotFoundError` found by actually running chapter 4, not just building it.
- `jb/build.sh` now builds JupyterLite and copies it into `_build/html/jupyterlite-vN/` before
  `ghp-import`, so it survives the branch's force-push instead of needing a separate,
  easily-forgotten deploy step. Documented as a third coupling hazard in `PUBLISHING.md`.
- chap08's five `!head`/`!tail` preview cells (no shell under Pyodide, and nothing to
  pre-bundle since they don't fetch anything) are now rewritten to plain-Python equivalents
  via `CELL_PATCHES` in `tools/build_jupyterlite_content.py` — only in the generated
  `jupyterlite/content/` copy, `chapters/chap08.ipynb` is untouched. Verified all four
  reachable patched cells execute correctly; the fifth is gated behind a still-unsolved
  in-chapter exercise, same as in Colab.
- `tools/build_jupyterlite_content.py --check` (wired into `make check`): scans every
  chapter already in the JupyterLite build for `!`-prefixed lines not already covered by
  `CELL_PATCHES` or the known guarded-download pattern, so a future chapter addition or an
  upstream merge that introduces a new shell-magic cell fails loudly instead of silently
  breaking JupyterLite.
- JupyterLite deploys are now versioned: `jb/build.sh` reads `jupyterlite/VERSION` and
  publishes to `jupyterlite-vN/` instead of a bare `jupyterlite/`, so a republished fix can
  never be masked by a stale cached copy in a student's browser or a school network's
  caching proxy — a new version is a URL nobody has fetched before. `CLAUDE.md` and
  `PUBLISHING.md` both document the rule: bump `VERSION` before any content-changing
  republish, never reuse a version number, never add `?enableCache=true` to a link (confirmed
  by reading the built service worker that this is what actually enables its caching).
- `jupyterlite/ascii_art.py`: lets a student opt into `pyfiglet`, `art`, `cowsay`, or
  `ascii_magic` with `import ascii_art; await ascii_art.use('pyfiglet')`. None of these are
  in Pyodide's own curated packages, so (unlike `matplotlib`) they need an explicit
  `piplite.install()`, not a bare import — confirmed by testing each one directly before
  writing anything. Lives in `jupyterlite/`, not repo root, since it has no upstream
  equivalent to mirror. Copied once into the shared `content/` directory rather than
  per-chapter, so it's importable from any chapter with zero wiring; verified from `chap02`
  specifically to confirm that.
- `jupyterlite/check.py`: a from-scratch, stdlib-only reimplementation of
  `otter.Notebook.check()`/`check_all()` — reads the same OK-format `tests/*.py` files real
  `otter assign` writes (with `tests: files: true` in its config) and runs each case as a
  `doctest` against the caller's globals, mirroring `otter.test_files.ok_test.OKTestFile`'s
  own approach closely enough that conformance is achievable rather than hoped for. Verified
  with `jupyterlite/check_conformance.py` against a real local `otter-grader` install: 10
  submissions across 5 fixtures (including a deliberate case-isolation test and float/
  exception/multi-line-output edge cases), all matching exactly, both overall and per case.
  Full otter-grader's `assign`/`generate`/`run`/`grade`/PDF export/logging/plugins/Gradescope
  integration are explicitly out of scope and stay on a machine with a real Python. Not yet
  used by any chapter — infrastructure ahead of content, same as `ascii_art.py`.
- JupyterLite deploy bumped to `jupyterlite-v2/`. `v1` was republished in place with
  `ascii_art.py`/`check.py` added, which is exactly the mistake the versioning rule above
  exists to prevent — a student hit a stale-cache `ModuleNotFoundError` for `ascii_art` as a
  direct result. `jupyterlite-v1/` is no longer served; use `jupyterlite-v2/`.

### Investigated, not pursued
- Full Otter Grader package: infeasible under Pyodide. Hard-depends on Docker
  (`python-on-whales`) and a real Chromium process (`playwright`) for its full CLI grading
  path — an architectural mismatch with a WASM sandbox, not something a custom Pyodide build
  can fix. See `ucbds-infra/otter-grader#458`. (The student-facing `check()` piece alone is
  small enough to reimplement instead — see `jupyterlite/check.py` above.)

## 2026-08-08 — jupyter_intro.ipynb vendored into JupyterLite; chap01 links to it there

### Added
- `chapters/jupyter_intro.ipynb` added to `tools/build_jupyterlite_content.py`'s `CHAPTERS`
  map (needs only `thinkpython.py`, same as chap01), so it now ships inside
  `jupyterlite/content/` instead of only existing as a forked-but-unwired file.
- chap01 gets a new `type="note"` sentinel cell, right after the upstream Colab paragraph,
  offering `jupyter_intro.ipynb` in JupyterLite (`/lab/index.html?path=jupyter_intro.ipynb`)
  as a fallback when Colab is unreachable. The upstream paragraph and its Colab links are
  untouched — this is additive, following the same pattern as the existing Codespaces note.
- JupyterLite deploy bumped to `jupyterlite-v3/`.

### Changed
- Nothing in `chapters/` outside the one new sentinel cell in chap01.

## 2026-08-06 — Split the Codespaces link into two, experimentally

### Changed
- `.devcontainer/devcontainer.json` (default) no longer auto-launches Jupyter Lab -- it's
  back to a plain VS Code Codespace (Python/Jupyter extensions, `ipykernel`/`matplotlib`/
  `pyyaml`/`jupyterlab` preinstalled, no `postStartCommand`/port forwarding). That
  behavior moved to a new `.devcontainer/jupyter/devcontainer.json`, selected via the
  `devcontainer_path` URL parameter.
- `chap01`'s Codespaces note now links both: "Open in a notebook view" (the `jupyter/`
  config, auto-forwarded Jupyter Lab) and "Open in VS Code" (the default config). Both
  URLs also gained `?quickstart=1`, which turned out to be required for the "reopen your
  existing Codespace" behavior the note already promised -- without it, `codespaces.new`
  skips that check and goes straight to a creation page. This was a real bug in the
  original single-link version, caught while researching whether two `devcontainer_path`
  links could safely coexist.

**Not independently verified.** Could not confirm from GitHub's documentation whether a
student who already has a Codespace from one of these links gets offered to resume it when
they click the *other* link (different `devcontainer_path`), or whether that silently
creates a second Codespace instead -- which would defeat the entire point of scoping both
links to one shared URL. Needs a live test (open one link, then the other, watch what
happens) before this goes out to the whole class. See `AUDIT.md`.

## 2026-08-06 — GitHub Codespaces option for chap01

### Added
- `.devcontainer/devcontainer.json`: repo-root devcontainer (Python 3.11, VS Code Python/
  Jupyter extensions, `pip install ipykernel matplotlib pyyaml jupyterlab` on create) so
  the repo can be opened as a GitHub Codespace. Sized from an actual grep of every
  chapter's imports, not a guess at Colab's full preinstalled set -- `matplotlib` and
  `pyyaml` are the only third-party runtime dependencies anywhere in `chapters/`.
  `thinkpython`, `diagram`, `jupyturtle`, and `structshape` are single-file modules the
  notebooks fetch themselves via `urlretrieve`, same as on Colab, so they need no
  preinstall.
- `.devcontainer/devcontainer.json`: `postStartCommand` launches Jupyter Lab in the
  background on port 8888 (token/password disabled -- redundant given Codespaces' own
  per-owner authenticated port forwarding); `forwardPorts`/`portsAttributes` auto-forwards
  that port and opens it in a new browser tab the moment the server comes up, so the
  Codespace lands students in a plain notebook UI close to what Colab already looks like,
  rather than the full VS Code editor. The VS Code editor is still there in the tab
  underneath (that's what the devcontainer's `customizations.vscode` config was already
  for) -- nothing about it was removed, just no longer the first thing a student sees.
- `.devcontainer/devcontainer.json`: `python.defaultInterpreterPath` pinned to the image's
  one Python interpreter, so the VS Code Jupyter extension has an unambiguous default and
  (with `ipykernel` preinstalled) shouldn't need to ask "Select Kernel Source" the first
  time a student runs a cell there. Every student gets a fresh container, so without this
  every student would hit that prompt cold.
- `chap01`: a `type="note"` sentinel cell, inserted right after the existing Welcome/Colab
  cell, linking to `https://codespaces.new/porttack/working-in-python` and describing both
  the auto-opened notebook tab and the VS Code tab behind it. Deliberately the same URL
  that would go in every other chapter, not a per-notebook link -- Codespaces are created
  per-repository, so a student who already has one for this repo gets GitHub's own "reopen
  existing Codespace" prompt instead of a new one, which is what keeps everyone at one
  Codespace total regardless of how many chapters they've clicked through. `make check`
  passes.

Scoped to chapter 1 only, by request; chapters 2-19 don't have the link yet. The Colab link
in the same cell still points at `AllenDowney/ThinkPython` (upstream), a pre-existing
mismatch noted in `PUBLISHING.md`, not touched here.

## 2026-08-06 — chap01 front-matter cleanup; site-wide hr visibility fix

### Removed
- The upstream front-matter cell in `chapters/chap01.ipynb` pointing readers to buy print
  and ebook copies from Bookshop.org and Amazon. Not relevant to students working from this
  fork.
- The "This is the Jupyter notebook for Chapter 1 of *Think Python*, 3rd edition, by Allen
  B. Downey" sentence from the Welcome cell -- redundant with the *Think Python* credit and
  copyright already in the chapter's closing note.

### Changed
- Added a `---` rule above the "Working in Python" fork-attribution note in chap01's
  closing `type="note"` sentinel block, to set it off visually from the exercises above it.
  (First tried a literal `<hr>` tag directly under the sentinel's HTML comment with no
  blank line between them; that turned out fine, and was not the actual problem -- see
  below.)
- `jb/_config.yml`: added `html_static_path`/`html_css_files` pointing at a new
  `jb/_static/custom.css`. The sphinx-book-theme ships all `<hr>` at 25% opacity, which is
  what made the rule above nearly invisible -- not the markup. First attempt raised
  opacity to 0.6 only; still reported as too light. Final version sets `opacity: 1`,
  `border-top-width: 2px`, and an explicit `border-top-color:
  var(--pst-color-text-base)` (the theme's own body-text color, so it stays correct in
  both light and dark mode) instead of tuning opacity. Scoped to `.bd-article hr` so it
  only affects rendered chapter content, not the theme's own sidebar/modal chrome.
  Affects every `<hr>` and `---` in the built site, not just chap01's.

`projector/` regenerated after each `chapters/` edit; `make check` passes. Verified by
rendering the actual built page with headless Chrome and inspecting a screenshot, not
just grepping the HTML/CSS.

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

## 2026-07-30 — AP CSP standards reference page

### Added
- `alignment/apcsp-standards-reference.html`: a single self-contained page indexing the
  full AP CSP framework (Practices, Big Ideas, Topics, Learning Objectives, and Essential
  Knowledge) with a stable `#CODE` anchor on every item, built on top of
  `standards/apcsp.json`. Extends that file's existing topic-level paraphrases down to all
  66 Learning Objectives and 331 Essential Knowledge statements, each in original wording
  — only AP's own codes are reproduced as-is, never College Board's descriptive prose.
  Lets `alignment/standards_alignment.md` and future Step 4 standards inserts deep-link to
  a specific EK statement instead of just a topic. See `AUDIT.md` for method and an
  automated verbatim-overlap check.

## 2026-07-30 — Second retitle: *Working in Python*

### Changed
- Retitled this fork again, from *A Python Notebook* to *Working in Python* (subtitle
  unchanged: *adapted from Allen Downey's Think Python, Third Edition*). Same treatment as
  the first retitle: `README.md` and `jb/_config.yml` (title/subtitle), the book's own
  name wherever used as prose (`mods/pass-3-alignment.md`, `alignment/glossary-map.md`,
  `alignment/supplement-plan.md`), the `carrier` slug (`python_notebook` ->
  `working_in_python`) everywhere it appears — including
  `alignment/apcsp-standards-reference.html`, added since the first retitle and caught by
  this pass's occurrence sweep — and the GitHub repository
  (`porttack/python-notebook` -> `porttack/working-in-python`), with every link updated to
  match. `projector/` regenerated, not hand-edited.
- Added the book's publication URL, `python.porttack.com`, to `README.md` and as a comment
  in `jb/_config.yml`. No GitHub Pages custom-domain setup (CNAME file, DNS) included —
  scoped to just the two references, by request.
- This entry and the "Book retitled to *A Python Notebook*" entry above are both left as
  written — each documents the name at the time of that specific rename. Only
  current-state references (title fields, the carrier slug, live links) get updated on
  each rename; narrative history does not. See `AP_MODIFICATIONS.md`'s Naming section for
  the current name in one place.

### Fixed
- `jb/_config.yml`'s `repository.url` (used for the built site's "view source" button)
  pointed at upstream (`AllenDowney/ThinkPython`) rather than this fork's own repo. Left
  that way through both retitles as a judgment call rather than a decision; the
  maintainer has now confirmed it should point at this fork instead, so it's
  `porttack/working-in-python` (branch `v3`). `ATTRIBUTION.md`'s own reference to the
  upstream repo is unaffected — that one is a Downey credit, not a build setting.

## 2026-07-30 — Redo AP CSP linking: our own anchors, not CodeHS

### Changed
- `type="standards"` sentinel in chap01, chap02, and chap03: the **AP CSP** label is no
  longer a link; each topic it cites now links individually to its own `#T-<code>` anchor
  on `alignment/apcsp-standards-reference.html` (to be hosted at
  `https://python.porttack.com/alignment/apcsp-standards-reference.html`). The
  **California 9-12** label is unchanged, still linking to CodeHS's framework page — we
  have no hosted CA reference page yet. `mods/pass-3-alignment.md`'s Amendments bullet and
  both Step 4 templates updated to match, so chapters 4-19 pick up the new convention.
  `projector/` regenerated; `make check` passes.
