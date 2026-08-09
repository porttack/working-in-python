# Pass 3 — Standards Alignment

## Amendments

- **`chapters/` is `.ipynb` only.** The `.md` exports were deleted. Standards inserts go
  into notebook JSON. After every chapter, `make check` must pass; it asserts each notebook
  parses as JSON and that cell counts match `upstream/v3`. Those two assertions are how a
  botched JSON edit gets caught, so do not skip them.
- **Notebook hygiene, revised.** Introduce no new outputs and change no existing
  `execution_count`. Upstream ships 1353 of them; leave them alone. Never run `nbstripout`
  across the book.
- **Confirm `standards/csstandards.pdf` exists before Step 2.** The PDFs are gitignored, so
  presence is not visible in git. If it is missing, do Steps 1, 3, and 5, and stop before
  Step 2. Note in the handoff that the California half is outstanding.
- **Kind D exists.** Prose that mentions virtual assistants without directing the student to
  use one is kept, no action. Relevant only if you touch VA prose, which this pass should not.
- **Standards links, AP CSP.** As of 2026-07-30 we host our own AP CSP standards reference
  at `alignment/apcsp-standards-reference.html`, deployed to
  `https://python.porttack.com/alignment/apcsp-standards-reference.html`, with a `#T-<code>`
  anchor on every topic (e.g. `#T-3.10`). Do not link the **AP CSP** label itself — link each
  individual topic citation in the line to its own anchor, e.g.
  `[3.10 Lists](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.10)`.
  This superseded the earlier CodeHS-framework-page convention (still visible in commit
  b0a2f53 for chapters 1-3, later redone in the AUDIT.md handoff dated 2026-07-30 "Redo AP
  linking"); do not link to `codehs.com` for AP CSP going forward.
- **Standards links, California.** As of 2026-08-09 we host our own CA CS standards
  reference at `alignment/ca-cs-standards-reference.html`, deployed to
  `https://python.porttack.com/alignment/ca-cs-standards-reference.html`, with a
  `#S-<code>` anchor on every standard (e.g. `#S-9-12.AP.16`). Same treatment as AP CSP: do
  not link the **California 9-12** label itself — link each individual code cited in the
  line to its own anchor, e.g.
  `[9-12.AP.16](https://python.porttack.com/alignment/ca-cs-standards-reference.html#S-9-12.AP.16)`.
  This superseded the CodeHS-framework-page convention (still visible in commit b0a2f53 and
  every chapter before this change; redone for chapters 1-3 in the AUDIT.md handoff dated
  2026-08-09 "CA links point at our own page"); do not link to `codehs.com` for California
  going forward. Link only the line that actually cites a code; leave a line unlinked if it
  says "not assessed" or "no standard names this content on its own."
- **Two more frameworks, added 2026-08-09: CSTA 2026 and CA CTE (ICT).** Out of this pass's
  original scope (AP CSP + CA CS only) but requested by the maintainer and treated the same
  way. `standards/csta2026.json` (46 "High School"-level CSTA 2026 standards; the CSV's
  lower grade bands and two elective "Specialty" tiers are not indexed) and
  `standards/ca-ict-anchor.json` (the 11 cross-sector CTE Anchor Standards plus ICT Pathway
  C, Software and Systems Development — the pathway that maps to this course; the sector's
  other three pathways are not indexed) both follow the same shape as `apcsp.json` — a
  `carriers` array per standard, `[]` when unassigned — and both have their own reference
  page with a `#T-<code>` anchor per standard:
  `alignment/csta2026-standards-reference.html` and
  `alignment/ca-ict-anchor-standards-reference.html`. Same linking convention as AP/CA: never
  link the framework label itself, link each cited code to its own anchor.
  **Status as of 2026-08-09: alignment done for chapters 1-3 only**, added alongside that
  session's AP/CA carrier work, not as a full Step 1-3 pass — no `crosswalk.json` entries
  exist yet between these two frameworks and AP/CA, and `standards_alignment.md`'s four
  views haven't been extended to cover them. Chapters 4-19 need the same treatment: read the
  chapter, check it against `csta2026.json`'s 46 standards and `ca-ict-anchor.json`'s 170
  items, and be as willing to find nothing as something — CSTA's HS-band standards in
  particular assume middle-school-level programming vocabulary is already established, so
  many chapters (this book's own chapter 1, for instance) may legitimately carry none of
  them, the same kind of honest gap Step 1 already normalized for AP/CA.

## Go...

Read `CLAUDE.md` first, then the last handoff note in `AUDIT.md`. Do not read the other
pass files.

**Mode:** analysis, then additive back matter. Nothing in this pass removes anything.

**Blocked by:** pass 1 (the ledger and chapter inventory), and `csstandards.pdf` for the
California half. The AP half can proceed without it. If `csstandards.pdf` is missing, do
Steps 1, 3, and 5, and stop before Step 2.

**Not blocked by:** pass 2. Standards inserts are back matter, so a chapter already being
taught can receive one with no disruption.

---

## Step 1 — AP index (STOP after)

`standards/apcsp.json`, from the 2023 CED.

```json
{
  "meta": { "ced_version": "...", "extracted": "YYYY-MM-DD",
            "section_ii_format": "on-exam-day written response with Personalized Project Reference",
            "cpt_class_hours_minimum": 9 },
  "big_ideas": [
    { "id": "AAP", "number": 3, "name": "Algorithms and Programming",
      "mcq_weight_low": 30, "mcq_weight_high": 35, "carrier": "working_in_python" }
  ],
  "practices": [
    { "id": "P5", "name": "Computing Innovations", "mcq_weight_low": 28, "mcq_weight_high": 33 }
  ],
  "topics": [
    { "code": "3.10", "big_idea": "AAP", "title": "Lists",
      "los": ["AAP-2.N", "AAP-2.O"], "paraphrase": "<original wording only>",
      "class_periods": null, "tp_chapters": [9],
      "carrier": "working_in_python",
      "exclusions": ["linked lists are outside course scope (AAP-1.D.6)"] }
  ]
}
```

Notes:

- **Weights** come from the CED's own table. Verify rather than trusting any table you were
  handed. Expected shape: CRD 10–13, DAT 17–22, AAP 30–35, CSN 11–15, IOC 21–26.
- **`class_periods`** comes from the Course at a Glance table, which does not survive PDF
  text extraction cleanly. Parse from the table layout, not the text layer. Leave `null`
  with a note rather than guessing; these numbers feed the course calendar.
- **`exclusions`** are time savings and there are more than you'd expect. Known: linked
  lists out of scope (AAP-1.D.6); specific implementations of binary search out of scope
  (AAP-2.P.1). Find the rest.
- **`tp_chapters`** by reading chapters, not guessing.
- **`carrier`** is `working_in_python`, `little_brother`, `supplement`, or `unassigned`. Report
  every `unassigned` topic; do not leave one quietly.

---

## Step 2 — California index (STOP after)

`standards/castandards.json`, from `csstandards.pdf`. Same shape:

```json
{ "code": "9-12.AP.14", "strand": "AP", "strand_name": "Algorithms & Programming",
  "grade_band": "9-12", "core": true, "paraphrase": "<original wording only>",
  "tp_chapters": [14, 15], "carrier": "working_in_python" }
```

Validate your extraction against the expected shape: five strands, thirty core standards in
the 9–12 band. CS.1–3 (Computing Systems), NI.4–7 (Networks and the Internet), DA.8–11
(Data and Analysis), AP.12–22 (Algorithms and Programming), IC.23–30 (Impacts of
Computing). **If your extraction disagrees with this shape, report the disagreement rather
than silently adopting either version.**

---

## Step 3 — Crosswalk and alignment docs (STOP after)

`standards/crosswalk.json`:

```json
{ "ap": "3.10", "ca": "9-12.AP.14", "strength": "strong|partial|related",
  "note": "<why they do or do not fully correspond>" }
```

Be honest about `strength`. A crosswalk that claims everything corresponds is useless; the
value is in seeing where one lesson earns credit twice and where the two frameworks
genuinely diverge.

Then generate:

**`alignment/standards_alignment.md`** — four views:
1. by chapter: what each chapter covers in both frameworks
2. by AP topic: coverage, carrier, chapters
3. by CA standard: coverage, carrier, chapters
4. gaps: anything `unassigned` in either framework

**`alignment/supplement-plan.md`** — what is taught outside this book and by what. Expected
division of labor, stated plainly so the boundary is legible rather than accidental:
- Working in Python carries AP Big Idea 3 almost entirely, Big Idea 1 partially, and CA's AP.12–22
  strand heavily
- partial on AP Big Idea 2 and CA's DA.8–11, via file and CSV work; not binary numbers or
  data compression
- not carried: AP Big Ideas 4 and 5, CA's NI and IC strands. A separate novel unit covers
  these.

**`alignment/glossary-map.md`** — **concept mapping, not string diffing.** The CED has no
glossary appendix; its vocabulary lives in Essential Knowledge prose and in the Exam
Reference Sheet's own naming. A string-level diff against Downey's `**term:** definition`
entries produces noise.

Lead with the table that actually costs students points:

| Working in Python | AP CSP |
|---|---|
| function | procedure |
| conditional | selection |
| `%` | `MOD` |
| `print` | `DISPLAY` |
| `input` | `INPUT` |
| `len(x)` | `LENGTH(x)` |
| `x.append(v)` | `APPEND(x, v)` |
| `=` assignment | `←` |
| `==` equality | `=` |
| 0-based index | **1-based index** |

Then: terms AP expects that Working in Python doesn't use (with a proposed carrier for each, many
of which are `little_brother`), and terms Working in Python uses that AP doesn't need (marked
`keep` or `defer`, recommended never deleted).

