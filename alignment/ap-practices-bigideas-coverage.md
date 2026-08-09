# AP CSP Coverage — Practices, Big Ideas, and Topics

Reorganizes `standards/apcsp.json` around the exam's own structure — the 6 Computational
Thinking Practices, then the 5 Big Ideas and every topic (sub-item) inside each — so
coverage can be read top-down the way the CED is organized, rather than by chapter. AP CSP
only; for California/CSTA/ICT coverage see `alignment/standards_alignment.md`. Chapters
14–19 carry no AP CSP content (confirmed in `standards_alignment.md` View 1) and are
omitted from the tables below.

Chapter links point at the source notebooks in `chapters/`. Topic codes link to this
project's own hosted reference page, per the linking convention in
`mods/pass-3-alignment.md` (never the College Board's own text).

---

## Practices

The CED weights these across the whole MCQ section regardless of which Big Idea a
question happens to test. They're skills, not content, so "coverage" here means something
different from the topic tables below: does the book's *activity* — what a student
actually does, chapter after chapter — build the skill.

| Practice | MCQ weight | What it asks a student to do | Built by this book? |
|---|---|---|---|
| [P1](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-P1) Computational Solution Design | 18–25% | Choosing procedures, data structures, and program structure to fit a problem before writing code. | **Strong.** chap04's development-plan section models this directly; the choice between list/dict/tuple in chap09–11 is this skill applied concretely. |
| [P2](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-P2) Algorithms and Program Development | 20–28% | Writing, completing, and modifying code — expressions, conditionals, iteration, procedures. | **Strong.** This is most of what the book's exercises are, chapters 1–13. |
| [P3](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-P3) Abstraction in Program Development | 7–12% | Using functions and data abstraction to manage complexity instead of repeating or inlining everything. | **Strong.** Functions from chap03 on; lists/dicts/tuples as abstraction in chap09–11. |
| [P4](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-P4) Code Analysis | 12–19% | Reading code someone else wrote, tracing execution, predicting output, locating an error — without writing new code from scratch. | **Partial.** Every chapter's Debugging section builds the mindset, and chap07's doctest work is close, but the book rarely gives a finished snippet and asks "what does this print" or "where's the bug" the way MCQ trace questions do — its exercises default to write-new-code, not read-and-predict. **Coding-relevant gap** — see below. |
| [P5](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-P5) Computing Innovations | 28–33% | Analyzing a computing innovation's purpose, data use, and effects — reading and writing about impact, not code. | **Not carried here, by design.** This is Big Idea 5's practice; it's [`little_brother`](https://porttack.com/2026/06/14/little-brother.html)'s job (see Big Idea 5 below), not a coding skill. |
| [P6](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-P6) Responsible Computing | not MCQ-weighted (Create PT only) | Licensing, accessibility, and crediting sources inside a student's own project. | **Mostly not carried**, but one piece of this — crediting code taken from elsewhere — *is* a coding habit, not an impact-of-computing topic, and it has no counterpart anywhere in the book (`apcsp.json` topic 1.3's note). **Coding-relevant gap** — see below. |

---

## Big Ideas and their topics

### Big Idea 1 — Creative Development (CRD), 10–13% of MCQ

| Topic | Title | Carrier | Chapters | Note |
|---|---|---|---|---|
| [1.1](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-1.1) | Collaboration | supplement | — | Lab pair work + Create PT, not a standalone lesson |
| [1.2](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-1.2) | Program Function and Purpose | working_in_python | [1](../chapters/chap01.ipynb), [5](../chapters/chap05.ipynb) | partial — no event-driven programming anywhere |
| [1.3](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-1.3) | Program Design and Development | working_in_python | [4](../chapters/chap04.ipynb) | crediting others' code (CRD-2.H) uncarried |
| [1.4](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-1.4) | Identifying and Correcting Errors | working_in_python | [1](../chapters/chap01.ipynb)–[13](../chapters/chap13.ipynb) | every chapter's Debugging section |

### Big Idea 2 — Data (DAT), 17–22% of MCQ

| Topic | Title | Carrier | Chapters | Note |
|---|---|---|---|---|
| [2.1](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-2.1) | Binary Numbers | supplement | — | CS50T Multimedia |
| [2.2](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-2.2) | Data Compression | supplement | — | CS50T Multimedia |
| [2.3](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-2.3) | Extracting Information from Data | working_in_python | [12](../chapters/chap12.ipynb), [13](../chapters/chap13.ipynb) | metadata specifically uncarried |
| [2.4](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-2.4) | Using Programs with Data | working_in_python | [12](../chapters/chap12.ipynb), [13](../chapters/chap13.ipynb) | file/YAML/shelve work |

### Big Idea 3 — Algorithms and Programming (AAP), 30–35% of MCQ

The book's core, and the exam's biggest single Big Idea.

