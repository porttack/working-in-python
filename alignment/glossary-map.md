# Glossary Map

Concept mapping, not string diffing. The CED has no glossary appendix of its own — its
vocabulary lives in Essential Knowledge prose and the Exam Reference Sheet's naming — so a
literal diff against Downey's `**term:** definition` entries would be mostly noise. This
maps concepts instead.

**A literal, word-by-word version of that diff was built anyway on 2026-08-09**, on
maintainer request — `alignment/vocabulary-by-chapter.md` (every Downey glossary term, by
chapter) and `alignment/ap-vocabulary-coverage.md` (a *compiled*, not extracted, AP CSP
vocabulary list — see its methodology note — matched term by term against the book). The
two documents complement each other: this one explains *why* a term does or doesn't need
to transfer; that one just says whether the word appears. Hosted twins:
[`vocabulary-by-chapter.html`](https://python.porttack.com/alignment/vocabulary-by-chapter.html)
and
[`ap-vocabulary-coverage.html`](https://python.porttack.com/alignment/ap-vocabulary-coverage.html).

## The table that actually costs students points

Same term, different name. These are the substitutions most likely to cost a point on an
exam question that's otherwise easy — a student who knows the Python cold but hasn't
mapped it onto the exam's own words.

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

The last row is the single biggest source of off-by-one errors on multiple-choice
questions: every Python list in this book is indexed from 0, and every exam-reference-sheet
list is indexed from 1. Worth a standing callout wherever a standards insert touches
lists or iteration (topics 3.8, 3.10, 3.11), not just a one-time mention.

## Terms AP CSP expects that Working in Python doesn't use

With a proposed carrier for each — most are the already-established supplements from
`alignment/supplement-plan.md`, not new decisions.

| AP CSP term | What it means | Proposed carrier |
|---|---|---|
| computing innovation | the CED's umbrella term for any program, physical device, or nonphysical concept built with computing | supplement (introduced through the Create Performance Task) |
| computational artifact | the CED/CA's shared term for the thing a student builds and submits | supplement (Create Performance Task) |
| event / event-driven | a program structured around responding to user or system triggers rather than running top-to-bottom | unassigned — real gap, see `alignment/standards_alignment.md` |
| heuristic | an approach that produces a good-enough, not-guaranteed-optimal solution | supplement (November algorithms block) |
| decidable / undecidable problem | a problem for which no algorithm can always produce a correct yes/no answer | supplement (November algorithms block) |
| bit / byte, lossy / lossless compression | binary representation and data-compression vocabulary | unassigned — real gap as of 2026-08-09; CS50T Multimedia dropped, not taught since year one. Pico/MicroPython I2C chapter has a partial touchpoint for byte/hex notation, none for compression. |
| digital divide | unequal access to computing/internet by socioeconomic, geographic, or demographic line | little_brother |
| crowdsourcing / citizen science | obtaining input or data from large distributed groups over the internet | little_brother |
| fault tolerance | a system's ability to keep working when some of its parts fail | little_brother |
| symmetric / asymmetric (public/private key) encryption | the two families of encryption approaches named on the exam reference sheet | little_brother |
| personally identifiable information (PII) | the CED's term for data that identifies a specific individual | little_brother |

## Terms Working in Python uses that AP CSP doesn't need

Recommended: never delete these. They're either the Python-specific name for a concept
AP CSP does require (in which case the term itself just isn't tested, only the idea
underneath it), or they're extra content this course teaches beyond the exam's scope.

| Working in Python term | Status | Why |
|---|---|---|
| recursion / recursive | keep | not part of the AP CSP reference sheet's required pseudocode at all (only `REPEAT n TIMES` / `REPEAT UNTIL` iteration are), but this book uses it as its primary vehicle for indefinite repetition — see the `while`-loop gap in the AP index and `standards_alignment.md`. Load-bearing for this course even though it isn't exam vocabulary. |
| docstring | keep | Python's realization of AP's general "program documentation" concept (CRD-2.G) — the idea is tested, the term isn't. |
| traceback | keep | Python's specific error-report format; realizes AP's general "run-time error" concept (CRD-2.I.3) without needing the word. |
| encapsulation, generalization | keep | general CS vocabulary this book uses precisely; conceptually close to AP's abstraction language (AAP-1.C) without being required exam terms. |
| development plan | keep | this book's name for AP's "development process" (CRD-2.E) — same idea, book-specific phrasing. |
| aliasing | keep | a real correctness issue (two names for one mutable object) that isn't named or tested by AP CSP but matters for writing correct Python. |
| f-strings, YAML, shelve | keep | Python/tooling-specific, well beyond anything DAT-2 asks for, but this is exactly the "file and CSV work" that carries DAT-2's partial coverage per the supplement plan. |
| Markov analysis, bigram | keep | book-specific technique names from chap12; the underlying skill (processing text data for patterns) is what carries AP 2.3/2.4, not these particular vocabulary words. |
| inheritance, polymorphism | defer | chapters 16–17 content. Object-oriented programming is explicitly outside the AP CSP framework (already stated in the Step 4 short-form standards-insert template for chapters 14–19). Valuable as a CS50/AP CSA on-ramp, not exam prep. |
