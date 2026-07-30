# CLAUDE.md

Fork of Allen Downey's *Think Python* 3rd edition, adapted into the reading spine and
homework text for a high school AP Computer Science Principles course in California.

## Read this first

Work happens in three passes. **Read only the pass file for the pass you are running.**
Do not read the other pass files; they will fill your context with work that isn't yours.

| Pass | File | Mode | Status |
|---|---|---|---|
| 1. Survey and scaffold | `docs/pass-1-survey.md` (actually at `mods/pass-1-survey.md` — see `AUDIT.md` handoff) | read-only + tooling | done, see `AUDIT.md` handoff |
| 2. Chapter surgery | `mods/pass-2-surgery.md` | destructive edits + authoring | in progress — ch. 1–2 done, **stopped at the register/marker-density gate**; ch. 3–19 pending. Pacing question still open. See `AUDIT.md` |
| 3. Standards alignment | `docs/pass-3-alignment.md` | analysis + additive back matter | in progress — Steps 1–2 done (`standards/apcsp.json`, `standards/castandards.json` built); stopped at the Step 2 gate. Steps 3–5 not started. See `AUDIT.md` |

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
| **12–13** | May, post-exam | teacher decision | full | full form |
| **14–19** | Independent study, post-AP pathway | `keep` | **none** | short form |

Blanks exist to be projected and worked through live. A chapter read independently gains
nothing from them. If a chapter later moves into live instruction, add markers then.

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
  apcsp.json                 from the 2023 CED
  castandards.json           from csstandards.pdf
  crosswalk.json             AP topic <-> CA standard
alignment/
  standards_alignment.md     GENERATED. four views: chapter, AP, CA, gaps.
  glossary-map.md            GENERATED
  supplement-plan.md         GENERATED. what is taught outside this book.
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

## Context

Course calendar: 39 weeks, 176 hours. Chapters 1–11 taught Aug 6 to Dec 17, one per week.
January is consolidation. *Little Brother* carries AP Big Ideas 4 and 5 (up to 41% of the
exam) and CA's NI and IC strands; do not add that material to this book. First student day
is 2026-08-06.