| Topic | Title | Carrier | Chapters | Note |
|---|---|---|---|---|
| [3.1](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.1) | Variables and Assignments | working_in_python | [2](../chapters/chap02.ipynb) | |
| [3.2](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.2) | Data Abstraction | working_in_python | [9](../chapters/chap09.ipynb), [10](../chapters/chap10.ipynb), [11](../chapters/chap11.ipynb) | |
| [3.3](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.3) | Mathematical Expressions | working_in_python | [1](../chapters/chap01.ipynb), [2](../chapters/chap02.ipynb) | |
| [3.4](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.4) | Strings | working_in_python | [1](../chapters/chap01.ipynb), [8](../chapters/chap08.ipynb) | |
| [3.5](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.5) | Boolean Expressions | working_in_python | [5](../chapters/chap05.ipynb) | |
| [3.6](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.6) | Conditionals | working_in_python | [5](../chapters/chap05.ipynb) | |
| [3.7](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.7) | Nested Conditionals | working_in_python | [5](../chapters/chap05.ipynb) | |
| [3.8](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.8) | Iteration | working_in_python | [3](../chapters/chap03.ipynb), [7](../chapters/chap07.ipynb) | **no `while` loop anywhere in the book** — see below |
| [3.9](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.9) | Developing Algorithms | working_in_python | [6](../chapters/chap06.ipynb), [7](../chapters/chap07.ipynb) | incremental development, linear search |
| [3.10](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.10) | Lists | working_in_python | [9](../chapters/chap09.ipynb) | |
| [3.11](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.11) | Binary Search | supplement | — | linear search is taught; binary search never introduced, even conceptually |
| [3.12](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.12) | Calling Procedures | working_in_python | [3](../chapters/chap03.ipynb), [6](../chapters/chap06.ipynb) | |
| [3.13](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.13) | Developing Procedures | working_in_python | [3](../chapters/chap03.ipynb), [4](../chapters/chap04.ipynb) | |
| [3.14](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.14) | Libraries | working_in_python | [2](../chapters/chap02.ipynb), [4](../chapters/chap04.ipynb), [8](../chapters/chap08.ipynb) | |
| [3.15](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.15) | Random Values | working_in_python | [12](../chapters/chap12.ipynb) | |
| [3.16](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.16) | Simulations | supplement | — | no simulation content in chapters 1–13 |
| [3.17](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.17) | Algorithmic Efficiency | supplement | — | no informal efficiency discussion anywhere |
| [3.18](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-3.18) | Undecidable Problems | supplement | — | not carried; conceptual, non-programming topic |

### Big Idea 4 — Computer Systems and Networks (CSN), 11–15% of MCQ

| Topic | Title | Carrier |
|---|---|---|
| [4.1](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-4.1) | The Internet | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |
| [4.2](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-4.2) | Fault Tolerance | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |
| [4.3](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-4.3) | Parallel and Distributed Computing | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |

### Big Idea 5 — Impact of Computing (IOC), 21–26% of MCQ

| Topic | Title | Carrier |
|---|---|---|
| [5.1](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-5.1) | Beneficial and Harmful Effects | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |
| [5.2](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-5.2) | Digital Divide | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |
| [5.3](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-5.3) | Computing Bias | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |
| [5.4](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-5.4) | Crowdsourcing | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |
| [5.5](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-5.5) | Legal and Ethical Concerns | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |
| [5.6](https://python.porttack.com/alignment/apcsp-standards-reference.html#T-5.6) | Safe Computing | [little_brother](https://porttack.com/2026/06/14/little-brother.html) |

Big Ideas 4 and 5 carry zero topics in this book, entirely by design — that division of
labor is stated in `alignment/supplement-plan.md`, not a finding of this document.

---

## What isn't covered, ranked by relevance to coding

35 topics total: 19 `working_in_python` (54%), 7 `supplement` (20%, planned for the
November algorithms block or CS50T but not currently in the book itself), 9
[`little_brother`](https://porttack.com/2026/06/14/little-brother.html) (26%, all of Big Ideas 4–5). The split below separates gaps that are
about writing or reading code from gaps that are about computing's effects on the world —
the second kind is expected and already covered elsewhere; the first kind is the one worth
watching.

### Coding-related gaps (worth tracking)

1. **No `while` loop anywhere in the book (3.8 / AAP-2.K).** The single most consequential
   finding in this whole index — also flagged in `standards_alignment.md`. Indefinite
   iteration is taught only through recursion (chap05, chap06). Conceptually related, but
   it isn't the same pseudocode construct the exam tests, and it can't produce the
   `REPEAT UNTIL`-specific edge cases (infinite loop from a condition that never flips;
   zero-iteration when the condition already holds) that the CED calls out by name.
2. **Crediting code taken from another source (1.3 / CRD-2.H, and the matching CA gap
   AP.19).** Not an abstract ethics topic — it's a habit a student needs while actually
   writing code, and nothing in the book models it.
3. **Code Analysis as an exercise format (Practice P4).** The book's exercises default to
   "write a function that…" rather than "here's a snippet — what does it print, or where's
   the bug." Debugging sections build the mindset; they don't drill the trace-and-predict
   format the MCQ actually uses.
4. **Event-driven programs (part of 1.2 / CRD-2.C.5–6).** Every program in the book runs
   top to bottom; there's no event loop or callback anywhere.
5. **Binary search, simulations, algorithmic efficiency, undecidable problems (3.11,
   3.16–3.18).** All four are `supplement` — planned for the November algorithms block, not
   absent by design, but not yet present in the book as written. Linear search is taught
   (chap07) so 3.11 in particular is a direct, nameable next step rather than a cold start.

### Not coding-related, carried elsewhere (lower priority for this book)

- Binary numbers and data compression (2.1–2.2) — CS50T Multimedia.
- Everything in Big Ideas 4 and 5, and Practice P5 — [`little_brother`](https://porttack.com/2026/06/14/little-brother.html)'s territory, per
  `supplement-plan.md`. Not a gap in this book; a different book's job.

---

*Sourced from `standards/apcsp.json` (2026-07-30 extraction) and cross-checked against
`alignment/standards_alignment.md` View 2. Regenerate by hand if either changes — no build
script for this file yet, same as the other `alignment/*.md` docs.*
