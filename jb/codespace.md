# Using a Codespace

If Colab or JupyterLite is unreliable on a school network, or you'd rather work the way
real Python developers do -- in a terminal, with real files -- a GitHub Codespace is a
full computer running in your browser. It's free for the amount of use this class needs.

There are two ways to set one up. Either works. Pick one and stick with it for the
semester, rather than switching back and forth.

## The quick way: whatever's already there

If you already have a Codespace open for something else (cs50.dev, or any other class),
you can drop a chapter notebook straight into it -- no setup at all.

1. Download the chapter: click **Download** in the chapter's own link bar, or run this in
   the Codespace's terminal (swap in the actual chapter number):

   ```bash
   curl -L -o chapNN.ipynb https://raw.githubusercontent.com/porttack/working-in-python/v3/chapters/chapNN.ipynb
   ```

2. Open the file. The first time you run a cell, VS Code offers to install the Python and
   Jupyter extensions -- click **Install**, and pick the Python interpreter it offers.
3. If a cell fails with `ModuleNotFoundError: No module named 'matplotlib'` (or `yaml`),
   run `pip install matplotlib pyyaml` once in the terminal, then try again.

This is the fastest way to try one chapter. The tradeoff: it uses whatever Python is
already in that Codespace, shared with anything else you're doing there.

## Our way: a dedicated environment

This keeps this class's Python environment separate from anything else in the Codespace,
and avoids a couple of rough edges the quick way runs into (see below).

**Once, the first time:**

```bash
curl -L -o setup.sh https://raw.githubusercontent.com/porttack/working-in-python/v3/setup.sh
bash setup.sh
```

This creates a `wip/` folder with its own Python environment (`wip/.venv`) and installs
everything the chapters need. Safe to run again later -- it won't recreate an existing
environment.

**Each week, from inside `wip/`:**

```bash
curl -L -o chapNN.ipynb https://raw.githubusercontent.com/porttack/working-in-python/v3/chapters/chapNN.ipynb
```

(`python3 wip/fetch.py chapter-number` is also there if you'd rather not retype the URL --
run `fetch.py --help` to see it. It asks before overwriting a chapter you already have,
same as `cp` or `mv` would.)

Open the notebook, select **wip/.venv** as the kernel the first time, do the homework,
then use whichever of "Finished? Copy your work" or "OR save your homework for
submission" fits how you're turning it in.

### Want every chapter at once instead?

Two zip files are published, and both unzip straight into a ready-to-go `wip/` folder:

- [`wip-tools.zip`](wip-tools.zip) -- just the setup and fetch scripts, no chapters. Unzip
  it, run `setup.sh`, then fetch chapters one at a time as you go.
- [`wip.zip`](wip.zip) -- the same two scripts, plus every chapter that's ready right now.

The all-at-once zip is a snapshot, not a live copy. If a chapter gets fixed after you
download it, your copy doesn't update on its own -- if you're not sure yours is current,
re-fetch that one chapter (`python3 fetch.py chapter-number`, or plain `curl`) rather
than re-downloading the whole zip.
