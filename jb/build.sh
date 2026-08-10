#!/usr/bin/env bash
#
# Build and publish the Working in Python website.
#
#   one-time:  pip install jupyter-book ghp-import jupyterlite-core \
#              jupyterlite-pyodide-kernel jupyter-server
#   build only: cd jb && ./build.sh --local
#   publish:    cd jb && ./build.sh
#
# --local builds into _build/html and stops. Use it for every check. The
# publish path force-pushes gh-pages and should be run by a human who has
# just looked at the local output.
#
# Differs from Downey's upstream build.sh in one important way: he copies from
# ../ThinkPythonSolutions/soln/, because his published site includes worked
# solutions in collapsed cells. This fork publishes ../chapters/ instead, which
# carry "# Solution goes here" placeholders. Students should not be able to
# unfold the answer to tonight's homework.

set -euo pipefail

# Refuse to build from a dirty chapters/ tree. The copies below are mutated in
# place by prep_notebooks.py, and the failure mode if you get confused about
# which is which is committing solution-stripped notebooks over the real ones.
if ! git diff --quiet -- ../chapters/; then
  echo "ERROR: ../chapters/ has uncommitted changes. Commit or stash first." >&2
  exit 1
fi

# Clear any copies left from a previous run so a deleted chapter cannot linger.
rm -f chap*.ipynb jupyter_intro.ipynb index.ipynb

cp ../chapters/chap[0-1][0-9].ipynb .
cp ../chapters/jupyter_intro.ipynb .
cp ../chapters/index.ipynb .

# chap01.ipynb and jupyter_intro.ipynb each embed a live JupyterLite iframe of
# themselves, and index.ipynb links to the JupyterLite lab view; all three
# carry a placeholder (JUPYTERLITE_DEPLOY_PATH) instead of a
# hardcoded deploy path. The id is a hash of everything that affects what
# ships in jupyterlite/content/ (see tools/build_jupyterlite_content.py), so
# it changes automatically whenever that content does -- nothing to bump by
# hand, and it can never collide with a previous, differently-built deploy.
# Computed once here and exported so prep_notebooks.py's substitution (below)
# and the JupyterLite build's own copy (further below) agree on the same id.
export JUPYTERLITE_DEPLOY_ID=$(cd .. && python3 tools/build_jupyterlite_content.py --print-deploy-id)

# NOT OPTIONAL. Besides blanking solution cells and substituting the deploy id
# above, this injects the (section_name)= MyST labels that every internal
# cross-reference in the book depends on, and strips %%expect magic that
# would otherwise render as visible junk. Skip it and the book builds fine
# with silently broken links.
python prep_notebooks.py

jb build .

# JupyterLite (chap01-11, Colab-outage fallback): built separately from
# ../jupyterlite/content/ and copied in as a subdirectory so it survives the
# ghp-import force-push below, which otherwise replaces the whole branch with
# just _build/html. See AUDIT.md, 2026-08-07/08.
#
# Deployed under $JUPYTERLITE_DEPLOY_ID (computed above), not a bare
# jupyterlite/, so a republish can never be masked by a stale cached copy in
# a student's browser or a school network's caching proxy -- a content change
# always lands at a URL nobody has ever fetched before, which no
# cache-control header or proxy policy can get wrong. See CLAUDE.md and
# PUBLISHING.md.
# Regenerated fresh first: build_jupyterlite_content.py reads projector/
# directly (for the projector-variant notebooks it ships alongside each
# regular chapter, see AUDIT.md 2026-08-08 follow-up 15), so a stale
# projector/ would ship stale content with no error to notice it by.
(cd .. && python3 tools/build_blanks.py --dst projector && python3 tools/build_jupyterlite_content.py && jupyter lite build --contents jupyterlite/content --output-dir jupyterlite/_output)
# Sphinx's own build only manages files it knows about, so a jupyterlite* dir
# from an older run lingers in _build/html across runs unless swept here.
# Without this, a stale one could ride along into the next ghp-import publish.
rm -rf _build/html/jupyterlite _build/html/jupyterlite-*
cp -r ../jupyterlite/_output "_build/html/${JUPYTERLITE_DEPLOY_ID}"

# Stable aliases so a link pasted once into Schoology survives every future
# rebuild: current/{notebooks,lab}/index.html just redirect to this run's
# $JUPYTERLITE_DEPLOY_ID, preserving the query string (?path=...). Since
# ghp-import force-pushes the whole branch, these two files are regenerated
# with the new hash on every publish -- nothing to re-edit in Schoology, ever.
mkdir -p _build/html/current/notebooks _build/html/current/lab
for view in notebooks lab; do
  cat > "_build/html/current/${view}/index.html" <<REDIRECT
<!doctype html>
<meta charset="utf-8">
<title>Redirecting to current build&hellip;</title>
<script>
  location.replace("/${JUPYTERLITE_DEPLOY_ID}/${view}/index.html" + location.search);
</script>
<p>Redirecting to the current build&hellip;
<a id="fallback" href="#">click here</a> if nothing happens.</p>
<script>
  document.getElementById("fallback").href =
    "/${JUPYTERLITE_DEPLOY_ID}/${view}/index.html" + location.search;
</script>
REDIRECT
done

if [[ "${1:-}" == "--local" ]]; then
  echo
  echo "Local build only. Output in jb/_build/html/index.html"
  echo "Nothing was published. Re-run without --local to deploy."
  exit 0
fi

# -n writes .nojekyll, which is what keeps GitHub Pages from stripping
# _static/ and destroying every stylesheet in the book. -f force-pushes, which
# is why CNAME must come from extra/ (see _config.yml) rather than being
# committed to the gh-pages branch by hand: a manual CNAME gets wiped here.
ghp-import -n -p -f _build/html

echo
echo "Published. Verify before telling anyone:"
echo "  1. https://python.porttack.com/ loads with CSS intact"
echo "  2. a chapter's Open in Colab badge actually opens"
echo "  3. an internal cross-reference resolves (chap10 -> earlier section)"
echo "  4. https://python.porttack.com/${JUPYTERLITE_DEPLOY_ID}/notebooks/index.html?path=__chap01-welcome.ipynb runs"
echo "  5. https://python.porttack.com/${JUPYTERLITE_DEPLOY_ID}/lab/index.html shows the grouped file browser"
echo "  6. https://python.porttack.com/current/notebooks/index.html?path=__chap01-welcome.ipynb redirects and runs"
