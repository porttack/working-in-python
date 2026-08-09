# Pass 4 — Chapter Chrome

Read `CLAUDE.md` first, then the last handoff note in `AUDIT.md`. Do not read the other
pass files.

**Mode:** destructive edits to `chapters/*.ipynb`, but scoped to front/back matter only —
the link bar, the embedded live JupyterLite pane, the retail-links cell, and the closing
attribution note. Never the exposition, glossary, or exercises in between; that is Pass 2's
job. Never the standards-alignment block at the bottom; that is Pass 3's job.

**Blocked by:** nothing from Pass 1/2/3. This pass is orthogonal to chapter-surgery content —
it can run before, after, or interleaved with Pass 2/3 work on the same chapter without
conflict, since it never touches the cells they touch.

**Only in scope for a chapter that is Live/`strip` (chapters 1–11 per the treatment matrix in
`CLAUDE.md`) and already listed in `CHAPTERS` in `tools/build_jupyterlite_content.py`.**
Chapters 12–19 are `keep`/independent study or post-exam and get none of this — no link bar,
no embedded pane, no exercises notebook. Confirm the chapter's row in `CHAPTER_MANIFEST.md`
before starting one.

---

## What earlier sessions found that changes this pass

1. **The mechanics live in `HOW_TO_EDIT.md`, not here.** This file is scope and order of
   work; `HOW_TO_EDIT.md`'s "Editing something that also runs in JupyterLite" section has the
   `CELL_PATCHES`/deploy-path/preload mechanics that make the embedded pane and the
   JupyterLite link work at all. Read both before starting a chapter.
2. **`NotebookEdit` is not safe for byte-parity-sensitive cells.** At least once, editing a
   cell's `source` through that tool HTML-entity-escaped `<!--`/`-->` into `&lt;`/`&gt;`, and
   separately stored the edited cell with `source` as a single string and `metadata` moved
   after it, rather than this repo's usual list-of-lines/metadata-before-source convention —
   which, once the whole notebook gets rewritten by a naive `json.dump`, reorders *every*
   cell's keys (code cells key `source` after `outputs`; markdown cells don't). Do the cell
   edits in Step 3–5 below as a plain Python `json.load`/mutate/`json.dump` (`indent=1,
   ensure_ascii=False`, cells as plain dicts in the correct key order), not through
   `NotebookEdit`. Verify with `git diff --stat` before trusting any edit to one of these
   cells — a handful of touched cells should produce a small diff; hundreds of lines means
   something reformatted the whole file.
3. **The embedded pane's visible text must not assume the book site's chrome exists.**
   Outside the JB site (Colab, a raw download, a Codespace) there is no sidebar and no
   divider to drag, so pane text describing either reads as broken. Use
   `*Ignore this cell — used when running JupyterLite.*` (wrapped in `<p id="...-note">` so
   the script can target it), not anything describing the live-pane experience itself.
4. **A chapter with the embedded pane needs a `?readonly` escape hatch**, or its "Markdown"/
   "Read Only" link bar entry is worthless — without it, that link points at the exact same
   page the pane takes over, which is neither printable nor searchable. See Step 4.
5. **Upstream's own `blank/chapNN.ipynb` (all code cells emptied, prose intact) is not the
   same thing as our `projector/chapNN.ipynb`** (prose-blank-and-prompt teaching copy, Pass
   2's output). The link bar's "Blank" entry currently points at `projector/` on purpose —
   confirmed with the user, not an oversight. Do not repoint it without asking again.

---

## Order of work

1. **Chapters 1–2** — done. Not a single pass; built up across several sessions of live
   testing against the real deployed site (see `AUDIT.md`, 2026-08-08 follow-ups 13, 16, 18,
   and 2026-08-09 follow-ups 19–21). Treat these two chapters' current state as the reference
   pattern, not any single commit in isolation.
2. **Chapters 3–8** — done, 2026-08-09, matched the reference pattern (chapter 3 first, then
   4-6 as a batch, then 7-8). Chapter 8 needed one wrinkle: it already had a `CELL_PATCHES`
   entry (its `!head`/`!tail` shell-magic fixes) that the new pane patch had to be merged
   into rather than added as a second top-level key. See `AUDIT.md`'s "chapter 3 gets the
   chapter-1/2 chrome treatment", "chapters 4-6 get the same chrome treatment", and
   "chapters 7-8 get the same chrome treatment; chap08's CELL_PATCHES merge" handoffs.
3. **Chapters 9–11** — not started. Apply the pattern from chapters 1–8 exactly, one chapter
   (or a small batch) at a time, with `make check` passing before moving to the next. Check
   each for a pre-existing `CELL_PATCHES` entry before writing a fresh top-level key, the
   way chapter 8 required.
4. **Chapters 12–19** — out of scope entirely. Confirm this hasn't drifted (a chapter moving
   tiers in `CHAPTER_MANIFEST.md` would change it) before skipping them.

---

## Step 1 — Exercises notebook

