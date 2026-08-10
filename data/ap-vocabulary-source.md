# AP CSP Vocabulary — Source of Truth

**Course:** AP Computer Science Principles, 5th period, 2026–27
**Teacher:** Eric Brown, SLVHS, room C103
**Status:** Working draft. This file is the single source; downstream artifacts are generated from it, not edited independently.

---

## 1. What this file is for

This is a data file, not a handout. Hand it to a coding agent and ask for one of the build targets in §6. Every artifact regenerates from this table, so a correction here propagates rather than forking.

### Course constraints any generated artifact must respect

- **Python-first.** Students learn Python (forked *Think Python 3e*, JupyterLite at python.porttack.com) before they see College Board pseudocode. Every place the two diverge is a predictable error, not a student failing. Those divergences are marked in the `Note` column and collected in §4.
- **No AI tools in the classroom.** School policy. Student-facing material must contain no instruction to consult an AI assistant, and no "ask ChatGPT if stuck" scaffolding.
- **Binder-bound.** Glossary lives behind a tab in a 1" round-ring binder that stays in the room. Print artifacts must be single-sided-safe, hole-punch-safe (0.75" left margin minimum), and legible in black and white.
- **Attribution.** Course materials derive in part from Allen Downey's *Think Python 3e* under CC BY-NC-SA 4.0. Any printed packet carries the attribution line. This matters extra because copyright and Creative Commons are taught in March.
- **Cohort:** ~15 students, most also in the ROV/robotics course.

### Instructional priority

Last year's exam analysis: submitted Create Task components were near-perfect; **exam-day written responses (WR1, WR2a/b/c) were the gap**, including among stronger students. Vocabulary work should bias toward terms that appear in *prompt language* over terms that appear in *answer keys*. See the `WR` flag.

---

## 2. Column key

| Column | Values | Meaning |
|---|---|---|
| **Tier** | `C` / `L` / `F` | **C**oncept: a genuinely new idea; needs instruction time. **L**abel: the AP name for something students already do in Python; costs about 90 seconds. **F**act: lookupable, no mental model required; counts for coverage, never gets a warm-up slot. |
| **HF** | `★` | Flagged high-frequency by apcsexamprep.com's CSP list. Frequency ≠ instructional cost — many `★` terms are Tier L. |
| **KA** | `✓` | Appears in Khan Academy's AP CSP vocabulary review, which students do independently for the non-programming Big Ideas. Blank means *you are the only source*. |
| **WR** | `✎` | Appears in written-response **prompt** language. Highest instructional value given last year's results. |
| **Note** | prose | Python divergence, common misconception, or teaching hook. Blank is fine. |

**Teach list = every row where Tier is `C`.** Everything else lives in the glossary for reference and coverage accounting.

---

## 3. The terms

### Big Idea 1 — Creative Development

