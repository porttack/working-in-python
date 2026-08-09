# AP CSP Vocabulary Coverage

**There is no official AP CSP glossary.** The Course and Exam Description has no glossary appendix of its own (see `alignment/glossary-map.md`); its vocabulary lives scattered across Essential Knowledge prose and the Exam Reference Sheet's own naming. The list below is *compiled*, not extracted, from three sources, and every gloss is written fresh in our own words — no third-party definition is reproduced:

- the official 2026 AP CSP **Exam Reference Sheet** (College Board), for the pseudocode instructions, operators, and Robot commands
- term names (not prose) from a community-compiled study list at [apcsexamprep.com](https://www.apcsexamprep.com/pages/ap-csp-vocabulary-list)
- term names (not prose) from Khan Academy's AP CSP vocabulary review page

This is best-effort, not authoritative — there is no ground truth to extract against. Treat gaps below as **candidates to check**, not confirmed absences.

**140 AP CSP terms compiled. 39 are taught in this book (directly or under a documented synonym), 26 have an established home elsewhere in the course, 48 are *Little Brother*'s territory, and 27 have no carrier yet.**

## The two sets, symbolically

```
   Working in Python vocabulary (~185 terms, ch. 1-18)
        ┌────────────────────────────┐
        │                            │
        │      ┌──────────────┐      │
        │      │  overlap:    │      │
        │      │   39 terms    │      │
        │      │  (function/  │      │
        │      │  procedure,  │      │
        │      │  list, loop, │      │
        │      │  MOD, ...)   │      │
        │      └──────────────┘      │
        │                            │
        └────────────────────────────┘
                        ┌──────────────────────────────┐
                        │  AP CSP vocabulary (~140 terms)  │
                        └──────────────────────────────┘
```

A literal Venn — every word plotted — would be illegible at this size (185 x 140 terms). The hosted `.html` twin draws the same two sets as a proportional two-circle diagram with the counts above; this `.md` version is the text equivalent for repo-local reading.

## Big Idea 1 — Creative Development (CRD)

19 terms — 7 in book, 3 planned, 0 Little Brother, 9 gap.

| AP CSP term | Status | Working in Python | Chapter | Note |
|---|---|---|---|---|
| **Algorithm** | gap | — | — | Used constantly in the book's own prose (“Developing Algorithms,” ch. 6-7) but never itself a glossary headword. |
| **Program** | gap | — | — | Same as Algorithm: everywhere, but Downey never defines the word itself. |
| **Code Segment** | gap | — | — | Exam-format vocabulary with no real analog outside the exam. |
| **Computing Innovation** | planned | — | — | Create Performance Task (see glossary-map.md). |
| **Collaboration** | planned | — | — | Lab pair work + Create PT, not a standalone lesson. |
| **Pair Programming** | planned | — | — | Create PT / classroom practice, not book content. |
| **Program Documentation** | in book | docstring | 4 | Python's realization of this idea; the word itself is Python-specific. |
| **Comments** | in book | comment | 2 |  |
| **Syntax Error** | in book | syntax error | 1 |  |
| **Logic Error** | in book | semantic error | 2 | Same idea, different name — see the swap table. |
| **Run-time Error** | in book | runtime error | 2 |  |
| **Overflow Error** | gap | — | — | Python's integers have arbitrary precision, so this error class structurally doesn't arise in the language the book teaches. |
| **Testing** | in book | test discovery | 18 | Also ch. 7's pass/fail vocabulary; the word “testing” itself isn't a headword. |
| **Test Cases** | gap | — | — | The practice exists in exercises; the term is never named. |
| **Hand Tracing** | gap | — | — | A notebook-first book has no reason to teach this as its own skill; matches Practice P4's gap in ap-practices-bigideas-coverage.html. |
| **Iterative Development Process** | gap | — | — | Distinct from Incremental Development, which the book does name (see below). |
| **Incremental Development Process** | in book | incremental development | 6 |  |
| **Event** | gap | — | — | Already flagged in glossary-map.md as a real, unassigned gap. |
| **Event-Driven Programming** | gap | — | — | Every program in this book runs top to bottom; no event loop anywhere. |

## Big Idea 2 — Data (DAT)

23 terms — 2 in book, 15 planned, 0 Little Brother, 6 gap.

| AP CSP term | Status | Working in Python | Chapter | Note |
|---|---|---|---|---|
| **Binary** | planned | — | — | CS50T Multimedia (extending the existing bit/byte plan). |
| **Bit** | planned | — | — | CS50T Multimedia. |
| **Byte** | planned | — | — | CS50T Multimedia. |
| **Decimal** | planned | — | — | CS50T Multimedia. |
| **Hexadecimal** | planned | — | — | CS50T Multimedia. |
| **Abstraction** | in book | encapsulation / generalization | 4, 9, 10, 11 | Data abstraction specifically is AP topic 3.2; see the coverage map. |
| **Analog Data** | planned | — | — | CS50T Multimedia. |
| **Digital Data** | planned | — | — | CS50T Multimedia. |
| **Sampling** | planned | — | — | CS50T Multimedia. |
| **Lossless Data Compression** | planned | — | — | CS50T Multimedia (extending the existing plan). |
| **Lossy Data Compression** | planned | — | — | CS50T Multimedia. |
| **Metadata** | gap | — | — | Already flagged in ap-practices-bigideas-coverage.html as uncarried under topic 2.3. |
| **Data** | gap | — | — | Used constantly as a plain word (“configuration data,” ch. 13); never its own headword. |
| **Information** | gap | — | — |  |
| **Data Set** | gap | — | — |  |
| **Correlation** | gap | — | — |  |
| **Data Cleaning** | gap | — | — |  |
| **Data Filtering** | in book | filtering | 10 |  |
| **ASCII** | planned | — | — | CS50T Multimedia. |
| **Unicode** | planned | — | — | CS50T Multimedia. |
| **RGB** | planned | — | — | CS50T Multimedia. |
| **Pixel** | planned | — | — | CS50T Multimedia. |
| **Roundoff Error** | planned | — | — | CS50T Multimedia. |

## Big Idea 3 — Algorithms and Programming (AAP)

50 terms — 30 in book, 8 planned, 0 Little Brother, 12 gap.

| AP CSP term | Status | Working in Python | Chapter | Note |
|---|---|---|---|---|
| **Variable** | in book | variable | 2 |  |
| **Constant** | gap | — | — | Python has no language-level constant; not taught as its own idea. |
| **Data Type** | in book | type | 1 |  |
| **Integer** | in book | integer | 1 |  |
| **String** | in book | string | 1 |  |
| **Boolean** | in book | boolean expression | 5 |  |
| **List** | in book | list | 9 |  |
| **Index** | in book | index | 8 | 0-based here; the exam's own notation is 1-based — see the swap table in glossary-map.md. |
| **Expression** | in book | expression | 1 |  |
| **Assignment** | in book | assignment statement | 2 | `=` here; `←` on the exam reference sheet. |
| **Sequencing** | gap | — | — | The default behavior of every program in the book; never named as its own concept. |
| **Selection** | in book | conditional statement | 5 | The single biggest name swap between this book and the exam — see glossary-map.md. |
| **Iteration** | in book | loop | 3, 7 | Definite iteration (`for`) only — this book has no `while` loop at all, so indefinite iteration (REPEAT UNTIL, below) is a real gap even though Iteration itself is covered. |
| **Procedure** | in book | function | 1 | The exam's word for what this book calls a function. |
| **Parameter** | in book | parameter | 3 |  |
| **Argument** | in book | argument | 2 |  |
| **RETURN Statement** | in book | return value | 6 |  |
| **Procedural Abstraction** | in book | interface design | 4 |  |
| **Modularity** | gap | — | — | encapsulation/generalization (ch. 4) are adjacent, but “modularity” itself is never named. |
| **Software Library** | in book | module | 2 |  |
| **API** | gap | — | — |  |
| **Relational Operators** | in book | relational operator | 5 |  |
| **Logical Operators** | in book | logical operator | 5 |  |
| **MOD** | in book | modulus operator | 5 | `%` here; `MOD` on the exam reference sheet. |
| **Nested Conditionals** | in book | nested conditional | 5 |  |
| **Infinite Loop** | gap | — | — | “Infinite recursion” (ch. 5) is the book's only named version of this idea; the iterative case is never named. |
| **Linear Search** | in book | linear search | 7 |  |
| **Binary Search** | planned | — | — | November algorithms block; linear search is already taught, so this is a direct next step. |
| **RANDOM** | in book | pseudorandom | 12 | Python's `random` module, first used in ch. 12. |
| **Simulation** | planned | — | — | November algorithms block. |
| **Algorithmic Efficiency** | planned | — | — | November algorithms block. |
| **Reasonable Time** | planned | — | — | November algorithms block. |
| **Unreasonable Time** | planned | — | — | November algorithms block. |
| **Heuristic** | planned | — | — | November algorithms block. |
| **Decidable Problem** | planned | — | — | November algorithms block. |
| **Undecidable Problem** | planned | — | — | November algorithms block. |
| **Traversal** | gap | — | — | The book's single most common activity, but never named as its own term — “loop variable” (ch. 7) and “element” (ch. 9) are the closest adjacent headwords. |
| **DISPLAY** | in book | print() | 1 | Used from the very first function-call example; not itself a glossary headword. |
| **INPUT** | in book | input() | 5 | First used in ch. 5's code, verified directly against the notebooks. |
| **REPEAT n TIMES** | in book | for loop | 3 |  |
| **REPEAT UNTIL** | gap | — | — | This book has no `while` loop anywhere — the single largest gap flagged in ap-practices-bigideas-coverage.html, and it lands here too. |
| **INSERT** | gap | — | — | Verified directly: `.insert(` never appears in any chapter's code. |
| **APPEND** | in book | .append() | 9 | First used in ch. 5's code; formalized as a list operation in ch. 9. |
| **REMOVE** | in book | .remove() | 9 |  |
| **LENGTH** | in book | len() | 1, 9 | Used on strings from ch. 1; formalized for lists in ch. 9. |
| **FOR EACH** | in book | for x in list | 7 |  |
| **MOVE_FORWARD** | gap | — | — | The book's turtle module (first used ch. 4) draws shapes rather than navigating a grid — a loose analog, not a match. |
| **ROTATE_LEFT** | gap | — | — |  |
| **ROTATE_RIGHT** | gap | — | — |  |
| **CAN_MOVE** | gap | — | — |  |

## Big Idea 4 — Computer Systems and Networks (CSN)

22 terms — 0 in book, 0 planned, 22 Little Brother, 0 gap.

| AP CSP term | Status | Working in Python | Chapter | Note |
|---|---|---|---|---|
| **Internet** | Little Brother | — | — |  |
| **World Wide Web** | Little Brother | — | — |  |
| **Computer Network** | Little Brother | — | — |  |
| **Computing Device** | Little Brother | — | — |  |
| **Packet** | Little Brother | — | — |  |
| **Routing** | Little Brother | — | — |  |
| **Bandwidth** | Little Brother | — | — |  |
| **Protocol** | Little Brother | — | — |  |
| **TCP** | Little Brother | — | — |  |
| **IP** | Little Brother | — | — |  |
| **IP Address** | Little Brother | — | — |  |
| **UDP** | Little Brother | — | — |  |
| **HTTP/HTTPS** | Little Brother | — | — |  |
| **DNS** | Little Brother | — | — |  |
| **Router** | Little Brother | — | — |  |
| **Scalability** | Little Brother | — | — |  |
| **Fault Tolerance** | Little Brother | — | — |  |
| **Redundancy** | Little Brother | — | — |  |
| **Sequential Computing** | Little Brother | — | — |  |
| **Parallel Computing** | Little Brother | — | — |  |
| **Distributed Computing** | Little Brother | — | — |  |
| **Speedup** | Little Brother | — | — |  |

## Big Idea 5 — Impact of Computing (IOC)

26 terms — 0 in book, 0 planned, 26 Little Brother, 0 gap.

| AP CSP term | Status | Working in Python | Chapter | Note |
|---|---|---|---|---|
| **Digital Divide** | Little Brother | — | — |  |
| **Bias** | Little Brother | — | — |  |
| **Crowdsourcing** | Little Brother | — | — |  |
| **Citizen Science** | Little Brother | — | — |  |
| **Machine Learning** | Little Brother | — | — |  |
| **Data Mining** | Little Brother | — | — |  |
| **Intellectual Property** | Little Brother | — | — |  |
| **Copyright** | Little Brother | — | — |  |
| **Creative Commons** | Little Brother | — | — |  |
| **Open Source** | Little Brother | — | — |  |
| **Open Access** | Little Brother | — | — |  |
| **Plagiarism** | Little Brother | — | — |  |
| **Personally Identifiable Information** | Little Brother | — | — |  |
| **Encryption** | Little Brother | — | — |  |
| **Symmetric Key Encryption** | Little Brother | — | — |  |
| **Public Key Encryption** | Little Brother | — | — |  |
| **Authentication** | Little Brother | — | — |  |
| **Multifactor Authentication** | Little Brother | — | — |  |
| **Phishing** | Little Brother | — | — |  |
| **Malware** | Little Brother | — | — |  |
| **Computer Virus** | Little Brother | — | — |  |
| **Keylogging** | Little Brother | — | — |  |
| **Rogue Access Point** | Little Brother | — | — |  |
| **Cookies** | Little Brother | — | — |  |
| **Digital Certificate** | Little Brother | — | — |  |
| **Certificate Authority** | Little Brother | — | — |  |

## Methodology notes, explicitly

- `planned` for Big Idea 2's encoding cluster (ASCII, Unicode, RGB, pixel, decimal, hexadecimal, analog/digital data, sampling, roundoff error) extends the already-stated CS50T Multimedia plan for bit/byte/compression (see `glossary-map.md`) to the rest of that same topic cluster — a reasonable inference made in this pass, not something previously logged. Confirm CS50T Multimedia actually reaches all of these before relying on it.
- Big Ideas 4 and 5 are marked `else` (*Little Brother*) uniformly, matching the topic-level call already made in `ap-practices-bigideas-coverage.html`.
- "in book" includes documented synonyms (procedure/function, selection/conditional, etc.) from `glossary-map.md`'s swap table, not just exact name matches.
- `.insert()`, `while`, and Robot-style grid navigation were checked directly against the notebooks' code cells this session, not assumed.

