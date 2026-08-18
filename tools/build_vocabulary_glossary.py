#!/usr/bin/env python3
"""Generate the merged AP CSP vocabulary glossary.

Merges every term from `alignment/vocabulary-by-chapter.md` (this book's own
glossary, chapter numbers parsed live from that file) with every term from
`alignment/ap-vocabulary-coverage.md` (the full AP CSP exam vocabulary list)
into one alphabetized reference for the AP binder's vocabulary tab.

ENTRIES below is a hand-curated snapshot -- which terms are on the AP list,
and a short note where this book's word for a concept differs from the
exam's -- maintained the same way as ap-vocabulary-coverage.md itself: by
hand, when a chapter's vocabulary or the AP coverage page changes. Chapter
numbers are NOT hardcoded here; they're parsed fresh from
vocabulary-by-chapter.md every run, so adding a chapter's terms there and
rerunning this script picks up the new chapter links automatically.

Writes:
  alignment/ap-vocabulary-glossary.md             plain-text source, alphabetical
  alignment/ap-vocabulary-glossary.html           hosted, interactive twin (screen)
  alignment/ap-vocabulary-glossary.pdf            printable, all terms
  alignment/ap-vocabulary-glossary-ap-only.pdf    printable, AP-tested terms only

Regenerate with: python3 tools/build_vocabulary_glossary.py (or `make glossary`)

Requires weasyprint (`pip install weasyprint`) for the two PDFs; the .md and
.html still get written even if weasyprint isn't installed.
"""
import html
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB_BY_CHAPTER = ROOT / "alignment" / "vocabulary-by-chapter.md"
OUT_MD = ROOT / "alignment" / "ap-vocabulary-glossary.md"
OUT_HTML = ROOT / "alignment" / "ap-vocabulary-glossary.html"
OUT_PDF_ALL = ROOT / "alignment" / "ap-vocabulary-glossary.pdf"
OUT_PDF_AP = ROOT / "alignment" / "ap-vocabulary-glossary-ap-only.pdf"

SITE = "https://python.porttack.com"

BANNER_MD = (
    "<!-- GENERATED FILE. Do not hand-edit. -->\n"
    "<!-- Source: tools/build_vocabulary_glossary.py (ENTRIES table) "
    "+ alignment/vocabulary-by-chapter.md (chapter numbers) -->\n"
    "<!-- Regenerate with: python3 tools/build_vocabulary_glossary.py (or `make glossary`) -->\n\n"
)