| Term | Tier | HF | KA | WR | Definition | Note |
|---|---|---|---|---|---|---|
| Algorithm | C | ★ | | ✎ | A finite sequence of steps that solves a problem or completes a task. Can be written in English, pseudocode, or code. | Students conflate this with "program." An algorithm is the plan; a program is one implementation of it. |
| Program | L | | | ✎ | A collection of statements that performs a task when run. | |
| Program purpose | C | | | ✎ | What problem the program solves or what need it serves — the *why*. | Not on any published list. It is the literal opening of WR1 and students answer it vaguely. Teach purpose/function/input/output as one four-part frame, not four terms. |
| Program function | C | | | ✎ | What the program does when it runs — the *what*, described behaviorally. | Students describe features instead of behavior. "It has a scoreboard" is not a function statement. |
| Program input | C | | | ✎ | Data the program receives while running: user action, file, sensor, network, another program. | Must be *at runtime*. Hard-coded values are not input. |
| Program output | C | | | ✎ | What the program produces: display, sound, file, movement, data sent elsewhere. | |
| Code segment | L | | | ✎ | A portion of a program, one or more lines, treated as a unit. | WR2 asks about a "code segment" by name. Students need to know they are being asked to point at specific lines. |
| Computing innovation | C | | | ✎ | A product, service, or concept that includes a program as an integral part of its function. May be physical, software, or conceptual. | The "includes a program" clause is load-bearing. A bridge is not a computing innovation; a bridge with a load-monitoring system is. |
| Collaboration | L | | | | Working with others to develop a computing innovation; benefits from varied perspectives and skills. | |
| Pair programming | L | | | | Two programmers at one workstation: one drives, one reviews and thinks ahead. | Already the classroom norm. Just attach the name. |
| Program documentation | L | | | ✎ | Written description of what a segment, procedure, or program does and how it was built. | |
| Comments | L | | | ✎ | Documentation written inside the code for human readers; ignored at execution. | Comments are graded in this course, so the term is already lived. |
| Debugging | C | | | | The process of finding and fixing errors in a program. | Missing from all three published lists despite being the daily activity. Name it so students can talk about it. |
| Syntax error | C | ★ | ✓ | | A violation of the language's grammar rules; the program typically will not run at all. | Teach as a three-way contrast with logic and run-time, not separately. |
| Logic error | C | ★ | ✓ | | The program runs but produces the wrong result. | Hardest of the three to detect, because nothing complains. |
| Run-time error | C | | ✓ | | An error that appears only during execution, such as dividing by zero. | Python raises these as tracebacks; connect the term to what they already see on screen. |
| Overflow error | C | ★ | ✓ | | The value is outside the range representable in the available bits. | Python's ints are arbitrary precision, so students never see this natively. Needs a deliberate demo. |
| Roundoff error | C | | ✓ | | Loss of precision because a fixed number of bits cannot represent a real number exactly. | `0.1 + 0.2` in the console does this work for you. |
| Testing | L | | | | Verifying a program behaves correctly by running it with defined inputs. | |
| Test case | C | | | ✎ | A specific input paired with its expected output. Good sets include typical, boundary, and edge values. | Maps directly onto the doctest format and Bootstrap's design recipe (contract → examples → definition). Boundary and edge are the part students omit. |
| Hand tracing | C | | | | Manually stepping through code, tracking variable values, to locate an error. | Python Tutor is the visualization; hand tracing is the paper version, and the exam only has paper. |
| Iterative development | C | | | ✎ | Repeated cycles of build, feedback, and revision; earlier phases get revisited. | Teach with incremental as a pair — students merge them into "we kept working on it." |
| Incremental development | C | | | ✎ | Breaking a problem into pieces and confirming each works before integrating. | |
| Event | L | | | | An action supplied to a program as input: key press, click, sensor reading. | |
| Event-driven programming | L | | | | Statements execute in response to events rather than in top-to-bottom sequence. | The micro:bit opener and CMU-style graphics both demonstrate this before the term is needed. |

### Big Idea 2 — Data

