# Publishing

How the website is built, and why it is built this way. Read this before
changing anything in `jb/`.

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

Non-optional. Without it, every build leaves twenty mutated notebooks in
`git status`, and the failure mode is committing solution-stripped copies over
the real chapters.

```gitignore
# Jupyter Book build artifacts
jb/chap*.ipynb
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
result into `_build/html/jupyterlite/` *before* `ghp-import` runs, so it rides
along in the same force-push instead of needing a separate one. If you ever
build and publish by hand outside `build.sh`, this subdirectory silently
vanishes on the next `ghp-import` unless you regenerate it the same way.
`porttack/learn` also embeds this repo's `gh-pages` branch as a git submodule
(serves at `learn.porttack.com/working-in-python/`); that submodule pins an
exact commit, so it does **not** pick up a new `gh-pages` push automatically
-- bump it deliberately with `git submodule update --remote working-in-python`
in that repo when you want the live copy to move forward.

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
7. Verify `https://python.porttack.com/jupyterlite/notebooks/index.html?path=chap01.ipynb`
   loads and runs (Colab-outage fallback, chapters 1-11 only -- see AUDIT.md).

## Later, not now

Move the build to a GitHub Action on push to `main`. Reason to wait: a local
build that fails is a build you notice. An Action that fails is a stale site
you find out about from a student. Do it once the chapter content stops
changing weekly.
