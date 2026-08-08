"""Optional ASCII-art packages for JupyterLite, installed on demand.

Not part of any chapter's exercises -- available for a student who wants to
try pyfiglet, art, cowsay, or ascii_magic on their own. None of these are in
Pyodide's own curated package set, so a bare `import pyfiglet` fails with
ModuleNotFoundError; piplite.install() is required first. Outside Pyodide
(Colab, Codespaces, a real Jupyter install) this module doesn't apply --
`pip install pyfiglet` (etc.) the normal way instead.

    import ascii_art
    await ascii_art.use('pyfiglet')
    import pyfiglet
    print(pyfiglet.figlet_format('Hi'))
"""
import sys

PACKAGES = ("pyfiglet", "art", "cowsay", "ascii_magic")


async def use(*names):
    if "pyodide" not in sys.modules:
        raise RuntimeError(
            "ascii_art.use() is for JupyterLite only -- outside it, "
            "pip install " + " ".join(names or PACKAGES)
        )
    import piplite

    for name in names or PACKAGES:
        await piplite.install(name)