| Term | Tier | HF | KA | WR | Definition | Note |
|---|---|---|---|---|---|---|
| Binary | L | ★ | | | Base-2 representation using only 0 and 1. | |
| Bit | F | | ✓ | | A single binary digit. | |
| Byte | F | | ✓ | | Eight bits. | |
| Hexadecimal | F | | | | Base-16, using 0–9 and A–F; four bits per digit. | Keep for the color-code and CRC32 work, not for the exam. |
| Decimal | F | | | | Base-10. | Cut candidate. Earns a glossary row only for symmetry with binary and hex. |
| Abstraction | C | ★ | | ✎ | Reducing complexity by exposing essential features and hiding implementation detail. | The single most important word in the course and the one students define circularly. Every other abstraction term below is a special case of this one. |
| Analog data | C | | ✓ | | Values that vary continuously and smoothly. | Teach as a contrast pair with digital; separately they are near-empty. |
| Digital data | C | | | | Values represented in discrete steps, ultimately as bits. | |
| Sampling | C | | | | Approximating an analog signal by measuring it at regular intervals. | Rate and bit depth are the two knobs. Students think only about rate. |
| Lossless compression | C | ★ | ✓ | | Reduces size while allowing exact reconstruction of the original. | Contrast pair with lossy. The exam tests the *choice between them*, not the definitions. |
| Lossy compression | C | ★ | ✓ | | Reduces size further, but only an approximation can be recovered. | |
| Metadata | C | ★ | ✓ | | Data describing other data: creation date, size, author, location, format. | Photo EXIF is the demo that lands. Connects directly to the *Little Brother* and PII threads. |
| Data | F | | | | Values that can be stored and processed by a program. | Cut candidate — near-free definition. |
| Information | C | | | ✎ | Meaning, patterns, or insight extracted from data. | Taught only as the contrast with data. That contrast is genuinely tested. |
| Data set | F | | | | A collection of related data organized for analysis. | |
| Correlation | C | | | ✎ | An association between two variables where changes in one accompany changes in the other. | The whole lesson is "correlation is not causation," and it is worth the full period. |
| Data cleaning | C | | | ✎ | Making data uniform and consistent without changing its meaning. | Students think this means deleting rows they dislike. It does not. |
| Data filtering | L | | | | Selecting a subset of data by defined criteria. | |
| ASCII | F | | | | A 7-bit character encoding covering 128 characters. | |
| Unicode | F | | | | A character encoding standard covering the world's writing systems; extends ASCII. | |
| RGB | F | | | | Color represented as red, green, and blue channels, typically 0–255 each. | |
| Pixel | F | | | | The smallest addressable color element of a display or image. | |

### Big Idea 3 — Algorithms and Programming