# term, is_ap_vocabulary, definition, note (short parenthetical, e.g. the AP
# exam's own name for this concept when it differs from the book's word)
ENTRIES = [
("absolute path", False, "A path that does not depend on the current directory.", None),
("abstraction", True, "Reducing complexity by exposing essential features and hiding implementation detail.", None),
("accumulator", False, "A variable used in a loop to add up or accumulate a result.", None),
("aggregation of information", True, "Combining separately harmless pieces of data to identify or profile a person.", None),
("algorithm", True, "A finite sequence of steps that solves a problem or completes a task. Can be written in English, pseudocode, or code.", None),
("algorithmic efficiency", True, "An estimate of the computational resources an algorithm uses as a function of input size.", None),
("aliased", False, "If there is more than one variable that refers to an object, the object is aliased.", None),
("analog data", True, "Values that vary continuously and smoothly, with no steps.", None),
("anonymization", True, "Removing identifying details from data — and its limits, since aggregation can re-identify.", None),
("API", True, "The specification of how a library's procedures are called and how they behave.", None),
("argument", True, "A value provided to a function when the function is called.", None),
("arithmetic operator", False, "A symbol, like + and *, that denotes an arithmetic operation like addition or multiplication.", None),
("ASCII", True, "A table assigning a number from 0 to 127 to each of a small set of characters.", None),
("assignment statement", True, "A statement that assigns a value to a variable.", None),
("attribute", False, "A named value associated with an object; called an instance variable when it belongs to a class instance.", None),
("authentication", True, "Verifying that a user is who they claim to be.", None),
("bandwidth", True, "Maximum data transmittable per unit time, in bits per second.", None),
("base case", False, "A conditional branch in a recursive function that does not make a recursive call.", None),
("beneficial and harmful effects", True, "Every computing innovation has both, and they can fall on different groups of people.", None),
("bias", True, "Systematic unfairness embedded in an algorithm or in the data it was built from.", None),
("bigram", False, "A sequence of two elements, often words.", None),
("binary", True, "Base-2 representation, using only the digits 0 and 1.", None),
("binary mode", False, "A way of opening a file so the contents are interpreted as a sequence of bytes rather than a sequence of characters.", None),
("binary search", True, "Repeatedly halving a sorted list to locate a value.", None),
("bit", True, "A single binary digit, 0 or 1.", None),
("block", False, "One or more statements indented to indicate they are part of another statement.", None),
("body", False, "The sequence of statements inside a function definition.", None),
("boolean expression", True, "An expression whose value is either True or False.", None),
("boundary case", False, "A test case at the value where a function's behavior changes, such as zero, an empty string, or the first or last item.", None),
("branch", False, "One of the alternative sequences of statements in a conditional statement.", None),
("bug", False, "An error in a program.", None),
("byte", True, "Eight bits. Enough to hold one of 256 values.", None),
("call graph", False, "A diagram that shows every frame created during the execution of a program, with an arrow from each caller to each callee.", None),
("canvas", False, "A window used to display graphical elements including lines, circles, rectangles, and other shapes.", None),
("certificate authority", True, "An organization that issues and vouches for digital certificates.", None),
("chained conditional", False, "A conditional statement with a series of alternative branches.", None),
("character", False, "An element of a string, including letters, numbers, and symbols.", None),
("character encoding", False, "The agreement about which numbers stand for which characters. Read bits with the wrong encoding and you get the right data as the wrong text.", None),
("child class", False, "A class that inherits from another class.", None),
("citizen science", True, "Scientific research carried out partly by volunteers using their own devices.", None),
("class", False, "A programmer-defined type. A class definition creates a new class object.", None),
("class object", False, "An object that represents a class — it is the result of a class definition.", None),
("class variable", False, "A variable defined inside a class definition, but not inside any method.", None),
("code segment", True, "A portion of a program, one or more lines, treated as a unit.", None),
("collaboration", True, "Working with others to develop a computing innovation; benefits from varied perspectives and skills.", None),
("comment", True, "Text included in a program that provides information about the program but has no effect on its execution.", None),
("compression ratio", False, "Compressed size divided by original size.", None),
("compound conditional", True, "A single condition combining multiple Boolean expressions with AND, OR, or NOT.", None),
("computer network", True, "Interconnected computing devices able to send and receive data.", None),
("computer virus", True, "Malware that copies itself, typically by attaching to other programs or files.", None),
("computing device", True, "A physical artifact that can run a program.", None),
("computing innovation", True, "A product, service, or concept that includes a program as an integral part of its function. May be physical, software, or conceptual.", None),
("computing system", True, "A group of computing devices and programs working together.", None),
("concatenation", True, "Joining two strings end-to-end.", None),
("condition", False, "The boolean expression in a conditional statement that determines which branch runs.", None),
("conditional expression", False, "An expression that uses a conditional to select one of two values.", None),
("conditional statement", True, "A statement that controls the flow of execution depending on some condition.", "AP calls this selection"),
("configuration data", False, "Data, often stored in a file, that specifies what a program should do and how.", None),
("constant", True, "A named value that does not change during execution.", None),
("cookies", True, "Small data files stored by a site to track a user's state or behavior.", None),
("copyright", True, "The exclusive right of a creator to reproduce, distribute, and display a work.", None),
("correlation", True, "An association between two variables where changes in one accompany changes in the other.", None),
("counter", False, "A variable used to count something, usually initialized to zero and then incremented.", None),
("creative commons", True, "A set of public licenses letting a creator pre-authorize specific reuse under stated conditions.", None),
("crowdsourcing", True, "Gathering input, funding, or labor from many people over the Internet.", None),
("current working directory", False, "The default directory used by a program unless another directory is specified.", None),
("data", True, "Values that can be stored and processed by a program.", None),
("data abstraction", True, "Using a data structure, typically a list, to represent related values as one named unit, hiding the individual pieces.", None),
("data cleaning", True, "Making data uniform and consistent without changing its meaning.", None),
("data mining", True, "Analyzing large data sets to find patterns and relationships.", None),
("data set", True, "A collection of related data organized for analysis.", None),
("data structure", False, "A collection of values, organized to perform certain operations efficiently.", None),
("database", False, "A file whose contents are organized to perform certain operations efficiently.", None),
("dead code", False, "Part of a program that can never run, often because it appears after a return statement.", None),
("debugging", True, "The process of finding and correcting errors.", None),
("decidable problem", True, "A yes/no problem for which an algorithm can always produce the correct answer.", None),
("decimal", True, "Base-10, the system you already use.", None),
("decrement", False, "Decrease the value of a variable.", None),
("deep copy", False, "A copy operation that also copies nested objects.", None),
("default value", False, "The value assigned to a parameter if no argument is provided.", None),
("delegation", False, "When one method passes responsibility to another method to do most or all of the work.", None),
("delimiter", False, "A character or string used to indicate where a string should be split.", None),
("deserialization", False, "Converting a string to an object.", None),
("design-first development", False, "A way of developing programs with more careful planning than prototype and patch.", None),
("deterministic", False, "A deterministic program does the same thing each time it runs, given the same inputs.", None),
("development plan", False, "A process for writing programs.", None),
("dictionary", False, "An object that contains key-value pairs, also called items.", None),
("digest", False, "The result of a hash function, especially when it is used to check whether two objects are the same.", None),
("digital certificate", True, "A credential issued by an authority binding a public key to an identity.", None),
("digital data", True, "Values represented in discrete steps, ultimately as bits.", None),
("digital divide", True, "Unequal access to computing and the Internet across socioeconomic, geographic, or demographic lines.", None),
("directory", False, "A collection of files and other directories.", None),
("distributed computing", True, "Multiple devices in different locations running parts of one program.", None),
("DNS", True, "Translates domain names into IP addresses.", None),
("docstring", True, "A string at the beginning of a function that documents what the function does; unlike a comment, it is stored on the function and can be read by the program.", "AP calls this program documentation"),
("doctest", False, "An example call and its expected result, written inside a docstring, that can be run automatically to check the function.", None),
("dot operator", False, "The operator, ., used to access a function in another module by specifying the module name followed by a dot and the function name.", None),
("edge case", False, "A test case at an unusual or extreme input, where a function is most likely to be wrong.", None),
("element", True, "One of the values in a list or other sequence.", None),
("empty string", False, "A string that contains no characters and has length 0.", None),
("encode", False, "To represent one set of values using another set of values by constructing a mapping between them.", None),
("encapsulation", False, "The process of transforming a sequence of statements into a function definition.", None),
("encryption", True, "Encoding data so only holders of the key can read it.", None),
("enumerate object", False, "The result of calling the built-in function enumerate, can be used to loop through a sequence of tuples.", None),
("ephemeral", False, "An ephemeral program typically runs for a short time and, when it ends, its data are lost.", None),
("equivalent", False, "Having the same value.", None),
("evaluate", False, "Perform the operations in an expression in order to compute a value.", None),
("event", True, "An action supplied to a program as input: key press, click, sensor reading.", None),
("event-driven programming", True, "Statements execute in response to events rather than in top-to-bottom sequence.", None),
("exception", False, "An error that is detected while the program is running.", None),
("execute", False, "Run a statement and do what it says.", None),
("expected value", False, "What a test says the answer should be, as opposed to what the code actually produced.", None),
("expression", True, "A combination of variables, values, and operators.", None),
("f-string", False, "A string that has the letter f before the opening quotation mark, and contains one or more expressions in curly braces.", None),
("factory", False, "A function used to create objects, often passed as a parameter to a function.", None),
("fail", False, "A test whose actual result does not match its expected value.", None),
("fault tolerance", True, "Continuing to operate when components fail.", None),
("file object", False, "An object that represents an open file and keeps track of which parts of the file have been read or written.", None),
("filtering", True, "Looping through a sequence and selecting or omitting elements.", "AP calls this data filtering"),
("floating-point", False, "A type that represents integers and numbers with decimal parts.", None),
("formal language", False, "Any of the languages that people have designed for specific purposes, such as representing mathematical ideas or computer programs. All programming languages are formal languages.", None),
("format specifier", False, "In an f-string, a format specifier determines how a value is converted to a string.", None),
("frame", False, "A box in a stack diagram that represents a function call. It contains the local variables and parameters of the function.", None),
("function", True, "A named sequence of statements that performs some useful operation. Functions may or may not take arguments and may or may not produce a result.", "AP calls this a procedure"),
("function call", False, "An expression — or part of an expression — that runs a function. It consists of the function name followed by an argument list in parentheses.", None),
("function definition", False, "A statement that creates a function.", None),
("function object", False, "A value created by a function definition. The name of the function is a variable that refers to a function object.", None),
("functional programming style", False, "A way of programming that uses pure functions whenever possible.", None),
("generalization", False, "The process of replacing something unnecessarily specific (like a number) with something appropriately general (like a variable or parameter).", None),
("generator expression", False, "Similar to a list comprehension except that it does not create a list.", None),
("hand tracing", True, "Working through code on paper line by line, writing down each variable's value, in order to find an error without running the program.", None),
("hash function", False, "A function that takes an object and computes an integer — sometimes called a digest — used to locate a key in a hash table or to check whether two objects are the same.", None),
("hash table", False, "A collection of key-value pairs organized so that we can look up a key and find its value efficiently.", None),
("hashable", False, "Immutable types like integers, floats and strings are hashable. Mutable types like lists and dictionaries are not.", None),
("header", False, "The first line of a function definition.", None),
("heuristic", True, "An approach that finds a good-enough solution when finding the optimal one is impractical.", None),
("hexadecimal", True, "Base-16, using 0 through 9 and A through F. Four bits per digit, so one byte is exactly two hex digits.", None),
("HTTP / HTTPS", True, "The Web's request/response protocol; HTTPS adds encryption in transit.", None),
("identical", False, "Being the same object (which implies equivalence).", None),
("immutable", False, "If the elements of an object cannot be changed, the object is immutable.", None),
("import statement", False, "A statement that reads a module file so we can use the variables and functions it contains.", None),
("increment", False, "Increase the value of a variable.", None),
("incremental development", True, "A program development plan intended to avoid debugging by adding and testing only a small amount of code at a time.", None),
("index", True, "An integer value used to select an item in a sequence, such as a character in a string. In Python indices start from 0.", None),
("infinite loop", True, "A loop whose ending condition never becomes true.", None),
("infinite recursion", False, "A recursion that doesn't have a base case, or never reaches it. Eventually, an infinite recursion causes a runtime error.", None),
("information", True, "Meaning, patterns, or insight extracted from data.", None),
("inheritance", False, "The ability to define a new class that is a modified version of a previously defined class.", None),
("initialize", False, "Create a new variable and give it a value.", None),
("input validation", False, "Checking the parameters of a function to make sure they have the correct types and values.", None),
("instance", False, "An object that belongs to a class.", None),
("instance method", False, "A method that must be invoked with an object as receiver.", None),
("instantiation", False, "The process of creating an object that belongs to a class.", None),
("integer", True, "A type that represents numbers with no fractional or decimal part.", None),
("integer division", False, "An operator, //, that divides two numbers and rounds down to an integer.", None),
("intellectual property", True, "Creative or technical work legally owned by its creator.", None),
("interface design", True, "A process for designing the interface of a function, which includes the parameters it should take.", "AP calls this procedural abstraction"),
("internet", True, "A network of interconnected networks using standardized open protocols.", None),
("invariant", False, "A condition that should always be true during the execution of a program.", None),
("invocation", False, "An expression — or part of an expression — that calls a method.", None),
("IP", True, "Protocol for addressing devices and routing packets between them.", None),
("IP address", True, "The unique identifier assigned to a device on a network.", None),
("item", False, "In a dictionary, another name for a key-value pair.", None),
("iterative development", True, "Repeated cycles of build, feedback, and revision; earlier phases get revisited.", None),
("key", False, "An object that appears in a dictionary as the first part of a key-value pair.", None),
("key-value stores", False, "A database whose contents are organized like a dictionary with keys that correspond to values.", None),
("keylogging", True, "Recording keystrokes to capture passwords and confidential input.", None),
("keyword", False, "A special word used to specify the structure of a program.", None),
("keyword argument", False, "An argument that includes the name of the parameter.", None),
("linear search", True, "A computational pattern that searches through a sequence of elements and stops when it finds what it is looking for.", None),
("list", True, "An object that contains a sequence of values.", "on the AP exam, list indices start at 1; in Python, at 0"),
("list comprehension", False, "A concise way to loop through a sequence and create a list.", None),
("local variable", False, "A variable defined inside a function, and which can only be accessed inside the function.", None),
("logical operator", True, "One of the operators that combines boolean expressions, including and, or, and not.", None),
("lossless compression", True, "Reduces size while allowing the original to be reconstructed exactly.", None),
("lossy compression", True, "Reduces size further, but only an approximation of the original can be recovered.", None),
("loop", True, "A statement that runs one or more statements, often repeatedly.", "AP calls this iteration"),
("loop variable", False, "A variable defined in the header of a for loop.", None),
("machine learning", True, "Systems that improve at a task from data rather than from explicit programming.", None),
("malware", True, "Software intended to damage or take control of a system.", None),
("mapping", False, "A relationship in which each element of one set corresponds to an element of another set.", None),
("memo", False, "A computed value stored to avoid unnecessary future computation.", None),
("metadata", True, "Data describing other data: creation date, size, author, location, format.", None),
("method", False, "A function that is associated with an object and called using the dot operator; when defined inside a class it is invoked on instances of that class.", None),
("modularity", True, "Dividing a program into independent parts each responsible for one aspect.", None),
("module", True, "A file that contains Python code, including function definitions and sometimes other statements.", "AP calls this a software library"),
("modulus operator", True, "An operator, %, that works on integers and returns the remainder when one number is divided by another.", "AP calls this MOD"),
("multifactor authentication", True, "Requiring evidence from two or more categories: knowledge, possession, inherence.", None),
("multiline string", False, "A string enclosed in triple quotes that can span more than one line of a program.", None),
("n-gram", False, "A sequence of an unspecified number of elements.", None),
("natural language", False, "Any of the languages that people speak that evolved naturally.", None),
("nested conditional", True, "A conditional statement that appears in one of the branches of another conditional statement.", None),
("nested list", False, "A list that is an element of another list.", None),
("newline", False, "A character that creates a line break between two parts of a string.", None),
("object", False, "Something a variable can refer to. An object has a type and a value.", None),
("object diagram", False, "A graphical representation of an object, its attributes, and their values.", None),
("object-oriented language", False, "A language that provides features to support object-oriented programming, notably user-defined types.", None),
("object-oriented programming", False, "A style of programming that uses objects to organize code and data.", None),
("overflow error", True, "An error that happens when a value is too large for the number of bits available to hold it.", None),
("open access", True, "Research or data made available free of access restrictions.", None),
("open source", True, "Software whose source is public and may be modified and redistributed.", None),
("open standard", True, "A publicly available specification that anyone may implement without permission or fee.", None),
("operand", False, "One of the values on which an operator operates.", None),
("operator overloading", False, "The process of using special methods to change the way operators work with user-defined types.", None),
("override", False, "To replace a default value with an argument.", None),
("pack", False, "Collect multiple arguments into a tuple.", None),
("packet", True, "A chunk of data carrying metadata such as its destination, sent across a network.", None),
("packet switching", True, "Splitting a message into packets that travel independently, possibly by different routes, and are reassembled at the destination.", None),
("pair programming", True, "Two programmers at one workstation: one drives, one reviews and thinks ahead.", None),
("parallel computing", True, "A program split into operations, some performed simultaneously.", None),
("parameter", True, "A name used inside a function to refer to the value passed as an argument.", None),
("parent class", False, "A class that is inherited from.", None),
("pass", False, "A test whose actual result matches its expected value.", None),
("path", False, "A string that specifies a sequence of directories, often leading to a file.", None),
("pattern", False, "A rule that specifies the requirements a string has to meet to constitute a match.", None),
("persistent", False, "A persistent program runs indefinitely and keeps at least some of its data in permanent storage.", None),
("phishing", True, "Tricking a user into revealing private information by impersonating a trusted party.", None),
("PII", True, "Information that identifies or can be linked to a specific individual.", None),
("pixel", True, "The smallest addressable color element of a display or image.", None),
("plagiarism", True, "Presenting someone else's work as your own.", None),
("polymorphism", False, "The ability of a method or operator to work with multiple types of objects.", None),
("postcondition", False, "A requirement that should be satisfied by the function before it ends.", None),
("precondition", False, "A requirement that should be satisfied by the caller before a function starts.", None),
("procedure", True, "The exam's word for a named, reusable block of code, whether or not it returns a value. This book says function. In older languages the two words were distinct: a procedure returned nothing, a function returned a value.", None),
("program", True, "A collection of statements that performs a task when run.", None),
("program function", True, "What a program does when it runs, described as behavior.", None),
("program input", True, "Data a program receives while it is running.", None),
("program output", True, "What a program produces: displayed text, a returned value, a file, a sound, a movement.", None),
("program purpose", True, "The need a program serves, or the problem it solves; why it exists.", None),
("protocol", True, "An agreed set of rules governing system behavior.", None),
("prototype and patch", False, "A way of developing programs by starting with a rough draft and gradually adding features and fixing bugs.", None),
("pseudorandom", True, "A pseudorandom sequence of numbers appears to be random, but is generated by a deterministic program.", "AP calls this RANDOM(a, b) — inclusive on both ends, unlike Python's range"),
("public key encryption", True, "A public key encrypts; a different private key decrypts.", None),
("pure function", False, "A function that does not modify its parameters or have any effect other than returning a value.", None),
("reasonable time", True, "Run time that grows polynomially or slower with input size.", None),
("receiver", False, "The object a method is invoked on.", None),
("recursion", False, "The process of calling the function that is currently executing.", None),
("recursive", False, "A function that calls itself is recursive.", None),
("redundancy", True, "Duplicate paths or components that allow operation to continue after a failure.", None),
("refactoring", False, "The process of modifying a working program to improve function interfaces and other qualities of the code.", None),
("reference", False, "The association between a variable and its value.", None),
("regression", False, "A bug that reappears in code that used to work.", None),
("regular expression", False, "A sequence of characters that defines a search pattern.", None),
("relational operator", True, "One of the operators that compares its operands: ==, !=, >, <, >=, and <=.", None),
("relative path", False, "A path that starts from the current working directory, or some other specified directory.", None),
("return value", True, "The result of a function. If a function call is used as an expression, the return value is the value of the expression.", "AP calls this the RETURN statement"),
("RGB", True, "Color stored as three numbers, the amounts of red, green, and blue, each usually one byte.", None),
("rogue access point", True, "An unauthorized wireless access point used to intercept network traffic.", None),
("roundoff error", True, "A loss of precision that happens because a fixed number of bits cannot represent some numbers exactly.", None),
("router", True, "A device that forwards packets between networks toward their destination.", None),
("routing", True, "Determining a path from sender to receiver across a network.", None),
("rubber duck debugging", False, "A way of debugging by explaining a problem aloud to an inanimate object.", None),
("runtime error", True, "An error that causes a program to display an error message and exit.", None),
("run-length encoding", False, "A lossless scheme that replaces runs of a repeated value with the value and a count.", None),
("sampling", True, "Approximating an analog signal by measuring it at regular intervals. Two independent settings: how often you measure (rate) and how precisely you record each measurement (bit depth).", None),
("scaffolding", False, "Code that is used during program development but is not part of the final version.", None),
("scalability", True, "A system's ability to keep working acceptably as demand grows.", None),
("semantic error", True, "An error that lets the program run but produces a wrong result.", "AP calls this a logic error"),
("sequence", False, "An ordered collection of values where each value is identified by an integer index.", None),
("sequencing", True, "Executing steps in the order written.", None),
("sequential computing", True, "Operations performed one at a time, in order.", None),
("serialization", False, "Converting an object to a string.", None),
("shallow copy", False, "A copy operation that does not copy nested objects.", None),
("shell command", False, "A statement in a shell language, which is a language used to interact with an operating system.", None),
("side effect", False, "Any effect a function has other than returning a value, such as displaying output or drawing on a canvas.", None),
("simulation", True, "An abstraction of a real phenomenon using varying values to represent changing states, run for a purpose.", None),
("slice", False, "A part of a string specified by a range of indices.", None),
("sort key", False, "A value, or function that computes a value, used to sort the elements of a collection.", None),
("special method", False, "A method that changes the way operators and some functions work with an object.", None),
("specialization", False, "A way of using inheritance to create a new class that is a specialized version of an existing class.", None),
("speedup", True, "Sequential time divided by parallel time.", None),
("stack diagram", False, "A graphical representation of a stack of functions, their variables, and the values they refer to.", None),
("state diagram", False, "A graphical representation of a set of variables and the values they refer to.", None),
("statement", False, "One or more lines of code that represent a command or action.", None),
("static method", False, "A method that can be invoked without an object as receiver.", None),
("string", True, "A type that represents sequences of characters.", None),
("string substitution", False, "Replacement of a string, or part of a string, with another string.", None),
("substring", True, "A contiguous portion of a string.", None),
("symmetric key encryption", True, "One shared key both encrypts and decrypts.", None),
("syntax error", True, "An error in a program that makes it impossible to parse — and therefore impossible to run.", None),
("TCP", True, "Transport protocol providing reliable, ordered delivery with retransmission.", None),
("test case", True, "A specific input paired with its expected output. Good sets include typical, boundary, and edge values.", None),
("test discovery", False, "A process used to find and run tests.", None),
("testing", True, "Checking that a program behaves correctly by running it on chosen inputs and comparing what comes out against what should have come out.", None),
("totally ordered", False, "A set of objects is totally ordered if we can compare any two elements and the results are consistent.", None),
("traceback", False, "A list of the functions that are executing, printed when an exception occurs.", None),
("traversal", True, "Iterating over the items of a list. Full traversal visits every element; partial stops early.", None),
("trigram", False, "A sequence of three elements.", None),
("Turing complete", False, "A language, or subset of a language, is Turing complete if it can perform any computation that can be described by an algorithm.", None),
("type", True, "A category of values. The types we have seen so far are integers (type int), floating-point numbers (type float), and strings (type str).", "AP calls this data type"),
("UDP", True, "Lightweight transport protocol with minimal error checking; faster, less reliable.", None),
("undecidable problem", True, "A problem for which no algorithm can always give a correct yes/no answer for every input.", None),
("Unicode", True, "A far larger table, covering the writing systems ASCII left out.", None),
("unpack", False, "Treat a tuple (or other sequence) as multiple arguments.", None),
("unreasonable time", True, "Run time that grows exponentially or factorially with input size.", None),
("update", False, "An assignment statement that gives a new value to a variable that already exists, rather than creating a new variable.", None),
("value", False, "An integer, floating-point number, string, or other kind of data a program works with. In a dictionary, a value is specifically the second part of a key-value pair.", None),
("variable", True, "A name that refers to a value.", None),
("world wide web", True, "A system of linked pages and files that runs on top of the Internet using HTTP.", None),
("zip object", False, "The result of calling the built-in function zip, can be used to loop through a sequence of tuples.", None),
]


