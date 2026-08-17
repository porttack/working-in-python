# Publishing

How the website is built, and why it is built this way. Read this before
changing anything in `jb/`. Looking for which file to edit and what to run,
rather than the architecture and reasoning? See `HOW_TO_EDIT.md` instead.

## The site is a Jupyter Book, not a Jekyll site

Upstream builds with Jupyter Book, config isolated in `jb/`. This fork keeps
that. The reasons, recorded so this does not get relitigated:

- **The pipeline already exists.** Adopting it cost a TOC edit and one changed
  line in `build.sh`.
- **Navigation is generated.** `_toc.yml` produces the sidebar, chapter
  numbering, next/previous links, and full-text search. Nothing links to
  chapters by hand, so nothing rots when a chapter moves.
- **Chapters render as web pages.** A student can read a chapter without
  launching Colab. A Jekyll site would have been a page of links to notebooks.
- **Jekyll and Jupyter Book cannot coexist.** Jekyll strips directories whose
  names start with an underscore, and `_static/` holds every stylesheet and
  script in the book. This is why `.nojekyll` is mandatory, and why
  `ghp-import -n` in `build.sh` is not a stylistic choice.

## Architecture

| | |
|---|---|
| Source of truth | `chapters/*.ipynb` on `main` |
| Site source | `jb/` on `main` |
| Build | `cd jb && ./build.sh`, run locally |
| Published output | `gh-pages` branch, force-pushed |
| Served at | `python.porttack.com` |

GitHub Pages source must be set to **branch `gh-pages`, folder `/`**. Not
`/docs`, not `main`.

`jb/` contains four tracked prose files plus config: `index.md`,
`orientation.md`, `about.md`, `_toc.yml`, `_config.yml`, `build.sh`,
`prep_notebooks.py`, and `extra/CNAME`. The `chap*.ipynb` files that appear
there during a build are copies and must never be committed.

## Add this to .gitignore

Non-optional. Without it, every build leaves twenty-one mutated notebooks in
`git status`, and the failure mode is committing solution-stripped copies over
the real chapters.

```gitignore
# Jupyter Book build artifacts
jb/chap*.ipynb
jb/jupyter_intro.ipynb
jb/_build/
```

## prep_notebooks.py is not optional

It looks like it only blanks solution cells. It does three things:

1. Empties cells whose source starts with `# Solution`.
2. Strips `%%expect` cell magic, which would otherwise render as visible junk
   in chapters that demonstrate exceptions.
3. **Injects `(section_name)=` MyST labels from cell tags.** Downey's chapters
   contain internal cross-references such as
   `[a previous section](section_dictionary_in_operator)`. Without the labels,
   the book builds successfully with every internal link silently broken.

Point 3 is the one that will bite. A clean build is not evidence of a correct
build.

## Divergence from upstream build.sh

Downey copies from `../ThinkPythonSolutions/soln/`, because his site publishes
worked solutions in collapsed cells. This fork copies `../chapters/` instead.
Students should not be able to unfold the answer to tonight's homework.

## Three coupling hazards

**CNAME.** `build.sh` force-pushes `gh-pages`, so a CNAME committed to that
branch by hand is destroyed on the next build. It lives in `jb/extra/CNAME`
and reaches the site root via Sphinx `html_extra_path`.

**Colab badges.** These embed `github.com/USER/REPO/blob/...` and are
unaffected by the custom domain. They stay coupled to the repo name
permanently. Renaming the repo requires regenerating every badge in the same
commit, and Colab's fetcher does not reliably follow GitHub's redirect.

**JupyterLite.** Same force-push problem as CNAME, different shape: `build.sh`
now builds `../jupyterlite/content/` and `../jupyterlite/_output/` (see
`tools/build_jupyterlite_content.py`, `AUDIT.md` 2026-08-07/08) and copies the
result into `_build/html/jupyterlite-<hash>/` *before* `ghp-import` runs, so it
rides along in the same force-push instead of needing a separate one. If you
ever build and publish by hand outside `build.sh`, this subdirectory silently
vanishes on the next `ghp-import` unless you regenerate it the same way.
`porttack/learn` also embeds this repo's `gh-pages` branch as a git submodule
(serves at `learn.porttack.com/working-in-python/`); that submodule pins an
exact commit, so it does **not** pick up a new `gh-pages` push automatically
-- bump it deliberately with `git submodule update --remote working-in-python`
in that repo when you want the live copy to move forward.