| Term | Tier | HF | KA | WR | Definition | Note |
|---|---|---|---|---|---|---|
| Variable | L | ★ | | ✎ | A named location holding a value that can change through assignment. | |
| Constant | L | | | | A named value that does not change during execution. | |
| Data type | L | | | | The classification of a value, determining what operations apply. | |
| Integer | F | | | | A whole number. | |
| String | L | | | | An ordered sequence of characters. | |
| Boolean | L | | | | A value that is either true or false. | |
| Boolean expression | C | | | ✎ | An expression that evaluates to true or false. | Distinct from the Boolean *type*. Students who only know the type cannot parse "the Boolean expression in line 4." |
| Expression | L | | | | A combination of values, variables, operators, and calls that evaluates to a single value. | |
| Assignment | L | | | | Storing a value in a variable. | Pseudocode uses `←`. Recognition only; they never have to write it. |
| List | C | ★ | | ✎ | An ordered sequence of elements, each reachable by index. | **Indices start at 1 in College Board pseudocode and 0 in Python.** This is the single biggest trap for a Python-first cohort. Attach the convention to this row rather than making it its own term. |
| Element | L | | | ✎ | One item stored in a list. | Distinct from index. WR2 prompts use both words in one sentence. |
| Index | L | | | | The position of an element within a list. | See the List note. |
| Substring | F | | | | A contiguous portion of a string. | |
| Concatenation | F | | | | Joining strings end to end. | |
| Sequencing | L | ★ | ✓ | | Executing steps in the order written. | Tier L, but they must be able to *name* it — the exam asks which construct a segment demonstrates. |
| Selection | L | ★ | ✓ | | Choosing between paths based on a condition. | |
| Iteration | L | ★ | ✓ | | Repeating steps a set number of times or until a condition is met. | `REPEAT UNTIL (condition)` **exits** when the condition is true. Python's `while` **continues** when true. Inverted sense; put this note on the row rather than teaching the keyword. |
| Nested conditional | L | | | | A conditional inside another conditional. | |
| Compound conditional | C | | | ✎ | A single condition combining multiple Boolean expressions with AND, OR, or NOT. | Not covered by "nested." Students merge the two and then mis-answer questions that hinge on the difference. |
| Relational operators | F | | | | Comparison operators: =, ≠, >, <, ≥, ≤. | |
| Logical operators | L | | | | AND, OR, NOT. | The truth-table drill is worth one warm-up cycle, especially NOT applied to a compound. |
| MOD | C | | | | The remainder after integer division. | Kept despite looking like notation — the concept is tested. Even/odd and cycling are the two uses. Negative operands behave unintuitively; worth a distractor. |
| Infinite loop | L | | | | A loop whose ending condition never becomes true. | |
| Procedure | C | ★ | ✓ | ✎ | A named, reusable block of code that performs a task and can be called repeatedly. | AP says procedure; Python says function; the ROV course says method. Say all three out loud once, early. |
| Parameter | C | | | ✎ | A named variable in a procedure's definition that receives an input value. | Contrast pair with argument. Bootstrap's design recipe maps this cleanly: parameter = domain, return value = range. |
| Argument | C | | | ✎ | The actual value supplied for a parameter at the call site. | Students use the two words interchangeably all year unless corrected in week one. |
| RETURN statement | L | | | ✎ | Exits a procedure immediately and hands a value back to the caller. | The classic misconception is that `return` prints. |
| Procedural abstraction | C | | | ✎ | Naming a process so it can be used knowing *what* it does without knowing *how*. | WR2b routinely asks students to explain this about their own code. Practice on their own Create Task drafts, not on generic examples. |
| Data abstraction | C | | | ✎ | Using a data structure, typically a list, to represent related values as one named unit, hiding the individual pieces. | Missing from the original list and a standing WR2 target. The exam wants: what does the list represent, and how does using it manage complexity? |
| Modularity | L | | ✓ | | Dividing a program into independent parts each responsible for one aspect. | |
| Software library | L | | ✓ | | A collection of pre-written procedures available for reuse. | |
| API | L | | ✓ | | The specification of how a library's procedures are called and how they behave. | |
| RANDOM(a, b) | C | | | | Returns a random integer from a to b, **inclusive on both ends**, each equally likely. | `random.randint` matches this; `random.random` and `range` do not. Off-by-one on the upper bound is a reliable distractor. |
| Simulation | C | | | ✎ | An abstraction of a real phenomenon using varying values to represent changing states, run for a purpose. | The exam cares about *why simulate*: cost, risk, time, or repeatability. Students answer "because it's easier." |
| Traversal | C | | ✓ | ✎ | Iterating over the items of a list. Full traversal visits every element; partial stops early. | The full/partial distinction is the tested part. |
| Linear search | C | ★ | ✓ | | Checking each element in turn until the target is found or the list ends. | Contrast pair with binary search. |
| Binary search | C | ★ | ✓ | | Repeatedly halving a **sorted** list to locate a value. | The sorted precondition is the whole question. Students skip it. |
| Algorithmic efficiency | C | | | ✎ | An estimate of the computational resources an algorithm uses as a function of input size. | |
| Reasonable time | C | | ✓ | | Run time that grows polynomially or slower with input size. | Khan defines this with polynomial-vs-superpolynomial language, which is more precise than the CED requires. Your students will have seen that framing. |
| Unreasonable time | C | | | | Run time that grows exponentially or factorially with input size. | |
| Heuristic | C | | ✓ | ✎ | An approach that finds a good-enough solution when finding the optimal one is impractical. | Flagged in the TODO as needing multiple passes. Not high-frequency on the published list, but genuinely hard, and the definition students give is usually "a guess." |
| Decidable problem | C | | | | A yes/no problem for which an algorithm can always produce the correct answer. | Contrast pair with undecidable. |
| Undecidable problem | C | | ✓ | | A problem for which no algorithm can always give a correct yes/no answer for every input. | Halting problem. Students think it means "very hard." |

### Big Idea 4 — Computing Systems and Networks