def esc(s):
    return html.escape(s, quote=False)


def parse_chapter_map():
    """Term (lowercase) -> list of chapter labels ("01".."19", "06b", "07b"),
    parsed live from vocabulary-by-chapter.md's own `## Chapter N` / `##
    Interlude` headers, so a new chapter's terms get correct links here
    automatically without editing this file."""
    chapter_map = {}
    current = None
    interlude_count = 0
    with open(VOCAB_BY_CHAPTER) as f:
        for line in f:
            m_ch = re.match(r"^## Chapter (\d+)", line)
            m_int = re.match(r"^## Interlude", line)
            if m_ch:
                current = m_ch.group(1).zfill(2)
                continue
            if m_int:
                interlude_count += 1
                # Only two interludes exist today (between ch. 6/7 and 7/8).
                # A third would need a rule here; the surrounding chapter
                # numbers in vocabulary-by-chapter.md's own section text are
                # the tell if this ever needs to grow past two.
                current = "06b" if interlude_count == 1 else "07b"
                continue
            m_term = re.match(r"\|\s*\*\*(.+?)\*\*\s*\|", line)
            if m_term and current:
                term = m_term.group(1).strip().lower()
                chapter_map.setdefault(term, [])
                if current not in chapter_map[term]:
                    chapter_map[term].append(current)
    return chapter_map


