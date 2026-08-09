import os
import sys
from glob import glob

import nbformat as nbf

# chap01.ipynb and jupyter_intro.ipynb each embed a live JupyterLite iframe of
# themselves and carry this placeholder instead of a hardcoded deploy path
# (see tools/build_jupyterlite_content.py). build.sh/watch.sh compute the real
# id once (python3 ../tools/build_jupyterlite_content.py --print-deploy-id)
# and pass it in via this env var so both copies -- this one and the one
# inside jupyterlite/content/ -- end up pointing at the same path.
DEPLOY_PATH_PLACEHOLDER = 'JUPYTERLITE_DEPLOY_PATH'
DEPLOY_ID = os.environ.get('JUPYTERLITE_DEPLOY_ID')


def process_cell(cell):
    # get tags
    tags = cell['metadata'].get('tags', [])

    if DEPLOY_PATH_PLACEHOLDER in cell['source']:
        if not DEPLOY_ID:
            sys.exit(
                f"error: a cell contains {DEPLOY_PATH_PLACEHOLDER} but "
                "JUPYTERLITE_DEPLOY_ID is not set. Run via build.sh/watch.sh, "
                "or set it by hand: JUPYTERLITE_DEPLOY_ID=$(python3 "
                "../tools/build_jupyterlite_content.py --print-deploy-id)"
            )
        cell['source'] = cell['source'].replace(DEPLOY_PATH_PLACEHOLDER, DEPLOY_ID)

    # add hide-cell tag to solutions
    if cell['cell_type'] == 'code':
        source = cell['source']

        # remove solutions
        if source.startswith('# Solution') or 'solution' in tags:
            cell['source'] = []

        # remove %%expect cell magic
        if source.startswith('%%expect'):
            t = source.split('\n')[1:]
            cell['source'] = '\n'.join(t)

    # add reference label
    for tag in tags:
        if tag.startswith('chapter') or tag.startswith('section'):
            # print(tag)
            label = f'({tag})=\n'
            cell['source'] = label + cell['source']


def process_notebook(path):
    ntbk = nbf.read(path, nbf.NO_CONVERT)

    for cell in ntbk.cells:
        process_cell(cell)

    nbf.write(ntbk, path)


# Collect a list of the notebooks in the content folder. jupyter_intro.ipynb
# and index.ipynb don't match chap*.ipynb but need the same deploy-path
# substitution (index.ipynb links to the JupyterLite lab view).
paths = glob("chap*.ipynb") + glob("jupyter_intro.ipynb") + glob("index.ipynb")

for path in sorted(paths):
    print('prepping', path)
    process_notebook(path)
