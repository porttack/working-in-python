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

