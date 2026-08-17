import contextlib
import io
import json
import re


# ANSI escape codes for colored/formatted print() output. These work in a
# real terminal and in JupyterLite's output renderer without installing
# anything (no pip install needed, unlike colorama).
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"


def colored(text, color, bold=False):
    """Wrap text in ANSI codes so it prints in the given color.

    text: string
    color: one of the color constants above, e.g. RED
    bold: boolean

    returns: string
    """
    style = BOLD + color if bold else color
    return f"{style}{text}{RESET}"


def extract_function_name(text):
    """Find a function definition and return its name.

    text: String

    returns: String or None
    """
    pattern = r"def\s+(\w+)\s*\("
    match = re.search(pattern, text)
    if match:
        func_name = match.group(1)
        return func_name
    else:
        return None


# the functions that define cell magic commands are only defined
# if we're running in Jupyter.

try:
    from IPython.core.magic import register_cell_magic
    from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

    @register_cell_magic
    def add_method_to(args, cell):

        # get the name of the function defined in this cell
        func_name = extract_function_name(cell)
        if func_name is None:
            return f"This cell doesn't define any new functions."

        # get the class we're adding it to
        namespace = get_ipython().user_ns
        class_name = args
        cls = namespace.get(class_name, None)
        if cls is None:
            return f"Class '{class_name}' not found."

        # save the old version of the function if it was already defined
        old_func = namespace.get(func_name, None)
        if old_func is not None:
            del namespace[func_name]

        # Execute the cell to define the function
        get_ipython().run_cell(cell)

        # get the newly defined function
        new_func = namespace.get(func_name, None)
        if new_func is None:
            return f"This cell didn't define {func_name}."

        # add the function to the class and remove it from the namespace
        setattr(cls, func_name, new_func)
        del namespace[func_name]

        # restore the old function to the namespace
        if old_func is not None:
            namespace[func_name] = old_func

    @register_cell_magic
    def expect_error(line, cell):
        try:
            get_ipython().run_cell(cell)
        except Exception as e:
            get_ipython().run_cell("%tb")

    @magic_arguments()
    @argument("exception", help="Type of exception to catch")
    @register_cell_magic
    def expect(line, cell):
        args = parse_argstring(expect, line)
        exception = eval(args.exception)
        try:
            get_ipython().run_cell(cell)
        except exception as e:
            get_ipython().run_cell("%tb")

    def traceback(mode):
        """Set the traceback mode.

        mode: string
        """
        with contextlib.redirect_stdout(io.StringIO()):
            get_ipython().run_cell(f"%xmode {mode}")

    traceback("Minimal")
except (ImportError, NameError):
    print("Warning: IPython is not available, cell magic not defined.")


