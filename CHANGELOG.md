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
