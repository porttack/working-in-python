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

## `carriers[]` — the reverse map

Every standard-level entry (a topic in `apcsp.json`, a standard in `castandards.json` /
`csta2026.json`, an anchor standard or pathway standard, including nested `items`, in
`ca-ict-anchor.json`) carries a `carriers` array instead of a single `carrier` string:

```json
"carriers": [
  { "source": "working_in_python", "chapters": [7, 9] },
  { "source": "little_brother", "chapters": [] }
]
```

An empty array (`"carriers": []`) means unassigned — no source covers this standard yet,
not "checked and found nothing." `source` is a free-form slug, not a closed enum; add a new
one (e.g. a future non-book resource) the first time something actually carries a standard
for it. `chapters` holds whatever locator makes sense for that source — chapter numbers for
`working_in_python`, so far always empty for `little_brother` and `supplement` since neither
has per-unit tracking yet.

This shape is what lets a standard list more than one carrier (a book chapter *and* a unit
in another resource, say), which a flat `carrier` string couldn't express. `apcsp.json`'s
`big_ideas[].carrier` is unrelated and untouched — that's a coarser "primary carrier for
this whole Big Idea" rollup label, not a per-standard mapping.

Nothing yet reverses this into "which standards does chapter N cover" or "what fraction of
framework X does source Y cover" — both are real next steps, not built here.
