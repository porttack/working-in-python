# Future: moving publishing into GitHub Actions

Not built yet. This describes what `cd jb && ./build.sh` does today, by hand, on
whoever's laptop runs it, and what would need to change to run it as a GitHub
Action on push instead. Read `PUBLISHING.md` first for why the site is built the
way it is; this is only about *where* the build runs.

## Why not now

`build.sh` changed twice in the last few days (JupyterLite added, then the
version-bump automated) and the site's page structure changed under it (chap01's
split view, the sitewide resizer, the top navbar removal). None of that has
settled yet — automating a moving target just means debugging CI instead of a
local shell, with a slower feedback loop. Revisit once a week or two goes by
without a `build.sh`/`jb/_static/` change.

## What today's process actually requires, that CI would need too

Reading `jb/build.sh` top to bottom:

1. **A clean `../chapters/` tree.** The script refuses to run otherwise (see its
   own comment: the copies it makes get mutated by `prep_notebooks.py`, and a
   dirty source tree risks that mutation landing in a commit). In CI, a checkout
   is always clean, so this check is moot there — but it means CI must run
   `prep_notebooks.py`'s mutations only against a fresh checkout, never against
   a workspace something else in the same job already touched.
2. **Python packages**: `jupyter-book`, `ghp-import`, `jupyterlite-core`,
   `jupyterlite-pyodide-kernel`, `jupyter-server` (the same list `PUBLISHING.md`
   gives for a human's one-time setup).
3. **A real build**: `jb build .`, then `tools/build_jupyterlite_content.py` +
   `jupyter lite build`, then the copy into `_build/html/${JUPYTERLITE_DEPLOY_ID}`
   (see `HOW_TO_EDIT.md` — this part is now fully automatic, no version to pass
   in).
4. **Write access to push `gh-pages`.** `ghp-import -n -p -f` force-pushes. In
   CI this needs `permissions: contents: write` on the job (the built-in
   `GITHUB_TOKEN` is enough for this — same repo, same remote) and a configured
   git identity (`ghp-import` makes a real commit; CI needs `user.name`/
   `user.email` set, e.g. to `github-actions[bot]`).
5. **A human looking at the result before it's called done.** `build.sh --local`
   stops after step 3 specifically so someone can eyeball the output first. CI
   removes the human from the loop by construction — see the tradeoff below.

## The one real design decision: does a green push auto-publish?

Two shapes, not mutually exclusive:

- **CI as a gate, publish stays manual.** Every push to `v3` runs `make check` +
  a `build.sh --local`-equivalent as a required status check. Publishing is a
  separate, manually-triggered `workflow_dispatch` button in the Actions tab (or
  still done locally, same as today) — CI's job is only to catch a broken build
  before a human decides to publish it.
- **CI publishes automatically on push to `v3`.** Closer to what `build.sh`
  (no `--local`) already does when a human runs it today — nothing currently
  stops that from immediately going live either. The difference CI adds is
  *reproducibility* (same clean environment every time, not whatever state a
  laptop happens to be in) and a guaranteed `make check` gate before the force-push,
  which today is only a convention, not enforced.

Recommendation when this gets built: start with the first shape (gate, manual
publish button) for at least a few weeks of actually using it, since a bad push
going instantly live to a classroom site is a worse failure mode than a build
that has to wait for someone to click a button. Move to the second shape once
the workflow itself is trusted.

Either way: the workflow triggers on push to **`v3`**, not `main` — that's this
repo's actual default/production branch (`main` in `git remote show` terms may
still point at upstream conventions; check `git branch -vv` / the repo's GitHub
settings before assuming).

## Things this does NOT solve, and shouldn't try to

- **`porttack/learn`'s submodule pin.** `PUBLISHING.md` already documents that
  `learn.porttack.com` embeds this repo's `gh-pages` branch as a git submodule
  pinned to an exact commit, bumped by hand (`git submodule update --remote
  working-in-python`) in that other repo. A CI job here has no natural
  permission boundary to reach into a different repo and bump it — that would
  need a second workflow, in `porttack/learn`, with its own trigger (a
  `repository_dispatch` sent from this repo's workflow, or just a human doing it,
  same as today). Not blocking; just don't try to fold it into this repo's
  workflow.
- **DNS / HTTPS certificate provisioning.** One-time, already done, not a
  per-publish concern.
- **Caching the JupyterLite build across runs.** `jupyterlite-core` +
  `jupyterlite-pyodide-kernel` pull down a real Pyodide distribution; a cold CI
  runner will feel this every time. Worth an `actions/cache` step keyed on
  something like the installed package versions once this exists for real —
  not worth designing blind before there's an actual workflow file to attach it
  to.

## Rough shape of the workflow file, when it's time

Not written yet, on purpose — sketch only, so whoever builds this doesn't start
from nothing:

```yaml
# .github/workflows/publish.yml (sketch, not real)
on:
  push:
    branches: [v3]
  workflow_dispatch: {}   # if going with the gate-only shape, drop the publish
                          # step from the push trigger and only real-publish here

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install jupyter-book ghp-import jupyterlite-core jupyterlite-pyodide-kernel jupyter-server
      - run: python3 tools/build_jupyterlite_content.py --check
      - run: cd jb && ./build.sh --local
      # gate ends here for the gate-only shape; the rest is the publish job
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
      - run: cd jb && ./build.sh
```

`build.sh` itself needs no changes for this — it already refuses a dirty
`chapters/` tree (always true in CI) and already does the version-id/copy/publish
steps in order. The workflow's whole job is arranging *where* those same
commands run, not changing what they do.