**JupyterLite caching, and why the path is content-hashed.** GitHub Pages sets
`Cache-Control: max-age=600` on these files -- short, but not zero, and a
school network's own caching proxy is under no obligation to respect it as
faithfully as a browser would. JupyterLite also ships a service worker that
*can* cache aggressively, though it's off by default (confirmed by reading
the built `service-worker.js`: it only caches if the page URL includes
`?enableCache=true` -- never add that param to a student-facing link). Rather
than rely on every caching layer between here and a Chromebook getting cache
invalidation right, `jb/build.sh` deploys to `jupyterlite-<hash>/`, where the
hash comes from `tools/build_jupyterlite_content.py --print-deploy-id` -- a
SHA-256 of every file that affects what ships in `jupyterlite/content/`
(the notebooks, their vendored dependencies, and the build script itself).
This used to be a hand-maintained `jupyterlite/VERSION` counter that had to be
bumped manually before every content-changing republish, and separately kept
in sync with a few hardcoded copies of the version number inside the notebooks
themselves (see `AUDIT.md`, 2026-08-08 follow-ups 8-10 for the fallout when
that was forgotten, twice) -- replaced with the hash so there is nothing to
remember and nothing that can drift out of sync: **any** change to that
content changes the hash, automatically, every time. The tradeoff: since
`ghp-import` replaces the whole branch each publish, only the *current*
hash's directory exists on `gh-pages` after a publish -- a tab left open on
an old `jupyterlite-<hash>/` URL 404s on reload rather than silently running
stale content, which for a live classroom fallback is the failure mode you
want.

**Stable links for Schoology.** Posting a hashed URL directly into Schoology
means every republish breaks it -- there's no way to edit a hash into a link
that's already been handed to a class. `build.sh` also writes
`current/notebooks/index.html` and `current/lab/index.html`: tiny pages that
redirect (preserving the query string) to that run's real
`jupyterlite-<hash>/...` path. `ghp-import -f` replaces the whole branch each
publish, so these two files are always regenerated pointing at whatever just
shipped -- paste `https://python.porttack.com/current/notebooks/index.html?path=...`
into Schoology once and it never needs editing again. This does reopen a
sliver of the caching problem the hash exists to close: for up to the 600s
`Cache-Control` window after a republish, a cached `current/...` redirect
could still point at the *previous* hash, so a reload briefly runs the old
build instead of 404ing. Accepted deliberately -- a Schoology link that goes
stale for ten minutes beats one that's permanently dead.

The redirect target is a **relative** path (`../../<hash>/...`), not
root-absolute, on purpose: `porttack/learn` embeds this repo's `gh-pages`
branch as a submodule and serves it at `learn.porttack.com/working-in-python/`,
not the domain root (see the submodule coupling hazard above). A root-absolute
`/jupyterlite-<hash>/...` redirect resolves correctly on `python.porttack.com`
but 404s on `learn.porttack.com`, since it skips the `/working-in-python/`
prefix; a relative redirect resolves correctly under either mount point with
no site-specific configuration. Same submodule-pin caveat applies as
everywhere else on that mirror: `current/` there is only as current as the
last `git submodule update --remote working-in-python` in that repo, not
truly live.

## First deploy, in order

Each step fails independently, so verify each before starting the next.

1. `pip install jupyter-book ghp-import jupyterlite-core jupyterlite-pyodide-kernel jupyter-server`
2. Add the `.gitignore` entries above, commit.
3. `cd jb && ./build.sh`
4. Set Pages source to `gh-pages` / `/`. Confirm the default
   `*.github.io/working-in-python/` URL loads **with CSS**. Unstyled output
   means `.nojekyll` did not land.
5. DNS: `CNAME` record for `python` pointing at `[CONFIRM: user].github.io`.
   Set the custom domain in the Pages UI. Wait for HTTPS to provision before
   handing the URL to anyone; a certificate warning in week one is a bad first
   impression of the course.
6. Verify an internal cross-reference resolves. Chapter 10 links back to an
   earlier section; click it.
7. Verify `https://python.porttack.com/<hash>/notebooks/index.html?path=Chapter01-Welcome.ipynb`
   (get the current `<hash>` with `python3 tools/build_jupyterlite_content.py
   --print-deploy-id`, or read it off the last build's own printed output) loads and
   runs -- Colab-outage fallback, chapters 1-11 only, see `AUDIT.md`. Also verify
   `https://python.porttack.com/<hash>/lab/index.html` opens the full workbench with
   the file browser grouping notebooks ahead of helper files (`_start-here.ipynb` first,
   then each chapter's own notebook/teach-copy/exercises variants sorted together by
   name) -- this depends on the repo-root `overrides.json` (`sortNotebooksFirst`)
   reaching the build; see `AUDIT.md`, 2026-08-09 and 2026-08-16 (naming cleanup).
8. Verify `https://python.porttack.com/current/notebooks/index.html?path=Chapter01-Welcome.ipynb`
   redirects to the same hashed URL from step 7 and runs. This is the link to
   actually hand to students (Schoology, etc.) -- see "Stable links for
   Schoology" above.

## Later, not now

Move the build to a GitHub Action on push to `main`. Reason to wait: a local
build that fails is a build you notice. An Action that fails is a stale site
you find out about from a student. Do it once the chapter content stops
changing weekly.