Create `chapters/chapNN-exercises.ipynb`: copy `chap01-exercises.ipynb` exactly, changing
only the `# Chapter N exercises` heading and the two cell ids. Register it in `CHAPTERS` in
`tools/build_jupyterlite_content.py` with an empty dependency list (`[]`) — it has no deps
until it has real content.

## Step 2 — Drop the retail-links cell

If the chapter still has one — a leading markdown cell offering Bookshop.org/Amazon
print-edition links — delete it outright. Nothing takes its place.

## Step 3 — Link bar

Insert as the new first cell, inside a `type="note"` sentinel block:

Exercises (pointing at the notebook from Step 1, marked `**TODO:**` if it's still blank) |
JupyterLite | Colab | Read Only | Download | Codespace (notebook) | Codespace (VS Code) |
Blank (JupyterLite) — copy the exact shape from chapter 1 or 2's link-bar cell, updating the
chapter number throughout.

- **JupyterLite / Blank links** use the `JUPYTERLITE_DEPLOY_PATH` placeholder (see
  `tools/build_jupyterlite_content.py`) — never a hand-written hash. No new substitution
  wiring needed; it's a plain notebook cell and the existing substitution covers every cell.
- **Read Only** points at `https://python.porttack.com/chapNN.html?readonly` — the same
  rendered page, with the query flag from Step 4. Not a separate page.
- **Download** points at `https://python.porttack.com/_sources/chapNN.ipynb` with an
  explicit `download="chapNN.ipynb"` HTML attribute (markdown link syntax can't carry one, so
  this line is raw HTML in the cell) — `_sources/` is served as `application/x-ipynb+json`,
  which browsers don't render inline, unlike `raw.githubusercontent.com`'s `text/plain`.
- Drop the Codespace links if the chapter shouldn't have them (current chapter 1/2 state has
  removed both — confirm against the current pattern before copying, don't assume the list
  above is exhaustive if it's since changed again).

## Step 4 — Embedded live pane, with a `?readonly` escape hatch

Insert as the new second cell — copy chapter 1's or 2's pane cell verbatim, substituting the
chapter number in the sentinel's `chapter="NN"` attribute, the `id="chapNN-jupyterlite-pane"`
and `id="chapNN-jupyterlite-note"` (each appears twice: the HTML element and the script's
`getElementById` call), and the iframe's `?path=chapNN.ipynb`. Nothing else changes chapter
to chapter — in particular, the script's `URLSearchParams(location.search).has("readonly")`
guard, which hides both the pane and its note and returns before any positioning logic runs,
is chapter-number-independent and must be copied exactly.

## Step 5 — Matching `CELL_PATCHES` entry

Add an entry in `tools/build_jupyterlite_content.py` for `"chapNN.ipynb"`, keyed on the exact
tuple of lines from Step 4, so the copy that ships inside JupyterLite swaps the live pane for
a one-line placeholder note instead of recursively embedding itself. If the key doesn't match
byte-for-byte, this silently does nothing. **Verify programmatically, don't eyeball it:**

```python
import json, sys
sys.path.insert(0, "tools")
import build_jupyterlite_content as b
nb = json.load(open("chapters/chapNN.ipynb"))
patched = b.apply_cell_patches("chapNN.ipynb", nb["cells"])
assert any("already running" in "".join(c.get("source", [])) for c in patched)
```

## Step 6 — Attribution note

The closing note should open with a `---` rule before "**Working in Python** — modified
by...", the same as chapter 1's (added there in `f5aa6c0`). Some chapters were written before
that fix and are missing it — check, don't assume it's already there.

## Step 7 — Per-chapter checkout

1. `make projector && make check` — catches a missing/incorrect `CELL_PATCHES` entry
   (`jupyterlite --check` scans for unhandled `!`-shell-magic; the recursive-embed case has
   no automated check yet, so also eyeball the built `jupyterlite/content/chapNN.ipynb` for
   the placeholder note).
2. `git diff --stat` on every touched notebook — a handful of cells changed should produce a
   small diff. If it's not small, see "What earlier sessions found," item 2.
3. If a headless browser is available, actually load `?readonly` on the built page and
   confirm the pane and its note both disappear. If not, note in the handoff that this step
   was skipped and why (as of 2026-08-09, no headless-browser tooling was available in the
   session's environment, and this was verified only by exercising the script's three
   branches in Node with a stubbed `document`/`location`).

## Step 8 — Log it

A `CHANGELOG.md` entry and an `AUDIT.md` handoff note, same shape as the chapter-1/2 ones
this pass's pattern came from.

---

## Handoff

Append to `AUDIT.md`:

- which chapters were completed this round, and whether they matched the pattern exactly or
  needed a judgment call (and what it was)
- any `CELL_PATCHES` entries added, confirmed programmatically to fire
- anything found that suggests the pattern itself (not just this chapter's application of it)
  needs to change — if so, stop and raise it rather than deciding alone; the pattern is
  shared across every chapter that will ever use it
- update this file's Order of work section and `CLAUDE.md`'s status table to match
