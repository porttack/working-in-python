# standards/

Paraphrased standards data only — `apcsp.json`, `castandards.json`, `csta2026.json`,
`ca-ict-anchor.json`, and `crosswalk.json`. Each contains only official standard codes and
original paraphrases written for this project, per `CLAUDE.md` non-negotiable #1.

The third-party framework documents these are built from are never committed here:

- AP CSP Course and Exam Description (2023) — College Board
- California K-12 Computer Science Standards — CDE
- CSTA K-12 Computer Science Standards, 2026 revision — CSTA
- California CTE Model Curriculum Standards, ICT sector — CDE

They live in `scratch/` (gitignored wholesale) for the duration of whatever extraction pass
reads them, then can be discarded — nothing under `standards/` should ever be a raw
extract. `.gitignore`'s `standards/*.pdf` line is a backstop, not the intended home for
these files.
