# Standards Alignment

Generated from `standards/apcsp.json`, `standards/castandards.json`, and
`standards/crosswalk.json`. Four views: by chapter, by AP topic, by CA standard, and gaps.
Regenerate this file by hand whenever those three JSON files change; there is no build
script for it yet.

**The scope question, answered up front:** see the "Scope question" section at the bottom
before reading the rest. Short answer: no, chapters 14–19 are not required for anything in
either framework's core 9–12 content. Chapters 1–13 are sufficient.

---

## View 1 — By chapter

Only chapters 1–13 appear; chapters 14–19 (classes, independent-study range) carry no AP
or CA content under either standard as currently written. `jupyter_intro` and `chap00`
(Preface) carry none either.

| Chapter | AP CSP topics | CA standards |
|---|---|---|
| 1. Welcome | 1.2 Program Function and Purpose (partial), 1.4 Identifying and Correcting Errors, 3.3 Mathematical Expressions, 3.4 Strings | — |
| 2. Variables and Statements | 1.4, 3.1 Variables and Assignments, 3.3 Mathematical Expressions, 3.14 Libraries (`import`) | AP.17 |
| 3. Functions | 1.4, 3.8 Iteration (`for`, partial — see gaps), 3.12 Calling Procedures, 3.13 Developing Procedures | AP.16 |
| 4. Functions and Interfaces | 1.3 Program Design and Development, 1.4, 3.13 Developing Procedures, 3.14 Libraries (jupyturtle) | AP.16, AP.17, AP.20, AP.22 |
| 5. Conditionals and Recursion | 1.2 (partial, keyboard input), 1.4, 3.5 Boolean Expressions, 3.6 Conditionals, 3.7 Nested Conditionals | AP.14 |
| 6. Return Values | 1.4, 3.9 Developing Algorithms (incremental development), 3.12 Calling Procedures | AP.14 |
| 7. Iteration and Search | 1.4, 3.8 Iteration (partial), 3.9 Developing Algorithms (linear search) | AP.12, AP.20 |
| 8. Strings and Regular Expressions | 1.4, 3.4 Strings, 3.14 Libraries (`re`) | AP.17 |
| 9. Lists | 1.4, 3.2 Data Abstraction, 3.10 Lists | AP.12 (partial, sort), AP.13 |
| 10. Dictionaries | 1.4, 3.2 Data Abstraction | — |
| 11. Tuples | 1.4, 3.2 Data Abstraction | — |
| 12. Text Analysis and Generation | 1.4, 2.3 Extracting Information from Data, 2.4 Using Programs with Data, 3.15 Random Values | — |
| 13. Files and Databases | 1.4, 2.3, 2.4 | — |
| 14–19. Classes and Objects, Inheritance, Python Extras, Final thoughts | none | none |

Notes:
- **1.4 (Identifying and Correcting Errors)** appears in every row 1–13 because every
  chapter carries a "Debugging" section — see the AP index for this finding.
- **Chapters 14–19 carrying nothing is expected, not a gap.** Object-oriented programming
  is outside the AP CSP framework entirely, and no CA 9–12 core standard requires it
  specifically (see "Scope question" below) — every CA standard this book satisfies is
  already satisfied by chapters 1–13 alone.

---

## View 2 — By AP CSP topic

Full coverage, carrier, and chapters, from `standards/apcsp.json`. Topics with
`carrier: supplement` show where they're actually taught, per direction given for this
pass.

