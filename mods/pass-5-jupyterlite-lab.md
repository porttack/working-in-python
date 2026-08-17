# Pass 5 — JupyterLite lab view and naming

Read `CLAUDE.md` first, then the last handoff note in `AUDIT.md`. Do not read the other
pass files.

**Mode:** additive tooling/build work — `chapters/index.ipynb`, `tools/build_jupyterlite_content.py`
(`CONTENT_NAMES`, `overrides.json`), `jb/_static/custom.js` — plus, going forward, a small
piece of *every* future Pass 4 chapter chrome step and every future Pass 2/4 chapter added
to `CHAPTERS`. This pass doesn't touch chapter exposition, glossary, exercises, or the
standards block; that's Passes 2 and 3.

**Blocked by:** nothing to start. But the two forward-looking steps below (adding a
chapter's chrome links, adding a chapter to `CHAPTERS` for the first time) are each blocked
on Pass 4 and Pass 2/4 respectively having done their part of that chapter first — this
pass only supplies the *name*, not the chrome cells or the dependency list.

**Scope note:** `CONTENT_NAMES` in `tools/build_jupyterlite_content.py` may have entries for
a chapter that isn't in `CHAPTERS` yet (chapters 12–19 today) — those are inert until
`CHAPTERS` catches up. Don't read a `CONTENT_NAMES` entry as evidence the chapter already
ships into JupyterLite; check `CHAPTERS` for that.

---

## What earlier sessions found that changes this pass

1. **JupyterLite's *lab* app cannot deep-link to a file** the way the *notebooks* app's
   `?path=` can — confirmed by reading the built JS bundles (`lab` routes through
   `/lab/tree/<file>` pathname matching, which 404s on GitHub Pages; `?path=` is a
   Notebook-7-only feature). **Sort order is the only lever available** for making the
   right file obvious in lab. If a future `jupyterlite-core` upgrade adds lab-side
   deep-linking, re-check before assuming the naming scheme is still the only option — but
   it costs nothing to keep either way.
2. **The `teach` prefix requires `sortNotebooksFirst` (root `overrides.json`) to group
   correctly, and this is load-bearing, not cosmetic.** Unlike the old `blank-`/`-projector`
   prefixes, `teach` starts with a letter, so without `sortNotebooksFirst` it sorts
   alphabetically among the upstream helper `.py`/`.txt` files instead of with the other
   notebooks. There is no punctuation that sorts after letters, so there is no naming-only
   fallback if this setting ever stops taking effect — stop and raise it, don't invent a new
   prefix.
3. **`.jupyterlite.doit.db`'s incremental build cache merges `settingsOverrides` forward,
   never replaces it** — a stale key from a source file that no longer exists (or never
   existed on this machine) can silently survive builds indefinitely. When verifying a
   settings change, build into a fresh `--output-dir` at least once to rule out the cache
   lying to you, rather than trusting whatever's already sitting in `jupyterlite/_output/`.
   See `AUDIT.md`, 2026-08-09, for a live example (a dead `loadPyodideOptions` override that
   "deletion" never actually removed).
4. **`CONTENT_NAMES` descriptions are derived from each chapter's own H1**, slugified, not
   hand-typed — read the chapter, don't guess. If a chapter's title wording ever changes,
   its `CONTENT_NAMES` entry (and, if that chapter already has chrome, its `?path=` links
   and `CELL_PATCHES` key) goes stale silently; nothing checks this automatically.
5. **`index.ipynb` and the `-exercises` notebooks deliberately have no `"teach"` key.** A
   blanked title-and-one-empty-cell notebook is meaningless clutter — this was a real bug
   (eight pointless `chapNN-exercises-projector.ipynb` files shipping) fixed by making
   `"teach"` opt-in rather than automatic for any notebook with a `projector/` copy. Don't
   add a `"teach"` entry to a notebook just because `projector/` happens to have produced one
   for it — check whether a blanked copy makes sense for that notebook first.

---

## Order of work

1. **Front page, naming foundation, sticky read-only nav** — done, 2026-08-09. See
   `AUDIT.md`'s "JupyterLite lab view: front page as a notebook, student-legible filenames"
   handoff for the full account: `chapters/index.ipynb` replacing `jb/index.md`,
   `CONTENT_NAMES` covering everything currently in `CHAPTERS` (index, jupyter_intro,
   chapters 1–11, the eight exercises notebooks), root `overrides.json`, and the
   `?readonly`-persists-through-the-left-nav feature in `jb/_static/custom.js`.
2. **Chapters 9–11** — `CONTENT_NAMES` entries already exist (`chapter09-lists.ipynb` etc.,
   with `teach` names). Chrome links not yet updated because Pass 4 hasn't written these
   chapters' link bar/embedded pane yet. When it does, use "Adding a chapter's chrome links"
   below instead of copying a literal `chapNN.ipynb` from an earlier chapter.
3. **Chapters 12–13** — `CONTENT_NAMES` entries pre-populated, including `teach` names
   (full blank markers per `CLAUDE.md`'s treatment matrix). Not yet in `CHAPTERS` — no
   dependency list known yet. See "Adding a chapter to CHAPTERS" below once Pass 2 reaches
   them.
4. **Chapters 14–19** — `CONTENT_NAMES` entries pre-populated, deliberately with no `teach`
   key (no blank markers by design, independent-study tier). Same as above otherwise.

---

## Adding a chapter's chrome links (once Pass 4 creates them)

When Pass 4 writes a chapter's link bar and embedded pane for the first time
(`mods/pass-4-chrome.md`, Steps 3–5), its literal `chapNN.ipynb` text is wrong for every
`?path=` link and the `CELL_PATCHES` iframe `src` — those all need the name from
`CONTENT_NAMES`, not the bare chapter filename:

- Chapter link (`?path=chapNN.ipynb`) → `CONTENT_NAMES["chapNN.ipynb"]["name"]`
- There is no separate Exercises link/notebook anymore (superseded 2026-08-16 -- see
  `mods/pass-4-chrome.md`'s Step 1 and `AUDIT.md`). Homework lives in the chapter's own
  `## Extra Exercises` section instead.
- "Blank"/Teach Copy link (`?path=chapNN-projector.ipynb`) →
  `CONTENT_NAMES["chapNN.ipynb"]["teach"]` — and use the label **"Teach Copy (JupyterLite)"**,
  not "Blank (JupyterLite)" (retired along with the `-projector` suffix; chapters 1–8 already
  use the new label).
- The `CELL_PATCHES` entry's iframe line uses the same `CONTENT_NAMES[...]["name"]` value.

Verify the same way Pass 4 already does (`apply_cell_patches` round-trip), plus confirm the
`?path=` value byte-matches `CONTENT_NAMES` — a typo here fails silently (the JupyterLite
build won't error; the link just 404s in a browser).

## Adding a chapter to CHAPTERS for the first time (12–19)

1. Confirm `CONTENT_NAMES["chapNN.ipynb"]` still matches the chapter's current H1 — titles
   can drift between when this pass pre-populated the entry and when Pass 2 actually reaches
   it. Regenerate the slug from the current title if it's changed, and flag the change here
   and in `AUDIT.md` — it changes what ships to students, not just an internal name.
2. Add the `CHAPTERS` entry with the chapter's real dependencies (read its `download()`
   cells — same as every chapter 1–11 entry already there).
3. `make check`.

---

## Handoff

Append to `AUDIT.md`:

- which chapters' chrome links (if any) were updated to use `CONTENT_NAMES` this round
- which chapters (if any) were newly added to `CHAPTERS`, and whether their pre-populated
  `CONTENT_NAMES` entry needed correcting for title drift first
- anything found that suggests the naming scheme itself (not just its application to one
  chapter) needs to change — stop and raise it rather than deciding alone, the same as
  Pass 4's own handoff rule
- update this file's Order of work section and `CLAUDE.md`'s status table to match
