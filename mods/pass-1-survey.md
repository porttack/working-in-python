# Pass 1 — Survey and Scaffold

Read `CLAUDE.md` first. Do not read the other pass files.

**Mode:** read-only analysis plus infrastructure. **Nothing in `chapters/` is edited in
this pass.** If you find yourself about to change a chapter file, stop; that's pass 2.

**Blocked by:** nothing. `csstandards.pdf` is not needed here.

**Why this pass exists:** everything downstream depends on knowing which file is which
chapter, how long each chapter actually takes a student, and whether the tooling works.
Getting any of those wrong is expensive to undo.

---

## Deliverables

1. `CHAPTER_MANIFEST.md` — filename map, treatment, VA decision
2. `AUDIT.md` — inventory, effort estimate, findings, handoff note
3. `data/exercise-ledger.json` — seeded with every existing exercise
4. Repo layout per `CLAUDE.md`, with doc stubs
5. `tools/check_sync.py`, `tools/build_ledger.py`, `Makefile`
6. `build_blanks.py` verified against exactly one chapter

---

## Step 1 — Filename mapping (STOP after)

Upstream numbering starts at `chap00`, so "chapter N" is ambiguous. Resolve it by reading
the chapter titles and the book's own preface, not by assuming an offset.

Produce a table in `CHAPTER_MANIFEST.md`:

| File | Chapter # | Title | Treatment | VA decision |
|---|---|---|---|---|

Treatment comes from the matrix in `CLAUDE.md`. VA decision defaults to propose:
chapters 1–8 `strip`, 9–11 `decide`, 12–13 `decide` leaning `keep`, 14–19 `keep`.

**Stop here and get this approved.** A wrong mapping means pass 2 makes destructive edits
to chapters that were supposed to stay untouched. This is the single most expensive mistake
available in this project.

Also note in the table any file that isn't a chapter (preface, Jupyter intro, appendices)
and confirm what it is.

---

## Step 2 — Inventory

Per chapter, into `AUDIT.md`:

- section headings, in order
- every "Ask a virtual assistant" item, **classified**, with line ranges:
  - **A** graded exercise whose task is to ask an assistant and evaluate the answer
  - **B** bare bulleted prompt list with no task attached
  - **C** inline sentence mid-prose suggesting an assistant could explain something
- every exercise, with a one-line description
- every glossary term
- prose word count
- code cell count

The A/B/C classification is the important part. Pass 2 replaces only kind A one-for-one;
replacing kind B would pad the book with busywork. Report the counts per chapter so the
real size of the replacement job is visible before anyone starts writing.

---

## Step 3 — Seed the exercise ledger

Write `data/exercise-ledger.json` with one entry per existing exercise, `action: "kept"`,
`kind: "native"` for exercises unrelated to VA material and `A`/`B`/`C` for those that are.

```json
{
  "chapter": "chap09",
  "id": "ch09-ex04",
  "anchor": "Write a function called uses_none",
  "kind": "native",
  "action": "kept",
  "replacement_id": null,
  "targets_ap": [],
  "targets_ca": [],
  "est_minutes_before": 15,
  "est_minutes_after": 15,
  "self_verifying": true,
  "note": ""
}
```

`targets_ap` and `targets_ca` stay empty in this pass; pass 3 fills them. `self_verifying`
is true if the exercise passes or fails via doctest or unittest.

This file is the single source for `CHANGELOG_DETAIL.md`, the counts in
`AP_MODIFICATIONS.md`, and the effort estimate. Get the ids stable now, because everything
later references them.

---

## Step 4 — Effort estimate (STOP after)

The course assumes one chapter per week at roughly 60 to 75 minutes of homework. Test that
assumption rather than accepting it.

Method:
- reading minutes = prose words / 130 (technical prose, interrupted by code)
- code cells to run and inspect: 1 minute each
- exercises classified `trivial` (≤5 min), `standard` (10–20), `extended` (25+)
- total estimated student minutes per chapter, plus a ratio against the median

Present as a table sorted heaviest first. Then answer these three directly:

1. Does chapter 1 support the hypothesis that it's roughly a 30-minute read?
2. Which chapters exceed 75 minutes?
3. Is chapter 9 (Lists) the heaviest of chapters 1–11? It's the load-bearing week for the
   Create Performance Task, and the calendar places its buffer immediately before it.

**Recommend, do not decide.** The teacher holds a uniform one-week pace deliberately and
backs off only if students struggle. Frame this as where the pressure will land, and note
which chapters could pair into one week and which might want two, as options rather than a
re-pacing proposal.

**Stop here.** This estimate may change the calendar, and pass 2 shouldn't start until the
pace is settled.

---

## Step 5 — Scaffold

Create the layout from `CLAUDE.md`. Then:

- **`.gitignore`**: `sessions/`, any scratch paths, and the framework extracts. Verify no
  extract is currently tracked; if one is, remove it from the index and say so loudly.
- **Doc stubs**: `ATTRIBUTION.md` (complete it, it's short and doesn't change),
  `AP_MODIFICATIONS.md` (section headers only), `CHANGELOG.md` (Keep a Changelog skeleton),
  `CHANGELOG_DETAIL.md` (generated banner only).
- **`tools/build_ledger.py`**: reads `data/exercise-ledger.json`, writes
  `CHANGELOG_DETAIL.md` grouped by chapter with per-chapter and total counts. Idempotent.
- **`tools/check_sync.py`**: verifies sentinel blocks are balanced and well-formed, that
  every `type` is valid, that every standards code referenced in a chapter resolves against
  the JSON indexes (skip this check while the indexes are empty), and that no chapter
  outside its treatment tier carries markers it shouldn't.
- **`Makefile`**: the four targets from `CLAUDE.md`.

---

## Step 6 — Verify the blanks tooling

`tools/build_blanks.py` is provided and tested. Do not rewrite it.

Pick **one** chapter from 1–11. Add blank markers to that chapter only. Then:

```
make blanks          # should write blanks/<chapter>
make check           # should pass
```

Then deliberately break it twice, to confirm the guardrails are live:
- hand-edit `blanks/<chapter>` and confirm `make check` exits 1
- remove a `<!--/blank-->` in the chapter and confirm the build exits 2 naming the file

Report the marker count you used and how it felt. Marker density is the one thing that
reads fine in a diff and feels wrong in front of a class, so one chapter reviewed carefully
beats eleven done fast.

**Note:** this is the only chapter edit permitted in pass 1, and it is additive markup, not
surgery.

---

## Handoff

Append to `AUDIT.md`:

- the approved filename mapping, restated
- A/B/C counts per chapter and the total size of the replacement job
- the effort table and the answers to the three questions in step 4
- which chapter got markers, with the count
- anything the mapping or inventory turned up that contradicts the treatment matrix
- what pass 2 needs to know before it starts
