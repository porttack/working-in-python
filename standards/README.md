# standards/

**This is now a synced, read-only copy.** The catalog (`apcsp.json`,
`castandards.json`, `csta2026.json`, `ca-ict-anchor.json`, `crosswalk.json`)
and the generator (`../tools/build_alignment.py`) are canonical in the
`learn` repo now, not here — a standards catalog stopped being book-specific
the moment a second content source (a blog post, `little_brother`) needed to
cite it. See `SYNCED_FROM.md` for the commit this was synced from and
`../CLAUDE.md`'s Layout section for how that fits the rest of this repo.

**Do not hand-edit these JSON files or `build_alignment.py`.** Edit them in
`learn`, then re-run `learn/tools/sync-standards.sh /path/to/this/repo
working_in_python` to refresh this copy.

Each catalog file contains only official standard codes and original
paraphrases written for this project, per `CLAUDE.md` non-negotiable #1 —
never verbatim framework text. The third-party framework documents these are
built from are never committed here or in `learn`:

- AP CSP Course and Exam Description (2023) — College Board
- California K-12 Computer Science Standards — CDE
- CSTA K-12 Computer Science Standards, 2026 revision — CSTA
- California CTE Model Curriculum Standards, ICT sector — CDE

## What changed from the old schema

Every standard used to carry a `carriers: [{source, chapters}]` array inline
(see git history on this file for the old contract). That reverse-map data
now lives separately in `carriers/working-in-python.json` — **only this
book's own coverage**, keyed by framework and code, e.g.:

```json
"coverage": {
  "apcsp": { "3.8": { "locators": [3, 7], "note": "..." } }
}
```

This repo's copy of `carriers/` intentionally holds only
`working-in-python.json`. Other sources (`little_brother`, `supplement`)
have their own carrier files that live in `learn`, not here — this repo
generates a **book-scoped** view (run `build_alignment.py` with `--source
working_in_python`) and has no visibility into the wider course picture on
purpose. The cross-source reverse map is `learn.porttack.com/standards/alignment/`.

## Regenerating this repo's reference pages

```
python3 tools/build_alignment.py --catalog standards --carriers standards/carriers \
  --out alignment --source working_in_python --scope-label "Working in Python"
```
