# Vocabulary by Chapter

Every term from Downey's own chapter-ending `## Glossary` sections, chapters 1-18, plus any interludes' own glossaries, in reading order. Chapter 19 ("Final thoughts") has no glossary. This is the book's *own* vocabulary — see [`ap-vocabulary-coverage.md`](ap-vocabulary-coverage.md) for how it lines up against AP CSP's vocabulary, and [`glossary-map.md`](glossary-map.md) for the concept-level (not word-level) crosswalk written during Pass 3.

**204 terms across 18 chapters plus 1 interlude.**

## Chapter 1 — Welcome

| Term | Definition |
|---|---|
| **arithmetic operator** | A symbol, like `+` and `*`, that denotes an arithmetic operation like addition or multiplication. |
| **integer** | A type that represents numbers with no fractional or decimal part. |
| **floating-point** | A type that represents integers and numbers with decimal parts. |
| **integer division** | An operator, `//`, that divides two numbers and rounds down to an integer. |
| **expression** | A combination of variables, values, and operators. |
| **value** | An integer, floating-point number, or string — or one of other kinds of values we will see later. |
| **function** | A named sequence of statements that performs some useful operation. Functions may or may not take arguments and may or may not produce a result. |
| **function call** | An expression — or part of an expression — that runs a function. It consists of the function name followed by an argument list in parentheses. |
| **syntax error** | An error in a program that makes it impossible to parse — and therefore impossible to run. |
| **string** | A type that represents sequences of characters. |
| **concatenation** | Joining two strings end-to-end. |
| **type** | A category of values. The types we have seen so far are integers (type `int`), floating-point numbers (type ` float`), and strings (type `str`). |
| **operand** | One of the values on which an operator operates. |
| **natural language** | Any of the languages that people speak that evolved naturally. |
| **formal language** | Any of the languages that people have designed for specific purposes, such as representing mathematical ideas or computer programs. All programming languages are formal languages. |
| **bug** | An error in a program. |
| **debugging** | The process of finding and correcting errors. |

## Chapter 2 — Variables and Statements

| Term | Definition |
|---|---|
| **variable** | A name that refers to a value. |
| **assignment statement** | A statement that assigns a value to a variable. |
| **state diagram** | A graphical representation of a set of variables and the values they refer to. |
| **keyword** | A special word used to specify the structure of a program. |
| **import statement** | A statement that reads a module file so we can use the variables and functions it contains. |
| **module** | A file that contains Python code, including function definitions and sometimes other statements. |
| **dot operator** | The operator, `.`, used to access a function in another module by specifying the module name followed by a dot and the function name. |
| **evaluate** | Perform the operations in an expression in order to compute a value. |
| **statement** | One or more lines of code that represent a command or action. |
| **execute** | Run a statement and do what it says. |
| **argument** | A value provided to a function when the function is called. |
| **comment** | Text included in a program that provides information about the program but has no effect on its execution. |
| **runtime error** | An error that causes a program to display an error message and exit. |
| **exception** | An error that is detected while the program is running. |
| **semantic error** | An error that causes a program to do the wrong thing, but not to display an error message. |

## Chapter 3 — Functions

| Term | Definition |
|---|---|
| **function definition** | A statement that creates a function. |
| **header** | The first line of a function definition. |
| **body** | The sequence of statements inside a function definition. |
| **function object** | A value created by a function definition. The name of the function is a variable that refers to a function object. |
| **parameter** | A name used inside a function to refer to the value passed as an argument. |
| **loop** | A statement that runs one or more statements, often repeatedly. |
| **local variable** | A variable defined inside a function, and which can only be accessed inside the function. |
| **stack diagram** | A graphical representation of a stack of functions, their variables, and the values they refer to. |
| **frame** | A box in a stack diagram that represents a function call. It contains the local variables and parameters of the function. |
| **traceback** | A list of the functions that are executing, printed when an exception occurs. |

## Chapter 4 — Functions and Interfaces

| Term | Definition |
|---|---|
| **interface design** | A process for designing the interface of a function, which includes the parameters it should take. |
| **canvas** | A window used to display graphical elements including lines, circles, rectangles, and other shapes. |
| **encapsulation** | The process of transforming a sequence of statements into a function definition. |
| **generalization** | The process of replacing something unnecessarily specific (like a number) with something appropriately general (like a variable or parameter). |
| **keyword argument** | An argument that includes the name of the parameter. |
| **refactoring** | The process of modifying a working program to improve function interfaces and other qualities of the code. |
| **development plan** | A process for writing programs. |
| **docstring** | A string that appears at the top of a function definition to document the function's interface. |
| **multiline string** | A string enclosed in triple quotes that can span more than one line of a program. |
| **precondition** | A requirement that should be satisfied by the caller before a function starts. |
| **postcondition** | A requirement that should be satisfied by the function before it ends. |

