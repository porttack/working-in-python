# Changelog

All notable changes to this adaptation are documented here, dated, at a summary level.
For a generated, per-exercise breakdown, see `CHANGELOG_DETAIL.md`.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 2026-08-17 — front page JupyterLite Lab link survives the learn.porttack.com submodule pin

### Fixed
- `chapters/index.ipynb`: the "JupyterLite Lab" link used the `JUPYTERLITE_DEPLOY_PATH`
  placeholder like `chap01.ipynb`'s and `jupyter_intro.ipynb`'s embedded iframes, which is
  correct on `python.porttack.com` (each publish substitutes that build's own hash, so it's
  always self-consistent there) but not on the `porttack/learn` mirror: that repo embeds this
  one's `gh-pages` branch as a submodule pinned to a fixed commit, so the relative embedded
  link freezes at whatever hash was live when that commit was pinned, and could break
  outright if a later force-push makes that commit unreachable and it gets garbage
  collected. Repointed at the absolute `https://python.porttack.com/current/lab/index.html`
  redirect instead, so the link always resolves against the live primary site regardless of
  the submodule's pin state. Added an HTML comment next to the link recording why it's
  absolute and not the placeholder. See "Stable links for Schoology" and the submodule-pin
  caveat in `PUBLISHING.md`.

## [Unreleased]

### Added
- Repo scaffold for the AP CSP adaptation: `CHAPTER_MANIFEST.md`, `AUDIT.md`,
  `data/exercise-ledger.json`, `tools/build_ledger.py`, `tools/check_sync.py`, `Makefile`.
- `data/exercise-ledger.json` seeded with all 81 existing exercises, classified and
  counted but not yet modified.

### Changed
- Nothing in `chapters/` yet — Pass 1 is read-only analysis plus tooling.

## 2026-08-17 — download() docstring, chapters 5-18

