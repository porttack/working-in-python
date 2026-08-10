# About This Book

*Working in Python* is the reading text for a high school AP Computer Science
Principles course. It is an adaptation of Allen Downey's
[*Think Python*, Third Edition](https://allendowney.github.io/ThinkPython/),
used and redistributed under the license Downey chose for it.

This page explains why it exists, what was changed, and what it deliberately
does not do. It is written for teachers, parents, and anyone who found the
repo and wondered what they were looking at.

---

## Why not use a curriculum that already exists?

Several good AP CSP curricula exist. Code.org's is free, thorough, and carries a
pre-approved Course Audit syllabus, which is a real convenience. CMU CS Academy
teaches Python. CodeHS is widely adopted. Using this book instead of one of them
costs me the audit shortcut and a great deal of authoring time, so the reasons
had better be good ones.

They come down to three.

**The programming text should be a book.** Most CSP curricula deliver
programming as a sequence of short activities inside a web platform. That works,
and students complete it. What it does not produce is a student who can sit down
with a chapter of technical prose and get something out of it. That skill is the
one that keeps paying after the course ends, in every later CS class and in every
job that involves code. A platform cannot teach it. A book can, if students are
actually required to read it.

**The language should be the one we use everywhere else.** I also teach robotics.
Our robots run Python. Our data work is Python. A student who spends a year in a
block environment or in App Lab has learned real computational thinking and then
has to start over on syntax. Starting in Python means the fall semester's work
transfers directly to the spring and to everything after.

**I want to be able to change it.** A hosted curriculum is a thing you follow. A
text you can edit is a thing you can fix. When a chapter runs long for my
students, I cut it. When my state standards need a paragraph the original does
not have, I add one, marked as mine. That is only possible because Downey
licensed his book to allow it.

## Why Downey's book specifically

*Think Python* has been the strongest free introductory Python text for well over
a decade, and the third edition made two changes that matter here. It is written
as Jupyter notebooks, so the prose and the runnable code are the same document.
And it takes software testing seriously, introducing doctest early, which almost
no beginner text does and which quietly builds the habit of asking whether your
code is right rather than whether it ran.

It is also unusually well built for adaptation. The vocabulary is defined
carefully and each chapter ends with a glossary, which turns out to matter more
than it sounds like it should. Learning to program means learning two languages:
Python, and the language people use to talk about Python. Downey is deliberate
about the second one. Students who have it can read an error message, read
documentation, and ask a precise question. Students who do not are stuck.

## Why Jupyter notebooks

Because the alternative is asking fourteen-year-olds to install a toolchain in
the first week of school, and that week is expensive.

Notebooks let a student open a chapter in a browser, run the examples, break
them, and fix them, in the same document they are reading. The chapter is not
a description of the code. It is the code. Every chapter here opens in JupyterLite
with nothing to install.

There is a real cost, which I want to state plainly rather than pretend away.
Notebooks encourage running cells out of order and leaving state lying around,
which is a genuinely bad habit, and they are not how professional Python is
written. We address that directly later in the year by moving to files and a
terminal. The first semester's priority is removing every obstacle between a
student and a running program.

## Why no AI assistants

I taught Harvard's cs50ap for two years with a prompt engineered AI [cs50.ai](https://cs50.ai). It helped some students. But too many students used it to do the cs50 problem sets. And later assessments proved they didn't really retain content.

The original book takes the opposite position. Downey wrote the third edition
partly to teach students to use virtual assistants well, and he is not wrong to.
Those sections are removed here.

Learning to program involves a specific unpleasant experience: you have a broken
program, you do not know why, and you have to reason your way to the cause. That
experience is the mechanism by which the skill is acquired. An assistant removes
it. Skipping it feels like progress and is not.

We spend real class time on why this line is drawn where it is. Students are
invited to disagree out loud.

## What was changed

The full record is in [`AP_MODIFICATIONS.md`](AP_MODIFICATIONS.md), which exists
both because the license requires changes to be indicated and because it doubles
as evidence for the AP Course Audit. In summary:

- **Virtual assistant material removed** from the chapters used in the fall,
  consistent with the AI policy above. Passages where Downey merely mentions
  assistants as a fact about the world are left alone. So is the Preface, where
  he describes his own pedagogy; editing an author's account of his own method
  is a larger intervention than this project needs.
- **Standards alignment blocks added**, mapping chapter content to AP CSP topics
  and to the California 9–12 computer science standards.
- **Additional graded exercises written**, separate from Downey's, so that his
  exercises can stay ungraded practice.
- **Fill-in-the-blank projector versions generated** from the chapters for
  live coding in class. These are built by script, never edited by hand.

Every addition is wrapped in comment sentinels, so what is Downey's and what is
mine can be separated mechanically at any time.

## What this book does not cover

This is a division of labor, not a gap I failed to fill.

*Working in Python* carries a considerable portion of the algorithms and programming content of AP CSP, and part of the creative development content through its
treatment of debugging, incremental development, and testing. It reaches some of
the data material through file and CSV work.

It does not cover binary representation, data compression, computer networks,
the internet, cybersecurity, or the global and ethical impacts of computing.
Those are between a third and a half of the exam. In this course they are
carried by a separate unit built around Cory Doctorow's novel *Little Brother*,
plus three computing innovation investigations. That unit is not a supplement.
It is structurally load-bearing, and it is where most of the course's writing and
argument happens.

## License and attribution

*Think Python*, Third Edition is copyright 2024 Allen B. Downey. Downey licensed
the text under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
and the code under the [MIT License](https://mit-license.org/).

This adaptation carries the same licenses. Text is CC BY-NC-SA 4.0, code is MIT.
That means you may use it, adapt it, and share your adaptation, for
non-commercial purposes, with attribution, under these same terms.

Downey sells print and ebook editions of the original. If this book is useful to
you, buy his. Full details in [`ATTRIBUTION.md`](ATTRIBUTION.md).

## Corrections

Errors introduced by this adaptation are mine. Corrections and suggestions are
welcome at **ericbrown@porttack.com**. If you are reporting a typo, quoting part of the
sentence it appears in makes it much easier to find than a page number.

Errors in the original book should go to Downey at `feedback@thinkpython.com`.
Please do not send him mine.
