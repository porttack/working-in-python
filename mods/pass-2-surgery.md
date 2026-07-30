# Pass 2 — Chapter Surgery

Read `CLAUDE.md` first, then the last handoff note in `AUDIT.md`. Do not read the other
pass files.

**Mode:** destructive edits to `chapters/`, plus a small amount of exercise authoring.

**Blocked by:** Pass 1, specifically the approved filename mapping in `CHAPTER_MANIFEST.md`.
If that table is not present and approved, stop and say so.

**Not blocked by:** `csstandards.pdf` or either standards index. Nothing here needs them.
Leave `targets_ap` and `targets_ca` empty in the ledger; Pass 3 fills them.

---

## What Pass 1 found that changes this pass

1. **Only 4 exercises are genuinely VA-driven (kind A).** The replacement-authoring job is
   four exercises, not dozens. Do not go looking for more work than that.
2. **Upstream already ships a `blank/` directory** — chapter notebooks with outputs cleared
   and some examples removed, so the teacher can run through them live and make mistakes on
   purpose. **Do not duplicate that.** It changes where our markers add value. See Step 4.
3. **Median chapter is 165 minutes of student time against a 75-minute homework budget.**
   The resolution is that chapter *reading* is homework and chapter *exercises* are lab work
   in the 120-minute blocks. This does not change what you do in this pass, but it means
   marker placement should serve live classroom work, not solo reading.
4. **Chapter 11 is the heaviest chapter, not chapter 9.** Expect its markup to take longer.

Our generated output directory is `projector/`. Upstream's `blank/` is not ours: never write
to it, never modify it.

---

## Order of work

August 6 is the first student day. Fast students will reach chapter 3 within two weeks, so
chapters 1 through 8 all ship before then.

1. **Chapters 1–2** — complete, then **STOP** for a register and marker-density review.
   This gate is about establishing the pattern, not about progress.
2. **Chapters 3–8** — one batch, conforming to the approved pattern from chapters 1–2.
3. **Chapters 9–11** — VA decision is `decide`; do not touch VA material without a ruling.
   Blank markers proceed regardless.
4. **Chapters 12–13** — same, leaning `keep`.
5. **Chapters 14–19** — `keep`, no markers. Nearly a no-op. Confirm nothing was touched.

**Model guidance:** chapters 1–2 run on Opus, because marker density is a judgment call and
this is where the pattern gets set. Chapters 3–8 run on opusplan, because they are
conformance to a pattern a human has already reviewed.

---

## Step 1 — VA removal

Only chapters whose VA decision is `strip`. Use the A/B/C classification already recorded in
`AUDIT.md` and `data/exercise-ledger.json`.

| Kind | What it is | Action |
|---|---|---|
| **A** | graded exercise whose task is to ask an assistant and evaluate the answer | remove, replace one-for-one |
| **B** | bare bulleted prompt list with no task attached | remove, no replacement |
| **C** | inline sentence mid-prose suggesting an assistant could explain something | remove, no replacement |

Removing a kind C sometimes leaves a sentence reading as a stub. Repair minimally, in
Downey's register, and record it as a prose edit in the handoff. If repairing would mean
rewriting a paragraph, stop and raise it: that is a case where removal costs more than it
saves.

Record every removal in the ledger with `action: "removed"`.

---

## Step 2 — Replacement exercises

**Four total, across the whole book.** One per removed kind-A exercise. No more. Padding to
match a raw VA count is the failure mode here.

Each replacement:
- matches Downey's register: short, concrete, testable, built on the chapter's own examples
- where the chapter uses doctest or unittest, written the same way, with
  `self_verifying: true` in the ledger
- lands within a few minutes of the removed exercise's estimated time, so the Pass 1 effort
  table stays honest
- sits inside a `type="exercise"` sentinel block
- is recorded with `action: "added"` and a `replacement_id` linking it to what it replaced

Do not write AI-critique exercises. Fundamentals are taught by hand in the fall, and
attribution is taught separately, outside this text.

After each chapter: `make ledger`, and confirm `CHANGELOG_DETAIL.md` regenerates cleanly.

---

## Step 3 — Policy note

**Once, in front matter, nowhere else.** One paragraph, matter-of-fact: first-semester work
is done by hand, and the policy changes later in the year. Inside a `type="note"` sentinel.

Do not moralize. Do not repeat it per chapter. Do not write attribution guidance.

---

## Step 4 — Blank markers

Chapters 1–13 only. Chapters 14–19 get none.

### What upstream already does, and what we add

Downey's `blank/` directory already provides notebooks with outputs cleared and some code
examples removed, for live teaching. **Code blanking is largely upstream's job.** What
upstream does not provide is prose blanks and spoken prompts. That is our contribution.

Target per chapter, roughly:
- **4 to 6 prose blanks** on glossary terms and the operative verbs of definitions
- **2 to 4 `<!--blank-only:-->` prompts**, the questions you would ask aloud at that moment
- **0 to 2 `# blank` code lines**, only where a specific line carries a concept the prose
  blanks cannot reach

A chapter with five prose blanks and three good prompts beats one with fifteen underscores.
If a chapter seems to want far more code blanking than this, check whether upstream's
`blank/` version of that chapter already handles it.

### Placement rules

- Blank **worked examples in the chapter body**, never exercises. Upstream exercises already
  ship as `# Solution goes here` stubs.
- **One blank per paragraph at most.**
- Prefer glossary terms and the operative verb of a definition over incidental nouns.
- In code, blank the line carrying the concept: the loop header, the condition, the return.
  Never boilerplate or imports.
- Every blank must be recoverable from surrounding context by a student who did the reading.
  If it is not, it is a quiz question, not a blank.
- `<!--blank-only:-->` prompts are worth more than underscores. Use them where a question
  would land better than a gap.

Marker syntax is in `CLAUDE.md`. Note that `# blank` works in both `.ipynb` code cells and
`.md` fenced blocks; a `# blank` outside a fence in a `.md` file is an error and the build
will say so.

`make projector && make check` after each chapter.

---

## Step 5 — Per-chapter checkout

Before moving on:

1. `make check` passes
2. `make ledger` regenerates with no manual edits
3. `git diff upstream/v3 -- chapters/<file>` shows only: removed VA sections, sentinel
   blocks, blank markers, and any minimal prose repair from Step 1
4. `git status` shows nothing added or modified under `blank/` — that directory is upstream's
5. the notebook has no outputs and no execution counts
6. one line appended to `CHANGELOG.md`

**Commit per chapter, not per pass.** Chapter-sized commits make a revert a one-command
operation.

---

## Handoff

Append to `AUDIT.md`:

- chapters completed, with per-chapter removal and replacement counts
- the four replacement exercises, with what each replaced
- every prose repair made under Step 1, so a reader of the original can be told what moved
- marker counts per chapter, broken out by prose blanks, prompts, and code blanks, against
  the Step 4 targets, with reasons for any outliers
- whether upstream's `blank/` version of any chapter made our markers redundant
- chapters left in `decide` state and what ruling they need
- anything that made you want to restructure upstream prose, and what you did instead