| Term | Tier | HF | KA | WR | Definition | Note |
|---|---|---|---|---|---|---|
| Internet | C | ★ | | | A network of interconnected networks using standardized open protocols. | Teach as a contrast pair with the Web. The exam tests the distinction directly. |
| World Wide Web | C | | ✓ | | A system of linked pages and files that runs *on top of* the Internet using HTTP. | |
| Computer network | L | | ✓ | | Interconnected computing devices able to send and receive data. | |
| Computing device | F | | ✓ | | A physical artifact that can run a program. | |
| Computing system | F | | | | A group of computing devices and programs working together. | Distinct from device. Low cost, occasionally tested. |
| Packet | L | ★ | | | A chunk of data carrying metadata such as its destination, sent across a network. | |
| Packet switching | C | | | | Splitting a message into packets that travel independently, possibly by different routes, and are reassembled at the destination. | The term is the concept. Having "packet" and "routing" separately does not get you here. |
| Routing | L | | | | Determining a path from sender to receiver across a network. | |
| Bandwidth | F | | ✓ | | Maximum data transmittable per unit time, in bits per second. | Students confuse this with latency. One sentence fixes it. |
| Protocol | L | | ✓ | | An agreed set of rules governing system behavior. | |
| Open standard | C | | | ✎ | A publicly available specification that anyone may implement without permission or fee. | This is *why* the Internet scales and interoperates, and it is the expected phrasing in network answers. |
| TCP | F | | ✓ | | Transport protocol providing reliable, ordered delivery with retransmission. | |
| UDP | F | | ✓ | | Lightweight transport protocol with minimal error checking; faster, less reliable. | |
| IP | F | | ✓ | | Protocol for addressing devices and routing packets between them. | |
| IP address | F | | | | The unique identifier assigned to a device on a network. | |
| HTTP / HTTPS | F | | ✓ | | The Web's request/response protocol; HTTPS adds encryption in transit. | |
| DNS | F | | | | Translates domain names into IP addresses. | Ch. 16 of *Little Brother* is the DNS tunneling hook, already in the calendar. |
| Router | F | | | | A device that forwards packets between networks toward their destination. | |
| Scalability | C | | ✓ | ✎ | A system's ability to keep working acceptably as demand grows. | |
| Fault tolerance | C | ★ | | ✎ | Continuing to operate when components fail. | Contrast pair with redundancy: redundancy is the mechanism, fault tolerance is the property. Students state them as synonyms. |
| Redundancy | C | | | | Duplicate paths or components that allow operation to continue after a failure. | |
| Sequential computing | L | | | | Operations performed one at a time, in order. | Three-way contrast with parallel and distributed. |
| Parallel computing | C | ★ | ✓ | ✎ | A program split into operations, some performed simultaneously. | |
| Distributed computing | C | | ✓ | | Multiple devices in different locations running parts of one program. | |
| Speedup | C | | ✓ | | Sequential time divided by parallel time. | The arithmetic question appears nearly every year and it is free points. Drill it. |

### Big Idea 5 — Impact of Computing