# "Copy Notebook" button, rendered as plain cell output -- the same basic
# mechanism as displaying an image or any other rich output, deliberately
# chosen after a floating, document.body-injected version rendered nothing
# (unconfirmed why; not worth chasing further when this is simpler and has
# fewer ways to fail -- confirmed working). Automates a gesture already
# confirmed to work by hand: selecting with the mouse from the first cell
# through the last, then copying, pastes into a document correctly --
# images included -- whereas Jupyter's own Ctrl+A/copy produces an internal
# clipboard format that doesn't. The selection is the painful part for a
# student to do by hand, not the copy itself, so that's what this automates.
#
# `position: sticky` (not `fixed`) keeps it pinned to the top of the
# notebook's own scrolling area as a student scrolls through a long
# notebook, without needing document.body injection (the thing that didn't
# render) or touching every notebook file individually.
#
# A real toolbar/menu entry would be nicer. Two routes there were tried and
# both failed: `ipylab` registers commands cleanly, but only its JS half is
# vendored in this build -- its Python package isn't in the offline pip
# index, so `import ipylab` fails with no network available (confirmed: not
# present in the piplite index). `window.jupyterapp` would work without
# ipylab, but JupyterLite only exposes it via a build flag with a known,
# unresolved bug making it unreliable through the normal config path
# (jupyterlite/jupyterlite#681). Sticky positioning covers most of the same
# practical need (always visible without hunting for it) at far lower risk;
# revisit a real toolbar entry only if that turns out not to be enough.
#
# Execution-count prompts ("In [1]:") are excluded from selection by
# JupyterLab itself -- `.jp-InputPrompt`/`.jp-OutputPrompt` both carry a
# deliberate `user-select: none` (confirmed by reading the actual CSS
# shipped in the build; the comment right above the rule literally says
# "Disable text selection"), so no amount of Range/Selection manipulation
# picks them up. Worked around by toggling `user-select` back to `text` on
# just those elements for the moment of copying, then reverting it.
#
# Code cells pasted into Google Docs showed exaggerated (~triple) line
# spacing, confirmed by the user as *between individual lines within a cell*,
# not between cells. Not reproducible from here -- only shows up after Google
# Docs' own paste-from-web handling, not in the JupyterLite view itself.
# CodeMirror 6 renders each code line as its own `.cm-line` block div
# (`display: block`, confirmed in the built CSS); a first attempt just forced
# `margin: 0; line-height: normal` on each one, which the user confirmed did
# NOT fully fix it. Most likely explanation: Google Docs treats each
# block-level element in pasted HTML as its own paragraph and applies its own
# default paragraph spacing, regardless of the source's inline margin/
# line-height -- tweaking those values on a still-block-level element doesn't
# stop Docs from treating it as a paragraph in the first place. Second
# attempt, still in place: temporarily switch every `.cm-line` from
# `display: block` to `display: inline` and insert a real `<br>` after each
# one, for the moment of copying only -- this changes the DOM shape itself
# (one continuous inline flow with explicit soft line breaks) rather than
# just styling still-separate blocks, which should read as ONE paragraph with
# line breaks to Google Docs instead of N paragraphs. Deliberately keeps each
# line's syntax-highlighting spans intact (doesn't replace their content),
# only changes how the lines are laid out relative to each other. Still
# unverified whether this fully fixes the symptom -- flagged for the user to
# re-test live again.
#
# Known limitation: cells scrolled out of view may not be attached to the
# DOM at all (JupyterLab's own cell virtualization -- separate from
# anything in this file). If a long notebook copies incomplete, scroll all
# the way through it once first so every cell has been mounted, then click
# the button.
#
# A function, not a bare display() call, so a second copy can be dropped at
# the end of a notebook (e.g. chap0N-exercises.ipynb, right after the last
# exercise, which is where it's actually needed) with one line, in addition
# to the one that shows automatically on import.
#
# Only meaningful inside JupyterLite -- no-op on Colab or a local install,
# where IPython's rich display isn't hooked up the same way.

try:
    from IPython.display import HTML, display

    def show_copy_notebook_button():
        """Display a button that copies the whole notebook for pasting elsewhere."""
        display(HTML("""
<div style="position: sticky; top: 0; z-index: 10;
            background: var(--jp-layout-color0, white);
            padding: 6px 0; display: flex; align-items: center; gap: 8px;">
  <button
    onclick="
      var nb = document.querySelector('.jp-Notebook');
      if (!nb) { alert('Could not find the notebook.'); return; }
      var prompts = nb.querySelectorAll('.jp-InputPrompt, .jp-OutputPrompt');
      prompts.forEach(function (p) {
        p.style.userSelect = 'text';
        p.style.webkitUserSelect = 'text';
      });
      var codeLines = nb.querySelectorAll('.cm-line');
      var insertedBreaks = [];
      codeLines.forEach(function (l) {
        l.style.margin = '0';
        l.style.lineHeight = 'normal';
        l.style.display = 'inline';
        var br = document.createElement('br');
        l.insertAdjacentElement('afterend', br);
        insertedBreaks.push(br);
      });
      var sel = window.getSelection();
      sel.removeAllRanges();
      var range = document.createRange();
      range.selectNodeContents(nb);
      sel.addRange(range);
      document.execCommand('copy');
      sel.removeAllRanges();
      prompts.forEach(function (p) {
        p.style.userSelect = '';
        p.style.webkitUserSelect = '';
      });
      insertedBreaks.forEach(function (br) { br.remove(); });
      codeLines.forEach(function (l) {
        l.style.margin = '';
        l.style.lineHeight = '';
        l.style.display = '';
      });
      var b = this;
      var original = b.textContent;
      b.textContent = 'Copied! Now paste (Ctrl+V) into a document.';
      setTimeout(function () { b.textContent = original; }, 2000);
    "
    style="padding:8px 16px; background:#2196F3; color:white; border:none;
           border-radius:4px; font-size:14px; cursor:pointer;"
  >Copy Notebook</button>
  <span style="font-size:12px; color:#666;">
    Paste into a document. Long notebook? Scroll all the way through it
    once first so every cell has loaded.
  </span>
</div>
"""))

    show_copy_notebook_button()
except ImportError:
    pass