def build_full_list():
    seen = {}
    for term, ap, definition, note in ENTRIES:
        key = term.lower()
        if key in seen:
            sys.exit(f"ERROR: duplicate glossary term {term!r}")
        seen[key] = True
    entries_sorted = sorted(ENTRIES, key=lambda e: e[0].lower())
    chapter_map = parse_chapter_map()
    full = []
    for term, ap, definition, note in entries_sorted:
        chapters = chapter_map.get(term.lower(), [])
        full.append({"term": term, "ap": ap, "def": definition, "note": note, "chapters": chapters})
    return full


def chapter_url(ch):
    return f"{SITE}/chap{ch}.html"


def term_html(e, linked=True):
    t = esc(e["term"])
    sup = ""
    if e["ap"]:
        sup += '<sup class="ap">AP</sup>'
    if e["chapters"]:
        if linked:
            links = ",".join(f'<a href="{chapter_url(c)}">{c.lstrip("0") or c}</a>' for c in e["chapters"])
        else:
            links = ",".join(c.lstrip("0") or c for c in e["chapters"])
        sup += f'<sup class="ch">{links}</sup>'
    return f"<b>{t}</b>{sup}"


def def_html(e):
    d = esc(e["def"])
    if e["note"]:
        d += f' <i class="note">({esc(e["note"])}.)</i>'
    return d


