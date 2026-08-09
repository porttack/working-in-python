# How to edit this book

A practical, task-oriented companion to `PUBLISHING.md` (which explains *why* the
site is built the way it is) and `CLAUDE.md` (which governs how upstream content
gets modified — sentinels, blank markers, the treatment matrix). Read this one
when you just want to know which file to open and what to run.

## Where things live: source vs. generated

Only edit files in the left column. Everything in the right column is rebuilt
from it and gets overwritten the next time someone runs the corresponding build
step — hand edits there are silently lost.

| Edit this (source) | Never this (generated) |
|---|---|
| `chapters/chapNN.ipynb`, `chapters/jupyter_intro.ipynb` | `projector/*.ipynb`, `jb/chapNN.ipynb`, `jb/jupyter_intro.ipynb`, `jupyterlite/content/*` |
| `jb/index.md`, `orientation.md`, `about.md`, `_toc.yml`, `_config.yml` | `jb/_build/` (the whole rendered site) |
| `tools/build_jupyterlite_content.py`, `jupyterlite/*.py` (the ones with no upstream file to fork, e.g. `ascii_art.py`, `check.py`) | `jupyterlite/_output/` |

If you're not sure which column a file is in: `git status` after a build. If a
build step keeps re-touching a file you didn't edit, it's generated.

## Everyday editing: chapter text, exercises, glossary

1. Open `chapters/chapNN.ipynb` in VS Code (or Jupyter) and edit it directly.
2. Follow the sentinel/blank-marker rules in `CLAUDE.md` if you're touching a
   numbered chapter — additions go in `<!-- apcsp:begin ... -->` blocks, upstream
   prose is never reflowed.
3. Preview live:
   ```
   cd jb && ./watch.sh
   ```
   Opens `http://localhost:8000/` and auto-reloads on every save to
   `chapters/*.ipynb`. This is fast because it deliberately **skips the
   JupyterLite build** — see the next section if what you're editing needs that.
4. Run the checks before committing:
   ```
   make check      # blanks/--check, check_sync, jupyterlite --check
   ```
5. If you touched an exercise, log it: see `data/exercise-ledger.json` /
   `tools/build_ledger.py` (`make ledger`).

## Editing something that also runs in JupyterLite

Right now, two notebooks embed a *live* JupyterLite instance of themselves,
filling the page next to the left nav: `chap01.ipynb` and `jupyter_intro.ipynb`
("About Jupyter Notebooks"). If you're editing one of those:

**The tutorial text/code cells** — edit normally, no extra steps beyond the
everyday flow above. `watch.sh` shows your text changes immediately; the
*embedded live copy* only picks them up after you rebuild JupyterLite (next
bullet), since `watch.sh` intentionally doesn't do that automatically.