### The scope question

**Report this explicitly and prominently.** Do any California standards, particularly in the
AP.12–22 strand, require content that only chapters 14–19 provide, and that nothing else in
the course reaches? Abstraction, modularity, and program structure are the likely candidates.

If yes, chapters 14–19 are core rather than enrichment, and the treatment matrix in
`CLAUDE.md` needs revising to give them blank markers and live instruction time. That is a
teacher decision, but it turns on evidence you are the first to see. Do not decide it; state
it clearly enough that it can be decided.

---

## Step 4 — Standards inserts

One per chapter, in back matter, inside a `type="standards"` sentinel. All codes and weights
read from the JSON; nothing hardcoded. Under 200 words. Signposting, not a second textbook.

**Full form, chapters 1–13:**

```markdown
<!-- apcsp:begin type="standards" chapter="09" -->
---

## Standards alignment

**AP CSP:** [3.10 Lists](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.10), [3.2 Data Abstraction](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.2) — Big Idea 3, 30–35% of the exam
**California 9–12:** [9-12.AP.14](https://python.porttack.com/alignment/ca-cs-standards-reference.html#S-9-12.AP.14), [9-12.AP.16](https://python.porttack.com/alignment/ca-cs-standards-reference.html#S-9-12.AP.16)
**CSTA 2026:** [HS-PRO-PD-12](https://python.porttack.com/alignment/csta2026-standards-reference.html#T-HS-PRO-PD-12) <or: not carried — see the CSTA amendment above on legitimate gaps>
**CA CTE (ICT):** [C4.9](https://python.porttack.com/alignment/ca-ict-anchor-standards-reference.html#T-C4.9) <codes from either the Anchor Standards or Pathway C, whichever actually apply>

<One to three sentences of original prose connecting this chapter's Python to the way the
exam frames the same idea. Heavily weighted topics only; light ones get the headers alone.>

**Vocabulary:** this book says *function*; the exam says *procedure*.
**Indexing:** Python lists start at 0. Exam pseudocode lists start at 1.

**Covered elsewhere:** 5.6 Safe Computing and 9-12.IC.30 are carried by the novel unit.
<!-- apcsp:end -->
```