def entry_div(e, linked=True):
    cls = "entry is-ap" if e["ap"] else "entry"
    return f'<div class="{cls}">{term_html(e, linked)}&ensp;{def_html(e)}</div>'


# ---------------------------------------------------------------- markdown --

def write_markdown(full):
    ap_count = sum(1 for e in full if e["ap"])
    book_count = sum(1 for e in full if e["chapters"])
    both = sum(1 for e in full if e["ap"] and e["chapters"])

    groups = {}
    for e in full:
        letter = e["term"][0].upper() if e["term"][0].isalpha() else "#"
        groups.setdefault(letter, []).append(e)

    lines = [BANNER_MD.rstrip("\n"), ""]
    lines.append("# AP CSP Vocabulary Glossary")
    lines.append("")
    lines.append(
        "Every term from [`vocabulary-by-chapter.md`](vocabulary-by-chapter.md) (this book's own "
        "glossary) merged with every term from [`ap-vocabulary-coverage.md`](ap-vocabulary-coverage.md) "
        "(the full AP CSP exam vocabulary list), alphabetized into one binder-ready reference. Hosted "
        f"twin: [`ap-vocabulary-glossary.html`]({SITE}/alignment/ap-vocabulary-glossary.html). Printable "
        f"PDFs: [all terms]({SITE}/alignment/ap-vocabulary-glossary.pdf), "
        f"[AP-tested only]({SITE}/alignment/ap-vocabulary-glossary-ap-only.pdf)."
    )
    lines.append("")
    lines.append(
        f"**{len(full)} terms. {ap_count} are on the AP CSP exam's own vocabulary list (marked AP below); "
        f"{book_count} appear somewhere in this book's chapters (chapter number(s) noted); {both} are both.**"
    )
    lines.append("")
    lines.append(
        "Where this book uses a different word than the exam for the same idea (e.g. this book's `loop` "
        "vs. the exam's `iteration`), the entry keeps the book's word as the headword and notes the "
        "exam's name in parentheses -- the point is to recognize the exam's phrasing when it shows up on "
        "a test, not to relearn vocabulary you already have."
    )
    lines.append("")

    for letter in sorted(groups):
        lines.append(f"## {letter}")
        lines.append("")
        lines.append("| Term | AP | Ch. | Definition |")
        lines.append("|---|---|---|---|")
        for e in groups[letter]:
            ap_mark = "AP" if e["ap"] else ""
            ch_mark = ", ".join(e["chapters"]) if e["chapters"] else "—"
            d = e["def"]
            if e["note"]:
                d += f" *({e['note']}.)*"
            lines.append(f"| **{e['term']}** | {ap_mark} | {ch_mark} | {d} |")
        lines.append("")

    OUT_MD.write_text("\n".join(lines))


