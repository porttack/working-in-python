# Chapter Manifest

Filename → chapter mapping, resolved by reading each chapter's actual title (first
top-level heading in the `.md` rendering) and cross-checked against `jb/_toc.yml`, the
upstream Jupyter Book table of contents. Upstream numbering starts at `chap00`, which is
front matter (Preface), not Chapter 0. The "Chapters" part of the TOC runs `chap01`
through `chap19`, numbered, so **file number == chapter number for chap01–chap19.**
`jupyter_intro` is not listed in `jb/_toc.yml` at all — it's supplementary material read
before Chapter 1, not a numbered chapter.

VA decision follows the default proposed in `mods/pass-1-survey.md` Step 1 (chapters 1–8
`strip`, 9–11 `decide`, 12–13 `decide` leaning `keep`, 14–19 `keep`), which is finer-grained
than the treatment matrix in `CLAUDE.md` for chapters 1–11. Treatment tier is otherwise
taken directly from that matrix.

| File | Chapter # | Title | Treatment | VA decision |
|---|---|---|---|---|
| `chap00.md` / `.ipynb` | — (front matter) | Preface | not a chapter | n/a |
| `chap01.md` / `.ipynb` | 1 | Welcome | Live, 1–11 | strip |
| `chap02.md` / `.ipynb` | 2 | Variables and Statements | Live, 1–11 | strip |
| `chap03.md` / `.ipynb` | 3 | Functions | Live, 1–11 | strip |
| `chap04.md` / `.ipynb` | 4 | Functions and Interfaces | Live, 1–11 | strip |
| `chap05.md` / `.ipynb` | 5 | Conditionals and Recursion | Live, 1–11 | strip |
| `chap06.md` / `.ipynb` | 6 | Return Values | Live, 1–11 | strip |
| `chap07.md` / `.ipynb` | 7 | Iteration and Search | Live, 1–11 | strip |
| `chap08.md` / `.ipynb` | 8 | Strings and Regular Expressions | Live, 1–11 | strip |
| `chap09.md` / `.ipynb` | 9 | Lists | Live, 1–11 | decide |
| `chap10.md` / `.ipynb` | 10 | Dictionaries | Live, 1–11 | decide |
| `chap11.md` / `.ipynb` | 11 | Tuples | Live, 1–11 | decide |
| `chap12.md` / `.ipynb` | 12 | Text Analysis and Generation | May, post-exam, 12–13 | decide, leaning keep |
| `chap13.md` / `.ipynb` | 13 | Files and Databases | May, post-exam, 12–13 | decide, leaning keep |
| `chap14.md` / `.ipynb` | 14 | Classes and Functions | Independent study, 14–19 | keep |
| `chap15.md` / `.ipynb` | 15 | Classes and Methods | Independent study, 14–19 | keep |
| `chap16.md` / `.ipynb` | 16 | Classes and Objects | Independent study, 14–19 | keep |
| `chap17.md` / `.ipynb` | 17 | Inheritance | Independent study, 14–19 | keep |
| `chap18.md` / `.ipynb` | 18 | Python Extras | Independent study, 14–19 | keep |
| `chap19.md` / `.ipynb` | 19 | Final thoughts | Independent study, 14–19 | keep |
| `jupyter_intro.md` / `.ipynb` | not numbered | *Think Python* on Jupyter | supplementary, read before Ch. 1; absent from `jb/_toc.yml` | n/a |

## Non-chapter files, confirmed

- **`chap00`** — Preface. Front matter, precedes the numbered chapters in
  `jb/_toc.yml`'s "Front Matter" part. No chapter number.
- **`jupyter_intro`** — a standalone notebook/orientation to Jupyter, linked from Chapter 1
  (`chap01.md` references it directly as "Jupyter notebook introduction"). Not present in
  `jb/_toc.yml` at all, so upstream doesn't treat it as part of the chapter sequence either.
- No separate appendix files exist under `chapters/`. `chap18` ("Python Extras") is the
  closest thing to an appendix but is a numbered chapter (19 total: 1–19) and is treated as
  such.

## Naming collision to flag, not fix

A directory named **`blank/`** (singular) already exists at the repo root and is tracked
by `jb/_toc.yml` as an "End Matter" part. It is an **upstream build artifact**: each
`blank/chapNN.ipynb` is the same notebook with markdown prose kept but code cells and their
surrounding narration compressed out — not the same thing as this project's own
**`blanks/`** (plural), which will hold Pass 2/3-generated notebooks with blank markers
resolved to underscores. The two names are one character apart. Recommend leaving `blank/`
untouched and never pointing `tools/build_blanks.py` output at it. Confirming this instead
of silently renaming or deleting anything, per `CLAUDE.md`'s destructive-action guidance.

## Discrepancy to flag, not fix

`CLAUDE.md` states pass files live at `docs/pass-1-survey.md`, `docs/pass-2-surgery.md`,
`docs/pass-3-alignment.md`. The file actually supplied for this pass is
`mods/pass-1-survey.md` — a different directory. No `docs/` directory exists yet. Proceeding
on the explicit instruction to follow `mods/pass-1-survey.md`, but this should be reconciled
(rename `mods/` to `docs/`, or update `CLAUDE.md`) before Pass 2 starts, so the next cold
read doesn't stall on the same ambiguity.