| Term | Tier | HF | KA | WR | Definition | Note |
|---|---|---|---|---|---|---|
| Beneficial and harmful effects | C | | | ✎ | Every computing innovation has both, and they can fall on different groups of people. | Not a vocabulary word so much as the required shape of an Explore-style answer. Students name only benefits. Belongs in the WR tier regardless. |
| Digital divide | C | ★ | ✓ | ✎ | Unequal access to computing and the Internet across socioeconomic, geographic, or demographic lines. | |
| Bias | C | | | ✎ | Systematic unfairness embedded in an algorithm or in the data it was built from. | Distinguish bias *in the data* from bias *in the design*. The exam accepts either, but students should know which one they are claiming. |
| Crowdsourcing | L | | ✓ | | Gathering input, funding, or labor from many people over the Internet. | |
| Citizen science | F | | ✓ | | Scientific research carried out partly by volunteers using their own devices. | |
| Machine learning | F | | | | Systems that improve at a task from data rather than from explicit programming. | Given the classroom AI policy, expect this to generate discussion. Plan for it. |
| Data mining | F | | | | Analyzing large data sets to find patterns and relationships. | |
| Aggregation of information | C | | | ✎ | Combining separately harmless pieces of data to identify or profile a person. | Not on any published list. It is the central privacy mechanism in *Little Brother* and the most exam-relevant privacy idea after PII. |
| Anonymization | C | | | | Removing identifying details from data — and its limits, since aggregation can re-identify. | Pairs with the row above; teach them together or neither. |
| PII | C | ★ | ✓ | ✎ | Information that identifies or can be linked to a specific individual. | |
| Intellectual property | L | | | | Creative or technical work legally owned by its creator. | |
| Copyright | L | | | | The exclusive right of a creator to reproduce, distribute, and display a work. | |
| Creative Commons | C | | ✓ | | A set of public licenses letting a creator pre-authorize specific reuse under stated conditions. | The course text is a CC BY-NC-SA fork. Use the actual license notice on their own printed book as the example. |
| Open source | L | | | | Software whose source is public and may be modified and redistributed. | |
| Open access | F | | ✓ | | Research or data made available free of access restrictions. | |
| Plagiarism | F | | | | Presenting someone else's work as your own. | |
| Encryption | C | ★ | ✓ | | Encoding data so only holders of the key can read it. | |
| Symmetric key encryption | C | | ✓ | | One shared key both encrypts and decrypts. | Contrast pair with public key. The keygen party already in the calendar is the hook. |
| Public key encryption | C | | ✓ | | A public key encrypts; a different private key decrypts. | The asymmetry is the idea. Students describe it as "two passwords." |
| Authentication | L | | | | Verifying that a user is who they claim to be. | |
| Multifactor authentication | L | | ✓ | | Requiring evidence from two or more categories: knowledge, possession, inherence. | The three categories are the tested part, not the count. |
| Phishing | L | ★ | ✓ | | Tricking a user into revealing private information by impersonating a trusted party. | Cluster with malware, keylogging, and rogue AP. One lesson, four terms, high recognition and low cost. |
| Malware | L | | | | Software intended to damage or take control of a system. | |
| Computer virus | L | | ✓ | | Malware that copies itself, typically by attaching to other programs or files. | |
| Keylogging | L | | | | Recording keystrokes to capture passwords and confidential input. | |
| Rogue access point | L | | ✓ | | An unauthorized wireless access point used to intercept network traffic. | |
| Cookies | F | | ✓ | | Small data files stored by a site to track a user's state or behavior. | |
| Digital certificate | F | | | | A credential issued by an authority binding a public key to an identity. | |
| Certificate authority | F | | | | An organization that issues and vouches for digital certificates. | |

---

## 4. Python-first misconception bank

These are the divergences between what students will have internalized in Python and what the exam expects. Each is a ready-made Peer Instruction question: the wrong answer here is a real mental model, not a careless slip, which is what produces a usable room split.

| # | Divergence | Python belief | Exam reality | Distractor to write |
|---|---|---|---|---|
| M1 | List indexing | `list[0]` is the first element | Pseudocode indices start at **1** | Ask for the third element of a five-item pseudocode list; offer both off-by-one answers |
| M2 | Loop exit sense | `while cond:` **continues** while true | `REPEAT UNTIL (cond)` **exits** when true | Trace a loop where the two readings terminate at different iteration counts |
| M3 | Random bounds | `range(a, b)` excludes `b` | `RANDOM(a, b)` **includes** both ends | Ask how many distinct values `RANDOM(1, 6)` can return |
| M4 | Procedure vocabulary | function, method | **procedure**; **parameter** vs **argument** | Give a call site and a definition; ask which word names which thing |
| M5 | Return vs. print | `print` shows a value, so it "returns" it | RETURN hands a value to the caller; nothing is displayed | Segment whose value is returned but never printed; ask what the user sees |
| M6 | MOD with negatives | intuition says the sign follows the dividend | worth verifying before asserting either way in class | Only use non-negative operands in assessment items unless you have checked the CED's position |
| M7 | Abstraction | "making something simpler" | *hiding detail behind a name* while preserving use | Offer a shortened-but-not-abstracted option as the distractor |
| M8 | Binary search | works on any list | requires the list be **sorted** | Unsorted list where binary search returns a plausible wrong answer |
| M9 | Fault tolerance vs. redundancy | synonyms | redundancy is mechanism; fault tolerance is the resulting property | Scenario with redundancy present but no failover; ask if it is fault tolerant |
| M10 | Data vs. information | synonyms | information is what analysis extracts from data | Raw sensor log vs. the trend derived from it |