## Chapter 5 — Conditionals and Recursion

| Term | Definition |
|---|---|
| **recursion** | The process of calling the function that is currently executing. |
| **modulus operator** | An operator, `%`, that works on integers and returns the remainder when one number is divided by another. |
| **boolean expression** | An expression whose value is either `True` or `False`. |
| **relational operator** | One of the operators that compares its operands: `==`, `!=`, `>`, `<`, `>=`, and `<=`. |
| **logical operator** | One of the operators that combines boolean expressions, including `and`, `or`, and `not`. |
| **conditional statement** | A statement that controls the flow of execution depending on some condition. |
| **condition** | The boolean expression in a conditional statement that determines which branch runs. |
| **block** | One or more statements indented to indicate they are part of another statement. |
| **branch** | One of the alternative sequences of statements in a conditional statement. |
| **chained conditional** | A conditional statement with a series of alternative branches. |
| **nested conditional** | A conditional statement that appears in one of the branches of another conditional statement. |
| **recursive** | A function that calls itself is recursive. |
| **base case** | A conditional branch in a recursive function that does not make a recursive call. |
| **infinite recursion** | A recursion that doesn't have a base case, or never reaches it. Eventually, an infinite recursion causes a runtime error. |
| **newline** | A character that creates a line break between two parts of a string. |

## Chapter 6 — Return Values

| Term | Definition |
|---|---|
| **return value** | The result of a function. If a function call is used as an expression, the return value is the value of the expression. |
| **side effect** | Any effect a function has other than returning a value, such as displaying output or drawing on a canvas. |
| **pure function** | A function that returns a value and has no side effects. |
| **dead code** | Part of a program that can never run, often because it appears after a `return` statement. |
| **incremental development** | A program development plan intended to avoid debugging by adding and testing only a small amount of code at a time. |
| **scaffolding** | Code that is used during program development but is not part of the final version. |
| **Turing complete** | A language, or subset of a language, is Turing complete if it can perform any computation that can be described by an algorithm. |
| **input validation** | Checking the parameters of a function to make sure they have the correct types and values |

## Interlude — Docstrings and Doctests

Between Chapter 6 and Chapter 7 — original content, not part of *Think Python*. See `CHAPTER_MANIFEST.md`'s Interludes section.

