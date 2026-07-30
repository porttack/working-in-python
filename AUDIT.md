# Audit — Pass 1 (Survey and Scaffold)

Working notes and handoff notes for the survey/scaffold pass. See `CHAPTER_MANIFEST.md`
for the approved filename-to-chapter mapping this audit builds on.

---

## Step 2 — Per-chapter inventory

Method: headings extracted from `chapters/chapNN.md` (fenced code blocks masked out first
so code comments aren't mistaken for markdown headings); glossary terms read from the
`## Glossary` section; exercises read from the `## Exercises` section; prose word count is
the whole file with fenced/inline code stripped; code cell count is every `code`-type cell
in `chapters/chapNN.ipynb`.

`chap00` (Preface) and `jupyter_intro` have no `Exercises` or `Glossary` sections — both
are front matter, consistent with the manifest. They're skipped below except for their VA
mentions, noted at the end of this section.

### Ask a virtual assistant — classification, all chapters

Every chapter 1–18 has exactly one `### Ask a virtual assistant` subsection under
`## Exercises`. Read in full, **every one of these 18 sections is kind B** — a paragraph or
bulleted list of suggested prompts, with no attached graded task. None of them ask the
student to turn in a transcript, a written answer, or a specific deliverable; they are
explicitly framed as optional ("if you are curious," "consider asking," "you might want
to"). Chapter 19 has no such section (it has no Exercises/Glossary at all).

Beyond those 18 sections, VA mentions occur in two more places: **inline asides inside
otherwise-native exercises** (kind C — the graded task is ordinary code, the VA is
mentioned as one optional way to get unstuck or to learn more) and **four exercises whose
entire task is to prompt a VA and evaluate what comes back** (kind A). The four kind-A
exercises are the only places in the book where a VA interaction is the graded deliverable
itself:

| Chapter | Line | What makes it kind A |
|---|---|---|
| chap05 | 921 | Exercise's whole task is "ask a VA for a program that draws a Sierpiński triangle," then debug it. No independent version of the task exists. |
| chap07 | 808 | Exercise's whole task is the verbatim VA prompt given in the text, then `run_doctests` to check it. |
| chap07 | 824 | Same pattern, one exercise later, targeting a different function. |
| chap17 | 1181 | Kangaroo mutable-default-argument bug: "see if you can figure out what went wrong, then ask a virtual assistant..." No solution cell exists — the deliverable is the explanation. |

Two exercises came close to kind A but were classified C on inspection because the VA
prompt is a preamble/warm-up, not the graded task: chap05 line 872 (Koch curve — the VA
question is "What is the Koch curve?", but the graded task is writing the `koch` function)
and chap13 line 912 (`is_image` — VA is offered as one alternative hint among others, not
the task itself).

**Per-chapter counts** (A / B / C, with B always the one dedicated section):

| Chapter | A | B | C | Notes |
|---|---|---|---|---|
| chap01 | 0 | 1 | 1 | C at line 551 (rounding curiosity, optional) |
| chap02 | 0 | 1 | 1 | C at line 567 (math.e aside in Part 3) |
| chap03 | 0 | 1 | 1 | C at line 329 (print function parameters, optional) |
| chap04 | 0 | 1 | 0 | |
| chap05 | 1 | 1 | 2 | A at 921 (Sierpiński); C at 847, 872 |
| chap06 | 0 | 1 | 0 | |
| chap07 | 2 | 1 | 0 | A at 808 and 824 |
| chap08 | 0 | 1 | 2 | C at 825, 911 |
| chap09 | 0 | 1 | 0 | |
| chap10 | 0 | 1 | 1 | C at 860 |
| chap11 | 0 | 1 | 2 | C at 784, 1038 |
| chap12 | 0 | 1 | 0 | |
| chap13 | 0 | 1 | 1 | C at 912 |
| chap14 | 0 | 1 | 0 | |
| chap15 | 0 | 1 | 0 | |
| chap16 | 0 | 1 | 1 | C at 639 (in Debugging, not Exercises) |
| chap17 | 1 | 1 | 1 | A at 1181 (Kangaroo); C at 890 (general encouragement) |
| chap18 | 0 | 1 | 2 | C at 923, 968 (both in Debugging) |
| chap19 | 0 | 0 | 0 | 2 narrative mentions in prose (lines 50, 53), not exercise-attached |
| **Total** | **4** | **18** | **15** | |

**Size of the replacement job** (per `mods/pass-1-survey.md`: pass 2 replaces only kind A
one-for-one): **4 exercises**, across 3 chapters (05, 07 ×2, 17). This is a small, bounded
job — not 18 chapters' worth of rewriting. The 18 kind-B sections are handled at the
section level by the VA-removal column of the treatment matrix (`strip`/`keep`/`decide`),
not one-for-one exercise replacement. The 15 kind-C asides are single sentences inside
exercises that are otherwise unrelated to VA material; per the pass-1 instruction they are
explicitly *not* padded into replacement work.

`chap00` and `jupyter_intro` mention virtual assistants only in narrative, book-level prose
(chap00 lines 15, 22, 69, 76, 83) — these describe the book's overall approach in the
Preface and aren't exercise- or section-scoped, so they're out of scope for the A/B/C
scheme entirely.

### Per-chapter detail

For each chapter: section headings (level 2), glossary term count and list, exercise count
and one-line description (full descriptions and IDs are in `data/exercise-ledger.json`),
prose word count, and code cell count.

**chap01 — Welcome**
Headings: Arithmetic operators · Expressions · Arithmetic functions · Strings · Values and
types · Formal and natural languages · Debugging · Glossary · Exercises
Glossary (17): arithmetic operator, integer, floating-point, integer division, expression,
value, function, function call, syntax error, string, concatenation, type, operand, natural
language, formal language, bug, debugging
Exercises (4): round() and 0.5 rounding · deliberate syntax errors · guess-the-type ·
arithmetic word problems
Prose words: 2622 · Code cells: 50

**chap02 — Variables and Statements**
Headings: Variables · State diagrams · Variable names · The import statement · Expressions
and statements · The print function · Arguments · Comments · Debugging · Glossary ·
Exercises
Glossary (15): variable, assignment statement, state diagram, keyword, import statement,
module, dot operator, evaluate, statement, execute, argument, comment, runtime error,
exception, semantic error
Exercises (2): deliberate assignment/import errors · interpreter-as-calculator (sphere
volume, trig identity)
Prose words: 2210 · Code cells: 49

**chap03 — Functions**
Headings: Defining new functions · Parameters · Calling functions · Repetition · Variables
and parameters are local · Stack diagrams · Tracebacks · Why functions? · Debugging ·
Glossary · Exercises
Glossary (10): function definition, header, body, function object, parameter, loop, local
variable, stack diagram, frame, traceback
Exercises (4): print_right · triangle pyramid · rectangle · 99 Bottles of Beer
Prose words: 2178 · Code cells: 39

**chap04 — Functions and Interfaces**
Headings: The jupyturtle module · Making a square · Encapsulation and generalization ·
Approximating a circle · Refactoring · Stack diagram · A development plan · Docstrings ·
Debugging · Glossary · Exercises
Glossary (11): interface design, canvas, encapsulation, generalization, keyword argument,
refactoring, development plan, docstring, multiline string, precondition, postcondition
Exercises (5): rectangle (turtle) · rhombus · parallelogram · pie of triangles · flower
petals
Prose words: 2260 · Code cells: 49

**chap05 — Conditionals and Recursion**
Headings: Integer division and modulus · Boolean expressions · Logical operators · if
statements · The else clause · Chained conditionals · Nested conditionals · Recursion ·
Stack diagrams for recursive functions · Infinite recursion · Keyboard input · Debugging ·
Glossary · Exercises
Glossary (15): recursion, modulus operator, boolean expression, relational operator,
logical operator, conditional statement, condition, block, branch, chained conditional,
nested conditional, recursive, base case, infinite recursion, newline
Exercises (6): Unix epoch → h:m:s · triangle inequality · predict output/stack diagram ·
jupyturtle function prediction · Koch curve · **[A] Sierpiński triangle via VA**
Prose words: 2795 · Code cells: 80

**chap06 — Return Values**
Headings: Some functions have return values · And some have None · Return values and
conditionals · Incremental development · Boolean functions · Recursion with return values ·
Leap of faith · Fibonacci · Checking types · Debugging · Glossary · Exercises
Glossary (7): return value, pure function, dead code, incremental development, scaffolding,
Turing complete, input validation
Exercises (5): hypot (incremental dev) · is_between · Ackermann · is_power · gcd
Prose words: 3149 · Code cells: 87

**chap07 — Iteration and Search**
Headings: Loops and strings · Reading the word list · Updating variables · Looping and
counting · The in operator · Search · Doctest · Glossary · Exercises
Glossary (11): loop variable, file object, method, update, initialize, increment,
decrement, counter, linear search, pass, fail
Exercises (7): uses_none · uses_only · uses_all · Spelling Bee puzzle · derive one function
from another · **[A] uses_all via uses_only, VA prompt** · **[A] uses_all via uses_any, VA
prompt**
Prose words: 2442 · Code cells: 72

**chap08 — Strings and Regular Expressions**
Headings: A string is a sequence · String slices · Strings are immutable · String
comparison · String methods · Writing files · Find and replace · Regular expressions ·
String substitution · Debugging · Glossary · Exercises
Glossary (12): sequence, character, index, slice, empty string, object, immutable,
invocation, regular expression, pattern, string substitution, shell command
Exercises (4): head-like function · Wordle solver · Wordle continuation · word-frequency
analysis of *Monte Cristo*
Prose words: 3262 · Code cells: 85

**chap09 — Lists**
Headings: A list is a sequence · Lists are mutable · List slices · List operations · List
methods · Lists and strings · Looping through a list · Sorting lists · Objects and values ·
Aliasing · List arguments · Making a word list · Debugging · Glossary · Exercises
Glossary (9): list, element, nested list, delimiter, equivalent, identical, reference,
aliased, attribute
Exercises (4): anagram checker · reversed() exploration · reverse_sentence · total_length
Prose words: 2387 · Code cells: 88

**chap10 — Dictionaries**
Headings: A dictionary is a mapping · Creating dictionaries · The in operator · A
collection of counters · Looping and dictionaries · Lists and dictionaries · Accumulating a
list · Memos · Debugging · Glossary · Exercises
Glossary (12): dictionary, item, key, value, mapping, hash table, hashable, hash function,
accumulator, filtering, call graph, memo
Exercises (5): dict.get() · has_duplicates · find_repeats · add_counters · interlocking
words
Prose words: 3014 · Code cells: 71

**chap11 — Tuples**
Headings: Tuples are like lists · But tuples are immutable · Tuple assignment · Tuples as
return values · Argument packing · Zip · Comparing and sorting · Inverting a dictionary ·
Debugging · Glossary · Exercises
Glossary (6): pack, unpack, zip object, enumerate object, sort key, data structure
Exercises (7): mutable-value-in-tuple hashability · invert alphabet dict · most_frequent_
letters · harder anagram sets · word_distance · metathesis pairs · bonus exercise (not in
book)
Prose words: 3586 · Code cells: 105

**chap12 — Text Analysis and Generation**
Headings: Unique words · Punctuation · Word frequencies · Optional parameters · Dictionary
subtraction · Random numbers · Bigrams · Markov analysis · Generating text · Debugging ·
Glossary · Exercises
Glossary (8): default value, override, deterministic, pseudorandom, bigram, trigram,
n-gram, rubber duck debugging
Exercises (3): trigram counter · add_trigram (Markov) · random-text generation loop
Prose words: 3926 · Code cells: 87

**chap13 — Files and Databases**
Headings: Filenames and paths · f-strings · YAML · Shelve · Storing data structures ·
Checking for equivalent files · Walking directories · Debugging · Glossary · Exercises
Glossary (16): ephemeral, persistent, directory, current working directory, path, relative
path, absolute path, f-string, configuration data, serialization, deserialization,
database, key-value stores, binary mode, hash function, digest
Exercises (3): replace_all across files · add_word (shelve) · duplicate-file finder
Prose words: 3507 · Code cells: 85

**chap14 — Classes and Functions**
Headings: Programmer-defined types · Attributes · Objects as return values · Objects are
mutable · Copying · Pure functions · Prototype and patch · Design-first development ·
Debugging · Glossary · Exercises
Glossary (12): object-oriented programming, class, class object, instantiation, instance,
attribute, object diagram, format specifier, pure function, functional programming style,
prototype and patch, design-first development
Exercises (3): subtract_time · is_after · Date class (multi-part)
Prose words: 2598 · Code cells: 72

**chap15 — Classes and Methods**
Headings: Defining methods · Another method · Static methods · Comparing Time objects · The
__str__ method · The init method · Operator overloading · Debugging · Glossary · Exercises
Glossary (8): object-oriented language, method, receiver, static method, instance method,
special method, operator overloading, invariant
Exercises (1): rewrite Date-class functions from ch14 as methods (multi-part)
Prose words: 1750 · Code cells: 43

**chap16 — Classes and Objects**
Headings: Creating a Point · Creating a Line · Equivalence and identity · Creating a
Rectangle · Changing rectangles · Deep copy · Polymorphism · Debugging · Glossary ·
Exercises
Glossary (3): shallow copy, deep copy, polymorphism
Exercises (5): Line.__eq__ · Line.midpoint · Rectangle.midpoint · Rectangle.make_cross ·
Circle class
Prose words: 2213 · Code cells: 79

**chap17 — Inheritance**
Headings: Representing cards · Card attributes · Printing cards · Comparing cards · Decks ·
Printing the deck · Add, remove, shuffle and sort · Parents and children · Specialization ·
Debugging · Glossary · Exercises
Glossary (8): inheritance, encode, class variable, totally ordered, delegation, parent
class, child class, specialization
Exercises (7): Trick class (bridge) · PokerHand setup/read · has_straight ·
has_straightflush · has_pair · has_fullhouse · **[A] Kangaroo mutable-default-argument
bug, VA to confirm**
Prose words: 3634 · Code cells: 109

**chap18 — Python Extras**
Headings: Sets · Counters · defaultdict · Conditional expressions · List comprehensions ·
any and all · Named tuples · Packing keyword arguments · Debugging · Glossary · Exercises
Glossary (5): factory, conditional expression, list comprehension, generator expression,
test discovery
Exercises (6): faster uses_none with set · Scrabble tile check · partition PokerHand by
suit · Fibonacci with conditional expressions · binomial coefficient rewrite · Deck.__str__
rewrite
Prose words: 3193 · Code cells: 118

**chap19 — Final thoughts**
No headings below the chapter title, no Glossary, no Exercises — this is a short closing
essay, not a worked chapter. Prose words: 840 · Code cells: 1.

Full exercise-by-exercise detail (all 81 native + 4 kind-A) is in
`data/exercise-ledger.json`, seeded in Step 3.

---

## Step 3 — Exercise ledger

`data/exercise-ledger.json` seeded with 81 entries (one per existing `### Exercise`),
IDs `ch{NN}-ex{NN}` in chapter order. 77 are `kind: "native"`, 4 are `kind: "A"` (the
VA-driven exercises identified above, in chap05, chap07 ×2, chap17). All entries currently
have `action: "kept"`, `replacement_id: null`, empty `targets_ap`/`targets_ca` (pass 3's
job), and `est_minutes_before == est_minutes_after` since pass 1 changes nothing.
`self_verifying` is `true` for exercises with a doctest/example-based check, `false` for
open-ended or exploratory ones (no single correct answer to assert against).

Per-exercise time estimates use the trivial (≤5) / standard (10–20) / extended (25+)
buckets from `mods/pass-1-survey.md` Step 4, judged from each exercise's word count, number
of code cells, and whether it's multi-part. These are first-pass estimates from reading the
text, not from timing a student — treat them as directional for the chapter-level effort
estimate below, and expect pass 2/3 to refine individual entries as exercises are actually
touched.

---

## Step 4 — Effort estimate

**Method**, applied per chapter 1–19:

- reading minutes = prose words / 130, counting only the exposition (through the end of
  the Debugging section — *before* Glossary and Exercises, so exercise-prompt text isn't
  counted twice against both "reading" and "exercise time")
- code-cell minutes = 1 minute × number of code cells in the exposition only (again
  excluding cells inside the Exercises section, since running/checking a solution cell is
  already priced into that exercise's estimate)
- exercise minutes = sum of each exercise's trivial/standard/extended estimate from
  `data/exercise-ledger.json`
- total = reading + code-cell + exercise minutes

This differs from a naive "whole-file word count + whole-notebook code-cell count"
approach, which double-counts exercise reading and solution-cell time. The whole-chapter
prose/code totals in Step 2 above are the raw inventory numbers; the table below uses the
exposition-only figures to avoid that double count.

| Chapter | Expo words | Reading min | Expo code cells | Exercise min | **Total min** | Ratio to median |
|---|---:|---:|---:|---:|---:|---:|
| **11 Tuples** | 2289 | 17.6 | 72 | 175 | **265** | 1.60 |
| **17 Inheritance** | 2499 | 19.2 | 63 | 150 | **232** | 1.41 |
| **18 Python Extras** | 2688 | 20.7 | 92 | 105 | **218** | 1.32 |
| 06 Return Values | 2646 | 20.4 | 54 | 105 | 179 | 1.09 |
| 07 Iteration and Search | 1669 | 12.8 | 46 | 115 | 174 | 1.05 |
| 08 Strings/Regex | 2539 | 19.5 | 68 | 85 | 173 | 1.05 |
| 05 Conditionals/Recursion | 1998 | 15.4 | 52 | 105 | 172 | 1.04 |
| 10 Dictionaries | 2339 | 18.0 | 50 | 100 | 168 | 1.02 |
| 12 Text Analysis | 3366 | 25.9 | 72 | 70 | 168 | 1.02 |
| 13 Files and Databases | 2758 | 21.2 | 66 | 75 | 162 | 0.98 |
| 16 Classes and Objects | 1771 | 13.6 | 48 | 95 | 157 | 0.95 |
| 09 Lists | 1786 | 13.7 | 69 | 60 | 143 | 0.86 |
| 04 Functions/Interfaces | 1833 | 14.1 | 29 | 90 | 133 | 0.81 |
| 14 Classes and Functions | 2081 | 16.0 | 52 | 60 | 128 | 0.78 |
| 01 Welcome | 2025 | 15.6 | 39 | 60 | 115 | 0.69 |
| 03 Functions | 1676 | 12.9 | 27 | 70 | 110 | 0.67 |
| 02 Variables/Statements | 1691 | 13.0 | 42 | 40 | 95 | 0.58 |
| 15 Classes and Methods | 1435 | 11.0 | 35 | 30 | 76 | 0.46 |
| 19 Final thoughts | 840 | 6.5 | 1 | 0 | 8 | 0.05 |

Median across chap01–18 (excluding chap19, which isn't a worked chapter): **165 minutes.**

### 1. Does chapter 1 support the hypothesis that it's roughly a 30-minute read?

**No, not once code cells and exercises are counted.** The flowing-prose reading time alone
is 15.6 minutes — in the right neighborhood of "30-minute read" if that phrase meant prose
only. But chapter 1 has 39 expository code cells students are meant to run and inspect
(round-off behavior, string operators, type checks), which brings it to ~55 minutes before
touching an exercise, and its 4 exercises add another 60, for a **total of ~115 minutes** —
roughly 4x a 30-minute read. Chapter 1 is in fact one of the *lighter* chapters (0.69 of
median), so if a 30-minute figure was the planning assumption for the lightest chapter in
the sequence, every chapter 1–18 is going to land well above that.

### 2. Which chapters exceed 75 minutes?

**All of them except chapter 19** (which isn't a taught chapter). Every chapter in 1–18
comes in between 76 minutes (ch15, the lightest worked chapter) and 265 minutes (ch11, the
heaviest) — i.e. **every single chapter the course teaches exceeds the 60–75 minute weekly
homework budget**, most by a wide margin. Only chapter 15 (76 min) comes close to fitting
inside it.

### 3. Is chapter 9 (Lists) the heaviest of chapters 1–11?

**No.** Chapter 9 comes in at 143 minutes, ratio 0.86 — below the whole-book median, and
the **4th-lightest** of chapters 1–11. Five chapters in that range are heavier: 6, 7, 8, 5,
and 10 all exceed chapter 9, and **chapter 11 (Tuples) is the heaviest chapter in the
entire book** at 265 minutes — nearly twice chapter 9's estimate and 3.5x the nominal
75-minute budget.

This directly contradicts the assumption behind the current buffer placement. The buffer
week sits before chapter 9 on the premise that it's the load-bearing week for the Create
Performance Task; by this estimate the actual load-bearing week is **chapter 11**, two
weeks later, immediately before the Aug–Dec live sequence ends and the pace changes to
independent study. There is currently no buffer adjacent to chapter 11.

**Recommendation, not a re-pacing decision:** the teacher should look hardest at chapter 11
before committing to one-week-per-chapter for the fall. If a buffer is going to move, moving
it to sit before or after chapter 11 (rather than chapter 9) would track the actual effort
data better. Chapters 17 and 18 are similarly heavy but fall in the independent-study tier
(14–19), where the pacing constraint is looser. Candidate chapters to consider **pairing**
into a single week if the calendar needs to compress rather than expand: chapter 2 (95 min)
with chapter 3 (110 min) — both light, both early, combined still under chapter 11 alone.
Chapter 15 (76 min) is the only chapter light enough to safely absorb a second, smaller
assignment without risk. No chapter in 1–11 is light enough to pair with chapter 11 itself;
if it needs relief, it needs its own extra time, not a partner chapter.

**Pacing discussion outcome:** raised directly with the teacher mid-pass. The specific
buffer-week dates and whether the existing buffer is fixed (a school holiday/testing day)
or freely relocatable weren't available in this session, so no calendar change was made.
This finding stands as an open flag for pass 3 / the teacher to resolve before the fall
calendar is finalized — see "What pass 2 needs to know" below.

---

## Step 5 — Scaffold

Built per the layout in `CLAUDE.md`:

- `.gitignore`: added `sessions/` and a backstop `standards/*.pdf` / `scratch/` ignore.
- `ATTRIBUTION.md`: complete (upstream MIT/CC BY-NC-SA licensing, this fork's licensing,
  explicit statement that framework material is never included verbatim).
- `AP_MODIFICATIONS.md`, `CHANGELOG.md`, `CHANGELOG_DETAIL.md`: stubbed per spec.
- `tools/build_ledger.py`: reads `data/exercise-ledger.json`, writes `CHANGELOG_DETAIL.md`
  grouped by chapter with per-chapter and total counts. Verified idempotent (identical
  output byte-for-byte across two runs).
- `tools/check_sync.py`: checks sentinel balance/valid `type`, standards-code resolution
  (currently skipped — `standards/apcsp.json`, `castandards.json`, `crosswalk.json` are all
  seeded as empty `{}` stubs for pass 3 to fill), and that chapters 14–19 plus front matter
  carry no blank markers. Runs clean against the current repo (42 files: 21 chapters ×
  `.md`/`.ipynb`).
- `Makefile`: the four targets from `CLAUDE.md`, all exercised successfully below.
- `alignment/` and `appendix/` directories created (empty — their generated files are pass
  3's job).

**Flagged, not fixed, during scaffolding:**

- **Framework extracts are sitting inside the repo directory.** `standards/*.pdf` (the 2023
  CED, the SDG, and `csstandards.pdf`) are currently untracked by git — confirmed via
  `git ls-files`, nothing standards-related is in the index, so there is nothing to remove
  from history. But `CLAUDE.md` Non-negotiable #1 says these extracts should "stay in
  scratch, **outside the repo**, never committed" — sitting untracked inside `standards/`
  satisfies "never committed" only as an accident of nobody running `git add -A` yet. I
  added `standards/*.pdf` to `.gitignore` as a backstop, but the extracts are still
  physically inside the repo working directory, which the instruction says they shouldn't
  be. Recommend moving these three PDFs to scratch (outside this directory tree) rather
  than relying on `.gitignore` alone.

## Step 6 — Blanks tooling verification

Chapter chosen: **chap03 (Functions)**. Added **4 markers**, one of each documented type,
to both `chap03.md` and `chap03.ipynb` in parallel (the definition of `print_lyrics`, the
header/body sentence, and the parameter-assignment discussion point):

1. `<!--blank-->**function definition**<!--/blank-->` — prose term blank.
2. `<!--blank-->**header**<!--/blank-->` — prose term blank (one per paragraph; `**body**`
   in the same sentence was left visible since the sentence already carries two bolded
   terms and the marker guidance caps it at one blank per paragraph).
3. `<!--blank-only: What gets assigned to the parameter when the function is called?-->` —
   a live-discussion prompt after the `print_twice` parameter explanation.
4. A code blank on the `print_lyrics` definition — done two different ways in the two
   formats specifically to compare them: `# blank` suffix on the `def` line in `chap03.md`,
   and a `"tags": ["blank"]` whole-cell marker on the equivalent code cell in
   `chap03.ipynb`.

**`make blanks` && `make check` passed clean** after generation (42 source files, all
chapters, not just chap03 — `build_blanks.py` processes every file in `chapters/`
regardless of whether it carries markers).

**Both guardrails confirmed:**
- Hand-editing `blanks/chap03.md` (appended a stray line) → `python3 tools/build_blanks.py
  --check` reported `blanks/ is stale`, named the file, exited 1. `make check` failed as
  expected.
- Removing the `<!--/blank-->` closing tag from the header marker in `chapters/chap03.md`
  → `python3 tools/build_blanks.py` reported `chap03.md: 2 <!--blank--> vs 1
  <!--/blank-->`, exited 2, correctly naming the file. Both changes were reverted
  immediately after confirming the guardrail; `chapters/chap03.md` and `chap03.ipynb` are
  back to their post-marker, pre-break state, and `make check` is clean again.

**Marker count and density:** 4 markers across ~90 lines of prose/code touched, in a
chapter with 10 `##` sections. That felt right for a worked-example section: enough to
break up a lecture without turning every sentence into a fill-in-the-blank. Consistent
with the guidance that this reads fine in a diff but needs to be *felt*, not just counted —
4 in one section, scaled to 10+ sections across a full chapter, would be dense; pass 2
should sanity-check density per chapter rather than applying a fixed per-chapter count.

**Important gap found, not fixed (do not rewrite `build_blanks.py` per `CLAUDE.md`):** the
`# blank` code-line marker **only works inside `.ipynb` code cells**. `transform_markdown`
(used for `.md` files) calls `blank_markdown`, which only resolves `<!--blank-->` and
`<!--blank-only:-->` — it never calls `blank_code`. A `# blank` marker placed in a `.md`
fenced code block is silently left untouched in `blanks/`: it shows up verbatim as
`def print_lyrics():  # blank` in the confirmation run above, no error, no warning. This
matters because `CLAUDE.md`'s own marker table doesn't distinguish `.md` from `.ipynb` for
this marker type, and both formats are shipped in parallel per chapter. Whole-cell tagging
(`"tags": ["blank"]`) is the only code-blanking mechanism that actually works, and it's
`.ipynb`-only by construction (there's no metadata channel in plain Markdown to carry a
cell tag). **Recommendation for pass 2: never use a bare `# blank` line in a `.md` fenced
code block — it will silently do nothing.** Either restrict code blanking to the notebook
version (which is what's actually projected live in class) and leave `.md` prose-only, or
raise this as a fix to `build_blanks.py` itself before relying on it further, since
"provided and tested" evidently didn't cover this path.

---

## Handoff

**Filename mapping** (approved): `chap00` = Preface, front matter, unnumbered. `chap01`
through `chap19` map 1:1 to chapter numbers 1–19. `jupyter_intro` is supplementary,
unnumbered, and absent from upstream's own `jb/_toc.yml`. Full table in
`CHAPTER_MANIFEST.md`.

**VA classification, whole book:** 4 kind-A exercises (chap05 ex06, chap07 ex06/ex07,
chap17 ex07 — all in `data/exercise-ledger.json`), 18 kind-B sections (one per chapter,
1–18, all bare prompt lists with no attached task), 15 kind-C inline asides. The pass-2
one-for-one replacement job is **4 exercises across 3 chapters**, not a book-wide rewrite.

**Effort estimate:** median 165 min/chapter across chap01–18, against a 60–75 min/week
budget. Every taught chapter exceeds budget; chapter 11 (Tuples) is the heaviest in the
book at 265 min (not chapter 9, which is 4th-lightest of 1–11 at 143 min). Full table and
the three required answers are under Step 4 above. This was raised with the teacher mid-
pass; no calendar decision was made this session (see "What pass 2 needs to know").

**Chapter marked with blanks:** chap03, 4 markers, one of each documented type. Both
`build_blanks.py` guardrails (`--check` on a hand-edit, malformed-marker detection on a
missing closing tag) confirmed working and reverted cleanly.

**Findings that contradict or complicate the treatment matrix / plan, not yet resolved:**

1. **Pass-file location mismatch.** `CLAUDE.md` says pass files live in `docs/`; the file
   actually used for this pass is `mods/pass-1-survey.md`. No `docs/` directory exists.
   Reconcile before pass 2 starts (rename `mods/` → `docs/`, or update `CLAUDE.md`) so the
   next cold read doesn't stall.
2. **`blank/` vs `blanks/` naming collision.** An upstream-generated `blank/` (singular)
   directory already exists at the repo root, unrelated to this project's own `blanks/`
   (plural). Left untouched; `tools/build_blanks.py` correctly targets `blanks/` only.
3. **Framework extracts inside the repo.** `standards/*.pdf` are untracked but physically
   present in the repo tree, contradicting "stay in scratch, outside the repo." Now
   `.gitignore`d as a backstop; recommend physically relocating them.
4. **`# blank` code marker is `.ipynb`-only**, silently inert in `.md`. See Step 6 above.
5. **Pacing is not just a chapter-11 problem.** Every chapter 1–18 exceeds the 75-minute
   budget; chapters 5–10 in particular cluster at 130–180% of budget with no dip anywhere
   near the current buffer's placement before chapter 9.

**What pass 2 needs to know before it starts:**

- Read `CHAPTER_MANIFEST.md` and the VA classification table above before touching any
  chapter — the one-for-one replacement scope is exactly the 4 kind-A exercises, not every
  "Ask a virtual assistant" section.
- Do not use bare `# blank` in `.md` fenced code; use notebook cell tags for code blanking,
  or resolve item 4 above first.
- The pacing/buffer-placement question is open. If pass 2 starts touching chapters 9–11
  under the assumption that chapter 9 carries the calendar buffer, that assumption is not
  supported by this pass's effort estimate — confirm with the teacher before pass 2's
  chapter-by-chapter work implies a re-pacing decision by omission.
- `data/exercise-ledger.json` IDs are stable and referenced by `CHANGELOG_DETAIL.md`;
  don't renumber them even if an exercise is later split or merged — use `replacement_id`
  instead.

---

# Audit — Pass 2 (Chapter Surgery)

## Gate: chapters 1–2 complete, stopping for register and marker-density review

Per `mods/pass-2-surgery.md` "Order of work" step 1, work stops here. Chapters 3–8 are the
next batch and should conform to whatever pattern this review approves or amends.

### Preconditions checked before starting

- `CHAPTER_MANIFEST.md` filename mapping is present and approved. Not blocked.
- `upstream/v3` had no local ref; fetched it. **Note for the checkout step:** upstream ships
  only `chapters/*.ipynb`. The parallel `chapters/*.md` files are this fork's own exports
  (commit c780265), so `git diff upstream/v3 -- chapters/chapNN.md` shows the whole file as
  new and proves nothing. The meaningful upstream diff is against the `.ipynb`. Both
  renderings are hand-edited in parallel and were verified byte-equivalent in marker counts
  after every change.

### Uncommitted prep found in the working tree

A prior session had already staged, but not committed, the `blanks/` → `projector/` rename
called for by this pass (Makefile, `CLAUDE.md` layout section, `standards/README.md`) and a
fix to `tools/build_blanks.py` closing the Pass 1 gap where `# blank` was silently inert in
`.md` files. That work is verified and committed separately as a prep commit so the
chapter commits stay revertible on their own. One additional fix was needed: the Makefile's
`.PHONY` still listed the old `blanks` target, so `make projector` no-opped against the
existing `projector/` directory.

Two stray files, `CLAUDE.md.bak` and `Makefile.bak`, are left untracked and uncommitted.

### Step 1 — VA removal

| Chapter | Kind A | Kind B | Kind C | Prose repair needed |
|---|---|---|---|---|
| chap01 | 0 | 1 | 1 | none |
| chap02 | 0 | 1 | 1 | none |

- **chap01 kind B** — the whole "Ask a virtual assistant" subsection under `## Exercises`
  (3 consecutive notebook cells). Removed whole.
- **chap01 kind C** — the closing line of exercise 1, inviting the student to ask an
  assistant how Python rounds a trailing `0.5`. It was a standalone paragraph after the two
  `round` cells; removing it leaves the exercise ending on "Try these examples and see if
  you can figure out what rule it follows," which reads correctly. **No repair.**
- **chap02 kind B** — same subsection, one notebook cell. Removed whole.
- **chap02 kind C** — a clause inside exercise 2 Part 3 offering an assistant as a way to
  find out what `math.e` is. The sentence now runs "…written in math notation as $e$. Now
  let's compute $e^2$ three ways:" — coherent as written. **No repair.**

**No prose repairs were made in either chapter**, so there is nothing here a reader of the
original needs to be told about beyond the removals themselves.

**One VA mention deliberately left in place.** `chap01` line 50 ends "…you will need it to
understand the rest of the book, to communicate with other programmers, and to use and
understand virtual assistants." Pass 1's A/B/C sweep did not classify it: it is not a
suggestion that an assistant could explain something, it is a reason the vocabulary matters,
and it sits in chapter-body prose rather than an exercise. Removing the trailing clause
would be an edit to upstream prose outside the three defined kinds. **Left as-is, raised
here for the gate review to rule on** — the same judgment will recur in `chap00`, whose
Preface discusses assistants at book level in five places and is likewise unclassified.

### Step 2 — Replacement exercises

**None.** Neither chapter has a kind-A exercise. The four replacements owed across the book
are all in chapters 5, 7, and 17.

### Step 3 — Policy note

Added once, in `chap00`, as `## Doing the work by hand`, inside
`<!-- apcsp:begin type="note" chapter="00" -->`. Placed after "Navigating the Book" —
the section that tells the student how to work through the book — and before "What's new in
the third edition?". Four sentences, second person, present tense, no moralizing and no
attribution guidance. It will not be repeated per chapter.

### Step 4 — Blank markers

| Chapter | Prose blanks | Prompts | Code blanks | Against target (4–6 / 2–4 / 0–2) |
|---|---:|---:|---:|---|
| chap01 | 5 | 3 | 0 | in range on all three |
| chap02 | 5 | 3 | 0 | in range on all three |

**chap01 prose blanks** (one per paragraph, five different sections): `arithmetic operator`,
`expression`, `calling` (the operative verb, with `function call` left visible in the next
sentence as the recovery cue), `concatenation`, `type`. Left visible on purpose: `bug` /
`debugging` in the Debugging section, and `natural`/`formal language`, so the chapter's two
discussion sections stay readable rather than becoming vocabulary drills.

**chap01 prompts**: before the `84 / 2` cell (predict 42 vs 42.0); before `len('Spam')`
(does `len` count the quotes); after the `1,000,000` paragraph (if it is not an integer,
what is it). Each is answered by the cell that follows or the next paragraph, so all three
are recoverable by a student who did the reading.

**chap02 prose blanks**, again one per paragraph across five sections:
`assignment statement`, `state diagram`, `keyword`, `module`, `argument`.

**chap02 prompts**: after "`class` is also illegal, but it might not be obvious why"
(the first two illegal names fail for visible reasons — what is wrong with `class`);
after the import-statement paragraph (what separates an expression from a statement); after
the "explain *why*, not *what*" paragraph, immediately before the two contrasting comment
cells (which one earns its space).

**Code blanks: zero in both chapters, and this is the right answer, not an omission.**
Two independent reasons:

1. **Upstream's `blank/` makes it redundant.** `blank/chap01.ipynb` and `blank/chap02.ipynb`
   are the same notebooks with the source of *every* code cell emptied — 50 and 49 cells
   respectively. There is nothing left for a `# blank` marker to add.
2. **There is nothing worth blanking.** Chapters 1 and 2 have no multi-line worked example
   in the body. Every expository cell is a one-line expression (`84 // 2`, `type(42.0)`,
   `math.pow(5, 2)`) whose entire content *is* the concept, so blanking the line leaves no
   surrounding context to recover it from — that is a quiz question, not a blank. The only
   multi-line cells are the `download` boilerplate and the `diagram` state-diagram
   plumbing, both explicitly off-limits.

Expect this to change from chapter 3 onward, where `def` headers, loop headers, and
conditions give a code blank something to carry. Reason 1 above will still apply, so the
0–2 target should be read as a ceiling that most chapters will not need to reach.

### Step 5 — Per-chapter checkout

- `make check` passes (42 source files, `check_sync` clean).
- `make ledger` regenerates with no manual edits; verified byte-identical across two runs.
- `make projector` verified idempotent.
- Cell-level diff of `chap01.ipynb` and `chap02.ipynb` against `upstream/v3` shows exactly
  the intended changes and no whitespace or formatting drift: chap01, 8 cells edited (5
  blanks + 3 prompts) and 4 cells deleted (3 VA + 1 kind-C); chap02, 9 cells edited (5
  blanks + 3 prompts + 1 kind-C) and 1 cell deleted (VA). Notebook JSON round-trips
  byte-identically, so the diffs are content-only.
- `git status` shows nothing added or modified under `blank/`.
- Marker counts verified equal between each chapter's `.md` and `.ipynb`.

### Notebook hygiene — a conflict to rule on, not resolved here

`CLAUDE.md` non-negotiable #5 says notebooks carry no execution counts and that `nbstripout`
runs before commit. **Upstream's own notebooks ship with execution counts** — 49 of them in
`chap01.ipynb` alone, 1353 across `chapters/`. Running `nbstripout` over the book would
touch every chapter and produce exactly the whole-file reflow that non-negotiable #2
forbids, and would guarantee a conflict on every future upstream pull.

What was done instead: verified that **this pass introduced no outputs and changed no
execution count** in `chap00`, `chap01`, or `chap02`, and that those three files contain no
cell outputs at all. The only committed outputs anywhere in `chapters/` are two cells in
`jupyter_intro.ipynb` (a stream and a deliberate error), which are upstream's and are the
point of that notebook.

**Ruling needed:** either non-negotiable #5 means "add no outputs or execution counts of our
own" (which is what was done, and is compatible with #2), or it means the fork strips the
whole book once and accepts permanent divergence from upstream. Do not let pass 3 decide
this by accident.

### Ledger

`data/exercise-ledger.json` is now 83 entries, up from 81. Two added: `ch01-va01` and
`ch02-va01`, `kind: "B"`, `action: "removed"`, both at 0 minutes before and after — those
sections were optional and ungraded and were never priced into the Pass 1 effort table, so
their removal does not change either chapter's estimate. Two existing entries moved from
`action: "kept"` to `action: "edited"` with a note naming the kind-C removal: `ch01-ex01`
and `ch02-ex02`. No IDs were renumbered.

### Handoff to the next batch (chapters 3–8)

- **The pattern to conform to**, pending this review: 5 prose blanks and 3 prompts per
  chapter, each blank in a different section, one per paragraph, on glossary terms and
  operative verbs; code blanks only where a multi-line worked example has a line that
  carries the concept, and never as a substitute for what upstream's `blank/` already does.
- **chap03 already carries 4 markers from Pass 1** (2 prose blanks, 1 prompt, 1 code blank
  on the `print_lyrics` header) added to verify the tooling. It needs topping up to the
  pattern, not starting from scratch — and its `# blank` line in the `.md` now actually
  works, since the build fix landed.
- **chap05 and chap07 carry three of the four kind-A replacements** (`ch05-ex06`,
  `ch07-ex06`, `ch07-ex07`). Those are the only exercise-authoring work in the 3–8 batch.
  chap07 uses doctest, so its two replacements are written the same way with
  `self_verifying: true`.
- The `chap01` line-50 question above will recur; a single ruling should cover all of them.
- The pacing/buffer question raised by Pass 1 is **still open** and this pass did nothing
  that depends on it. Chapters 9–11 remain `decide` on VA and must not be stripped without
  a ruling; their blank markers can proceed regardless.
- Nothing in these two chapters tempted a restructure. The only two places where the text
  wanted rewriting were the two kind-C removals, and both closed cleanly on their own.
---

## Pass 2, chapters 3–5

Continues from the chapters 1–2 gate. The pattern approved there (5 prose blanks, 3
spoken prompts, code blanks only where warranted, per-chapter checkout) was applied
without changes. This batch stops at chapter 5, not chapter 8 — a partial installment
of the "chapters 3–8" batch in `mods/pass-2-surgery.md`'s order of work. Chapters 6–8
remain to do.

### Repo change found at the start of this session, not made by this pass

`chapters/*.md` and `projector/*.md` (the parallel Markdown exports from the Pass 2 prep
commit) were gone when this session started, removed by a commit titled "Cleanup" that
landed after the chapters 1–2 gate and that this session did not make. `.gitignore` had
also been hand-edited (uncommitted) to add `chapters/*.md`. Net effect: `chapters/` is
now `.ipynb`-only, matching what upstream actually ships. This is a reasonable
simplification — blank markers (HTML comments) are just as invisible in a rendered
Jupyter markdown cell as in rendered `.md` — so this pass adopted it: committed the
`.gitignore` catch-up separately, and edited `chapters/chapNN.ipynb` directly with no
parallel file to keep in sync. `git diff upstream/v3 -- chapters/chapNN.md` is no longer
a meaningful check (there's nothing to compare); use the `.ipynb`.

### Step 1 — VA removal

| Chapter | Kind A | Kind B | Kind C | Prose repair needed |
|---|---|---|---|---|
| chap03 | 0 | 1 | 1 | none |
| chap04 | 0 | 1 | 0 | none |
| chap05 | 1 | 1 | 2 | none |

- **chap03 kind B** — the "Ask a virtual assistant" cell under Exercises (spaces-vs-tabs
  history, "ask your VA to write `repeat`", debugging `print_twice`). Removed whole.
- **chap03 kind C** — inside the stack-diagram discussion: "In the frame for `print`,
  the question mark indicates that we don't know the name of the parameter. If you are
  curious, ask a virtual assistant..." Removed the second sentence; the first stands on
  its own. **No repair.**
- **chap04 kind B** — the "Ask a virtual assistant" section (writing a spiral-drawing
  function). Two cells, removed whole. No kind C in this chapter, matching Pass 1.
- **chap05 kind B** — larger than the others: runs from the "### Ask a virtual
  assistant" heading through a countdown_by_two debugging vignette, twelve cells total,
  with no `### Exercise` heading and no Solution cell anywhere in the span. Removed as
  one block. **Flagged, not changed:** the countdown_by_two piece ("But it has an error.
  Ask a virtual assistant what's wrong and how to fix it. Paste the solution it provides
  back here and test it.") reads like it could independently qualify as kind A, on the
  same logic Pass 1 used for the chap17 Kangaroo exercise (no solution cell exists; the
  deliverable is the VA's explanation). Pass 1's audit didn't call this piece out
  separately the way it flagged the Koch curve and `is_image` borderline cases. This
  pass removed it under the existing kind-B classification and did **not** add a fifth
  replacement exercise — `mods/pass-2-surgery.md` Step 2 caps replacements at four
  book-wide and warns explicitly against padding, and this is exactly the kind of
  classification judgment call that should be confirmed rather than decided in passing.
  **Raise this at the next gate**: if it's ruled kind A after all, a fifth replacement
  is owed; if kind B stands, nothing further is needed.
- **chap05 kind C, Koch curve (`ch05-ex05`)** — already documented by Pass 1's ledger
  note. Removed the opening line ("Ask a virtual assistant 'What is the Koch curve?'");
  the exercise now opens directly with the numbered recursive recipe. **No repair.**
- **chap05 kind C, `ch05-ex04`** — a second aside Pass 1's audit counted (chap05 C=2)
  but that wasn't yet located when chapter 3 and 4 work started: "Adjust the values of
  `length`, `angle` and `factor`... If you are not sure you understand how it works, try
  asking a virtual assistant." Removed the second sentence. **No repair.**

### Step 2 — Replacement exercise (the book's first)

`ch05-ex06`, the Sierpiński triangle exercise ("ask a VA for a program that draws one,
then debug it"), is replaced by `ch05-ex07`: a self-contained spec for
`draw_sierpinski(size, degree)`, keeping the exact function name, parameters, and the
original's solution/demo cells untouched — only the prompt paragraph changed. It gives
the recursive definition (base case is a plain triangle; case `n` is three half-size
corner triangles with a gap where the middle one would go) and points at `penup`/
`pendown` for repositioning, without dictating exact turtle commands — the student still
has to work out the geometry, same as the four other kind-A replacements are meant to.

**This recursive algorithm was verified before being written into the exercise, not
just remembered.** A well-known textbook snippet for "recursive Sierpinski with a
turtle" uses only `forward`/`back`/`left`/`right` (no pen lifting) between sub-triangles.
That version was built and run headlessly against the real `jupyturtle` module
(downloaded and driven with `auto_render=False`, no display needed) and checked against
a pure-coordinate reference implementation of the standard Sierpiński gasket edge set.
It matched at depth 1 but **visibly drifted at depth ≥ 2** — the turtle does not return
to its own starting position/heading after a nested call, so the position math the
outer call depends on breaks. The version actually given to students instead lifts the
pen (`penup`/`pendown`) around every reposition; this was verified to exactly reproduce
the expected edge set (no extra, no missing lines, using a tolerance-based segment
comparison to rule out float-rounding false positives) at depths 0 through 4, and to
render as a correct Sierpiński triangle. `penup`/`pendown` are real `jupyturtle`
functions but weren't yet imported in this notebook (only `forward`/`left`/`right`/
`back` were, for the Koch exercise) — the prompt tells students to import them the same
way, rather than silently assuming they're available.

`ch05-ex06` → `action: "removed"`; `ch05-ex07` added with `replacement_id: "ch05-ex06"`,
`est_minutes_after: 20` (same as the original's estimate, per Step 2's "lands within a
few minutes" guidance), `self_verifying: false` (visual/graphical, matching this
chapter's other jupyturtle exercises, not doctested).

### Step 4 — Blank markers

| Chapter | Prose blanks | Prompts | Code blanks | Notes |
|---|---:|---:|---:|---|
| chap03 | 5 | 3 | 1 (Pass 1's) | topped up from 2/1/1 |
| chap04 | 5 | 3 | 0 | |
| chap05 | 5 | 3 | 0 | |

**chap03** already carried `function definition` and `header` from Pass 1's tooling
check; topped up with `parameter`, `local`, `traceback` (one per remaining section:
Parameters, Variables and parameters are local, Tracebacks) to reach 5. Prompts: before
the first `for` loop (predict iteration count); before the `NameError` demonstration
(why does displaying `cat` fail outside the function). Its Pass-1 code blank on
`print_lyrics`'s header is unchanged.

**chap04**: blanks on `canvas`, `encapsulation`, `generalization`, `development plan`,
`docstring` — five different sections. Prompts: before the first `for`-loop
simplification of the square-drawing code; after the "`n` is a constant" limitation
paragraph (what happens at a much larger radius); after the precondition/postcondition
paragraph in Debugging (whose bug is it). Zero code blanks: `blank/chap04.ipynb` empties
all 49 code cells already.

**chap05**: blanks on `modulus operator`, `boolean expression`, `chained conditional`,
`recursive`, `infinite recursion` — five different sections, deliberately skipping
`logical operators` and `nested conditional` to stay at the target rather than push to
six. Prompts: before the clock-arithmetic result (predict `(11+3) % 12`); before the
first `countdown` call (predict the output); before the `ValueError` from non-integer
input (what kind of error). Zero code blanks, same reasoning.

**Finding that changes the Pass-1 handoff's expectation:** Pass 1 predicted code blanks
would become more common from chapter 3 onward, once `def` headers and loop bodies give
them something to carry. That hasn't happened in practice: `blank/chapNN.ipynb` empties
**every single code cell** in chapters 4 through 19 (verified directly), and in chapters
1–3 the only code left non-empty is boilerplate (the `download` cell), diagram-plumbing,
the `%xmode`/debug-setup cell, or exercise test-call cells — none of which are things
this pass's rules allow blanking anyway. Expect **zero code blanks to remain the norm**
for the rest of the book, not the exception; the 0–2 target in `CLAUDE.md` should be
read as a ceiling nearly no chapter will need to reach, not a per-chapter quota.

### Step 5 — Per-chapter checkout

- `make check` passes (21 source files — down from 42 now that `chapters/` is
  `.ipynb`-only; `check_sync` clean).
- `make ledger` regenerates with no manual edits; byte-identical across two runs.
- `make projector` regenerated and re-checked clean after every chapter's edits.
- Cell-level diff against `upstream/v3` for each chapter shows exactly the intended
  changes: chap03, 8 cells edited + 1 deleted; chap04, 8 edited + 2 deleted; chap05, 11
  edited + 12 deleted. No insertions (every change is an edit-in-place or a deletion —
  the one new exercise reuses an existing cell rather than adding one), no whitespace or
  formatting drift.
- All three files: zero `virtual assistant` mentions remain; zero cell outputs or
  execution-count changes (verified against both `HEAD` and `upstream/v3`), consistent
  with the notebook-hygiene approach from the chapters 1–2 gate (add none of our own;
  the whole-book `nbstripout` question from that gate is still open, unaffected by this
  batch).
- `git status` shows nothing added or modified under `blank/`.

### Ledger

87 entries, up from 83. Six additions: `ch03-va01`, `ch04-va01`, `ch05-va01` (kind B,
removed, 0 minutes, matching the chapters 1–2 pattern) and `ch05-ex07` (kind native,
added, `replacement_id: "ch05-ex06"`, 20 minutes). Three existing entries moved from
`kept` to `edited`: `ch05-ex04` and `ch05-ex05` (kind-C removals) — `ch03`'s kind-C
removal wasn't inside any ledgered exercise (it's expository prose in the Stack diagrams
section, not an exercise), so no chap03 exercise entry needed an action change there.
`ch05-ex06` moved from `kept` to `removed`. No IDs renumbered.

### Handoff to the rest of the batch (chapters 6–8) and to the next gate

- **Open classification question, needs a ruling before it's forgotten:** is the
  chap05 countdown_by_two VA vignette (inside the removed kind-B block) actually a
  second kind-A exercise? See Step 1 above. This determines whether a fifth replacement
  is owed anywhere in the book.
- **chap07 carries two of the remaining three kind-A replacements** (`ch07-ex06`,
  `ch07-ex07`, both doctest-based per Pass 1's notes — write their replacements the same
  way, with `self_verifying: true`). That's the next chapter with exercise-authoring
  work, not chapter 6 or 8.
- **Code blanks: stop expecting them.** Confirmed zero-code-blank is the norm through
  at least chapter 19's `blank/` directory (all code cells emptied). Don't budget time
  for hunting good code-blank candidates in 6–8 unless a chapter's `blank/` version
  turns out to be the exception — check first, the way this pass did for chap04/05.
- The two open items from the chapters 1–2 gate (the unclassified chap01/chap00
  virtual-assistant mentions in body prose, and the notebook-hygiene vs.
  small-diffs tension) are both still open and untouched by this batch.
- The pacing/buffer question from Pass 1 remains open and undecided.
- Nothing in chapters 3–5 tempted a restructure beyond what's logged above. The Koch
  and `ch05-ex04` kind-C removals both closed cleanly on their own, same as chapters 1–2.
---

## 2026-07-30 — Modification footer (all chapters, cross-cutting)

Every file in `chapters/` (chap00–chap19, jupyter_intro — 21 files) now carries a
`type="note"` sentinel appended to the existing Downey copyright/license footer,
attributing the modifications to Eric Brown for a high school CS class and linking to
`github.com/porttack/ThinkPython`. No email address, by request (public repo). Applied
uniformly to every chapter regardless of which pass has touched it — so chapters not
yet reached by Pass 2 (6–19) will show one sentinel block (this footer note) before any
other surgery happens to them. Not a per-chapter checkout item; no ledger entry, since
it isn't exercise-related. `make check` clean; cell counts and outputs unchanged in
every file (verified against `HEAD` before this change).

---

## 2026-07-30 — Pass 3, Step 1 (AP index) — stopped at the Step 1 gate by request

Ran only Step 1 of `mods/pass-3-alignment.md`: built `standards/apcsp.json` from
`standards/ap-computer-science-principles-course-and-exam-description-2023.pdf` (262 pages,
"Effective Fall 2023" / V.1). Stopped after Step 1 as instructed — Steps 2-5 (California
index, crosswalk/alignment docs, standards inserts, appendices) were **not started**, not
because anything blocked them (`standards/csstandards.pdf` is present, so Step 2 is
unblocked whenever this resumes).

### What's in the index

35 topics across all 5 Big Ideas, 66 learning objectives, every LO code cross-checked
against a full-document regex sweep of the PDF (zero missing either direction). Weights
verified against the CED's own tables (both the multiple-choice-by-big-idea table on
Course Framework p.18/163 and the by-practice table on Exam Information p.164) and they
match the shape this file predicted exactly: CRD 10–13, DAT 17–22, AAP 30–35, CSN 11–15,
IOC 21–26. Practice weights: P1 18–25, P2 20–28, P3 7–12, P4 12–19, P5 28–33, P6 not on the
MCQ at all (Create Performance Task only).

**Topic → LO mapping was not trusted from the "Big Idea at a Glance" summary tables
alone.** Those tables' multi-column layout collapses under `pdftotext`, and two boundary
cases came out wrong on first read: Big Idea 5's 5.2–5.6 row order, and (less seriously)
whether AAP-2.I belongs to 3.6 or 3.7. Every LO-to-topic assignment in the JSON was
verified against that topic's own detail page, not the summary table alone — this matters
if anyone re-extracts from a future CED revision using the same tool: the summary table is
a fast first pass, not a source of truth by itself.

### Every `unassigned` topic (7), as required

- **1.1 Collaboration** — no pair-programming/collaborative-workflow content in the book.
  Possibly realized as a classroom practice rather than book content; that's a Step 3
  supplement-plan call, not decided here.
- **2.1 Binary Numbers**, **2.2 Data Compression** — confirmed not carried, consistent with
  `CLAUDE.md`'s own framing of what this book carries of Big Idea 2.
- **3.11 Binary Search** — the book teaches **linear search** by name (chap07) but never
  introduces binary search, not even conceptually. No `bisect`, no sorted-list-halving
  example anywhere. This is a real content gap against a topic the CED requires, not
  something the AAP-2.P.1 exclusion (implementation details only) covers.
- **3.16 Simulations** — no dedicated simulation content in chapters 1–13. The word only
  appears in chap19 (independent-study range). chap12's random-number work is adjacent
  but isn't the same idea.
- **3.17 Algorithmic Efficiency** — no informal-efficiency discussion anywhere in
  chapters 1–13. "Efficient"/"sufficient" hits elsewhere in the book are incidental.
- **3.18 Undecidable Problems** — not carried at all; a non-programming conceptual topic.

### Load-bearing finding beyond the "every unassigned topic" list

**3.8 Iteration (AAP-2.J/K) is only half-carried, and it isn't flagged by the exclusion
mechanism.** The exam reference sheet gives this topic two pseudocode forms: `REPEAT n
TIMES` (definite, matches Python's `for`) and `REPEAT UNTIL(condition)` (indefinite,
matches Python's `while`). **This edition of the book has no `while` loop anywhere** —
confirmed by scanning every code cell in chapters 1–13 for the token, zero hits outside
incidental English "while." Indefinite repetition is instead handled through recursion
(chap05, chap06), which is a real conceptual substitute but not the same construct on the
exam, and doesn't produce the `REPEAT UNTIL`-specific edge cases the CED calls out
(AAP-2.K.4 infinite loop from a condition that never turns true; AAP-2.K.5 zero-iteration
when the condition is already true going in). Whether to add a short `while`-loop
supplement or treat recursion as sufficient coverage is a real pedagogical call — raising
it here rather than deciding it, per `CLAUDE.md`'s "raise rather than decide" list (this is
close to "a standard has no plausible carrier," just partial rather than total).

### Exclusion statements found (8 total, all in the JSON; 6 beyond the two known ones)

Known going in: linked lists (AAP-1.D.6, on 3.2) and specific binary-search
implementations (AAP-2.P.1, on 3.11). Six more found by grepping every
"EXCLUSION STATEMENT" occurrence in the PDF and deduplicating against Appendix 2's repeat
of the same content: real-number range limits (DAT-1.B.3, on 2.1); parallel traversal of
two lists with a shared index (AAP-2.O.1, on 3.10); formal Big-O analysis (AAP-4.A.3, on
3.17); specific heuristic solutions (AAP-4.A.9, on 3.17); determining undecidability itself
(AAP-4.B.2, on 3.18); specific encryption/decryption math (IOC-2.B.5, on 5.6, Little
Brother's territory not this book's, recorded anyway since the index covers the whole
framework).

### `class_periods`

Left `null` for all 35 topics, by design rather than extraction failure: the CED's Course
at a Glance table has no per-topic time-estimate column at all. The numbers printed next
to each topic in that table are Computational Thinking Practice references (1–6, matching
the six practices' names), not period counts. Recorded once in `meta.class_periods_note`
rather than repeated 35 times in the topic array.

### For a future maintainer, when the CED is revised

- Don't trust the "Big Idea at a Glance" table's topic→LO grouping without cross-checking
  each topic's own detail page — see the boundary-case note above.
- The full-document LO-code regex sweep (`\b(CRD|DAT|AAP|CSN|IOC)-[0-9]\.[A-Z]\b`, deduped)
  is a fast way to get a checksum: this pass's JSON accounts for all 66 codes found that
  way, in both directions, with no gaps.
- The 8 exclusion statements appear twice each in the source PDF (once in the Big Idea
  guide, once in Appendix 2's "Conceptual Framework" restatement) — `grep -c` will report
  16, not 8; dedupe by EK code before treating a change in count as a real CED revision.

### What's still open

- Steps 2–5 not started: California index, crosswalk, `standards_alignment.md`,
  `supplement-plan.md`, `glossary-map.md` (including the scope question about chapters
  14–19), standards inserts, and both appendices. All unblocked whenever this resumes —
  `standards/csstandards.pdf` is present.
- The three `unassigned`/gap topics above that read as real pedagogical decisions (3.8
  partial, 3.11, 3.16, 3.17 missing entirely) should probably inform the Step 3 scope
  question and supplement plan directly, not just sit in the JSON.
- Pass 2 (chapter surgery) and its open items are untouched by this pass and remain as
  Pass 2 left them.

---

## 2026-07-30 — Pass 3 follow-up: AP index corrections + Step 2 (CA index) — stopped at the Step 2 gate

### Corrections to `standards/apcsp.json` from the Step 1 gate

- **`meta.mcq_format` had a real arithmetic error**: it read "65 single-select ... plus 8
  multi-select" alongside the 5-question reading-passage set, which sums to 78, not the
  70 questions the exam actually has. Rechecked against the CED's exam-format table
  (Exam Information p.163): the breakdown is **57** individual single-select + **8**
  individual multi-select (65 individual questions total) + **1 set of 5** single-select
  questions tied to a reading passage = 70. The reading-passage set is additional to the
  65 individual questions, not additional to a 65-question single-select count — the "65"
  in the CED's own prose ("70 total questions, including 65 individual questions and one
  set of five...") is single-select-plus-multi-select combined, not single-select alone.
  Fixed; both the CED's summary sentence and its own table now agree with the corrected
  field.
- **All 7 `unassigned` topics reassigned to `carrier: "supplement"`** with a note on
  where each is actually taught, per direction: 2.1 Binary Numbers and 2.2 Data
  Compression → CS50T Multimedia; 3.11 Binary Search, 3.16 Simulations, 3.17 Algorithmic
  Efficiency, 3.18 Undecidable Problems → the November algorithms block; 1.1
  Collaboration → continuous, through lab pair work and the Create Performance Task, not
  a standalone lesson. Zero `unassigned` topics remain in `standards/apcsp.json`.

### Step 2 — `standards/castandards.json`

Built from `standards/csstandards.pdf` (270 pages, CDE, framework-alignment updates
through Nov. 2023). **Extraction matched the expected shape exactly, no disagreement to
report**: five strands, thirty core 9-12 standards (CS.1–3, NI.4–7, DA.8–11, AP.12–22,
IC.23–30). A separate, non-core "9-12 Specialty" set (`9-12S.*`) exists in the same
document for a more advanced pathway; confirmed it's genuinely a different standard set
(its own numbering, its own section header "9–12 Specialty" starting right after IC.30)
and left it out of the index, since Step 2 only asked for the 30 core standards.

**Carrier counts**: 7 `thinkpython`, 12 `little_brother`, 3 `supplement`, 8 `unassigned`.

- `little_brother` (12): all 4 NI standards, all 8 IC standards. Matches `CLAUDE.md`'s
  course context directly — it names CA's NI and IC strands specifically as Little
  Brother's territory, so this wasn't a judgment call.
- `supplement` (3): **DA.8** and **DA.9** — same real-world content as AP's DAT-1.A/DAT-1.D
  (binary data representation, compression tradeoffs; DA.9's own worked example is
  image-format size-vs-quality, which *is* compression), so given CS50T Multimedia carries
  those on the AP side, it carries these too. **AP.21** — same collaboration/team-roles
  practice as AP CRD-1.1, so it gets the same "continuous, via lab pairing and the CPT"
  note. These three are inferences from this session's AP carrier decisions, not separate
  instructions for the CA framework — flagging that distinction so it can be pushed back
  on if the reasoning doesn't hold.
- `thinkpython` (7): AP.12 (chap07 linear search + chap09 sort), AP.13 (chap09 Lists),
  AP.14 (chap05/chap06 — the CED's own worked example for this standard is recursive vs.
  iterative Fibonacci, and chap06 has a section literally named "Fibonacci"), AP.16
  (chap03/chap04 procedures; classes in chap14–19 carry the rest but sit outside the
  Aug–Dec sequence), AP.17 (chap02/chap04/chap08, same library evidence as AP AAP-3.D),
  AP.20 (chap04/chap07, testing and iteration — but not its usability/accessibility
  clauses), AP.22 (chap04, in-code documentation only, not the presentation/graphics
  forms this standard also names).
- `unassigned` (8), every one flagged: **CS.1**, **CS.2** (hardware/systems abstraction,
  no carrier in either framework as scoped), **CS.3** (troubleshooting — the standard's
  own examples are network/help-desk scenarios, not code debugging; deliberately not
  claimed by the book's Debugging sections, which carry AP CRD-1.4 instead, a different
  skill), **DA.10** (data visualization — no charting/plotting content anywhere in the
  book), **DA.11** (validating a computational model against real data — chap12's Markov
  model is adjacent but the chapter never validates or refines it against real-world
  data), **AP.15** (event-driven/GUI programming — every program in the book runs
  top-to-bottom to completion, no event loop anywhere), **AP.18** (design incorporating
  user feedback from a broad audience — chap04's development plan is solo and technical,
  never audience-facing; distinct from AP.21's teammate-collaboration gap), **AP.19**
  (software license limitations — same gap as AP CRD-2.H already flagged in the AP index;
  the book uses libraries in chap04/chap08 but never discusses their licensing terms).

### For a future maintainer

- The CS.3 vs. CRD-1.4 distinction (troubleshooting-in-general vs. code-debugging-
  specifically) is subtle and easy to blur in the crosswalk — worth a deliberate note
  there rather than letting `CS.3` quietly inherit `CRD-1.4`'s `thinkpython` carrier.
- The three CA `supplement` assignments above are this session's inferences from the
  already-decided AP carriers, not independently confirmed against the same source the
  AP assignments came from (a direct instruction naming where each is taught). Worth a
  quick confirm before Step 3 treats them as settled.

### What's still open

- Steps 3–5 not started: crosswalk (`standards/crosswalk.json`), the three
  `alignment/*.md` docs (including the Step 3 scope question about chapters 14–19),
  standards inserts, and both appendices. Nothing blocks Step 3 now that both indexes
  exist.
- Everything listed as still-open in the Step 1 handoff above remains open (the 3.8
  iteration gap, the four fully-unassigned-in-AP topics now carried as `supplement`, and
  Pass 2's untouched items).

---

## 2026-07-30 — Pass 3, Step 3 (crosswalk + alignment docs) — stopped at the Step 3 gate

Built `standards/crosswalk.json` and all three `alignment/*.md` docs from the two indexes.
Stopped after Step 3 as instructed. Steps 4–5 (standards inserts, appendices) not started.

### Crosswalk: counts and where the frameworks diverge

33 rows. **18 strong, 8 partial, 6 related.** Deliberately not exhaustive — pairs with no
honest correspondence are left out of the file and covered instead as gaps in
`alignment/standards_alignment.md`, per the instruction to be honest about strength
rather than force full coverage.

The 6 `related` rows are the ones worth reading over the others; each is a case where two
similar-sounding standards turned out, on close reading, not to test the same thing:
- **AP 1.4 vs. CA CS.3** — both nominally "troubleshooting," but CS.3's own examples are
  network/help-desk scenarios, not code debugging. Kept apart deliberately so the book's
  Debugging sections don't get credited for a systems-level skill they don't teach.
- **AP 3.11 (Binary Search) vs. CA AP.12** — AP CSP names binary search as its own
  required topic; CA's parallel standard only says "searching and sorting algorithms"
  generically, satisfiable by linear search alone. The book's binary-search gap is a
  sharper problem for AP than for CA.
- **AP 3.15 (Random Values) vs. CA AP.12** — CA folds randomization into its algorithms
  standard rather than giving it a dedicated topic the way AP CSP's 3.15 does.
- **AP 3.16 (Simulations) vs. CA DA.11 (model refinement)** — sound adjacent, aren't:
  AP's is about trading off realism for repeatability/cost, CA's is about validating a
  model against real observations. Flagged so these two gaps aren't treated as one
  problem needing one fix.
- **AP 4.2 (Fault Tolerance) vs. CA NI.6 (security)** — adjacent within Networks, not the
  same idea; doesn't matter for this book since both are Little Brother's territory.
- **AP 1.1 (Collaboration) vs. CA IC.27** — same rough territory, filed under different
  big ideas on each side (CRD vs. IC), with mismatched carriers on this book's side (1.1
  is supplement/CPT, IC.27 is little_brother).

**Two `strong` rows flag matching gaps rather than matching coverage** — worth calling
out separately since a "strong" match usually means "well covered," not here: AP
CRD-2.H and CA AP.19 are the *same uncarried gap* (crediting/licensing borrowed code),
and AP 1.1 / CA AP.21 are the same *carried-by-practice-not-book* item (collaboration).

### The scope question (Step 3's central deliverable) — answered with evidence

**No**, chapters 14–19 are not required by any CA 9–12 core standard. The two CA
standards that could plausibly demand OOP (`AP.16`, decomposition; `AP.17`, modular
design) both phrase classes as one option among several ("procedures, modules, **and/or**
classes" — CA's own wording), not a requirement, and both are already fully satisfied by
chapters 2–4 and 8 alone. Cross-checked against View 1 of `standards_alignment.md`:
chapters 14–19 carry zero AP or CA topics under the current mapping, and nothing in
either 30-or-35-item index changes that conclusion. Stated as evidence, not decided as
policy, per the pass file's instruction — a teacher could still have non-standards
reasons to move OOP earlier, but standards coverage doesn't compel it.

### What a future maintainer needs to know

- The crosswalk is intentionally lopsided toward Big Ideas 1–3 / CS, DA, AP strands,
  where this book's actual decisions live. Big Ideas 4–5 / NI, IC strands got a lighter
  pass (block-level "both Little Brother" rows, not exhaustive sub-topic matching) since
  neither framework routes that content through this book — spending more effort there
  wouldn't change any decision this project can make.
- `alignment/supplement-plan.md`'s "no assigned carrier anywhere" list (7 items: AP
  CRD-2.H/CA AP.19, CA AP.15, CA AP.18, CA CS.1/CS.2/CS.3, CA DA.10, CA DA.11) is the
  actual punch list if someone wants to close remaining gaps — small enough to patch
  individually, not large enough to justify a new supplement course the way CS50T
  Multimedia or the November block do.
- The AP 3.8 / CA AP.14 iteration finding (no `while` loop in the book) is reiterated a
  third time now, across the AP index, the CA crosswalk, and both alignment docs. That
  repetition is deliberate, not an oversight — it's the finding most likely to get lost
  if a reader only skims one of the four documents.

### What's still open

- Steps 4–5 not started: standards inserts (one per chapter, `type="standards"`
  sentinel, back matter) and the two appendices (`pseudocode-crosswalk.md`,
  `cs50p-map.md`). Both unblocked — everything they need now exists in the three JSON
  files and three alignment docs.
- The exercise-ledger backfill (`targets_ap`/`targets_ca` for Pass 2's replacement
  exercises, part of Step 4) is also still outstanding.
- Everything still open from the Step 1 and Step 2 handoffs above remains open.
