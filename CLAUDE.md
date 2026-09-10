# CLAUDE.md

Fork of Allen Downey's *Think Python* 3rd edition, adapted into the reading spine and
homework text for a high school AP Computer Science Principles course in California.

## Read this first

Work happens in five passes. **Read only the pass file for the pass you are running.**
Do not read the other pass files; they will fill your context with work that isn't yours.

| Pass | File | Mode | Status |
|---|---|---|---|
| 1. Survey and scaffold | `docs/pass-1-survey.md` (actually at `mods/pass-1-survey.md` — see `AUDIT.md` handoff) | read-only + tooling | done, see `AUDIT.md` handoff |
| 2. Chapter surgery | `mods/pass-2-surgery.md` | destructive edits + authoring | in progress — ch. 1–8 done (the whole "chapters 3–8" batch, across three sessions). Ch. 9–19: Step 1 (VA removal) and Step 2 (replacement exercise) done 2026-09-09, for all eleven chapters in one batch, following the book-wide VA-removal policy decided the same day (see the treatment matrix above and `AUDIT.md`'s 2026-09-09 handoff). This closes out the book's kind-A count at four-for-four: ch17-ex07 (Kangaroo mutable-default-argument bug) was the last one standing and now has a native replacement, ch17-ex07r. Blank markers (Step 4, chapters 9–13 only) and per-chapter checkout (Step 5) for ch. 9–19 are still pending -- Step 1/2 was done as a single cross-chapter policy pass rather chapter-by-chapter in the usual order, so those steps remain open work, not implicitly done. Three of the four kind-A replacements before today stood as written; the fourth (ch05-ex06's replacement, ch05-ex07, a Sierpinski-triangle turtle exercise) was written, then removed 2026-08-24 as too failure-prone for ungraded optional practice with no in-class reference solution -- that slot still has no native replacement (this is unrelated to today's ch17 work). See `data/exercise-ledger.json` and `AUDIT.md`. Pacing question still open. `chap06b`, the first *interlude* (original content between two numbered chapters — see `CHAPTER_MANIFEST.md`), authored outside this pass's normal order and fully wired 2026-08-17; more interludes planned (unit testing, binary). `chap07b`, the second interlude ("Representing Data," between chapters 7 and 8), supplied 2026-08-17 as an outline only — no drafted prose or exercises yet — and wired into the TOC and vocab/standards back matter ahead of authoring; still needs actual Pass 2 drafting. See `AUDIT.md` |
| 3. Standards alignment | `mods/pass-3-alignment.md` | analysis + additive back matter | in progress — Steps 1–3 done (both indexes, `standards/crosswalk.json`, all three `alignment/*.md` docs); Step 4 done for chapters 1–8, all four frameworks (AP CSP, CA 9-12, CSTA 2026, CA CTE/ICT — the latter two added 2026-08-09, out of this pass's original scope). Chapters 9–19 and Step 5 not started. AP 2.1/2.2 and CA DA.8/DA.9 carriers reassigned to `chap07b` 2026-08-17, ahead of that chapter actually being drafted — see `AUDIT.md`. CSTA 2026 and CA CTE/ICT for `chap07b` still TBD. See `AUDIT.md` |
| 4. Chapter chrome | `mods/pass-4-chrome.md` | destructive edits (front/back matter only — link bar, embedded pane, exercises notebook, attribution rule) | in progress — ch. 1–2 done, built up across several rounds of live testing against the deployed site; ch. 3–8 done 2026-08-09, matched the pattern exactly (ch. 8 needed a `CELL_PATCHES` merge, not a fresh key — see `AUDIT.md`); ch. 9–11 pending; ch. 12–19 out of scope (independent-study/post-exam tier gets none of this). `chap06b` interlude got the same chrome treatment 2026-08-17, plus a `jb/_toc.yml`/`jb/build.sh` wrinkle unique to interludes — see `AUDIT.md`. `chap07b` (second interlude, outline only) deliberately has NOT had this pass's treatment yet — no chrome for a chapter with no prose — pending its actual authoring. Step 1 (Homework-section content authoring, superseded from the old separate-notebook pattern 2026-08-16) is its own tracked sub-progress: chapters 1, 2, 4, 5, 6, and 6b have a `## Homework` section; chapter 8 got its first one 2026-09-07 and chapter 7 got its first one 2026-09-08 (both out of order, same-day assignments — see `AUDIT.md`); chapters 9–11 still have none. **Terminology split, deliberate:** chapters 7 and 8 number their graded Homework items "Problem N" (renamed from "Exercise N" 2026-09-08, to stop that word meaning two different things depending on section); chapters 1, 2, 4, 5, 6, and 6b still say "Exercise N" in their own Homework sections — not yet reconciled, see `AUDIT.md` for the scoping call. Any new Homework section (9–11) should use "Problem N" |
| 5. JupyterLite lab & naming | `mods/pass-5-jupyterlite-lab.md` | additive tooling (`chapters/index.ipynb`, `CONTENT_NAMES`, `overrides.json`, `custom.js`) + a small piece of every future Pass 2/4 chapter | in progress — front page, naming foundation for everything currently in `CHAPTERS`, and sticky `?readonly` nav done 2026-08-09; `CONTENT_NAMES` pre-populated for ch. 9–19 ahead of Passes 2/4 reaching them, not yet wired into `CHAPTERS`. `chap07b` (second interlude, outline only as of 2026-08-17) deliberately NOT added to `CHAPTERS`/`CONTENT_NAMES` yet — pending actual authoring, same reasoning as Pass 4. See `AUDIT.md` |

Keep the Status column current. Each pass ends by appending a handoff note to `AUDIT.md`
so the next pass can start cold. If you weren't told which pass to run, read the last
handoff note in `AUDIT.md` and ask.

---

## Non-negotiable

1. **No copyrighted framework prose in this repo.** Reference AP codes (`AAP-2.N`,
   `DAT-1.A`) and CA codes (`9-12.AP.14`) freely. Paraphrase everything else in original
   words. The CED extract and the CA standards extract stay in scratch, outside the repo,
   never committed. This repo is CC BY-NC-SA; relicensing College Board or state prose
   under it is not ours to do.

2. **Small, legible diffs against upstream.** Every addition goes inside a sentinel block.
   Never reflow, re-wrap, restyle, reorder, or rename upstream content. The goal is to pull
   Downey's corrections next year instead of re-forking.

3. **`projector/` is generated. Never hand-edit it.** `make check` will catch it.

4. **Every exercise touched is recorded in `data/exercise-ledger.json`.** No silent edits.

5. **Notebook hygiene.** No committed outputs, no execution counts. `nbstripout` before commit.

---

## Treatment matrix

Every chapter gets treated. Which treatment depends on how it's taught.

| Chapters | Taught how | VA removal | Blank markers | Standards block |
|---|---|---|---|---|
| **1–11** | Live, Aug–Dec, one per week | `strip` | full | full form |
| **12–13** | May, post-exam | `strip` | full | full form |
| **14–19** | Independent study, post-AP pathway | `strip` | **none** | short form |

Blanks exist to be projected and worked through live. A chapter read independently gains
nothing from them. If a chapter later moves into live instruction, add markers then.

**VA removal is `strip` for every tier, decided 2026-09-09.** The earlier per-tier split
(full removal for 1–11, an open "teacher decision" for 12–13, `keep` for 14–19) assumed
older, more independent students in the 12–19 range could be trusted to use a VA well.
The maintainer decided that assumption doesn't hold — the temptation to lean on a VA
instead of doing the work is not something students grow out of — and it was too early
in the year to make a narrower call, so the simple, uniform answer is to strip it
everywhere. See `AUDIT.md`'s 2026-09-09 handoff for what this changed in chapters 9–19.

This table is keyed by chapter number, which an *interlude* (original content inserted
between two numbered chapters, not part of *Think Python* — see `CHAPTER_MANIFEST.md`)
doesn't have. An interlude inherits its tier from the chapters on either side of it, not
from a lookup in this table — `chap06b`, between two Live/1–11 chapters, is `strip`/full
blanks/full form. Record each interlude's inherited tier in `CHAPTER_MANIFEST.md` as it's
added.

---

## Sentinels and markers

**Sentinels.** All additions to upstream files:

```markdown
<!-- apcsp:begin type="standards" chapter="09" -->
...
<!-- apcsp:end -->
```

Valid `type`: `standards`, `glossary`, `exercise`, `note`, `pseudocode`.

**Blank markers.** HTML comments, invisible when rendered, so `chapters/` needs no build
step and displays correctly as written. Only `projector/` is generated.

| Marker | In `chapters/` | In `projector/` |
|---|---|---|
| `<!--blank-->visible text<!--/blank-->` | renders normally | underscores, sized to original |
| `<!--blank-only: prompt text-->` | invisible | renders the prompt |
| code line ending `# blank` | normal code | code replaced by underscores, indent kept |
| code cell tagged `blank` | normal code | first line kept, indented `# your code here` |

Placement: blank worked examples in the body, never exercises (upstream exercises already
ship as `# Solution goes here`). One blank per paragraph at most. Prefer glossary terms and
the operative verb of a definition. In code, blank the line carrying the concept, not
boilerplate. Every blank must be recoverable from context by a student who did the reading;
if it isn't, it's a quiz question, not a blank. Use `<!--blank-only: ...-->` for the
question you'd ask aloud at that moment.

---

## Layout

```
chapters/                    forked upstream. the source of truth.
projector/                   GENERATED. committed. never hand-edited.
sessions/                    gitignored. dated copies for live annotation.
standards/
  SYNCED, read-only copy of the learn repo's catalog + generator. Do not hand-edit
  the JSON files or build_alignment.py; see standards/README.md.
  apcsp.json                 from the 2023 CED
  castandards.json           from csstandards.pdf
  csta2026.json              CSTA 2026 revision
  ca-ict-anchor.json         CA CTE ICT sector, anchor + Pathway C
  crosswalk.json             AP topic <-> CA standard
  carriers/working-in-python.json   this book's own coverage only (locators, not carrier/tp_chapters)
alignment/
  *-standards-reference.html GENERATED (book-scoped) by tools/build_alignment.py
  standards_alignment.md     GENERATED (book-scoped): coverage summary + by-source + gaps
  glossary-map.md            hand-curated, not generated (vocabulary system, separate from standards)
  (supplement-plan.md removed 2026-08-28 -- it described non-book carriers; the
  cross-source version lives at learn.porttack.com/standards/alignment/)
appendix/
  pseudocode-crosswalk.md
  cs50p-map.md
data/
  exercise-ledger.json       every exercise touched
tools/
  build_blanks.py            PROVIDED AND TESTED. do not rewrite.
  build_ledger.py
  check_sync.py
docs/                        pass files
AUDIT.md                     working notes + handoff notes
CHAPTER_MANIFEST.md          filename map, treatment, VA decision per chapter
ATTRIBUTION.md               credit and licensing
AP_MODIFICATIONS.md          what changed and why, in prose
PUBLISHING.md                how the site is built, and why (architecture, mechanics)
HOW_TO_EDIT.md               task-oriented: which file to edit, what to run
FUTURE_DEPLOYMENT.md         plan for moving publishing into GitHub Actions -- not built yet
CHANGELOG.md                 dated, append-only, summary level
CHANGELOG_DETAIL.md          GENERATED from the ledger
Makefile
```

```make
projector: ; python3 tools/build_blanks.py --dst projector
ledger:  ; python3 tools/build_ledger.py
check:   ; python3 tools/build_blanks.py --dst projector --check && python3 tools/check_sync.py
session: ; @mkdir -p sessions/$(shell date +%F)-$(CH) && cp projector/$(CH).ipynb sessions/$(shell date +%F)-$(CH)/
```

`tools/build_blanks.py` is provided and tested. Extensions must preserve three behaviors:
idempotent regeneration; `--check` exits 1 on stale or hand-edited output; malformed markers
exit 2 naming the file.

---

## Style

Match Downey's voice: plain, short sentences, terms defined on first use, no hype. Second
person for the student, present tense. Em dashes sparingly. No emoji. No meta-commentary
about the adaptation inside student-facing text; teacher notes go in `AUDIT.md` or commit
messages. Every new term goes into that chapter's glossary.

---

## Done, every pass

1. `make check` passes
2. `git diff upstream/v3 -- chapters/` shows changes only inside sentinel blocks, blank
   markers, and removed VA sections, and touches only the chapters this pass owns
3. No verbatim framework prose anywhere; no extract committed
4. Notebooks carry no outputs or execution counts
5. `CHANGELOG.md` has a dated entry
6. Handoff note appended to `AUDIT.md`: what was done, what was decided, what the next pass
   needs to know, what is still open

---

## Raise rather than decide

- The filename mapping is ambiguous in any way
- A chapter's effort estimate exceeds double the median
- Removing VA material leaves a section incoherent rather than merely shorter
- A standard in either framework has no plausible carrier
- The two frameworks disagree in a way that changes what must be taught
- Any temptation to restructure, resequence, or rewrite upstream prose
- Any case where following instructions would require reproducing CED, CA framework, or
  CS50 text

## JupyterLite versioning

Every JupyterLite deploy (the Colab-outage fallback for chapters 1-11) is served from
`jupyterlite-<hash>/`, never a bare `jupyterlite/`. The hash is computed automatically from
the content that ships (`tools/build_jupyterlite_content.py`'s `compute_deploy_id()`) --
there is no `VERSION` file to bump and nothing to remember. **Never add `?enableCache=true`**
to a JupyterLite link. Both this and the content-hashed path exist so a live deploy can never
be masked by a stale copy in a student's browser or a school network's caching proxy -- a
content change always lands at a URL nobody has ever fetched before, which no cache policy can
get wrong. See `PUBLISHING.md` for the mechanics and the full reasoning.

## Context

Course calendar: 39 weeks, 176 hours. Chapters 1–11 taught Aug 6 to Dec 17, one per week.
January is consolidation. *Little Brother* carries AP Big Ideas 4 and 5 (up to 41% of the
exam) and CA's NI and IC strands; do not add that material to this book. First student day
is 2026-08-06.