### Fixed
- `chapters/chap05.ipynb` through `chap18.ipynb`: added an identical one-line docstring to
  `download()` in every chapter's setup cell (`"""Download a file if it isn't already here,
  and return its filename."""`). From chapter 5 on, `enable_docstring_reminders()` is active,
  so this cell was warning about its own code before a student had written anything --
  `download()` was defined identically in all 14 chapters, confirmed before editing, and
  nothing else in any setup cell was undocumented.

## 2026-08-16 — koch exercise gets back a description of what it's drawing

### Added
- `chapters/chap05.ipynb`: a short, original-wording description of what a Koch curve is
  (the segment-replaces-itself-with-a-bump substitution), plus a small ASCII diagram of one
  substitution step, ahead of the exercise's existing numbered recursive recipe. Pass 2 had
  removed the chapter's only source of this context (an "ask a virtual assistant" line) and
  never replaced it -- a real gap, since this course doesn't allow AI use, so students had no
  way to picture the shape first. Deliberately conceptual only, no pseudocode or code for the
  actual `koch()` function, so it orients without spoiling the exercise.
- `data/exercise-ledger.json`: `ch05-ex05`'s note updated to record the addition.

## 2026-08-16 — chap05 gets the chap04 homework treatment: Extra Exercises, choose-one pair, time check, extra credit

### Added
- `chapters/chap05.ipynb`: a new `## Extra Exercises` section, structurally matching
  chap04's -- intro, six numbered exercises (a choose-one pair plus four required), a time
  check, extra credit, then a "Finished? Copy your work" cell. Required work is five
  exercises (whichever of 1/2, plus 3-6), about 38 minutes, same framing chap04 uses.
  - Exercise 1 (`letter_grade`) and Exercise 2 (`rps_winner`) are the choose-one pair --
    interchangeable for grading, identical standards tagging, structurally identical cells
    (prompt, solution, "test your function" note, four test-call cells) so neither reads as
    the more "real" option. `letter_grade`'s tests sit on the grade boundaries (89/90,
    59/60); `rps_winner`'s cover a tie and both possible winners.
  - Exercise 3 (`is_leap_year`) tests the century-year exception directly (1900 is
    divisible by 4 but not 400).
  - Exercise 4 restores `countdown_by_two` as a plain debugging exercise, no
    virtual-assistant framing: the buggy function was recovered verbatim from git history
    (commit `e46eaa2`, pre-Pass-2) rather than reconstructed. Works for even starting
    values, infinite-recurses past zero for odd ones -- the same failure mode the chapter's
    own `recurse()` example already covers, demonstrated with the chapter's existing
    `%xmode Context` / `%%expect RecursionError` convention rather than a new one. Two
    answer cells (markdown, then code), closing the open classification question `ch05-va01`
    raised about this exact function.
  - Exercise 5 is a one-round hi-lo game (`input()`, `int()`, chained conditional, no
    loop -- looping isn't taught until chapter 7). Exercise 6 is the reflection question,
    matched to chap04 Exercise 6's voice.
  - None of the six exercises use loops, the `in` operator, or a return value -- chapter 5
    hasn't taught the first two, and this chapter's recursion only prints, per direct
    instruction.
  - The intro adds one sentence flagging that `enable_docstring_reminders()`'s warning is
    expected starting this chapter and how to satisfy it.
- `chapters/chap05.ipynb`: the three turtle-based exercises in Downey's original
  (ungraded) `## Exercises` section -- `draw`, koch, and Sierpiński -- are now marked
  optional, matching chap04's treatment of pie and flower.
- `chapters/chap05.ipynb`: a "Finished? Copy your work" cell, matching chap04's, added for
  the first time to this chapter.
- `data/exercise-ledger.json`: entries for all six new exercises, the time check, and the
  three newly-optional practice exercises; `ch05-va01`'s note updated to record closure.

### Changed
- `chapters/chap05.ipynb`: the extra-credit section (fractal tree / Collatz, added earlier
  this session) moved from directly after the ungraded practice exercises to its correct
  place, after the time check -- it had landed with no `## Extra Exercises` section to sit
  inside, which this entry fixes. Its intro no longer claims students have "already
  completed" the koch/snowflake cells, since those are optional as of this entry; it now
  just invites them to run those cells first if they haven't.
- `data/exercise-ledger.json`: `ch05-tree`'s note updated to match the revised intro wording.

## 2026-08-16 — Title Case filenames; teach/blank copies stop shipping to JupyterLite for now

### Fixed
- `working_in_python.py`: added `console.log` diagnostics to `check_for_update()` at every
  branch (entry, guard checks, fetch status, comparison result, error) -- the function had
  no logging at all, so a live test that produced no banner was genuinely ambiguous ("ran
  and found no update" vs. "never ran" vs. "silently errored"). Live-tested end to end after
  adding it: confirmed the whole mechanism works (fetch, compare, banner) once a real
  version mismatch exists.
- `chapters/chap04.ipynb`: merged the `download()` cell, the `import working_in_python` +
  `%autoreload` cell, and the `check_for_update()` call into one cell. Per direct feedback
  after the live test: `check_for_update()` only runs when its own cell executes, and a
  student reading top-to-bottom (not doing Run All) might never run a cell that exists only
  to check for updates. Folding it into the setup cell every student has to run anyway (to
  get their imports) means the check can't be skipped without also skipping the imports
  themselves.

### Changed
- All JupyterLite-visible filenames are now Title Case, including the `Chapter` prefix
  itself (`Chapter02-Variables-and-Statements.ipynb`, `_Start-Here.ipynb`,
  `_Using-Notebooks.ipynb`) -- small words ("and") stay lowercase. The two temporary
  chapter 2/3 aliases (`__chap02-variables-and-statements.ipynb`,
  `__chap03-functions.ipynb`) are deliberately NOT recapitalized -- they exist only to match
  whatever exact path a student's browser may already have cached from before the naming
  cleanup, so they have to stay byte-for-byte what they always were.
- Reverted the "teach" copy filename from a `-teach` suffix back to a `teach` *prefix*
  (`teach01-welcome.ipynb`, not `chapter01-welcome-teach.ipynb`) -- the suffix version sorted
  each teach copy next to its own chapter; the prefix sorts all teach copies together, after
  every chapter, which is what was actually wanted. This was a same-day regression, caught
  and fixed before it went anywhere.

### Removed
- Teach/blank copies no longer ship into `jupyterlite/content/` at all (`tools/
  build_jupyterlite_content.py`'s new `SHIP_TEACH_COPIES = False` flag). What to call this
  file and how to make it sort sensibly in the flat JupyterLite lab file browser turned into
  an extended back-and-forth with no fully clean answer -- "blank" (matching this repo's own
  "blank markers" terminology) sorts before chapters alphabetically; "teach" sorts after but
  reintroduces wording this project had deliberately moved away from; capitalizing either
  doesn't change sort order at all (confirmed from the actual built JupyterLab source: the
  file-browser comparator uses `localeCompare` with `sensitivity: "base"`, which is
  case-insensitive by definition). Decided to stop shipping it into the student-facing lab
  entirely for now rather than ship a compromise, with a real teacher-facing lab/manifest
  left as future work. All the underlying build logic (`CONTENT_NAMES`'s `teach` key,
  `teach_name_for()`, the `write_notebook_variant()` call) is untouched, just gated behind
  the one flag -- turning it back on is a one-line change once there's a real plan for where
  these copies belong.
- The "Blank (JupyterLite)" / "Teach Copy (JupyterLite)" chrome-bar link removed from
  chapters 1-8, since it would otherwise point at a file no longer shipped. Easy to re-add
  once the above is resolved.

## 2026-08-16 — All -exercises.ipynb files retired; no-scaffold-without-content rule

### Removed
- `chapters/chap01-exercises.ipynb`, `chap02-exercises.ipynb`, `chap03-exercises.ipynb`
  (real homework content, already submitted -- migrated first, see Changed below) and
  `chap05-exercises.ipynb` through `chap08-exercises.ipynb` (empty 2-cell stubs, no content
  ever written, nothing to migrate) -- deleted outright, along with their `projector/`
  copies and their `CHAPTERS`/`CONTENT_NAMES` entries in `tools/build_jupyterlite_content.py`.
  Chapter 4's own `-exercises.ipynb` was already retired earlier the same day; this closes
  out the pattern repo-wide. No chapter in the book now has homework in a separate notebook.
- `chapters/chap04.ipynb`: removed two answer cells (docstrings, pinwheel) that were bare
  `# Solution goes here` with no starter code -- a student adds their own cell for those now.
  Kept the ones that seed real starter code (`make_turtle()` for the turtle exercises,
  the three `time_check()` variables) and the two markdown "type your answer here" cells
  (a written-response placeholder isn't the same as a content-free code stub, and per
  direct feedback the answer belongs in its own new cell, not the prompt cell).
- Stripped the visible `# apcsp:begin`/`# apcsp:end` comment wrapper from every plain code
  cell that's a whole new addition (the copy-button call in `chap01.ipynb`-`chap04.ipynb`,
  chapter 4's remaining answer/time-check cells) -- a whole new cell is self-evidently an
  addition in any diff without a comment marking it, unlike prose folded into an existing
  upstream cell where the sentinel actually disambiguates old from new. Per feedback that
  the visible comments read as confusing and unpolished to a student. Markdown sentinels
  are untouched (HTML comments there are genuinely invisible when rendered, so they cost
  nothing visually).

### Added
- `chapters/chap01.ipynb`, `chap03.ipynb`: two exercises whose "solution" cell in the
  now-deleted exercises files was actually the exercise's own starter code (a deliberately
  broken expression/function to run and debug), not a blank placeholder -- migrated as real
  cells into each chapter's own `## Extra Exercises` prompt (chapter 1's "fix the TypeError,"
  chapter 3's "read the traceback"), and the redundant inert code block that had been
  duplicating the same snippet inside the prompt text itself was removed.
- `chapters/chap01.ipynb`, `chap02.ipynb`, `chap03.ipynb`: "Extra Exercises" intro no longer
  says work is answered in a separate notebook -- matches chapter 4's wording now that none
  of the book has one.
- `mods/pass-4-chrome.md`, `mods/pass-5-jupyterlite-lab.md`: corrected instructions that
  would have told a future session (chapters 9-11) to recreate the separate-exercises-file
  pattern, or reference an Exercises chrome-bar link, that this pass eliminated.

## 2026-08-16 — Book-wide filename cleanup; version-check banner; time_check polish

### Added
- `tools/build_jupyterlite_content.py`: `ALIASES` dict -- temporarily serves chapters 2
  and 3's identical content under both their new canonical name and their old
  (pre-cleanup) served name, so any student with in-progress work already cached in their
  browser's IndexedDB under the old path can still reach it. Chapter 4 doesn't need one
  (not live for students until Monday, under the new name from the start). Meant to be
  removed after a few days; the corresponding `porttack/learn` submodule's `_config.yml`
  `include:` entries for these two alias filenames should be removed at the same time.
- `working_in_python.py`: `check_for_update(version, filename)` -- shows a non-blocking
  banner ("A newer version of this chapter has been published") if the currently-served
  copy of a notebook differs from the one baked into the running session, detected via a
  plain `fetch(..., {cache: 'no-store'})` against `files/<name>` (bypassing JupyterLite's
  own IndexedDB-backed storage entirely, which is what makes a stale copy invisible to an
  ordinary reload). Never overwrites anything automatically -- offers a Reload button only.
  Wired into `chap04.ipynb` via a placeholder call (`check_for_update("JUPYTERLITE_DEPLOY_PATH",
  ...)`), substituted at build time the same way the embedded JupyterLite iframe links
  already are. Whether the Reload button actually pulls fresh content, versus needing a
  manual file-browser delete-and-reopen, is unverified from here -- flagged for live testing.

### Changed
- `working_in_python.py`: `time_check()` no longer prints a "fill this in" reminder --
  that logic was removed entirely. The reminder now lives as a plain comment at the top of
  the notebook cell that calls it, above the three variables a student fills in
  (`chapter_minutes`, `extra_exercises_minutes`, `longest`), per direct feedback that a
  runtime-printed reminder was confusing and that the cell should read as three lines of
  data, nothing cleverer.
- `working_in_python.py`: `show_copy_notebook_button()` now also toggles `margin: 0;
  line-height: normal` on every `.cm-line` element for the moment of copying, then reverts
  it -- an attempted fix for code cells pasting into Google Docs with exaggerated
  (~triple) line spacing, based on reading the actual built CSS (`.cm-editor`'s inherited
  `line-height` applied per source-line block) rather than guessing. Unverified whether
  this fully resolves the Google Docs symptom -- flagged for live testing.
- `chapters/chap04.ipynb`: removed em dashes from every piece of exercise text authored
  this pass (intro, Exercises 1-4, time check, spiral, "Finished? Copy your work") --
  17 instances rewritten as separate sentences or parentheticals, per feedback that the
  density read as an obvious AI tell.
- **Book-wide filename cleanup** (`tools/build_jupyterlite_content.py`'s `CONTENT_NAMES`,
  and every chapter 1-8 plus `jupyter_intro.ipynb`'s own chrome-bar links, self-embedding
  iframe `src`, and matching `CELL_PATCHES` entry): dropped the `___`/`__`/`_` prefix
  naming scheme (front matter / chapters / exercises) in favor of plain, student-legible
  names -- `chapter04-functions-and-interfaces.ipynb`, with `-teach` and `-exercises`
  suffixes for those variants, clustering each chapter's own files together alphabetically
  instead of grouping by file *type*. Front matter (`_start-here.ipynb`,
  `_using-notebooks.ipynb`) keeps a single leading underscore specifically so it still
  sorts first under `overrides.json`'s `sortNotebooksFirst`, which groups notebooks ahead
  of helper `.py`/`.txt` files but has no other chapter-order awareness of its own.
  Chapter 4 in particular gets a genuinely new filename (not just new content under the
  old name) precisely because JupyterLite's browser storage (IndexedDB, via `localforage`)
  persists by path under a fixed `contentsStorageName` -- a same-path content update is
  invisible to any browser that already opened the old version, no matter how the page is
  reloaded. A new path is the only way to guarantee every student gets the current content
  regardless of browsing history. See `AUDIT.md` for the full investigation, including why
  `check_for_update()` alone can't retroactively warn browsers that already hold a copy
  from before that function existed (chapter 4's rename is what actually closes that gap
  for this transition; `check_for_update()` is for *future* same-name updates only).
- Two `CELL_PATCHES` entries (`chap04.ipynb`, `jupyter_intro.ipynb`) were caught and fixed
  mid-pass after an interrupted first rename attempt left them matching an already-stale
  filename -- see `AUDIT.md`. Added a standing verification step (compares every
  `CELL_PATCHES` key against the actual notebook content) rather than trusting `--check`
  alone, which doesn't catch this failure mode.
- `PUBLISHING.md`, `HOW_TO_EDIT.md`, `mods/pass-5-jupyterlite-lab.md`: example filenames
  and file-browser sort-order descriptions updated to match the new naming scheme.

## 2026-08-16 — chap04-exercises.ipynb deleted; all chapter 4 homework now lives in chap04.ipynb

### Added
- `chap04.ipynb`: real answer cells for Exercises 1, 3, 4, 5, and 6 (previously
  preview-only, pointing students at the separate exercises notebook) -- code cells for
  initials, docstrings, and pinwheel; markdown "Type your answer here" cells for
  interface-vs-implementation and reflection, with each prompt's "Answer in the markdown
  cell below" pointer restored to match.

### Changed
- `chap04.ipynb`: fixed a physical cell-ordering bug from the previous pass -- pinwheel
  (labeled Exercise 4) sat before docstrings (labeled Exercise 3) in reading order, even
  though the headings were renumbered correctly. Cells now read 1-6 in order.
- `chap04.ipynb`: "Extra Exercises" intro no longer mentions a separate answer notebook;
  everything is answered in this chapter now.
- `tools/build_jupyterlite_content.py`: removed the `chap04-exercises.ipynb` entry from
  `CHAPTERS` and `CONTENT_NAMES`. Chapters 1-3 and 5-8's exercises notebooks are untouched
  -- this migration is chapter 4 only, since those chapters are already submitted.
- `data/exercise-ledger.json`: `ch04ex-hw01` through `ch04ex-hw05` now record `chapter:
  "chap04"` instead of `"chap04-exercises"`, and their notes no longer describe a
  preview/answer-file desync, since there is only one file now.

### Removed
- `chapters/chap04-exercises.ipynb` and `projector/chap04-exercises.ipynb`, deleted
  outright (`git rm`). Its student-facing content (name/timestamp cell, redundant
  turtle/jump setup, and the "Finished? Copy your work" cell) was not carried over --
  see `AUDIT.md` for the full inventory and disposition of every cell.

### Fixed
- Closes the gap flagged in the previous entry below and recorded as deferred in
  `AUDIT.md`: since students submit by pasting the whole chapter into a Google Doc,
  having graded answers split across two files meant half of a choose-one pair (the
  house exercise) was captured on submission and the other half (initials) was not.
  All six numbered exercises, the time check, and the spiral now live in one file.

## 2026-08-16 — chap04 homework: house exercise, choose-one pairing, time check, spiral

### Added
- `working_in_python.py`: `time_check(chapter=0, exercises=0, longest="")` — prints a
  chapter/exercise/total time summary (`XhYYm` at an hour or more, `Ym` below that, via
  `divmod`) and a plain-text reminder, using `colored()` but readable with color stripped,
  when any argument is left at its default.
- `chap04.ipynb`: new Exercise 2, "draw a house from parts" (`draw_wall`/`draw_roof`/
  `draw_door`/`draw_house`), a choose-one alternative to Exercise 1 (initials) — a student
  does either, not both, and both carry identical standards tagging so grading never
  depends on which one is picked.
- `chap04.ipynb`: unnumbered "Time check" section (graded on completion, not on the
  numbers) and an unnumbered "Spiral (extra credit)" section at the end of "Extra
  Exercises," worth 0.5 points and never a substitute for a required exercise. The spiral
  prompt is written fresh, replacing the one Downey originally placed inside the "Ask a
  virtual assistant" section that was removed earlier in this pass — no VA framing
  reintroduced.
- `chap04.ipynb`: one-line "this one is optional" notes added after the pie and flower
  prompts in the chapter's own (ungraded) Exercises section; rectangle/rhombus/
  parallelogram remain the expected practice set.

### Changed
- `chap04.ipynb`: Exercises 1 and 2 headings marked "(do 1 or 2)"; docstrings (Exercise 3)
  rewritten to reference the student's own choose-one function instead of pinwheel, so it
  no longer depends on an exercise assigned later; pinwheel/interface/reflection renumbered
  to Exercises 4/5/6. The "Extra Exercises" intro rewritten with the choose-one framing,
  required-work total (five exercises, ~38 min), and the time-check/spiral pointers.
- `chap04-exercises.ipynb`: "Before you start" and closing-footer cells no longer tell
  students to rename and download the file for Schoology; both now point at the
  Copy-Notebook button already at the end of that file, consistent with the paste-into-a-
  doc submission model.

### Known gap, not resolved this pass
- `chap04.ipynb`'s five previewed exercises (1, 3-6) still direct students to answer in
  the separate `chap04-exercises.ipynb`, but only that chapter file — not the exercises
  file — is now told to be pasted whole into a submission doc. The house/spiral/time-check
  exercises live only in `chap04.ipynb` and would be captured; the other five would not.
  Left as-is per explicit instruction pending the deferred exercises-file migration
  (see `AUDIT.md`). `data/exercise-ledger.json` notes on `ch04ex-hw02` through `ch04ex-hw05`
  also flag that those exercises' `chap04.ipynb` preview numbering/content is now out of
  sync with the unchanged `chap04-exercises.ipynb` answer file.

## 2026-08-16 — "Copy Notebook" button and docstring reminders for JupyterLite

### Added
- `working_in_python.py`: `show_copy_notebook_button()`, shown automatically on import and
  callable again anywhere. Copies the whole notebook (code, output, images) for pasting into
  a document — automates the mouse gesture already confirmed to paste correctly, since
  Jupyter's own Ctrl+A/copy doesn't. Sticky-positioned so it stays visible while scrolling.
  Works around a real limitation along the way: execution-count prompts carry a deliberate
  `user-select: none` in JupyterLab's own CSS, so they're excluded and re-enabled just for
  the moment of copying.
- `working_in_python.py`: `enable_docstring_reminders()` — a non-blocking warning (via an
  IPython `post_run_cell` hook + `ast`) when a cell defines a function with no docstring.
  Wired into `chap05.ipynb`–`chap18.ipynb` (chapters from where docstrings are taught
  onward).
- `chap01.ipynb`–`chap04.ipynb`: a "Finished? Copy your work" cell added to the end of the
  "## Extra Exercises" section, right after Exercise 5.
- `chap01-exercises.ipynb`–`chap04-exercises.ipynb`: the same copy button added at the end,
  and (previously missing) an `import working_in_python` cell to support it.
- `tools/build_jupyterlite_content.py`: `working_in_python.py` added as a companion file for
  all 8 `chap0N-exercises.ipynb` notebooks.

### Fixed
- `chap01.ipynb`–`chap08.ipynb`: removed the stale `**TODO:** [Chapter Exercises](...)` chrome-
  bar link (flagged in the 2026-08-11 handoff for chapters 1-4; also found present in 5-8).
  Removed outright rather than just fixing the label — see `AUDIT.md`: the separate
  `chap0N-exercises.ipynb` notebooks are being deprecated, exercises will live entirely
  inside each chapter going forward.

### Investigated, not shipped
- A download relay (Cloudflare Worker) for students on managed Chromebooks who can't
  download `.ipynb` from JupyterLite — built and then paused for a FERPA concern (routing
  student work through an unvetted third party), not a technical one. Stashed
  (`git stash list`), not committed. See `AUDIT.md` for the full investigation, including
  ruling out the File System Access API, Chrome's `URLBlocklist`, and GoGuardian in turn.
- Printing JupyterLite's own notebook UI — real root cause found (a fixed-height, internally-
  scrolling container that clips anything off-screen from print, independent of any notebook
  setting), but no working fix inside this offline build. Abandoned in favor of the copy
  button above; see `AUDIT.md`.

## 2026-08-16 — Print CSS fallback for the primary sidebar and JupyterLite panes

### Fixed
- `jb/_static/custom.css`: added a plain `@media print` rule hiding `.bd-sidebar-primary`
  (the left nav) unconditionally. The theme only hid it on print via a `.noprint` class
  added by `sphinx-book-theme.js` at page load, with no CSS-only fallback if that script
  doesn't run in time. See `AUDIT.md` for the investigation, including ruling out the
  `porttack/learn` submodule mount as the actual cause.
- `jb/_static/custom.css`: added a second `@media print` rule, `[id$="-jupyterlite-pane"]`,
  hiding the live JupyterLite iframe embedded in chap01-08 and `jupyter_intro`. That pane's
  own CSS sets `display: block` and `position: fixed` unconditionally, with no print
  scoping and no coverage from the theme's `noprint` mechanism, so printing one of those
  chapters printed a full-height fixed box on top of the article text. See `AUDIT.md`.

## 2026-08-11 — chap02 previews its homework as "Extra Exercises"

### Added
- `chapters/chap02.ipynb`: new "## Extra Exercises" section, six markdown cells inside
  `type="exercise"` sentinels, inserted after the chapter's own upstream "## Exercises"
  section and before the closing attribution note. Previews the five homework prompts
  from `chap02-exercises.ipynb` as read-only text (no name/timestamp cell, no
  rename/Schoology submission instructions, no `# Solution goes here` cells, no
  `<!-- teacher: ~N min -->` timing comments -- none of that applies inside the reading
  chapter) with a pointer back to the real Exercises notebook, linked from the chrome bar,
  where students actually do and submit the work. Intent: a student skimming straight to
  the separate Exercises notebook via the chrome-bar link currently never has to open
  `chap02.ipynb` at all; this puts the homework where reading the chapter is what surfaces
  it.
- `data/exercise-ledger.json`: appended a note to each of the five existing
  `chap02-exercises`/`ch02ex-hw01`-`ch02ex-hw05` entries recording the new preview
  location. No new ledger entries -- these are the same five exercises, not new ones.

### Changed
- `projector/chap02.ipynb`: regenerated (`make projector`) to pick up the new section;
  no blank markers in it, so it renders identically to `chapters/chap02.ipynb`.
- `chapters/chap02.ipynb`: nulled the `execution_count` on all 48 code cells that had one
  (inherited, non-null, from upstream -- `projector/chap02.ipynb` already had these
  stripped by `build_blanks.py`, so this only affected the source file). Grading chapter 2
  itself now, not the separate exercises notebook: a student who skips straight to "Extra
  Exercises" without running the chapter's own cells will show `null` on everything they
  skipped, instead of the pre-baked 1-48 that made every cell look already-run regardless
  of what the student actually did.

## 2026-08-11 — chap01 and chap03 get the same "Extra Exercises" + null exec-count treatment

### Added
- `chapters/chap01.ipynb`, `chapters/chap03.ipynb`: same "Extra Exercises" preview
  section added to chap02.ipynb above, sourced from `chap01-exercises.ipynb` /
  `chap03-exercises.ipynb`'s five homework prompts each, minus submission mechanics.
- `data/exercise-ledger.json`: appended a preview-location note to the existing
  `ch01ex-hw01`-`05` and `ch03ex-hw01`-`05` entries. No new entries.

### Changed
- `chapters/chap01.ipynb`, `chapters/chap03.ipynb`: nulled stale upstream
  `execution_count`s on all code cells (48 and 38 respectively), same reasoning as
  chap02's exec-count fix.
- `projector/chap01.ipynb`, `projector/chap03.ipynb`: regenerated.

## 2026-08-16 — chap04 gets "Extra Exercises" + null exec counts, plus a new docstrings exercise

### Added
- `chapters/chap04-exercises.ipynb`: new Exercise 3, "docstrings" -- students add a
  docstring to the `pinwheel` function they wrote in Exercise 2 (following the chapter's
  own `polyline` example), re-run that cell, then run `help(pinwheel)` and confirm it
  renders. Added at the user's explicit request: writing a docstring isn't enough on its
  own to confirm a student understands it works -- checking with `help()` is the point.
  Interface-vs-implementation and reflection, previously Exercises 3 and 4, shift down to
  4 and 5 to make room right after pinwheel, which the new exercise depends on.
- `chapters/chap04.ipynb`: same "Extra Exercises" preview section as chap01-03, sourced
  from `chap04-exercises.ipynb`'s five (now) homework prompts, in the same order,
  including the new docstrings exercise. Notes that the chapter's own turtle-drawing
  exercises above it (rectangle, rhombus, parallelogram, pie, flower) are practice, not
  graded -- this is the graded homework.
- `data/exercise-ledger.json`: new `ch04ex-hw05` entry for the docstrings exercise;
  appended preview-location notes to `ch04ex-hw01`-`04`, and renumbering notes to
  `ch04ex-hw03`/`04` recording their heading-number shift (ledger ids unchanged).

### Changed
- `chapters/chap04.ipynb`: nulled stale upstream `execution_count`s on all 47 code cells
  that had one, same reasoning as chap01-03.
- `projector/chap04.ipynb`, `projector/chap04-exercises.ipynb`: regenerated.

## 2026-08-11 — Fork thinkpython.py as working_in_python.py

### Changed
- Every notebook's setup cell (`chap01`–`chap18`, `jupyter_intro`) downloaded the book's
  support module straight from `github.com/AllenDowney/ThinkPython`. Even though the file
  was already vendored at this repo's root, edits to that local copy never reached a
  student, since a fresh Colab or JupyterLite run always re-fetched Downey's original.
  Renamed the vendored copy `working_in_python.py` and repointed every download URL at
  this repo's own raw URL instead, so future edits to the support module actually ship.
  Also updated: `tools/build_jupyterlite_content.py`'s per-chapter companion-file lists,
  and the one sentence in `jupyter_intro.ipynb` that names the file by name. Consciously
  reverses the "leave thinkpython.py untouched" policy recorded in `AP_MODIFICATIONS.md`;
  see that file's Naming section for the reasoning, and `ATTRIBUTION.md` for the
  still-applicable MIT credit to Downey.

## 2026-08-10 — Fix stale filenames surviving in the JupyterLite lab view

### Fixed
- `jb/build.sh` and `Makefile`'s `jupyterlite` target now `rm -rf jupyterlite/_output
  .jupyterlite.doit.db` before every build. `jupyter lite build` is an incremental doit
  build that only adds/updates outputs still present in `jupyterlite/content/`; it never
  prunes an old output whose source was renamed or removed. Every chapter renamed by
  `CONTENT_NAMES` (2026-08-09) had its pre-rename filename (`chap01.ipynb`,
  `chap02-exercises.ipynb`, etc.) lingering forever in `_output/files/` alongside the
  correct one, visible in the lab file browser. Flagged as a risk but not fixed in
  AUDIT.md's 2026-08-09 entry (there it only affected a dead `settingsOverrides` key,
  judged cosmetic); this is the same mechanism causing a user-visible symptom.

## 2026-08-09 — AP CSP vocabulary coverage rebuilt from a real course-priority list

### Added
- `data/ap-vocabulary-source.md`: this course's own curated AP CSP vocabulary list (144
  terms), with Tier (Concept/Label/Fact instructional cost), HF/KA/WR flags, original
  definitions and notes, a 10-item Python-vs-exam misconception bank, and an explicit
  exclusion list. Declares itself the single source for downstream artifacts.

### Changed
- `alignment/ap-vocabulary-coverage.md` + `.html` rebuilt entirely from the new source
  file, replacing the previous compiled 140-term list. Every term not in the new list was
  dropped. Adds the Working-in-Python chapter mapping the source file doesn't have; page
  redesigned around Tier, with a new misconception-bank section.

### Fixed
- The Big Idea 2 encoding cluster (binary, bit, byte, hex, ASCII, RGB, compression, ...)
  was marked `planned` against a CS50T Multimedia unit that (per the maintainer's own
  `glossary-map.md` edit) was dropped and hasn't been taught since year one. Corrected to
  `gap`, with a narrower note where the Pico/MicroPython I2C unit has a partial touchpoint
  (byte/hex notation only).

## 2026-08-09 — Hide the About page; preface and About content tweaks

### Removed
- `about.md` unlinked: dropped from `jb/_toc.yml`'s left nav, and its links from
  `orientation.md` and the front page (`chapters/index.ipynb`) removed. The file itself is
  untouched and stays in the repo, just orphaned from navigation, so it can be relinked
  later.

### Changed
- `jb/about.md`: reworded the AI-assistants section (dropped the January assistants-with-
  attribution policy in favor of a flat "removed" statement, added a CS50AI teaching
  anecdote as rationale), swapped Colab references for JupyterLite, removed the "scope
  reduced" bullet and the "adopting this book" caveat, and filled in the real corrections
  contact (`ericbrown@porttack.com`) in place of the `[CONFIRM: ...]` placeholders.
- `chapters/chap00.ipynb` (Downey's Preface): removed the Bookshop/Amazon purchase-link
  cell and all ChatGPT/virtual-assistant references, replaced the "What's new in the third
  edition" retrospective with a "Working in Python Modifications" summary, and pointed the
  notebook-access instructions at JupyterLite instead of Colab.

## 2026-08-09 — Stable JupyterLite links for Schoology

### Added
- `jb/build.sh` now also writes `current/notebooks/index.html` and `current/lab/index.html`:
  tiny pages that redirect (query string preserved) to that build's real
  `jupyterlite-<hash>/...` path. Regenerated on every publish since `ghp-import -f`
  replaces the whole branch, so a link posted once to Schoology
  (`https://python.porttack.com/current/notebooks/index.html?path=...`) keeps working
  across every future rebuild instead of 404ing the moment the hash changes.

### Changed
- `PUBLISHING.md`: documented the `current/` alias and its caching tradeoff (a redirect
  can point at the previous build for up to the 600s `Cache-Control` window after a
  republish), and added it as verification step 8.

### Fixed
- The `current/` redirect used a root-absolute path (`/jupyterlite-<hash>/...`), which
  resolves correctly on `python.porttack.com` but not on `learn.porttack.com`, which embeds
  this repo's `gh-pages` branch as a submodule under `/working-in-python/` instead of the
  domain root. Changed to a relative path (`../../jupyterlite-<hash>/...`) so it resolves
  correctly regardless of mount point.

## 2026-08-09 — Retire the CS50T Multimedia carrier for binary numbers/data compression

### Changed
- `standards/apcsp.json` (topics 2.1, 2.2), `standards/castandards.json` (9-12.DA.8, DA.9),
  and `standards/crosswalk.json`: removed "CS50T Multimedia" as the carrier for AP Binary
  Numbers/Data Compression and their CA counterparts. Teacher confirmation: that supplement
  hasn't actually been taught since year one, so the assignment was stale, not real
  coverage. All four now read as real, unassigned gaps (`carriers: []`), matching the
  convention used elsewhere for gaps with no plausible carrier.
- `alignment/supplement-plan.md`, `standards_alignment.md`, `ap-vocabulary-coverage.md`,
  `ap-practices-bigideas-coverage.md`, `glossary-map.md`: updated to match — CS50T
  references removed, topic/vocabulary counts corrected, and a note added that the
  Pico/MicroPython unit's I2C chapter (`source/rpi-pico-2e` ch.14, read from the source
  EPUB to confirm) is a partial, non-closing touchpoint for hex/byte notation (2.1, DA.8)
  but has nothing for data compression (2.2, DA.9). No replacement carrier decided yet —
  see the `learn` repo's `_program-notes/apcsp-python-scope-sequence.md` for the live
  discussion. Hosted `.html` twins under `alignment/` not regenerated here; they're
  `jb/build.sh` output, due for a rebuild.

## 2026-08-09 — Supplementary homework exercises for chapters 1-4

### Added
- `chapters/chap01-exercises.ipynb`, `chap02-exercises.ipynb`, `chap03-exercises.ipynb`,
  `chap04-exercises.ipynb`: filled in with original homework exercise sets (previously
  blank placeholders). Each has a name/timestamp identification cell and rename-before-
  download submission instructions (`answersNN-<first name>.ipynb`, to avoid identical
  filenames colliding when many students submit), plus invisible `<!-- teacher: ~N min
  -->` time-estimate comments. Chapters 2-4 are fully independent homework with no
  in-class walkthrough. Chapter 4's packet is that chapter's sole graded artifact --
  `chap04.ipynb`'s own 5 native exercises (90 minutes) are practice only, not collected,
  to avoid double-checking the same material in two files.
- `chapters/chap01.ipynb`: two new exercises inside a `type="exercise"` sentinel -- a
  fix-a-`TypeError` exercise and a markdown-answer exercise -- serving as the live
  in-class demo for two response formats then reused directly in the homework packets.
- `data/exercise-ledger.json`: 21 new entries for the above (2 in `chap01`, 5 each in
  `chap01-exercises` through `chap03-exercises`, 4 in `chap04-exercises`).
- `tools/build_jupyterlite_content.py`: registered `jupyturtle.py` as a
  `chap04-exercises.ipynb` dependency, since its exercises now use turtle graphics and
  the notebook has no shared runtime with `chap04.ipynb`.

## 2026-08-09 — Vocabulary by chapter, and AP CSP vocabulary coverage (word-level)

### Added
- `alignment/vocabulary-by-chapter.md` + hosted `vocabulary-by-chapter.html`: every term
  from Downey's own chapter-ending `## Glossary` sections, chapters 1-18 (185 terms), by
  chapter. Chapter 19 has no glossary section.
- `alignment/ap-vocabulary-coverage.md` + hosted `ap-vocabulary-coverage.html`: a
  *compiled* (not extracted — no official AP CSP glossary exists) 140-term AP CSP
  vocabulary list, sourced from the official Exam Reference Sheet's keyword names plus
  term names only (not prose) from two third-party study lists, with original glosses.
  Each term tagged `book` / `planned` / `else` (*Little Brother*) / `gap` against this
  book's own vocabulary, with the matching term and chapter cited where one exists. The
  hosted twin includes a symbolic (explicitly non-area-proportional) two-circle Venn
  diagram of the two vocabularies, as inline SVG.
- Both new pages added to `jb/_toc.yml`'s Reference section; one-line pointers added to
  `apcsp-standards-reference.html` and `ap-practices-bigideas-coverage.html`, and a
  paragraph added to `glossary-map.md` framing the new pages as its word-level companion.

### Fixed
- Confirmed, not assumed: `.insert()` never appears in any chapter's code (a real,
  previously-unlogged vocabulary gap against AP's INSERT), and `turtle` first appears in
  chapter 4 — corroborating (not yet fixing) the `section_turtle_module` broken
  cross-reference logged earlier in `AUDIT.md`.

## 2026-08-09 — JupyterLite lab view: front page as a notebook, student-legible filenames

### Added
- `chapters/index.ipynb`: the book's front page (`https://python.porttack.com/`) is now a
  fork-authored notebook, not `jb/index.md` (deleted). Same content, plus a new link to the
  JupyterLite *lab* view (the full workbench, as opposed to the single-chapter view every
  chapter's chrome already links to) — needed the front page to carry the
  `JUPYTERLITE_DEPLOY_PATH` placeholder the same way `chap01.ipynb`/`jupyter_intro.ipynb` do,
  which only notebooks can. Dropped a stray "Standards alignment" block that had been
  duplicated onto `jb/index.md` by mistake (chap01.ipynb already carries the real one).
- `tools/build_jupyterlite_content.py` gains `CONTENT_NAMES`: every notebook shipped into
  `jupyterlite/content/` gets a student-legible name instead of the raw `chapters/` filename
  (e.g. `chap02.ipynb` → `__chap02-variables-and-statements.ipynb`), grouped by an
  underscore-prefix scheme (front matter, chapters, exercises, teach copies, then the
  upstream helper `.py`/`.txt` files) so the JupyterLite lab file browser reads in order
  instead of 49 names in one flat alphabetical list. `chapters/*.ipynb` filenames themselves
  are untouched — the rename lives entirely in the JupyterLite output layer. Pre-populated
  for chapters 9-19 (not yet in `CHAPTERS`) so the naming convention is settled before those
  chapters get their chrome pass.
- Root `overrides.json`: `sortNotebooksFirst` on the JupyterLab file browser, required for
  the new names to group correctly (`teach*` sorts alphabetically among the helper files
  otherwise).
- The old `-projector` suffix is retired in favor of `teach<NN>-<desc>.ipynb`, and is now
  opt-in per notebook (`CONTENT_NAMES`'s optional `"teach"` key) rather than automatic for
  every notebook with a `projector/` copy — drops eight meaningless
  `chapNN-exercises-projector.ipynb` variants (a title and one empty cell, blanked) that
  were shipping for no reason.

### Changed
- Chapters 1-8's chrome link bar and self-embedding iframe (and the matching
  `CELL_PATCHES` entries) updated to the new JupyterLite filenames; "Blank (JupyterLite)"
  relabeled "Teach Copy (JupyterLite)" to match.
- `jb/build.sh`, `jb/watch.sh`, `jb/prep_notebooks.py` updated to copy/prep
  `chapters/index.ipynb` alongside the chapter notebooks.

## 2026-08-09 — CSTA 2026 and CA ICT/Anchor alignment, chapters 1-3

### Added
- `standards/csta2026.json` and `standards/ca-ict-anchor.json` gain real `carriers` data for
  the first time: 4 CSTA standards and 7 ICT/Anchor items, each tied to chapter 1, 2, or 3
  with a note explaining the match. Both reference-page generators fixed to actually render
  carrier/note data on ICT/Anchor sub-items (previously only shown on top-level entries) and
  regenerated.
- Chapters 1, 2, and 3's `type="standards"` sentinel extended from AP CSP + California to a
  4-line citation block adding CSTA 2026 and CA CTE (ICT), following the same
  never-link-the-label, link-each-code convention. Chapter 1's CSTA line reads "not
  carried" — a real finding, not a gap in the work: CSTA's High School band assumes basic
  expressions and types are already covered by middle school.
- `mods/pass-3-alignment.md` updated with a new Amendments bullet tracking CSTA 2026 and
  ICT/Anchor, and both Step 4 templates extended to the 4-line format.

## 2026-08-09 — Reverse-map links on the AP CSP and CA CS reference pages (preview)

### Changed
- `alignment/apcsp-standards-reference.html` and `alignment/ca-cs-standards-reference.html`:
  every "Book chapters: N, M" line now links each chapter number individually — to the
  chapter's Read Only page (chapters 1-2, the only ones with that Pass 4 chrome so far) or
  to the plain chapter page otherwise. A preview of what the reverse map (standard ->
  chapter) looks like rendered on the page, using the real AP/CA carrier data that already
  existed from Pass 3. Not yet extended to the whole book or to CSTA/ICT (both still have no
  carrier data to link).
- CSTA and ICT/Anchor page generators updated with the same chapter-linking logic, gated to
  the `working_in_python` source, so future regenerations behave consistently once those
  frameworks have real carrier data. No visible change yet since neither has any.

## 2026-08-09 — Standards schema grows a reverse map (`carriers[]`)

### Changed
- All four `standards/*.json` files: replaced the flat `"carrier": "X", "tp_chapters": [...]`
  pair on every topic/standard (and, in `ca-ict-anchor.json`, every nested sub-item) with a
  `"carriers": [{"source": "X", "chapters": [...]}]` array — 281 entries migrated, unassigned
  becomes an empty array rather than the string `"unassigned"`. Groundwork for reverse-
  mapping standards to chapters, and eventually to other content sources beyond this book.
  `standards/README.md` documents the new shape.
- CSTA and ICT/Anchor reference-page generators updated to read `carriers[]`; regenerated
  and confirmed byte-identical output, since neither framework has any populated carriers
  yet. AP CSP and CA CS pages unaffected — neither is regenerated from JSON at render time.

## 2026-08-09 — CA links point at our own page, not CodeHS (chapters 1-3)

### Changed
- `type="standards"` sentinel in chap02 and chap03: the **California 9-12** label is no
  longer a link to `codehs.com/standards/framework/CA_9-12`; each standard code it cites now
  links individually to its own `#S-<code>` anchor on
  `alignment/ca-cs-standards-reference.html` (e.g. `#S-9-12.AP.17`). Same convention already
  used for the **AP CSP** label. chap01 unchanged — it cites no California standard, so
  there was nothing to relink. `projector/` regenerated; `make check` passes.
- `mods/pass-3-alignment.md`'s Amendments bullet and both Step 4 templates updated so
  chapters 4-19 pick up the new convention automatically — the CodeHS carve-out is gone now
  that a hosted CA page with per-standard anchors exists.

## 2026-08-09 — Three more standards reference pages: CA CS, CSTA 2026, CA ICT & Anchor

### Added
- `alignment/ca-cs-standards-reference.html`: same self-contained, searchable, anchor-linked
  template as `apcsp-standards-reference.html`, built from the existing
  `standards/castandards.json` (all 30 core 9-12 California CS standards, five strands).
  Carries the same carrier/chapter data the Step 4 work already established.
- `standards/csta2026.json` and `alignment/csta2026-standards-reference.html`: new
  extraction, maintainer-supplied source (`csta2026-standards.csv`, kept in `scratch/`,
  never committed, per non-negotiable #1). Covers the CSTA 2026 revision's 46 "High School"
  level standards across five concepts. The CSV's two elective "Specialty" tiers (135
  standards covering Data Science, Cybersecurity, AI, Game Development, Software
  Development, Physical Computing, X+CS) are not indexed, mirroring how `castandards.json`
  excludes the CA framework's own "9-12 Specialty" set.
- `standards/ca-ict-anchor.json` and `alignment/ca-ict-anchor-standards-reference.html`:
  new extraction from a maintainer-supplied PDF (`CTEModelCurrStds-ICT.pdf`, kept in
  `scratch/`, never committed). Covers the 11 CTE Anchor Standards (common to all 15
  industry sectors, 99 items including sub-standards) plus the ICT sector's Pathway C,
  Software and Systems Development (71 items) — the pathway that maps to a Python
  programming course, confirmed with the maintainer. The sector's other three pathways
  (A. Information Support and Services, B. Networking, D. Games and Simulation) are not
  indexed.
- All three pages added to `jb/_toc.yml`'s Reference sidebar section and `jb/index.md`'s
  "Also here" list, alongside the existing AP CSP page.

### Notes
- Every paraphrase in both new JSON files was checked against its source text with an
  n-gram overlap script (6-word shared sequences), same method as the AP CSP page's pass.
  CSTA: one hit found and rewritten. ICT/Anchor: twenty hits found and rewritten; one
  remaining hit (`C8.3`, database relationship-type names and key terminology) is treated
  as fixed technical vocabulary with no substitute wording, the same category as the AP
  page's accepted "TCP/IP" and "rogue access point."
- Unlike `apcsp.json` and `castandards.json`, no chapter-alignment pass has been run
  against CSTA 2026 or the ICT/Anchor standards — every entry in both new JSON files
  carries `carrier: "unassigned"` as a placeholder, not a finding. Both reference pages
  say so explicitly in their provenance box.

## 2026-08-09 — Chapter chrome becomes its own pass (Pass 4)

### Added
- `mods/pass-4-chrome.md`: the link bar / embedded pane / exercises notebook / attribution
  bundle chapters 1-2 have been carrying gets its own pass file, matching the format of
  passes 1-3. Moved (not duplicated) from `HOW_TO_EDIT.md`'s "Adding a chapter's ways to open
  this chapter link bar" and "Applying the chapter-1 chrome treatment" sections, updated to
  include this session's `?readonly`/"Read Only" mechanism and the `NotebookEdit` formatting
  hazard. `CLAUDE.md`'s pass table gets a fourth row; `HOW_TO_EDIT.md` keeps only the
  underlying non-chapter-specific mechanics and points here for the per-chapter checklist.

## 2026-08-09 — A real Read Only page for chapters 1-2, via a ?readonly flag on the same URL

### Added
- `chapters/chap01.ipynb`, `chap02.ipynb`, `jupyter_intro.ipynb`: the embedded-pane script now
  checks `new URLSearchParams(location.search).has("readonly")` and, if present, hides both the
  pane and its note entirely instead of doing anything else -- leaving just the chapter's plain
  rendered content. The "Ignore this cell" note text is now wrapped in `<p id="...-note">` so the
  script can target and hide it specifically. Same URL as the normal chapter page
  (`chapNN.html`), just with `?readonly` appended -- no new Sphinx page, no new `_toc.yml` entry,
  no duplicate notebook to keep in sync.

### Changed
- `chapters/chap01.ipynb`, `chap02.ipynb`: renamed the link bar's "Markdown" entry to "Read
  Only" and pointed it at `https://python.porttack.com/chapNN.html?readonly` instead of the bare
  page. Previously this link led to the exact same page the embedded live pane takes over --
  functionally identical to the "JupyterLite" link, not a plain readable page at all, which is
  why it never actually worked for printing or in-page search (browsers generally can't
  search into cross-frame iframe content, and the pane covered the article either way).
  `tools/build_jupyterlite_content.py`'s three matching `CELL_PATCHES` keys (chap01, chap02,
  jupyter_intro) updated to the new cell text; verified programmatically that all three patches
  still fire.

### Verified
- The new script logic in isolation, three branches, via Node with a stubbed `document`/
  `location` (no headless browser available in this session): `?readonly` hides both pane and
  note and never touches `position`; normal mode with a sidebar present goes fixed and positions
  correctly; normal mode without a sidebar (Colab) leaves the pane completely untouched, same as
  before this change. `make check` clean. Not yet verified against a real published page --
  `jb/build.sh --local` correctly refuses to run against an uncommitted `chapters/` tree, so the
  actual rendered `?readonly` page hasn't been eyeballed in a real browser yet.

## 2026-08-09 — Revert cowsay auto-install; fix the "Try it here" pane text everywhere it isn't the live pane

### Changed
- `chapters/chap01.ipynb`, `chap02.ipynb`, `jupyter_intro.ipynb`: the embedded-pane cell's
  visible text was written assuming the JB site's live-pane context, so it read literally and
  confusingly everywhere else the cell renders unstyled (Colab, raw download, Codespace/VS
  Code) — "**Try it here**... drag the thin divider" when there's no divider or live pane to
  speak of there. Replaced with `*Ignore this cell — used when running JupyterLite.*` in all
  three. `tools/build_jupyterlite_content.py`'s matching `CELL_PATCHES` keys (chap01, chap02,
  jupyter_intro) updated to the new text so the JupyterLite-hosted copy still correctly swaps
  it for the "you're already running this live" placeholder — verified the patch still matches
  in all three.

### Reverted
- `tools/build_jupyterlite_content.py`: undid the cowsay auto-install added earlier this
  session (`ALWAYS_PIPLITE_PACKAGES`, the piplite branch of `bootstrap_cell()`) at the user's
  request — back to `ascii_art.use('cowsay')` being the only way to get it, same as before.

## 2026-08-09 — Link-bar fixes; cowsay auto-installs in every JupyterLite notebook

### Changed
- `chapters/chap01.ipynb`, `chapters/chap02.ipynb`: dropped both Codespace links from the
  link bar. Download link now points at `https://python.porttack.com/_sources/chapNN.ipynb`
  (the copy Sphinx already publishes, served as `application/x-ipynb+json` rather than
  `raw.githubusercontent.com`'s `text/plain`) with an explicit `download` attribute, so it
  saves to disk instead of opening as raw JSON in the browser.
- `tools/build_jupyterlite_content.py`: `bootstrap_cell()` now also handles piplite-only
  packages (installed via `await piplite.install(...)` before import), and a new
  `ALWAYS_PIPLITE_PACKAGES` list (currently just `["cowsay"]`) gets bootstrapped into every
  notebook in `CHAPTERS`, not just ones with a matching `PRELOAD_ON_DEP` entry. A plain
  `import cowsay` now resolves instantly in any chapter's JupyterLite copy, no
  `ascii_art.use()` ceremony needed — same idea as the existing matplotlib preload, just not
  tied to a chapter dependency. Confirmed via a real `jupyter lite build`: the bootstrap cell
  survives intact into `jupyterlite/_output`.

### Investigated, not changed
- Whether to pre-bundle matplotlib/cowsay into our own build output: no, and no need to.
  Neither Pyodide's runtime nor any package wheel lives in `jupyterlite/_output` or our
  `gh-pages` branch — both are fetched live from `cdn.jsdelivr.net`/`pypi.org` by the
  student's browser. Confirmed the `loadPyodideOptions.packages` preload-at-init config is
  still broken in `jupyterlite-pyodide-kernel` 0.8.2 (the latest release), so the bootstrap-
  cell approach remains the only reliable mechanism.
- The site's existing "Print to PDF" button (via `window.print()`, already wired with a
  sidebar-hiding print stylesheet) already gives a standalone-for-printing view — holding off
  on building a new page for this until it's confirmed that doesn't already cover the need.

## 2026-08-08 — Chapter 2 gets the chapter-1 chrome treatment

### Added
- `chapters/chap02-exercises.ipynb`: blank teacher-exercises notebook, same shape as
  `chap01-exercises.ipynb`. Registered in `tools/build_jupyterlite_content.py`'s `CHAPTERS`
  (no deps).
- `chapters/chap02.ipynb`: the same "ways to open this chapter" link bar chapter 1 has
  (Exercises | JupyterLite | Colab | Markdown | Download | Codespace (notebook) | Codespace
  (VS Code) | Blank), plus an embedded live JupyterLite pane. `tools/build_jupyterlite_content.py`
  gets a matching `CELL_PATCHES` entry so the copy that ships inside JupyterLite swaps the pane
  for a one-line note instead of recursively embedding itself.

### Changed
- `chapters/chap02.ipynb`: dropped the Bookshop/Amazon retail-links cell (same cleanup chapter 1
  got in `f5aa6c0`). Closing attribution note now opens with the same `---` rule chapter 1's does,
  so both chapters' bottom matter renders identically.
- `HOW_TO_EDIT.md`: the link-bar section is no longer marked "pilot, chapter 1 only" now that a
  second chapter carries it; added a consolidated recipe for applying the whole chapter-1 chrome
  treatment (link bar, embedded pane, exercises notebook, retail-link removal, attribution rule)
  to the next chapter in one pass.

### Fixed
- `projector/chap02.ipynb`, `jupyterlite/content/` regenerated; `make check` passes.

## 2026-08-08 — Projector variants in JupyterLite; chap01 gets a teacher exercises notebook

### Added
- `tools/build_jupyterlite_content.py`: every chapter's `projector/` (blanked-for-demo) copy now
  also ships in JupyterLite automatically, as `<chapter>-projector.ipynb` alongside the regular
  chapter -- no separate list to maintain, it rides on `CHAPTERS`. `jb/build.sh` and `make
  jupyterlite` regenerate `projector/` first so this can't ship stale.
- `chapters/chap01-exercises.ipynb`: blank notebook for teacher-authored exercises, separate from
  the chapter itself. Servable in JupyterLite; not yet in the left nav (deferred).

### Changed
- `chapters/chap01.ipynb`: the link bar's "Exercises" entry now opens
  `chap01-exercises.ipynb` in JupyterLite instead of the `#exercises` anchor on the rendered page.

## 2026-08-08 — Fix chapter 1's live pane visual seam, and a recursive-iframe bug found along the way

### Fixed
- `chapters/chap01.ipynb`: the embedded live JupyterLite pane now has a `box-shadow`/`border-bottom`
  so its edge reads as intentional, not a rendering glitch, now that `862a524` (capping the pane at
  a fixed height instead of covering the whole page) is actually live for the first time.
- `tools/build_jupyterlite_content.py`: `CELL_PATCHES` for `chap01.ipynb` and `jupyter_intro.ipynb`
  had gone stale against `862a524`'s cell changes, so both notebooks were shipping a real
  recursive-iframe cell (a notebook embedding a live copy of itself inside JupyterLite) instead of
  the intended placeholder note. Fixed both keys. See `AUDIT.md`, 2026-08-08 follow-up 14.
- `chapters/chap01.ipynb`: two cells had `source` stored as a single string rather than the usual
  list-of-lines (a `NotebookEdit` artifact from this session) — harmless for rendering, but the
  proximate cause of the `CELL_PATCHES` mismatch above, since the match is keyed on
  `tuple(cell["source"])`. Normalized to match the rest of the file.

## 2026-08-08 — Chapter 1 gets a "ways to open this chapter" link bar (pilot)

### Added
- `chapters/chap01.ipynb`: a one-line link bar near the top — Exercises | JupyterLite | Colab |
  Markdown | Download | Codespace (notebook) | Codespace (VS Code) — replacing what had been two
  separate note cells (Colab-unavailable-use-JupyterLite, and the Codespace note); their
  explanatory prose was kept, merged into one paragraph under the link row. Lives inside the
  notebook itself rather than in any one renderer's chrome, so it shows up identically in Colab,
  JupyterLite, a Codespace, a raw download, and the rendered page — one edit reaches everywhere the
  notebook is opened. Pilot: chapter 1 only.
- `HOW_TO_EDIT.md`: no new section needed — the existing "Editing something that also runs in
  JupyterLite" section already documents this notebook's placeholder-substitution mechanics, which
  this link bar reuses unchanged.

### Reverted (documented, not shipped — see `AUDIT.md`, 2026-08-08 follow-up 13)
- A `_toc.yml` `sections:` entry under `chap01`, meant to render as nested sidebar links: doesn't
  work, nested `url:`-only entries never reach the sidebar in this theme.
- A `custom.js`-injected `<details>/<summary>` disclosure under chapter 1's sidebar link: worked,
  but added a second line to every chapter's entry in the contents, which wasn't wanted.

## 2026-08-08 — JupyterLite deploy path is now a content hash, not a hand-bumped VERSION

### Added
- `tools/build_jupyterlite_content.py`: `compute_deploy_id()` hashes every file that affects
  `jupyterlite/content/` (the notebooks, their dependencies, `SHARED_FILES`, the script
  itself) into `jupyterlite-<hash>`. New `--print-deploy-id` flag exposes it to shell scripts.
  `chap01.ipynb` and `jupyter_intro.ipynb` now carry a stable placeholder
  (`JUPYTERLITE_DEPLOY_PATH`) instead of a hardcoded path; `substitute_deploy_path()` fills in
  the real id for the copy that ships inside JupyterLite, and a matching step in
  `jb/prep_notebooks.py` (reading a `JUPYTERLITE_DEPLOY_ID` env var, computed once by
  `jb/build.sh`/`jb/watch.sh`) does the same for the copy on the JB site.

### Removed
- `jupyterlite/VERSION` and the manual "bump it, then update three hardcoded copies of the
  version number" process it required — replaced by the automatic hash above. This was the
  fragility flagged (and, twice, actually hit) in the last several rounds.

### Changed
- `CLAUDE.md`, `PUBLISHING.md`, `HOW_TO_EDIT.md`: versioning sections rewritten to describe
  the automatic hash instead of the manual bump.

See `AUDIT.md`, 2026-08-08 follow-up 12.

## 2026-08-08 — HOW_TO_EDIT.md added; jb/watch.sh committed

### Added
- `HOW_TO_EDIT.md`: task-oriented guide to editing this book by hand — which files are
  source vs. generated, the everyday chapter-editing loop, the extra steps needed when a
  change touches the JupyterLite-embedded notebooks (chap01, jupyter_intro), the current
  manual four-place version-bump process, and a command reference. Companion to
  `PUBLISHING.md` (architecture/why) and `CLAUDE.md` (upstream-content rules); pointed to
  from both.
- `jb/watch.sh` (this session's live-reload preview script, previously untracked) is now
  part of the repo, since `HOW_TO_EDIT.md` documents it as the standard local-preview
  workflow.

See `AUDIT.md`, 2026-08-08 follow-up 11.

## 2026-08-08 — jupyter_intro joins the left nav as its own live JupyterLite split view

### Added
- `jb/_toc.yml`: `jupyter_intro` (titled "About Jupyter Notebooks") is now the first entry
  under "Start Here", ahead of `orientation`. It was never actually part of the built site
  before this — `jb/build.sh`'s copy step only ever matched `chapNN` filenames — so this
  also required extending that copy step, `jb/watch.sh`'s equivalent (and its
  `sphinx-autobuild` ignore list), and `jb/prep_notebooks.py`'s glob to include it.
- `chapters/jupyter_intro.ipynb` gets the same live-takeover treatment chap01 got below:
  a sentinel cell that fills the page (right of the primary sidebar) with a live JupyterLite
  instance of itself, tracking the sidebar's width via `ResizeObserver`. Same `CELL_PATCHES`
  recursive-embed guard as chap01, added to `tools/build_jupyterlite_content.py`.
- JupyterLite deploy bumped to `jupyterlite-v4/`. Also fixed, in the same pass: chap01's
  iframe `src` and its link to this notebook were still hardcoded to `jupyterlite-v3` from
  the last two rounds — both now point at `v4` too.

### Changed
- Nothing in `chapters/` outside the one new cell in `jupyter_intro.ipynb` described above.

See `AUDIT.md`, 2026-08-08 follow-up 10.

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

## 2026-08-09 — Pass 4, chapters 7-8 chrome

### Added
- `chapters/chap07-exercises.ipynb`, `chap08-exercises.ipynb`: blank teacher-exercises
  notebooks, same shape as chapters 1-6's. Registered in
  `tools/build_jupyterlite_content.py`'s `CHAPTERS` with no deps.
- Link bar and embedded live JupyterLite pane added to `chap07.ipynb` and `chap08.ipynb`
  as their first two cells, matching the established pattern exactly. Matching
  `CELL_PATCHES` entries added to `tools/build_jupyterlite_content.py`, each verified
  programmatically to fire. Chapter 8's pane patch was merged into its existing
  `CELL_PATCHES` entry (which already rewrote its `!head`/`!tail` shell-magic cells)
  rather than added as a second top-level key, since a duplicate dict-literal key
  would have silently dropped one entry or the other; confirmed both sets of patches
  still fire on the live notebook.

### Fixed
- `chap07.ipynb`, `chap08.ipynb`: Bookshop/Amazon retail-links cell dropped from each,
  and each bottom attribution note given the leading `---` rule (both were still
  missing it, same universal pre-`f5aa6c0` gap as chapters 2-6).

## 2026-08-09 — Pass 4, chapters 4-6 chrome

### Added
- `chapters/chap04-exercises.ipynb`, `chap05-exercises.ipynb`, `chap06-exercises.ipynb`:
  blank teacher-exercises notebooks, same shape as chapters 1-3's. Registered in
  `tools/build_jupyterlite_content.py`'s `CHAPTERS` with no deps.
- Link bar and embedded live JupyterLite pane added to `chap04.ipynb`, `chap05.ipynb`,
  `chap06.ipynb` as their first two cells, matching the chapter 1-3 pattern exactly.
  Matching `CELL_PATCHES` entries added to `tools/build_jupyterlite_content.py`, each
  verified programmatically to fire.

### Fixed
- `chap04.ipynb`, `chap05.ipynb`, `chap06.ipynb`: Bookshop/Amazon retail-links cell
  dropped from each, and each bottom attribution note given the leading `---` rule
  (all three were still missing it, same gap chapters 2 and 3 had before their fixes).

## 2026-08-09 — Pass 4, chapter 3 chrome

### Added
- `chapters/chap03-exercises.ipynb`: blank teacher-exercises notebook, same two-cell shape
  as `chap01-exercises.ipynb`/`chap02-exercises.ipynb`. Registered in
  `tools/build_jupyterlite_content.py`'s `CHAPTERS` with no deps.
- Link bar and embedded live JupyterLite pane added to `chap03.ipynb` as its first two
  cells, matching chapters 1-2's current pattern exactly (Exercises/JupyterLite/Colab/Read
  Only/Download/Blank, no Codespace links; `?readonly` escape hatch on the pane). Matching
  `CELL_PATCHES` entry added to `tools/build_jupyterlite_content.py`, verified
  programmatically to fire.

### Fixed
- `chap03.ipynb`'s Bookshop/Amazon retail-links cell dropped, and its bottom attribution
  note given the leading `---` rule chapter 1 has had since `f5aa6c0` (chapter 3 was still
  missing it, same gap chapter 2 had before its own fix).

## 2026-08-09 — Pass 3, Step 4 (all four frameworks), chapters 4-8

### Added
- `type="standards"` sentinel in chap04-chap08: extended to the 4-line citation format
  (AP CSP, California 9-12, CSTA 2026, CA CTE (ICT)) that chapters 1-3 already carry.
  CSTA 2026 and CA CTE (ICT) alignment is new for these five chapters — read against
  `csta2026.json`'s 46 standards and `ca-ict-anchor.json`'s 170 items the same
  genuine-matches-only way chapters 1-3 were. `standards/csta2026.json` and
  `standards/ca-ict-anchor.json` gain real carrier data on 5 CSTA standards and 12
  ICT/Anchor items; `alignment/csta2026-standards-reference.html` and
  `alignment/ca-ict-anchor-standards-reference.html` patched to match.
  `projector/` regenerated; `make check` and `make ledger` pass.

### Fixed
- `CLAUDE.md`'s Pass 3 status row pointed at a nonexistent `docs/pass-3-alignment.md`; the
  file has always lived at `mods/pass-3-alignment.md`. Corrected, and the status text
  updated to reflect Step 4 now covering chapters 1-8 across all four frameworks.

## 2026-08-09 — AP CSP coverage map: wired into nav, linked both ways

### Added
- `alignment/ap-practices-bigideas-coverage.html`: the coverage-by-Practice/Big-Idea/topic
  reference (previously a repo-only `.md`) as a hosted page matching the four
  `*-standards-reference.html` pages' template, with topic and chapter numbers linking out
  to `apcsp-standards-reference.html` and the live chapter pages respectively. Added to
  `jb/_toc.yml`'s Reference section as "AP CSP Coverage Map."
- `alignment/apcsp-standards-reference.html`: one-line pointer to the new coverage map,
  right after the provenance box, so the connection runs both directions.

### Fixed
- `alignment/ap-practices-bigideas-coverage.md`'s Practices table linked
  `apcsp-standards-reference.html#T-P1`..`#T-P6`; the page's actual practice anchors are
  bare `#P1`..`#P6` (topics use `#T-<code>`, practices don't). All six links were landing
  at the top of the page instead of the right row. Corrected in both the `.md` and the new
  `.html`.
