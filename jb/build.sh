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
rm -f chap*.ipynb

cp ../chapters/chap[0-1][0-9].ipynb .

# NOT OPTIONAL. Besides blanking solution cells, this injects the
# (section_name)= MyST labels that every internal cross-reference in the book
# depends on, and strips %%expect magic that would otherwise render as visible
# junk. Skip it and the book builds fine with silently broken links.
python prep_notebooks.py

jb build .

# JupyterLite (chap01-11, Colab-outage fallback): built separately from
# ../jupyterlite/content/ and copied in as a subdirectory so it survives the
# ghp-import force-push below, which otherwise replaces the whole branch with
# just _build/html. See AUDIT.md, 2026-08-07/08.
(cd .. && python3 tools/build_jupyterlite_content.py && jupyter lite build --contents jupyterlite/content --output-dir jupyterlite/_output)
rm -rf _build/html/jupyterlite
cp -r ../jupyterlite/_output _build/html/jupyterlite

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
echo "  4. https://python.porttack.com/jupyterlite/notebooks/index.html?path=chap01.ipynb runs"