# -------------------------------------------------------------------- html --

SHARED_TOKENS_CSS = """
:root {
  --ink: #1c211f; --ink-soft: #4b534f; --paper: #f5f6f3; --paper-raised: #ffffff;
  --line: #d8dcd6; --line-soft: #e6e9e4; --accent: #3e4c8c; --accent-soft: #eceef7;
  --accent-ink: #2c3768; --strong: #3f7d5c; --strong-bg: #e6efe9; --partial: #b8863a;
  --partial-bg: #f6ecda; --elsewhere: #64708a; --elsewhere-bg: #eaecf1;
  --serif: "Iowan Old Style", "Palatino Linotype", Georgia, "Times New Roman", serif;
  --sans: -apple-system, "Segoe UI", "Noto Sans", sans-serif;
  --mono: ui-monospace, "SF Mono", "Cascadia Code", "Roboto Mono", Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ink: #e8e7e1; --ink-soft: #aeb4ac; --paper: #14181a; --paper-raised: #1a1f21;
    --line: #2c3230; --line-soft: #232826; --accent: #8e9fe8; --accent-soft: #232a45;
    --accent-ink: #b7c2f2; --strong: #6cbf94; --strong-bg: #1e2c25; --partial: #d3a159;
    --partial-bg: #2e2517; --elsewhere: #9aa4bd; --elsewhere-bg: #232733;
  }
}
:root[data-theme="dark"] {
  --ink: #e8e7e1; --ink-soft: #aeb4ac; --paper: #14181a; --paper-raised: #1a1f21;
  --line: #2c3230; --line-soft: #232826; --accent: #8e9fe8; --accent-soft: #232a45;
  --accent-ink: #b7c2f2; --strong: #6cbf94; --strong-bg: #1e2c25; --partial: #d3a159;
  --partial-bg: #2e2517; --elsewhere: #9aa4bd; --elsewhere-bg: #232733;
}
"""