**The live-embed pane cell itself** (the one containing the `<iframe>`, its
`<style>`, and the `ResizeObserver` script) — this is matched **byte-for-byte**
by an entry in `tools/build_jupyterlite_content.py`'s `CELL_PATCHES` dict, so
the copy of the notebook that ships *inside* JupyterLite can swap it for a
one-line note instead of trying to embed another copy of itself inside itself.
If you change this cell's text at all, update the matching `CELL_PATCHES` tuple
to match exactly, or the swap silently stops happening and the recursive-iframe
bug comes back (nothing will error — you'll just see it break in the browser).

**The iframe `src`/link itself uses a placeholder, not a literal path** —
`chap01.ipynb` and `jupyter_intro.ipynb` both carry the literal text
`JUPYTERLITE_DEPLOY_PATH` where the real `jupyterlite-<hash>` path goes. Leave
it as the placeholder in `chapters/`; it gets substituted automatically,
separately, for each of the two copies that need a real value (the one on the
JB site page, and the one inside `jupyterlite/content/`). You should basically
never need to touch this — see the next section.

**Rebuild and preview the JupyterLite copy:**
```
DEPLOY_ID=$(python3 tools/build_jupyterlite_content.py --print-deploy-id)
python3 tools/build_jupyterlite_content.py
.venv/bin/jupyter lite build --contents jupyterlite/content --output-dir jupyterlite/_output
cp -r jupyterlite/_output "jb/_build/html/${DEPLOY_ID}"
```
`watch.sh` won't clobber that directory on its own, but a fresh `./watch.sh
--clean` (or anything that deletes `jb/_build/`) will — just rerun the commands
above afterward. Note the id is content-derived (see next section) — if you
edited one of the two notebooks since your last rebuild, it will have changed,
and the old directory name is simply the wrong one now; there's nothing to
reconcile by hand, just rerun the four lines above.

## Publishing for real: the deploy path is automatic, not versioned by hand

`tools/build_jupyterlite_content.py --print-deploy-id` hashes every file that
affects what ships in `jupyterlite/content/` — both notebooks that embed
themselves, every vendored dependency, and the script itself — into
`jupyterlite-<hash>`. `jb/build.sh` computes this once, near the top, and
threads it through everything downstream (`prep_notebooks.py`'s placeholder
substitution, the JupyterLite build's own copy step). There is no `VERSION`
file and nothing to bump: changing any of those inputs changes the hash,
automatically, every time, and running the exact same inputs twice reproduces
the exact same hash. Just:

1. Edit whatever needed editing.
2. `make check`.
3. `cd jb && ./build.sh --local` first, verify locally, then `./build.sh` for real.

This used to be a manual, four-place, easy-to-forget step (bump a `VERSION`
file, then find and update three separate hardcoded copies of the version
number) — see `AUDIT.md`, 2026-08-08 follow-ups 8-10, for the two times
forgetting it actually broke something. Automated in follow-up 12; if you're
reading this and it's gone manual again, something regressed.

## Adding a new chapter to the JupyterLite fallback

1. Add it to `CHAPTERS` in `tools/build_jupyterlite_content.py`, listing every
   vendored dependency file its `download()`/`!wget` cells need.
2. Run `python3 tools/build_jupyterlite_content.py --check` — it scans for any
   `!`-prefixed shell-magic line not already covered by `CELL_PATCHES` or the
   guarded-download pattern, and fails loudly (rather than silently breaking
   inside JupyterLite) if it finds one.
3. `make check`, then publish per the steps above — no separate versioning step needed.

## Adding or editing a page in the left nav (not a numbered chapter)

Edit `jb/_toc.yml`. Meta pages like `orientation.md`/`about.md`/the new
`jupyter_intro.ipynb` don't need sentinel blocks (they're not forked upstream
chapter content), but if the page's source file is a notebook rather than a
`.md` file, check `jb/build.sh`'s and `jb/watch.sh`'s copy steps — they only
copy filenames matching `chapNN.ipynb` or the ones explicitly listed by name.
A new notebook page needs an explicit `cp` line added in both places (this bit
us once with `jupyter_intro.ipynb` — see `AUDIT.md`, 2026-08-08 follow-up 10).

## Adding a chapter's "ways to open this chapter" link bar

Chapters 1 and 2 have a one-line link bar near the top — Exercises |
JupyterLite | Colab | Markdown | Download | Codespace (notebook) | Codespace
(VS Code) | Blank (JupyterLite) — inside a `type="note"` sentinel block,
right after the chapter's opening cell.

**It's a markdown cell in the notebook itself, not sidebar or theme chrome.**
Two other shapes were tried first and abandoned — a `_toc.yml` `sections:`
entry (doesn't reach the sidebar unless every child is a real page, not a
`url:`) and a `custom.js`-injected sidebar disclosure (worked, but added a
second line to every chapter's entry in the contents, which wasn't wanted).
See `AUDIT.md`, 2026-08-08 follow-up 13, for both. Putting the bar in the
notebook instead means one edit shows up identically everywhere that
notebook is opened — Colab, JupyterLite, a Codespace, a raw download, and the
rendered page — which is also why the "Markdown" link matters: it's the only
one of these that gets a reader who arrived via any of the other five *back*
to the rendered page.

**To add another chapter:** copy the pattern from chapter 1 or 2's link-bar
cell, updating the chapter number throughout. For the JupyterLite link, use
the same `JUPYTERLITE_DEPLOY_PATH` placeholder those chapters' own embedded
panes use (see `tools/build_jupyterlite_content.py`) — never a hand-written
hash; it needs no new substitution wiring, since it's a plain notebook cell
and `prep_notebooks.py`/`jupyterlite/content`'s existing substitution already
covers every cell in the notebook, not just the ones that had it before.
Only add the JupyterLite link for a chapter that's actually in `CHAPTERS` in
`tools/build_jupyterlite_content.py` — for a chapter that's `keep`/independent
study (14-19, per the treatment matrix in `CLAUDE.md`), drop that one entry.

## Applying the chapter-1 chrome treatment to another chapter

Chapters 1 and 2 both carry a bundle of site-chrome pieces that has nothing to
do with chapter-surgery content (Pass 2 in `CLAUDE.md`/`AUDIT.md`) — it's
purely about how the chapter is opened and how it's framed at top and bottom.
This is the checklist to repeat for chapter 3 and onward, in order. See
`AUDIT.md`, 2026-08-08 follow-up 18, for the chapter-2 pass this was written
from.

**Only for chapters that are Live/`strip` (1–11 per the treatment matrix in
`CLAUDE.md`) and already listed in `CHAPTERS` in
`tools/build_jupyterlite_content.py`.** Chapters 12+ are `keep`/independent
study or post-exam and don't get the embedded pane or the JupyterLite link —
confirm the chapter's row in `CHAPTER_MANIFEST.md` before starting.

1. **Add the exercises notebook.** Create `chapters/chapNN-exercises.ipynb`:
   copy `chap01-exercises.ipynb` exactly, changing only the `# Chapter N
   exercises` heading and the two cell ids. Register it in `CHAPTERS` in
   `tools/build_jupyterlite_content.py` with an empty dependency list (`[]`)
   — it has no deps until it has real content.
2. **Drop the retail-links cell**, if the chapter still has one — a leading
   markdown cell offering Bookshop.org/Amazon print-edition links. Delete it
   outright; nothing takes its place.
3. **Insert the link bar** as the new first cell (see the section above for
   its exact shape), pointing the Exercises link at the notebook from step 1
   and the Blank link at `chapNN-projector.ipynb`.
4. **Insert the embedded live pane** as the new second cell — copy chapter
   1's or 2's pane cell verbatim, substituting the chapter number in the
   sentinel's `chapter="NN"` attribute, the `id="chapNN-jupyterlite-pane"`
   (both places it appears), and the iframe's `?path=chapNN.ipynb`. Nothing
   else in that cell changes chapter to chapter.
5. **Add a matching `CELL_PATCHES` entry** in
   `tools/build_jupyterlite_content.py` for `"chapNN.ipynb"`, keyed on the
   exact tuple of lines from step 4, so the copy that ships inside
   JupyterLite swaps the live pane for a one-line placeholder note instead of
   recursively embedding itself. If the key doesn't match byte-for-byte, this
   silently does nothing — see the `NotebookEdit` warning below.
6. **Fix the bottom attribution note** to open with a `---` rule before
   "**Working in Python** — modified by...", the same as chapter 1's (added
   there in `f5aa6c0`) — some earlier chapters were written before that fix
   and are missing it.
7. **Regenerate and check:** `make projector && make check`. This also
   catches a missing/incorrect `CELL_PATCHES` entry (`jupyterlite --check`
   scans for unhandled `!`-shell-magic, though the recursive-embed case
   itself has no automated check yet — eyeball the built
   `jupyterlite/content/chapNN.ipynb` for the placeholder note if in doubt).
8. **Log it**: a `CHANGELOG.md` entry and an `AUDIT.md` follow-up, same shape
   as the chapter-2 one this recipe came from.

**Watch out for `NotebookEdit` on cells that need to be byte-identical to
another chapter's cell** (steps 3–5 above). At least once, editing a cell's
`source` through that tool has HTML-entity-escaped `<!--`/`-->` into
`&lt;`/`&gt;`, and separately stored the edited cell with `source` as a
single string and `metadata` moved after it rather than this repo's usual
list-of-lines/metadata-before-source convention — which, if the whole
notebook then gets rewritten by a naive `json.dump`, reorders *every* cell's
keys the moment code cells (which key `source` after `outputs`) get mixed
into the same blanket fix as markdown cells. Both are easy to miss because
the tool's own echo of what it wrote looks correct. **Before trusting it**,
run `git diff --stat` on the notebook — a handful of touched cells should
produce a small diff; if it's hundreds of lines for a few intended changes,
something reformatted the whole file. If that happens, `git checkout` the
file and redo the edit as a plain Python `json.load`/mutate/`json.dump`
(`indent=1, ensure_ascii=False`, cells as plain dicts in the correct key
order) instead of through `NotebookEdit`.

## Local preview gotchas

- **`jb/_build/` isn't real output** — it's gitignored scratch, rebuilt from
  scratch by `./watch.sh --clean` or `./build.sh`. If a page 404s that worked
  five minutes ago, this is almost always why; see the JupyterLite-rebuild
  commands above.
- **Browser cache.** `python3 -m http.server` (what `jupyterlite-serve` uses)
  sends no `Cache-Control` header, so a tab left open across many rebuilds can
  keep serving old CSS/JS it fetched before a change existed. Hard-refresh
  (or open a fresh incognito window) before concluding a fix didn't work.
- **`watch.sh` never touches JupyterLite.** By design, for iteration speed. If
  what you're testing is inside an embedded JupyterLite pane, you need the
  manual rebuild+copy from above at least once per session.

## Full command reference

```
make check             # everything: blanks --check, check_sync, jupyterlite --check
make projector         # regenerate projector/ after editing a chapter
make ledger            # regenerate CHANGELOG_DETAIL.md from data/exercise-ledger.json
make jupyterlite       # build tools/build_jupyterlite_content.py + jupyter lite build
make jupyterlite-serve # serve jupyterlite/_output/ on :8123, standalone (no JB site chrome)
cd jb && ./watch.sh          # live-reload preview of the real site, fast, no JupyterLite
cd jb && ./watch.sh --clean  # same, but wipe _build/ first
cd jb && ./build.sh --local  # full real build (site + JupyterLite), no publish
cd jb && ./build.sh           # full real build AND publish (force-pushes gh-pages)
```