---

## 5. Deliberately excluded

Do not re-add these when regenerating artifacts. They were cut on purpose.

**Pseudocode notation block** — `DISPLAY`, `INPUT`, `REPEAT n TIMES`, `REPEAT UNTIL`, `INSERT`, `APPEND`, `REMOVE`, `LENGTH`, `FOR EACH`, `MOVE_FORWARD`, `ROTATE_LEFT`, `ROTATE_RIGHT`, `CAN_MOVE`.

Rationale: the exam supplies a reference sheet, so these are recognition items, not recall items. Teaching them as vocabulary spends instructional minutes on lookup. The *conventions* that survive the cut — 1-based indexing, inverted loop-exit sense, inclusive RANDOM — are attached as notes to List, Iteration, and RANDOM rather than living as their own terms. See §4.

**Also cut:** the robot-grid terms entirely (rarely load-bearing for this cohort). Retained despite looking like notation: `MOD`, `RANDOM(a, b)`, `RETURN`, because each carries a concept rather than a keyword.

---

## 6. Build targets

Ask for these individually. Each regenerates from §3.

### 6.1 Printed glossary (binder tab)
Every row, all tiers, grouped by Big Idea, term and definition only. Alphabetical index of terms with their Big Idea on the last page. Notes column omitted — that is teacher-facing. Leave a blank line under each definition: students rewrite the definition in their own words, which is the point of the tab. Two columns, 10pt minimum, 0.75" left margin for the punch.

### 6.2 Teach list (pacing)
Tier `C` rows only, ~39 entries once contrast pairs are collapsed. Group the pairs explicitly — lossless/lossy, linear/binary, symmetric/public-key, fault tolerance/redundancy, analog/digital, decidable/undecidable, parameter/argument, data/information, Internet/Web — since each pair is one lesson, not two. Output as a checklist against the first-semester TOC once that exists.

### 6.3 Warm-up generator seed
JSON, one object per Tier `C` row: `term`, `big_idea`, `definition`, `wr_flag`, `khan_covered`, `misconception` (null where absent), `pair_with` (null or term). Generator modes: vocabulary recall, code trace, WR prompt practice. Pre-generate into a review queue; no live API calls in class.

### 6.4 Misconception bank
§4 expanded to full Peer Instruction items: stem, four options, correct answer, and a one-line note on what believing each distractor reveals. Target a genuine room split, not a question most students get right — a question everyone answers correctly has no discussion phase and wastes the cycle.

### 6.5 WR-tier drill set
The `✎` rows only, ~30 terms. These are prompt-language terms, and exam-day written response was last year's measured gap. Timed practice, not untimed. Purpose/function/input/output taught as one four-part frame.

---

## 7. Provenance

- Term inventory and high-frequency flags: apcsexamprep.com AP CSP vocabulary list, consulted August 2026. Definitions here are rewritten, not copied.
- Khan coverage flags: Khan Academy AP CSP vocabulary review.
- Additions not on either list: program purpose/function/input/output, data abstraction, debugging, compound conditional, Boolean expression, packet switching, open standard, computing system, aggregation of information, anonymization, element, substring, concatenation, beneficial and harmful effects.
- Course text: *Working in Python*, a fork of Allen Downey's *Think Python* 3e, used under CC BY-NC-SA 4.0. Attribution required on printed materials.
