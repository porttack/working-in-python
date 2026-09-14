# Using an Existing Codespace

If Colab or JupyterLite is unreliable on a school network, or you'd rather work the way
real Python developers do -- in a terminal, with real files -- you can do your homework in
a GitHub Codespace: a full computer running in your browser. This page assumes you already
have one open (for CS50, or any other class) and walks through setting up this course's own
environment inside it.

**Once, the first time:**

1. Start your Codespace. If you're using CS50's, just go to
   [https://cs50.dev](https://cs50.dev) -- don't create or switch to a different folder,
   just use the one it opens you into.

2. Download the tools, unzip them, and move into the new folder:

   ```bash
   wget https://python.porttack.com/wip-tools.zip
   unzip wip-tools.zip
   cd wip
   ```

3. Create a virtual environment -- your own private copy of Python for this class, kept
   separate from anything else in the Codespace -- and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the packages the chapters need:

   ```bash
   pip install ipykernel matplotlib pyyaml notebook
   ```

**Each week, from inside `wip/`** (activate the environment again first if you closed the
terminal: `source .venv/bin/activate`):

5. Download the chapter you're working on (swap in the actual chapter number):

   ```bash
   wget https://raw.githubusercontent.com/porttack/working-in-python/v3/chapters/chapNN.ipynb
   ```

   (`python3 fetch.py chapter-number` also works, if you'd rather not retype the URL --
   run `fetch.py --help` to see it. It asks before overwriting a chapter you already have,
   same as `cp` or `mv` would.)

6. Open it:

   ```bash
   code chapNN.ipynb
   ```

   The first time, VS Code offers to install the Python and Jupyter extensions -- click
   **Install**. Then select **wip/.venv** as the kernel.

Do the homework, then use whichever of "Finished? Copy your work" or "OR save your homework
for submission" fits how you're turning it in.

### Want every chapter at once instead?

Two zip files are published, and both unzip straight into a ready-to-go `wip/` folder:

- [`wip-tools.zip`](wip-tools.zip) -- just `setup.sh`, `fetch.py`, and `requirements.txt`,
  no chapters. Unzip it, then follow steps 3-4 above (or run `bash setup.sh`, which sets up
  the same environment for you -- it installs from `requirements.txt`, pinned exact
  versions, rather than typing package names by hand), and fetch chapters one at a time as
  you go.
- [`wip.zip`](wip.zip) -- the same files, plus every chapter that's ready right now.

The all-at-once zip is a snapshot, not a live copy. If a chapter gets fixed after you
download it, your copy doesn't update on its own -- if you're not sure yours is current,
re-fetch that one chapter (`python3 fetch.py chapter-number`, or the `wget` command above)
rather than re-downloading the whole zip.