| Topic | Title | Carrier | Chapters | Note |
|---|---|---|---|---|
| 1.1 | Collaboration | supplement | — | Lab pair work + Create Performance Task, continuous |
| 1.2 | Program Function and Purpose | working_in_python | 1, 5 | partial — no event-driven programming |
| 1.3 | Program Design and Development | working_in_python | 4 | CRD-2.H (crediting others' code) uncarried |
| 1.4 | Identifying and Correcting Errors | working_in_python | 1–13 | every chapter's Debugging section |
| 2.1 | Binary Numbers | unassigned | — | real gap — CS50T Multimedia dropped 2026-08-09, not taught since year one; Pico I2C chapter is a partial, non-closing touchpoint (hex/byte notation) |
| 2.2 | Data Compression | unassigned | — | real gap — CS50T Multimedia dropped 2026-08-09, same reason; no replacement identified |
| 2.3 | Extracting Information from Data | working_in_python | 12, 13 | |
| 2.4 | Using Programs with Data | working_in_python | 12, 13 | |
| 3.1 | Variables and Assignments | working_in_python | 2 | |
| 3.2 | Data Abstraction | working_in_python | 9, 10, 11 | |
| 3.3 | Mathematical Expressions | working_in_python | 1, 2 | |
| 3.4 | Strings | working_in_python | 1, 8 | |
| 3.5 | Boolean Expressions | working_in_python | 5 | |
| 3.6 | Conditionals | working_in_python | 5 | |
| 3.7 | Nested Conditionals | working_in_python | 5 | |
| 3.8 | Iteration | working_in_python | 3, 7 | partial — **no `while` loop anywhere in the book** |
| 3.9 | Developing Algorithms | working_in_python | 6, 7 | |
| 3.10 | Lists | working_in_python | 9 | |
| 3.11 | Binary Search | supplement | — | November algorithms block |
| 3.12 | Calling Procedures | working_in_python | 3, 6 | |
| 3.13 | Developing Procedures | working_in_python | 3, 4 | |
| 3.14 | Libraries | working_in_python | 2, 4, 8 | |
| 3.15 | Random Values | working_in_python | 12 | |
| 3.16 | Simulations | supplement | — | November algorithms block |
| 3.17 | Algorithmic Efficiency | supplement | — | November algorithms block |
| 3.18 | Undecidable Problems | supplement | — | November algorithms block |
| 4.1–4.3 | Computer Systems and Networks (all 3) | little_brother | — | |
| 5.1–5.6 | Impact of Computing (all 6) | little_brother | — | |

---

## View 3 — By CA standard

From `standards/castandards.json`.

| Standard | Strand | Carrier | Chapters | Note |
|---|---|---|---|---|
| 9-12.CS.1 | Computing Systems | unassigned | — | hardware abstraction, no carrier in either framework |
| 9-12.CS.2 | Computing Systems | unassigned | — | hardware/software layers, same status |
| 9-12.CS.3 | Computing Systems | unassigned | — | troubleshooting — distinct skill from AP 1.4's code debugging, not the same standard |
| 9-12.NI.4 | Networks & the Internet | little_brother | — | |
| 9-12.NI.5 | Networks & the Internet | little_brother | — | |
| 9-12.NI.6 | Networks & the Internet | little_brother | — | |
| 9-12.NI.7 | Networks & the Internet | little_brother | — | |
| 9-12.DA.8 | Data & Analysis | unassigned | — | real gap — CS50T Multimedia dropped 2026-08-09, not taught since year one; Pico I2C chapter is a partial, non-closing touchpoint |
| 9-12.DA.9 | Data & Analysis | unassigned | — | real gap — CS50T Multimedia dropped 2026-08-09, same reason; scope is broader than compression alone anyway |
| 9-12.DA.10 | Data & Analysis | unassigned | — | data visualization — no plotting/charting anywhere in the book |
| 9-12.DA.11 | Data & Analysis | unassigned | — | validating a model against real data |
| 9-12.AP.12 | Algorithms & Programming | working_in_python | 7, 9 | |
| 9-12.AP.13 | Algorithms & Programming | working_in_python | 9 | |
| 9-12.AP.14 | Algorithms & Programming | working_in_python | 5, 6 | recursive half strong, iterative half thin (no `while`) |
| 9-12.AP.15 | Algorithms & Programming | unassigned | — | event-driven/GUI programming, none in the book |
| 9-12.AP.16 | Algorithms & Programming | working_in_python | 3, 4 | satisfied by procedures alone — see scope question |
| 9-12.AP.17 | Algorithms & Programming | working_in_python | 2, 4, 8 | |
| 9-12.AP.18 | Algorithms & Programming | unassigned | — | audience feedback in design, none in the book |
| 9-12.AP.19 | Algorithms & Programming | unassigned | — | license limitations — same gap as AP CRD-2.H |
| 9-12.AP.20 | Algorithms & Programming | working_in_python | 4, 7 | usability/accessibility clauses uncarried |
| 9-12.AP.21 | Algorithms & Programming | supplement | — | lab pair work + Create Performance Task |
| 9-12.AP.22 | Algorithms & Programming | working_in_python | 4 | presentation/graphics forms uncarried |
| 9-12.IC.23–30 | Impacts of Computing (all 8) | little_brother | — | |

---

## View 4 — Gaps

### Unassigned in the AP framework (2 topics, newly opened 2026-08-09)
- **2.1 Binary Numbers, 2.2 Data Compression** — both were carried by CS50T Multimedia as
  of this pass's original writing. Removed per teacher confirmation that CS50T hasn't
  actually been taught since year one, so the assignment was stale, not real coverage.
  The Pico/MicroPython unit's I2C chapter (source/rpi-pico-2e ch.14) teaches hexadecimal
  as compact byte notation for device addresses — a partial, authentic touchpoint for 2.1
  — but doesn't walk through binary place-value or binary<->decimal conversion, and
  doesn't touch compression at all, so neither topic is closed. No replacement identified
  for either as of this note.

### Unassigned in the CA framework (10 standards, no carrier yet)
- **9-12.DA.8, 9-12.DA.9** — same removal as AP 2.1/2.2 above (both were routed to the same
  stale CS50T Multimedia assignment); see that note for the Pico partial-touchpoint detail.
- **9-12.CS.1, 9-12.CS.2** — hardware/computing-systems abstraction. Neither this book nor
  Little Brother covers computer hardware internals. No plausible carrier identified.
- **9-12.CS.3** — troubleshooting. Deliberately kept separate from AP CRD-1.4 (see the
  crosswalk); this book's Debugging sections don't satisfy it.
- **9-12.DA.10** — data visualization. No plotting/charting library or content anywhere in
  chapters 1–13.
- **9-12.DA.11** — refining a computational model against real-world data. chap12's Markov
  model is adjacent but the chapter never validates it against real data.
- **9-12.AP.15** — event-driven/GUI programming. Every program in the book runs
  top-to-bottom; there is no event loop anywhere.
- **9-12.AP.18** — design incorporating feedback from a broad audience of users. chap04's
  development plan is solo and technical, never audience-facing.
- **9-12.AP.19** — software license limitations. Same underlying gap as AP CRD-2.H (see
  crosswalk); the book uses libraries but never discusses licensing them.

### CA standards with no AP CSP counterpart at all
Not "unassigned" so much as "the two frameworks don't even ask the same question" —
worth distinguishing from the list above:
- **9-12.CS.1, 9-12.CS.2** (hardware/systems layers) — AP CSP dropped hardware-internals
  content from its own framework; there's no AP topic to even crosswalk against.
- **9-12.DA.10** (data visualization) — AP CSP's DAT strand asks students to *extract*
  information from data, never to *visualize* it. No AP counterpart exists.

### AP CSP topics with no CA counterpart at all
- **3.18 Undecidable Problems** — CA's 9–12 core standards don't test decidability theory.
- **4.3 Parallel and Distributed Computing** — no dedicated CA 9–12 core standard for this
  (it may exist in the separate 9-12 Specialty set, which is out of scope for this index).
- **5.2 Digital Divide, 5.4 Crowdsourcing** — both Little Brother's territory regardless,
  and neither has a precise, dedicated match among the 8 IC standards indexed here.

### The load-bearing finding that isn't a "gap" in either framework by itself
**AP topic 3.8 / CA AP.14 (iteration and control-structure choice):** this book has **no
`while` loop anywhere**, confirmed by scanning every code cell in chapters 1–13.
Indefinite iteration is taught only through recursion. Both frameworks' pseudocode/
comparison expectations (`REPEAT UNTIL` on the AP side; recursive-vs-iterative Fibonacci
on the CA side) assume the student has seen a real condition-controlled loop. This
shows up as "working_in_python, partial" rather than "unassigned" in both indexes, which is
accurate but risks being read past — flagging it here too since it's the single most
consequential coverage question this pass surfaced.

---

## Scope question (Step 3, as instructed: state the evidence, not the decision)

**Question:** do any California 9–12 standards, particularly in the AP.12–22 strand,
require content that only chapters 14–19 (classes/OOP) provide, and that nothing else in
the course reaches? If so, chapters 14–19 would need to move from enrichment to core,
with blank markers and live instruction time, per the treatment matrix in `CLAUDE.md`.

**Evidence:** No. The two CA standards that mention class-like constructs both phrase
them as one option among several, not a requirement:

- **9-12.AP.16**: "...using constructs such as procedures, modules, **and/or** classes."
- **9-12.AP.17** ("modular design"): its own descriptive statement says students should
  "create computational artifacts with interacting procedures, modules, **and/or**
  libraries" — again, classes are not named as mandatory.

Both standards are already carried by chapters 3, 4, 2, and 8 (procedures and libraries)
with no need for chapters 14–19. Checked View 1 above to confirm: chapters 14–19 carry
zero AP or CA topics under the current mapping, and nothing in either framework's
30-standard CA core or 35-topic AP index changes that — every standard this book carries
is fully satisfiable through chapter 13.

**Conclusion stated, not decided:** on the evidence gathered in this pass, chapters
14–19 are enrichment, not core, for standards-coverage purposes. The treatment matrix in
`CLAUDE.md` does not need revising on standards grounds. (There may be other, non-standards
reasons to teach OOP earlier — that's a separate call this pass doesn't weigh in on.)