The leading `---` is a markdown rule, matching the one already used in this cell's `note`
sentinel — not a raw `<hr>` tag. None of the four framework labels is ever a link — link
each individual code citation to its own anchor instead: AP topics to `#T-<code>` on
`alignment/apcsp-standards-reference.html`; CA standards to `#S-<code>` on
`alignment/ca-cs-standards-reference.html`; CSTA standards to `#T-<code>` on
`alignment/csta2026-standards-reference.html`; CA CTE (ICT) codes to `#T-<code>` on
`alignment/ca-ict-anchor-standards-reference.html`. Codes in the order they're named. Leave
a line unlinked only when it cites no code — and for CSTA/ICT specifically, write "not
carried" rather than a link when that's genuinely the finding; don't force a match to avoid
an empty line.

**Short form, chapters 14–19:**

```markdown
<!-- apcsp:begin type="standards" chapter="15" -->
---

## Standards alignment

**AP CSP:** not assessed. Object-oriented programming is outside the AP CSP framework.
**California 9–12:** <codes, if any, each linked to its own `#S-<code>` anchor>
**CSTA 2026:** <codes, if any, each linked to its own `#T-<code>` anchor>
**CA CTE (ICT):** <codes, if any, each linked to its own `#T-<code>` anchor>

Included because <one line: on-ramp to AP CSA, CMU 15-111, or a CA standard nothing else
in the course reaches>.
<!-- apcsp:end -->
```

No label is ever linked (per the full-form note above); the **AP CSP** line here also cites
no code, so there is doubly nothing to link. If a chapter's California, CSTA, or ICT line
is also empty, leave that unlinked too.

Telling a student "this is not on the exam, and here is why we're doing it anyway" is better
information than silence.

Also backfill `targets_ap` and `targets_ca` in `data/exercise-ledger.json` for every
replacement exercise pass 2 wrote, then `make ledger`.

---

## Step 5 — Appendices

**`appendix/pseudocode-crosswalk.md`.** Likely the highest-value artifact in the fork:
roughly a third of multiple-choice items involve pseudocode, and the mismatches bite
students who *do* know Python. Verify every row against the Exam Reference Sheet in CED
Appendix 1. Side-by-side code pairs, not prose.

Cover the Step 3 vocabulary table plus:
- **1-based indexing**, led with, and out-of-range producing an error that terminates the
  program (AAP-1.D.8)
- `REPEAT n TIMES` vs `for _ in range(n)`
- `REPEAT UNTIL (cond)` vs `while`, noting the sense is **inverted**
- `FOR EACH item IN aList` vs `for item in aList`
- `NOT` / `AND` / `OR` vs `not` / `and` / `or`
- `RANDOM(a, b)` inclusive of both endpoints, matching `random.randint` and **not**
  `random.randrange`
- `REMOVE(aList, i)` shifts left, `INSERT(aList, i, value)` shifts right, both 1-based
- the robot-in-a-grid instruction set, which has no Python analogue and is taught separately

Close with a two-way translation exercise set, Python to pseudocode and back.

**`appendix/cs50p-map.md`.** Each chapter to the CS50P week whose problem set can serve as a
lab. Do not reorder chapters to fit. Note that CS50P sets from week 3 onward are steeper
than CSP requires and belong as differentiation rather than whole-class work. Identify the
four topics CS50P covers that Working in Python underweights: exceptions as a first-class topic,
pytest, command-line arguments, and APIs.

---

## Handoff

Append to `AUDIT.md`:

- both indexes: counts, and every `unassigned` standard in either framework
- crosswalk: how many `strong`, `partial`, `related`, and where the frameworks diverge
- **the scope question from Step 3, answered with evidence**
- any `class_periods` left null and why
- exclusion statements found beyond the two known ones
- what a future maintainer needs to know when the CED or the CA framework is revised