def build_html(full):
    ap_count = sum(1 for e in full if e["ap"])
    book_count = sum(1 for e in full if e["chapters"])

    groups = {}
    for e in full:
        letter = e["term"][0].upper() if e["term"][0].isalpha() else "#"
        groups.setdefault(letter, []).append(e)
    letters = sorted(groups)

    nav_links = "\n    ".join(
        f'<a href="#letter-{l.lower()}" data-ap-count="{sum(1 for e in groups[l] if e["ap"])}">{l}</a>'
        for l in letters
    )

    sections = []
    for letter in letters:
        entries_html = "".join(entry_div(e) for e in groups[letter])
        ap_in_letter = sum(1 for e in groups[letter] if e["ap"])
        sections.append(f"""
<section id="letter-{letter.lower()}" data-ap-count="{ap_in_letter}">
  <div class="bigidea-head">
    <h2>{letter}</h2>
    <span class="name" data-total="{len(groups[letter])}" data-ap="{ap_in_letter}">{len(groups[letter])} term{'s' if len(groups[letter]) != 1 else ''}</span>
  </div>
  <div class="entries-wrap">{entries_html}</div>
</section>""")
    sections_html = "\n".join(sections)

    doc = f"""<title>AP CSP Vocabulary Glossary — Working in Python</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{SHARED_TOKENS_CSS}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--paper); color: var(--ink); font-family: var(--sans);
  font-size: 15.5px; line-height: 1.55; -webkit-font-smoothing: antialiased;
}}
a {{ color: var(--accent-ink); text-decoration: none; border-bottom: 1px solid currentColor; opacity: 0.9; }}
a:hover {{ opacity: 1; }}
a:focus-visible, button:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}

.page {{ max-width: 920px; margin: 0 auto; padding: 0 24px 96px; }}

header.masthead {{ padding: 40px 0 28px; border-bottom: 1px solid var(--line); }}
.eyebrow {{
  display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap;
  font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.09em; text-transform: uppercase;
  color: var(--ink-soft); margin: 0 0 14px;
}}
.eyebrow a {{ border-bottom: 1px dotted currentColor; text-transform: none; letter-spacing: 0.02em; }}
h1 {{
  font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 4.2vw, 38px);
  line-height: 1.12; margin: 0 0 12px; text-wrap: balance; color: var(--ink);
}}
.lede {{ margin: 0; max-width: 68ch; color: var(--ink-soft); font-size: 16px; }}

.stats {{
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--line);
  border: 1px solid var(--line); border-radius: 10px; overflow: hidden; margin-top: 28px;
}}
.stat {{ background: var(--paper-raised); padding: 16px 18px; }}
.stat .n {{ font-family: var(--mono); font-variant-numeric: tabular-nums; font-size: 26px; font-weight: 600; line-height: 1; }}
.stat .label {{ margin-top: 6px; font-size: 12.5px; color: var(--ink-soft); }}
.stat.book .n {{ color: var(--strong); }}
.stat.planned .n {{ color: var(--partial); }}
.stat.elsewhere .n {{ color: var(--elsewhere); }}

nav.jump {{
  position: sticky; top: 0; z-index: 10; background: color-mix(in srgb, var(--paper) 92%, transparent);
  backdrop-filter: blur(6px); border-bottom: 1px solid var(--line); margin: 0 -24px 40px; padding: 0 24px;
}}
.jump-inner {{
  max-width: 920px; margin: 0 auto; display: flex; gap: 4px; overflow-x: auto; padding: 10px 0;
  scrollbar-width: none;
}}
.jump-inner::-webkit-scrollbar {{ display: none; }}
.jump a {{
  border-bottom: none; font-size: 13px; font-weight: 500; color: var(--ink-soft); padding: 6px 11px;
  border-radius: 999px; white-space: nowrap; flex-shrink: 0;
}}
.jump a:hover {{ color: var(--ink); background: var(--line-soft); }}
.jump a.external {{ margin-left: auto; color: var(--accent-ink); }}

section {{ margin: 48px 0; }}
section > .bigidea-head h2 {{
  font-family: var(--serif); font-size: 22px; font-weight: 600; margin: 0; color: var(--ink); scroll-margin-top: 60px;
}}
.bigidea-head {{ display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 10px; }}
.bigidea-head .name {{ font-size: 12.5px; font-family: var(--mono); color: var(--ink-soft); }}

.entries-wrap {{ border: 1px solid var(--line); border-radius: 10px; background: var(--paper-raised); padding: 4px 16px; }}
.entry {{ padding: 10px 0; border-top: 1px solid var(--line-soft); font-size: 13.8px; }}
.entry:first-child {{ border-top: none; }}
.entry b {{ font-family: var(--sans); font-weight: 600; }}

sup.ap {{
  font-family: var(--mono); font-size: 9.5px; font-weight: 700; letter-spacing: 0.02em;
  color: var(--accent-ink); background: var(--accent-soft); border-radius: 3px; padding: 0 3px;
  vertical-align: super; margin-left: 3px;
}}
sup.ch {{ font-family: var(--mono); font-size: 10.5px; color: var(--ink-soft); vertical-align: super; margin-left: 3px; }}
sup.ch a {{ border-bottom: 1px dotted currentColor; color: var(--ink-soft); }}
sup.ch a:hover {{ color: var(--accent-ink); }}
i.note {{ color: var(--ink-soft); font-style: italic; }}

.legend2 {{ display: flex; gap: 18px; flex-wrap: wrap; font-size: 13px; color: var(--ink-soft); margin: 14px 0 0; }}

.filterbar {{
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  margin-top: 18px; padding: 12px 16px; background: var(--paper-raised);
  border: 1px solid var(--line); border-radius: 10px;
}}
.filter-label {{ font-size: 13.5px; font-weight: 600; color: var(--ink); }}
.segmented {{ display: inline-flex; background: var(--line-soft); border-radius: 999px; padding: 3px; gap: 2px; }}
.seg-btn {{
  font-family: var(--sans); font-size: 13px; font-weight: 500; color: var(--ink-soft);
  background: transparent; border: none; border-radius: 999px; padding: 7px 14px; cursor: pointer;
}}
.seg-btn:hover {{ color: var(--ink); }}
.seg-btn[aria-pressed="true"] {{ background: var(--accent); color: var(--paper); }}
.filter-count {{ font-size: 12.5px; color: var(--ink-soft); font-family: var(--mono); margin-left: auto; }}
body.ap-only .entry:not(.is-ap) {{ display: none; }}

.pdfbar {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }}
.pdfbar a {{
  border-bottom: none; font-size: 13px; font-weight: 600; color: var(--accent-ink);
  background: var(--accent-soft); padding: 8px 14px; border-radius: 8px;
}}
.pdfbar a:hover {{ background: var(--line-soft); }}

footer {{ margin-top: 64px; padding-top: 20px; border-top: 1px solid var(--line); font-size: 12.5px; color: var(--ink-soft); }}

@media print {{
  :root {{ --ink: #000; --ink-soft: #333; --paper: #fff; --paper-raised: #fff; --line: #999; --line-soft: #ccc; }}
  body {{ font-size: 10pt; }}
  .page {{ max-width: none; padding: 0; }}
  nav.jump, .filterbar, .pdfbar, .stats {{ display: none; }}
  section {{ margin: 0 0 18px; break-inside: avoid-page; }}
  .entries-wrap {{ border: none; padding: 0; }}
  .entry {{ break-inside: avoid; font-size: 10pt; }}
}}
</style>

<div class="page">

<header class="masthead">
  <p class="eyebrow">
    <span>Working in Python &middot; Full Vocabulary</span>
    <a href="{SITE}/alignment/vocabulary-by-chapter.html">&#8618; Vocabulary by Chapter</a>
    <a href="{SITE}/alignment/ap-vocabulary-coverage.html">&#8618; AP CSP Vocabulary Coverage</a>
  </p>
  <h1>AP CSP Vocabulary Glossary</h1>
  <p class="lede">Every term this book defines, merged with the full AP CSP exam vocabulary list, alphabetized into one reference &mdash; the two source pages linked above, combined for a binder tab instead of split by chapter or Big Idea.</p>
  <div class="stats">
    <div class="stat book"><div class="n">{len(full)}</div><div class="label">terms, A&ndash;Z</div></div>
    <div class="stat planned"><div class="n">{ap_count}</div><div class="label">on the AP CSP exam's own vocabulary list</div></div>
    <div class="stat elsewhere"><div class="n">{book_count}</div><div class="label">defined somewhere in this book (chapter linked)</div></div>
  </div>
  <p class="legend2">
    <span><sup class="ap">AP</sup> on the exam's vocabulary list</span>
    <span><sup class="ch">9</sup> defined in this book &mdash; chapter number links to it</span>
  </p>
  <div class="filterbar">
    <span class="filter-label">Studying for the exam?</span>
    <div class="segmented" role="group" aria-label="Vocabulary filter">
      <button type="button" class="seg-btn" data-filter="all" aria-pressed="true">All {len(full)} terms</button>
      <button type="button" class="seg-btn" data-filter="ap" aria-pressed="false">AP-tested only &middot; {ap_count}</button>
    </div>
    <span class="filter-count" id="filterCount"></span>
  </div>
  <div class="pdfbar">
    <a href="{SITE}/alignment/ap-vocabulary-glossary.pdf">Download printable PDF &middot; all {len(full)} terms</a>
    <a href="{SITE}/alignment/ap-vocabulary-glossary-ap-only.pdf">Download printable PDF &middot; AP-tested only ({ap_count})</a>
  </div>
</header>

<nav class="jump">
  <div class="jump-inner">
    {nav_links}
    <a class="external" href="{SITE}/alignment/ap-vocabulary-coverage.html">AP CSP coverage &#8599;</a>
  </div>
</nav>

<div class="glossary-columns">
{sections_html}
</div>

<footer>
  Vocabulary drawn from <i>Working in Python</i>, a fork of Allen Downey's <i>Think Python</i>, 3rd edition (CC BY-NC-SA&nbsp;4.0), and this course's own AP&nbsp;CSP vocabulary reference (<code>data/ap-vocabulary-source.md</code>). AP&nbsp;CSP definitions here are written in this course's own words, not copied from the College Board's Course and Exam Description. Repo-local source and full per-chapter/per-Big-Idea provenance: <a href="{SITE}/alignment/vocabulary-by-chapter.html">Vocabulary by Chapter</a> and <a href="{SITE}/alignment/ap-vocabulary-coverage.html">AP CSP Vocabulary Coverage</a>. For printing, use the PDF links above -- they paginate correctly; this HTML page's own browser-print output does not.
</footer>

</div>

<script>
(function() {{
  var STORAGE_KEY = "apVocabFilterMode";
  var AP_TOTAL = {ap_count};
  var ALL_TOTAL = {len(full)};
  var buttons = document.querySelectorAll(".seg-btn");
  var countEl = document.getElementById("filterCount");

  function applyMode(mode) {{
    document.body.classList.toggle("ap-only", mode === "ap");
    for (var i = 0; i < buttons.length; i++) {{
      var b = buttons[i];
      b.setAttribute("aria-pressed", b.getAttribute("data-filter") === mode ? "true" : "false");
    }}
    var sections = document.querySelectorAll('section[id^="letter-"]');
    for (var j = 0; j < sections.length; j++) {{
      var sec = sections[j];
      var apCount = parseInt(sec.getAttribute("data-ap-count"), 10) || 0;
      sec.style.display = (mode === "ap" && apCount === 0) ? "none" : "";
      var nameEl = sec.querySelector(".name");
      if (nameEl) {{
        var total = nameEl.getAttribute("data-total");
        var apHere = nameEl.getAttribute("data-ap");
        nameEl.textContent = mode === "ap"
          ? (apHere + (apHere === "1" ? " AP term" : " AP terms"))
          : (total + (total === "1" ? " term" : " terms"));
      }}
    }}
    var jumpLinks = document.querySelectorAll(".jump a[data-ap-count]");
    for (var k = 0; k < jumpLinks.length; k++) {{
      var a = jumpLinks[k];
      var apLinkCount = parseInt(a.getAttribute("data-ap-count"), 10) || 0;
      a.style.display = (mode === "ap" && apLinkCount === 0) ? "none" : "";
    }}
    if (countEl) {{
      countEl.textContent = mode === "ap" ? ("showing " + AP_TOTAL + " AP-tested terms") : ("showing all " + ALL_TOTAL + " terms");
    }}
    try {{ localStorage.setItem(STORAGE_KEY, mode); }} catch (e) {{}}
  }}

  for (var m = 0; m < buttons.length; m++) {{
    buttons[m].addEventListener("click", function(ev) {{ applyMode(ev.currentTarget.getAttribute("data-filter")); }});
  }}

  var saved = "all";
  try {{ saved = localStorage.getItem(STORAGE_KEY) || "all"; }} catch (e) {{}}
  applyMode(saved);
}})();
</script>
"""
    OUT_HTML.write_text(doc)