def enable_docstring_reminders():
    """Warn, without blocking, when a cell defines a function with no docstring.

    Meant for exercises notebooks in chapters where docstrings have already
    been taught (chapter 4 on) -- call this once, early, and it checks every
    cell run for the rest of the session. Checks only the function(s)
    actually defined in the cell that just ran (via `ast`, on that cell's own
    source), not the whole notebook's history or the live namespace, so
    re-running earlier cells doesn't re-trigger it and unrelated code isn't
    flagged.
    """
    import ast

    def _check(result):
        try:
            tree = ast.parse(result.info.raw_cell)
        except SyntaxError:
            return
        missing = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and ast.get_docstring(node) is None
        ]
        if missing:
            names = ", ".join(f"`{name}`" for name in missing)
            from IPython.display import HTML, display

            display(HTML(
                '<div style="color:#a94442; background:#f2dede; '
                'border:1px solid #ebccd1; padding:6px 10px; '
                'border-radius:4px; font-size:13px; margin-top:4px;">'
                f"⚠️ Missing docstring: {names}. Every function "
                "needs one (see Chapter 4)."
                "</div>"
            ))

    ip = get_ipython()
    if ip is not None:
        ip.events.register("post_run_cell", _check)


def time_check(chapter=0, exercises=0, longest=""):
    """Print a summary of time spent on this chapter.

    chapter: whole minutes spent reading the chapter and its practice exercises
    exercises: whole minutes spent on the numbered extra exercises
    longest: string naming which exercise took longest, e.g. "Exercise 1"
    """

    def fmt(minutes):
        hours, remainder = divmod(minutes, 60)
        return f"{hours}h{remainder:02d}m" if hours else f"{remainder}m"

    total = chapter + exercises
    print(f"Chapter time: {fmt(chapter)}")
    print(f"Exercise time: {fmt(exercises)}")
    print(f"Total: {fmt(total)}")
    if longest:
        print(f"Longest: {longest}")


def check_for_update(version, filename):
    """Show a banner if a newer build of this notebook has been published.

    version: this build's deploy id -- pass the literal string
        "JUPYTERLITE_DEPLOY_PATH"; tools/build_jupyterlite_content.py
        substitutes the real value in only the built copy, same as it
        already does for the embedded JupyterLite iframe links. Never edit
        chapters/*.ipynb to hardcode a real value here.
    filename: this notebook's own filename as served under files/, e.g.
        "chapter04-functions-and-interfaces.ipynb"

    Fetches the currently-served copy of this same file straight from the
    server (bypassing JupyterLite's own browser storage, which is what
    normally makes a stale copy invisible to a plain reload) and compares it
    against `version`. Does nothing automatically -- only offers a button.

    No-op if the placeholder was never substituted (Colab, a plain local
    install, or `chapters/` opened directly, none of which go through the
    JupyterLite build) or if there's no JupyterLite notebook DOM to attach
    the banner to.
    """
    try:
        from IPython.display import HTML, display
    except ImportError:
        return

    display(HTML(f"""
<script>
(function () {{
  var version = {json.dumps(version)};
  var filename = {json.dumps(filename)};
  console.log('[check_for_update] running, version=', version, 'filename=', filename);
  if (version.indexOf('JUPYTERLITE_DEPLOY_PATH') !== -1) {{
    console.log('[check_for_update] placeholder never substituted, skipping');
    return;
  }}
  var nb = document.querySelector('.jp-Notebook');
  if (!nb) {{
    console.log('[check_for_update] no .jp-Notebook found, skipping');
    return;
  }}
  var url = new URL('../files/' + filename, location.href);
  console.log('[check_for_update] fetching', url.href);
  fetch(url, {{cache: 'no-store'}})
    .then(function (r) {{
      console.log('[check_for_update] fetch status', r.status);
      return r.text();
    }})
    .then(function (text) {{
      var found = text.indexOf(version) !== -1;
      console.log('[check_for_update] served copy contains my version?', found,
        '(fetched length', text.length, ')');
      if (found) return;
      console.log('[check_for_update] mismatch -- showing banner');
      var bar = document.createElement('div');
      bar.style.cssText = 'position: sticky; top: 0; z-index: 20; ' +
        'background: #fff3cd; border-bottom: 2px solid #ffca2c; ' +
        'padding: 8px 12px; font-size: 13px; display: flex; ' +
        'align-items: center; gap: 10px; color: #664d03;';
      bar.innerHTML = 'A newer version of this chapter has been published. ' +
        'Reloading may not always pick it up -- if the page still looks the ' +
        'same after reloading, tell your teacher. ' +
        '<button style="padding:4px 10px;cursor:pointer;">Reload</button>';
      bar.querySelector('button').onclick = function () {{ location.reload(); }};
      if (nb.parentElement) {{
        nb.parentElement.insertBefore(bar, nb);
      }} else {{
        document.body.insertBefore(bar, document.body.firstChild);
      }}
    }})
    .catch(function (err) {{ console.log('[check_for_update] fetch failed', err); }});
}})();
</script>
"""))
