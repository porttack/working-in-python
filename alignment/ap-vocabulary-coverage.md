# AP CSP Vocabulary Coverage

**Source of truth:** [`data/ap-vocabulary-source.md`](../data/ap-vocabulary-source.md), a teacher-curated instructional-priority list for this specific course (5th period, 2026–27) — not a generic AP CSP glossary. It carries its own Tier/HF/KA/WR columns; this page adds the one thing that source doesn't have: how each term maps onto *Working in Python*'s own chapters.

**144 terms. 66 Concept (need instruction time), 46 Label (name something already taught), 32 Fact (lookupable, no warm-up slot needed).** Of those, 38 are taught in this book directly or under a documented synonym, 11 have an established home elsewhere in the course, 54 are *Little Brother*'s territory, and 41 have no carrier yet.

## Column key

| Column | Meaning |
|---|---|
| **Tier** | `C` Concept (new idea, needs instruction) / `L` Label (AP's name for something already taught) / `F` Fact (lookup only) |
| **HF** | ★ = high-frequency per a community-compiled AP CSP study list |
| **KA** | ✓ = appears in Khan Academy's AP CSP vocabulary review |
| **WR** | ✎ = appears in written-response prompt language — this course's measured weak spot |
| **WiP** | in book / planned / Little Brother / gap — this book's own coverage, added here |

**Deliberately excluded** (see `data/ap-vocabulary-source.md` §5): the whole exam pseudocode notation block (`DISPLAY`, `INPUT`, `REPEAT n TIMES`, `REPEAT UNTIL`, `INSERT`, `APPEND`, `REMOVE`, `LENGTH`, `FOR EACH`) and the Robot commands (`MOVE_FORWARD`, `ROTATE_LEFT`, `ROTATE_RIGHT`, `CAN_MOVE`) — the exam supplies a reference sheet, so these are recognition items, not vocabulary. `MOD`, `RANDOM(a, b)`, and `RETURN` are kept because each carries a concept, not just a keyword.

## Big Idea 1 — Creative Development (CRD)

25 terms — 8 in book, 3 planned, 0 Little Brother, 14 gap.

| Term | Tier | HF | KA | WR | WiP | WiP term | Ch. | Definition | Note |
|---|---|---|---|---|---|---|---|---|---|
| **Algorithm** | C | ★ |  | ✎ | gap | — | — | A finite sequence of steps that solves a problem or completes a task. Can be written in English, pseudocode, or code. | Students conflate this with “program.” An algorithm is the plan; a program is one implementation of it. *(WiP: Used constantly in the book's own prose but never itself a glossary headword.)* |
| **Program** | L |  |  | ✎ | gap | — | — | A collection of statements that performs a task when run. | *(WiP: Same as Algorithm: everywhere, never its own headword.)* |
| **Program purpose** | C |  |  | ✎ | gap | — | — | What problem the program solves or what need it serves — the *why*. | Not on any published list. It is the literal opening of WR1 and students answer it vaguely. Teach purpose/function/input/output as one four-part frame, not four terms. |
| **Program function** | C |  |  | ✎ | gap | — | — | What the program does when it runs — the *what*, described behaviorally. | Students describe features instead of behavior. “It has a scoreboard” is not a function statement. |
| **Program input** | C |  |  | ✎ | gap | — | — | Data the program receives while running: user action, file, sensor, network, another program. | Must be *at runtime*. Hard-coded values are not input. |
| **Program output** | C |  |  | ✎ | gap | — | — | What the program produces: display, sound, file, movement, data sent elsewhere. |  |
| **Code segment** | L |  |  | ✎ | gap | — | — | A portion of a program, one or more lines, treated as a unit. | WR2 asks about a “code segment” by name. Students need to know they are being asked to point at specific lines. |
| **Computing innovation** | C |  |  | ✎ | planned | — | — | A product, service, or concept that includes a program as an integral part of its function. May be physical, software, or conceptual. | The “includes a program” clause is load-bearing. A bridge is not a computing innovation; a bridge with a load-monitoring system is. *(WiP: Create Performance Task.)* |
| **Collaboration** | L |  |  |  | planned | — | — | Working with others to develop a computing innovation; benefits from varied perspectives and skills. | *(WiP: Lab pair work + Create PT.)* |
| **Pair programming** | L |  |  |  | planned | — | — | Two programmers at one workstation: one drives, one reviews and thinks ahead. | Already the classroom norm. Just attach the name. *(WiP: Create PT / classroom practice.)* |
| **Program documentation** | L |  |  | ✎ | in book | docstring | 4 | Written description of what a segment, procedure, or program does and how it was built. |  |
| **Comments** | L |  |  | ✎ | in book | comment | 2 | Documentation written inside the code for human readers; ignored at execution. | Comments are graded in this course, so the term is already lived. |
| **Debugging** | C |  |  |  | in book | debugging | 1 | The process of finding and fixing errors in a program. | Missing from all three published lists despite being the daily activity. Name it so students can talk about it. |
| **Syntax error** | C | ★ | ✓ |  | in book | syntax error | 1 | A violation of the language's grammar rules; the program typically will not run at all. | Teach as a three-way contrast with logic and run-time, not separately. |
| **Logic error** | C | ★ | ✓ |  | in book | semantic error | 2 | The program runs but produces the wrong result. | Hardest of the three to detect, because nothing complains. *(WiP: Same idea, different name.)* |
| **Run-time error** | C |  | ✓ |  | in book | runtime error | 2 | An error that appears only during execution, such as dividing by zero. | Python raises these as tracebacks; connect the term to what they already see on screen. |
| **Overflow error** | C | ★ | ✓ |  | gap | — | — | The value is outside the range representable in the available bits. | Python's ints are arbitrary precision, so students never see this natively. Needs a deliberate demo. *(WiP: Structurally can't arise in the language the book teaches.)* |
| **Roundoff error** | C |  | ✓ |  | gap | — | — | Loss of precision because a fixed number of bits cannot represent a real number exactly. | `0.1 + 0.2` in the console does this work for you. |
| **Testing** | L |  |  |  | in book | test discovery | 18 | Verifying a program behaves correctly by running it with defined inputs. | *(WiP: Also ch. 7's pass/fail vocabulary.)* |
| **Test case** | C |  |  | ✎ | gap | — | — | A specific input paired with its expected output. Good sets include typical, boundary, and edge values. | Maps directly onto the doctest format and Bootstrap's design recipe (contract → examples → definition). Boundary and edge are the part students omit. *(WiP: The practice exists in exercises; the term is never named.)* |
| **Hand tracing** | C |  |  |  | gap | — | — | Manually stepping through code, tracking variable values, to locate an error. | Python Tutor is the visualization; hand tracing is the paper version, and the exam only has paper. |
| **Iterative development** | C |  |  | ✎ | gap | — | — | Repeated cycles of build, feedback, and revision; earlier phases get revisited. | Teach with incremental as a pair — students merge them into “we kept working on it.” *(WiP: Distinct from Incremental, which the book does name.)* |
| **Incremental development** | C |  |  | ✎ | in book | incremental development | 6 | Breaking a problem into pieces and confirming each works before integrating. |  |
| **Event** | L |  |  |  | gap | — | — | An action supplied to a program as input: key press, click, sensor reading. | *(WiP: Already a known, real gap.)* |
| **Event-driven programming** | L |  |  |  | gap | — | — | Statements execute in response to events rather than in top-to-bottom sequence. | The micro:bit opener and CMU-style graphics both demonstrate this before the term is needed. *(WiP: Every program in this book runs top to bottom.)* |

## Big Idea 2 — Data (DAT)

22 terms — 2 in book, 0 planned, 0 Little Brother, 20 gap.

| Term | Tier | HF | KA | WR | WiP | WiP term | Ch. | Definition | Note |
|---|---|---|---|---|---|---|---|---|---|
| **Binary** | L | ★ |  |  | gap | — | — | Base-2 representation using only 0 and 1. | *(WiP: Partial touchpoint in the Pico/MicroPython I2C unit; not this book.)* |
| **Bit** | F |  | ✓ |  | gap | — | — | A single binary digit. | *(WiP: Partial touchpoint in the Pico/MicroPython I2C unit (byte/hex notation).)* |
| **Byte** | F |  | ✓ |  | gap | — | — | Eight bits. | *(WiP: Partial touchpoint in the Pico/MicroPython I2C unit (byte/hex notation).)* |
| **Hexadecimal** | F |  |  |  | gap | — | — | Base-16, using 0–9 and A–F; four bits per digit. | Keep for the color-code and CRC32 work, not for the exam. *(WiP: Partial touchpoint in the Pico/MicroPython I2C unit (byte/hex notation).)* |
| **Decimal** | F |  |  |  | gap | — | — | Base-10. | Cut candidate. Earns a glossary row only for symmetry with binary and hex. |
| **Abstraction** | C | ★ |  | ✎ | in book | encapsulation / generalization | 4, 9, 10, 11 | Reducing complexity by exposing essential features and hiding implementation detail. | The single most important word in the course and the one students define circularly. Every other abstraction term below is a special case of this one. |
| **Analog data** | C |  | ✓ |  | gap | — | — | Values that vary continuously and smoothly. | Teach as a contrast pair with digital; separately they are near-empty. |
| **Digital data** | C |  |  |  | gap | — | — | Values represented in discrete steps, ultimately as bits. |  |
| **Sampling** | C |  |  |  | gap | — | — | Approximating an analog signal by measuring it at regular intervals. | Rate and bit depth are the two knobs. Students think only about rate. |
| **Lossless compression** | C | ★ | ✓ |  | gap | — | — | Reduces size while allowing exact reconstruction of the original. | Contrast pair with lossy. The exam tests the *choice between them*, not the definitions. |
| **Lossy compression** | C | ★ | ✓ |  | gap | — | — | Reduces size further, but only an approximation can be recovered. |  |
| **Metadata** | C | ★ | ✓ |  | gap | — | — | Data describing other data: creation date, size, author, location, format. | Photo EXIF is the demo that lands. Connects directly to the *Little Brother* and PII threads. *(WiP: Already flagged as uncarried under AP topic 2.3.)* |
| **Data** | F |  |  |  | gap | — | — | Values that can be stored and processed by a program. | Cut candidate — near-free definition. |
| **Information** | C |  |  | ✎ | gap | — | — | Meaning, patterns, or insight extracted from data. | Taught only as the contrast with data. That contrast is genuinely tested. |
| **Data set** | F |  |  |  | gap | — | — | A collection of related data organized for analysis. |  |
| **Correlation** | C |  |  | ✎ | gap | — | — | An association between two variables where changes in one accompany changes in the other. | The whole lesson is “correlation is not causation,” and it is worth the full period. |
| **Data cleaning** | C |  |  | ✎ | gap | — | — | Making data uniform and consistent without changing its meaning. | Students think this means deleting rows they dislike. It does not. |
| **Data filtering** | L |  |  |  | in book | filtering | 10 | Selecting a subset of data by defined criteria. |  |
| **ASCII** | F |  |  |  | gap | — | — | A 7-bit character encoding covering 128 characters. |  |
| **Unicode** | F |  |  |  | gap | — | — | A character encoding standard covering the world's writing systems; extends ASCII. |  |
| **RGB** | F |  |  |  | gap | — | — | Color represented as red, green, and blue channels, typically 0–255 each. |  |
| **Pixel** | F |  |  |  | gap | — | — | The smallest addressable color element of a display or image. |  |

## Big Idea 3 — Algorithms and Programming (AAP)

43 terms — 28 in book, 8 planned, 0 Little Brother, 7 gap.

| Term | Tier | HF | KA | WR | WiP | WiP term | Ch. | Definition | Note |
|---|---|---|---|---|---|---|---|---|---|
| **Variable** | L | ★ |  | ✎ | in book | variable | 2 | A named location holding a value that can change through assignment. |  |
| **Constant** | L |  |  |  | gap | — | — | A named value that does not change during execution. | *(WiP: Python has no language-level constant.)* |
| **Data type** | L |  |  |  | in book | type | 1 | The classification of a value, determining what operations apply. |  |
| **Integer** | F |  |  |  | in book | integer | 1 | A whole number. |  |
| **String** | L |  |  |  | in book | string | 1 | An ordered sequence of characters. |  |
| **Boolean** | L |  |  |  | in book | boolean expression | 5 | A value that is either true or false. |  |
| **Boolean expression** | C |  |  | ✎ | in book | boolean expression | 5 | An expression that evaluates to true or false. | Distinct from the Boolean *type*. Students who only know the type cannot parse “the Boolean expression in line 4.” |
| **Expression** | L |  |  |  | in book | expression | 1 | A combination of values, variables, operators, and calls that evaluates to a single value. |  |
| **Assignment** | L |  |  |  | in book | assignment statement | 2 | Storing a value in a variable. | Pseudocode uses `←`. Recognition only; they never have to write it. |
| **List** | C | ★ |  | ✎ | in book | list | 9 | An ordered sequence of elements, each reachable by index. | **Indices start at 1 in College Board pseudocode and 0 in Python.** This is the single biggest trap for a Python-first cohort. Attach the convention to this row rather than making it its own term. |
| **Element** | L |  |  | ✎ | in book | element | 9 | One item stored in a list. | Distinct from index. WR2 prompts use both words in one sentence. |
| **Index** | L |  |  |  | in book | index | 8 | The position of an element within a list. | See the List note. |
| **Substring** | F |  |  |  | gap | — | — | A contiguous portion of a string. | *(WiP: `slice` (ch. 8) is the mechanism; the word itself isn't a headword.)* |
| **Concatenation** | F |  |  |  | in book | concatenation | 1 | Joining strings end to end. |  |
| **Sequencing** | L | ★ | ✓ |  | gap | — | — | Executing steps in the order written. | Tier L, but they must be able to *name* it — the exam asks which construct a segment demonstrates. *(WiP: The default behavior of every program in the book; never named as its own concept.)* |
| **Selection** | L | ★ | ✓ |  | in book | conditional statement | 5 | Choosing between paths based on a condition. | *(WiP: The single biggest name swap between this book and the exam.)* |
| **Iteration** | L | ★ | ✓ |  | in book | loop | 3, 7 | Repeating steps a set number of times or until a condition is met. | `REPEAT UNTIL (condition)` **exits** when the condition is true. Python's `while` **continues** when true. Inverted sense; put this note on the row rather than teaching the keyword. *(WiP: Definite iteration (`for`) only — this book has no `while` loop at all.)* |
| **Nested conditional** | L |  |  |  | in book | nested conditional | 5 | A conditional inside another conditional. |  |
| **Compound conditional** | C |  |  | ✎ | in book | logical operator | 5 | A single condition combining multiple Boolean expressions with AND, OR, or NOT. | Not covered by “nested.” Students merge the two and then mis-answer questions that hinge on the difference. *(WiP: The mechanism is taught; the AP-specific label isn't used verbatim.)* |
| **Relational operators** | F |  |  |  | in book | relational operator | 5 | Comparison operators: =, ≠, >, <, ≥, ≤. |  |
| **Logical operators** | L |  |  |  | in book | logical operator | 5 | AND, OR, NOT. | The truth-table drill is worth one warm-up cycle, especially NOT applied to a compound. |
| **MOD** | C |  |  |  | in book | modulus operator | 5 | The remainder after integer division. | Kept despite looking like notation — the concept is tested. Even/odd and cycling are the two uses. Negative operands behave unintuitively; worth a distractor. *(WiP: `%` here; `MOD` on the exam reference sheet.)* |
| **Infinite loop** | L |  |  |  | gap | — | — | A loop whose ending condition never becomes true. | *(WiP: “Infinite recursion” (ch. 5) is the book's only named version of this idea.)* |
| **Procedure** | C | ★ | ✓ | ✎ | in book | function | 1 | A named, reusable block of code that performs a task and can be called repeatedly. | AP says procedure; Python says function; the ROV course says method. Say all three out loud once, early. |
| **Parameter** | C |  |  | ✎ | in book | parameter | 3 | A named variable in a procedure's definition that receives an input value. | Contrast pair with argument. Bootstrap's design recipe maps this cleanly: parameter = domain, return value = range. |
| **Argument** | C |  |  | ✎ | in book | argument | 2 | The actual value supplied for a parameter at the call site. | Students use the two words interchangeably all year unless corrected in week one. |
| **RETURN statement** | L |  |  | ✎ | in book | return value | 6 | Exits a procedure immediately and hands a value back to the caller. | The classic misconception is that `return` prints. |
| **Procedural abstraction** | C |  |  | ✎ | in book | interface design | 4 | Naming a process so it can be used knowing *what* it does without knowing *how*. | WR2b routinely asks students to explain this about their own code. Practice on their own Create Task drafts, not on generic examples. |
| **Data abstraction** | C |  |  | ✎ | in book | list / dict / tuple | 9, 10, 11 | Using a data structure, typically a list, to represent related values as one named unit, hiding the individual pieces. | Missing from the original list and a standing WR2 target. The exam wants: what does the list represent, and how does using it manage complexity? |
| **Modularity** | L |  | ✓ |  | gap | — | — | Dividing a program into independent parts each responsible for one aspect. | *(WiP: encapsulation/generalization (ch. 4) are adjacent, but the word itself is never named.)* |
| **Software library** | L |  | ✓ |  | in book | module | 2 | A collection of pre-written procedures available for reuse. |  |
| **API** | L |  | ✓ |  | gap | — | — | The specification of how a library's procedures are called and how they behave. |  |
| **RANDOM(a, b)** | C |  |  |  | in book | pseudorandom | 12 | Returns a random integer from a to b, **inclusive on both ends**, each equally likely. | `random.randint` matches this; `random.random` and `range` do not. Off-by-one on the upper bound is a reliable distractor. *(WiP: Python's `random` module, first used in ch. 12.)* |
| **Simulation** | C |  |  | ✎ | planned | — | — | An abstraction of a real phenomenon using varying values to represent changing states, run for a purpose. | The exam cares about *why simulate*: cost, risk, time, or repeatability. Students answer “because it's easier.” *(WiP: November algorithms block.)* |
| **Traversal** | C |  | ✓ | ✎ | gap | — | — | Iterating over the items of a list. Full traversal visits every element; partial stops early. | The full/partial distinction is the tested part. *(WiP: “Loop variable” (ch. 7) and “element” (ch. 9) are the closest adjacent headwords.)* |
| **Linear search** | C | ★ | ✓ |  | in book | linear search | 7 | Checking each element in turn until the target is found or the list ends. | Contrast pair with binary search. |
| **Binary search** | C | ★ | ✓ |  | planned | — | — | Repeatedly halving a **sorted** list to locate a value. | The sorted precondition is the whole question. Students skip it. *(WiP: November algorithms block; linear search already taught.)* |
| **Algorithmic efficiency** | C |  |  | ✎ | planned | — | — | An estimate of the computational resources an algorithm uses as a function of input size. | *(WiP: November algorithms block.)* |
| **Reasonable time** | C |  | ✓ |  | planned | — | — | Run time that grows polynomially or slower with input size. | Khan defines this with polynomial-vs-superpolynomial language, which is more precise than the CED requires. Your students will have seen that framing. *(WiP: November algorithms block.)* |
| **Unreasonable time** | C |  |  |  | planned | — | — | Run time that grows exponentially or factorially with input size. | *(WiP: November algorithms block.)* |
| **Heuristic** | C |  | ✓ | ✎ | planned | — | — | An approach that finds a good-enough solution when finding the optimal one is impractical. | Flagged in the TODO as needing multiple passes. Not high-frequency on the published list, but genuinely hard, and the definition students give is usually “a guess.” *(WiP: November algorithms block.)* |
| **Decidable problem** | C |  |  |  | planned | — | — | A yes/no problem for which an algorithm can always produce the correct answer. | Contrast pair with undecidable. *(WiP: November algorithms block.)* |
| **Undecidable problem** | C |  | ✓ |  | planned | — | — | A problem for which no algorithm can always give a correct yes/no answer for every input. | Halting problem. Students think it means “very hard.” *(WiP: November algorithms block.)* |

## Big Idea 4 — Computer Systems and Networks (CSN)

25 terms — 0 in book, 0 planned, 25 Little Brother, 0 gap.

| Term | Tier | HF | KA | WR | WiP | WiP term | Ch. | Definition | Note |
|---|---|---|---|---|---|---|---|---|---|
| **Internet** | C | ★ |  |  | Little Brother | — | — | A network of interconnected networks using standardized open protocols. | Teach as a contrast pair with the Web. The exam tests the distinction directly. |
| **World Wide Web** | C |  | ✓ |  | Little Brother | — | — | A system of linked pages and files that runs *on top of* the Internet using HTTP. |  |
| **Computer network** | L |  | ✓ |  | Little Brother | — | — | Interconnected computing devices able to send and receive data. |  |
| **Computing device** | F |  | ✓ |  | Little Brother | — | — | A physical artifact that can run a program. |  |
| **Computing system** | F |  |  |  | Little Brother | — | — | A group of computing devices and programs working together. | Distinct from device. Low cost, occasionally tested. |
| **Packet** | L | ★ |  |  | Little Brother | — | — | A chunk of data carrying metadata such as its destination, sent across a network. |  |
| **Packet switching** | C |  |  |  | Little Brother | — | — | Splitting a message into packets that travel independently, possibly by different routes, and are reassembled at the destination. | The term is the concept. Having “packet” and “routing” separately does not get you here. |
| **Routing** | L |  |  |  | Little Brother | — | — | Determining a path from sender to receiver across a network. |  |
| **Bandwidth** | F |  | ✓ |  | Little Brother | — | — | Maximum data transmittable per unit time, in bits per second. | Students confuse this with latency. One sentence fixes it. |
| **Protocol** | L |  | ✓ |  | Little Brother | — | — | An agreed set of rules governing system behavior. |  |
| **Open standard** | C |  |  | ✎ | Little Brother | — | — | A publicly available specification that anyone may implement without permission or fee. | This is *why* the Internet scales and interoperates, and it is the expected phrasing in network answers. |
| **TCP** | F |  | ✓ |  | Little Brother | — | — | Transport protocol providing reliable, ordered delivery with retransmission. |  |
| **UDP** | F |  | ✓ |  | Little Brother | — | — | Lightweight transport protocol with minimal error checking; faster, less reliable. |  |
| **IP** | F |  | ✓ |  | Little Brother | — | — | Protocol for addressing devices and routing packets between them. |  |
| **IP address** | F |  |  |  | Little Brother | — | — | The unique identifier assigned to a device on a network. |  |
| **HTTP / HTTPS** | F |  | ✓ |  | Little Brother | — | — | The Web's request/response protocol; HTTPS adds encryption in transit. |  |
| **DNS** | F |  |  |  | Little Brother | — | — | Translates domain names into IP addresses. | Ch. 16 of *Little Brother* is the DNS tunneling hook, already in the calendar. |
| **Router** | F |  |  |  | Little Brother | — | — | A device that forwards packets between networks toward their destination. |  |
| **Scalability** | C |  | ✓ | ✎ | Little Brother | — | — | A system's ability to keep working acceptably as demand grows. |  |
| **Fault tolerance** | C | ★ |  | ✎ | Little Brother | — | — | Continuing to operate when components fail. | Contrast pair with redundancy: redundancy is the mechanism, fault tolerance is the property. Students state them as synonyms. |
| **Redundancy** | C |  |  |  | Little Brother | — | — | Duplicate paths or components that allow operation to continue after a failure. |  |
| **Sequential computing** | L |  |  |  | Little Brother | — | — | Operations performed one at a time, in order. | Three-way contrast with parallel and distributed. |
| **Parallel computing** | C | ★ | ✓ | ✎ | Little Brother | — | — | A program split into operations, some performed simultaneously. |  |
| **Distributed computing** | C |  | ✓ |  | Little Brother | — | — | Multiple devices in different locations running parts of one program. |  |
| **Speedup** | C |  | ✓ |  | Little Brother | — | — | Sequential time divided by parallel time. | The arithmetic question appears nearly every year and it is free points. Drill it. |

## Big Idea 5 — Impact of Computing (IOC)

29 terms — 0 in book, 0 planned, 29 Little Brother, 0 gap.

| Term | Tier | HF | KA | WR | WiP | WiP term | Ch. | Definition | Note |
|---|---|---|---|---|---|---|---|---|---|
| **Beneficial and harmful effects** | C |  |  | ✎ | Little Brother | — | — | Every computing innovation has both, and they can fall on different groups of people. | Not a vocabulary word so much as the required shape of an Explore-style answer. Students name only benefits. Belongs in the WR tier regardless. |
| **Digital divide** | C | ★ | ✓ | ✎ | Little Brother | — | — | Unequal access to computing and the Internet across socioeconomic, geographic, or demographic lines. |  |
| **Bias** | C |  |  | ✎ | Little Brother | — | — | Systematic unfairness embedded in an algorithm or in the data it was built from. | Distinguish bias *in the data* from bias *in the design*. The exam accepts either, but students should know which one they are claiming. |
| **Crowdsourcing** | L |  | ✓ |  | Little Brother | — | — | Gathering input, funding, or labor from many people over the Internet. |  |
| **Citizen science** | F |  | ✓ |  | Little Brother | — | — | Scientific research carried out partly by volunteers using their own devices. |  |
| **Machine learning** | F |  |  |  | Little Brother | — | — | Systems that improve at a task from data rather than from explicit programming. | Given the classroom AI policy, expect this to generate discussion. Plan for it. |
| **Data mining** | F |  |  |  | Little Brother | — | — | Analyzing large data sets to find patterns and relationships. |  |
| **Aggregation of information** | C |  |  | ✎ | Little Brother | — | — | Combining separately harmless pieces of data to identify or profile a person. | Not on any published list. It is the central privacy mechanism in *Little Brother* and the most exam-relevant privacy idea after PII. |
| **Anonymization** | C |  |  |  | Little Brother | — | — | Removing identifying details from data — and its limits, since aggregation can re-identify. | Pairs with the row above; teach them together or neither. |
| **PII** | C | ★ | ✓ | ✎ | Little Brother | — | — | Information that identifies or can be linked to a specific individual. |  |
| **Intellectual property** | L |  |  |  | Little Brother | — | — | Creative or technical work legally owned by its creator. |  |
| **Copyright** | L |  |  |  | Little Brother | — | — | The exclusive right of a creator to reproduce, distribute, and display a work. |  |
| **Creative Commons** | C |  | ✓ |  | Little Brother | — | — | A set of public licenses letting a creator pre-authorize specific reuse under stated conditions. | The course text is a CC BY-NC-SA fork. Use the actual license notice on their own printed book as the example. *(WiP: The book you're teaching from is itself the example.)* |
| **Open source** | L |  |  |  | Little Brother | — | — | Software whose source is public and may be modified and redistributed. |  |
| **Open access** | F |  | ✓ |  | Little Brother | — | — | Research or data made available free of access restrictions. |  |
| **Plagiarism** | F |  |  |  | Little Brother | — | — | Presenting someone else's work as your own. |  |
| **Encryption** | C | ★ | ✓ |  | Little Brother | — | — | Encoding data so only holders of the key can read it. |  |
| **Symmetric key encryption** | C |  | ✓ |  | Little Brother | — | — | One shared key both encrypts and decrypts. | Contrast pair with public key. The keygen party already in the calendar is the hook. |
| **Public key encryption** | C |  | ✓ |  | Little Brother | — | — | A public key encrypts; a different private key decrypts. | The asymmetry is the idea. Students describe it as “two passwords.” |
| **Authentication** | L |  |  |  | Little Brother | — | — | Verifying that a user is who they claim to be. |  |
| **Multifactor authentication** | L |  | ✓ |  | Little Brother | — | — | Requiring evidence from two or more categories: knowledge, possession, inherence. | The three categories are the tested part, not the count. |
| **Phishing** | L | ★ | ✓ |  | Little Brother | — | — | Tricking a user into revealing private information by impersonating a trusted party. | Cluster with malware, keylogging, and rogue AP. One lesson, four terms, high recognition and low cost. |
| **Malware** | L |  |  |  | Little Brother | — | — | Software intended to damage or take control of a system. |  |
| **Computer virus** | L |  | ✓ |  | Little Brother | — | — | Malware that copies itself, typically by attaching to other programs or files. |  |
| **Keylogging** | L |  |  |  | Little Brother | — | — | Recording keystrokes to capture passwords and confidential input. |  |
| **Rogue access point** | L |  | ✓ |  | Little Brother | — | — | An unauthorized wireless access point used to intercept network traffic. |  |
| **Cookies** | F |  | ✓ |  | Little Brother | — | — | Small data files stored by a site to track a user's state or behavior. |  |
| **Digital certificate** | F |  |  |  | Little Brother | — | — | A credential issued by an authority binding a public key to an identity. |  |
| **Certificate authority** | F |  |  |  | Little Brother | — | — | An organization that issues and vouches for digital certificates. |  |

## Python-first misconception bank

Where Python's own behavior and the exam's pseudocode disagree — predictable errors, not carelessness. From `data/ap-vocabulary-source.md` §4, each one is a ready-made Peer Instruction question.

| # | Divergence | Python belief | Exam reality | Distractor to write |
|---|---|---|---|---|
| M1 | List indexing | `list[0]` is the first element | Pseudocode indices start at **1** | Ask for the third element of a five-item pseudocode list; offer both off-by-one answers |
| M2 | Loop exit sense | `while cond:` **continues** while true | `REPEAT UNTIL (cond)` **exits** when true | Trace a loop where the two readings terminate at different iteration counts |
| M3 | Random bounds | `range(a, b)` excludes `b` | `RANDOM(a, b)` **includes** both ends | Ask how many distinct values `RANDOM(1, 6)` can return |
| M4 | Procedure vocabulary | function, method | **procedure**; **parameter** vs **argument** | Give a call site and a definition; ask which word names which thing |
| M5 | Return vs. print | `print` shows a value, so it “returns” it | RETURN hands a value to the caller; nothing is displayed | Segment whose value is returned but never printed; ask what the user sees |
| M6 | MOD with negatives | intuition says the sign follows the dividend | worth verifying before asserting either way in class | Only use non-negative operands in assessment items unless you have checked the CED's position |
| M7 | Abstraction | “making something simpler” | *hiding detail behind a name* while preserving use | Offer a shortened-but-not-abstracted option as the distractor |
| M8 | Binary search | works on any list | requires the list be **sorted** | Unsorted list where binary search returns a plausible wrong answer |
| M9 | Fault tolerance vs. redundancy | synonyms | redundancy is mechanism; fault tolerance is the resulting property | Scenario with redundancy present but no failover; ask if it is fault tolerant |
| M10 | Data vs. information | synonyms | information is what analysis extracts from data | Raw sensor log vs. the trend derived from it |

## Provenance

Term inventory, Tier/HF/KA/WR flags, definitions, and notes come from `data/ap-vocabulary-source.md`, this course's own curated list — not the CED (which has no glossary appendix; see `glossary-map.md`), and not a straight copy of either community source it draws on (apcsexamprep.com's list and Khan Academy's vocabulary review — term names and frequency flags only, every definition rewritten). The WiP columns (status / WiP term / chapter) are this page's own addition, cross-checked against the actual notebook code where a specific claim could be verified (`.insert()` never appears in any chapter; there is no `while` loop anywhere in the book).

**Correction from the previous version of this page:** the Big Idea 2 encoding cluster (binary, bit, byte, hex, ASCII, RGB, compression, …) was previously marked `planned` against a CS50T Multimedia unit. That unit was dropped and hasn't been taught since year one (per `glossary-map.md`), so those terms are corrected to `gap` here. Binary, bit, byte, and hex get a note that the Pico/MicroPython I2C unit has a partial touchpoint (byte/hex notation only, not compression) — not this book, and not a full carrier.