| Term | Definition |
|---|---|
| **docstring** | A string at the beginning of a function that documents what the function does; unlike a comment, it is stored on the function and can be read by the program. *(Python's name for what the exam calls* program documentation.*)* |
| **doctest** | An example call and its expected result, written inside a docstring, that can be run automatically to check the function. *(Python; not exam vocabulary.)* |
| **testing** | Checking that a program behaves correctly by running it on chosen inputs and comparing what comes out against what should have come out. |
| **test case** | A single input, paired with the result it should produce. |
| **boundary case** | A test case at the value where a function's behavior changes, such as zero, an empty string, or the first or last item. |
| **edge case** | A test case at an unusual or extreme input, where a function is most likely to be wrong. |
| **expected value** | What a test says the answer should be, as opposed to what the code actually produced. |
| **pass** | A test whose actual result matches its expected value. |
| **fail** | A test whose actual result does not match its expected value. |
| **hand tracing** | Working through code on paper line by line, writing down each variable's value, in order to find an error without running the program. |
| **semantic error** | An error that lets the program run but produces a wrong result. *(The exam calls this a* logic error.*)* |
| **roundoff error** | A loss of precision that happens because a fixed number of bits cannot represent some numbers exactly. |
| **program purpose** | The need a program serves, or the problem it solves; *why* it exists. |
| **program function** | What a program does when it runs, described as behavior. |
| **program input** | Data a program receives while it is running. |
| **program output** | What a program produces: displayed text, a returned value, a file, a sound, a movement. |
| **procedure** | The exam's word for a named, reusable block of code, whether or not it returns a value. This book says *function*. In older languages the two words were distinct: a procedure returned nothing, a function returned a value. |
| **regression** | A bug that reappears in code that used to work. Tests exist mainly to catch these. *(Professional vocabulary, not exam vocabulary.)* |

## Chapter 7 — Iteration and Search

| Term | Definition |
|---|---|
| **loop variable** | A variable defined in the header of a `for` loop. |
| **file object** | An object that represents an open file and keeps track of which parts of the file have been read or written. |
| **method** | A function that is associated with an object and called using the dot operator. |
| **update** | An assignment statement that give a new value to a variable that already exists, rather than creating a new variables. |
| **initialize** | Create a new variable and give it a value. |
| **increment** | Increase the value of a variable. |
| **decrement** | Decrease the value of a variable. |
| **counter** | A variable used to count something, usually initialized to zero and then incremented. |
| **linear search** | A computational pattern that searches through a sequence of elements and stops when it finds what it is looking for. |
| **pass** | If a test runs and the result is as expected, the test passes. |
| **fail** | If a test runs and the result is not as expected, the test fails. |

## Chapter 8 — Strings and Regular Expressions

| Term | Definition |
|---|---|
| **sequence** | An ordered collection of values where each value is identified by an integer index. |
| **character** | An element of a string, including letters, numbers, and symbols. |
| **index** | An integer value used to select an item in a sequence, such as a character in a string. In Python indices start from `0`. |
| **slice** | A part of a string specified by a range of indices. |
| **empty string** | A string that contains no characters and has length `0`. |
| **object** | Something a variable can refer to. An object has a type and a value. |
| **immutable** | If the elements of an object cannot be changed, the object is immutable. |
| **invocation** | An expression — or part of an expression — that calls a method. |
| **regular expression** | A sequence of characters that defines a search pattern. |
| **pattern** | A rule that specifies the requirements a string has to meet to constitute a match. |
| **string substitution** | Replacement of a string, or part of a string, with another string. |
| **shell command** | A statement in a shell language, which is a language used to interact with an operating system. |

## Chapter 9 — Lists

| Term | Definition |
|---|---|
| **list** | An object that contains a sequence of values. |
| **element** | One of the values in a list or other sequence. |
| **nested list** | A list that is an element of another list. |
| **delimiter** | A character or string used to indicate where a string should be split. |
| **equivalent** | Having the same value. |
| **identical** | Being the same object (which implies equivalence). |
| **reference** | The association between a variable and its value. |
| **aliased** | If there is more than one variable that refers to an object, the object is aliased. |
| **attribute** | One of the named values associated with an object. |

## Chapter 10 — Dictionaries

| Term | Definition |
|---|---|
| **dictionary** | An object that contains key-value pairs, also called items. |
| **item** | In a dictionary, another name for a key-value pair. |
| **key** | An object that appears in a dictionary as the first part of a key-value pair. |
| **value** | An object that appears in a dictionary as the second part of a key-value pair. This is more specific than our previous use of the word "value". |
| **mapping** | A relationship in which each element of one set corresponds to an element of another set. |
| **hash table** | A collection of key-value pairs organized so that we can look up a key and find its value efficiently. |
| **hashable** | Immutable types like integers, floats and strings are hashable. Mutable types like lists and dictionaries are not. |
| **hash function** | A function that takes an object and computes an integer that is used to locate a key in a hash table. |
| **accumulator** | A variable used in a loop to add up or accumulate a result. |
| **filtering** | Looping through a sequence and selecting or omitting elements. |
| **call graph** | A diagram that shows every frame created during the execution of a program, with an arrow from each caller to each callee. |
| **memo** | A computed value stored to avoid unnecessary future computation. |

## Chapter 11 — Tuples

| Term | Definition |
|---|---|
| **pack** | Collect multiple arguments into a tuple. |
| **unpack** | Treat a tuple (or other sequence) as multiple arguments. |
| **zip object** | The result of calling the built-in function `zip`, can be used to loop through a sequence of tuples. |
| **enumerate object** | The result of calling the built-in function `enumerate`, can be used to loop through a sequence of tuples. |
| **sort key** | A value, or function that computes a value, used to sort the elements of a collection. |
| **data structure** | A collection of values, organized to perform certain operations efficiently. |

## Chapter 12 — Text Analysis and Generation

| Term | Definition |
|---|---|
| **default value** | The value assigned to a parameter if no argument is provided. |
| **override** | To replace a default value with an argument. |
| **deterministic** | A deterministic program does the same thing each time it runs, given the same inputs. |
| **pseudorandom** | A pseudorandom sequence of numbers appears to be random, but is generated by a deterministic program. |
| **bigram** | A sequence of two elements, often words. |
| **trigram** | A sequence of three elements. |
| **n-gram** | A sequence of an unspecified number of elements. |
| **rubber duck debugging** | A way of debugging by explaining a problem aloud to an inanimate object. |

## Chapter 13 — Files and Databases

| Term | Definition |
|---|---|
| **ephemeral** | An ephemeral program typically runs for a short time and, when it ends, its data are lost. |
| **persistent** | A persistent program runs indefinitely and keeps at least some of its data in permanent storage. |
| **directory** | A collection of files and other directories. |
| **current working directory** | The default directory used by a program unless another directory is specified. |
| **path** | A string that specifies a sequence of directories, often leading to a file. |
| **relative path** | A path that starts from the current working directory, or some other specified directory. |
| **absolute path** | A path that does not depend on the current directory. |
| **f-string** | A string that has the letter `f` before the opening quotation mark, and contains one or more expressions in curly braces. |
| **configuration data** | Data, often stored in a file, that specifies what a program should do and how. |
| **serialization** | Converting an object to a string. |
| **deserialization** | Converting a string to an object. |
| **database** | A file whose contents are organized to perform certain operations efficiently. |
| **key-value stores** | A database whose contents are organized like a dictionary with keys that correspond to values. |
| **binary mode** | A way of opening a file so the contents are interpreted as sequence of bytes rather than a sequence of characters. |
| **hash function** | A function that takes and object and computes an integer, which is sometimes called a digest. |
| **digest** | The result of a hash function, especially when it is used to check whether two objects are the same. |

## Chapter 14 — Classes and Functions

| Term | Definition |
|---|---|
| **object-oriented programming** | A style of programming that uses objects to organize code and data. |
| **class** | A programmer-defined type. A class definition creates a new class object. |
| **class object** | An object that represents a class — it is the result of a class definition. |
| **instantiation** | The process of creating an object that belongs to a class. |
| **instance** | An object that belongs to a class. |
| **attribute** | A variable associated with an object, also called an instance variable. |
| **object diagram** | A graphical representation of an object, its attributes, and their values. |
| **format specifier** | In an f-string, a format specifier determines how a value is converted to a string. |
| **pure function** | A function that does not modify its parameters or have any effect other than returning a value. |
| **functional programming style** | A way of programming that uses pure functions whenever possible. |
| **prototype and patch** | A way of developing programs by starting with a rough draft and gradually adding features and fixing bugs. |
| **design-first development** | A way of developing programs with more careful planning that prototype and patch. |

## Chapter 15 — Classes and Methods

| Term | Definition |
|---|---|
| **object-oriented language** | A language that provides features to support object-oriented programming, notably user-defined types. |
| **method** | A function that is defined inside a class definition and is invoked on instances of that class. |
| **receiver** | The object a method is invoked on. |
| **static method** | A method that can be invoked without an object as receiver. |
| **instance method** | A method that must be invoked with an object as receiver. |
| **special method** | A method that changes the way operators and some functions work with an object. |
| **operator overloading** | The process of using special methods to change the way operators with with user-defined types. |
| **invariant** | A condition that should always be true during the execution of a program. |

## Chapter 16 — Classes and Objects

| Term | Definition |
|---|---|
| **shallow copy** | A copy operation that does not copy nested objects. |
| **deep copy** | A copy operation that also copies nested objects. |
| **polymorphism** | The ability of a method or operator to work with multiple types of objects. |

## Chapter 17 — Inheritance

| Term | Definition |
|---|---|
| **inheritance** | The ability to define a new class that is a modified version of a previously defined class. |
| **encode** | To represent one set of values using another set of values by constructing a mapping between them. |
| **class variable** | A variable defined inside a class definition, but not inside any method. |
| **totally ordered** | A set of objects is totally ordered if we can compare any two elements and the results are consistent. |
| **delegation** | When one method passes responsibility to another method to do most or all of the work. |
| **parent class** | A class that is inherited from. |
| **child class** | A class that inherits from another class. |
| **specialization** | A way of using inheritance to create a new class that is a specialized version of an existing class. |

## Chapter 18 — Python Extras

| Term | Definition |
|---|---|
| **factory** | A function used to create objects, often passed as a parameter to a function. |
| **conditional expression** | An expression that uses a conditional to select one of two values. |
| **list comprehension** | A concise way to loop through a sequence and create a list. |
| **generator expression** | Similar to a list comprehension except that it does not create a list. |
| **test discovery** | A process used to find and run tests. |

