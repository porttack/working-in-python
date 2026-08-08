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

**Rebuild and preview the JupyterLite copy:**
```
python3 tools/build_jupyterlite_content.py
.venv/bin/jupyter lite build --contents jupyterlite/content --output-dir jupyterlite/_output
cp -r jupyterlite/_output jb/_build/html/jupyterlite-vN     # vN = current jupyterlite/VERSION
```
`watch.sh` won't clobber that directory on its own, but a fresh `./watch.sh
--clean` (or anything that deletes `jb/_build/`) will — just rerun the three
commands above afterward.

## Publishing for real (bumping VERSION) — currently a manual, four-place step

**This part is not automated yet.** `jb/build.sh` reads whatever's in
`jupyterlite/VERSION` and deploys to that path; it does not decide when to
change it. If you change anything that affects what ships inside
`jupyterlite/content/` — either notebook's cells, a vendored dependency file,
or `tools/build_jupyterlite_content.py` itself — and you're about to publish
for real (`cd jb && ./build.sh`, no `--local`), you must, by hand, in this
order:

1. Bump `jupyterlite/VERSION` (e.g. `v4` → `v5`). Never reuse a number.
2. Find every hardcoded `jupyterlite-v4` literal and change it to match:
   ```
   grep -rn "jupyterlite-v[0-9]" chapters/ tools/
   ```
   As of this writing that's `chapters/chap01.ipynb` (twice — its own iframe
   `src`, and its link to `jupyter_intro.ipynb`), `chapters/jupyter_intro.ipynb`
   (its iframe `src`), and `tools/build_jupyterlite_content.py` (the
   `CELL_PATCHES` key for chap01's iframe cell, which must stay byte-identical
   to the real cell).
3. Regenerate `projector/` (`make projector`) since the chapter notebooks changed.
4. Run `make check`.
5. `cd jb && ./build.sh --local` first, verify locally, then `./build.sh` for real.

Skipping step 1 republishes under a URL a browser or school proxy may have
already cached — this has actually happened once (see `AUDIT.md`, "republished
... to the SAME jupyterlite-v1/"). Skipping step 2 leaves a stale, wrong version
number baked into a notebook, which mostly still works (old content is never
deleted mid-session) but is confusing and wrong the moment `VERSION` moves again.

*This four-place manual step is the thing most worth automating next — see
`AUDIT.md` for the standing note, and ask about it if it's not fixed yet by
the time you read this.*

## Adding a new chapter to the JupyterLite fallback

1. Add it to `CHAPTERS` in `tools/build_jupyterlite_content.py`, listing every
   vendored dependency file its `download()`/`!wget` cells need.
2. Run `python3 tools/build_jupyterlite_content.py --check` — it scans for any
   `!`-prefixed shell-magic line not already covered by `CELL_PATCHES` or the
   guarded-download pattern, and fails loudly (rather than silently breaking
   inside JupyterLite) if it finds one.
3. Follow the publish steps above (VERSION bump etc.) before it goes live.

## Adding or editing a page in the left nav (not a numbered chapter)

Edit `jb/_toc.yml`. Meta pages like `orientation.md`/`about.md`/the new
`jupyter_intro.ipynb` don't need sentinel blocks (they're not forked upstream
chapter content), but if the page's source file is a notebook rather than a
`.md` file, check `jb/build.sh`'s and `jb/watch.sh`'s copy steps — they only
copy filenames matching `chapNN.ipynb` or the ones explicitly listed by name.
A new notebook page needs an explicit `cp` line added in both places (this bit
us once with `jupyter_intro.ipynb` — see `AUDIT.md`, 2026-08-08 follow-up 10).

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