# --------------------------------------------------------------------- pdf --

def build_pdf(item_list, out_path, subtitle):
    try:
        import weasyprint
    except ImportError:
        print(f"SKIPPED {out_path.name}: weasyprint not installed (pip install weasyprint)")
        return

    groups = {}
    for e in item_list:
        letter = e["term"][0].upper() if e["term"][0].isalpha() else "#"
        groups.setdefault(letter, []).append(e)

    body_parts = []
    for letter in sorted(groups):
        body_parts.append(f'<h2 class="letter">{esc(letter)}</h2>')
        body_parts.extend(entry_div(e, linked=True) for e in groups[letter])

    doc = f"""<html><head><meta charset="utf-8"><style>
@page {{ size: letter; margin: 0.6in 0.6in 0.6in 0.75in; }}
* {{ box-sizing: border-box; }}
body {{ font-family: Georgia, "Times New Roman", serif; font-size: 9pt; line-height: 1.32; color: #000; }}
h1 {{ font-family: Helvetica, Arial, sans-serif; font-size: 16pt; margin: 0 0 2px; }}
.meta {{ font-family: Helvetica, Arial, sans-serif; font-size: 9pt; color: #333; margin: 0 0 8px; }}
.legend {{ font-family: Helvetica, Arial, sans-serif; font-size: 8.5pt; font-style: italic; color: #333; margin: 0 0 10px; }}
.cols {{ column-count: 2; column-gap: 0.4in; column-rule: 1px solid #999; column-fill: auto; }}
h2.letter {{
  font-family: Helvetica, Arial, sans-serif; font-weight: 700; font-size: 12pt;
  margin: 8px 0 3px; break-after: avoid; break-inside: avoid;
}}
.cols > h2.letter:first-child {{ margin-top: 0; }}
.entry {{ break-inside: avoid; margin: 0 0 4px; }}
.entry b {{ font-family: Helvetica, Arial, sans-serif; }}
sup.ap {{
  font-family: Helvetica, Arial, sans-serif; font-size: 7pt; font-weight: 700;
  letter-spacing: 0.02em; vertical-align: super; margin-left: 2px;
}}
sup.ch {{ font-family: Helvetica, Arial, sans-serif; font-size: 7pt; color: #333; vertical-align: super; margin-left: 2px; }}
sup.ch a {{ color: #333; text-decoration: underline; }}
i.note {{ color: #333; font-style: italic; }}
.footnote {{ font-family: Helvetica, Arial, sans-serif; font-size: 7.5pt; color: #333; margin-top: 10px; border-top: 0.75pt solid #000; padding-top: 5px; }}
</style></head>
<body>
<h1>AP CSP Vocabulary Glossary</h1>
<div class="meta">Working in Python &middot; alphabetical &middot; {len(item_list)} terms &middot; {subtitle}</div>
<div class="legend">Terms marked <sup class="ap">AP</sup> appear on the College Board AP CSP exam's own vocabulary list. A superscript chapter number links to where this book defines the term.</div>
<div class="cols">
{''.join(body_parts)}
</div>
<div class="footnote">
Vocabulary drawn from <i>Working in Python</i>, a fork of Allen Downey's <i>Think Python</i>, 3rd edition (CC BY-NC-SA 4.0), and this course's own AP CSP vocabulary reference. AP CSP definitions here are written in this course's own words, not copied from the College Board's Course and Exam Description.
</div>
</body></html>
"""
    weasyprint.HTML(string=doc).write_pdf(str(out_path))


def main():
    full = build_full_list()
    ap_count = sum(1 for e in full if e["ap"])
    book_count = sum(1 for e in full if e["chapters"])
    print(f"total={len(full)} ap={ap_count} book={book_count}")

    write_markdown(full)
    build_html(full)
    build_pdf(full, OUT_PDF_ALL, "all terms")
    build_pdf([e for e in full if e["ap"]], OUT_PDF_AP, "AP-tested terms only")

    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(f"wrote {OUT_HTML.relative_to(ROOT)}")
    if OUT_PDF_ALL.exists():
        print(f"wrote {OUT_PDF_ALL.relative_to(ROOT)}")
    if OUT_PDF_AP.exists():
        print(f"wrote {OUT_PDF_AP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
